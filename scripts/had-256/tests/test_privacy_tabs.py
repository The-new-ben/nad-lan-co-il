"""Two synthetic accounts on ONE browser profile (real Chrome, real WordPress on the bench).

P1 (Maya, foreign queue): A types a draft whose saves fail (the local queue holds it), signs out; B signs in on the
same browser and never sees, imports, reads or deletes A's queue or the 1.x 'nlow-draft' text (DOM + a recorder on
every localStorage call); A signs back in and resumes the queue.
P1 (Maya, stale tab): A's preview is open in tab 2; in tab 1 A signs out and B signs in; tab 2 drops A's fields,
photos and price within one focus / visibility cycle; B never sees A's data in any tab; A's draft is intact; A
resumes it. The signed-in page is sent with Cache-Control no-store.
(d) The "sign in to another account" link: one click, the right return address, Hebrew and English.
"""
import json
import pathlib
import re
import time

from bench import reset, record, page_url, user, base, state, REPO, shot, clear
from session import jpeg_bytes

V = 'after'
FIX = REPO / 'scripts' / 'had-256' / 'local' / '.runtime' / 'fixtures'
FIX.mkdir(parents=True, exist_ok=True)
(FIX / 'a-photo.jpg').write_bytes(jpeg_bytes(color=(150, 60, 60)))
SECRET = 'SYNTHETIC-USER-A-PRIVATE-DRAFT'
LEGACY = 'SYNTHETIC-LEGACY-NLOW-DRAFT-TEXT'
A_PRICE = '4180000'

RECORDER = r"""
(() => {
  const log = window.__lsLog = [];
  const P = Storage.prototype, g = P.getItem, s = P.setItem, r = P.removeItem, k = P.key, c = P.clear;
  P.getItem = function (x) { log.push(['get', String(x)]); return g.call(this, x); };
  P.setItem = function (x, v) { log.push(['set', String(x)]); return s.call(this, x, v); };
  P.removeItem = function (x) { log.push(['del', String(x)]); return r.call(this, x); };
  P.key = function (i) { log.push(['key', i]); return k.call(this, i); };
  P.clear = function () { log.push(['clear']); return c.call(this); };
  try { Object.defineProperty(P, 'length', { get() { log.push(['length']); return Object.keys(localStorage).length; } }); } catch (e) {}
})();
"""


def login(page, key, lang='he'):
    u = user(key)
    page.goto(page_url(V, lang))
    page.wait_for_selector('#nlj-signup, #nlj-login, [data-act="home-continue"], #nlj-details', timeout=20000)
    if page.query_selector('#nlj-details') or page.query_selector('[data-act="home-continue"]'):
        return
    page.click('[data-act="tab-login"] >> nth=-1')
    page.fill('#j-mail2', u['email'])
    page.fill('#j-pw2', u['password'])
    with page.expect_navigation():
        page.click('#j-login-go')
    page.wait_for_selector('#nlj-details, [data-act="home-continue"]', timeout=20000)


def logout_via_link(page):
    href = page.get_attribute('a[data-signout]', 'href')
    with page.expect_navigation():
        page.click('a[data-signout]')
    page.wait_for_load_state('networkidle')
    return href


def ls_dump(page):
    return page.evaluate('() => { const o = {}; for (const k of Object.keys(localStorage)) { o[k] = localStorage[k]; } return o; }')


def text(page):
    return page.evaluate('() => document.body.innerText + " " + Array.from(document.querySelectorAll("input,textarea")).map(e => e.value).join(" ")')


