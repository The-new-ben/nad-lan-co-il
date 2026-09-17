#!/usr/bin/env python3
"""Claude Design canvas: broker minisite for nad-lan, shown with Meital Katzir's real listings.
Clickable prototype: Home, Listings (filters), Property (gallery, buyer-type costs, viewing form), About and contact,
two mobile screens, and nad-lan's page that offers the minisite to brokers."""
import json, os, sys, html, re, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_canvas as G
from gen_canvas import (PAPER, SURF, INK, INK2, MUTE, LINE, SEA, SEA_H, DEEP, ABYSS, SAND, MIST, FOAM, SANS, SERIF_HE, NUM,
                        ico, e, iso, fint, btn, eyebrow, CARDS, ORDER, T, AMEN, KIND, qr)
from scenes import plate, estate_night, hero_scene, card_scene

BASE = G.BASE
OUT = BASE + 'minisite/project/'
MEASURE = os.environ.get('MEASURE') == '1'
HM = json.load(open(HERE + '/heights_minisite.json')) if os.path.exists(HERE + '/heights_minisite.json') else {}
t = T['he']
W = 1440
PAD = 80
WA = '#'

def H(name, default):
    """A {{hole}} in the canvas; its default value when measuring locally."""
    return str(default) if MEASURE else '{{ ' + name + ' }}'

def IF(cond, visible_by_default, inner):
    if MEASURE:
        return inner if visible_by_default else ''
    return f'<sc-if value="{{{{ {cond} }}}}" hint-placeholder-val="{{{{ {"true" if visible_by_default else "false"} }}}}">{inner}</sc-if>'

def txt(size, color=INK, weight=400, lh=1.6, family=SANS, extra=''):
    return f'margin: 0; font-family: {family}; font-size: {size}px; line-height: {lh}; font-weight: {weight}; color: {color};{(" " + extra) if extra else ""}'

def h2(text, size=52, color=INK, mt=18):
    return f'<h2 style="margin: {mt}px 0 0; font-family: {SERIF_HE}; font-size: {size}px; line-height: 1.1; font-weight: 400; color: {color}; text-wrap: balance;">{text}</h2>'

def link_btn(label, href, kind='sea', icon=None, h=52, size=16, full=False, pad=26):
    return btn(label, kind, icon, 'he', h=h, size=size, full=full, pad=pad, href=href)

# ---------------------------------------------------------------- header and footer
NAV = [('Main.dc.html', 'דף הבית'), ('Listings.dc.html', 'נכסים'), ('Property.dc.html', 'עמוד נכס'), ('About.dc.html', 'אודות וקשר')]

def brand(dark):
    c1, c2 = (PAPER, MIST) if dark else (INK, SEA)
    return (f'<a href="Main.dc.html" style="display: flex; flex-direction: column; gap: 4px; text-decoration: none;">'
            f'<span style="font-family: {SERIF_HE}; font-size: 25px; line-height: 1; font-weight: 500; color: {c1};">מיטל קציר</span>'
            f'<span style="font-family: {SANS}; font-size: 12px; line-height: 1; font-weight: 700; letter-spacing: 0.1em; color: {c2};">נדל״ן על הים</span></a>')

def header(active, dark=False, overlay=False):
    fg = PAPER if dark else INK
    bg = 'transparent' if overlay else (ABYSS if dark else PAPER)
    bd = 'rgba(207, 227, 234, 0.16)' if dark else LINE
    pos = 'position: absolute; top: 0; left: 0; right: 0; z-index: 3;' if overlay else 'position: relative;'
    def nav_link(href, label):
        cur = ' aria-current="page"' if href == active else ''
        under = (MIST if dark else SEA) if href == active else 'transparent'
        weight = 700 if href == active else 600
        return (f'<a href="{href}"{cur} style="display: inline-flex; align-items: center; height: 44px; font-family: {SANS}; font-size: 16px; font-weight: {weight}; '
                f'color: {fg}; text-decoration: none; border-bottom: 2px solid {under};">{label}</a>')
    links = ''.join(nav_link(h, l) for h, l in NAV)
    wa_kind = 'paper' if dark else 'sea'
    return (f'<header style="{pos} height: 88px; box-sizing: border-box; padding-inline: {PAD}px; display: flex; align-items: center; justify-content: space-between; gap: 32px; background: {bg}; border-bottom: 1px solid {bd}; flex-shrink: 0;">'
            f'{brand(dark)}<nav aria-label="ניווט ראשי" style="display: flex; align-items: center; gap: 36px;">{links}</nav>'
            f'<div style="display: flex; align-items: center; gap: 10px;">{btn(iso("052-3631582"), "ghost" if dark else "line", "phone", "he", h=44, size=15, pad=16, aria="052-3631582")}'
            f'{btn("וואטסאפ", wa_kind, "wa", "he", h=44, size=15, pad=18)}</div></header>')

def header_mobile(dark=False, overlay=False):
    fg = PAPER if dark else INK
    pos = 'position: absolute; top: 0; left: 0; right: 0; z-index: 3;' if overlay else 'position: relative;'
    bg = 'transparent' if overlay else (ABYSS if dark else PAPER)
    bd = 'rgba(207, 227, 234, 0.16)' if dark else LINE
    return (f'<header style="{pos} height: 68px; box-sizing: border-box; padding-inline: 20px; display: flex; align-items: center; justify-content: space-between; background: {bg}; border-bottom: 1px solid {bd}; flex-shrink: 0;">'
            f'{brand(dark).replace("font-size: 25px", "font-size: 21px").replace("font-size: 12px", "font-size: 11px")}'
            f'<button type="button" aria-label="תפריט" style="display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; padding: 0; border-radius: 999px; border: 1px solid {"rgba(247, 246, 242, 0.3)" if dark else LINE}; background: transparent; color: {fg}; cursor: pointer;">{ico("menu", 20, fg)}</button></header>')

def footer(pad=PAD, mobile=False):
    cols_nav = ''.join(f'<a href="{h}" style="{txt(15, "rgba(207, 227, 234, 0.9)", 600)} text-decoration: none;">{l}</a>' for h, l in NAV)
    channels = (f'<a href="#" style="{txt(15, "rgba(207, 227, 234, 0.9)", 600)} text-decoration: none; display: flex; align-items: center; gap: 8px;">{ico("wa", 16, MIST)}וואטסאפ</a>'
                f'<a href="#" style="{txt(15, "rgba(207, 227, 234, 0.9)", 600)} text-decoration: none; display: flex; align-items: center; gap: 8px;">{ico("phone", 16, MIST)}{iso("052-3631582")}</a>'
                f'<a href="#" style="{txt(15, "rgba(207, 227, 234, 0.9)", 600)} text-decoration: none; display: flex; align-items: center; gap: 8px;">{ico("ig", 16, MIST)}{iso("@meitalkatzir_realestate")}</a>')
    grid = 'repeat(1, minmax(0, 1fr))' if mobile else 'minmax(0, 1.4fr) repeat(2, minmax(0, 1fr))'
    return (f'<footer style="{"" if MEASURE else "flex-grow: 1; "}padding: {56 if mobile else 80}px {pad}px {120 if mobile else 48}px; background: {ABYSS}; color: {PAPER}; display: flex; flex-direction: column; gap: {32 if mobile else 48}px;">'
            f'<div style="display: grid; grid-template-columns: {grid}; gap: {28 if mobile else 48}px;">'
            f'<div style="display: flex; flex-direction: column; gap: 16px;">{brand(True)}'
            f'<p style="{txt(15, "rgba(207, 227, 234, 0.82)")} max-width: 420px;">נכסי יוקרה בבלעדיות בקו החוף הצפוני של תל אביב, בשרונה ובהרצליה פיתוח. מתווכת מורשית, רישיון {iso("3131540")}.</p></div>'
            f'<nav aria-label="ניווט תחתון" style="display: flex; flex-direction: column; gap: 12px;"><p style="{txt(13, MIST, 700)} letter-spacing: 0.04em;">באתר</p>{cols_nav}</nav>'
            f'<div style="display: flex; flex-direction: column; gap: 12px;"><p style="{txt(13, MIST, 700)} letter-spacing: 0.04em;">יצירת קשר</p>{channels}</div></div>'
            f'<div style="padding-top: 24px; border-top: 1px solid rgba(207, 227, 234, 0.18); display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px;">'
            f'<p style="{txt(13, "rgba(207, 227, 234, 0.66)", 400, 1.7)} max-width: 860px;">המידע נאסף ממודעות המשווקת ומפרסומים ציבוריים ונכון ל-16.9.2026. אין בו הצעה מחייבת, שמאות או ייעוץ.</p>'
            f'<p style="{txt(13, "rgba(207, 227, 234, 0.66)", 600)}">אתר מתווך ב-{iso("nad-lan.co.il")}</p></div></footer>')

def section_head(eyebrow_text, title, lead=None, size=52, center=False):
    al = 'align-items: center; text-align: center;' if center else ''
    lead_html = f'<p style="{txt(18, INK2, 400, 1.6)} margin-top: 16px; max-width: 680px;">{lead}</p>' if lead else ''
    return f'<div style="display: flex; flex-direction: column; {al}">{eyebrow(eyebrow_text, "he")}{h2(title, size)}{lead_html}</div>'

def select(id_, label, options, value_hole=None, onchange=None, width=None, dark=False, h=52, show_label=False, default=None):
    opts = ''.join(f'<option value="{v}">{l}</option>' for v, l in options)
    val = ''
    if value_hole and not MEASURE:
        val = f' value="{{{{ {value_hole} }}}}"'
    ch = f' onChange="{{{{ {onchange} }}}}"' if (onchange and not MEASURE) else ''
    w = f'width: {width}px; ' if width else 'width: 100%; '
    lab_style = (f'{txt(13, MUTE, 700)} letter-spacing: 0.02em;' if show_label else 'position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0);')
    return (f'<div style="position: relative; display: flex; flex-direction: column; gap: 6px; {w}min-width: 0;"><label for="{id_}" style="{lab_style}">{label}</label>'
            f'<select id="{id_}"{val}{ch} style="box-sizing: border-box; width: 100%; height: {h}px; padding-inline: 16px 36px; border-radius: 10px; border: 1px solid {LINE}; background: #FFFFFF; '
            f'font-family: {SANS}; font-size: 16px; font-weight: 600; color: {INK}; appearance: auto;">{opts}</select></div>')

AREAS = [('הרצליה פיתוח', 1, 'estate', 'dusk', 'האחוזה הפרטית, כחמש דקות מכיכר דה שליט'),
         ('צוקי אביב', 4, 'boutique', 'dusk', 'בניין בוטיק מול טיילת הצוק, ומגדלי נאמן'),
         ('נופי ים', 2, 'lowrise', 'day', 'בניינים נמוכים ליד פארק החוף'),
         ('רמת אביב', 1, 'complex', 'day', 'מתחם עם בריכה, חדר כושר ושומר'),
         ('כוכב הצפון', 1, 'penthouse', 'dusk', 'מיני פנטהאוז חדש בבניין בוטיק'),
         ('שרונה', 2, 'twin', 'day', 'ב.ס.ר שרונה, טופס 4 ממרץ 2026')]
AREA_KEY = {'הרצליה פיתוח': 'herzliya', 'צוקי אביב': 'tzukei', 'נופי ים': 'nofei', 'רמת אביב': 'ramat', 'כוכב הצפון': 'kochav', 'שרונה': 'sarona'}
LISTING_AREA = {'L01': 'herzliya', 'L07': 'kochav', 'L08': 'tzukei', 'L05': 'tzukei', 'L04': 'tzukei', 'L06': 'tzukei', 'L02': 'sarona', 'L03': 'sarona', 'L09': 'nofei', 'L10': 'nofei', 'L11': 'ramat'}
ROOMS = {'L01': 7, 'L07': 5, 'L08': 4.5, 'L05': 3.5, 'L04': 3, 'L06': 5, 'L02': 4.5, 'L03': 5, 'L09': 5, 'L10': 3, 'L11': 5}

def mcard(lid, **kw):
    return G.card(lid, 'he', href='Property.dc.html', **kw)

