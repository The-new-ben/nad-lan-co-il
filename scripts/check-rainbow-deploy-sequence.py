#!/usr/bin/env python3
"""Report the exact deploy sequence state for the Rainbow showroom stack.

This is a read-only coordination gate. It answers the practical question:
"What still has to merge/deploy before the GLB CMS payload can be applied?"
"""

from __future__ import annotations

import argparse
import json
import subprocess
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://nad-lan.co.il"
REQUIRED_VERSION = (1, 63, 4)
STACK_BRANCHES = [
    ("1.63.2", "origin/codex/rainbow-cms-units-rest-1632", "project_3d.unit_meta_rest"),
    ("1.63.3", "origin/codex/rainbow-mobile-contact-polish-1633", "project_3d.floating_action_rail_v1633"),
    ("1.63.4", "origin/codex/rainbow-page-seo-1634", "project_page_assembly.rainbow_seo_v1634"),
    ("GLB assets", "origin/codex/rainbow-prototype-model-1631", "project_3d.projects_with_glb >= 1 after CMS apply"),
]


@dataclass
class Row:
    status: str
    name: str
    detail: str


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def version_tuple(value: object) -> tuple[int, ...]:
    parts: list[int] = []
    for part in str(value or "").split("."):
        if not part.isdigit():
            break
        parts.append(int(part))
    return tuple(parts)


def endpoint(base_url: str, path: str) -> str:
    return urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def fetch_health(base_url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        endpoint(base_url, "/wp-json/nadlan/v1/healthcheck"),
        headers={"User-Agent": "Codex-Rainbow-Deploy-Sequence/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected healthcheck response")
    return data


def git_ref(ref: str) -> str:
    result = run_git(["rev-parse", "--verify", ref])
    return result.stdout.strip() if result.returncode == 0 else ""


def is_ancestor(ancestor: str, descendant: str) -> bool:
    if not git_ref(ancestor) or not git_ref(descendant):
        return False
    result = run_git(["merge-base", "--is-ancestor", ancestor, descendant])
    return result.returncode == 0


def status_rows(base_url: str, should_fetch: bool) -> list[Row]:
    rows: list[Row] = []
    if should_fetch:
        result = run_git(["fetch", "origin", "main", "--prune"])
        detail = result.stderr.strip() or result.stdout.strip() or "ok"
        rows.append(Row("PASS" if result.returncode == 0 else "FAIL", "git fetch origin main", detail))

    main_sha = git_ref("origin/main")
    rows.append(Row("PASS" if main_sha else "FAIL", "origin/main", main_sha[:12] if main_sha else "missing"))

    for label, branch, marker in STACK_BRANCHES:
        sha = git_ref(branch)
        if not sha:
            rows.append(Row("FAIL", f"{label} branch", f"{branch} missing locally; run git fetch --all"))
            continue
        merged = is_ancestor(branch, "origin/main")
        rows.append(
            Row(
                "PASS" if merged else "BLOCKED",
                f"{label} merged to main",
                f"{branch}@{sha[:12]} {'is on main' if merged else 'is not on main'}; marker {marker}",
            )
        )

    try:
        health = fetch_health(base_url)
    except Exception as exc:  # noqa: BLE001 - coordination gate should report reachable failures.
        rows.append(Row("FAIL", "live healthcheck", str(exc)))
        return rows

    version = str(health.get("version", ""))
    project_3d = health.get("project_3d", {}) if isinstance(health.get("project_3d"), dict) else {}
    assembly = health.get("project_page_assembly", {}) if isinstance(health.get("project_page_assembly"), dict) else {}
    rows.append(
        Row(
            "PASS" if version_tuple(version) >= REQUIRED_VERSION else "BLOCKED",
            "live plugin version",
            f"{version or 'unknown'}; required >= 1.63.4 before GLB apply",
        )
    )
    live_checks = [
        ("project_3d.model_viewer_ready", project_3d.get("model_viewer_ready") is True, project_3d.get("model_viewer_ready")),
        ("project_3d.unit_meta_rest", project_3d.get("unit_meta_rest") is True, project_3d.get("unit_meta_rest")),
        (
            "project_3d.floating_action_rail_v1633",
            project_3d.get("floating_action_rail_v1633") is True,
            project_3d.get("floating_action_rail_v1633"),
        ),
        (
            "project_page_assembly.rainbow_seo_v1634",
            assembly.get("rainbow_seo_v1634") is True,
            assembly.get("rainbow_seo_v1634"),
        ),
        (
            "project_3d.projects_with_glb",
            isinstance(project_3d.get("projects_with_glb"), int) and project_3d.get("projects_with_glb") >= 1,
            project_3d.get("projects_with_glb"),
        ),
    ]
    for name, ok, value in live_checks:
        rows.append(Row("PASS" if ok else "BLOCKED", name, f"{value!r}"))
    return rows


def print_rows(rows: list[Row]) -> None:
    print("# Rainbow deploy sequence status")
    print()
    for row in rows:
        print(f"[{row.status}] {row.name}: {row.detail}")
    print()
    print("Required owner/deploy order after merges:")
    print("1. Merge/deploy plugin stack through 1.63.4.")
    print("2. Pull/sync UPress server Git and update/upload the NadLan Config plugin.")
    print("3. Clear cache and confirm healthcheck markers are true.")
    print("4. Apply the Rainbow CMS payload.")
    print("5. Run `python scripts\\check-rainbow-finish-line.py`.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--fetch", action="store_true", help="Fetch origin/main before checking local remote refs.")
    parser.add_argument(
        "--expect-incomplete",
        action="store_true",
        help="Exit 0 when blockers are detected. Useful for proving the checker catches the current incomplete live state.",
    )
    args = parser.parse_args()

    rows = status_rows(args.base_url, args.fetch)
    print_rows(rows)
    blocked = any(row.status in {"FAIL", "BLOCKED"} for row in rows)
    if args.expect_incomplete:
        return 0 if blocked else 2
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
