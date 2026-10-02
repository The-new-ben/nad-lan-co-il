/* The apartment's basket (design system L9Nqz7Viv7K3MYeZrBc9s8 version 86, BasketOne; the journey: BuyJourney v78).
 * What the buyer picked on the project page, in one drawer: the example apartment (the stage's nl:floor / nl:facing), the
 * design style (the 360 viewer's nl:view), a team of real professionals (inc/basket.php, never a sample profile), the full
 * price (purchase tax by the brackets in force), and two ways on: the basket to the representative on WhatsApp and the
 * shared viewing room. Nothing is sold or paid here; the drawer says so. Kept in this browser only, per project. */
(function () {
  'use strict';
  const cfgEl = document.getElementById('nadlan-basket-cfg');
  if (!cfgEl) return;
  let C;
  try { C = JSON.parse(cfgEl.textContent); } catch (e) { return; }
  const KEY = 'nl-basket:' + C.slug;
  const ga = (n, p) => { try { if (window.nadlanGA) window.nadlanGA(n, Object.assign({ project: C.name }, p || {})); } catch (e) { /* none */ } };
  const nf = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  const ils = (n) => nf.format(Math.round(n)) + ' ₪';
  const BUYERS = [
    { id: 'single', label: 'דירה יחידה', brackets: 'single' },
    { id: 'additional', label: 'דירה נוספת', brackets: 'additional' },
    { id: 'foreign', label: 'תושב/ת חוץ', brackets: 'additional', note: 'תושב חוץ אינו זכאי למדרגות של דירה יחידה ומשלם לפי מדרגות דירה נוספת מהשקל הראשון.' },
  ];
  const STYLES = { bare: 'כמו במסירה', warm: 'עץ חם', light: 'בהיר', stone: 'אבן' };

  /* ---------------- the state, in this browser ---------------- */
  let S = { unit: null, style: null, team: {}, price: { amount: '', buyer: 'single', lawyer: '' } };
  try { const s = JSON.parse(localStorage.getItem(KEY) || 'null'); if (s && typeof s === 'object') S = Object.assign(S, s, { price: Object.assign(S.price, s.price || {}) }); } catch (e) { /* private window */ }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* none */ } paint(); };

  const words = (b) => {
    if (b == null) return '';
    const x = ((Number(b) % 360) + 360) % 360;
    for (const s of C.sectors || []) {
      const a = s[0], z = s[1];
      if (a <= z ? (x >= a && x < z) : (x >= a || x < z)) return s[2];
    }
    return '';
  };
  // 1.72.391: a world page's own words for the apartment (its label) come before the sectors' direction words
  const unitLine = (u) => u ? ('קומה ' + u.floor + (u.label ? ' · ' + u.label : (u.bearing != null && words(u.bearing) ? ' · ' + words(u.bearing) : ''))) : '';
  const count = () => (S.unit ? 1 : 0) + (S.style && S.style !== 'bare' ? 1 : 0) + Object.keys(S.team || {}).length;

  /* ---------------- what the page reports ---------------- */
  window.addEventListener('nl:floor', (e) => {
    const f = e.detail && Number(e.detail.floor);
    if (!(f > 0)) return;
    S.unit = { floor: f, bearing: S.unit && S.unit.floor === f ? S.unit.bearing : null };
    save();
  });
  window.addEventListener('nl:facing', (e) => {
    const d = e.detail || {};
    if (!(Number(d.floor) > 0)) return;
    S.unit = { floor: Number(d.floor), bearing: d.bearing != null ? Math.round(Number(d.bearing)) : null, unit: d.unit || null, label: d.label ? String(d.label).slice(0, 60) : null };
    save();
  });
  window.addEventListener('nl:view', (e) => {
    const d = e.detail || {};
    if (d.mode === 'inside' && d.style && STYLES[d.style]) { if (S.style !== d.style) { S.style = d.style; save(); } }
  });

  /* ---------------- the full price ---------------- */
  function tax(amount, buyer) {
    const b = BUYERS.find((x) => x.id === buyer) || BUYERS[0];
    const br = (C.tax && C.tax[b.brackets]) || [];
    let t = 0, prev = 0;
    for (const [ceil, rate] of br) {
      const top = ceil == null ? Infinity : Number(ceil);
      if (amount > prev) t += (Math.min(amount, top) - prev) * Number(rate);
      prev = top;
      if (amount <= top) break;
    }
    return t;
  }
  // the price the buyer enters (from the representative): a published average is shown as a hint, never multiplied into a
  // price (averages are reported before or after VAT, and no apartment is the average)
  function priceOf() {
    const typed = Number(String(S.price.amount || '').replace(/[^\d]/g, ''));
    return { amount: typed > 0 ? typed : 0 };
  }

  /* ---------------- the drawer ---------------- */
  const h = (tag, cls, text, attrs) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
    return n;
  };
  let root = null, body = null, opener = null;
  const proCache = {};

  function build() {
    root = h('div', 'nlbk', null, { role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'nlbk-t', dir: 'rtl', lang: 'he', hidden: '' });
    const scrim = h('div', 'nlbk__scrim');
    scrim.addEventListener('click', close);
    const sheet = h('div', 'nlbk__sheet');
    const head = h('div', 'nlbk__head');
    const tt = h('div', 'nlbk__tt');
    tt.appendChild(h('p', 'nlbk__kick', C.name));
    tt.appendChild(h('h2', 'nlbk__title', 'סל הדירה', { id: 'nlbk-t' }));
    const x = h('button', 'nlbk__x', '×', { type: 'button', 'aria-label': 'סגירת הסל' });
    x.addEventListener('click', close);
    head.append(tt, x);
    body = h('div', 'nlbk__body');
    sheet.append(head, body);
    root.append(scrim, sheet);
    document.body.appendChild(root);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && root && !root.hidden) close(); });
  }

  function steps() {
    const ol = h('ol', 'nlbk__steps', null, { 'aria-label': 'השלבים' });
    const st = [['הבניין', true], ['הדירה', !!S.unit], ['העיצוב', !!S.style], ['הצוות', Object.keys(S.team || {}).length > 0], ['המחיר', priceOf().amount > 0]];
    st.forEach(([t, done], i) => {
      const li = h('li', 'nlbk__step' + (done ? ' is-done' : ''));
      li.appendChild(h('i', null, done ? '✓' : String(i + 1), { 'aria-hidden': 'true' }));
      li.appendChild(document.createTextNode(t));
      if (done) li.appendChild(h('span', 'nlbk__sr', ' (נבחר)'));
      ol.appendChild(li);
    });
    return ol;
  }

  function sec(title, sub) {
    const s = h('section', 'nlbk__sec');
    s.appendChild(h('h3', 'nlbk__h', title));
    if (sub) s.appendChild(h('p', 'nlbk__sub', sub));
    return s;
  }

  function goStage() {
    close();
    const t = document.getElementById('nlps') || document.getElementById('nlps-t');
    if (t) t.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'center' });
  }
  // 1.72.392: a world page (the shared 3D world) offers its own way inside (window.__nlInsideGo: the example apartment's 360)
  const insideOk = () => !!document.querySelector('.nlat__go') || typeof window.__nlInsideGo === 'function';
  function goInside() {
    close();
    const b = document.querySelector('.nlat__go');
    if (b) b.click(); else if (typeof window.__nlInsideGo === 'function') window.__nlInsideGo();
  }

  function renderUnit() {
    const s = sec('הדירה');
    if (S.unit) {
      const row = h('div', 'nlbk__item');
      row.appendChild(h('span', 'nlbk__badge', String(S.unit.floor), { 'aria-hidden': 'true' }));
      const tx = h('div', 'nlbk__itx');
      tx.appendChild(h('b', null, 'דירה לדוגמה · ' + unitLine(S.unit)));
      tx.appendChild(h('span', null, S.unit.bearing != null ? 'הדירות, התוכניות והמחירים מהנציג' : 'עוד לא נבחר כיוון בטבעת הקומה'));
      row.appendChild(tx);
      const ch = h('button', 'nlbk__link', 'להחליף', { type: 'button' });
      ch.addEventListener('click', goStage);
      row.appendChild(ch);
      s.appendChild(row);
    } else {
      s.appendChild(h('p', 'nlbk__empty', 'עוד לא נבחרה קומה.'));
      const b = h('button', 'nlbk__btn nlbk__btn--2', 'לבחירת קומה על הבניין', { type: 'button' });
      b.addEventListener('click', goStage);
      s.appendChild(b);
    }
    return s;
  }

  function renderStyle() {
    const s = sec('העיצוב', 'רעיון עיצוב להמחשה בדירה לדוגמה, לא המפרט של היזם.');
    const has = insideOk();
    // 1.72.392: on a world page "bare" is the original rendered design (furnished), not a design choice
    if (S.style && !(S.style === 'bare' && typeof window.__nlInsideGo === 'function')) {
      const row = h('div', 'nlbk__item');
      row.appendChild(h('span', 'nlbk__sw nlbk__sw--' + S.style, null, { 'aria-hidden': 'true' }));
      const tx = h('div', 'nlbk__itx');
      tx.appendChild(h('b', null, STYLES[S.style] || S.style));
      tx.appendChild(h('span', null, 'נבחר בתוך הדירה ב־360°'));
      row.appendChild(tx);
      if (has) { const ch = h('button', 'nlbk__link', 'להחליף', { type: 'button' }); ch.addEventListener('click', goInside); row.appendChild(ch); }
      s.appendChild(row);
    } else if (has) {
      const b = h('button', 'nlbk__btn nlbk__btn--2', 'להיכנס לדירה ולבחור סגנון', { type: 'button' });
      b.addEventListener('click', goInside);
      s.appendChild(b);
    } else {
      s.appendChild(h('p', 'nlbk__empty', 'הדירה מבפנים עוד לא זמינה בפרויקט הזה.'));
    }
    return s;
  }

  function waLink(text) {
    return C.wa ? 'https://wa.me/' + C.wa + '?text=' + encodeURIComponent(text) : '';
  }

  function renderTeam() {
    const s = sec('הצוות שלכם', 'אנשי מקצוע מהמאגר, עם בדיקת רישיון כשיש. בלי עמלה על הפנייה.');
    const list = h('div', 'nlbk__team');
    for (const t of C.team || []) {
      const slot = h('div', 'nlbk__slot');
      const chosen = S.team && S.team[t.key];
      const top = h('div', 'nlbk__slot-top');
      top.appendChild(h('span', 'nlbk__mono', chosen ? (chosen.name || '').slice(0, 1) : '+', { 'aria-hidden': 'true' }));
      const tx = h('div', 'nlbk__itx');
      tx.appendChild(h('b', null, t.label));
      tx.appendChild(h('span', null, chosen ? chosen.name + (chosen.license ? ' · רישיון ' + chosen.license : '') : 'עוד לא נבחר'));
      top.appendChild(tx);
      if (chosen) {
        const rm = h('button', 'nlbk__link', 'להסיר', { type: 'button', 'aria-label': 'להסיר את ' + chosen.name });
        rm.addEventListener('click', () => { delete S.team[t.key]; save(); ga('basket_team_remove', { profession: t.key }); });
        top.appendChild(rm);
      } else {
        const pick = h('button', 'nlbk__link', 'לבחור', { type: 'button', 'aria-expanded': 'false' });
        pick.addEventListener('click', () => {
          const open = pick.getAttribute('aria-expanded') === 'true';
          pick.setAttribute('aria-expanded', open ? 'false' : 'true');
          const box = slot.querySelector('.nlbk__pros');
          if (open) { if (box) box.remove(); return; }
          slot.appendChild(prosBox(t));
        });
        top.appendChild(pick);
      }
      slot.appendChild(top);
      list.appendChild(slot);
    }
    s.appendChild(list);
    const j = h('p', 'nlbk__note');
    j.appendChild(document.createTextNode('אנשי מקצוע: '));
    j.appendChild(h('a', null, 'להצטרפות למאגר', { href: C.join }));
    s.appendChild(j);
    return s;
  }

  function prosBox(t) {
    const box = h('div', 'nlbk__pros', null, { 'aria-live': 'polite' });
    box.appendChild(h('p', 'nlbk__sub', 'טוען…'));
    const done = (pros) => {
      box.textContent = '';
      if (!pros.length) {
        box.appendChild(h('p', 'nlbk__sub', 'עוד אין במאגר ' + t.ask + ' באזור.'));
        const a = h('a', 'nlbk__btn nlbk__btn--2', 'לבקש המלצה בוואטסאפ', { href: waLink('שלום, אני בונה סל דירה ב' + C.name + ' באתר nad-lan.co.il ומחפש/ת ' + t.ask + '. אשמח להמלצה.'), target: '_blank', rel: 'noopener' });
        a.addEventListener('click', () => ga('basket_team_ask', { profession: t.key }));
        if (C.wa) box.appendChild(a);
        return;
      }
      for (const p of pros) {
        const r = h('div', 'nlbk__pro');
        const tx = h('div', 'nlbk__itx');
        const nm = h('a', null, p.name, { href: p.url, target: '_blank', rel: 'noopener' });
        const b = h('b'); b.appendChild(nm); tx.appendChild(b);
        tx.appendChild(h('span', null, [p.role, p.city, p.license ? 'רישיון ' + p.license : ''].filter(Boolean).join(' · ')));
        r.appendChild(tx);
        const add = h('button', 'nlbk__btn nlbk__btn--sm', 'לצוות', { type: 'button', 'aria-label': 'להוסיף את ' + p.name + ' לצוות' });
        add.addEventListener('click', () => { S.team[t.key] = { id: p.id, name: p.name, license: p.license || '', url: p.url }; save(); ga('basket_team_add', { profession: t.key }); });
        r.appendChild(add);
        box.appendChild(r);
      }
    };
    if (proCache[t.key]) { done(proCache[t.key]); return box; }
    fetch(C.rest + '?profession=' + encodeURIComponent(t.key) + '&city=' + encodeURIComponent(C.city || ''), { credentials: 'omit' })
      .then((r) => r.json()).then((j) => { proCache[t.key] = (j && j.pros) || []; done(proCache[t.key]); })
      .catch(() => done([]));
    return box;
  }

  function renderPrice() {
    const s = sec('המחיר המלא', 'כל שורה עם המקור שלה. מה שלא ידוע לא מוערך.');
    const f = h('div', 'nlbk__form');
    const lab1 = h('label', 'nlbk__field');
    lab1.appendChild(h('span', null, 'מחיר הדירה (₪)'));
    const inA = h('input', null, null, { type: 'text', inputmode: 'numeric', autocomplete: 'off', placeholder: 'המחיר מהנציג' });
    inA.value = S.price.amount ? nf.format(Number(String(S.price.amount).replace(/[^\d]/g, ''))) : '';
    inA.addEventListener('change', () => { S.price.amount = inA.value.replace(/[^\d]/g, ''); save(); ga('basket_price'); });
    lab1.appendChild(inA);
    f.appendChild(lab1);
    s.appendChild(f);
    if (C.hint) s.appendChild(h('p', 'nlbk__note', C.hint));
    const seg = h('div', 'nlbk__seg', null, { role: 'radiogroup', 'aria-label': 'סוג הרוכש' });
    for (const b of BUYERS) {
      const on = S.price.buyer === b.id;
      const bt = h('button', 'nlbk__chip' + (on ? ' is-on' : ''), b.label, { type: 'button', role: 'radio', 'aria-checked': on ? 'true' : 'false' });
      bt.addEventListener('click', () => { S.price.buyer = b.id; save(); });
      seg.appendChild(bt);
    }
    s.appendChild(seg);
    const buyer = BUYERS.find((x) => x.id === S.price.buyer) || BUYERS[0];
    if (buyer.note) s.appendChild(h('p', 'nlbk__note', buyer.note));
    const p = priceOf();
    const lines = h('dl', 'nlbk__lines');
    const line = (k, v, src) => {
      const d = h('div', 'nlbk__line');
      const dt = h('dt'); dt.appendChild(h('b', null, k)); if (src) dt.appendChild(h('span', null, src));
      d.append(dt, h('dd', null, v));
      lines.appendChild(d);
    };
    if (p.amount > 0) {
      const tx = tax(p.amount, buyer.id);
      const lawPct = Number(String(S.price.lawyer || '').replace(/[^\d.]/g, ''));
      const law = lawPct > 0 && lawPct < 5 ? p.amount * lawPct / 100 : 0;
      line('מחיר הדירה', ils(p.amount), 'כפי שהזנתם');
      line('מס רכישה', ils(tx), 'לפי מדרגות רשות המסים מ־' + (C.tax.effective || '') + (C.tax.frozen ? ', קפואות עד ' + C.tax.frozen : ''));
      line('שכר טרחת עו״ד', law ? ils(law) : 'לפי ההצעה שתקבלו', law ? lawPct + '% מהמחיר, לפני מע״מ' : '');
      const tot = h('div', 'nlbk__line nlbk__line--tot');
      tot.append(h('dt', null, 'סך הכול, לפני משכנתא'), h('dd', null, ils(p.amount + tx + law)));
      lines.appendChild(tot);
      s.appendChild(lines);
      const lab3 = h('label', 'nlbk__field nlbk__field--sm');
      lab3.appendChild(h('span', null, 'שכר טרחת עו״ד באחוזים (לא חובה)'));
      const inL = h('input', null, null, { type: 'text', inputmode: 'decimal', autocomplete: 'off', placeholder: 'למשל 0.5' });
      inL.value = S.price.lawyer || '';
      inL.addEventListener('change', () => { S.price.lawyer = inL.value.replace(/[^\d.]/g, ''); save(); });
      lab3.appendChild(inL);
      s.appendChild(lab3);
      const m = h('p', 'nlbk__note');
      m.appendChild(h('a', null, 'ההחזר החודשי במחשבון המשכנתא', { href: C.mortgage }));
      m.appendChild(document.createTextNode(' · אומדן בלבד, לא חוות דעת מס. '));
      if (C.tax.source) m.appendChild(h('a', null, 'המדרגות ברשות המסים', { href: C.tax.source, target: '_blank', rel: 'noopener nofollow' }));
      s.appendChild(m);
    } else {
      s.appendChild(h('p', 'nlbk__empty', 'הזינו את המחיר שקיבלתם מהנציג כדי לראות את מס הרכישה והסכום המלא.'));
    }
    return s;
  }

  function message() {
    const out = ['שלום, בניתי סל דירה ב' + C.name + ' באתר nad-lan.co.il:'];
    if (S.unit) out.push('• דירה לדוגמה: ' + unitLine(S.unit));
    if (S.style) out.push('• עיצוב: ' + (STYLES[S.style] || S.style));
    const tm = (C.team || []).filter((t) => S.team && S.team[t.key]).map((t) => t.label + ': ' + S.team[t.key].name);
    if (tm.length) out.push('• הצוות: ' + tm.join(', '));
    const p = priceOf();
    if (p.amount > 0) {
      const b = BUYERS.find((x) => x.id === S.price.buyer) || BUYERS[0];
      out.push('• המחיר שהזנתי: ' + ils(p.amount) + ', ' + b.label + ', מס רכישה לפי המדרגות: ' + ils(tax(p.amount, b.id)));
    }
    out.push('אשמח לתוכניות, למחירים ולזמינות. זו בקשה למידע, לא הזמנה.');
    return out.join('\n');
  }

  function renderActions() {
    const s = h('section', 'nlbk__sec nlbk__acts');
    if (C.wa) {
      const a = h('a', 'nlbk__btn nlbk__btn--wa', 'שליחת הסל לנציג בוואטסאפ', { href: '#', target: '_blank', rel: 'noopener' });
      a.addEventListener('click', () => { a.href = waLink(message()); ga('basket_send', { items: count() }); });
      s.appendChild(a);
    }
    const video = document.querySelector('a[data-nlps-ev="hero-video"]');
    if (video) {
      const r = h('button', 'nlbk__btn nlbk__btn--2', 'לחדר צפייה משותף עם נציג', { type: 'button' });
      r.addEventListener('click', () => { close(); ga('basket_room'); video.click(); });
      s.appendChild(r);
    }
    s.appendChild(h('p', 'nlbk__legal', 'הסל אינו רכישה והדירה לא נמכרת באתר. בקשת שריון והמחירים מול הנציג; כל תשלום על הדירה רק לחשבון הליווי של הפרויקט, מול ערבות לפי חוק המכר. נדל״ן אינו מתווך ואינו היזם. הסל נשמר רק בדפדפן הזה.'));
    const clr = h('button', 'nlbk__link nlbk__clear', 'לרוקן את הסל', { type: 'button' });
    clr.addEventListener('click', () => { S = { unit: null, style: null, team: {}, price: { amount: '', buyer: 'single', lawyer: '' } }; save(); ga('basket_clear'); });
    s.appendChild(clr);
    return s;
  }

  function renderBody() {
    if (!body) return;
    const y = body.scrollTop;
    body.textContent = '';
    body.append(steps(), renderUnit(), renderStyle(), renderTeam(), renderPrice(), renderActions());
    body.scrollTop = y;
  }

  function open(from) {
    if (!root) build();
    opener = from || document.activeElement;
    renderBody();
    root.hidden = false;
    document.documentElement.classList.add('nlbk-open');
    requestAnimationFrame(() => root.classList.add('is-on'));
    const x = root.querySelector('.nlbk__x');
    if (x) x.focus();
    ga('basket_open', { items: count() });
  }
  function close() {
    if (!root || root.hidden) return;
    root.classList.remove('is-on');
    document.documentElement.classList.remove('nlbk-open');
    root.hidden = true;
    if (opener && opener.focus) opener.focus();
  }

  /* ---------------- the ways in ---------------- */
  const entries = [];
  function paint() {
    const n = count();
    for (const b of entries) {
      const c = b.querySelector('.nlbk-count');
      if (c) { c.textContent = String(n); c.hidden = n === 0; }
    }
    if (root && !root.hidden) renderBody();
  }
  function entry(cls, label) {
    const b = h('button', cls, null, { type: 'button', 'aria-haspopup': 'dialog' });
    b.appendChild(h('span', null, label));
    b.appendChild(h('b', 'nlbk-count', '0', { 'aria-label': 'פריטים בסל' }));
    b.addEventListener('click', () => open(b));
    entries.push(b);
    return b;
  }
  function mount() {
    const stepsList = document.querySelector('.nlps-steps');
    if (stepsList) {
      const li = h('li');
      li.appendChild(entry('nlps-step nlbk-step', 'סל הדירה'));
      stepsList.appendChild(li);
    }
    const cta = document.getElementById('nlps-view-cta');
    if (cta) cta.appendChild(entry('nlds-btn nlds-btn--secondary nlbk-add', 'לסל הדירה'));
    paint();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
  window.__nlBasket = { open, close, get state() { return JSON.parse(JSON.stringify(S)); } };
})();
