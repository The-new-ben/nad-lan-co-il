# -*- coding: utf-8 -*-
"""HAD-712, the French Kikar page (post 8116) after its own search research (docs/research/2026-11-11-kikar-search/lang-fr.md,
11.11.2026). Ben's word through the Kikar session (11.11.2026, late evening): English and French only, French by French search intent.
What French searchers bring that the page did not answer in their terms (autocomplete fr/il, two hand searches on google.fr):
  - euros: the French agencies on page one (BARNES, immobilier-telaviv, Le Figaro Propriétés) and Google's own answer print prices
    in euros beside shekels. Ben approved an approximate euro figure next to the shekel price on the language pages (25.10.2026):
    the shekel stays the price; the conversion is marked approximate with the Bank of Israel rate and its date. The rate is the site's
    own file assets/instruments/data/boi-fx.json (EUR 3.4844 on 23.10.2026, read live on 11.11.2026).
  - "vente appartement tel aviv particulier": the towers are sold by their owners, not a developer; the page now says so in those words.
  - "location appartement tel aviv longue durée": the rent paragraph names it.
No FAQ answer changes (so no schema release). Title and H1 untouched. Anchored on the LIVE text, pinned md5, backup before, read-back
after; dry by default.   python scripts/kikar/had712_fr_intent.py [--go]"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
PID, SLUG, PIN = 8116, "hamedina-fr", "9f86e97a8e59ab4bc13f30e3a7fe5c0b"  # written by had712_lang.py fr, 11.11.2026 18:57 local
EUR, EUR_DATE = 3.4844, "23 octobre 2026"
assert abs(9.58 / EUR - 2.75) < 0.006 and abs(10.63 / EUR - 3.05) < 0.006 and abs(10 / EUR - 2.87) < 0.006


def _fr(s):  # "~" is a no-break space; a no-break space before ; : ? ! and inside « »
    s = s.replace("~", "\xa0")
    for p in (";", ":", "?", "!"):
        s = s.replace(" " + p, "\xa0" + p)
    return s.replace("« ", "«\xa0").replace(" »", "\xa0»")


SWAPS = [(_fr(a), _fr(b)) for a, b in [
    # 1. the opening: the deal range with its approximate euro value
    ("En 2024, trois ventes publiées se sont échelonnées de 9,58 à 10,63 M₪.",
     "En 2024, trois ventes publiées se sont échelonnées de 9,58 à 10,63 M₪, soit environ 2,75 à 3,05 M€ au cours de la Banque d’Israël du " + EUR_DATE + "."),
    # 2. the prices chapter: how the euro figures are made
    ("Une cession de droits exige, elle, de regarder ce qui reste à payer pour obtenir l’appartement achevé.</p>",
     "Une cession de droits exige, elle, de regarder ce qui reste à payer pour obtenir l’appartement achevé.</p>"
     "<p>Les prix sont fixés et payés en shekels. Les montants en euros sur cette page sont indicatifs : ils utilisent le cours représentatif "
     "de la Banque d’Israël du " + EUR_DATE + " (1~€ = 3,4844~₪), auquel 10~M₪ représentent environ 2,87~M€. Le montant en euros change avec le cours.</p>"),
    # 3. the sale chapter: a sale between private parties
    ("Les propriétaires revendent généralement par l’intermédiaire d’agents immobiliers.",
     "Les propriétaires revendent généralement par l’intermédiaire d’agents immobiliers. Il s’agit donc de ventes entre particuliers : le vendeur est le propriétaire de l’appartement, et non un promoteur."),
    # 4. rent: long-term letting
    ("envisage de louer son appartement,", "envisage de louer son appartement en location longue durée,"),
]]

if __name__ == "__main__":
    GO = "--go" in sys.argv
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h712f"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
    s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % PID)
    assert s == 200 and g["slug"] == SLUG, (s, g.get("slug"))
    raw = g["content"]["raw"]
    now = hashlib.md5(raw.encode("utf-8")).hexdigest()
    if now != PIN:
        raise SystemExit("the live post changed since it was read (%s, modified %s)" % (now[:10], g["modified"]))
    new = raw
    for a, b in SWAPS:
        if new.count(a) != 1:
            raise SystemExit("anchor x%d: %s" % (new.count(a), a[:80]))
        new = new.replace(a, b)
    assert new.count("<h2>") == raw.count("<h2>") and new.count("<h3>") == raw.count("<h3>")
    # the FAQ section must be untouched (its schema is post meta)
    f0, f1 = raw[raw.index('id="nlws-faq"'):], new[new.index('id="nlws-faq"'):]
    assert f0 == f1, "the FAQ changed"
    print("[plan] fr post %d: %d changes; %d -> %d chars" % (PID, len(SWAPS), len(raw), len(new)))
    if not GO:
        io.open(os.path.join(HERE, "_had712_fr_intent_preview.html"), "w", encoding="utf-8", newline="").write(new)
        sys.exit(0)
    bk = os.path.join(REPO, "docs", "qa", "had-712")
    stamp = time.strftime("%Y%m%dT%H%M%S")
    io.open(os.path.join(bk, "backup-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
    s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
    assert s1 in (200, 201), (s1, str(r1)[:300])
    s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % PID)
    ok = r["content"]["raw"] == new
    res = {"lang": "fr", "post": PID, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(),
           "read_back_equal": ok, "modified": r.get("modified"), "what": "French intent"}
    json.dump({"stamp": stamp, "result": res}, open(os.path.join(bk, "result-fr-intent-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
    if not ok:
        sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": raw})
        raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
    print("[done] fr post %d written and read back (%s)" % (PID, stamp))
