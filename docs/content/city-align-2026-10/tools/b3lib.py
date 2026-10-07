# -*- coding: utf-8 -*-
"""Helpers for the TIER-3 builders (listing-site rents under the CEO rule of 7.10.2026).

DATA ONLY. A builder module b3_<slug>.py defines build(P) and calls P.edit(...) / P.table(...) / P.delete_para(...); b_tier3_ceo.py loads the
live page (tier 1 and tier 2 are live), applies the edits in order to a copy, and appends them to docs/content/city-align-2026-10/<slug>.align-edits.json
as "tier": 3 entries (n continuing the numbering).

Actions (ceo_action): replaced = an official CBS value (city + size group) now stands there, with its quarter and source_url;
                      removed  = the number is gone, the sentence / cell stays (qualitative text kept only where no number is needed);
                      deleted  = the sentence, row, column or paragraph is gone because it has no value without the number.
"""
import io, json, os, re, sys
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.dirname(HERE)
CBS = json.load(io.open(os.path.join(HERE, "cbs_rent_2026_q2.json"), encoding="utf-8"))
RENT_URL = CBS["urls"]["table_he_pdf"]
CBS_NAME = "הלשכה המרכזית לסטטיסטיקה"
Q2 = "ברבעון השני של 2026 (אפריל עד יוני)"
GROUP_HE = {"1-2": "1 עד 2 חדרים", "2.5-3": "2.5 עד 3 חדרים", "3.5-4": "3.5 עד 4 חדרים", "4.5+": "4.5 חדרים ומעלה"}
ACTION_WORD = {"A": "replaced", "B": "removed", "C": "deleted"}


def r0(v):
    """CBS one-decimal average -> whole shekels, half up (the page text rule of tools/cbs_rent_2026_q2.json)"""
    return f"{int(Decimal(str(v)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)):,}"


def cbs(city_he, grp="total"):
    row = CBS["rows"][city_he]
    return row["total"] if grp == "total" else row["groups"][grp]


def c(city_he, grp="total"):
    """whole-shekel text of a CBS figure"""
    v = cbs(city_he, grp)
    assert v is not None, (city_he, grp)
    return r0(v)


def key(city_he, grp="total"):
    return f"cbs_rent[{city_he}].{grp}.q2_2026"


def raw_risk(old, spans_tags):
    r = []
    if '"' in old:
        r.append("straight double quote")
    if "'" in old:
        r.append("apostrophe")
    if "–" in old:
        r.append("en dash")
    if "\n" in old:
        r.append("line break")
    if "  " in old:
        r.append("double space")
    if spans_tags:
        r.append("whole table: apply via anchor")
    elif "<" in old:
        r.append("contains tags")
    return r


# ---- table helpers (same as the tier-2 builder) -----------------------------------------------------------------------
def parse_table(h):
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", h, re.S)
    cells = [re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S) for r in rows]
    return cells[0], cells[1:]


def table_fmt(old):
    attr = ' dir="rtl"' if old.startswith('<table dir="rtl"') else ""
    m = re.match(r"<table[^>]*>(\s*)<thead", old)
    return attr, m.group(1)


def table_html(head, body, fmt):
    attr, sep = fmt

    def tr(cs, tag):
        return f"<tr{attr}>" + sep + sep.join(f"<{tag}{attr}>{x}</{tag}>" for x in cs) + sep + "</tr>"
    return (f"<table{attr}>" + sep + f"<thead{attr}>" + sep + tr(head, "th") + sep + "</thead>" + sep + f"<tbody{attr}>" + sep
            + sep.join(tr(r, "td") for r in body) + sep + "</tbody>" + sep + "</table>")


def rebuild(old, head=None, body=None):
    """rebuild a table with the page's own markup style; head/body default to the current ones"""
    h, rows = parse_table(old)
    return table_html(head if head is not None else h, body if body is not None else rows, table_fmt(old))


