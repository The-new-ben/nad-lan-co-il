# -*- coding: utf-8 -*-
"""HAD-768: builds plugins/nadlan-config/assets/forms/forms.json, the data of /forms/ (the life of a building), from:
  - forms-inventory.json + media.json: the state's form files (gov.il) and their copies in our Media Library (byte-checked);
  - lifecycle/A..D-*.json: the four research bands (approvals, reports, fees, deadlines, rights) with sources;
  - curate.json: the stage texts, the roles, the related pages on the site and any per-item correction (hand-written).
Every item keeps its sources; an item with no source is dropped and listed. Long dashes are replaced by a colon or a comma.
  python -I docs/research/2026-11-17-gov-forms/build_forms_data.py"""
import glob, json, os, re, sys

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "forms", "forms.json")
sys.stdout.reconfigure(encoding="utf-8")
inv = json.load(open(os.path.join(H, "forms-inventory.json"), encoding="utf-8"))
media = json.load(open(os.path.join(H, "media.json"), encoding="utf-8")) if os.path.exists(os.path.join(H, "media.json")) else {}
cur = json.load(open(os.path.join(H, "curate.json"), encoding="utf-8"))
ACC = "2026-11-17"


def clean(s):
    if s is None:
        return ""
    if isinstance(s, dict):
        s = s.get("text") or s.get("he") or s.get("value") or ""
    if isinstance(s, (list, tuple)):
        s = " ".join(str(x) for x in s if x)
    s = str(s).replace("הממשק המקוון", "רישוי זמין").replace("—", ",").replace("–", "-").replace(" ,", ",")
    return re.sub(r"\s+", " ", s).strip()


def slug(s):
    s = re.sub(r"[^A-Za-z0-9\-]+", "-", str(s)).strip("-").lower()
    return s or "x"


ROLE = {"buying": ["buyer"], "selling": ["owner"], "inheriting": ["owner"], "mortgage": ["buyer", "owner"], "leasehold": ["owner", "buyer"],
        "building": ["dev"], "condominium": ["committee", "owner"], "renting": ["owner"]}
items, dropped, used_files = [], [], set()


def file_of(lp):
    if not lp:
        return None
    m = media.get(lp.replace("\\", "/"))
    return m if m and m.get("byte_check") == "OK" else None


