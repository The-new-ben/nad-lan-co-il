"""L02, L04, L06, L10, L11, L12, L13, L15 in a real Chrome on real WordPress (the AFTER bench), synthetic data.

    python test_journey.py            # all
    python test_journey.py L02 L06    # some
"""
import json
import re
import sys
import time
import urllib.request

from bench import Browser, reset, record, user, page_url, base, mails, state, shot, clear, fault
from screens import fixtures, FIX

V = 'after'
SAVED = 'נשמר בחשבון'


def login(p, key, pw=None):
    u = user(key)
    p.goto(page_url(V))
    p.wait_for_selector('#nlj-signup, #nlj-details, [data-act="home-continue"]')
    if not p.query_selector('#nlj-signup'):
        return
    p.click('[data-act="tab-login"] >> nth=-1')
    p.fill('#j-mail2', u['email'])
    p.fill('#j-pw2', pw or u['password'])
    with p.expect_navigation():
        p.click('#j-login-go')
    p.wait_for_selector('#nlj-details, [data-act="home-continue"]')


def saved(p, t=20000):
    p.wait_for_function('t => (document.getElementById("nlj-st")||{}).innerText.indexOf(t) > -1', arg=SAVED, timeout=t)


def fill(p, **kw):
    v = {'city': 'תל אביב יפו', 'hood': 'שכונת הדוגמה', 'rooms': '4', 'size': '96', 'floor': '3 מתוך 8', 'price': '3450000', 'desc': 'דירה מוארת בקומה שלישית, שלושה כיווני אוויר ומרפסת שמש. חניה ומחסן.', 'cname': 'דנה'}
    v.update(kw)
    p.click('[data-deal="%s"]' % v.pop('deal', 'sale'))
    p.select_option('#j-type', v.pop('ptype', 'apartment'))
    for k, val in v.items():
        p.fill('#j-' + k, val)
    p.check('#j-owner-ok')
    saved(p)


def to_photos(p, files=('living.jpg',)):
    p.click('#j-to-photos')
    p.wait_for_selector('#j-files', state='attached')
    if files:
        p.set_input_files('#j-files', [str(FIX / f) for f in files])
        p.wait_for_function('n => document.querySelectorAll("#j-tiles [data-act=ph-rm]").length >= n && !document.querySelector("#j-tiles .nlj-up")', arg=len(files), timeout=60000)
        saved(p)


def anon_status(url):
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''


def L02(br):
    reset(V)
    c = br.ctx('390', 'he')
    p = c.new_page()
    login(p, 'dana')
    fill(p, desc='דירה לדוגמה לבדיקת שחזור הסיסמה, עם מרפסת ומחסן.')
    draft_url = p.url
    href = p.get_attribute('a[data-signout]', 'href')
    with p.expect_navigation():
        p.click('a[data-signout]')
    p.click('[data-act="tab-login"] >> nth=-1')
    p.click('[data-act="tab-recover"]')
    p.fill('#j-mail3', user('dana')['email'])
    p.click('#j-rec-go')
    p.wait_for_selector('#nlj-recover .nlj-status--ok')
    m = [x for x in mails(V) if x['to'] == user('dana')['email'] or user('dana')['email'] in json.dumps(x['to'])]
    body = m[-1]['message'] if m else ''
    link = re.search(r'(http://127\.0\.0\.1:\d+/wp-login\.php\?[^\s<>]*action=rp[^\s<>]*)', body)
    back = re.search(r'(http://127\.0\.0\.1:\d+/post-listing/[^\s<>]*)', body)
    link = link.group(1) if link else ''
    p.goto(link)
    p.wait_for_selector('#pass1')
    new_pw = 'New-Sample-Dana-2026!'
    p.fill('#pass1', new_pw)
    if p.query_selector('#pass2') and p.is_visible('#pass2'):
        p.fill('#pass2', new_pw)
    if p.query_selector('.pw-weak input') and p.is_visible('.pw-weak input'):
        p.check('.pw-weak input')
    p.click('#wp-submit')
    p.wait_for_load_state('networkidle')
    reset_ok = 'reset' in p.inner_text('body').lower()
    shot(p, V, 'L02-password-reset-done', full=False)
    # used again: refused
    p.goto(link)
    p.wait_for_load_state('networkidle')
    reused = p.url
    reused_refused = 'invalidkey' in reused or 'expiredkey' in reused or 'invalid' in p.inner_text('body').lower()
    # back to the draft: the address from the mail, sign in with the new password, the draft is there
    p.goto(back.group(1) if back else page_url(V))
    login(p, 'dana', pw=new_pw)
    if p.query_selector('[data-act="home-continue"]'):
        p.click('[data-act="home-continue"]')
    p.wait_for_selector('#j-desc')
    resumed = 'שחזור הסיסמה' in p.input_value('#j-desc')
    shot(p, V, 'L02-back-to-the-draft', full=False)
    # an expired link: the bench shortens the key's life to 2 seconds
    fault(V, 'reset_ttl', {'secs': 2})
    s = urllib.request.Request(base(V) + '/wp-json/nadlan/v1/owner/account/recover', data=json.dumps({'email': user('dana')['email']}).encode(), headers={'Content-Type': 'application/json'}, method='POST')
    urllib.request.urlopen(s).read()
    body2 = mails(V)[-1]['message']
    link2 = re.search(r'(http://127\.0\.0\.1:\d+/wp-login\.php\?[^\s<>]*action=rp[^\s<>]*)', body2).group(1)
    time.sleep(4)
    p.goto(link2)
    p.wait_for_load_state('networkidle')
    expired = 'expiredkey' in p.url or 'invalidkey' in p.url
    fault(V, 'reset_ttl', None)
    c.close()
    ok = bool(link) and reset_ok and reused_refused and resumed and expired and bool(back)
    record({'id': 'L02', 'variant': V, 'label': 'real-wp+chrome', 'title': "recovery: WordPress' own reset link (mail sink), used once, refused when used again or expired; the mail leads back to the draft", 'status': 'pass' if ok else 'fail',
            'evidence': {'mail_has_reset_link': bool(link), 'mail_has_way_back': bool(back), 'reset_done': reset_ok, 'used_again': reused, 'refused': reused_refused, 'expired_link_refused': expired, 'draft_resumed_after_new_password': resumed}})


