#!/usr/bin/env python3
"""One-shot, fail-closed continuation for retained Einstein run 4527b2.

This is intentionally not a general recovery mode.  Every mutable identity is
pinned to the retained 2026-08-14 run.  It patches only the known filtered
slug-identity block in Code Snippets row 450, continues post 6594 through the
existing release gates, finalizes twice, and hard-removes row 450 last.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

import wp_deploy_private_unit_journey as release


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = (
    REPO_ROOT
    / "reports"
    / "private-unit-journey-release"
    / "einstein-flagship-20260814T124439Z-4527b2.json"
)
REPORT_SHA256 = "2c415b460965c23e12b9f648d57d76fd99d6c4211cd8c5ff74eb9124286838c2"
STAGE_REQUEST_PATH = (
    REPO_ROOT / "docs" / "wp-drafts" / "einstein-tower-flagship-v3-private-stage.json"
)
STAGE_REQUEST_SHA256 = "d2a97fe08e6270d3e799c6c0fc93aa4ccbab59a7970298f515bf67e836aebb4b"
ACCEPTANCE_PATH = REPO_ROOT / "scripts" / "qa-einstein-flagship-live.mjs"
ACCEPTANCE_SHA256 = "98c1810bb709df1196936ef982ac927a0a62478666be3bf9360f74ce4eb73d15"
DRIVER_PATH = REPO_ROOT / "scripts" / "wp_deploy_private_unit_journey.py"
DRIVER_SHA256 = "1d6500ba1cea2f288483f2b494033234c52642f8b840bb892e5ecb7333aeacff"
DRIVER_BLOB_SHA256 = "fb3a40a6cbd7ae1d4334b565df749e8efd3114432d506ba02c8deb3bc73efce2"
TEMPLATE_PATH = REPO_ROOT / "scripts" / "templates" / "nadlan-unit-journey-deploy-helper.php.tpl"
TEMPLATE_SHA256 = "3854449fc8e072c79bdaebfef89ba450fb01b840b36377383e3a6a1d0b11a024"
TEMPLATE_BLOB_SHA256 = "035225a95f517a4cca2d52ca786617e1efd5f75bf29c9f0329ca538ce59c3b2c"
CORE_TEMPLATE_BLOB_SHA256 = "e3fd05c5acab768f8799a3c98d0d9ad768454d13abccd273d9330ade3d9d66ff"
CORE_FIX_COMMIT = "b9482f76d874945900da9cc507baff291292721a"
OLD_SOURCE_COMMIT = "a0e5033c4a97033c0209c13c68c15bef90670789"

RUN_ID = "einstein-flagship-20260814T124439Z-4527b2"
HELPER_ID = 450
HELPER_NAME = "x-einstein-flagship-20260814T124439Z-4527b2"
ROUTE_PATH = "/deploy-einstein-flagship-20260814T124439Z-4527b2"
HELPER_ROUTE = f"nadlan-private-release/v1{ROUTE_PATH}"
OLD_HELPER_SHA256 = "119647accfef27d41272b3587043282dcf7186935fdc0d47101a8d98c90ad47e"
PRIOR_PATCHED_HELPER_SHA256 = (
    "3a365295c1122fdccacc397d0f93e31ee694ec432513616f26490a7c6c5aa449"
)
HOTFIX_ID = 449
HOTFIX_NAME = "x-einstein-private-stage-direct-route-6885-32"
HOTFIX_SHA256 = "dbe87ddc2bd1a5055e0fe75f2aff134ddb04bd327a5f9715981408fe403677a8"
POST_ID = 6594
CANONICAL_POST_ID = 4867
EXPECTED_VERSION = "1.72.206"
PLUGIN_FILE = "nadlan-config/nadlan-config.php"
PLUGIN_FILES = 286
PLUGIN_BYTES = 22114295
PLUGIN_DIGEST = "556b5dd577b6bab0ca713d301aaa2951d17affab9e7f6de507d6279c069ecfc9"
BACKUP_FILES = 469
BACKUP_BYTES = 28047176
BACKUP_DIGEST = "f1d3a5729bca013a04cced06d54fbc3061733540a948b28eb68c73cefbee3470"
ARTIFACT_SHA256 = "97e9d1d89ee057a4f2027525fa6714298d15b37b5fda10f5affc3a3a34afe341"
ARTIFACT_BYTES = 12585473
ARTIFACT_ENTRIES = 286
ARTIFACT_UNCOMPRESSED_BYTES = 22114295
CANONICAL_STORAGE_SHA256 = "8e502f9d598fcd2521290ae929d95a0662c90ef965ee0bbc416b772c0d49750b"
CANONICAL_REST_SHA256 = "6b9ac9e265fe19260461b514114fe92f76a840434b1244b702671950cc41caee"
CHECKPOINT_SCHEMA = "nadlan-einstein-4527b2-pre-finalize-checkpoint/v1"
POST_FINAL_CHECKPOINT_SCHEMA = "nadlan-einstein-4527b2-post-finalize-checkpoint/v1"

IDENTITY_START = "\t\t\t\t\t$stage_slug_matches = "
IDENTITY_END = "\n\t\t\t\t\tif (\n\t\t\t\t\t\t! $stage_candidate"
SNAPSHOT_IDENTITY_START = "\t\t\t\t$slug_matches = "
SNAPSHOT_IDENTITY_END = (
    "\n\t\t\t\tif (\n\t\t\t\t\t$external_stage_commit_enabled"
)
RESUME_ACTION_START = "\n\t\t\tif ( 'resume_retained_contract' === $action ) {"
RESUME_ACTION_END = "\n\n\t\t\tif ( 'recovery_status' === $action ) {"
TERMINAL_ACTION_START = "\n\n\t\t\tif ( 'terminal_self_delete' === $action ) {"
SCOPE_ABSENCE_START = "\t\t\t$stage_scope_absent = function"
SCOPE_ABSENCE_END = "\n\n\t\t\t$stage_absence_proved = function"
REST_EXPECTATION_START = "\t\t\t\t\t$expected_meta = $external_stage_expected_meta;"
REST_EXPECTATION_NEW_START = "\t\t\t\t\t$expected_rest_meta = $external_stage_expected_meta;"
REST_EXPECTATION_END = "\n\t\t\t\t\tksort( $expected_meta, SORT_STRING );"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def extract_identity_block(source: str) -> str:
    anchor = source.find("$stage_commit_failure_reason_code = 'stage_identity_mismatch';")
    start = source.find(IDENTITY_START, anchor)
    end = source.find(IDENTITY_END, start)
    if anchor < 0 or start < 0 or end <= start:
        raise RuntimeError("Exact stage identity block is unavailable")
    block = source[start:end]
    if source.count(block) != 1:
        raise RuntimeError("Stage identity block is not unique")
    return block


def extract_snapshot_identity_block(source: str) -> str:
    anchor = source.find("$stage_contract_snapshot = function")
    # Include the closure prologue so the runtime patch also injects the
    # function-local WordPress database handle required by the direct query.
    start = source.find("\n\t\t\t) {", anchor)
    if start >= 0:
        start += 1
    end = source.find(SNAPSHOT_IDENTITY_END, start)
    if anchor < 0 or start < 0 or end <= start:
        raise RuntimeError("Exact stage snapshot identity block is unavailable")
    block = source[start:end]
    if source.count(block) != 1:
        raise RuntimeError("Stage snapshot identity block is not unique")
    return block


def extract_resume_action(source: str) -> str:
    start = source.find(RESUME_ACTION_START)
    end = source.find(RESUME_ACTION_END, start)
    if start < 0 or end <= start or source.find(RESUME_ACTION_START, start + 1) >= 0:
        raise RuntimeError("Retained resume contract action is unavailable or ambiguous")
    return source[start:end]


def extract_scope_absence_block(source: str) -> str:
    start = source.find(SCOPE_ABSENCE_START)
    end = source.find(SCOPE_ABSENCE_END, start)
    if start < 0 or end <= start or source.find(SCOPE_ABSENCE_START, start + 1) >= 0:
        raise RuntimeError("Stage scope absence block is unavailable or ambiguous")
    return source[start:end]


def extract_rest_expectation_block(source: str) -> str:
    snapshot = source.find("$stage_contract_snapshot = function")
    old_start = source.find(REST_EXPECTATION_START, snapshot)
    new_start = source.find(REST_EXPECTATION_NEW_START, snapshot)
    starts = [position for position in (old_start, new_start) if position >= 0]
    if snapshot < 0 or len(starts) != 1:
        raise RuntimeError("Stage REST expectation block start is unavailable or ambiguous")
    start = starts[0]
    end = source.find(REST_EXPECTATION_END, start)
    if end <= start:
        raise RuntimeError("Stage REST expectation block end is unavailable")
    block = source[start:end]
    if source.count(block) != 1:
        raise RuntimeError("Stage REST expectation block is not unique")
    return block


def git_show_text(commit: str, path: str) -> str:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("Pinned Git source object is unavailable")
    return completed.stdout.decode("utf-8")


def canonical_lf_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def core_source_bytes_are_exact(driver_bytes: bytes, template_bytes: bytes) -> bool:
    return secrets.compare_digest(sha256_bytes(driver_bytes), DRIVER_BLOB_SHA256) and secrets.compare_digest(
        sha256_bytes(template_bytes), CORE_TEMPLATE_BLOB_SHA256
    )


def source_patch_contract(*, require_merged: bool) -> dict[str, str]:
    for path, expected in (
        (DRIVER_PATH, DRIVER_SHA256),
        (TEMPLATE_PATH, TEMPLATE_SHA256),
        (STAGE_REQUEST_PATH, STAGE_REQUEST_SHA256),
        (ACCEPTANCE_PATH, ACCEPTANCE_SHA256),
    ):
        if not path.is_file() or not secrets.compare_digest(sha256_path(path), expected):
            raise RuntimeError(f"Pinned source file changed: {path.name}")
    old_template = git_show_text(
        OLD_SOURCE_COMMIT,
        "scripts/templates/nadlan-unit-journey-deploy-helper.php.tpl",
    )
    prior_template = git_show_text(
        CORE_FIX_COMMIT,
        "scripts/templates/nadlan-unit-journey-deploy-helper.php.tpl",
    )
    new_template = TEMPLATE_PATH.read_text(encoding="utf-8")
    old_block = extract_identity_block(old_template)
    new_block = extract_identity_block(new_template)
    old_snapshot_block = extract_snapshot_identity_block(old_template)
    new_snapshot_block = extract_snapshot_identity_block(new_template)
    old_scope_absence = extract_scope_absence_block(old_template)
    new_scope_absence = extract_scope_absence_block(new_template)
    old_rest_expectation = extract_rest_expectation_block(old_template)
    new_rest_expectation = extract_rest_expectation_block(new_template)
    prior_resume_action = extract_resume_action(prior_template)
    resume_action = extract_resume_action(new_template)
    if (
        "$stage_slug_matches = get_posts(" not in old_block
        or "$wpdb->get_col(" not in new_block
        or "ORDER BY ID ASC LIMIT 2" not in new_block
        or "External stage slug identity read failed." not in new_block
        or old_block == new_block
        or "$slug_matches = get_posts(" not in old_snapshot_block
        or "global $wpdb;" in old_snapshot_block
        or "global $wpdb;" not in new_snapshot_block
        or "$wpdb->get_col(" not in new_snapshot_block
        or "Stage contract slug identity read failed." not in new_snapshot_block
        or old_snapshot_block == new_snapshot_block
        or old_scope_absence.count("get_posts(") != 2
        or "global $wpdb;" in old_scope_absence
        or new_scope_absence.count("$wpdb->get_col(") != 2
        or "global $wpdb;" not in new_scope_absence
        or "Stage scope marker absence read failed." not in new_scope_absence
        or "get_posts(" in new_scope_absence
        or old_scope_absence == new_scope_absence
        or old_rest_expectation != REST_EXPECTATION_START
        or "$expected_rest_meta['lat'] = round(" not in new_rest_expectation
        or "$expected_rest_meta['lng'] = round(" not in new_rest_expectation
        or "$expected_rest_meta['project_3d_units'] = '';" not in new_rest_expectation
        or "array( 'lat', 'lng', 'project_3d_units' )" not in new_rest_expectation
        or old_rest_expectation == new_rest_expectation
        or "'nadlan-private-release-retained-resume-contract/v1'" not in resume_action
        or "$resume_backup_inventory = $inventory( $resume_backup_path );"
        not in resume_action
        or TERMINAL_ACTION_START not in resume_action
        or "'nadlan-private-release-terminal-self-delete/v1'" not in resume_action
        or "\\Code_Snippets\\delete_snippet( $helper_id, false )" not in resume_action
        or "SELECT id FROM {$wpdb->prefix}snippets WHERE id = %d OR name = %s" not in resume_action
        or resume_action == prior_resume_action
    ):
        raise RuntimeError("Pinned direct-DB/resume helper patch is not exact")
    protected_main_commit = ""
    resume_source_exact = "false"
    if require_merged:
        origin_main = subprocess.run(
            ["git", "rev-parse", "origin/main"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if origin_main.returncode != 0 or re.fullmatch(
            r"[a-f0-9]{40}", origin_main.stdout.strip()
        ) is None:
            raise RuntimeError("Protected-main ref could not be resolved exactly")
        protected_main_commit = origin_main.stdout.strip()
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if head.returncode != 0 or re.fullmatch(r"[a-f0-9]{40}", head.stdout.strip()) is None:
            raise RuntimeError("Local HEAD could not be resolved exactly")
        head_commit = head.stdout.strip()
        head_ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", head_commit, protected_main_commit],
            cwd=REPO_ROOT,
            capture_output=True,
            check=False,
        )
        core_ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", CORE_FIX_COMMIT, protected_main_commit],
            cwd=REPO_ROOT,
            capture_output=True,
            check=False,
        )
        committed_driver = subprocess.run(
            ["git", "show", f"{protected_main_commit}:scripts/wp_deploy_private_unit_journey.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            check=False,
        )
        committed_template = subprocess.run(
            ["git", "show", f"{protected_main_commit}:scripts/templates/nadlan-unit-journey-deploy-helper.php.tpl"],
            cwd=REPO_ROOT,
            capture_output=True,
            check=False,
        )
        core_driver = subprocess.run(
            ["git", "show", f"{CORE_FIX_COMMIT}:scripts/wp_deploy_private_unit_journey.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            check=False,
        )
        core_template = subprocess.run(
            ["git", "show", f"{CORE_FIX_COMMIT}:scripts/templates/nadlan-unit-journey-deploy-helper.php.tpl"],
            cwd=REPO_ROOT,
            capture_output=True,
            check=False,
        )
        protected_paths = (
            (Path(__file__).resolve(), "scripts/wp_resume_einstein_stage_4527b2.py"),
            (STAGE_REQUEST_PATH, "docs/wp-drafts/einstein-tower-flagship-v3-private-stage.json"),
            (ACCEPTANCE_PATH, "scripts/qa-einstein-flagship-live.mjs"),
        )
        protected_main_exact = True
        for local_path, repository_path in protected_paths:
            committed = subprocess.run(
                ["git", "show", f"{protected_main_commit}:{repository_path}"],
                cwd=REPO_ROOT,
                capture_output=True,
                check=False,
            )
            protected_main_exact = (
                protected_main_exact
                and committed.returncode == 0
                and secrets.compare_digest(
                    canonical_lf_bytes(local_path), committed.stdout
                )
            )
        if (
            head_ancestor.returncode != 0
            or core_ancestor.returncode != 0
            or committed_driver.returncode != 0
            or committed_template.returncode != 0
            or not secrets.compare_digest(sha256_bytes(committed_driver.stdout), DRIVER_BLOB_SHA256)
            or not secrets.compare_digest(sha256_bytes(committed_template.stdout), TEMPLATE_BLOB_SHA256)
            or core_driver.returncode != 0
            or core_template.returncode != 0
            or not core_source_bytes_are_exact(
                core_driver.stdout, core_template.stdout
            )
            or not protected_main_exact
        ):
            raise RuntimeError("Protected-main resume/core source provenance differs")
        resume_source_exact = "true"
    return {
        "old_identity": old_block,
        "new_identity": new_block,
        "old_snapshot_identity": old_snapshot_block,
        "new_snapshot_identity": new_snapshot_block,
        "old_scope_absence": old_scope_absence,
        "new_scope_absence": new_scope_absence,
        "old_rest_expectation": old_rest_expectation,
        "new_rest_expectation": new_rest_expectation,
        "prior_resume_action": prior_resume_action,
        "resume_action": resume_action,
        "protected_main_commit": protected_main_commit,
        "resume_source_exact": resume_source_exact,
    }


def pinned_report() -> dict[str, Any]:
    if not REPORT_PATH.is_file() or not secrets.compare_digest(
        sha256_path(REPORT_PATH), REPORT_SHA256
    ):
        raise RuntimeError("Pinned retained-run report is missing or changed")
    payload = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    checks = payload.get("checks") if isinstance(payload.get("checks"), dict) else {}
    deploy = checks.get("deploy") if isinstance(checks.get("deploy"), dict) else {}
    plugin = deploy.get("plugin") if isinstance(deploy.get("plugin"), dict) else {}
    inventory = plugin.get("inventory") if isinstance(plugin.get("inventory"), dict) else {}
    backup = deploy.get("backup") if isinstance(deploy.get("backup"), dict) else {}
    canonical = (
        checks.get("canonical_public_postdeploy")
        if isinstance(checks.get("canonical_public_postdeploy"), dict)
        else {}
    )
    baseline = canonical.get("baseline") if isinstance(canonical.get("baseline"), dict) else {}
    same_schema = (
        checks.get("canonical_public_same_schema_stage_baseline")
        if isinstance(checks.get("canonical_public_same_schema_stage_baseline"), dict)
        else {}
    )
    helper = payload.get("helper") if isinstance(payload.get("helper"), dict) else {}
    artifact = payload.get("artifact") if isinstance(payload.get("artifact"), dict) else {}
    if not (
        payload.get("run_id") == RUN_ID
        and payload.get("passed") is False
        and payload.get("error")
        == "External Einstein stage commit did not reconcile within its retry bound"
        and helper
        == {
            "name": HELPER_NAME,
            "route": HELPER_ROUTE,
            "id": HELPER_ID,
            "code_sha256": OLD_HELPER_SHA256,
        }
        and artifact.get("mode") == "upload"
        and artifact.get("sha256") == ARTIFACT_SHA256
        and artifact.get("archive_bytes") == ARTIFACT_BYTES
        and artifact.get("entry_count") == ARTIFACT_ENTRIES
        and artifact.get("uncompressed_bytes") == ARTIFACT_UNCOMPRESSED_BYTES
        and plugin.get("plugin_file") == PLUGIN_FILE
        and plugin.get("version") == EXPECTED_VERSION
        and plugin.get("active") is True
        and inventory
        == {"file_count": PLUGIN_FILES, "bytes": PLUGIN_BYTES, "digest": PLUGIN_DIGEST}
        and backup
        == {"digest": BACKUP_DIGEST, "file_count": BACKUP_FILES, "bytes": BACKUP_BYTES}
        and baseline.get("contract_sha256") == CANONICAL_STORAGE_SHA256
        and canonical.get("unchanged") is True
        and same_schema.get("snapshot_sha256") == CANONICAL_REST_SHA256
        and checks.get("failure_status", {}).get("state_phase") == "page_creating"
        and checks.get("failure_status", {}).get("backup_ready") is True
        and checks.get("independent_helper_cleanup", {}).get("recovery_retained") is True
    ):
        raise RuntimeError("Pinned retained-run report contract is not exact")
    return payload


def php_assignment(code: str, variable: str, *, integer: bool = False) -> Any:
    if integer:
        matches = re.findall(rf"\${re.escape(variable)}\s*=\s*([0-9]+)\s*;", code)
        if len(matches) != 1:
            raise RuntimeError("Embedded integer helper identity is not exact")
        return int(matches[0])
    matches = re.findall(
        rf'\${re.escape(variable)}\s*=\s*("(?:\\.|[^"\\])*")\s*;', code
    )
    if len(matches) != 1:
        raise RuntimeError("Embedded string helper identity is not exact")
    value = json.loads(matches[0])
    if not isinstance(value, str):
        raise RuntimeError("Embedded helper value is not a string")
    return value


def patch_helper_code(
    code: str, patch_contract: dict[str, str]
) -> tuple[str, str, str]:
    embedded = {
        "route_path": php_assignment(code, "route_path"),
        "token": php_assignment(code, "expected_token"),
        "run_id": php_assignment(code, "run_id"),
        "helper_id": php_assignment(code, "helper_id", integer=True),
        "helper_name": php_assignment(code, "helper_name"),
        "artifact_mode": php_assignment(code, "artifact_mode"),
        "artifact_sha256": php_assignment(code, "artifact_sha256"),
        "artifact_bytes": php_assignment(code, "artifact_bytes", integer=True),
        "artifact_entry_count": php_assignment(code, "artifact_entry_count", integer=True),
        "artifact_uncompressed_bytes": php_assignment(
            code, "artifact_uncompressed_bytes", integer=True
        ),
        "expected_version": php_assignment(code, "expected_version"),
        "source_post_id": php_assignment(code, "source_post_id", integer=True),
        "page_slug": php_assignment(code, "page_slug"),
        "project_contract_id": php_assignment(code, "project_contract_id"),
    }
    expected = {
        "route_path": ROUTE_PATH,
        "run_id": RUN_ID,
        "helper_id": HELPER_ID,
        "helper_name": HELPER_NAME,
        "artifact_mode": "upload",
        "artifact_sha256": ARTIFACT_SHA256,
        "artifact_bytes": ARTIFACT_BYTES,
        "artifact_entry_count": ARTIFACT_ENTRIES,
        "artifact_uncompressed_bytes": ARTIFACT_UNCOMPRESSED_BYTES,
        "expected_version": EXPECTED_VERSION,
        "source_post_id": CANONICAL_POST_ID,
        "page_slug": release.EINSTEIN_STAGE_SLUG,
        "project_contract_id": release.EINSTEIN_PROJECT_CONTRACT_ID,
    }
    if any(embedded[key] != value for key, value in expected.items()):
        raise RuntimeError("Live helper embedded contract differs from retained run")
    token = embedded["token"]
    if not re.fullmatch(r"[a-f0-9]{64}", token):
        raise RuntimeError("Live helper token shape is invalid")
    old_block = patch_contract["old_identity"]
    new_block = patch_contract["new_identity"]
    old_snapshot = patch_contract["old_snapshot_identity"]
    new_snapshot = patch_contract["new_snapshot_identity"]
    old_scope_absence = patch_contract["old_scope_absence"]
    new_scope_absence = patch_contract["new_scope_absence"]
    old_rest_expectation = patch_contract["old_rest_expectation"]
    new_rest_expectation = patch_contract["new_rest_expectation"]
    prior_resume_action = patch_contract["prior_resume_action"]
    resume_action = patch_contract["resume_action"]
    old_count = code.count(old_block)
    new_count = code.count(new_block)
    old_snapshot_count = code.count(old_snapshot)
    new_snapshot_count = code.count(new_snapshot)
    old_scope_absence_count = code.count(old_scope_absence)
    new_scope_absence_count = code.count(new_scope_absence)
    resume_start_count = code.count(RESUME_ACTION_START)
    terminal_action_count = code.count(TERMINAL_ACTION_START)
    prior_resume_count = code.count(prior_resume_action)
    resume_count = code.count(resume_action)
    old_rest_count = code.count(old_rest_expectation)
    new_rest_count = code.count(new_rest_expectation)
    current_hash = release.sha256_text(code)
    if (
        old_count == 1
        and new_count == 0
        and old_snapshot_count == 1
        and new_snapshot_count == 0
        and old_scope_absence_count == 1
        and new_scope_absence_count == 0
        and resume_start_count == 0
        and terminal_action_count == 0
        and prior_resume_count == 0
        and resume_count == 0
        and old_rest_count == 1
        and new_rest_count == 0
    ):
        if not secrets.compare_digest(current_hash, OLD_HELPER_SHA256):
            raise RuntimeError("Old live helper hash differs from retained evidence")
        if code.count(RESUME_ACTION_END) != 1:
            raise RuntimeError("Live helper resume action insertion anchor is not unique")
        patched = code.replace(old_block, new_block, 1)
        patched = patched.replace(old_snapshot, new_snapshot, 1)
        patched = patched.replace(old_scope_absence, new_scope_absence, 1)
        patched = patched.replace(RESUME_ACTION_END, resume_action + RESUME_ACTION_END, 1)
        patched = patched.replace(old_rest_expectation, new_rest_expectation, 1)
    elif (
        old_count == 0
        and new_count == 1
        and old_snapshot_count == 0
        and new_snapshot_count == 1
        and old_scope_absence_count == 0
        and new_scope_absence_count == 1
        and resume_start_count == 1
        and terminal_action_count == 0
        and prior_resume_count == 1
        and resume_count == 0
        and old_rest_count == 1
        and new_rest_count == 0
    ):
        if not secrets.compare_digest(current_hash, PRIOR_PATCHED_HELPER_SHA256):
            raise RuntimeError("Prior patched helper hash differs from retained evidence")
        patched = code.replace(prior_resume_action, resume_action, 1)
        patched = patched.replace(old_rest_expectation, new_rest_expectation, 1)
        reconstructed_old = code.replace(prior_resume_action, "", 1)
        reconstructed_old = reconstructed_old.replace(
            new_scope_absence, old_scope_absence, 1
        )
        reconstructed_old = reconstructed_old.replace(new_snapshot, old_snapshot, 1)
        reconstructed_old = reconstructed_old.replace(new_block, old_block, 1)
        if not secrets.compare_digest(
            release.sha256_text(reconstructed_old), OLD_HELPER_SHA256
        ):
            raise RuntimeError("Already-patched helper cannot reconstruct the pinned old hash")
    elif (
        old_count == 0
        and new_count == 1
        and old_snapshot_count == 0
        and new_snapshot_count == 1
        and old_scope_absence_count == 0
        and new_scope_absence_count == 1
        and resume_start_count == 1
        and terminal_action_count == 1
        and resume_count == 1
        and old_rest_count == 0
        and new_rest_count == 1
    ):
        patched = code
        reconstructed_prior = code.replace(resume_action, prior_resume_action, 1)
        reconstructed_prior = reconstructed_prior.replace(
            new_rest_expectation, old_rest_expectation, 1
        )
        if not secrets.compare_digest(
            release.sha256_text(reconstructed_prior), PRIOR_PATCHED_HELPER_SHA256
        ):
            raise RuntimeError("REST-patched helper cannot reconstruct the pinned prior hash")
        reconstructed_old = reconstructed_prior.replace(prior_resume_action, "", 1)
        reconstructed_old = reconstructed_old.replace(
            new_scope_absence, old_scope_absence, 1
        )
        reconstructed_old = reconstructed_old.replace(new_snapshot, old_snapshot, 1)
        reconstructed_old = reconstructed_old.replace(new_block, old_block, 1)
        if not secrets.compare_digest(
            release.sha256_text(reconstructed_old), OLD_HELPER_SHA256
        ):
            raise RuntimeError("REST-patched helper cannot reconstruct the original hash")
    else:
        raise RuntimeError("Live helper identity patch cardinality is unsafe")
    patched_hash = release.sha256_text(patched)
    if not (
        patched.count(new_block) == 1
        and patched.count(old_block) == 0
        and patched.count(new_snapshot) == 1
        and patched.count(old_snapshot) == 0
        and patched.count(new_scope_absence) == 1
        and patched.count(old_scope_absence) == 0
        and patched.count(resume_action) == 1
        and patched.count(RESUME_ACTION_START) == 1
        and patched.count(TERMINAL_ACTION_START) == 1
        and patched.count(new_rest_expectation) == 1
        and patched.count(old_rest_expectation) == 0
    ):
        raise RuntimeError("Patched helper identity block is not exact")
    return patched, patched_hash, token


def exact_plugin(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or set(payload) != {
        "plugin_file",
        "version",
        "active",
        "inventory",
    }:
        raise RuntimeError("Live plugin payload shape is not exact")
    inventory = payload.get("inventory")
    if (
        payload.get("plugin_file") != PLUGIN_FILE
        or payload.get("version") != EXPECTED_VERSION
        or payload.get("active") is not True
        or inventory
        != {"file_count": PLUGIN_FILES, "bytes": PLUGIN_BYTES, "digest": PLUGIN_DIGEST}
    ):
        raise RuntimeError("Live plugin differs from the pinned candidate")
    return payload


def exact_hotfix(row: Any) -> dict[str, Any]:
    observed = release.observed_snippet(row) if isinstance(row, dict) else {}
    if not (
        observed.get("id") == HOTFIX_ID
        and observed.get("name") == HOTFIX_NAME
        and observed.get("active") is True
        and observed.get("scope") == "global"
        and observed.get("code_sha256") == HOTFIX_SHA256
    ):
        raise RuntimeError("Route hotfix row 449 is not exact and active")
    return observed


def exact_status(payload: dict[str, Any], *, phase: str) -> dict[str, Any]:
    if set(payload) != {
        "http_status",
        "plugin",
        "state_phase",
        "backup_ready",
        "page_id",
        "page_rollback_tracked",
        "upload",
    } or payload.get("http_status") != 200:
        raise RuntimeError("Retained helper status shape is not exact")
    exact_plugin(payload.get("plugin"))
    upload = payload.get("upload") if isinstance(payload.get("upload"), dict) else {}
    retained_phase = phase in {"page_creating", "page_ready"}
    expected_upload = {
        "mode": "upload",
        "verified": retained_phase,
        "next_index": 97 if retained_phase else 0,
        "total_chunks": 97,
        "received_bytes": ARTIFACT_BYTES if retained_phase else 0,
        "temp_absent": True,
        "temp_exists": False,
        "temp_safe": True,
        "temp_bytes": 0,
    }
    if not (
        payload.get("state_phase") == phase
        and payload.get("backup_ready") is retained_phase
        and payload.get("page_id") == (POST_ID if retained_phase else 0)
        and isinstance(payload.get("page_rollback_tracked"), bool)
        and upload == expected_upload
    ):
        raise RuntimeError("Retained helper status contract differs")
    return payload


def exact_resume_contract(payload: dict[str, Any], *, phase: str) -> dict[str, Any]:
    if not (
        set(payload)
        == {
            "http_status",
            "schema",
            "run_id",
            "state_phase",
            "lock_owned",
            "page_id",
            "plugin",
            "backup",
            "upload",
            "canonical_storage_sha256",
        }
        and payload.get("http_status") == 200
        and payload.get("schema")
        == "nadlan-private-release-retained-resume-contract/v1"
        and payload.get("run_id") == RUN_ID
        and payload.get("state_phase") == phase
        and phase in {"page_creating", "page_ready"}
        and payload.get("lock_owned") is True
        and payload.get("page_id") == POST_ID
        and payload.get("backup")
        == {
            "version": "1.72.204",
            "active": True,
            "digest": BACKUP_DIGEST,
            "file_count": BACKUP_FILES,
            "bytes": BACKUP_BYTES,
        }
        and payload.get("upload")
        == {
            "verified": True,
            "next_index": 97,
            "total_chunks": 97,
            "received_bytes": ARTIFACT_BYTES,
            "temp_absent": True,
            "temp_exists": False,
            "temp_safe": True,
            "temp_bytes": 0,
        }
        and payload.get("canonical_storage_sha256")
        == CANONICAL_STORAGE_SHA256
    ):
        raise RuntimeError("Physical retained backup/upload contract differs")
    exact_plugin(payload.get("plugin"))
    return payload


def exact_inspect(payload: dict[str, Any], *, phase: str, lock_owned: bool) -> dict[str, Any]:
    if set(payload) != {
        "http_status",
        "run_id",
        "plugin",
        "lock_free",
        "lock_owned",
        "state_phase",
        "target_exact",
        "artifact",
        "upload_temp_absent",
    } or payload.get("http_status") != 200 or payload.get("run_id") != RUN_ID:
        raise RuntimeError("Retained helper inspect identity differs")
    exact_plugin(payload.get("plugin"))
    if not (
        payload.get("state_phase") == phase
        and payload.get("lock_owned") is lock_owned
        and payload.get("lock_free") is (not lock_owned)
        and payload.get("target_exact") == PLUGIN_FILE
        and payload.get("artifact")
        == {
            "mode": "upload",
            "sha256": ARTIFACT_SHA256,
            "archive_bytes": ARTIFACT_BYTES,
            "entry_count": ARTIFACT_ENTRIES,
            "uncompressed_bytes": ARTIFACT_UNCOMPRESSED_BYTES,
        }
        and payload.get("upload_temp_absent") is True
    ):
        raise RuntimeError("Retained helper inspect contract differs")
    return payload


def exact_stage_commit(payload: dict[str, Any]) -> dict[str, Any]:
    if not (
        set(payload)
        == {
            "http_status",
            "schema",
            "idempotent",
            "state_phase",
            "page_id",
            "created_new",
            "page_contract_kind",
            "page_contract_sha256",
            "page_meta_key_count",
            "password_protected",
            "plugin_digest",
        }
        and payload.get("http_status") == 200
        and payload.get("schema") == "nadlan-private-release-stage-commit/v1"
        and isinstance(payload.get("idempotent"), bool)
        and payload.get("state_phase") == "page_ready"
        and payload.get("page_id") == POST_ID
        and payload.get("created_new") is True
        and payload.get("page_contract_kind") == "external_committed"
        and re.fullmatch(r"[a-f0-9]{64}", str(payload.get("page_contract_sha256") or ""))
        and payload.get("password_protected") is True
        and payload.get("plugin_digest") == PLUGIN_DIGEST
    ):
        raise RuntimeError("External-stage commit response is not exact")
    return payload


def exact_stage_commit_failure(payload: dict[str, Any], *, attempt: int) -> dict[str, Any]:
    data = payload.get("data") if isinstance(payload, dict) else None
    allowed_pairs = {
        ("contract_validation", "stage_commit_disabled"),
        ("contract_validation", "stage_publish_forbidden"),
        ("contract_validation", "stage_commit_request_invalid"),
        ("contract_validation", "stage_commit_phase_invalid"),
        ("lock_validation", "lock_not_owned"),
        ("plugin_validation", "deployed_plugin_mismatch"),
        ("canonical_post_validation", "canonical_post_storage_changed"),
        ("stage_intent", "stage_intent_invalid"),
        ("stage_identity", "stage_identity_mismatch"),
        ("stage_validation", "stage_contract_mismatch"),
        ("stage_validation", "stage_password_mismatch"),
        ("state_commit", "stage_tracking_state_persist_failed"),
        ("state_commit", "stage_state_persist_failed"),
    }
    if (
        not isinstance(attempt, int)
        or isinstance(attempt, bool)
        or not 1 <= attempt <= 3
        or not isinstance(payload, dict)
        or set(payload) != {"http_status", "code", "message", "data"}
        or payload.get("http_status") != 409
        or payload.get("code") != "nadlan_release_stage_commit_failed"
        or payload.get("message") != "External stage commit failed."
        or not isinstance(data, dict)
        or set(data) != {"status", "failure_stage", "failure_reason_code"}
        or data.get("status") != 409
        or (data.get("failure_stage"), data.get("failure_reason_code"))
        not in allowed_pairs
    ):
        raise RuntimeError("External-stage commit failure payload is not finite and exact")
    return {
        "attempt": attempt,
        "http_status": 409,
        "code": "nadlan_release_stage_commit_failed",
        "failure_stage": str(data["failure_stage"]),
        "failure_reason_code": str(data["failure_reason_code"]),
    }


def exact_finalize(payload: dict[str, Any], *, require_idempotent: bool | None) -> dict[str, Any]:
    if not release.normal_rollback_finalize_response_is_exact(
        payload,
        HELPER_ID,
        idempotent=payload.get("idempotent") if isinstance(payload.get("idempotent"), bool) else False,
    ):
        raise RuntimeError("Finalize response is not exact")
    if require_idempotent is not None and payload.get("idempotent") is not require_idempotent:
        raise RuntimeError("Finalize idempotence differs from the required phase")
    return payload


def exact_terminal_self_delete(payload: dict[str, Any], *, page_contract_sha256: str) -> dict[str, Any]:
    if not (
        isinstance(payload, dict)
        and set(payload)
        == {
            "http_status",
            "schema",
            "helper_deleted",
            "state_absent",
            "lock_absent",
            "resources_absent",
            "page_id",
            "page_contract_sha256",
            "plugin_digest",
            "canonical_storage_sha256",
        }
        and payload.get("http_status") == 200
        and payload.get("schema")
        == "nadlan-private-release-terminal-self-delete/v1"
        and payload.get("helper_deleted") is True
        and payload.get("state_absent") is True
        and payload.get("lock_absent") is True
        and payload.get("resources_absent") is True
        and payload.get("page_id") == POST_ID
        and payload.get("page_contract_sha256") == page_contract_sha256
        and payload.get("plugin_digest") == PLUGIN_DIGEST
        and payload.get("canonical_storage_sha256") == CANONICAL_STORAGE_SHA256
    ):
        raise RuntimeError("Terminal helper self-delete response is not exact")
    return payload


def safe_page_url(record: dict[str, Any]) -> str:
    value = str(record.get("link") or "")
    parsed = urlparse(value)
    if not (
        parsed.scheme == "https"
        and parsed.hostname == "nad-lan.co.il"
        and not parsed.username
        and not parsed.password
        and not parsed.query
        and not parsed.fragment
        and release.EINSTEIN_STAGE_SLUG in parsed.path
    ):
        raise RuntimeError("Retained stage URL is unsafe")
    return value


def checkpoint_contract_sha256(payload: dict[str, Any]) -> str:
    body = {key: value for key, value in payload.items() if key != "contract_sha256"}
    return release.sha256_bytes(release.exact_json_bytes(body))


def exact_checkpoint(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or set(payload) != {
        "schema",
        "run_id",
        "helper_id",
        "helper_sha256",
        "post_id",
        "page_url",
        "page_contract_sha256",
        "stage_readback_sha256",
        "acceptance_summary_path",
        "acceptance_summary_sha256",
        "acceptance_proof",
        "canonical_storage_sha256",
        "canonical_rest_sha256",
        "plugin_digest",
        "hotfix_id",
        "hotfix_sha256",
        "ready_for_finalize",
        "contract_sha256",
    }:
        raise RuntimeError("Pre-finalize checkpoint shape is not exact")
    if not (
        payload.get("schema") == CHECKPOINT_SCHEMA
        and payload.get("run_id") == RUN_ID
        and payload.get("helper_id") == HELPER_ID
        and re.fullmatch(r"[a-f0-9]{64}", str(payload.get("helper_sha256") or ""))
        and payload.get("post_id") == POST_ID
        and safe_page_url({"link": payload.get("page_url")}) == payload.get("page_url")
        and re.fullmatch(r"[a-f0-9]{64}", str(payload.get("page_contract_sha256") or ""))
        and re.fullmatch(r"[a-f0-9]{64}", str(payload.get("stage_readback_sha256") or ""))
        and payload.get("acceptance_summary_path") == "acceptance/summary.json"
        and re.fullmatch(r"[a-f0-9]{64}", str(payload.get("acceptance_summary_sha256") or ""))
        and isinstance(payload.get("acceptance_proof"), dict)
        and payload["acceptance_proof"].get("passed") is True
        and payload.get("canonical_storage_sha256") == CANONICAL_STORAGE_SHA256
        and payload.get("canonical_rest_sha256") == CANONICAL_REST_SHA256
        and payload.get("plugin_digest") == PLUGIN_DIGEST
        and payload.get("hotfix_id") == HOTFIX_ID
        and payload.get("hotfix_sha256") == HOTFIX_SHA256
        and payload.get("ready_for_finalize") is True
        and secrets.compare_digest(
            str(payload.get("contract_sha256") or ""),
            checkpoint_contract_sha256(payload),
        )
    ):
        raise RuntimeError("Pre-finalize checkpoint contract differs")
    return payload


def fsync_parent_directory(path: Path) -> None:
    try:
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        directory_fd = os.open(str(path.parent), directory_flags)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except OSError:
        if os.name != "nt":
            raise


def checkpoint_candidate_exists(path: Path) -> bool:
    temporary = path.with_name(path.name + ".tmp")
    return path.exists() or path.is_symlink() or temporary.exists() or temporary.is_symlink()


def durable_atomic_json_read(path: Path, validator: Any, label: str) -> dict[str, Any]:
    temporary = path.with_name(path.name + ".tmp")
    if not path.exists() and not path.is_symlink():
        if not temporary.is_file() or temporary.is_symlink():
            raise RuntimeError(f"Exact {label} checkpoint is unavailable")
        try:
            temporary_bytes = temporary.read_bytes()
            temporary_payload = validator(json.loads(temporary_bytes.decode("utf-8")))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise RuntimeError(f"Exact {label} checkpoint temporary is unreadable") from error
        expected_bytes = (
            json.dumps(temporary_payload, ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8")
        if temporary_bytes != expected_bytes:
            raise RuntimeError(f"Exact {label} checkpoint temporary encoding differs")
        with temporary.open("rb+") as handle:
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        fsync_parent_directory(path)
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"Exact {label} checkpoint is unavailable")
    try:
        observed_bytes = path.read_bytes()
        observed = validator(json.loads(observed_bytes.decode("utf-8")))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Exact {label} checkpoint is unreadable") from error
    expected_bytes = (json.dumps(observed, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )
    if observed_bytes != expected_bytes:
        raise RuntimeError(f"Exact {label} checkpoint encoding differs")
    return observed


def durable_atomic_json_write(path: Path, exact: dict[str, Any], validator: Any) -> dict[str, Any]:
    encoded = (json.dumps(exact, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.parent.is_symlink() or not path.parent.is_dir():
        raise RuntimeError("Checkpoint parent directory is unsafe")
    temporary = path.with_name(path.name + ".tmp")
    if temporary.exists() or temporary.is_symlink():
        if not temporary.is_file() or temporary.is_symlink() or temporary.read_bytes() != encoded:
            raise RuntimeError("Existing checkpoint temporary file differs")
        with temporary.open("rb+") as handle:
            handle.flush()
            os.fsync(handle.fileno())
    else:
        with temporary.open("xb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
    os.replace(temporary, path)
    fsync_parent_directory(path)
    if not path.is_file() or path.is_symlink() or path.read_bytes() != encoded:
        raise RuntimeError("Durable checkpoint readback differs")
    try:
        observed = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError("Durable checkpoint encoding is invalid") from error
    return validator(observed)


def write_checkpoint(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    exact = dict(payload)
    exact["contract_sha256"] = checkpoint_contract_sha256(exact)
    exact_checkpoint(exact)
    if path.exists() or path.is_symlink():
        existing = read_checkpoint(path)
        if existing != exact:
            raise RuntimeError("Existing pre-finalize checkpoint differs")
        return existing
    return durable_atomic_json_write(path, exact, exact_checkpoint)


def read_checkpoint(path: Path) -> dict[str, Any]:
    return durable_atomic_json_read(path, exact_checkpoint, "pre-finalize")


def exact_post_finalize_checkpoint(payload: Any) -> dict[str, Any]:
    keys = {
        "schema",
        "run_id",
        "helper_id",
        "helper_sha256",
        "pre_finalize_contract_sha256",
        "post_id",
        "page_url",
        "page_contract_sha256",
        "stage_readback_sha256",
        "acceptance_summary_sha256",
        "canonical_storage_sha256",
        "canonical_rest_sha256",
        "plugin_digest",
        "hotfix_id",
        "hotfix_sha256",
        "resources_finalized",
        "ready_for_cleanup",
        "contract_sha256",
    }
    if not isinstance(payload, dict) or set(payload) != keys:
        raise RuntimeError("Post-finalize checkpoint shape is not exact")
    if not (
        payload.get("schema") == POST_FINAL_CHECKPOINT_SCHEMA
        and payload.get("run_id") == RUN_ID
        and payload.get("helper_id") == HELPER_ID
        and re.fullmatch(r"[a-f0-9]{64}", str(payload.get("helper_sha256") or ""))
        and re.fullmatch(
            r"[a-f0-9]{64}", str(payload.get("pre_finalize_contract_sha256") or "")
        )
        and payload.get("post_id") == POST_ID
        and safe_page_url({"link": payload.get("page_url")}) == payload.get("page_url")
        and re.fullmatch(
            r"[a-f0-9]{64}", str(payload.get("page_contract_sha256") or "")
        )
        and re.fullmatch(
            r"[a-f0-9]{64}", str(payload.get("stage_readback_sha256") or "")
        )
        and re.fullmatch(
            r"[a-f0-9]{64}", str(payload.get("acceptance_summary_sha256") or "")
        )
        and payload.get("canonical_storage_sha256") == CANONICAL_STORAGE_SHA256
        and payload.get("canonical_rest_sha256") == CANONICAL_REST_SHA256
        and payload.get("plugin_digest") == PLUGIN_DIGEST
        and payload.get("hotfix_id") == HOTFIX_ID
        and payload.get("hotfix_sha256") == HOTFIX_SHA256
        and payload.get("resources_finalized") is True
        and payload.get("ready_for_cleanup") is True
        and secrets.compare_digest(
            str(payload.get("contract_sha256") or ""),
            checkpoint_contract_sha256(payload),
        )
    ):
        raise RuntimeError("Post-finalize checkpoint contract differs")
    return payload


def write_post_finalize_checkpoint(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    exact = dict(payload)
    exact["contract_sha256"] = checkpoint_contract_sha256(exact)
    exact_post_finalize_checkpoint(exact)
    if path.exists() or path.is_symlink():
        existing = read_post_finalize_checkpoint(path)
        if existing != exact:
            raise RuntimeError("Existing post-finalize checkpoint differs")
        return existing
    return durable_atomic_json_write(path, exact, exact_post_finalize_checkpoint)


def read_post_finalize_checkpoint(path: Path) -> dict[str, Any]:
    return durable_atomic_json_read(
        path, exact_post_finalize_checkpoint, "post-finalize"
    )


def self_test() -> dict[str, Any]:
    report = pinned_report()
    patch_contract = source_patch_contract(require_merged=False)
    if (
        patch_contract["old_identity"].count("get_posts(") != 1
        or patch_contract["new_identity"].count("$wpdb->get_col(") != 1
        or patch_contract["old_snapshot_identity"].count("get_posts(") != 1
        or "global $wpdb;" in patch_contract["old_snapshot_identity"]
        or patch_contract["new_snapshot_identity"].count("global $wpdb;") != 1
        or patch_contract["new_snapshot_identity"].count("$wpdb->get_col(") != 1
        or patch_contract["old_scope_absence"].count("get_posts(") != 2
        or patch_contract["new_scope_absence"].count("$wpdb->get_col(") != 2
        or patch_contract["old_rest_expectation"] != REST_EXPECTATION_START
        or patch_contract["new_rest_expectation"].count(
            "array( 'lat', 'lng', 'project_3d_units' )"
        )
        != 1
        or patch_contract["resume_action"].count("resume_retained_contract") != 1
        or patch_contract["resume_action"].count(
            "'terminal_self_delete' === $action"
        )
        != 1
        or patch_contract["prior_resume_action"].count(
            "'terminal_self_delete' === $action"
        )
        != 0
    ):
        raise RuntimeError("Identity patch self-test failed")
    if not (
        secrets.compare_digest(
            sha256_bytes(canonical_lf_bytes(DRIVER_PATH)), DRIVER_BLOB_SHA256
        )
        and secrets.compare_digest(
            sha256_bytes(canonical_lf_bytes(TEMPLATE_PATH)), TEMPLATE_BLOB_SHA256
        )
    ):
        raise RuntimeError("Canonical LF source-blob contract self-test failed")
    stage = release.validate_einstein_stage_request(STAGE_REQUEST_PATH)
    if stage["body"]["slug"] != release.EINSTEIN_STAGE_SLUG:
        raise RuntimeError("Pinned stage request self-test failed")
    request_meta = stage["body"]["meta"]
    raw_before = release.exact_json_bytes(request_meta)
    rest_meta = release.einstein_stage_expected_rest_meta(request_meta)
    changed_keys = sorted(
        key for key in request_meta if request_meta[key] != rest_meta[key]
    )
    if not (
        changed_keys == sorted(release.EINSTEIN_STAGE_REST_NORMALIZED_META_KEYS)
        and rest_meta["lat"] == 32.111736
        and rest_meta["lng"] == 34.788433
        and rest_meta["project_3d_units"] == ""
        and release.exact_json_bytes(request_meta) == raw_before
    ):
        raise RuntimeError("Pinned REST/raw representation split self-test failed")
    for key, drift in (
        ("lat", str(request_meta["lat"])),
        ("lng", True),
        ("project_3d_units", ""),
    ):
        drifted = dict(request_meta)
        drifted[key] = drift
        try:
            release.einstein_stage_expected_rest_meta(drifted)
        except RuntimeError:
            continue
        raise RuntimeError(f"REST normalization accepted drifted input: {key}")
    finite_failure = exact_stage_commit_failure(
        {
            "http_status": 409,
            "code": "nadlan_release_stage_commit_failed",
            "message": "External stage commit failed.",
            "data": {
                "status": 409,
                "failure_stage": "stage_validation",
                "failure_reason_code": "stage_contract_mismatch",
            },
        },
        attempt=1,
    )
    if finite_failure != {
        "attempt": 1,
        "http_status": 409,
        "code": "nadlan_release_stage_commit_failed",
        "failure_stage": "stage_validation",
        "failure_reason_code": "stage_contract_mismatch",
    }:
        raise RuntimeError("Finite stage failure projection self-test failed")
    core_test = release.self_test()
    if core_test.get("passed") is not True or core_test.get("php_lint") != "passed":
        raise RuntimeError("Release engine self-test or rendered PHP lint failed")
    source = Path(__file__).read_text(encoding="utf-8")
    main_start = source.find("\ndef main() -> int:")
    if main_start < 0:
        raise RuntimeError("One-shot resume main entry point is missing")
    main_source = source[main_start:]
    normal_start = main_source.find("        commit_extra = {")
    cleanup_start = main_source.find("    def cleanup_helper_terminal(")
    runtime_start = main_source.find("\n    try:\n        me =")
    if min(normal_start, cleanup_start, runtime_start) < 0:
        raise RuntimeError("One-shot resume runtime slices are missing")
    normal_source = main_source[normal_start:]
    ordered = [
        '"commit_external_stage", extra=commit_extra',
        "stage_readback = release.assert_einstein_stage_readback(",
        'evidence["checks"]["anonymous_private_surfaces"] = release.anonymous_einstein_probes(',
        "acceptance = subprocess.run(",
        "storage_final = release.canonical_post_storage_comparison(",
        "checkpoint = write_checkpoint(",
        'evidence["checks"]["finalize_twice"] = finalize_twice(',
        "record_post_finalize_checkpoint(checkpoint)",
        "cleanup_helper_terminal(hotfix_before)",
    ]
    positions = [normal_source.find(marker) for marker in ordered]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        raise RuntimeError("One-shot resume gate ordering drifted")
    runtime_source = main_source[runtime_start:]
    for marker in (
        'retained_phase not in {"page_creating", "page_ready", "none"}',
        'if retained_phase == "none":',
        "reusable_pre_finalize = read_checkpoint(checkpoint_path)",
        '"resume_retained_contract", timeout=180',
        "exact_resume_contract(resume_before, phase=retained_phase)",
        "exact_resume_contract(resume_ready, phase=\"page_ready\")",
        "read_post_finalize_checkpoint(post_finalize_checkpoint_path)",
        'evidence["checks"]["helper_cleanup_last"] = cleanup_reconciliation',
        "exact_stage_commit_failure(candidate, attempt=attempt)",
        "and not cleanup_terminal_probe_started",
        '"reused_immutable_checkpoint": True',
    ):
        if marker not in runtime_source:
            raise RuntimeError("One-shot response-loss gate is missing")
    cleanup_end = main_source.find("\n    try:\n        me =", cleanup_start)
    cleanup_source = main_source[cleanup_start:cleanup_end]
    cleanup_order = [
        "pre_finalize = read_checkpoint(checkpoint_path)",
        "rows_before = client.all_snippets()",
        "cleanup_terminal_probe_started = True",
        '"terminal_self_delete",',
        "helper_after = client.request(",
        "route_after = client.request(",
        "hotfix_after = exact_hotfix(",
        "rows_after = client.all_snippets()",
        "final_hotfix = exact_hotfix(final_hotfix_rows[0])",
    ]
    cleanup_positions = [cleanup_source.find(marker) for marker in cleanup_order]
    if any(position < 0 for position in cleanup_positions) or cleanup_positions != sorted(
        cleanup_positions
    ):
        raise RuntimeError("Terminal helper cleanup ordering drifted")
    proof_start = cleanup_source.find("        proof = {")
    proof_end = cleanup_source.find("        evidence[\"checks\"][\"helper_cleanup_last\"]", proof_start)
    proof_source = cleanup_source[proof_start:proof_end]
    if not (
        proof_start >= 0
        and proof_end > proof_start
        and '"target_absent": True' in proof_source
        and '"terminal_self_delete_response_loss_reconciled"' in proof_source
        and '"cleanup_helpers_created": 0' in proof_source
        and "independently_remove_snippet" not in cleanup_source
        and "os.fsync(handle.fileno())" in source
        and "os.replace(temporary, path)" in source
        and "Durable checkpoint readback differs" in source
    ):
        raise RuntimeError("Terminal self-delete/checkpoint durability self-test failed")
    return {
        "passed": True,
        "run_id": report["run_id"],
        "helper_id": HELPER_ID,
        "post_id": POST_ID,
        "report_sha256": REPORT_SHA256,
        "template_sha256": TEMPLATE_SHA256,
        "driver_sha256": DRIVER_SHA256,
        "stage_request_sha256": STAGE_REQUEST_SHA256,
        "acceptance_sha256": ACCEPTANCE_SHA256,
        "rendered_helper_php_lint": "passed",
        "direct_db_patch_exact": True,
        "live_calls": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--env", type=Path, default=REPO_ROOT / ".env")
    parser.add_argument("--acceptance-timeout-seconds", type=int, default=2400)
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False, indent=2))
        return 0
    if not 60 <= args.acceptance_timeout_seconds <= 7200:
        raise SystemExit("--acceptance-timeout-seconds must be between 60 and 7200")

    pinned_report()
    patch_contract = source_patch_contract(require_merged=True)
    stage_request = release.validate_einstein_stage_request(STAGE_REQUEST_PATH)
    env = release.read_env(args.env)
    base_url = release.validate_site_url(os.environ.get("WP_BASE_URL") or env.get("WP_BASE_URL") or "")
    wp_user = os.environ.get("WP_USER") or env.get("WP_USER") or ""
    wp_password = os.environ.get("WP_APP_PASSWORD") or env.get("WP_APP_PASSWORD") or ""
    post_password = os.environ.get("SANDBOX_POST_PASSWORD") or env.get("SANDBOX_POST_PASSWORD") or ""
    if not wp_user or not wp_password or not post_password or len(post_password) > 255:
        raise SystemExit("WP credentials and SANDBOX_POST_PASSWORD are required")
    redactor = release.Redactor((wp_user, wp_password, post_password))
    client = release.WordpressClient(base_url, wp_user, wp_password)
    public = requests.Session()
    public.headers.update({"User-Agent": "NadLan-Einstein-4527b2-Resume/1.0", "Accept": "application/json"})
    output_dir = (
        REPO_ROOT
        / "reports"
        / "private-unit-journey-release"
        / "resume-4527b2"
    )
    if output_dir.is_symlink() or (output_dir.exists() and not output_dir.is_dir()):
        raise SystemExit("Pinned resume evidence directory is unsafe")
    acceptance_dir = output_dir / "acceptance"
    if acceptance_dir.is_symlink() or (
        acceptance_dir.exists() and not acceptance_dir.is_dir()
    ):
        raise SystemExit("Pinned acceptance evidence directory is unsafe")
    invocation_started = datetime.now(timezone.utc)
    invocation_slug = invocation_started.strftime("%Y%m%dT%H%M%S%fZ")
    evidence: dict[str, Any] = {
        "schema": "nadlan-einstein-4527b2-same-run-resume/v1",
        "run_id": RUN_ID,
        "started_at_utc": invocation_started.isoformat(),
        "pinned": {
            "report_path": str(REPORT_PATH.relative_to(REPO_ROOT)),
            "report_sha256": REPORT_SHA256,
            "core_fix_commit": CORE_FIX_COMMIT,
            "protected_main_commit": patch_contract["protected_main_commit"],
            "resume_source_exact": patch_contract["resume_source_exact"] == "true",
            "old_helper_sha256": OLD_HELPER_SHA256,
            "helper_id": HELPER_ID,
            "helper_name": HELPER_NAME,
            "post_id": POST_ID,
            "plugin": {"version": EXPECTED_VERSION, "digest": PLUGIN_DIGEST, "files": PLUGIN_FILES, "bytes": PLUGIN_BYTES},
            "backup": {"digest": BACKUP_DIGEST, "files": BACKUP_FILES, "bytes": BACKUP_BYTES},
            "artifact": {"sha256": ARTIFACT_SHA256, "bytes": ARTIFACT_BYTES, "entries": ARTIFACT_ENTRIES, "uncompressed_bytes": ARTIFACT_UNCOMPRESSED_BYTES},
            "canonical_storage_sha256": CANONICAL_STORAGE_SHA256,
            "canonical_rest_sha256": CANONICAL_REST_SHA256,
        },
        "checks": {},
        "passed": False,
    }
    token = ""
    patched_hash = ""
    helper_cleanup_proved = False
    cleanup_terminal_probe_started = False
    checkpoint_path = output_dir / "pre-finalize-checkpoint.json"
    post_finalize_checkpoint_path = output_dir / "post-finalize-checkpoint.json"

    def call_helper(action: str, *, extra: dict[str, Any] | None = None, timeout: int = 120) -> tuple[requests.Response, dict[str, Any]]:
        body: dict[str, Any] = {"token": token, "helper_sha256": patched_hash, "action": action}
        if extra:
            if {"token", "helper_sha256", "action"}.intersection(extra):
                raise RuntimeError("Helper extras attempted to replace protected fields")
            body.update(extra)
        response = client.request("POST", HELPER_ROUTE, json_body=body, timeout=timeout)
        return response, release.response_payload(response)

    def finalize_twice(*, first_must_be_idempotent: bool) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for finalize_index in range(2):
            exact: dict[str, Any] = {}
            for attempt in range(1, 3):
                try:
                    response, candidate = call_helper("finalize", timeout=180)
                    if response.status_code == 200:
                        exact = exact_finalize(
                            candidate,
                            require_idempotent=(
                                True
                                if first_must_be_idempotent or finalize_index == 1
                                else None
                            ),
                        )
                        exact["driver_attempts"] = attempt
                        break
                except requests.RequestException:
                    pass
            if not exact:
                raise RuntimeError("Release finalization did not reconcile")
            results.append(exact)
        if results[1].get("idempotent") is not True:
            raise RuntimeError("Second finalization did not prove idempotence")
        return results

    def prove_post_finalize() -> dict[str, Any]:
        status_response, status_finalized = call_helper("status", timeout=60)
        release.require_response(status_response, "Post-finalize status")
        exact_status(status_finalized, phase="none")
        inspect_response, inspect_finalized = call_helper("inspect", timeout=60)
        release.require_response(inspect_response, "Post-finalize inspect")
        exact_inspect(inspect_finalized, phase="none", lock_owned=False)
        proof = {
            "state_absent": True,
            "lock_free": True,
            "backup_deleted": True,
            "storage_root_deleted": True,
            "upload_temp_absent": True,
            "plugin_version": EXPECTED_VERSION,
            "plugin_digest": PLUGIN_DIGEST,
        }
        evidence["checks"]["resources_finalized"] = proof
        return proof

    def record_post_finalize_checkpoint(pre_finalize: dict[str, Any]) -> dict[str, Any]:
        exact_checkpoint(pre_finalize)
        terminal = write_post_finalize_checkpoint(
            post_finalize_checkpoint_path,
            {
                "schema": POST_FINAL_CHECKPOINT_SCHEMA,
                "run_id": RUN_ID,
                "helper_id": HELPER_ID,
                "helper_sha256": patched_hash,
                "pre_finalize_contract_sha256": pre_finalize["contract_sha256"],
                "post_id": POST_ID,
                "page_url": pre_finalize["page_url"],
                "page_contract_sha256": pre_finalize["page_contract_sha256"],
                "stage_readback_sha256": pre_finalize["stage_readback_sha256"],
                "acceptance_summary_sha256": pre_finalize[
                    "acceptance_summary_sha256"
                ],
                "canonical_storage_sha256": CANONICAL_STORAGE_SHA256,
                "canonical_rest_sha256": CANONICAL_REST_SHA256,
                "plugin_digest": PLUGIN_DIGEST,
                "hotfix_id": HOTFIX_ID,
                "hotfix_sha256": HOTFIX_SHA256,
                "resources_finalized": True,
                "ready_for_cleanup": True,
            },
        )
        evidence["checks"]["post_finalize_checkpoint"] = {
            "path": str(post_finalize_checkpoint_path.relative_to(REPO_ROOT)),
            "contract_sha256": terminal["contract_sha256"],
            "pre_finalize_contract_sha256": terminal[
                "pre_finalize_contract_sha256"
            ],
        }
        return terminal

    def cleanup_helper_terminal(hotfix_before: dict[str, Any]) -> dict[str, Any]:
        nonlocal helper_cleanup_proved, cleanup_terminal_probe_started
        pre_finalize = read_checkpoint(checkpoint_path)
        post_finalize = read_post_finalize_checkpoint(post_finalize_checkpoint_path)
        if not (
            pre_finalize["helper_sha256"] == patched_hash
            and post_finalize["helper_sha256"] == patched_hash
            and post_finalize["pre_finalize_contract_sha256"]
            == pre_finalize["contract_sha256"]
            and post_finalize["page_contract_sha256"]
            == pre_finalize["page_contract_sha256"]
            and post_finalize["page_url"] == pre_finalize["page_url"]
            and post_finalize["stage_readback_sha256"]
            == pre_finalize["stage_readback_sha256"]
            and post_finalize["acceptance_summary_sha256"]
            == pre_finalize["acceptance_summary_sha256"]
        ):
            raise RuntimeError("Terminal cleanup checkpoints are not linked exactly")
        rows_before = client.all_snippets()
        if any(
            str(row.get("name") or "").startswith("x-unit-journey-cleanup-")
            for row in rows_before
        ):
            raise RuntimeError("Pre-terminal collection contains an old cleanup helper")
        helper_before_rows = [
            row
            for row in rows_before
            if int(row.get("id") or 0) == HELPER_ID
            or str(row.get("name") or "") == HELPER_NAME
        ]
        if len(helper_before_rows) != 1 or release.observed_snippet(
            helper_before_rows[0]
        ) != {
            "id": HELPER_ID,
            "name": HELPER_NAME,
            "active": True,
            "scope": "global",
            "code_sha256": patched_hash,
        }:
            raise RuntimeError("Pre-terminal helper collection identity differs")
        cleanup_terminal_probe_started = True
        cleanup_response_lost = False
        terminal_response_exact = False
        try:
            terminal_response, terminal_payload = call_helper(
                "terminal_self_delete",
                extra={
                    "page_id": POST_ID,
                    "page_contract_sha256": pre_finalize[
                        "page_contract_sha256"
                    ],
                    "plugin_digest": PLUGIN_DIGEST,
                    "canonical_storage_sha256": CANONICAL_STORAGE_SHA256,
                },
                timeout=180,
            )
            if terminal_response.status_code == 200:
                exact_terminal_self_delete(
                    terminal_payload,
                    page_contract_sha256=pre_finalize["page_contract_sha256"],
                )
                terminal_response_exact = True
        except requests.RequestException:
            cleanup_response_lost = True
        helper_after = client.request(
            "GET", f"code-snippets/v1/snippets/{HELPER_ID}", timeout=60
        )
        route_after = client.request(
            "POST", HELPER_ROUTE, json_body={"action": "status"}, timeout=60
        )
        hotfix_after = exact_hotfix(
            release.require_response(
                client.request(
                    "GET", f"code-snippets/v1/snippets/{HOTFIX_ID}", timeout=60
                ),
                "Route hotfix 449 final read",
            )
        )
        if hotfix_after != hotfix_before:
            raise RuntimeError("Route hotfix 449 changed during helper cleanup")
        # The complete collection is deliberately the last external call.  If it
        # fails, the failure path must not make a later retention request.
        rows_after = client.all_snippets()
        if not release.snippet_absence_is_proved(
            helper_after,
            rows_after,
            snippet_id=HELPER_ID,
            snippet_name=HELPER_NAME,
            route_status=route_after.status_code,
        ):
            raise RuntimeError("Helper 450 ID/name/route absence is not proved")
        if any(
            str(row.get("name") or "").startswith("x-unit-journey-cleanup-")
            for row in rows_after
        ):
            raise RuntimeError("Authoritative final collection contains a cleanup helper")
        final_hotfix_rows = [
            row
            for row in rows_after
            if int(row.get("id") or 0) == HOTFIX_ID
            or str(row.get("name") or "") == HOTFIX_NAME
        ]
        if len(final_hotfix_rows) != 1:
            raise RuntimeError("Authoritative final collection hotfix identity is ambiguous")
        final_hotfix = exact_hotfix(final_hotfix_rows[0])
        if final_hotfix != hotfix_before:
            raise RuntimeError("Authoritative final collection hotfix changed")
        proof = {
            "target_absent": True,
            "target_get_status": helper_after.status_code,
            "target_missing_response_exact": True,
            "method": (
                "terminal_self_delete_response_loss_reconciled"
                if cleanup_response_lost
                else "terminal_self_delete"
            ),
            "terminal_response_exact": terminal_response_exact,
            "helper_id_absent": True,
            "helper_name_absent": True,
            "helper_route_status": route_after.status_code,
            "route_hotfix_449_unchanged_active": True,
            "route_hotfix_449": hotfix_after,
            "route_hotfix_449_final_collection": final_hotfix,
            "cleanup_helpers_created": 0,
            "cleanup_helpers_absent": True,
            "response_loss_reconciled": cleanup_response_lost,
            "authoritative_collection_last": True,
        }
        evidence["checks"]["helper_cleanup_last"] = proof
        helper_cleanup_proved = True
        return proof

    try:
        me = release.require_response(client.request("GET", "wp/v2/users/me", timeout=60), "Resume authentication")
        if me.get("id") != 1:
            raise RuntimeError("Resume requires the pinned owner administrator")
        hotfix_before_row = release.require_response(
            client.request("GET", f"code-snippets/v1/snippets/{HOTFIX_ID}", timeout=60),
            "Route hotfix 449 read",
        )
        hotfix_before = exact_hotfix(hotfix_before_row)
        evidence["checks"]["route_hotfix_before"] = hotfix_before

        helper_response = client.request("GET", f"code-snippets/v1/snippets/{HELPER_ID}", timeout=60)
        if release.is_exact_missing_snippet_response(helper_response):
            pre_finalize = read_checkpoint(checkpoint_path)
            post_finalize = read_post_finalize_checkpoint(post_finalize_checkpoint_path)
            if not (
                post_finalize["pre_finalize_contract_sha256"]
                == pre_finalize["contract_sha256"]
                and post_finalize["page_url"] == pre_finalize["page_url"]
                and post_finalize["page_contract_sha256"]
                == pre_finalize["page_contract_sha256"]
                and post_finalize["stage_readback_sha256"]
                == pre_finalize["stage_readback_sha256"]
                and post_finalize["acceptance_summary_sha256"]
                == pre_finalize["acceptance_summary_sha256"]
                and post_finalize["helper_sha256"] == pre_finalize["helper_sha256"]
            ):
                raise RuntimeError("Post-finalize checkpoint is not linked to its exact pre-finalize proof")
            patched_hash = str(post_finalize["helper_sha256"])
            summary_path = output_dir / str(pre_finalize["acceptance_summary_path"])
            if (
                not summary_path.is_file()
                or summary_path.is_symlink()
                or not secrets.compare_digest(
                    sha256_path(summary_path), pre_finalize["acceptance_summary_sha256"]
                )
            ):
                raise RuntimeError("Finalized acceptance evidence differs")
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            if release.acceptance_summary_proof(summary, einstein_mode=True) != pre_finalize[
                "acceptance_proof"
            ]:
                raise RuntimeError("Finalized acceptance proof differs")
            finalized_record = release.get_authenticated_post(client, POST_ID)
            finalized_readback = release.assert_einstein_stage_readback(
                finalized_record, stage_request, post_password
            )
            if not secrets.compare_digest(
                release.sha256_bytes(release.exact_json_bytes(finalized_readback)),
                post_finalize["stage_readback_sha256"],
            ):
                raise RuntimeError("Finalized stage readback differs")
            finalized_page_url = safe_page_url(finalized_record)
            if finalized_page_url != post_finalize["page_url"]:
                raise RuntimeError("Finalized stage URL differs")
            evidence["page_url"] = finalized_page_url
            evidence["checks"]["final_anonymous_private_surfaces"] = (
                release.anonymous_einstein_probes(
                    base_url,
                    finalized_page_url,
                    POST_ID,
                    stage_request,
                    post_password,
                )
            )
            canonical_finalized = release.wordpress_post_snapshot(
                release.get_authenticated_post(client, CANONICAL_POST_ID)
            )
            if not secrets.compare_digest(
                release.sha256_bytes(release.exact_json_bytes(canonical_finalized)),
                CANONICAL_REST_SHA256,
            ):
                raise RuntimeError("Canonical REST snapshot changed after helper cleanup")
            health = public.get(
                f"{base_url}/wp-json/nadlan/v1/healthcheck",
                params={"cb": f"{RUN_ID}-cleanup-reconcile"},
                timeout=30,
            )
            health_version = (
                release.find_health_version(health.json())
                if health.status_code == 200
                else ""
            )
            if health.status_code != 200 or health_version != EXPECTED_VERSION:
                raise RuntimeError("Finalized cleanup reconciliation healthcheck differs")
            route_after = client.request(
                "POST", HELPER_ROUTE, json_body={"action": "status"}, timeout=60
            )
            hotfix_after = exact_hotfix(
                release.require_response(
                    client.request(
                        "GET", f"code-snippets/v1/snippets/{HOTFIX_ID}", timeout=60
                    ),
                    "Route hotfix 449 cleanup reconciliation read",
                )
            )
            if hotfix_after != hotfix_before:
                raise RuntimeError("Route hotfix 449 changed after helper cleanup")
            cleanup_terminal_probe_started = True
            rows_after = client.all_snippets()
            if not release.snippet_absence_is_proved(
                helper_response,
                rows_after,
                snippet_id=HELPER_ID,
                snippet_name=HELPER_NAME,
                route_status=route_after.status_code,
            ) or any(
                str(row.get("name") or "").startswith("x-unit-journey-cleanup-")
                for row in rows_after
            ):
                raise RuntimeError("Finalized helper/cleanup-row absence is not exact")
            final_hotfix_rows = [
                row
                for row in rows_after
                if int(row.get("id") or 0) == HOTFIX_ID
                or str(row.get("name") or "") == HOTFIX_NAME
            ]
            if len(final_hotfix_rows) != 1:
                raise RuntimeError("Final authoritative collection hotfix is ambiguous")
            final_hotfix = exact_hotfix(final_hotfix_rows[0])
            if final_hotfix != hotfix_before:
                raise RuntimeError("Final authoritative collection hotfix differs")
            helper_cleanup_proved = True
            cleanup_reconciliation = {
                "target_absent": True,
                "target_get_status": helper_response.status_code,
                "target_missing_response_exact": True,
                "method": "already_absent_post_finalize_checkpoint_reconciled",
                "pre_finalize_contract_sha256": pre_finalize["contract_sha256"],
                "post_finalize_contract_sha256": post_finalize["contract_sha256"],
                "helper_id_absent": True,
                "helper_name_absent": True,
                "helper_route_status": route_after.status_code,
                "cleanup_helpers_absent": True,
                "route_hotfix_449_unchanged_active": True,
                "route_hotfix_449": hotfix_after,
                "route_hotfix_449_final_collection": final_hotfix,
                "response_loss_reconciled": True,
                "authoritative_collection_last": True,
            }
            evidence["checks"]["helper_cleanup_last"] = cleanup_reconciliation
            evidence["checks"]["helper_cleanup_response_loss_reconciled"] = (
                cleanup_reconciliation
            )
            evidence["passed"] = True
            return 0
        helper_row = release.require_response(helper_response, "Retained helper 450 read")
        helper_observed = release.observed_snippet(helper_row)
        if not (
            helper_observed["id"] == HELPER_ID
            and helper_observed["name"] == HELPER_NAME
            and helper_observed["scope"] == "global"
            and isinstance(helper_observed["active"], bool)
        ):
            raise RuntimeError("Retained helper row identity differs")
        patched_code, patched_hash, token = patch_helper_code(
            str(helper_row.get("code") or ""), patch_contract
        )
        redactor = release.Redactor((wp_user, wp_password, post_password, token))
        evidence["checks"]["helper_patch_plan"] = {
            "old_sha256": OLD_HELPER_SHA256,
            "new_sha256": patched_hash,
            "exact_identity_block_replacements": 2,
            "exact_scope_absence_block_replacements": 1,
            "exact_read_only_action_insertions": 1,
            "source_template_sha256": TEMPLATE_SHA256,
        }

        desired_inactive = {
            "id": HELPER_ID,
            "name": HELPER_NAME,
            "active": False,
            "scope": "global",
            "code_sha256": patched_hash,
        }
        inactive_exact = False
        for _attempt in range(2):
            try:
                client.request(
                    "PUT",
                    f"code-snippets/v1/snippets/{HELPER_ID}",
                    json_body={"name": HELPER_NAME, "code": patched_code, "scope": "global", "active": False},
                    timeout=60,
                )
            except requests.RequestException:
                pass
            observed_response = client.request("GET", f"code-snippets/v1/snippets/{HELPER_ID}", timeout=60)
            if observed_response.status_code == 200 and release.observed_snippet(observed_response.json()) == desired_inactive:
                inactive_exact = True
                break
        if not inactive_exact:
            raise RuntimeError("Patched helper inactive update did not reconcile")
        evidence["checks"]["patched_helper_inactive"] = desired_inactive

        desired_active = {**desired_inactive, "active": True}
        active_exact = False
        for _attempt in range(2):
            try:
                client.request(
                    "PUT",
                    f"code-snippets/v1/snippets/{HELPER_ID}/activate",
                    json_body={},
                    timeout=60,
                )
            except requests.RequestException:
                pass
            observed_response = client.request("GET", f"code-snippets/v1/snippets/{HELPER_ID}", timeout=60)
            if observed_response.status_code == 200 and release.observed_snippet(observed_response.json()) == desired_active:
                active_exact = True
                break
        if not active_exact:
            raise RuntimeError("Patched helper activation did not reconcile")
        evidence["checks"]["patched_helper_active"] = desired_active

        status_response, status_before = call_helper("status", timeout=60)
        release.require_response(status_response, "Retained same-run status")
        retained_phase = str(status_before.get("state_phase") or "")
        if retained_phase not in {"page_creating", "page_ready", "none"}:
            raise RuntimeError("Retained same-run phase cannot be reconciled")
        exact_status(status_before, phase=retained_phase)
        inspect_response, inspect_before = call_helper("inspect", timeout=60)
        release.require_response(inspect_response, "Retained same-run inspect")
        exact_inspect(
            inspect_before,
            phase=retained_phase,
            lock_owned=retained_phase != "none",
        )
        evidence["checks"]["retained_state_before_commit"] = {
            "state_phase": retained_phase,
            "page_id": POST_ID if retained_phase != "none" else 0,
            "lock_owned": retained_phase != "none",
            "backup_ready": retained_phase != "none",
            "plugin_digest": PLUGIN_DIGEST,
        }
        reusable_pre_finalize: dict[str, Any] | None = None
        if checkpoint_candidate_exists(checkpoint_path):
            reusable_pre_finalize = read_checkpoint(checkpoint_path)
            if not secrets.compare_digest(
                reusable_pre_finalize["helper_sha256"], patched_hash
            ):
                raise RuntimeError("Existing checkpoint helper hash differs")
            if retained_phase == "page_creating":
                raise RuntimeError("Pre-finalize checkpoint exists before page-ready state")

        if retained_phase == "none":
            if reusable_pre_finalize is None:
                raise RuntimeError("Finalized state is missing its exact pre-finalize checkpoint")
            checkpoint = reusable_pre_finalize
            summary_path = output_dir / checkpoint["acceptance_summary_path"]
            if (
                not summary_path.is_file()
                or summary_path.is_symlink()
                or not secrets.compare_digest(
                    sha256_path(summary_path),
                    checkpoint["acceptance_summary_sha256"],
                )
            ):
                raise RuntimeError("Finalized checkpoint acceptance evidence differs")
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            acceptance_proof = release.acceptance_summary_proof(
                summary, einstein_mode=True
            )
            if acceptance_proof != checkpoint["acceptance_proof"]:
                raise RuntimeError("Finalized checkpoint acceptance proof differs")
            finalized_record = release.get_authenticated_post(client, POST_ID)
            finalized_readback = release.assert_einstein_stage_readback(
                finalized_record, stage_request, post_password
            )
            finalized_readback_sha = release.sha256_bytes(
                release.exact_json_bytes(finalized_readback)
            )
            finalized_page_url = safe_page_url(finalized_record)
            if not (
                secrets.compare_digest(
                    finalized_readback_sha, checkpoint["stage_readback_sha256"]
                )
                and finalized_page_url == checkpoint["page_url"]
            ):
                raise RuntimeError("Finalized checkpoint stage readback differs")
            evidence["page_url"] = finalized_page_url
            evidence["checks"]["finalized_response_loss_reconciliation"] = {
                "checkpoint_contract_sha256": checkpoint["contract_sha256"],
                "stage_readback_sha256": finalized_readback_sha,
                "acceptance_summary_sha256": checkpoint[
                    "acceptance_summary_sha256"
                ],
                "state_absent": True,
            }
            evidence["checks"]["final_anonymous_private_surfaces"] = (
                release.anonymous_einstein_probes(
                    base_url,
                    finalized_page_url,
                    POST_ID,
                    stage_request,
                    post_password,
                )
            )
            canonical_finalized = release.wordpress_post_snapshot(
                release.get_authenticated_post(client, CANONICAL_POST_ID)
            )
            canonical_finalized_sha = release.sha256_bytes(
                release.exact_json_bytes(canonical_finalized)
            )
            if not secrets.compare_digest(
                canonical_finalized_sha, CANONICAL_REST_SHA256
            ):
                raise RuntimeError(
                    "Same-schema canonical REST snapshot changed after finalization"
                )
            health = public.get(
                f"{base_url}/wp-json/nadlan/v1/healthcheck",
                params={"cb": f"{RUN_ID}-finalized-reconcile"},
                timeout=30,
            )
            health_version = (
                release.find_health_version(health.json())
                if health.status_code == 200
                else ""
            )
            if health.status_code != 200 or health_version != EXPECTED_VERSION:
                raise RuntimeError("Finalized reconciliation healthcheck differs")
            evidence["checks"]["finalize_twice"] = finalize_twice(
                first_must_be_idempotent=True
            )
            prove_post_finalize()
            record_post_finalize_checkpoint(checkpoint)
            cleanup_helper_terminal(hotfix_before)
            evidence["passed"] = True
            return 0

        resume_response, resume_before = call_helper(
            "resume_retained_contract", timeout=180
        )
        release.require_response(
            resume_response, "Physical retained backup/upload contract"
        )
        exact_resume_contract(resume_before, phase=retained_phase)
        evidence["checks"]["physical_retained_contract_before_commit"] = (
            resume_before
        )

        canonical_before = release.wordpress_post_snapshot(
            release.get_authenticated_post(client, CANONICAL_POST_ID)
        )
        canonical_before_sha = release.sha256_bytes(release.exact_json_bytes(canonical_before))
        if not secrets.compare_digest(canonical_before_sha, CANONICAL_REST_SHA256):
            raise RuntimeError("Same-schema canonical REST baseline changed before commit")
        storage_response, storage_before_payload = call_helper(
            release.CANONICAL_POST_STORAGE_VERIFY_ACTION, timeout=120
        )
        release.require_response(storage_response, "Canonical storage before resumed commit")
        storage_before = release.canonical_post_storage_comparison(
            storage_before_payload, CANONICAL_POST_ID
        )
        if (
            storage_before["state_phase"] != retained_phase
            or storage_before["unchanged"] is not True
            or storage_before["baseline"]["contract_sha256"] != CANONICAL_STORAGE_SHA256
        ):
            raise RuntimeError("Canonical raw storage differs before resumed commit")
        evidence["checks"]["canonical_before_commit"] = {
            "rest_sha256": canonical_before_sha,
            "storage": storage_before,
        }

        commit_extra = {
            "page_id": 0,
            "created_new": True,
            "post_password": post_password,
            "stage_title": str(stage_request["body"]["title"]),
            "stage_content": str(stage_request["body"]["content"]),
            "stage_excerpt": str(stage_request["body"]["excerpt"]),
        }
        stage_commit: dict[str, Any] = {}
        stage_commit_failures: list[dict[str, Any]] = []
        for attempt in range(1, 4):
            try:
                commit_response, candidate = call_helper(
                    "commit_external_stage", extra=commit_extra, timeout=180
                )
                if commit_response.status_code == 200:
                    stage_commit = exact_stage_commit(candidate)
                    stage_commit["driver_attempts"] = attempt
                    break
                stage_commit_failures.append(
                    exact_stage_commit_failure(candidate, attempt=attempt)
                )
            except requests.RequestException:
                stage_commit_failures.append(
                    {"attempt": attempt, "outcome": "response_lost"}
                )
        evidence["checks"]["external_stage_commit_failures"] = stage_commit_failures
        if not stage_commit:
            raise RuntimeError("Resumed external-stage commit did not reconcile")
        expected_meta_count = len(stage_request["body"]["meta"])
        if stage_commit.get("page_meta_key_count") != expected_meta_count:
            raise RuntimeError("Resumed stage meta-key count differs")
        evidence["checks"]["external_stage_commit"] = stage_commit

        status_response, status_ready = call_helper("status", timeout=60)
        release.require_response(status_response, "Retained page-ready status")
        exact_status(status_ready, phase="page_ready")
        inspect_response, inspect_ready = call_helper("inspect", timeout=60)
        release.require_response(inspect_response, "Retained page-ready inspect")
        exact_inspect(inspect_ready, phase="page_ready", lock_owned=True)
        resume_response, resume_ready = call_helper(
            "resume_retained_contract", timeout=180
        )
        release.require_response(
            resume_response, "Physical retained contract after stage commit"
        )
        exact_resume_contract(resume_ready, phase="page_ready")
        evidence["checks"]["physical_retained_contract_page_ready"] = resume_ready

        stage_record = release.get_authenticated_post(client, POST_ID)
        stage_readback = release.assert_einstein_stage_readback(
            stage_record, stage_request, post_password
        )
        page_url = safe_page_url(stage_record)
        evidence["checks"]["authenticated_stage_readback"] = stage_readback
        evidence["page_url"] = page_url
        evidence["checks"]["anonymous_private_surfaces"] = release.anonymous_einstein_probes(
            base_url, page_url, POST_ID, stage_request, post_password
        )

        if reusable_pre_finalize is not None:
            summary_path = output_dir / reusable_pre_finalize[
                "acceptance_summary_path"
            ]
            if not (
                retained_phase == "page_ready"
                and stage_commit["page_contract_sha256"]
                == reusable_pre_finalize["page_contract_sha256"]
                and page_url == reusable_pre_finalize["page_url"]
                and release.sha256_bytes(release.exact_json_bytes(stage_readback))
                == reusable_pre_finalize["stage_readback_sha256"]
                and summary_path.is_file()
                and not summary_path.is_symlink()
                and secrets.compare_digest(
                    sha256_path(summary_path),
                    reusable_pre_finalize["acceptance_summary_sha256"],
                )
            ):
                raise RuntimeError("Reusable page-ready checkpoint differs from live stage")
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            acceptance_proof = release.acceptance_summary_proof(
                summary, einstein_mode=True
            )
            if acceptance_proof != reusable_pre_finalize["acceptance_proof"]:
                raise RuntimeError("Reusable page-ready acceptance proof differs")
            secret_scan = release.assert_tree_has_no_secret_bytes(
                acceptance_dir, (post_password, wp_password, token)
            )
            evidence["checks"]["browser_acceptance"] = {
                "exit_code": 0,
                "proof": acceptance_proof,
                "secret_scan": secret_scan,
                "reused_immutable_checkpoint": True,
            }
        else:
            node = shutil.which("node")
            if not node:
                raise RuntimeError("Node.js is unavailable for live acceptance")
            acceptance_env = dict(os.environ)
            for secret_key in ("WP_APP_PASSWORD", "WP_USER", "WP_BASE_URL"):
                acceptance_env.pop(secret_key, None)
            acceptance_env.update(
                {
                    "SANDBOX_URL": page_url,
                    "SANDBOX_POST_PASSWORD": post_password,
                    "OUTPUT_DIR": str(acceptance_dir),
                    "EXPECTED_PLUGIN_VERSION": EXPECTED_VERSION,
                    "EXPECTED_PROJECT_CONTRACT_ID": release.EINSTEIN_PROJECT_CONTRACT_ID,
                    "EXPECTED_STAGE_POST_ID": str(POST_ID),
                }
            )
            acceptance = subprocess.run(
                [node, str(ACCEPTANCE_PATH)],
                cwd=REPO_ROOT,
                env=acceptance_env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=args.acceptance_timeout_seconds,
                check=False,
            )
            secret_scan = release.assert_tree_has_no_secret_bytes(
                acceptance_dir, (post_password, wp_password, token)
            )
            summary_path = acceptance_dir / "summary.json"
            summary = (
                json.loads(summary_path.read_text(encoding="utf-8"))
                if summary_path.is_file()
                else {}
            )
            acceptance_proof = release.acceptance_summary_proof(
                summary, einstein_mode=True
            )
            evidence["checks"]["browser_acceptance"] = {
                "exit_code": acceptance.returncode,
                "proof": acceptance_proof,
                "secret_scan": secret_scan,
                "stdout_tail": redactor.text(acceptance.stdout[-1200:]),
                "stderr_tail": redactor.text(acceptance.stderr[-1200:]),
                "reused_immutable_checkpoint": False,
            }
            if acceptance.returncode != 0 or acceptance_proof.get("passed") is not True:
                raise RuntimeError("Existing Einstein live acceptance v2 failed")

        final_record = release.get_authenticated_post(client, POST_ID)
        final_stage_readback = release.assert_einstein_stage_readback(
            final_record, stage_request, post_password
        )
        evidence["checks"]["final_authenticated_stage_readback"] = final_stage_readback
        storage_response, storage_final_payload = call_helper(
            release.CANONICAL_POST_STORAGE_VERIFY_ACTION, timeout=120
        )
        release.require_response(storage_response, "Canonical storage before finalization")
        storage_final = release.canonical_post_storage_comparison(
            storage_final_payload, CANONICAL_POST_ID
        )
        if (
            storage_final["state_phase"] != "page_ready"
            or storage_final["unchanged"] is not True
            or storage_final["baseline"]["contract_sha256"] != CANONICAL_STORAGE_SHA256
        ):
            raise RuntimeError("Canonical raw storage differs before finalization")
        canonical_final = release.wordpress_post_snapshot(
            release.get_authenticated_post(client, CANONICAL_POST_ID)
        )
        canonical_final_sha = release.sha256_bytes(release.exact_json_bytes(canonical_final))
        if not secrets.compare_digest(canonical_final_sha, CANONICAL_REST_SHA256):
            raise RuntimeError("Same-schema canonical REST snapshot changed before finalization")
        evidence["checks"]["canonical_before_finalize"] = {
            "rest_sha256": canonical_final_sha,
            "storage": storage_final,
        }
        evidence["checks"]["final_anonymous_private_surfaces"] = release.anonymous_einstein_probes(
            base_url, page_url, POST_ID, stage_request, post_password
        )

        health = public.get(
            f"{base_url}/wp-json/nadlan/v1/healthcheck",
            params={"cb": f"{RUN_ID}-final"},
            timeout=30,
        )
        health_version = release.find_health_version(health.json()) if health.status_code == 200 else ""
        if health.status_code != 200 or health_version != EXPECTED_VERSION:
            raise RuntimeError("Final healthcheck differs from pinned plugin version")
        evidence["checks"]["final_health"] = {
            "http_status": health.status_code,
            "version": health_version,
        }
        checkpoint = write_checkpoint(
            checkpoint_path,
            {
                "schema": CHECKPOINT_SCHEMA,
                "run_id": RUN_ID,
                "helper_id": HELPER_ID,
                "helper_sha256": patched_hash,
                "post_id": POST_ID,
                "page_url": page_url,
                "page_contract_sha256": stage_commit["page_contract_sha256"],
                "stage_readback_sha256": release.sha256_bytes(
                    release.exact_json_bytes(final_stage_readback)
                ),
                "acceptance_summary_path": "acceptance/summary.json",
                "acceptance_summary_sha256": sha256_path(summary_path),
                "acceptance_proof": acceptance_proof,
                "canonical_storage_sha256": CANONICAL_STORAGE_SHA256,
                "canonical_rest_sha256": CANONICAL_REST_SHA256,
                "plugin_digest": PLUGIN_DIGEST,
                "hotfix_id": HOTFIX_ID,
                "hotfix_sha256": HOTFIX_SHA256,
                "ready_for_finalize": True,
            },
        )
        evidence["checks"]["pre_finalize_checkpoint"] = {
            "path": str(checkpoint_path.relative_to(REPO_ROOT)),
            "contract_sha256": checkpoint["contract_sha256"],
        }
        evidence["checks"]["finalize_twice"] = finalize_twice(
            first_must_be_idempotent=False
        )
        prove_post_finalize()
        record_post_finalize_checkpoint(checkpoint)
        cleanup_helper_terminal(hotfix_before)
        evidence["passed"] = True
    except Exception as error:
        evidence["error"] = redactor.text(error)
    finally:
        if (
            evidence.get("passed") is not True
            and patched_hash
            and not helper_cleanup_proved
            and not cleanup_terminal_probe_started
        ):
            retention: dict[str, Any] = {"active_exact_helper_retained": False}
            try:
                retained_response = client.request(
                    "GET", f"code-snippets/v1/snippets/{HELPER_ID}", timeout=60
                )
                if retained_response.status_code == 200:
                    retained = release.observed_snippet(retained_response.json())
                    exact_identity = (
                        retained.get("id") == HELPER_ID
                        and retained.get("name") == HELPER_NAME
                        and retained.get("scope") == "global"
                        and retained.get("code_sha256") == patched_hash
                    )
                    if exact_identity and retained.get("active") is False:
                        try:
                            client.request(
                                "PUT",
                                f"code-snippets/v1/snippets/{HELPER_ID}/activate",
                                json_body={},
                                timeout=60,
                            )
                        except requests.RequestException:
                            pass
                        retained_response = client.request(
                            "GET",
                            f"code-snippets/v1/snippets/{HELPER_ID}",
                            timeout=60,
                        )
                        retained = (
                            release.observed_snippet(retained_response.json())
                            if retained_response.status_code == 200
                            else {}
                        )
                    retention = {
                        "active_exact_helper_retained": retained
                        == {
                            "id": HELPER_ID,
                            "name": HELPER_NAME,
                            "active": True,
                            "scope": "global",
                            "code_sha256": patched_hash,
                        }
                    }
                elif release.is_exact_missing_snippet_response(retained_response):
                    retention = {
                        "active_exact_helper_retained": False,
                        "helper_already_absent": True,
                    }
            except Exception as retention_error:
                retention = {
                    "active_exact_helper_retained": False,
                    "error": redactor.text(retention_error),
                }
            evidence["checks"]["failure_helper_retention"] = retention
        evidence["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        sanitized = redactor.value(evidence)
        serialized = json.dumps(sanitized, ensure_ascii=False, indent=2) + "\n"
        redactor.assert_absent(serialized)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"resume-4527b2-{invocation_slug}.json"
        if output_path.exists() or output_path.is_symlink():
            raise RuntimeError("Run evidence output path already exists")
        temp_path = output_path.with_suffix(".tmp")
        temp_path.write_text(serialized, encoding="utf-8")
        os.replace(temp_path, output_path)
        release.assert_tree_has_no_secret_bytes(
            output_dir, (post_password, wp_password, token)
        )
        print(
            json.dumps(
                {
                    "passed": sanitized.get("passed") is True,
                    "run_id": RUN_ID,
                    "page_url": sanitized.get("page_url", "") if sanitized.get("passed") else "",
                    "output": str(output_path),
                    "helper_450_absent": bool(
                        sanitized.get("checks", {}).get("helper_cleanup_last", {}).get("helper_id_absent")
                    ),
                    "hotfix_449_active": bool(
                        sanitized.get("checks", {}).get("helper_cleanup_last", {}).get("route_hotfix_449_unchanged_active")
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return 0 if evidence.get("passed") is True else 3


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise
    except Exception as fatal:
        print(
            json.dumps(
                {
                    "passed": False,
                    "error": type(fatal).__name__,
                    "message": "Pinned same-run resume failed before evidence finalization.",
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(4)
