/* HAD-712 step 6 (12.11.2026): on Kikar, "Build me an offer" (project-stage/world/kikarbuy.js) above the WhatsApp button. */
/* HAD-712 (12.11.2026): waymarks, view with details, floor plan (the Kikar showroom's inside counts as the way inside: the Design section offers it). */
/* HAD-712 (11.11.2026): words from showroom-i18n.js; direction from the page language. */
/* The apartment's basket (design system L9Nqz7Viv7K3MYeZrBc9s8 version 86, BasketOne; the journey: BuyJourney v78).
 * What the buyer picked on the project page, in one drawer: the example apartment (the stage's nl:floor / nl:facing), the
 * design style (the 360 viewer's nl:view), a team of real professionals (inc/basket.php, never a sample profile), the full
 * price (purchase tax by the brackets in force), and two ways on: the basket to the representative on WhatsApp and the
 * shared viewing room. Nothing is sold or paid here; the drawer says so. Kept in this browser only, per project.
 * Words (HAD-712): window.__nlI18n (project-stage/world/showroom-i18n.js) by the page language (cfg.lang, then the page); each
 * call carries today's Hebrew as the fallback, so a Hebrew page without the dictionary prints exactly what it printed before.
 * On an en/fr page the basket loads the dictionary itself; the directory's professionals (Hebrew names) are not listed there:
 * each role asks NadLan for a recommendation on WhatsApp instead. */
