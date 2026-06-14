#!/usr/bin/env python3
"""Run the Rainbow showroom finish-line gate.

This is the final, post-deploy proof command. It intentionally combines the
page assembly/SEO gate, the model/CMS readiness gate and the real browser DOM
gate, because the showroom is only done when all three pass together.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://nad-lan.co.il"
DEFAULT_PROJECT_SLUG = "rainbow-tel-aviv"
DEFAULT_POST_ID = 4464
DEFAULT_SCREENSHOT_OUT = "docs/qa/screenshots-rainbow-finish-line"
REQUIRED_VERSION = (1, 63, 4)


def endpoint(base_url: str, path: str) -> str:
    return urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "Codex-Rainbow-Finish-Line/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = json.loads(response.read().decode("utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected JSON response")
    return data


def version_tuple(value: object) -> tuple[int, ...]:
    parts: list[int] = []
    for part in str(value or "").split("."):
        if not part.isdigit():
            break
        parts.append(int(part))
    return tuple(parts)


def run_step(name: str, command: list[str]) -> bool:
    print(f"\n## {name}", flush=True)
    print(" ".join(command), flush=True)
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode == 0:
        print(f"PASS: {name}", flush=True)
        return True
    print(f"FAIL: {name} exited {result.returncode}", flush=True)
    return False


def check_health(base_url: str) -> bool:
    print("\n## Live health preflight", flush=True)
    health = fetch_json(endpoint(base_url, "/wp-json/nadlan/v1/healthcheck"))
    project_3d = health.get("project_3d", {})
    assembly = health.get("project_page_assembly", {})
    if not isinstance(project_3d, dict):
        project_3d = {}
    if not isinstance(assembly, dict):
        assembly = {}

    rows = {
        "version": health.get("version"),
        "model_viewer_ready": project_3d.get("model_viewer_ready"),
        "unit_meta_rest": project_3d.get("unit_meta_rest"),
        "floating_action_rail_v1633": project_3d.get("floating_action_rail_v1633"),
        "rainbow_seo_v1634": assembly.get("rainbow_seo_v1634"),
        "projects_with_glb": project_3d.get("projects_with_glb"),
    }
    print(json.dumps(rows, ensure_ascii=False, indent=2), flush=True)

    errors: list[str] = []
    if version_tuple(rows["version"]) < REQUIRED_VERSION:
        errors.append(f"version {rows['version'] or 'unknown'} < 1.63.4")
    for key in ("model_viewer_ready", "unit_meta_rest", "floating_action_rail_v1633", "rainbow_seo_v1634"):
        if rows.get(key) is not True:
            errors.append(f"{key} is not true")
    if not isinstance(rows.get("projects_with_glb"), int) or int(rows["projects_with_glb"]) < 1:
        errors.append(f"projects_with_glb is {rows.get('projects_with_glb')}, expected >= 1")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", flush=True)
        return False
    print("PASS: live health preflight", flush=True)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--project-slug", default=DEFAULT_PROJECT_SLUG)
    parser.add_argument("--post-id", type=int, default=DEFAULT_POST_ID)
    parser.add_argument("--out", default=DEFAULT_SCREENSHOT_OUT)
    parser.add_argument("--skip-browser", action="store_true", help="Skip the Chrome/Edge DOM screenshot gate.")
    args = parser.parse_args()

    all_passed = True
    try:
        all_passed = check_health(args.base_url) and all_passed
    except Exception as exc:  # noqa: BLE001 - finish-line gate should report all reachable failures.
        print(f"FAIL: live health preflight could not run: {exc}", flush=True)
        all_passed = False

    all_passed = run_step(
        "Page assembly and SEO strict gate",
        [
            sys.executable,
            "scripts/check-rainbow-page-assembly.py",
            "--base-url",
            args.base_url,
            "--project-slug",
            args.project_slug,
            "--post-id",
            str(args.post_id),
            "--strict",
        ],
    ) and all_passed

    all_passed = run_step(
        "Showroom asset and live GLB readiness gate",
        [
            sys.executable,
            "scripts/check-rainbow-showroom-readiness.py",
            "--project-slug",
            args.project_slug,
            "--require-plugin-stack",
            "--expect-live-glb",
            "--healthcheck-url",
            endpoint(args.base_url, "/wp-json/nadlan/v1/healthcheck"),
        ],
    ) and all_passed

    if not args.skip_browser:
        all_passed = run_step(
            "Live browser DOM gate",
            [
                "node",
                "scripts/check-rainbow-live-dom.mjs",
                "--url",
                endpoint(args.base_url, f"/projects/{args.project_slug}/"),
                "--out",
                args.out,
                "--expect-glb",
            ],
        ) and all_passed
    else:
        print("\n## Live browser DOM gate", flush=True)
        print("SKIPPED by --skip-browser", flush=True)

    print("\n## Finish-line result", flush=True)
    if all_passed:
        print("PASS: Rainbow showroom finish-line gate passed.", flush=True)
        return 0
    print("FAIL: Rainbow showroom is not finish-line ready yet.", flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
