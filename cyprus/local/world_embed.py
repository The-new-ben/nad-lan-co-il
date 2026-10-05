# -*- coding: utf-8 -*-
"""Packs the walkable 3D area (cyprus/local/world3d) into the project-page plugin bundle.
On the project page a card shows the area poster; "enter" opens the 3D in a full-screen dialog over the page
(no iframe), loading three.js and the data only then. The standalone viewer is adapted, not forked by hand:
- its global CSS (:root, *, html/body, button, kbd, :focus-visible) is scoped to .w3, and its h1 becomes an h2,
  so the page keeps exactly one h1;
- it never writes the page's <html lang/dir> (the site owns them) and its [data-t] lookups stay inside #w3;
- three.js loads from the jsDelivr "+esm" builds (no import map, so nothing can clash with WordPress's own map);
- data paths come from window.CYPX_W3.base (the plugin's bundle folder)."""
import io, json, os, re, shutil

THREE = 'https://cdn.jsdelivr.net/npm/three@0.170.0/+esm'
ORBIT = 'https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/controls/OrbitControls.js/+esm'

COPY = {
 'he': {'eyebrow': 'תלת־ממד', 'title': 'השכונה סביב הבתים, בתלת־ממד',
        'lead': 'הגבעה של אגיוס אתנסיוס, הרחובות, הבתים הסמוכים והים באופק. מסתובבים מלמעלה, הולכים ברחוב בגובה העיניים ובודקים מה קרוב.',
        'go': 'כניסה לסיור בתלת־ממד', 'note': 'המחשה: מיקום הבתים לפי תוכנית המגרש, גובה הבניינים מוערך.',
        'alt': 'מפה מלמעלה של הרחובות והבניינים סביב המגרש', 'close': 'סגירת התלת־ממד', 'dlg': 'השכונה סביב הבתים, בתלת־ממד'},
 'en': {'eyebrow': '3D', 'title': 'The neighbourhood around the homes, in 3D',
        'lead': 'The Agios Athanasios hillside, the streets, the neighbouring buildings and the sea on the horizon. Orbit from above, walk the street at eye level and see what is close.',
        'go': 'Enter the 3D tour', 'note': 'Illustration: homes placed from the site plan, building heights estimated.',
        'alt': 'Top-down map of the streets and buildings around the plot', 'close': 'Close the 3D view', 'dlg': 'The neighbourhood around the homes, in 3D'},
}


def rep(s, old, new, n=1):
    c = s.count(old)
    if c != n:
        raise SystemExit(f'world_embed: expected {n}x, found {c}x: {old[:80]!r}')
    return s.replace(old, new)


def scope_css(css):
    css = rep(css, ':root {', '.w3 {')
    css = re.sub(r'(^|\n)\*\s*\{', r'\1.w3, .w3 * {', css, count=1)
    css = re.sub(r'(^|\n)html,\s*body\s*\{', r'\1.w3 {', css, count=1)
    css = re.sub(r'(^|\n)button\s*\{', r'\1.w3 button {', css, count=1)
    css = re.sub(r'(^|\n):focus-visible\s*\{', r'\1.w3 :focus-visible {', css, count=1)
    css = re.sub(r'(^|\n)kbd\s*\{', r'\1.w3 kbd {', css, count=1)
    css = css.replace('.w3-head h1', '.w3-head .w3-title')
    for bad in ('\nhtml', '\nbody', '\n:root', '\n* {', '\nbutton {'):
        if bad in css:
            raise SystemExit(f'world_embed: global selector left: {bad!r}')
    return css + ('\n.w3-head .w3-title{color:var(--cream)}'
                  '\n.cypx-w3dlg{width:100vw;height:100vh;height:100dvh;max-width:none;max-height:none;margin:0;padding:0;border:0;background:#12293E;overflow:hidden}'
                  '\n.cypx-w3dlg::backdrop{background:#0C1C2B}'
                  '\n.cypx-w3dlg .w3{height:100%}'
                  '\n.cypx-w3dlg .w3-lang{display:none}'
                  '\n.cypx-w3close{position:absolute;z-index:20;top:10px;inset-inline-end:12px;width:44px;height:44px;border:0;border-radius:50%;'
                  'background:rgba(244,239,230,.94);color:#12293E;font:700 24px/1 Arial,sans-serif;cursor:pointer}\n')


def patch_js(js):
    js = rep(js, "import('three'), import('three/addons/controls/OrbitControls.js'),",
             f"import('{THREE}'), import('{ORBIT}'),")
    js = rep(js, "fetchProgress('world.json', pct), fetch('places.json')",
             "fetchProgress(W3BASE + 'world.json', pct), fetch(W3BASE + 'places.json')")
    js = rep(js, "  document.documentElement.lang = lang;\n  document.documentElement.dir = rtl ? 'rtl' : 'ltr';\n",
             "  { const r0 = document.getElementById('w3'); if (r0) { r0.lang = lang; r0.dir = rtl ? 'rtl' : 'ltr'; } }\n")
    js = rep(js, "  document.title = T.title;\n", "  // the host page keeps its own <title>\n")
    js = rep(js, "  document.querySelectorAll('[data-t]').forEach(",
             "  (document.getElementById('w3') || document).querySelectorAll('[data-t]').forEach(")
    return "const W3BASE = (typeof window !== 'undefined' && window.CYPX_W3 && window.CYPX_W3.base) || '';\n" + js


