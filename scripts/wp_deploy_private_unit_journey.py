#!/usr/bin/env python3
"""Guarded nadlan-config release plus a password-protected unit-journey sandbox.

The script intentionally has one target plugin, one source post, and one page
slug. It creates a short-lived Code Snippets REST bridge, verifies the bridge
while inactive, deploys an immutable artifact with a server-side rollback
backup, creates the private sandbox idempotently, and hard-deletes the bridge.
Artifacts may come from an immutable raw commit URL or from the exact canonical
plugin-dist ZIP, which is streamed in bounded authenticated chunks and verified
again server-side before the recorded run-scoped path can be installed.
No credential, token, or sandbox password is written to evidence or stdout.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import urlencode, urlparse

import requests


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPO_ROOT / "scripts" / "templates" / "nadlan-unit-journey-deploy-helper.php.tpl"
PLUGIN_FILE = "nadlan-config/nadlan-config.php"
PLUGIN_ROOT = "nadlan-config"
SOURCE_POST_ID = 6201
PAGE_SLUG = "sandbox-apartment-journey"
PAGE_TITLE = "[PRIVATE] מסע בחירת דירה מלא"
PROJECT_DISPLAY_NAME = "Rainbow Tel Aviv"
ROUTE_NAMESPACE = "nadlan-private-release/v1"
MAX_ARCHIVE_BYTES = 25 * 1024 * 1024
MAX_EXPANDED_BYTES = 100 * 1024 * 1024
MAX_ENTRY_BYTES = 20 * 1024 * 1024
MAX_ENTRIES = 4000
UPLOAD_CHUNK_BYTES = 128 * 1024
MAX_UPLOAD_CHUNKS = 256
MARKER_RE = re.compile(r"__[A-Z0-9_]+__")
EINSTEIN_STAGE_SCHEMA = "nadlan-wordpress-private-stage-request/v1"
EINSTEIN_STAGE_SLUG = "sandbox-einstein-tower-flagship-v3-review"
EINSTEIN_CANONICAL_POST_ID = 4867
EINSTEIN_PROJECT_CONTRACT_ID = "einstein-tower-6885-32"
EINSTEIN_PRIVATE_MARKER = "private-unit-journey-v2"
EINSTEIN_ACCEPTANCE_SCHEMA = "nadlan-einstein-flagship-live-acceptance/v2"
EINSTEIN_ACCEPTANCE_VIEWPORTS = ("320x568", "390x844", "568x320", "1280x800")
EINSTEIN_ACCEPTANCE_ACCESSIBILITY_VIEWPORTS = ("390x844", "568x320")
EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS = {
    "keyboardViewports": 2,
    "keyboardToolChecks": 8,
    "keyboardEscapeRestores": 8,
    "browserHistoryTransitions": 2,
    "textResizeViewports": 2,
    "textResizeDialogChecks": 8,
}
EINSTEIN_ACCEPTANCE_ASSETS = (
    "model-hd.glb",
    "model-lod.glb",
    "poster.webp",
    "experience/representative-apartment-living-v1.webp",
    "experience/representative-apartment-bedroom-v1.webp",
    "experience/facility-arrival-gallery-v1.webp",
    "experience/facility-landscaped-terrace-v1.webp",
)
MISSING_SNIPPET_CODE = "rest_cannot_get"
MISSING_SNIPPET_MESSAGE = "The snippet could not be found."
DEPLOY_PREFLIGHT_SCHEMA = "nadlan-private-release-deploy-preflight/v1"
DEPLOY_FAILURE_CONTRACT = {
    "request_validation": ("artifact_identity_invalid",),
    "lock_acquisition": ("deployment_lock_unavailable",),
    "idempotent_cleanup": ("artifact_cleanup_failed",),
    "preflight": (
        "plugin_state_unavailable",
        "plugin_inactive",
        "prior_backup_present",
    ),
    "artifact_acquisition": ("artifact_download_failed", "upload_path_unavailable"),
    "artifact_verification": (
        "artifact_hash_mismatch",
        "artifact_zip_invalid",
        "artifact_contract_mismatch",
    ),
    "capacity_check": ("disk_space_unavailable", "disk_space_insufficient"),
    "backup_prepare": (
        "backup_destination_unsafe",
        "filesystem_unavailable",
        "upgrade_directory_prepare_failed",
        "backup_root_create_failed",
        "backup_guard_write_failed",
    ),
    "backup_copy": ("plugin_backup_copy_failed",),
    "backup_verify": ("backup_inventory_failed", "backup_digest_mismatch"),
    "backup_commit": ("backup_state_persist_failed",),
    "plugin_install": ("plugin_upgrade_failed",),
    "post_install": (
        "cache_purge_failed",
        "plugin_state_unavailable",
        "plugin_contract_mismatch",
    ),
    "artifact_cleanup": ("artifact_cleanup_failed",),
    "deployment_commit": ("deployment_state_persist_failed",),
}
DEPLOY_FAILURE_CODES = {
    "nadlan_release_artifact_identity_invalid",
    "nadlan_release_locked",
    "nadlan_release_upload_cleanup_failed",
    "nadlan_release_deploy_failed",
}
DEPLOY_FAILURE_REQUIRES_ROLLBACK_STAGES = {
    "plugin_install",
    "post_install",
    "artifact_cleanup",
    "deployment_commit",
}
DEPLOY_FAILURE_PREBACKUP_STAGES = {
    "preflight",
    "artifact_acquisition",
    "artifact_verification",
    "capacity_check",
    "backup_prepare",
    "backup_copy",
    "backup_verify",
}
DEPLOY_FAILURE_CODE_STAGES = {
    "nadlan_release_artifact_identity_invalid": {"request_validation"},
    "nadlan_release_locked": {"lock_acquisition"},
    "nadlan_release_upload_cleanup_failed": {"idempotent_cleanup"},
    "nadlan_release_deploy_failed": (
        DEPLOY_FAILURE_PREBACKUP_STAGES
        | {"backup_commit"}
        | DEPLOY_FAILURE_REQUIRES_ROLLBACK_STAGES
    ),
}


class EinsteinStageRecoveryBlocked(RuntimeError):
    """A stage write may have landed, but exact rollback scope cannot be proved."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def exact_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def validate_einstein_stage_request(path: Path) -> dict[str, Any]:
    """Load the one governed Einstein stage payload and fail closed on scope drift."""
    expected_path = REPO_ROOT / "docs" / "wp-drafts" / "einstein-tower-flagship-v3-private-stage.json"
    resolved = path.expanduser().resolve(strict=True)
    if os.path.normcase(str(resolved)) != os.path.normcase(str(expected_path.resolve(strict=True))):
        raise ValueError("--einstein-stage-request must be the exact governed WordPress draft")
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema") != EINSTEIN_STAGE_SCHEMA:
        raise ValueError("Einstein stage request schema is invalid")
    lookup = payload.get("lookup") if isinstance(payload.get("lookup"), dict) else {}
    body = payload.get("body") if isinstance(payload.get("body"), dict) else {}
    meta = body.get("meta") if isinstance(body.get("meta"), dict) else {}
    expected = payload.get("expected") if isinstance(payload.get("expected"), dict) else {}
    secret_contract = payload.get("secret_injection")
    password_contract = (
        secret_contract.get("post_password") if isinstance(secret_contract, dict) else {}
    )
    if (
        payload.get("operation") != "create_or_replace_exact_private_sandbox"
        or payload.get("endpoint") != "https://nad-lan.co.il/wp-json/wp/v2/nadlan_project"
        or
        lookup.get("post_type") != "nadlan_project"
        or lookup.get("exact_slug") != EINSTEIN_STAGE_SLUG
        or int(lookup.get("canonical_source_post_id") or 0) != EINSTEIN_CANONICAL_POST_ID
        or lookup.get("duplicate_catalog_source_id_forbidden") is not True
        or body.get("slug") != EINSTEIN_STAGE_SLUG
        or body.get("status") != "publish"
        or not isinstance(body.get("title"), str)
        or not isinstance(body.get("excerpt"), str)
        or not isinstance(body.get("content"), str)
        or not body["content"]
        or meta.get("source_id") != ""
        or meta.get("_nadlan_private_unit_journey") != EINSTEIN_PRIVATE_MARKER
        or int(meta.get("_nadlan_flagship_source_post_id") or 0) != EINSTEIN_CANONICAL_POST_ID
        or meta.get("project_contract_id") != EINSTEIN_PROJECT_CONTRACT_ID
        or expected.get("public_visibility") != "password_protected_only"
        or expected.get("anonymous_rest_presence") is not False
        or expected.get("collection_presence") is not False
        or not isinstance(password_contract, dict)
        or password_contract.get("environment_variable") != "SANDBOX_POST_PASSWORD"
        or password_contract.get("inject_at") != "body.password"
        or password_contract.get("required") is not True
        or password_contract.get("serialized_value_forbidden") is not True
    ):
        raise ValueError("Einstein stage request violates the exact private-stage contract")
    forbidden_body_keys = {"id", "date", "author", "link", "guid"}.intersection(body)
    if forbidden_body_keys:
        raise ValueError("Einstein stage body contains server-owned fields")
    if "password" in body or "post_password" in exact_json_bytes(body).decode("utf-8"):
        raise ValueError("Einstein stage request must not serialize a password")
    contract_hashes = payload.get("contract_hashes")
    if not isinstance(contract_hashes, dict):
        raise ValueError("Einstein stage request lacks contract hashes")
    hash_map = {
        "article_sha256": body["content"],
        "identity_sha256": meta.get("project_identity_contract_json"),
        "representations_sha256": meta.get("project_representation_registry_json"),
        "visual_sha256": meta.get("project_visual_playground_json"),
        "buyer_decision_sha256": meta.get("project_buyer_decision_contract_json"),
        "experiences_sha256": meta.get("project_experience_registry_json"),
    }
    for hash_name, source_value in hash_map.items():
        expected_hash = str(contract_hashes.get(hash_name) or "")
        if not isinstance(source_value, str) or not re.fullmatch(r"[a-f0-9]{64}", expected_hash):
            raise ValueError(f"Einstein stage hash contract is incomplete: {hash_name}")
        if not secrets.compare_digest(sha256_text(source_value), expected_hash):
            raise ValueError(f"Einstein stage hash mismatch: {hash_name}")
    project_package = (
        REPO_ROOT / "assets" / "projects" / "einstein-tower" / "contracts" / "flagship-project.json"
    )
    package_hash = str(contract_hashes.get("project_package_sha256") or "")
    if (
        not project_package.is_file()
        or not re.fullmatch(r"[a-f0-9]{64}", package_hash)
        or not secrets.compare_digest(sha256_bytes(project_package.read_bytes()), package_hash)
    ):
        raise ValueError("Einstein stage project-package hash is stale")
    return payload


