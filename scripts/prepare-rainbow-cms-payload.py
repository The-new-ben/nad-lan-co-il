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


def flatten_environment(value):
    """Convert the rich research object into the list shape v1.63.0 renders."""
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if not isinstance(value, dict):
        return []

    items = []
    district = value.get("district_context")
    if isinstance(district, dict):
        detail_bits = []
        if district.get("planned_units"):
            detail_bits.append(f"{district.get('planned_units'):,} דירות מתוכננות")
        if district.get("planned_population"):
            detail_bits.append(f"{district.get('planned_population'):,} תושבים מתוכננים")
        if district.get("planning_area_dunam"):
            detail_bits.append(f"{district.get('planning_area_dunam'):,} דונם")
        if district.get("planning_status"):
            detail_bits.append(str(district.get("planning_status")))
        items.append(
            {
                "label": "רובע שדה דב",
                "type": "district_context",
                "category": "district",
                "detail": "; ".join(detail_bits),
                "note": str(value.get("source_policy", "")),
                "source": "עיריית תל אביב-יפו / Gov.il / אתר רובע שדה דב",
            }
        )

    for layer in value.get("layers", []):
        if not isinstance(layer, dict):
            continue
        category = str(layer.get("id") or "environment")
        layer_label = str(layer.get("label") or category)
        for entry in layer.get("items", []):
            if not isinstance(entry, dict):
                continue
            label = entry.get("name") or entry.get("label") or entry.get("id")
            if not label:
                continue
            detail_parts = []
            for key in ("area", "status"):
                if entry.get(key):
                    detail_parts.append(str(entry[key]))
            clean = {
                "label": str(label),
                "type": str(entry.get("type") or category),
                "category": category,
                "detail": " | ".join(detail_parts) or layer_label,
                "url": str(entry.get("url") or entry.get("source_url") or ""),
            }
            for key in ("lat", "lng", "distance"):
                if key in entry:
                    clean[key] = entry[key]
            items.append(clean)
            if len(items) >= 40:
                return items
    return items


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
    environment = flatten_environment(meta.get("project_3d_environment_json", []))

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
    print("project_3d_environment_json (flattened for v1.63.0 REST/metabox):")
    print(json.dumps(environment, ensure_ascii=False, indent=2))
    print()
    print("REST note:")
    print("- project_model_glb, project_model_poster, project_model_usdz, project_3d_model_type,")
    print("  project_3d_drawings_json and project_3d_environment_json are REST-writable in v1.63.0.")
    print("- project_3d_units is not REST-registered in v1.63.0; paste it in the Rainbow 3D metabox")
    print("  unless a later plugin patch exposes that key.")
    print("- Optional helper: python scripts\\apply-rainbow-cms-payload.py --branch main --apply")
    print()
    print("QA after write:")
    print("- Clear cache and hard refresh /projects/rainbow-tel-aviv/.")
    print("- Confirm <model-viewer> renders and hotspots select units.")
    print("- Confirm /wp-json/nadlan/v1/healthcheck reports projects_with_glb >= 1.")
    print("- Keep inquiry-only and illustrative-model disclaimers until official BIM/inventory arrives.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
