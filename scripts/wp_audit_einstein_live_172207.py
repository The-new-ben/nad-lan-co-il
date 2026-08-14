#!/usr/bin/env python3
"""Governed Phase-A audit of the unknown live nadlan-config 1.72.207 tree.

This reviewed phase permits only ``audit`` and ``cleanup-helper``. ``audit``
creates one temporary, admin-gated Code Snippets helper and performs two stable
read-only audits. It emits the complete observed baseline for independent
review. Snapshot creation and download are structurally unavailable until a
separate commit embeds that exact reviewed contract and explicitly enables the
Phase-B commands. ``cleanup-helper`` removes only this vehicle's exact helper
after reserving durable terminal evidence, then proves absence.

This vehicle never adopts, resumes, changes, or deletes retained run 4527b2.
Credentials and the generated route token are read only from memory and are
never included in reports, URLs, command output, or repository source. The
token exists only inside the temporary live helper until that row is deleted.
"""

from __future__ import annotations

import argparse
import base64
import contextlib
import datetime as dt
import hashlib
import hmac
import importlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any, Iterable
from urllib.parse import urlsplit
import zipfile


REPO_ROOT = Path(__file__).resolve().parents[1]
DRIVER_PATH = Path(__file__).resolve()
TEMPLATE_PATH = (
    REPO_ROOT / "scripts" / "templates" / "nadlan-einstein-live-recovery-helper.php.tpl"
)
SOURCE_PATHS = (DRIVER_PATH, TEMPLATE_PATH, REPO_ROOT / ".gitattributes")
SOURCE_REPO_PATHS = tuple(
    path.relative_to(REPO_ROOT).as_posix() for path in SOURCE_PATHS
)
RUN_ID = "einstein-flagship-20260814T124439Z-4527b2"
ROUTE_NAMESPACE = "nadlan-live-recovery/v1"
TOKEN_ENV = "NADLAN_EINSTEIN_RECOVERY_TOKEN"
SNAPSHOT_ACTIONS_ENABLED = False
PINNED_EXPECTED_LIVE_CONTRACT: dict[str, Any] | None = None
PINNED_EXPECTED_LIVE_CONTRACT_SHA256 = ""
TEMPLATE_SHA256 = "c3fdf588027bb5be6bb9ddfde3ecc1e1e4618f2e599ababab6d6eb1b83c12e17"
EXPECTED_RAW_META_MAP_SHA256 = (
    "cc0fd63af6f339e70115231f0bfacf62e3f37628ed0abd45a4b0d8fa76a1ee48"
)
EXPECTED_CANONICAL_STORAGE_SHA256 = (
    "8e502f9d598fcd2521290ae929d95a0662c90ef965ee0bbc416b772c0d49750b"
)
EXPECTED_HELPERS = {
    "449": {
        "id": 449,
        "name": "x-einstein-private-stage-direct-route-6885-32",
        "scope": "global",
        "active": True,
        "code_sha256": (
            "dbe87ddc2bd1a5055e0fe75f2aff134ddb04bd327a5f9715981408fe403677a8"
        ),
        "exact": True,
    },
    "450": {
        "id": 450,
        "name": "x-einstein-flagship-20260814T124439Z-4527b2",
        "scope": "global",
        "active": True,
        "code_sha256": (
            "3a365295c1122fdccacc397d0f93e31ee694ec432513616f26490a7c6c5aa449"
        ),
        "exact": True,
    },
}
HASH_RE = re.compile(r"[a-f0-9]{64}\Z")
COMMIT_RE = re.compile(r"[a-f0-9]{40}\Z")
MARKER_RE = re.compile(r"__[A-Z0-9_]+__")
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
MAX_TREE_BYTES = 64 * 1024 * 1024
MAX_FILE_BYTES = 25 * 1024 * 1024
MAX_FILES = 1024
CHUNK_BYTES = 64 * 1024
MISSING_SNIPPET_CODE = "rest_cannot_get"
MISSING_SNIPPET_MESSAGE = "The snippet could not be found."

_REQUESTS: Any | None = None


class RecoveryHold(RuntimeError):
    """A fail-closed state that requires review but not a destructive retry."""


class NetworkRequestFailed(RuntimeError):
    """A sanitized requests transport failure."""


def requests_module() -> Any:
    global _REQUESTS
    if _REQUESTS is None:
        try:
            _REQUESTS = importlib.import_module("requests")
        except ModuleNotFoundError as error:
            raise RuntimeError(
                "Live actions require the optional 'requests' package"
            ) from error
    return _REQUESTS


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def exact_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=False
    ).encode("utf-8")


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_lf_source_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError(f"Source has a UTF-8 BOM: {path.name}")
    if b"\r" in raw:
        raise RuntimeError(f"Source is not canonical LF: {path.name}")
    if not raw.endswith(b"\n"):
        raise RuntimeError(f"Source lacks a final LF: {path.name}")
    raw.decode("utf-8")
    return raw


def read_env(path: Path | None) -> dict[str, str]:
    values: dict[str, str] = {}
    if path is None:
        return values
    if not path.is_file():
        raise RuntimeError("Explicit credential environment file is unavailable")
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        values[key.strip()] = value
    return values


class Redactor:
    def __init__(
        self,
        secret_values: Iterable[str],
        identifier_values: Iterable[str] = (),
    ):
        self.secret_values = tuple(
            sorted({value for value in secret_values if value}, key=len, reverse=True)
        )
        self.identifier_literals = tuple(
            json.dumps(value, ensure_ascii=False)
            for value in sorted(
                {value for value in identifier_values if value}, key=len, reverse=True
            )
        )

    def assert_absent(self, text: str) -> None:
        if any(value in text for value in self.secret_values) or any(
            literal in text for literal in self.identifier_literals
        ):
            raise RuntimeError("Credential/token redaction assertion failed")


def resolve_runtime(
    env_file: Path | None,
) -> tuple[str, str, str, str, Redactor]:
    file_values = read_env(env_file)

    def value(name: str) -> str:
        return str(os.environ.get(name) or file_values.get(name) or "").strip()

    base_url = value("WP_BASE_URL").rstrip("/")
    user = value("WP_USER")
    password = value("WP_APP_PASSWORD")
    token = str(os.environ.get(TOKEN_ENV) or "").strip()
    parsed = urlsplit(base_url)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "nad-lan.co.il"
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or parsed.path not in ("", "/")
    ):
        raise RuntimeError(
            "WP_BASE_URL must be exactly the canonical HTTPS site origin"
        )
    if not user or not password:
        raise RuntimeError("Current WordPress credentials are unavailable")
    if not re.fullmatch(r"[a-f0-9]{64}", token):
        raise RuntimeError(
            f"{TOKEN_ENV} must be a caller-held 64-character lowercase hex token"
        )
    return (
        base_url,
        user,
        password,
        token,
        Redactor((password, token), identifier_values=(user,)),
    )


def run_git(*args: str, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
    )
    return completed.stdout


