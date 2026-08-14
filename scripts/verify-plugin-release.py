#!/usr/bin/env python3
"""Verify a nadlan-config release package before merge or deployment.

The authoritative plugin source is the Git index, not platform-dependent
working-tree bytes. Every ZIP entry must exactly equal its indexed Git blob.
For UTOPIA, all twelve raw runtime pins - five articles, the GLB model, four
concept WebPs, project CSS, and project JavaScript - are checked against both
Git and ZIP bytes.

Usage:
  python scripts/verify-plugin-release.py
  python scripts/verify-plugin-release.py 1.72.136
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Optional

from plugin_release_git import (
    IndexedPluginBlob,
    ReleaseInputError,
    plugin_blob_map,
    verify_archive_bytes,
)


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "plugin-dist"
MANIFEST = DIST / "nadlan-config.json"
MAIN_ARCHIVE_PATH = "nadlan-config/nadlan-config.php"
HEALTH_ARCHIVE_PATH = "nadlan-config/inc/health.php"
UTOPIA_MODULE_ARCHIVE_PATH = "nadlan-config/inc/utopia-sde-dov.php"
UTOPIA_PROJECT_ARCHIVE_ROOT = (
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/"
)
UTOPIA_PINNED_PATHS = {
    "article_he": UTOPIA_PROJECT_ARCHIVE_ROOT + "article-he.html",
    "article_en": UTOPIA_PROJECT_ARCHIVE_ROOT + "article-en.html",
    "article_fr": UTOPIA_PROJECT_ARCHIVE_ROOT + "article-fr.html",
    "article_ru": UTOPIA_PROJECT_ARCHIVE_ROOT + "article-ru.html",
    "article_ar": UTOPIA_PROJECT_ARCHIVE_ROOT + "article-ar.html",
    "model": "nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb",
    "exterior": UTOPIA_PROJECT_ARCHIVE_ROOT + "utopia-concept-exterior-v1.webp",
    "interior": UTOPIA_PROJECT_ARCHIVE_ROOT + "utopia-concept-interior-v1.webp",
    "window_view": UTOPIA_PROJECT_ARCHIVE_ROOT + "utopia-concept-window-view-v1.webp",
    "wellness": UTOPIA_PROJECT_ARCHIVE_ROOT + "utopia-concept-wellness-v1.webp",
    "showroom_css": UTOPIA_PROJECT_ARCHIVE_ROOT + "utopia.css",
    "showroom_js": UTOPIA_PROJECT_ARCHIVE_ROOT + "utopia-showroom.js",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing file: {path.relative_to(ROOT)}")


def indexed_text(
    blobs: dict[str, IndexedPluginBlob],
    archive_path: str,
) -> str:
    try:
        return blobs[archive_path].data.decode("utf-8")
    except KeyError:
        fail(f"missing indexed plugin file: {archive_path}")
    except UnicodeDecodeError:
        fail(f"indexed plugin file is not valid UTF-8: {archive_path}")


def one_match(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        fail(f"could not find {label}")
    return match.group(1)


def optional_match(pattern: str, text: str) -> Optional[str]:
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1) if match else None


def resolve_health_version(text: str, label: str, constant_version: Optional[str]) -> str:
    expression = one_match(
        r"['\"]version['\"]\s*=>\s*([^,\r\n]+)",
        text,
        f"{label} version expression",
    ).strip()
    literal = re.fullmatch(r"['\"]([0-9][0-9.]*)['\"]", expression)
    if literal:
        return literal.group(1)
    if expression == "NADLAN_CONFIG_VERSION":
        if constant_version is None:
            fail(f"{label} uses undefined NADLAN_CONFIG_VERSION")
        return constant_version
    conditional_constant = re.fullmatch(
        r"defined\s*\(\s*['\"]NADLAN_CONFIG_VERSION['\"]\s*\)"
        r"\s*\?\s*NADLAN_CONFIG_VERSION\s*:\s*['\"]unknown['\"]",
        expression,
    )
    if conditional_constant:
        if constant_version is None:
            fail(f"{label} uses undefined NADLAN_CONFIG_VERSION")
        return constant_version
    fail(f"unsupported {label} version expression: {expression}")


def detect_versions(blobs: dict[str, IndexedPluginBlob]) -> dict[str, str]:
    main = indexed_text(blobs, MAIN_ARCHIVE_PATH)
    health = (
        indexed_text(blobs, HEALTH_ARCHIVE_PATH)
        if HEALTH_ARCHIVE_PATH in blobs
        else ""
    )
    constant_version = optional_match(
        r"define\s*\(\s*['\"]NADLAN_CONFIG_VERSION['\"]\s*,\s*['\"]([0-9][0-9.]*)['\"]\s*\)",
        main,
    )
    versions = {
        "plugin_header": one_match(
            r"^\s*\*\s*Version:\s*([0-9][0-9.]*)",
            main,
            "plugin header Version",
        ),
        "healthcheck_main": resolve_health_version(
            main,
            "main healthcheck",
            constant_version,
        ),
    }
    if constant_version is not None:
        versions["version_constant"] = constant_version
    if health:
        versions["health_module"] = resolve_health_version(
            health,
            "health module",
            constant_version,
        )
    with MANIFEST.open(encoding="utf-8") as fh:
        manifest = json.load(fh)
    versions["manifest"] = str(manifest.get("version", ""))
    versions["manifest_download_url"] = str(manifest.get("download_url", ""))
    return versions


def parse_utopia_integrity_pins(module: str) -> dict[str, str]:
    pins: dict[str, str] = {}
    for lang in ("he", "en", "fr", "ru", "ar"):
        pins[f"article_{lang}"] = one_match(
            rf"'{lang}'\s*=>\s*array\(\s*'sha256'\s*=>\s*'([0-9a-f]{{64}})'",
            module,
            f"UTOPIA article-{lang} SHA-256 pin",
        )
    for key in (
        "model",
        "exterior",
        "interior",
        "window_view",
        "wellness",
        "showroom_css",
        "showroom_js",
    ):
        pins[key] = one_match(
            rf"'{key}'\s*=>\s*array\(\s*'path'\s*=>[^,\r\n]+,\s*"
            rf"'sha256'\s*=>\s*'([0-9a-f]{{64}})'",
            module,
            f"UTOPIA {key} SHA-256 pin",
        )
    return pins


def verify_utopia_integrity_pins(
    blobs: dict[str, IndexedPluginBlob],
    zip_path: Path,
) -> dict[str, object]:
    module = indexed_text(blobs, UTOPIA_MODULE_ARCHIVE_PATH)
    pins = parse_utopia_integrity_pins(module)
    results: dict[str, dict[str, object]] = {}
    with zipfile.ZipFile(zip_path) as zf:
        for key, archive_path in UTOPIA_PINNED_PATHS.items():
            if archive_path not in blobs:
                fail(f"missing indexed UTOPIA pinned asset: {archive_path}")
            git_bytes = blobs[archive_path].data
            try:
                zip_bytes = zf.read(archive_path)
            except KeyError:
                fail(f"missing ZIP UTOPIA pinned asset: {archive_path}")
            git_sha = hashlib.sha256(git_bytes).hexdigest()
            zip_sha = hashlib.sha256(zip_bytes).hexdigest()
            pin = pins[key]
            if git_sha != pin:
                fail(
                    f"UTOPIA integrity pin does not match Git blob for {key}: "
                    f"{pin} != {git_sha}"
                )
            if zip_sha != pin:
                fail(
                    f"UTOPIA integrity pin does not match ZIP bytes for {key}: "
                    f"{pin} != {zip_sha}"
                )
            results[key] = {
                "path": archive_path,
                "sha256": pin,
                "git_blob_match": True,
                "zip_entry_match": True,
            }
    return {
        "count": len(results),
        "all_match_git_blobs": True,
        "all_match_zip_entries": True,
        "pins": results,
    }


def verify_utopia_release_markers(
    blobs: dict[str, IndexedPluginBlob],
    plugin_version: str,
) -> dict[str, object]:
    module = indexed_text(blobs, UTOPIA_MODULE_ARCHIVE_PATH)
    release_literals = sorted(set(re.findall(r"\b1\.72\.\d+\b", module)))
    option_markers = sorted(set(re.findall(r"\bv172\d+\b", module)))
    if len(release_literals) != 1:
        fail(
            "UTOPIA must have exactly one internally coherent release literal: "
            f"{release_literals}"
        )
    module_version = release_literals[0]
    compact = module_version.replace(".", "")
    expected_option_marker = f"v{compact}"
    if option_markers != [expected_option_marker]:
        fail(
            "UTOPIA option/function markers do not exclusively use "
            f"{expected_option_marker}: {option_markers}"
        )
    seed_function = f"nadlan_utopia_seed_{expected_option_marker}"
    if f"function {seed_function}(" not in module:
        fail(f"missing UTOPIA seed function for {module_version}")
    if (
        f"add_action( 'init', '{seed_function}', 40 );"
        not in module
    ):
        fail(f"missing UTOPIA init seed hook for {module_version}")
    return {
        "module_release": module_version,
        "plugin_release": plugin_version,
        "module_release_is_independent": module_version != plugin_version,
        "release_literal_occurrences": len(
            re.findall(rf"\b{re.escape(module_version)}\b", module)
        ),
        "option_marker": expected_option_marker,
        "option_marker_occurrences": module.count(expected_option_marker),
        "seed_function": seed_function,
    }


def verify_source_syntax(zip_path: Path) -> dict[str, int]:
    """Lint the exact archive bytes after Git-index parity is established."""
    php = shutil.which("php")
    node = shutil.which("node")
    if not php or not node:
        fail("php and node executables are required for complete source syntax checks")
    with tempfile.TemporaryDirectory(prefix="nadlan-plugin-verify-") as temp_dir:
        root = Path(temp_dir)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(root)
        plugin = root / "nadlan-config"
        php_files = sorted(plugin.rglob("*.php"))
        js_files = sorted(plugin.rglob("*.js"))
        for path in php_files:
            result = subprocess.run(
                [php, "-l", str(path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode != 0:
                detail = (result.stderr or result.stdout).strip().splitlines()
                fail(f"PHP lint failed for {path.relative_to(root)}: {detail[-1] if detail else 'unknown error'}")
        for path in js_files:
            result = subprocess.run(
                [node, "--check", str(path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode != 0:
                detail = (result.stderr or result.stdout).strip().splitlines()
                fail(f"JavaScript syntax failed for {path.relative_to(root)}: {detail[-1] if detail else 'unknown error'}")
    return {"php_files": len(php_files), "js_files": len(js_files)}


def verify_zip(
    version: str,
    blobs: dict[str, IndexedPluginBlob],
) -> tuple[dict[str, object], Path]:
    zip_path = DIST / f"nadlan-config-{version}.zip"
    if not zip_path.exists():
        fail(f"missing ZIP: {zip_path.relative_to(ROOT)}")
    try:
        result = verify_archive_bytes(zip_path, list(blobs.values()))
    except ReleaseInputError as exc:
        fail(str(exc))
    return {
        "zip": zip_path.relative_to(ROOT).as_posix(),
        **result,
    }, zip_path


def main() -> None:
    try:
        blobs = plugin_blob_map(ROOT)
    except ReleaseInputError as exc:
        fail(str(exc))
    versions = detect_versions(blobs)
    version = sys.argv[1] if len(sys.argv) > 1 else versions["plugin_header"]
    mismatches = {
        key: value
        for key, value in versions.items()
        if key != "manifest_download_url" and value != version
    }
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
    markers = verify_utopia_release_markers(blobs, version)
    zip_result, zip_path = verify_zip(version, blobs)
    syntax = verify_source_syntax(zip_path)
    integrity = verify_utopia_integrity_pins(blobs, zip_path)
    print(
        json.dumps(
            {
                "ok": True,
                "version": version,
                "versions": versions,
                "utopia_release_markers": markers,
                "utopia_integrity_pins": integrity,
                "syntax": syntax,
                "zip": zip_result,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
