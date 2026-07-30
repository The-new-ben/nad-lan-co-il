from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "build-plugin-zip.py"
SPEC = importlib.util.spec_from_file_location("build_plugin_zip_test_module", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)

from plugin_release_git import ReleaseInputError  # noqa: E402


class GitBlobZipBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.plugin = self.root / "plugins" / "nadlan-config"
        self.plugin.mkdir(parents=True)
        (self.root / "plugin-dist").mkdir()
        self.main = self.plugin / "nadlan-config.php"
        self.main.write_bytes(
            b"<?php\n/**\n * Plugin Name: Test\n * Version: 1.2.3\n */\n"
            b"define( 'NADLAN_CONFIG_VERSION', '1.2.3' );\n"
        )
        self.payload = self.plugin / "payload.txt"
        self.payload.write_bytes(b"alpha\nbeta\n")
        self.git("init", "-q")
        self.git("config", "user.email", "release-test@example.invalid")
        self.git("config", "user.name", "Release Test")
        self.git("config", "core.autocrlf", "true")
        self.git("add", "plugins/nadlan-config")
        self.git("commit", "-qm", "fixture")

        # Simulate a Windows checkout. Git normalizes this back to the same LF
        # index blob, so it is intentionally not semantic worktree drift.
        self.main.write_bytes(self.main.read_bytes().replace(b"\n", b"\r\n"))
        self.payload.write_bytes(b"alpha\r\nbeta\r\n")
        clean = self.run_git(
            "diff",
            "--quiet",
            "--",
            "plugins/nadlan-config",
            check=False,
        )
        self.assertEqual(clean.returncode, 0)
        self.assertIn(b"\r\n", self.payload.read_bytes())

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            ["git", *args],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=check,
        )

    def git(self, *args: str) -> None:
        self.run_git(*args)

    def test_crlf_checkout_cannot_reappear_in_zip(self) -> None:
        output = BUILD.build("1.2.3", self.root)
        with zipfile.ZipFile(output) as zf:
            payload = zf.read("nadlan-config/payload.txt")
            main = zf.read("nadlan-config/nadlan-config.php")
            info = zf.getinfo("nadlan-config/payload.txt")
        self.assertEqual(payload, b"alpha\nbeta\n")
        self.assertNotIn(b"\r\n", payload)
        self.assertNotIn(b"\r\n", main)
        self.assertEqual(info.date_time, BUILD.ZIP_TIMESTAMP)
        self.assertEqual(info.create_system, 3)
        self.assertEqual((info.external_attr >> 16) & 0xFFFF, 0o100644)

    def test_repeated_clean_build_is_byte_deterministic(self) -> None:
        first = BUILD.build("1.2.3", self.root)
        first_hash = hashlib.sha256(first.read_bytes()).hexdigest()
        first.unlink()
        second = BUILD.build("1.2.3", self.root)
        self.assertEqual(
            hashlib.sha256(second.read_bytes()).hexdigest(),
            first_hash,
        )

    def test_refuses_to_overwrite_release_artifact(self) -> None:
        BUILD.build("1.2.3", self.root)
        with self.assertRaises(BUILD.BuildError):
            BUILD.build("1.2.3", self.root)

    def test_rejects_unstaged_plugin_drift(self) -> None:
        self.payload.write_bytes(b"semantic drift\n")
        with self.assertRaises(ReleaseInputError):
            BUILD.build("1.2.3", self.root)

    def test_rejects_untracked_plugin_file(self) -> None:
        (self.plugin / "untracked.php").write_bytes(b"<?php\n")
        with self.assertRaises(ReleaseInputError):
            BUILD.build("1.2.3", self.root)

    def test_rejects_version_not_equal_to_indexed_header(self) -> None:
        with self.assertRaises(BUILD.BuildError):
            BUILD.build("1.2.4", self.root)


if __name__ == "__main__":
    unittest.main()
