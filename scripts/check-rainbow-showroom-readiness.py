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
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HEALTHCHECK = "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck"
MAX_GLB_BYTES = 4 * 1024 * 1024
MAX_POSTER_BYTES = 80 * 1024


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


def check_meta(path: Path, gate: Gate) -> None:
    if not path.exists():
        gate.fail("project-meta-example.json", "missing")
        return
    meta = read_json(path)
    if not isinstance(meta, dict):
        gate.fail("project-meta-example.json", "root is not object")
        return
    for field in ["project_model_glb", "project_model_poster", "project_3d_units"]:
        if field in meta:
            gate.pass_(field, "present")
        else:
            gate.fail(field, "missing from CMS payload")
    for field in ["project_model_glb", "project_model_poster"]:
        value = str(meta.get(field, ""))
        if "raw.githubusercontent.com/The-new-ben/nad-lan-co-il/" in value and "/main/" not in value:
            gate.fail(field, "raw GitHub asset URL must point at main after merge, not a draft branch")
        elif value:
            gate.pass_(f"{field} URL durability", "main raw URL or custom hosted URL")
    units = meta.get("project_3d_units", [])
    if isinstance(units, list) and units:
        gate.pass_("project_3d_units count", str(len(units)))
    else:
        gate.fail("project_3d_units count", "missing or empty")
        units = []
    required_unit_fields = ["id", "floor", "hotspot_position", "hotspot_normal", "source_note"]
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
    env = meta.get("project_3d_environment_json")
    if isinstance(env, dict):
        layers = env.get("layers", [])
        if isinstance(layers, list) and layers:
            gate.pass_("project_3d_environment_json", f"{len(layers)} layers")
        else:
            gate.fail("project_3d_environment_json", "missing layers")
    else:
        gate.fail("project_3d_environment_json", "missing from CMS payload")


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


def fetch_healthcheck(url: str) -> dict | None:
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def check_healthcheck(url: str, expect_live_glb: bool, gate: Gate) -> None:
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
    if version >= "1.63.0":
        gate.pass_("live plugin version", version)
    else:
        gate.fail("live plugin version", f"{version} < 1.63.0")
    if isinstance(project_3d, dict) and project_3d.get("model_viewer_ready") is True:
        gate.pass_("model_viewer_ready", "true")
    else:
        gate.fail("model_viewer_ready", "not true")
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
    parser.add_argument("--skip-live", action="store_true", help="Skip live healthcheck")
    parser.add_argument("--expect-live-glb", action="store_true", help="Require healthcheck projects_with_glb >= 1")
    parser.add_argument("--healthcheck-url", default=DEFAULT_HEALTHCHECK)
    args = parser.parse_args()

    root = Path(args.root)
    asset_dir = root / "assets" / "projects" / "rainbow-tel-aviv"
    gate = Gate()
    check_glb(asset_dir / "model.glb", gate)
    check_poster(asset_dir / "poster.png", gate)
    check_meta(asset_dir / "project-meta-example.json", gate)
    check_environment(asset_dir / "environment.json", gate)
    if not args.skip_live:
        check_healthcheck(args.healthcheck_url, args.expect_live_glb, gate)
    gate.print()
    return 1 if gate.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
