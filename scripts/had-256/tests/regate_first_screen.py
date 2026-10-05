"""Re-gates the T4 "first screen" rows of a theme run on the landing screens only (auth-signup, auth-login), from the
evidence the run recorded (first_field_at_rest per screen). The runs of 5.10 gated every auth screen, including the
recovery screen and the existing-email answer, which a visitor reaches by a tap (not a first screen); test_theme.py now
gates the landing screens and this script brings the earlier rows to the same rule. Nothing is measured again.
    python regate_first_screen.py theme-candidate-2.0.2-A theme-candidate-2.0.2-B
"""
import json
import sys

from bench import RESULTS, _Lock

LANDING = ('auth-signup', 'auth-login')
variants = sys.argv[1:]
with _Lock():
    rows = json.loads(RESULTS.read_text(encoding='utf-8'))
    for r in rows:
        if r['id'] != 'T4' or r.get('variant') not in variants or not r.get('title', '').startswith('first screen'):
            continue
        e = r['evidence']
        vp = int(r['title'].split('(')[-1].split(' ')[0])
        ff = e.get('first_field_at_rest') or {}
        bad = {k: v for k, v in ff.items() if k in LANDING and v and v.get('under')} if vp < 768 else {}
        e['under'] = bad
        e['gate'] = 'landing screens only (auth-signup, auth-login), re-gated from the recorded evidence by regate_first_screen.py'
        e['info_tap_screens_under'] = {k: v for k, v in ff.items() if k not in LANDING and v and v.get('under')}
        old = r['status']
        r['status'] = 'pass' if not bad else 'fail'
        print(r['variant'], r['title'].split('(')[-1].rstrip(')'), old, '->', r['status'], {k: (v['top'], v['under']) for k, v in bad.items()})
    RESULTS.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
