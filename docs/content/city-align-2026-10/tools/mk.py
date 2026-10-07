# -*- coding: utf-8 -*-
"""Builder helpers for docs/content/city-align-2026-10/<slug>.align-edits.json (schema of docs/content/sde-dov-prices-2026-10/align-edits.json
plus a claims inventory). Usage inside a per-page builder script:

    from mk import Page
    P = Page("ashkelon-apartment-prices")
    P.claim("p@4300", "דירת 3 חדרים סביב 1.0-1.35 מיליון", "sale", "CONFLICT", "edit 1", rooms="3", official="rooms.3.latest 918,100 (1-3.2026)")
    n = P.edit(old, new, ["rooms.3.latest"], "CONFLICT", "why ...")
    P.table(anchor, new_html, keys, verdict, why)      # whole <table> element located by a unique anchor string inside it
    P.write()
"""
import io, json, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
OUTDIR = os.path.join(REPO, "docs", "content", "city-align-2026-10")
CITIES = os.path.join(REPO, "scripts", "project-stage", "price_guide", "cities")
VERDICTS = ("CONFLICT", "STALE", "UNSOURCED", "CONSISTENT", "WORDING")
MEASURES = ("sale", "sale_avg", "sale_nb", "sale_street", "sale_new_used", "deal", "per_m2", "rent", "yield", "change", "macro", "count", "other")


