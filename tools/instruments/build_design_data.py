"""Build plugins/nadlan-config/assets/instruments/data/design.json for the apartment-design tools (HAD-707, 11.11.2026).

One source for every number the design tools show:
  - docs/research/2026-11-10-apartment-designer/prices-items/price-ranges.json  (items: furniture, kitchen, finishes, systems)
  - docs/research/2026-11-10-apartment-designer/prices-items/designer-fees.json  (designer, styling and plan fees)
  - RULES below: the physical and ergonomic numbers (clearances, lumens, paint coverage, waste), each with its basis and kind:
      "standard" = a published guideline or official figure, "thumb" = a common rule of thumb (said so on the page),
      "assumption" = our own modelling choice (documented in docs/design-lab/apartment-designer/tools/NOTES.md).

Owner rules enforced here: no site name and no URL ever reaches the public file (checked, the build fails otherwise); prices
stay ranges with their unit, VAT status, number of sources and confidence; the month the prices were read is stated.

Run from the repo root:  python tools/instruments/build_design_data.py
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RES = os.path.join(ROOT, 'docs', 'research', '2026-11-10-apartment-designer', 'prices-items')
OUT = os.path.join(ROOT, 'plugins', 'nadlan-config', 'assets', 'instruments', 'data', 'design.json')

RULES = {
    # ---- living room and walkways ----
    'walk_main_cm': {'v': 90, 'kind': 'thumb', 'he': 'מעבר נוח בין רהיטים', 'basis': 'Common interior planning rule (Neufert, Architects\' Data: main circulation about 90 cm).'},
    'walk_min_cm': {'v': 60, 'kind': 'thumb', 'he': 'מעבר צר אבל אפשרי', 'basis': 'Common interior planning rule (a single person passing sideways needs about 60 cm).'},
    'sofa_table_gap_cm': {'v': 45, 'kind': 'thumb', 'he': 'בין הספה לשולחן הסלון', 'basis': 'Common rule of thumb: 40 to 50 cm between a sofa and its coffee table, reachable while seated.'},
    'wall_margin_cm': {'v': 5, 'kind': 'assumption', 'he': 'מרווח מהקיר', 'basis': 'Our choice: 5 cm of play between a sofa and a side wall so it can be pushed in.'},
    'door_margin_cm': {'v': 2, 'kind': 'assumption', 'he': 'מרווח במעבר בפתח', 'basis': 'Our choice: 2 cm of play when carrying an item through a door opening.'},
    # ---- rugs ----
    'rug_under_sofa_cm': {'v': 20, 'kind': 'thumb', 'he': 'השטיח נכנס מתחת לרגליים הקדמיות', 'basis': 'Common styling rule: the front legs of the sofa stand on the rug, about 15 to 20 cm in.'},
    'rug_side_overhang_cm': {'v': 15, 'kind': 'thumb', 'he': 'השטיח בולט מכל צד של הספה', 'basis': 'Common styling rule: the rug extends 15 to 20 cm past each end of the sofa.'},
    'rug_wall_margin_cm': {'v': 30, 'kind': 'thumb', 'he': 'רצפה גלויה בין השטיח לקיר', 'basis': 'Common styling rule seen in search answers (11.11.2026): 15 to 50 cm of floor between rug and wall; we use 30.'},
    'rug_sizes_cm': {'v': [[120, 170], [160, 230], [200, 290], [240, 340], [300, 400]], 'kind': 'thumb', 'he': 'מידות שטיח מוכנות', 'basis': 'The ready-made sizes sold in Israeli shops; 200 x 290 is priced in our data as "200 x 290 or so".'},
    # ---- dining ----
    'seat_width_cm': {'v': 60, 'kind': 'standard', 'he': 'רוחב מקום לסועד ליד שולחן מלבני', 'basis': 'Neufert, Architects\' Data: 60 cm of table edge per diner.'},
    'seat_round_cm': {'v': 65, 'kind': 'thumb', 'he': 'מקום לסועד על היקף שולחן עגול', 'basis': 'Rule of thumb: on a round table the place is measured on the edge, so a little more than 60 cm.'},
    'table_depth_cm': {'v': 90, 'kind': 'thumb', 'he': 'עומק שולחן אוכל', 'basis': 'Common dining-table depth 80 to 100 cm; we use 90.'},
    'chair_wall_cm': {'v': 81, 'kind': 'standard', 'he': 'מקצה השולחן לקיר, בלי מעבר מאחור', 'basis': 'NKBA Kitchen and Bath Planning Guidelines, seating clearance: 32 in (81 cm) when no traffic passes behind.'},
    'chair_edge_cm': {'v': 91, 'kind': 'standard', 'he': 'מקצה השולחן, כשעוברים בצד', 'basis': 'NKBA guidelines: 36 in (91 cm) to edge past a seated diner.'},
    'chair_walk_cm': {'v': 112, 'kind': 'standard', 'he': 'מקצה השולחן, כשעוברים מאחורי הכיסא', 'basis': 'NKBA guidelines: 44 in (112 cm) to walk past a seated diner.'},
    'table_end_cm': {'v': 60, 'kind': 'thumb', 'he': 'מעבר בקצה השולחן', 'basis': 'Rule of thumb: 60 cm at a table end with no seat there.'},
    # ---- bedroom ----
    'beds_cm': {'v': [[90, 190], [120, 190], [140, 190], [160, 200], [180, 200]], 'kind': 'thumb', 'he': 'מידות מיטה נפוצות', 'basis': 'The mattress sizes sold in Israel (single 90, youth 120, double 140, 160, 180).'},
    'bed_side_cm': {'v': 60, 'kind': 'thumb', 'he': 'מעבר בצד המיטה', 'basis': 'Common bedroom planning rule: 60 cm (50 at the least) beside a bed you get in from.'},
    'bed_foot_cm': {'v': 70, 'kind': 'thumb', 'he': 'מעבר למרגלות המיטה', 'basis': 'Common bedroom planning rule: 60 to 90 cm at the foot of the bed; we use 70.'},
    'wardrobe_depth_cm': {'v': 60, 'kind': 'thumb', 'he': 'עומק ארון בגדים', 'basis': 'Standard wardrobe depth 55 to 65 cm.'},
    'wardrobe_front_hinged_cm': {'v': 90, 'kind': 'thumb', 'he': 'מקום מול ארון עם דלתות', 'basis': 'Rule of thumb: an opening door (about 50 cm) plus a person standing.'},
    'wardrobe_front_sliding_cm': {'v': 60, 'kind': 'thumb', 'he': 'מקום מול ארון הזזה', 'basis': 'Rule of thumb: a person standing in front of sliding doors.'},
    # ---- lighting ----
    'lux': {'v': {'living': 150, 'dining': 200, 'kitchen': 300, 'bedroom': 150, 'kids': 300, 'study': 300, 'bath': 250, 'hall': 100},
            'kind': 'thumb', 'he': 'עוצמת אור כללית בחדר (לוקס)', 'basis': 'Rule-of-thumb values inside the residential ranges of the IES Lighting Handbook (living 100 to 300 lx, kitchen and study tasks 300 to 500 lx).'},
    'kelvin': {'v': {'living': '2700 עד 3000', 'dining': '2700 עד 3000', 'kitchen': '3000 עד 4000', 'bedroom': '2700', 'kids': '3000 עד 4000', 'study': '4000', 'bath': '3000 עד 4000', 'hall': '3000'},
               'kind': 'thumb', 'he': 'גוון האור (קלווין)', 'basis': 'The ranges the search answer for תכנון תאורה לבית showed on 11.11.2026 (2700K-3000K warm, 3000K-4000K neutral, 5000K cold) and lighting-shop guides.'},
    'lumen_factor': {'v': 1.25, 'kind': 'thumb', 'he': 'תוספת לאובדן אור', 'basis': 'Rule of thumb: lumens = lux x m2, plus 25% for light lost on walls and shades in a room with light walls.'},
    'fixtures_lm': {'v': {'spot': 600, 'ceiling': 2000, 'profile': 1000, 'pendant': 1200}, 'kind': 'thumb', 'he': 'אור מגוף אחד (לומן)', 'basis': 'Typical catalogue output of LED fittings: 7 W spot about 600 lm, ceiling fitting about 2,000 lm, LED profile about 1,000 lm per metre, pendant about 1,200 lm. Check the box.'},
    # ---- painting ----
    'paint_cover_m2l': {'v': 10, 'kind': 'thumb', 'he': 'כמה מ"ר צובע ליטר בשכבה אחת', 'basis': 'Interior acrylic paint data sheets give about 8 to 12 m2 per litre per coat; we use 10. Check the can.'},
    'paint_coats': {'v': 2, 'kind': 'thumb', 'he': 'שכבות', 'basis': 'Two coats is the usual repaint.'},
    'door_m2': {'v': 1.7, 'kind': 'thumb', 'he': 'שטח דלת', 'basis': 'A standard interior door opening of 0.80 x 2.10 m = 1.68 m2.'},
    'paint_cans_l': {'v': [18, 5, 1], 'kind': 'thumb', 'he': 'גודלי פחי צבע', 'basis': 'The can sizes sold in Israeli paint shops (18 l, 5 l, 1 l); some brands sell 4.5 l or 0.75 l.'},
    # ---- flooring ----
    'waste_pct': {'v': {'straight': 8, 'diagonal': 15, 'herringbone': 15}, 'kind': 'thumb', 'he': 'פחת לפי צורת ההנחה', 'basis': 'Installer rule of thumb: straight lay 5 to 10%, diagonal and herringbone 15% or more.'},
    'box_m2': {'v': {'tile60': 1.44, 'tile80': 1.28, 'tile120': 1.44, 'laminate': 2.2, 'engineered': 2.0, 'spc': 2.2}, 'kind': 'thumb', 'he': 'מ"ר בקרטון', 'basis': 'Usual pack sizes (60x60: 4 tiles, 80x80: 2 tiles, 120x120: 1 tile; plank packs about 2 to 2.4 m2). The exact figure is printed on the box.'},
    # ---- budgets and sizes ----
    'contingency_pct': {'v': 10, 'kind': 'thumb', 'he': 'רזרבה לבלתי צפוי', 'basis': 'Common budgeting rule of thumb (10 to 15%); no Israeli source chosen yet.'},
    'vat_rate': {'v': 0.18, 'kind': 'standard', 'he': 'מע"מ', 'basis': 'Israeli VAT rate since 1.1.2025: 18%.'},
    'rooms_m2': {'v': {'2': 60, '3': 80, '4': 100, '5': 130, '6': 150}, 'kind': 'assumption', 'he': 'שטח דירה לפי מספר חדרים', 'basis': 'The size bands the search answers use with the designer-fee tables (3 rooms about 80, 4 about 100, 5 about 130 m2), seo/designer-market/architecture.md; 2 and 6 rooms are our extension.'},
    'kitchen_m_by_rooms': {'v': {'2': 3, '3': 4, '4': 5, '5': 6, '6': 6.5}, 'kind': 'assumption', 'he': 'אורך מטבח לפי גודל הדירה', 'basis': 'Our default only, to open the example; the reader types the real run from the plan.'},
    'level_split': {'v': 'thirds', 'kind': 'assumption', 'he': 'בסיסי, בינוני, גבוה', 'basis': 'The usual band of each item (or the full published range when no usual band exists) is split into three equal parts: basic = lowest third, mid = middle, high = top third.'},
    'service_split': {'v': 'halves', 'kind': 'assumption', 'he': 'תכנון בלבד מול ליווי מלא', 'basis': 'Designer fee bands run "from planning only to full supervision": planning only = lower half of the usual band, full supervision = upper half.'},
    'lift_stretcher_cm': {'v': [110, 210, 220], 'kind': 'thumb', 'he': 'מעלית אלונקה', 'basis': 'Israeli high-rise buildings must have a stretcher lift; its cabin is commonly 110 x 210 cm. Only an example: measure your own lift.'},
    'build_months_cbs': {'v': [32.3, 37.8], 'kind': 'standard', 'he': 'משך בנייה ממוצע', 'basis': 'CBS release 089/2026 (19.3.2026), buildings completed in 2025: 32.3 months per building, 37.8 weighted by flats.'},
}

# The 14 steps from signing to moving in. m = latest sensible month relative to handover (negative = before). Typical, not a rule:
# the order follows market/journey-and-trades.md (which itself calls the timing an assumption); the developer's contract dates win.
STEPS = [
    {'k': 'pro', 'm': -20, 'he': 'בוחרים מעצב או יועץ', 'why': 'כדי שיספיק לתכנן לפני שהיזם סוגר את מועד השינויים.'},
    {'k': 'changes', 'm': -16, 'he': 'מגישים שינויים ליזם: קירות, חדרים רטובים, מטבח', 'why': 'בשלב השלד והמחיצות. את המועד האחרון קובע החוזה עם היזם.'},
    {'k': 'points', 'm': -16, 'he': 'תכנית חשמל ותאורה: נקודות, מפסקים, תקשורת', 'why': 'הנקודות צריכות להיות בקירות לפני הטיח.'},
    {'k': 'ac', 'm': -16, 'he': 'מיזוג: תעלות, ניקוז ומקום ליחידות', 'why': 'התעלות והניקוז נכנסים עם השינויים; היחידות אחרי קבלת המפתח.'},
    {'k': 'smart', 'm': -16, 'he': 'חיווט לבית חכם ולתקשורת', 'why': 'החוטים נכנסים עם החשמל.'},
    {'k': 'floors', 'm': -14, 'he': 'בוחרים ריצוף, פרקט וחדרי רחצה', 'why': 'זיכוי או שדרוג אצל היזם נבחרים עם השינויים.'},
    {'k': 'kitchen_plan', 'm': -14, 'he': 'מתכננים את המטבח', 'why': 'מיקום הכיור, הגז והחשמל נקבע עם השינויים.'},
    {'k': 'kitchen_order', 'm': -4, 'he': 'מזמינים את המטבח', 'why': 'הזמנה כמה חודשים לפני המסירה, הרכבה אחרי קבלת המפתח.'},
    {'k': 'furniture', 'm': -3, 'he': 'מזמינים רהיטים', 'why': 'לרהיטים בהזמנה יש זמן אספקה; מקבלים אותם אחרי המפתח.'},
    {'k': 'appliances', 'm': -1, 'he': 'קונים מוצרי חשמל', 'why': 'בחודש האחרון, לפי מידות הנישות במטבח.'},
    {'k': 'inspection', 'm': 0, 'he': 'בדק בית ופרוטוקול מסירה', 'why': 'ביום המסירה, מול התכניות והמפרט.'},
    {'k': 'carpentry', 'm': 0, 'he': 'מדידה לנגרות ולארונות', 'why': 'מודדים בדירה הגמורה.'},
    {'k': 'paint', 'm': 1, 'he': 'צביעה, וילונות ותריסים', 'why': 'אחרי המפתח ולפני שהרהיטים נכנסים.'},
    {'k': 'move', 'm': 1, 'he': 'מעבר דירה', 'why': 'בסוף החודש ובקיץ המובילים יקרים יותר.'},
]

# Display names that the page may not show as the research wrote them (language-dna blacklist: no "3D" words, "אריח" is a UI word there)
NAME_OVERRIDE = {
    'render_view': 'הדמיה של חדר',
    'tile_material_60': 'פורצלן 60×60, חומר בלבד',
    'tile_material_80': 'פורצלן 80×80, חומר בלבד',
    'tile_material_120': 'פורצלן 120×120, חומר בלבד',
}
NOTE_OVERRIDE = {'tile_laying': 'עבודה בלבד; פורצלן גדול ועבודה מאפס יקרים יותר.', 'tile_supplied_laid': 'לא כל מקור מפרט אם הפורצלן עצמו כלול.', 'acoustic_ceiling': 'לוחות מינרליים בתחתית הטווח.'}
BLACK = re.compile(r'תלת[ -־]?ממד|ממשק|סימולציה|אריח|—')

DOMAIN = re.compile(r'(https?://|www\.|\.co\.il|\.com\b|\.org\b|\.net\b)', re.I)


def item(r):
    dr = r.get('date_range') or []
    o = {
        'g': r['group'], 'name': r['name_he'], 'unit': r['unit_he'],
        'low': r.get('low'), 'high': r.get('high'), 'tlo': r.get('typical_low'), 'thi': r.get('typical_high'),
        'vat': r.get('vat', 'unknown'), 'n': int(r.get('n_sources') or 0), 'conf': r.get('confidence', 'low'),
        'from': str(dr[0])[:7] if dr else None, 'to': str(dr[-1])[:7] if dr else None, 'note': r.get('note_he', ''),
    }
    if o['low'] is None:
        raise SystemExit('item without a low price: ' + r['id'])
    return o


def main():
    prices = json.load(open(os.path.join(RES, 'price-ranges.json'), encoding='utf-8'))
    fees = json.load(open(os.path.join(RES, 'designer-fees.json'), encoding='utf-8'))
    items = {r['id']: item(r) for r in prices}
    fee = {r['id']: item(r) for r in fees}
    for coll in (items, fee):
        for k, v in coll.items():
            if k in NAME_OVERRIDE:
                v['name'] = NAME_OVERRIDE[k]
            if k in NOTE_OVERRIDE:
                v['note'] = NOTE_OVERRIDE[k]
            for f in ('name', 'note'):
                if BLACK.search(v[f] or ''):
                    raise SystemExit('a blacklisted word would reach the page: %s.%s = %s' % (k, f, v[f]))
    out = {
        'key': 'design', 'built': '2026-11-11', 'read': '2026-11', 'readHe': 'נובמבר 2026',
        'vatHe': {'included': 'כולל מע"מ', 'mixed': 'חלק מהמקורות כוללים מע"מ וחלק לא', 'unknown': 'המקורות לא ציינו אם כולל מע"מ', 'excluded': 'לא כולל מע"מ'},
        'items': items, 'fees': fee, 'rules': RULES, 'steps': STEPS,
    }
    text = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
    bad = DOMAIN.findall(text)
    if bad:
        raise SystemExit('a site name or URL would reach the public file: ' + repr(bad[:5]))
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('design.json: %d items, %d fees, %d rules, %d steps, %d bytes' % (len(items), len(fee), len(RULES), len(STEPS), len(text.encode('utf-8'))))


if __name__ == '__main__':
    sys.exit(main())
