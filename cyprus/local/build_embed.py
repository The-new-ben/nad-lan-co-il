# -*- coding: utf-8 -*-
"""Builds the site version of the local plan journey: ONE self-contained block for a WordPress Custom HTML block.
Usage: python cyprus/local/build_embed.py --register <private register> --media <media.json> --title-he "..." --title-en "..." --out <file>
The block is scoped under #cyx (ids prefixed cyx-, CSS prefixed .cyx), follows the site's ?lang= (he default, other languages
fall back to English), never touches <html> lang/dir, and sends the chosen home to the site's existing WhatsApp route.
No developer or brand name may appear in the output: the build fails if it does."""
import argparse, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from serve import project_packet  # noqa: E402  (the same allowlist the local server uses)

WA = '972525101555'  # the number the live site already links to (wa.me) on every page
MEDIA_KEYS = {'/media/site.png': 'site', '/media/a-ground.png': 'a-ground', '/media/a-upper.png': 'a-upper',
              '/media/b-ground.png': 'b-ground', '/media/b-upper.png': 'b-upper', '/media/architect-exterior.jpg': 'exterior'}


def read(name):
    return io.open(os.path.join(HERE, name), encoding='utf-8').read()


def rep(s, old, new, n=1):
    c = s.count(old)
    if c != n:
        raise SystemExit(f'build_embed: expected {n}x, found {c}x: {old[:90]!r}')
    return s.replace(old, new)


def ids_of(html):
    return sorted(set(re.findall(r'\bid="([a-z][a-z0-9-]*)"', html)))


def prefix_ids(html, ids):
    for i in ids:
        html = re.sub(rf'\b(id|for|aria-labelledby)="{i}"', rf'\1="cyx-{i}"', html)
        html = html.replace(f'href="#{i}"', f'href="#cyx-{i}"')
    return html