def fresh_main_authority(
    head: str, *, process_runner: Any = subprocess.run
) -> str:
    """Fetch and authorize only against the just-resolved FETCH_HEAD commit."""

    fetch_command = [
        "git",
        "fetch",
        "--no-tags",
        "--no-recurse-submodules",
        "origin",
        "main",
    ]
    fetch = process_runner(
        fetch_command,
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if fetch.returncode != 0:
        raise RuntimeError("Fresh protected-main fetch failed")
    resolved = process_runner(
        ["git", "rev-parse", "--verify", "FETCH_HEAD^{commit}"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    fetched_main = str(resolved.stdout or "").strip().lower()
    if resolved.returncode != 0 or not COMMIT_RE.fullmatch(fetched_main):
        raise RuntimeError("Fresh FETCH_HEAD commit could not be resolved exactly")
    ancestor = process_runner(
        ["git", "merge-base", "--is-ancestor", head, fetched_main],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=False,
        check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError(
            "Recovery source commit is not contained in freshly fetched main"
        )
    return fetched_main


def source_facts(expected_commit: str, *, require_main: bool = True) -> dict[str, Any]:
    if not COMMIT_RE.fullmatch(expected_commit):
        raise RuntimeError("Expected source commit must be a full lowercase SHA-1")
    head = str(run_git("rev-parse", "HEAD")).strip().lower()
    if head != expected_commit:
        raise RuntimeError("Checked-out source commit differs from the approved commit")
    status = str(
        run_git(
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--",
            *SOURCE_REPO_PATHS,
        )
    )
    if status.strip():
        raise RuntimeError("Recovery source files are dirty or untracked")
    files: dict[str, dict[str, Any]] = {}
    for disk_path, repo_path in zip(SOURCE_PATHS, SOURCE_REPO_PATHS):
        disk_bytes = read_lf_source_bytes(disk_path)
        committed = run_git("show", f"{head}:{repo_path}", binary=True)
        if not isinstance(committed, bytes) or committed != disk_bytes:
            raise RuntimeError(f"Committed source bytes differ: {repo_path}")
        files[repo_path] = {
            "sha256": sha256_bytes(disk_bytes),
            "bytes": len(disk_bytes),
            "canonical_lf": True,
        }
    if files[SOURCE_REPO_PATHS[1]]["sha256"] != TEMPLATE_SHA256:
        raise RuntimeError("Recovery helper template source hash drifted")
    fresh_main_commit = fresh_main_authority(head) if require_main else None
    return {
        "commit": head,
        "contained_in_fresh_main": require_main,
        "fresh_main_commit": fresh_main_commit,
        "files": files,
    }


def session_identity(token: str) -> dict[str, str]:
    suffix = hashlib.sha256(f"{RUN_ID}|{token}".encode()).hexdigest()[:12]
    storage_hash = hashlib.sha256(f"{RUN_ID}|{token}|storage".encode()).hexdigest()[:32]
    return {
        "helper_name": f"x-einstein-live-recovery-172207-{suffix}",
        "route_path": f"/einstein-live-recovery-172207-{suffix}",
        "route": f"{ROUTE_NAMESPACE}/einstein-live-recovery-172207-{suffix}",
        "storage_slug": f".nadlan-live-recovery-{storage_hash}",
    }


def render_helper(
    *, token: str, helper_id: int, source_commit: str
) -> tuple[str, dict[str, str]]:
    template_bytes = read_lf_source_bytes(TEMPLATE_PATH)
    if sha256_bytes(template_bytes) != TEMPLATE_SHA256:
        raise RuntimeError("Recovery helper template hash drifted")
    identity = session_identity(token)
    replacements = {
        "__ROUTE_PATH_JSON__": json.dumps(identity["route_path"]),
        "__TOKEN_JSON__": json.dumps(token),
        "__RUN_ID_JSON__": json.dumps(RUN_ID),
        "__HELPER_ID_INT__": str(int(helper_id)),
        "__HELPER_NAME_JSON__": json.dumps(identity["helper_name"]),
        "__SOURCE_COMMIT_JSON__": json.dumps(source_commit),
        "__STORAGE_SLUG_JSON__": json.dumps(identity["storage_slug"]),
        "__SNAPSHOT_ACTIONS_ENABLED_BOOL__": (
            "true" if SNAPSHOT_ACTIONS_ENABLED else "false"
        ),
        "__EXPECTED_LIVE_CONTRACT_JSON__": json.dumps(
            PINNED_EXPECTED_LIVE_CONTRACT,
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        "__EXPECTED_LIVE_CONTRACT_SHA256_JSON__": json.dumps(
            PINNED_EXPECTED_LIVE_CONTRACT_SHA256
        ),
    }
    rendered = template_bytes.decode("utf-8")
    for marker, replacement in replacements.items():
        if rendered.count(marker) != 1:
            raise RuntimeError(f"Helper template marker count changed: {marker}")
        rendered = rendered.replace(marker, replacement)
    leftovers = MARKER_RE.findall(rendered)
    if leftovers or "\r" in rendered or not rendered.endswith("\n"):
        raise RuntimeError("Rendered helper source contract is invalid")
    return rendered, identity


def observed_snippet(payload: dict[str, Any]) -> dict[str, Any]:
    code = payload.get("code")
    if not isinstance(code, str):
        raise RuntimeError("Snippet response omits source code")
    return {
        "id": int(payload.get("id") or 0),
        "name": str(payload.get("name") or ""),
        "active": payload.get("active") is True,
        "scope": str(payload.get("scope") or ""),
        "code_sha256": sha256_bytes(code.encode("utf-8")),
    }


class WordpressClient:
    def __init__(
        self,
        base_url: str,
        user: str,
        password: str,
        *,
        session: Any | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests_module().Session()
        self.session.auth = (user, password)
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "NadLan-Einstein-Live-Recovery/1.0",
            }
        )

    @staticmethod
    def is_host_html_403(response: Any) -> bool:
        content_type = str(response.headers.get("Content-Type") or "").lower()
        prefix = response.content[:512].lower()
        return (
            response.status_code == 403
            and "json" not in content_type
            and (b"<html" in prefix or b"<!doctype" in prefix)
        )

    def request(
        self,
        method: str,
        route: str,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 60,
    ) -> Any:
        normalized = route.lstrip("/")
        try:
            response = self.session.request(
                method,
                f"{self.base_url}/wp-json/{normalized}",
                json=json_body,
                params=params,
                headers=headers,
                timeout=timeout,
            )
        except Exception as error:
            module = _REQUESTS
            if module is not None and isinstance(error, module.RequestException):
                raise NetworkRequestFailed(
                    "Authenticated network request failed"
                ) from error
            raise
        if self.is_host_html_403(response):
            fallback_params = {"rest_route": f"/{normalized}"}
            if params:
                fallback_params.update(params)
            try:
                response = self.session.request(
                    method,
                    f"{self.base_url}/",
                    json=json_body,
                    params=fallback_params,
                    headers=headers,
                    timeout=timeout,
                )
            except Exception as error:
                module = _REQUESTS
                if module is not None and isinstance(error, module.RequestException):
                    raise NetworkRequestFailed(
                        "Authenticated fallback network request failed"
                    ) from error
                raise
        return response

    def all_snippets(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        page = 1
        total_pages = 1
        while page <= total_pages:
            response = self.request(
                "GET",
                "code-snippets/v1/snippets",
                params={"per_page": 100, "page": page},
                timeout=60,
            )
            if not 200 <= response.status_code < 300:
                raise RuntimeError("Code Snippets collection read failed")
            try:
                payload = response.json()
            except ValueError as error:
                raise RuntimeError("Code Snippets collection is not JSON") from error
            if not isinstance(payload, list):
                raise RuntimeError("Code Snippets collection has an invalid shape")
            rows.extend(row for row in payload if isinstance(row, dict))
            total_pages = int(response.headers.get("X-WP-TotalPages", "1") or "1")
            if total_pages < 1 or total_pages > 100:
                raise RuntimeError("Code Snippets pagination is outside its bound")
            page += 1
        return rows


def require_object(response: Any, label: str) -> dict[str, Any]:
    if not 200 <= response.status_code < 300:
        code = "unknown"
        try:
            payload = response.json()
            if isinstance(payload, dict):
                code = str(payload.get("code") or "unknown")
        except ValueError:
            code = "non_json"
        raise RuntimeError(f"{label} failed ({response.status_code}, {code})")
    try:
        payload = response.json()
    except ValueError as error:
        raise RuntimeError(f"{label} did not return JSON") from error
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label} returned an invalid JSON shape")
    return payload


def is_exact_missing_snippet(response: Any) -> bool:
    if response.status_code not in (404, 500):
        return False
    try:
        payload = response.json()
    except ValueError:
        return False
    if not isinstance(payload, dict):
        return False
    if response.status_code == 500:
        return (
            payload.get("code") == MISSING_SNIPPET_CODE
            and payload.get("message") == MISSING_SNIPPET_MESSAGE
        )
    return payload.get("code") in {MISSING_SNIPPET_CODE, "rest_post_invalid_id"}


def is_exact_missing_route(response: Any) -> bool:
    if response.status_code != 404:
        return False
    try:
        payload = response.json()
    except ValueError:
        return False
    return isinstance(payload, dict) and payload.get("code") == "rest_no_route"


def helper_expected(
    helper_id: int, helper_code: str, identity: dict[str, str], *, active: bool
) -> dict[str, Any]:
    return {
        "id": helper_id,
        "name": identity["helper_name"],
        "active": active,
        "scope": "global",
        "code_sha256": sha256_bytes(helper_code.encode("utf-8")),
    }


def inspect_owned_helper(
    client: WordpressClient,
    *,
    identity: dict[str, str],
    token: str,
    helper_id: int,
    helper_code: str,
) -> dict[str, Any]:
    rows = client.all_snippets()
    matches = [
        row
        for row in rows
        if str(row.get("name") or "") == identity["helper_name"]
        or (helper_id > 0 and int(row.get("id") or 0) == helper_id)
    ]
    unique_ids = {int(row.get("id") or 0) for row in matches}
    if len(unique_ids) > 1:
        return {"state": "uncertain_multiple_rows", "safe_to_mutate": False}
    if not matches:
        item_absent = helper_id <= 0
        if helper_id > 0:
            item_response = client.request(
                "GET", f"code-snippets/v1/snippets/{helper_id}", timeout=60
            )
            item_absent = is_exact_missing_snippet(item_response)
        route_response = call_helper(
            client,
            route=identity["route"],
            token=token,
            helper_sha256="0" * 64,
            action="storage_status",
        )
        return {
            "state": (
                "absent"
                if item_absent and is_exact_missing_route(route_response)
                else "uncertain"
            ),
            "item_absent": item_absent,
            "collection_absent": True,
            "route_absent": is_exact_missing_route(route_response),
            "safe_to_mutate": False,
        }
    observed_id = next(iter(unique_ids))
    response = client.request(
        "GET", f"code-snippets/v1/snippets/{observed_id}", timeout=60
    )
    payload = require_object(response, "Owned recovery helper inspection")
    observed = observed_snippet(payload)
    placeholder = f"/* inactive placeholder for {identity['helper_name']} */"
    allowed = [
        {
            "label": "exact_inactive_placeholder",
            "expected": {
                "id": observed_id,
                "name": identity["helper_name"],
                "active": False,
                "scope": "global",
                "code_sha256": sha256_bytes(placeholder.encode("utf-8")),
            },
        }
    ]
    if helper_code:
        allowed.extend(
            {
                "label": f"exact_{'active' if active else 'inactive'}_helper",
                "expected": helper_expected(
                    observed_id, helper_code, identity, active=active
                ),
            }
            for active in (False, True)
        )
    for candidate in allowed:
        if observed == candidate["expected"]:
            return {
                "state": candidate["label"],
                "helper": observed,
                "safe_to_delete": True,
                "safe_to_self_delete": observed["active"] is True,
            }
    return {"state": "drifted", "helper": observed, "safe_to_mutate": False}


def verify_helper_row(
    client: WordpressClient,
    helper_id: int,
    expected: dict[str, Any],
) -> dict[str, Any]:
    response = client.request(
        "GET", f"code-snippets/v1/snippets/{helper_id}", timeout=60
    )
    payload = require_object(response, "Recovery helper read")
    observed = observed_snippet(payload)
    if observed != expected:
        raise RuntimeError("Recovery helper identity, state, or code hash changed")
    return observed


def call_helper(
    client: WordpressClient,
    *,
    route: str,
    token: str,
    helper_sha256: str,
    action: str,
    extra: dict[str, Any] | None = None,
    timeout: int = 180,
) -> Any:
    body: dict[str, Any] = {
        "helper_sha256": helper_sha256,
        "action": action,
    }
    if extra:
        body.update(extra)
    return client.request(
        "POST",
        route,
        json_body=body,
        headers={"X-Nadlan-Recovery-Token": token},
        timeout=timeout,
    )


def call_helper_object_retry(
    client: WordpressClient,
    *,
    route: str,
    token: str,
    helper_sha256: str,
    action: str,
    label: str,
    extra: dict[str, Any] | None = None,
    timeout: int = 180,
    attempts: int = 2,
) -> dict[str, Any]:
    last_error: Exception | None = None
    for _attempt in range(attempts):
        try:
            return require_object(
                call_helper(
                    client,
                    route=route,
                    token=token,
                    helper_sha256=helper_sha256,
                    action=action,
                    extra=extra,
                    timeout=timeout,
                ),
                label,
            )
        except NetworkRequestFailed as error:
            last_error = error
    if last_error is not None:
        raise last_error
    raise RuntimeError(f"{label} did not converge")


def auth_preflight(client: WordpressClient) -> dict[str, Any]:
    response = client.request(
        "GET", "wp/v2/users/me", params={"context": "edit", "_fields": "id,roles"}
    )
    payload = require_object(response, "Authenticated user preflight")
    roles = payload.get("roles")
    if (
        int(payload.get("id") or 0) != 1
        or not isinstance(roles, list)
        or "administrator" not in roles
    ):
        raise RuntimeError("Authenticated user is not the exact owner administrator")
    rows = client.all_snippets()
    return {
        "authenticated": True,
        "user_id": 1,
        "administrator": True,
        "snippet_count": len(rows),
    }


def validate_inventory_contract(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "file_count",
        "directory_count",
        "bytes",
        "digest",
        "tree_digest",
        "rows",
        "directories",
    }:
        raise RuntimeError("Full inventory shape is invalid")
    rows = value.get("rows")
    directories = value.get("directories")
    if not isinstance(rows, list) or not isinstance(directories, list):
        raise RuntimeError("Full inventory rows are unavailable")
    normalized_rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"}:
            raise RuntimeError("Full inventory file row is invalid")
        path = validate_relative_path(str(row.get("path") or ""))
        folded = path.casefold()
        size = row.get("bytes")
        digest = str(row.get("sha256") or "")
        if (
            folded in seen
            or not isinstance(size, int)
            or isinstance(size, bool)
            or not 0 <= size <= MAX_FILE_BYTES
            or not HASH_RE.fullmatch(digest)
        ):
            raise RuntimeError("Full inventory file identity is invalid")
        seen.add(folded)
        normalized_rows.append({"path": path, "bytes": size, "sha256": digest})
    normalized_directories: list[str] = []
    for raw_directory in directories:
        directory = validate_relative_path(str(raw_directory or ""))
        folded = directory.casefold()
        if folded in seen:
            raise RuntimeError("Full inventory directory collision detected")
        seen.add(folded)
        normalized_directories.append(directory)
    if (
        len(normalized_rows) > MAX_FILES
        or len(normalized_directories) > 2048
        or normalized_rows != sorted(normalized_rows, key=lambda row: row["path"])
        or normalized_directories != sorted(normalized_directories)
    ):
        raise RuntimeError("Full inventory ordering or bounds are invalid")
    calculated = inventory_contract(normalized_rows, normalized_directories)
    if calculated != value or calculated["bytes"] > MAX_TREE_BYTES:
        raise RuntimeError("Full inventory digest is invalid")
    return value


def validate_storage_proof(value: Any, post_id: int) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "schema",
        "post_id",
        "core_sha256",
        "core_column_count",
        "raw_meta_sha256",
        "raw_meta_row_count",
        "term_relationships_sha256",
        "term_relationships_row_count",
        "contract_sha256",
    }:
        raise RuntimeError("Post storage proof shape is invalid")
    base = {key: child for key, child in value.items() if key != "contract_sha256"}
    if (
        value.get("schema") != "nadlan-canonical-post-storage-proof/v1"
        or value.get("post_id") != post_id
        or any(
            not HASH_RE.fullmatch(str(value.get(key) or ""))
            for key in (
                "core_sha256",
                "raw_meta_sha256",
                "term_relationships_sha256",
                "contract_sha256",
            )
        )
        or value.get("contract_sha256") != sha256_bytes(exact_json_bytes(base))
    ):
        raise RuntimeError("Post storage proof aggregate hash is invalid")
    return value


def validate_raw_snapshot(value: Any, post_id: int) -> dict[str, Any]:
    """Recompute the byte-stable direct-DB JSON snapshot contract."""

    if not isinstance(value, dict) or set(value) != {
        "schema",
        "post_id",
        "core",
        "meta",
        "terms",
        "contract_sha256",
    }:
        raise RuntimeError("Raw post snapshot shape is invalid")
    core = value.get("core")
    meta_rows = value.get("meta")
    terms = value.get("terms")
    if (
        value.get("schema") != "nadlan-einstein-public-raw-snapshot/v1"
        or value.get("post_id") != post_id
        or not isinstance(core, dict)
        or not isinstance(meta_rows, list)
        or not isinstance(terms, list)
        or len(core) > 128
        or len(meta_rows) > 4096
        or len(terms) > 1024
        or int(core.get("ID") or 0) != post_id
    ):
        raise RuntimeError("Raw post snapshot core contract is invalid")
    normalized_meta: list[dict[str, str]] = []
    prior_meta_id = 0
    for row in meta_rows:
        if not isinstance(row, dict) or set(row) != {
            "meta_id",
            "post_id",
            "meta_key",
            "meta_value",
        }:
            raise RuntimeError("Raw post snapshot metadata row is invalid")
        normalized = {
            "meta_id": str(row.get("meta_id") or ""),
            "post_id": str(row.get("post_id") or ""),
            "meta_key": str(row.get("meta_key") or ""),
            "meta_value": str(row.get("meta_value") or ""),
        }
        if (
            not normalized["meta_id"].isdigit()
            or int(normalized["meta_id"]) <= prior_meta_id
            or normalized["post_id"] != str(post_id)
            or not normalized["meta_key"]
        ):
            raise RuntimeError("Raw post snapshot metadata ordering is invalid")
        prior_meta_id = int(normalized["meta_id"])
        normalized_meta.append(normalized)
    normalized_terms: list[dict[str, str]] = []
    prior_term_id = -1
    for row in terms:
        if not isinstance(row, dict) or set(row) != {
            "object_id",
            "term_taxonomy_id",
            "term_order",
        }:
            raise RuntimeError("Raw post snapshot term row is invalid")
        normalized = {
            "object_id": str(row.get("object_id") or ""),
            "term_taxonomy_id": str(row.get("term_taxonomy_id") or ""),
            "term_order": str(row.get("term_order") or ""),
        }
        if (
            normalized["object_id"] != str(post_id)
            or not normalized["term_taxonomy_id"].isdigit()
            or int(normalized["term_taxonomy_id"]) < prior_term_id
            or not normalized["term_order"].lstrip("-").isdigit()
        ):
            raise RuntimeError("Raw post snapshot term ordering is invalid")
        prior_term_id = int(normalized["term_taxonomy_id"])
        normalized_terms.append(normalized)
    normalized_core = dict(core)
    base = {
        "schema": "nadlan-einstein-public-raw-snapshot/v1",
        "post_id": post_id,
        "core": normalized_core,
        "meta": normalized_meta,
        "terms": normalized_terms,
    }
    if (
        not HASH_RE.fullmatch(str(value.get("contract_sha256") or ""))
        or value.get("contract_sha256") != sha256_bytes(exact_json_bytes(base))
    ):
        raise RuntimeError("Raw post snapshot aggregate hash is invalid")
    return value


def raw_snapshot_meta_contract(
    snapshot: dict[str, Any],
) -> tuple[dict[str, str], list[str], list[str]]:
    raw_map: dict[str, str] = {}
    duplicates: list[str] = []
    for row in snapshot["meta"]:
        key = row["meta_key"]
        if key in raw_map:
            duplicates.append(key)
        else:
            raw_map[key] = row["meta_value"]
    return (
        {key: raw_map[key] for key in sorted(raw_map)},
        sorted(raw_map),
        sorted(set(duplicates)),
    )


def validate_option_baseline(
    value: Any,
    *,
    option_name: str,
    required_keys: set[str],
) -> dict[str, Any]:
    expected_fields = {
        "option_name",
        "autoload",
        "raw_sha256",
        "raw_bytes",
        "keys",
        "keys_sha256",
        "decoded_sha256",
        "run_id",
    }
    expected_fields.update(
        ("phase", "page_id")
        if option_name.startswith("nadlan_unit_journey_state_")
        else ("created_at",)
    )
    if not isinstance(value, dict) or set(value) != expected_fields:
        raise RuntimeError("Option baseline shape is invalid")
    keys = value.get("keys")
    if (
        value.get("option_name") != option_name
        or not isinstance(keys, list)
        or keys != sorted(keys)
        or len(keys) != len(set(keys))
        or not required_keys.issubset(set(keys))
        or value.get("keys_sha256") != sha256_bytes(exact_json_bytes(keys))
        or not isinstance(value.get("raw_bytes"), int)
        or not 0 < value["raw_bytes"] <= 2 * 1024 * 1024
        or any(
            not HASH_RE.fullmatch(str(value.get(key) or ""))
            for key in ("raw_sha256", "keys_sha256", "decoded_sha256")
        )
        or value.get("run_id") != RUN_ID
    ):
        raise RuntimeError("Option baseline exact key/hash contract failed")
    return value


def validate_baseline_contract(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "schema",
        "run_id",
        "retained_helpers",
        "state",
        "lock",
        "retained_storage",
        "stage_post",
        "canonical_post",
        "plugin",
        "marker_pre_registered",
        "known_semantic_integrity",
        "contract_sha256",
    }:
        raise RuntimeError("Observed live baseline shape is invalid")
    base = {key: child for key, child in value.items() if key != "contract_sha256"}
    if (
        value.get("schema") != "nadlan-einstein-live-recovery-baseline/v1"
        or value.get("run_id") != RUN_ID
        or value.get("retained_helpers") != EXPECTED_HELPERS
        or value.get("known_semantic_integrity") is not True
        or value.get("marker_pre_registered") is not True
        or value.get("contract_sha256") != sha256_bytes(exact_json_bytes(base))
    ):
        raise RuntimeError("Observed live baseline identity failed")
    state_key = "nadlan_unit_journey_state_" + hashlib.sha256(RUN_ID.encode()).hexdigest()[:16]
    state = validate_option_baseline(
        value.get("state"),
        option_name=state_key,
        required_keys={"run_id", "phase", "page_id", "backup_root", "upload_path"},
    )
    lock = validate_option_baseline(
        value.get("lock"),
        option_name="nadlan_unit_journey_deploy_lock",
        required_keys={"run_id", "created_at"},
    )
    if state.get("phase") != "page_creating" or state.get("page_id") != 6594:
        raise RuntimeError("Observed retained phase/post identity changed")
    if not isinstance(lock.get("created_at"), int) or lock["created_at"] <= 0:
        raise RuntimeError("Observed retained lock ownership is invalid")
    storage = value.get("retained_storage")
    if not isinstance(storage, dict) or set(storage) != {
        "storage_leaf",
        "inventory",
        "backup",
        "upload_relative_path",
        "upload_temp_absent",
    }:
        raise RuntimeError("Observed retained storage baseline is invalid")
    storage_inventory = validate_inventory_contract(storage.get("inventory"))
    backup = storage.get("backup")
    if (
        not isinstance(backup, dict)
        or set(backup) != {"version", "inventory"}
        or backup.get("version") != "1.72.204"
        or storage.get("upload_relative_path") != "artifact/nadlan-config.zip"
        or storage.get("upload_temp_absent") is not True
        or not re.fullmatch(r"\.nadlan-unit-journey-release-[a-f0-9]{32}", str(storage.get("storage_leaf") or ""))
    ):
        raise RuntimeError("Observed retained storage identity changed")
    backup_inventory = validate_inventory_contract(backup.get("inventory"))
    if (
        backup_inventory["file_count"] != 469
        or backup_inventory["bytes"] != 28047176
        or backup_inventory["digest"]
        != "f1d3a5729bca013a04cced06d54fbc3061733540a948b28eb68c73cefbee3470"
    ):
        raise RuntimeError("Observed retained backup identity changed")
    retained_rows = {row["path"]: row for row in storage_inventory["rows"]}
    for row in backup_inventory["rows"]:
        retained = retained_rows.get(f"backup/nadlan-config/{row['path']}")
        if retained != {
            "path": f"backup/nadlan-config/{row['path']}",
            "bytes": row["bytes"],
            "sha256": row["sha256"],
        }:
            raise RuntimeError("Backup inventory is not embedded in retained storage")
    stage = value.get("stage_post")
    if not isinstance(stage, dict) or set(stage) != {
        "post_id",
        "core",
        "core_columns",
        "core_columns_sha256",
        "storage",
        "raw_snapshot",
        "raw_map_sha256",
        "raw_meta_keys",
        "raw_meta_keys_sha256",
        "duplicate_keys",
    }:
        raise RuntimeError("Stage baseline shape is invalid")
    stage_proof = validate_storage_proof(stage.get("storage"), 6594)
    stage_raw_snapshot = validate_raw_snapshot(stage.get("raw_snapshot"), 6594)
    stage_raw_map, stage_derived_keys, stage_duplicates = raw_snapshot_meta_contract(
        stage_raw_snapshot
    )
    stage_keys = stage.get("raw_meta_keys")
    core_columns = stage.get("core_columns")
    core = stage.get("core")
    if (
        stage.get("post_id") != 6594
        or stage_proof.get("core_column_count") != 23
        or stage_proof.get("raw_meta_row_count") != 37
        or stage_proof.get("term_relationships_row_count") != 0
        or len(stage_raw_snapshot["meta"])
        != stage_proof.get("raw_meta_row_count")
        or len(stage_raw_snapshot["terms"])
        != stage_proof.get("term_relationships_row_count")
        or stage.get("raw_map_sha256") != EXPECTED_RAW_META_MAP_SHA256
        or stage.get("raw_map_sha256")
        != sha256_bytes(exact_json_bytes(stage_raw_map))
        or not isinstance(stage_keys, list)
        or stage_keys != sorted(stage_keys)
        or len(stage_keys) != 37
        or stage.get("raw_meta_keys_sha256") != sha256_bytes(exact_json_bytes(stage_keys))
        or stage.get("duplicate_keys") != []
        or stage_duplicates != []
        or stage_derived_keys != stage_keys
        or not isinstance(core_columns, list)
        or len(core_columns) != 23
        or stage.get("core_columns_sha256") != sha256_bytes(exact_json_bytes(core_columns))
        or not isinstance(core, dict)
        or core.get("post_status") != "publish"
        or core.get("password_length") != 0
        or stage_raw_snapshot["core"].get("post_status") != "publish"
        or stage_raw_snapshot["core"].get("post_type") != "nadlan_project"
        or len(str(stage_raw_snapshot["core"].get("post_password") or "")) != 0
        or sha256_bytes(
            str(stage_raw_snapshot["core"].get("post_title") or "").encode("utf-8")
        )
        != core.get("title_sha256")
        or sha256_bytes(
            str(stage_raw_snapshot["core"].get("post_content") or "").encode("utf-8")
        )
        != core.get("content_sha256")
        or sha256_bytes(
            str(stage_raw_snapshot["core"].get("post_excerpt") or "").encode("utf-8")
        )
        != core.get("excerpt_sha256")
    ):
        raise RuntimeError("Independent stage hashes/keysets are incomplete")
    canonical = value.get("canonical_post")
    if not isinstance(canonical, dict) or set(canonical) != {
        "post_id",
        "core_columns",
        "core_columns_sha256",
        "storage",
        "raw_snapshot",
        "raw_map_sha256",
        "raw_meta_keys",
        "raw_meta_keys_sha256",
    }:
        raise RuntimeError("Canonical baseline shape is invalid")
    canonical_proof = validate_storage_proof(canonical.get("storage"), 4867)
    canonical_raw_snapshot = validate_raw_snapshot(
        canonical.get("raw_snapshot"), 4867
    )
    canonical_raw_map, canonical_derived_keys, _canonical_duplicates = (
        raw_snapshot_meta_contract(canonical_raw_snapshot)
    )
    if (
        canonical_proof.get("contract_sha256")
        != EXPECTED_CANONICAL_STORAGE_SHA256
        or len(canonical_raw_snapshot["meta"])
        != canonical_proof.get("raw_meta_row_count")
        or len(canonical_raw_snapshot["terms"])
        != canonical_proof.get("term_relationships_row_count")
        or canonical.get("raw_map_sha256")
        != sha256_bytes(exact_json_bytes(canonical_raw_map))
        or canonical.get("raw_meta_keys") != canonical_derived_keys
    ):
        raise RuntimeError("Canonical storage proof changed")
    plugin = value.get("plugin")
    if not isinstance(plugin, dict) or set(plugin) != {
        "plugin_file",
        "version",
        "active",
        "provenance",
        "main_file_sha256",
        "inventory",
    }:
        raise RuntimeError("Current plugin baseline shape is invalid")
    plugin_inventory = validate_inventory_contract(plugin.get("inventory"))
    if (
        plugin.get("plugin_file") != "nadlan-config/nadlan-config.php"
        or plugin.get("version") != "1.72.207"
        or plugin.get("active") is not True
        or plugin.get("provenance") != "unknown_live_1.72.207_capture"
        or not HASH_RE.fullmatch(str(plugin.get("main_file_sha256") or ""))
        or plugin_inventory["file_count"] < 1
        or plugin_inventory["bytes"] < 1
    ):
        raise RuntimeError("Current plugin exact baseline failed")
    return value


def validate_audit(payload: dict[str, Any]) -> dict[str, Any]:
    baseline = validate_baseline_contract(payload.get("baseline_contract"))
    baseline_sha256 = sha256_bytes(exact_json_bytes(baseline))
    holds = payload.get("safety_holds")
    if (
        payload.get("schema") != "nadlan-einstein-live-recovery-audit/v2"
        or payload.get("run_id") != RUN_ID
        or payload.get("integrity_passed") is not True
        or payload.get("snapshot_eligible") is not False
        or payload.get("expected_contract_match") is not False
        or payload.get("baseline_contract_sha256") != baseline_sha256
        or not HASH_RE.fullmatch(str(payload.get("audit_fingerprint") or ""))
        or payload.get("retained_helpers") != EXPECTED_HELPERS
        or not isinstance(holds, list)
        or "phase_a_snapshot_actions_structurally_disabled" not in holds
        or "independent_reviewed_baseline_not_embedded" not in holds
        or "stage_post_password_absent" not in holds
        or "live_plugin_provenance_unknown" not in holds
    ):
        raise RuntimeError("Phase-A retained baseline audit failed closed")
    return payload


def write_report(path: Path, payload: dict[str, Any], redactor: Redactor) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    )
    redactor.assert_absent(serialized)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(serialized)


def fsync_parent_directory(path: Path) -> bool:
    if os.name == "nt":
        return False
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor = os.open(path.parent, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return True


def reserve_terminal_report(
    path: Path,
    prepared: dict[str, Any],
    redactor: Redactor,
) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    checkpoint = {
        "schema": "nadlan-einstein-live-recovery-terminal-checkpoint/v1",
        "status": "PREPARED_BEFORE_DESTRUCTIVE_CLEANUP",
        "prepared_at_utc": utc_now(),
        "directory_fsync_supported": os.name != "nt",
        "planned": prepared,
    }
    serialized = json.dumps(
        checkpoint, ensure_ascii=False, indent=2, sort_keys=False
    ) + "\n"
    redactor.assert_absent(serialized)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(serialized)
        handle.flush()
        os.fsync(handle.fileno())
    fsync_parent_directory(path)
    return checkpoint


def finalize_terminal_report(
    path: Path,
    payload: dict[str, Any],
    redactor: Redactor,
) -> None:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError("Reserved terminal evidence checkpoint is unavailable")
    temp_path = path.with_name(f".{path.name}.final-{secrets.token_hex(8)}")
    serialized = json.dumps(
        payload, ensure_ascii=False, indent=2, sort_keys=False
    ) + "\n"
    redactor.assert_absent(serialized)
    try:
        with temp_path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        fsync_parent_directory(path)
    finally:
        with contextlib.suppress(FileNotFoundError):
            temp_path.unlink()


def read_json_object(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink() or path.stat().st_size > 8 * 1024 * 1024:
        raise RuntimeError("Required evidence report is unavailable or oversized")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("Required evidence report has an invalid shape")
    return payload


def create_and_audit(args: argparse.Namespace) -> int:
    if args.confirm_create_helper != "CREATE-READ-ONLY-LIVE-AUDIT-HELPER":
        raise RuntimeError("Exact helper-creation confirmation is required")
    source = source_facts(args.expected_source_commit)
    base_url, user, password, token, redactor = resolve_runtime(args.env)
    identity = session_identity(token)
    client = WordpressClient(base_url, user, password)
    auth = auth_preflight(client)
    collisions = [
        row
        for row in client.all_snippets()
        if str(row.get("name") or "") == identity["helper_name"]
    ]
    if collisions:
        raise RecoveryHold(
            "Exact recovery helper name already exists; reconcile it first"
        )

    helper_id = 0
    helper_code = ""
    helper_hash = ""
    try:
        placeholder = f"/* inactive placeholder for {identity['helper_name']} */"
        try:
            created = require_object(
                client.request(
                    "POST",
                    "code-snippets/v1/snippets",
                    json_body={
                        "name": identity["helper_name"],
                        "code": placeholder,
                        "scope": "global",
                        "active": False,
                    },
                ),
                "Inactive recovery helper creation",
            )
            helper_id = int(created.get("id") or 0)
        except (NetworkRequestFailed, RuntimeError) as create_error:
            matches = [
                row
                for row in client.all_snippets()
                if str(row.get("name") or "") == identity["helper_name"]
            ]
            if len(matches) != 1:
                raise RecoveryHold(
                    "Response-lost helper creation did not reconcile to one exact row"
                ) from create_error
            helper_id = int(matches[0].get("id") or 0)
            placeholder_payload = require_object(
                client.request(
                    "GET", f"code-snippets/v1/snippets/{helper_id}", timeout=60
                ),
                "Response-lost placeholder read",
            )
            placeholder_observed = observed_snippet(placeholder_payload)
            if placeholder_observed != {
                "id": helper_id,
                "name": identity["helper_name"],
                "active": False,
                "scope": "global",
                "code_sha256": sha256_bytes(placeholder.encode("utf-8")),
            }:
                raise RecoveryHold("Response-lost helper creation row is not exact")
        if helper_id < 1 or helper_id in (449, 450):
            raise RuntimeError("Inactive recovery helper returned an invalid ID")
        helper_code, rendered_identity = render_helper(
            token=token, helper_id=helper_id, source_commit=source["commit"]
        )
        if rendered_identity != identity:
            raise RuntimeError("Rendered recovery identity drifted")
        helper_hash = sha256_bytes(helper_code.encode("utf-8"))
        inactive_expected = helper_expected(
            helper_id, helper_code, identity, active=False
        )
        inactive_verified = False
        for _attempt in range(2):
            with contextlib.suppress(NetworkRequestFailed):
                client.request(
                    "PUT",
                    f"code-snippets/v1/snippets/{helper_id}",
                    json_body={
                        "name": identity["helper_name"],
                        "code": helper_code,
                        "scope": "global",
                        "active": False,
                    },
                )
            try:
                verify_helper_row(client, helper_id, inactive_expected)
                inactive_verified = True
                break
            except RuntimeError:
                continue
        if not inactive_verified:
            raise RecoveryHold("Inactive helper update did not reconcile")
        active_expected = helper_expected(helper_id, helper_code, identity, active=True)
        active: dict[str, Any] | None = None
        for _attempt in range(2):
            with contextlib.suppress(NetworkRequestFailed):
                client.request(
                    "PUT",
                    f"code-snippets/v1/snippets/{helper_id}/activate",
                    json_body={},
                )
            try:
                active = verify_helper_row(client, helper_id, active_expected)
                break
            except RuntimeError:
                continue
        if active is None:
            raise RecoveryHold("Recovery helper activation did not reconcile")

        first = validate_audit(
            call_helper_object_retry(
                client,
                route=identity["route"],
                token=token,
                helper_sha256=helper_hash,
                action="audit",
                label="First retained live audit",
            )
        )
        time.sleep(0.25)
        second = validate_audit(
            call_helper_object_retry(
                client,
                route=identity["route"],
                token=token,
                helper_sha256=helper_hash,
                action="audit",
                label="Second retained live audit",
            )
        )
        if first != second:
            raise RecoveryHold("Consecutive retained live audits were not byte-stable")
        storage = call_helper_object_retry(
            client,
            route=identity["route"],
            token=token,
            helper_sha256=helper_hash,
            action="storage_status",
            label="Recovery snapshot storage absence",
        )
        if (
            storage.get("schema") != "nadlan-einstein-live-recovery-storage-status/v1"
            or not isinstance(storage.get("storage"), dict)
            or storage["storage"].get("absent") is not True
        ):
            raise RecoveryHold("Recovery snapshot storage is not initially absent")

        report = {
            "schema": "nadlan-einstein-live-recovery-client-audit/v2",
            "generated_at_utc": utc_now(),
            "source": source,
            "target": {"base_url": base_url, "plugin_version": "1.72.207"},
            "auth": auth,
            "helper": active,
            "control": {
                "route": identity["route"],
                "helper_id": helper_id,
                "helper_name": identity["helper_name"],
                "helper_sha256": helper_hash,
            },
            "audit": second,
            "snapshot_storage_initially_absent": True,
            "passed": True,
            "status": "PHASE_A_BASELINE_CAPTURED_REVIEW_AND_HELPER_CLEANUP_REQUIRED",
        }
        write_report(args.report, report, redactor)
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "helper_id": helper_id,
                    "audit_fingerprint": second["audit_fingerprint"],
                    "report": str(args.report.resolve()),
                },
                separators=(",", ":"),
            )
        )
        return 0
    except Exception as original_error:
        # Never overwrite, reactivate, or delete an uncertain/drifted row from
        # an exception handler. Capture only exact ownership state and require
        # the separately confirmed terminal cleanup workflow.
        try:
            ownership = inspect_owned_helper(
                client,
                identity=identity,
                token=token,
                helper_id=helper_id,
                helper_code=helper_code,
            )
        except Exception as inspection_error:
            raise RecoveryHold(
                "Audit failed and recovery-helper ownership is uncertain; no cleanup mutation was attempted"
            ) from inspection_error
        raise RecoveryHold(
            "Audit failed; no exception-path mutation was attempted; "
            f"owned helper id {helper_id} state is {ownership['state']}"
        ) from original_error


def validate_control_report(
    report: dict[str, Any], token: str, expected_commit: str
) -> tuple[dict[str, str], int, str]:
    if report.get("schema") != "nadlan-einstein-live-recovery-client-audit/v2":
        raise RuntimeError("Audit report schema is invalid")
    source = report.get("source")
    control = report.get("control")
    audit = report.get("audit")
    if (
        not isinstance(source, dict)
        or not isinstance(control, dict)
        or not isinstance(audit, dict)
    ):
        raise RuntimeError("Audit report is structurally incomplete")
    if source.get("commit") != expected_commit:
        raise RuntimeError("Audit report source commit differs")
    validate_audit(audit)
    identity = session_identity(token)
    helper_id = int(control.get("helper_id") or 0)
    helper_hash = str(control.get("helper_sha256") or "")
    if (
        helper_id < 1
        or helper_id in (449, 450)
        or control.get("route") != identity["route"]
        or control.get("helper_name") != identity["helper_name"]
        or not HASH_RE.fullmatch(helper_hash)
    ):
        raise RuntimeError("Audit report recovery control identity changed")
    return identity, helper_id, helper_hash


def prove_helper_absence(
    client: WordpressClient,
    *,
    identity: dict[str, str],
    token: str,
    helper_id: int,
    helper_hash: str,
    public_session: Any | None = None,
) -> dict[str, bool | int]:
    item_response = client.request(
        "GET", f"code-snippets/v1/snippets/{helper_id}", timeout=60
    )
    item_absent = is_exact_missing_snippet(item_response)
    rows = client.all_snippets()
    collection_absent = not any(
        int(row.get("id") or 0) == helper_id
        or str(row.get("name") or "") == identity["helper_name"]
        for row in rows
    )
    route_response = call_helper(
        client,
        route=identity["route"],
        token=token,
        helper_sha256=helper_hash,
        action="storage_status",
    )
    route_absent = is_exact_missing_route(route_response)
    session = public_session or requests_module().Session()
    try:
        public_response = session.request(
            "POST",
            f"{client.base_url}/wp-json/{identity['route'].lstrip('/')}",
            json={"action": "storage_status", "helper_sha256": helper_hash},
            headers={
                "Accept": "application/json",
                "User-Agent": "NadLan-Einstein-Recovery-Public-Absence/1.0",
            },
            timeout=60,
            allow_redirects=False,
        )
    except Exception as error:
        module = _REQUESTS
        if module is not None and isinstance(error, module.RequestException):
            raise NetworkRequestFailed(
                "Unauthenticated helper-route absence request failed"
            ) from error
        raise
    public_route_absent = is_exact_missing_route(public_response)
    return {
        "item_absent": item_absent,
        "collection_absent": collection_absent,
        "route_absent": route_absent,
        "route_http_status": int(route_response.status_code),
        "public_route_absent": public_route_absent,
        "public_route_http_status": int(public_response.status_code),
    }


def cleanup_audit_helper(args: argparse.Namespace) -> int:
    if args.confirm_cleanup != "CLEANUP-PHASE-A-AUDIT-HELPER":
        raise RuntimeError("Exact Phase-A helper cleanup confirmation is required")
    source = source_facts(args.expected_source_commit)
    base_url, user, password, token, redactor = resolve_runtime(args.env)
    identity = session_identity(token)
    audit_report_sha256: str | None = None
    if args.audit_report is not None:
        audit_report = read_json_object(args.audit_report)
        identity, helper_id, helper_hash = validate_control_report(
            audit_report, token, source["commit"]
        )
        audit_report_sha256 = sha256_bytes(args.audit_report.read_bytes())
        cleanup_authority = "validated_phase_a_audit_report"
    else:
        helper_id = int(args.helper_id or 0)
        if helper_id < 1 or helper_id in (449, 450):
            raise RuntimeError("Interrupted helper cleanup ID is outside scope")
        provisional_code, provisional_identity = render_helper(
            token=token, helper_id=helper_id, source_commit=source["commit"]
        )
        if provisional_identity != identity:
            raise RuntimeError("Interrupted helper cleanup identity changed")
        helper_hash = sha256_bytes(provisional_code.encode("utf-8"))
        cleanup_authority = "exact_interrupted_owned_state"
    client = WordpressClient(base_url, user, password)
    auth = auth_preflight(client)
    helper_code, _ = render_helper(
        token=token, helper_id=helper_id, source_commit=source["commit"]
    )
    expected_helper = helper_expected(helper_id, helper_code, identity, active=True)
    if expected_helper["code_sha256"] != helper_hash:
        raise RuntimeError("Phase-A helper source hash differs from audit evidence")
    ownership = inspect_owned_helper(
        client,
        identity=identity,
        token=token,
        helper_id=helper_id,
        helper_code=helper_code,
    )
    checkpoint = reserve_terminal_report(
        args.report,
        {
            "operation": "delete_exact_phase_a_audit_helper",
            "source_commit": source["commit"],
            "audit_report_sha256": audit_report_sha256,
            "cleanup_authority": cleanup_authority,
            "helper_id": helper_id,
            "helper_name": identity["helper_name"],
            "helper_sha256": helper_hash,
            "observed_ownership_state": ownership["state"],
        },
        redactor,
    )
    direct_absence = False
    delete_response_lost = False
    deletion_method = "already_absent"
    rest_delete_response_observed = False
    if ownership["state"] == "exact_active_helper":
        deletion_method = "active_helper_direct_wpdb_self_delete"
        verify_helper_row(client, helper_id, expected_helper)
        storage = call_helper_object_retry(
            client,
            route=identity["route"],
            token=token,
            helper_sha256=helper_hash,
            action="storage_status",
            label="Phase-A private storage absence",
        )
        storage_evidence = storage.get("storage")
        if (
            not isinstance(storage_evidence, dict)
            or storage_evidence.get("absent") is not True
            or storage_evidence.get("outside_webroot") is not True
        ):
            raise RecoveryHold(
                "Reserved cleanup checkpoint, but private storage absence was not proved"
            )
        try:
            delete_payload = require_object(
                call_helper(
                    client,
                    route=identity["route"],
                    token=token,
                    helper_sha256=helper_hash,
                    action="delete_self",
                    extra={"confirmation": "DELETE-OWN-RECOVERY-HELPER"},
                ),
                "Phase-A recovery helper hard deletion",
            )
            direct_absence = (
                delete_payload.get("schema")
                == "nadlan-einstein-live-recovery-helper-delete/v1"
                and delete_payload.get("helper_id") == helper_id
                and delete_payload.get("direct_snippet_row_count") == 0
                and delete_payload.get("storage_absent") is True
                and delete_payload.get("retained_helpers_unchanged") is True
                and delete_payload.get("mutation_mutex_held") is True
            )
        except NetworkRequestFailed:
            delete_response_lost = True
    elif ownership["state"] in {
        "exact_inactive_placeholder",
        "exact_inactive_helper",
    }:
        deletion_method = "exact_inactive_helper_code_snippets_rest_delete"
        try:
            delete_response = client.request(
                "DELETE", f"code-snippets/v1/snippets/{helper_id}", timeout=60
            )
            rest_delete_response_observed = 200 <= delete_response.status_code < 300
            if not rest_delete_response_observed:
                raise RecoveryHold(
                    "Reserved cleanup checkpoint; exact inactive helper REST deletion was rejected"
                )
        except NetworkRequestFailed:
            delete_response_lost = True
    elif ownership["state"] != "absent":
        raise RecoveryHold(
            "Reserved cleanup checkpoint; helper is not the exact active owned row; no mutation attempted"
        )
    absence = prove_helper_absence(
        client,
        identity=identity,
        token=token,
        helper_id=helper_id,
        helper_hash=helper_hash,
    )
    if not all(
        absence[key]
        for key in (
            "item_absent",
            "collection_absent",
            "route_absent",
            "public_route_absent",
        )
    ):
        raise RecoveryHold(
            "Reserved cleanup checkpoint; item/collection/route absence is uncertain"
        )
    uncertainty = None
    if not direct_absence:
        if delete_response_lost:
            uncertainty = "delete_response_lost_direct_database_absence_not_observed"
        elif rest_delete_response_observed:
            uncertainty = (
                "exact_inactive_rest_delete_observed_direct_database_absence_unavailable"
            )
        else:
            uncertainty = (
                "helper_was_already_absent_direct_database_absence_not_observed"
            )
    report = {
        "schema": "nadlan-einstein-live-recovery-client-helper-cleanup/v1",
        "generated_at_utc": utc_now(),
        "source": source,
        "auth": auth,
        "checkpoint": checkpoint,
        "audit_report_sha256": audit_report_sha256,
        "helper_id": helper_id,
        "direct_database_absence_proved": direct_absence,
        "cleanup_authority": cleanup_authority,
        "deletion_method": deletion_method,
        "rest_delete_response_observed": rest_delete_response_observed,
        "delete_response_lost": delete_response_lost,
        "absence": absence,
        "uncertainty": uncertainty,
        "passed": direct_absence,
        "status": (
            "PHASE_A_HELPER_CLEANUP_COMPLETE_DIRECTLY_PROVED"
            if direct_absence
            else "PHASE_A_HELPER_ABSENCE_RECONCILED_WITH_EXPLICIT_UNCERTAINTY"
        ),
    }
    finalize_terminal_report(args.report, report, redactor)
    print(
        json.dumps(
            {"status": report["status"], "report": str(args.report.resolve())},
            separators=(",", ":"),
        )
    )
    return 0 if direct_absence else 2


def validate_manifest(
    manifest: dict[str, Any],
    *,
    source_commit: str,
    audit_fingerprint: str,
    token: str,
    storage_slug: str | None = None,
) -> dict[str, Any]:
    """Validate the dormant Phase-B manifest against independent primitives."""

    plugin = manifest.get("plugin")
    archive = manifest.get("archive")
    if not isinstance(plugin, dict) or not isinstance(archive, dict):
        raise RuntimeError("Snapshot manifest sections are incomplete")
    if not (
        set(manifest)
        == {
            "schema",
            "run_id",
            "source_commit",
            "storage_slug",
            "created_at_utc",
            "audit_fingerprint",
            "plugin",
            "archive",
            "contract_sha256",
            "auth_hmac_sha256",
        }
        and manifest.get("schema") == "nadlan-einstein-live-plugin-snapshot/v1"
        and manifest.get("run_id") == RUN_ID
        and manifest.get("source_commit") == source_commit
        and (storage_slug is None or manifest.get("storage_slug") == storage_slug)
        and re.fullmatch(
            r"\.nadlan-live-recovery-[a-f0-9]{32}",
            str(manifest.get("storage_slug") or ""),
        )
        and manifest.get("audit_fingerprint") == audit_fingerprint
        and HASH_RE.fullmatch(str(manifest.get("contract_sha256") or ""))
        and HASH_RE.fullmatch(str(manifest.get("auth_hmac_sha256") or ""))
        and plugin.get("plugin_file") == "nadlan-config/nadlan-config.php"
        and set(plugin)
        == {
            "plugin_file",
            "version",
            "active",
            "provenance",
            "main_file_sha256",
            "inventory",
        }
        and plugin.get("version") == "1.72.207"
        and plugin.get("active") is True
        and plugin.get("provenance") == "unknown_live_1.72.207_capture"
        and HASH_RE.fullmatch(str(plugin.get("main_file_sha256") or ""))
        and HASH_RE.fullmatch(str(archive.get("sha256") or ""))
        and set(archive)
        == {
            "sha256",
            "bytes",
            "chunk_bytes",
            "chunks",
            "chunk_sha256",
            "mtime",
        }
        and isinstance(archive.get("bytes"), int)
        and not isinstance(archive.get("bytes"), bool)
        and 0 < archive["bytes"] <= MAX_ARCHIVE_BYTES
        and archive.get("chunk_bytes") == CHUNK_BYTES
        and isinstance(archive.get("chunks"), int)
        and not isinstance(archive.get("chunks"), bool)
        and archive.get("chunks") == (archive["bytes"] + CHUNK_BYTES - 1) // CHUNK_BYTES
        and isinstance(archive.get("chunk_sha256"), list)
        and len(archive["chunk_sha256"]) == archive["chunks"]
        and all(
            isinstance(digest, str) and HASH_RE.fullmatch(digest)
            for digest in archive["chunk_sha256"]
        )
        and isinstance(archive.get("mtime"), int)
        and not isinstance(archive.get("mtime"), bool)
        and archive["mtime"] > 0
        and re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
            str(manifest.get("created_at_utc") or ""),
        )
    ):
        raise RuntimeError("Snapshot manifest exact contract failed")
    manifest_base = {
        "schema": manifest.get("schema"),
        "run_id": manifest.get("run_id"),
        "source_commit": manifest.get("source_commit"),
        "storage_slug": manifest.get("storage_slug"),
        "created_at_utc": manifest.get("created_at_utc"),
        "audit_fingerprint": manifest.get("audit_fingerprint"),
        "plugin": plugin,
        "archive": archive,
    }
    if sha256_bytes(exact_json_bytes(manifest_base)) != manifest.get("contract_sha256"):
        raise RuntimeError("Snapshot manifest aggregate hash is invalid")
    signed = {**manifest_base, "contract_sha256": manifest["contract_sha256"]}
    expected_hmac = hmac.new(
        token.encode("utf-8"), exact_json_bytes(signed), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected_hmac, manifest["auth_hmac_sha256"]):
        raise RuntimeError("Snapshot manifest authentication hash is invalid")
    inventory = validate_inventory_contract(plugin.get("inventory"))
    if inventory["file_count"] < 1 or inventory["bytes"] < 1:
        raise RuntimeError("Snapshot manifest plugin inventory is empty")
    return manifest


