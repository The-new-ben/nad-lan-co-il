#!/usr/bin/env python3
"""Create the starter asset/CMS contract for a future project showroom.

The generated folder is intentionally not public-ready. It creates the same
contract Rainbow uses so the next project can accept official model, media,
drawings, unit inventory and view-layer data without manual copy/paste.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ASSET_ROOT = ROOT / "assets" / "projects"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-slug", required=True, help="ASCII URL/asset slug, e.g. first-by-hagag.")
    parser.add_argument("--project-name", required=True, help="Display name used in internal scaffold notes.")
    parser.add_argument("--post-id", type=int, default=0, help="Target nadlan_project id when known.")
    parser.add_argument("--city", default="", help="City or municipality.")
    parser.add_argument("--developer", default="", help="Developer name, if known.")
    parser.add_argument("--lat", type=float, default=None, help="Approximate project latitude.")
    parser.add_argument("--lng", type=float, default=None, help="Approximate project longitude.")
    parser.add_argument("--floors", type=int, default=0, help="Known tower/building floor count.")
    parser.add_argument("--asset-root", type=Path, default=DEFAULT_ASSET_ROOT, help="Folder that contains project asset folders.")
    parser.add_argument("--dry-run", action="store_true", help="Print the file plan without writing files.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files.")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not SLUG_RE.fullmatch(args.project_slug):
        raise SystemExit("--project-slug must be lowercase ASCII letters, numbers and hyphens only.")
    if args.post_id < 0:
        raise SystemExit("--post-id must be 0 or a positive integer.")
    if args.floors < 0:
        raise SystemExit("--floors must be 0 or a positive integer.")
    if (args.lat is None) != (args.lng is None):
        raise SystemExit("--lat and --lng must be supplied together.")
    if args.lat is not None and not (-90 <= args.lat <= 90):
        raise SystemExit("--lat must be between -90 and 90.")
    if args.lng is not None and not (-180 <= args.lng <= 180):
        raise SystemExit("--lng must be between -180 and 180.")


def center(args: argparse.Namespace) -> dict[str, Any]:
    if args.lat is None or args.lng is None:
        return {
            "lat": None,
            "lng": None,
            "precision": "pending_verified_pin",
            "source_note": "Fill after official address, survey pin or verified map coordinate is approved.",
        }
    return {
        "lat": round(args.lat, 7),
        "lng": round(args.lng, 7),
        "precision": "owner_supplied_or_public_verified_pending_review",
        "source_note": "Verify against official project material before public launch.",
    }


def environment(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "status": "scaffold_pending_sources",
        "updated": date.today().isoformat(),
        "project": {
            "name": args.project_name,
            "city": args.city,
            "developer": args.developer,
            "center": center(args),
        },
        "source_policy": (
            "Use public/official facts or owner-approved licensed data only. Do not publish "
            "paid-source rows, exact inventory or unsourced pins."
        ),
        "district_context": {},
        "layers": [
            {"id": "neighbor_projects", "label": "Nearby projects", "ui": "clickable_project_chips", "items": []},
            {"id": "parks_and_coast", "label": "Parks and coast", "ui": "environment_cards", "items": []},
            {"id": "mobility", "label": "Transport and access", "ui": "mobility_facts", "items": []},
            {"id": "education", "label": "Schools and kindergartens", "ui": "service_cards", "items": []},
            {"id": "public_services", "label": "Public services", "ui": "service_cards", "items": []},
        ],
        "implementation_notes": [
            "Show planned/future labels for facilities that are not built yet.",
            "Use verified coordinates before rendering clickable map pins.",
            "Keep this JSON separate from unit inventory and pricing.",
        ],
    }


def project_meta(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "project_model_glb": "",
        "project_model_poster": "",
        "project_model_usdz": "",
        "project_3d_model_type": "procedural",
        "project_3d_image": "",
        "project_3d_video_url": "",
        "project_3d_tour_url": "",
        "project_3d_cesium_tiles_url": "",
        "project_3d_avg_price_per_sqm": 0,
        "project_3d_price_source_note": "",
        "project_3d_units": [],
        "project_3d_drawings_json": [],
        "project_3d_environment_json": environment(args),
        "_scaffold_note": (
            "Internal scaffold only. Do not apply to the public CMS until official or approved "
            "prototype assets, source notes and QA are filled."
        ),
    }


def drawings(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "status": "pending_official_material",
        "project_slug": args.project_slug,
        "items": [],
        "required_official_replacements": [
            "official_elevation",
            "typical_floor_plan",
            "site_plan",
            "unit_plan",
        ],
        "note": "Attach only approved developer drawings or owner-licensed material.",
    }


def material_intake(args: argparse.Namespace) -> dict[str, Any]:
    fields = [
        ("official_model", "project_model_glb", "GLB/GLTF, OBJ, FBX, SketchUp, Revit export"),
        ("poster", "project_model_poster", "PNG/WebP/JPG poster under the approved size budget"),
        ("ios_ar", "project_model_usdz", "Optional USDZ"),
        ("sales_video", "project_3d_video_url", "YouTube/Vimeo/approved HTTPS video URL"),
        ("interior_or_unit_tour", "project_3d_tour_url", "Kuula/CloudPano/Panoee/approved tour URL"),
        ("cesium_or_3d_tiles", "project_3d_cesium_tiles_url", "Approved Cesium ion or 3D Tiles URL/config"),
        ("drawings", "project_3d_drawings_json", "Elevation, site plan, typical floor, unit plans"),
        ("unit_inventory", "project_3d_units", "Unit ids, floor, sqm, rooms, direction, status, source note"),
        ("surroundings", "project_3d_environment_json", "Nearby projects, parks, mobility, education, public services"),
    ]
    return {
        "project_slug": args.project_slug,
        "post_id": args.post_id,
        "purpose": "Developer handoff checklist for an official project showroom.",
        "public_use_policy": "Use only owner-approved/official/licensed material. No copied paid-source media.",
        "items": [
            {
                "id": item_id,
                "cms_field": cms_field,
                "accepted_formats": accepted_formats,
                "status": "needed",
                "owner_action": "collect_or_approve",
                "notes": "",
            }
            for item_id, cms_field, accepted_formats in fields
        ],
    }


def view_layer_config(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "project_slug": args.project_slug,
        "post_id": args.post_id,
        "version": 1,
        "status": "scaffold_pending_sources",
        "project_center": center(args),
        "cms_inputs": {
            "lat": args.lat,
            "lng": args.lng,
            "project_3d_units": "unit-map.json",
            "project_3d_environment_json": "environment.json",
            "project_3d_cesium_tiles_url": "",
        },
        "providers": {
            "mapbox": {
                "state": "ready_when_token_and_coords_exist",
                "load_policy": "user_open_only",
                "rtl_text_plugin_required": True,
                "camera_formula": "ground_elevation_m + 4.0 + (floor - 1) * floor_height_m + 1.55",
                "ground_elevation_m": 0,
                "floor_height_m": 3.05,
                "camera_distance_m": 900,
                "pitch_degrees": 65,
                "bearing_source": "unit direction -> bearing_degrees",
            },
            "cesium": {
                "state": "ready_seam_pending_approved_tiles",
                "load_policy": "user_open_only",
                "tiles_url": "",
                "accepted_sources": [
                    "Cesium ion asset",
                    "Google Photorealistic 3D Tiles config",
                    "approved 3D Tiles endpoint",
                ],
                "public_policy": "Do not enable until token/cost governance and public-use rights are approved.",
            },
        },
        "cost_controls": {
            "instantiate_on_page_load": False,
            "lazy_on_user_gesture": True,
            "dedupe_per_session": True,
            "static_preview_fallback": True,
            "do_not_autoplay_tiles": True,
        },
        "unit_views": [],
        "overlays": [
            {
                "id": "neighbor_projects",
                "source": "project_3d_environment_json",
                "render_policy": "Only show clickable pins for verified coordinates; otherwise show source-aware cards.",
            },
            {
                "id": "parks_and_coast",
                "source": "project_3d_environment_json",
                "render_policy": "Planned/future labels required until built and verified.",
            },
            {
                "id": "mobility",
                "source": "project_3d_environment_json",
                "render_policy": "Transport items must show current/planned status.",
            },
        ],
        "qa_requirements": [
            "Default page state remains building selector, not map/tiles.",
            "View layer opens only after buyer action.",
            "Hebrew map labels require RTL plugin before Mapbox init.",
            "Unit selection recomputes altitude and bearing from selected unit.",
            "Cesium/3D Tiles controls stay hidden or pending until an approved tiles URL exists.",
        ],
    }


def source_notes(args: argparse.Namespace) -> str:
    return f"""# {args.project_name} showroom source notes

