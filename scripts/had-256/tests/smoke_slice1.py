"""First slice on real WordPress (Playground): open an account, fill details, the draft saves to the account, a reload resumes it."""
import sys
from bench import *

V = 'after'
reset(V)
br = Browser()
c = br.ctx('390', 'he')
p = c.new_page()
errors = []
p.on('pageerror', lambda e: errors.append(str(e)))
p.goto(page_url(V))
p.wait_for_selector('#nlj-signup')
ev = [shot(p, V, 'slice1-01-auth-390-he')]

# open an account with a fresh synthetic address
p.fill('#j-name', 'נועה')
p.fill('#j-mail', 'noa.sample@example.test')
p.fill('#j-pw', 'Sample-Noa-2026!')
with p.expect_navigation():
    p.click('#j-signup-go')
p.wait_for_selector('#nlj-details')
ev.append(shot(p, V, 'slice1-02-details-new-390-he'))

# type: the status goes device -> account; then the server holds it
p.click('[data-deal="sale"]')
p.select_option('#j-type', 'apartment')
p.fill('#j-city', 'תל אביב יפו')
p.fill('#j-hood', 'שכונת הדוגמה')
p.fill('#j-rooms', '4')
wait_status(p, 'נשמר בחשבון')
ev.append(shot(p, V, 'slice1-03-saved-in-account-390-he'))
draft = p.evaluate('() => new URLSearchParams(location.search).get("draft")')

# reload without the draft address: the saved draft is offered; continue restores the fields
p.goto(page_url(V))
p.wait_for_selector('[data-act="home-continue"]')
ev.append(shot(p, V, 'slice1-04-saved-draft-390-he'))
p.click('[data-act="home-continue"]')
p.wait_for_selector('#nlj-details')
vals = p.evaluate('() => ({city: document.getElementById("j-city").value, hood: document.getElementById("j-hood").value, rooms: document.getElementById("j-rooms").value, deal: document.querySelector("[data-deal=sale]").getAttribute("aria-pressed")})')
ok_resume = vals == {'city': 'תל אביב יפו', 'hood': 'שכונת הדוגמה', 'rooms': '4', 'deal': 'true'}
ev.append(shot(p, V, 'slice1-05-resumed-390-he'))
c.close()

# the email that already has an account: the error keeps the input and offers sign-in
c2 = br.ctx('390', 'he')
p2 = c2.new_page()
p2.goto(page_url(V))
p2.fill('#j-name', 'דנה')
p2.fill('#j-mail', user('dana')['email'])
p2.fill('#j-pw', 'Another-pass-1')
p2.click('#j-signup-go')
p2.wait_for_selector('#j-mail-err')
kept = p2.input_value('#j-mail') == user('dana')['email'] and p2.input_value('#j-name') == 'דנה'
ev.append(shot(p2, V, 'slice1-06-existing-email-390-he'))
p2.click('[data-act="exists-login"]')
mail_carried = p2.input_value('#j-mail2') == user('dana')['email']
p2.fill('#j-pw2', 'wrong-password-1')
p2.click('#j-login-go')
p2.wait_for_selector('#j-form-err')
generic = p2.inner_text('#j-form-err')
ev.append(shot(p2, V, 'slice1-07-wrong-password-390-he'))
c2.close()
br.close()

print('draft', draft, 'resume', ok_resume, vals, 'kept', kept, 'carried', mail_carried, 'generic', generic, 'js errors', errors)
record({'id': 'L01', 'variant': V, 'label': 'real-wp+chrome', 'title': 'open an account; an existing email keeps the input and offers sign-in; a wrong password gets one neutral message', 'status': 'pass' if kept and mail_carried and 'אינם נכונים' in generic and not errors else 'fail',
        'evidence': {'existing_email_input_kept': kept, 'email_carried_to_sign_in': mail_carried, 'wrong_password_message': generic, 'js_errors': errors}})
record({'id': 'L04', 'variant': V, 'label': 'real-wp+chrome', 'title': 'a new account types details: saved to the account; a reload offers the saved draft and restores it', 'status': 'pass' if ok_resume else 'fail', 'evidence': {'restored': vals, 'draft': draft}})
sys.exit(0 if ok_resume and kept and mail_carried and not errors else 1)