def L04_L10(br):
    reset(V)
    fixtures()
    c = br.ctx('390', 'he')
    p = c.new_page()
    login(p, 'dana')
    fill(p)
    to_photos(p, ('living.jpg', 'kitchen.jpg'))
    # cover = the second photo, then reload: order and cover from the server
    tiles = p.evaluate('() => Array.from(document.querySelectorAll("#j-tiles img")).map(i => i.getAttribute("src"))')
    p.click('#j-tiles li:nth-child(2) [data-act="ph-cover"]')
    saved(p)
    st_text = p.inner_text('#nlj-st')
    p.reload()
    p.wait_for_selector('#j-tiles li')
    p.wait_for_timeout(800)
    after = p.evaluate('() => Array.from(document.querySelectorAll("#j-tiles img")).map(i => i.getAttribute("src"))')
    ref = lambda u: re.search(r'r=([a-f0-9]{32})', u).group(1)
    order_ok = [ref(x) for x in after] == [ref(tiles[1]), ref(tiles[0])]
    shot(p, V, 'L04-reload-order-and-cover', full=False)
    record({'id': 'L04', 'variant': V, 'label': 'real-wp+chrome', 'title': 'autosave, reload: fields, photos, their order and the cover come back from the server; the status shows the server time', 'status': 'pass' if order_ok and 'השמירה האחרונה ב' in st_text else 'fail',
            'evidence': {'order_after_reload_is_the_saved_order': order_ok, 'status_line': st_text}})
    # L10 remove a photo while it uploads; the upload finishes; it must not come back
    n0 = len(json.loads(json.dumps(state(V)['attachments'])))
    p.route(re.compile(r'.*/owner/photo$'), lambda r: (time.sleep(2.5), r.continue_()))
    p.set_input_files('#j-files', [str(FIX / 'living.jpg')])
    p.wait_for_selector('#j-tiles .nlj-up')
    p.click('#j-tiles .nlj-up [data-act="ph-rm"]')
    p.wait_for_timeout(4000)
    p.unroute(re.compile(r'.*/owner/photo$'))
    saved(p)
    p.reload()
    p.wait_for_selector('#j-tiles li')
    p.wait_for_timeout(800)
    count_removed = len(p.query_selector_all('#j-tiles li'))
    # refresh during an upload: the photos the server took are not lost
    p.route(re.compile(r'.*/owner/photo$'), lambda r: (time.sleep(1.0), r.continue_()))
    p.set_input_files('#j-files', [str(FIX / 'living.jpg'), str(FIX / 'kitchen.jpg')])
    p.wait_for_function('() => document.querySelectorAll("#j-tiles [data-act=ph-rm]").length >= 3 && document.querySelector("#j-tiles .nlj-up")', timeout=30000)
    p.reload()
    p.unroute(re.compile(r'.*/owner/photo$'))
    p.wait_for_selector('#j-tiles li')
    p.wait_for_timeout(1500)
    count_refresh = len(p.query_selector_all('#j-tiles li'))
    saved(p)
    shot(p, V, 'L10-after-refresh-during-upload', full=False)
    c.close()
    record({'id': 'L10', 'variant': V, 'label': 'real-wp+chrome', 'title': 'a photo removed while uploading does not come back; a refresh during uploads keeps every photo the server took', 'status': 'pass' if count_removed == 2 and count_refresh >= 3 else 'fail',
            'evidence': {'tiles_after_remove_during_upload (expected 2)': count_removed, 'tiles_after_refresh_during_upload (expected 3 or 4)': count_refresh}})