Status: scaffold only, not public-ready.

## Required before public CMS wiring

- Official or owner-approved model/poster, or a clearly labelled original prototype model.
- Verified project pin and address.
- Unit inventory with source notes for every field.
- Approved drawings/floor plans or explicit pending state.
- Surroundings facts from official/public sources.
- Price context approved by the owner; estimates must be non-binding.
- Browser QA at 390, 760 and 1440 px.

## Project facts to fill

- Slug: `{args.project_slug}`
- Post id: `{args.post_id or "pending"}`
- City: `{args.city or "pending"}`
- Developer: `{args.developer or "pending"}`
- Floors: `{args.floors or "pending"}`
- Center: `{args.lat if args.lat is not None else "pending"}, {args.lng if args.lng is not None else "pending"}`
"""


def qa_doc(args: argparse.Namespace) -> str:
    return f"""# {args.project_name} showroom QA

This folder is a scaffold. It is not clone-ready until every item below passes.

## Local gates

```powershell
python scripts\\check-rainbow-showroom-readiness.py --project-slug {args.project_slug} --skip-live
python scripts\\prepare-rainbow-cms-payload.py --project-slug {args.project_slug} --post-id {args.post_id or 0} --branch main
```

## Required evidence

- model.glb loads in a browser preview and is not only a poster.
- poster image is under the size budget.
- unit hotspots have 44px+ click/tap targets.
- project_model_glb and project_model_poster point to main/CDN/Media URLs, not draft branches.
- material-intake-template.json lists every missing official material.
- view-layer-config.json keeps Mapbox/Cesium lazy and user-opened.
- page has one H1, no raw code leak, and no horizontal overflow.
- price/availability wording is sourced and non-binding unless official inventory is approved.
"""


def file_plan(args: argparse.Namespace) -> dict[str, str]:
    return {
        "project-meta-example.json": json.dumps(project_meta(args), ensure_ascii=False, indent=2) + "\n",
        "unit-map.json": json.dumps([], ensure_ascii=False, indent=2) + "\n",
        "drawings.json": json.dumps(drawings(args), ensure_ascii=False, indent=2) + "\n",
        "environment.json": json.dumps(environment(args), ensure_ascii=False, indent=2) + "\n",
        "material-intake-template.json": json.dumps(material_intake(args), ensure_ascii=False, indent=2) + "\n",
        "view-layer-config.json": json.dumps(view_layer_config(args), ensure_ascii=False, indent=2) + "\n",
        "source-notes.md": source_notes(args),
        "qa.md": qa_doc(args),
    }


def main() -> int:
    args = parse_args()
    validate_args(args)
    asset_dir = args.asset_root / args.project_slug
    files = file_plan(args)

    if args.dry_run:
        print(f"Project showroom scaffold plan: {asset_dir}")
        for name in files:
            print(f"- {asset_dir / name}")
        return 0

    asset_dir.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        path = asset_dir / name
        if path.exists() and not args.force:
            raise SystemExit(f"Refusing to overwrite existing file without --force: {path}")
        path.write_text(content, encoding="utf-8", newline="\n")

    print(f"Created project showroom scaffold: {asset_dir}")
    for name in files:
        print(f"- {name}")
    print("Next: collect official/prototype model assets, fill units, then run the readiness checker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
