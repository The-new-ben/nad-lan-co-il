# campaign_check.py - read-only evidence collector for developer new-project pages (HAD-678).
# Opens ONE page in headless Chrome, scrolls it, records evidence, takes screenshots.
# Never types, never submits, never accepts cookies (only a "decline" button is pressed if offered).
#
# usage: python campaign_check.py <slug> "<developer>" "<project>" <url> [--follow <url>]... [--viewer-selector <css>]
import sys, json, re, time, datetime, argparse, urllib.parse, os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campaign-check")
OUT = os.path.abspath(OUT)
NO_CLOSE = False
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
BLOCK = re.compile(r"google-analytics|googletagmanager|hotjar|facebook\.net|connect\.facebook|doubleclick|clarity\.ms|tiktok|googleadservices|googlesyndication", re.I)

REQUIRED_WORDS = ["סיור וירטואלי", "360", "תלת מימד", "3D", "בחירת דירה", "בחר דירה", "בחר קומה", "קומה",
                  "מלאי", "זמינות", "הדמיות", "תוכניות", "השאירו פרטים", "טופס"]
EXTRA_WORDS = ["תלת-מימד", "תלת ממד", "וירטואלי", "סיור", "דירה לדוגמה", "דירה לדוגמא", "בחרו דירה", "בחירת קומה",
               "תכניות", "תוכנית", "פנויה", "נמכרה", "מפרט", "הורדת", "קטלוג", "סרטון", "וידאו", "צפייה"]
VIEWER_DOMAINS = re.compile(r"matterport|kuula|3dvista|panoee|pano|360|krpano|marzipano|roundme|cloudpano|momento360|"
                            r"vr|unity|sketchfab|three|babylon|virtual|tour|spacial|envision|showroom|buildingvr|"
                            r"vizzer|ojo|ivisit|lamina|archilogic|floorplanner|apartment|picker|dira|bina", re.I)
NOT_VIEWER = re.compile(r"recaptcha|google\.com/maps|maps\.google|glassix|youtube|vimeo|facebook|cookiebot|consent|doubleclick|wix.*form|filesusr", re.I)
LINK_PAT = re.compile(r"360|סיור|tour|3d|תלת|virtual|וירטואל|matterport|kuula|3dvista|בחירת\s*דירה|בחר\s*דירה|בחרו\s*דירה|"
                      r"בחר\s*קומה|בחירת\s*קומה|apartment|picker|מלאי|זמינות|דירות\s*פנויות|דירה\s*לדוגמ|showroom|"
                      r"interactive|אינטראקטיב|building|explore|אתר\s*הפרויקט|אתר\s*הפרוייקט|minisite", re.I)


def ctx_snips(text, word, n=3, width=45):
    out = []
    flags = re.I if re.search(r"[A-Za-z]", word) else 0
    for m in re.finditer(re.escape(word), text, flags):
        s = max(0, m.start() - width); e = min(len(text), m.end() + width)
        out.append(text[s:e].replace("\n", " "))
        if len(out) >= n:
            break
    return out


def count_word(text, word):
    flags = re.I if re.search(r"[A-Za-z]", word) else 0
    return len(re.findall(re.escape(word), text, flags))


def decline_cookies(pg):
    """Press only a decline/reject button if one is visible. Never accept."""
    pat = re.compile(r"^\s*(דחה|דחי|דחיי|סרב|reject|decline|only necessary|רק הכרחי)", re.I)
    try:
        loc = pg.locator("button, [role=button], a.cky-btn-reject, .cky-btn-reject")
        for i in range(min(loc.count(), 300)):
            el = loc.nth(i)
            try:
                t = (el.inner_text(timeout=300) or "").strip()
            except Exception:
                continue
            if t and len(t) < 40 and pat.search(t) and el.is_visible():
                el.click(timeout=2000); pg.wait_for_timeout(700)
                return t
    except Exception:
        pass
    # banners with no decline button: use the banner's own close (X) control, never "accept"
    for sel in ["#CybotCookiebotDialogBodyButtonDecline", "#CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll",
                "#CybotCookiebotDialog button[aria-label*=close i]", "#CybotCookiebotDialog button[aria-label*=סגור]",
                ".cky-banner-btn-close", "#onetrust-close-btn-container button", ".cc-window .cc-close"]:
        try:
            el = pg.locator(sel).first
            if el.count() and el.is_visible():
                el.click(timeout=2000); pg.wait_for_timeout(700)
                return "close:" + sel
        except Exception:
            pass
    return None