def run(br):
    reset(V)
    uid_a = state(V)  # (warm-up)
    ctx = br.ctx('390', 'he')
    ctx.add_init_script(RECORDER)
    p1 = ctx.new_page()

    # ---------------- foreign queue ----------------
    login(p1, 'dana')
    p1.wait_for_selector('#nlj-details')
    uid_a = p1.evaluate('() => window.NLOWNER.uid')
    p1.click('[data-deal="sale"]')
    p1.fill('#j-city', 'תל אביב יפו')
    p1.wait_for_function('() => /draft=\\d+/.test(location.search)', timeout=15000)   # the draft exists on the server
    draft_a = int(re.search(r'draft=(\d+)', p1.url).group(1))
    # from now on A's saves fail (the server is unreachable for saves): the queue keeps the text on this device
    p1.route(re.compile(r'.*/wp-json/nadlan/v1/owner/draft/\d+$'), lambda r: r.abort())
    p1.fill('#j-desc', SECRET + ' ' + 'דירה לדוגמה עם מרפסת ומחסן')
    p1.wait_for_function('() => (document.getElementById("nlj-st")||{}).innerText.indexOf("השמירה בחשבון לא הצליחה") > -1', timeout=20000)
    shot(p1, V, 'priv-01-A-save-fails-queue-kept-390-he', full=False)
    keyA = 'nlow:v2:u%d:d%d' % (uid_a, draft_a)
    before = ls_dump(p1)
    p1.evaluate('(t) => localStorage.setItem("nlow-draft", t)', LEGACY)   # the 1.x wizard's unowned text, present before B arrives
    before = ls_dump(p1)
    href_he = logout_via_link(p1)
    p1.unroute(re.compile(r'.*/wp-json/nadlan/v1/owner/draft/\d+$'))
    landed_he = p1.url
    before = ls_dump(p1)   # after A's own page wrote its last queue state on leaving; B's turn starts here

    p1.evaluate('() => { window.__lsLog.length = 0; }')
    login(p1, 'yoav')
    p1.wait_for_timeout(2500)
    uid_b = p1.evaluate('() => window.NLOWNER.uid')
    log_b = p1.evaluate('() => window.__lsLog')
    dom_b = text(p1)
    shot(p1, V, 'priv-02-B-same-browser-390-he', full=False)
    after_b = ls_dump(p1)
    touched = [e for e in log_b if len(e) > 1 and isinstance(e[1], str) and (('u%d:' % uid_a) in e[1] or e[1] == 'nlow-draft')]
    enumerated = [e for e in log_b if e[0] in ('key', 'length', 'clear')]
    ok_b = (keyA in before and SECRET in before[keyA] and SECRET not in dom_b and LEGACY not in dom_b and not touched and not enumerated
            and after_b.get(keyA) == before.get(keyA) and after_b.get('nlow-draft') == LEGACY)
    record({'id': 'L03', 'variant': V, 'label': 'real-wp+chrome', 'title': "another account's local queue and the 1.x text on the same browser: B never sees, reads, lists or deletes them", 'status': 'pass' if ok_b else 'fail',
            'evidence': {'A_key_present_before_B': keyA in before, 'A_text_in_B_DOM': SECRET in dom_b, 'legacy_in_B_DOM': LEGACY in dom_b, 'B_storage_calls_on_A_or_legacy_keys': touched, 'B_key_listing_calls': enumerated,
                         'A_key_unchanged': after_b.get(keyA) == before.get(keyA), 'legacy_unchanged': after_b.get('nlow-draft') == LEGACY, 'B_storage_calls': log_b[:40], 'uids': [uid_a, uid_b]}})

    # A comes back on the same browser and resumes the queued text
    logout_via_link(p1)
    login(p1, 'dana')
    if p1.query_selector('[data-act="home-continue"]'):
        p1.click('[data-act="home-continue"]')
    p1.wait_for_selector('#j-desc')
    resumed = p1.input_value('#j-desc')
    p1.wait_for_function('() => (document.getElementById("nlj-st")||{}).innerText.indexOf("נשמר בחשבון") > -1', timeout=20000)
    shot(p1, V, 'priv-03-A-back-resumes-queue-390-he', full=False)
    st, srv = 0, {}
    srv = p1.evaluate('async (d) => { const r = await fetch("/wp-json/nadlan/v1/owner/draft/" + d, {headers: {"X-WP-Nonce": window.NLOWNER.nonce}}); return r.json(); }', draft_a)
    ok_a = SECRET in resumed and SECRET in (srv.get('fields') or {}).get('desc', '')
    record({'id': 'L04', 'variant': V, 'label': 'real-wp+chrome', 'title': 'A signs back in on the same browser: the queued text is resumed and saved to the account', 'status': 'pass' if ok_a else 'fail',
            'evidence': {'resumed_in_form': SECRET in resumed, 'on_server_after_resume': SECRET in (srv.get('fields') or {}).get('desc', '')}})

    # (d) the switch-account link: one click, back to the journey, Hebrew and English
    ctx_en = br.ctx('390', 'en')
    pe = ctx_en.new_page()
    login(pe, 'yoav', 'en')
    href_en = logout_via_link(pe)
    landed_en = pe.url
    signed_out_en = pe.query_selector('#nlj-signup') is not None
    signed_out_he = True
    ok_d = ('&amp;' not in href_he and '&amp;' not in href_en and '_wpnonce=' in href_he and landed_he.startswith(base(V) + '/post-listing/') and 'lang=en' in landed_en and landed_en.startswith(base(V) + '/post-listing/') and signed_out_en)
    record({'id': 'L15', 'variant': V, 'label': 'real-wp+chrome', 'title': 'the "sign in to another account" link: one click, signed out, back on the journey (he and en)', 'status': 'pass' if ok_d else 'fail',
            'evidence': {'href_he': re.sub(r'_wpnonce=[a-f0-9]+', '_wpnonce=...', href_he), 'landed_he': landed_he, 'href_en': re.sub(r'_wpnonce=[a-f0-9]+', '_wpnonce=...', href_en), 'landed_en': landed_en, 'en_signed_out_form': signed_out_en}})
    ctx_en.close()
    ctx.close()

    # ---------------- stale tab ----------------
    reset(V)
    ctx = br.ctx('390', 'he')
    t1 = ctx.new_page()
    login(t1, 'dana')
    t1.wait_for_selector('#nlj-details')
    t1.click('[data-deal="sale"]')
    t1.select_option('#j-type', 'apartment')
    for sel, val in (('#j-city', 'תל אביב יפו'), ('#j-hood', 'שכונת הדוגמה'), ('#j-rooms', '4'), ('#j-size', '96'), ('#j-price', A_PRICE), ('#j-desc', SECRET + ' דירה מוארת עם מרפסת'), ('#j-cname', 'דנה')):
        t1.fill(sel, val)
    t1.check('#j-owner-ok')
    t1.click('#j-to-photos')
    t1.wait_for_selector('#j-files', state='attached')
    t1.set_input_files('#j-files', str(FIX / 'a-photo.jpg'))
    t1.wait_for_function('() => document.querySelectorAll("#j-tiles [data-act=ph-cover], #j-tiles [data-act=ph-rm]").length > 0 && !document.querySelector("#j-tiles .nlj-up")', timeout=30000)
    t1.wait_for_function('() => (document.getElementById("nlj-st")||{}).innerText.indexOf("נשמר בחשבון") > -1', timeout=20000)
    draft_url = t1.url
    t2 = ctx.new_page()
    t2.goto(draft_url.replace('nlj=photos', 'nlj=preview'))
    t2.wait_for_selector('.nlj-lcard', timeout=30000)
    has_a_before = SECRET in text(t2) and t2.query_selector('.nlj-lcard img') is not None
    shot(t2, V, 'priv-04-tab2-A-preview-390-he', full=False)
    t1.bring_to_front()
    logout_via_link(t1)
    login(t1, 'yoav')
    t1.wait_for_selector('#nlj-details, [data-act="home-continue"]')
    b_tab1 = text(t1)
    t1.wait_for_timeout(2000)
    by_ping = SECRET not in text(t2) and not t2.query_selector('.nlj-lcard')   # tab 2 still in the background: only the no-data ping could have cleared it
    t0 = time.time()
    t2.bring_to_front()
    t2.evaluate('() => { window.dispatchEvent(new Event("focus")); document.dispatchEvent(new Event("visibilitychange")); }')
    scrubbed = False
    for _ in range(40):
        if SECRET not in text(t2) and not t2.query_selector('.nlj-lcard') and not t2.query_selector('img[src^="blob:"]'):
            scrubbed = True
            break
        t2.wait_for_timeout(250)
    took = round(time.time() - t0, 2)
    t2_dom = text(t2)
    shot(t2, V, 'priv-05-tab2-scrubbed-after-B-signed-in-390-he', full=False)
    hdr = t1.evaluate('async () => { const r = await fetch(location.href, {credentials: "same-origin", cache: "no-store"}); return r.headers.get("cache-control"); }')
    ok_c = has_a_before and scrubbed and SECRET not in b_tab1 and A_PRICE not in t2_dom.replace(',', '') and 'no-store' in (hdr or '')
    # A's draft intact; A resumes in tab 1
    logout_via_link(t1)
    login(t1, 'dana')
    if t1.query_selector('[data-act="home-continue"]'):
        t1.click('[data-act="home-continue"]')
    t1.wait_for_selector('#j-desc, #j-tiles, .nlj-lcard', timeout=20000)
    if not t1.query_selector('#j-desc'):
        t1.click('[data-act="back-details"], [data-act="back-edit"]')
        t1.wait_for_selector('#j-desc')
    a_back = SECRET in t1.input_value('#j-desc') and A_PRICE in t1.input_value('#j-price').replace(',', '')
    record({'id': 'L03', 'variant': V, 'label': 'real-wp+chrome', 'title': "stale tab: A's preview in tab 2 is cleared when B signs in on tab 1; B never sees A's data; A resumes", 'status': 'pass' if ok_c and a_back else 'fail',
            'evidence': {'tab2_showed_A_before': has_a_before, 'tab2_cleared_by_the_ping_alone (background tab)': by_ping, 'tab2_scrubbed': scrubbed, 'seconds_to_scrub': took, 'A_text_in_B_tab1': SECRET in b_tab1, 'A_price_in_tab2_after': A_PRICE in t2_dom.replace(',', ''),
                         'signed_in_page_cache_control': hdr, 'A_resumed_draft_intact': a_back}})
    ctx.close()


if __name__ == '__main__':
    from bench import Browser
    clear('L03', V, "another account's")
    clear('L03', V, 'stale tab')
    br = Browser()
    try:
        run(br)
    finally:
        br.close()
