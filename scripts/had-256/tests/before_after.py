"""BEFORE / AFTER in a real Chrome on the two benches (BEFORE = 6e9cf930 on :9411, AFTER = this worktree on :9401),
the same key scenarios, at 390 Hebrew, 320 Hebrew, 390 English and 1440 Hebrew. Screenshots: docs/qa/had-256/shots/<variant>/ba-*.png.
The engine scenarios (double submit, parallel publish, crash between insert and result) are proven over HTTP in
test_engine.py / engine_after.py; here they are shown as the user sees them.

    python before_after.py before
    python before_after.py after
"""
import re
import sys
import time

from bench import Browser, reset, record, shot, user, page_url, base, state, fault, clear
from screens import fixtures, FIX

SETS = [('390', 'he'), ('320', 'he'), ('390', 'en'), ('1440', 'he')]
TEXT_HE = 'למכירה, 4 חדרים, 96 מ״ר, קומה 3 מתוך 8. שכונת הדוגמה, תל אביב יפו. 3,450,000 ש״ח.'


def wp_login(page, V, key, lang='he'):
    u = user(key)
    page.goto(base(V) + '/wp-login.php')
    page.fill('#user_login', u['email'])
    page.fill('#user_pass', u['password'])
    with page.expect_navigation():
        page.click('#wp-submit')
    page.goto(page_url(V, lang))


