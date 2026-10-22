# -*- coding: utf-8 -*-
"""Greece data for the Instruments tools grbuy / grgv / gryield (HAD-592, the page loop, 22.10.2026). Built ONLY from
docs/research/2026-10-22-greece/facts.json (every number there has its source and as_of; facts.md has the full citations).
Writes plugins/nadlan-config/assets/instruments/data/greece.json (compact). Regions: Spitogatos asking prices Q2 2026 (ReDataset
Jan-May 2026 where Spitogatos has no level); gross yields only where a source gives one (Spitogatos price-to-rent 2025 for
Attica, Global Property Guide for Thessaloniki), never invented. Golden-visa tier by the 2024 law: Attica, Thessaloniki regional
unit, Mykonos, Santorini and every island over 3,100 inhabitants = EUR 800K (so Crete, Rhodes and Corfu are 800K); the rest of
Greece 400K.
  python tools/instruments/build_greece_data.py"""
import io, json, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = json.load(io.open(os.path.join(REPO, "docs", "research", "2026-10-22-greece", "facts.json"), encoding="utf-8"))
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "greece.json")
pc = F["purchase_costs"]; en = F["annual_holding_costs"]["enfia"]; P = F["prices"]
ask = {a["area"]: a for a in P["asking_price_eur_m2"]}
spy = P["gross_yields"]["spitogatos_price_to_rent_2025"]["areas"]; gpg = P["gross_yields"]["gpg"]


def A(area):
    a = ask[area]; return a["eur_m2"], a.get("yoy"), a["period"]


# id, Hebrew label, asking source area, gv tier, border permit (non-EU), STR freeze 2026, yield (value, label of source)
REG = [
    ("athens-center", "אתונה, מרכז העיר", "Athens Centre", 800, False, "part", (spy["Athens Centre"]["gross_yield"], "Spitogatos 2025")),
    ("athens-south", "אתונה, פרברי הדרום (גליפדה, ווּלה)", "Athens South suburbs", 800, False, False, (spy["Southern Suburbs"]["gross_yield"], "Spitogatos 2025")),
    ("athens-north", "אתונה, פרברי הצפון", "Athens North suburbs", 800, False, False, (spy["Northern Suburbs"]["gross_yield"], "Spitogatos 2025")),
    ("athens-west", "אתונה, פרברי המערב", "Athens West suburbs", 800, False, False, (spy["Western Suburbs"]["gross_yield"], "Spitogatos 2025")),
    ("piraeus", "פיראוס", "Piraeus", 800, False, False, (spy["Piraeus"]["gross_yield"], "Spitogatos 2025")),
    ("vouliagmeni", "וּוּליאגמני (הריביירה)", "Vouliagmeni (top of Attica)", 800, False, False, None),
    ("thessaloniki", "סלוניקי", "Thessaloniki municipality", 800, False, "part", (gpg["thessaloniki_avg"], "Global Property Guide 2026")),
    ("kalamaria", "קלמריה (סלוניקי)", "Kalamaria (top of Thessaloniki)", 800, False, False, None),
    ("halkidiki", "חלקידיקי", "Halkidiki (all)", 400, False, False, None),
    ("chania", "חאניה, כרתים", "Chania regional unit", 800, False, False, None),
    ("heraklion", "הרקליון, כרתים", "Heraklion regional unit", 800, False, False, (gpg["heraklion_avg"], "Global Property Guide 2026")),
    ("rethymno", "רתימנו, כרתים", "Rethymno regional unit", 800, False, False, None),
    ("corfu", "קורפו", "Corfu prefecture", 800, False, False, None),
    ("rhodes", "רודוס", "Rhodes", 800, True, False, None),
    ("mykonos", "מיקונוס", "Mykonos", 800, False, False, None),
    ("santorini", "סנטוריני", "Santorini (Thira)", 800, True, False, None),
]
regions = []
for rid, he, area, gv, border, freeze, y in REG:
    m2, yoy, per = A(area)
    regions.append({"id": rid, "he": he, "m2": m2, "yoy": yoy, "per": per, "src": ask[area]["provider"], "gv": gv, "border": border,
                    "freeze": freeze, "yld": round(y[0], 4) if y else None, "ysrc": y[1] if y else None})

