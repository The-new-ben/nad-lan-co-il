# Discovery helper: render a developer homepage / projects index in headless Chrome
# and list links that look like project pages, with the visible card text near them.
# Read-only: no clicks except scrolling, no forms.
import sys, json, re, time
from playwright.sync_api import sync_playwright
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
BLOCK = re.compile(r"google-analytics|googletagmanager|hotjar|facebook\.net|doubleclick|clarity\.ms|tiktok|connect\.facebook", re.I)

def run(url, pattern=None):
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL", user_agent=UA)
        ctx.route("**/*", lambda r: r.abort() if BLOCK.search(r.request.url) else r.continue_())
        pg = ctx.new_page()
        out = {"start": url}
        try:
            resp = pg.goto(url, wait_until="domcontentloaded", timeout=60000)
            out["status"] = resp.status if resp else None
            pg.wait_for_timeout(5000)
            for _ in range(12):
                pg.mouse.wheel(0, 900); pg.wait_for_timeout(250)
            pg.wait_for_timeout(1500)
            out["final"] = pg.url
            out["title"] = pg.title()
            links = pg.evaluate("""() => Array.from(document.querySelectorAll('a[href]')).map(a => {
                let card = a.closest('article,li,div');
                return {h: a.href, t: (a.innerText||'').trim().replace(/\s+/g,' ').slice(0,80),
                        c: card ? (card.innerText||'').trim().replace(/\s+/g,' ').slice(0,140) : ''};
            })""")
            seen = set(); res = []
            for l in links:
                if l["h"] in seen: continue
                seen.add(l["h"])
                if pattern and not re.search(pattern, l["h"] + " " + l["t"] + " " + l["c"], re.I): continue
                res.append(l)
            out["links"] = res
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {str(e)[:200]}"
        b.close()
    return out

if __name__ == "__main__":
    url = sys.argv[1]; pat = sys.argv[2] if len(sys.argv) > 2 else None
    o = run(url, pat)
    print(json.dumps({k: v for k, v in o.items() if k != "links"}, ensure_ascii=False))
    for l in o.get("links", [])[:120]:
        import urllib.parse as _u; print("-", _u.unquote(l["h"]), "|", l["t"], "|", l["c"][:110])
