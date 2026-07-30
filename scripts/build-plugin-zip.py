#!/usr/bin/env python3
"""Build a deterministic nadlan-config ZIP from exact Git index blobs.

Windows checkouts may contain CRLF bytes while the reviewed Git blobs contain
LF. UTOPIA validates raw article, CSS, and JavaScript hashes at runtime, so the
working tree must never be the release byte source.

Usage:  python scripts/build-plugin-zip.py            # uses indexed Version
        python scripts/build-plugin-zip.py 1.72.136    # explicit version
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path

from plugin_release_git import (
    ZIP_TIMESTAMP,
    IndexedPluginBlob,
    ReleaseInputError,
    indexed_plugin_blobs,
    verify_archive_bytes,
)


ROOT = Path(__file__).resolve().parents[1]
DIST_RELATIVE = Path("plugin-dist")
MAIN_ARCHIVE_PATH = "nadlan-config/nadlan-config.php"


class BuildError(RuntimeError):
    """The release archive could not be built safely."""


def _indexed_version(files: list[IndexedPluginBlob]) -> str:
    by_archive_path = {item.archive_path: item for item in files}
    try:
        main = by_archive_path[MAIN_ARCHIVE_PATH].data.decode("utf-8")
    except KeyError as exc:
        raise BuildError(f"missing indexed plugin main file: {MAIN_ARCHIVE_PATH}") from exc
    except UnicodeDecodeError as exc:
        raise BuildError("indexed plugin main file is not valid UTF-8") from exc
    match = re.search(r"^\s*\*\s*Version:\s*([0-9][0-9.]*)", main, re.MULTILINE)
    if not match:
        raise BuildError("could not detect Version: header in indexed plugin main file")
    return match.group(1)


def detect_version(root: Path = ROOT) -> str:
    return _indexed_version(indexed_plugin_blobs(root))


def _zip_info(item: IndexedPluginBlob) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(item.archive_path, date_time=ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    permissions = 0o755 if item.mode == "100755" else 0o644
    info.external_attr = (0o100000 | permissions) << 16
    info.internal_attr = 0
    info.extra = b""
    info.comment = b""
    return info


def build(version: str | None = None, root: Path = ROOT) -> Path:
    root = root.resolve()
    files = indexed_plugin_blobs(root)
    indexed_version = _indexed_version(files)
    version = version or indexed_version
    if version != indexed_version:
        raise BuildError(
            f"requested version {version} does not match indexed plugin version {indexed_version}"
        )
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)+", version):
        raise BuildError(f"unsafe release version: {version}")

    dist = root / DIST_RELATIVE
    dist.mkdir(parents=True, exist_ok=True)
    output = dist / f"nadlan-config-{version}.zip"
    if output.exists():
        raise BuildError(
            f"refusing to overwrite immutable release artifact: {output.relative_to(root)}"
        )

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".nadlan-config-{version}-",
            suffix=".zip.tmp",
            dir=dist,
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
        with zipfile.ZipFile(
            temporary_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
            allowZip64=True,
        ) as zf:
            for item in files:
                zf.writestr(
                    _zip_info(item),
                    item.data,
                    compress_type=zipfile.ZIP_DEFLATED,
                    compresslevel=9,
                )
            zf.comment = b""
        try:
            result = verify_archive_bytes(temporary_path, files)
        except ReleaseInputError as exc:
            raise BuildError(str(exc)) from exc
        os.replace(temporary_path, output)
        temporary_path = None
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(
        f"OK {output.name} entries={result['entries']} sha256={digest} "
        "git_blob_mismatches=0 deterministic_metadata=True"
    )
    return output


def main() -> None:
    version = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        build(version)
    except (BuildError, ReleaseInputError) as exc:
        print(f"REJECTED: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