ex = en["examples_computed"]
out = {
    "key": "greece", "built": F["_meta"]["as_of"],
    "buy": {
        "tt": pc["transfer_tax"]["effective_rate"], "tt_base": "higher of price or objective value", "tt_payer": "buyer",
        "tt_noneu": pc["transfer_tax_non_eu_proposed"]["effective_rate"], "tt_noneu_from": pc["transfer_tax_non_eu_proposed"]["effective_for"].split(" ")[-1],
        "tt_noneu_consult": pc["transfer_tax_non_eu_proposed"]["consultation_until"],
        "vat": pc["vat_new_build"]["rate"], "vat_susp_until": pc["vat_new_build"]["suspension_in_force_until"],
        "vat_ext_planned": pc["vat_new_build"]["planned_extension_until"],
        "notary": [[b["upto"], b["rate"]] for b in pc["notary_fee_scale"]["brackets"]], "notary_fixed": pc["notary_fee_scale"]["fixed_eur"],
        "svc_vat": pc["notary_fee_scale"]["vat"], "cad": pc["cadastre_fee"]["proportional"], "cad_fixed": pc["cadastre_fee"]["fixed_eur"][0],
        "cad_mortgage": pc["cadastre_fee"]["mortgage_registration"]["proportional"],
        "lawyer": pc["lawyer_fee"]["default_for_calculator"], "lawyer_range": pc["lawyer_fee"]["typical_range"],
        "agent": pc["agent_fee"]["typical_buyer_side"], "engineer": pc["engineer_legality_certificate"]["electronic_building_id_cost_eur"],
    },
    "enfia": {"zones": [[z["zone_price_max"], z["base"]] for z in en["zones"]], "age": en["age_coef"], "floor": en["floor_coef"],
              "gamma": [[b["upto"], b["rate"]] for b in en["value_tax_section_gamma"]["brackets_on_value_of_each_right"]],
              "gamma_from": en["value_tax_section_gamma"]["applies_if_total_property_value_over"],
              "sur": [[b["upto"], b["pct"]] for b in en["surcharge_on_main_tax_section_e"]["bands"]],
              "sur_from": en["surcharge_on_main_tax_section_e"]["applies_if_total_value_over"],
              "ins": [en["insurance_discount"]["rate_if_total_residential_value_le_500k"], en["insurance_discount"]["rate_above"]]},
    "rent": {"br": [[b["to"], b["rate"]] for b in F["rental_income_tax_greece_individuals"]["brackets_income_from_2026"]], "ded": 0.05},
    "str": {"fee": F["short_term_rental"]["climate_resilience_fee_eur_per_night"]["str_unit"], "biz_from": 3, "vat": F["short_term_rental"]["vat_rate_business"]},
    "il": {"flat": F["israel_tax"]["foreign_rent_15pct_track"]["rate"], "cgt": F["israel_tax"]["capital_gain_foreign_property"]["rate_real_gain"],
           "report_over": F["israel_tax"]["annual_report_triggers_tax_year_2025"]["foreign_assets_over_ils"]},
    "gv": {"t": [g["min_eur"] for g in F["golden_visa"]["thresholds"]], "m2": 120, "fee_main": F["golden_visa"]["fees"]["main_applicant_eur"],
           "fee_family": F["golden_visa"]["fees"]["family_member_eur"], "years": F["golden_visa"]["permit_years"], "str_fine": F["golden_visa"]["short_term_rental_ban"]["fine_eur"],
           "months": F["golden_visa"]["processing_months"]},
    "mort": {"ltv": F["mortgages"]["greek_bank_non_resident"]["ltv_max"], "rates": F["mortgages"]["greek_bank_non_resident"]["fixed_rates_published"],
             "term_il": F["mortgages"]["greek_bank_non_resident"]["term_years_israeli_residents"], "avg_float": F["mortgages"]["market_rates"]["bog_avg_new_housing_loans_floating_aug_2026"]},
    "regions": regions,
    "sources": [
        {"label": "AADE, מס העברה", "url": pc["transfer_tax"]["sources"][0]["source"]},
        {"label": "משרד האוצר היווני, תקציב 2027 (15.10.2026)", "url": "https://minfin.gov.gr/wp-content/uploads/2026/10/Greece_DBP_2027_final.pdf"},
        {"label": "Spitogatos, מחירים מבוקשים רבעון 2 2026", "url": "https://www.ot.gr/2026/07/11/oikonomia/akinita/spitogatos-pos-diamorfothikan-oi-times-polisis-kai-enoikiasis-katoikion-to-v%CE%84-trimino-2026/"},
        {"label": "רשות המסים בישראל, מדריך 2025", "url": F["israel_tax"]["foreign_rent_15pct_track"]["sources"][0]["source"]},
    ],
}
io.open(OUT, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print("greece.json", os.path.getsize(OUT), "bytes,", len(regions), "regions")
for r in regions: print("  ", r["id"], r["m2"], r["yoy"], r["gv"], "border" if r["border"] else "", "freeze:%s" % r["freeze"] if r["freeze"] else "", r["yld"])