def validate_relative_path(value: str) -> str:
    if (
        not value
        or len(value) > 512
        or "\\" in value
        or "\x00" in value
        or value.startswith("/")
        or ":" in value
        or not value.isascii()
    ):
        raise RuntimeError("Archive contains an unsafe path")
    pure = PurePosixPath(value)
    windows_reserved = {"con", "prn", "aux", "nul"} | {
        f"{prefix}{number}" for prefix in ("com", "lpt") for number in range(1, 10)
    }
    if any(
        segment in ("", ".", "..")
        or len(segment) > 191
        or any(ord(char) < 32 or ord(char) == 127 for char in segment)
        or segment.endswith((" ", "."))
        or segment.split(".", 1)[0].casefold() in windows_reserved
        for segment in pure.parts
    ):
        raise RuntimeError("Archive contains an unsafe path segment")
    return pure.as_posix()


def inventory_contract(
    rows: list[dict[str, Any]], directories: Iterable[str] = ()
) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda row: row["path"])
    ordered_directories = sorted(directories)
    digest_bytes = "\n".join(
        f"{row['path']}\t{row['bytes']}\t{row['sha256']}" for row in ordered
    ).encode("utf-8")
    tree_lines = [f"D\t{directory}" for directory in ordered_directories]
    tree_lines.extend(
        f"F\t{row['path']}\t{row['bytes']}\t{row['sha256']}" for row in ordered
    )
    tree_lines.sort()
    return {
        "file_count": len(ordered),
        "directory_count": len(ordered_directories),
        "bytes": sum(int(row["bytes"]) for row in ordered),
        "digest": sha256_bytes(digest_bytes),
        "tree_digest": sha256_bytes("\n".join(tree_lines).encode("utf-8")),
        "rows": ordered,
        "directories": ordered_directories,
    }


