// HAD-712 1.72.664: on the LIVE Kikar pages (no interception) the video buttons lead to a room, not to the booking band (#nlsch).
// No room is opened (a room mails the owner): the buttons' targets and the availability answer are read only.
import { browser } from './waymarks_test.mjs';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (const [L, url] of [['he', 'https://nad-lan.co.il/projects/hamedina/'], ['en', 'https://nad-lan.co.il/projects/hamedina-en/']]) for (const w of [390, 1440]) {
  const b = await browser({ w, h: w < 900 ? 844 : 900, L });
  await b.go(url + '#dira=B20-270'); await b.until("!!document.querySelector('.nlsr-go')", 30000); await sleep(3000);
  const card = await b.ev("JSON.stringify([...document.querySelectorAll('.nlsr a[data-ev=\"call\"], .nlsr .nlsr-call')].map((a) => ({ t: a.innerText.trim().slice(0, 40), href: a.getAttribute('href'), cls: a.className })))");
  await b.ev("document.querySelector('.nlsr-go').click(); true"); await sleep(3500);
  const ck = await b.ev("JSON.stringify([...document.querySelectorAll('.nlck a.nlck-call, .nlck [data-ev=\"call\"]')].map((a) => ({ t: a.innerText.trim().slice(0, 40), href: a.getAttribute('href') })))");
  console.log(L, w, 'showroom', card, '| cockpit', ck, '| errs', b.errs.length, 'failed', b.failed.length);
  await b.shot(`${L}-${w}-cockpit-call`); await b.close();
}
