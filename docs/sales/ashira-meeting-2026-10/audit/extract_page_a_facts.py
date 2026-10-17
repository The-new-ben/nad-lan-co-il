# -*- coding: utf-8 -*-
import json, re, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL")
    pg = ctx.new_page()
    pg.goto("https://nad-lan.co.il/projects/ashira-sde-dov/", wait_until="load", timeout=90000)
    pg.wait_for_timeout(4000)
    
    # Extract facts cards
    facts = pg.evaluate("""() => {
        const out = [];
        document.querySelectorAll('.nlpf__item, .nlpf p, #nlv2-ashira-info table tr, #nlv2-ashira-info li, .nlprog__step').forEach(e => {
            const t = e.innerText.trim();
            if (t) out.push(t);
        });
        return out;
    }""")
    print("=== FACTS ON PAGE A ===")
    for f in facts[:40]:
        print(f.replace('\n', ' -- '))
        
    # Extract article text blocks
    article_text = pg.evaluate("""() => {
        const out = [];
        const sec = document.querySelector('#nlv2-ashira-info') || document.querySelector('article') || document.querySelector('main');
        if (sec) {
            sec.querySelectorAll('h2, h3, p, li, table').forEach(e => {
                const t = e.innerText.trim();
                if (t && t.length > 10) out.push({tag: e.tagName, text: t});
            });
        }
        return out;
    }""")
    with open(os.path.join(HERE, 'page-a-article.json'), 'w', encoding='utf-8') as f:
        json.dump(article_text, f, ensure_ascii=False, indent=2)
    print(f"Extracted {len(article_text)} article blocks from Page A.")
    ctx.close()
    b.close()