G.ICONS.update({
 'doc': '<path d="M7 3.5h7l4 4V20a.5.5 0 01-.5.5h-10.5A.5.5 0 016.5 20V4a.5.5 0 01.5-.5z"/><path d="M14 3.5V8h4M9.5 12h5M9.5 15.5h5"/>',
 'calc': '<rect x="5" y="3.5" width="14" height="17" rx="2"/><path d="M8.5 7.5h7M8.5 11.5h1M12 11.5h1M15.5 11.5h.01M8.5 15h1M12 15h1M15.5 15v2.5"/>',
 'chart': '<path d="M4 20V4M4 20h16M8 16v-5M12 16V8M16 16v-3"/>',
 'share': '<circle cx="17.5" cy="5.5" r="2.5"/><circle cx="6.5" cy="12" r="2.5"/><circle cx="17.5" cy="18.5" r="2.5"/><path d="M8.7 10.8l6.6-4M8.7 13.2l6.6 4"/>',
 'heart': '<path d="M12 20s-7.5-4.6-7.5-10.1A4.3 4.3 0 0112 7.4a4.3 4.3 0 017.5 2.5C19.5 15.4 12 20 12 20z"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'search': '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/>',
 'calendar': '<rect x="4" y="5.5" width="16" height="14.5" rx="2"/><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4"/>',
 'train': '<rect x="6" y="3.5" width="12" height="13" rx="3"/><path d="M6 10.5h12M9 20.5l1.5-4M15 20.5l-1.5-4M9 13.5h.01M15 13.5h.01"/>',
 'tree': '<path d="M12 20.5V14M12 3.5c3.6 0 6 2.8 6 6 0 2.6-2.2 4.5-6 4.5s-6-1.9-6-4.5c0-3.2 2.4-6 6-6z"/>',
 'crane': '<path d="M6 20.5V4.5L19.5 7M6 7h13.5M15 7v4.5M13.5 11.5h3v2.5h-3zM4 20.5h5"/>',
 'camera': '<path d="M4 8.5h3l1.5-2.5h7L17 8.5h3v11H4z"/><circle cx="12" cy="13.5" r="3.5"/>',
 'globe': '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 3.7 5.4 3.7 8.5s-1.2 5.9-3.7 8.5c-2.5-2.6-3.7-5.4-3.7-8.5S9.5 6.1 12 3.5z"/>',
 'mail': '<rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="M4 7l8 6 8-6"/>',
})
ARROW = ico('arrow_he', 16)

def pill_group(state, options, label, h=44, size=15, bg_idle='transparent'):
    items = []
    for key, text_ in options:
        on_default = key == options[0][0]
        bg = H(f'{state}.{key}.bg', INK if on_default else bg_idle)
        fg = H(f'{state}.{key}.fg', PAPER if on_default else INK)
        pressed = H(f'{state}.{key}.pressed', 'true' if on_default else 'false')
        click = '' if MEASURE else f' onClick="{{{{ {state}.{key}.pick }}}}"'
        items.append(f'<button type="button" aria-pressed="{pressed}"{click} style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; height: {h}px; padding-inline: 18px; border-radius: 999px; '
                     f'border: 1px solid {H(f"{state}.{key}.bd", INK if on_default else LINE)}; background: {bg}; color: {fg}; font-family: {SANS}; font-size: {size}px; font-weight: 700; cursor: pointer; white-space: nowrap;">{text_}</button>')
    return f'<div role="group" aria-label="{label}" style="display: flex; flex-wrap: wrap; gap: 8px;">{"".join(items)}</div>'

AREA_OPTIONS = [('all', 'כל האזורים')] + [(AREA_KEY[a[0]], a[0]) for a in AREAS]
ROOM_OPTIONS = [('all', 'כל מספר חדרים'), ('3', '3 עד 3.5 חדרים'), ('4', '4 עד 4.5 חדרים'), ('5', '5 חדרים ומעלה')]

# ---------------------------------------------------------------- home (desktop)
def home_hero():
    stats = [('רישיון תיווך', '3131540'), ('נכסים בבלעדיות', '11'), ('שכונות על קו החוף', '6'), ('נתונים נכונים ל', '16.9.2026')]
    meta = ''.join(f'<div style="display: flex; flex-direction: column; gap: 6px;"><span style="{txt(13, MIST, 600, 1.2)} letter-spacing: 0.03em;">{a}</span>'
                   f'<span style="{txt(22, PAPER, 600, 1.2)} {NUM}">{b}</span></div>' for a, b in stats)
    search = (f'<div role="search" style="margin-top: 44px; width: 900px; box-sizing: border-box; padding: 12px; border-radius: 18px; background: rgba(247, 246, 242, 0.97); '
              f'box-shadow: 0 24px 60px rgba(5, 16, 20, 0.35); display: flex; align-items: center; gap: 10px;">'
              f'{pill_group("deal", [("sale", "למכירה"), ("rent", "להשכרה")], "סוג עסקה")}'
              f'<div style="flex: 1; min-width: 0;">{select("home-area", "אזור", AREA_OPTIONS)}</div>'
              f'<div style="width: 200px; flex-shrink: 0;">{select("home-rooms", "חדרים", ROOM_OPTIONS)}</div>'
              f'<a href="Listings.dc.html" style="box-sizing: border-box; display: inline-flex; align-items: center; justify-content: center; gap: 10px; height: 52px; padding-inline: 26px; border-radius: 12px; background: {SEA}; color: #FFFFFF; '
              f'font-family: {SANS}; font-size: 16px; font-weight: 700; text-decoration: none; white-space: nowrap; flex-shrink: 0;">{ico("search", 18, "#FFFFFF")}<span>חיפוש נכסים</span></a></div>')
    return (f'<section style="position: relative; height: 960px; flex-shrink: 0; background: {ABYSS}; overflow: hidden;">'
            f'<div style="position: absolute; inset: 0;">{hero_scene(W, 960, hz=776, sun_x=520, sky_x0=40, sky_x1=430, seed="ms-hero", sun_r=56, max_h=170)}</div>'
            f'{header("Main.dc.html", dark=True, overlay=True)}'
            f'<div style="position: absolute; top: 164px; right: {PAD}px; width: 900px; display: flex; flex-direction: column; align-items: flex-start;">'
            f'{eyebrow("נדל״ן על הים · צפון תל אביב, שרונה והרצליה פיתוח", "he", MIST, 15)}'
            f'<h1 style="margin: 26px 0 0; font-family: {SERIF_HE}; font-size: 104px; line-height: 1.02; font-weight: 400; color: {PAPER}; text-wrap: balance;">נכסי יוקרה על קו המים</h1>'
            f'<p style="{txt(22, "rgba(247, 246, 242, 0.88)", 400, 1.55)} margin-top: 24px; max-width: 640px;">מיטל קציר, מתווכת מורשית. 11 נכסים בבלעדיות, מדירות בבנייני בוטיק ועד אחוזה פרטית, עם עמוד מלא לכל נכס.</p>'
            f'{search}</div>'
            f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 104px; box-sizing: border-box; padding-inline: {PAD}px; display: flex; align-items: center; gap: 64px; border-top: 1px solid rgba(207, 227, 234, 0.18);">{meta}</div>'
            f'</section>')

def home_feature():
    stats = ''.join(f'<div style="display: flex; flex-direction: column; gap: 8px;"><b style="{txt(44, INK, 300, 1)} {NUM}">{a}</b><span style="{txt(14, MUTE)}">{b}</span></div>' for a, b in t['f_stats'])
    return (f'<section style="flex-shrink: 0; padding: 112px {PAD}px; background: {PAPER};">'
            f'<div style="display: flex; gap: 40px; align-items: center;">'
            f'<div style="width: 480px; flex-shrink: 0; display: flex; flex-direction: column;">{eyebrow(t["f_eyebrow"], "he")}{h2(t["f_title"], 64)}'
            f'<p style="{txt(19, INK2, 400, 1.65)} margin-top: 22px;">{t["f_lead"]}</p>'
            f'<div style="margin-top: 30px; padding-top: 22px; border-top: 1px solid {LINE}; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px;">{stats}</div>'
            f'<p style="{txt(16, INK2)} margin-top: 26px;">{t["f_amen"]}</p>'
            f'<div style="margin-top: 26px; display: flex; flex-direction: column; gap: 4px;"><strong style="{txt(24, INK, 800, 1.2)}">{t["f_price"]}</strong><span style="{txt(15, MUTE)}">{t["f_price_sub"]}</span></div>'
            f'<div style="margin-top: 30px; display: flex; flex-wrap: wrap; gap: 12px;">{link_btn(t["f_cta"], "#", "abyss", "wa")}{link_btn("לכל הנכסים", "Listings.dc.html", "line")}</div></div>'
            f'<div style="position: relative; flex: 1; min-width: 0; height: 600px; border-radius: 22px; overflow: hidden; background: {ABYSS};">{estate_night()}'
            f'<span style="position: absolute; top: 20px; right: 20px; display: inline-flex; align-items: center; height: 30px; padding-inline: 12px; border-radius: 8px; background: rgba(16, 38, 47, 0.62); color: {PAPER}; font-family: {SANS}; font-size: 13px; font-weight: 700; letter-spacing: 0.06em;">L01</span>'
            f'<span style="position: absolute; bottom: 18px; left: 20px; {txt(12, "rgba(207, 227, 234, 0.72)", 600)} letter-spacing: 0.04em;">איור</span></div>'
            f'</div></section>')

def home_new():
    ids = ['L01', 'L10', 'L02']
    lines = max(G.TL('he', i) for i in ids)
    cards = ''.join(mcard(i, title_lines=lines) for i in ids)
    return (f'<section style="flex-shrink: 0; padding: 104px {PAD}px 112px; background: #FFFFFF; border-block: 1px solid {LINE};">'
            f'<div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 40px;">{section_head("חדש באתר", "נכסים שעודכנו לאחרונה", "לכל נכס עמוד מלא: מחיר ומחיר למ״ר, עלויות, השוואות שוק והסביבה.")}'
            f'{link_btn("לכל 11 הנכסים", "Listings.dc.html", "line", None)}</div>'
            f'<div style="margin-top: 48px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 32px; align-items: stretch;">{cards}</div></section>')

def area_tile(name, n, kind, mode, desc, compact=False):
    count = f'{n} נכסים' if n > 1 else 'נכס אחד'
    ph = 150 if compact else 180
    return (f'<a href="Listings.dc.html" style="display: flex; flex-direction: column; background: #FFFFFF; border: 1px solid {LINE}; border-radius: 12px; overflow: hidden; text-decoration: none; color: {INK};">'
            f'<div style="position: relative; height: {ph}px; background: {ABYSS};">{plate(kind, mode, seed="area-" + name)}'
            f'<span style="position: absolute; top: 14px; right: 14px; display: inline-flex; align-items: center; height: 28px; padding-inline: 12px; border-radius: 999px; background: {PAPER}; color: {ABYSS}; {txt(13, ABYSS, 700, 1)}">{count}</span></div>'
            f'<div style="padding: 20px 22px 22px; display: flex; flex-direction: column; gap: 8px;">'
            f'<p style="{txt(26, INK, 400, 1.15, SERIF_HE)}">{name}</p><p style="{txt(15, INK2, 400, 1.5)}">{desc}</p>'
            f'<span style="margin-top: 6px; display: flex; align-items: center; gap: 8px; {txt(15, SEA, 700, 1.2)}">לנכסים באזור{ico("arrow_he", 16, SEA)}</span></div></a>')

def home_areas():
    tiles = ''.join(area_tile(*a) for a in AREAS)
    return (f'<section style="flex-shrink: 0; padding: 112px {PAD}px; background: {PAPER};">'
            f'{section_head("אזורים", "על קו המים, מהרצליה ועד שרונה", "שש שכונות, כל אחת עם הנכסים שלה. לחיצה על אזור פותחת את רשימת הנכסים.")}'
            f'<div style="margin-top: 48px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 32px;">{tiles}</div></section>')

METHOD = [('doc', 'כל מספר עם מקור', 'נתוני הנכס מסומנים כנתוני המשווקת, והנתונים מסביב מקושרים למקור ציבורי.'),
          ('calc', 'העלות האמיתית', 'מס רכישה לפי סוג רוכש, מימון, ארנונה ודמי ניהול, ובשכירות גם חוק השכירות ההוגנת.'),
          ('chart', 'השוק והסביבה', 'עסקאות ומודעות להשוואה, בתי ספר, תחבורה ותכניות בנייה סביב הנכס.')]