def scope_css(css, ids):
    """Prefix every selector with .cyx; :root/body/main become .cyx; the removed chrome (header, nav, footer) is dropped."""
    drop = ('header', 'nav', '.brand', '.langs', 'footer', 'html')
    out, i = [], 0

    def scope_sel(sel):
        sel = sel.strip()
        for x in ids:
            sel = re.sub(rf'#{x}(?![\w-])', f'#cyx-{x}', sel)
        if sel in (':root', 'body', 'main'):
            return '.cyx'
        if sel.split()[0].split(':')[0].split('[')[0] in drop:
            return None
        return '.cyx ' + sel

    def rules(block):
        res, j = [], 0
        while j < len(block):
            k = block.find('{', j)
            if k < 0:
                break
            head = block[j:k].strip()
            depth, m = 1, k + 1
            while depth:
                depth += {'{': 1, '}': -1}.get(block[m], 0)
                m += 1
            body = block[k + 1:m - 1]
            if head.startswith('@media'):
                inner = rules(body)
                if inner:
                    res.append(head + '{' + inner + '}')
            elif head.startswith('@keyframes'):
                res.append(head.replace('shine', 'cyx-shine') + '{' + body + '}')
            else:
                sels = [x for x in (scope_sel(s) for s in head.split(',')) if x]
                if sels:
                    res.append(','.join(sels) + '{' + body + '}')
            j = m
        return ''.join(res)

    out = rules(css)
    return out.replace('animation:shine', 'animation:cyx-shine')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--register', required=True)
    ap.add_argument('--media', required=True, help='JSON {site,a-ground,a-upper,b-ground,b-upper,exterior: url}')
    ap.add_argument('--title-he', required=True)
    ap.add_argument('--title-en', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    media = json.load(io.open(a.media, encoding='utf-8'))
    packet = project_packet(__import__('pathlib').Path(a.register))
    packet.pop('name', None)  # the brochure name never reaches the page
    packet.pop('district', None)

    # ---------- markup: the local page minus its own chrome ----------
    html = read('index.html')
    body = html[html.index('<figure class="architecture">'):html.index('<footer>')]
    dialogs = html[html.index('<dialog id="conversation"'):html.index('<script src="/plan-data.js">')]
    lead = ('<section class="cyx-lead"><p class="eyebrow" id="district"></p><p class="cyx-lead-text" data-t="intro"></p>'
            '<div class="cyx-cta"><a href="#residences" class="cyx-go" data-t="explore"></a>'
            '<a class="cyx-wa" id="wa-top" target="_blank" rel="noopener" data-t="prepare"></a></div></section>')
    dialogs = rep(dialogs, '<button class="primary" id="copy" data-t="copy"></button><p class="small" data-t="noSend"></p>',
                  '<a class="primary cyx-wa-send" id="wa-send" target="_blank" rel="noopener" data-t="sendWa"></a>'
                  '<button class="secondary" id="copy" data-t="copy"></button>')
    markup = lead + body + dialogs
    markup = rep(markup, 'src="/media/architect-exterior.jpg"', f'src="{media["exterior"]}" loading="lazy" decoding="async"')
    ids = ids_of(markup)
    markup = prefix_ids(markup, ids)

    # ---------- data ----------
    plans = read('plan-data.js')
    plans = '\n'.join(l for l in plans.splitlines() if not l.startswith('//') and l.strip() != "'use strict';")
    plans = rep(plans, 'const DUNE_PLANS = ', 'const PLANS = ')
    for path, key in MEDIA_KEYS.items():
        if path in plans:
            plans = rep(plans, f"'{path}'", json.dumps(media[key]))

    # ---------- behaviour ----------
    js = read('app.js')
    js = js.replace("'use strict';\n", '', 1)
    js = rep(js, 'DUNE_PLANS', 'PLANS', n=js.count('DUNE_PLANS'))
    js, k = re.subn(r"exteriorAlt:'[^']*'", "exteriorAlt:''", js)  # the local alt text names the brand; the site copy below fills it
    if k != 2:
        raise SystemExit(f'build_embed: exteriorAlt x{k}')
    js = rep(js, "const q=new URLSearchParams(location.search);\nlet data,lang=q.get('lang')==='en'?'en':'he',",
             "const q=new URLSearchParams(location.search),root=document.getElementById('cyx'),CFG=JSON.parse(document.getElementById('cyx-config').textContent);\n"
             "let data,lang=['he',null,''].includes(q.get('lang'))?'he':'en',")
    js = rep(js, 'const $=s=>document.querySelector(s)', "const $=s=>root.querySelector(s.replace(/#([a-z])/g,'#cyx-$1'))")
    js = rep(js, 'document.querySelectorAll(', 'root.querySelectorAll(', n=4)
    js = rep(js, 'document.documentElement.lang=lang;document.documentElement.dir=LOCALES[lang].dir;', 'root.lang=lang;root.dir=LOCALES[lang].dir;')
    js = rep(js, "$('#district').textContent=data.district;", "$('#district').textContent=t('district');$('#wa-top').href=waLink(t('waAsk'));")
    js = rep(js, "from?.closest('#site-canvas')", "from?.closest('#cyx-site-canvas')")
    js = rep(js, "event.target.closest('#plan-canvas')", "event.target.closest('#cyx-plan-canvas')")
    js = rep(js, "document.addEventListener('click',", "root.addEventListener('click',")
    js = rep(js, "document.addEventListener('keydown',", "root.addEventListener('keydown',")
    js = rep(js, " if(b.dataset.lang){lang=b.dataset.lang;render();}\n", '')
    js = rep(js, "url.searchParams.set('lang',lang);", '')
    js = rep(js, "$('#brief').value=[data.name,u.id,", "$('#brief').value=[t('pageTitle'),u.id,")
    js = rep(js, "$('#conversation').showModal();};",
             "$('#wa-send').href=waLink(t('waAsk')+'\\n'+$('#brief').value);$('#conversation').showModal();};")
    js = rep(js, "function toast(msg){",
             "function waLink(text){return 'https://wa.me/'+CFG.wa+'?text='+encodeURIComponent(t('waHello')+'\\n'+text+'\\n'+location.origin+location.pathname+(selected?'?unit='+selected:''));}\nfunction toast(msg){")
    js = rep(js, "fetch('/api/project').then(r=>{if(!r.ok)throw Error('Local source unavailable');return r.json()}).then(packet=>{data=packet;",
             "Promise.resolve(CFG.packet).then(packet=>{data=packet;")
    # Site copy: no local-preview wording, the site's own WhatsApp wording, no brand.
    copy = {
        'he': {'intro': 'ארבעה בתים חדשים בשני זוגות באגיוס אתנסיוס שבלימסול: בכל בית ארבעה חדרי שינה וחמישה חדרי רחצה על פני שתי קומות, מרפסות מקורות וחניה מקורה. בחרו בית בתוכנית המגרש, היכנסו לתוכניות הקומות שלו והשוו בין הבתים.',
               'district': 'אגיוס אתנסיוס, לימסול', 'pageTitle': a.title_he, 'prepare': 'לקבלת פרטים נוספים בוואטסאפ',
               'prepareBody': 'אלה פרטי הבית שבחרתם. שלחו אותם בוואטסאפ ונחזור אליכם, מענה בעברית.', 'sendWa': 'שליחה בוואטסאפ',
               'waHello': 'שלום, הגעתי מהאתר CY-PRUS.', 'waAsk': 'אשמח לפרטים על הבתים באגיוס אתנסיוס בלימסול.',
               'loadError': 'פרטי הבתים לא נטענו. נסו לרענן את הדף.', 'exteriorAlt': 'הדמיה: שני זוגות בתים לבנים בני שתי קומות עם מסגרות עץ, מבט מהרחוב'},
        'en': {'intro': 'Four new homes in two pairs in Agios Athanasios, Limassol: four bedrooms and five bathrooms over two floors in each, with covered terraces and covered parking. Select a home on the site plan, step into its floor plans and compare the homes.',
               'district': 'Agios Athanasios, Limassol', 'pageTitle': a.title_en, 'prepare': 'Get more details on WhatsApp',
               'prepareBody': 'These are the details of the home you chose. Send them on WhatsApp and we will get back to you.', 'sendWa': 'Send on WhatsApp',
               'waHello': 'Hello, I came from the CY-PRUS website.', 'waAsk': 'I would like details about the homes in Agios Athanasios, Limassol.',
               'loadError': 'The home details did not load. Please refresh the page.', 'exteriorAlt': 'Visual: two pairs of white two-storey homes with timber frames, seen from the street'}}
    js = rep(js, 'const AREAS=', 'for(const l of ["he","en"])Object.assign(COPY[l],' + json.dumps(copy, ensure_ascii=False) + '[l]);\nconst AREAS=')
    script = '(function(){\'use strict\';\n' + plans + '\n' + js + '\n})();'

    # ---------- style ----------
    scoped = scope_css(read('style.css'), ids)
    css = ('.cyx{--paper:#f5f2eb;--ink:#23392f;--muted:#5c6459;--line:#d7d9cd;--accent:#c3a374;--cream:#e7dfd0;'
           'background:var(--paper);color:var(--ink);font-family:inherit;padding:8px clamp(16px,5vw,64px) 40px;box-sizing:border-box}'
           '.cyx h2,.cyx h3{font-family:inherit;letter-spacing:normal;text-transform:none;line-height:1.25}'
           '.cyx button{font-family:inherit;letter-spacing:normal;text-transform:none;border-radius:0;box-shadow:none}'
           '.cyx figure{margin:0}.cyx img{max-width:100%}'
           '.cyx-lead{padding:36px 0 28px;max-width:760px}.cyx-lead-text{font-size:18px;line-height:1.8;margin:0 0 22px}'
           '.cyx-cta{display:flex;flex-wrap:wrap;gap:12px}.cyx-cta a{display:inline-flex;align-items:center;min-height:48px;padding:0 22px;text-decoration:none;font-size:15px}'
           '.cyx-go{border:1px solid var(--ink);color:var(--ink)}.cyx-wa,.cyx .cyx-wa-send{background:#1f7a4d;color:#fff!important;border:0}'
           '.cyx .cyx-wa-send{display:flex;justify-content:center;align-items:center;text-decoration:none;min-height:48px}'
           '.cyx[lang=he] .eyebrow{letter-spacing:.5px}'
           '@media(max-width:600px){.cyx-lead{padding:24px 0 20px}.cyx-lead-text{font-size:16px}.cyx-cta a{flex:1 1 100%;justify-content:center}}')
    css = scoped + css  # the site-specific rules come last and win over the scoped local ones
    config = json.dumps({'wa': WA, 'packet': packet}, ensure_ascii=False)
    block = (f'<style>{css}</style>\n<div class="cyx" id="cyx" lang="he" dir="rtl">{markup}</div>\n'
             f'<script type="application/json" id="cyx-config">{config}</script>\n<script>{script}</script>')
    low = block.lower()
    for banned in ('dune', 'mansions', '/media/', '127.0.0.1', 'localhost', 'register', 'brochureid'):
        if banned in low:
            raise SystemExit(f'build_embed: banned text in output: {banned}')
    io.open(a.out, 'w', encoding='utf-8', newline='\n').write(block)
    print(f'wrote {a.out}: {len(block.encode("utf-8"))} bytes, {len(ids)} ids scoped')


if __name__ == '__main__':
    main()
