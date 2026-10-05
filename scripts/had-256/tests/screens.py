"""Drives the journey through every screen on the AFTER bench (real Chrome, real WordPress) and calls back on each.

visit(br, lang, vp, on_screen) resets the site, then walks: signup, signup with an existing email, sign in, recovery
sent, details empty, details with errors, details filled, photos (two uploaded + one refused), preview, published,
My listings, the saved-draft screen, promotion. on_screen(page, name) runs on each.
"""
import io
import pathlib

from PIL import Image

from bench import reset, page_url, user, REPO
from session import jpeg_bytes

FIX = REPO / 'scripts' / 'had-256' / 'local' / '.runtime' / 'fixtures'


def fixtures():
    FIX.mkdir(parents=True, exist_ok=True)
    (FIX / 'living.jpg').write_bytes(jpeg_bytes(w=1600, h=1200, color=(60, 110, 150)))
    (FIX / 'kitchen.jpg').write_bytes(jpeg_bytes(w=1200, h=1600, color=(150, 120, 70)))
    (FIX / 'broken.jpg').write_bytes(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00' + b'\x13\x37' * 300)


def walk(page, lang, on_screen, V='after'):
    he = lang == 'he'
    L = {'he': {'continue': 'המשך', 'saved': 'נשמר בחשבון'}, 'en': {'continue': 'Continue', 'saved': 'Saved in your account'}}[lang]
    page.goto(page_url(V, lang))
    page.wait_for_selector('#nlj-signup')
    on_screen(page, 'auth-signup')
    page.fill('#j-name', 'דנה' if he else 'Dana')
    page.fill('#j-mail', user('dana')['email'])
    page.fill('#j-pw', 'Another-pass-1')
    page.click('#j-signup-go')
    page.wait_for_selector('#j-mail-err')
    on_screen(page, 'auth-existing-email')
    page.click('[data-act="exists-login"]')
    page.wait_for_selector('#nlj-login')
    on_screen(page, 'auth-login')
    page.click('[data-act="tab-recover"]')
    page.wait_for_selector('#nlj-recover')
    page.click('#j-rec-go')
    page.wait_for_selector('#nlj-recover .nlj-status--ok')
    on_screen(page, 'auth-recovery-sent')
    page.click('[data-act="tab-login"] >> nth=-1')
    page.fill('#j-mail2', user('dana')['email'])
    page.fill('#j-pw2', user('dana')['password'])
    with page.expect_navigation():
        page.click('#j-login-go')
    page.wait_for_selector('#nlj-details')
    on_screen(page, 'details-empty')
    page.click('#j-to-photos')
    page.wait_for_selector('#nlj-errsum')
    on_screen(page, 'details-errors')
    page.click('[data-deal="sale"]')
    page.select_option('#j-type', 'apartment')
    vals = {'#j-city': 'תל אביב יפו', '#j-hood': 'שכונת הדוגמה', '#j-rooms': '4', '#j-size': '96', '#j-floor': '3 מתוך 8' if he else '3 of 8', '#j-price': '3450000',
            '#j-desc': 'דירה מוארת בקומה שלישית, שלושה כיווני אוויר, מרפסת שמש של 10 מ״ר לכיוון מערב. חניה בטאבו ומחסן.' if he else 'A bright third-floor apartment with windows on three sides and a 10 m² west-facing balcony. Registered parking and a storage room.',
            '#j-cname': 'דנה' if he else 'Dana', '#j-phone': '050-0000000'}
    for k, v in vals.items():
        page.fill(k, v)
    page.check('#j-phone-ok')
    page.check('#j-owner-ok')
    page.wait_for_function('t => (document.getElementById("nlj-st")||{}).innerText.indexOf(t) > -1', arg=L['saved'], timeout=20000)
    on_screen(page, 'details-filled')
    page.click('#j-to-photos')
    page.wait_for_selector('#j-files', state='attached')
    page.set_input_files('#j-files', [str(FIX / 'living.jpg'), str(FIX / 'kitchen.jpg'), str(FIX / 'broken.jpg')])
    page.wait_for_function('() => !document.querySelector("#j-tiles .nlj-up") && document.querySelectorAll("#j-tiles li").length === 3 && document.querySelector("#j-tiles .is-fail")', timeout=60000)
    page.wait_for_function('t => (document.getElementById("nlj-st")||{}).innerText.indexOf(t) > -1', arg=L['saved'], timeout=20000)
    on_screen(page, 'photos')
    page.click('#j-tiles .is-fail [data-act="ph-rm"]')
    page.click('#j-to-preview')
    page.wait_for_selector('.nlj-lcard', timeout=30000)
    page.wait_for_function('() => { const i = document.querySelector(".nlj-lcard img"); return !i || i.complete; }', timeout=15000)
    on_screen(page, 'preview')
    page.click('#j-publish')
    page.wait_for_selector('.nlj-okmark', timeout=60000)
    on_screen(page, 'published')
    page.click('[data-act="go-mine"] >> nth=-1')
    page.wait_for_selector('.nlj-mine, .nlj-note', timeout=20000)
    page.wait_for_selector('[data-act="mine-new"]')
    page.click('[data-act="mine-new"]')
    page.wait_for_selector('#nlj-details')
    page.click('[data-deal="rent"]')
    page.fill('#j-city', 'תל אביב יפו')
    page.fill('#j-rooms', '2')
    page.wait_for_function('t => (document.getElementById("nlj-st")||{}).innerText.indexOf(t) > -1', arg=L['saved'], timeout=20000)
    page.click('[data-act="go-mine"] >> nth=0')
    page.wait_for_selector('.nlj-mine')
    page.wait_for_timeout(500)
    on_screen(page, 'my-listings')
    page.click('[data-act="go-promote"]')
    page.wait_for_selector('fieldset[disabled]')
    on_screen(page, 'promotion-off')
    page.goto(page_url(V, lang))
    page.wait_for_selector('[data-act="home-continue"]')
    on_screen(page, 'saved-draft')


def visit(br, lang, vp, on_screen, V='after'):
    fixtures()
    reset(V)
    ctx = br.ctx(vp, lang)
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    try:
        walk(page, lang, on_screen, V)
    finally:
        ctx.close()
    return errors
