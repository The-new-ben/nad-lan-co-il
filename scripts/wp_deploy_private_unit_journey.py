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
from urllib.parse import urlparse

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


def require_response(response: requests.Response, operation: str) -> dict[str, Any]:
    payload = response_payload(response)
    if response.status_code < 200 or response.status_code >= 300:
        code = str(payload.get("code") or "unknown_error")
        rolled_back = payload.get("data", {}).get("rolled_back") if isinstance(payload.get("data"), dict) else None
        suffix = f"; rolled_back={bool(rolled_back)}" if rolled_back is not None else ""
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
			if ( $target ) {
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
			if ( $target ) {
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
        return {
            "target_absent": not name_matches,
            "target_get_status": 404,
            "release_resource_cleanup_proved": True,
            "method": "already_absent",
        }

    target_response = client.request("GET", f"code-snippets/v1/snippets/{target_id}", timeout=60)
    target_already_absent = target_response.status_code == 404
    if target_already_absent:
        remaining = client.all_snippets()
        absent = all(
            int(row.get("id") or 0) != target_id and str(row.get("name") or "") != target_name
            for row in remaining
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
            {"id": cleanup_id, "name": cleanup_name, "code_sha256": cleanup_hash}
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
                        {"id": cleanup_id, "name": cleanup_name, "code_sha256": cleanup_hash}
                    )
            except Exception:
                if depth >= 3:
                    raise
        if cleanup_id is not None:
            cleanup_after = client.request("GET", f"code-snippets/v1/snippets/{cleanup_id}", timeout=60)
            if cleanup_after.status_code != 404:
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
    target_absent = all(
        int(row.get("id") or 0) != target_id and str(row.get("name") or "") != target_name
        for row in rows_after
    )
    cleanup_absent = all(
        int(row.get("id") or 0) != (cleanup_id or 0) and str(row.get("name") or "") != cleanup_name
        for row in rows_after
    )
    if not (
        target_after.status_code == 404
        and route_after.status_code == 404
        and target_absent
        and cleanup_absent
    ):
        raise RuntimeError("Independent helper hard-delete proof failed")
    return {
        "target_absent": True,
        "target_get_status": target_after.status_code,
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
    if not (
        0 <= main_position < success_health_position < phase_one_position < finally_position < phase_two_position
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
        "rollback_activation_contract": True,
        "secure_local_upload": True,
        "noncanonical_path_rejected": noncanonical_path_rejected,
        "canonical_sha_mismatch_rejected": canonical_sha_mismatch_rejected,
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
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "reports" / "private-unit-journey-release",
    )
    parser.add_argument(
        "--acceptance-script",
        type=Path,
        default=REPO_ROOT / "scripts" / "qa-private-unit-journey.mjs",
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
    acceptance_script = args.acceptance_script.resolve()
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

    file_env = read_env(args.env)
    merged_env = dict(file_env)
    merged_env.update({key: value for key, value in os.environ.items() if value})
    base_url_input = merged_env.get("WP_BASE_URL", "").rstrip("/")
    wp_user = merged_env.get("WP_USER", "")
    wp_password = merged_env.get("WP_APP_PASSWORD", "")
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

    run_id = f"unit-journey-{utc_slug()}-{secrets.token_hex(3)}"
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
    resources_finalized = False
    deployed = False
    page_url = ""
    before_plugin_contract: dict[str, Any] = {}
    created_cleanup_rows: list[dict[str, Any]] = []
    artifact_evidence: dict[str, Any] = {
        "mode": artifact_mode,
        "sha256": artifact_sha256,
    }
    if commit_sha:
        artifact_evidence["source_commit_sha"] = commit_sha
    result: dict[str, Any] = {
        "schema_version": 1,
        "run_id": run_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "target": {
            "site": base_url,
            "plugin_file": PLUGIN_FILE,
            "expected_version": str(args.expected_version),
            "source_post_id": SOURCE_POST_ID,
            "page_slug": PAGE_SLUG,
            "page_title": PAGE_TITLE,
            "project_display_name": PROJECT_DISPLAY_NAME,
        },
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

        if artifact_mode == "upload":
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

        deploy_started = True
        deploy_response, deploy = call_helper("deploy", timeout=360)
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
        for attempt in range(1, args.health_attempts + 1):
            status_response, status = call_helper("status", timeout=60)
            status_version = ""
            upload_temp_absent = False
            if status_response.status_code == 200 and isinstance(status.get("plugin"), dict):
                status_version = str(status["plugin"].get("version") or "")
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
                "upload_temp_absent": upload_temp_absent,
                "health_status": health_status,
                "health_version": health_version,
                "expected": status_version == str(args.expected_version)
                and upload_temp_absent
                and health_status == 200
                and health_version == str(args.expected_version),
            }
            health_checks.append(attempt_result)
            if attempt_result["expected"]:
                stable = True
                break
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
        summary_path = acceptance_dir / "summary.json"
        summary_payload: dict[str, Any] = {}
        if summary_path.is_file():
            try:
                loaded_summary = json.loads(summary_path.read_text(encoding="utf-8"))
                if isinstance(loaded_summary, dict):
                    summary_payload = loaded_summary
            except (OSError, ValueError):
                summary_payload = {}
        hard_failures = summary_payload.get("hardFailures")
        warnings = summary_payload.get("warnings")
        result["checks"]["browser_acceptance"] = {
            "exit_code": acceptance.returncode,
            "summary_json": str(summary_path),
            "summary_markdown": str(acceptance_dir / "summary.md"),
            "hard_failure_count": len(hard_failures) if isinstance(hard_failures, list) else None,
            "warning_count": len(warnings) if isinstance(warnings, list) else None,
            "stdout_tail": redactor.text(acceptance.stdout[-1200:]),
            "stderr_tail": redactor.text(acceptance.stderr[-1200:]),
        }
        if acceptance.returncode != 0 or not summary_payload or (
            isinstance(hard_failures, list) and hard_failures
        ):
            raise RuntimeError("Pre-finalize browser acceptance failed; release will roll back")

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
            if rollback_required:
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
                except Exception as rollback_error:
                    result["checks"]["failure_rollback"] = {
                        "confirmed": False,
                        "error": redactor.text(rollback_error),
                    }

            # Never discard a possibly required rollback backup when deployment
            # state cannot be established. Activation failures occur before
            # deploy_started and are safe to finalize without release state.
            safe_to_finalize = (
                not deploy_started
                or (status_confirmed and not rollback_required)
                or rollback_confirmed
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
                if cleanup_get.status_code == 404:
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
            for cleanup_row in created_cleanup_rows:
                try:
                    cleanup_get = client.request(
                        "GET",
                        f"code-snippets/v1/snippets/{int(cleanup_row['id'])}",
                        timeout=60,
                    )
                    cleanup_absent = cleanup_get.status_code == 404
                except Exception as cleanup_error:
                    cleanup_failure = cleanup_error
                    cleanup_absent = False
                if not cleanup_absent:
                    residual_cleanup_rows.append(int(cleanup_row["id"]))
            if residual_cleanup_rows:
                cleanup_failure = RuntimeError("Secondary cleanup helper absence could not be proved")

            helper_absent = False
            helper_get_status = 0
            route_after_status = 0
            snippet_count_after: int | None = None
            try:
                snippets_after = client.all_snippets()
                snippet_count_after = len(snippets_after)
                helper_absent = all(
                    (helper_id is None or int(row.get("id") or 0) != helper_id)
                    and str(row.get("name") or "") != helper_name
                    for row in snippets_after
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
                route_after = client.request(
                    "POST", route, json_body={"action": "inspect"}, timeout=60
                )
                route_after_status = route_after.status_code
            except Exception as cleanup_error:
                cleanup_failure = cleanup_error

            main_absence_proved = (
                helper_absent
                and helper_get_status == 404
                and route_after_status == 404
                and cleanup_proof is not None
                and cleanup_proof.get("release_resource_cleanup_proved") is True
            )
            if not main_absence_proved:
                cleanup_failure = RuntimeError("Main helper row or route absence could not be proved")
            if cleanup_proof is not None:
                cleanup_proof["secondary_helpers_created"] = len(created_cleanup_rows)
                cleanup_proof["secondary_helpers_absent"] = not residual_cleanup_rows
                cleanup_proof["main_helper_absent_from_collection"] = helper_absent
                cleanup_proof["main_helper_get_status"] = helper_get_status
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
