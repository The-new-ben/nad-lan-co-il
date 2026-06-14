#!/usr/bin/env python3
"""Dry-run or apply Rainbow's prototype model payload through WordPress REST.

Default mode is read-only. Use --apply only after the asset PR is merged, the
server Git copy has been pulled, the required plugin stack is live, and you are
ready to wire the live project card.

Environment for --apply:
  WP_BASE_URL       Defaults to https://nad-lan.co.il
  WP_USER           WordPress username
  WP_APP_PASSWORD   WordPress application password

The script never logs credentials. It writes only REST-registered meta.
project_3d_units is included only when the live healthcheck reports
project_3d.unit_meta_rest=true (v1.63.2+). The write path also requires the
v1.63.4 page-assembly SEO gate so the model is not wired onto an unfinished
flagship page. Dry-run still prints the payload for review; --apply refuses
older plugin versions before any write.
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
RAW_BASE = "https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/{branch}/assets/projects/{project_slug}"
DEFAULT_PROJECT_SLUG = "rainbow-tel-aviv"
DEFAULT_BASE_URL = "https://nad-lan.co.il"
DEFAULT_POST_ID = 4464
GITHUB_RAW_HOST = "raw.githubusercontent.com"
GITHUB_RAW_OWNER = "The-new-ben"
GITHUB_RAW_REPO = "nad-lan-co-il"
REQUIRED_PLUGIN_STACK_VERSION = (1, 63, 4)
REQUIRED_PLUGIN_STACK_LABEL = "1.63.4"


def meta_path(project_slug: str) -> Path:
    return ROOT / "assets" / "projects" / project_slug / "project-meta-example.json"


def load_source_meta(branch: str, project_slug: str) -> dict[str, Any]:
    path = meta_path(project_slug)
    if not path.exists():
        raise FileNotFoundError(f"Missing project meta file: {path}")
    meta = json.loads(path.read_text(encoding="utf-8"))
    raw_base = RAW_BASE.format(branch=branch, project_slug=project_slug)
    meta["project_model_glb"] = f"{raw_base}/model.glb"
    meta["project_model_poster"] = f"{raw_base}/poster.png"
    meta.setdefault("project_model_usdz", "")
    return meta


def iter_urls(value: Any) -> list[str]:
    urls: list[str] = []
    if isinstance(value, dict):
        for item in value.values():
            urls.extend(iter_urls(item))
    elif isinstance(value, list):
        for item in value:
            urls.extend(iter_urls(item))
    elif isinstance(value, str) and value.startswith(("http://", "https://")):
        urls.append(value)
    return urls


def unsafe_branch_raw_urls(value: Any) -> list[str]:
    unsafe: list[str] = []
    for url in iter_urls(value):
        parsed = urllib.parse.urlparse(url)
        if parsed.netloc != GITHUB_RAW_HOST:
            continue
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) < 3:
            continue
        if parts[0] == GITHUB_RAW_OWNER and parts[1] == GITHUB_RAW_REPO and parts[2] != "main":
            unsafe.append(url)
    return sorted(set(unsafe))


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


def build_rest_meta(source: dict[str, Any], *, include_units: bool = False) -> dict[str, str]:
    drawings = source.get("project_3d_drawings_json", [])
    environment = flatten_environment(source.get("project_3d_environment_json", []))
    meta = {
        "project_3d_model_type": "gltf",
        "project_model_glb": str(source.get("project_model_glb", "")),
        "project_model_poster": str(source.get("project_model_poster", "")),
        "project_model_usdz": str(source.get("project_model_usdz", "")),
        "project_3d_avg_price_per_sqm": str(source.get("project_3d_avg_price_per_sqm", "") or ""),
        "project_3d_price_source_note": str(source.get("project_3d_price_source_note", "") or ""),
        "project_3d_drawings_json": json.dumps(drawings, ensure_ascii=False, separators=(",", ":")),
        "project_3d_environment_json": json.dumps(environment, ensure_ascii=False, separators=(",", ":")),
    }
    if include_units:
        units = source.get("project_3d_units", [])
        meta["project_3d_units"] = json.dumps(units if isinstance(units, list) else [], ensure_ascii=False, separators=(",", ":"))
    return meta


def parse_meta_json(value: Any) -> Any:
    if isinstance(value, (list, dict)):
        return value
    if value is None:
        return None
    raw = str(value).strip()
    if raw == "":
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def item_count(value: Any) -> int:
    parsed = parse_meta_json(value)
    if isinstance(parsed, list):
        return len(parsed)
    if isinstance(parsed, dict):
        return len(parsed)
    return 0


def item_ids(value: Any) -> list[str]:
    parsed = parse_meta_json(value)
    if not isinstance(parsed, list):
        return []
    ids: list[str] = []
    for item in parsed:
        if isinstance(item, dict) and item.get("id"):
            ids.append(str(item["id"]))
    return ids


def verify_updated_meta(updated_meta: dict[str, Any], expected_meta: dict[str, str]) -> list[str]:
    errors: list[str] = []
    exact_keys = (
        "project_3d_model_type",
        "project_model_glb",
        "project_model_poster",
        "project_model_usdz",
        "project_3d_avg_price_per_sqm",
        "project_3d_price_source_note",
    )
    for key in exact_keys:
        expected = str(expected_meta.get(key, ""))
        actual = str(updated_meta.get(key, ""))
        if actual != expected:
            errors.append(f"{key}: expected {expected or '(empty)'}, got {actual or '(empty)'}")

    for key in ("project_3d_drawings_json", "project_3d_environment_json", "project_3d_units"):
        if key not in expected_meta:
            continue
        expected_count = item_count(expected_meta.get(key, ""))
        actual_count = item_count(updated_meta.get(key, ""))
        if actual_count != expected_count:
            errors.append(f"{key}: expected {expected_count} items, got {actual_count}")

    if "project_3d_units" in expected_meta:
        expected_ids = item_ids(expected_meta["project_3d_units"])
        actual_ids = item_ids(updated_meta.get("project_3d_units", ""))
        missing = [unit_id for unit_id in expected_ids if unit_id not in actual_ids]
        if missing:
            errors.append("project_3d_units: missing unit ids " + ", ".join(missing[:8]))

    return errors


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


def version_tuple(value: object) -> tuple[int, ...]:
    parts: list[int] = []
    for part in str(value or "").split("."):
        if not part.isdigit():
            break
        parts.append(int(part))
    return tuple(parts)


def plugin_stack_errors(health: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    version = str(health.get("version", ""))
    project_3d = health.get("project_3d", {}) if isinstance(health, dict) else {}
    assembly = health.get("project_page_assembly", {}) if isinstance(health, dict) else {}
    if version_tuple(version) < REQUIRED_PLUGIN_STACK_VERSION:
        errors.append(f"version {version or 'unknown'} < {REQUIRED_PLUGIN_STACK_LABEL}")
    if not (isinstance(project_3d, dict) and project_3d.get("model_viewer_ready") is True):
        errors.append("project_3d.model_viewer_ready is not true")
    if not (isinstance(project_3d, dict) and project_3d.get("unit_meta_rest") is True):
        errors.append("project_3d.unit_meta_rest is not true")
    if not (isinstance(project_3d, dict) and project_3d.get("floating_action_rail_v1633") is True):
        errors.append("project_3d.floating_action_rail_v1633 is not true")
    if not (isinstance(assembly, dict) and assembly.get("rainbow_seo_v1634") is True):
        errors.append("project_page_assembly.rainbow_seo_v1634 is not true")
    return errors


def print_summary(rest_meta: dict[str, str], source: dict[str, Any], post_id: int, project_slug: str, *, include_units: bool = False) -> None:
    units = source.get("project_3d_units", [])
    print("# Project showroom CMS apply summary")
    print(f"Project slug: {project_slug}")
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
    print("Unit payload:")
    print(f"- project_3d_units: {len(units) if isinstance(units, list) else 0} units")
    if include_units:
        print("  Included in REST payload because healthcheck reported project_3d.unit_meta_rest=true.")
    else:
        print("  Conditional: --apply writes this field only when healthcheck reports project_3d.unit_meta_rest=true.")
        print("  If the live plugin is older, paste this value in the Rainbow 3D metabox:")
        print(json.dumps(units, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", default="main", help="GitHub branch/ref for raw asset URLs.")
    parser.add_argument("--project-slug", default=DEFAULT_PROJECT_SLUG, help="Asset folder under assets/projects/.")
    parser.add_argument("--post-id", default=DEFAULT_POST_ID, type=int, help="Target nadlan_project post id.")
    parser.add_argument("--base-url", default=os.getenv("WP_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--apply", action="store_true", help="Write REST-registered fields to WordPress.")
    parser.add_argument(
        "--allow-branch-assets",
        action="store_true",
        help="Permit --apply with non-main raw GitHub URLs for explicit temporary QA only.",
    )
    parser.add_argument(
        "--skip-plugin-stack-check",
        action="store_true",
        help="Permit --apply without live v1.63.4 stack markers. Use only for explicit manual fallback QA.",
    )
    args = parser.parse_args()

    source = load_source_meta(args.branch, args.project_slug)
    rest_meta = build_rest_meta(source, include_units=False)
    unsafe_urls = unsafe_branch_raw_urls(source)

    if not args.apply:
        print_summary(rest_meta, source, args.post_id, args.project_slug, include_units=False)
        if unsafe_urls:
            print()
            print("WARNING: payload contains draft/non-main GitHub raw asset URLs:")
            for url in unsafe_urls:
                print(f"- {url}")
        print()
        print("DRY RUN ONLY. Add --apply with WP_USER and WP_APP_PASSWORD to write REST fields.")
        return 0

    if unsafe_urls:
        print()
        print("WARNING: payload contains draft/non-main GitHub raw asset URLs:")
        for url in unsafe_urls:
            print(f"- {url}")

    if unsafe_urls and not args.allow_branch_assets:
        print(
            "ERROR: refusing --apply with draft/non-main raw asset URLs. "
            "Merge the assets to main or pass --allow-branch-assets for a temporary QA write.",
            file=sys.stderr,
        )
        return 3
    if unsafe_urls and args.allow_branch_assets:
        print(
            "WARNING: --allow-branch-assets is active. Do not leave the live project card pointing at draft URLs.",
            file=sys.stderr,
        )

    health_url = endpoint(args.base_url, "/wp-json/nadlan/v1/healthcheck")
    health: dict[str, Any] = {}
    try:
        health = request_json("GET", health_url)
    except RuntimeError as exc:
        if not args.skip_plugin_stack_check:
            print(f"ERROR: cannot verify live plugin stack before apply: {exc}", file=sys.stderr)
            return 4
        print(f"WARNING: plugin stack healthcheck failed but override is active: {exc}", file=sys.stderr)

    if health:
        errors = plugin_stack_errors(health)
        if errors and not args.skip_plugin_stack_check:
            print("ERROR: refusing --apply until the live plugin stack is ready:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            print("Deploy PRs #164, #165, #166 and #167 first, clear cache, then rerun.", file=sys.stderr)
            return 4
        if errors and args.skip_plugin_stack_check:
            print("WARNING: --skip-plugin-stack-check is active despite:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)

    print_summary(rest_meta, source, args.post_id, args.project_slug, include_units=False)

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

    unit_meta_rest = False
    try:
        if not health:
            health = request_json("GET", health_url)
        project_3d = health.get("project_3d", {}) if isinstance(health, dict) else {}
        unit_meta_rest = bool(project_3d.get("unit_meta_rest"))
        print(
            "Healthcheck before write: "
            f"version={health.get('version', 'unknown')} "
            f"unit_meta_rest={unit_meta_rest}"
        )
    except RuntimeError as exc:
        print(f"WARNING: healthcheck read failed before write; skipping project_3d_units: {exc}", file=sys.stderr)

    if unit_meta_rest:
        rest_meta = build_rest_meta(source, include_units=True)
        print("project_3d_units is REST-enabled; including unit payload in this write.")
    else:
        print("project_3d_units is not REST-enabled on this site yet; leaving unit JSON for the metabox fallback.")

    before = request_json("GET", project_url, auth=auth)
    print(f"Target project before write: id={before.get('id')} slug={before.get('slug')} status={before.get('status')}")

    updated = request_json("POST", project_url, auth=auth, payload={"meta": rest_meta})
    updated_meta = updated.get("meta") if isinstance(updated.get("meta"), dict) else {}
    print("REST write completed.")
    for key in rest_meta:
        current = str(updated_meta.get(key, ""))
        print(f"- {key}: {'present' if current else 'empty'}")

    verify_errors = verify_updated_meta(updated_meta, rest_meta)
    if verify_errors:
        print("ERROR: REST write verification failed:", file=sys.stderr)
        for error in verify_errors:
            print(f"- {error}", file=sys.stderr)
        return 5
    print("REST write verification passed.")

    try:
        health = request_json("GET", health_url)
        project_3d = health.get("project_3d", {}) if isinstance(health, dict) else {}
        print(
            "Healthcheck: "
            f"version={health.get('version', 'unknown')} "
            f"unit_meta_rest={project_3d.get('unit_meta_rest', 'unknown')} "
            f"projects_with_glb={project_3d.get('projects_with_glb', 'unknown')}"
        )
    except RuntimeError as exc:
        print(f"WARNING: healthcheck read failed after write: {exc}", file=sys.stderr)

    print()
    if unit_meta_rest:
        print("Next: clear cache, hard refresh, and run the live DOM GLB gate.")
    else:
        print("Next: paste project_3d_units through the Rainbow 3D admin metabox, clear cache, and hard refresh.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
