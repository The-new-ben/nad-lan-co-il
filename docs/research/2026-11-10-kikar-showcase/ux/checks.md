# Buyer gaze checks: measurable browser tests

Companion to rules.md (same folder). Each check names the rule it comes from, how to measure it, a pass
threshold, and where the threshold comes from:

- **Standard**: a published standard or platform guideline (WCAG, Apple, Material, Core Web Vitals).
- **Study**: a number taken directly from a cited study.
- **Derived**: our translation of a rule into a number. Derived thresholds are starting points; tighten or
  loosen them after R36 experiments.

Run every check at two sizes: phone 375 x 812 (DevTools device mode, touch on, mobile user agent) and
desktop 1440 x 900. Run the phone pass in Hebrew and in one left-to-right language at least; release
candidates get all five languages. Audit three states on the phone: peek, half and full (full scrolled
to each section once).

The automated script at the end covers the checks marked "auto". It is read-only and was smoke-tested on
he.wikipedia.org (desktop and mobile sites, right-to-left) on 10.11.2026 without errors.

## Check table

| ID | What to measure | Pass threshold | Threshold source | Rule | Mode |
|---|---|---|---|---|---|
| K0 | Page has a mobile viewport (layout width equals screen width on a phone) | innerWidth = screen width | Standard (otherwise every px size shrinks) | R14 | auto |
| K1 | Share of the visible panel area that is the apartment's own visual (plan, view, interior, tower) | 0.30 to 0.60 in the half state and the first desktop screen | Derived from R1 and R2 | R1, R2 | auto |
| K2 | First-screen essentials visible without scrolling: identity line (floor, rooms, m2, orientation), all-in price, one primary action | all three, at 375 x 812 half state and 1440 x 900 | Derived from NN/g 2018 (57% of viewing time above the fold) | R2 | manual |
| K3 | Words of text visually above the first visual in the panel | at most 20 | Derived (an identity line plus price is 12 to 18 words) | R1, R3 | auto |
| K4 | Section headings that carry a figure or verdict | at least 50% with a number automatically, at least 80% including verdict words on review | Derived from NN/g layer-cake pattern | R4 | auto + manual |
| K5a | Interactive targets smaller than 24 x 24 CSS px (inline text links exempt) | 0 | Standard: WCAG 2.2 SC 2.5.8 | R14 | auto |
| K5b | Targets smaller than 44 x 44 CSS px | at most 10% of targets on screen, none of them primary actions | Standard: Apple 44 pt, WCAG 2.5.5; 10% allowance derived | R14 | auto |
| K5c | Targets centred within 64 px of a screen corner that are smaller than 48 x 48 | 0 | Study: Hoober corner accuracy about 12 mm; Standard: Material 48 dp | R12, R14 | auto |
| K6 | Small targets (under 24 px) with another target's centre closer than 24 px | 0 | Standard: WCAG 2.5.8 spacing | R15 | auto |
| K7 | Primary actions (marked data-cta) whose centre lies outside 35% to 98% of screen height or 8% to 92% of width, on phones | 0 | Derived from Hoober 2017 and NN/g 2023 (middle is easiest) | R12, R13 | auto |
| K8a | Interactive elements fully visible in one screen of the panel | at most 8 | Derived from Hick-Hyman, Cowan (about 4 chunks) and NN/g (up to 4 visible links) | R17 | auto |
| K8b | Primary-styled actions visible at once | 1 or 2 | Derived | R19 | auto |
| K9 | Horizontal tab lists hiding core apartment content | 0 | Study: Baymard, 27% overlooked tabbed content versus 8% vertical | R9 | auto |
| K10 | Core sections (plan, view, price, monthly cost, area, shops, video call, 360) reachable only through a hamburger, kebab or "more" menu | 0 | Study: NN/g 2016, hidden navigation cut discoverability by over 20% | R10 | auto flags, manual decides |
| K11 | Sheet behaviour: Back closes the full state; a visible close button at least 44 px; swipe-down closes; Escape closes on desktop; full state has its own URL; never two layers stacked | all six | Expert: NN/g 2023 bottom sheets | R7, R11 | manual |
| K12 | A vertical swipe that starts on an embedded 3D, 360 or map view scrolls the panel instead of rotating the view (until the user enters explore mode) | yes on iOS Safari and Android Chrome | Platform practice (Google Maps cooperative gestures) | R16 | manual (check computed touch-action: pan-y on the embed) |
| K13 | Largest Contentful Paint | at most 2.5 s at the 75th percentile of real phone visits; lab run with Lighthouse mobile as an early warning | Standard: Core Web Vitals | R29 | auto (lab) + field data |
| K14 | 3D and 360 assets (.glb, .gltf, .ktx2, .drc, .splat, .ply, .hdr, .exr, .usdz) requested before LCP | 0 | Derived from R27 and R29 | R27, R29 | auto |
| K15 | Interaction to Next Paint for tapping an apartment and opening the cockpit; first visible feedback | INP at most 200 ms; feedback at most 100 ms (check in the Performance panel with 4x CPU slowdown) | Standard: Core Web Vitals; Study: 0.1 s limit (Miller 1968, Card 1991) | R30 | auto + manual |
| K16 | Cumulative Layout Shift including opening the panel and loading the price | at most 0.1 | Standard: Core Web Vitals | R31 | auto |
| K17 | Loading feedback: any wait over 1 s shows progress; anything near 10 s shows percent or steps | yes | Study: response-time limits; skeleton evidence mixed | R32 | manual (throttle to Slow 4G) |
| K18 | All-in price: total including VAT on peek and first view; one-time costs and monthly cost in the same section; rate, term and date shown | all present | Standard: Israeli Consumer Protection Law 17A-17B; Study: StubHub field experiment | R21, R23 | manual |
| K19 | Urgency or social-proof wording (5 languages) not wrapped in an element with data-source and data-asof; ticking countdown clocks | 0 and 0 | Law: Israeli CPL sections 2, 3, 7; EU UCPD Annex I point 7 | R24 | auto |
| K20 | Struck-through prices and "was" prices | each tied to a dated price record | Law: Israeli CPL section 2(a) on past prices | R22 | auto flags, manual verifies |
| K21 | Renders, virtual staging, AI images and simulated views carry a visible label inside the image | 100% | Law inference: Israeli CPL sections 2 and 7 | R25 | manual |
| K22 | Floor plan reachable within one tap of the first view; pinch-zoom works; room dimensions and north arrow present | all | Survey and vendor data (weak) | R26 | manual |
| K23 | Number runs with symbols (₪, %, ranges, phone numbers, dates) inside right-to-left text without isolation (bdi, dir="ltr" or "auto", unicode-bidi isolate) | 0 | Standard: Unicode UAX 9, W3C bidi guidance | R33 | auto |
| K24 | Pseudo-localisation: labels expanded by 100% (short) and 30% (long) | no clipped, overlapping or truncated text at 375 px in any of the 5 languages | Standard: W3C text size in translation | R34 | manual |
| K25 | html lang and dir match the language; direction-bearing icons mirrored in Hebrew and Arabic; plan, compass, 3D orientation, clocks and media controls not mirrored | all | Standard: Material and Apple bidirectionality | R35 | auto (lang/dir) + manual |
| K26 | Fixed or sticky bottom bars | height at most 11% of viewport (about 88 px on 812) incl. safe area; appears only after the in-flow action leaves the screen; never covers a focused input | Derived from NN/g sticky-header guidance | R19 | auto (height) + manual |
| K27 | Ad-like treatment of facts or actions: animated promos, boxed offer strips, rotating banners | 0 | Study: NN/g banner blindness (1997, 2007, 2018) | R6 | manual |
| K28a | Form inputs with font size under 16 px; numeric fields without inputmode | 0 and 0 | Platform fact: iOS Safari zooms into inputs under 16 px | R5, R20 | auto |
| K28b | Share of running-text characters at 16 px or more on phones | at least 0.80 | Derived from platform body sizes (Apple 17 pt, Material 16 sp) | R5 | auto |
| K29 | Gallery: count indicator ("3 / 12") on phones, visible thumbnails on desktop; swipe direction follows dir | all | Study: Baymard (24% of mobile sites show thumbnails; dots hard to tap) | R28 | manual |
| K30 | "Similar apartments" comparison size | 2 or 3 items | Derived from choice-overload moderators (Chernev 2015) | R18 | manual |
| K31 | Calculator defaults: each default visible, editable, matches the current Bank of Israel rule and is date-stamped | all | Study: default effect d = 0.68 (Jachimowicz 2019) | R20 | manual |
| K32 | Every shipped cockpit change has a declared metric, a test or before/after window, and results split by device and language | yes | Method: Kohavi 2009 and 2020 | R36 | process |