(function () {
  'use strict';
  const cfgEl = document.getElementById('nadlan-basket-cfg');
  if (!cfgEl) return;
  let C;
  try { C = JSON.parse(cfgEl.textContent); } catch (e) { return; }
  const SELF = (document.currentScript && document.currentScript.src) || '';
  const KEY = 'nl-basket:' + C.slug;
  const ga = (n, p) => { try { if (window.nadlanGA) window.nadlanGA(n, Object.assign({ project: C.name }, p || {})); } catch (e) { /* none */ } };

  /* ---------------- the words (HAD-712) ---------------- */
  const LG = () => {
    const v = String(C.lang || (window.__nlI18n ? window.__nlI18n.lang() : '') || document.documentElement.lang || '').slice(0, 2).toLowerCase();
    return !v ? 'he' : (v === 'he' || v === 'en' || v === 'fr' ? v : 'en');
  };
  const EN = () => LG() !== 'he'; // en or fr: a left-to-right page that must not print Hebrew
  const heb = (s) => /[֐-׿]/.test(String(s == null ? '' : s));
  const fill = (s, v) => (v ? s.replace(/\$\{(\w+)\}/g, (m, k) => (v[k] == null ? '' : String(v[k]))) : s);
  const T = (key, he, v) => (window.__nlI18n ? window.__nlI18n.t(key, v, LG()) : fill(he, v)); // Hebrew until the dictionary is there
  if (!window.__nlI18n && EN() && SELF) { try { import(SELF.replace(/basket\/basket\.js(\?.*)?$/, 'project-stage/world/showroom-i18n.js$1')).catch(() => {}); } catch (e) { /* none */ } }
  const NF = {};
  const nf = { format: (n) => { const l = { he: 'he-IL', en: 'en-GB', fr: 'fr-FR' }[LG()] || 'he-IL'; return (NF[l] = NF[l] || new Intl.NumberFormat(l, { maximumFractionDigits: 0 })).format(n); } };
  const ils = (n) => T('money', '${n} ₪', { n: nf.format(Math.round(n)) });
  const BUYERS = [
    { id: 'single', get label() { return T('bk_buyer_single', 'דירה יחידה'); }, brackets: 'single' },
    { id: 'additional', get label() { return T('tax_additional_home', 'דירה נוספת'); }, brackets: 'additional' },
    { id: 'foreign', get label() { return T('bk_buyer_foreign', 'תושב/ת חוץ'); }, brackets: 'additional', get note() { return T('bk_buyer_foreign_note', 'תושב חוץ אינו זכאי למדרגות של דירה יחידה ומשלם לפי מדרגות דירה נוספת מהשקל הראשון.'); } },
  ];
  const STYLES = {
    get bare() { return T('bk_style_bare', 'כמו במסירה'); }, get warm() { return T('style_warm', 'עץ חם'); },
    get light() { return T('style_light', 'בהיר'); }, get stone() { return T('style_stone', 'אבן'); },
  };
  // the project's name, the team's words and a chosen professional in the page language (on en/fr never the Hebrew from PHP)
  const projName = (title) => { // title: the heading form (fr 'Tours Kikar Hamedina'), else the in-sentence form
    if (!EN()) return C.name;
    if (/hamedina|kikar/i.test(String(C.slug || '')) && window.__nlI18n) return T(title ? 'project_title' : 'project_name', '');
    const n = C['name_' + LG()] || C.name_en || C.name || '';
    return heb(n) ? '' : n;
  };
  const teamLabel = (t) => (EN() ? T('bk_team_' + t.key, t.label) : t.label);
  const teamAsk = (t) => (EN() ? T('bk_ask_' + t.key, t.ask) : t.ask);
  const proName = (p) => (EN() && heb(p.name) ? T('bk_team_chosen', 'נבחר מהמאגר') : p.name);

  /* ---------------- the state, in this browser ---------------- */
  let S = { unit: null, style: null, team: {}, price: { amount: '', buyer: 'single', lawyer: '' } };
  try { const s = JSON.parse(localStorage.getItem(KEY) || 'null'); if (s && typeof s === 'object') S = Object.assign(S, s, { price: Object.assign(S.price, s.price || {}) }); } catch (e) { /* private window */ }
  // HAD-712: a choice saved by the showroom before 11.11.2026 carries its tower as Hebrew words ("מגדל A"): read it as the tower letter
  if (S.unit && !S.unit.tower && typeof S.unit.label === 'string') { const m = /^מגדל ([A-Z])$/.exec(S.unit.label); if (m) { S.unit.tower = m[1]; S.unit.label = null; } }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* none */ } paint(); };

  const DKEYS = ['dir_to_n', 'dir_to_ne', 'dir_to_e', 'dir_to_se', 'dir_to_s', 'dir_to_sw', 'dir_to_w', 'dir_to_nw'];
  const words = (b) => {
    if (b == null) return '';
    const x = ((Number(b) % 360) + 360) % 360;
    for (const s of C.sectors || []) {
      const a = s[0], z = s[1];
      if (a <= z ? (x >= a && x < z) : (x >= a || x < z)) {
        if (!EN()) return s[2];
        const I = window.__nlI18n; // en/fr: the dictionary's sector word, else the direction word; never the PHP Hebrew
        return I ? (I.secWord(s[2], LG()) || I.t(DKEYS[Math.round(x / 45) % 8], null, LG())) : '';
      }
    }
    return '';
  };
  // 1.72.391: a world page's own words for the apartment (its label) come before the sectors' direction words
  // HAD-712: the showroom's choice is data (the tower letter), its words are made here in the page language
  const unitName = (u) => (u.tower ? T('tower_n', 'מגדל ${tower}', { tower: u.tower }) : (u.label && !(EN() && heb(u.label)) ? u.label : ''));
  const unitLine = (u) => u ? (T('floor_n', 'קומה ${floor}', { floor: u.floor }) + (unitName(u) ? ' · ' + unitName(u) : (u.bearing != null && words(u.bearing) ? ' · ' + words(u.bearing) : ''))) : '';
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
    const tw = d.source === 'showroom' && d.tower ? String(d.tower).slice(0, 4) : null; // HAD-712: stored as data, not as words
    S.unit = { floor: Number(d.floor), bearing: d.bearing != null ? Math.round(Number(d.bearing)) : null, unit: d.unit || null, label: !tw && d.label ? String(d.label).slice(0, 60) : null };
    if (tw) { S.unit.tower = tw; if (d.side != null && isFinite(d.side)) S.unit.side = Number(d.side); }
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
    root = h('div', 'nlbk', null, { role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'nlbk-t', dir: EN() ? 'ltr' : 'rtl', lang: LG(), hidden: '' });
    const scrim = h('div', 'nlbk__scrim');
    scrim.addEventListener('click', close);
    const sheet = h('div', 'nlbk__sheet');
    const head = h('div', 'nlbk__head');
    const tt = h('div', 'nlbk__tt');
    tt.appendChild(h('p', 'nlbk__kick', projName(true)));
    tt.appendChild(h('h2', 'nlbk__title', T('basket_name', 'סל הדירה'), { id: 'nlbk-t' }));
    const x = h('button', 'nlbk__x', '×', { type: 'button', 'aria-label': T('bk_aria_close', 'סגירת הסל') });
    x.addEventListener('click', close);
    head.append(tt, x);
    body = h('div', 'nlbk__body');
    sheet.append(head, body);
    root.append(scrim, sheet);
    document.body.appendChild(root);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && root && !root.hidden) close(); });
  }

  function steps() {
    const ol = h('ol', 'nlbk__steps', null, { 'aria-label': T('bk_aria_steps', 'השלבים') });
    const st = [[T('bk_step_building', 'הבניין'), true], [T('bk_apartment', 'הדירה'), !!S.unit], [T('bk_design', 'העיצוב'), !!S.style], [T('bk_step_team', 'הצוות'), Object.keys(S.team || {}).length > 0], [T('bk_step_price', 'המחיר'), priceOf().amount > 0]];
    st.forEach(([t, done], i) => {
      const li = h('li', 'nlbk__step' + (done ? ' is-done' : ''));
      li.appendChild(h('i', null, done ? '✓' : String(i + 1), { 'aria-hidden': 'true' }));
      li.appendChild(document.createTextNode(t));
      if (done) li.appendChild(h('span', 'nlbk__sr', T('bk_sr_done', ' (נבחר)')));
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
  // HAD-712 (12.11.2026): the Kikar showroom (world/showroom.js) announces window.__nlShowroomInside, the apartment screen's inside
  // in 360 with its finishes; the basket checked only the earlier stage's hooks, so Kikar read "not available yet". It comes first.
  const showroomIn = () => typeof window.__nlShowroomInside === 'function';
  const worldIn = () => showroomIn() || typeof window.__nlInsideGo === 'function';
  const insideOk = () => showroomIn() || !!document.querySelector('.nlat__go') || typeof window.__nlInsideGo === 'function';
  function goInside() {
    close();
    if (showroomIn()) { window.__nlShowroomInside(); return; }
    const b = document.querySelector('.nlat__go');
    if (b) b.click(); else if (typeof window.__nlInsideGo === 'function') window.__nlInsideGo();
  }

  function renderUnit() {
    const s = sec(T('bk_apartment', 'הדירה'));
    if (S.unit) {
      const row = h('div', 'nlbk__item');
      row.appendChild(h('span', 'nlbk__badge', String(S.unit.floor), { 'aria-hidden': 'true' }));
      const tx = h('div', 'nlbk__itx');
      tx.appendChild(h('b', null, T('bk_unit_example', 'דירה לדוגמה · ${unit}', { unit: unitLine(S.unit) })));
      tx.appendChild(h('span', null, S.unit.bearing != null ? T('bk_unit_from_rep', 'הדירות, התוכניות והמחירים מהנציג') : T('bk_unit_no_dir', 'עוד לא נבחר כיוון בטבעת הקומה')));
      row.appendChild(tx);
      const ch = h('button', 'nlbk__link', T('bk_change', 'להחליף'), { type: 'button' });
      ch.addEventListener('click', goStage);
      row.appendChild(ch);
      s.appendChild(row);
    } else {
      s.appendChild(h('p', 'nlbk__empty', T('bk_no_floor', 'עוד לא נבחרה קומה.')));
      const b = h('button', 'nlbk__btn nlbk__btn--2', T('bk_pick_floor', 'לבחירת קומה על הבניין'), { type: 'button' });
      b.addEventListener('click', goStage);
      s.appendChild(b);
    }
    return s;
  }

  function renderStyle() {
    const s = sec(T('bk_design', 'העיצוב'), T('bk_design_sub', 'רעיון עיצוב להמחשה בדירה לדוגמה, לא המפרט של היזם.'));
    const has = insideOk();
    // 1.72.392: on a world page "bare" is the original rendered design (furnished), not a design choice
    if (S.style && !(S.style === 'bare' && worldIn())) {
      const row = h('div', 'nlbk__item');
      row.appendChild(h('span', 'nlbk__sw nlbk__sw--' + S.style, null, { 'aria-hidden': 'true' }));
      const tx = h('div', 'nlbk__itx');
      tx.appendChild(h('b', null, STYLES[S.style] || S.style));
      tx.appendChild(h('span', null, T('bk_style_chosen', 'נבחר בתוך הדירה ב־360°')));
      row.appendChild(tx);
      if (has) { const ch = h('button', 'nlbk__link', T('bk_change', 'להחליף'), { type: 'button' }); ch.addEventListener('click', goInside); row.appendChild(ch); }
      s.appendChild(row);
    } else if (has) {
      const b = h('button', 'nlbk__btn nlbk__btn--2', T('bk_go_inside', 'להיכנס לדירה ולבחור סגנון'), { type: 'button' });
      b.addEventListener('click', goInside);
      s.appendChild(b);
    } else {
      s.appendChild(h('p', 'nlbk__empty', T('bk_inside_na', 'הדירה מבפנים עוד לא זמינה בפרויקט הזה.')));
    }
    return s;
  }

  function waLink(text) {
    return C.wa ? 'https://wa.me/' + C.wa + '?text=' + encodeURIComponent(text) : '';
  }
  // the request for a recommendation (Ben's Hebrew; en/fr AWAITING BEN: the English page's sentence)
  function recoText(t) {
    const v = { project: projName(), ask: teamAsk(t) };
    v.desc = T('bk_wa_reco_desc', '${ask}, ${project}', v);
    return T('bk_wa_reco', 'שלום, אני בונה סל דירה ב${project} באתר nad-lan.co.il ומחפש/ת ${ask}. אשמח להמלצה.', v);
  }

  function renderTeam() {
    const s = sec(T('bk_team_title', 'הצוות שלכם'), EN() ? T('bk_team_sub_rec', 'אנשי מקצוע מהמאגר, עם בדיקת רישיון כשיש. בלי עמלה על הפנייה.') : T('bk_team_sub', 'אנשי מקצוע מהמאגר, עם בדיקת רישיון כשיש. בלי עמלה על הפנייה.'));
    const list = h('div', 'nlbk__team');
    for (const t of C.team || []) {
      const slot = h('div', 'nlbk__slot');
      const chosen = S.team && S.team[t.key];
      const top = h('div', 'nlbk__slot-top');
      let ask = null; // en/fr: the recommendation request, on its own row under the role
      top.appendChild(h('span', 'nlbk__mono', chosen ? (EN() && heb(chosen.name) ? '✓' : (chosen.name || '').slice(0, 1)) : '+', { 'aria-hidden': 'true' }));
      const tx = h('div', 'nlbk__itx');
      tx.appendChild(h('b', null, teamLabel(t)));
      tx.appendChild(h('span', null, chosen ? proName(chosen) + (chosen.license ? ' · ' + T('bk_license_n', 'רישיון ${license}', { license: chosen.license }) : '') : T('bk_not_chosen', 'עוד לא נבחר')));
      top.appendChild(tx);
      if (chosen) {
        const rm = h('button', 'nlbk__link', T('bk_remove', 'להסיר'), { type: 'button', 'aria-label': T('bk_aria_remove', 'להסיר את ${name}', { name: proName(chosen) }) });
        rm.addEventListener('click', () => { delete S.team[t.key]; save(); ga('basket_team_remove', { profession: t.key }); });
        top.appendChild(rm);
      } else if (EN()) { // HAD-712: on en/fr no directory list (Hebrew names): NadLan recommends, on WhatsApp
        if (C.wa) {
          const a = h('a', 'nlbk__link', T('bk_ask_nadlan', 'לבקש המלצה בוואטסאפ'), { href: waLink(recoText(t)), target: '_blank', rel: 'noopener' });
          a.addEventListener('click', () => ga('basket_team_ask', { profession: t.key }));
          ask = a;
        }
      } else {
        const pick = h('button', 'nlbk__link', T('bk_choose', 'לבחור'), { type: 'button', 'aria-expanded': 'false' });
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
      if (ask) slot.appendChild(ask);
      list.appendChild(slot);
    }
    s.appendChild(list);
    const j = h('p', 'nlbk__note');
    j.appendChild(document.createTextNode(T('bk_join_prefix', 'אנשי מקצוע: ')));
    j.appendChild(h('a', null, T('bk_join', 'להצטרפות למאגר'), { href: C.join }));
    s.appendChild(j);
    return s;
  }

  function prosBox(t) {
    const box = h('div', 'nlbk__pros', null, { 'aria-live': 'polite' });
    box.appendChild(h('p', 'nlbk__sub', T('loading', 'טוען…')));
    const done = (pros) => {
      box.textContent = '';
      if (!pros.length) {
        box.appendChild(h('p', 'nlbk__sub', T('bk_pros_none', 'עוד אין במאגר ${ask} באזור.', { ask: teamAsk(t) })));
        const a = h('a', 'nlbk__btn nlbk__btn--2', T('bk_ask_reco', 'לבקש המלצה בוואטסאפ'), { href: waLink(recoText(t)), target: '_blank', rel: 'noopener' });
        a.addEventListener('click', () => ga('basket_team_ask', { profession: t.key }));
        if (C.wa) box.appendChild(a);
        return;
      }
      for (const p of pros) {
        const r = h('div', 'nlbk__pro');
        const tx = h('div', 'nlbk__itx');
        const nm = h('a', null, p.name, { href: p.url, target: '_blank', rel: 'noopener' });
        const b = h('b'); b.appendChild(nm); tx.appendChild(b);
        tx.appendChild(h('span', null, [p.role, p.city, p.license ? T('bk_license_n', 'רישיון ${license}', { license: p.license }) : ''].filter(Boolean).join(' · ')));
        r.appendChild(tx);
        const add = h('button', 'nlbk__btn nlbk__btn--sm', T('bk_add_team', 'לצוות'), { type: 'button', 'aria-label': T('bk_aria_add', 'להוסיף את ${name} לצוות', { name: p.name }) });
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
    const s = sec(T('bk_price_title', 'המחיר המלא'), T('bk_price_sub', 'כל שורה עם המקור שלה. מה שלא ידוע לא מוערך.'));
    const f = h('div', 'nlbk__form');
    const lab1 = h('label', 'nlbk__field');
    lab1.appendChild(h('span', null, T('bk_price_label', 'מחיר הדירה (₪)')));
    const inA = h('input', null, null, { type: 'text', inputmode: 'numeric', autocomplete: 'off', placeholder: T('bk_price_ph', 'המחיר מהנציג') });
    inA.value = S.price.amount ? nf.format(Number(String(S.price.amount).replace(/[^\d]/g, ''))) : '';
    inA.addEventListener('change', () => { S.price.amount = inA.value.replace(/[^\d]/g, ''); save(); ga('basket_price'); });
    lab1.appendChild(inA);
    f.appendChild(lab1);
    s.appendChild(f);
    if (C.hint && !EN()) s.appendChild(h('p', 'nlbk__note', C.hint)); // HAD-712: the hint is Hebrew from PHP: never on en/fr
    const seg = h('div', 'nlbk__seg', null, { role: 'radiogroup', 'aria-label': T('bk_aria_buyer', 'סוג הרוכש') });
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
      const frozen = C.tax.frozen ? (EN() ? (window.__nlI18n ? window.__nlI18n.heDate(C.tax.frozen, LG()) : '') : C.tax.frozen) : '';
      line(T('bk_line_price', 'מחיר הדירה'), ils(p.amount), T('bk_line_price_src', 'כפי שהזנתם'));
      line(T('purchase_tax', 'מס רכישה'), ils(tx), T('bk_tax_src', 'לפי מדרגות רשות המסים מ־${effective}${frozen}', { effective: C.tax.effective || '', frozen: frozen ? T('bk_tax_frozen', ', קפואות עד ${date}', { date: frozen }) : '' }));
      line(T('bk_line_lawyer', 'שכר טרחת עו״ד'), law ? ils(law) : T('bk_lawyer_quote', 'לפי ההצעה שתקבלו'), law ? T('bk_lawyer_pct', '${pct}% מהמחיר, לפני מע״מ', { pct: LG() === 'fr' ? String(lawPct).replace('.', ',') : lawPct }) : '');
      const tot = h('div', 'nlbk__line nlbk__line--tot');
      tot.append(h('dt', null, T('bk_total', 'סך הכול, לפני משכנתא')), h('dd', null, ils(p.amount + tx + law)));
      lines.appendChild(tot);
      s.appendChild(lines);
      const lab3 = h('label', 'nlbk__field nlbk__field--sm');
      lab3.appendChild(h('span', null, T('bk_lawyer_pct_label', 'שכר טרחת עו״ד באחוזים (לא חובה)')));
      const inL = h('input', null, null, { type: 'text', inputmode: 'decimal', autocomplete: 'off', placeholder: T('bk_lawyer_ph', 'למשל 0.5') });
      inL.value = S.price.lawyer || '';
      inL.addEventListener('change', () => { S.price.lawyer = (LG() === 'fr' ? inL.value.replace(',', '.') : inL.value).replace(/[^\d.]/g, ''); save(); });
      lab3.appendChild(inL);
      s.appendChild(lab3);
      const m = h('p', 'nlbk__note');
      m.appendChild(h('a', null, T('bk_mortgage_link', 'ההחזר החודשי במחשבון המשכנתא'), { href: C.mortgage }));
      m.appendChild(document.createTextNode(T('bk_estimate', ' · אומדן בלבד, לא חוות דעת מס. ')));
      if (C.tax.source) m.appendChild(h('a', null, T('bk_tax_link', 'המדרגות ברשות המסים'), { href: C.tax.source, target: '_blank', rel: 'noopener nofollow' }));
      s.appendChild(m);
    } else {
      s.appendChild(h('p', 'nlbk__empty', T('bk_price_empty', 'הזינו את המחיר שקיבלתם מהנציג כדי לראות את מס הרכישה והסכום המלא.')));
    }
    return s;
  }

  function message() {
    const tm = (C.team || []).filter((t) => S.team && S.team[t.key]).map((t) => teamLabel(t) + ': ' + proName(S.team[t.key]));
    const p = priceOf(), b = BUYERS.find((x) => x.id === S.price.buyer) || BUYERS[0];
    const pv = p.amount > 0 ? { price: ils(p.amount), buyer: b.label, tax: ils(tax(p.amount, b.id)) } : null;
    if (EN()) { // AWAITING BEN: the English page's sentence; the selection, in the page language, is its subject
      const d = [T('bk_wa_desc', '', { project: projName() })];
      if (S.unit) d.push(T('bk_wa_d_unit', '', { unit: unitLine(S.unit) }));
      if (S.style) d.push(T('bk_wa_d_style', '', { style: STYLES[S.style] || S.style }));
      if (tm.length) d.push(T('bk_wa_d_team', '', { team: tm.join(', ') }));
      if (pv) d.push(T('bk_wa_d_price', '', pv));
      return T('bk_wa_sentence', '${desc}', { desc: d.join('; ') });
    }
    const out = [T('bk_wa_msg_intro', 'שלום, בניתי סל דירה ב${project} באתר nad-lan.co.il:', { project: C.name })];
    if (S.unit) out.push(T('bk_wa_msg_unit', '• דירה לדוגמה: ${unit}', { unit: unitLine(S.unit) }));
    if (S.style) out.push(T('bk_wa_msg_style', '• עיצוב: ${style}', { style: STYLES[S.style] || S.style }));
    if (tm.length) out.push(T('bk_wa_msg_team', '• הצוות: ${team}', { team: tm.join(', ') }));
    if (pv) out.push(T('bk_wa_msg_price', '• המחיר שהזנתי: ${price}, ${buyer}, מס רכישה לפי המדרגות: ${tax}', pv));
    out.push(T('bk_wa_msg_close', 'אשמח לתוכניות, למחירים ולזמינות. זו בקשה למידע, לא הזמנה.'));
    return out.join('\n');
  }

  // HAD-712 step 6 (12.11.2026): Kikar's "Build me an offer" (project-stage/world/kikarbuy.js): the selection becomes a request to
  // the seller through the showroom engine's two calls (lead, then the request document); loaded on the tap only
  const KIKAR = /^hamedina(-(en|fr))?$/.test(String(C.slug || ''));
  function offer(btn) {
    const go = (m) => { close(); m.open({ state: JSON.parse(JSON.stringify(S)), cfg: C, from: btn }); };
    try { import(SELF.replace(/basket\/basket\.js(\?.*)?$/, 'project-stage/world/kikarbuy.js$1')).then(go).catch((e) => console.warn('[basket] offer', e)); } catch (e) { /* none */ }
    ga('basket_offer', { items: count() });
  }

  function renderActions() {
    const s = h('section', 'nlbk__sec nlbk__acts');
    if (KIKAR && SELF) {
      const o = h('button', 'nlbk__btn nlbk__btn--offer', T('kb_open', 'בנו לי הצעה'), { type: 'button' });
      o.addEventListener('click', () => offer(o));
      s.appendChild(o);
    }
    if (C.wa) {
      const a = h('a', 'nlbk__btn nlbk__btn--wa', T('bk_send_wa', 'שליחת הסל לנציג בוואטסאפ'), { href: '#', target: '_blank', rel: 'noopener' });
      a.addEventListener('click', () => { a.href = waLink(message()); ga('basket_send', { items: count() }); });
      s.appendChild(a);
    }
    const video = document.querySelector('a[data-nlps-ev="hero-video"]');
    if (video) {
      const r = h('button', 'nlbk__btn nlbk__btn--2', T('bk_room', 'לחדר צפייה משותף עם נציג'), { type: 'button' });
      r.addEventListener('click', () => { close(); ga('basket_room'); video.click(); });
      s.appendChild(r);
    }
    s.appendChild(h('p', 'nlbk__legal', T('bk_legal', 'הסל אינו רכישה והדירה לא נמכרת באתר. בקשת שריון והמחירים מול הנציג; כל תשלום על הדירה רק לחשבון הליווי של הפרויקט, מול ערבות לפי חוק המכר. נדל״ן אינו מתווך ואינו היזם. הסל נשמר רק בדפדפן הזה.')));
    const clr = h('button', 'nlbk__link nlbk__clear', T('bk_clear', 'לרוקן את הסל'), { type: 'button' });
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
  function entry(cls, key, he) {
    const b = h('button', cls, null, { type: 'button', 'aria-haspopup': 'dialog' });
    b.appendChild(h('span', null, T(key, he)));
    b.appendChild(h('b', 'nlbk-count', '0', { 'aria-label': T('bk_aria_count', 'פריטים בסל') }));
    b._nlk = [key, he];
    b.addEventListener('click', () => open(b));
    entries.push(b);
    return b;
  }
  // HAD-712: the dictionary arrived after the basket painted (en/fr): the same elements, their words in the page language
  function relabel() {
    for (const b of entries) {
      const s = b.querySelector('span'), c = b.querySelector('.nlbk-count');
      if (s && b._nlk) s.textContent = T(b._nlk[0], b._nlk[1]);
      if (c) c.setAttribute('aria-label', T('bk_aria_count', 'פריטים בסל'));
    }
    if (root) {
      const k = root.querySelector('.nlbk__kick'), tt = root.querySelector('.nlbk__title'), x = root.querySelector('.nlbk__x');
      if (k) k.textContent = projName(true); if (tt) tt.textContent = T('basket_name', 'סל הדירה'); if (x) x.setAttribute('aria-label', T('bk_aria_close', 'סגירת הסל'));
      if (!root.hidden) renderBody();
    }
  }
  window.addEventListener('nl:i18n', relabel);
  function mount() {
    const stepsList = document.querySelector('.nlps-steps');
    if (stepsList) {
      const li = h('li');
      li.appendChild(entry('nlps-step nlbk-step', 'basket_name', 'סל הדירה'));
      stepsList.appendChild(li);
    }
    const cta = document.getElementById('nlps-view-cta');
    if (cta) cta.appendChild(entry('nlds-btn nlds-btn--secondary nlbk-add', 'bk_open', 'לסל הדירה'));
    paint();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
  window.__nlBasket = { open, close, get state() { return JSON.parse(JSON.stringify(S)); } };
})();
