"""Formatting and calculation helpers for the nad-lan Prestige listing build."""
import json, math, re, html, os
BASE = os.environ.get('NLX_BASE') or (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/')
C = json.load(open(BASE + 'build/constants.json'))

def esc(s):
    return html.escape(str(s), quote=True) if s is not None else ''

def fint(n):
    return f"{int(round(n)):,}"

def num(s):
    return f'<span class="nlx-num">{s}</span>'

def money(n, lang, dec=False):
    if n is None:
        return ''
    s = fint(n)
    return num(f"{s} ₪") if lang == 'he' else num(f"NIS {s}")

def pct(x, d=2):
    return num(f"{x*100:.{d}f}%")

def sqm(n, lang):
    if n is None:
        return ''
    s = (f"{n:g}")
    return num(s) + (' מ״ר' if lang == 'he' else ' sqm')

def tax_progressive(price, brackets):
    tax, lower = 0.0, 0.0
    for upper, rate in brackets:
        top = price if upper is None else min(price, upper)
        if top > lower:
            tax += (top - lower) * rate
        if upper is None or price <= upper:
            break
        lower = upper
    return tax

def purchase_taxes(price):
    single = tax_progressive(price, C['tax_single'])
    additional = tax_progressive(price, C['tax_additional'])
    if price <= C['oleh_cap']:
        oleh = tax_progressive(price, C['tax_oleh'])
        oleh_note = 'oleh_brackets'
    else:
        oleh = single
        oleh_note = 'above_cap'
    return {'single': single, 'additional': additional, 'oleh': oleh, 'oleh_note': oleh_note}

def fx(n):
    return {'usd': n / C['fx']['usd'], 'eur': n / C['fx']['eur']}

DASH_RE = re.compile('[\u2013\u2014]')
def assert_no_dash(s, where=''):
    if DASH_RE.search(s or ''):
        raise ValueError(f'Long dash found in {where}: {s[:120]}')
    return s

if __name__ == '__main__':
    for p in (4650000, 4999000, 5900000, 18000000, 46000000):
        t = purchase_taxes(p)
        print(p, {k: (round(v) if isinstance(v, float) else v) for k, v in t.items()})
