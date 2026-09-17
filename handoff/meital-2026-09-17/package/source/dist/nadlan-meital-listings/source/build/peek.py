import json, sys
D = '/tmp/claude-0/-home-claude/65564abe-2682-55e6-800e-705f1cddbd65/scratchpad/meital/dossiers/'
def t(s, n=230):
    s = (s or '').replace('\n', ' ')
    return s if len(s) <= n else s[:n] + '…'
lid = sys.argv[1]
secs = sys.argv[2].split(',') if len(sys.argv) > 2 else None
d = json.load(open(D + lid + '.json'))
def show(k):
    return secs is None or k in secs
if show('id'):
    i = d['identification']
    print('IDENT:', t(i.get('summary_en'), 700), '|', i.get('address_or_project_en'), '|', i.get('confidence'), i.get('source_ids'))
if show('cross'):
    for c in d.get('cross_listings', []):
        print('CROSS:', t(c.get('what_en'), 120), '| price', c.get('price_nis'), '|', c.get('date'), '|', t(c.get('details_en'), 260), '| evidence:', t(c.get('same_unit_evidence_en'), 200), '|', c.get('confidence'), '|', c.get('url'))
for key, lab, short in [('building_facts','BLD','bld'), ('neighborhood_facts','NBH','nbh')]:
    if show(short):
        for f in d.get(key, []):
            print(f'{lab}:', f.get('label_en'), '=', t(f.get('value_en'), 260), f"[{f.get('basis')}/{f.get('confidence')}]", f.get('source_ids'))
if show('dist'):
    for f in d.get('distances', []):
        print('DIST:', f.get('to_en'), '=', f.get('value_en'), f"[{f.get('basis')}]", f.get('source_ids'), t(f.get('note_en'), 120))
if show('schools'):
    for f in d.get('schools', []):
        print('SCH:', f.get('name_en'), '|', f.get('level_en'), '|', t(f.get('note_en'), 140), f.get('source_ids'))
if show('transport'):
    for f in d.get('transport', []):
        print('TRN:', t(f.get('item_en'), 160), '|', t(f.get('status_en'), 160), f.get('source_ids'))
if show('plan'):
    for f in d.get('planning_future', []):
        print('PLN:', t(f.get('item_en'), 220), '| impact:', t(f.get('impact_en'), 200), f.get('source_ids'))
if show('stats'):
    for f in d.get('market_stats', []):
        print('STAT:', t(f.get('metric_en'), 150), '=', t(f.get('value_en'), 150), f.get('as_of'), f.get('source_ids'))
if show('sale'):
    for f in d.get('sale_comps', []):
        print('SALE:', f.get('date'), '|', t(f.get('where_en'), 70), '|', f.get('rooms'), 'r |', f.get('sqm'), 'sqm | fl', f.get('floor'), '|', f.get('price_nis'), '|', f.get('price_per_sqm_nis'), '/sqm |', f.get('kind'), f.get('source_ids'), t(f.get('note_en'), 100))
if show('rent'):
    for f in d.get('rent_comps', []):
        print('RENT:', f.get('date'), '|', t(f.get('where_en'), 70), '|', f.get('rooms'), 'r |', f.get('sqm'), 'sqm |', f.get('rent_nis'), '|', f.get('rent_per_sqm_nis'), '/sqm |', f.get('kind'), f.get('source_ids'), t(f.get('note_en'), 100))
if show('costs'):
    for f in d.get('costs', []):
        print('COST:', f.get('item_en'), '=', t(f.get('value_en'), 200), f"[{f.get('basis')}]", f.get('source_ids'), t(f.get('note_en'), 160))
if show('risks'):
    for f in d.get('risks', []):
        print('RISK:', t(f.get('en'), 260), f.get('source_ids'))
if show('q'):
    for f in d.get('buyer_or_renter_questions', []):
        print('Q:', t(f.get('en'), 200))
if show('gaps'):
    for f in d.get('gaps', []):
        print('GAP:', t(f.get('en'), 200))
if show('src'):
    for s in d.get('sources', []):
        print('SRC:', s['id'], '|', t(s.get('title'), 90), '|', s.get('url'), '|', s.get('published'))