def local_tree_inventory(root: Path) -> dict[str, Any]:
    if not root.is_dir() or root.is_symlink():
        raise RuntimeError("Extracted snapshot root is unavailable or unsafe")
    rows: list[dict[str, Any]] = []
    directories: list[str] = []
    seen: set[str] = set()
    stack = [root]
    while stack:
        directory = stack.pop()
        with os.scandir(directory) as entries:
            ordered = sorted(entries, key=lambda entry: entry.name)
        for entry in ordered:
            path = Path(entry.path)
            if entry.is_symlink():
                raise RuntimeError("Extracted snapshot contains a symlink")
            relative = validate_relative_path(path.relative_to(root).as_posix())
            folded = relative.casefold()
            if folded in seen:
                raise RuntimeError("Extracted snapshot has a case-colliding entry")
            seen.add(folded)
            if entry.is_dir(follow_symlinks=False):
                if len(directories) >= 2048:
                    raise RuntimeError("Extracted snapshot directory limit exceeded")
                directories.append(relative)
                stack.append(path)
                continue
            if not entry.is_file(follow_symlinks=False):
                raise RuntimeError("Extracted snapshot contains a non-file entry")
            size = entry.stat(follow_symlinks=False).st_size
            if size < 0 or size > MAX_FILE_BYTES or len(rows) >= MAX_FILES:
                raise RuntimeError("Extracted snapshot file limit exceeded")
            digest = hashlib.sha256()
            observed = 0
            with path.open("rb") as handle:
                while True:
                    block = handle.read(128 * 1024)
                    if not block:
                        break
                    observed += len(block)
                    digest.update(block)
            if observed != size:
                raise RuntimeError("Extracted snapshot file changed during hashing")
            rows.append({"path": relative, "bytes": size, "sha256": digest.hexdigest()})
    inventory = inventory_contract(rows, directories)
    if inventory["bytes"] > MAX_TREE_BYTES:
        raise RuntimeError("Extracted snapshot tree exceeds its bound")
    return inventory