def markup(index_html):
    i = index_html.index('<div class="w3" id="w3">')
    j = index_html.index('<script type="module" src="world3d.js">')
    m = index_html[i:j].strip()
    m = rep(m, 'src="poster.svg"', 'src="__W3__poster.svg"')
    m = rep(m, '<h1 data-t="title">', '<h2 class="w3-title" data-t="title">')
    m = rep(m, '</h1>', '</h2>')
    return m


def launcher_js(m, copy=None, text=None):
    """Appended inside the project bundle's IIFE (uses its A, root and lang). copy: the card's words per language;
    text: the viewer's own words for this project (title, lead, posterAlt, region, note), handed over in window.CYPX_W3."""
    return ("\n// The walkable 3D area: a card on the page; the 3D opens full-screen over the page, loaded only on request.\n"
            "(function(){const A3=A+'world/',W=" + json.dumps(copy or COPY, ensure_ascii=False) + "[lang==='he'?'he':'en'];\n"
            " const card=document.createElement('section');card.className='cypx-w3card';card.setAttribute('aria-label',W.title);\n"
            " card.innerHTML='<img src=\"'+A3+'poster.svg\" alt=\"'+W.alt+'\" loading=\"lazy\" decoding=\"async\" width=\"960\" height=\"960\">'\n"
            "  +'<div><p class=\"eyebrow\">'+W.eyebrow+'</p><h2>'+W.title+'</h2><p>'+W.lead+'</p><button type=\"button\" class=\"cypx-w3go\">'+W.go+'</button><p class=\"small\">'+W.note+'</p></div>';\n"
            " root.after(card);let dlg=null;\n"
            " card.querySelector('.cypx-w3go').addEventListener('click',async()=>{\n"
            "  if(dlg){dlg.showModal();return;}\n"
            "  const css=document.createElement('link');css.rel='stylesheet';css.href=A3+'world3d.css';document.head.append(css);\n"
            "  dlg=document.createElement('dialog');dlg.className='cypx-w3dlg';dlg.setAttribute('aria-label',W.dlg);\n"
            "  dlg.innerHTML=" + json.dumps(m, ensure_ascii=False) + ".replace(/__W3__/g,A3)+'<button type=\"button\" class=\"cypx-w3close\">×</button>';\n"
            "  document.body.append(dlg);const x=dlg.querySelector('.cypx-w3close');x.setAttribute('aria-label',W.close);x.addEventListener('click',()=>dlg.close());\n"
            "  dlg.showModal();window.CYPX_W3={base:A3,text:" + json.dumps(text or None, ensure_ascii=False) + "};\n"
            "  try{await import(A3+'world3d.js');const go=document.getElementById('w3-enter');if(go)go.click();}catch(e){dlg.close();}\n"
            " });\n"
            "})();\n")


CARD_CSS = ('.cypx-w3card{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr);gap:24px;align-items:center;margin:8px 0 36px;padding:20px;'
            'background:var(--cy-navy,#12293E);color:#F4EFE6;border-radius:8px}'
            '.cypx-w3card img{display:block;width:100%;height:auto;border-radius:6px;background:#F4EFE6}'
            'body .cypx-w3card h2{font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif;color:#F4EFE6;font-size:clamp(22px,2.6vw,28px);line-height:1.25;margin:4px 0 10px}'
            '.cypx-w3card p{margin:0 0 14px;line-height:1.7;font-size:16px;color:#D9E2E8}'
            '.cypx-w3card .eyebrow{color:#9FD3CB;font-size:12.5px;font-weight:700;letter-spacing:.04em;margin:0}'
            '.cypx-w3card .small{font-size:12.5px;color:#9FB3C2;margin:12px 0 0}'
            '.cypx-w3go{display:inline-flex;align-items:center;min-height:48px;padding:0 22px;border:0;border-radius:6px;background:var(--cy-teal-light,#2FA79A);'
            'color:#0C1C2B;font:700 16px var(--cy-font-body,"Assistant"),Arial,sans-serif;cursor:pointer}'
            '.cypx-w3go:hover{background:#45BBAE}'
            '@media(max-width:700px){.cypx-w3card{grid-template-columns:1fr;padding:16px}.cypx-w3go{width:100%;justify-content:center}}')


def pack(world_dir, bundle_dir, data_dir=None):
    """Copies the data, writes the adapted viewer, returns (launcher js, card css).
    world_dir holds the viewer (world3d.js/css, index.html); data_dir (default: world_dir) holds world.json, places.json,
    poster.svg and, for a project other than the first, embed-text.json ({"card": {he, en}, "viewer": {he, en}})."""
    data_dir = data_dir or world_dir
    out = os.path.join(bundle_dir, 'world')
    os.makedirs(out, exist_ok=True)
    for f in ('world.json', 'places.json', 'poster.svg'):
        shutil.copyfile(os.path.join(data_dir, f), os.path.join(out, f))
    words = {}
    if os.path.exists(os.path.join(data_dir, 'embed-text.json')):
        words = json.load(io.open(os.path.join(data_dir, 'embed-text.json'), encoding='utf-8'))
    js = patch_js(io.open(os.path.join(world_dir, 'world3d.js'), encoding='utf-8').read())
    io.open(os.path.join(out, 'world3d.js'), 'w', encoding='utf-8', newline='\n').write(js)
    css = scope_css(io.open(os.path.join(world_dir, 'world3d.css'), encoding='utf-8').read())
    io.open(os.path.join(out, 'world3d.css'), 'w', encoding='utf-8', newline='\n').write(css)
    m = markup(io.open(os.path.join(world_dir, 'index.html'), encoding='utf-8').read())
    return launcher_js(m, words.get('card'), words.get('viewer')), CARD_CSS