def home_method():
    cols = ''.join(f'<div style="display: flex; flex-direction: column; gap: 14px; padding-top: 28px; border-top: 2px solid {DEEP};">{ico(i, 30, SEA, 1.5)}'
                   f'<h3 style="margin: 0; font-family: {SERIF_HE}; font-size: 28px; line-height: 1.2; font-weight: 400; color: {INK};">{a}</h3><p style="{txt(17, INK2, 400, 1.6)}">{b}</p></div>' for i, a, b in METHOD)
    return (f'<section style="flex-shrink: 0; padding: 104px {PAD}px; background: #FFFFFF; border-block: 1px solid {LINE};">'
            f'<div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 40px;">{section_head("עמוד נכס ב-nad-lan", "יותר ממודעה")}'
            f'{link_btn("לדוגמה: עמוד נכס", "Property.dc.html", "line", None)}</div>'
            f'<div style="margin-top: 48px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 48px;">{cols}</div></section>')

def home_ig():
    return (f'<section style="flex-shrink: 0; padding: 72px {PAD}px; background: {SAND};">'
            f'<div style="display: flex; align-items: center; gap: 48px;">'
            f'<div style="padding: 14px; background: #FFFFFF; border-radius: 12px; flex-shrink: 0;">{qr(G.IG_URL, 132, ABYSS)}</div>'
            f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 12px;">{eyebrow("באינסטגרם", "he")}'
            f'<p dir="ltr" style="{txt(40, INK, 400, 1.1, G.SERIF_EN)} text-align: right;">@meitalkatzir_realestate</p>'
            f'<p style="{txt(17, INK2)}">תמונות וסרטונים מכל הנכסים, ישירות מהחשבון של מיטל. סריקת הקוד פותחת את החשבון.</p></div>'
            f'{link_btn("לעמוד האינסטגרם", "#", "line", "ig")}</div></section>')

def cta_band():
    return (f'<section style="flex-shrink: 0; padding: 96px {PAD}px; background: {DEEP}; color: {PAPER};">'
            f'<div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 48px;">'
            f'<div style="display: flex; flex-direction: column;">{eyebrow("יצירת קשר", "he", MIST)}{h2("לתיאום סיור פרטי", 64, PAPER, 20)}'
            f'<p style="{txt(20, "rgba(207, 227, 234, 0.9)")} margin-top: 16px;">מיטל קציר, נדל״ן על הים. מתווכת מורשית, רישיון {iso("3131540")}.</p></div>'
            f'<div style="display: flex; gap: 12px; flex-shrink: 0;">{link_btn("וואטסאפ", "#", "paper", "wa", h=56, size=17)}{link_btn("לטופס יצירת קשר", "About.dc.html", "ghost", None, h=56, size=17)}</div>'
            f'</div></section>')

def page_home():
    return home_hero() + home_feature() + home_new() + home_areas() + G.numbers_desktop('he') + home_method() + home_ig() + cta_band() + footer()

ED7 = json.load(open(BASE + 'build/editorial/L07.json'))
def strip(s):
    return re.sub(r'\[\[[^\]]+\]\]', '', s or '').strip()

# ---------------------------------------------------------------- listings
LISTINGS_LOGIC = '''class Component extends DCLogic {
  renderVals() {
    const s = this.state || {};
    const deal = s.deal || 'all';
    const area = s.area || 'all';
    const rooms = s.rooms || 'all';
    const data = %s;
    const roomOk = (r) => rooms === 'all' || (rooms === '3' && r >= 3 && r < 4) || (rooms === '4' && r >= 4 && r < 5) || (rooms === '5' && r >= 5);
    const vis = {};
    let count = 0;
    Object.keys(data).forEach((k) => {
      const d = data[k];
      const ok = (deal === 'all' || d[0] === deal) && (area === 'all' || d[1] === area) && roomOk(d[2]);
      vis[k] = ok;
      if (ok) { count += 1; }
    });
    const pill = (key) => ({
      pick: () => this.setState({ deal: key }),
      pressed: deal === key,
      bg: deal === key ? '#14212B' : '#FFFFFF',
      fg: deal === key ? '#F7F6F2' : '#14212B',
      bd: deal === key ? '#14212B' : '#E3E1DA'
    });
    return {
      vis: vis,
      count: count,
      empty: count === 0,
      deal: { all: pill('all'), sale: pill('sale'), rent: pill('rent') },
      area: area,
      rooms: rooms,
      onArea: (ev) => this.setState({ area: ev.target.value }),
      onRooms: (ev) => this.setState({ rooms: ev.target.value }),
      reset: () => this.setState({ deal: 'all', area: 'all', rooms: 'all' })
    };
  }
}''' % json.dumps({k: [CARDS[k]['deal'], LISTING_AREA[k], ROOMS[k]] for k in ORDER})

def page_listings():
    crumbs = (f'<nav aria-label="מיקום בדף" style="display: flex; align-items: center; gap: 10px; {txt(14, MUTE, 600, 1)}">'
              f'<a href="Main.dc.html" style="color: {MUTE}; text-decoration: none;">דף הבית</a><span aria-hidden="true">/</span><span style="color: {INK};">נכסים</span></nav>')
    head = (f'<section style="flex-shrink: 0; padding: 48px {PAD}px 36px; background: {PAPER};">{crumbs}'
            f'<div style="margin-top: 22px; display: flex; align-items: flex-end; justify-content: space-between; gap: 40px;">'
            f'<div style="display: flex; flex-direction: column;"><h1 style="margin: 0; font-family: {SERIF_HE}; font-size: 72px; line-height: 1.05; font-weight: 400; color: {INK};">כל הנכסים</h1>'
            f'<p style="{txt(19, INK2)} margin-top: 14px;">11 נכסים בבלעדיות של מיטל קציר, נדל״ן על הים: 5 למכירה ו-6 להשכרה. הנתונים נכונים ל-16.9.2026.</p></div>'
            f'<p style="{txt(15, MUTE, 600, 1.3)}">מציג <b style="color: {INK}; {NUM}">{H("count", 11)}</b> מתוך 11 נכסים</p></div></section>')
    reset_click = '' if MEASURE else ' onClick="{{ reset }}"'
    bar = (f'<div style="flex-shrink: 0; padding: 16px {PAD}px; background: #FFFFFF; border-block: 1px solid {LINE}; display: flex; align-items: center; gap: 16px;">'
           f'{pill_group("deal", [("all", "הכול"), ("sale", "למכירה"), ("rent", "להשכרה")], "סוג עסקה", bg_idle="#FFFFFF")}'
           f'<span aria-hidden="true" style="width: 1px; height: 32px; background: {LINE};"></span>'
           f'{select("f-area", "אזור", AREA_OPTIONS, "area", "onArea", 260)}{select("f-rooms", "חדרים", ROOM_OPTIONS, "rooms", "onRooms", 240)}'
           f'<button type="button"{reset_click} style="margin-inline-start: auto; height: 44px; padding-inline: 16px; border: 0; background: transparent; {txt(15, SEA, 700, 1)} cursor: pointer;">ניקוי הסינון</button></div>')
    lines_by_row = {}
    def pair_lines(i):
        k = ORDER.index(i)
        row = ORDER[k - k % 2: k - k % 2 + 2]
        return max(G.TL('he', j) for j in row)
    cards = ''.join(IF(f'vis.{i}', True, mcard(i, title_lines=pair_lines(i))) for i in ORDER)
    empty = IF('empty', False, f'<div style="grid-column: 1 / -1; padding: 64px 32px; border: 1px dashed #AEB8BF; border-radius: 12px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center;">'
                                f'<p style="{txt(26, INK, 400, 1.2, SERIF_HE)}">אין נכס שמתאים לסינון</p><p style="{txt(16, INK2)}">אפשר לנקות את הסינון, או לכתוב למיטל מה מחפשים.</p>'
                                f'<div style="display: flex; gap: 10px;"><button type="button"{reset_click} style="height: 48px; padding-inline: 22px; border-radius: 999px; border: 1px solid {INK}; background: transparent; {txt(15, INK, 700, 1)} cursor: pointer;">ניקוי הסינון</button>{link_btn("וואטסאפ למיטל", "#", "sea", "wa", h=48, size=15)}</div></div>')
    area_rows = ''.join(f'<li style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding-block: 12px; border-top: 1px solid {LINE};"><span style="{txt(16, INK, 600, 1.2)}">{n}</span><span style="{txt(14, MUTE, 600, 1.2)} {NUM}">{c if c > 1 else 1} {"נכסים" if c > 1 else "נכס"}</span></li>' for n, c, *_ in AREAS)
    aside = (f'<aside style="width: 400px; flex-shrink: 0; display: flex; flex-direction: column; gap: 16px;">'
             f'<div style="border-radius: 14px; overflow: hidden; border: 1px solid {LINE};">{G.coast_map("he", 398)}</div>'
             f'<p style="{txt(13, MUTE, 400, 1.5)}">{t["map_caption"]}</p>'
             f'<ul style="margin: 0; padding: 0; list-style: none;">{area_rows}</ul></aside>')
    body = (f'<section style="flex-shrink: 0; padding: 40px {PAD}px 112px; background: {PAPER}; display: flex; gap: 32px; align-items: flex-start;">'
            f'<div style="flex: 1; min-width: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px; align-items: stretch;">{cards}{empty}</div>{aside}</section>')
    return header('Listings.dc.html') + head + bar + body + cta_band() + footer()

# ---------------------------------------------------------------- property (L07)
PRICE = 18_000_000
BUYERS = [('single', 'דירה יחידה', 1153886, '6.41%', 75), ('additional', 'דירה נוספת או תושב חוץ', 1678899, '9.33%', 50), ('oleh', 'עולה חדש זכאי', 975976, '5.42%', 75)]

def buyer_values():
    out = {}
    for key, label, tax, rate, ltv in BUYERS:
        loan = PRICE * ltv // 100
        equity = PRICE - loan
        out[key] = {'tax': fint(tax), 'rate': rate, 'ltv': f'{ltv}%', 'loan': fint(loan), 'equity': fint(equity), 'total': fint(equity + tax)}
    return out

PROPERTY_LOGIC = '''class Component extends DCLogic {
  renderVals() {
    const s = this.state || {};
    const img = typeof s.img === 'number' ? s.img : 0;
    const buyer = s.buyer || 'single';
    const values = %s;
    const n = 5;
    const shots = [0, 1, 2, 3, 4].map((i) => ({
      pick: () => this.setState({ img: i }),
      ring: img === i ? '#2F6F86' : 'transparent',
      pressed: img === i
    }));
    const tab = (key) => ({
      pick: () => this.setState({ buyer: key }),
      selected: buyer === key,
      bg: buyer === key ? '#14212B' : 'transparent',
      fg: buyer === key ? '#F7F6F2' : '#14212B'
    });
    return {
      show: { i0: img === 0, i1: img === 1, i2: img === 2, i3: img === 3, i4: img === 4 },
      counter: (img + 1) + ' / ' + n,
      prev: () => this.setState({ img: (img + n - 1) %% n }),
      next: () => this.setState({ img: (img + 1) %% n }),
      shots: shots,
      tabs: { single: tab('single'), additional: tab('additional'), oleh: tab('oleh') },
      v: values[buyer],
      saved: !!s.saved,
      notSaved: !s.saved,
      toggleSave: () => this.setState({ saved: !s.saved }),
      sent: !!s.sent,
      notSent: !s.sent,
      onSubmit: (ev) => { ev.preventDefault(); this.setState({ sent: true }); }
    };
  }
}''' % json.dumps(buyer_values(), ensure_ascii=False)

SHOTS = [x['he'] for x in ED7['shots'][:5]]

def photo_slot(caption, idx, big=False):
    icon_size = 44 if big else 22
    return (f'<div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: {14 if big else 6}px; background: {DEEP};">'
            f'<div style="position: absolute; inset: 0; opacity: 0.35;">{plate("penthouse", "dusk", seed="slot" + str(idx))}</div>'
            f'<span style="position: relative; display: flex; color: {MIST};">{ico("camera", icon_size, MIST, 1.3)}</span>'
            f'<span style="position: relative; {txt(22 if big else 12, PAPER, 600, 1.3)} text-align: center; padding-inline: 12px;">{caption}</span>'
            + (f'<span style="position: relative; {txt(14, MIST, 600, 1.3)}">התמונה של מיטל תוצב כאן</span>' if big else '') + '</div>')