def verify_and_extract_archive(
    archive_path: Path,
    extract_root: Path,
    expected_inventory: dict[str, Any],
    *,
    create: bool,
) -> dict[str, Any]:
    if not archive_path.is_file() or archive_path.is_symlink():
        raise RuntimeError("Local snapshot archive is unavailable or unsafe")
    if archive_path.stat().st_size > MAX_ARCHIVE_BYTES:
        raise RuntimeError("Local snapshot archive exceeds its bound")
    expected_rows = expected_inventory.get("rows")
    expected_directories = expected_inventory.get("directories")
    if not isinstance(expected_rows, list) or not isinstance(expected_directories, list):
        raise RuntimeError("Expected snapshot inventory rows are unavailable")
    expected_by_path = {row["path"]: row for row in expected_rows}
    if len(expected_by_path) != len(expected_rows):
        raise RuntimeError("Expected snapshot inventory contains duplicate paths")
    if create:
        extract_root.mkdir(parents=False, exist_ok=False)
    elif not extract_root.is_dir() or extract_root.is_symlink():
        raise RuntimeError("Local extracted snapshot root is unavailable or unsafe")

    observed_rows: list[dict[str, Any]] = []
    observed_directories: list[str] = []
    seen: set[str] = set()
    root_seen = False
    with zipfile.ZipFile(archive_path, "r") as archive:
        if len(archive.infolist()) > MAX_FILES + 2048 + 1:
            raise RuntimeError("Snapshot ZIP entry count exceeds its bound")
        for info in archive.infolist():
            name = info.filename
            if name == "nadlan-config/":
                if root_seen:
                    raise RuntimeError("Snapshot ZIP has a duplicate root directory")
                root_seen = True
                continue
            if not name.startswith("nadlan-config/"):
                raise RuntimeError("Snapshot ZIP has an unexpected root")
            relative_raw = name[len("nadlan-config/") :]
            if info.is_dir():
                if not relative_raw:
                    raise RuntimeError("Snapshot ZIP has a duplicate root directory")
                relative = validate_relative_path(relative_raw.rstrip("/"))
                folded = relative.casefold()
                if folded in seen or len(observed_directories) >= 2048:
                    raise RuntimeError("Snapshot ZIP directory collision or limit")
                seen.add(folded)
                observed_directories.append(relative)
                destination = extract_root.joinpath(*PurePosixPath(relative).parts)
                if create:
                    destination.mkdir(parents=True, exist_ok=True)
                elif not destination.is_dir() or destination.is_symlink():
                    raise RuntimeError("Extracted snapshot directory is unsafe")
                continue
            relative = validate_relative_path(relative_raw)
            folded = relative.casefold()
            mode = (info.external_attr >> 16) & 0xFFFF
            if stat.S_ISLNK(mode) or folded in seen or info.flag_bits & 0x1:
                raise RuntimeError(
                    "Snapshot ZIP link, duplicate, or encryption rejected"
                )
            if (
                info.file_size < 0
                or info.file_size > MAX_FILE_BYTES
                or info.compress_size < 0
                or (info.file_size > 1024 * 1024 and info.compress_size == 0)
                or (
                    info.compress_size > 0 and info.file_size / info.compress_size > 500
                )
            ):
                raise RuntimeError("Snapshot ZIP entry size/ratio is unsafe")
            seen.add(folded)
            destination = extract_root.joinpath(*PurePosixPath(relative).parts)
            resolved_parent = destination.parent.resolve()
            root_resolved = extract_root.resolve()
            if (
                resolved_parent != root_resolved
                and root_resolved not in resolved_parent.parents
            ):
                raise RuntimeError("Snapshot extraction target escaped its root")
            expected = expected_by_path.get(relative)
            if expected is None or expected["bytes"] != info.file_size:
                raise RuntimeError("Snapshot ZIP entry is outside the manifest")
            digest = hashlib.sha256()
            observed_bytes = 0
            if create:
                destination.parent.mkdir(parents=True, exist_ok=True)
                handle_context = destination.open("xb")
            else:
                if not destination.is_file() or destination.is_symlink():
                    raise RuntimeError(
                        "Extracted snapshot file is unavailable or unsafe"
                    )
                handle_context = contextlib.nullcontext(None)
            with archive.open(info, "r") as source, handle_context as output:
                while True:
                    block = source.read(128 * 1024)
                    if not block:
                        break
                    observed_bytes += len(block)
                    if observed_bytes > MAX_FILE_BYTES:
                        raise RuntimeError(
                            "Snapshot ZIP entry expanded beyond its bound"
                        )
                    digest.update(block)
                    if output is not None:
                        output.write(block)
            observed_hash = digest.hexdigest()
            if (
                observed_bytes != expected["bytes"]
                or observed_hash != expected["sha256"]
            ):
                raise RuntimeError("Snapshot ZIP entry hash differs from manifest")
            observed_rows.append(
                {"path": relative, "bytes": observed_bytes, "sha256": observed_hash}
            )
        bad_member = archive.testzip()
        if bad_member is not None:
            raise RuntimeError("Snapshot ZIP CRC validation failed")
    if not root_seen:
        raise RuntimeError("Snapshot ZIP root directory is missing")
    observed = inventory_contract(observed_rows, observed_directories)
    if observed != expected_inventory:
        raise RuntimeError("Extracted snapshot tree inventory differs from manifest")
    if local_tree_inventory(extract_root) != expected_inventory:
        raise RuntimeError("Extracted snapshot disk tree differs from manifest")
    return observed


def snapshot(args: argparse.Namespace) -> int:
    if not SNAPSHOT_ACTIONS_ENABLED or not PINNED_EXPECTED_LIVE_CONTRACT:
        raise RecoveryHold(
            "Phase-B snapshot is structurally disabled until the reviewed live "
            "baseline is pinned in a separate commit"
        )
    if args.confirm_snapshot != "SNAPSHOT-LIVE-NADLAN-CONFIG-1.72.207":
        raise RuntimeError("Exact snapshot confirmation is required")
    source = source_facts(args.expected_source_commit)
    base_url, user, password, token, redactor = resolve_runtime(args.env)
    audit_report = read_json_object(args.audit_report)
    identity, helper_id, helper_hash = validate_control_report(
        audit_report, token, source["commit"]
    )
    client = WordpressClient(base_url, user, password)
    auth = auth_preflight(client)
    helper_code, _ = render_helper(
        token=token, helper_id=helper_id, source_commit=source["commit"]
    )
    expected_helper = helper_expected(helper_id, helper_code, identity, active=True)
    if expected_helper["code_sha256"] != helper_hash:
        raise RuntimeError("Re-rendered helper hash differs from audit evidence")
    verify_helper_row(client, helper_id, expected_helper)
    current_audit = validate_audit(
        call_helper_object_retry(
            client,
            route=identity["route"],
            token=token,
            helper_sha256=helper_hash,
            action="audit",
            label="Pre-snapshot retained live audit",
        )
    )
    expected_fingerprint = str(audit_report["audit"]["audit_fingerprint"])
    if current_audit["audit_fingerprint"] != expected_fingerprint:
        raise RecoveryHold("Live retained/plugin fingerprint changed since audit")

    try:
        create_payload = require_object(
            call_helper(
                client,
                route=identity["route"],
                token=token,
                helper_sha256=helper_hash,
                action="snapshot_create",
                extra={"confirmation": "SNAPSHOT-LIVE-NADLAN-CONFIG-1.72.207"},
                timeout=300,
            ),
            "Live plugin snapshot creation",
        )
    except (NetworkRequestFailed, RuntimeError) as create_error:
        try:
            reconciled = call_helper_object_retry(
                client,
                route=identity["route"],
                token=token,
                helper_sha256=helper_hash,
                action="snapshot_status",
                label="Response-lost snapshot creation reconciliation",
                timeout=300,
            )
        except Exception:
            raise create_error
        create_payload = {
            "schema": "nadlan-einstein-live-plugin-snapshot-create/v1",
            "idempotent": True,
            "manifest": reconciled.get("manifest"),
            "audit": current_audit,
        }
    if create_payload.get("schema") != "nadlan-einstein-live-plugin-snapshot-create/v1":
        raise RuntimeError("Snapshot creation response schema is invalid")
    manifest = validate_manifest(
        create_payload.get("manifest")
        if isinstance(create_payload.get("manifest"), dict)
        else {},
        source_commit=source["commit"],
        audit_fingerprint=expected_fingerprint,
        token=token,
        storage_slug=identity["storage_slug"],
    )

    storage_guard_payload = call_helper_object_retry(
        client,
        route=identity["route"],
        token=token,
        helper_sha256=helper_hash,
        action="storage_status",
        label="Private snapshot storage guard",
    )
    storage_guard = storage_guard_payload.get("storage")
    if not (
        isinstance(storage_guard, dict)
        and storage_guard.get("outside_webroot") is True
        and storage_guard.get("root_mode") == "0700"
        and storage_guard.get("exact_entries") == ["snapshot.json", "snapshot.zip"]
        and storage_guard.get("entry_modes")
        == {"snapshot.json": "0400", "snapshot.zip": "0400"}
    ):
        raise RecoveryHold("Snapshot storage is not the exact private contract")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    archive_hash = manifest["archive"]["sha256"]
    archive_path = (
        args.output_dir / f"nadlan-config-1.72.207-live-{archive_hash[:12]}.zip"
    )
    extract_root = args.output_dir / f"nadlan-config-1.72.207-live-{archive_hash[:12]}"
    report_path = args.output_dir / f"snapshot-{archive_hash[:12]}.json"
    if archive_path.exists() or extract_root.exists() or report_path.exists():
        raise RuntimeError("Snapshot local output target already exists")

    archive_digest = hashlib.sha256()
    downloaded = 0
    with archive_path.open("xb") as handle:
        for index in range(int(manifest["archive"]["chunks"])):
            chunk = call_helper_object_retry(
                client,
                route=identity["route"],
                token=token,
                helper_sha256=helper_hash,
                action="download_chunk",
                label=f"Snapshot chunk {index}",
                extra={"archive_sha256": archive_hash, "index": index},
                timeout=120,
                attempts=3,
            )
            try:
                data = base64.b64decode(str(chunk.get("data_b64") or ""), validate=True)
            except (ValueError, TypeError) as error:
                raise RuntimeError("Snapshot chunk base64 is invalid") from error
            if not (
                chunk.get("schema") == "nadlan-einstein-live-plugin-snapshot-chunk/v1"
                and chunk.get("archive_sha256") == archive_hash
                and chunk.get("index") == index
                and chunk.get("chunks") == manifest["archive"]["chunks"]
                and chunk.get("offset") == downloaded
                and chunk.get("bytes") == len(data)
                and len(data)
                == min(CHUNK_BYTES, manifest["archive"]["bytes"] - downloaded)
                and chunk.get("chunk_sha256") == sha256_bytes(data)
                and chunk.get("chunk_sha256")
                == manifest["archive"]["chunk_sha256"][index]
            ):
                raise RuntimeError("Snapshot chunk contract changed")
            handle.write(data)
            archive_digest.update(data)
            downloaded += len(data)
        handle.flush()
        os.fsync(handle.fileno())
    if (
        downloaded != manifest["archive"]["bytes"]
        or archive_digest.hexdigest() != archive_hash
    ):
        raise RecoveryHold("Downloaded snapshot full archive identity failed")

    status_payload = call_helper_object_retry(
        client,
        route=identity["route"],
        token=token,
        helper_sha256=helper_hash,
        action="snapshot_status",
        label="Post-download server snapshot status",
        timeout=300,
    )
    if status_payload.get("schema") != "nadlan-einstein-live-plugin-snapshot-status/v1":
        raise RuntimeError("Post-download snapshot status schema is invalid")
    status_manifest = validate_manifest(
        status_payload.get("manifest")
        if isinstance(status_payload.get("manifest"), dict)
        else {},
        source_commit=source["commit"],
        audit_fingerprint=expected_fingerprint,
        token=token,
        storage_slug=identity["storage_slug"],
    )
    if status_manifest != manifest:
        raise RecoveryHold("Server snapshot manifest changed during download")

    extracted_inventory = verify_and_extract_archive(
        archive_path,
        extract_root,
        manifest["plugin"]["inventory"],
        create=True,
    )
    audit_after = validate_audit(
        call_helper_object_retry(
            client,
            route=identity["route"],
            token=token,
            helper_sha256=helper_hash,
            action="audit",
            label="Post-snapshot retained live audit",
            timeout=180,
        )
    )
    if audit_after["audit_fingerprint"] != expected_fingerprint:
        raise RecoveryHold(
            "Retained/plugin fingerprint changed during snapshot capture"
        )

    report = {
        "schema": "nadlan-einstein-live-recovery-client-snapshot/v1",
        "generated_at_utc": utc_now(),
        "source": source,
        "auth": auth,
        "control": audit_report["control"],
        "audit_fingerprint": expected_fingerprint,
        "manifest": manifest,
        "private_storage_guard": storage_guard,
        "download": {
            "archive_path": str(archive_path.resolve()),
            "archive_sha256": archive_hash,
            "archive_bytes": downloaded,
            "chunks": manifest["archive"]["chunks"],
            "extract_root": str(extract_root.resolve()),
            "extracted_inventory": extracted_inventory,
        },
        "server_status_reverified": True,
        "retained_audit_unchanged": True,
        "passed": True,
        "status": "LOCAL_SNAPSHOT_VERIFIED_CLEANUP_PENDING",
    }
    write_report(report_path, report, redactor)
    print(
        json.dumps(
            {
                "status": report["status"],
                "archive_sha256": archive_hash,
                "archive": str(archive_path.resolve()),
                "extracted": str(extract_root.resolve()),
                "report": str(report_path.resolve()),
            },
            separators=(",", ":"),
        )
    )
    return 0