## How to run the manual checks quickly

1. **K2, K11, K18, K22 (5 minutes):** open the tower on a phone-size viewport, tap one apartment, take a
   screenshot of peek, half and full. Mark on the screenshot: identity line, all-in price, primary action,
   plan entry point. Press the browser Back button from the full state and confirm the sheet closes and the
   tower is unchanged.
2. **K12 (2 minutes):** in the full state, start a vertical swipe on the embedded 360 or view preview.
   The panel must scroll. Then tap "Explore" and confirm the view rotates and a visible exit exists.
3. **K15 (3 minutes):** DevTools Performance panel, 4x CPU slowdown, record, tap an apartment, stop.
   The interaction row must be under 200 ms and the first frame showing a highlight or sheet movement
   under 100 ms after the pointer event.
4. **K17 (2 minutes):** Network throttling "Slow 4G", open the 360. Progress must appear within 1 s.
5. **K19, K21, K27 (5 minutes):** read every badge and label in the panel in Hebrew, then in Russian
   and Arabic. Any urgency line without a live source is a fail even if it is true today.
6. **K24 (10 minutes):** run the page with a pseudo-locale that doubles short strings (for example
   repeat each label once) at 375 px; look for clipping, overflow and two-line buttons that push the
   price below the first screen.
7. **K25 (3 minutes):** switch Hebrew to English: the panel moves sides on desktop (R8), arrows flip,
   the plan and the 3D tower do not.