class Page:
    def __init__(self, slug):
        self.slug = slug
        self.page = json.load(open(os.path.join(HERE, "pages", slug + ".json"), encoding="utf-8"))
        self.c = self.page["content"]["rendered"]
        self.d = json.load(open(os.path.join(CITIES, slug + ".json"), encoding="utf-8"))
        self.edits, self.claims = [], []
        self._text = self.c  # text after the edits so far (for sequential matching)

    # ---- claims ---------------------------------------------------------------------------------------------------
    def claim(self, where, quote, measure, verdict, action, rooms="", official="", figures=1, note=""):
        assert verdict in VERDICTS[:4], verdict
        assert measure in MEASURES, measure
        self.claims.append({"id": len(self.claims) + 1, "where": where, "quote": quote, "measure": measure, "rooms": str(rooms),
                            "figures": figures, "official": official, "verdict": verdict, "action": action, "note": note})

    # ---- edits ----------------------------------------------------------------------------------------------------
    def _add(self, e):
        e["n"] = len(self.edits) + 1
        self.edits.append(e)
        return e["n"]

    def edit(self, old, new, keys, verdict, why, replace_all=False, expect=None, kept=None, tier=1):
        assert verdict in VERDICTS, verdict
        c = self._text.count(old)
        if replace_all:
            assert c == expect, f"replace_all expected {expect}, found {c}: {old[:80]!r}"
            self._text = self._text.replace(old, new)
        else:
            assert c == 1, f"old matches {c} times: {old[:100]!r}"
            self._text = self._text.replace(old, new)
        e = {"page_id": self.page["id"], "url": self.page["link"], "field": "content", "old": old, "new": new, "source_keys": keys,
             "audit_verdict": verdict, "verdict": verdict, "why": why, "matches_in_live": c, "tier": tier}
        if replace_all:
            e["replace_all"] = True
            e["expect_matches"] = expect
        if kept:
            e["kept_numbers"] = kept
        return self._add(e)

    def table_html(self, anchor):
        i = self._text.find(anchor)
        assert i >= 0 and self._text.count(anchor) == 1, f"anchor count {self._text.count(anchor)}: {anchor}"
        a, z = self._text.rfind("<table", 0, i), self._text.find("</table>", i)
        return self._text[a:z + len("</table>")]

    def table(self, anchor, new, keys, verdict, why, kept=None, tier=1):
        old = self.table_html(anchor)
        assert self._text.count(old) == 1
        self._text = self._text.replace(old, new)
        e = {"page_id": self.page["id"], "url": self.page["link"], "field": "content", "old": old, "new": new, "source_keys": keys,
             "audit_verdict": verdict, "verdict": verdict, "why": why, "matches_in_live": 1, "tier": tier, "spans_tags": True, "anchor": anchor}
        if kept:
            e["kept_numbers"] = kept
        return self._add(e)

    def find(self, start, end=None):
        """exact substring of the current text from `start` up to and including `end` (both must be unique from start)."""
        i = self._text.find(start)
        assert i >= 0 and self._text.count(start) == 1, f"start count {self._text.count(start)}: {start[:60]!r}"
        if end is None:
            return start
        j = self._text.find(end, i)
        assert j >= 0, f"end not found: {end[:60]!r}"
        return self._text[i:j + len(end)]

    # ---- output ---------------------------------------------------------------------------------------------------
    def write(self, notes=""):
        counts = {v: 0 for v in VERDICTS[:4]}
        figs = {v: 0 for v in VERDICTS[:4]}
        for cl in self.claims:
            counts[cl["verdict"]] += 1
            figs[cl["verdict"]] += int(cl.get("figures") or 1)
        J = {
            "generated": time.strftime("%d.%m.%Y").lstrip("0").replace(".0", "."),
            "page": {"id": self.page["id"], "slug": self.slug, "link": self.page["link"], "modified": self.page.get("modified")},
            "source": f"GET https://nad-lan.co.il/wp-json/wp/v2/pages?slug={self.slug}&_fields=id,link,title,content,modified (content.rendered), public, retrieved {self.page.get('retrieved_utc')} UTC, {len(self.c):,} characters. The price-list section (<section id=\"nlpg\">, the [nadlan_price_guide] shortcode), <script> and <style> are outside the audit.",
            "facts": f"scripts/project-stage/price_guide/cities/{self.slug}.json (official medians from data.nadlan.gov.il; source_keys are JSON paths in that file: rooms.<k>.latest, rooms.<k>.year_ago, rooms.<k>.change_pct, rooms.<k>.quarters[<q>], israel.<k>, neighbourhoods[<name>].rooms.<k>; 'page' = a number kept from the page's own text)",
            "apply_rules": [
                "Apply in the listed order on the RAW content (context=edit). Every \"old\" matches content.rendered exactly once at its turn (matches_in_live), except \"replace_all\" entries, which match exactly \"expect_matches\" times.",
                "Edits with \"spans_tags\": true replace a whole <table> element: if \"old\" does not match the raw content exactly (raw line breaks between tags can differ), locate the single <table> element that contains \"anchor\" and replace that element with \"new\".",
                "Every other old string sits inside one paragraph, list item or table cell and holds no HTML entity. The rendered content shows straight quotes (ש\"ח, מ\"ר) and no texturized characters, so raw and rendered text are expected to be identical inside a paragraph; re-check each old against the raw content right before applying.",
                "tier 1 = sale-price alignment with the official list (conflicts, stale and unsourced sale figures); tier 2 = rent or other figures with no dated source. Applying tier 1 alone is valid (tier 2 olds do not overlap tier 1 results).",
                "All or nothing per page: if any old does not match, write nothing. Re-fetch the page first; another session may have edited it. Data only: nothing here was applied.",
            ],
            "claims_summary": {"claims": counts, "figures": figs, "edits": len(self.edits), "tier1": sum(1 for e in self.edits if e.get("tier", 1) == 1),
                               "tier2": sum(1 for e in self.edits if e.get("tier", 1) == 2)},
            "notes": notes,
            "claims": self.claims,
            "edits": self.edits,
        }
        os.makedirs(OUTDIR, exist_ok=True)
        fn = os.path.join(OUTDIR, self.slug + ".align-edits.json")
        io.open(fn, "w", encoding="utf-8", newline="\n").write(json.dumps(J, ensure_ascii=False, indent=1) + "\n")
        print(f"wrote {fn}: {len(self.edits)} edits, claims {counts}")
        return fn
