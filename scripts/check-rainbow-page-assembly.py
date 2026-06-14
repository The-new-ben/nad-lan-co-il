#!/usr/bin/env python3
"""Check Rainbow's public project-page assembly and SEO readiness.

Default mode is read-only and report-only. Use --strict when this checker is
part of a deploy gate; strict mode exits non-zero on any blocker.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Any


DEFAULT_BASE_URL = "https://nad-lan.co.il"
DEFAULT_PROJECT_SLUG = "rainbow-tel-aviv"
DEFAULT_POST_ID = 4464

KEYWORD_RULES = (
    ("למכירה", 3),
    ("מחיר", 8),
    ("שדה דב", 5),
)

PUBLIC_LEAK_PATTERNS = (
    "class=&quot;",
    "class =",
    "nlpf dl rdl",
    "Fatal error",
    "Warning:",
    "Notice:",
    "Stack trace",
)

MOJIBAKE_PATTERNS = (
    "×ž",
    "×“",
    "×”",
    "×œ",
    "Ã",
    "Â",
    "\ufffd",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_stack: list[str] = []
        self.current_h1: list[str] | None = None
        self.h1s: list[str] = []
        self.text_parts: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.meta_description = ""
        self.jsonld_raw: list[str] = []
        self.current_jsonld: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k.lower(): v or "" for k, v in attrs}
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "template"}:
            if tag == "script" and "application/ld+json" in attrs_dict.get("type", "").lower():
                self.current_jsonld = []
            self.skip_stack.append(tag)
            return
        if self.skip_stack:
            return
        if tag == "h1":
            self.current_h1 = []
        elif tag == "title":
            self.in_title = True
        elif tag == "meta" and attrs_dict.get("name", "").lower() == "description":
            self.meta_description = attrs_dict.get("content", "")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.skip_stack:
            if tag == "script" and self.current_jsonld is not None:
                self.jsonld_raw.append("".join(self.current_jsonld).strip())
                self.current_jsonld = None
            if tag == self.skip_stack[-1]:
                self.skip_stack.pop()
            return
        if tag == "h1" and self.current_h1 is not None:
            text = normalize_text(" ".join(self.current_h1))
            if text:
                self.h1s.append(text)
            self.current_h1 = None
        elif tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.current_jsonld is not None:
            self.current_jsonld.append(data)
            return
        if self.skip_stack:
            return
        if self.current_h1 is not None:
            self.current_h1.append(data)
        if self.in_title:
            self.title_parts.append(data)
        if data.strip():
            self.text_parts.append(data)


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Codex-Rainbow-QA/1.0"})
    with urllib.request.urlopen(req, timeout=45) as res:
        return res.read().decode("utf-8")


def fetch_json(url: str) -> Any:
    return json.loads(fetch_text(url))


def endpoint(base_url: str, path: str) -> str:
    return urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def meta_from_rest(base_url: str, post_id: int) -> dict[str, Any]:
    url = endpoint(base_url, f"/wp-json/wp/v2/nadlan_project/{post_id}?context=view&_fields=id,slug,meta,content,title")
    data = fetch_json(url)
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected WordPress REST response")
    return data


def collect_jsonld(raw_items: list[str]) -> tuple[list[str], list[dict[str, Any]], list[str]]:
    found: list[str] = []
    objects: list[dict[str, Any]] = []
    errors: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            objects.append(value)
            item_type = value.get("@type")
            if isinstance(item_type, str):
                found.append(item_type)
            graph = value.get("@graph")
            if isinstance(graph, list):
                for child in graph:
                    walk(child)
            for key in ("mainEntity", "itemListElement"):
                children = value.get(key)
                if isinstance(children, list):
                    for child in children:
                        walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for raw in raw_items:
        if raw == "":
            continue
        try:
            walk(json.loads(raw))
        except json.JSONDecodeError as exc:
            errors.append(str(exc))
    return found, objects, errors


def count_words(text: str) -> int:
    return len(re.findall(r"[\w\u0590-\u05ff]+", text, flags=re.UNICODE))


def check_page(base_url: str, slug: str, post_id: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    page_url = endpoint(base_url, f"/projects/{slug}/")
    html_text = fetch_text(page_url)
    parser = PageParser()
    parser.feed(html_text)
    visible_text = normalize_text(" ".join(parser.text_parts))
    title = normalize_text(" ".join(parser.title_parts))
    description = normalize_text(parser.meta_description)

    if len(parser.h1s) != 1:
        errors.append(f"expected exactly one visible H1, found {len(parser.h1s)}: {parser.h1s[:4]}")
    if "nadlan-guide" not in html_text or "nadlan-rainbow-seo-v1610-start" not in html_text:
        errors.append("nadlan-guide Rainbow SEO block marker missing from public HTML")
    if any(pattern in html_text for pattern in PUBLIC_LEAK_PATTERNS):
        errors.append("public HTML contains raw code/error/class leak pattern")
    if any(pattern in html_text for pattern in MOJIBAKE_PATTERNS):
        errors.append("public HTML contains mojibake/replacement pattern")

    word_count = count_words(visible_text)
    if word_count < 2500:
        errors.append(f"visible text too thin for flagship project page: {word_count} words")

    for keyword, minimum in KEYWORD_RULES:
        count = visible_text.count(keyword)
        if count < minimum:
            errors.append(f"keyword '{keyword}' count {count} < {minimum}")

    if "Rainbow" not in title or "שדה דב" not in title:
        errors.append(f"title missing Rainbow/Sde Dov signals: {title}")
    if "למכירה" not in title and "מחיר" not in title and "מחירים" not in title:
        errors.append(f"title is not transaction-led yet: {title}")
    if "Rainbow" not in description or "שדה דב" not in description:
        errors.append(f"meta description missing Rainbow/Sde Dov signals: {description}")
    if "מחיר" not in description and "מחירים" not in description:
        errors.append(f"meta description does not mention price: {description}")

    jsonld_types, jsonld_objects, jsonld_errors = collect_jsonld(parser.jsonld_raw)
    if jsonld_errors:
        errors.append("JSON-LD parse errors: " + "; ".join(jsonld_errors[:3]))
    for required_type in ("FAQPage", "ApartmentComplex", "BreadcrumbList"):
        if required_type not in jsonld_types:
            errors.append(f"missing JSON-LD type {required_type}; found {sorted(set(jsonld_types))}")

    apartment = next((item for item in jsonld_objects if item.get("@type") == "ApartmentComplex"), {})
    offer = apartment.get("offers", {}) if isinstance(apartment, dict) else {}
    amenities = apartment.get("amenityFeature", []) if isinstance(apartment, dict) else []
    same_as = apartment.get("sameAs", []) if isinstance(apartment, dict) else []
    if not isinstance(amenities, list) or len(amenities) < 5:
        errors.append(f"ApartmentComplex schema has too few amenities: {len(amenities) if isinstance(amenities, list) else 'invalid'}")
    if not isinstance(same_as, list) or len(same_as) < 2:
        errors.append(f"ApartmentComplex schema has too few official/reference links: {len(same_as) if isinstance(same_as, list) else 'invalid'}")
    if not isinstance(offer, dict) or offer.get("@type") != "AggregateOffer":
        errors.append("ApartmentComplex schema missing AggregateOffer")
    else:
        if not offer.get("lowPrice") or not offer.get("highPrice") or offer.get("priceCurrency") != "ILS":
            errors.append("AggregateOffer schema missing lowPrice/highPrice/ILS currency")

    faq_page = next((item for item in jsonld_objects if item.get("@type") == "FAQPage"), {})
    faq_entities = faq_page.get("mainEntity", []) if isinstance(faq_page, dict) else []
    if not isinstance(faq_entities, list) or len(faq_entities) < 4:
        errors.append(f"FAQPage schema has too few questions: {len(faq_entities) if isinstance(faq_entities, list) else 'invalid'}")

    health = fetch_json(endpoint(base_url, "/wp-json/nadlan/v1/healthcheck"))
    assembly = health.get("project_page_assembly", {}) if isinstance(health, dict) else {}
    for key in ("loaded", "rainbow_seed", "faq_meta", "price_meta"):
        if assembly.get(key) is not True:
            errors.append(f"healthcheck project_page_assembly.{key} is not true")

    rest = meta_from_rest(base_url, post_id)
    meta = rest.get("meta") if isinstance(rest.get("meta"), dict) else {}
    public_meta_present = sorted(key for key, value in meta.items() if str(value).strip() != "")

    print("# Rainbow page assembly check")
    print(f"URL: {page_url}")
    print(f"H1s: {len(parser.h1s)} -> {parser.h1s}")
    print(f"Visible words: {word_count}")
    print(f"Title: {title}")
    print(f"Meta description: {description}")
    print("Keyword counts: " + ", ".join(f"{keyword}={visible_text.count(keyword)}" for keyword, _ in KEYWORD_RULES))
    print("JSON-LD types: " + ", ".join(sorted(set(jsonld_types))))
    print("Health assembly: " + json.dumps(assembly, ensure_ascii=False, sort_keys=True))
    print(f"Schema amenities: {len(amenities) if isinstance(amenities, list) else 0}")
    print(f"Schema sameAs links: {len(same_as) if isinstance(same_as, list) else 0}")
    print(f"Schema FAQ questions: {len(faq_entities) if isinstance(faq_entities, list) else 0}")
    print("Public REST meta exposed: " + (", ".join(public_meta_present[:24]) if public_meta_present else "(none)"))
    if warnings:
        print()
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print()
        print("Errors:")
        for error in errors:
            print(f"- {error}")
    else:
        print()
        print("PASS: Rainbow page assembly checks passed.")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--project-slug", default=DEFAULT_PROJECT_SLUG)
    parser.add_argument("--post-id", type=int, default=DEFAULT_POST_ID)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on errors.")
    args = parser.parse_args()

    errors, _warnings = check_page(args.base_url, args.project_slug, args.post_id)
    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
