#!/usr/bin/env python3
"""Fail-closed diff checks for the governed Einstein release surface."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import PurePosixPath


TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".php",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}
EXACT_GOVERNED = {
    ".gitattributes",
    ".github/workflows/einstein-release-gates.yml",
    "plugin-dist/nadlan-config.json",
    "plugins/nadlan-config/nadlan-config.php",
    "plugins/nadlan-config/inc/flagship-surface.php",
    "scripts/ci/einstein_release_diff_gate.py",
    "scripts/templates/nadlan-unit-journey-deploy-helper.php.tpl",
    "scripts/wp_deploy_private_unit_journey.py",
}
PLACEHOLDER = re.compile(
    r"^(?:__[A-Z0-9_]+__|\$\{[A-Z0-9_]+\}|<[^>]+>)$", re.IGNORECASE
)
ASSIGNMENT = re.compile(
    r"(?P<key>\$?[A-Za-z_][A-Za-z0-9_$-]*|['\"][^'\"]+['\"]+)"
    r"\s*[:=]\s*(?P<quote>['\"])(?P<value>.*?)(?P=quote)"
)
ENV_ASSIGNMENT = re.compile(
    r"^\s*(?:export\s+|\$env:)?(?P<key>[A-Za-z_][A-Za-z0-9_]*)"
    r"\s*=\s*(?P<value>[^\s#'\"]+)\s*(?:#.*)?$",
    re.IGNORECASE,
)
AUTHORIZATION_BASIC = re.compile(
    r"(?i)\bauthorization\b[^\r\n]{0,48}\bbasic\s+[A-Za-z0-9+/=]{12,}"
)
KNOWN_SECRET = re.compile(
    r"(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
    r"(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}|"
    r"\bsk-[A-Za-z0-9_-]{20,}|"
    r"\bAKIA[0-9A-Z]{16}\b|"
    r"https?://[^\s/:]+:[^\s/@]+@)",
    re.IGNORECASE,
)


def run_bytes(args: list[str]) -> bytes:
    return subprocess.run(args, check=True, capture_output=True).stdout


def governed(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if normalized.startswith("./"):
        normalized = normalized[2:]
    lower = normalized.lower()
    if normalized in EXACT_GOVERNED:
        return True
    if lower.startswith("assets/projects/einstein-tower/"):
        return True
    if lower.startswith("docs/qa/einstein-tower-"):
        return True
    if lower.startswith("docs/wp-drafts/einstein-tower-"):
        return True
    if lower.startswith("plugins/nadlan-config/assets/flagship-v3/"):
        return True
    if lower.startswith("plugin-dist/nadlan-config-1.72.20") and lower.endswith(".zip"):
        return True
    return lower.startswith("scripts/") and "einstein" in lower


def governed_text(path: str) -> bool:
    lower = path.lower()
    return governed(path) and (
        PurePosixPath(lower).suffix in TEXT_SUFFIXES or lower.endswith(".php.tpl")
    )


def changed_paths(base: str) -> list[str]:
    raw = run_bytes(["git", "diff", "--name-only", "-z", base, "HEAD", "--"])
    return [item.decode("utf-8") for item in raw.split(b"\0") if item]


def head_blob(path: str) -> bytes | None:
    present = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{path}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if present.returncode != 0:
        return None
    return run_bytes(["git", "show", f"HEAD:{path}"])


def normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def sensitive_key(key: str) -> bool:
    value = normalized_key(key)
    if any(marker in value for marker in ("password", "secret", "credential", "apikey")):
        return True
    if "token" not in value:
        return False
    return not any(
        marker in value
        for marker in ("sha", "hash", "digest", "schema", "count", "name", "route")
    )


def literal_is_placeholder(value: str) -> bool:
    return not value or PLACEHOLDER.fullmatch(value.strip()) is not None


def credential_reason(line: str) -> str | None:
    if AUTHORIZATION_BASIC.search(line):
        return "literal Basic authorization"
    if KNOWN_SECRET.search(line):
        return "known secret-token shape"
    for match in ASSIGNMENT.finditer(line):
        key = match.group("key").strip("'\"")
        value = match.group("value").strip()
        if sensitive_key(key) and not literal_is_placeholder(value):
            suffix = line[match.end() :]
            if len(value) == 1 and re.fullmatch(
                r"\s*\*\s*[1-9][0-9]{0,3}\s*[,;]?\s*", suffix
            ):
                continue
            return f"literal assigned to sensitive key {key}"
    match = ENV_ASSIGNMENT.match(line)
    if (
        match
        and match.group("key") == match.group("key").upper()
        and sensitive_key(match.group("key"))
    ):
        value = match.group("value").strip()
        if "(" not in value and not literal_is_placeholder(value) and not re.match(
            r"^(?:\$|process\.env|os\.environ|getenv\()", value
        ):
            return f"unquoted literal assigned to sensitive key {match.group('key')}"
    return None


def added_lines(base: str, paths: list[str]) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for path in paths:
        diff = run_bytes(
            ["git", "diff", "--unified=0", "--no-ext-diff", base, "HEAD", "--", path]
        ).decode("utf-8", errors="replace")
        for line in diff.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                found.append((path, line[1:]))
    return found


def self_test() -> None:
    governed_yes = (
        ".gitattributes",
        ".github/workflows/einstein-release-gates.yml",
        "docs/qa/einstein-tower-extra.md",
        "docs/wp-drafts/einstein-tower-extra.json",
        "scripts/build-einstein-flagship-public-release.mjs",
        "plugins/nadlan-config/assets/flagship-v3/contracts/registry.json",
        "plugin-dist/nadlan-config-1.72.208.zip",
    )
    governed_no = ("scripts/deploy_drafts.js", "docs/qa/other.md", "README.md")
    if not all(governed(path) for path in governed_yes) or any(
        governed(path) for path in governed_no
    ):
        raise RuntimeError("Governed path matcher self-test failed")

    rejected = (
        "WP_APP_" + "PASS" + "WORD" + chr(61) + "abcdefghijklmnop",
        'const WP_APP_' + 'PASS' + 'WORD ' + chr(61) + ' "' + 'abcdefghijklmnop";',
        'const cfg = { wpApp' + 'Pass' + 'word' + chr(58) + ' "' + 'abcdefghijklmnop" };',
        "$WP_APP_" + "PASS" + "WORD " + chr(61) + " '" + "abcdefghijklmnop';",
        '"Author' + 'ization": "Ba' + 'sic YWJjZGVmZ2hpamtsbW5vcA=="',
        "helper" + "To" + "ken" + chr(58) + " '" + "abcdefghijklmnop'",
        "-----BEGIN " + "PRIVATE KEY-----",
        "const x = 'github_" + "pat_abcdefghijklmnopqrstuvwxyz';",
    )
    allowed = (
        "WP_APP_PASSWORD=${WP_APP_PASSWORD}",
        'const cfg = { wpAppPassword: "__WP_APP_PASSWORD__" };',
        "$expected_token = __EXPECTED_TOKEN_JSON__;",
        'token_sha256: "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"',
        'password: ""',
        "to" + 'ken: "' + "a" + '" * 64',
    )
    if any(credential_reason(line) is None for line in rejected) or any(
        credential_reason(line) is not None for line in allowed
    ):
        raise RuntimeError("Credential detector fixture self-test failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test()
    if args.self_test and not args.base:
        print(json.dumps({"passed": True, "fixtures": 13}, separators=(",", ":")))
        return 0
    if not args.base:
        raise RuntimeError("--base is required outside standalone self-test")

    paths = [path for path in changed_paths(args.base) if governed(path)]
    bad_lf = []
    for path in paths:
        if not governed_text(path):
            continue
        blob = head_blob(path)
        if blob is not None and b"\r" in blob:
            bad_lf.append(path)
    if bad_lf:
        raise RuntimeError("Governed Git blobs are not canonical LF: " + ", ".join(bad_lf))

    credential_hits = []
    for path, line in added_lines(args.base, paths):
        reason = credential_reason(line)
        if reason:
            credential_hits.append(f"{path}: {reason}")
    if credential_hits:
        raise RuntimeError("Credential literals detected:\n" + "\n".join(credential_hits))

    print(
        json.dumps(
            {
                "passed": True,
                "governed_changed_files": len(paths),
                "lf_checked_files": sum(governed_text(path) for path in paths),
                "credential_hits": 0,
            },
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
