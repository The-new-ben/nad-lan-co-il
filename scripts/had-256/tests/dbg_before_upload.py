"""Debug: the 1.0 tool's photo upload on the BEFORE bench."""
from bench import Browser, reset, page_url
from before_after import wp_login
from screens import fixtures, FIX

V = 'before'
reset(V)
fixtures()
br = Browser()
c = br.ctx('390', 'he')
p = c.new_page()
p.on('response', lambda r: print('RESP', r.status, r.url[-60:]) if '/owner/' in r.url else None)
p.on('console', lambda m: print('CONSOLE', m.text))
p.on('pageerror', lambda e: print('PAGEERROR', e))
wp_login(p, V, 'dana')
p.wait_for_selector('#nlow-f')
p.set_input_files('#nlow-files', [str(FIX / 'living.jpg'), str(FIX / 'broken.jpg')])
p.wait_for_timeout(8000)
print('texturized' if '&#038;&#038;' in p.content() else 'clean', p.url)
print(p.evaluate('() => Array.from(document.querySelectorAll("#nlow-thumbs li")).map(l => l.getAttribute("data-s"))'))
br.close()