def close_popups(pg):
    """Close lead/marketing popups that cover the page (Escape, then a visible close control inside a dialog). Never submits."""
    closed = []
    try:
        pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    except Exception:
        pass
    sel = ('[role=dialog] [aria-label*="close" i], [role=dialog] [aria-label*="סגור"], [aria-modal=true] [aria-label*="close" i], '
           '[aria-modal=true] [aria-label*="סגור"], .modal [aria-label*="close" i], .popup [aria-label*="close" i], '
           '[class*=popup] [class*=close], [class*=modal] [class*=close], [id*=popup] [class*=close], .elementor-popup-modal .dialog-close-button, '
           '[data-testid=lightbox-close], #POPUPS_ROOT [aria-label*="close" i], #POPUPS_ROOT [aria-label*="סגור"]')
    try:
        loc = pg.locator(sel)
        for i in range(min(loc.count(), 6)):
            el = loc.nth(i)
            try:
                if el.is_visible():
                    el.click(timeout=1500); pg.wait_for_timeout(500); closed.append(i)
            except Exception:
                pass
    except Exception:
        pass
    return closed


JS_MARK_SCROLLER = r"""() => {
  const doc = Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0);
  if (doc > window.innerHeight + 60) return {mode: 'window', h: doc};
  let best = null, bh = 0;
  for (const e of document.querySelectorAll('*')) {
    const st = getComputedStyle(e);
    if (/(auto|scroll)/.test(st.overflowY) && e.scrollHeight > e.clientHeight + 60 && e.clientHeight > 300 && e.scrollHeight > bh) { best = e; bh = e.scrollHeight; }
  }
  if (!best) return {mode: 'window', h: doc};
  document.querySelectorAll('[data-cc-scroller]').forEach(x => x.removeAttribute('data-cc-scroller'));
  best.setAttribute('data-cc-scroller', '1');
  return {mode: 'element', h: bh};
}"""


def scroll_to(pg, mode, y):
    if mode == "element":
        pg.evaluate(f"(() => {{ const e = document.querySelector('[data-cc-scroller]'); if (e) e.scrollTop = {y}; }})()")
        return pg.evaluate("(() => { const e = document.querySelector('[data-cc-scroller]'); return e ? e.scrollTop : 0 })()")
    pg.evaluate(f"window.scrollTo(0, {y})")
    return pg.evaluate("window.scrollY")


def slow_scroll(pg, step=650, pause=280):
    info = pg.evaluate(JS_MARK_SCROLLER)
    mode, h = info["mode"], info["h"]
    y = 0; n = 0
    while y < h and n < 80:
        y += step; n += 1
        scroll_to(pg, mode, y)
        pg.wait_for_timeout(pause)
        h = pg.evaluate(JS_MARK_SCROLLER)["h"] if mode == "window" else pg.evaluate(
            "(() => { const e = document.querySelector('[data-cc-scroller]'); return e ? e.scrollHeight : 0 })()")
    pg.wait_for_timeout(1500)
    return mode, h

