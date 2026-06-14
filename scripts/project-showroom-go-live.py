#!/usr/bin/env python3
"""Run the safe project-showroom go-live sequence.

This orchestrates the existing read-only and write helpers in the only order
that is safe for a public 3D project showroom:

1. prove the required plugin stack is merged/deployed,
2. prove local and remote model/material assets are valid,
3. dry-run or apply the REST CMS payload,
4. after an apply, run the live finish-line browser gate.

It never merges, deploys, clears cache or writes without ``--apply``. The owner
or operator still has to pull/sync the UPress server Git copy and update the
WordPress plugin before this can pass.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://nad-lan.co.il"
DEFAULT_PROJECT_SLUG = "rainbow-tel-aviv"
DEFAULT_POST_ID = 4464
DEFAULT_ASSET_BRANCH = "origin/codex/rainbow-prototype-model-1631"
DEFAULT_SCREENSHOT_OUT = "docs/qa/screenshots-rainbow-finish-line"


def endpoint(base_url: str, path: str) -> str:
    return urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def run_step(name: str, command: list[str]) -> int:
    print(f"\n## {name}", flush=True)
    print(" ".join(command), flush=True)
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode == 0:
        print(f"PASS: {name}", flush=True)
    else:
        print(f"STOP: {name} exited {result.returncode}", flush=True)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--project-slug", default=DEFAULT_PROJECT_SLUG)
    parser.add_argument("--post-id", type=int, default=DEFAULT_POST_ID)
    parser.add_argument("--branch", default="main", help="GitHub ref for raw model/material URLs.")
    parser.add_argument(
        "--asset-branch",
        default=DEFAULT_ASSET_BRANCH,
        help="Remote feature branch that carries the project asset package for merge-state checks.",
    )
    parser.add_argument("--out", default=DEFAULT_SCREENSHOT_OUT)
    parser.add_argument("--apply", action="store_true", help="Write the CMS payload after all preflights pass.")
    parser.add_argument("--wait-ready", action="store_true", help="Poll healthcheck before apply.")
    parser.add_argument("--wait-timeout", type=int, default=900)
    parser.add_argument("--poll-seconds", type=int, default=20)
    parser.add_argument("--skip-browser", action="store_true", help="Skip the final live browser gate after apply.")
    parser.add_argument(
        "--expect-incomplete",
        action="store_true",
        help="Exit 0 only when the deploy-sequence gate detects the current live stack is incomplete.",
    )
    args = parser.parse_args()

    deploy_cmd = [
        sys.executable,
        "scripts/check-rainbow-deploy-sequence.py",
        "--base-url",
        args.base_url,
        "--project-slug",
        args.project_slug,
        "--asset-branch",
        args.asset_branch,
        "--fetch",
    ]
    if args.expect_incomplete:
        deploy_cmd.append("--expect-incomplete")
        code = run_step("Deploy sequence negative-control gate", deploy_cmd)
        if code == 0:
            print(
                "\nExpected incomplete state detected. Stop here until the stack is merged, "
                "the UPress server Git copy is pulled/synced, the plugin is updated and cache is cleared.",
                flush=True,
            )
        return code

    code = run_step("Deploy sequence preflight", deploy_cmd)
    if code != 0:
        print(
            "\nStop: merge/deploy the missing stack first. Do not apply the CMS payload to an old live plugin.",
            flush=True,
        )
        return code

    readiness_cmd = [
        sys.executable,
        "scripts/check-rainbow-showroom-readiness.py",
        "--project-slug",
        args.project_slug,
        "--require-plugin-stack",
        "--check-remote-assets",
        "--healthcheck-url",
        endpoint(args.base_url, "/wp-json/nadlan/v1/healthcheck"),
    ]
    if args.branch != "main":
        readiness_cmd.extend(["--remote-ref", args.branch])
    code = run_step("Asset and CMS payload readiness", readiness_cmd)
    if code != 0:
        print("\nStop: fix the asset/CMS payload before writing WordPress meta.", flush=True)
        return code

    apply_cmd = [
        sys.executable,
        "scripts/apply-rainbow-cms-payload.py",
        "--project-slug",
        args.project_slug,
        "--post-id",
        str(args.post_id),
        "--base-url",
        args.base_url,
        "--branch",
        args.branch,
    ]
    if args.apply:
        apply_cmd.append("--apply")
        if args.wait_ready:
            apply_cmd.extend(["--wait-ready", "--wait-timeout", str(args.wait_timeout), "--poll-seconds", str(args.poll_seconds)])

    code = run_step("CMS payload dry-run" if not args.apply else "CMS payload REST apply", apply_cmd)
    if code != 0:
        print("\nStop: CMS payload was not safely applied.", flush=True)
        return code
    if not args.apply:
        print(
            "\nDry run complete. Re-run with --apply only after WordPress credentials are available "
            "and the owner is ready to wire the live project card.",
            flush=True,
        )
        return 0

    finish_cmd = [
        sys.executable,
        "scripts/check-rainbow-finish-line.py",
        "--base-url",
        args.base_url,
        "--project-slug",
        args.project_slug,
        "--post-id",
        str(args.post_id),
        "--out",
        args.out,
    ]
    if args.skip_browser:
        finish_cmd.append("--skip-browser")
    code = run_step("Post-apply finish-line gate", finish_cmd)
    if code != 0:
        print("\nStop: CMS was written, but the live showroom did not pass the finish-line gate.", flush=True)
        return code

    print("\nPASS: project showroom go-live sequence passed.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