class P3:
    def __init__(self, slug, page_json, live_text, n_start):
        self.slug = slug
        self.J = page_json
        self.page_id = page_json["page"]["id"]
        self.url = page_json["page"]["link"]
        self.text = live_text
        self.edits = []
        self.n = n_start

    # ---- locating exact strings in the CURRENT text (after the earlier tier-3 edits) -----------------------------------
    def sub(self, start, end=None):
        """exact substring from `start` up to and including `end`; `start` must be unique in the current text"""
        assert self.text.count(start) == 1, f"[{self.slug}] start count {self.text.count(start)}: {start[:70]!r}"
        i = self.text.find(start)
        if end is None:
            return start
        j = self.text.find(end, i)
        assert j >= 0, f"[{self.slug}] end not found: {end[:70]!r}"
        return self.text[i:j + len(end)]

    def element(self, phrase, tag="p"):
        """the whole <tag ...>...</tag> element that contains `phrase` (unique); returns the exact string"""
        assert self.text.count(phrase) == 1, f"[{self.slug}] phrase count {self.text.count(phrase)}: {phrase[:70]!r}"
        i = self.text.find(phrase)
        a = self.text.rfind(f"<{tag}", 0, i)
        z = self.text.find(f"</{tag}>", i)
        assert a >= 0 and z >= 0
        return self.text[a:z + len(f"</{tag}>")]

    def table_html(self, anchor):
        assert self.text.count(anchor) == 1, f"[{self.slug}] anchor count {self.text.count(anchor)}: {anchor[:70]!r}"
        i = self.text.find(anchor)
        a, z = self.text.rfind("<table", 0, i), self.text.find("</table>", i)
        return self.text[a:z + len("</table>")]

    # ---- recording -------------------------------------------------------------------------------------------------------
    def _record(self, old, new, action, note, why, keys, kept, url, spans_tags=False, anchor=None):
        e = {"page_id": self.page_id, "url": self.url, "field": "content", "old": old, "new": new, "source_keys": keys,
             "audit_verdict": "UNSOURCED", "verdict": "UNSOURCED", "why": why, "matches_in_live": 1, "tier": 3, "n": self.n}
        if spans_tags:
            e["spans_tags"] = True
            e["anchor"] = anchor
        e["raw_risk"] = raw_risk(old, spans_tags)
        if kept:
            e["kept_numbers"] = kept
        e["ceo_action"] = ACTION_WORD[action]
        e["ceo_note"] = note
        if url:
            e["source_url"] = url
        self.edits.append(e)
        self.n += 1
        return e["n"]

    def edit(self, old, new, action, note, why, keys=None, kept=None, url=None):
        assert action in "ABC"
        assert self.text.count(old) == 1, f"[{self.slug}] old matches {self.text.count(old)}: {old[:90]!r}"
        assert (action == "A") == bool(url), f"[{self.slug}] source_url only on replacements: {note[:60]}"
        self.text = self.text.replace(old, new)
        return self._record(old, new, action, note, why, keys or ["page"], kept, url)

    def delete_para(self, phrase, note, why, tag="p", keys=None):
        old = self.element(phrase, tag)
        return self.edit(old, "", "C", note, why, keys)

    def table(self, anchor, fn, action, note, why, keys=None, kept=None, url=None):
        assert action in "ABC"
        assert (action == "A") == bool(url), f"[{self.slug}] source_url only on replacements: {note[:60]}"
        old = self.table_html(anchor)
        new = fn(old)
        assert new != old
        self.text = self.text.replace(old, new)
        return self._record(old, new, action, note, why, keys or ["page"], kept, url, spans_tags=True, anchor=anchor)


# ---- Hebrew phrase helpers ----------------------------------------------------------------------------------------------
def by_size(city, cur='ש"ח', groups=("1-2", "2.5-3", "3.5-4", "4.5+")):
    """'3,119 ש"ח לדירות של 1 עד 2 חדרים, 3,906 ... ו-6,239 ש"ח לדירות של 4.5 חדרים ומעלה' (groups the CBS did not publish are skipped)"""
    parts = [f"{c(city, g)} {cur} לדירות של {GROUP_HE[g]}" for g in groups if cbs(city, g) is not None]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " ו-" + parts[-1]


def keys_all(city, groups=("total", "1-2", "2.5-3", "3.5-4", "4.5+")):
    return [key(city, g) for g in groups if cbs(city, g) is not None]


def table_cell_swap(old, col, repl, head=None):
    """rebuild `old` with column `col` of every body row set by repl(row_cells)->str (None keeps it); `head` is the new header text of that column"""
    h, rows = parse_table(old)
    new_rows = []
    for r in rows:
        r = list(r)
        v = repl(r)
        if v is not None:
            r[col] = v
        new_rows.append(r)
    if head is not None:
        h = list(h)
        h[col] = head
    return table_html(h, new_rows, table_fmt(old))