def verify_local_snapshot(
    snapshot_report: dict[str, Any], token: str,
) -> tuple[Path, Path, dict[str, Any]]:
    if (
        snapshot_report.get("schema")
        != "nadlan-einstein-live-recovery-client-snapshot/v1"
    ):
        raise RuntimeError("Snapshot report schema is invalid")
    manifest = snapshot_report.get("manifest")
    download = snapshot_report.get("download")
    source = snapshot_report.get("source")
    if not all(isinstance(row, dict) for row in (manifest, download, source)):
        raise RuntimeError("Snapshot report sections are incomplete")
    manifest = validate_manifest(
        manifest,
        source_commit=str(source.get("commit") or ""),
        audit_fingerprint=str(snapshot_report.get("audit_fingerprint") or ""),
        token=token,
    )
    archive_path = Path(str(download.get("archive_path") or ""))
    extract_root = Path(str(download.get("extract_root") or ""))
    if (
        not archive_path.is_absolute()
        or not extract_root.is_absolute()
        or not archive_path.is_file()
        or archive_path.is_symlink()
        or archive_path.stat().st_size != manifest["archive"]["bytes"]
    ):
        raise RuntimeError("Local snapshot archive identity changed")
    archive_digest = hashlib.sha256()
    with archive_path.open("rb") as handle:
        while True:
            block = handle.read(128 * 1024)
            if not block:
                break
            archive_digest.update(block)
    if archive_digest.hexdigest() != manifest["archive"]["sha256"]:
        raise RuntimeError("Local snapshot archive identity changed")
    verify_and_extract_archive(
        archive_path,
        extract_root,
        manifest["plugin"]["inventory"],
        create=False,
    )
    return archive_path, extract_root, manifest


def cleanup(args: argparse.Namespace) -> int:
    if not SNAPSHOT_ACTIONS_ENABLED or not PINNED_EXPECTED_LIVE_CONTRACT:
        raise RecoveryHold(
            "Phase-B cleanup is structurally disabled until the reviewed live "
            "baseline is pinned in a separate commit"
        )
    if args.confirm_cleanup != "CLEANUP-VERIFIED-SNAPSHOT-AND-HELPER":
        raise RuntimeError("Exact cleanup confirmation is required")
    source = source_facts(args.expected_source_commit)
    base_url, user, password, token, redactor = resolve_runtime(args.env)
    snapshot_report = read_json_object(args.snapshot_report)
    archive_path, extract_root, manifest = verify_local_snapshot(snapshot_report, token)
    if snapshot_report["source"].get("commit") != source["commit"]:
        raise RuntimeError("Snapshot report source commit differs")
    control = snapshot_report.get("control")
    if not isinstance(control, dict):
        raise RuntimeError("Snapshot report control is unavailable")
    identity = session_identity(token)
    helper_id = int(control.get("helper_id") or 0)
    helper_hash = str(control.get("helper_sha256") or "")
    if (
        helper_id < 1
        or helper_id in (449, 450)
        or control.get("route") != identity["route"]
        or control.get("helper_name") != identity["helper_name"]
        or not HASH_RE.fullmatch(helper_hash)
    ):
        raise RuntimeError("Snapshot cleanup control identity changed")
    client = WordpressClient(base_url, user, password)
    auth = auth_preflight(client)
    helper_code, _ = render_helper(
        token=token, helper_id=helper_id, source_commit=source["commit"]
    )
    expected_helper = helper_expected(helper_id, helper_code, identity, active=True)
    if expected_helper["code_sha256"] != helper_hash:
        raise RuntimeError("Cleanup helper source hash differs")
    verify_helper_row(client, helper_id, expected_helper)

    storage_preflight = call_helper_object_retry(
        client,
        route=identity["route"],
        token=token,
        helper_sha256=helper_hash,
        action="storage_status",
        label="Pre-cleanup snapshot storage status",
        timeout=300,
    )
    storage_preflight_evidence = storage_preflight.get("storage")
    if not isinstance(storage_preflight_evidence, dict):
        raise RuntimeError("Pre-cleanup snapshot storage evidence is invalid")
    checkpoint = reserve_terminal_report(
        args.report,
        {
            "operation": "verified_snapshot_and_helper_cleanup",
            "source_commit": source["commit"],
            "helper_id": helper_id,
            "helper_sha256": helper_hash,
            "archive_sha256": manifest["archive"]["sha256"],
            "archive_path": str(archive_path.resolve()),
            "extract_root": str(extract_root.resolve()),
            "storage_preflight": storage_preflight_evidence,
        },
        redactor,
    )
    storage_initially_absent = storage_preflight_evidence.get("absent") is True
    if not storage_initially_absent:
        entries = storage_preflight_evidence.get("exact_entries")
        if not isinstance(entries, list):
            raise RuntimeError("Pre-cleanup snapshot entry evidence is invalid")
        complete_pair = "snapshot.json" in entries and "snapshot.zip" in entries
        if complete_pair:
            status = call_helper_object_retry(
                client,
                route=identity["route"],
                token=token,
                helper_sha256=helper_hash,
                action="snapshot_status",
                label="Pre-cleanup server snapshot status",
                timeout=300,
            )
            server_manifest = validate_manifest(
                status.get("manifest")
                if isinstance(status.get("manifest"), dict)
                else {},
                source_commit=source["commit"],
                audit_fingerprint=snapshot_report["audit_fingerprint"],
                token=token,
                storage_slug=identity["storage_slug"],
            )
            if server_manifest != manifest:
                raise RecoveryHold("Server snapshot changed before cleanup")
        else:
            partial_cleanup = call_helper_object_retry(
                client,
                route=identity["route"],
                token=token,
                helper_sha256=helper_hash,
                action="cleanup_snapshot",
                extra={
                    "confirmation": "CLEANUP-OWN-PARTIAL-SNAPSHOT",
                    "archive_sha256": "",
                    "allow_partial": True,
                },
                label="Interrupted snapshot cleanup convergence",
            )
            if (
                partial_cleanup.get("schema")
                != "nadlan-einstein-live-plugin-snapshot-cleanup/v1"
                or partial_cleanup.get("absent") is not True
            ):
                raise RecoveryHold("Interrupted snapshot cleanup did not converge")
            storage_initially_absent = True
    try:
        audit_before_payload = call_helper_object_retry(
            client,
            route=identity["route"],
            token=token,
            helper_sha256=helper_hash,
            action="audit",
            label="Pre-cleanup retained live audit",
        )
        audit_before = validate_audit(audit_before_payload)
        retained_unchanged = (
            audit_before["audit_fingerprint"] == snapshot_report["audit_fingerprint"]
        )
    except RuntimeError:
        # Retained drift is important evidence, but it must never strand this
        # vehicle's own snapshot/helper. Cleanup scope remains exact and local.
        retained_unchanged = False

    cleanup_response_reconciled = storage_initially_absent
    cleanup_payload = {
        "schema": "nadlan-einstein-live-plugin-snapshot-cleanup/v1",
        "idempotent": True,
        "absent": True,
    }
    try:
        if not storage_initially_absent:
            cleanup_payload = require_object(
                call_helper(
                    client,
                    route=identity["route"],
                    token=token,
                    helper_sha256=helper_hash,
                    action="cleanup_snapshot",
                    extra={
                        "confirmation": "CLEANUP-VERIFIED-LIVE-SNAPSHOT",
                        "archive_sha256": manifest["archive"]["sha256"],
                        "allow_partial": False,
                    },
                ),
                "Run-owned snapshot cleanup",
            )
    except (NetworkRequestFailed, RuntimeError) as cleanup_error:
        reconciled_storage = call_helper_object_retry(
            client,
            route=identity["route"],
            token=token,
            helper_sha256=helper_hash,
            action="storage_status",
            label="Response-lost snapshot cleanup reconciliation",
        )
        storage_evidence = reconciled_storage.get("storage")
        if not isinstance(storage_evidence, dict):
            raise cleanup_error
        if storage_evidence.get("absent") is not True:
            entries = storage_evidence.get("exact_entries")
            if not isinstance(entries, list):
                raise cleanup_error
            complete_pair = "snapshot.json" in entries and "snapshot.zip" in entries
            retry_extra = (
                {
                    "confirmation": "CLEANUP-VERIFIED-LIVE-SNAPSHOT",
                    "archive_sha256": manifest["archive"]["sha256"],
                    "allow_partial": False,
                }
                if complete_pair
                else {
                    "confirmation": "CLEANUP-OWN-PARTIAL-SNAPSHOT",
                    "archive_sha256": "",
                    "allow_partial": True,
                }
            )
            try:
                cleanup_retry = call_helper_object_retry(
                    client,
                    route=identity["route"],
                    token=token,
                    helper_sha256=helper_hash,
                    action="cleanup_snapshot",
                    extra=retry_extra,
                    label="Snapshot cleanup convergence retry",
                )
            except Exception:
                raise cleanup_error
            if (
                cleanup_retry.get("schema")
                != "nadlan-einstein-live-plugin-snapshot-cleanup/v1"
                or cleanup_retry.get("absent") is not True
            ):
                raise cleanup_error
        cleanup_response_reconciled = True
    if (
        cleanup_payload.get("schema")
        != "nadlan-einstein-live-plugin-snapshot-cleanup/v1"
        or cleanup_payload.get("absent") is not True
    ):
        raise RecoveryHold("Run-owned snapshot cleanup absence proof failed")
    storage_after = call_helper_object_retry(
        client,
        route=identity["route"],
        token=token,
        helper_sha256=helper_hash,
        action="storage_status",
        label="Independent snapshot storage absence",
    )
    if (
        not isinstance(storage_after.get("storage"), dict)
        or storage_after["storage"].get("absent") is not True
    ):
        raise RecoveryHold("Snapshot storage remains after cleanup")

    direct_absence = False
    delete_response_reconciled = False
    try:
        delete_response = call_helper(
            client,
            route=identity["route"],
            token=token,
            helper_sha256=helper_hash,
            action="delete_self",
            extra={"confirmation": "DELETE-OWN-RECOVERY-HELPER"},
        )
        delete_payload = require_object(
            delete_response, "Recovery helper hard deletion"
        )
        direct_absence = (
            delete_payload.get("schema")
            == "nadlan-einstein-live-recovery-helper-delete/v1"
            and delete_payload.get("helper_id") == helper_id
            and delete_payload.get("direct_snippet_row_count") == 0
            and delete_payload.get("storage_absent") is True
            and delete_payload.get("retained_helpers_unchanged") is True
            and delete_payload.get("mutation_mutex_held") is True
        )
    except (NetworkRequestFailed, RuntimeError):
        delete_response_reconciled = True

    absence = prove_helper_absence(
        client,
        identity=identity,
        token=token,
        helper_id=helper_id,
        helper_hash=helper_hash,
    )
    if not all(
        absence[key]
        for key in (
            "item_absent",
            "collection_absent",
            "route_absent",
            "public_route_absent",
        )
    ):
        raise RecoveryHold("Recovery helper or route absence did not reconcile")
    uncertainty = None
    if not direct_absence:
        uncertainty = "delete_response_lost_direct_database_absence_not_observed"

    report = {
        "schema": "nadlan-einstein-live-recovery-client-cleanup/v1",
        "generated_at_utc": utc_now(),
        "source": source,
        "auth": auth,
        "checkpoint": checkpoint,
        "helper_id": helper_id,
        "archive_sha256": manifest["archive"]["sha256"],
        "local_snapshot_reverified": True,
        "retained_audit_unchanged": retained_unchanged,
        "snapshot_cleanup_response_reconciled": cleanup_response_reconciled,
        "snapshot_storage_directly_absent": True,
        "helper_direct_database_row_count": 0 if direct_absence else None,
        "helper_delete_response_reconciled": delete_response_reconciled,
        "helper_absence": absence,
        "uncertainty": uncertainty,
        "passed": direct_absence,
        "status": (
            (
                "CLEANUP_COMPLETE"
                if retained_unchanged
                else "CLEANUP_COMPLETE_RETAINED_STATE_DRIFT_RECORDED"
            )
            if direct_absence
            else "CLEANUP_RECONCILED_WITH_EXPLICIT_DIRECT_DB_UNCERTAINTY"
        ),
    }
    finalize_terminal_report(args.report, report, redactor)
    print(
        json.dumps(
            {"status": report["status"], "report": str(args.report.resolve())},
            separators=(",", ":"),
        )
    )
    return 0 if direct_absence else 2