JS_COLLECT = r"""() => {
  const abs = (u) => { try { return new URL(u, location.href).href } catch(e) { return u } };
  const ifr = Array.from(document.querySelectorAll('iframe')).map(f => ({
      src: f.src || '', data_src: f.getAttribute('data-src') || f.getAttribute('data-lazy-src') || '',
      w: f.getBoundingClientRect().width|0, h: f.getBoundingClientRect().height|0, title: f.title || ''}));
  const canv = Array.from(document.querySelectorAll('canvas')).map(c => {
      const r = c.getBoundingClientRect(); return {w: r.width|0, h: r.height|0, id: c.id || '', cls: (c.className||'').toString().slice(0,60)} });
  const links = Array.from(document.querySelectorAll('a[href]')).map(a => ({
      h: abs(a.getAttribute('href')), t: (a.innerText || a.getAttribute('aria-label') || a.title || '').trim().replace(/\s+/g,' ').slice(0,90)}));
  const buttons = Array.from(document.querySelectorAll('button,[role=button],[onclick]')).map(b =>
      (b.innerText || b.getAttribute('aria-label') || '').trim().replace(/\s+/g,' ').slice(0,70)).filter(Boolean);
  const scripts = Array.from(document.querySelectorAll('script[src]')).map(s => abs(s.getAttribute('src')));
  const forms = Array.from(document.querySelectorAll('form')).map(f => ({
      inputs: f.querySelectorAll('input:not([type=hidden]),textarea,select').length,
      names: Array.from(f.querySelectorAll('input:not([type=hidden]),textarea,select')).map(i => i.name || i.placeholder || i.type).slice(0,8)}));
  const looseInputs = document.querySelectorAll('input[type=tel],input[type=email],input[name*=phone i],input[name*=name i]').length;
  const videos = Array.from(document.querySelectorAll('video')).map(v => (v.currentSrc || v.src || (v.querySelector('source')||{}).src || '')).slice(0,10);
  const svgs = Array.from(document.querySelectorAll('svg')).map(s => s.querySelectorAll('polygon,path,rect').length).filter(n => n >= 15);
  const svgPoly = document.querySelectorAll('svg polygon').length;
  const areas = document.querySelectorAll('map area').length;
  const imgs = document.querySelectorAll('img').length;
  const pdfs = links.filter(l => /\.pdf(\?|$)/i.test(l.h)).map(l => l.h);
  return {iframes: ifr, canvases: canv, links, buttons, scripts, forms, looseInputs, videos, svg_big_counts: svgs,
          svg_polygons: svgPoly, image_map_areas: areas, img_count: imgs, pdf_links: pdfs,
          scrollHeight: Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0),
          text: (document.body ? document.body.innerText : '')};
}"""


def collect(pg):
    d = pg.evaluate(JS_COLLECT)
    # child frames: canvases + text (same-origin or cross-origin frames are both reachable through Playwright)
    frames = []
    for fr in pg.frames:
        if fr == pg.main_frame:
            continue
        info = {"url": fr.url}
        try:
            info["canvas"] = fr.evaluate("() => document.querySelectorAll('canvas').length")
            info["text_len"] = fr.evaluate("() => (document.body ? document.body.innerText.length : 0)")
            info["text_head"] = fr.evaluate("() => (document.body ? document.body.innerText.trim().replace(/\s+/g,' ').slice(0,160) : '')")
            info["inputs"] = fr.evaluate("() => document.querySelectorAll('input:not([type=hidden]),textarea,select').length")
        except Exception as e:
            info["err"] = type(e).__name__
        frames.append(info)
    d["frames"] = frames
    return d


