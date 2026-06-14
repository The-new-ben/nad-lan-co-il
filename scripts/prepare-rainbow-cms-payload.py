#!/usr/bin/env python3
"""Print a project showroom CMS payload after its asset PR merge.

This script is intentionally read-only. It does not call WordPress and does not
write live metadata. Use it to copy reviewed values into the Studio/admin flow.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECT_SLUG = "rainbow-tel-aviv"
DEFAULT_POST_ID = 4464
DEFAULT_ASSET_ROOT = ROOT / "assets" / "projects"
RAW_BASE = "https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/{branch}/assets/projects/{project_slug}"


def flatten_environment(value):
    """Convert the rich research object into the list shape v1.63.0 renders.

    The live plugin sanitizes this meta to renderer-safe card fields only. Keep
    provenance in `note`, keep links in `url`, and never turn schematic
    showroom positions into map coordinates.
    """
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if not isinstance(value, dict):
        return []

    items = []
    district = value.get("district_context")
    if isinstance(district, dict) and district:
        project = value.get("project") if isinstance(value.get("project"), dict) else {}
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
        sources = district.get("sources") if isinstance(district.get("sources"), list) else []
        source_labels = [str(item.get("label")) for item in sources if isinstance(item, dict) and item.get("label")]
        items[-1]["label"] = str(
            district.get("label") or district.get("name") or project.get("district") or "District context"
        )
        items[-1]["source"] = " / ".join(source_labels) if source_labels else ""

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
            if entry.get("source_note"):
                clean["note"] = str(entry["source_note"])
            if entry.get("source"):
                clean["source"] = str(entry["source"])
            if entry.get("map_status") != "needs_precise_pin":
                for key in ("lat", "lng"):
                    if key in entry:
                        clean[key] = entry[key]
            if "distance" in entry:
                clean["distance"] = entry["distance"]
            items.append(clean)
            if len(items) >= 40:
                return items
    return items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-slug",
        default=DEFAULT_PROJECT_SLUG,
        help="Asset folder under assets/projects/.",
    )
    parser.add_argument(
        "--post-id",
        type=int,
        default=DEFAULT_POST_ID,
        help="Target nadlan_project post id for the copy/paste note.",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="GitHub branch/ref for raw asset URLs. Use main after merge.",
    )
    parser.add_argument(
        "--asset-root",
        type=Path,
        default=DEFAULT_ASSET_ROOT,
        help="Folder that contains project asset folders.",
    )
    args = parser.parse_args()

    asset_dir = args.asset_root / args.project_slug
    meta_path = asset_dir / "project-meta-example.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"Missing project meta file: {meta_path}")

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    raw_base = RAW_BASE.format(branch=args.branch, project_slug=args.project_slug)
    if (asset_dir / "model.glb").exists():
        meta["project_model_glb"] = f"{raw_base}/model.glb"
    if (asset_dir / "poster.png").exists():
        meta["project_model_poster"] = f"{raw_base}/poster.png"

    units = meta.get("project_3d_units", [])
    drawings = meta.get("project_3d_drawings_json", [])
    environment = flatten_environment(meta.get("project_3d_environment_json", []))

    print(f"# {args.project_slug} CMS Payload")
    print()
    print(f"Post ID: {args.post_id}")
    print(f"project_model_glb: {meta.get('project_model_glb', '')}")
    print(f"project_model_poster: {meta.get('project_model_poster', '')}")
    print(f"project_model_usdz: {meta.get('project_model_usdz', '')}")
    print(f"project_3d_video_url: {meta.get('project_3d_video_url', '')}")
    print(f"project_3d_tour_url: {meta.get('project_3d_tour_url', '')}")
    print(f"project_3d_cesium_tiles_url: {meta.get('project_3d_cesium_tiles_url', '')}")
    print()
    print("project_3d_units:")
    print(json.dumps(units, ensure_ascii=False, indent=2))
    print()
    print("project_3d_drawings_json:")
    print(json.dumps(drawings, ensure_ascii=False, indent=2))
    print()
    print("project_3d_environment_json (flattened for the project showroom CMS field):")
    print(json.dumps(environment, ensure_ascii=False, indent=2))
    print()
    print("View layer note:")
    print(f"- See assets/projects/{args.project_slug}/view-layer-config.json for Mapbox/Cesium camera,")
    print("  unit altitude/bearing, overlay and cost-control rules. It is a handoff/QA contract, not")
    print("  a separate CMS field.")
    print()
    print("REST note:")
    print("- project_model_glb, project_model_poster, project_model_usdz, project_3d_model_type,")
    print("  project_3d_video_url, project_3d_tour_url, project_3d_cesium_tiles_url,")
    print("  project_3d_drawings_json and project_3d_environment_json are REST-writable in v1.63.0.")
    print("- project_3d_units is REST-writable when healthcheck reports project_3d.unit_meta_rest=true.")
    print("- The apply helper intentionally requires the full v1.63.4 stack before public GLB wiring:")
    print("  model_viewer_ready, unit_meta_rest, floating_action_rail_v1633 and rainbow_seo_v1634.")
    print(
        "- Optional helper after that stack is live: "
        f"python scripts\\apply-rainbow-cms-payload.py --project-slug {args.project_slug} "
        f"--post-id {args.post_id} --branch main --apply"
    )
    print()
    print("QA after write:")
    print("- Clear cache and hard refresh the target project URL.")
    print("- Confirm <model-viewer> renders and hotspots select units.")
    print("- Confirm /wp-json/nadlan/v1/healthcheck reports projects_with_glb >= 1.")
    print("- Keep inquiry-only and illustrative-model disclaimers until official BIM/inventory arrives.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