def cleanup_partial(args: argparse.Namespace) -> int:
    if not SNAPSHOT_ACTIONS_ENABLED or not PINNED_EXPECTED_LIVE_CONTRACT:
        raise RecoveryHold(
            "Phase-B partial cleanup is structurally disabled until the reviewed "
            "live baseline is pinned in a separate commit"
        )
    if args.confirm_partial_cleanup != "CLEANUP-OWN-PARTIAL-SNAPSHOT":
        raise RuntimeError("Exact partial cleanup confirmation is required")
    source = source_facts(args.expected_source_commit)
    base_url, user, password, token, redactor = resolve_runtime(args.env)
    audit_report = read_json_object(args.audit_report)
    identity, helper_id, helper_hash = validate_control_report(
        audit_report, token, source["commit"]
    )
    client = WordpressClient(base_url, user, password)
    auth_preflight(client)
    helper_code, _ = render_helper(
        token=token, helper_id=helper_id, source_commit=source["commit"]
    )
    verify_helper_row(
        client,
        helper_id,
        helper_expected(helper_id, helper_code, identity, active=True),
    )
    storage_before = call_helper_object_retry(
        client,
        route=identity["route"],
        token=token,
        helper_sha256=helper_hash,
        action="storage_status",
        label="Pre-partial-cleanup storage status",
    )
    checkpoint = reserve_terminal_report(
        args.report,
        {
            "operation": "partial_snapshot_cleanup",
            "source_commit": source["commit"],
            "helper_id": helper_id,
            "helper_sha256": helper_hash,
            "storage_preflight": storage_before.get("storage"),
        },
        redactor,
    )
    payload = require_object(
        call_helper(
            client,
            route=identity["route"],
            token=token,
            helper_sha256=helper_hash,
            action="cleanup_snapshot",
            extra={
                "confirmation": "CLEANUP-OWN-PARTIAL-SNAPSHOT",
                "archive_sha256": "",
                "allow_partial": True,
            },
        ),
        "Partial run-owned snapshot cleanup",
    )
    if payload.get("absent") is not True:
        raise RecoveryHold("Partial run-owned snapshot cleanup absence proof failed")
    storage_after = call_helper_object_retry(
        client,
        route=identity["route"],
        token=token,
        helper_sha256=helper_hash,
        action="storage_status",
        label="Post-partial-cleanup storage absence",
    )
    if not (
        isinstance(storage_after.get("storage"), dict)
        and storage_after["storage"].get("absent") is True
    ):
        raise RecoveryHold("Partial snapshot storage absence is uncertain")
    report = {
        "schema": "nadlan-einstein-live-recovery-client-partial-cleanup/v1",
        "generated_at_utc": utc_now(),
        "source": source,
        "checkpoint": checkpoint,
        "helper_id": helper_id,
        "snapshot_storage_directly_absent": True,
        "helper_retained": True,
        "passed": True,
        "status": "PARTIAL_SNAPSHOT_CLEANED_HELPER_RETAINED",
    }
    finalize_terminal_report(args.report, report, redactor)
    print(
        json.dumps(
            {"status": report["status"], "report": str(args.report.resolve())},
            separators=(",", ":"),
        )
    )
    return 0