def before(br):
    V = 'before'
    notes = {}
    for vp, lang in SETS:
        tag = '%s-%s' % (vp, lang)
        reset(V)
        fixtures()
        c = br.ctx(vp, lang)
        p = c.new_page()
        p.goto(page_url(V, lang))
        p.wait_for_selector('#nlow-gate')
        shot(p, V, 'ba-01-account-%s' % tag)
        p.fill('#nlowg-name', 'דנה')
        p.fill('#nlowg-email', user('dana')['email'])
        p.click('#nlowg-go')
        p.wait_for_selector('#nlowg-err:not([hidden])')
        notes['existing_email'] = p.inner_text('#nlowg-err')
        shot(p, V, 'ba-02-existing-email-%s' % tag)
        # recovery: 1.0 has none in the flow; WordPress' own form (the gate's "כניסה" leads to /login/ by auth.php)
        p.goto(base(V) + '/wp-login.php?action=lostpassword')
        p.fill('#user_login', 'nobody.sample@example.test')
        p.click('#wp-submit')
        p.wait_for_load_state('networkidle')
        notes['recovery_unknown_email'] = p.inner_text('#login_error') if p.query_selector('#login_error') else p.inner_text('body')[:200]
        shot(p, V, 'ba-03-recovery-unknown-email-%s' % tag)
        wp_login(p, V, 'dana', lang)
        p.wait_for_selector('#nlow-f')
        p.fill('#nlow-name', 'דנה')
        p.fill('#nlow-phone', '050-0000000')
        p.fill('#nlow-txt', TEXT_HE)
        p.set_input_files('#nlow-files', [str(FIX / 'living.jpg'), str(FIX / 'broken.jpg')])
        p.wait_for_function('() => document.querySelectorAll("#nlow-thumbs li[data-s=ok], #nlow-thumbs li[data-s=err]").length === 2', timeout=60000)
        notes['corrupt_jpeg_accepted'] = p.evaluate('() => Array.from(document.querySelectorAll("#nlow-thumbs li")).map(l => l.getAttribute("data-s"))')
        # a photo that fails on the way (the server answers 503 once)
        p.route(re.compile(r'.*/owner/photo$'), lambda r: r.fulfill(status=503, body='{"code":"down"}', content_type='application/json'))
        p.set_input_files('#nlow-files', [str(FIX / 'kitchen.jpg')])
        p.wait_for_selector('#nlow-thumbs li[data-s=err]', timeout=30000)
        p.unroute(re.compile(r'.*/owner/photo$'))
        p.check('#nlow-owner')
        p.check('#nlow-consent')
        p.click('#nlow-send')
        p.wait_for_selector('#nlow-status:not([hidden])')
        p.wait_for_timeout(800)
        notes['failed_photo'] = p.inner_text('#nlow-status')
        shot(p, V, 'ba-04-failed-photo-%s' % tag)
        # offline: only the text is kept, origin-wide; the photos are gone after a reload
        c.set_offline(True)
        p.fill('#nlow-txt', TEXT_HE + ' (נכתב בלי חיבור)')
        p.click('#nlow-thumbs li[data-s=err] .x')
        p.click('#nlow-send')
        p.wait_for_timeout(1500)
        notes['offline_send'] = p.inner_text('#nlow-status')
        shot(p, V, 'ba-05-offline-send-%s' % tag)
        c.set_offline(False)
        p.reload()
        p.wait_for_selector('#nlow-f')
        notes['after_reload'] = {'text_kept': 'נכתב בלי חיבור' in p.input_value('#nlow-txt'), 'photos_kept': len(p.query_selector_all('#nlow-thumbs li')), 'storage_key': p.evaluate('() => Object.keys(localStorage).filter(k => k.indexOf("nlow") === 0)')}
        shot(p, V, 'ba-06-after-reload-%s' % tag)
        # two tabs: one origin-wide key, the last keystroke wins silently
        p2 = c.new_page()
        p2.goto(page_url(V, lang))
        p2.wait_for_selector('#nlow-f')
        p.fill('#nlow-txt', 'טקסט מלשונית 1')
        p2.fill('#nlow-txt', 'טקסט מלשונית 2')
        p.reload()
        p.wait_for_selector('#nlow-f')
        notes['two_tabs_tab1_after_reload'] = p.input_value('#nlow-txt')
        shot(p, V, 'ba-07-two-tabs-tab1-reloaded-%s' % tag)
        p2.close()
        # the same listing sent twice in the UI (no AI on the bench: the plain reading misses the place, so each send is
        # held for "missing details", and each send is a new submission)
        p.fill('#nlow-name', 'דנה')
        p.fill('#nlow-phone', '050-0000000')
        p.fill('#nlow-txt', TEXT_HE)
        p.set_input_files('#nlow-files', [str(FIX / 'living.jpg')])
        p.wait_for_function('() => document.querySelectorAll("#nlow-thumbs li[data-s=ok]").length >= 1', timeout=60000)
        p.check('#nlow-owner')
        p.check('#nlow-consent')
        p.click('#nlow-send')
        p.wait_for_function('() => !document.getElementById("nlow-send").disabled', timeout=60000)
        p.click('#nlow-send')
        p.wait_for_function('() => !document.getElementById("nlow-send").disabled', timeout=60000)
        p.wait_for_timeout(500)
        drops = [d for d in state(V)['drops']]
        notes['two_sends_drops'] = len(drops)
        notes['held_answer'] = p.inner_text('#nlow-status')
        shot(p, V, 'ba-08-two-sends-%s' % tag)
        c.close()
        record({'id': 'BA', 'variant': V, 'label': 'real-wp+chrome', 'title': 'before (6e9cf930): the journey as it is (%s)' % tag, 'status': 'info', 'evidence': dict(notes)})