## How to report results

For every audited page and state write one line per check: ID, value, PASS / FAIL / MANUAL, and a one-line
note. Group failures by rule priority (the order in the skill draft). For each failure give the fix in
plain words and the rule ID. State what was not tested (devices, languages, states) and which thresholds
are derived rather than standard.

## Automated audit script (paste into the DevTools console)

Optional setup before pasting: `window.BGU = { panel: '#apartment-cockpit', cta: '[data-cta]' }`. Mark
the cockpit's primary actions with `data-cta` and every sourced urgency line with `data-source` and
`data-asof` so K7, K8b and K19 are exact. Tap an apartment before running so K15 has an interaction.
Scroll the panel and run again for each screen. The script prints a table and returns the rows.

Known limits: hit areas enlarged with pseudo-elements or padding on a parent are not seen (K5 may
over-report); K1 counts anything that is an image, canvas or video, so point `panel` at the cockpit, not
the whole page; K13 and K16 are lab values for this load only; LCP is not available in Safari.

```js
/* buyer-gaze-ux audit v0.1 (10.11.2026). Read-only: it measures, it changes nothing.
   Use: open the page, set the viewport (375x812 phone or 1440x900 desktop), open the cockpit,
   optionally set window.BGU = { panel: '#cockpit', cta: '[data-cta]' }, paste this, press Enter.
   Re-run after scrolling the panel to audit the next screen. */
(async () => {
  const cfg = Object.assign({
    panel: 'body',
    cta: '[data-cta], [data-primary], .btn-primary, .button--primary',
    visual: 'img, picture, video, canvas, [data-visual]',
  }, window.BGU || {});
  const vw = innerWidth, vh = innerHeight, phone = Math.min(screen.width, vw) < 768;
  const root = document.querySelector(cfg.panel) || document.body;
  const R = el => el.getBoundingClientRect();
  const shown = el => {
    if (!el || !el.isConnected) return false;
    const r = R(el), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05;
  };
  const onScreen = r => r.bottom > 0 && r.right > 0 && r.top < vh && r.left < vw;
  const fully = r => r.top >= 0 && r.left >= 0 && r.bottom <= vh && r.right <= vw;
  const label = el => (el.getAttribute('aria-label') || el.textContent || el.getAttribute('alt') || el.tagName).trim().replace(/\s+/g, ' ').slice(0, 40);
  const res = [];
  const add = (id, rule, value, pass, note) => res.push({ id, rule, value: typeof value === 'object' ? JSON.stringify(value).slice(0, 160) : value, pass: pass === null ? 'manual' : (pass ? 'PASS' : 'FAIL'), note: note || '' });
  const html = document.documentElement;
  const dir = html.getAttribute('dir') || getComputedStyle(html).direction;
  const scaled = phone && vw > screen.width + 1;
  add('K0', 'setup', `${vw}x${vh} ${phone ? 'phone' : 'desktop'}`, scaled ? false : null,
    (scaled ? 'NO mobile viewport meta: layout is ' + vw + ' px wide on a ' + screen.width + ' px screen, all sizes shrink; ' : '') +
    (document.querySelector(cfg.panel) ? 'panel: ' + cfg.panel : 'panel selector not found, auditing <body>; set window.BGU.panel'));

  // K1 share of the visible panel area that is the apartment's own visual (grid sample, occlusion aware)
  const pr = R(root);
  const box = { l: Math.max(0, pr.left), t: Math.max(0, pr.top), r: Math.min(vw, pr.right), b: Math.min(vh, pr.bottom) };
  let cells = 0, vis = 0;
  for (let y = box.t + 4; y < box.b; y += 8) for (let x = box.l + 4; x < box.r; x += 8) {
    const el = document.elementFromPoint(x, y);
    if (!el || !(root === document.body || root.contains(el))) continue;
    cells++; if (el.closest(cfg.visual)) vis++;
  }
  const share = cells ? vis / cells : 0;
  add('K1', 'R1,R2', share.toFixed(2), share >= 0.30 && share <= 0.60, 'visual share of visible panel; target 0.30-0.60');

  // K3 words of text visually above the first on-screen visual
  const visuals = [...root.querySelectorAll(cfg.visual)].filter(shown).filter(e => onScreen(R(e)) && R(e).width * R(e).height > 4000);
  const firstTop = visuals.length ? Math.min(...visuals.map(e => R(e).top)) : null;
  if (firstTop === null) add('K3', 'R1,R3', 'no visual on screen', false, 'first screen has no apartment visual');
  else {
    let words = 0; const rg = document.createRange();
    const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    for (let n; (n = tw.nextNode());) {
      const t = n.textContent.trim(); if (!t || !shown(n.parentElement)) continue;
      rg.selectNodeContents(n); const r = rg.getBoundingClientRect();
      if (r.height && r.bottom > 0 && r.bottom <= firstTop + 1) words += t.split(/\s+/).length;
    }
    add('K3', 'R1,R3', words, words <= 20, 'words above first visual; target <= 20');
  }

  // K4 section headings that carry a figure (layer-cake readers read only these)
  const heads = [...root.querySelectorAll('h2, h3, h4, summary, [role=heading]')].filter(shown);
  const withNum = heads.filter(h => /\d/.test(h.textContent || '')).length;
  add('K4', 'R4', `${withNum}/${heads.length}`, heads.length === 0 ? null : withNum / heads.length >= 0.5,
    'headings containing a number; target >= 50% automatically, then judge the rest by hand (a verdict word also counts)');

  // K20 struck-through prices need a documented past price
  const struck = [...root.querySelectorAll('s, del, strike, *')].filter(e => e.children.length === 0 && shown(e) && /\d/.test(e.textContent || '') &&
    (/line-through/.test(getComputedStyle(e).textDecorationLine) || /^(S|DEL|STRIKE)$/.test(e.tagName)));
  add('K20', 'R22', struck.length, struck.length === 0 ? true : null, struck.length ? 'struck-through numbers to verify against a dated price record: ' + struck.slice(0, 3).map(label).join(' | ') : '');

  // K5, K6, K7, K8 targets
  const SEL = 'a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [role=link], [role=tab], [role=checkbox], [role=radio], [role=switch], [role=slider], [role=menuitem], [tabindex]:not([tabindex="-1"])';
  const inlineLink = e => e.tagName === 'A' && getComputedStyle(e).display === 'inline' &&
    ((e.parentElement && e.parentElement.textContent) || '').trim().length > (e.textContent || '').trim().length + 15;
  const targets = [...root.querySelectorAll(SEL)].filter(shown).filter(e => !e.disabled && !inlineLink(e)).filter(e => onScreen(R(e)));
  const u24 = [], u44 = [], corner = [];
  targets.forEach(e => {
    const r = R(e);
    if (r.width < 24 || r.height < 24) u24.push(label(e)); else if (r.width < 44 || r.height < 44) u44.push(label(e));
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2, c = 64;
    if ((cx < c || cx > vw - c) && (cy < c || cy > vh - c) && (r.width < 48 || r.height < 48)) corner.push(label(e));
  });
  add('K5a', 'R14', u24.length, u24.length === 0, 'targets under 24x24: ' + u24.slice(0, 5).join(' | '));
  add('K5b', 'R14', `${u44.length}/${targets.length}`, targets.length === 0 || u44.length / targets.length <= 0.10, 'targets under 44x44 (target <= 10%): ' + u44.slice(0, 5).join(' | '));
  add('K5c', 'R12,R14', corner.length, corner.length === 0, 'corner targets under 48x48: ' + corner.slice(0, 5).join(' | '));
  let crowd = 0;
  const cs = targets.map(e => { const r = R(e); return { x: r.left + r.width / 2, y: r.top + r.height / 2, small: r.width < 24 || r.height < 24 }; });
  cs.forEach((a, i) => { if (!a.small) return; cs.forEach((b, j) => { if (i !== j && Math.hypot(a.x - b.x, a.y - b.y) < 24) crowd++; }); });
  add('K6', 'R15', crowd, crowd === 0, 'small targets with another target centre closer than 24 px');
  const ctas = [...root.querySelectorAll(cfg.cta)].filter(shown).filter(e => onScreen(R(e)));
  const outBand = ctas.filter(e => { const r = R(e), cy = (r.top + r.bottom) / 2, cx = (r.left + r.right) / 2;
    return phone && (cy < 0.35 * vh || cy > 0.98 * vh || cx < 0.08 * vw || cx > 0.92 * vw); }).map(label);
  add('K7', 'R12,R13', phone ? `${outBand.length}/${ctas.length}` : 'desktop: n/a', phone ? (ctas.length > 0 && outBand.length === 0) : null,
    ctas.length ? 'primary actions outside the 35-98% height band: ' + outBand.join(' | ') : 'no element matched cfg.cta; mark primary actions with data-cta');
  const full = targets.filter(e => fully(R(e)));
  add('K8a', 'R17', full.length, full.length <= 8, 'interactive elements fully visible in this screen; target <= 8');
  add('K8b', 'R19', ctas.length, ctas.length >= 1 && ctas.length <= 2, 'primary-styled actions on screen; target 1-2');

  // K9 horizontal tabs, K10 hidden menus
  const tablists = [...root.querySelectorAll('[role=tablist]')].filter(shown).filter(t => t.getAttribute('aria-orientation') !== 'vertical');
  add('K9', 'R9', tablists.length, tablists.length === 0, 'horizontal tablists (allowed only for non-core content)');
  const menus = [...root.querySelectorAll('button[aria-haspopup], [role=button][aria-haspopup], button[aria-expanded="false"]')].filter(shown)
    .filter(e => /menu|more|עוד|תפריט|ещё|еще|plus|المزيد|القائمة|☰|⋮|…/i.test(label(e) + ' ' + (e.className || '')));
  add('K10', 'R10', menus.length, null, 'menus that may hide core sections: ' + menus.slice(0, 5).map(label).join(' | '));

  // K23 bidi isolation of number runs in RTL text
  if (dir === 'rtl') {
    const bad = []; const tw2 = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const numRun = /(\d[\d.,]*\s*[-–/:%+₪$€]|[-–/:+₪$€]\s*\d|\d+\s*[-–]\s*\d+)/;
    for (let n; (n = tw2.nextNode());) {
      const t = n.textContent; const p = n.parentElement;
      if (!p || !shown(p) || !numRun.test(t) || !/[֐-׿؀-ۿ]/.test(t + (p.textContent || '').slice(0, 80))) continue;
      const dEl = p.closest('[dir]');
      const iso = p.closest('bdi, input, textarea') ||
        (dEl && dEl !== html && dEl !== document.body && /^(ltr|auto)$/i.test(dEl.getAttribute('dir'))) ||
        ['isolate', 'isolate-override', 'plaintext'].includes(getComputedStyle(p).unicodeBidi);
      if (!iso) bad.push(t.trim().slice(0, 30));
    }
    add('K23', 'R33', bad.length, bad.length === 0, 'number runs inside RTL text without isolation: ' + bad.slice(0, 4).join(' | '));
  } else add('K23', 'R33', 'page is ltr', null, 'run again on the Hebrew or Arabic version');

  // K26 sticky or fixed bottom bars
  const bars = [...document.querySelectorAll('body *')].filter(e => { const s = getComputedStyle(e); if (s.position !== 'fixed' && s.position !== 'sticky') return false;
    const r = R(e); return shown(e) && r.bottom >= vh - 2 && r.width >= vw * 0.6 && r.height < vh * 0.5; });
  const tall = bars.filter(e => R(e).height > 0.11 * vh).map(e => `${label(e)} ${Math.round(R(e).height)}px`);
  add('K26', 'R19', bars.length ? `${bars.length} bar(s)` : 'none', tall.length === 0, tall.length ? 'bottom bars taller than 11% of viewport: ' + tall.join(' | ') : 'height ok');

  // K28 input font size and numeric keyboards; running text size on phones
  const inputs = [...root.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([type=radio]), select, textarea')].filter(shown);
  const tinyInputs = inputs.filter(e => parseFloat(getComputedStyle(e).fontSize) < 16).length;
  const numNoMode = inputs.filter(e => e.type === 'text' && /price|amount|rate|years|sum|מחיר|סכום|ריבית|שנים|הון/i.test((e.name || '') + (e.id || '') + (e.placeholder || '')) && !e.getAttribute('inputmode')).length;
  add('K28a', 'R5,R20', `${tinyInputs} small, ${numNoMode} numeric w/o inputmode`, tinyInputs === 0 && numNoMode === 0, 'inputs must be >= 16px (iOS zooms below) and numeric fields need inputmode');
  if (phone) {
    let all = 0, big = 0;
    root.querySelectorAll('p, li, dd, td').forEach(e => { if (!shown(e)) return; const n = (e.textContent || '').trim().length; all += n; if (parseFloat(getComputedStyle(e).fontSize) >= 16) big += n; });
    add('K28b', 'R5', all ? (big / all).toFixed(2) : 'no running text', all === 0 || big / all >= 0.8, 'share of running-text characters at >= 16px; target >= 0.80');
  }

  // K19 urgency and social-proof wording without a data source
  const urg = /(נותר(ו)? רק|רק עוד \d|דירה אחרונה|אחרונות|צופים (כעת|עכשיו)|מבצע מסתיים|עד חצות|only \d+ left|\d+ (people|others) (are )?(viewing|looking)|ends in|last chance|selling fast|hurry|plus que \d+|dernière chance|se termine|осталось (всего |только )?\d+|сейчас смотрят|последний шанс|متبق(ي|ية) فقط|آخر فرصة|يشاهد(ون)? الآن)/i;
  const urgHits = [...root.querySelectorAll('*')].filter(e => e.children.length === 0 && shown(e) && urg.test(e.textContent || ''))
    .filter(e => !e.closest('[data-source][data-asof]')).map(e => (e.textContent || '').trim().slice(0, 40));
  const clock = /\b\d{1,2}:\d{2}:\d{2}\b/;
  const clockEls = [...root.querySelectorAll('*')].filter(e => e.children.length === 0 && shown(e) && clock.test(e.textContent || ''));
  const before = clockEls.map(e => e.textContent);
  await new Promise(r => setTimeout(r, 1200));
  const ticking = clockEls.filter((e, i) => e.textContent !== before[i]).length;
  add('K19', 'R24', `${urgHits.length} unsourced, ${ticking} ticking`, urgHits.length === 0 && ticking === 0, urgHits.slice(0, 3).join(' | '));

  // K13, K14, K15, K16 performance from buffered entries
  const observe = (type, extra) => new Promise(resolve => {
    const list = [];
    try { const po = new PerformanceObserver(l => list.push(...l.getEntries())); po.observe(Object.assign({ type, buffered: true }, extra || {}));
      setTimeout(() => { po.disconnect(); resolve(list); }, 300); } catch (e) { resolve(null); }
  });
  const [lcpE, clsE, evE] = await Promise.all([observe('largest-contentful-paint'), observe('layout-shift'), observe('event', { durationThreshold: 16 })]);
  const lcp = lcpE && lcpE.length ? lcpE[lcpE.length - 1].startTime : null;
  add('K13', 'R29', lcp === null ? 'n/a' : Math.round(lcp) + ' ms', lcp === null ? null : lcp <= 2500, 'lab LCP of this load; field p75 must also be <= 2500 ms');
  const heavy = performance.getEntriesByType('resource').filter(r => /\.(glb|gltf|usdz|ktx2|drc|splat|ply|hdr|exr)(\?|#|$)/i.test(r.name));
  const early = lcp === null ? [] : heavy.filter(r => r.startTime < lcp);
  add('K14', 'R27,R29', `${early.length} before LCP, ${heavy.length} total`, lcp === null ? null : early.length === 0,
    early.slice(0, 3).map(r => r.name.split('/').pop().slice(0, 40) + ' ' + Math.round((r.transferSize || 0) / 1024) + 'KB').join(' | '));
  const inter = (evE || []).filter(e => e.interactionId);
  const inp = inter.length ? Math.max(...inter.map(e => e.duration)) : null;
  add('K15', 'R30', inp === null ? 'no interaction yet' : Math.round(inp) + ' ms', inp === null ? null : inp <= 200, 'tap an apartment first, then run; worst interaction approximates INP');
  const cls = (clsE || []).filter(e => !e.hadRecentInput).reduce((s, e) => s + e.value, 0);
  add('K16', 'R31', cls.toFixed(3), cls <= 0.1, 'sum of unexpected shifts so far (upper bound of CLS)');

  add('K25', 'R35', `dir=${dir} lang=${html.lang || '(none)'}`, !!html.lang && (dir === 'rtl') === /^(he|ar|iw|fa|ur)/i.test(html.lang || ''), 'html dir must match the language');

  console.table(res);
  return res;
})();
```