def L06(br):
    for mode, script in (('blocked (SecurityError)', "Object.defineProperty(window, 'localStorage', {get() { throw new DOMException('blocked', 'SecurityError'); }});"),
                         ('full (QuotaExceededError)', "Storage.prototype.setItem = function () { throw new DOMException('full', 'QuotaExceededError'); };")):
        reset(V)
        c = br.ctx('390', 'he')
        c.add_init_script(script)
        p = c.new_page()
        errs = []
        p.on('pageerror', lambda e: errs.append(str(e)))
        login(p, 'dana')
        fill(p)
        txt = p.inner_text('#nlj-st')
        note = 'השמירה במכשיר חסומה' in txt
        shot(p, V, 'L06-storage-%s' % mode.split()[0], full=False)
        c.close()
        record({'id': 'L06', 'variant': V, 'label': 'real-wp+chrome', 'title': 'local storage %s: no crash, the limit is shown, the account save still works' % mode, 'status': 'pass' if note and not errs and SAVED in txt else 'fail',
                'evidence': {'status_text': txt, 'js_errors': errs}})


def L11(br):
    reset(V)
    c = br.ctx('390', 'he')
    p = c.new_page()
    login(p, 'dana')
    fill(p)
    # an expired nonce: the page gets a fresh one and the save goes through
    p.evaluate('() => { window.NLOWNER.nonce = "0000000000"; }')
    p.fill('#j-rooms', '5')
    saved(p)
    nonce_ok = p.evaluate('() => window.NLOWNER.nonce !== "0000000000"')
    # a 5xx on save: the honest status, a retry, the content kept
    p.route(re.compile(r'.*/owner/draft/\d+$'), lambda r: r.fulfill(status=503, body='{"code":"down","message":"down"}', content_type='application/json') if r.request.method == 'POST' else r.continue_())
    p.fill('#j-rooms', '6')
    p.wait_for_selector('#nlj-st .nlj-status--bad')
    s5 = p.inner_text('#nlj-st')
    shot(p, V, 'L11-save-5xx', full=False)
    p.unroute(re.compile(r'.*/owner/draft/\d+$'))
    p.click('#nlj-st [data-act="retry"]')
    saved(p)
    # a 429 on save
    p.route(re.compile(r'.*/owner/draft/\d+$'), lambda r: r.fulfill(status=429, body='{"code":"rate","message":"יותר מדי פעולות בזמן קצר. מה שכתבתם שמור; נסו שוב בעוד כמה דקות."}', content_type='application/json') if r.request.method == 'POST' else r.continue_())
    p.fill('#j-rooms', '7')
    p.wait_for_selector('#nlj-st .nlj-status--bad')
    s429 = p.inner_text('#nlj-st')
    p.unroute(re.compile(r'.*/owner/draft/\d+$'))
    p.click('#nlj-st [data-act="retry"]')
    saved(p)
    # the session ends in another tab: this page is cleared (another person may use the device), the text waits on the device
    p2 = c.new_page()
    p2.goto(page_url(V))
    p2.wait_for_selector('a[data-signout]')
    with p2.expect_navigation():
        p2.click('a[data-signout]')
    p.bring_to_front()
    p.wait_for_selector('#nlj-app [role="alert"] .nlj-h1', timeout=15000)
    cleared = 'דירה מוארת' not in p.inner_text('body')
    shot(p, V, 'L11-session-ended-elsewhere', full=False)
    # sign in again: the draft comes back, nothing was published on its own
    login(p, 'dana')
    if p.query_selector('[data-act="home-continue"]'):
        p.click('[data-act="home-continue"]')
    p.wait_for_selector('#j-rooms')
    back_ok = p.input_value('#j-rooms') == '7'
    published = [x for x in state(V)['properties'] if x['post_status'] == 'publish']
    c.close()
    ok = nonce_ok and 'השמירה בחשבון לא הצליחה' in s5 and 'יותר מדי פעולות' in s429 and cleared and back_ok and not published
    record({'id': 'L11', 'variant': V, 'label': 'real-wp+chrome', 'title': 'expired nonce, 5xx, 429, a session ended elsewhere: content kept, a way back, nothing published on its own', 'status': 'pass' if ok else 'fail',
            'evidence': {'nonce_refreshed': nonce_ok, 'status_on_5xx': s5, 'status_on_429': s429, 'page_cleared_when_signed_out_elsewhere': cleared, 'draft_back_after_sign_in (rooms 7)': back_ok, 'listings_published': len(published)},
            'notes': 'AI timeout: not applicable, the journey makes no model call (copy = the template + the owner\'s own words).'})


