#!/usr/bin/env python3
"""Check the Rainbow showroom asset/CMS readiness package.

This is a lightweight gate for the model payload branch. It checks local assets,
the CMS payload shape and, unless disabled, the live healthcheck capability flags.
It does not write to WordPress.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HEALTHCHECK = "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck"
DEFAULT_PROJECT_SLUG = "rainbow-tel-aviv"
MAX_GLB_BYTES = 4 * 1024 * 1024
MAX_POSTER_BYTES = 80 * 1024
REMOTE_READ_BYTES = 4096
REQUIRED_PLUGIN_STACK_VERSION = (1, 63, 4)
REQUIRED_PLUGIN_STACK_LABEL = "1.63.4"
PUBLIC_TEXT_MIN_HEBREW = {
    "project-meta-example.json": 1000,
    "unit-map.json": 500,
    "drawings.json": 100,
    "environment.json": 100,
    "view-layer-config.json": 10,
}


class Gate:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def pass_(self, name: str, detail: str) -> None:
        self.rows.append(("PASS", name, detail))

    def warn(self, name: str, detail: str) -> None:
        self.rows.append(("WARN", name, detail))

    def fail(self, name: str, detail: str) -> None:
        self.rows.append(("FAIL", name, detail))

    @property
    def failed(self) -> bool:
        return any(status == "FAIL" for status, _, _ in self.rows)

    def print(self) -> None:
        for status, name, detail in self.rows:
            print(f"[{status}] {name}: {detail}")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def hebrew_char_count(value: str) -> int:
    return sum(0x0590 <= ord(char) <= 0x05FF for char in value)


def mojibake_control_count(value: str) -> int:
    return sum(0x0080 <= ord(char) <= 0x009F for char in value)


def check_text_sanity(path: Path, gate: Gate, min_hebrew: int) -> None:
    if not path.exists():
        gate.fail(f"{path.name} text sanity", "missing")
        return
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        gate.fail(f"{path.name} text sanity", f"not valid UTF-8: {exc}")
        return

    replacement = text.count("\ufffd")
    controls = mojibake_control_count(text)
    hebrew = hebrew_char_count(text)
    if replacement or controls:
        gate.fail(
            f"{path.name} text sanity",
            f"replacement={replacement}, c1_controls={controls}; possible encoding corruption",
        )
        return
    if hebrew < min_hebrew:
        gate.fail(f"{path.name} text sanity", f"only {hebrew} Hebrew chars; expected at least {min_hebrew}")
        return
    gate.pass_(f"{path.name} text sanity", f"UTF-8 clean, Hebrew chars={hebrew}")


def local_path_for_raw_url(url: str, root: Path) -> Path | None:
    """Map a GitHub raw URL in this repo to the expected local file path."""
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != "raw.githubusercontent.com":
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 5 or parts[0] != "The-new-ben" or parts[1] != "nad-lan-co-il":
        return None
    return root.joinpath(*parts[3:])


def repo_raw_ref(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != "raw.githubusercontent.com":
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 5 or parts[0] != "The-new-ben" or parts[1] != "nad-lan-co-il":
        return None
    return parts[2]


def check_raw_url_local_file(url: str, root: Path, gate: Gate, label: str) -> None:
    local = local_path_for_raw_url(url, root)
    if local is None:
        return
    if local.exists() and local.is_file():
        gate.pass_(f"{label} local file", str(local.relative_to(root)))
    else:
        gate.fail(f"{label} local file", f"missing local file for raw URL: {local.relative_to(root)}")


def raw_url_for_ref(url: str, remote_ref: str | None) -> str:
    if not remote_ref:
        return url
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != "raw.githubusercontent.com":
        return url
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 4 or parts[0] != "The-new-ben" or parts[1] != "nad-lan-co-il":
        return url
    try:
        asset_index = parts.index("assets", 2)
    except ValueError:
        return url
    ref_parts = [part for part in remote_ref.split("/") if part]
    path_parts = parts[:2] + ref_parts + parts[asset_index:]
    return urllib.parse.urlunparse(parsed._replace(path="/" + "/".join(path_parts)))


def fetch_remote_prefix(url: str, byte_count: int = REMOTE_READ_BYTES) -> tuple[bytes, str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "nadlan-rainbow-readiness/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        content_type = response.headers.get("Content-Type", "")
        content_length = response.headers.get("Content-Length", "")
        return response.read(byte_count), content_type, content_length


def check_remote_asset(url: str, gate: Gate, label: str, kind: str) -> None:
    try:
        prefix, content_type, content_length = fetch_remote_prefix(url)
    except urllib.error.HTTPError as exc:
        gate.fail(f"{label} remote URL", f"HTTP {exc.code}: {url}")
        return
    except urllib.error.URLError as exc:
        gate.fail(f"{label} remote URL", f"{exc.reason}: {url}")
        return
    except TimeoutError:
        gate.fail(f"{label} remote URL", f"timeout: {url}")
        return

    normalized = prefix.lstrip().lower()
    if kind == "glb" and prefix[:4] != b"glTF":
        gate.fail(f"{label} remote signature", "first bytes are not GLB/glTF")
        return
    if kind == "png" and prefix[:8] != b"\x89PNG\r\n\x1a\n":
        gate.fail(f"{label} remote signature", "first bytes are not PNG")
        return
    if kind == "svg" and b"<svg" not in normalized[:REMOTE_READ_BYTES]:
        gate.fail(f"{label} remote signature", "first bytes do not contain <svg")
        return
    detail = f"type={content_type or 'unknown'}"
    if content_length:
        detail += f", bytes={content_length}"
    gate.pass_(f"{label} remote URL", detail)


def optional_https_url_state(value: object) -> str:
    raw = str(value or "").strip()
    if raw == "":
        return "empty"
    parsed = urllib.parse.urlparse(raw)
    if parsed.scheme != "https" or not parsed.netloc:
        return "bad"
    return "ok"


def check_glb(path: Path, gate: Gate) -> None:
    if not path.exists():
        gate.fail("model.glb", "missing")
        return
    data = path.read_bytes()
    if len(data) > MAX_GLB_BYTES:
        gate.fail("model.glb size", f"{len(data)} bytes exceeds {MAX_GLB_BYTES}")
    else:
        gate.pass_("model.glb size", f"{len(data)} bytes")
    if len(data) < 20 or data[0:4] != b"glTF":
        gate.fail("model.glb header", "not a GLB/glTF binary")
        return
    version = int.from_bytes(data[4:8], "little")
    declared = int.from_bytes(data[8:12], "little")
    chunk_type = data[16:20].decode("ascii", "replace")
    if version == 2 and declared == len(data) and chunk_type == "JSON":
        gate.pass_("model.glb header", f"glTF 2.0, {declared} declared bytes")
    else:
        gate.fail("model.glb header", f"version={version}, declared={declared}, chunk={chunk_type}")


def check_poster(path: Path, gate: Gate) -> None:
    if not path.exists():
        gate.fail("poster.png", "missing")
        return
    size = path.stat().st_size
    if size <= MAX_POSTER_BYTES:
        gate.pass_("poster.png size", f"{size} bytes")
    else:
        gate.fail("poster.png size", f"{size} bytes exceeds {MAX_POSTER_BYTES}")


def check_meta(path: Path, root: Path, gate: Gate, *, check_remote_assets: bool = False, remote_ref: str | None = None) -> int:
    if not path.exists():
        gate.fail("project-meta-example.json", "missing")
        return 0
    meta = read_json(path)
    if not isinstance(meta, dict):
        gate.fail("project-meta-example.json", "root is not object")
        return 0
    for field in ["project_model_glb", "project_model_poster", "project_3d_units"]:
        if field in meta:
            gate.pass_(field, "present")
        else:
            gate.fail(field, "missing from CMS payload")
    for field in ["project_model_glb", "project_model_poster"]:
        value = str(meta.get(field, ""))
        raw_ref = repo_raw_ref(value)
        if raw_ref and raw_ref != "main":
            gate.fail(field, "raw GitHub asset URL must point at main after merge, not a draft branch")
        elif value:
            gate.pass_(f"{field} URL durability", "main raw URL or custom hosted URL")
            check_raw_url_local_file(value, root, gate, field)
            if check_remote_assets:
                check_remote_asset(raw_url_for_ref(value, remote_ref), gate, field, "glb" if field.endswith("_glb") else "png")
    media_fields = ["project_3d_video_url", "project_3d_tour_url", "project_3d_cesium_tiles_url"]
    missing_media_fields = [field for field in media_fields if field not in meta]
    if missing_media_fields:
        gate.fail("project media slots", "missing: " + ", ".join(missing_media_fields))
    else:
        filled_media = []
        bad_media = []
        empty_media = []
        for field in media_fields:
            state = optional_https_url_state(meta.get(field))
            if state == "ok":
                filled_media.append(field)
            elif state == "bad":
                bad_media.append(field)
            else:
                empty_media.append(field)
        if bad_media:
            gate.fail("project media slot URLs", "must be empty or HTTPS: " + ", ".join(bad_media))
        elif filled_media:
            gate.pass_("project media slot URLs", "approved HTTPS slots present: " + ", ".join(filled_media))
            if empty_media:
                gate.warn("project media slots pending", "empty: " + ", ".join(empty_media))
        else:
            gate.warn("project media slots pending", "official video/tour/Cesium tiles not supplied yet")
    avg_price = meta.get("project_3d_avg_price_per_sqm", 0)
    try:
        avg_price_number = float(avg_price)
    except (TypeError, ValueError):
        avg_price_number = 0
    price_source_note = str(meta.get("project_3d_price_source_note", ""))
    if avg_price_number > 0:
        gate.pass_("avg price per sqm", f"{avg_price_number:,.0f}")
        if "אומדן" in price_source_note and "לא הצעה" in price_source_note and "לא התחייבות" in price_source_note:
            gate.pass_("avg price source note", "non-binding source note present")
        else:
            gate.fail("avg price source note", "must include אומדן + לא הצעה + לא התחייבות")
    else:
        gate.warn("avg price per sqm", "empty; buyer price estimate will show לפי פנייה unless project meta is filled")
    units = meta.get("project_3d_units", [])
    if isinstance(units, list) and units:
        gate.pass_("project_3d_units count", str(len(units)))
    else:
        gate.fail("project_3d_units count", "missing or empty")
        units = []
    required_unit_fields = ["id", "floor", "hotspot_position", "hotspot_normal", "source_note", "plan"]
    missing: list[str] = []
    for unit in units:
        if not isinstance(unit, dict):
            missing.append("<non-object unit>")
            continue
        unit_id = str(unit.get("id", "<missing id>"))
        for field in required_unit_fields:
            if not unit.get(field):
                missing.append(f"{unit_id}.{field}")
    if missing:
        gate.fail("unit hotspot/source fields", ", ".join(missing[:12]))
    else:
        gate.pass_("unit hotspot/source fields", f"{len(units)} units complete")
    disclaimer_missing = []
    for unit in units:
        if not isinstance(unit, dict):
            continue
        note = " ".join(
            str(unit.get(key, ""))
            for key in ("price_note", "market_note", "price_source", "source_note")
        )
        if "לא הצעה" not in note and "אומדן" not in note:
            disclaimer_missing.append(str(unit.get("id", "<missing id>")))
    if disclaimer_missing:
        gate.fail("unit price disclaimer", ", ".join(disclaimer_missing[:12]))
    else:
        gate.pass_("unit price disclaimer", "all demo units carry non-binding price/source language")
    plan_bad = []
    for unit in units:
        if not isinstance(unit, dict):
            continue
        plan = str(unit.get("plan", ""))
        raw_ref = repo_raw_ref(plan)
        if not plan.startswith("https://") or (raw_ref and raw_ref != "main"):
            plan_bad.append(str(unit.get("id", "<missing id>")))
        else:
            check_raw_url_local_file(plan, root, gate, f"{unit.get('id', '<missing id>')}.plan")
            if check_remote_assets:
                check_remote_asset(raw_url_for_ref(plan, remote_ref), gate, f"{unit.get('id', '<missing id>')}.plan", "svg")
    if plan_bad:
        gate.fail("unit plan URLs", ", ".join(plan_bad[:12]))
    else:
        gate.pass_("unit plan URLs", "all demo units point at durable schematic plan URLs")
    unit_media_missing: list[str] = []
    unit_media_bad: list[str] = []
    unit_media_filled = 0
    unit_media_empty = 0
    for unit in units:
        if not isinstance(unit, dict):
            continue
        unit_id = str(unit.get("id", "<missing id>"))
        for field in ("interior_url", "tour_url"):
            if field not in unit:
                unit_media_missing.append(f"{unit_id}.{field}")
                continue
            state = optional_https_url_state(unit.get(field))
            if state == "bad":
                unit_media_bad.append(f"{unit_id}.{field}")
            elif state == "ok":
                unit_media_filled += 1
            else:
                unit_media_empty += 1
    if unit_media_missing:
        gate.fail("unit media slots", "missing: " + ", ".join(unit_media_missing[:12]))
    elif unit_media_bad:
        gate.fail("unit media slot URLs", "must be empty or HTTPS: " + ", ".join(unit_media_bad[:12]))
    elif unit_media_filled:
        gate.pass_("unit media slot URLs", f"{unit_media_filled} approved HTTPS unit media URLs present")
        if unit_media_empty:
            gate.warn("unit media slots pending", f"{unit_media_empty} empty unit media slots")
    else:
        gate.warn("unit media slots pending", f"{unit_media_empty} official interior/tour URLs not supplied yet")
    drawings = meta.get("project_3d_drawings_json", [])
    if isinstance(drawings, list) and any(isinstance(item, dict) and item.get("url") for item in drawings):
        gate.pass_("drawing material URLs", f"{sum(1 for item in drawings if isinstance(item, dict) and item.get('url'))} linked items")
        for item in drawings:
            if not isinstance(item, dict) or not item.get("url"):
                continue
            drawing_url = str(item.get("url", ""))
            drawing_label = f"drawing.{item.get('type', 'item')}"
            check_raw_url_local_file(drawing_url, root, gate, drawing_label)
            if check_remote_assets:
                check_remote_asset(raw_url_for_ref(drawing_url, remote_ref), gate, drawing_label, "svg")
    else:
        gate.fail("drawing material URLs", "no linked drawing/site material in CMS payload")
    env = meta.get("project_3d_environment_json")
    if isinstance(env, dict):
        layers = env.get("layers", [])
        if isinstance(layers, list) and layers:
            gate.pass_("project_3d_environment_json", f"{len(layers)} layers")
        else:
            gate.fail("project_3d_environment_json", "missing layers")
    else:
        gate.fail("project_3d_environment_json", "missing from CMS payload")
    return len(units)


def check_environment(path: Path, gate: Gate) -> None:
    if not path.exists():
        gate.fail("environment.json", "missing")
        return
    env = read_json(path)
    if not isinstance(env, dict):
        gate.fail("environment.json", "root is not object")
        return
    layers = env.get("layers", [])
    if not isinstance(layers, list) or not layers:
        gate.fail("environment layers", "missing")
        return
    neighbor = next((layer for layer in layers if isinstance(layer, dict) and layer.get("id") == "neighbor_projects"), None)
    if isinstance(neighbor, dict) and isinstance(neighbor.get("items"), list):
        gate.pass_("neighbor project layer", f"{len(neighbor['items'])} items")
        missing_positions: list[str] = []
        bad_positions: list[str] = []
        for item in neighbor["items"]:
            if not isinstance(item, dict):
                bad_positions.append("<non-object>")
                continue
            item_id = str(item.get("id", "<unknown>"))
            position = item.get("showroom_position")
            if not isinstance(position, dict):
                missing_positions.append(item_id)
                continue
            x = position.get("x")
            z = position.get("z")
            precision = position.get("precision")
            if not isinstance(x, (int, float)) or not isinstance(z, (int, float)):
                bad_positions.append(f"{item_id}.x/z")
                continue
            if not (-100 <= float(x) <= 100 and -100 <= float(z) <= 100):
                bad_positions.append(f"{item_id}.bounds")
            if precision not in {"current_project", "illustrative_relative"}:
                bad_positions.append(f"{item_id}.precision")
            if position.get("do_not_use_as_map_pin") is not True:
                bad_positions.append(f"{item_id}.map-pin-policy")
        if missing_positions:
            gate.fail("neighbor showroom positions", "missing: " + ", ".join(missing_positions[:12]))
        elif bad_positions:
            gate.fail("neighbor showroom positions", "invalid: " + ", ".join(bad_positions[:12]))
        else:
            gate.pass_("neighbor showroom positions", "all neighbor projects have bounded schematic positions")
    else:
        gate.fail("neighbor project layer", "missing")
    fake_pins = []
    for layer in layers:
        if not isinstance(layer, dict):
            continue
        for item in layer.get("items", []):
            if isinstance(item, dict) and item.get("map_status") == "needs_precise_pin" and ("lat" in item or "lng" in item):
                fake_pins.append(str(item.get("id", "<unknown>")))
    if fake_pins:
        gate.fail("environment pin honesty", f"unverified items include coordinates: {', '.join(fake_pins)}")
    else:
        gate.pass_("environment pin honesty", "no fake coordinates on needs_precise_pin items")


def check_material_intake(path: Path, gate: Gate) -> None:
    if not path.exists():
        gate.fail("material-intake-template.json", "missing")
        return
    intake = read_json(path)
    if not isinstance(intake, dict):
        gate.fail("material-intake-template.json", "root is not object")
        return
    required_root = ["project_slug", "post_id", "url_rules", "official_materials", "zillow_parity_map"]
    missing_root = [field for field in required_root if field not in intake]
    if missing_root:
        gate.fail("material intake root fields", "missing: " + ", ".join(missing_root))
    else:
        gate.pass_("material intake root fields", "present")

    rules = intake.get("url_rules", {})
    if isinstance(rules, dict) and rules.get("approved_https_only") is True and rules.get("no_stock_interiors") is True:
        gate.pass_("material intake URL rules", "approved HTTPS only + no stock interiors")
    else:
        gate.fail("material intake URL rules", "must require approved HTTPS and forbid stock interiors")

    materials = intake.get("official_materials", [])
    if not isinstance(materials, list) or len(materials) < 8:
        gate.fail("material intake items", f"{len(materials) if isinstance(materials, list) else 'invalid'} items; expected at least 8")
        materials = []
    else:
        gate.pass_("material intake items", f"{len(materials)} official/prototype material slots")

    allowed_status = {"provided_prototype", "pending_official", "owner_approval_required", "not_applicable"}
    item_errors: list[str] = []
    official_without_source: list[str] = []
    for item in materials:
        if not isinstance(item, dict):
            item_errors.append("<non-object item>")
            continue
        item_id = str(item.get("id", "<missing id>"))
        for field in ("id", "label", "cms_field", "accepted_formats", "current_status", "public_policy"):
            if not item.get(field):
                item_errors.append(f"{item_id}.{field}")
        status = str(item.get("current_status", ""))
        if status not in allowed_status:
            item_errors.append(f"{item_id}.current_status={status}")
        if status in {"official_ready", "approved"} and not item.get("source_url"):
            official_without_source.append(item_id)
    if item_errors:
        gate.fail("material intake item shape", ", ".join(item_errors[:12]))
    else:
        gate.pass_("material intake item shape", "all items have CMS field, status, formats and public policy")
    if official_without_source:
        gate.fail("material intake source proof", "official items missing source_url: " + ", ".join(official_without_source[:12]))

    parity = intake.get("zillow_parity_map", {})
    if isinstance(parity, dict) and all(key in parity for key in ("building_spin", "unit_picker", "floor_plans", "video_and_tour", "view_layer", "surroundings", "price_context", "lead_capture")):
        gate.pass_("material intake Zillow parity map", "core showroom capabilities mapped")
    else:
        gate.fail("material intake Zillow parity map", "missing one or more core capability mappings")


def check_view_layer(path: Path, expected_unit_count: int, gate: Gate) -> None:
    if not path.exists():
        gate.fail("view-layer-config.json", "missing")
        return
    config = read_json(path)
    if not isinstance(config, dict):
        gate.fail("view-layer-config.json", "root is not object")
        return

    center = config.get("project_center", {})
    if isinstance(center, dict) and isinstance(center.get("lat"), (int, float)) and isinstance(center.get("lng"), (int, float)):
        lat = float(center["lat"])
        lng = float(center["lng"])
        if -90 <= lat <= 90 and -180 <= lng <= 180:
            gate.pass_("view-layer project center", f"lat={lat}, lng={lng}, precision={center.get('precision', 'unknown')}")
        else:
            gate.fail("view-layer project center", f"out of range lat={lat}, lng={lng}")
    else:
        gate.fail("view-layer project center", "missing numeric lat/lng")

    providers = config.get("providers", {})
    mapbox = providers.get("mapbox", {}) if isinstance(providers, dict) else {}
    cesium = providers.get("cesium", {}) if isinstance(providers, dict) else {}
    if isinstance(mapbox, dict) and mapbox.get("load_policy") == "user_open_only" and mapbox.get("rtl_text_plugin_required") is True:
        gate.pass_("view-layer Mapbox policy", "user_open_only + RTL plugin required")
    else:
        gate.fail("view-layer Mapbox policy", "must be user_open_only and require RTL text plugin")
    if isinstance(cesium, dict) and cesium.get("load_policy") == "user_open_only":
        state = optional_https_url_state(cesium.get("tiles_url", ""))
        if state == "bad":
            gate.fail("view-layer Cesium tiles URL", "must be empty or HTTPS")
        elif state == "ok":
            gate.pass_("view-layer Cesium tiles URL", "approved HTTPS seam present")
        else:
            gate.warn("view-layer Cesium tiles URL", "pending approved tiles/config")
    else:
        gate.fail("view-layer Cesium policy", "must be user_open_only")

    cost = config.get("cost_controls", {})
    if (
        isinstance(cost, dict)
        and cost.get("instantiate_on_page_load") is False
        and cost.get("lazy_on_user_gesture") is True
        and cost.get("do_not_autoplay_tiles") is True
    ):
        gate.pass_("view-layer cost controls", "lazy/user-opened controls present")
    else:
        gate.fail("view-layer cost controls", "must prevent page-load map/tiles spend")

    unit_views = config.get("unit_views", [])
    if not isinstance(unit_views, list) or len(unit_views) != expected_unit_count:
        gate.fail("view-layer unit views", f"{len(unit_views) if isinstance(unit_views, list) else 'invalid'}; expected {expected_unit_count}")
    else:
        bad_units: list[str] = []
        for item in unit_views:
            if not isinstance(item, dict):
                bad_units.append("<non-object>")
                continue
            unit_id = str(item.get("unit_id", "<missing>"))
            bearing = item.get("bearing_degrees")
            altitude = item.get("altitude_m")
            if not isinstance(bearing, (int, float)) or not (0 <= float(bearing) <= 360):
                bad_units.append(f"{unit_id}.bearing")
            if not isinstance(altitude, (int, float)) or float(altitude) <= 0:
                bad_units.append(f"{unit_id}.altitude")
            if not item.get("source_note"):
                bad_units.append(f"{unit_id}.source_note")
        if bad_units:
            gate.fail("view-layer unit views", ", ".join(bad_units[:12]))
        else:
            gate.pass_("view-layer unit views", f"{len(unit_views)} units have altitude/bearing/source notes")

    overlays = config.get("overlays", [])
    if isinstance(overlays, list) and len(overlays) >= 3 and all(isinstance(item, dict) and item.get("render_policy") for item in overlays):
        gate.pass_("view-layer overlays", f"{len(overlays)} overlay policies")
    else:
        gate.fail("view-layer overlays", "missing source-aware overlay policies")


def fetch_healthcheck(url: str) -> dict | None:
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def version_tuple(value: object) -> tuple[int, ...]:
    parts: list[int] = []
    for part in str(value or "").split("."):
        if not part.isdigit():
            break
        parts.append(int(part))
    return tuple(parts)


def check_healthcheck(url: str, expect_live_glb: bool, require_plugin_stack: bool, gate: Gate) -> None:
    try:
        health = fetch_healthcheck(url)
    except Exception as exc:  # noqa: BLE001 - report network failure as warning for local asset gate.
        gate.warn("live healthcheck", f"could not fetch: {exc}")
        return
    if not isinstance(health, dict):
        gate.fail("live healthcheck", "unexpected response")
        return
    version = str(health.get("version", ""))
    project_3d = health.get("project_3d", {})
    assembly = health.get("project_page_assembly", {})
    parsed_version = version_tuple(version)
    if parsed_version >= (1, 63, 0):
        gate.pass_("live plugin version", version)
    else:
        gate.fail("live plugin version", f"{version} < 1.63.0")
    if isinstance(project_3d, dict) and project_3d.get("model_viewer_ready") is True:
        gate.pass_("model_viewer_ready", "true")
    else:
        gate.fail("model_viewer_ready", "not true")
    if require_plugin_stack:
        if parsed_version >= REQUIRED_PLUGIN_STACK_VERSION:
            gate.pass_("plugin stack version", version)
        else:
            gate.fail("plugin stack version", f"{version} < {REQUIRED_PLUGIN_STACK_LABEL}; deploy PRs #164, #165, #166 and #167 before CMS apply")
        if isinstance(project_3d, dict) and project_3d.get("unit_meta_rest") is True:
            gate.pass_("unit_meta_rest", "true")
        else:
            gate.fail("unit_meta_rest", "not true; v1.63.2 REST unit registration is required before automated unit write")
        if isinstance(project_3d, dict) and project_3d.get("floating_action_rail_v1633") is True:
            gate.pass_("floating_action_rail_v1633", "true")
        else:
            gate.fail("floating_action_rail_v1633", "not true; v1.63.3 contact rail clearance is required before showroom review")
        if isinstance(assembly, dict) and assembly.get("rainbow_seo_v1634") is True:
            gate.pass_("rainbow_seo_v1634", "true")
        else:
            gate.fail("rainbow_seo_v1634", "not true; v1.63.4 page SEO gate closure is required before showroom review")
    glb_count = project_3d.get("projects_with_glb") if isinstance(project_3d, dict) else None
    if expect_live_glb:
        if isinstance(glb_count, int) and glb_count >= 1:
            gate.pass_("projects_with_glb", str(glb_count))
        else:
            gate.fail("projects_with_glb", f"{glb_count}; expected >= 1 after CMS wire-in")
    else:
        gate.warn("projects_with_glb", f"{glb_count}; expected 0 until post-merge CMS wire-in")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT), help="Repository root")
    parser.add_argument("--project-slug", default=DEFAULT_PROJECT_SLUG, help="Asset folder under assets/projects/")
    parser.add_argument("--skip-live", action="store_true", help="Skip live healthcheck")
    parser.add_argument("--expect-live-glb", action="store_true", help="Require healthcheck projects_with_glb >= 1")
    parser.add_argument(
        "--require-plugin-stack",
        action="store_true",
        help="Require the deployed v1.63.1-v1.63.4 plugin markers before CMS apply.",
    )
    parser.add_argument("--check-remote-assets", action="store_true", help="Fetch raw/CDN asset URLs and verify signatures.")
    parser.add_argument(
        "--remote-ref",
        default="",
        help="For pre-merge QA only: fetch repository raw assets from this ref while keeping payload URLs durable.",
    )
    parser.add_argument("--healthcheck-url", default=DEFAULT_HEALTHCHECK)
    args = parser.parse_args()

    root = Path(args.root)
    asset_dir = root / "assets" / "projects" / args.project_slug
    gate = Gate()
    for filename, min_hebrew in PUBLIC_TEXT_MIN_HEBREW.items():
        check_text_sanity(asset_dir / filename, gate, min_hebrew)
    check_glb(asset_dir / "model.glb", gate)
    check_poster(asset_dir / "poster.png", gate)
    unit_count = check_meta(
        asset_dir / "project-meta-example.json",
        root,
        gate,
        check_remote_assets=args.check_remote_assets,
        remote_ref=args.remote_ref or None,
    )
    check_environment(asset_dir / "environment.json", gate)
    check_material_intake(asset_dir / "material-intake-template.json", gate)
    check_view_layer(asset_dir / "view-layer-config.json", unit_count, gate)
    if not args.skip_live:
        check_healthcheck(args.healthcheck_url, args.expect_live_glb, args.require_plugin_stack, gate)
    gate.print()
    return 1 if gate.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
