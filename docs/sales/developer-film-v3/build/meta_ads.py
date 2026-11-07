# meta_ads.py - read-only look at the public Meta Ad Library for a developer name (HAD-678).
# No login, no ad clicks. Only a "decline optional cookies" button may be pressed. Scrolls to load cards.
# usage: python meta_ads.py <slug> "<query>"
import sys, os, re, json, datetime, urllib.parse
from playwright.sync_api import sync_playwright

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campaign-check"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
BLOCK = re.compile(r"google-analytics|googletagmanager|hotjar|doubleclick|clarity\.ms|tiktok", re.I)


def main():
    slug, q = sys.argv[1], sys.argv[2]
    url = ("https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IL&q="
           + urllib.parse.quote(q) + "&search_type=keyword_unordered")
    now = datetime.datetime.now().astimezone()
    rec = {"slug": slug, "query": q, "url": url, "checked_local": now.strftime("%Y-%m-%d %H:%M %Z (UTC%z)")}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL", user_agent=UA, timezone_id="Asia/Jerusalem")
        ctx.route("**/*", lambda r: r.abort() if BLOCK.search(r.request.url) else r.continue_())
        pg = ctx.new_page()
        try:
            resp = pg.goto(url, wait_until="domcontentloaded", timeout=70000)
            rec["http_status"] = resp.status if resp else None
            pg.wait_for_timeout(9000)
            # decline optional cookies only
            for pat in [r"^(Decline optional cookies|דחיית קובצי Cookie אופציונליים|דחה קובצי Cookie אופציונליים|Only allow essential cookies|אפשר רק קובצי Cookie חיוניים)$"]:
                try:
                    loc = pg.get_by_role("button", name=re.compile(pat, re.I))
                    if loc.count() and loc.first.is_visible():
                        loc.first.click(timeout=3000); pg.wait_for_timeout(1500)
                        rec["cookie_declined"] = True
                except Exception:
                    pass
            rec["final_url"] = pg.url
            rec["title"] = pg.title()
            for _ in range(6):
                pg.mouse.wheel(0, 1200); pg.wait_for_timeout(1200)
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1000)
            text = pg.evaluate("document.body ? document.body.innerText : ''")
            rec["login_wall"] = bool(re.search(r"(Log in|Log In|התחבר|התחברות|כניסה לפייסבוק)", text[:3000])) and not re.search(r"(Library ID|מזהה בספרייה|מזהה ספרייה)", text)
            m = re.search(r"(~?\s?[\d,\.]+\s*(results|תוצאות))|((כ-|~)?\s?[\d,\.]+\s*תוצאות)", text)
            rec["results_line"] = m.group(0) if m else None
            rec["library_id_count_loaded"] = len(re.findall(r"(Library ID|מזהה בספרייה|מזהה ספרייה)", text))
            rec["started_running_lines"] = re.findall(r"(?:Started running on|התחיל לפעול ב(?:תאריך)?)[^\n]{0,30}", text)[:15]
            # landing-domain captions on cards are usually upper-case domain lines
            doms = re.findall(r"\b([A-Z0-9][A-Z0-9\-]+(?:\.[A-Z0-9\-]+)*\.(?:CO\.IL|COM|CO|IL|NET|ORG|ONLINE|SITE))\b", text)
            rec["card_domains"] = sorted(set(doms))[:40]
            low = re.findall(r"\b([a-z0-9][a-z0-9\-]+\.(?:co\.il|com|net|online|site))\b", text)
            rec["lowercase_domains_in_text"] = sorted(set(d for d in low if "facebook" not in d and "instagram" not in d))[:40]
            from collections import Counter
            names = [a or b for a, b in re.findall(r"\n([^\n]{2,60})\nSponsored|\n([^\n]{2,60})\nממומן", text)]
            rec["advertiser_counts_loaded_cards"] = Counter(names).most_common(15)
            rec["cta_buttons"] = Counter(re.findall(r"\n(Learn More|Shop Now|Sign Up|Send WhatsApp Message|Send Message|Contact Us|Get Quote|Book Now|Apply Now|Subscribe|Watch More|Get Offer|Call Now|Download)\n", text)).most_common(10)
            rec["full_text"] = text
            rec["text_head"] = text[:2500]
            rec["text_len"] = len(text)
            rec["img_count"] = pg.evaluate("document.querySelectorAll('img').length")
            rec["video_count"] = pg.evaluate("document.querySelectorAll('video').length")
            shot = os.path.join(OUT, f"meta_{slug}.jpg")
            pg.screenshot(path=shot, type="jpeg", quality=80)
            rec["shot"] = os.path.basename(shot)
            pg.evaluate("window.scrollTo(0, 700)"); pg.wait_for_timeout(2500)
            shot2 = os.path.join(OUT, f"meta_{slug}_cards.jpg")
            pg.screenshot(path=shot2, type="jpeg", quality=80)
            rec["shot_cards"] = os.path.basename(shot2)
        except Exception as e:
            rec["error"] = f"{type(e).__name__}: {str(e)[:300]}"
        b.close()
    with open(os.path.join(OUT, f"meta_{slug}.json"), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in rec.items() if k not in ("text_head", "full_text")}, ensure_ascii=False, indent=0)[:2500])
    print("---- text head ----")
    print(rec.get("text_head", "")[:1500])


if __name__ == "__main__":
    main()
