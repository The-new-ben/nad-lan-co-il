#!/usr/bin/env python3
"""Dry-run or apply Rainbow's prototype model payload through WordPress REST.

Default mode is read-only. Use --apply only after PR #163 is merged, the server
Git copy has been pulled, and you are ready to wire the live Rainbow card.

Environment for --apply:
  WP_BASE_URL       Defaults to https://nad-lan.co.il
  WP_USER           WordPress username
  WP_APP_PASSWORD   WordPress application password

The script never logs credentials. It writes only REST-registered v1.63.0 meta.
project_3d_units is still printed for the admin metabox because v1.63.0 does
not expose that key through register_post_meta(... show_in_rest => true).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "assets" / "projects" / "rainbow-tel-aviv" / "project-meta-example.json"
RAW_BASE = "https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/{branch}/assets/projects/rainbow-tel-aviv"
DEFAULT_BASE_URL = "https://nad-lan.co.il"
DEFAULT_POST_ID = 4464


def load_source_meta(branch: str) -> dict[str, Any]:
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    raw_base = RAW_BASE.format(branch=branch)
    meta["project_model_glb"] = f"{raw_base}/model.glb"
    meta["project_model_poster"] = f"{raw_base}/poster.png"
    meta.setdefault("project_model_usdz", "")
    return meta


def flatten_environment(value: Any) -> list[dict[str, Any]]:
    """Convert the rich research object into the list shape v1.63.0 renders."""
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if not isinstance(value, dict):
        return []

    items: list[dict[str, Any]] = []
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
            clean: dict[str, Any] = {
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


def build_rest_meta(source: dict[str, Any]) -> dict[str, str]:
    drawings = source.get("project_3d_drawings_json", [])
    environment = flatten_environment(source.get("project_3d_environment_json", []))
    return {
        "project_3d_model_type": "gltf",
        "project_model_glb": str(source.get("project_model_glb", "")),
        "project_model_poster": str(source.get("project_model_poster", "")),
        "project_model_usdz": str(source.get("project_model_usdz", "")),
        "project_3d_drawings_json": json.dumps(drawings, ensure_ascii=False, separators=(",", ":")),
        "project_3d_environment_json": json.dumps(environment, ensure_ascii=False, separators=(",", ":")),
    }


def auth_header(user: str, password: str) -> str:
    token = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def request_json(
    method: str,
    url: str,
    *,
    auth: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if auth:
        headers["Authorization"] = auth
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as res:
            body = res.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed with HTTP {exc.code}: {body[:1200]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{method} {url} failed: {exc.reason}") from exc


def endpoint(base_url: str, path: str) -> str:
    return urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def print_summary(rest_meta: dict[str, str], source: dict[str, Any], post_id: int) -> None:
    units = source.get("project_3d_units", [])
    print("# Rainbow CMS apply summary")
    print(f"Post ID: {post_id}")
    print("REST-writable fields:")
    for key, value in rest_meta.items():
        if key.endswith("_json"):
            try:
                count = len(json.loads(value))
            except (TypeError, json.JSONDecodeError):
                count = 0
            print(f"- {key}: JSON items={count}, bytes={len(value.encode('utf-8'))}")
        else:
            print(f"- {key}: {value or '(empty)'}")
    print()
    print("Manual admin-metabox field still required in v1.63.0:")
    print(f"- project_3d_units: {len(units) if isinstance(units, list) else 0} units")
    print("  Reason: project_3d_units is not REST-registered in v1.63.0.")
    print("  Paste this value in the Rainbow 3D metabox until a later plugin patch exposes it safely:")
    print(json.dumps(units, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", default="main", help="GitHub branch/ref for raw asset URLs.")
    parser.add_argument("--post-id", default=DEFAULT_POST_ID, type=int, help="Rainbow post id.")
    parser.add_argument("--base-url", default=os.getenv("WP_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--apply", action="store_true", help="Write REST-registered fields to WordPress.")
    args = parser.parse_args()

    source = load_source_meta(args.branch)
    rest_meta = build_rest_meta(source)
    print_summary(rest_meta, source, args.post_id)

    if not args.apply:
        print()
        print("DRY RUN ONLY. Add --apply with WP_USER and WP_APP_PASSWORD to write REST fields.")
        return 0

    user = os.getenv("WP_USER", "")
    password = os.getenv("WP_APP_PASSWORD", "")
    if not user or not password:
        print("ERROR: --apply requires WP_USER and WP_APP_PASSWORD environment variables.", file=sys.stderr)
        return 2

    auth = auth_header(user, password)
    me_url = endpoint(args.base_url, "/wp-json/wp/v2/users/me?context=edit&_fields=id,name,roles")
    project_url = endpoint(
        args.base_url,
        f"/wp-json/wp/v2/nadlan_project/{args.post_id}?context=edit&_fields=id,slug,status,meta",
    )

    me = request_json("GET", me_url, auth=auth)
    print()
    print(f"Authenticated as WordPress user id {me.get('id')} ({me.get('name', 'unknown')}).")

    before = request_json("GET", project_url, auth=auth)
    print(f"Target project before write: id={before.get('id')} slug={before.get('slug')} status={before.get('status')}")

    updated = request_json("POST", project_url, auth=auth, payload={"meta": rest_meta})
    updated_meta = updated.get("meta") if isinstance(updated.get("meta"), dict) else {}
    print("REST write completed.")
    for key in rest_meta:
        current = str(updated_meta.get(key, ""))
        print(f"- {key}: {'present' if current else 'empty'}")

    health_url = endpoint(args.base_url, "/wp-json/nadlan/v1/healthcheck")
    try:
        health = request_json("GET", health_url)
        project_3d = health.get("project_3d", {}) if isinstance(health, dict) else {}
        print(
            "Healthcheck: "
            f"version={health.get('version', 'unknown')} "
            f"projects_with_glb={project_3d.get('projects_with_glb', 'unknown')}"
        )
    except RuntimeError as exc:
        print(f"WARNING: healthcheck read failed after write: {exc}", file=sys.stderr)

    print()
    print("Next: paste project_3d_units through the Rainbow 3D admin metabox, clear cache, and hard refresh.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
