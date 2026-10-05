"""debug (theme bench): where does the details screen's "My listings" button go when it is focused after the error summary"""
import json
from bench import Browser, reset, page_url, user
br = Browser()
try:
    reset('theme')
    ctx = br.ctx('390', 'he'); page = ctx.new_page()
    page.goto(page_url('theme', 'he')); page.wait_for_selector('#nlj-signup')
    page.click('[data-act="tab-login"] >> nth=-1'); page.fill('#j-mail2', user('dana')['email']); page.fill('#j-pw2', user('dana')['password'])
    with page.expect_navigation(): page.click('#j-login-go')
    page.wait_for_selector('#nlj-details'); page.click('#j-to-photos'); page.wait_for_selector('#nlj-errsum'); page.wait_for_timeout(800)
    out = page.evaluate('''async () => {
      const settle = async () => { let last=-1,same=0; for (let i=0;i<90&&same<4;i++){ await new Promise(r=>requestAnimationFrame(r)); const y=scrollY; same=(y===last)?same+1:0; last=y; } };
      const res = [];
      const hdr = document.querySelector('.nlhp-top');
      for (const sel of ['[data-act="go-mine"]']) {
        const all = Array.from(document.querySelectorAll('#nlj-app ' + sel));
        for (const e of all) {
          const before = {y: scrollY, r: e.getBoundingClientRect().toJSON()};
          e.focus({preventScroll:false}); await settle();
          res.push({sel, n: all.length, visible: e.offsetParent !== null, active: document.activeElement === e, before, after: {y: scrollY, r: e.getBoundingClientRect().toJSON()}, hdr: hdr ? hdr.getBoundingClientRect().toJSON() : null, hdrPos: hdr ? getComputedStyle(hdr).position : null, spt: getComputedStyle(document.documentElement).scrollPaddingTop, html: e.outerHTML.slice(0, 200), parent: e.parentElement.className, cs: getComputedStyle(e).position});
        }
      }
      return res;
    }''')
    print(json.dumps(out, ensure_ascii=False, indent=1))
    page.screenshot(path=r'C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\638c26e3-6032-438a-9641-ab6fd06c26f5\scratchpad\gomine.png')
finally:
    br.close()