def gallery(width=1280, height=600, thumbs=True, mobile=False):
    mains = ''
    for i in range(5):
        inner = (f'<div style="position: absolute; inset: 0;">{plate("penthouse", "dusk", seed="L07")}</div>'
                 f'<span style="position: absolute; bottom: 18px; left: 20px; {txt(12, "rgba(207, 227, 234, 0.8)", 600, 1)} letter-spacing: 0.04em;">איור · {SHOTS[0]}</span>') if i == 0 else photo_slot(SHOTS[i], i, big=True)
        mains += IF(f'show.i{i}', i == 0, f'<div style="position: absolute; inset: 0;">{inner}</div>')
    prev_c = '' if MEASURE else ' onClick="{{ prev }}"'
    next_c = '' if MEASURE else ' onClick="{{ next }}"'
    nav_btn = lambda label, ic, click, side: (f'<button type="button" aria-label="{label}"{click} style="position: absolute; top: 50%; {side}: 16px; transform: translateY(-50%); width: 48px; height: 48px; border-radius: 999px; border: 0; '
                                              f'background: rgba(247, 246, 242, 0.92); color: {INK}; display: flex; align-items: center; justify-content: center; cursor: pointer;">{ico(ic, 20, INK)}</button>')
    main = (f'<div style="position: relative; width: 100%; height: {height}px; border-radius: {0 if mobile else 16}px; overflow: hidden; background: {ABYSS};">{mains}'
            f'{nav_btn("התמונה הקודמת", "arrow_en", prev_c, "right")}{nav_btn("התמונה הבאה", "arrow_he", next_c, "left")}'
            f'<span style="position: absolute; top: 16px; left: 16px; display: inline-flex; align-items: center; height: 30px; padding-inline: 12px; border-radius: 999px; background: rgba(16, 38, 47, 0.7); {txt(13, PAPER, 700, 1)} {NUM}" dir="ltr">{H("counter", "1 / 5")}</span></div>')
    if not thumbs:
        return main
    th = ''
    for i in range(5):
        click = '' if MEASURE else f' onClick="{{{{ shots.{i}.pick }}}}"'
        inner = plate('penthouse', 'dusk', seed='L07') if i == 0 else photo_slot(SHOTS[i], i)
        th += (f'<button type="button" aria-label="{SHOTS[i]}" aria-pressed="{H(f"shots.{i}.pressed", "true" if i == 0 else "false")}"{click} style="position: relative; height: 104px; padding: 0; border-radius: 10px; overflow: hidden; cursor: pointer; '
               f'border: 3px solid {H(f"shots.{i}.ring", SEA if i == 0 else "transparent")}; background: {ABYSS};"><div style="position: absolute; inset: 0;">{inner}</div></button>')
    return f'<div style="display: flex; flex-direction: column; gap: 12px;">{main}<div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px;">{th}</div></div>'

FACT_ICONS = ['rooms', 'area', 'balcony', 'floor', 'exposure', 'parking', 'storage', 'mamad']

def facts_grid(cols=4, compact=False):
    items = ''.join(f'<div style="display: flex; flex-direction: column; gap: 8px; padding: {14 if compact else 18}px; border-radius: 10px; background: #FFFFFF; border: 1px solid {LINE};">{ico(FACT_ICONS[k], 22, SEA)}'
                    f'<b style="{txt(19 if compact else 21, INK, 700, 1.2)} {NUM}">{f["value"]["he"]}</b><span style="{txt(13, MUTE, 600, 1.3)}">{f["label"]["he"]}</span></div>' for k, f in enumerate(ED7['facts']))
    return (f'<div style="display: flex; flex-direction: column; gap: 10px;"><div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 12px;">{items}</div>'
            f'<p style="{txt(13, MUTE, 400, 1.5)}">לפי מודעות המשווקת. חלק מהשטחים ומספר כיווני האוויר אינם אחידים בין המודעות, ויש לאמת אותם בתשריט.</p></div>')

def cost_block(compact=False):
    tabs = ''
    for key, label, *_ in BUYERS:
        click = '' if MEASURE else f' onClick="{{{{ tabs.{key}.pick }}}}"'
        on = key == 'single'
        tabs += (f'<button type="button" role="tab" aria-selected="{H(f"tabs.{key}.selected", "true" if on else "false")}"{click} style="height: 44px; padding-inline: {14 if compact else 20}px; border-radius: 999px; border: 1px solid {INK}; '
                 f'background: {H(f"tabs.{key}.bg", INK if on else "transparent")}; color: {H(f"tabs.{key}.fg", PAPER if on else INK)}; font-family: {SANS}; font-size: {14 if compact else 15}px; line-height: 1; font-weight: 700; cursor: pointer; white-space: nowrap;">{label}</button>')
    d = buyer_values()['single']
    def fig(label, hole, default, sub_hole=None, sub_default=None, strong=False):
        sub = f'<span style="{txt(13, MUTE, 600, 1.3)} {NUM}">{H(sub_hole, sub_default)}</span>' if sub_hole else ''
        return (f'<div style="display: flex; flex-direction: column; gap: 6px; padding: 18px; border-radius: 12px; background: {ABYSS if strong else "#FFFFFF"}; border: 1px solid {ABYSS if strong else LINE};">'
                f'<span style="{txt(13, MIST if strong else MUTE, 700, 1.3)}">{label}</span>'
                f'<b style="{txt(26 if not compact else 22, PAPER if strong else INK, 700, 1.15)} {NUM}"><span>{H(hole, default)}</span>&nbsp;₪</b>{sub}</div>')
    figs = (fig('מס רכישה', 'v.tax', d['tax'], 'v.rate', d['rate']) + fig('משכנתא מקסימלית', 'v.loan', d['loan'], 'v.ltv', d['ltv'])
            + fig('הון עצמי מינימלי', 'v.equity', d['equity']) + fig('הון עצמי ומס יחד', 'v.total', d['total'], strong=True))
    ledger_rows = [('למ״ר משוקלל, מרפסות בשליש משטחן', '83,077 ₪'), ('למ״ר משוקלל, מרפסות בחצי משטחן', '78,261 ₪'),
                   ('ארנונה, הערכה שנתית', iso('20,706-37,692') + ' ₪'), ('דמי ניהול', 'לא פורסמו'), ('המחיר בדולרים', 'כ-5.9 מיליון')]
    ledger = ''.join(f'<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 16px; padding-block: 12px; border-top: 1px solid {LINE};">'
                     f'<span style="{txt(15, INK2, 600, 1.3)}">{a}</span><b style="{txt(16, INK, 700, 1.3)} {NUM} white-space: nowrap;">{b}</b></div>' for a, b in ledger_rows)
    cols = 2 if compact else 4
    return (f'<div style="display: flex; flex-direction: column; gap: 18px;">'
            f'<div role="tablist" aria-label="סוג רוכש" style="display: flex; flex-wrap: wrap; gap: 8px;">{tabs}</div>'
            f'<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 12px;">{figs}</div>'
            f'<div style="display: flex; flex-direction: column;">{ledger}</div>'
            f'<p style="{txt(13, MUTE, 400, 1.6)}">חישוב לפי מדרגות מס הרכישה ומגבלות המימון של בנק ישראל שפורסמו עד 16.9.2026, על המחיר המבוקש במודעות המשווקת. ההערכה אינה ייעוץ, ומס בפועל תלוי בנסיבות הרוכש.</p></div>')

BARS = [('הדירה, על 190 מ״ר בנוי', 94737, None, True), ('הדירה, מרפסות בשליש משטחן', 83077, None, True), ('פרויקטים חדשים בשכונה, עד', 95000, '90,000 עד 95,000', False),
        ('עסקה: סמינר הקיבוצים, 4 חדרים, יולי 2026', 75793, None, False), ('עסקה: ש״י עגנון 40, 5 חדרים, 2026', 75281, None, False), ('ממוצע למ״ר בשכונה', 51000, '49,000 עד 51,000', False)]

def bars_block(width=848):
    rows = ''
    for label, v, vt, this in BARS:
        pct = v / 100000 * 100
        rows += (f'<div style="display: grid; grid-template-columns: 300px minmax(0, 1fr); align-items: center; gap: 16px;">'
                 f'<span style="{txt(14, INK if this else INK2, 700 if this else 600, 1.35)}">{label}</span>'
                 f'<div style="position: relative; height: 30px; background: {FOAM}; border-radius: 6px;">'
                 f'<div style="position: absolute; top: 0; bottom: 0; right: 0; width: {pct:.1f}%; background: {SEA if this else "#9CC3CF"}; border-radius: 6px;"></div>'
                 f'<span style="position: absolute; top: 50%; right: 12px; transform: translateY(-50%); {txt(13, "#FFFFFF" if this else INK, 700, 1)} {NUM} white-space: nowrap;">{vt if vt else iso(fint(v))} ₪</span></div></div>')
    ticks = ''.join(f'<span style="position: absolute; right: {p}%; transform: translateX(50%); {txt(12, MUTE, 400, 1)} {NUM}">{iso(l)}</span>' for p, l in ((0, '0'), (25, '25,000'), (50, '50,000'), (75, '75,000'), (100, '100,000')))
    return (f'<div style="display: flex; flex-direction: column; gap: 12px;">{rows}'
            f'<div style="display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: 16px;"><span></span><div style="position: relative; height: 18px;">{ticks}</div></div>'
            f'<p style="{txt(13, MUTE, 400, 1.5)}">מחיר למ״ר בשקלים. מקורות: ביזפורטל, יולי 2026, ועסקאות שדווחו ב-2026. הפרויקטים החדשים והממוצע מוצגים לפי הערך העליון בטווח.</p></div>')

def location_block(compact=False):
    paras = ED7['location']['he']
    bullets = [('tree', 'פארק הירקון', 'גובל בשכונה לאורך שדרות רוקח, כ-3,750 דונם כולל הספורטק.'),
               ('train', 'הקו הירוק', 'צפוי לפעול בקטעו הדרומי ב-2028 ובמלואו ב-2030, עם תחנת רדינג מצפון לשדרות רוקח.'),
               ('crane', 'סמינר הקיבוצים', 'בפינת רוקח ונמיר מתוכננים שלושה מגדלי מגורים בני 28 קומות ו-450 דירות.')]
    cards = ''.join(f'<div style="display: flex; gap: 14px; align-items: flex-start; padding: 16px; border-radius: 12px; background: #FFFFFF; border: 1px solid {LINE};">{ico(i, 24, SEA)}'
                    f'<div style="display: flex; flex-direction: column; gap: 4px;"><b style="{txt(16, INK, 700, 1.3)}">{a}</b><span style="{txt(14, INK2, 400, 1.5)}">{b}</span></div></div>' for i, a, b in bullets)
    return (f'<div style="display: flex; flex-direction: column; gap: 18px;"><p style="{txt(17 if not compact else 16, INK2, 400, 1.7)}">{strip(paras[0])}</p>'
            f'<div style="display: grid; grid-template-columns: repeat({1 if compact else 3}, minmax(0, 1fr)); gap: 12px;">{cards}</div></div>')

OPEN_ATTR = ' open=""'

def faq_block(n=3):
    items = ''.join(f'<details style="border-top: 1px solid {LINE}; padding-block: 18px;"{OPEN_ATTR if k == 0 else ""}><summary style="cursor: pointer; {txt(18, INK, 700, 1.4)}">{x["q"]["he"]}</summary>'
                    f'<p style="{txt(16, INK2, 400, 1.7)} margin-top: 12px;">{strip(x["a"]["he"])}</p></details>' for k, x in enumerate(ED7['faq'][:n]))
    return f'<div style="display: flex; flex-direction: column; border-bottom: 1px solid {LINE};">{items}</div>'

def viewing_form(compact=False):
    sub = '' if MEASURE else ' onSubmit="{{ onSubmit }}"'
    field = lambda id_, label, typ, ph, auto: (f'<div style="display: flex; flex-direction: column; gap: 6px;"><label for="{id_}" style="{txt(13, INK2, 700, 1.2)}">{label}</label>'
                                              f'<input id="{id_}" type="{typ}" placeholder="{ph}" autocomplete="{auto}" style="box-sizing: border-box; width: 100%; height: 48px; padding-inline: 14px; border-radius: 10px; border: 1px solid {LINE}; background: #FFFFFF; font-family: {SANS}; font-size: 16px; color: {INK};"></div>')
    form = (f'<form{sub} style="display: flex; flex-direction: column; gap: 12px;">'
            f'{field("v-name", "שם מלא", "text", "השם שלך", "name")}{field("v-phone", "טלפון", "tel", "050-0000000", "tel")}'
            f'{select("v-time", "מתי נוח לך?", [("morning", "בוקר"), ("noon", "צהריים"), ("evening", "ערב")], h=48, show_label=True)}'
            f'<button type="submit" style="height: 50px; border-radius: 999px; border: 0; background: {ABYSS}; color: {PAPER}; {txt(16, PAPER, 700, 1)} cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px;">{ico("calendar", 18, PAPER)}בקשה לתיאום סיור</button></form>')
    done = (f'<div role="status" style="display: flex; flex-direction: column; align-items: flex-start; gap: 10px; padding: 18px; border-radius: 12px; background: {FOAM};">'
            f'<span style="display: flex; align-items: center; gap: 8px; {txt(16, DEEP, 700, 1.3)}">{ico("check", 20, DEEP, 2)}הבקשה נשלחה</span>'
            f'<span style="{txt(14, INK2, 400, 1.5)}">מיטל תחזור אליך לתיאום. אפשר גם לכתוב לה ישירות בוואטסאפ.</span></div>')
    return IF('notSent', True, form) + IF('sent', False, done)

