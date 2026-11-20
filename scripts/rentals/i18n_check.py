# -*- coding: utf-8 -*-
"""Rentals i18n gate (HAD-383): he and en must hold the same keys, every key the
JS uses must exist, every dynamic family must be complete, and the Hebrew must
pass the language-DNA blacklist. Exit 1 on any failure."""
import json, re, sys, pathlib
A = pathlib.Path(__file__).resolve().parents[2] / "plugins/nadlan-config/assets/rentals"
he = json.load(open(A / "i18n/he.json", encoding="utf-8"))
en = json.load(open(A / "i18n/en.json", encoding="utf-8"))
bad = []
for part in ("ui", "msg"):
    a, b = set(he[part]), set(en[part])
    for k in sorted(a - b): bad.append("en missing %s.%s" % (part, k))
    for k in sorted(b - a): bad.append("he missing %s.%s" % (part, k))
src = "".join(open(A / f, encoding="utf-8").read() for f in ("rm-core.js", "rm-views.js", "rm-drawers.js", "rm-portal.js", "rm-import.js") if (A / f).exists())
used = set(re.findall(r'\bt\(\s*"([a-z0-9_]+)"', src)) | set(re.findall(r'N\.t\(\s*"([a-z0-9_]+)"', src))
for m in re.findall(r'N\.tn\(\s*"([a-z0-9_]+)"', src): used |= {m + "_one", m + "_many"}
used |= set(re.findall(r'\?\s*"([a-z_]+)"\s*:\s*"([a-z_]+)"', src) and [])
FAM = {
 "nav_": "today properties people money repairs leasing docs reports settings more label",
 "st_": "ok due late vacant ending notmine", "kind_": "tenant prospect guarantor vendor coowner other charge payment expense income",
 "cat_": "rent deposit arnona vaad water electric gas repair insurance mortgage tax fee other", "m_": "transfer standing cheque bit paybox cash card other",
 "ls_": "open paid partial pending deposited bounced void", "ts_": "new scheduled progress waiting done cancelled",
 "tc_": "general plumbing electric ac appliance boiler roof mold locks pests paint other", "dk_": "all lease protocol id payslip bank receipt invoice insurance nesach photo plan cheque other",
 "ak_": "boiler ac panel water_meter gas fridge oven washer dishwasher heater shutter", "dir_": "north south east west ne nw se sw",
 "stage_": "new contacted viewing applied approved signed lost", "seg_": "tenant prospect guarantor vendor all", "mtab_": "ledger cheques expenses pnl cpi tax",
 "trade_": "plumbing electric ac boiler locks paint general appliance roof mold pests", "ev_": "note call visit msg_in msg_out sign doc_new link_new link_revoke export delete",
 "plan_": "free pro business", "plan_lead_": "free pro business", "rep_": "owner tenant vendor", "new_": "tenant prospect guarantor vendor coowner other contact",
 "att_": "late due ended ending option cheque sec unsigned vacant repair_urgent repair_over repair repair_new confirm applicant tax", "cap_": "line over need_rent",
}
for pre, names in FAM.items():
    for n in names.split(): used.add(pre + n)
for k in sorted(x for x in used if not x.endswith("_")):
    if k not in he["ui"]: bad.append("missing key %s" % k)
for k in ("hello rent_reminder renewal portal_invite sign_invite apply_invite vendor_dispatch ticket_update owner_quick pay_bit pay_bank st_new st_scheduled st_progress st_waiting st_done st_cancelled").split():
    if k not in he["msg"]: bad.append("missing msg %s" % k)
BLACK = ["ממשק", "המערכת", "הפלטפורמה", "דמו", "הדגמה", "טכנולוגיה", "אינטראקטיבי", "רספונסיבי", "סימולציה", "בקרוב", "פרוטוטייפ", "פיילוט", "אטלס", "מנגנון", "שכבה", "סכמטי", "—", "–"]
for part in ("ui", "msg"):
    for k, v in he[part].items():
        for w in BLACK:
            if w in v: bad.append("blacklist %r in he.%s.%s" % (w, part, k))
    for k, v in en[part].items():
        for w in ("—", "–"):
            if w in v: bad.append("dash in en.%s.%s" % (part, k))
print("keys he:", len(he["ui"]), "en:", len(en["ui"]), "used:", len(used))
print("\n".join(bad) if bad else "OK: parity, coverage and blacklist clean")
sys.exit(1 if bad else 0)