def L12_L13(br):
    reset(V)
    fixtures()
    c = br.ctx('390', 'he')
    p = c.new_page()
    login(p, 'dana')
    fill(p)
    to_photos(p, ('living.jpg',))
    p.click('#j-to-preview')
    p.wait_for_selector('.nlj-lcard')
    # back to edit: a new price and city, then the preview again
    p.click('[data-act="back-edit"]')
    p.fill('#j-price', '3290000')
    p.fill('#j-city', 'רמת גן')
    p.fill('#j-hood', 'שכונת המבחן')
    saved(p)
    p.click('#j-to-photos')
    p.click('#j-to-preview')
    p.wait_for_selector('.nlj-lcard')
    pv = p.inner_text('.nlj-lcard')
    p.click('#j-publish')
    p.wait_for_selector('.nlj-okmark', timeout=60000)
    url = p.get_attribute('a.nlj-btn--primary', 'href')
    st, html = anon_status(url)
    body = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', html)
    ok12 = '3,290,000' in pv and 'רמת גן' in pv and st == 200 and '3,290,000' in body and 'רמת גן' in body and '3,450,000' not in body and 'wa.me/972500000000' not in html and 'tel:+972500000000' not in html and '050-0000000' not in body and 'ramat-gan' in url
    record({'id': 'L12', 'variant': V, 'label': 'real-wp+chrome', 'title': 'preview, fix price and place, publish: the page carries the approved values, nothing else; no phone without consent', 'status': 'pass' if ok12 else 'fail',
            'evidence': {'url': url, 'http': st, 'price_and_city_on_page': ['3,290,000' in body, 'רמת גן' in body], 'old_price_absent': '3,450,000' not in body, 'owner_phone_whatsapp_call_or_number_on_page': ('wa.me/972500000000' in html, 'tel:+972500000000' in html, '050-0000000' in body), 'note': "the site's own floating bar (#nlcta) carries the SITE's WhatsApp number; it is not the owner's"}})
    # L13: a hold, a fix, live; sold; removed; back
    p.click('[data-act="go-mine"] >> nth=-1')
    p.wait_for_selector('[data-act="L-edit"]')
    p.click('[data-act="L-edit"]')
    p.wait_for_selector('#j-desc')
    p.fill('#j-desc', 'דירה מוארת בקומה שלישית, מתאים למשפחות, מרפסת שמש. חניה ומחסן.')
    saved(p)
    p.click('#j-to-photos')
    p.click('#j-to-preview')
    p.wait_for_selector('.nlj-lcard')
    hold_note = 'בדיקה של אדם' in p.inner_text('#nlj-pv')
    p.click('#j-publish')
    p.wait_for_selector('.nlj-okmark', timeout=60000)
    held_title = p.inner_text('.nlj-h1')
    held_http = anon_status(url)[0]
    p.click('[data-act="go-mine"] >> nth=-1')
    p.wait_for_selector('.nlj-chip--warn')
    chip_pending = p.inner_text('.nlj-chip--warn')
    shot(p, V, 'L13-held-in-my-listings', full=False)
    p.click('[data-act="L-edit"]')
    p.wait_for_selector('#j-desc')
    p.fill('#j-desc', 'דירה מוארת בקומה שלישית, מרפסת שמש. חניה ומחסן.')
    saved(p)
    p.click('#j-to-photos')
    p.click('#j-to-preview')
    p.wait_for_selector('.nlj-lcard')
    p.click('#j-publish')
    p.wait_for_selector('.nlj-okmark', timeout=60000)
    live_http = anon_status(url)[0]
    p.click('[data-act="go-mine"] >> nth=-1')
    p.wait_for_selector('[data-act="L-mark"]')
    p.click('[data-act="L-mark"]')
    p.click('[data-act="L-mark-yes"]')
    p.wait_for_selector('[data-act="L-active"]')
    sold_http, sold_html = anon_status(url)
    sold_bar = 'nlx-soldbar' in sold_html and 'הנכס נמכר' in sold_html
    p.click('[data-act="L-active"]')
    p.wait_for_selector('[data-act="L-rm"]')
    p.click('[data-act="L-rm"]')
    p.click('[data-act="L-rm-yes"]')
    p.wait_for_selector('[data-act="L-republish"]')
    removed_http = anon_status(url)[0]
    shot(p, V, 'L13-removed-in-my-listings', full=False)
    p.click('[data-act="L-republish"]')
    p.wait_for_selector('.nlj-chip--live')
    back_http = anon_status(url)[0]
    c.close()
    ok13 = hold_note and 'בדיקה' in held_title and held_http == 404 and 'בבדיקה' in chip_pending and live_http == 200 and sold_http == 200 and sold_bar and removed_http == 404 and back_http == 200
    record({'id': 'L13', 'variant': V, 'label': 'real-wp+chrome', 'title': 'held, fixed, live, sold (the page says so, the contact buttons go), removed (gone), published again: the screen matches the server', 'status': 'pass' if ok13 else 'fail',
            'evidence': {'preview_warned_of_the_hold': hold_note, 'published_screen_when_held': held_title, 'anonymous_http': {'held': held_http, 'fixed': live_http, 'sold': sold_http, 'removed': removed_http, 'published_again': back_http}, 'my_listings_chip_when_held': chip_pending, 'sold_notice_on_page': sold_bar}})


