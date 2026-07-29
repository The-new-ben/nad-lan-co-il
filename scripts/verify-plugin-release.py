#!/usr/bin/env python3
"""Verify a nadlan-config release package before it is merged or deployed.

This is the companion gate for scripts/build-plugin-zip.py. It catches the
failure modes that have hurt the live site:

- plugin header, healthcheck versions, manifest version, and ZIP filename drift;
- manifest download_url pointing at the wrong artifact;
- Windows/backslash ZIP entries that create junk files on Linux/uPress;
- ZIPs that do not contain every tracked plugin source file under nadlan-config/.

Usage:
  python scripts/verify-plugin-release.py
  python scripts/verify-plugin-release.py 1.66.3
"""
from __future__ import annotations

import json
import os
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "nadlan-config"
DIST = ROOT / "plugin-dist"
MAIN = PLUGIN / "nadlan-config.php"
HEALTH = PLUGIN / "inc" / "health.php"
MANIFEST = DIST / "nadlan-config.json"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing file: {path.relative_to(ROOT)}")


def one_match(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        fail(f"could not find {label}")
    return match.group(1)


def detect_versions() -> dict[str, str]:
    main = read_text(MAIN)
    health = read_text(HEALTH) if HEALTH.exists() else ""
    constant = one_match(
        r"define\(\s*['\"]NADLAN_CONFIG_VERSION['\"]\s*,\s*['\"]([0-9][0-9.]*)['\"]\s*\)",
        main,
        "NADLAN_CONFIG_VERSION constant",
    )
    if not re.search(r"'version'\s*=>\s*NADLAN_CONFIG_VERSION\b", main):
        fail("main healthcheck does not use NADLAN_CONFIG_VERSION")
    versions = {
        "plugin_header": one_match(r"^\s*\*\s*Version:\s*([0-9][0-9.]*)", main, "plugin header Version"),
        "plugin_constant": constant,
        "healthcheck_main": constant,
    }
    if health:
        if not re.search(r"'version'\s*=>\s*defined\(\s*['\"]NADLAN_CONFIG_VERSION['\"]\s*\)\s*\?\s*NADLAN_CONFIG_VERSION", health):
            fail("health module does not use NADLAN_CONFIG_VERSION")
        versions["health_module"] = constant
    with MANIFEST.open(encoding="utf-8") as fh:
        manifest = json.load(fh)
    versions["manifest"] = str(manifest.get("version", ""))
    versions["manifest_download_url"] = str(manifest.get("download_url", ""))
    return versions


def expected_source_entries() -> set[str]:
    entries: set[str] = set()
    for path in sorted(PLUGIN.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(PLUGIN).as_posix()
        entries.add(f"nadlan-config/{rel}")
    return entries


def verify_zip(version: str) -> dict[str, object]:
    zip_path = DIST / f"nadlan-config-{version}.zip"
    if not zip_path.exists():
        fail(f"missing ZIP: {zip_path.relative_to(ROOT)}")
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if not names:
            fail("ZIP is empty")
        bad_backslash = [name for name in names if "\\" in name]
        bad_root = [name for name in names if not name.startswith("nadlan-config/")]
        crc = zf.testzip()
        if bad_backslash:
            fail(f"ZIP contains backslash paths, first={bad_backslash[0]}")
        if bad_root:
            fail(f"ZIP contains entries outside nadlan-config/, first={bad_root[0]}")
        if crc is not None:
            fail(f"ZIP CRC failed at {crc}")
        missing = sorted(expected_source_entries() - set(names))
        if missing:
            fail(f"ZIP is missing plugin source entries, first={missing[0]}, count={len(missing)}")
    return {
        "zip": zip_path.relative_to(ROOT).as_posix(),
        "entries": len(names),
        "backslash_paths": 0,
        "rooted": True,
        "crc": "ok",
    }


def main() -> None:
    versions = detect_versions()
    version = sys.argv[1] if len(sys.argv) > 1 else versions["plugin_header"]
    mismatches = {k: v for k, v in versions.items() if k != "manifest_download_url" and v != version}
    if mismatches:
        fail(f"version surfaces do not all equal {version}: {mismatches}")
    expected_url = (
        "https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/"
        f"plugin-dist/nadlan-config-{version}.zip"
    )
    if versions["manifest_download_url"] != expected_url:
        fail(
            "manifest download_url mismatch: "
            f"{versions['manifest_download_url']} != {expected_url}"
        )
    zip_result = verify_zip(version)
    print(json.dumps({
        "ok": True,
        "version": version,
        "versions": versions,
        "zip": zip_result,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