def after(br):
    V = 'after'
    for vp, lang in SETS:
        tag = '%s-%s' % (vp, lang)
        he = lang == 'he'
        notes = {}
        reset(V)
        fixtures()
        c = br.ctx(vp, lang)
        p = c.new_page()
        p.goto(page_url(V, lang))
        p.wait_for_selector('#nlj-signup')
        shot(p, V, 'ba-01-account-%s' % tag)
        p.fill('#j-name', 'דנה' if he else 'Dana')
        p.fill('#j-mail', user('dana')['email'])
        p.fill('#j-pw', 'Another-pass-1')
        p.click('#j-signup-go')
        p.wait_for_selector('#j-mail-err')
        notes['existing_email'] = {'message': p.inner_text('#j-mail-err'), 'input_kept': p.input_value('#j-mail') == user('dana')['email']}
        shot(p, V, 'ba-02-existing-email-%s' % tag)
        p.click('[data-act="exists-login"]')
        p.click('[data-act="tab-recover"]')
        p.fill('#j-mail3', 'nobody.sample@example.test')
        p.click('#j-rec-go')
        p.wait_for_selector('#nlj-recover .nlj-status--ok')
        notes['recovery_unknown_email'] = p.inner_text('#nlj-recover .nlj-status--ok')
        shot(p, V, 'ba-03-recovery-unknown-email-%s' % tag)
        p.click('[data-act="tab-login"] >> nth=-1')
        p.fill('#j-mail2', user('dana')['email'])
        p.fill('#j-pw2', user('dana')['password'])
        with p.expect_navigation():
            p.click('#j-login-go')
        p.wait_for_selector('#nlj-details')
        p.click('[data-deal="sale"]')
        p.select_option('#j-type', 'apartment')
        for k, v in {'#j-city': 'תל אביב יפו', '#j-hood': 'שכונת הדוגמה', '#j-rooms': '4', '#j-size': '96', '#j-floor': '3', '#j-price': '3450000', '#j-desc': 'דירה מוארת בקומה שלישית, שלושה כיווני אוויר ומרפסת שמש. חניה ומחסן.', '#j-cname': 'דנה' if he else 'Dana'}.items():
            p.fill(k, v)
        p.check('#j-owner-ok')
        p.wait_for_function('t => (document.getElementById("nlj-st")||{}).innerText.indexOf(t) > -1', arg='נשמר בחשבון' if he else 'Saved in your account', timeout=20000)
        # offline: the device keeps it, the status says so; back online it is saved to the account
        c.set_offline(True)
        p.evaluate('() => window.dispatchEvent(new Event("offline"))')
        p.fill('#j-desc', 'דירה מוארת בקומה שלישית. נכתב בלי חיבור.')
        p.wait_for_timeout(1500)
        notes['offline_status'] = p.inner_text('#nlj-st')
        shot(p, V, 'ba-05-offline-%s' % tag)
        c.set_offline(False)
        p.evaluate('() => window.dispatchEvent(new Event("online"))')
        p.wait_for_function('t => (document.getElementById("nlj-st")||{}).innerText.indexOf(t) > -1', arg='נשמר בחשבון' if he else 'Saved in your account', timeout=20000)
        notes['back_online_status'] = p.inner_text('#nlj-st')
        p.reload()
        p.wait_for_selector('#j-desc')
        notes['after_reload'] = {'text_kept': 'נכתב בלי חיבור' in p.input_value('#j-desc'), 'storage_keys': p.evaluate('() => Object.keys(localStorage).filter(k => k.indexOf("nlow") === 0)')}
        shot(p, V, 'ba-06-after-reload-%s' % tag)
        # the same draft open elsewhere (a second browser profile = another device or a tab without the tab channel),
        # both edit from the same revision
        c2 = br.ctx(vp, lang)
        p2 = c2.new_page()
        p2.goto(page_url(V, lang))
        p2.click('[data-act="tab-login"] >> nth=-1')
        p2.fill('#j-mail2', user('dana')['email'])
        p2.fill('#j-pw2', user('dana')['password'])
        with p2.expect_navigation():
            p2.click('#j-login-go')
        p2.goto(p.url)
        p2.wait_for_selector('#j-desc')
        p.fill('#j-rooms', '5')
        p.wait_for_function('t => (document.getElementById("nlj-st")||{}).innerText.indexOf(t) > -1', arg='נשמר בחשבון' if he else 'Saved in your account', timeout=20000)
        p2.fill('#j-size', '120')
        p2.wait_for_selector('[data-act="cf-load"]', timeout=20000)
        notes['two_tabs'] = p2.inner_text('#nlj-st')[:300]
        shot(p2, V, 'ba-07-two-tabs-conflict-%s' % tag)
        notes['conflict_lists_rooms'] = ('חדרים' if he else 'Rooms') in p2.inner_text('#nlj-st')
        p2.click('[data-act="cf-keep"]')
        p2.wait_for_function('t => (document.getElementById("nlj-st")||{}).innerText.indexOf(t) > -1', arg='נשמר בחשבון' if he else 'Saved in your account', timeout=20000)
        c2.close()
        p.reload()
        p.wait_for_selector('#j-size')
        notes['two_tabs_result'] = {'rooms': p.input_value('#j-rooms'), 'size': p.input_value('#j-size')}
        # a failed photo, retried alone
        p.click('#j-to-photos')
        p.wait_for_selector('#j-files', state='attached')
        p.set_input_files('#j-files', [str(FIX / 'living.jpg'), str(FIX / 'kitchen.jpg')])
        p.wait_for_function('() => document.querySelectorAll("#j-tiles [data-act=ph-rm]").length === 2 && !document.querySelector("#j-tiles .nlj-up")', timeout=60000)
        fault(V, 'kill', None)
        p.route(re.compile(r'.*/owner/photo$'), lambda r: r.fulfill(status=503, body='{"code":"down"}', content_type='application/json'))
        p.set_input_files('#j-files', [str(FIX / 'living.jpg')])
        p.wait_for_selector('#j-tiles .is-fail', timeout=30000)
        notes['failed_photo'] = p.inner_text('#j-tiles .is-fail')
        shot(p, V, 'ba-04-failed-photo-%s' % tag)
        p.unroute(re.compile(r'.*/owner/photo$'))
        p.click('#j-tiles .is-fail [data-act="ph-retry"]')
        p.wait_for_function('() => !document.querySelector("#j-tiles .is-fail") && !document.querySelector("#j-tiles .nlj-up") && document.querySelectorAll("#j-tiles li").length === 3', timeout=60000)
        notes['after_retry'] = {'tiles': len(p.query_selector_all('#j-tiles li')), 'failed': len(p.query_selector_all('#j-tiles .is-fail'))}
        p.wait_for_function('t => (document.getElementById("nlj-st")||{}).innerText.indexOf(t) > -1', arg='נשמר בחשבון' if he else 'Saved in your account', timeout=20000)
        shot(p, V, 'ba-04b-retried-%s' % tag)
        # publish: a double click, the server answer lost on the first try, then the same request again
        p.click('#j-to-preview')
        p.wait_for_selector('#j-publish:not([disabled])', timeout=30000)
        lost = {'n': 0}

        def drop_first(route):
            if lost['n'] == 0:
                lost['n'] += 1
                resp = route.fetch()          # the server publishes...
                route.abort()                 # ...and the answer never reaches the page
            else:
                route.continue_()
        p.route(re.compile(r'.*/owner/draft/\d+/publish$'), drop_first)
        p.dblclick('#j-publish')
        p.wait_for_selector('[data-act="pub-again"]', timeout=60000)
        notes['lost_answer'] = p.inner_text('#nlj-pv .nlj-status--bad')
        shot(p, V, 'ba-08-answer-lost-%s' % tag)
        p.click('[data-act="pub-again"]')
        p.wait_for_selector('.nlj-okmark', timeout=60000)
        p.unroute(re.compile(r'.*/owner/draft/\d+/publish$'))
        props = [x for x in state(V)['properties'] if x['post_status'] == 'publish']
        notes['published_rows'] = len(props)
        shot(p, V, 'ba-09-published-%s' % tag)
        c.close()
        ok = notes['existing_email']['input_kept'] and notes['after_reload']['text_kept'] and notes['after_retry']['failed'] == 0 and notes['after_retry']['tiles'] == 3 and notes['published_rows'] == 1 and notes['two_tabs_result'] == {'rooms': '4', 'size': '120'} and notes['conflict_lists_rooms']
        record({'id': 'BA', 'variant': V, 'label': 'real-wp+chrome', 'title': 'after: the same scenarios (%s)' % tag, 'status': 'pass' if ok else 'fail', 'evidence': notes})


if __name__ == '__main__':
    which = sys.argv[1:] or ['before', 'after']
    br = Browser()
    try:
        if 'before' in which:
            clear('BA', 'before')
            before(br)
        if 'after' in which:
            clear('BA', 'after')
            after(br)
    finally:
        br.close()