def price_card(compact=False):
    return (f'<div style="display: flex; flex-direction: column; gap: 18px; padding: 26px; border-radius: 16px; background: #FFFFFF; border: 1px solid {LINE}; box-shadow: 0 18px 40px rgba(16, 38, 47, 0.08);">'
            f'<div style="display: flex; flex-direction: column; gap: 6px;"><span style="{txt(13, SEA, 700, 1.2)} letter-spacing: 0.03em;">למכירה · מחיר מבוקש</span>'
            f'<b style="{txt(40, INK, 800, 1.1)} {NUM}">18,000,000&nbsp;₪</b>'
            f'<span style="{txt(15, MUTE, 600, 1.4)}"><span style="{NUM}">94,737</span>&nbsp;₪ למ״ר · כ-5.9 מיליון דולר</span></div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 6px;">' + ''.join(f'<span style="display: inline-flex; align-items: center; gap: 6px; height: 30px; padding-inline: 10px; border-radius: 999px; background: {FOAM}; {txt(13, DEEP, 600, 1)}">{ico(i, 14, DEEP)}{l}</span>' for i, l in (('rooms', '5 חדרים'), ('area', 'כ-190 מ״ר'), ('floor', 'קומה 11'))) + '</div>'
            f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px;">{link_btn("וואטסאפ", "#", "sea", "wa", h=50, size=16, full=True, pad=10)}{link_btn("חיוג", "#", "line", "phone", h=50, size=16, full=True, pad=10)}</div>'
            f'<div style="height: 1px; background: {LINE};"></div>'
            f'<div style="display: flex; flex-direction: column; gap: 12px;"><h3 style="margin: 0; font-family: {SERIF_HE}; font-size: 24px; line-height: 1.2; font-weight: 400; color: {INK};">סיור פרטי בנכס</h3>{viewing_form()}</div>'
            f'</div>')

def broker_mini():
    return (f'<div style="display: flex; align-items: center; gap: 14px; padding: 18px; border-radius: 14px; background: {ABYSS}; color: {PAPER};">'
            f'<div style="width: 56px; height: 56px; border-radius: 50%; overflow: hidden; flex-shrink: 0; position: relative;">{card_scene()}</div>'
            f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px;"><b style="{txt(18, PAPER, 500, 1.2, SERIF_HE)}">מיטל קציר</b>'
            f'<span style="{txt(13, MIST, 600, 1.3)}">נדל״ן על הים · רישיון {iso("3131540")}</span></div>'
            f'<a href="About.dc.html" style="{txt(14, MIST, 700, 1.2)} text-decoration: none; white-space: nowrap;">פרופיל</a></div>')

def page_property():
    save_click = '' if MEASURE else ' onClick="{{ toggleSave }}"'
    crumbs = (f'<nav aria-label="מיקום בדף" style="display: flex; align-items: center; gap: 10px; {txt(14, MUTE, 600, 1)}">'
              f'<a href="Main.dc.html" style="color: {MUTE}; text-decoration: none;">דף הבית</a><span aria-hidden="true">/</span>'
              f'<a href="Listings.dc.html" style="color: {MUTE}; text-decoration: none;">נכסים</a><span aria-hidden="true">/</span><span>כוכב הצפון</span><span aria-hidden="true">/</span><span style="color: {INK};">L07</span></nav>')
    badges = ''.join(G.badge(x, k) for x, k in (('למכירה', 'sale'), ('בלעדיות: מיטל קציר', 'note'), ('בניין בוטיק חדש', 'rent')))
    save_label = IF('notSaved', True, '<span>שמירה</span>') + IF('saved', False, '<span>נשמר</span>')
    title = (f'<section style="flex-shrink: 0; padding: 40px {PAD}px 28px; background: {PAPER};">{crumbs}'
             f'<div style="margin-top: 22px; display: flex; align-items: flex-end; justify-content: space-between; gap: 40px;">'
             f'<div style="display: flex; flex-direction: column; gap: 14px; max-width: 900px;"><p style="{txt(15, SEA, 700, 1.2)} letter-spacing: 0.02em;">{ED7["kicker"]["he"]}</p>'
             f'<h1 style="margin: 0; font-family: {SERIF_HE}; font-size: 60px; line-height: 1.08; font-weight: 400; color: {INK}; text-wrap: balance;">מיני פנטהאוז חדש עם 80 מ״ר מרפסות</h1>'
             f'<div style="display: flex; flex-wrap: wrap; gap: 8px;">{badges}</div></div>'
             f'<div style="display: flex; gap: 10px; flex-shrink: 0;">'
             f'<button type="button" style="height: 44px; padding-inline: 16px; border-radius: 999px; border: 1px solid {LINE}; background: #FFFFFF; {txt(15, INK, 700, 1)} display: flex; align-items: center; gap: 8px; cursor: pointer;">{ico("share", 18, INK)}<span>שיתוף</span></button>'
             f'<button type="button"{save_click} aria-pressed="{H("saved", "false")}" style="height: 44px; padding-inline: 16px; border-radius: 999px; border: 1px solid {LINE}; background: #FFFFFF; {txt(15, INK, 700, 1)} display: flex; align-items: center; gap: 8px; cursor: pointer;">{ico("heart", 18, SEA)}{save_label}</button>'
             f'</div></div></section>')
    gal = f'<section style="flex-shrink: 0; padding: 0 {PAD}px; background: {PAPER};">{gallery()}</section>'
    feats = ''.join(f'<div style="display: flex; gap: 12px; align-items: flex-start; padding-block: 14px; border-top: 1px solid {LINE};">{ico("check", 20, SEA, 2)}'
                    f'<div style="display: flex; flex-direction: column; gap: 3px;"><b style="{txt(17, INK, 700, 1.35)}">{a}</b><span style="{txt(15, INK2, 400, 1.5)}">{strip(b)}</span></div></div>' for a, b in ED7['features']['he'])
    main = (f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 72px;">'
            f'<div>{facts_grid()}</div>'
            f'<div style="display: flex; flex-direction: column; gap: 18px;">{eyebrow("על הנכס", "he")}{h2(ED7["story_h2"]["he"], 42, INK, 0)}'
            + ''.join(f'<p style="{txt(18, INK2, 400, 1.75)}">{strip(p)}</p>' for p in ED7['story']['he']) + '</div>'
            f'<div style="display: flex; flex-direction: column; gap: 10px;">{eyebrow("מה מיוחד", "he")}<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 32px;">{feats}</div></div>'
            f'<div style="display: flex; flex-direction: column; gap: 18px;">{eyebrow("העלות האמיתית", "he")}{h2("18,000,000 ₪, בחשבון של רוכש", 42, INK, 0)}{cost_block()}</div>'
            f'<div style="display: flex; flex-direction: column; gap: 18px;">{eyebrow("מחיר מול השוק", "he")}{h2("מחיר למ״ר: הדירה מול השכונה", 42, INK, 0)}{bars_block()}</div>'
            f'<div style="display: flex; flex-direction: column; gap: 18px;">{eyebrow("הסביבה", "he")}{h2(ED7["location_h2"]["he"], 42, INK, 0)}{location_block()}</div>'
            f'<div style="display: flex; flex-direction: column; gap: 18px;">{eyebrow("שאלות נפוצות", "he")}{faq_block(3)}</div>'
            f'</div>')
    aside = f'<aside style="width: 400px; flex-shrink: 0; display: flex; flex-direction: column; gap: 16px;">{price_card()}{broker_mini()}</aside>'
    body = f'<section style="flex-shrink: 0; padding: 56px {PAD}px 112px; background: {PAPER}; display: flex; gap: 48px; align-items: flex-start;">{main}{aside}</section>'
    sims = ['L08', 'L05', 'L04']
    lines = max(G.TL('he', i) for i in sims)
    similar = (f'<section style="flex-shrink: 0; padding: 96px {PAD}px 112px; background: #FFFFFF; border-top: 1px solid {LINE};">'
               f'<div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 40px;">{section_head("עוד למכירה", "נכסים נוספים של מיטל")}{link_btn("לכל הנכסים", "Listings.dc.html", "line")}</div>'
               f'<div style="margin-top: 44px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 32px;">{"".join(mcard(i, title_lines=lines) for i in sims)}</div></section>')
    return header('Property.dc.html') + title + gal + body + similar + footer()

FORM_LOGIC = '''class Component extends DCLogic {
  renderVals() {
    const s = this.state || {};
    return {
      sent: !!s.sent,
      notSent: !s.sent,
      onSubmit: (ev) => { ev.preventDefault(); this.setState({ sent: true }); }
    };
  }
}'''

HOME_LOGIC = '''class Component extends DCLogic {
  renderVals() {
    const s = this.state || {};
    const deal = s.deal || 'sale';
    const pill = (key) => ({
      pick: () => this.setState({ deal: key }),
      pressed: deal === key,
      bg: deal === key ? '#14212B' : 'transparent',
      fg: deal === key ? '#F7F6F2' : '#14212B',
      bd: deal === key ? '#14212B' : '#E3E1DA'
    });
    return { deal: { sale: pill('sale'), rent: pill('rent') } };
  }
}'''

def input_field(id_, label, typ='text', ph='', auto='off', full=False, textarea=False, required=False):
    req = ' required=""' if required else ''
    span = 'grid-column: 1 / -1; ' if full else ''
    star = f' <span style="color: {SEA};" aria-hidden="true">*</span>' if required else ''
    ctl = (f'<textarea id="{id_}" rows="4" placeholder="{ph}"{req} style="box-sizing: border-box; width: 100%; min-height: 120px; padding: 12px 14px; border-radius: 10px; border: 1px solid {LINE}; background: #FFFFFF; font-family: {SANS}; font-size: 16px; line-height: 1.5; color: {INK}; resize: vertical;"></textarea>'
           if textarea else
           f'<input id="{id_}" type="{typ}" placeholder="{ph}" autocomplete="{auto}"{req} style="box-sizing: border-box; width: 100%; height: 52px; padding-inline: 14px; border-radius: 10px; border: 1px solid {LINE}; background: #FFFFFF; font-family: {SANS}; font-size: 16px; color: {INK};">')
    return f'<div style="{span}display: flex; flex-direction: column; gap: 6px; min-width: 0;"><label for="{id_}" style="{txt(14, INK2, 700, 1.2)}">{label}{star}</label>{ctl}</div>'

def success_box(title, body):
    return (f'<div role="status" style="display: flex; flex-direction: column; align-items: flex-start; gap: 12px; padding: 28px; border-radius: 14px; background: {FOAM}; border: 1px solid {MIST};">'
            f'<span style="display: flex; align-items: center; gap: 10px; {txt(22, DEEP, 700, 1.3)}">{ico("check", 24, DEEP, 2)}{title}</span><span style="{txt(16, INK2, 400, 1.6)}">{body}</span></div>')

