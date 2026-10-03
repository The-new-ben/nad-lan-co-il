"""Debug helper: prints the browser console and the app's first markup for a URL on the bench."""
import sys
from bench import *

url = sys.argv[1] if len(sys.argv) > 1 else page_url('after')
br = Browser()
c = br.ctx('390', 'he')
p = c.new_page()
p.on('console', lambda m: print('CONSOLE', m.type, m.text))
p.on('pageerror', lambda e: print('PAGEERROR', e))
p.goto(url)
p.wait_for_timeout(2500)
print(p.evaluate('() => (document.getElementById("nlj-app")||{innerHTML:"(no app)"}).innerHTML.slice(0,800)'))
br.close()