def summarise(d, base_host):
    text = d.pop("text", "")
    words = {w: count_word(text, w) for w in REQUIRED_WORDS}
    extra = {w: count_word(text, w) for w in EXTRA_WORDS}
    snips = {w: ctx_snips(text, w) for w in REQUIRED_WORDS + EXTRA_WORDS
             if w in ("סיור וירטואלי", "360", "תלת מימד", "3D", "בחירת דירה", "בחר דירה", "בחר קומה", "מלאי",
                      "זמינות", "תלת-מימד", "וירטואלי", "סיור", "דירה לדוגמה", "בחרו דירה", "בחירת קומה")}
    snips = {k: v for k, v in snips.items() if v}
    iframe_domains = sorted({urllib.parse.urlparse(f["src"] or f["data_src"]).netloc for f in d["iframes"] if (f["src"] or f["data_src"])})
    script_domains = sorted({urllib.parse.urlparse(s).netloc for s in d["scripts"]})
    seen = set(); cand = []; ext_domains = set()
    for l in d["links"]:
        h = l["h"]; t = l["t"]
        net = urllib.parse.urlparse(h).netloc
        if net and base_host not in net and not h.startswith(("tel:", "mailto:", "javascript:")):
            ext_domains.add(net)
        if h in seen:
            continue
        seen.add(h)
        if LINK_PAT.search(urllib.parse.unquote(h)) or LINK_PAT.search(t):
            if not re.search(r"facebook|instagram|youtube\.com/(?!embed)|linkedin|twitter|waze|whatsapp|tiktok", h, re.I):
                cand.append({"href": urllib.parse.unquote(h), "text": t})
    btn = [b for b in d["buttons"] if LINK_PAT.search(b)]
    return {
        "rendered_text_chars": len(text),
        "words_required": words, "words_extra": extra, "word_contexts": snips,
        "iframe_count": len(d["iframes"]), "iframes": d["iframes"], "iframe_domains": iframe_domains,
        "canvas_count": len(d["canvases"]), "canvases": d["canvases"][:20],
        "frames": d["frames"][:30],
        "viewer_like_iframes": [f for f in d["iframes"] if VIEWER_DOMAINS.search(urllib.parse.urlparse(f["src"] or f["data_src"]).netloc + urllib.parse.urlparse(f["src"] or f["data_src"]).path)
                                and not NOT_VIEWER.search(f["src"] or f["data_src"])],
        "candidate_links_3d_tour_picker": cand[:40], "candidate_buttons": sorted(set(btn))[:40],
        "external_link_domains": sorted(ext_domains)[:60], "script_domains": script_domains[:80],
        "forms": d["forms"], "loose_contact_inputs": d["looseInputs"], "videos": d["videos"],
        "svg_with_15plus_shapes": d["svg_big_counts"][:20], "svg_polygons": d["svg_polygons"],
        "image_map_areas": d["image_map_areas"], "img_count": d["img_count"], "pdf_links": d["pdf_links"][:30],
        "scrollHeight": d["scrollHeight"],
    }


def rtl_wide_capture(ctx, pg, top_path, full_path, H):
    """Workaround for RTL pages with a very wide horizontal overflow, where headless viewport shots come out as the
    empty overflow area: capture beyond the viewport through CDP and crop the right-most 1440 px (where an RTL page starts)."""
    import base64, io
    from PIL import Image
    cdp = ctx.new_cdp_session(pg)
    r = cdp.send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
    im = Image.open(io.BytesIO(base64.b64decode(r["data"]))).convert("RGB")
    w, h = im.size
    x0 = max(0, w - 1440)
    im.crop((x0, 0, w, min(900, h))).save(top_path, "JPEG", quality=80)
    im.crop((x0, 0, w, min(H, h, 9000))).save(full_path, "JPEG", quality=80)
    return {"doc_width": w, "doc_height": h, "crop_x": x0}