# ---------------------------------------------------------------- about and contact
def page_about():
    facts = [('רישיון תיווך', iso('3131540')), ('נכסים בבלעדיות', '11: 5 למכירה ו-6 להשכרה'), ('אזורי פעילות', 'צפון תל אביב, שרונה, הרצליה פיתוח'), ('אינסטגרם', iso('@meitalkatzir_realestate'))]
    dl = ''.join(f'<div style="display: flex; flex-direction: column; gap: 6px; padding: 18px; border-radius: 12px; background: #FFFFFF; border: 1px solid {LINE};"><dt style="{txt(13, MUTE, 700, 1.2)}">{a}</dt><dd style="{txt(17, INK, 700, 1.4)}">{b}</dd></div>' for a, b in facts)
    intro = (f'<section style="flex-shrink: 0; padding: 88px {PAD}px 104px; background: {PAPER}; display: flex; gap: 72px; align-items: center;">'
             f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column;">{eyebrow("אודות", "he")}'
             f'<h1 style="margin: 22px 0 0; font-family: {SERIF_HE}; font-size: 104px; line-height: 1; font-weight: 400; color: {INK};">מיטל קציר</h1>'
             f'<p style="{txt(40, SEA, 300, 1.2, SERIF_HE)} margin-top: 14px;">נדל״ן על הים</p>'
             f'<p style="{txt(20, INK2, 400, 1.7)} margin-top: 26px; max-width: 660px;">מתווכת מורשית, רישיון {iso("3131540")}, תחת המותג נדל״ן על הים. הנכסים שלה נמצאים בקו החוף הצפוני של תל אביב, בשרונה ובהרצליה פיתוח: דירות בבנייני בוטיק, מיני פנטהאוזים ואחוזה פרטית.</p>'
             f'<dl style="margin: 32px 0 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; max-width: 720px;">{dl}</dl>'
             f'<div style="margin-top: 32px; display: flex; flex-wrap: wrap; gap: 12px;">{link_btn("וואטסאפ", "#", "sea", "wa")}{link_btn(iso("052-3631582"), "#", "line", "phone")}{link_btn("לכל הנכסים", "Listings.dc.html", "line")}</div></div>'
             f'<figure style="margin: 0; position: relative; width: 500px; height: 640px; flex-shrink: 0; border-radius: 250px 250px 22px 22px; overflow: hidden; background: {ABYSS};">'
             f'<div style="position: absolute; inset: 0;">{hero_scene(500, 640, hz=470, sun_x=250, sky_x0=0, sky_x1=0, seed="portrait", sun_r=44, max_h=10)}</div>'
             f'<figcaption style="position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%); display: inline-flex; align-items: center; gap: 8px; height: 36px; padding-inline: 16px; border-radius: 999px; background: rgba(247, 246, 242, 0.94); {txt(14, INK, 700, 1)} white-space: nowrap;">{ico("camera", 16, SEA)}תמונת פרופיל של מיטל</figcaption></figure></section>')
    quotes = ''.join(f'<figure style="margin: 0; display: flex; flex-direction: column; justify-content: space-between; gap: 28px; padding: 30px; border-radius: 14px; background: #FFFFFF; border: 1px dashed #AEB8BF;">'
                     f'<blockquote style="margin: 0; {txt(19, MUTE, 400, 1.6, SERIF_HE)}">[המלצה של לקוח, מילה במילה]</blockquote>'
                     f'<figcaption style="{txt(14, MUTE, 700, 1.4)}">[שם מלא] · [סוג העסקה] · [שנה]</figcaption></figure>' for _ in range(3))
    testimonials = (f'<section style="flex-shrink: 0; padding: 96px {PAD}px; background: {SAND};">'
                    f'{section_head("לקוחות", "מה אומרים על העבודה עם מיטל", "המלצות מוצגות רק בשם מלא ובאישור בכתב של הממליצים. עד שיגיעו, המקום שמור.")}'
                    f'<div style="margin-top: 44px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px;">{quotes}</div></section>')
    sub = '' if MEASURE else ' onSubmit="{{ onSubmit }}"'
    interest = [('buy', 'קנייה'), ('rent', 'שכירות'), ('sell', 'מכירת נכס'), ('let', 'השכרת נכס')]
    form = (f'<form{sub} style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px;">'
            f'{input_field("c-name", "שם מלא", "text", "השם שלך", "name", required=True)}{input_field("c-phone", "טלפון", "tel", "050-0000000", "tel", required=True)}'
            f'{input_field("c-mail", "דוא״ל (רשות)", "email", "name@example.com", "email")}'
            f'{select("c-interest", "מה מעניין אותך", interest, show_label=True)}'
            f'<div style="grid-column: 1 / -1;">{select("c-area", "אזור", AREA_OPTIONS, show_label=True)}</div>'
            f'{input_field("c-msg", "הודעה", ph="מה חשוב לך בנכס הבא?", full=True, textarea=True)}'
            f'<div style="grid-column: 1 / -1; display: flex; align-items: flex-start; gap: 10px;"><input id="c-consent" type="checkbox" style="width: 22px; height: 22px; margin: 2px 0 0; accent-color: {SEA}; flex-shrink: 0;">'
            f'<label for="c-consent" style="{txt(15, INK2, 400, 1.5)}">מאשר/ת שמיטל תחזור אליי בטלפון או בוואטסאפ לגבי הפנייה.</label></div>'
            f'<div style="grid-column: 1 / -1;"><button type="submit" style="height: 56px; padding-inline: 36px; border-radius: 999px; border: 0; background: {SEA}; color: #FFFFFF; font-family: {SANS}; font-size: 17px; font-weight: 700; cursor: pointer;">שליחת הפרטים</button></div></form>')
    channel = lambda icon_name, title, body, extra: (f'<div style="display: flex; gap: 18px; align-items: center; padding: 22px; border-radius: 14px; background: {PAPER}; border: 1px solid {LINE};">{extra}'
                                                     f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px;"><span style="display: flex; align-items: center; gap: 8px; {txt(17, INK, 700, 1.3)}">{ico(icon_name, 20, SEA)}{title}</span><span style="{txt(15, INK2, 400, 1.5)}">{body}</span></div></div>')
    qr_box = lambda data, size: f'<div style="padding: 8px; background: #FFFFFF; border-radius: 8px; border: 1px solid {LINE}; flex-shrink: 0;">{qr(data, size, INK)}</div>'
    channels = (channel('wa', 'וואטסאפ', 'סריקה פותחת שיחה עם מיטל.', qr_box('https://wa.me/' + G.WA_NUM, 96))
                + channel('phone', iso('052-3631582'), 'חיוג ישיר.', '')
                + channel('ig', 'אינסטגרם', iso('@meitalkatzir_realestate'), qr_box(G.IG_URL, 96)))
    contact = (f'<section style="flex-shrink: 0; padding: 104px {PAD}px 120px; background: #FFFFFF; display: flex; gap: 64px; align-items: flex-start;">'
               f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 36px;">{section_head("יצירת קשר", "השאירו פרטים", "הפרטים נשלחים ישירות למיטל. אפשר גם לכתוב לה בוואטסאפ.")}'
               f'{IF("notSent", True, form)}{IF("sent", False, success_box("הפרטים נשלחו", "תודה. מיטל תחזור אליך בטלפון או בוואטסאפ."))}</div>'
               f'<aside style="width: 420px; flex-shrink: 0; display: flex; flex-direction: column; gap: 14px; padding-top: 8px;">{channels}</aside></section>')
    return header('About.dc.html') + intro + testimonials + contact + footer()

# ---------------------------------------------------------------- mobile
def sticky(wa='וואטסאפ', call='חיוג'):
    return (f'<div style="position: absolute; left: 0; right: 0; bottom: 0; box-sizing: border-box; padding: 12px 16px 16px; background: rgba(247, 246, 242, 0.97); border-top: 1px solid {LINE}; '
            f'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; z-index: 5;">{link_btn(wa, "#", "sea", "wa", h=48, size=16, full=True, pad=10)}{link_btn(call, "#", "white", "phone", h=48, size=16, full=True, pad=10)}</div>')

def page_home_mobile():
    meta = ''.join(f'<div style="display: flex; flex-direction: column; gap: 3px; min-width: 0;"><span style="{txt(11, MIST, 600, 1.2)}">{a}</span><span style="{txt(15, PAPER, 600, 1.2)} {NUM}">{b}</span></div>'
                   for a, b in (('רישיון תיווך', '3131540'), ('נכסים בבלעדיות', '11'), ('שכונות', '6')))
    panel = (f'<div role="search" style="margin-top: 24px; box-sizing: border-box; padding: 12px; border-radius: 16px; background: rgba(247, 246, 242, 0.97); display: flex; flex-direction: column; gap: 10px;">'
             f'{pill_group("deal", [("sale", "למכירה"), ("rent", "להשכרה")], "סוג עסקה", h=44, size=15)}'
             f'{select("m-area", "אזור", AREA_OPTIONS)}{select("m-rooms", "חדרים", ROOM_OPTIONS)}'
             f'<a href="Listings.dc.html" style="box-sizing: border-box; display: flex; align-items: center; justify-content: center; gap: 10px; height: 52px; border-radius: 12px; background: {SEA}; color: #FFFFFF; font-family: {SANS}; font-size: 16px; font-weight: 700; text-decoration: none;">{ico("search", 18, "#FFFFFF")}<span>חיפוש נכסים</span></a></div>')
    hero = (f'<section style="position: relative; height: 960px; flex-shrink: 0; background: {ABYSS}; overflow: hidden;">'
            f'<div style="position: absolute; inset: 0;">{hero_scene(390, 960, hz=850, sun_x=64, sky_x0=210, sky_x1=390, seed="ms-hm", sun_r=28, max_h=90)}</div>'
            f'{header_mobile(dark=True, overlay=True)}'
            f'<div style="position: absolute; top: 96px; left: 24px; right: 24px; display: flex; flex-direction: column;">{eyebrow("נדל״ן על הים", "he", MIST, 13)}'
            f'<h1 style="margin: 16px 0 0; font-family: {SERIF_HE}; font-size: 50px; line-height: 1.05; font-weight: 400; color: {PAPER}; text-wrap: balance;">נכסי יוקרה על קו המים</h1>'
            f'<p style="{txt(17, "rgba(247, 246, 242, 0.88)", 400, 1.55)} margin-top: 14px;">מיטל קציר, מתווכת מורשית. 11 נכסים בבלעדיות בצפון תל אביב, בשרונה ובהרצליה פיתוח.</p>{panel}</div>'
            f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 76px; box-sizing: border-box; padding-inline: 24px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); align-items: center; gap: 12px; border-top: 1px solid rgba(207, 227, 234, 0.18);">{meta}</div></section>')
    stats = ''.join(f'<div style="display: flex; flex-direction: column; gap: 6px; padding-block: 14px; border-top: 1px solid {LINE};"><b style="{txt(34, INK, 300, 1)} {NUM}">{a}</b><span style="{txt(13, MUTE)}">{b}</span></div>' for a, b in t['f_stats'])
    feature = (f'<section style="flex-shrink: 0; background: {PAPER};"><div style="position: relative; height: 300px; overflow: hidden; background: {ABYSS};">{estate_night()}'
               f'<span style="position: absolute; top: 16px; right: 16px; display: inline-flex; align-items: center; height: 26px; padding-inline: 10px; border-radius: 6px; background: rgba(16, 38, 47, 0.62); {txt(12, PAPER, 700, 1)} letter-spacing: 0.06em;">L01</span></div>'
               f'<div style="padding: 36px 24px 48px; display: flex; flex-direction: column;">{eyebrow(t["f_eyebrow"], "he", SEA, 13)}{h2(t["f_title"], 40, INK, 14)}'
               f'<p style="{txt(17, INK2, 400, 1.65)} margin-top: 14px;">{t["f_lead"]}</p>'
               f'<div style="margin-top: 20px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 20px;">{stats}</div>'
               f'<div style="margin-top: 18px; display: flex; flex-direction: column; gap: 2px;"><strong style="{txt(22, INK, 800, 1.2)}">{t["f_price"]}</strong><span style="{txt(14, MUTE)}">{t["f_price_sub"]}</span></div>'
               f'<div style="margin-top: 22px; display: flex; flex-direction: column; gap: 10px;">{link_btn(t["f_cta"], "#", "abyss", "wa", full=True)}{link_btn("לכל הנכסים", "Listings.dc.html", "line", full=True)}</div></div></section>')
    new = (f'<section style="flex-shrink: 0; padding: 56px 24px; background: #FFFFFF; border-block: 1px solid {LINE}; display: flex; flex-direction: column;">{eyebrow("חדש באתר", "he", SEA, 13)}{h2("נכסים שעודכנו לאחרונה", 34, INK, 14)}'
           f'<div style="margin-top: 24px; display: flex; flex-direction: column; gap: 20px;">{mcard("L01", media_h=214, pad=20, mobile=True)}{mcard("L10", media_h=214, pad=20, mobile=True)}</div>'
           f'<div style="margin-top: 20px;">{link_btn("לכל 11 הנכסים", "Listings.dc.html", "line", full=True)}</div></section>')
    rows = ''.join(f'<a href="Listings.dc.html" style="display: flex; align-items: center; gap: 14px; padding-block: 12px; border-top: 1px solid {LINE}; text-decoration: none;">'
                   f'<div style="position: relative; width: 76px; height: 58px; border-radius: 8px; overflow: hidden; flex-shrink: 0; background: {ABYSS};">{plate(k, m, seed="area-" + n)}</div>'
                   f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px;"><span style="{txt(21, INK, 400, 1.2, SERIF_HE)}">{n}</span><span style="{txt(13, MUTE, 600, 1.3)}">{c if c > 1 else "נכס"} {"נכסים" if c > 1 else "אחד"}</span></div>{ico("arrow_he", 18, SEA)}</a>'
                   for n, c, k, m, d in AREAS)
    areas = (f'<section style="flex-shrink: 0; padding: 56px 24px; background: {PAPER}; display: flex; flex-direction: column;">{eyebrow("אזורים", "he", SEA, 13)}{h2("על קו המים, מהרצליה ועד שרונה", 32, INK, 14)}'
             f'<div style="margin-top: 20px; display: flex; flex-direction: column; border-bottom: 1px solid {LINE};">{rows}</div></section>')
    ig = (f'<section style="flex-shrink: 0; padding: 40px 24px; background: {SAND}; display: flex; align-items: center; gap: 18px;">'
          f'<div style="padding: 10px; background: #FFFFFF; border-radius: 10px; flex-shrink: 0;">{qr(G.IG_URL, 88, ABYSS)}</div>'
          f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 8px;"><span style="{txt(13, SEA, 700, 1.2)}">באינסטגרם</span>'
          f'<span dir="ltr" style="{txt(17, INK, 400, 1.3, G.SERIF_EN)} text-align: right; overflow-wrap: anywhere;">@meitalkatzir_realestate</span>'
          f'<span style="{txt(14, INK2, 400, 1.5)}">תמונות וסרטונים מכל הנכסים.</span></div></section>')
    cta = (f'<section style="flex-shrink: 0; padding: 56px 24px; background: {DEEP}; display: flex; flex-direction: column;">{eyebrow("יצירת קשר", "he", MIST, 13)}{h2("לתיאום סיור פרטי", 40, PAPER, 14)}'
           f'<p style="{txt(16, "rgba(207, 227, 234, 0.9)")} margin-top: 12px;">מיטל קציר, נדל״ן על הים. מתווכת מורשית, רישיון {iso("3131540")}.</p>'
           f'<div style="margin-top: 22px; display: flex; flex-direction: column; gap: 10px;">{link_btn("וואטסאפ", "#", "paper", "wa", full=True)}{link_btn("לטופס יצירת קשר", "About.dc.html", "ghost", None, full=True)}</div></section>')
    return hero + feature + new + areas + ig + cta + footer(24, True) + sticky()

def page_property_mobile():
    badges = ''.join(G.badge(x, k) for x, k in (('למכירה', 'sale'), ('בלעדיות: מיטל קציר', 'note')))
    title = (f'<section style="flex-shrink: 0; padding: 24px 24px 8px; background: {PAPER}; display: flex; flex-direction: column; gap: 12px;">'
             f'<nav aria-label="מיקום בדף" style="display: flex; gap: 8px; {txt(13, MUTE, 600, 1)}"><a href="Listings.dc.html" style="color: {MUTE}; text-decoration: none;">נכסים</a><span aria-hidden="true">/</span><span>כוכב הצפון</span></nav>'
             f'<p style="{txt(14, SEA, 700, 1.3)}">{ED7["kicker"]["he"]}</p>'
             f'<h1 style="margin: 0; font-family: {SERIF_HE}; font-size: 32px; line-height: 1.15; font-weight: 400; color: {INK}; text-wrap: balance;">מיני פנטהאוז חדש עם 80 מ״ר מרפסות</h1>'
             f'<div style="display: flex; flex-wrap: wrap; gap: 6px;">{badges}</div></section>')
    price = (f'<section style="flex-shrink: 0; padding: 16px 24px 8px; background: {PAPER};"><div style="display: flex; flex-direction: column; gap: 14px; padding: 20px; border-radius: 14px; background: #FFFFFF; border: 1px solid {LINE};">'
             f'<div style="display: flex; flex-direction: column; gap: 4px;"><span style="{txt(12, SEA, 700, 1.2)}">מחיר מבוקש</span><b style="{txt(32, INK, 800, 1.1)} {NUM}">18,000,000&nbsp;₪</b>'
             f'<span style="{txt(14, MUTE, 600, 1.4)}"><span style="{NUM}">94,737</span>&nbsp;₪ למ״ר · כ-5.9 מיליון דולר</span></div>'
             f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px;">{link_btn("וואטסאפ", "#", "sea", "wa", h=48, size=15, full=True, pad=8)}{link_btn("חיוג", "#", "line", "phone", h=48, size=15, full=True, pad=8)}</div></div></section>')
    sec = lambda eb, title_, inner, bg=PAPER: (f'<section style="flex-shrink: 0; padding: 44px 24px; background: {bg}; display: flex; flex-direction: column; gap: 16px;">{eyebrow(eb, "he", SEA, 13)}'
                                               + (h2(title_, 30, INK, 0) if title_ else '') + inner + '</section>')
    story = ''.join(f'<p style="{txt(16, INK2, 400, 1.75)}">{strip(p)}</p>' for p in ED7['story']['he'][:2])
    form = (f'<div style="display: flex; flex-direction: column; gap: 12px; padding: 20px; border-radius: 14px; background: #FFFFFF; border: 1px solid {LINE};">'
            f'<h3 style="margin: 0; font-family: {SERIF_HE}; font-size: 24px; line-height: 1.2; font-weight: 400; color: {INK};">סיור פרטי בנכס</h3>{viewing_form(True)}</div>')
    body = (f'<section style="flex-shrink: 0; padding: 28px 24px 8px; background: {PAPER};">{facts_grid(2, True)}</section>'
            + sec('על הנכס', ED7['story_h2']['he'], story)
            + sec('העלות האמיתית', '18,000,000 ₪, בחשבון של רוכש', cost_block(True), '#FFFFFF')
            + sec('הסביבה', ED7['location_h2']['he'], location_block(True))
            + sec('תיאום סיור', None, form, SAND)
            + sec('שאלות נפוצות', None, faq_block(3))
            + sec('עוד למכירה', 'נכסים נוספים של מיטל', mcard('L08', media_h=214, pad=20, mobile=True), '#FFFFFF'))
    return header_mobile() + f'<section style="flex-shrink: 0;">{gallery(390, 300, thumbs=False, mobile=True)}</section>' + title + price + body + footer(24, True) + sticky()

# ---------------------------------------------------------------- for brokers (nad-lan)
def nb_header():
    links = ''.join(f'<a href="#{h}" style="display: inline-flex; align-items: center; height: 44px; {txt(16, INK, 600, 1)} text-decoration: none;">{l}</a>' for h, l in (('includes', 'מה כלול'), ('example', 'הדוגמה החיה'), ('how', 'איך זה עובד')))
    return (f'<header style="position: relative; height: 88px; box-sizing: border-box; padding-inline: {PAD}px; display: flex; align-items: center; justify-content: space-between; gap: 32px; background: {PAPER}; border-bottom: 1px solid {LINE}; flex-shrink: 0;">'
            f'<a href="#" dir="ltr" style="display: flex; align-items: baseline; font-family: {SANS}; font-size: 26px; font-weight: 800; letter-spacing: -0.01em; color: {INK}; text-decoration: none;">nad-lan<span style="font-weight: 400; color: {SEA};">.co.il</span></a>'
            f'<nav aria-label="ניווט ראשי" style="display: flex; gap: 36px;">{links}</nav>{link_btn("לקבלת מיניסייט", "#join", "sea", None, h=46, size=15, pad=22)}</header>')

def laptop_mock():
    screen = (f'<div style="position: relative; width: 640px; height: 400px; overflow: hidden; border-radius: 8px; background: {ABYSS};">'
              f'<div style="position: absolute; inset: 0;">{hero_scene(640, 400, hz=320, sun_x=230, sky_x0=16, sky_x1=190, seed="mock", sun_r=26, max_h=80)}</div>'
              f'<div style="position: absolute; top: 0; left: 0; right: 0; height: 40px; box-sizing: border-box; padding-inline: 26px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(207, 227, 234, 0.16);">'
              f'<span style="display: flex; flex-direction: column; gap: 2px;"><span style="{txt(11, PAPER, 500, 1, SERIF_HE)}">מיטל קציר</span><span style="{txt(6, MIST, 700, 1)} letter-spacing: 0.1em;">נדל״ן על הים</span></span>'
              f'<span style="display: flex; gap: 14px; {txt(7, PAPER, 600, 1)}"><span>דף הבית</span><span>נכסים</span><span>עמוד נכס</span><span>אודות וקשר</span></span>'
              f'<span style="display: inline-flex; align-items: center; height: 18px; padding-inline: 9px; border-radius: 999px; background: {PAPER}; {txt(7, ABYSS, 700, 1)}">וואטסאפ</span></div>'
              f'<div style="position: absolute; top: 74px; right: 36px; width: 420px; display: flex; flex-direction: column; align-items: flex-start;">'
              f'<span style="{txt(7, MIST, 700, 1)}">נדל״ן על הים · צפון תל אביב, שרונה והרצליה פיתוח</span>'
              f'<span style="{txt(44, PAPER, 400, 1.02, SERIF_HE)} margin-top: 10px; display: flex; flex-direction: column;"><span>נכסי יוקרה</span><span>על קו המים</span></span>'
              f'<span style="margin-top: 14px; width: 380px; height: 34px; border-radius: 8px; background: rgba(247, 246, 242, 0.97); display: flex; align-items: center; gap: 6px; padding: 5px; box-sizing: border-box;">'
              f'<span style="height: 24px; width: 46px; border-radius: 999px; background: {INK};"></span><span style="height: 24px; width: 46px; border-radius: 999px; border: 1px solid {LINE};"></span>'
              f'<span style="height: 24px; flex: 1; border-radius: 5px; border: 1px solid {LINE}; background: #fff;"></span><span style="height: 24px; width: 70px; border-radius: 5px; background: {SEA};"></span></span></div></div>')
    return (f'<div style="position: relative; display: flex; flex-direction: column; align-items: center;">'
            f'<div style="padding: 14px; border-radius: 20px; background: #0B1B21; box-shadow: 0 40px 80px rgba(16, 38, 47, 0.3);">{screen}</div>'
            f'<div style="width: 760px; height: 16px; border-radius: 0 0 18px 18px; background: linear-gradient(#C9CFD2, #9AA3A8);"></div></div>')

def phone_mock():
    screen = (f'<div style="position: relative; width: 190px; height: 400px; overflow: hidden; border-radius: 22px; background: {ABYSS};">'
              f'<div style="position: absolute; inset: 0;">{hero_scene(190, 400, hz=350, sun_x=40, sky_x0=110, sky_x1=190, seed="mockm", sun_r=14, max_h=40)}</div>'
              f'<div style="position: absolute; top: 18px; left: 14px; right: 14px; display: flex; flex-direction: column;">'
              f'<span style="{txt(10, PAPER, 500, 1, SERIF_HE)}">מיטל קציר</span><span style="{txt(26, PAPER, 400, 1.05, SERIF_HE)} margin-top: 34px;">נכסי יוקרה על קו המים</span>'
              f'<span style="margin-top: 14px; height: 110px; border-radius: 10px; background: rgba(247, 246, 242, 0.97); display: flex; flex-direction: column; gap: 6px; padding: 8px; box-sizing: border-box;">'
              f'<span style="height: 20px; border-radius: 999px; background: {INK}; width: 60%;"></span><span style="height: 20px; border-radius: 5px; border: 1px solid {LINE};"></span><span style="height: 24px; border-radius: 6px; background: {SEA};"></span></span></div>'
              f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 40px; background: rgba(247, 246, 242, 0.97); display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px; padding: 6px; box-sizing: border-box;">'
              f'<span style="border-radius: 999px; background: {SEA};"></span><span style="border-radius: 999px; border: 1px solid {LINE}; background: #fff;"></span></div></div>')
    return f'<div style="padding: 10px; border-radius: 32px; background: #0B1B21; box-shadow: 0 30px 60px rgba(16, 38, 47, 0.35);">{screen}</div>'

INCLUDES = [('rooms', 'דף בית ממותג', 'שם המתווך והמותג, חיפוש נכסים, אזורים, כפתור וואטסאפ קבוע ופס יצירת קשר.'),
            ('doc', 'עמוד מלא לכל נכס', 'מחיר ומחיר למ״ר, מס רכישה לפי סוג רוכש, מימון, השוואות שוק והסביבה, עם מקור לכל מספר.'),
            ('search', 'סינון נכסים ומפה', 'סינון לפי סוג עסקה, אזור וחדרים, ומפת חוף עם מספר הנכסים בכל שכונה.'),
            ('phone', 'כרטיס ביקור דיגיטלי', 'חזית וגב עם קוד QR שפותח שיחה בוואטסאפ, ופוסט מוכן לאינסטגרם.'),
            ('globe', 'עברית ואנגלית', 'כל עמוד בשתי השפות, לקונים מקומיים ולמשקיעים מחו״ל.'),
            ('calendar', 'פניות מכל נכס', 'הודעת וואטסאפ עם קוד הנכס, חיוג בלחיצה וטופס לתיאום סיור.')]

def page_for_brokers():
    hero = (f'<section style="flex-shrink: 0; padding: 96px {PAD}px 104px; background: {PAPER}; display: flex; align-items: center; gap: 40px;">'
            f'<div style="width: 560px; flex-shrink: 0; display: flex; flex-direction: column;">{eyebrow("למתווכים ולמשרדי תיווך", "he")}'
            f'<h1 style="margin: 22px 0 0; font-family: {SERIF_HE}; font-size: 80px; line-height: 1.04; font-weight: 400; color: {INK}; text-wrap: balance;">מיניסייט יוקרה לכל מתווך</h1>'
            f'<p style="{txt(20, INK2, 400, 1.65)} margin-top: 24px;">אתר מתווך מלא בתוך nad-lan: דף בית ממותג, עמוד מחקר לכל נכס, סינון ומפה, כרטיס ביקור דיגיטלי וגרסה באנגלית. הדוגמה החיה: מיטל קציר, נדל״ן על הים.</p>'
            f'<div style="margin-top: 34px; display: flex; flex-wrap: wrap; gap: 12px;">{link_btn("לקבלת מיניסייט", "#join", "sea", None, h=56, size=17)}{link_btn("לדוגמה החיה", "Main.dc.html", "line", None, h=56, size=17)}</div>'
            f'<p style="{txt(14, MUTE, 600, 1.5)} margin-top: 20px;">כל נתון בעמודים עם מקור, בלי המלצות מומצאות, ושום עמוד לא עולה בלי אישור שלך.</p></div>'
            f'<div style="position: relative; flex: 1; min-width: 0; height: 520px;">'
            f'<div style="position: absolute; top: 10px; left: 0;">{laptop_mock()}</div>'
            f'<div style="position: absolute; bottom: -24px; left: -18px;">{phone_mock()}</div></div></section>')
    tiles = ''.join(f'<div style="display: flex; flex-direction: column; gap: 14px; padding: 30px; border-radius: 16px; background: {PAPER}; border: 1px solid {LINE};">'
                    f'<span style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 14px; background: {FOAM};">{ico(i, 26, SEA)}</span>'
                    f'<h3 style="margin: 0; font-family: {SERIF_HE}; font-size: 26px; line-height: 1.2; font-weight: 400; color: {INK};">{a}</h3><p style="{txt(16, INK2, 400, 1.6)}">{b}</p></div>' for i, a, b in INCLUDES)
    includes = (f'<section id="includes" style="flex-shrink: 0; padding: 104px {PAD}px; background: #FFFFFF; border-block: 1px solid {LINE};">'
                f'{section_head("מה כלול", "כל מה שמתווך יוקרה צריך, באתר אחד")}'
                f'<div style="margin-top: 48px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px;">{tiles}</div></section>')
    stats = [('11', 'עמודי נכס, בעברית ובאנגלית'), ('658', 'מקורות מקושרים בעמודי הנכס'), ('108', 'פוסטים באינסטגרם שנבדקו'), ('6', 'שכונות על מפת החוף')]
    st = ''.join(f'<div style="display: flex; flex-direction: column; gap: 10px; padding-top: 22px; border-top: 1px solid rgba(207, 227, 234, 0.22);"><b style="{txt(64, PAPER, 300, 1)} {NUM}">{a}</b><span style="{txt(16, MIST, 600, 1.4)}">{b}</span></div>' for a, b in stats)
    lines7 = G.TL('he', 'L07')
    example = (f'<section id="example" style="flex-shrink: 0; padding: 104px {PAD}px; background: {ABYSS}; color: {PAPER}; display: flex; align-items: center; gap: 72px;">'
               f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column;">{eyebrow("הדוגמה החיה", "he", MIST)}{h2("מיטל קציר, נדל״ן על הים", 60, PAPER, 20)}'
               f'<p style="{txt(19, "rgba(207, 227, 234, 0.9)", 400, 1.65)} margin-top: 18px; max-width: 640px;">המיניסייט הראשון נבנה על הנכסים האמיתיים של מיטל: אחוזה בהרצליה פיתוח, מיני פנטהאוזים ודירות בצוקי אביב, בנופי ים ובשרונה. כל עמוד נכס עבר מחקר ובדיקה.</p>'
               f'<div style="margin-top: 40px; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 28px;">{st}</div>'
               f'<div style="margin-top: 40px;">{link_btn("לדוגמה החיה", "Main.dc.html", "paper", None, h=56, size=17)}</div></div>'
               f'<div style="width: 408px; flex-shrink: 0; transform: rotate(-2deg);">{mcard("L07", title_lines=lines7)}</div></section>')
    steps = [('שולחים את הנכסים', 'קישור לאינסטגרם, לאתר או לרשימת הנכסים הפעילים. אנחנו אוספים את כל הפרטים.'),
             ('אנחנו בונים ובודקים', 'עמוד מלא לכל נכס: מספרים, מקורות, עלויות והסביבה, בעברית ובאנגלית, ודף בית ממותג.'),
             ('מאשרים ומפרסמים', 'עוברים על הנוסח והמחירים. שום עמוד לא עולה לאתר בלי אישור בכתב שלך.')]
    sts = ''.join(f'<div style="display: flex; flex-direction: column; gap: 14px; padding: 32px; border-radius: 16px; background: #FFFFFF; border: 1px solid {LINE};">'
                  f'<b style="{txt(64, SEA, 300, 1, SERIF_HE)} {NUM}">{k + 1}</b><h3 style="margin: 0; font-family: {SERIF_HE}; font-size: 28px; line-height: 1.2; font-weight: 400; color: {INK};">{a}</h3>'
                  f'<p style="{txt(16, INK2, 400, 1.6)}">{b}</p></div>' for k, (a, b) in enumerate(steps))
    how = (f'<section id="how" style="flex-shrink: 0; padding: 104px {PAD}px; background: {PAPER};">{section_head("איך זה עובד", "שלושה שלבים עד שהמיניסייט באוויר")}'
           f'<div style="margin-top: 48px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px;">{sts}</div></section>')
    sub = '' if MEASURE else ' onSubmit="{{ onSubmit }}"'
    form = (f'<form{sub} style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px;">'
            f'{input_field("j-name", "שם מלא", "text", "השם שלך", "name", required=True)}{input_field("j-office", "שם המשרד או המותג", "text", "למשל: נדל״ן על הים", "organization")}'
            f'{input_field("j-phone", "טלפון", "tel", "050-0000000", "tel", required=True)}{input_field("j-link", "קישור לאינסטגרם או לאתר", "url", "https://", "url")}'
            f'<div style="grid-column: 1 / -1;">{select("j-count", "כמה נכסים פעילים יש לך?", [("5", "עד 5"), ("15", "6 עד 15"), ("16", "16 ומעלה")], show_label=True)}</div>'
            f'<div style="grid-column: 1 / -1;"><button type="submit" style="height: 56px; padding-inline: 36px; border-radius: 999px; border: 0; background: {SEA}; color: #FFFFFF; font-family: {SANS}; font-size: 17px; font-weight: 700; cursor: pointer;">לקבלת הצעה</button></div></form>')
    join = (f'<section id="join" style="flex-shrink: 0; padding: 104px {PAD}px 120px; background: #FFFFFF; border-top: 1px solid {LINE}; display: flex; gap: 72px; align-items: flex-start;">'
            f'<div style="width: 440px; flex-shrink: 0; display: flex; flex-direction: column;">{eyebrow("הצטרפות", "he")}{h2("רוצה מיניסייט כזה?", 56)}'
            f'<p style="{txt(19, INK2, 400, 1.65)} margin-top: 18px;">משאירים פרטים, ונחזור אליך עם הצעה ועם דוגמה שנבנית על הנכסים שלך.</p></div>'
            f'<div style="flex: 1; min-width: 0;">{IF("notSent", True, form)}{IF("sent", False, success_box("הפרטים התקבלו", "נחזור אליך עם הצעה ודוגמה על הנכסים שלך."))}</div></section>')
    foot = (f'<footer style="{"" if MEASURE else "flex-grow: 1; "}padding: 40px {PAD}px; background: {ABYSS}; display: flex; align-items: center; justify-content: space-between; gap: 24px;">'
            f'<span dir="ltr" style="font-family: {SANS}; font-size: 22px; font-weight: 800; color: {PAPER};">nad-lan<span style="font-weight: 400; color: {MIST};">.co.il</span></span>'
            f'<span style="{txt(14, "rgba(207, 227, 234, 0.8)", 600, 1.4)}">מידע נדל״ן ואולם תצוגה דיגיטלי</span></footer>')
    return nb_header() + hero + includes + example + how + join + foot

# ---------------------------------------------------------------- files and index
BOARDS = [
    ('Main.dc.html', 'site', 1440, 'דף הבית', page_home, HOME_LOGIC, ABYSS),
    ('Listings.dc.html', 'site', 1440, 'כל הנכסים (סינון)', page_listings, LISTINGS_LOGIC, ABYSS),
    ('Property.dc.html', 'site', 1440, 'עמוד נכס: L07', page_property, PROPERTY_LOGIC, ABYSS),
    ('About.dc.html', 'site', 1440, 'אודות ויצירת קשר', page_about, FORM_LOGIC, ABYSS),
    ('HomeMobile.dc.html', 'mobile', 390, 'דף הבית במובייל', page_home_mobile, HOME_LOGIC, ABYSS),
    ('PropertyMobile.dc.html', 'mobile', 390, 'עמוד נכס במובייל', page_property_mobile, PROPERTY_LOGIC, ABYSS),
    ('ForBrokers.dc.html', 'brokers', 1440, 'למתווכים: הצטרפות למיניסייט', page_for_brokers, FORM_LOGIC, ABYSS),
]

def build():
    os.makedirs(OUT, exist_ok=True)
    sizes = {}
    for fname, page, w, title, fn, logic, bg in BOARDS:
        h = HM.get(fname, 6000)
        src = G.dc_file('he', w, h, fn(), logic, bg=bg)
        assert chr(0x2013) not in src and chr(0x2014) not in src, fname
        open(OUT + fname, 'w', encoding='utf-8').write(src)
        sizes[fname] = len(src)
    x = {'site': 0, 'mobile': 0, 'brokers': 0}
    boards = {}
    for fname, page, w, title, *_ in BOARDS:
        boards[fname] = {'x': x[page], 'y': 0, 'w': w, 'h': HM.get(fname, 6000), 'title': title, 'page': page, 'is_interactive': True}
        x[page] += w + 80
    idx = {
        'v': 3, 'createdOnFiles': {'v': 1, 'at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
        'title': 'מיניסייט מתווכים', 'launch': {'view': 'canvas', 'page': 'site'},
        'pages': [{'id': 'site', 'name': 'המיניסייט'}, {'id': 'mobile', 'name': 'מובייל'}, {'id': 'brokers', 'name': 'למתווכים'}],
        'boards': boards, 'order': [b[0] for b in BOARDS],
        'notes': {
            'title-site': {'x': 0, 'y': -300, 'text': 'מיניסייט המתווכת · מיטל קציר, נדל״ן על הים', 'kind': 'title1', 'maxW': x['site'] - 80, 'page': 'site'},
            'title-mobile': {'x': 0, 'y': -300, 'text': 'המיניסייט במובייל', 'kind': 'title1', 'maxW': x['mobile'] - 80, 'page': 'mobile'},
        },
        'designSystems': [],
    }
    open(OUT + 'canvas.json', 'w', encoding='utf-8').write(json.dumps(idx, ensure_ascii=False, indent=1))
    return sizes

if __name__ == '__main__':
    for k, v in build().items():
        print(f'{k:26s} {v:>9,}')