class FakeResponse:
    def __init__(
        self,
        status: int,
        body: bytes,
        content_type: str,
        *,
        payload: Any | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.status_code = status
        self.content = body
        self.headers = {"Content-Type": content_type, **(headers or {})}
        self._payload = payload

    def json(self) -> Any:
        if self._payload is None:
            raise ValueError("not json")
        return self._payload


class FakeSession:
    def __init__(self, responses: list[FakeResponse | Exception]):
        self.responses = list(responses)
        self.calls: list[dict[str, Any]] = []
        self.auth: tuple[str, str] | None = None
        self.headers: dict[str, str] = {}

    def request(self, method: str, url: str, **kwargs: Any) -> FakeResponse:
        self.calls.append({"method": method, "url": url, **kwargs})
        if not self.responses:
            raise AssertionError("Unexpected fake network request")
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def secret_scan(paths: Iterable[Path]) -> dict[str, Any]:
    patterns = (
        re.compile(r"Basic\s+[A-Za-z0-9+/]{24,}={0,2}"),
        re.compile(r"(?:[A-Za-z0-9]{4}\s+){5}[A-Za-z0-9]{4}"),
        re.compile(r"https?://[^\s/:]+:[^\s/@]+@"),
    )
    scanned = 0
    for path in paths:
        text = read_lf_source_bytes(path).decode("utf-8")
        scanned += len(text.encode("utf-8"))
        if any(pattern.search(text) for pattern in patterns):
            raise RuntimeError(f"Secret-pattern scan failed: {path.name}")
    return {"files": len(tuple(paths)), "bytes": scanned, "passed": True}


def self_test() -> int:
    tests: dict[str, Any] = {}
    template = read_lf_source_bytes(TEMPLATE_PATH)
    if sha256_bytes(template) != TEMPLATE_SHA256:
        raise RuntimeError("Template source hash constant is stale")
    tests["template_sha256"] = TEMPLATE_SHA256

    redactor = Redactor(("fixture-password", "f" * 64), ("admin",))
    redactor.assert_absent('{"administrator":true}')
    for leaked in ('{"user":"admin"}', '{"value":"fixture-password"}'):
        try:
            redactor.assert_absent(leaked)
        except RuntimeError:
            continue
        raise RuntimeError("Credential redaction fixture did not fail closed")
    tests["credential_redaction"] = True

    fixture_token = "b" * 64
    helper, identity = render_helper(
        token=fixture_token, helper_id=451, source_commit="a" * 40
    )
    if MARKER_RE.search(helper) or "\r" in helper:
        raise RuntimeError("Rendered helper marker/EOL gate failed")
    for required in (
        "current_user_can( 'update_plugins' )",
        "get_header( 'x-nadlan-recovery-token' )",
        "get_param( 'token' )",
        "SELECT id, name, code, scope, active",
        "SELECT option_id, option_name, option_value, autoload",
        "SELECT COUNT(*) FROM {$snippets_table} WHERE id = %d",
        "SELECT GET_LOCK(%s, 0)",
        "SELECT RELEASE_LOCK(%s)",
        "sys_get_temp_dir()",
        "auth_hmac_sha256",
        "chunk_sha256",
        "snapshot_create",
        "download_chunk",
        "cleanup_snapshot",
        "delete_self",
        "@is_link",
        "ZipArchive::CHECKCONS",
        "nadlan_release_stage_marker_registration_conflict",
    ):
        present = required in helper
        if required == "nadlan_release_stage_marker_registration_conflict":
            present = not present
        if not present:
            raise RuntimeError(
                f"Rendered helper security marker gate failed: {required}"
            )
    for forbidden in (
        ".htaccess",
        "public_probe_url",
        "wp_upload_dir",
    ):
        if forbidden in helper:
            raise RuntimeError(
                f"Rendered helper contains forbidden public-storage/auth marker: {forbidden}"
            )
    tests["rendered_helper_sha256"] = sha256_bytes(helper.encode("utf-8"))
    tests["session_identity"] = {
        "helper_name_shape": identity["helper_name"].startswith(
            "x-einstein-live-recovery-172207-"
        ),
        "route_shape": identity["route"].startswith(f"{ROUTE_NAMESPACE}/"),
    }

    php = shutil.which("php")
    if not php:
        raise RuntimeError("php is required for rendered helper lint")
    with tempfile.TemporaryDirectory(prefix="einstein-recovery-selftest-") as temp:
        lint_path = Path(temp) / "rendered-helper.php"
        lint_path.write_bytes(b"<?php\n" + helper.encode("utf-8"))
        lint = subprocess.run(
            [php, "-l", str(lint_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        if lint.returncode != 0:
            raise RuntimeError("Rendered recovery helper PHP lint failed")
        tests["rendered_php_lint"] = True

        lf_fixture = Path(temp) / "lf.txt"
        lf_fixture.write_bytes(b"one\ntwo\n")
        if read_lf_source_bytes(lf_fixture) != b"one\ntwo\n":
            raise RuntimeError("LF source fixture failed")
        crlf_fixture = Path(temp) / "crlf.txt"
        crlf_fixture.write_bytes(b"one\r\ntwo\r\n")
        try:
            read_lf_source_bytes(crlf_fixture)
        except RuntimeError:
            tests["crlf_rejected"] = True
        else:
            raise RuntimeError("CRLF source fixture was not rejected")

        archive = Path(temp) / "fixture.zip"
        expected_rows = [
            {"path": "inc/a.php", "bytes": 4, "sha256": sha256_bytes(b"a\n\n\n")},
            {"path": "nadlan-config.php", "bytes": 4, "sha256": sha256_bytes(b"main")},
        ]
        expected_inventory = inventory_contract(expected_rows, ["inc"])
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            bundle.writestr("nadlan-config/", b"")
            bundle.writestr("nadlan-config/inc/", b"")
            bundle.writestr("nadlan-config/inc/a.php", b"a\n\n\n")
            bundle.writestr("nadlan-config/nadlan-config.php", b"main")
        extracted = Path(temp) / "extracted"
        if (
            verify_and_extract_archive(
                archive, extracted, expected_inventory, create=True
            )
            != expected_inventory
        ):
            raise RuntimeError("Safe snapshot extraction fixture failed")
        verify_and_extract_archive(archive, extracted, expected_inventory, create=False)
        tests["archive_roundtrip"] = True
        (extracted / "unexpected.txt").write_text("drift", encoding="utf-8")
        try:
            verify_and_extract_archive(
                archive, extracted, expected_inventory, create=False
            )
        except RuntimeError:
            tests["extracted_extra_file_rejected"] = True
        else:
            raise RuntimeError("Extra extracted file fixture was not rejected")

        malicious = Path(temp) / "malicious.zip"
        with zipfile.ZipFile(malicious, "w") as bundle:
            bundle.writestr("nadlan-config/../escape.php", b"bad")
        try:
            verify_and_extract_archive(
                malicious, Path(temp) / "bad-extract", expected_inventory, create=True
            )
        except RuntimeError:
            tests["path_traversal_rejected"] = True
        else:
            raise RuntimeError("Path-traversal ZIP fixture was not rejected")
        try:
            validate_relative_path("inc/CON.php")
        except RuntimeError:
            tests["windows_device_path_rejected"] = True
        else:
            raise RuntimeError("Windows device-name path fixture was not rejected")

        symlink_archive = Path(temp) / "symlink.zip"
        link_info = zipfile.ZipInfo("nadlan-config/link.php")
        link_info.create_system = 3
        link_info.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(symlink_archive, "w") as bundle:
            bundle.writestr(link_info, b"target.php")
        link_inventory = inventory_contract(
            [
                {
                    "path": "link.php",
                    "bytes": len(b"target.php"),
                    "sha256": sha256_bytes(b"target.php"),
                }
            ]
        )
        try:
            verify_and_extract_archive(
                symlink_archive,
                Path(temp) / "link-extract",
                link_inventory,
                create=True,
            )
        except RuntimeError:
            tests["symlink_rejected"] = True
        else:
            raise RuntimeError("Symlink ZIP fixture was not rejected")

        manifest_storage = ".nadlan-live-recovery-" + "e" * 32
        manifest_base = {
            "schema": "nadlan-einstein-live-plugin-snapshot/v1",
            "run_id": RUN_ID,
            "source_commit": "a" * 40,
            "storage_slug": manifest_storage,
            "created_at_utc": "2026-08-14T12:00:00Z",
            "audit_fingerprint": "d" * 64,
            "plugin": {
                "plugin_file": "nadlan-config/nadlan-config.php",
                "version": "1.72.207",
                "active": True,
                "provenance": "unknown_live_1.72.207_capture",
                "main_file_sha256": "f" * 64,
                "inventory": expected_inventory,
            },
            "archive": {
                "sha256": "c" * 64,
                "bytes": 123,
                "chunk_bytes": CHUNK_BYTES,
                "chunks": 1,
                "chunk_sha256": ["8" * 64],
                "mtime": 1,
            },
        }
        signed_manifest = {
            **manifest_base,
            "contract_sha256": sha256_bytes(exact_json_bytes(manifest_base)),
        }
        valid_manifest = {
            **signed_manifest,
            "auth_hmac_sha256": hmac.new(
                fixture_token.encode("utf-8"),
                exact_json_bytes(signed_manifest),
                hashlib.sha256,
            ).hexdigest(),
        }
        validate_manifest(
            valid_manifest,
            source_commit="a" * 40,
            audit_fingerprint="d" * 64,
            token=fixture_token,
            storage_slug=manifest_storage,
        )
        tampered_manifest = json.loads(json.dumps(valid_manifest))
        tampered_manifest["archive"]["chunk_sha256"][0] = "7" * 64
        try:
            validate_manifest(
                tampered_manifest,
                source_commit="a" * 40,
                audit_fingerprint="d" * 64,
                token=fixture_token,
                storage_slug=manifest_storage,
            )
        except RuntimeError:
            tests["signed_chunk_index_tamper_rejected"] = True
        else:
            raise RuntimeError("Signed chunk index tamper fixture was accepted")
        oversize_manifest = json.loads(json.dumps(valid_manifest))
        oversize_rows = [
            {"path": "huge.bin", "bytes": MAX_FILE_BYTES + 1, "sha256": "9" * 64}
        ]
        oversize_manifest["plugin"]["inventory"] = inventory_contract(oversize_rows)
        oversize_base = {
            key: oversize_manifest[key]
            for key in (
                "schema",
                "run_id",
                "source_commit",
                "storage_slug",
                "created_at_utc",
                "audit_fingerprint",
                "plugin",
                "archive",
            )
        }
        oversize_manifest["contract_sha256"] = sha256_bytes(
            exact_json_bytes(oversize_base)
        )
        oversize_signed = {
            **oversize_base,
            "contract_sha256": oversize_manifest["contract_sha256"],
        }
        oversize_manifest["auth_hmac_sha256"] = hmac.new(
            fixture_token.encode("utf-8"),
            exact_json_bytes(oversize_signed),
            hashlib.sha256,
        ).hexdigest()
        try:
            validate_manifest(
                oversize_manifest,
                source_commit="a" * 40,
                audit_fingerprint="d" * 64,
                token=fixture_token,
                storage_slug=manifest_storage,
            )
        except RuntimeError:
            tests["oversize_rejected"] = True
        else:
            raise RuntimeError("Oversize manifest fixture was not rejected")

        raw_snapshot_base = {
            "schema": "nadlan-einstein-public-raw-snapshot/v1",
            "post_id": 4867,
            "core": {
                "ID": "4867",
                "post_author": "1",
                "post_content": "fixture",
                "post_status": "publish",
            },
            "meta": [
                {
                    "meta_id": "10",
                    "post_id": "4867",
                    "meta_key": "fixture_key",
                    "meta_value": "fixture_value",
                }
            ],
            "terms": [
                {
                    "object_id": "4867",
                    "term_taxonomy_id": "2",
                    "term_order": "0",
                }
            ],
        }
        raw_snapshot = {
            **raw_snapshot_base,
            "contract_sha256": sha256_bytes(exact_json_bytes(raw_snapshot_base)),
        }
        validate_raw_snapshot(raw_snapshot, 4867)
        reordered_snapshot = json.loads(json.dumps(raw_snapshot))
        reordered_snapshot["core"] = {
            "post_author": "1",
            "ID": "4867",
            "post_content": "fixture",
            "post_status": "publish",
        }
        try:
            validate_raw_snapshot(reordered_snapshot, 4867)
        except RuntimeError:
            tests["raw_snapshot_key_order_drift_rejected"] = True
        else:
            raise RuntimeError("Raw snapshot key-order drift fixture was accepted")

        checkpoint_path = Path(temp) / "terminal-checkpoint.json"
        checkpoint = reserve_terminal_report(
            checkpoint_path,
            {"operation": "offline_fixture", "identity_sha256": "1" * 64},
            Redactor(("never-written-secret",)),
        )
        if (
            read_json_object(checkpoint_path).get("status")
            != "PREPARED_BEFORE_DESTRUCTIVE_CLEANUP"
        ):
            raise RuntimeError("Durable terminal checkpoint fixture failed")
        finalize_terminal_report(
            checkpoint_path,
            {
                "schema": "offline-terminal-fixture/v1",
                "checkpoint": checkpoint,
                "passed": True,
            },
            Redactor(("never-written-secret",)),
        )
        if read_json_object(checkpoint_path).get("passed") is not True:
            raise RuntimeError("Atomic terminal report finalize fixture failed")
        if list(Path(temp).glob(".terminal-checkpoint.json.final-*")):
            raise RuntimeError("Atomic terminal report left a temporary file")
        tests["durable_terminal_checkpoint_and_atomic_finalize"] = True

    # Every transport response is injected. The optional HTTP dependency must
    # remain unloaded, making the CI self-test genuinely stdlib-only.
    if _REQUESTS is not None:
        raise RuntimeError("Self-test started after the optional HTTP module loaded")
    try:
        success_session = FakeSession(
            [FakeResponse(200, b"{}", "application/json", payload={})]
        )
        client = WordpressClient(
            "https://nad-lan.co.il", "u", "p", session=success_session
        )  # type: ignore[arg-type]
        if client.request("POST", "example/v1/run", json_body={}).status_code != 200:
            raise RuntimeError("Transport success fixture failed")
        if len(success_session.calls) != 1:
            raise RuntimeError("Transport success used a fallback")
        helper_session = FakeSession(
            [FakeResponse(200, b"{}", "application/json", payload={})]
        )
        helper_client = WordpressClient(
            "https://nad-lan.co.il", "u", "p", session=helper_session
        )  # type: ignore[arg-type]
        call_helper(
            helper_client,
            route="nadlan-live-recovery/v1/fixture-route",
            token=fixture_token,
            helper_sha256="1" * 64,
            action="audit",
        )
        helper_call = helper_session.calls[0]
        if (
            fixture_token in str(helper_call["url"])
            or "token" in helper_call["json"]
            or helper_call["headers"]
            != {"X-Nadlan-Recovery-Token": fixture_token}
        ):
            raise RuntimeError("Helper token transport is not header-only")
        tests["header_only_token_transport"] = True

        missing_payload = {
            "code": MISSING_SNIPPET_CODE,
            "message": MISSING_SNIPPET_MESSAGE,
        }
        route_missing_payload = {"code": "rest_no_route"}
        absence_session = FakeSession(
            [
                FakeResponse(
                    500,
                    exact_json_bytes(missing_payload),
                    "application/json",
                    payload=missing_payload,
                ),
                FakeResponse(
                    200,
                    b"[]",
                    "application/json",
                    payload=[],
                    headers={"X-WP-TotalPages": "1"},
                ),
                FakeResponse(
                    404,
                    exact_json_bytes(route_missing_payload),
                    "application/json",
                    payload=route_missing_payload,
                ),
            ]
        )
        public_absence_session = FakeSession(
            [
                FakeResponse(
                    404,
                    exact_json_bytes(route_missing_payload),
                    "application/json",
                    payload=route_missing_payload,
                )
            ]
        )
        absence_client = WordpressClient(
            "https://nad-lan.co.il", "u", "p", session=absence_session
        )  # type: ignore[arg-type]
        absence = prove_helper_absence(
            absence_client,
            identity=identity,
            token=fixture_token,
            helper_id=451,
            helper_hash="1" * 64,
            public_session=public_absence_session,
        )
        if not all(
            absence[key]
            for key in (
                "item_absent",
                "collection_absent",
                "route_absent",
                "public_route_absent",
            )
        ):
            raise RuntimeError("Exact helper absence matrix fixture failed")
        public_call = public_absence_session.calls[0]
        if (
            public_absence_session.auth is not None
            or fixture_token in str(public_call)
            or "X-Nadlan-Recovery-Token" in public_call.get("headers", {})
            or public_call.get("allow_redirects") is not False
        ):
            raise RuntimeError("Public route absence request leaked authentication")
        tests["authoritative_and_public_route_absence"] = True

        denial_session = FakeSession(
            [
                FakeResponse(
                    403,
                    b'{"code":"rest_forbidden"}',
                    "application/json",
                    payload={"code": "rest_forbidden"},
                )
            ]
        )
        client = WordpressClient(
            "https://nad-lan.co.il", "u", "p", session=denial_session
        )  # type: ignore[arg-type]
        if client.request("POST", "example/v1/run", json_body={}).status_code != 403:
            raise RuntimeError("JSON denial fixture changed")
        if len(denial_session.calls) != 1:
            raise RuntimeError("JSON WordPress denial incorrectly fell back")

        fallback_session = FakeSession(
            [
                FakeResponse(403, b"<!doctype html><html>", "text/html"),
                FakeResponse(200, b"{}", "application/json", payload={}),
            ]
        )
        client = WordpressClient(
            "https://nad-lan.co.il", "u", "p", session=fallback_session
        )  # type: ignore[arg-type]
        if (
            client.request("POST", "example/v1/run", json_body={"x": 1}).status_code
            != 200
        ):
            raise RuntimeError("HTML WAF fallback fixture failed")
        if len(fallback_session.calls) != 2:
            raise RuntimeError("HTML WAF fallback count changed")
        if fallback_session.calls[0]["json"] != fallback_session.calls[1]["json"]:
            raise RuntimeError("HTML WAF fallback changed the JSON body")

        malformed_session = FakeSession([FakeResponse(403, b"forbidden", "text/plain")])
        client = WordpressClient(
            "https://nad-lan.co.il", "u", "p", session=malformed_session
        )  # type: ignore[arg-type]
        client.request("POST", "example/v1/run", json_body={})
        if len(malformed_session.calls) != 1:
            raise RuntimeError("Non-HTML 403 incorrectly fell back")

        fallback_failure_session = FakeSession(
            [
                FakeResponse(403, b"<!doctype html><html>", "text/html"),
                FakeResponse(
                    403,
                    b'{"code":"rest_forbidden"}',
                    "application/json",
                    payload={"code": "rest_forbidden"},
                ),
            ]
        )
        client = WordpressClient(
            "https://nad-lan.co.il",
            "u",
            "p",
            session=fallback_failure_session,  # type: ignore[arg-type]
        )
        if client.request("POST", "example/v1/run", json_body={}).status_code != 403:
            raise RuntimeError("Fallback-failure fixture changed")
        if len(fallback_failure_session.calls) != 2:
            raise RuntimeError("Fallback-failure request count changed")

        class OfflineTimeout(Exception):
            pass

        timeout_session = FakeSession([OfflineTimeout("offline timeout fixture")])
        client = WordpressClient(
            "https://nad-lan.co.il",
            "u",
            "p",
            session=timeout_session,  # type: ignore[arg-type]
        )
        try:
            client.request("POST", "example/v1/run", json_body={})
        except OfflineTimeout:
            tests["timeout_fail_closed"] = True
        else:
            raise RuntimeError("Timeout fixture did not fail closed")
    finally:
        if _REQUESTS is not None:
            raise RuntimeError("Self-test lazy-loaded the optional HTTP module")
    tests["stdlib_only_lazy_http_dependency"] = True
    tests["transport_matrix_blocked_network"] = True
    authority_calls: list[list[str]] = []

    def authority_runner(command: list[str], **_kwargs: Any) -> Any:
        authority_calls.append(command)
        if command[1:3] == ["fetch", "--no-tags"]:
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
        if command[1:3] == ["rev-parse", "--verify"]:
            return subprocess.CompletedProcess(
                command, 0, stdout="2" * 40 + "\n", stderr=""
            )
        if command[1:3] == ["merge-base", "--is-ancestor"]:
            return subprocess.CompletedProcess(command, 0, stdout=b"", stderr=b"")
        raise AssertionError("Unexpected fresh-main fixture command")

    if fresh_main_authority("1" * 40, process_runner=authority_runner) != "2" * 40:
        raise RuntimeError("Fresh-main authority fixture returned the wrong commit")
    if authority_calls != [
        [
            "git",
            "fetch",
            "--no-tags",
            "--no-recurse-submodules",
            "origin",
            "main",
        ],
        ["git", "rev-parse", "--verify", "FETCH_HEAD^{commit}"],
        ["git", "merge-base", "--is-ancestor", "1" * 40, "2" * 40],
    ]:
        raise RuntimeError("Fresh-main authority command sequence changed")

    def failed_fetch_runner(command: list[str], **_kwargs: Any) -> Any:
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="offline")

    try:
        fresh_main_authority("1" * 40, process_runner=failed_fetch_runner)
    except RuntimeError:
        tests["fresh_fetch_failure_rejected"] = True
    else:
        raise RuntimeError("Fresh-main fetch failure fixture was accepted")
    tests["fresh_fetch_head_authority_not_cached_origin"] = True
    parser_choices = build_parser()._subparsers._group_actions[0].choices
    if set(parser_choices) != {"self-test", "audit", "cleanup-helper"}:
        raise RuntimeError("Phase-A parser exposes a Phase-B action")
    tests["phase_b_commands_structurally_absent"] = True
    tests["secret_scan"] = secret_scan(SOURCE_PATHS)
    tests["passed"] = True
    print(json.dumps(tests, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("self-test", help="Run offline tests only")

    def live_common(command: argparse.ArgumentParser) -> None:
        command.add_argument("--env", type=Path)
        command.add_argument("--expected-source-commit", required=True)

    audit = subparsers.add_parser(
        "audit", help="Create helper and run stable read-only audit"
    )
    live_common(audit)
    audit.add_argument("--report", type=Path, required=True)
    audit.add_argument("--confirm-create-helper", required=True)

    helper_cleanup = subparsers.add_parser(
        "cleanup-helper", help="Terminally remove the exact Phase-A audit helper"
    )
    live_common(helper_cleanup)
    helper_authority = helper_cleanup.add_mutually_exclusive_group(required=True)
    helper_authority.add_argument("--audit-report", type=Path)
    helper_authority.add_argument(
        "--helper-id",
        type=int,
        help="Exact interrupted helper ID reported by a failed audit attempt",
    )
    helper_cleanup.add_argument("--report", type=Path, required=True)
    helper_cleanup.add_argument("--confirm-cleanup", required=True)

    if SNAPSHOT_ACTIONS_ENABLED:
        snap = subparsers.add_parser(
            "snapshot", help="Create/download verified live plugin snapshot"
        )
        live_common(snap)
        snap.add_argument("--audit-report", type=Path, required=True)
        snap.add_argument("--output-dir", type=Path, required=True)
        snap.add_argument("--confirm-snapshot", required=True)

        clean = subparsers.add_parser(
            "cleanup", help="Remove verified snapshot and own helper"
        )
        live_common(clean)
        clean.add_argument("--snapshot-report", type=Path, required=True)
        clean.add_argument("--report", type=Path, required=True)
        clean.add_argument("--confirm-cleanup", required=True)

        partial = subparsers.add_parser(
            "cleanup-partial",
            help="Remove only an interrupted run-owned partial snapshot",
        )
        live_common(partial)
        partial.add_argument("--audit-report", type=Path, required=True)
        partial.add_argument("--report", type=Path, required=True)
        partial.add_argument("--confirm-partial-cleanup", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    if effective_argv == ["--self-test"]:
        return self_test()
    args = build_parser().parse_args(effective_argv)
    if args.command == "self-test":
        return self_test()
    if args.command == "audit":
        return create_and_audit(args)
    if args.command == "cleanup-helper":
        return cleanup_audit_helper(args)
    if args.command == "snapshot":
        return snapshot(args)
    if args.command == "cleanup":
        return cleanup(args)
    if args.command == "cleanup-partial":
        return cleanup_partial(args)
    raise RuntimeError("Unknown command")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RecoveryHold as error:
        print(f"HOLD: {error}", file=sys.stderr)
        raise SystemExit(2)
    except NetworkRequestFailed:
        print("ERROR: authenticated network request failed", file=sys.stderr)
        raise SystemExit(1)
    except (RuntimeError, OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
