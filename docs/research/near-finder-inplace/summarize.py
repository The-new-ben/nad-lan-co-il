"""results.json -> summary.json + a printed pass/fail table (one row per page x width)."""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
R = json.loads((HERE / (sys.argv[1] if len(sys.argv) > 1 else 'results.json')).read_text(encoding='utf-8'))
NOISE = ('tawk.to', 'ERR_FAILED')  # the live chat widget's CORS error, on live and after alike


def errs(lst):
    return [e for e in (lst or []) if not any(n in e for n in NOISE)]


rows = []
for page, vps in R.items():
    for vp, x in vps.items():
        if 'fatal' in x:
            rows.append({'page': page, 'vp': vp, 'fatal': x['fatal']})
            continue
        a, lv, ld = x.get('after', {}), x.get('live', {}), x.get('lidi', {})
        sw = a.get('switch') or {}
        btn_h = [b['h'] for b in sw.get('buttons', [])] + ([a['fs']['h']] if a.get('fs') else [])
        lf, af = lv.get('finder') or {}, a.get('finder') or {}
        mv, la = a.get('map_view') or {}, a.get('list_again') or {}
        r = {
            'page': page, 'vp': vp,
            'launcher_live_visible': lv.get('launchVisible'), 'launcher_after_exists': a.get('launchExists'), 'fixed_after': a.get('fixedVisible'),
            'cls_live': lv.get('cls'), 'cls_after': a.get('cls'), 'held_height_exact': a.get('anchor_same_as_nojs'),
            'switch': [b['t'] for b in sw.get('buttons', [])], 'controls_min_h': min(btn_h) if btn_h else None,
            'count_live': lf.get('count'), 'rows_live': lf.get('rows'), 'count_after': af.get('count'), 'rows_after': af.get('rows'),
            'map_canvas': af.get('canvas'), 'pins_after': af.get('pins'),
            'map_in_place': (mv.get('app_visible') and mv.get('app_in_host') and not mv.get('stage_visible') and not mv.get('grid_visible')) if mv else None,
            'back_to_list': (la.get('list_visible') and not la.get('app_visible')) if la else None,
            'fullscreen_open': (a.get('fs_open') or {}).get('dlg') and (a.get('fs_open') or {}).get('inDlg'),
            'escape_returns': (a.get('fs_closed') or {}).get('back') and not (a.get('fs_closed') or {}).get('dlg') and not (a.get('fs_closed') or {}).get('htmlOpen'),
            'lidi_map_in_place': (not ld.get('dlg_open')) and ld.get('app_visible') and ('true' in (ld.get('pressed') or ['true'])[-1:] or not ld.get('pressed')),
            'lidi_target_top': ld.get('target_top_in_view'),
            'hscroll': max(a.get('hScroll', 0), mv.get('hScroll', 0) if mv else 0, a.get('hScroll_end', 0)),
            'errors_live': errs(x.get('errors', {}).get('live')), 'errors_after': errs(x.get('errors', {}).get('after')), 'errors_lidi': errs(x.get('errors', {}).get('lidi')),
        }
        rows.append(r)
(HERE / 'summary.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
for r in rows:
    print(json.dumps(r, ensure_ascii=False))
