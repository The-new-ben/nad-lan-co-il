# -*- coding: utf-8 -*-
"""Offline check of madlan_rewrite.json against madlan_posts.json.

For every post: each "old" must occur exactly once in the original field, the olds of one
field must not overlap, and applying them in order must succeed (each old still found exactly
once at the moment it is applied). Meta entries must carry the md5 of the value they replace.
After applying everything, no field may match (?i)מדלן|madlan.
Extra guards: HTML tag count unchanged, no em/en dash introduced, digit tokens unchanged
(except where listed in ALLOWED_NUMBER_DELTA)."""
import difflib, hashlib, io, json, os, re, sys
from collections import Counter

if (sys.stdout.encoding or "").lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
POSTS = json.load(open(os.path.join(HERE, "madlan_posts.json"), encoding="utf-8"))
REW = json.load(open(os.path.join(HERE, "madlan_rewrite.json"), encoding="utf-8"))
R = re.compile(r"(?i)מדלן|madlan")
NUM = re.compile(r"\d+(?:[.,]\d+)*")
# 4555: 'לספירה של 470 הדירות' repeats the 470 shown one row above, and the removed Madlan-only
#       source entry 'מדלן מודיעין מכבים רעות, נקרא ביום 5.6.2026;' takes one read-date with it.
ALLOWED_NUMBER_DELTA = {4555: Counter({"470": 1, "5.6.2026": 1})}


def occ(T, s):
    out, i = [], T.find(s)
    while i != -1:
        out.append(i)
        i = T.find(s, i + 1)
    return out


def changed_chars(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return sum((i2 - i1) + (j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")


problems = []
non_unique = 0
by_post = {}
for e in REW["posts"]:
    by_post.setdefault(str(e["id"]), []).append(e)
meta_by_post = {}
for e in REW["meta"]:
    meta_by_post.setdefault(str(e["id"]), []).append(e)

rows = []
total_before = total_after = 0
for pid, v in POSTS.items():
    fields = {f: v[f] or "" for f in ("title", "excerpt", "content")}
    metas = {k: (mv["value"] or "") for k, mv in v["meta"].items()}
    before = sum(len(R.findall(t)) for t in fields.values()) + sum(len(R.findall(t)) for t in metas.values())
    new_fields = dict(fields)
    chg = 0
    n_rep = 0
    for f in fields:
        entries = [e for e in by_post.get(pid, []) if e["field"] == f]
        if not entries:
            continue
        T = fields[f]
        spans = []
        for e in entries:
            o = occ(T, e["old"])
            if len(o) != 1:
                non_unique += 1
                problems.append(f"{pid}/{f}: old occurs {len(o)} times: {e['old'][:80]!r}")
                continue
            spans.append((o[0], o[0] + len(e["old"])))
        spans.sort()
        for (a1, b1), (a2, b2) in zip(spans, spans[1:]):
            if a2 < b1:
                problems.append(f"{pid}/{f}: overlapping olds at {a1}-{b1} and {a2}-{b2}")
        cur = T
        for e in entries:
            o = occ(cur, e["old"])
            if len(o) != 1:
                problems.append(f"{pid}/{f}: at apply time old occurs {len(o)} times: {e['old'][:80]!r}")
                continue
            cur = cur[:o[0]] + e["new"] + cur[o[0] + len(e["old"]):]
            chg += changed_chars(e["old"], e["new"])
            n_rep += 1
            if len(e["old"]) < 25 or len(e["old"]) > 300:
                problems.append(f"{pid}/{f}: old length {len(e['old'])} outside 25..300")
        # guards
        if T.count("<") != cur.count("<") or T.count(">") != cur.count(">"):
            problems.append(f"{pid}/{f}: tag count changed")
        for dash in ("—", "–"):
            if cur.count(dash) > T.count(dash):
                problems.append(f"{pid}/{f}: {dash!r} introduced")
        for art in ("  ", " ,", " .", " ;", ",,", "( ", " )"):
            if cur.count(art) > T.count(art):
                problems.append(f"{pid}/{f}: spacing artifact {art!r} introduced")
        lds_before = re.findall(r'<script type="application/ld\+json">(.*?)</script>', T, re.S)
        lds_after = re.findall(r'<script type="application/ld\+json">(.*?)</script>', cur, re.S)
        for i, (lb, la) in enumerate(zip(lds_before, lds_after)):
            try:
                json.loads(lb)
            except Exception:
                continue  # was not valid JSON before either
            try:
                json.loads(la)
            except Exception as ex:
                problems.append(f"{pid}/{f}: JSON-LD block {i} no longer parses: {ex}")
        nb, na = Counter(NUM.findall(T)), Counter(NUM.findall(cur))
        delta = (na - nb) + (nb - na)
        allowed = ALLOWED_NUMBER_DELTA.get(int(pid), Counter())
        if delta != allowed:
            problems.append(f"{pid}/{f}: digit tokens changed: added {dict(na - nb)} removed {dict(nb - na)}")
        new_fields[f] = cur
    new_metas = dict(metas)
    for e in meta_by_post.get(pid, []):
        k = e["key"]
        if hashlib.md5(metas[k].encode("utf-8")).hexdigest() != e["old_md5"] or v["meta"][k]["md5"] != e["old_md5"]:
            problems.append(f"{pid}/meta {k}: old_md5 mismatch")
        chg += changed_chars(metas[k], e["new"])
        new_metas[k] = e["new"]
        n_rep += 1
        if "—" in e["new"] and "—" not in metas[k]:
            problems.append(f"{pid}/meta {k}: em dash introduced")
    after = sum(len(R.findall(t)) for t in new_fields.values()) + sum(len(R.findall(t)) for t in new_metas.values())
    total_before += before
    total_after += after
    rows.append((pid, v["type"], v["status"], before, after, n_rep, chg, v["title"][:48]))

print(f"{'post':>5} {'type':<15} {'status':<8} {'before':>6} {'after':>5} {'edits':>5} {'chars':>6}  title")
for r in rows:
    print(f"{r[0]:>5} {r[1]:<15} {r[2]:<8} {r[3]:>6} {r[4]:>5} {r[5]:>5} {r[6]:>6}  {r[7]}")
print()
print(f"posts checked: {len(rows)}  replacement entries: {len(REW['posts'])}  meta entries: {len(REW['meta'])}")
print(f"occurrences before: {total_before}")
print(f"remaining after: {total_after}")
print(f"non-unique old strings: {non_unique}")
print(f"other problems: {len(problems)}")
for p in problems:
    print("  PROBLEM:", p)
sys.exit(0 if (total_after == 0 and non_unique == 0 and not problems) else 1)