def validate_protected_main_artifact(
    commit_sha: str, artifact_path: Path, expected_version: str, expected_sha256: str
) -> dict[str, Any]:
    """Prove local bytes are the exact artifact at current origin/main."""
    if not re.fullmatch(r"[a-f0-9]{40}", commit_sha):
        raise ValueError("--protected-main-commit must be exactly 40 lowercase hex characters")
    try:
        origin_main = subprocess.run(
            ["git", "rev-parse", "origin/main"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=30,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError) as error:
        raise ValueError("Could not resolve protected origin/main") from error
    if not secrets.compare_digest(origin_main, commit_sha):
        raise ValueError("--protected-main-commit must equal the current origin/main commit")
    repository_path = f"plugin-dist/nadlan-config-{expected_version}.zip"
    try:
        committed = subprocess.run(
            ["git", "show", f"{commit_sha}:{repository_path}"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            timeout=120,
            check=True,
        ).stdout
    except (OSError, subprocess.SubprocessError) as error:
        raise ValueError("Protected-main release artifact is missing") from error
    committed_sha256 = sha256_bytes(committed)
    local_sha256 = sha256_bytes(artifact_path.read_bytes())
    if not (
        secrets.compare_digest(committed_sha256, expected_sha256)
        and secrets.compare_digest(local_sha256, expected_sha256)
        and secrets.compare_digest(committed, artifact_path.read_bytes())
    ):
        raise ValueError("Canonical local artifact differs from protected origin/main bytes")
    try:
        manifest_raw = subprocess.run(
            ["git", "show", f"{commit_sha}:plugin-dist/nadlan-config.json"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            timeout=30,
            check=True,
        ).stdout
        plugin_main_raw = subprocess.run(
            ["git", "show", f"{commit_sha}:{PLUGIN_FILE.replace(PLUGIN_ROOT + '/', 'plugins/' + PLUGIN_ROOT + '/', 1)}"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            timeout=30,
            check=True,
        ).stdout
        manifest = json.loads(manifest_raw.decode("utf-8"))
        plugin_main = plugin_main_raw.decode("utf-8")
        with zipfile.ZipFile(artifact_path, "r") as archive:
            archive_main = archive.read(PLUGIN_FILE).decode("utf-8")
    except (OSError, UnicodeError, ValueError, KeyError, zipfile.BadZipFile, subprocess.SubprocessError) as error:
        raise ValueError("Protected-main version surfaces could not be inspected") from error
    expected_download = (
        "https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/"
        + repository_path
    )
    header_pattern = re.compile(
        rf"^\s*\*\s*Version:\s*{re.escape(expected_version)}\s*$", re.MULTILINE
    )
    constant_pattern = re.compile(
        rf"define\(\s*'NADLAN_CONFIG_VERSION'\s*,\s*'{re.escape(expected_version)}'\s*\)"
    )
    if (
        not isinstance(manifest, dict)
        or manifest.get("version") != expected_version
        or manifest.get("download_url") != expected_download
        or not header_pattern.search(plugin_main)
        or not constant_pattern.search(plugin_main)
        or not header_pattern.search(archive_main)
        or not constant_pattern.search(archive_main)
    ):
        raise ValueError("Protected-main manifest, source, archive, and expected version disagree")
    return {
        "source_commit_sha": commit_sha,
        "repository_path": repository_path,
        "sha256": committed_sha256,
        "bytes": len(committed),
        "local_equals_protected_main": True,
        "version_surfaces_exact": True,
        "manifest_download_exact": True,
    }


def _raw_field(record: dict[str, Any], name: str) -> str:
    value = record.get(name)
    if isinstance(value, dict) and isinstance(value.get("raw"), str):
        return value["raw"]
    return value if isinstance(value, str) else ""


def wordpress_post_snapshot(record: dict[str, Any]) -> dict[str, Any]:
    """Select only mutable fields the stage transaction may touch."""
    meta = record.get("meta") if isinstance(record.get("meta"), dict) else {}
    return {
        "id": int(record.get("id") or 0),
        "slug": str(record.get("slug") or ""),
        "status": str(record.get("status") or ""),
        "title": _raw_field(record, "title"),
        "content": _raw_field(record, "content"),
        "excerpt": _raw_field(record, "excerpt"),
        "password": str(record.get("password") or ""),
        "meta": copy.deepcopy(meta),
    }


def wordpress_post_restore_body(
    snapshot: dict[str, Any], applied_meta_keys: Iterable[str] | None = None
) -> dict[str, Any]:
    meta_keys = list(applied_meta_keys or snapshot["meta"].keys())
    restore_meta = {
        key: copy.deepcopy(snapshot["meta"][key]) if key in snapshot["meta"] else None
        for key in meta_keys
    }
    return {
        "title": snapshot["title"],
        "slug": snapshot["slug"],
        "status": snapshot["status"],
        "content": snapshot["content"],
        "excerpt": snapshot["excerpt"],
        "password": snapshot["password"],
        "meta": restore_meta,
    }


def get_authenticated_post(client: "WordpressClient", post_id: int) -> dict[str, Any]:
    response = client.request(
        "GET", f"wp/v2/nadlan_project/{post_id}?context=edit", timeout=60
    )
    return require_response(response, f"Authenticated project {post_id} read")


def exact_stage_matches(client: "WordpressClient", slug: str) -> list[dict[str, Any]]:
    query = urlencode(
        {
            "slug": slug,
            "context": "edit",
            "status": "any",
            "per_page": 100,
        }
    )
    response = client.request("GET", f"wp/v2/nadlan_project?{query}", timeout=60)
    if response.status_code < 200 or response.status_code >= 300:
        require_response(response, "Exact Einstein stage lookup")
    payload = response.json()
    if not isinstance(payload, list):
        raise RuntimeError("Exact Einstein stage lookup did not return a collection")
    return [row for row in payload if isinstance(row, dict) and row.get("slug") == slug]


def assert_owned_einstein_stage(record: dict[str, Any]) -> None:
    post_id = int(record.get("id") or 0)
    meta = record.get("meta") if isinstance(record.get("meta"), dict) else {}
    if (
        post_id < 1
        or post_id == EINSTEIN_CANONICAL_POST_ID
        or record.get("slug") != EINSTEIN_STAGE_SLUG
        or meta.get("_nadlan_private_unit_journey") != EINSTEIN_PRIVATE_MARKER
        or int(meta.get("_nadlan_flagship_source_post_id") or 0) != EINSTEIN_CANONICAL_POST_ID
        or meta.get("project_contract_id") != EINSTEIN_PROJECT_CONTRACT_ID
        or meta.get("source_id") != ""
    ):
        raise RuntimeError("Existing slug is not the exact owned Einstein private stage")


def assert_einstein_stage_readback(
    record: dict[str, Any], request_payload: dict[str, Any], post_password: str
) -> dict[str, Any]:
    body = request_payload["body"]
    expected_meta = body["meta"]
    observed = wordpress_post_snapshot(record)
    if (
        observed["id"] < 1
        or observed["id"] == EINSTEIN_CANONICAL_POST_ID
        or observed["slug"] != EINSTEIN_STAGE_SLUG
        or observed["status"] != "publish"
        or observed["title"] != body["title"]
        or observed["content"] != body["content"]
        or observed["excerpt"] != body["excerpt"]
        or observed["password"] != post_password
    ):
        raise RuntimeError("Einstein stage authenticated readback differs from the request")
    for key, expected_value in expected_meta.items():
        if key not in observed["meta"] or observed["meta"][key] != expected_value:
            raise RuntimeError(f"Einstein stage meta readback mismatch: {key}")
    hashes = request_payload["contract_hashes"]
    content_hash = sha256_text(observed["content"])
    meta_hashes = {
        "identity_sha256": sha256_text(str(observed["meta"]["project_identity_contract_json"])),
        "representations_sha256": sha256_text(
            str(observed["meta"]["project_representation_registry_json"])
        ),
        "visual_sha256": sha256_text(str(observed["meta"]["project_visual_playground_json"])),
        "buyer_decision_sha256": sha256_text(
            str(observed["meta"]["project_buyer_decision_contract_json"])
        ),
        "experiences_sha256": sha256_text(
            str(observed["meta"]["project_experience_registry_json"])
        ),
    }
    if not secrets.compare_digest(content_hash, str(hashes["article_sha256"])):
        raise RuntimeError("Einstein stage content hash failed authenticated readback")
    for name, digest in meta_hashes.items():
        if not secrets.compare_digest(digest, str(hashes[name])):
            raise RuntimeError(f"Einstein stage contract hash failed readback: {name}")
    return {
        "post_id": observed["id"],
        "slug": observed["slug"],
        "status": observed["status"],
        "password_present": bool(observed["password"]),
        "source_id_blank": observed["meta"].get("source_id") == "",
        "private_marker_exact": observed["meta"].get("_nadlan_private_unit_journey")
        == EINSTEIN_PRIVATE_MARKER,
        "source_post_crosswalk_exact": int(
            observed["meta"].get("_nadlan_flagship_source_post_id") or 0
        )
        == EINSTEIN_CANONICAL_POST_ID,
        "project_contract_exact": observed["meta"].get("project_contract_id")
        == EINSTEIN_PROJECT_CONTRACT_ID,
        "article_sha256": content_hash,
        "meta_hashes": meta_hashes,
    }


def write_einstein_stage(
    client: "WordpressClient", request_payload: dict[str, Any], post_password: str
) -> dict[str, Any]:
    """Apply one exact REST mutation and retain an in-memory rollback snapshot."""
    matches = exact_stage_matches(client, EINSTEIN_STAGE_SLUG)
    if len(matches) > 1:
        raise RuntimeError("Einstein private-stage slug is ambiguous")
    before_public = wordpress_post_snapshot(
        get_authenticated_post(client, EINSTEIN_CANONICAL_POST_ID)
    )
    before_public_hash = sha256_bytes(exact_json_bytes(before_public))
    prior_snapshot: dict[str, Any] | None = None
    target_id: int | None = None
    if matches:
        assert_owned_einstein_stage(matches[0])
        target_id = int(matches[0]["id"])
        prior_snapshot = wordpress_post_snapshot(get_authenticated_post(client, target_id))

    body = copy.deepcopy(request_payload["body"])
    body["password"] = post_password
    route = "wp/v2/nadlan_project" if target_id is None else f"wp/v2/nadlan_project/{target_id}"
    transaction: dict[str, Any] = {
        "post_id": int(target_id or 0),
        "created_new": prior_snapshot is None,
        "prior_snapshot": prior_snapshot,
        "applied_meta_keys": sorted(body["meta"]),
        "canonical_public_snapshot": before_public,
        "canonical_public_sha256": before_public_hash,
    }
    try:
        response = client.request("POST", route, json_body=body, timeout=180)
        written = require_response(response, "Exact Einstein private-stage write")
        written_id = int(written.get("id") or 0)
        if written_id < 1 or written_id == EINSTEIN_CANONICAL_POST_ID:
            raise RuntimeError("Einstein stage write returned an unsafe post ID")
        transaction["post_id"] = written_id
        readback = get_authenticated_post(client, written_id)
        proof = assert_einstein_stage_readback(readback, request_payload, post_password)
        link = str(readback.get("link") or written.get("link") or "")
        parsed_link = urlparse(link)
        if (
            parsed_link.scheme != "https"
            or parsed_link.hostname != "nad-lan.co.il"
            or parsed_link.username
            or parsed_link.password
            or parsed_link.fragment
            or EINSTEIN_STAGE_SLUG not in parsed_link.path
        ):
            raise RuntimeError("Einstein stage readback returned an unsafe URL")
        after_public = wordpress_post_snapshot(
            get_authenticated_post(client, EINSTEIN_CANONICAL_POST_ID)
        )
        after_public_hash = sha256_bytes(exact_json_bytes(after_public))
        if not secrets.compare_digest(before_public_hash, after_public_hash):
            raise RuntimeError("Canonical public Einstein post 4867 changed during private staging")
        transaction.update({"page_url": link, "readback": proof})
        return transaction
    except Exception as error:
        try:
            if prior_snapshot is None:
                reconciled = exact_stage_matches(client, EINSTEIN_STAGE_SLUG)
                if len(reconciled) > 1:
                    raise EinsteinStageRecoveryBlocked(
                        "Response-lost create produced an ambiguous exact slug"
                    )
                if reconciled:
                    assert_owned_einstein_stage(reconciled[0])
                    transaction["post_id"] = int(reconciled[0]["id"])
                    rollback_einstein_stage(client, transaction)
                else:
                    raise EinsteinStageRecoveryBlocked(
                        "Response-lost create has no exact-slug match; recovery scope is unproved"
                    )
            else:
                transaction["post_id"] = int(prior_snapshot["id"])
                rollback_einstein_stage(client, transaction)
        except Exception as rollback_error:
            raise EinsteinStageRecoveryBlocked(
                "Einstein stage write became indeterminate and exact rollback is unproved"
            ) from rollback_error
        raise error


def rollback_einstein_stage(client: "WordpressClient", transaction: dict[str, Any]) -> dict[str, Any]:
    post_id = int(transaction["post_id"])
    prior = transaction.get("prior_snapshot")
    if prior is None:
        matches = exact_stage_matches(client, EINSTEIN_STAGE_SLUG)
        if not matches:
            direct = client.request(
                "GET", f"wp/v2/nadlan_project/{post_id}?context=edit", timeout=60
            )
            if direct.status_code == 404:
                stage_proof = {"created_post_deleted": True, "already_absent": True}
                current_public = wordpress_post_snapshot(
                    get_authenticated_post(client, EINSTEIN_CANONICAL_POST_ID)
                )
                current_public_hash = sha256_bytes(exact_json_bytes(current_public))
                if not secrets.compare_digest(
                    current_public_hash, str(transaction["canonical_public_sha256"])
                ):
                    raise RuntimeError("Canonical public post differs after Einstein stage rollback")
                return {
                    **stage_proof,
                    "canonical_public_4867_unchanged": True,
                    "canonical_public_sha256": current_public_hash,
                }
            raise EinsteinStageRecoveryBlocked(
                "Created-stage rollback found the post ID outside the exact slug"
            )
        if len(matches) != 1 or int(matches[0].get("id") or 0) != post_id:
            raise EinsteinStageRecoveryBlocked(
                "Created-stage rollback found an ambiguous or changed exact slug"
            )
        assert_owned_einstein_stage(matches[0])
        response = client.request(
            "DELETE", f"wp/v2/nadlan_project/{post_id}?force=true", timeout=120
        )
        payload = require_response(response, "Einstein stage creation rollback")
        if payload.get("deleted") is not True:
            raise RuntimeError("New Einstein stage deletion was not confirmed")
        direct = client.request("GET", f"wp/v2/nadlan_project/{post_id}?context=edit", timeout=60)
        if direct.status_code != 404 or exact_stage_matches(client, EINSTEIN_STAGE_SLUG):
            raise RuntimeError("New Einstein stage remains after rollback")
        stage_proof: dict[str, Any] = {"created_post_deleted": True}
    else:
        if int(prior.get("id") or 0) != post_id or post_id == EINSTEIN_CANONICAL_POST_ID:
            raise EinsteinStageRecoveryBlocked("Existing-stage rollback identity is invalid")
        current = get_authenticated_post(client, post_id)
        if current.get("slug") != EINSTEIN_STAGE_SLUG:
            raise EinsteinStageRecoveryBlocked("Existing-stage slug changed after write attempt")
        restore_body = wordpress_post_restore_body(
            prior, transaction.get("applied_meta_keys", [])
        )
        response = client.request(
            "POST",
            f"wp/v2/nadlan_project/{post_id}",
            json_body=restore_body,
            timeout=180,
        )
        require_response(response, "Einstein stage update rollback")
        restored = wordpress_post_snapshot(get_authenticated_post(client, post_id))
        if restored != prior:
            raise RuntimeError("Existing Einstein stage rollback did not restore exact mutable fields")
        stage_proof = {
            "existing_post_restored": True,
            "restored_snapshot_sha256": sha256_bytes(exact_json_bytes(restored)),
        }
    current_public = wordpress_post_snapshot(
        get_authenticated_post(client, EINSTEIN_CANONICAL_POST_ID)
    )
    current_public_hash = sha256_bytes(exact_json_bytes(current_public))
    if not secrets.compare_digest(
        current_public_hash, str(transaction["canonical_public_sha256"])
    ):
        raise RuntimeError("Canonical public post differs after Einstein stage rollback")
    return {
        **stage_proof,
        "canonical_public_4867_unchanged": True,
        "canonical_public_sha256": current_public_hash,
    }


def anonymous_einstein_probes(
    base_url: str,
    page_url: str,
    post_id: int,
    request_payload: dict[str, Any],
    post_password: str,
) -> dict[str, Any]:
    """Prove an anonymous visitor can discover only the password challenge."""
    session = requests.Session()
    session.headers.update(
        {"User-Agent": "NadLan-Einstein-Private-Stage-Probe/1.0", "Accept": "*/*"}
    )
    page = session.get(page_url, params={"cb": secrets.token_hex(6)}, timeout=60)
    html = page.text
    robots = page.headers.get("X-Robots-Tag", "").lower()
    cache_control = page.headers.get("Cache-Control", "").lower()
    link_header = page.headers.get("Link", "").lower()
    password_form = "post_password" in html and (
        "action=postpass" in html or "wp-pass.php" in html
    )
    hidden_markers = (
        EINSTEIN_PROJECT_CONTRACT_ID,
        "NADLAN_SHOWROOM",
        "nlfs-article",
        "flagship-private-asset",
        request_payload["expected"]["global_demo_label"],
        post_password,
    )
    if not (
        page.status_code == 200
        and password_form
        and all(marker not in html for marker in hidden_markers)
        and all(token in robots for token in ("noindex", "nofollow", "noarchive"))
        and "private" in cache_control
        and "no-store" in cache_control
        and "api.w.org" not in link_header
        and "oembed" not in link_header
        and "rel=\"canonical\"" not in html.lower()
        and "application/json+oembed" not in html.lower()
        and "application/json\"" not in html.lower()
    ):
        raise RuntimeError("Anonymous Einstein password-gate or discovery-link proof failed")

    direct = session.get(
        f"{base_url}/wp-json/wp/v2/nadlan_project/{post_id}", timeout=60
    )
    if direct.status_code != 404:
        raise RuntimeError("Anonymous exact Einstein REST ID is enumerable")

    slug_response = session.get(
        f"{base_url}/wp-json/wp/v2/nadlan_project",
        params={"slug": EINSTEIN_STAGE_SLUG},
        timeout=60,
    )
    slug_payload: Any = None
    try:
        slug_payload = slug_response.json()
    except ValueError:
        pass
    if not (
        (slug_response.status_code == 200 and slug_payload == [])
        or slug_response.status_code == 404
    ):
        raise RuntimeError("Anonymous Einstein REST slug is enumerable")

    search_response = session.get(
        f"{base_url}/wp-json/wp/v2/search",
        params={"search": "EINSTEIN TOWER", "subtype": "nadlan_project", "per_page": 100},
        timeout=60,
    )
    try:
        search_payload = search_response.json()
    except ValueError:
        search_payload = None
    if search_response.status_code != 200 or not isinstance(search_payload, list):
        raise RuntimeError("Anonymous WordPress search probe was unavailable")
    if any(
        isinstance(row, dict)
        and (
            int(row.get("id") or 0) == post_id
            or EINSTEIN_STAGE_SLUG in str(row.get("url") or "")
        )
        for row in search_payload
    ):
        raise RuntimeError("Anonymous WordPress search reveals the Einstein private stage")

    oembed = session.get(
        f"{base_url}/wp-json/oembed/1.0/embed", params={"url": page_url}, timeout=60
    )
    embed = session.get(page_url.rstrip("/") + "/embed/", timeout=60, allow_redirects=False)
    feed = session.get(page_url.rstrip("/") + "/feed/", timeout=60, allow_redirects=False)
    if oembed.status_code != 404 or embed.status_code != 404 or feed.status_code != 404:
        raise RuntimeError("Anonymous oEmbed, embed, or feed surface reveals stage existence")

    sitemap = session.get(
        f"{base_url}/wp-sitemap-posts-nadlan_project-1.xml",
        params={"cb": secrets.token_hex(6)},
        timeout=60,
    )
    if sitemap.status_code == 200 and (
        EINSTEIN_STAGE_SLUG in sitemap.text or f">{post_id}<" in sitemap.text
    ):
        raise RuntimeError("Einstein private stage appears in the public project sitemap")

    meta = request_payload["body"]["meta"]
    asset_urls = {
        str(meta["project_model_glb"]),
        str(meta["project_model_lod_glb"]),
        str(meta["project_model_poster"]),
    }
    experiences = json.loads(str(meta["project_experience_registry_json"]))
    for scene in experiences.get("scenes", []):
        if isinstance(scene, dict):
            for key in ("preview_url", "fullscreen_url"):
                if scene.get(key):
                    asset_urls.add(str(scene[key]))
    asset_probes: list[dict[str, Any]] = []
    for asset_url in sorted(asset_urls):
        parsed = urlparse(asset_url)
        if parsed.scheme != "https" or parsed.hostname != "nad-lan.co.il":
            raise RuntimeError("Einstein private asset URL escaped the exact site origin")
        response = session.get(asset_url, timeout=60, allow_redirects=False)
        asset_cache = response.headers.get("Cache-Control", "").lower()
        asset_robots = response.headers.get("X-Robots-Tag", "").lower()
        if (
            response.status_code != 404
            or len(response.content) > 64 * 1024
            or "no-store" not in asset_cache
            or "noindex" not in asset_robots
        ):
            raise RuntimeError("Anonymous Einstein private asset route returned usable bytes")
        asset_probes.append(
            {
                "path": parsed.path,
                "http_status": response.status_code,
                "response_bytes": len(response.content),
            }
        )
    return {
        "page": {
            "http_status": page.status_code,
            "password_form": password_form,
            "body_hidden": True,
            "password_not_reflected": True,
            "x_robots_tag": page.headers.get("X-Robots-Tag", ""),
            "cache_control": page.headers.get("Cache-Control", ""),
            "discovery_links_absent": True,
        },
        "rest_id_status": direct.status_code,
        "rest_slug_hidden": True,
        "search_hidden": True,
        "oembed_status": oembed.status_code,
        "embed_status": embed.status_code,
        "feed_status": feed.status_code,
        "sitemap_status": sitemap.status_code,
        "sitemap_hidden": EINSTEIN_STAGE_SLUG not in sitemap.text,
        "private_assets": asset_probes,
    }


def assert_tree_has_no_secret_bytes(root: Path, secret_values: Iterable[str]) -> dict[str, Any]:
    secrets_bytes = [value.encode("utf-8") for value in secret_values if value]
    checked_files = 0
    checked_bytes = 0
    if not root.is_dir():
        raise RuntimeError("Browser acceptance evidence directory is missing")
    for candidate in root.rglob("*"):
        if not candidate.is_file() or candidate.is_symlink():
            continue
        checked_files += 1
        with candidate.open("rb") as stream:
            overlap = b""
            while True:
                chunk = stream.read(1024 * 1024)
                if not chunk:
                    break
                checked_bytes += len(chunk)
                probe = overlap + chunk
                if any(secret_value in probe for secret_value in secrets_bytes):
                    try:
                        candidate.unlink()
                    except OSError:
                        pass
                    raise RuntimeError("Browser evidence contained a secret and was removed")
                overlap = probe[-256:]
    return {
        "files_checked": checked_files,
        "bytes_checked": checked_bytes,
        "secret_bytes_absent": True,
    }


def acceptance_summary_proof(
    payload: dict[str, Any], *, einstein_mode: bool
) -> dict[str, Any]:
    """Validate the exact runner schema; preserve the legacy summary contract."""
    if not einstein_mode:
        hard_failures = payload.get("hardFailures")
        warnings = payload.get("warnings")
        if isinstance(hard_failures, list) and hard_failures:
            raise RuntimeError("Legacy browser acceptance reported hard failures")
        return {
            "schema": str(payload.get("schema") or "legacy"),
            "passed": True,
            "hard_failure_count": len(hard_failures)
            if isinstance(hard_failures, list)
            else None,
            "warning_count": len(warnings) if isinstance(warnings, list) else None,
        }

    totals = payload.get("totals") if isinstance(payload.get("totals"), dict) else {}
    failures = payload.get("failures")
    warnings = payload.get("warnings")
    matrix = payload.get("matrix")
    assets = payload.get("assets")
    privacy_gates = ("anonymous", "discovery", "health", "unlocked")
    behavior_gates = ("browserBack", "keyboard", "browserHistory", "textResize200")
    gates = privacy_gates + behavior_gates
    evidence_counts = (
        payload.get("evidenceCounts")
        if isinstance(payload.get("evidenceCounts"), dict)
        else {}
    )
    evidence_expected = evidence_counts.get("expected")
    evidence_observed = evidence_counts.get("observed")
    keyboard = payload.get("keyboard")
    keyboard_viewports = (
        keyboard.get("viewports") if isinstance(keyboard, dict) else None
    )
    keyboard_rows_exact = isinstance(keyboard_viewports, list) and all(
        isinstance(row, dict) and isinstance(row.get("tools"), list)
        for row in keyboard_viewports
    )
    keyboard_viewport_names = (
        [str(row.get("viewport") or "") for row in keyboard_viewports]
        if keyboard_rows_exact
        else []
    )
    keyboard_tools = (
        [
            tool
            for row in keyboard_viewports
            for tool in row.get("tools", [])
            if isinstance(tool, dict)
        ]
        if keyboard_rows_exact
        else []
    )
    browser_history = payload.get("browserHistory")
    history_transitions = (
        browser_history.get("transitions")
        if isinstance(browser_history, dict)
        else None
    )
    text_resize = payload.get("textResize200")
    text_resize_viewports = (
        text_resize.get("viewports") if isinstance(text_resize, dict) else None
    )
    text_resize_rows_exact = isinstance(text_resize_viewports, list) and all(
        isinstance(row, dict) and isinstance(row.get("dialogs"), list)
        for row in text_resize_viewports
    )
    text_resize_viewport_names = (
        [str(row.get("viewport") or "") for row in text_resize_viewports]
        if text_resize_rows_exact
        else []
    )
    text_resize_dialogs = (
        [
            dialog
            for row in text_resize_viewports
            for dialog in row.get("dialogs", [])
            if isinstance(dialog, dict)
        ]
        if text_resize_rows_exact
        else []
    )
    matrix_names = (
        [str(row.get("viewport") or "") for row in matrix if isinstance(row, dict)]
        if isinstance(matrix, list)
        else []
    )
    asset_names = (
        [str(row.get("name") or "") for row in assets if isinstance(row, dict)]
        if isinstance(assets, list)
        else []
    )

    def exact_integer(value: Any, expected: int) -> bool:
        return (
            isinstance(value, int)
            and not isinstance(value, bool)
            and value == expected
        )

    def exact_evidence_map(value: Any) -> bool:
        return (
            isinstance(value, dict)
            and set(value) == set(EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS)
            and all(
                exact_integer(value[key], expected)
                for key, expected in EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS.items()
            )
        )

    exact = (
        payload.get("schema") == EINSTEIN_ACCEPTANCE_SCHEMA
        and totals.get("passed") is True
        and exact_integer(totals.get("failures"), 0)
        and exact_integer(
            totals.get("viewports"), len(EINSTEIN_ACCEPTANCE_VIEWPORTS)
        )
        and exact_integer(
            totals.get("assetsObserved"), len(EINSTEIN_ACCEPTANCE_ASSETS)
        )
        and exact_integer(
            totals.get("keyboardToolChecks"),
            EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS["keyboardToolChecks"],
        )
        and exact_integer(
            totals.get("textResizeDialogChecks"),
            EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS["textResizeDialogChecks"],
        )
        and exact_integer(
            totals.get("historyTransitions"),
            EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS["browserHistoryTransitions"],
        )
        and isinstance(failures, list)
        and len(failures) == 0
        and isinstance(matrix, list)
        and len(matrix) == len(EINSTEIN_ACCEPTANCE_VIEWPORTS)
        and tuple(matrix_names) == EINSTEIN_ACCEPTANCE_VIEWPORTS
        and all(isinstance(row, dict) and row.get("passed") is True for row in matrix)
        and isinstance(assets, list)
        and len(assets) == len(EINSTEIN_ACCEPTANCE_ASSETS)
        and tuple(sorted(asset_names)) == tuple(sorted(EINSTEIN_ACCEPTANCE_ASSETS))
        and all(
            isinstance(payload.get(gate), dict) and payload[gate].get("passed") is True
            for gate in gates
        )
        and evidence_counts.get("matched") is True
        and exact_evidence_map(evidence_expected)
        and exact_evidence_map(evidence_observed)
        and evidence_expected == evidence_observed
        and keyboard_rows_exact
        and len(keyboard_viewports)
        == EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS["keyboardViewports"]
        and tuple(keyboard_viewport_names)
        == EINSTEIN_ACCEPTANCE_ACCESSIBILITY_VIEWPORTS
        and all(
            row.get("passed") is True
            and isinstance(row.get("tools"), list)
            and len(row["tools"]) == 4
            for row in keyboard_viewports
        )
        and len(keyboard_tools)
        == EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS["keyboardToolChecks"]
        and all(
            tool.get("passed") is True and tool.get("escapeClosed") is True
            for tool in keyboard_tools
        )
        and sum(tool.get("escapeClosed") is True for tool in keyboard_tools)
        == EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS["keyboardEscapeRestores"]
        and isinstance(history_transitions, list)
        and len(history_transitions)
        == EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS["browserHistoryTransitions"]
        and [
            str(transition.get("direction") or "")
            for transition in history_transitions
            if isinstance(transition, dict)
        ]
        == ["back", "forward"]
        and all(
            isinstance(transition, dict) and transition.get("passed") is True
            for transition in history_transitions
        )
        and text_resize_rows_exact
        and len(text_resize_viewports)
        == EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS["textResizeViewports"]
        and tuple(text_resize_viewport_names)
        == EINSTEIN_ACCEPTANCE_ACCESSIBILITY_VIEWPORTS
        and all(
            row.get("passed") is True
            and isinstance(row.get("dialogs"), list)
            and len(row["dialogs"]) == 4
            for row in text_resize_viewports
        )
        and len(text_resize_dialogs)
        == EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS["textResizeDialogChecks"]
        and all(dialog.get("passed") is True for dialog in text_resize_dialogs)
    )
    if not exact:
        raise RuntimeError("Einstein browser acceptance report contract failed")
    return {
        "schema": EINSTEIN_ACCEPTANCE_SCHEMA,
        "passed": True,
        "failure_count": 0,
        "warning_count": len(warnings) if isinstance(warnings, list) else None,
        "matrix_count": len(matrix),
        "matrix_passed": len(matrix),
        "asset_count": len(assets),
        "asset_expected": len(EINSTEIN_ACCEPTANCE_ASSETS),
        "gates_passed": list(gates),
        "evidence_expected": copy.deepcopy(evidence_expected),
        "evidence_observed": copy.deepcopy(evidence_observed),
        "keyboard_tool_checks": len(keyboard_tools),
        "keyboard_escape_restores": sum(
            tool.get("escapeClosed") is True for tool in keyboard_tools
        ),
        "history_transitions": len(history_transitions),
        "text_resize_dialog_checks": len(text_resize_dialogs),
    }


def utc_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
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


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class Redactor:
    def __init__(self, secrets_to_hide: Iterable[str]):
        self._secrets = sorted(
            {value for value in secrets_to_hide if isinstance(value, str) and value},
            key=len,
            reverse=True,
        )

    def text(self, value: Any) -> str:
        output = str(value)
        for secret in self._secrets:
            output = output.replace(secret, "[REDACTED]")
        return output

    def value(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {str(key): self.value(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [self.value(item) for item in value]
        if isinstance(value, str):
            return self.text(value)
        return value

    def assert_absent(self, serialized: str) -> None:
        leaked = [secret for secret in self._secrets if secret in serialized]
        if leaked:
            raise RuntimeError("Credential redaction assertion failed")


class WordpressClient:
    def __init__(self, base_url: str, user: str, application_password: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = (user, application_password)
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "NadLan-Private-Unit-Journey-Release/1.0",
            }
        )

    @staticmethod
    def _is_host_html_403(response: requests.Response) -> bool:
        content_type = response.headers.get("Content-Type", "").lower()
        prefix = response.text[:300].lower()
        return (
            response.status_code == 403
            and "json" not in content_type
            and ("<html" in prefix or "<!doctype" in prefix)
        )

    def request(
        self,
        method: str,
        route: str,
        *,
        json_body: dict[str, Any] | None = None,
        timeout: int = 60,
    ) -> requests.Response:
        normalized = route.lstrip("/")
        response = self.session.request(
            method,
            f"{self.base_url}/wp-json/{normalized}",
            json=json_body,
            timeout=timeout,
        )
        if self._is_host_html_403(response):
            response = self.session.request(
                method,
                f"{self.base_url}/?rest_route=/{normalized}",
                json=json_body,
                timeout=timeout,
            )
        return response

    def all_snippets(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        page = 1
        total_pages = 1
        while page <= total_pages:
            response = self.session.get(
                f"{self.base_url}/wp-json/code-snippets/v1/snippets",
                params={"per_page": 100, "page": page},
                timeout=60,
            )
            if self._is_host_html_403(response):
                response = self.session.get(
                    f"{self.base_url}/",
                    params={
                        "rest_route": "/code-snippets/v1/snippets",
                        "per_page": 100,
                        "page": page,
                    },
                    timeout=60,
                )
            response.raise_for_status()
            total_pages = int(response.headers.get("X-WP-TotalPages", "1"))
            payload = response.json()
            if not isinstance(payload, list):
                raise RuntimeError("Code Snippets collection is not a list")
            rows.extend(payload)
            page += 1
        return rows


def response_payload(response: requests.Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError:
        return {"http_status": response.status_code, "code": "non_json_response"}
    if not isinstance(payload, dict):
        return {"http_status": response.status_code, "code": "unexpected_json_shape"}
    payload = dict(payload)
    payload["http_status"] = response.status_code
    return payload


def is_exact_missing_snippet_response(response: requests.Response) -> bool:
    """Recognize only the two observed Code Snippets item-missing responses."""
    if response.status_code == 404:
        return True
    if response.status_code != 500:
        return False
    try:
        payload = response.json()
    except ValueError:
        return False
    if not isinstance(payload, dict):
        return False
    if (
        payload.get("code") != MISSING_SNIPPET_CODE
        or payload.get("message") != MISSING_SNIPPET_MESSAGE
    ):
        return False
    keys = set(payload)
    return keys == {"code", "message"} or (
        keys == {"code", "message", "data"}
        and payload.get("data") == {"status": 500}
    )


def snippet_absent_from_collection(
    rows: list[dict[str, Any]], *, snippet_id: int, snippet_name: str
) -> bool:
    return all(
        int(row.get("id") or 0) != snippet_id
        and str(row.get("name") or "") != snippet_name
        for row in rows
    )


def snippet_absence_is_proved(
    response: requests.Response,
    rows: list[dict[str, Any]],
    *,
    snippet_id: int,
    snippet_name: str,
    route_status: int,
) -> bool:
    """Require item-missing, collection absence, and a dead helper route together."""
    return (
        is_exact_missing_snippet_response(response)
        and snippet_absent_from_collection(
            rows, snippet_id=snippet_id, snippet_name=snippet_name
        )
        and route_status == 404
    )


def deploy_failure_proof(
    response: requests.Response, payload: dict[str, Any]
) -> dict[str, Any]:
    """Return only allowlisted deployment diagnostics from a helper error."""
    data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
    code = str(payload.get("code") or "")
    stage = str(data.get("failure_stage") or "")
    reason = str(data.get("failure_reason_code") or "")
    rollback_outcome = str(data.get("rollback_outcome") or "")
    rollback_semantics_valid = (
        (stage in DEPLOY_FAILURE_PREBACKUP_STAGES and rollback_outcome == "not_required")
        or (
            stage == "backup_commit"
            and rollback_outcome in {"not_required", "succeeded", "failed"}
        )
        or (
            stage in DEPLOY_FAILURE_REQUIRES_ROLLBACK_STAGES
            and rollback_outcome in {"succeeded", "failed"}
        )
    )
    catch_contract_valid = code != "nadlan_release_deploy_failed" or (
        isinstance(data.get("rolled_back"), bool)
        and isinstance(data.get("upload_temp_absent"), bool)
        and rollback_outcome in {"not_required", "succeeded", "failed"}
        and (data.get("rolled_back") is True) == (rollback_outcome == "succeeded")
        and rollback_semantics_valid
    )
    contract_valid = (
        code in DEPLOY_FAILURE_CODES
        and stage in DEPLOY_FAILURE_CODE_STAGES[code]
        and stage in DEPLOY_FAILURE_CONTRACT
        and reason in DEPLOY_FAILURE_CONTRACT[stage]
        and catch_contract_valid
    )
    return {
        "http_status": int(response.status_code),
        "code": code if code in DEPLOY_FAILURE_CODES else "unexpected_error",
        "failure_stage": stage if contract_valid else "invalid_contract",
        "failure_reason_code": reason if contract_valid else "invalid_contract",
        "contract_valid": contract_valid,
        "rolled_back": data.get("rolled_back") is True,
        "rollback_outcome": (
            rollback_outcome
            if contract_valid and code == "nadlan_release_deploy_failed"
            else "not_reported"
        ),
        "upload_temp_absent": data.get("upload_temp_absent") is True,
    }


def deploy_preflight_proof(
    payload: dict[str, Any],
    *,
    before_version: str,
    artifact_bytes: int,
    artifact_uncompressed_bytes: int,
) -> dict[str, Any]:
    """Validate and minimize the helper's read-only pre-deployment proof."""
    target = payload.get("target") if isinstance(payload.get("target"), dict) else {}
    disk = payload.get("disk") if isinstance(payload.get("disk"), dict) else {}
    upgrade = payload.get("upgrade") if isinstance(payload.get("upgrade"), dict) else {}
    filesystem = (
        payload.get("filesystem")
        if isinstance(payload.get("filesystem"), dict)
        else {}
    )

    def count(value: Any) -> int | None:
        return value if isinstance(value, int) and not isinstance(value, bool) else None

    target_files = count(target.get("file_count"))
    target_bytes = count(target.get("bytes"))
    free_bytes = count(disk.get("free_bytes"))
    required_bytes = count(disk.get("required_bytes"))
    expected_required = (
        target_bytes + artifact_uncompressed_bytes + artifact_bytes + 20 * 1024 * 1024
        if target_bytes is not None
        else None
    )
    structural = (
        payload.get("schema") == DEPLOY_PREFLIGHT_SCHEMA
        and target.get("readable") is True
        and target.get("active") is True
        and str(target.get("version") or "") == before_version
        and target_files is not None
        and target_files > 0
        and target_bytes is not None
        and target_bytes > 0
        and disk.get("measurable") is True
        and free_bytes is not None
        and required_bytes is not None
        and required_bytes == expected_required
        and disk.get("sufficient") is True
        and free_bytes >= required_bytes
        and upgrade.get("root_safe") is True
        and upgrade.get("root_writable") is True
        and upgrade.get("backup_path_absent") is True
        and filesystem.get("available") is True
        and payload.get("passed") is True
    )
    return {
        "schema": DEPLOY_PREFLIGHT_SCHEMA,
        "passed": structural,
        "target": {
            "readable": target.get("readable") is True,
            "active": target.get("active") is True,
            "version": str(target.get("version") or ""),
            "file_count": target_files or 0,
            "bytes": target_bytes or 0,
        },
        "disk": {
            "measurable": disk.get("measurable") is True,
            "free_bytes": free_bytes or 0,
            "required_bytes": required_bytes or 0,
            "sufficient": disk.get("sufficient") is True,
        },
        "upgrade": {
            "root_safe": upgrade.get("root_safe") is True,
            "root_writable": upgrade.get("root_writable") is True,
            "backup_path_absent": upgrade.get("backup_path_absent") is True,
        },
        "filesystem": {"available": filesystem.get("available") is True},
    }


def require_response(response: requests.Response, operation: str) -> dict[str, Any]:
    payload = response_payload(response)
    if response.status_code < 200 or response.status_code >= 300:
        code = str(payload.get("code") or "unknown_error")
        rolled_back = payload.get("data", {}).get("rolled_back") if isinstance(payload.get("data"), dict) else None
        suffix = (
            f"; rolled_back={rolled_back}"
            if isinstance(rolled_back, bool)
            else ""
        )
        raise RuntimeError(f"{operation} returned HTTP {response.status_code} ({code}){suffix}")
    return payload


def validate_immutable_url(url: str) -> str:
    parsed = urlparse(url)
    if (
        parsed.scheme.lower() != "https"
        or parsed.hostname is None
        or parsed.hostname.lower() != "raw.githubusercontent.com"
        or parsed.username
        or parsed.password
        or parsed.port not in (None, 443)
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Artifact URL must be an unadorned HTTPS raw.githubusercontent.com URL")
    match = re.fullmatch(
        r"/The-new-ben/nad-lan-co-il/([a-f0-9]{40})/plugin-dist/(nadlan-config-[A-Za-z0-9._-]+\.zip)",
        parsed.path,
    )
    if not match:
        raise ValueError("Artifact URL must contain an exact 40-hex commit and nadlan-config ZIP path")
    return match.group(1)


def validate_site_url(url: str) -> str:
    parsed = urlparse(url)
    if (
        parsed.scheme.lower() != "https"
        or (parsed.hostname or "").lower() != "nad-lan.co.il"
        or parsed.username
        or parsed.password
        or parsed.port not in (None, 443)
        or parsed.query
        or parsed.fragment
        or parsed.path not in ("", "/")
    ):
        raise ValueError("WP_BASE_URL must be exactly the credential-free HTTPS nad-lan.co.il origin")
    return "https://nad-lan.co.il"


def _validate_zip_name(name: str) -> tuple[PurePosixPath, bool]:
    if not name or "\x00" in name or "\\" in name or name.startswith("/") or ":" in name:
        raise ValueError(f"Unsafe ZIP path: {name!r}")
    is_dir = name.endswith("/")
    trimmed = name.rstrip("/")
    if not trimmed:
        raise ValueError("ZIP contains an empty root entry")
    parts = trimmed.split("/")
    if parts[0] != PLUGIN_ROOT or any(part in ("", ".", "..") for part in parts):
        raise ValueError(f"ZIP entry is outside exact {PLUGIN_ROOT}/ root")
    return PurePosixPath(trimmed), is_dir


def validate_zip(path: Path) -> dict[str, Any]:
    archive_bytes = path.stat().st_size
    if archive_bytes < 1 or archive_bytes > MAX_ARCHIVE_BYTES:
        raise ValueError("Artifact archive size is outside the release limit")
    total_expanded = 0
    has_main = False
    seen_names: set[str] = set()
    with zipfile.ZipFile(path, "r") as archive:
        entries = archive.infolist()
        if not entries or len(entries) > MAX_ENTRIES:
            raise ValueError("Artifact ZIP entry count is outside the release limit")
        for info in entries:
            normalized, is_dir = _validate_zip_name(info.filename)
            normalized_name = normalized.as_posix()
            if normalized_name in seen_names:
                raise ValueError("Artifact ZIP contains a duplicate path")
            seen_names.add(normalized_name)
            if normalized_name == PLUGIN_ROOT and not is_dir:
                raise ValueError("Artifact ZIP root entry is not a directory")
            mode = (info.external_attr >> 16) & 0o170000
            if mode == 0o120000:
                raise ValueError("Artifact ZIP contains a symbolic link")
            if info.file_size < 0 or info.file_size > MAX_ENTRY_BYTES:
                raise ValueError("Artifact ZIP entry size is outside the release limit")
            total_expanded += info.file_size
            if total_expanded > MAX_EXPANDED_BYTES:
                raise ValueError("Artifact expanded size exceeds the release limit")
            if not is_dir:
                with archive.open(info, "r") as stream:
                    while stream.read(1024 * 1024):
                        pass
            if normalized.as_posix() == PLUGIN_FILE:
                has_main = True
        bad_crc = archive.testzip()
        if bad_crc is not None:
            raise ValueError(f"Artifact ZIP CRC failed for {bad_crc!r}")
    if not has_main:
        raise ValueError(f"Artifact ZIP is missing exact {PLUGIN_FILE}")
    return {
        "archive_bytes": archive_bytes,
        "entry_count": len(entries),
        "uncompressed_bytes": total_expanded,
        "root": f"{PLUGIN_ROOT}/",
        "crc_valid": True,
    }


def download_and_validate_artifact(url: str, expected_sha256: str, destination: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    total = 0
    with requests.get(url, stream=True, timeout=(20, 120), allow_redirects=True) as response:
        response.raise_for_status()
        with destination.open("wb") as output:
            for chunk in response.iter_content(1024 * 1024):
                if not chunk:
                    continue
                total += len(chunk)
                if total > MAX_ARCHIVE_BYTES:
                    raise ValueError("Artifact download exceeds the release archive limit")
                digest.update(chunk)
                output.write(chunk)
    observed = digest.hexdigest()
    if not secrets.compare_digest(expected_sha256, observed):
        raise ValueError("Downloaded artifact SHA-256 does not match --artifact-sha256")
    proof = validate_zip(destination)
    proof["sha256"] = observed
    return proof


def validate_canonical_artifact_path(
    candidate: Path, expected_version: str, expected_sha256: str
) -> tuple[Path, dict[str, Any]]:
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+){1,3}(?:[-.][A-Za-z0-9]+)*", expected_version):
        raise ValueError("Expected version is not a safe canonical artifact version")
    expected = REPO_ROOT / "plugin-dist" / f"nadlan-config-{expected_version}.zip"
    try:
        candidate_absolute = candidate.expanduser().absolute()
        expected_absolute = expected.absolute()
        if (
            os.path.normcase(str(candidate_absolute)) != os.path.normcase(str(expected_absolute))
            or candidate_absolute.is_symlink()
            or not candidate_absolute.is_file()
        ):
            raise ValueError
        resolved = candidate_absolute.resolve(strict=True)
        if os.path.normcase(str(resolved)) != os.path.normcase(str(expected_absolute.resolve(strict=True))):
            raise ValueError
    except (OSError, RuntimeError, ValueError) as error:
        raise ValueError("--artifact-path must be the exact canonical plugin-dist ZIP") from error

    digest = hashlib.sha256()
    total = 0
    try:
        with resolved.open("rb") as stream:
            while True:
                chunk = stream.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_ARCHIVE_BYTES:
                    raise ValueError("Local artifact exceeds the release archive limit")
                digest.update(chunk)
    except OSError as error:
        raise ValueError("Canonical local artifact could not be read") from error
    observed = digest.hexdigest()
    if not secrets.compare_digest(expected_sha256, observed):
        raise ValueError("Local artifact SHA-256 does not match --artifact-sha256")
    try:
        proof = validate_zip(resolved)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        raise ValueError("Canonical local artifact ZIP validation failed") from error
    proof["sha256"] = observed
    return resolved, proof


def render_helper(
    *,
    route_path: str,
    token: str,
    run_id: str,
    helper_id: int,
    helper_name: str,
    artifact_mode: str,
    artifact_url: str,
    artifact_sha256: str,
    artifact_bytes: int,
    artifact_entry_count: int,
    artifact_uncompressed_bytes: int,
    expected_version: str,
) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "__ROUTE_PATH__": json.dumps(route_path),
        "__TOKEN__": json.dumps(token),
        "__RUN_ID__": json.dumps(run_id),
        "__HELPER_ID__": str(helper_id),
        "__HELPER_NAME__": json.dumps(helper_name),
        "__ARTIFACT_MODE__": json.dumps(artifact_mode),
        "__ARTIFACT_URL__": json.dumps(artifact_url),
        "__ARTIFACT_SHA256__": json.dumps(artifact_sha256),
        "__ARTIFACT_BYTES__": str(int(artifact_bytes)),
        "__ARTIFACT_ENTRY_COUNT__": str(int(artifact_entry_count)),
        "__ARTIFACT_UNCOMPRESSED_BYTES__": str(int(artifact_uncompressed_bytes)),
        "__EXPECTED_VERSION__": json.dumps(expected_version),
        "__SOURCE_POST_ID__": str(SOURCE_POST_ID),
        "__PAGE_SLUG__": json.dumps(PAGE_SLUG),
        "__PAGE_TITLE__": json.dumps(PAGE_TITLE, ensure_ascii=False),
        "__PROJECT_DISPLAY_NAME__": json.dumps(PROJECT_DISPLAY_NAME, ensure_ascii=False),
    }
    for marker, value in replacements.items():
        if marker not in template:
            raise RuntimeError(f"Helper template is missing marker {marker}")
        template = template.replace(marker, value)
    unresolved = sorted(set(MARKER_RE.findall(template)))
    if unresolved:
        raise RuntimeError(f"Helper template contains unresolved markers: {', '.join(unresolved)}")
    return template.strip()


def render_cleanup_helper(
    *,
    route_path: str,
    token: str,
    helper_id: int,
    helper_name: str,
    target_id: int,
    target_name: str,
    target_hash: str,
    release_run_id: str,
    release_token: str,
    artifact_mode: str,
    artifact_sha256: str,
    artifact_bytes: int,
    artifact_entry_count: int,
    artifact_uncompressed_bytes: int,
    manage_release_resources: bool,
) -> str:
    replacements = {
        "__ROUTE_PATH__": json.dumps(route_path),
        "__TOKEN__": json.dumps(token),
        "__HELPER_ID__": str(helper_id),
        "__HELPER_NAME__": json.dumps(helper_name),
        "__TARGET_ID__": str(target_id),
        "__TARGET_NAME__": json.dumps(target_name),
        "__TARGET_HASH__": json.dumps(target_hash),
        "__RELEASE_RUN_ID__": json.dumps(release_run_id),
        "__RELEASE_TOKEN__": json.dumps(release_token),
        "__ARTIFACT_MODE__": json.dumps(artifact_mode),
        "__ARTIFACT_SHA256__": json.dumps(artifact_sha256),
        "__ARTIFACT_BYTES__": str(int(artifact_bytes)),
        "__ARTIFACT_ENTRY_COUNT__": str(int(artifact_entry_count)),
        "__ARTIFACT_UNCOMPRESSED_BYTES__": str(int(artifact_uncompressed_bytes)),
        "__MANAGE_RELEASE_RESOURCES__": "true" if manage_release_resources else "false",
    }
    code = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-private-release/v1', __ROUTE_PATH__, array(
		'methods'             => 'POST',
		'permission_callback' => function () {
			return current_user_can( 'update_plugins' );
		},
		'callback'            => function ( WP_REST_Request $request ) {
			if ( ! hash_equals( __TOKEN__, (string) $request->get_param( 'token' ) ) ) {
				return new WP_Error( 'cleanup_token_invalid', 'Cleanup token is invalid.', array( 'status' => 403 ) );
			}
			$helper_hash = strtolower( (string) $request->get_param( 'helper_sha256' ) );
			if ( 1 !== preg_match( '/^[a-f0-9]{64}$/', $helper_hash ) ) {
				return new WP_Error( 'cleanup_hash_invalid', 'Cleanup helper hash is invalid.', array( 'status' => 400 ) );
			}
			if ( ! function_exists( 'Code_Snippets\\get_snippet' ) || ! function_exists( 'Code_Snippets\\delete_snippet' ) ) {
				return new WP_Error( 'cleanup_api_missing', 'Code Snippets API is unavailable.', array( 'status' => 500 ) );
			}
			$self = \Code_Snippets\get_snippet( __HELPER_ID__, false );
			$self_valid =
				$self
				&& __HELPER_ID__ === (int) $self->id
				&& __HELPER_NAME__ === (string) $self->name
				&& 'global' === (string) $self->scope
				&& true === (bool) $self->active
				&& false === (bool) $self->network
				&& hash_equals( $helper_hash, hash( 'sha256', (string) $self->code ) )
				&& false !== strpos( (string) $self->code, __ROUTE_PATH__ );
			if ( ! $self_valid ) {
				return new WP_Error( 'cleanup_helper_changed', 'Cleanup helper identity changed.', array( 'status' => 409 ) );
			}

			$action = sanitize_key( (string) $request->get_param( 'action' ) );
			if ( 'discard' === $action ) {
				$self_deleted = \Code_Snippets\delete_snippet( __HELPER_ID__, false );
				$self_after   = \Code_Snippets\get_snippet( __HELPER_ID__, false );
				if ( ! $self_deleted || ( $self_after && 0 !== (int) $self_after->id ) ) {
					return new WP_Error( 'cleanup_self_delete_failed', 'Cleanup helper hard-delete failed.', array( 'status' => 500 ) );
				}
				return array( 'helper_deleted' => true, 'recovery_retained' => true );
			}
			if ( ! in_array( $action, array( 'prepare', 'delete' ), true ) ) {
				return new WP_Error( 'cleanup_action_invalid', 'Cleanup action is invalid.', array( 'status' => 400 ) );
			}

			$target = \Code_Snippets\get_snippet( __TARGET_ID__, false );
			$target_exists = $target && 0 < (int) $target->id;
			if ( $target_exists ) {
				$target_valid =
					__TARGET_ID__ === (int) $target->id
					&& __TARGET_NAME__ === (string) $target->name
					&& 'global' === (string) $target->scope
					&& false === (bool) $target->network
					&& hash_equals( __TARGET_HASH__, hash( 'sha256', (string) $target->code ) );
				if ( ! $target_valid ) {
					return new WP_Error( 'cleanup_target_changed', 'Cleanup target identity changed.', array( 'status' => 409 ) );
				}
			}

			$manage_release_resources = __MANAGE_RELEASE_RESOURCES__;
			$release_run_id           = __RELEASE_RUN_ID__;
			$release_token            = __RELEASE_TOKEN__;
			$artifact_mode            = __ARTIFACT_MODE__;
			$artifact_sha256          = __ARTIFACT_SHA256__;
			$artifact_bytes           = __ARTIFACT_BYTES__;
			$artifact_entry_count     = __ARTIFACT_ENTRY_COUNT__;
			$artifact_uncompressed    = __ARTIFACT_UNCOMPRESSED_BYTES__;
			$chunk_bytes              = 128 * 1024;
			$total_chunks             = (int) ceil( $artifact_bytes / $chunk_bytes );
			$upgrade_root             = wp_normalize_path( WP_CONTENT_DIR . '/upgrade' );
			$upload_root              = $upgrade_root . '/.nadlan-unit-journey-upload-' . substr( hash( 'sha256', $release_run_id . '|' . $release_token ), 0, 24 );
			$upload_path              = $upload_root . '/nadlan-config.zip';
			$state_key                = 'nadlan_unit_journey_state_' . substr( hash( 'sha256', $release_run_id ), 0, 16 );
			$lock_key                 = 'nadlan_unit_journey_deploy_lock';

			$upload_status = function () use ( $upgrade_root, $upload_root, $upload_path ) {
				clearstatcache( true, $upload_path );
				$root_exists = file_exists( $upload_root );
				$file_exists = file_exists( $upload_path );
				$root_real   = $root_exists ? @realpath( $upload_root ) : false;
				$file_real   = $file_exists ? @realpath( $upload_path ) : false;
				$safe        =
					0 === strpos( $upload_root, $upgrade_root . '/' )
					&& ! is_link( $upgrade_root )
					&& ! is_link( $upload_root )
					&& ! is_link( $upload_path )
					&& ( ! $root_exists || ( is_dir( $upload_root ) && false !== $root_real ) )
					&& (
						! $file_exists
						|| (
							false !== $root_real
							&& false !== $file_real
							&& wp_normalize_path( $root_real . '/nadlan-config.zip' ) === wp_normalize_path( $file_real )
						)
					);
				return array(
					'absent' => ! $root_exists && ! $file_exists,
					'safe'   => $safe,
				);
			};

			$prove_release_contract = function () use (
				$manage_release_resources,
				$release_run_id,
				$artifact_mode,
				$artifact_sha256,
				$artifact_bytes,
				$artifact_entry_count,
				$artifact_uncompressed,
				$chunk_bytes,
				$total_chunks,
				$upload_path,
				$state_key,
				$lock_key
			) {
				if ( ! $manage_release_resources ) {
					return array( 'state_present' => false, 'lock_present' => false, 'state_digest' => '', 'lock_digest' => '' );
				}
				$state = get_option( $state_key, false );
				if ( false !== $state ) {
					$state_valid =
						'upload' === $artifact_mode
						&& is_array( $state )
						&& $release_run_id === (string) ( isset( $state['run_id'] ) ? $state['run_id'] : '' )
						&& in_array( isset( $state['phase'] ) ? $state['phase'] : '', array( 'uploading', 'upload_verified' ), true )
						&& 'upload' === (string) ( isset( $state['artifact_mode'] ) ? $state['artifact_mode'] : '' )
						&& $upload_path === wp_normalize_path( (string) ( isset( $state['upload_path'] ) ? $state['upload_path'] : '' ) )
						&& hash_equals( $artifact_sha256, (string) ( isset( $state['upload_expected_sha256'] ) ? $state['upload_expected_sha256'] : '' ) )
						&& $artifact_bytes === (int) ( isset( $state['upload_expected_bytes'] ) ? $state['upload_expected_bytes'] : 0 )
						&& $artifact_entry_count === (int) ( isset( $state['upload_expected_entries'] ) ? $state['upload_expected_entries'] : 0 )
						&& $artifact_uncompressed === (int) ( isset( $state['upload_expected_uncompressed_bytes'] ) ? $state['upload_expected_uncompressed_bytes'] : 0 )
						&& $chunk_bytes === (int) ( isset( $state['upload_chunk_bytes'] ) ? $state['upload_chunk_bytes'] : 0 )
						&& $total_chunks === (int) ( isset( $state['upload_total_chunks'] ) ? $state['upload_total_chunks'] : 0 )
						&& empty( $state['backup_digest'] )
						&& empty( $state['backup_root'] )
						&& empty( $state['page_id'] );
					if ( ! $state_valid ) {
						throw new RuntimeException( 'Release state is not a safe pre-deployment upload owned by this run.' );
					}
				}
				$lock = get_option( $lock_key, false );
				if (
					false !== $lock
					&& (
						! is_array( $lock )
						|| $release_run_id !== (string) ( isset( $lock['run_id'] ) ? $lock['run_id'] : '' )
					)
				) {
					throw new RuntimeException( 'Global deployment lock is not owned by this run.' );
				}
				return array(
					'state_present' => false !== $state,
					'lock_present'  => false !== $lock,
					'state_digest'  => false === $state ? '' : hash( 'sha256', maybe_serialize( $state ) ),
					'lock_digest'   => false === $lock ? '' : hash( 'sha256', maybe_serialize( $lock ) ),
				);
			};

			if ( 'prepare' === $action ) {
				try {
					$ownership = $prove_release_contract();
					if ( $manage_release_resources ) {
						$status = $upload_status();
						if ( ! $status['safe'] ) {
							throw new RuntimeException( 'Run-scoped upload path is unsafe.' );
						}
						if ( ! $status['absent'] ) {
							require_once ABSPATH . 'wp-admin/includes/file.php';
							if ( ! WP_Filesystem() ) {
								throw new RuntimeException( 'WordPress filesystem is unavailable.' );
							}
							global $wp_filesystem;
							if ( ! is_object( $wp_filesystem ) || ! $wp_filesystem->delete( $upload_root, true, 'd' ) ) {
								throw new RuntimeException( 'Run-scoped upload cleanup failed.' );
							}
						}
						$status = $upload_status();
						if ( ! $status['safe'] || ! $status['absent'] ) {
							throw new RuntimeException( 'Run-scoped upload absence could not be proved.' );
						}
						$current_state = get_option( $state_key, false );
						if (
							$ownership['state_present']
							&& (
								false === $current_state
								|| ! hash_equals( $ownership['state_digest'], hash( 'sha256', maybe_serialize( $current_state ) ) )
							)
						) {
							throw new RuntimeException( 'Exact release state changed before cleanup.' );
						}
						if ( ! $ownership['state_present'] && false !== $current_state ) {
							throw new RuntimeException( 'Release state appeared before cleanup.' );
						}
						if ( $ownership['state_present'] ) {
							delete_option( $state_key );
						}
						if ( false !== get_option( $state_key, false ) ) {
							throw new RuntimeException( 'Exact release state cleanup could not be proved.' );
						}
						$current_lock = get_option( $lock_key, false );
						if (
							$ownership['lock_present']
							&& (
								false === $current_lock
								|| ! hash_equals( $ownership['lock_digest'], hash( 'sha256', maybe_serialize( $current_lock ) ) )
							)
						) {
							throw new RuntimeException( 'Owned release lock changed before cleanup.' );
						}
						if ( ! $ownership['lock_present'] && false !== $current_lock ) {
							throw new RuntimeException( 'A deployment lock appeared before cleanup.' );
						}
						if ( $ownership['lock_present'] ) {
							delete_option( $lock_key );
						}
						if ( false !== get_option( $lock_key, false ) ) {
							throw new RuntimeException( 'Owned release lock cleanup could not be proved.' );
						}
					}
					return array(
						'resource_cleanup_complete' => true,
						'release_resources_managed' => $manage_release_resources,
						'upload_temp_absent'        => true,
						'state_deleted'             => true,
						'lock_released'             => true,
						'target_retained'           => true,
					);
				} catch ( Throwable $error ) {
					return new WP_Error( 'cleanup_release_unsafe', 'Release recovery state was retained because ownership or phase is unsafe.', array( 'status' => 409 ) );
				}
			}

			if ( $manage_release_resources ) {
				$status = $upload_status();
				if (
					! $status['safe']
					|| ! $status['absent']
					|| false !== get_option( $state_key, false )
					|| false !== get_option( $lock_key, false )
				) {
					return new WP_Error( 'cleanup_prepare_required', 'Release resources must be absent before helper deletion.', array( 'status' => 409 ) );
				}
			}
			$target = \Code_Snippets\get_snippet( __TARGET_ID__, false );
			$target_exists = $target && 0 < (int) $target->id;
			if ( $target_exists ) {
				$target_ready =
					__TARGET_ID__ === (int) $target->id
					&& __TARGET_NAME__ === (string) $target->name
					&& 'global' === (string) $target->scope
					&& false === (bool) $target->network
					&& hash_equals( __TARGET_HASH__, hash( 'sha256', (string) $target->code ) );
				if ( ! $target_ready ) {
					return new WP_Error( 'cleanup_target_not_ready', 'Cleanup target is not the exact verified helper.', array( 'status' => 409 ) );
				}
				$target_deleted = \Code_Snippets\delete_snippet( __TARGET_ID__, false );
				$target_after   = \Code_Snippets\get_snippet( __TARGET_ID__, false );
				if ( ! $target_deleted || ( $target_after && 0 !== (int) $target_after->id ) ) {
					return new WP_Error( 'cleanup_target_delete_failed', 'Cleanup target hard-delete failed.', array( 'status' => 500 ) );
				}
			}
			$self_deleted = \Code_Snippets\delete_snippet( __HELPER_ID__, false );
			$self_after   = \Code_Snippets\get_snippet( __HELPER_ID__, false );
			if ( ! $self_deleted || ( $self_after && 0 !== (int) $self_after->id ) ) {
				return new WP_Error( 'cleanup_self_delete_failed', 'Cleanup helper hard-delete failed.', array( 'status' => 500 ) );
			}
			return array(
				'target_deleted_or_absent' => true,
				'helper_deleted'           => true,
				'release_resources_absent' => true,
			);
		},
	) );
} );
'''.strip()
    for marker, value in replacements.items():
        code = code.replace(marker, value)
    unresolved = sorted(set(MARKER_RE.findall(code)))
    if unresolved:
        raise RuntimeError(f"Cleanup helper contains unresolved markers: {', '.join(unresolved)}")
    return code


def independently_remove_snippet(
    client: WordpressClient,
    *,
    target_id: int | None,
    target_name: str,
    expected_hash: str = "",
    release_run_id: str,
    release_token: str,
    artifact_mode: str,
    artifact_sha256: str,
    artifact_bytes: int,
    artifact_entry_count: int,
    artifact_uncompressed_bytes: int,
    manage_release_resources: bool = True,
    resources_known_absent: bool = False,
    depth: int = 0,
    created_cleanup_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Clean owned release resources, hard-delete one exact row, and prove absence."""
    if depth > 3:
        raise RuntimeError("Independent helper cleanup exceeded its bounded retry depth")
    if created_cleanup_rows is None:
        created_cleanup_rows = []

    rows = client.all_snippets()
    name_matches = [row for row in rows if str(row.get("name") or "") == target_name]
    if target_id is None:
        if len(name_matches) > 1:
            raise RuntimeError("Independent helper cleanup found duplicate target names")
        target_id = int(name_matches[0].get("id") or 0) if name_matches else None
    if target_id is None or target_id < 1:
        if manage_release_resources and not resources_known_absent:
            raise RuntimeError(
                "Managed release-resource absence cannot be proved without the helper"
            )
        return {
            "target_absent": not name_matches,
            "target_get_status": 404,
            "target_missing_response_exact": True,
            "release_resource_cleanup_proved": (
                resources_known_absent or not manage_release_resources
            ),
            "method": "already_absent",
        }

    target_response = client.request("GET", f"code-snippets/v1/snippets/{target_id}", timeout=60)
    target_already_absent = is_exact_missing_snippet_response(target_response)
    if target_already_absent:
        remaining = client.all_snippets()
        absent = snippet_absent_from_collection(
            remaining, snippet_id=target_id, snippet_name=target_name
        )
        if not absent:
            raise RuntimeError("Independent helper cleanup found collection drift")
        target_hash = expected_hash
    else:
        target = require_response(target_response, "Independent helper identity read")
        observed = observed_snippet(target)
        target_hash = observed["code_sha256"]
        if (
            observed["id"] != target_id
            or observed["name"] != target_name
            or observed["scope"] != "global"
            or (expected_hash and target_hash != expected_hash)
        ):
            raise RuntimeError("Independent helper cleanup refused changed target identity")

    # Do not trust the REST DELETE endpoint as a hard delete: on the live Code
    # Snippets version it can only move a row to trash. The authenticated bridge
    # re-proves the exact target immediately before one hard delete, avoiding an
    # inactive-main-helper gap if the second phase is interrupted.

    cleanup_suffix = f"{utc_slug()}-{secrets.token_hex(3)}"
    cleanup_name = f"tmp-unit-journey-cleanup-{cleanup_suffix}"
    cleanup_path = f"/cleanup-{cleanup_suffix}"
    cleanup_route = f"{ROUTE_NAMESPACE}{cleanup_path}"
    cleanup_token = secrets.token_hex(32)
    cleanup_id: int | None = None
    cleanup_hash = ""
    try:
        created_response = client.request(
            "POST",
            "code-snippets/v1/snippets",
            json_body={
                "name": cleanup_name,
                "code": f"/* inactive placeholder for {cleanup_name} */",
                "scope": "global",
                "active": False,
            },
            timeout=60,
        )
        created = require_response(created_response, "Independent cleanup helper creation")
        cleanup_id = int(created.get("id") or 0)
        if cleanup_id < 1:
            raise RuntimeError("Independent cleanup helper creation returned no ID")
        cleanup_code = render_cleanup_helper(
            route_path=cleanup_path,
            token=cleanup_token,
            helper_id=cleanup_id,
            helper_name=cleanup_name,
            target_id=target_id,
            target_name=target_name,
            target_hash=target_hash,
            release_run_id=release_run_id,
            release_token=release_token,
            artifact_mode=artifact_mode,
            artifact_sha256=artifact_sha256,
            artifact_bytes=artifact_bytes,
            artifact_entry_count=artifact_entry_count,
            artifact_uncompressed_bytes=artifact_uncompressed_bytes,
            manage_release_resources=manage_release_resources,
        )
        cleanup_hash = sha256_text(cleanup_code)
        created_cleanup_rows.append(
            {
                "id": cleanup_id,
                "name": cleanup_name,
                "code_sha256": cleanup_hash,
                "route": cleanup_route,
            }
        )
        update_response = client.request(
            "PUT",
            f"code-snippets/v1/snippets/{cleanup_id}",
            json_body={
                "name": cleanup_name,
                "code": cleanup_code,
                "scope": "global",
                "active": False,
            },
            timeout=60,
        )
        require_response(update_response, "Independent cleanup helper update")
        inactive_response = client.request("GET", f"code-snippets/v1/snippets/{cleanup_id}", timeout=60)
        inactive = require_response(inactive_response, "Independent cleanup helper inactive verification")
        expected_inactive = {
            "id": cleanup_id,
            "name": cleanup_name,
            "active": False,
            "scope": "global",
            "code_sha256": cleanup_hash,
        }
        if observed_snippet(inactive) != expected_inactive:
            raise RuntimeError("Independent cleanup helper inactive identity changed")

        active_observed: dict[str, Any] = {}
        for _attempt in range(2):
            client.request(
                "PUT",
                f"code-snippets/v1/snippets/{cleanup_id}/activate",
                json_body={},
                timeout=60,
            )
            active_response = client.request("GET", f"code-snippets/v1/snippets/{cleanup_id}", timeout=60)
            if active_response.status_code == 200:
                active_observed = observed_snippet(active_response.json())
                if active_observed == {**expected_inactive, "active": True}:
                    break
        if active_observed != {**expected_inactive, "active": True}:
            raise RuntimeError("Independent cleanup helper activation could not be verified")

        prepare_response = client.request(
            "POST",
            cleanup_route,
            json_body={
                "token": cleanup_token,
                "helper_sha256": cleanup_hash,
                "action": "prepare",
            },
            timeout=120,
        )
        prepare_payload = require_response(prepare_response, "Independent cleanup preparation")
        if not (
            prepare_payload.get("resource_cleanup_complete") is True
            and prepare_payload.get("upload_temp_absent") is True
            and prepare_payload.get("state_deleted") is True
            and prepare_payload.get("lock_released") is True
            and prepare_payload.get("target_retained") is True
            and prepare_payload.get("release_resources_managed")
            is manage_release_resources
        ):
            raise RuntimeError("Independent cleanup preparation proof is incomplete")

        cleanup_response = client.request(
            "POST",
            cleanup_route,
            json_body={
                "token": cleanup_token,
                "helper_sha256": cleanup_hash,
                "action": "delete",
            },
            timeout=120,
        )
        cleanup_payload = require_response(cleanup_response, "Independent cleanup deletion")
        if not (
            cleanup_payload.get("target_deleted_or_absent") is True
            and cleanup_payload.get("helper_deleted") is True
            and cleanup_payload.get("release_resources_absent") is True
        ):
            raise RuntimeError("Independent cleanup route did not confirm target deletion")
    finally:
        if cleanup_id is None:
            try:
                cleanup_matches = [
                    row
                    for row in client.all_snippets()
                    if str(row.get("name") or "") == cleanup_name
                ]
                if len(cleanup_matches) > 1:
                    raise RuntimeError("Independent cleanup helper name is no longer unique")
                if cleanup_matches:
                    cleanup_id = int(cleanup_matches[0].get("id") or 0)
                    cleanup_hash = cleanup_hash or sha256_text(
                        f"/* inactive placeholder for {cleanup_name} */"
                    )
                    created_cleanup_rows.append(
                        {
                            "id": cleanup_id,
                            "name": cleanup_name,
                            "code_sha256": cleanup_hash,
                            "route": cleanup_route,
                        }
                    )
            except Exception:
                if depth >= 3:
                    raise
        if cleanup_id is not None:
            cleanup_after = client.request("GET", f"code-snippets/v1/snippets/{cleanup_id}", timeout=60)
            if not is_exact_missing_snippet_response(cleanup_after):
                try:
                    cleanup_row = require_response(cleanup_after, "Cleanup helper residual read")
                    cleanup_observed = observed_snippet(cleanup_row)
                    if cleanup_observed["active"] is True and cleanup_hash:
                        discard_response = client.request(
                            "POST",
                            cleanup_route,
                            json_body={
                                "token": cleanup_token,
                                "helper_sha256": cleanup_hash,
                                "action": "discard",
                            },
                            timeout=120,
                        )
                        discard_payload = require_response(
                            discard_response, "Independent cleanup helper discard"
                        )
                        if discard_payload.get("helper_deleted") is not True:
                            raise RuntimeError("Cleanup helper discard proof is incomplete")
                    else:
                        independently_remove_snippet(
                            client,
                            target_id=cleanup_id,
                            target_name=cleanup_name,
                            expected_hash=cleanup_hash
                            or sha256_text(f"/* inactive placeholder for {cleanup_name} */"),
                            release_run_id=release_run_id,
                            release_token=release_token,
                            artifact_mode=artifact_mode,
                            artifact_sha256=artifact_sha256,
                            artifact_bytes=artifact_bytes,
                            artifact_entry_count=artifact_entry_count,
                            artifact_uncompressed_bytes=artifact_uncompressed_bytes,
                            manage_release_resources=False,
                            depth=depth + 1,
                            created_cleanup_rows=created_cleanup_rows,
                        )
                except Exception:
                    if depth >= 3:
                        raise

    target_after = client.request("GET", f"code-snippets/v1/snippets/{target_id}", timeout=60)
    route_after = client.request("POST", cleanup_route, json_body={}, timeout=60)
    rows_after = client.all_snippets()
    cleanup_absent = snippet_absent_from_collection(
        rows_after, snippet_id=cleanup_id or 0, snippet_name=cleanup_name
    )
    if not (
        snippet_absence_is_proved(
            target_after,
            rows_after,
            snippet_id=target_id,
            snippet_name=target_name,
            route_status=route_after.status_code,
        )
        and cleanup_absent
    ):
        raise RuntimeError("Independent helper hard-delete proof failed")
    return {
        "target_absent": True,
        "target_get_status": target_after.status_code,
        "target_missing_response_exact": True,
        "cleanup_route_status": route_after.status_code,
        "cleanup_helper_absent": cleanup_absent,
        "release_resource_cleanup_proved": manage_release_resources,
        "target_was_already_absent": target_already_absent,
        "method": "verified_cleanup_bridge",
    }


def observed_snippet(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": int(row.get("id") or 0),
        "name": str(row.get("name") or ""),
        "active": row.get("active"),
        "scope": str(row.get("scope") or ""),
        "code_sha256": sha256_text(str(row.get("code") or "")),
    }


def find_health_version(payload: Any) -> str:
    preferred = {"version", "plugin_version", "nadlan_config_version"}
    if isinstance(payload, dict):
        for key, value in payload.items():
            if str(key).lower() in preferred and isinstance(value, (str, int, float)):
                return str(value)
        for value in payload.values():
            found = find_health_version(value)
            if found:
                return found
    elif isinstance(payload, list):
        for value in payload:
            found = find_health_version(value)
            if found:
                return found
    return ""


def self_test() -> dict[str, Any]:
    validate_immutable_url(
        "https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/"
        + "a" * 40
        + "/plugin-dist/nadlan-config-9.9.9.zip"
    )
    helper = render_helper(
        route_path="/deploy-self-test",
        token="b" * 64,
        run_id="self-test",
        helper_id=123,
        helper_name="tmp-self-test",
        artifact_mode="url",
        artifact_url=(
            "https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/"
            + "a" * 40
            + "/plugin-dist/nadlan-config-9.9.9.zip"
        ),
        artifact_sha256="c" * 64,
        artifact_bytes=355,
        artifact_entry_count=2,
        artifact_uncompressed_bytes=60,
        expected_version="9.9.9",
    )
    upload_helper = render_helper(
        route_path="/deploy-upload-self-test",
        token="e" * 64,
        run_id="upload-self-test",
        helper_id=125,
        helper_name="tmp-upload-self-test",
        artifact_mode="upload",
        artifact_url="",
        artifact_sha256="f" * 64,
        artifact_bytes=355,
        artifact_entry_count=2,
        artifact_uncompressed_bytes=60,
        expected_version="9.9.9",
    )
    cleanup_helper = render_cleanup_helper(
        route_path="/cleanup-self-test",
        token="d" * 64,
        helper_id=124,
        helper_name="tmp-cleanup-self-test",
        target_id=123,
        target_name="tmp-self-test",
        target_hash=sha256_text(helper),
        release_run_id="upload-self-test",
        release_token="e" * 64,
        artifact_mode="upload",
        artifact_sha256="f" * 64,
        artifact_bytes=355,
        artifact_entry_count=2,
        artifact_uncompressed_bytes=60,
        manage_release_resources=True,
    )
    for forbidden in (
        "_yoast_wpseo_",
        "'_thumbnail_id'",
        "'project_featured'",
        "foreach ( get_post_meta( $source_post_id )",
    ):
        if forbidden in helper:
            raise RuntimeError(f"Self-test found forbidden broad-clone marker: {forbidden}")
    for required_showroom_marker in (
        "'project_3d_units'",
        "'project_model_glb'",
        "'project_3d_environment_json'",
        "'project_interior_panoramas'",
        "'lat'",
        "'lng'",
        "'_nadlan_private_unit_journey_project_name'",
        '"Rainbow Tel Aviv"',
        "'nl_unit_scene_v2'",
        "$page_matches_expected",
    ):
        if required_showroom_marker not in helper:
            raise RuntimeError(f"Self-test is missing showroom clone marker: {required_showroom_marker}")

    finalize_start = helper.find("if ( 'finalize' === $action )")
    if finalize_start < 0:
        raise RuntimeError("Self-test is missing the release-resource finalize action")
    finalize_section = helper[finalize_start:]
    if r"\Code_Snippets\delete_snippet" in finalize_section or "'helper_deleted'" in finalize_section:
        raise RuntimeError("Main helper must not self-delete during resource finalization")
    for required_finalize_marker in (
        "'resource_cleanup_complete'",
        "'backup_deleted'",
        "'lock_released'",
        "'state_deleted'",
        "'upload_temp_absent'",
        "'helper_retained'",
        "'helper_cleanup_pending'",
    ):
        if required_finalize_marker not in finalize_section:
            raise RuntimeError(f"Self-test is missing two-phase finalize marker: {required_finalize_marker}")
    finalize_order = (
        finalize_section.find("$wp_filesystem->delete( $backup_root"),
        finalize_section.find("$lock_released = $release_lock();"),
        finalize_section.find("delete_option( $state_key );"),
        finalize_section.find(r"$helper_after = \Code_Snippets\get_snippet"),
    )
    if any(position < 0 for position in finalize_order) or tuple(sorted(finalize_order)) != finalize_order:
        raise RuntimeError("Two-phase finalize ordering is not backup -> lock -> state -> helper-retention proof")
    if cleanup_helper.count(r"\Code_Snippets\delete_snippet") < 2:
        raise RuntimeError("Independent cleanup helper must hard-delete both target and itself")
    for route_loss_marker in (
        "if ( 'prepare' === $action )",
        "array( 'uploading', 'upload_verified' )",
        "$release_run_id . '|' . $release_token",
        "delete_option( $state_key );",
        "delete_option( $lock_key );",
        "if ( 'discard' === $action )",
        "'cleanup_prepare_required'",
    ):
        if route_loss_marker not in cleanup_helper:
            raise RuntimeError(
                f"Self-test is missing route-loss cleanup marker: {route_loss_marker}"
            )
    route_loss_order = (
        cleanup_helper.find("$wp_filesystem->delete( $upload_root"),
        cleanup_helper.find("delete_option( $state_key );"),
        cleanup_helper.find("delete_option( $lock_key );"),
        cleanup_helper.find(r"$target_deleted = \Code_Snippets\delete_snippet"),
    )
    if any(position < 0 for position in route_loss_order) or tuple(
        sorted(route_loss_order)
    ) != route_loss_order:
        raise RuntimeError(
            "Route-loss cleanup must be upload -> state -> owned lock -> main helper"
        )

    cleanup_contract = {
        "run_id": "upload-self-test",
        "artifact_mode": "upload",
        "upload_path": "derived-only",
        "upload_expected_sha256": "f" * 64,
        "upload_expected_bytes": 355,
        "upload_expected_entries": 2,
        "upload_expected_uncompressed_bytes": 60,
        "upload_chunk_bytes": UPLOAD_CHUNK_BYTES,
        "upload_total_chunks": 1,
    }

    def simulated_route_loss_cleanup_safe(
        phase: str, *, backup: bool = False, foreign_lock: bool = False
    ) -> bool:
        state = {**cleanup_contract, "phase": phase}
        if backup:
            state["backup_digest"] = "recovery-must-survive"
        state_owned = (
            state["run_id"] == "upload-self-test"
            and state["artifact_mode"] == "upload"
            and state["upload_path"] == "derived-only"
            and state["upload_expected_sha256"] == "f" * 64
            and state["upload_expected_bytes"] == 355
            and state["upload_expected_entries"] == 2
            and state["upload_expected_uncompressed_bytes"] == 60
            and state["upload_chunk_bytes"] == UPLOAD_CHUNK_BYTES
            and state["upload_total_chunks"] == 1
            and phase in {"uploading", "upload_verified"}
            and not state.get("backup_digest")
            and not state.get("page_id")
        )
        lock_owned = not foreign_lock
        return state_owned and lock_owned

    if not simulated_route_loss_cleanup_safe("uploading"):
        raise RuntimeError("Route-loss simulation rejected exact upload_init state")
    if not simulated_route_loss_cleanup_safe("upload_verified"):
        raise RuntimeError("Route-loss simulation rejected exact upload_finish state")
    if simulated_route_loss_cleanup_safe("deployed", backup=True):
        raise RuntimeError("Route-loss simulation discarded a deployment recovery state")
    if simulated_route_loss_cleanup_safe("uploading", foreign_lock=True):
        raise RuntimeError("Route-loss simulation accepted a foreign global lock")
    for required_upload_marker in (
        "if ( 'deploy_preflight' === $action )",
        "'nadlan-private-release-deploy-preflight/v1'",
        "@disk_free_space( WP_CONTENT_DIR )",
        "'backup_path_absent'",
        "'filesystem' => array( 'available' => $filesystem_available )",
        "if ( 'upload_init' === $action )",
        "if ( 'upload_chunk' === $action )",
        "if ( 'upload_finish' === $action )",
        "$upload_chunk_bytes = 128 * 1024;",
        "base64_decode( $encoded, true )",
        "flock( $handle, LOCK_EX )",
        "$temp_file = $upload_path;",
        "$run_id . '|' . $expected_token",
        "'upload_temp_absent'",
        "'upload_verified'",
    ):
        if required_upload_marker not in upload_helper:
            raise RuntimeError(f"Self-test is missing secure upload marker: {required_upload_marker}")
    for stage, reason_codes in DEPLOY_FAILURE_CONTRACT.items():
        if f"'{stage}'" not in upload_helper:
            raise RuntimeError(f"Self-test is missing deployment failure stage: {stage}")
        for reason_code in reason_codes:
            if f"'{reason_code}'" not in upload_helper:
                raise RuntimeError(
                    f"Self-test is missing deployment failure reason: {reason_code}"
                )
    for diagnostic_marker in (
        "'failure_stage'",
        "'failure_reason_code'",
        "'rollback_outcome'",
        "'not_required'",
        "'succeeded'",
        "'failed'",
    ):
        if diagnostic_marker not in upload_helper:
            raise RuntimeError(
                f"Self-test is missing finite deploy diagnostic: {diagnostic_marker}"
            )
    if "getMessage()" in upload_helper:
        raise RuntimeError("Deploy helper must not serialize exception messages")
    if cleanup_helper.count("$target_exists = $target && 0 < (int) $target->id;") != 2:
        raise RuntimeError("Cleanup helper must treat truthy id=0 snippets as absent")
    for rollback_marker in (
        "activate_plugin( $plugin_file, '', false, true )",
        "deactivate_plugins( $plugin_file, true, false )",
        "$before_active !== (bool) $restored_plugin['active']",
        "$current_state['rollback_active']",
        "'rollback_digest'",
        "'before'",
    ):
        if rollback_marker not in helper:
            raise RuntimeError(
                f"Self-test is missing exact rollback activation marker: {rollback_marker}"
            )
    if "$request->get_param( 'upload_path' )" in upload_helper:
        raise RuntimeError("Deploy helper must never accept a caller-provided artifact path")
    if UPLOAD_CHUNK_BYTES > 256 * 1024 or (
        MAX_ARCHIVE_BYTES + UPLOAD_CHUNK_BYTES - 1
    ) // UPLOAD_CHUNK_BYTES > MAX_UPLOAD_CHUNKS:
        raise RuntimeError("Upload chunk/archive bounds are inconsistent")
    chunk_probe = b"x" * UPLOAD_CHUNK_BYTES
    encoded_probe = base64.b64encode(chunk_probe)
    if len(encoded_probe) > 256 * 1024 or base64.b64decode(encoded_probe, validate=True) != chunk_probe:
        raise RuntimeError("Bounded upload base64 round-trip failed")

    driver_source = Path(__file__).read_text(encoding="utf-8")
    main_position = driver_source.find("\ndef main(")
    success_health_position = driver_source.find("final_health = public.get(", main_position)
    phase_one_position = driver_source.find(
        "finalize_response, finalize, finalize_attempts = finalize_release_resources()",
        main_position,
    )
    finally_position = driver_source.find(
        "    finally:\n        retain_recovery_helper = deploy_started and not resources_finalized",
        main_position,
    )
    phase_two_position = driver_source.find(
        "cleanup_proof = independently_remove_snippet(", finally_position
    )
    preflight_driver_position = driver_source.find(
        'call_helper("deploy_preflight"', main_position
    )
    upload_driver_position = driver_source.find(
        'result["checks"]["artifact_upload"] = upload_local_artifact()',
        preflight_driver_position,
    )
    deploy_driver_position = driver_source.find(
        'deploy_response, deploy = call_helper("deploy"', upload_driver_position
    )
    if not (
        0 <= main_position < success_health_position < phase_one_position < finally_position < phase_two_position
        and 0
        <= preflight_driver_position
        < upload_driver_position
        < deploy_driver_position
        and "independently_remove_snippet(" not in driver_source[phase_one_position:finally_position]
        and "and not retain_recovery_helper" in driver_source[finally_position:phase_two_position]
        and "recovery_retained" in driver_source[finally_position:]
        and "def rollback_response_is_exact(" in driver_source[main_position:]
        and '"rolled_back",' in driver_source[main_position:]
        and "rollback_response_is_exact(rollback)" in driver_source[main_position:]
    ):
        raise RuntimeError("Driver must defer independent helper deletion to finally after phase one")
    with tempfile.TemporaryDirectory(prefix="nadlan-release-self-test-") as temp_dir:
        temp = Path(temp_dir)
        valid_zip = temp / "valid.zip"
        with zipfile.ZipFile(valid_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(
                f"{PLUGIN_ROOT}/nadlan-config.php",
                "<?php\n/* Plugin Name: Nadlan Config\nVersion: 9.9.9\n*/\n",
            )
            archive.writestr(f"{PLUGIN_ROOT}/inc/example.php", "<?php\n")
        zip_proof = validate_zip(valid_zip)
        noncanonical_path_rejected = False
        try:
            validate_canonical_artifact_path(
                valid_zip, "9.9.9", hashlib.sha256(valid_zip.read_bytes()).hexdigest()
            )
        except ValueError:
            noncanonical_path_rejected = True
        if not noncanonical_path_rejected:
            raise RuntimeError("Self-test accepted a ZIP outside canonical plugin-dist")

        traversal_zip = temp / "traversal.zip"
        with zipfile.ZipFile(traversal_zip, "w") as archive:
            archive.writestr(f"{PLUGIN_ROOT}/../escape.php", "<?php\n")
        traversal_rejected = False
        try:
            validate_zip(traversal_zip)
        except ValueError:
            traversal_rejected = True
        if not traversal_rejected:
            raise RuntimeError("Self-test did not reject ZIP traversal")

        php_lint = "not_available"
        php = shutil.which("php")
        if php:
            rendered = temp / "helper.php"
            rendered.write_text("<?php\n" + helper + "\n", encoding="utf-8")
            cleanup_rendered = temp / "cleanup-helper.php"
            cleanup_rendered.write_text("<?php\n" + cleanup_helper + "\n", encoding="utf-8")
            upload_rendered = temp / "upload-helper.php"
            upload_rendered.write_text("<?php\n" + upload_helper + "\n", encoding="utf-8")
            for candidate in (rendered, upload_rendered, cleanup_rendered):
                completed = subprocess.run(
                    [php, "-l", str(candidate)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                if completed.returncode != 0:
                    raise RuntimeError("Rendered PHP helper failed php -l")
            php_lint = "passed"

    canonical_candidates = sorted((REPO_ROOT / "plugin-dist").glob("nadlan-config-*.zip"))
    if not canonical_candidates:
        raise RuntimeError("Self-test found no canonical plugin-dist artifact")
    canonical_candidate = canonical_candidates[0]
    canonical_version = canonical_candidate.stem.removeprefix("nadlan-config-")
    canonical_sha256 = hashlib.sha256(canonical_candidate.read_bytes()).hexdigest()
    _, canonical_proof = validate_canonical_artifact_path(
        canonical_candidate, canonical_version, canonical_sha256
    )
    canonical_sha_mismatch_rejected = False
    try:
        validate_canonical_artifact_path(canonical_candidate, canonical_version, "0" * 64)
    except ValueError:
        canonical_sha_mismatch_rejected = True
    if not canonical_sha_mismatch_rejected:
        raise RuntimeError("Self-test accepted a canonical artifact with the wrong SHA-256")

    einstein_request = validate_einstein_stage_request(
        REPO_ROOT / "docs" / "wp-drafts" / "einstein-tower-flagship-v3-private-stage.json"
    )
    offline_password = "offline-einstein-stage-secret"

    class FakeResponse:
        def __init__(self, status_code: int, payload: Any):
            self.status_code = status_code
            self._payload = payload
            self.headers: dict[str, str] = {}
            self.text = json.dumps(payload, ensure_ascii=False)

        def json(self) -> Any:
            return copy.deepcopy(self._payload)

    missing_404 = FakeResponse(404, {"code": "rest_cannot_get"})
    missing_500 = FakeResponse(
        500,
        {
            "code": MISSING_SNIPPET_CODE,
            "message": MISSING_SNIPPET_MESSAGE,
            "data": {"status": 500},
        },
    )
    missing_500_without_data = FakeResponse(
        500,
        {"code": MISSING_SNIPPET_CODE, "message": MISSING_SNIPPET_MESSAGE},
    )
    wrong_missing_message = FakeResponse(
        500,
        {"code": MISSING_SNIPPET_CODE, "message": "Different message"},
    )
    extra_missing_field = FakeResponse(
        500,
        {
            "code": MISSING_SNIPPET_CODE,
            "message": MISSING_SNIPPET_MESSAGE,
            "unexpected": True,
        },
    )
    if not all(
        is_exact_missing_snippet_response(response)
        for response in (missing_404, missing_500, missing_500_without_data)
    ) or any(
        is_exact_missing_snippet_response(response)
        for response in (wrong_missing_message, extra_missing_field)
    ):
        raise RuntimeError("Exact Code Snippets missing-response predicate drifted")
    if snippet_absent_from_collection(
        [{"id": 7002, "name": "same-name"}],
        snippet_id=7001,
        snippet_name="same-name",
    ):
        raise RuntimeError("Same-name/different-ID snippet residue was accepted as absent")
    if not snippet_absence_is_proved(
        missing_500,
        [],
        snippet_id=7001,
        snippet_name="missing-helper",
        route_status=404,
    ) or snippet_absence_is_proved(
        missing_500,
        [],
        snippet_id=7001,
        snippet_name="missing-helper",
        route_status=200,
    ):
        raise RuntimeError("Snippet absence was not paired with exact route absence")

    class EmptySnippetClient:
        @staticmethod
        def all_snippets() -> list[dict[str, Any]]:
            return []

    managed_absence_without_proof_rejected = False
    try:
        independently_remove_snippet(
            EmptySnippetClient(),  # type: ignore[arg-type]
            target_id=None,
            target_name="missing-helper",
            release_run_id="missing-helper-test",
            release_token="1" * 64,
            artifact_mode="upload",
            artifact_sha256="2" * 64,
            artifact_bytes=355,
            artifact_entry_count=2,
            artifact_uncompressed_bytes=60,
            manage_release_resources=True,
        )
    except RuntimeError:
        managed_absence_without_proof_rejected = True
    if not managed_absence_without_proof_rejected:
        raise RuntimeError("Missing helper claimed unproved managed-resource cleanup")
    known_absence = independently_remove_snippet(
        EmptySnippetClient(),  # type: ignore[arg-type]
        target_id=None,
        target_name="never-created-helper",
        release_run_id="never-created-helper-test",
        release_token="3" * 64,
        artifact_mode="upload",
        artifact_sha256="4" * 64,
        artifact_bytes=355,
        artifact_entry_count=2,
        artifact_uncompressed_bytes=60,
        manage_release_resources=True,
        resources_known_absent=True,
    )
    if known_absence.get("release_resource_cleanup_proved") is not True:
        raise RuntimeError("Explicit pre-resource helper absence was not accepted")

    failure_payload = {
        "code": "nadlan_release_deploy_failed",
        "data": {
            "failure_stage": "backup_copy",
            "failure_reason_code": "plugin_backup_copy_failed",
            "rolled_back": False,
            "rollback_outcome": "not_required",
            "upload_temp_absent": True,
        },
    }
    failure_response = FakeResponse(500, failure_payload)
    finite_failure_proof = deploy_failure_proof(failure_response, failure_payload)
    if finite_failure_proof.get("contract_valid") is not True:
        raise RuntimeError("Valid finite deployment failure proof was rejected")
    cross_paired_failure = copy.deepcopy(failure_payload)
    cross_paired_failure["data"]["failure_reason_code"] = "disk_space_insufficient"
    if deploy_failure_proof(
        FakeResponse(500, cross_paired_failure), cross_paired_failure
    ).get("contract_valid") is not False:
        raise RuntimeError("Cross-paired deployment failure proof was accepted")
    nonboolean_failure = copy.deepcopy(failure_payload)
    nonboolean_failure["data"]["rolled_back"] = "false"
    if deploy_failure_proof(
        FakeResponse(500, nonboolean_failure), nonboolean_failure
    ).get("contract_valid") is not False:
        raise RuntimeError("Non-boolean deployment rollback evidence was accepted")
    rollback_outcomes = set()
    for outcome, rolled_back in (
        ("not_required", False),
        ("succeeded", True),
        ("failed", False),
    ):
        outcome_payload = copy.deepcopy(failure_payload)
        outcome_payload["data"]["failure_stage"] = "backup_commit"
        outcome_payload["data"]["failure_reason_code"] = (
            "backup_state_persist_failed"
        )
        outcome_payload["data"]["rollback_outcome"] = outcome
        outcome_payload["data"]["rolled_back"] = rolled_back
        outcome_proof = deploy_failure_proof(
            FakeResponse(500, outcome_payload), outcome_payload
        )
        if outcome_proof.get("contract_valid") is not True:
            raise RuntimeError("Finite deployment rollback outcome was rejected")
        rollback_outcomes.add(str(outcome_proof["rollback_outcome"]))
    if rollback_outcomes != {"not_required", "succeeded", "failed"}:
        raise RuntimeError("Deployment rollback outcomes are not distinguishable")
    impossible_prebackup_rollback = copy.deepcopy(failure_payload)
    impossible_prebackup_rollback["data"]["rolled_back"] = True
    impossible_prebackup_rollback["data"]["rollback_outcome"] = "succeeded"
    if deploy_failure_proof(
        FakeResponse(500, impossible_prebackup_rollback),
        impossible_prebackup_rollback,
    ).get("contract_valid") is not False:
        raise RuntimeError("Impossible pre-backup rollback outcome was accepted")
    contradictory_postinstall = copy.deepcopy(failure_payload)
    contradictory_postinstall["data"].update(
        {
            "failure_stage": "plugin_install",
            "failure_reason_code": "plugin_upgrade_failed",
            "rolled_back": False,
            "rollback_outcome": "not_required",
        }
    )
    if deploy_failure_proof(
        FakeResponse(500, contradictory_postinstall), contradictory_postinstall
    ).get("contract_valid") is not False:
        raise RuntimeError("Post-backup failure without rollback outcome was accepted")
    rolled_back_postinstall = copy.deepcopy(contradictory_postinstall)
    rolled_back_postinstall["data"]["rolled_back"] = True
    rolled_back_postinstall["data"]["rollback_outcome"] = "succeeded"
    if deploy_failure_proof(
        FakeResponse(500, rolled_back_postinstall), rolled_back_postinstall
    ).get("contract_valid") is not True:
        raise RuntimeError("Post-backup failure with confirmed rollback was rejected")

    preflight_target_bytes = 1234
    preflight_required = (
        preflight_target_bytes + 355 + 60 + 20 * 1024 * 1024
    )
    valid_preflight = {
        "schema": DEPLOY_PREFLIGHT_SCHEMA,
        "passed": True,
        "target": {
            "readable": True,
            "active": True,
            "version": "1.2.3",
            "file_count": 10,
            "bytes": preflight_target_bytes,
        },
        "disk": {
            "measurable": True,
            "free_bytes": preflight_required + 1,
            "required_bytes": preflight_required,
            "sufficient": True,
        },
        "upgrade": {
            "root_safe": True,
            "root_writable": True,
            "backup_path_absent": True,
        },
        "filesystem": {"available": True},
    }
    valid_preflight_proof = deploy_preflight_proof(
        valid_preflight,
        before_version="1.2.3",
        artifact_bytes=355,
        artifact_uncompressed_bytes=60,
    )
    if valid_preflight_proof.get("passed") is not True:
        raise RuntimeError("Valid read-only deployment preflight proof was rejected")
    failed_preflight = copy.deepcopy(valid_preflight)
    failed_preflight["upgrade"]["root_writable"] = False
    if deploy_preflight_proof(
        failed_preflight,
        before_version="1.2.3",
        artifact_bytes=355,
        artifact_uncompressed_bytes=60,
    ).get("passed") is not False:
        raise RuntimeError("Failed read-only deployment preflight was accepted")

    def fake_record(post_id: int, body: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": post_id,
            "slug": body["slug"],
            "status": body["status"],
            "title": {"raw": body["title"]},
            "content": {"raw": body["content"]},
            "excerpt": {"raw": body["excerpt"]},
            "password": body.get("password", ""),
            "meta": copy.deepcopy(body["meta"]),
            "link": f"https://nad-lan.co.il/projects/{body['slug']}/",
        }

    class ResponseLostClient:
        def __init__(
            self,
            stage: dict[str, Any] | None,
            *,
            created_post_id: int = 9001,
            created_slug: str = EINSTEIN_STAGE_SLUG,
        ):
            public_body = {
                "slug": "einstein-tower",
                "status": "publish",
                "title": "Canonical Einstein",
                "content": "canonical-public-body",
                "excerpt": "canonical-public-excerpt",
                "password": "",
                "meta": {"project_contract_id": EINSTEIN_PROJECT_CONTRACT_ID},
            }
            self.records: dict[int, dict[str, Any]] = {
                EINSTEIN_CANONICAL_POST_ID: fake_record(
                    EINSTEIN_CANONICAL_POST_ID, public_body
                )
            }
            if stage is not None:
                self.records[int(stage["id"])] = copy.deepcopy(stage)
            self.lose_next_stage_write = True
            self.created_post_id = created_post_id
            self.created_slug = created_slug
            self.delete_requests = 0

        def request(
            self,
            method: str,
            route: str,
            *,
            json_body: dict[str, Any] | None = None,
            timeout: int = 60,
        ) -> FakeResponse:
            del timeout
            normalized = route.split("?", 1)[0]
            if method == "GET" and normalized == "wp/v2/nadlan_project":
                rows = [
                    copy.deepcopy(row)
                    for row in self.records.values()
                    if row.get("slug") == EINSTEIN_STAGE_SLUG
                ]
                return FakeResponse(200, rows)
            match = re.fullmatch(r"wp/v2/nadlan_project/(\d+)", normalized)
            if method == "GET" and match:
                post_id = int(match.group(1))
                if post_id not in self.records:
                    return FakeResponse(404, {"code": "rest_post_invalid_id"})
                return FakeResponse(200, self.records[post_id])
            if method == "POST" and normalized == "wp/v2/nadlan_project":
                post_id = self.created_post_id
                created_body = dict(json_body or {})
                created_body["slug"] = self.created_slug
                self.records[post_id] = fake_record(post_id, created_body)
                if self.lose_next_stage_write:
                    self.lose_next_stage_write = False
                    raise requests.Timeout("simulated response loss after applied create")
                return FakeResponse(201, self.records[post_id])
            if method == "POST" and match:
                post_id = int(match.group(1))
                if post_id not in self.records:
                    return FakeResponse(404, {"code": "rest_post_invalid_id"})
                body = dict(json_body or {})
                record = self.records[post_id]
                for key in ("slug", "status", "password"):
                    if key in body:
                        record[key] = body[key]
                for key in ("title", "content", "excerpt"):
                    if key in body:
                        record[key] = {"raw": body[key]}
                if isinstance(body.get("meta"), dict):
                    for key, value in body["meta"].items():
                        if value is None:
                            record["meta"].pop(key, None)
                        else:
                            record["meta"][key] = copy.deepcopy(value)
                if self.lose_next_stage_write:
                    self.lose_next_stage_write = False
                    raise requests.Timeout("simulated response loss after applied update")
                return FakeResponse(200, record)
            if method == "DELETE" and match:
                self.delete_requests += 1
                post_id = int(match.group(1))
                existed = self.records.pop(post_id, None) is not None
                return FakeResponse(200 if existed else 404, {"deleted": existed})
            raise AssertionError(f"Unexpected fake WordPress request: {method} {route}")

    create_client = ResponseLostClient(None)
    create_lost_rolled_back = False
    try:
        write_einstein_stage(create_client, einstein_request, offline_password)
    except requests.Timeout:
        create_lost_rolled_back = not any(
            row.get("slug") == EINSTEIN_STAGE_SLUG
            for row in create_client.records.values()
        )
    if not create_lost_rolled_back:
        raise RuntimeError("Response-lost Einstein create was not deleted exactly")

    suffixed_client = ResponseLostClient(
        None,
        created_post_id=9009,
        created_slug=EINSTEIN_STAGE_SLUG + "-2",
    )
    suffixed_create_recovery_blocked = False
    try:
        write_einstein_stage(suffixed_client, einstein_request, offline_password)
    except EinsteinStageRecoveryBlocked:
        suffixed_create_recovery_blocked = (
            9009 in suffixed_client.records
            and suffixed_client.records[9009].get("slug")
            == EINSTEIN_STAGE_SLUG + "-2"
            and suffixed_client.delete_requests == 0
        )
    if not suffixed_create_recovery_blocked:
        raise RuntimeError(
            "Response-lost suffixed-slug Einstein create did not preserve recovery safely"
        )

    prior_body = copy.deepcopy(einstein_request["body"])
    prior_body.update(
        {
            "title": "Prior private stage",
            "content": "prior private content",
            "excerpt": "prior private excerpt",
            "password": "prior-private-password",
        }
    )
    prior_body["meta"]["unrelated_registered_meta"] = "preserve-me"
    prior_record = fake_record(9002, prior_body)
    prior_snapshot = wordpress_post_snapshot(prior_record)
    update_client = ResponseLostClient(prior_record)
    update_lost_rolled_back = False
    try:
        write_einstein_stage(update_client, einstein_request, offline_password)
    except requests.Timeout:
        update_lost_rolled_back = (
            wordpress_post_snapshot(update_client.records[9002]) == prior_snapshot
        )
    if not update_lost_rolled_back:
        raise RuntimeError("Response-lost Einstein update was not restored exactly")

    valid_acceptance = {
        "schema": EINSTEIN_ACCEPTANCE_SCHEMA,
        "totals": {
            "passed": True,
            "failures": 0,
            "warnings": 0,
            "viewports": len(EINSTEIN_ACCEPTANCE_VIEWPORTS),
            "assetsObserved": len(EINSTEIN_ACCEPTANCE_ASSETS),
            "keyboardToolChecks": EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS[
                "keyboardToolChecks"
            ],
            "textResizeDialogChecks": EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS[
                "textResizeDialogChecks"
            ],
            "historyTransitions": EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS[
                "browserHistoryTransitions"
            ],
        },
        "failures": [],
        "warnings": [],
        "matrix": [
            {"viewport": viewport, "passed": True}
            for viewport in EINSTEIN_ACCEPTANCE_VIEWPORTS
        ],
        "assets": [{"name": name} for name in EINSTEIN_ACCEPTANCE_ASSETS],
        "anonymous": {"passed": True},
        "discovery": {"passed": True},
        "health": {"passed": True},
        "unlocked": {"passed": True},
        "browserBack": {"passed": True},
        "keyboard": {
            "passed": True,
            "viewports": [
                {
                    "viewport": viewport,
                    "passed": True,
                    "tools": [
                        {
                            "tool": tool,
                            "escapeClosed": True,
                            "passed": True,
                        }
                        for tool in ("view", "interior", "design", "comments")
                    ],
                }
                for viewport in EINSTEIN_ACCEPTANCE_ACCESSIBILITY_VIEWPORTS
            ],
        },
        "browserHistory": {
            "passed": True,
            "transitions": [
                {"direction": "back", "passed": True},
                {"direction": "forward", "passed": True},
            ],
        },
        "textResize200": {
            "passed": True,
            "viewports": [
                {
                    "viewport": viewport,
                    "passed": True,
                    "dialogs": [
                        {"tool": tool, "passed": True}
                        for tool in ("view", "interior", "design", "comments")
                    ],
                }
                for viewport in EINSTEIN_ACCEPTANCE_ACCESSIBILITY_VIEWPORTS
            ],
        },
        "evidenceCounts": {
            "expected": copy.deepcopy(EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS),
            "observed": copy.deepcopy(EINSTEIN_ACCEPTANCE_EVIDENCE_COUNTS),
            "matched": True,
        },
    }
    valid_acceptance_proof = acceptance_summary_proof(
        valid_acceptance, einstein_mode=True
    )
    forged_exit_zero_rejected = False
    forged_acceptance = copy.deepcopy(valid_acceptance)
    forged_acceptance["totals"]["passed"] = False
    try:
        acceptance_summary_proof(forged_acceptance, einstein_mode=True)
    except RuntimeError:
        forged_exit_zero_rejected = True
    if not forged_exit_zero_rejected:
        raise RuntimeError("Self-test accepted an exit-zero Einstein report with failed totals")
    forged_evidence_rejected = False
    forged_acceptance = copy.deepcopy(valid_acceptance)
    forged_acceptance["evidenceCounts"]["observed"]["keyboardEscapeRestores"] = 7
    try:
        acceptance_summary_proof(forged_acceptance, einstein_mode=True)
    except RuntimeError:
        forged_evidence_rejected = True
    if not forged_evidence_rejected:
        raise RuntimeError("Self-test accepted forged Einstein evidence counts")
    forged_behavior_gate_rejected = False
    forged_acceptance = copy.deepcopy(valid_acceptance)
    forged_acceptance["browserHistory"]["passed"] = False
    try:
        acceptance_summary_proof(forged_acceptance, einstein_mode=True)
    except RuntimeError:
        forged_behavior_gate_rejected = True
    if not forged_behavior_gate_rejected:
        raise RuntimeError("Self-test accepted a failed Einstein behavior gate")
    if acceptance_summary_proof(
        {"hardFailures": [], "warnings": []}, einstein_mode=False
    ).get("passed") is not True:
        raise RuntimeError("Legacy browser acceptance summary handling changed")

    stage_write_position = driver_source.find(
        "einstein_transaction = write_einstein_stage(", main_position
    )
    browser_position = driver_source.find("acceptance = subprocess.run(", stage_write_position)
    final_readback_position = driver_source.find(
        'result["checks"]["final_stage_readback"]', browser_position
    )
    stage_rollback_position = driver_source.find(
        'result["checks"]["failure_stage_rollback"]', main_position
    )
    plugin_failure_status_position = driver_source.find(
        "status_confirmed = False", stage_rollback_position
    )
    blocked_state_position = driver_source.find(
        "if isinstance(error, EinsteinStageRecoveryBlocked):", main_position
    )
    blocked_plugin_rollback_guard = driver_source.find(
        "if rollback_required and not stage_rollback_blocked:", blocked_state_position
    )
    blocked_finalize_guard = driver_source.find(
        "safe_to_finalize = (", blocked_plugin_rollback_guard
    )
    deploy_recovery_finalize_guard = driver_source.find(
        "and not deploy_failure_recovery_blocked", blocked_finalize_guard
    )
    recovery_retention_position = driver_source.find(
        "retain_recovery_helper = deploy_started and not resources_finalized",
        blocked_finalize_guard,
    )
    if not (
        0
        <= stage_write_position
        < browser_position
        < final_readback_position
        < phase_one_position
        and 0 <= stage_rollback_position < plugin_failure_status_position
        and 0
        <= blocked_state_position
        < blocked_plugin_rollback_guard
        < blocked_finalize_guard
        < deploy_recovery_finalize_guard
        < recovery_retention_position
    ):
        raise RuntimeError("Einstein stage/browser/finalize or stage/plugin rollback ordering drifted")

    return {
        "passed": True,
        "template_sha256": hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(),
        "rendered_helper_bytes": len(helper.encode("utf-8")),
        "rendered_upload_helper_bytes": len(upload_helper.encode("utf-8")),
        "rendered_cleanup_helper_bytes": len(cleanup_helper.encode("utf-8")),
        "zip_validation": zip_proof,
        "traversal_rejected": traversal_rejected,
        "two_phase_finalize": True,
        "helper_cleanup_in_finally": True,
        "route_loss_cleanup_simulation": {
            "upload_init": "safe_cleanup",
            "upload_finish": "safe_cleanup",
            "deployed_recovery": "retained",
            "foreign_lock": "retained",
        },
        "code_snippets_missing_contract": {
            "http_404_accepted": True,
            "exact_http_500_accepted": True,
            "wrong_500_rejected": True,
            "same_name_different_id_rejected": True,
            "managed_absence_without_proof_rejected": (
                managed_absence_without_proof_rejected
            ),
        },
        "deploy_preflight": {
            "schema": DEPLOY_PREFLIGHT_SCHEMA,
            "valid_proof_passed": valid_preflight_proof["passed"],
            "failed_proof_rejected": True,
            "before_upload": True,
        },
        "deploy_failure_contract": {
            "finite_pair_allowlist": True,
            "cross_pair_rejected": True,
            "strict_booleans": True,
            "rollback_outcomes": sorted(rollback_outcomes),
        },
        "rollback_activation_contract": True,
        "secure_local_upload": True,
        "noncanonical_path_rejected": noncanonical_path_rejected,
        "canonical_sha_mismatch_rejected": canonical_sha_mismatch_rejected,
        "einstein_private_stage": {
            "request_validated": True,
            "exact_slug": EINSTEIN_STAGE_SLUG,
            "canonical_public_post_id": EINSTEIN_CANONICAL_POST_ID,
            "project_contract_id": EINSTEIN_PROJECT_CONTRACT_ID,
            "response_lost_create_rolled_back": create_lost_rolled_back,
            "response_lost_suffixed_create_recovery_blocked": suffixed_create_recovery_blocked,
            "response_lost_suffixed_create_delete_requests": suffixed_client.delete_requests,
            "blocked_stage_skips_plugin_rollback_and_finalize": True,
            "response_lost_update_rolled_back": update_lost_rolled_back,
            "scoped_meta_restore_preserved_unrelated": True,
            "browser_before_finalize": True,
            "stage_rollback_before_plugin_rollback": True,
            "acceptance_schema_exact": valid_acceptance_proof["schema"]
            == EINSTEIN_ACCEPTANCE_SCHEMA,
            "acceptance_matrix_count": valid_acceptance_proof["matrix_count"],
            "acceptance_asset_count": valid_acceptance_proof["asset_count"],
            "acceptance_evidence_expected": valid_acceptance_proof[
                "evidence_expected"
            ],
            "acceptance_evidence_observed": valid_acceptance_proof[
                "evidence_observed"
            ],
            "forged_exit_zero_failed_totals_rejected": forged_exit_zero_rejected,
            "forged_evidence_counts_rejected": forged_evidence_rejected,
            "forged_behavior_gate_rejected": forged_behavior_gate_rejected,
            "legacy_acceptance_contract_preserved": True,
        },
        "canonical_local_artifact": {
            "sha256": canonical_sha256,
            "archive_bytes": int(canonical_proof["archive_bytes"]),
            "entry_count": int(canonical_proof["entry_count"]),
        },
        "php_lint": php_lint,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", type=Path, default=REPO_ROOT / ".env")
    artifact_source = parser.add_mutually_exclusive_group()
    artifact_source.add_argument("--artifact-url", help="Immutable public raw-GitHub commit URL.")
    artifact_source.add_argument(
        "--artifact-path",
        type=Path,
        help="Exact canonical plugin-dist ZIP; uploaded through the temporary authenticated route.",
    )
    parser.add_argument("--artifact-sha256", help="Required reviewed artifact SHA-256 for either mode.")
    parser.add_argument("--expected-version")
    parser.add_argument(
        "--post-password",
        help="Private sandbox password; prefer SANDBOX_POST_PASSWORD to avoid shell history.",
    )
    parser.add_argument(
        "--einstein-stage-request",
        type=Path,
        help="Use the exact governed Einstein private-stage request instead of the legacy journey clone.",
    )
    parser.add_argument(
        "--protected-main-commit",
        help="Required in Einstein mode; exact origin/main commit containing the canonical ZIP.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "reports" / "private-unit-journey-release",
    )
    parser.add_argument(
        "--acceptance-script",
        type=Path,
        default=None,
        help="Playwright gate executed before the rollback backup and helper are removed.",
    )
    parser.add_argument("--acceptance-timeout-seconds", type=int, default=2400)
    parser.add_argument("--health-attempts", type=int, default=6)
    parser.add_argument("--health-delay-seconds", type=float, default=3.0)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False, indent=2))
        return 0

    einstein_request: dict[str, Any] | None = None
    if args.einstein_stage_request is not None:
        try:
            einstein_request = validate_einstein_stage_request(args.einstein_stage_request)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            raise SystemExit(str(error)) from error

    required_args = {
        "--artifact-sha256": args.artifact_sha256,
        "--expected-version": args.expected_version,
    }
    missing_args = [name for name, value in required_args.items() if not value]
    if missing_args:
        raise SystemExit(f"Missing required arguments: {', '.join(missing_args)}")
    if args.health_attempts < 1 or args.health_attempts > 20:
        raise SystemExit("--health-attempts must be between 1 and 20")
    if args.health_delay_seconds < 0 or args.health_delay_seconds > 30:
        raise SystemExit("--health-delay-seconds must be between 0 and 30")
    default_acceptance = (
        REPO_ROOT / "scripts" / "qa-einstein-flagship-live.mjs"
        if einstein_request is not None
        else REPO_ROOT / "scripts" / "qa-private-unit-journey.mjs"
    )
    acceptance_script = (args.acceptance_script or default_acceptance).resolve()
    if not acceptance_script.is_file():
        raise SystemExit(f"Acceptance script is missing: {acceptance_script}")
    if args.acceptance_timeout_seconds < 60 or args.acceptance_timeout_seconds > 7200:
        raise SystemExit("--acceptance-timeout-seconds must be between 60 and 7200")

    artifact_sha256 = str(args.artifact_sha256).lower()
    if not re.fullmatch(r"[a-f0-9]{64}", artifact_sha256):
        raise SystemExit("--artifact-sha256 must be 64 lowercase hexadecimal characters")
    if not re.fullmatch(
        r"[0-9]+(?:\.[0-9]+){1,3}(?:[-.][A-Za-z0-9]+)*", str(args.expected_version)
    ):
        raise SystemExit("--expected-version is not a safe plugin version")
    if bool(args.artifact_url) == bool(args.artifact_path):
        raise SystemExit("Exactly one of --artifact-url or --artifact-path is required")
    if einstein_request is not None and (
        args.artifact_path is None or args.artifact_url is not None or not args.protected_main_commit
    ):
        raise SystemExit(
            "Einstein mode requires --artifact-path and --protected-main-commit; URL mode is forbidden"
        )
    if einstein_request is None and args.protected_main_commit:
        raise SystemExit("--protected-main-commit is valid only with --einstein-stage-request")
    artifact_mode = "upload" if args.artifact_path else "url"
    commit_sha = validate_immutable_url(str(args.artifact_url)) if args.artifact_url else ""
    local_artifact_path: Path | None = None
    artifact_proof: dict[str, Any] | None = None
    if artifact_mode == "upload":
        try:
            local_artifact_path, artifact_proof = validate_canonical_artifact_path(
                args.artifact_path, str(args.expected_version), artifact_sha256
            )
        except ValueError as error:
            raise SystemExit(str(error)) from error
    protected_main_proof: dict[str, Any] | None = None
    if einstein_request is not None:
        if local_artifact_path is None:
            raise SystemExit("Einstein protected-main artifact proof requires the canonical local ZIP")
        try:
            protected_main_proof = validate_protected_main_artifact(
                str(args.protected_main_commit),
                local_artifact_path,
                str(args.expected_version),
                artifact_sha256,
            )
        except (OSError, ValueError) as error:
            raise SystemExit(str(error)) from error

    file_env = read_env(args.env)
    merged_env = dict(file_env)
    merged_env.update({key: value for key, value in os.environ.items() if value})
    base_url_input = merged_env.get("WP_BASE_URL", "").rstrip("/")
    wp_user = merged_env.get("WP_USER", "")
    wp_password = merged_env.get("WP_APP_PASSWORD", "")
    if einstein_request is not None and args.post_password:
        raise SystemExit("Einstein mode accepts SANDBOX_POST_PASSWORD from the environment only")
    post_password = args.post_password or merged_env.get("SANDBOX_POST_PASSWORD", "")
    missing_env = [
        key
        for key, value in {
            "WP_BASE_URL": base_url_input,
            "WP_USER": wp_user,
            "WP_APP_PASSWORD": wp_password,
            "SANDBOX_POST_PASSWORD or --post-password": post_password,
        }.items()
        if not value
    ]
    if missing_env:
        raise SystemExit(f"Missing required secret inputs: {', '.join(missing_env)}")
    base_url = validate_site_url(base_url_input)

    run_prefix = "einstein-flagship" if einstein_request is not None else "unit-journey"
    run_id = f"{run_prefix}-{utc_slug()}-{secrets.token_hex(3)}"
    helper_name = f"tmp-{run_id}"
    route_path = f"/deploy-{run_id}"
    route = f"{ROUTE_NAMESPACE}{route_path}"
    token = secrets.token_hex(32)
    redactor = Redactor(
        (
            wp_password,
            post_password,
            token,
            str(args.artifact_url or ""),
            str(args.artifact_path or ""),
            str(local_artifact_path or ""),
        )
    )
    client = WordpressClient(base_url, wp_user, wp_password)
    public = requests.Session()
    public.headers.update(
        {"User-Agent": "NadLan-Private-Unit-Journey-Health/1.0", "Accept": "application/json"}
    )
    helper_id: int | None = None
    helper_hash = ""
    helper_creation_attempted = False
    deploy_started = False
    release_resources_may_exist = False
    resources_finalized = False
    deployed = False
    page_url = ""
    einstein_transaction: dict[str, Any] | None = None
    stage_rollback_blocked = False
    deploy_failure_recovery_blocked = False
    einstein_public_predeploy_sha256 = ""
    before_plugin_contract: dict[str, Any] = {}
    created_cleanup_rows: list[dict[str, Any]] = []
    artifact_evidence: dict[str, Any] = {
        "mode": artifact_mode,
        "sha256": artifact_sha256,
    }
    if commit_sha:
        artifact_evidence["source_commit_sha"] = commit_sha
    if protected_main_proof is not None:
        artifact_evidence["protected_main"] = protected_main_proof
    target_contract = {
        "site": base_url,
        "plugin_file": PLUGIN_FILE,
        "expected_version": str(args.expected_version),
        "source_post_id": SOURCE_POST_ID,
        "page_slug": PAGE_SLUG,
        "page_title": PAGE_TITLE,
        "project_display_name": PROJECT_DISPLAY_NAME,
    }
    if einstein_request is not None:
        target_contract = {
            "site": base_url,
            "plugin_file": PLUGIN_FILE,
            "expected_version": str(args.expected_version),
            "canonical_public_post_id": EINSTEIN_CANONICAL_POST_ID,
            "page_slug": EINSTEIN_STAGE_SLUG,
            "project_contract_id": EINSTEIN_PROJECT_CONTRACT_ID,
            "mode": "exact_private_einstein_stage",
        }
    result: dict[str, Any] = {
        "schema_version": 1,
        "run_id": run_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "target": target_contract,
        "artifact": artifact_evidence,
        "helper": {"name": helper_name, "route": route},
        "checks": {},
    }

    def call_helper(action: str, *, extra: dict[str, Any] | None = None, timeout: int = 120) -> tuple[requests.Response, dict[str, Any]]:
        body: dict[str, Any] = {
            "token": token,
            "helper_sha256": helper_hash,
            "action": action,
        }
        if extra:
            if {"token", "helper_sha256", "action"}.intersection(extra):
                raise RuntimeError("Helper call extras attempted to replace a protected field")
            body.update(extra)
        response = client.request("POST", route, json_body=body, timeout=timeout)
        return response, response_payload(response)

    def rollback_response_is_exact(payload: dict[str, Any]) -> bool:
        plugin = payload.get("plugin") if isinstance(payload.get("plugin"), dict) else {}
        before = payload.get("before") if isinstance(payload.get("before"), dict) else {}
        inventory = (
            plugin.get("inventory") if isinstance(plugin.get("inventory"), dict) else {}
        )
        return bool(before_plugin_contract) and (
            payload.get("rolled_back") is True
            and payload.get("upload_temp_absent") is True
            and plugin.get("plugin_file") == PLUGIN_FILE
            and str(plugin.get("version") or "")
            == str(before_plugin_contract.get("version") or "")
            and plugin.get("active") is before_plugin_contract.get("active")
            and str(before.get("version") or "")
            == str(before_plugin_contract.get("version") or "")
            and before.get("active") is before_plugin_contract.get("active")
            and bool(payload.get("rollback_digest"))
            and secrets.compare_digest(
                str(payload.get("rollback_digest") or ""),
                str(inventory.get("digest") or ""),
            )
        )

    def upload_local_artifact() -> dict[str, Any]:
        if local_artifact_path is None or artifact_proof is None:
            raise RuntimeError("Canonical local artifact proof is unavailable")
        archive_bytes = int(artifact_proof["archive_bytes"])
        entry_count = int(artifact_proof["entry_count"])
        uncompressed_bytes = int(artifact_proof["uncompressed_bytes"])
        total_chunks = (archive_bytes + UPLOAD_CHUNK_BYTES - 1) // UPLOAD_CHUNK_BYTES
        if total_chunks < 1 or total_chunks > MAX_UPLOAD_CHUNKS:
            raise RuntimeError("Local artifact requires an unsafe number of upload chunks")
        contract: dict[str, Any] = {
            "expected_bytes": archive_bytes,
            "expected_sha256": artifact_sha256,
            "expected_entry_count": entry_count,
            "expected_uncompressed_bytes": uncompressed_bytes,
            "total_chunks": total_chunks,
        }

        def initialize() -> dict[str, Any]:
            response, payload = call_helper("upload_init", extra=contract, timeout=120)
            require_response(response, "Run-scoped artifact upload initialization")
            next_index = int(payload.get("next_index") if payload.get("next_index") is not None else -1)
            received_bytes = int(
                payload.get("received_bytes") if payload.get("received_bytes") is not None else -1
            )
            expected_received = min(archive_bytes, max(next_index, 0) * UPLOAD_CHUNK_BYTES)
            if not (
                0 <= next_index <= total_chunks
                and received_bytes == expected_received
                and int(payload.get("total_chunks") or 0) == total_chunks
                and int(payload.get("chunk_bytes_max") or 0) == UPLOAD_CHUNK_BYTES
                and int(payload.get("expected_bytes") or 0) == archive_bytes
                and (payload.get("verified") is not True or next_index == total_chunks)
            ):
                raise RuntimeError("Upload initialization returned inconsistent resume counters")
            return payload

        initialized = initialize()
        next_index = int(initialized["next_index"])
        recovery_count = 0
        accepted_responses = 0
        with local_artifact_path.open("rb") as stream:
            while next_index < total_chunks:
                expected_offset = next_index * UPLOAD_CHUNK_BYTES
                expected_chunk_bytes = min(UPLOAD_CHUNK_BYTES, archive_bytes - expected_offset)
                stream.seek(expected_offset)
                chunk = stream.read(expected_chunk_bytes)
                if len(chunk) != expected_chunk_bytes:
                    raise RuntimeError("Canonical local artifact changed during chunk upload")
                chunk_sha256 = hashlib.sha256(chunk).hexdigest()
                try:
                    response, payload = call_helper(
                        "upload_chunk",
                        extra={
                            "index": next_index,
                            "chunk_b64": base64.b64encode(chunk).decode("ascii"),
                        },
                        timeout=120,
                    )
                    require_response(response, "Sequential artifact upload chunk")
                    expected_next = next_index + 1
                    expected_received = min(archive_bytes, expected_next * UPLOAD_CHUNK_BYTES)
                    if not (
                        int(payload.get("accepted_index") if payload.get("accepted_index") is not None else -1)
                        == next_index
                        and int(payload.get("chunk_bytes") or 0) == expected_chunk_bytes
                        and secrets.compare_digest(str(payload.get("chunk_sha256") or ""), chunk_sha256)
                        and int(payload.get("next_index") or 0) == expected_next
                        and int(payload.get("received_bytes") or 0) == expected_received
                        and int(payload.get("total_chunks") or 0) == total_chunks
                    ):
                        raise RuntimeError("Upload chunk acknowledgement contract is inconsistent")
                    next_index = expected_next
                    accepted_responses += 1
                except Exception:
                    recovery_count += 1
                    if recovery_count > 3:
                        raise RuntimeError("Chunk upload exceeded its bounded resume budget")
                    resumed = initialize()
                    next_index = int(resumed["next_index"])

        finish_error: Exception | None = None
        finish_payload: dict[str, Any] = {}
        for _attempt in range(2):
            try:
                response, finish_payload = call_helper("upload_finish", timeout=180)
                require_response(response, "Uploaded artifact verification")
                if not (
                    finish_payload.get("verified") is True
                    and secrets.compare_digest(
                        str(finish_payload.get("sha256") or ""), artifact_sha256
                    )
                    and int(finish_payload.get("archive_bytes") or 0) == archive_bytes
                    and int(finish_payload.get("entry_count") or 0) == entry_count
                    and int(finish_payload.get("uncompressed_bytes") or 0)
                    == uncompressed_bytes
                    and int(finish_payload.get("total_chunks") or 0) == total_chunks
                ):
                    raise RuntimeError("Uploaded artifact verification contract is incomplete")
                finish_error = None
                break
            except Exception as error:
                finish_error = error
        if finish_error is not None:
            raise RuntimeError("Uploaded artifact verification failed after bounded retry") from finish_error
        return {
            "sha256": artifact_sha256,
            "archive_bytes": archive_bytes,
            "entry_count": entry_count,
            "uncompressed_bytes": uncompressed_bytes,
            "chunk_bytes_max": UPLOAD_CHUNK_BYTES,
            "chunk_count": total_chunks,
            "acknowledged_chunks": accepted_responses,
            "resume_count": recovery_count,
            "server_verified": True,
        }

    def finalize_release_resources(timeout: int = 180) -> tuple[requests.Response, dict[str, Any], int]:
        """Finish server resources while the authenticated helper remains retryable."""
        last_error: Exception | None = None
        for attempt in range(1, 3):
            try:
                response, payload = call_helper("finalize", timeout=timeout)
                require_response(response, "Release resource finalization")
                contract_valid = (
                    helper_id is not None
                    and payload.get("resource_cleanup_complete") is True
                    and payload.get("backup_deleted") is True
                    and payload.get("lock_released") is True
                    and payload.get("state_deleted") is True
                    and payload.get("upload_temp_absent") is True
                    and payload.get("helper_retained") is True
                    and payload.get("helper_cleanup_pending") is True
                    and int(payload.get("helper_id") or 0) == helper_id
                )
                if not contract_valid:
                    raise RuntimeError("Resource finalization returned an incomplete two-phase contract")
                return response, payload, attempt
            except Exception as error:
                last_error = error
        raise RuntimeError("Release resource finalization failed after bounded retry") from last_error

    try:
        if artifact_mode == "url":
            with tempfile.TemporaryDirectory(prefix="nadlan-unit-journey-artifact-") as temp_dir:
                downloaded_artifact = Path(temp_dir) / "nadlan-config.zip"
                artifact_proof = download_and_validate_artifact(
                    str(args.artifact_url), artifact_sha256, downloaded_artifact
                )
        if artifact_proof is None:
            raise RuntimeError("Artifact validation proof is unavailable")
        artifact_counts = {
            "sha256": str(artifact_proof["sha256"]),
            "archive_bytes": int(artifact_proof["archive_bytes"]),
            "entry_count": int(artifact_proof["entry_count"]),
            "uncompressed_bytes": int(artifact_proof["uncompressed_bytes"]),
            "crc_valid": artifact_proof.get("crc_valid") is True,
        }
        result["checks"]["local_artifact"] = artifact_counts
        result["artifact"].update(
            {
                "archive_bytes": artifact_counts["archive_bytes"],
                "entry_count": artifact_counts["entry_count"],
                "uncompressed_bytes": artifact_counts["uncompressed_bytes"],
            }
        )

        me_response = client.request("GET", "wp/v2/users/me", timeout=60)
        me = require_response(me_response, "WordPress authentication preflight")
        user_id = int(me.get("id") or 0)
        if user_id < 1:
            raise RuntimeError("WordPress authentication preflight returned no user ID")
        snippets_before = client.all_snippets()
        if any(str(row.get("name") or "") == helper_name for row in snippets_before):
            raise RuntimeError("Unique release helper name already exists")
        result["checks"]["auth_preflight"] = {
            "authenticated": True,
            "user_id": user_id,
            "code_snippets_collection_readable": True,
            "snippet_count_before": len(snippets_before),
        }
        if einstein_request is not None:
            public_record_before_deploy = wordpress_post_snapshot(
                get_authenticated_post(client, EINSTEIN_CANONICAL_POST_ID)
            )
            einstein_public_predeploy_sha256 = sha256_bytes(
                exact_json_bytes(public_record_before_deploy)
            )
            result["checks"]["canonical_public_predeploy"] = {
                "post_id": EINSTEIN_CANONICAL_POST_ID,
                "snapshot_sha256": einstein_public_predeploy_sha256,
            }

        public_preflight = public.get(
            f"{base_url}/wp-json/nadlan/v1/healthcheck",
            params={"cb": f"{run_id}-preflight"},
            timeout=30,
        )
        try:
            public_preflight_payload: Any = public_preflight.json()
        except ValueError:
            public_preflight_payload = {}
        public_preflight_version = find_health_version(public_preflight_payload)
        result["checks"]["public_health_preflight"] = {
            "http_status": public_preflight.status_code,
            "version": public_preflight_version,
            "reachable": public_preflight.status_code == 200 and bool(public_preflight_version),
        }
        if result["checks"]["public_health_preflight"]["reachable"] is not True:
            raise RuntimeError("Public health recovery preflight is not reachable")

        helper_creation_attempted = True
        create_response = client.request(
            "POST",
            "code-snippets/v1/snippets",
            json_body={
                "name": helper_name,
                "code": f"/* inactive placeholder for {helper_name} */",
                "scope": "global",
                "active": False,
            },
            timeout=60,
        )
        created = require_response(create_response, "Inactive helper creation")
        helper_id = int(created.get("id") or 0)
        if helper_id < 1:
            raise RuntimeError("Inactive helper creation returned no ID")
        result["helper"]["id"] = helper_id

        helper_code = render_helper(
            route_path=route_path,
            token=token,
            run_id=run_id,
            helper_id=helper_id,
            helper_name=helper_name,
            artifact_mode=artifact_mode,
            artifact_url=str(args.artifact_url or ""),
            artifact_sha256=artifact_sha256,
            artifact_bytes=int(artifact_proof["archive_bytes"]),
            artifact_entry_count=int(artifact_proof["entry_count"]),
            artifact_uncompressed_bytes=int(artifact_proof["uncompressed_bytes"]),
            expected_version=str(args.expected_version),
        )
        helper_hash = sha256_text(helper_code)
        result["helper"]["code_sha256"] = helper_hash
        update_response = client.request(
            "PUT",
            f"code-snippets/v1/snippets/{helper_id}",
            json_body={
                "name": helper_name,
                "code": helper_code,
                "scope": "global",
                "active": False,
            },
            timeout=60,
        )
        require_response(update_response, "Inactive helper update")
        inactive_response = client.request("GET", f"code-snippets/v1/snippets/{helper_id}", timeout=60)
        inactive = require_response(inactive_response, "Inactive helper verification")
        inactive_observed = observed_snippet(inactive)
        inactive_expected = {
            "id": helper_id,
            "name": helper_name,
            "active": False,
            "scope": "global",
            "code_sha256": helper_hash,
        }
        if inactive_observed != inactive_expected:
            raise RuntimeError("Inactive helper identity, state, or code hash changed")
        result["checks"]["inactive_helper"] = inactive_observed

        activate_response = client.request(
            "PUT",
            f"code-snippets/v1/snippets/{helper_id}/activate",
            json_body={},
            timeout=60,
        )
        require_response(activate_response, "Helper activation")
        active_response = client.request("GET", f"code-snippets/v1/snippets/{helper_id}", timeout=60)
        active = require_response(active_response, "Active helper verification")
        active_observed = observed_snippet(active)
        active_expected = dict(inactive_expected)
        active_expected["active"] = True
        if active_observed != active_expected:
            raise RuntimeError("Active helper identity, state, or code hash changed")
        result["checks"]["active_helper"] = active_observed

        inspect_response, inspect = call_helper("inspect")
        require_response(inspect_response, "Live plugin inspection")
        plugin_before = inspect.get("plugin") if isinstance(inspect.get("plugin"), dict) else {}
        if plugin_before.get("plugin_file") != PLUGIN_FILE or plugin_before.get("active") is not True:
            raise RuntimeError("Live inspection did not confirm exact active nadlan-config plugin")
        before_plugin_contract = {
            "version": str(plugin_before.get("version") or ""),
            "active": plugin_before.get("active"),
        }
        if not before_plugin_contract["version"]:
            raise RuntimeError("Live inspection did not provide the pre-deployment plugin version")
        inspected_artifact = inspect.get("artifact")
        if not (
            isinstance(inspected_artifact, dict)
            and inspected_artifact.get("mode") == artifact_mode
            and secrets.compare_digest(
                str(inspected_artifact.get("sha256") or ""), artifact_sha256
            )
            and int(inspected_artifact.get("archive_bytes") or 0)
            == int(artifact_proof["archive_bytes"])
            and int(inspected_artifact.get("entry_count") or 0)
            == int(artifact_proof["entry_count"])
            and int(inspected_artifact.get("uncompressed_bytes") or 0)
            == int(artifact_proof["uncompressed_bytes"])
            and inspect.get("upload_temp_absent") is True
        ):
            raise RuntimeError("Live helper inspection did not confirm the exact artifact contract")
        result["checks"]["live_before"] = inspect

        preflight_response, preflight = call_helper("deploy_preflight", timeout=120)
        require_response(preflight_response, "Read-only deployment preflight")
        preflight_proof = deploy_preflight_proof(
            preflight,
            before_version=str(before_plugin_contract["version"]),
            artifact_bytes=int(artifact_proof["archive_bytes"]),
            artifact_uncompressed_bytes=int(artifact_proof["uncompressed_bytes"]),
        )
        result["checks"]["deploy_preflight"] = preflight_proof
        if preflight_proof["passed"] is not True:
            raise RuntimeError("Read-only deployment preflight did not pass")

        if artifact_mode == "upload":
            release_resources_may_exist = True
            result["checks"]["artifact_upload"] = upload_local_artifact()
            upload_status_response, upload_status = call_helper("status", timeout=60)
            require_response(upload_status_response, "Verified upload status")
            upload_state = upload_status.get("upload")
            if not (
                upload_status.get("state_phase") == "upload_verified"
                and isinstance(upload_state, dict)
                and upload_state.get("verified") is True
                and upload_state.get("temp_exists") is True
                and upload_state.get("temp_safe") is True
                and int(upload_state.get("temp_bytes") or 0)
                == int(artifact_proof["archive_bytes"])
                and int(upload_state.get("next_index") or 0)
                == int(upload_state.get("total_chunks") or -1)
            ):
                raise RuntimeError("Server status did not confirm the exact verified upload")
            result["checks"]["verified_upload_status"] = {
                "state_phase": upload_status.get("state_phase"),
                "verified": True,
                "temp_exists": True,
                "temp_safe": True,
                "temp_bytes": int(upload_state["temp_bytes"]),
                "next_index": int(upload_state.get("next_index") or 0),
                "total_chunks": int(upload_state.get("total_chunks") or 0),
            }

        release_resources_may_exist = True
        deploy_started = True
        deploy_response, deploy = call_helper("deploy", timeout=360)
        if not 200 <= deploy_response.status_code < 300:
            deploy_failure = deploy_failure_proof(
                deploy_response, deploy
            )
            result["checks"]["deploy_failure"] = deploy_failure
            deploy_failure_recovery_blocked = (
                deploy_failure.get("contract_valid") is not True
                or deploy_failure.get("rollback_outcome") == "failed"
                or (
                    deploy_failure.get("failure_stage")
                    in DEPLOY_FAILURE_REQUIRES_ROLLBACK_STAGES
                    and deploy_failure.get("rollback_outcome") != "succeeded"
                )
            )
        require_response(deploy_response, "Guarded plugin deployment")
        deployed = True
        plugin_after = deploy.get("plugin") if isinstance(deploy.get("plugin"), dict) else {}
        if plugin_after.get("version") != str(args.expected_version) or plugin_after.get("active") is not True:
            raise RuntimeError("Deployment response did not confirm expected active plugin version")
        if deploy.get("backup_ready") is not True:
            raise RuntimeError("Deployment response did not confirm scoped rollback backup")
        if (
            deploy.get("artifact_mode") != artifact_mode
            or not secrets.compare_digest(str(deploy.get("artifact_sha256") or ""), artifact_sha256)
            or deploy.get("upload_temp_absent") is not True
        ):
            raise RuntimeError("Deployment response did not confirm artifact identity and temp cleanup")
        if deploy.get("idempotent") is not True:
            deployed_zip = deploy.get("zip")
            if not (
                isinstance(deployed_zip, dict)
                and int(deployed_zip.get("archive_bytes") or 0)
                == int(artifact_proof["archive_bytes"])
                and int(deployed_zip.get("entry_count") or 0)
                == int(artifact_proof["entry_count"])
                and int(deployed_zip.get("uncompressed_bytes") or 0)
                == int(artifact_proof["uncompressed_bytes"])
            ):
                raise RuntimeError("Deployment response did not confirm the exact ZIP contract")
            if not isinstance(deploy.get("disk"), dict) or deploy["disk"].get("sufficient") is not True:
                raise RuntimeError("Deployment response did not confirm sufficient release disk space")
            if (
                not isinstance(deploy.get("cache"), dict)
                or deploy["cache"].get("object_cache_flushed") is not True
                or deploy["cache"].get("litespeed_purge_requested") is not True
            ):
                raise RuntimeError("Deployment response did not confirm cache purge request")
        result["checks"]["deploy"] = deploy

        health_checks: list[dict[str, Any]] = []
        stable = False
        consecutive_stable = 0
        required_stable = 2 if einstein_request is not None else 1
        deployed_digest = str(
            (plugin_after.get("inventory") or {}).get("digest") or ""
        ) if isinstance(plugin_after.get("inventory"), dict) else ""
        for attempt in range(1, args.health_attempts + 1):
            status_response, status = call_helper("status", timeout=60)
            status_version = ""
            status_digest = ""
            upload_temp_absent = False
            if status_response.status_code == 200 and isinstance(status.get("plugin"), dict):
                status_version = str(status["plugin"].get("version") or "")
                status_inventory = status["plugin"].get("inventory")
                status_digest = str(status_inventory.get("digest") or "") if isinstance(
                    status_inventory, dict
                ) else ""
                status_upload = status.get("upload")
                upload_temp_absent = (
                    isinstance(status_upload, dict)
                    and status_upload.get("temp_absent") is True
                    and status_upload.get("temp_safe") is True
                )
            health_url = f"{base_url}/wp-json/nadlan/v1/healthcheck"
            try:
                health_response = public.get(
                    health_url,
                    params={"cb": f"{run_id}-{attempt}"},
                    timeout=30,
                )
                health_payload: Any = health_response.json() if health_response.status_code == 200 else {}
                health_version = find_health_version(health_payload)
                health_status = health_response.status_code
            except (requests.RequestException, ValueError):
                health_version = ""
                health_status = 0
            attempt_result = {
                "attempt": attempt,
                "helper_status": status_response.status_code,
                "helper_version": status_version,
                "plugin_digest_exact": bool(deployed_digest)
                and secrets.compare_digest(status_digest, deployed_digest),
                "upload_temp_absent": upload_temp_absent,
                "health_status": health_status,
                "health_version": health_version,
                "expected": status_version == str(args.expected_version)
                and bool(deployed_digest)
                and secrets.compare_digest(status_digest, deployed_digest)
                and upload_temp_absent
                and health_status == 200
                and health_version == str(args.expected_version),
            }
            health_checks.append(attempt_result)
            if attempt_result["expected"]:
                consecutive_stable += 1
                if consecutive_stable >= required_stable:
                    stable = True
                    break
            else:
                consecutive_stable = 0
            if attempt < args.health_attempts and args.health_delay_seconds:
                time.sleep(args.health_delay_seconds)
        result["checks"]["stabilization"] = health_checks
        if not stable:
            rollback_response, rollback = call_helper("rollback", timeout=240)
            result["checks"]["automatic_rollback"] = rollback
            deployed = False
            require_response(rollback_response, "Automatic stabilization rollback")
            if not rollback_response_is_exact(rollback):
                raise RuntimeError("Automatic rollback did not prove exact pre-deployment plugin state")
            raise RuntimeError("Expected plugin version did not stabilize; exact backup was restored")

        if einstein_request is not None:
            canonical_after_deploy = wordpress_post_snapshot(
                get_authenticated_post(client, EINSTEIN_CANONICAL_POST_ID)
            )
            canonical_after_deploy_sha256 = sha256_bytes(
                exact_json_bytes(canonical_after_deploy)
            )
            if not secrets.compare_digest(
                canonical_after_deploy_sha256, einstein_public_predeploy_sha256
            ):
                raise RuntimeError("Plugin deployment changed canonical public post 4867")
            result["checks"]["canonical_public_postdeploy"] = {
                "post_id": EINSTEIN_CANONICAL_POST_ID,
                "unchanged": True,
                "snapshot_sha256": canonical_after_deploy_sha256,
            }
            einstein_transaction = write_einstein_stage(client, einstein_request, post_password)
            page_url = str(einstein_transaction["page_url"])
            result["checks"]["private_page"] = {
                "post_id": int(einstein_transaction["post_id"]),
                "page_url": page_url,
                "created_new": einstein_transaction["created_new"] is True,
                "readback": einstein_transaction["readback"],
                "canonical_public_4867_unchanged": True,
                "canonical_public_sha256": einstein_transaction[
                    "canonical_public_sha256"
                ],
            }
            result["checks"]["anonymous_private_surfaces"] = anonymous_einstein_probes(
                base_url,
                page_url,
                int(einstein_transaction["post_id"]),
                einstein_request,
                post_password,
            )
        else:
            page_response, page = call_helper(
                "create_page",
                extra={"post_password": post_password},
                timeout=180,
            )
            require_response(page_response, "Private sandbox creation")
            page_url = str(page.get("page_url") or "")
            if (
                not page_url.startswith(base_url + "/")
                or page.get("password_protected") is not True
                or page.get("noindex") is not True
                or page.get("nofollow") is not True
                or not isinstance(page.get("cache"), dict)
                or page["cache"].get("litespeed_purge_requested") is not True
            ):
                raise RuntimeError("Private sandbox response did not prove scoped protection")
            result["checks"]["private_page"] = page

            protected_response = public.get(
                page_url,
                params={"cb": run_id},
                timeout=60,
                allow_redirects=True,
            )
            protected_html = protected_response.text
            robots_header = protected_response.headers.get("X-Robots-Tag", "")
            password_form = "post_password" in protected_html and (
                "action=postpass" in protected_html or "wp-pass.php" in protected_html
            )
            payload_hidden = "NADLAN_SHOWROOM" not in protected_html and "nl-showroom" not in protected_html
            password_absent = post_password not in protected_html
            noindex_header = "noindex" in robots_header.lower()
            nofollow_header = "nofollow" in robots_header.lower()
            noarchive_header = "noarchive" in robots_header.lower()
            if not (
                protected_response.status_code == 200
                and password_form
                and payload_hidden
                and password_absent
                and noindex_header
                and nofollow_header
                and noarchive_header
            ):
                raise RuntimeError("Unauthenticated private page protection proof failed")
            result["checks"]["unauthenticated_page"] = {
                "http_status": protected_response.status_code,
                "password_form": password_form,
                "showroom_payload_hidden": payload_hidden,
                "password_not_reflected": password_absent,
                "x_robots_tag": robots_header,
                "noindex_header": noindex_header,
                "nofollow_header": nofollow_header,
                "noarchive_header": noarchive_header,
            }

            rest_response = public.get(
                f"{base_url}/wp-json/wp/v2/nadlan_project",
                params={"slug": PAGE_SLUG},
                timeout=60,
            )
            rest_hidden = False
            rest_shape = "unavailable"
            if rest_response.status_code == 200:
                try:
                    rest_payload = rest_response.json()
                    rest_hidden = isinstance(rest_payload, list) and len(rest_payload) == 0
                    rest_shape = "empty_list" if rest_hidden else "non_empty"
                except ValueError:
                    rest_shape = "non_json"
            elif rest_response.status_code in (401, 403, 404):
                rest_hidden = True
                rest_shape = "not_public"
            result["checks"]["unauthenticated_rest"] = {
                "http_status": rest_response.status_code,
                "shape": rest_shape,
                "private_post_hidden": rest_hidden,
            }
            if not rest_hidden:
                raise RuntimeError("Private sandbox remains discoverable through unauthenticated REST")

        # Keep the server-side rollback copy and authenticated helper alive
        # through independent browser acceptance. Finalization happens only
        # after the real page, not merely the install response, passes.
        node = shutil.which("node")
        if not node:
            raise RuntimeError("Node.js is unavailable for the pre-finalize acceptance gate")
        acceptance_dir = args.output_dir.resolve() / run_id / "acceptance"
        acceptance_env = dict(os.environ)
        for secret_key in ("WP_APP_PASSWORD", "WP_USER", "WP_BASE_URL"):
            acceptance_env.pop(secret_key, None)
        acceptance_env.update(
            {
                "SANDBOX_URL": page_url,
                "SANDBOX_POST_PASSWORD": post_password,
                "OUTPUT_DIR": str(acceptance_dir),
                "EXPECTED_PLUGIN_VERSION": str(args.expected_version),
                "EXPECTED_PROJECT_CONTRACT_ID": (
                    EINSTEIN_PROJECT_CONTRACT_ID if einstein_request is not None else ""
                ),
                "EXPECTED_STAGE_POST_ID": (
                    str(einstein_transaction["post_id"])
                    if einstein_transaction is not None
                    else ""
                ),
            }
        )
        acceptance = subprocess.run(
            [node, str(acceptance_script)],
            cwd=str(REPO_ROOT),
            env=acceptance_env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=args.acceptance_timeout_seconds,
            check=False,
        )
        result["checks"]["acceptance_secret_scan"] = assert_tree_has_no_secret_bytes(
            acceptance_dir, (post_password, wp_password)
        )
        summary_path = acceptance_dir / "summary.json"
        summary_payload: dict[str, Any] = {}
        if summary_path.is_file():
            try:
                loaded_summary = json.loads(summary_path.read_text(encoding="utf-8"))
                if isinstance(loaded_summary, dict):
                    summary_payload = loaded_summary
            except (OSError, ValueError):
                summary_payload = {}
        summary_contract: dict[str, Any] = {}
        summary_contract_error = ""
        if summary_payload:
            try:
                summary_contract = acceptance_summary_proof(
                    summary_payload, einstein_mode=einstein_request is not None
                )
            except (RuntimeError, TypeError, ValueError) as contract_error:
                summary_contract_error = str(contract_error)
        result["checks"]["browser_acceptance"] = {
            "exit_code": acceptance.returncode,
            "summary_json": str(summary_path),
            "summary_markdown": str(acceptance_dir / "summary.md"),
            "report_contract": summary_contract,
            "report_contract_error": summary_contract_error,
            "stdout_tail": redactor.text(acceptance.stdout[-1200:]),
            "stderr_tail": redactor.text(acceptance.stderr[-1200:]),
        }
        if acceptance.returncode != 0 or not summary_payload or not summary_contract:
            raise RuntimeError("Pre-finalize browser acceptance failed; release will roll back")

        if einstein_request is not None:
            if einstein_transaction is None:
                raise RuntimeError("Einstein stage transaction disappeared before final readback")
            final_stage_record = get_authenticated_post(
                client, int(einstein_transaction["post_id"])
            )
            result["checks"]["final_stage_readback"] = assert_einstein_stage_readback(
                final_stage_record, einstein_request, post_password
            )
            final_public_snapshot = wordpress_post_snapshot(
                get_authenticated_post(client, EINSTEIN_CANONICAL_POST_ID)
            )
            final_public_hash = sha256_bytes(exact_json_bytes(final_public_snapshot))
            if not secrets.compare_digest(
                final_public_hash, str(einstein_transaction["canonical_public_sha256"])
            ):
                raise RuntimeError("Canonical public post 4867 changed before finalization")
            result["checks"]["final_public_post_immutability"] = {
                "post_id": EINSTEIN_CANONICAL_POST_ID,
                "unchanged": True,
                "snapshot_sha256": final_public_hash,
            }
            result["checks"]["final_anonymous_private_surfaces"] = anonymous_einstein_probes(
                base_url,
                page_url,
                int(einstein_transaction["post_id"]),
                einstein_request,
                post_password,
            )

        final_health = public.get(
            f"{base_url}/wp-json/nadlan/v1/healthcheck",
            params={"cb": f"{run_id}-final"},
            timeout=30,
        )
        final_version = find_health_version(final_health.json()) if final_health.status_code == 200 else ""
        result["checks"]["final_health"] = {
            "http_status": final_health.status_code,
            "version": final_version,
            "expected": final_health.status_code == 200 and final_version == str(args.expected_version),
        }
        if result["checks"]["final_health"]["expected"] is not True:
            raise RuntimeError("Final public healthcheck does not report expected plugin version")

        finalize_response, finalize, finalize_attempts = finalize_release_resources()
        resources_finalized = True
        result["checks"]["finalize"] = {
            **finalize,
            "http_status": finalize_response.status_code,
            "driver_attempts": finalize_attempts,
        }

        result["passed"] = True
        result["page_url"] = page_url
    except Exception as error:
        result["passed"] = False
        result["error"] = redactor.text(error)
        if isinstance(error, EinsteinStageRecoveryBlocked):
            stage_rollback_blocked = True
            result["checks"]["failure_stage_rollback"] = {
                "confirmed": False,
                "recovery_preserved": True,
                "reason": "indeterminate_stage_write",
            }
        if einstein_transaction is not None:
            try:
                result["checks"]["failure_stage_rollback"] = rollback_einstein_stage(
                    client, einstein_transaction
                )
                einstein_transaction = None
            except Exception as stage_rollback_error:
                stage_rollback_blocked = True
                result["checks"]["failure_stage_rollback"] = {
                    "confirmed": False,
                    "recovery_preserved": True,
                    "error": redactor.text(stage_rollback_error),
                }
        status_confirmed = False
        state_phase = "unknown"
        backup_ready = False
        if not resources_finalized and helper_id is not None and helper_hash:
            try:
                status_response, failure_status = call_helper("status", timeout=60)
                if status_response.status_code == 200:
                    status_confirmed = True
                    state_phase = str(failure_status.get("state_phase") or "none")
                    backup_ready = failure_status.get("backup_ready") is True
                failure_upload = (
                    failure_status.get("upload")
                    if isinstance(failure_status.get("upload"), dict)
                    else {}
                )
                result["checks"]["failure_status"] = {
                    "http_status": status_response.status_code,
                    "state_phase": state_phase,
                    "backup_ready": backup_ready,
                    "upload_temp_absent": failure_upload.get("temp_absent") is True,
                    "upload_temp_safe": failure_upload.get("temp_safe") is True,
                    "upload_temp_bytes": int(failure_upload.get("temp_bytes") or 0),
                }
            except Exception as status_error:
                result["checks"]["failure_status"] = {
                    "http_status": 0,
                    "state_phase": "unknown",
                    "backup_ready": False,
                    "error": redactor.text(status_error),
                }

            rollback_required = deployed or backup_ready or state_phase in {
                "backup_ready",
                "deployed",
                "page_creating",
                "page_ready",
                "rolled_back",
            }
            rollback_confirmed = False
            if rollback_required and not stage_rollback_blocked:
                try:
                    rollback_response, rollback = call_helper("rollback", timeout=240)
                    rollback_confirmed = (
                        rollback_response.status_code == 200
                        and rollback_response_is_exact(rollback)
                    )
                    result["checks"]["failure_rollback"] = {
                        "http_status": rollback_response.status_code,
                        "confirmed": rollback_confirmed,
                        "version": str(
                            (rollback.get("plugin") or {}).get("version") or ""
                        )
                        if isinstance(rollback.get("plugin"), dict)
                        else "",
                        "active": (rollback.get("plugin") or {}).get("active")
                        if isinstance(rollback.get("plugin"), dict)
                        else None,
                    }
                    if rollback_confirmed:
                        deployed = False
                        deploy_failure_recovery_blocked = False
                except Exception as rollback_error:
                    result["checks"]["failure_rollback"] = {
                        "confirmed": False,
                        "error": redactor.text(rollback_error),
                    }

            # Never discard a possibly required rollback backup when deployment
            # state cannot be established. Activation failures occur before
            # deploy_started and are safe to finalize without release state.
            safe_to_finalize = (
                not stage_rollback_blocked
                and not deploy_failure_recovery_blocked
                and (
                    not deploy_started
                    or (status_confirmed and not rollback_required)
                    or rollback_confirmed
                )
            )
            if safe_to_finalize:
                try:
                    cleanup_response, cleanup, cleanup_attempts = finalize_release_resources()
                    result["checks"]["failure_finalize"] = {
                        "http_status": cleanup_response.status_code,
                        "resource_cleanup_complete": cleanup.get("resource_cleanup_complete") is True,
                        "backup_deleted": cleanup.get("backup_deleted") is True,
                        "lock_released": cleanup.get("lock_released") is True,
                        "state_deleted": cleanup.get("state_deleted") is True,
                        "upload_temp_absent": cleanup.get("upload_temp_absent") is True,
                        "helper_retained_for_phase_two": cleanup.get("helper_retained") is True,
                        "driver_attempts": cleanup_attempts,
                    }
                    resources_finalized = True
                except Exception as cleanup_error:
                    result["checks"]["failure_finalize"] = {
                        "resource_cleanup_complete": False,
                        "error": redactor.text(cleanup_error),
                    }
            else:
                result["checks"]["failure_finalize"] = {
                    "resource_cleanup_complete": False,
                    "skipped_to_preserve_recovery": True,
                    "deploy_failure_recovery_blocked": (
                        deploy_failure_recovery_blocked
                    ),
                }
    finally:
        retain_recovery_helper = deploy_started and not resources_finalized
        if (helper_creation_attempted or helper_id is not None) and not retain_recovery_helper:
            cleanup_failure: Exception | None = None
            cleanup_proof: dict[str, Any] | None = None
            for _cleanup_attempt in range(2):
                try:
                    cleanup_proof = independently_remove_snippet(
                        client,
                        target_id=helper_id,
                        target_name=helper_name,
                        expected_hash=helper_hash
                        or sha256_text(f"/* inactive placeholder for {helper_name} */"),
                        release_run_id=run_id,
                        release_token=token,
                        artifact_mode=artifact_mode,
                        artifact_sha256=artifact_sha256,
                        artifact_bytes=int(artifact_proof["archive_bytes"]),
                        artifact_entry_count=int(artifact_proof["entry_count"]),
                        artifact_uncompressed_bytes=int(
                            artifact_proof["uncompressed_bytes"]
                        ),
                        resources_known_absent=(
                            resources_finalized or not release_resources_may_exist
                        ),
                        created_cleanup_rows=created_cleanup_rows,
                    )
                    if cleanup_proof.get("target_absent") is True:
                        cleanup_failure = None
                        break
                except Exception as cleanup_error:
                    cleanup_failure = cleanup_error

            # Every secondary cleanup bridge is part of the same privileged
            # lifecycle. Sweep the exact IDs we created and prove each absent.
            cursor = 0
            while cursor < len(created_cleanup_rows) and cursor < 12:
                cleanup_row = created_cleanup_rows[cursor]
                cursor += 1
                try:
                    cleanup_get = client.request(
                        "GET",
                        f"code-snippets/v1/snippets/{int(cleanup_row['id'])}",
                        timeout=60,
                    )
                except Exception as cleanup_error:
                    cleanup_failure = cleanup_error
                    continue
                # A missing item response only skips another delete attempt;
                # collection and route absence are still proved below.
                if is_exact_missing_snippet_response(cleanup_get):
                    continue
                try:
                    independently_remove_snippet(
                        client,
                        target_id=int(cleanup_row["id"]),
                        target_name=str(cleanup_row["name"]),
                        expected_hash=str(cleanup_row["code_sha256"]),
                        release_run_id=run_id,
                        release_token=token,
                        artifact_mode=artifact_mode,
                        artifact_sha256=artifact_sha256,
                        artifact_bytes=int(artifact_proof["archive_bytes"]),
                        artifact_entry_count=int(artifact_proof["entry_count"]),
                        artifact_uncompressed_bytes=int(
                            artifact_proof["uncompressed_bytes"]
                        ),
                        manage_release_resources=False,
                        depth=1,
                        created_cleanup_rows=created_cleanup_rows,
                    )
                except Exception as cleanup_error:
                    cleanup_failure = cleanup_error
            residual_cleanup_rows = []
            secondary_route_statuses: dict[int, int] = {}
            secondary_get_responses: dict[int, requests.Response] = {}
            helper_absent = False
            helper_get_status = 0
            helper_get_missing_exact = False
            route_after_status = 0
            snippet_count_after: int | None = None
            try:
                if len(created_cleanup_rows) > 12:
                    raise RuntimeError("Secondary cleanup helper bound was exceeded")
                for cleanup_row in created_cleanup_rows:
                    cleanup_id_value = int(cleanup_row["id"])
                    cleanup_get = client.request(
                        "GET",
                        f"code-snippets/v1/snippets/{cleanup_id_value}",
                        timeout=60,
                    )
                    secondary_get_responses[cleanup_id_value] = cleanup_get
                    cleanup_route = str(cleanup_row.get("route") or "")
                    if not cleanup_route.startswith(f"{ROUTE_NAMESPACE}/cleanup-"):
                        raise RuntimeError("Secondary cleanup helper route is invalid")
                    cleanup_route_after = client.request(
                        "POST", cleanup_route, json_body={}, timeout=60
                    )
                    secondary_route_statuses[cleanup_id_value] = (
                        cleanup_route_after.status_code
                    )
                if helper_id is None:
                    helper_get_status = int(
                        (cleanup_proof or {}).get("target_get_status") or 0
                    )
                else:
                    helper_get_after = client.request(
                        "GET", f"code-snippets/v1/snippets/{helper_id}", timeout=60
                    )
                    helper_get_status = helper_get_after.status_code
                    helper_get_missing_exact = is_exact_missing_snippet_response(
                        helper_get_after
                    )
                route_after = client.request(
                    "POST", route, json_body={"action": "inspect"}, timeout=60
                )
                route_after_status = route_after.status_code

                # One final collection snapshot is authoritative for the main
                # helper and every secondary bridge after all item/route probes.
                snippets_after = client.all_snippets()
                snippet_count_after = len(snippets_after)
                helper_absent = snippet_absent_from_collection(
                    snippets_after,
                    snippet_id=helper_id or 0,
                    snippet_name=helper_name,
                )
                if helper_id is None:
                    helper_get_missing_exact = helper_absent
                for cleanup_row in created_cleanup_rows:
                    cleanup_id_value = int(cleanup_row["id"])
                    cleanup_get = secondary_get_responses.get(cleanup_id_value)
                    if cleanup_get is None or not snippet_absence_is_proved(
                        cleanup_get,
                        snippets_after,
                        snippet_id=cleanup_id_value,
                        snippet_name=str(cleanup_row["name"]),
                        route_status=secondary_route_statuses.get(
                            cleanup_id_value, 0
                        ),
                    ):
                        residual_cleanup_rows.append(cleanup_id_value)
            except Exception as cleanup_error:
                cleanup_failure = cleanup_error
            if residual_cleanup_rows:
                cleanup_failure = RuntimeError(
                    "Secondary cleanup helper absence could not be proved"
                )

            main_absence_proved = (
                helper_absent
                and helper_get_missing_exact
                and route_after_status == 404
                and cleanup_proof is not None
                and cleanup_proof.get("release_resource_cleanup_proved") is True
            )
            if not main_absence_proved:
                cleanup_failure = RuntimeError("Main helper row or route absence could not be proved")
            if cleanup_proof is not None:
                cleanup_proof["secondary_helpers_created"] = len(created_cleanup_rows)
                cleanup_proof["secondary_helpers_absent"] = not residual_cleanup_rows
                cleanup_proof["secondary_helper_route_statuses"] = (
                    secondary_route_statuses
                )
                cleanup_proof["main_helper_absent_from_collection"] = helper_absent
                cleanup_proof["main_helper_get_status"] = helper_get_status
                cleanup_proof["main_helper_get_missing_exact"] = (
                    helper_get_missing_exact
                )
                cleanup_proof["main_route_status"] = route_after_status
                cleanup_proof["snippet_count_after"] = snippet_count_after
                result["checks"]["independent_helper_cleanup"] = cleanup_proof
            if (
                cleanup_failure is not None
                or cleanup_proof is None
                or cleanup_proof.get("target_absent") is not True
                or not main_absence_proved
            ):
                result["passed"] = False
                result["checks"]["independent_helper_cleanup"] = {
                    "target_absent": False,
                    "main_helper_absent_from_collection": helper_absent,
                    "main_helper_get_status": helper_get_status,
                    "main_helper_get_missing_exact": helper_get_missing_exact,
                    "main_route_status": route_after_status,
                    "secondary_helpers_absent": not residual_cleanup_rows,
                    "release_resource_cleanup_proved": bool(
                        (cleanup_proof or {}).get("release_resource_cleanup_proved")
                    ),
                    "error": redactor.text(cleanup_failure or "Independent cleanup proof is unavailable"),
                }
        elif retain_recovery_helper:
            result["passed"] = False
            retained = False
            retained_active = False
            retained_hash = ""
            try:
                if helper_id is not None:
                    retained_response = client.request(
                        "GET", f"code-snippets/v1/snippets/{helper_id}", timeout=60
                    )
                    retained_row = require_response(
                        retained_response, "Recovery helper retention verification"
                    )
                    retained_observed = observed_snippet(retained_row)
                    retained_hash = retained_observed["code_sha256"]
                    retained_active = retained_observed["active"] is True
                    retained = (
                        retained_observed["id"] == helper_id
                        and retained_observed["name"] == helper_name
                        and retained_observed["scope"] == "global"
                        and retained_active
                        and bool(helper_hash)
                        and retained_hash == helper_hash
                    )
            except Exception as retention_error:
                result["checks"]["recovery_helper_retention_error"] = redactor.text(
                    retention_error
                )
            result["checks"]["independent_helper_cleanup"] = {
                "target_absent": False,
                "recovery_retained": retained,
                "helper_active": retained_active,
                "helper_code_sha256": retained_hash,
                "reason": "deployment_state_or_rollback_not_proved_safe",
            }
        else:
            result["checks"]["independent_helper_cleanup"] = {
                "target_absent": True,
                "release_resource_cleanup_proved": True,
                "method": "not_created",
            }

    sanitized = redactor.value(result)
    serialized = json.dumps(sanitized, ensure_ascii=False, indent=2) + "\n"
    redactor.assert_absent(serialized)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / f"{run_id}.json"
    output.write_text(serialized, encoding="utf-8")
    summary = {
        "output": str(output),
        "passed": bool(sanitized.get("passed")),
        "run_id": run_id,
        "page_url": page_url if sanitized.get("passed") else "",
        "helper_cleanup_proved": bool(
            sanitized.get("checks", {}).get("independent_helper_cleanup", {}).get("target_absent")
        ),
    }
    print(json.dumps(redactor.value(summary), ensure_ascii=False, indent=2))
    return 0 if sanitized.get("passed") else 3


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        raise
    except Exception as fatal:
        # This outer guard cannot know secret values if failure happened before
        # inputs were loaded, so keep the message deliberately generic.
        print(
            json.dumps(
                {"passed": False, "error": type(fatal).__name__, "message": "Release driver failed before evidence finalization."},
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        sys.exit(4)
