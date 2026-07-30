from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "verify-plugin-release.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("verify_plugin_release", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class ResolveHealthVersionTests(unittest.TestCase):
    def test_resolves_legacy_literal(self) -> None:
        source = "'version' => '1.66.9',"
        self.assertEqual(
            VERIFY.resolve_health_version(source, "health", None),
            "1.66.9",
        )

    def test_resolves_bare_version_constant(self) -> None:
        source = "'version' => NADLAN_CONFIG_VERSION,"
        self.assertEqual(
            VERIFY.resolve_health_version(source, "health", "1.72.133"),
            "1.72.133",
        )

    def test_resolves_guarded_version_constant(self) -> None:
        source = (
            "'version' => defined( 'NADLAN_CONFIG_VERSION' ) "
            "? NADLAN_CONFIG_VERSION : 'unknown',"
        )
        self.assertEqual(
            VERIFY.resolve_health_version(source, "health", "1.72.133"),
            "1.72.133",
        )

    def test_rejects_unknown_expression(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                VERIFY.resolve_health_version(
                    "'version' => get_option( 'plugin_version' ),",
                    "health",
                    "1.72.133",
                )

    def test_rejects_constant_without_definition(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                VERIFY.resolve_health_version(
                    "'version' => NADLAN_CONFIG_VERSION,",
                    "health",
                    None,
                )


class UtopiaIntegrityPinParserTests(unittest.TestCase):
    def test_parses_all_twelve_raw_byte_pins(self) -> None:
        hashes = {
            "article_he": "1" * 64,
            "article_en": "2" * 64,
            "article_fr": "3" * 64,
            "article_ru": "4" * 64,
            "article_ar": "5" * 64,
            "model": "6" * 64,
            "exterior": "7" * 64,
            "interior": "8" * 64,
            "window_view": "9" * 64,
            "wellness": "a" * 64,
            "showroom_css": "b" * 64,
            "showroom_js": "c" * 64,
        }
        source = "\n".join(
            [
                f"'{lang}' => array( 'sha256' => '{hashes[f'article_{lang}']}', )"
                for lang in ("he", "en", "fr", "ru", "ar")
            ]
            + [
                f"'{key}' => array("
                f" 'path' => $root . '{key}',"
                f" 'sha256' => '{hashes[key]}', )"
                for key in (
                    "model",
                    "exterior",
                    "interior",
                    "window_view",
                    "wellness",
                    "showroom_css",
                    "showroom_js",
                )
            ]
        )
        self.assertEqual(VERIFY.parse_utopia_integrity_pins(source), hashes)


if __name__ == "__main__":
    unittest.main()
