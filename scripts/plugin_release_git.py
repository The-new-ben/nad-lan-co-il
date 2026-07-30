#!/usr/bin/env python3
"""Read deterministic plugin release inputs directly from the Git index.

The working tree is not a release byte source. On Windows, Git may materialize
text files with CRLF even though the reviewed blob is LF. WordPress runtime
integrity contracts hash raw bytes, so release archives must contain the exact
indexed blobs.
"""
from __future__ import annotations

import io
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


PLUGIN_PREFIX = "plugins/nadlan-config/"
ARCHIVE_ROOT = "nadlan-config/"
REGULAR_MODES = {"100644", "100755"}
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


class ReleaseInputError(RuntimeError):
    """The Git index cannot safely be used as a plugin release source."""


@dataclass(frozen=True)
class IndexedPluginBlob:
    repository_path: str
    archive_path: str
    mode: str
    oid: str
    data: bytes


def _git(root: Path, *args: str, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=root,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except FileNotFoundError as exc:
        raise ReleaseInputError("git is not available") from exc


def _git_ok(root: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    result = _git(root, *args, input_bytes=input_bytes)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise ReleaseInputError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout


def assert_no_unstaged_or_untracked_plugin_drift(root: Path) -> None:
    """Fail unless the plugin checkout is equivalent to its indexed state.

    Staged changes are allowed because the index blob is the reviewed candidate
    byte source. Unstaged and untracked plugin files are never silently omitted
    or substituted. A CRLF checkout that Git considers equivalent to an LF blob
    is safe because the archive is produced from the blob, not that checkout.
    """

    diff = _git(root, "diff", "--quiet", "--no-ext-diff", "--", "plugins/nadlan-config")
    if diff.returncode == 1:
        names = _git_ok(
            root,
            "diff",
            "--name-only",
            "--no-ext-diff",
            "--",
            "plugins/nadlan-config",
        ).decode("utf-8", "replace").splitlines()
        first = names[0] if names else "plugins/nadlan-config"
        raise ReleaseInputError(f"unstaged plugin drift detected: {first}")
    if diff.returncode != 0:
        detail = diff.stderr.decode("utf-8", "replace").strip()
        raise ReleaseInputError(f"could not inspect unstaged plugin drift: {detail}")

    untracked = _git_ok(
        root,
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
        "--",
        "plugins/nadlan-config",
    )
    if untracked:
        first = untracked.split(b"\0", 1)[0].decode("utf-8", "replace")
        raise ReleaseInputError(f"untracked plugin file detected: {first}")


def _indexed_metadata(root: Path) -> list[tuple[str, str, str]]:
    raw = _git_ok(
        root,
        "ls-files",
        "--stage",
        "-z",
        "--",
        "plugins/nadlan-config",
    )
    records: list[tuple[str, str, str]] = []
    seen_archive_paths: set[str] = set()
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            mode_bytes, oid_bytes, stage_bytes = metadata.split(b" ", 2)
        except ValueError as exc:
            raise ReleaseInputError("could not parse git ls-files output") from exc
        mode = mode_bytes.decode("ascii", "strict")
        oid = oid_bytes.decode("ascii", "strict")
        stage = stage_bytes.decode("ascii", "strict")
        path = raw_path.decode("utf-8", "surrogateescape")
        if stage != "0":
            raise ReleaseInputError(f"unmerged plugin index entry: {path}")
        if mode not in REGULAR_MODES:
            raise ReleaseInputError(f"unsupported plugin index mode {mode}: {path}")
        if not path.startswith(PLUGIN_PREFIX):
            raise ReleaseInputError(f"plugin index entry escaped expected prefix: {path}")
        relative = path[len(PLUGIN_PREFIX) :]
        pure = PurePosixPath(relative)
        if (
            not relative
            or pure.is_absolute()
            or "\\" in relative
            or any(part in ("", ".", "..") for part in pure.parts)
        ):
            raise ReleaseInputError(f"unsafe plugin index path: {path}")
        archive_path = ARCHIVE_ROOT + pure.as_posix()
        if archive_path in seen_archive_paths:
            raise ReleaseInputError(f"duplicate plugin archive path: {archive_path}")
        seen_archive_paths.add(archive_path)
        records.append((path, mode, oid))
    if not records:
        raise ReleaseInputError("Git index contains no nadlan-config plugin files")
    return sorted(records, key=lambda item: item[0].encode("utf-8", "surrogateescape"))


def _read_blobs(root: Path, oids: list[str]) -> dict[str, bytes]:
    unique_oids = list(dict.fromkeys(oids))
    request = b"".join(oid.encode("ascii") + b"\n" for oid in unique_oids)
    raw = _git_ok(root, "cat-file", "--batch", input_bytes=request)
    stream = io.BytesIO(raw)
    blobs: dict[str, bytes] = {}
    for requested_oid in unique_oids:
        header = stream.readline()
        if not header:
            raise ReleaseInputError(f"missing git cat-file response for {requested_oid}")
        fields = header.rstrip(b"\n").split(b" ")
        if len(fields) != 3 or fields[1] != b"blob":
            detail = header.decode("utf-8", "replace").strip()
            raise ReleaseInputError(f"unexpected git object response: {detail}")
        actual_oid = fields[0].decode("ascii", "strict")
        try:
            size = int(fields[2])
        except ValueError as exc:
            raise ReleaseInputError(f"invalid git blob size for {requested_oid}") from exc
        data = stream.read(size)
        terminator = stream.read(1)
        if len(data) != size or terminator != b"\n":
            raise ReleaseInputError(f"truncated git blob response for {requested_oid}")
        if actual_oid != requested_oid:
            raise ReleaseInputError(
                f"git returned {actual_oid} while {requested_oid} was requested"
            )
        blobs[requested_oid] = data
    if stream.read(1):
        raise ReleaseInputError("unexpected trailing bytes from git cat-file")
    return blobs


def indexed_plugin_blobs(
    root: Path,
    *,
    require_clean_checkout: bool = True,
) -> list[IndexedPluginBlob]:
    """Return the exact staged/committed plugin bytes in archive order."""

    root = root.resolve()
    if require_clean_checkout:
        assert_no_unstaged_or_untracked_plugin_drift(root)
    metadata = _indexed_metadata(root)
    data_by_oid = _read_blobs(root, [oid for _, _, oid in metadata])
    result: list[IndexedPluginBlob] = []
    for repository_path, mode, oid in metadata:
        relative = repository_path[len(PLUGIN_PREFIX) :]
        result.append(
            IndexedPluginBlob(
                repository_path=repository_path,
                archive_path=ARCHIVE_ROOT + relative,
                mode=mode,
                oid=oid,
                data=data_by_oid[oid],
            )
        )
    return result


def plugin_blob_map(
    root: Path,
    *,
    require_clean_checkout: bool = True,
) -> dict[str, IndexedPluginBlob]:
    return {
        item.archive_path: item
        for item in indexed_plugin_blobs(
            root,
            require_clean_checkout=require_clean_checkout,
        )
    }


def verify_archive_bytes(
    archive: Path,
    files: list[IndexedPluginBlob],
) -> dict[str, object]:
    """Prove archive membership, bytes, and normalized metadata."""

    expected = {item.archive_path: item for item in files}
    with zipfile.ZipFile(archive) as zf:
        infos = zf.infolist()
        names = [info.filename for info in infos]
        duplicate_count = len(names) - len(set(names))
        bad_backslash = [name for name in names if "\\" in name]
        bad_root = [name for name in names if not name.startswith(ARCHIVE_ROOT)]
        missing = sorted(set(expected) - set(names))
        extra = sorted(set(names) - set(expected))
        crc = zf.testzip()
        mismatches: list[str] = []
        metadata_mismatches: list[str] = []
        for info in infos:
            item = expected.get(info.filename)
            if item is None:
                continue
            if zf.read(info) != item.data:
                mismatches.append(info.filename)
            expected_mode = 0o100755 if item.mode == "100755" else 0o100644
            actual_mode = (info.external_attr >> 16) & 0xFFFF
            if (
                info.date_time != ZIP_TIMESTAMP
                or info.create_system != 3
                or actual_mode != expected_mode
                or info.extra
                or info.comment
            ):
                metadata_mismatches.append(info.filename)
        if (
            duplicate_count
            or bad_backslash
            or bad_root
            or missing
            or extra
            or crc is not None
            or mismatches
            or metadata_mismatches
            or zf.comment
        ):
            raise ReleaseInputError(
                "unsafe ZIP verification result: "
                f"duplicates={duplicate_count} backslash={len(bad_backslash)} "
                f"bad_root={len(bad_root)} missing={len(missing)} extra={len(extra)} "
                f"crc={crc} blob_mismatches={len(mismatches)} "
                f"metadata_mismatches={len(metadata_mismatches)} "
                f"archive_comment={bool(zf.comment)}"
            )
    return {
        "entries": len(files),
        "backslash_paths": 0,
        "rooted": True,
        "duplicates": 0,
        "crc": "ok",
        "missing_index_entries": 0,
        "extra_entries": 0,
        "git_blob_mismatches": 0,
        "metadata_mismatches": 0,
        "timestamp": "1980-01-01T00:00:00",
    }