# ---------------------------------------------------------------- the state's forms
for e in inv:
    fol = e.get("local_folder") or ""
    rule = cur["form_stage"].get(e.get("form_number") or "", None) or cur["form_stage"].get(e.get("original_filename") or "", None) or cur["folder_stage"].get(fol)
    if not rule:
        dropped.append(("no stage", e.get("form_number"), e.get("official_name_he")))
        continue
    m = file_of(e.get("local_path"))
    alt = [file_of(a.get("local_path")) for a in (e.get("additional_files") or [])]
    alt = [a for a in alt if a]
    if not m and alt:
        m, alt = alt[0], alt[1:]
    src = [{"url": u, "title": t} for u, t in ((e.get("service_page_url"), "עמוד השירות ב-gov.il"), (e.get("listing_page_url"), "רשימת הטפסים ב-gov.il"), (e.get("direct_file_url"), "הקובץ המקורי ב-gov.il")) if u]
    num = e.get("form_number") or ""
    shown_num = num if re.match(r"^\d{3,5}[א-ת]?$", num) else ""
    roles = sorted({r for s in (e.get("life_situations") or []) for r in ROLE.get(s, [])} | set(cur.get("form_roles", {}).get(fol, [])))
    it = {"id": "f-" + slug(num or e.get("original_filename") or str(e.get("id"))), "stage": rule, "kind": "form", "title": clean(e.get("official_name_he")),
          "authority": clean(e.get("agency")), "what": clean(e.get("purpose_he")), "roles": roles, "official": e.get("service_page_url") or e.get("listing_page_url") or "",
          "sources": src}
    if (e.get("online_filing") or {}).get("exists") and (e.get("online_filing") or {}).get("url"):
        it["online"] = e["online_filing"]["url"]
    for k in ("deadline", "fee"):
        v = e.get(k)
        if isinstance(v, dict) and v.get("source") and v["source"] not in [x["url"] for x in src]:
            src.append({"url": v["source"], "title": "מקור למועד או לאגרה (gov.il)"})
    if e.get("deadline"):
        it["when"] = clean(e["deadline"])
    if e.get("fee"):
        it["cost"] = clean(e["fee"])
    if m:
        ext = (e.get("file_type") or m["url"].rsplit(".", 1)[-1]).lower()
        it["form"] = {"file": m["url"], "ext": ext, "size": m["bytes"], "num": shown_num, "name": clean(e.get("official_name_he")),
                      "mime": {"pdf": "application/pdf", "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "doc": "application/msword"}.get(ext, "application/octet-stream")}
        if alt:
            it["form"]["alt"] = [{"file": a["url"], "ext": a["url"].rsplit(".", 1)[-1].lower(), "size": a["bytes"]} for a in alt]
        used_files.add(m["url"])
    if num in cur.get("days", {}):
        it["days"], it["dayFrom"] = cur["days"][num]
    items.append(it)

# ---------------------------------------------------------------- the four research bands
def pick(d, *keys):
    for k in keys:
        if d.get(k):
            return d[k]
    return ""


for path in sorted(glob.glob(os.path.join(H, "lifecycle", "*.json"))):
    band = os.path.basename(path)[0]
    raw = json.load(open(path, encoding="utf-8"))
    raw = raw.get("items", raw) if isinstance(raw, dict) else raw
    for r in raw:
        title = clean(pick(r, "title", "title_he", "name"))
        srcs = [s for s in (r.get("sources") or []) if isinstance(s, dict) and s.get("url")]
        if not title or not srcs:
            dropped.append(("no source" if title else "no title", band, title))
            continue
        st_txt = clean(pick(r, "stage", "stage_he"))
        stage = None
        for hay in (st_txt, title):
            for k, v in cur["band_stage"][band]:
                if re.search(k, hay):
                    stage = v
                    break
            if stage:
                break
        stage = stage or cur["band_default"][band]
        kind = clean(pick(r, "kind", "type")).lower() or "check"
        kind = cur["kind_alias"].get(kind, kind)
        it = {"id": slug(band + "-" + str(pick(r, "id") or len(items))), "stage": stage, "kind": kind, "title": title,
              "authority": clean(pick(r, "authority", "authority_he")), "basis": clean(pick(r, "legal_basis", "basis", "law")),
              "what": clean(pick(r, "what", "what_he", "description_he", "description")), "who": clean(pick(r, "who", "who_he")),
              "when": clean(pick(r, "when", "when_he", "when_and_duration", "when_how_long", "timing", "deadline")), "cost": clean(pick(r, "cost", "fee", "official_cost")),
              "expert": clean(pick(r, "expert_note", "expert_note_he", "expert")), "pitfall": clean(pick(r, "pitfall", "pitfall_he")),
              "official": pick(r, "official_url", "official_page_url", "official_page", "url"), "roles": cur["band_roles"][band],
              "sources": [{"url": s["url"], "title": clean(s.get("title") or s["url"])} for s in srcs]}
        if not it["official"] and isinstance(r.get("official_form"), dict) and r["official_form"].get("url"):
            it["official"] = r["official_form"]["url"]
        if re.search(r"partial|חלקי", clean(r.get("verification"))) or re.search(r"^weak|secondary|press|blocked|snippet", clean(r.get("source_quality")), re.I) or "search_snippet" in clean(r.get("evidence")):
            it["partial"] = True
        it = {k: v for k, v in it.items() if v not in ("", None, [])}
        items.append(it)

# ---------------------------------------------------------------- corrections, related pages, order
for it in items:
    fix = cur.get("item_fix", {}).get(it["id"])
    if fix:
        it.update(fix)
    for k in ("title", "what", "expert", "pitfall"):
        if k in it:
            assert "—" not in it[k] and "–" not in it[k], it["id"]
seen = set()
for it in items:
    while it["id"] in seen:
        it["id"] += "-2"
    seen.add(it["id"])
order = {s["id"]: i for i, s in enumerate(cur["stages"])}
korder = list(cur["kinds"].keys())
items.sort(key=lambda x: (order.get(x["stage"], 99), korder.index(x["kind"]) if x["kind"] in korder else 99))
for it in items:
    if it["kind"] not in cur["kinds"]:
        cur["kinds"][it["kind"]] = it["kind"]
data = {"updated": ACC, "updated_he": "17.11.2026", "checked_he": "17.11.2026", "stages": cur["stages"], "roles": cur["roles"], "kinds": cur["kinds"],
        "fairness": cur["fairness"], "facts": cur.get("facts", []), "items": items}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(data, open(OUT, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, separators=(",", ":"))
by = {}
for it in items:
    by[it["stage"]] = by.get(it["stage"], 0) + 1
print(f"forms.json: {len(items)} items, {sum(1 for i in items if i.get('form'))} with a file, {len(used_files)} files used | by stage {by}")
print(f"dropped {len(dropped)}:", dropped[:20])
