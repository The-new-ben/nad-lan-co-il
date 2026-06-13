#!/usr/bin/env python3
"""Print the CMS payload for wiring Rainbow's prototype GLB after PR merge.

This script is intentionally read-only. It does not call WordPress and does not
write live metadata. Use it to copy reviewed values into the Studio/admin flow.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "assets" / "projects" / "rainbow-tel-aviv" / "project-meta-example.json"
RAW_BASE = "https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/{branch}/assets/projects/rainbow-tel-aviv"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--branch",
        default="main",
        help="GitHub branch/ref for raw asset URLs. Use main after merge.",
    )
    args = parser.parse_args()

    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    raw_base = RAW_BASE.format(branch=args.branch)
    meta["project_model_glb"] = f"{raw_base}/model.glb"
    meta["project_model_poster"] = f"{raw_base}/poster.png"

    units = meta.get("project_3d_units", [])
    drawings = meta.get("project_3d_drawings_json", [])

    print("# Rainbow Tel Aviv CMS Payload")
    print()
    print("Post ID: 4464")
    print(f"project_model_glb: {meta['project_model_glb']}")
    print(f"project_model_poster: {meta['project_model_poster']}")
    print(f"project_model_usdz: {meta.get('project_model_usdz', '')}")
    print()
    print("project_3d_units:")
    print(json.dumps(units, ensure_ascii=False, indent=2))
    print()
    print("project_3d_drawings_json:")
    print(json.dumps(drawings, ensure_ascii=False, indent=2))
    print()
    print("QA after write:")
    print("- Clear cache and hard refresh /projects/rainbow-tel-aviv/.")
    print("- Confirm <model-viewer> renders and hotspots select units.")
    print("- Confirm /wp-json/nadlan/v1/healthcheck reports projects_with_glb >= 1.")
    print("- Keep inquiry-only and illustrative-model disclaimers until official BIM/inventory arrives.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
