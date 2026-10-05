"""Debug: where the floating bar sits on the journey page (390x844), and its classes, before and after a focus."""
import os
from bench import Browser, page_url

br = Browser()
c = br.ctx('390', 'he')
p = c.new_page()
p.goto(page_url('after'))
p.wait_for_selector('#nlj-signup')
p.wait_for_timeout(1500)
q = '() => { const b = document.getElementById("nlcta"); const r = b.getBoundingClientRect(); return {cls: b.className, top: r.top, bottom: r.bottom, left: r.left, right: r.right, ih: innerHeight, lift: b.style.getPropertyValue("--nlcta-lift"), rest: b.getAttribute("data-rest")}; }'
print('load', p.evaluate(q))
p.focus('#j-name')
p.wait_for_timeout(300)
print('focus name', p.evaluate(q), p.evaluate('() => document.getElementById("j-name").getBoundingClientRect().toJSON()'))
p.evaluate('() => document.activeElement.blur()')
p.wait_for_timeout(900)
print('blur', p.evaluate(q))
br.close()