def L15(br):
    reset(V)
    fixtures()
    c = br.ctx('390', 'he')
    p = c.new_page()
    login(p, 'dana')
    fill(p)
    to_photos(p, ('living.jpg',))
    p.click('#j-to-preview')
    p.wait_for_selector('.nlj-lcard')
    trail = []
    p.go_back()
    p.wait_for_selector('#j-tiles li')
    trail.append(('back', 'photos', len(p.query_selector_all('#j-tiles li'))))
    p.go_back()
    p.wait_for_selector('#j-desc')
    trail.append(('back', 'details', p.input_value('#j-city')))
    p.go_forward()
    p.wait_for_selector('#j-tiles li')
    trail.append(('forward', 'photos', len(p.query_selector_all('#j-tiles li'))))
    bar = p.query_selector('#nlcta a') is not None
    c.close()
    ok = trail[0][2] == 1 and trail[1][2] == 'תל אביב יפו' and trail[2][2] == 1 and bar
    record({'id': 'L15', 'variant': V, 'label': 'real-wp+chrome', 'title': 'back and forward between the steps keep the draft; the floating bar is on the page', 'status': 'pass' if ok else 'fail', 'evidence': {'trail': trail, 'floating_bar_present': bar}})


if __name__ == '__main__':
    want = sys.argv[1:] or ['L02', 'L04', 'L06', 'L11', 'L12', 'L15']
    br = Browser()
    try:
        for name, fn, ids in (('L02', L02, ['L02']), ('L04', L04_L10, ['L04', 'L10']), ('L06', L06, ['L06']), ('L11', L11, ['L11']), ('L12', L12_L13, ['L12', 'L13']), ('L15', L15, ['L15'])):
            if name in want:
                for i in ids:
                    clear(i, V, '')
                try:
                    fn(br)
                except Exception as e:   # one broken scenario must not hide the others; it is recorded as a fail
                    record({'id': ids[0], 'variant': V, 'label': 'real-wp+chrome', 'title': '%s scenario stopped' % name, 'status': 'fail', 'evidence': {'error': str(e)[:600]}})
    finally:
        br.close()