def check_page(ctx, url, slug, tag, viewer_selector=None, viewer_click=None, rtl_wide=False):
    pg = ctx.new_page()
    rec = {"tag": tag, "requested_url": url}
    chain = []
    try:
        resp = pg.goto(url, wait_until="domcontentloaded", timeout=70000)
        if resp:
            r = resp.request
            while r.redirected_from:
                r = r.redirected_from
                chain.append(r.url)
            rec["http_status"] = resp.status
        rec["redirect_chain"] = list(reversed(chain))
        try:
            pg.wait_for_load_state("load", timeout=25000)
        except Exception:
            rec["load_timeout"] = True
        pg.wait_for_timeout(7000)
        rec["cookie_declined_with"] = decline_cookies(pg)
        rec["final_url"] = urllib.parse.unquote(pg.url)
        rec["title"] = pg.title()
        top = os.path.join(OUT, f"{slug}{tag}_top.jpg")
        pg.screenshot(path=top, type="jpeg", quality=80)
        rec["shot_top"] = os.path.basename(top)
        if not NO_CLOSE:
            rec["popups_closed"] = close_popups(pg)
        mode, h = slow_scroll(pg)
        rec["scroll_mode"] = mode
        if not NO_CLOSE:
            rec["popups_closed_after_scroll"] = close_popups(pg)
        scroll_to(pg, mode, 0); pg.wait_for_timeout(1200)
        d = collect(pg)
        host = urllib.parse.urlparse(pg.url).netloc.replace("www.", "")
        rec.update(summarise(d, host))
        full = os.path.join(OUT, f"{slug}{tag}_full.jpg")
        H = min(int((h if mode == "element" else rec["scrollHeight"]) or h or 900), 9000)
        if mode == "element":
            rec["inner_scroll_height"] = h
        try:
            # stitched full page: scroll one viewport at a time (keeps 100vh layouts, triggers in-view content)
            from PIL import Image
            import io
            canvas_img = Image.new("RGB", (1440, H), "white")
            y = 0
            while y < H:
                sy = scroll_to(pg, mode, y); pg.wait_for_timeout(700)
                png = pg.screenshot(type="png")
                im = Image.open(io.BytesIO(png)).convert("RGB")
                canvas_img.paste(im, (0, int(sy)))
                if sy + 900 >= H or sy < y - 5:
                    break
                y += 900
            canvas_img.save(full, "JPEG", quality=80)
            rec["shot_full"] = os.path.basename(full); rec["shot_full_height"] = H
            rec["shot_full_method"] = "stitched 1440x900 viewport slices (fixed headers repeat per slice)"
        except Exception as e:
            rec["shot_full_error"] = str(e)[:200]
        finally:
            scroll_to(pg, mode, 0); pg.wait_for_timeout(800)
        if rtl_wide:
            try:
                rec["rtl_wide_capture"] = rtl_wide_capture(ctx, pg, top, full, H)
                rec["shot_full_method"] = "CDP captureBeyondViewport, right-most 1440 px crop (RTL page with wide horizontal overflow renders empty in headless viewport shots)"
            except Exception as e:
                rec["rtl_wide_capture_error"] = str(e)[:200]
        # viewer screenshot: explicit selector, else first viewer-like iframe, else largest canvas
        target = None
        if viewer_selector:
            target = pg.locator(viewer_selector).first
        elif rec["viewer_like_iframes"]:
            src = rec["viewer_like_iframes"][0]["src"] or rec["viewer_like_iframes"][0]["data_src"]
            target = pg.locator(f'iframe[src="{src}"], iframe[data-src="{src}"]').first
        else:
            big = [i for i, c in enumerate(rec["canvases"]) if c["w"] >= 300 and c["h"] >= 250]
            if big:
                target = pg.locator("canvas").nth(big[0])
        if viewer_click:
            # open a tab / button that reveals the viewer (a page control, never a form submit)
            try:
                c = pg.get_by_text(viewer_click, exact=False).first
                c.scroll_into_view_if_needed(timeout=8000)
                c.click(timeout=5000)
                pg.wait_for_timeout(6000)
                rec["viewer_click"] = viewer_click
            except Exception as e:
                rec["viewer_click_error"] = str(e)[:200]
        if target is not None:
            try:
                target.scroll_into_view_if_needed(timeout=8000)
                pg.wait_for_timeout(5000)
                vp = os.path.join(OUT, f"{slug}{tag}_viewer.jpg")
                pg.screenshot(path=vp, type="jpeg", quality=80)
                rec["shot_viewer"] = os.path.basename(vp)
            except Exception as e:
                rec["shot_viewer_error"] = str(e)[:200]
    except Exception as e:
        rec["error"] = f"{type(e).__name__}: {str(e)[:300]}"
        try:
            rec["final_url"] = urllib.parse.unquote(pg.url)
        except Exception:
            pass
    finally:
        pg.close()
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("developer"); ap.add_argument("project"); ap.add_argument("url")
    ap.add_argument("--follow", action="append", default=[])
    ap.add_argument("--viewer-selector", default=None)
    ap.add_argument("--follow-viewer-selector", default=None)
    ap.add_argument("--viewer-click", default=None)
    ap.add_argument("--follow-viewer-click", default=None)
    ap.add_argument("--rtl-wide", action="store_true", help="use the CDP beyond-viewport capture for RTL pages with wide overflow")
    ap.add_argument("--no-close", action="store_true", help="do not press Escape / close popups (for pages whose content is itself an overlay)")
    a = ap.parse_args()
    global NO_CLOSE
    NO_CLOSE = a.no_close
    os.makedirs(OUT, exist_ok=True)
    now = datetime.datetime.now().astimezone()
    result = {"slug": a.slug, "developer": a.developer, "project": a.project,
              "checked_local": now.strftime("%Y-%m-%d %H:%M %Z (UTC%z)"),
              "method": "headless Chrome (Playwright channel=chrome), 1440x900, he-IL, analytics/ads blocked in own context, no login, no form input",
              "pages": []}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL", user_agent=UA,
                            timezone_id="Asia/Jerusalem")
        ctx.route("**/*", lambda r: r.abort() if BLOCK.search(r.request.url) else r.continue_())
        result["pages"].append(check_page(ctx, a.url, a.slug, "", a.viewer_selector, a.viewer_click, a.rtl_wide))
        for i, f in enumerate(a.follow, 1):
            result["pages"].append(check_page(ctx, f, a.slug, f"_follow{i}", a.follow_viewer_selector, a.follow_viewer_click))
        b.close()
    path = os.path.join(OUT, f"{a.slug}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)
    # short console summary
    for pgr in result["pages"]:
        print(f"[{pgr['tag'] or 'main'}] {pgr.get('http_status')} {pgr.get('final_url')} | {pgr.get('title','')[:70]}")
        if pgr.get("error"):
            print("  ERROR", pgr["error"]); continue
        print("  iframes:", pgr["iframe_domains"], "| canvas:", pgr["canvas_count"], "| forms:", [f["inputs"] for f in pgr["forms"]],
              "| videos:", len(pgr["videos"]), "| pdf:", len(pgr["pdf_links"]), "| svg15+:", pgr["svg_with_15plus_shapes"][:5],
              "| areas:", pgr["image_map_areas"], "| h:", pgr["scrollHeight"])
        print("  words:", {k: v for k, v in pgr["words_required"].items() if v})
        print("  extra:", {k: v for k, v in pgr["words_extra"].items() if v})
        for k, v in pgr["word_contexts"].items():
            print("   ctx", k, "::", " || ".join(v)[:300])
        for c in pgr["candidate_links_3d_tour_picker"][:25]:
            print("   link", c["href"][:140], "|", c["text"][:60])
        if pgr["candidate_buttons"]:
            print("   buttons", pgr["candidate_buttons"][:15])
        print("  ext domains:", pgr["external_link_domains"][:25])
        print("  frames:", [(f["url"][:80], f.get("canvas"), f.get("inputs"), (f.get("text_head") or "")[:60]) for f in pgr["frames"][:10] if f["url"] != "about:blank"])
        print("  viewer-like iframes:", [(f["src"] or f["data_src"])[:100] for f in pgr["viewer_like_iframes"]][:6])
        print("  shots:", pgr.get("shot_top"), pgr.get("shot_full"), pgr.get("shot_viewer"), pgr.get("shot_viewer_error", "")[:80], pgr.get("viewer_click_error", "")[:80])


if __name__ == "__main__":
    main()
