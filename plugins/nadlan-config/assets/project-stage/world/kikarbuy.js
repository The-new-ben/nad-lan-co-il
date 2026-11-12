/* HAD-712 step 6 (12.11.2026): Kikar HaMedina, "Build me an offer" from My selection (boards ShowBuyHE / ShowBuyEN, S9 / E9).
 * Ben 11.11.2026: "enter, design, get a quote, buy, like a shop", like Rainbow and DUO.
 *
 * The same request as the showroom engine's buy flow (assets/showroom-engine/buyflow.js, live text 12.11.2026), not a second one:
 * the same two calls with the same fields: POST nadlan/v1/lead (source "rfp-v1", the "rfp-v1" message), then POST nadlan/v1/rfp
 * (project, unit, finish, extras, lang, name, lead_id), which writes the request document on the server (inc/rfp.php: an
 * unguessable link, 30 days, the unit re-read on the server, real advisors, a timeline that claims only what happened). Only the
 * screens are Kikar's, because the boards ask for three steps (summary, contact, confirmation) where buyflow.js shows five, and
 * buyflow.js needs the engine's window.NADLAN_SHOWROOM and a project_3d_units list that Kikar does not have.
 * What this adds to buyflow's request: the consent and its sentence (stored by the lead endpoint), the unit's tower, floor and
 * bearing as lead fields, one lead only (a failed document is retried alone, never a second lead), the request number.
 *
 * The apartment is an example apartment: tower, floor and the direction it faces, from the showroom (My selection's unit), sent
 * as "B20-276" (the page's own #dira= id). No rooms, no area, no price: none is published per apartment here.
 * The finish is My selection's style (the 360 inside): bare -> "std" (as delivered = the developer's spec), else its name.
 * Words: showroom-i18n.js (kb_* keys), he / en / fr. One pulse at a time: the step's primary button, still with reduced motion.
 *
 *   import('.../kikarbuy.js').then((m) => m.open({ state, cfg, from }))   state = window.__nlBasket.state, cfg = the basket's config
 */
const I = window.__nlI18n || (await import(new URL('showroom-i18n.js' + (new URL(import.meta.url).search || ''), import.meta.url).href)).default;
const L = (() => { const c = window.__nlJourneyCfg || {}; const v = String(c.lang || I.lang() || 'he').slice(0, 2); return v === 'he' || v === 'en' || v === 'fr' ? v : 'en'; })();
const t = (k, v) => I.t(k, v, L);
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const ga = (n, p) => { try { if (window.nadlanGA) window.nadlanGA(n, Object.assign({ project: 'hamedina' }, p || {})); } catch (e) { /* none */ } };
const reduced = () => { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } };
const norm = (b) => ((Number(b) % 360) + 360) % 360;
const ix = (b) => Math.round(norm(b) / 45) % 8;
const DTO = ['dir_to_n', 'dir_to_ne', 'dir_to_e', 'dir_to_se', 'dir_to_s', 'dir_to_sw', 'dir_to_w', 'dir_to_nw'];
const DN = ['dir_n', 'dir_ne', 'dir_e', 'dir_se', 'dir_s', 'dir_sw', 'dir_w', 'dir_nw'];
const dirTo = (b) => t(DTO[ix(b)]);
const dirNoun = (b) => (L === 'fr' ? t(DTO[ix(b)]) : t(DN[ix(b)])); // as the showroom's card ("מערב", "west", "ouest")
const REST = (location.origin || '') + '/wp-json/nadlan/v1/';
// My selection's team keys (inc/basket.php) -> the request's advisor kinds (inc/rfp.php nadlan_rfp_advisor_map)
const TEAM = [['designer', 'interior_designer'], ['lawyer', 'lawyer'], ['mortgage', 'mashkanta'], ['inspect', 'engineer']];
const SK = 'nlkb-sent:' + location.pathname; // a request already sent from this tab, per apartment: never a second lead

let root = null, opener = null, F = null;

function css() {
  if (document.getElementById('nlkb-css')) return;
  const s = document.createElement('style'); s.id = 'nlkb-css';
  s.textContent = `
.nlkb{--k-ink:#14212b;--k-sea:#2f6f86;--k-night:#0d2129;--k-paper:#f2f5f7;--k-line:#c9d2d8;--k-glass:#7fd3e6;--k-mute:#55636e;--k-wa:#0f7a63;
position:fixed;inset:0;z-index:100001;display:flex;justify-content:center;align-items:stretch;font-family:'Assistant','Segoe UI',Arial,sans-serif;color:var(--k-ink);text-align:start}
.nlkb[hidden]{display:none!important}
html.nlkb-open{overflow:hidden}
html.nlkb-open .nlsr-pulse,html.nlkb-open .nlsr-pulse-b,html.nlkb-open .nlpf__apt--pulse{animation:none!important;box-shadow:none!important}
.nlkb__scrim{position:absolute;inset:0;background:rgba(13,33,41,.55)}
.nlkb__panel{position:relative;width:100%;max-width:100%;height:100%;display:flex;flex-direction:column;background:var(--k-paper);overflow:hidden}
@media (min-width:760px){.nlkb{align-items:center;padding:24px}.nlkb__panel{max-width:600px;height:min(900px,calc(100dvh - 48px));border-radius:20px;box-shadow:0 24px 70px rgba(13,33,41,.35)}}
.nlkb__bar{flex:none;display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:64px;padding:10px 16px;background:var(--k-night);color:#fff}
.nlkb .nlkb__back{min-height:44px;min-width:44px;padding:0 16px;border:0;border-radius:999px!important;background:rgba(255,255,255,.1);color:#fff!important;font:700 16px/1 'Assistant',sans-serif;cursor:pointer;white-space:nowrap}
.nlkb__cnt{font:400 15px/1.2 'Assistant',sans-serif;color:#d6e1e6;white-space:nowrap}
.nlkb__body{flex:1;overflow-y:auto;overscroll-behavior:contain;padding:22px 18px 18px;display:flex;flex-direction:column;gap:12px}
:root body .nlkb h2.nlkb__t{margin:0!important;font:600 30px/1.15 'Noto Serif Hebrew','Noto Serif',Georgia,serif!important;color:var(--k-ink)!important;letter-spacing:0}
.nlkb__t:focus{outline:none}
.nlkb__sub{margin:-4px 0 4px!important;font:400 16px/1.4 'Assistant',sans-serif!important;color:#3b4753!important}
.nlkb__apt{display:flex;align-items:center;gap:14px;padding:14px;background:#fff;border:1px solid var(--k-line);border-radius:16px}
.nlkb__apt img{flex:none;width:96px;height:72px;object-fit:cover;border-radius:10px;background:#dfe7eb}
.nlkb__apt b{display:block;font:700 18px/1.25 'Assistant',sans-serif;color:var(--k-ink)}
.nlkb__apt span{display:block;font:400 14.5px/1.4 'Assistant',sans-serif;color:var(--k-mute)}
:root body .nlkb h3.nlkb__h{margin:10px 0 0!important;font:700 16px/1.3 'Assistant',sans-serif!important;color:var(--k-sea)!important}
.nlkb__rows{display:flex;flex-direction:column;gap:8px;margin:0;padding:0}
.nlkb__row{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:50px;padding:8px 16px;background:#fff;border:1px solid var(--k-line);border-radius:12px}
.nlkb__row dt{font:400 15.5px/1.3 'Assistant',sans-serif;color:var(--k-mute)}
.nlkb__row dd{margin:0;font:700 15.5px/1.3 'Assistant',sans-serif;color:var(--k-ink);text-align:end}
.nlkb__chk{display:flex;align-items:center;gap:14px;min-height:60px;padding:8px 16px;background:#fff;border:1px solid var(--k-line);border-radius:12px;cursor:pointer;font:600 16.5px/1.3 'Assistant',sans-serif;color:var(--k-ink)}
.nlkb__chk input{position:absolute;opacity:0;width:1px;height:1px}
.nlkb__box{flex:none;width:40px;height:40px;border-radius:9px;border:2px solid var(--k-sea);background:#fff;display:grid;place-items:center;color:#fff;font:700 20px/1 Arial,sans-serif}
.nlkb__chk input:checked+.nlkb__box{background:var(--k-sea)}
.nlkb__chk input:checked+.nlkb__box::after{content:'\\2713'}
.nlkb__chk input:focus-visible+.nlkb__box{outline:3px solid var(--k-glass);outline-offset:2px}
.nlkb__chk--consent{min-height:44px;padding:4px 0;background:none;border:0;font-weight:400;font-size:15.5px;align-items:flex-start}
.nlkb__note{margin:0!important;font:400 14px/1.5 'Assistant',sans-serif!important;color:var(--k-mute)!important}
.nlkb__note a{color:var(--k-sea)!important;font-weight:700;text-decoration:underline;text-underline-offset:3px}
.nlkb__f{display:block}
.nlkb__f span{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.nlkb__f input{box-sizing:border-box;width:100%;min-height:58px;padding:0 18px;border:1.5px solid var(--k-line)!important;border-radius:12px!important;background:#fff!important;font:400 17px/1 'Assistant',sans-serif;color:var(--k-ink);box-shadow:none}
.nlkb__f input:focus{outline:2px solid var(--k-sea);outline-offset:1px;border-color:var(--k-sea)}
.nlkb[dir=rtl] .nlkb__f input[type=tel]{text-align:right}
.nlkb__err{margin:0!important;padding:10px 12px;border-radius:10px;background:#fdecea;color:#8a1c12!important;font:600 14.5px/1.4 'Assistant',sans-serif!important}
.nlkb__err[hidden]{display:none}
.nlkb__two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.nlkb .nlkb__ghost{display:flex;align-items:center;justify-content:center;min-height:56px;padding:0 12px;border-radius:999px!important;border:1.5px solid var(--k-sea);background:#fff;color:var(--k-sea)!important;font:700 16.5px/1.1 'Assistant',sans-serif;text-decoration:none!important;cursor:pointer;text-align:center}
.nlkb .nlkb__ghost--wa{border-color:var(--k-wa);color:var(--k-wa)!important}
.nlkb__ref{padding:16px;background:#fff;border:1px solid var(--k-line);border-radius:16px;display:flex;flex-direction:column;gap:6px}
.nlkb__ref span{font:400 15px/1.3 'Assistant',sans-serif;color:var(--k-mute)}
.nlkb__ref b{font:700 26px/1.2 'Assistant',sans-serif;letter-spacing:.04em;color:var(--k-ink);direction:ltr;unicode-bidi:isolate;text-align:start}
.nlkb .nlkb__doc{display:flex;align-items:center;justify-content:center;min-height:56px;margin-top:8px;padding:0 16px;border:0;border-radius:999px!important;background:#e3eef2;color:var(--k-sea)!important;font:700 17px/1.2 'Assistant',sans-serif;text-decoration:none!important;cursor:pointer;text-align:center}
.nlkb__tl{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:14px}
.nlkb__tl li{display:flex;align-items:flex-start;gap:14px}
.nlkb__tl i{flex:none;width:36px;height:36px;border-radius:50%;border:2px solid var(--k-sea);box-sizing:border-box;display:grid;place-items:center;color:#fff;font:700 18px/1 Arial,sans-serif;font-style:normal}
.nlkb__tl li.is-on i{background:var(--k-sea)}
.nlkb__tl b{display:block;font:700 17px/1.3 'Assistant',sans-serif;color:var(--k-ink)}
.nlkb__tl span{display:block;font:400 14.5px/1.4 'Assistant',sans-serif;color:var(--k-mute)}
.nlkb__foot{flex:none;padding:12px 16px calc(10px + env(safe-area-inset-bottom,0px));background:var(--k-paper);border-top:1px solid #dde4e8;display:flex;flex-direction:column;align-items:stretch;gap:6px}
.nlkb .nlkb__go{min-height:58px;padding:0 18px;border:0;border-radius:999px!important;background:var(--k-sea);color:#fff!important;font:700 19px/1.1 'Assistant',sans-serif;cursor:pointer;display:flex;align-items:center;justify-content:center;text-decoration:none!important}
.nlkb .nlkb__go[disabled]{opacity:.7;cursor:progress}
.nlkb .nlkb__go--2{background:#e3eaee;color:var(--k-ink)!important}
.nlkb__fn{margin:0!important;text-align:center;font:400 14px/1.4 'Assistant',sans-serif!important;color:var(--k-mute)!important}
.nlkb button:focus-visible,.nlkb a:focus-visible{outline:3px solid var(--k-glass);outline-offset:2px}
.nlkb-pulse{animation:nlkbPulse 1.6s ease-out infinite}
@keyframes nlkbPulse{0%{box-shadow:0 0 0 0 rgba(127,211,230,.9)}70%{box-shadow:0 0 0 14px rgba(127,211,230,0)}100%{box-shadow:0 0 0 0 rgba(127,211,230,0)}}
@media (prefers-reduced-motion:reduce){.nlkb-pulse{animation:none!important;box-shadow:0 0 0 3px #7fd3e6,0 0 0 5px rgba(13,33,41,.55)!important}}
@media (max-width:380px){:root body .nlkb h2.nlkb__t{font-size:26px!important}.nlkb__apt img{width:80px;height:62px}}`;
  document.head.appendChild(s);
}

/* ---------------------------------------------------------------- the request, from My selection */
function fromSelection(state, cfg) {
  const u = (state && state.unit) || null, ok = !!(u && /^[ABC]$/.test(String(u.tower || '')) && Number(u.floor) > 0);
  const b = ok && u.bearing != null && isFinite(u.bearing) ? Math.round(norm(u.bearing)) : null;
  const team = (state && state.team) || {};
  const style = state && state.style && state.style !== 'bare' ? String(state.style) : '';
  return {
    ok, tower: ok ? u.tower : '', floor: ok ? Number(u.floor) : 0, bearing: b,
    id: ok ? u.tower + Number(u.floor) + (b != null ? '-' + b : '') : '', // B20-276: the page's own #dira= id
    style, finish: style || 'std',
    extras: TEAM.reduce((o, [x, k]) => { o[x] = !!team[k]; return o; }, {}),
    slug: String((cfg && cfg.slug) || 'hamedina').replace(/-(en|fr|ru|ar)$/, ''),
    wa: (cfg && cfg.wa) || ((window.__nlCockpitCfg || {}).wa) || '',
  };
}
const aptTitle = () => (F.ok ? (F.bearing != null ? t('kb_apt_title', { tower: F.tower, floor: F.floor, dir: dirNoun(F.bearing) }) : t('kb_apt_title_nodir', { tower: F.tower, floor: F.floor })) : t('kb_apt_none'));
const exampleLabel = () => t('bk_unit_example', { unit: t('tower_n', { tower: F.tower }) });
function waHref() {
  if (!F.wa) return '';
  const v = { floor: F.floor, tower: F.tower, dir: F.bearing != null ? dirTo(F.bearing) : '', dirTo: F.bearing != null ? dirTo(F.bearing) : '' };
  v.apt = t('sr_wa_apt', v);
  return 'https://wa.me/' + String(F.wa).replace(/\D/g, '') + '?text=' + encodeURIComponent(t('sr_wa_text', v));
}
function picture() { // the tower picture the showroom shows now, else the three towers from the air
  const p = document.querySelector('.nlsr .nlsr-pic');
  if (p && p.currentSrc && /\/turn\//.test(p.currentSrc)) return p.currentSrc;
  const c = window.__nlJourneyCfg || {};
  return c.base ? c.base + 'aerial-tall-800.webp' + (c.ver ? '?ver=' + c.ver : '') : '';
}

/* ---------------------------------------------------------------- the screens */
function shell(step, back, body, foot) {
  return `<div class="nlkb__scrim" data-kb="close"></div>
  <div class="nlkb__panel" role="dialog" aria-modal="true" aria-labelledby="nlkb-t">
    <div class="nlkb__bar"><button type="button" class="nlkb__back" data-kb="${back[0]}">${esc(back[1])}</button><span class="nlkb__cnt">${esc(t('kb_step', { n: step }))}</span></div>
    <div class="nlkb__body">${body}</div>
    <div class="nlkb__foot">${foot}</div>
  </div>`;
}
function aptCard() {
  const src = picture();
  return `<div class="nlkb__apt">${src ? `<img src="${esc(src)}" alt="${esc(t('sim'))}" decoding="async">` : ''}<div><b>${esc(aptTitle())}</b><span>${esc(F.ok ? t('kb_apt_sub') : t('kb_apt_none_sub'))}</span></div></div>`;
}
function head(title) { return `<h2 class="nlkb__t" id="nlkb-t" tabindex="-1">${esc(title)}</h2><p class="nlkb__sub">${esc(t('kb_sub'))}</p>${aptCard()}`; }
function nowRow() {
  const wa = waHref();
  return `<div class="nlkb__two"><button type="button" class="nlkb__ghost" data-kb="video">${esc(t('kb_video'))}</button>${wa ? `<a class="nlkb__ghost nlkb__ghost--wa" href="${esc(wa)}" target="_blank" rel="noopener" data-kb="wa">${esc(t('kb_wa'))}</a>` : ''}</div>`;
}

function step1() {
  if (!F.ok) {
    return shell(1, ['basket', t('kb_back_sel')], head(t('kb_title')),
      `<button type="button" class="nlkb__go nlkb-pulse" data-kb="stage">${esc(t('bk_pick_floor'))}</button>`);
  }
  const rows = [[t('kb_row_apt'), F.bearing != null ? t('kb_row_apt_v', { tower: F.tower, floor: F.floor, dirTo: dirTo(F.bearing) }) : t('kb_apt_title_nodir', { tower: F.tower, floor: F.floor })],
    [t('kb_row_finish'), F.style ? t('style_' + F.style) || F.style : t('bk_style_bare')],
    [t('kb_row_price'), t('kb_row_price_v')]];
  if (F.style) rows.push([t('kb_row_up'), t('kb_row_up_v')]);
  const body = head(t('kb_title')) +
    `<h3 class="nlkb__h">${esc(t('kb_chose'))}</h3><dl class="nlkb__rows">${rows.map(([a, b]) => `<div class="nlkb__row"><dt>${esc(a)}</dt><dd>${esc(b)}</dd></div>`).join('')}</dl>
    <h3 class="nlkb__h" id="nlkb-team">${esc(t('kb_team'))}</h3>
    <div class="nlkb__rows" role="group" aria-labelledby="nlkb-team">${TEAM.map(([x]) => `<label class="nlkb__chk"><input type="checkbox" data-x="${x}"${F.extras[x] ? ' checked' : ''}><span class="nlkb__box" aria-hidden="true"></span><span>${esc(t('kb_x_' + x))}</span></label>`).join('')}</div>
    <p class="nlkb__note">${esc(t('kb_est'))}</p>`;
  return shell(1, ['basket', t('kb_back_sel')], body,
    `<button type="button" class="nlkb__go nlkb-pulse" data-kb="next">${esc(t('kb_cont'))}</button><p class="nlkb__fn">${esc(t('kb_cont_note'))}</p>`);
}

function step2() {
  const pp = [...document.querySelectorAll('a[href*="privacy"],a[href*="%d7%a4%d7%a8%d7%98%d7%99%d7%95%d7%aa"]')].find((a) => /privacy|%d7%a4%d7%a8%d7%98%d7%99%d7%95%d7%aa/i.test(a.getAttribute('href') || ''));
  const priv = esc(t('kb_privacy')) + ' ' + (pp ? `<a href="${esc(pp.href)}" target="_blank" rel="noopener">${esc(t('kb_privacy_link'))}</a>` : esc(t('kb_privacy_foot')));
  const body = head(t('kb_t2')) +
    `<h3 class="nlkb__h">${esc(t('kb_where'))}</h3>
    <label class="nlkb__f"><span>${esc(t('kb_name'))}</span><input type="text" id="nlkb-name" autocomplete="given-name" placeholder="${esc(t('kb_name'))}" value="${esc(F.name || '')}" maxlength="60"></label>
    <label class="nlkb__f"><span>${esc(t('kb_phone'))}</span><input type="tel" id="nlkb-phone" autocomplete="tel" inputmode="tel" dir="ltr" placeholder="${esc(t('kb_phone'))}" value="${esc(F.phone || '')}" maxlength="20"></label>
    <label class="nlkb__chk nlkb__chk--consent"><input type="checkbox" id="nlkb-consent"${F.consent ? ' checked' : ''}><span class="nlkb__box" aria-hidden="true"></span><span>${esc(t('kb_consent'))}</span></label>
    <p class="nlkb__note">${priv}</p>
    <p class="nlkb__err" id="nlkb-err" role="alert" hidden></p>
    <h3 class="nlkb__h">${esc(t('kb_now'))}</h3>${nowRow()}`;
  return shell(2, ['back', t('kb_back')], body,
    `<button type="button" class="nlkb__go nlkb-pulse" data-kb="send" id="nlkb-send"${F.busy ? ' disabled' : ''}>${esc(F.busy ? t('kb_sending') : t('kb_send'))}</button><p class="nlkb__fn">${esc(t('kb_send_note'))}</p>`);
}

function step3() {
  let box;
  if (F.doc === 'ready') {
    box = `<div class="nlkb__ref"><span>${esc(t('kb_ref'))}</span><b>${esc(F.ref)}</b><a class="nlkb__doc${F.docOpened ? '' : ' nlkb-pulse'}" href="${esc(F.url)}" target="_blank" rel="noopener" data-kb="doc">${esc(t('kb_doc'))}</a></div>`;
  } else if (F.doc === 'failed') {
    box = `<div class="nlkb__ref"><p class="nlkb__err" role="alert">${esc(t('kb_doc_fail'))}</p><button type="button" class="nlkb__doc nlkb-pulse" data-kb="docretry"${F.busy ? ' disabled' : ''}>${esc(F.busy ? t('kb_sending') : t('kb_doc_retry'))}</button></div>`;
  } else {
    box = `<div class="nlkb__ref" aria-live="polite"><span>${esc(t('kb_doc_wait'))}</span></div>`;
  }
  const tl = [['kb_tl1', 'kb_tl1_s', true], ['kb_tl2', 'kb_tl2_s', false], ['kb_tl3', 'kb_tl3_s', false]];
  const body = head(t('kb_t3')) + box +
    `<h3 class="nlkb__h">${esc(t('kb_next'))}</h3>
    <ol class="nlkb__tl">${tl.map(([a, b, on]) => `<li${on ? ' class="is-on"' : ''}><i aria-hidden="true">${on ? '✓' : ''}</i><div><b>${esc(t(a))}</b><span>${esc(t(b))}</span></div></li>`).join('')}</ol>
    ${nowRow()}`;
  /* PAYMENT (later, on Ben's decision): a reservation step belongs here, between the timeline and "Back to the apartment":
     what is paid, how much, and who holds the money (the project's supervised account, against a Sale Law guarantee) are
     Ben's decisions. Nothing is shown until then. */
  return shell(3, ['home', t('kb_back_apt')], body, `<button type="button" class="nlkb__go nlkb__go--2" data-kb="home">${esc(t('kb_home'))}</button>`);
}

function render(focusTitle) {
  css();
  if (!root) {
    root = document.createElement('div'); root.className = 'nlkb'; root.hidden = true;
    root.addEventListener('click', onClick);
    root.addEventListener('change', (e) => { const x = e.target.closest('[data-x]'); if (x) { F.extras[x.dataset.x] = x.checked; ga('offer_team', { kind: x.dataset.x, on: x.checked }); } });
    root.addEventListener('input', () => { const er = root.querySelector('#nlkb-err'); if (er && !er.hidden) er.hidden = true; }); // the line goes once the buyer acts on it
    document.body.appendChild(root);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && root && !root.hidden) close(); });
  }
  root.dir = I.dir(L); root.lang = L;
  if (F.step === 2) keep();
  root.innerHTML = F.step === 1 ? step1() : F.step === 2 ? step2() : step3();
  root.hidden = false; document.documentElement.classList.add('nlkb-open');
  if (focusTitle) { const h = root.querySelector('#nlkb-t'); if (h) h.focus({ preventScroll: true }); root.querySelector('.nlkb__body').scrollTop = 0; }
}
function keep() { // what was typed survives a re-render
  const n = root && root.querySelector('#nlkb-name'), p = root && root.querySelector('#nlkb-phone'), c = root && root.querySelector('#nlkb-consent');
  if (n) F.name = n.value; if (p) F.phone = p.value; if (c) F.consent = c.checked;
}
function go(step) { if (F.step === 2) keep(); F.step = step; render(true); ga('offer_step', { step }); }
function close() {
  if (!root || root.hidden) return;
  if (F && F.step === 2) keep();
  root.hidden = true; document.documentElement.classList.remove('nlkb-open');
  if (opener && opener.isConnected && opener.focus) opener.focus();
}
function toApartment() {
  close();
  const s = document.getElementById('nlsr') || document.getElementById('nlps');
  if (s) s.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth', block: 'start' });
}

/* ---------------------------------------------------------------- sending: buyflow.js's two calls */
const post = (path, body) => fetch(REST + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify(body) })
  .then((r) => r.json().catch(() => ({})).then((j) => (r.ok ? j : Object.assign({ ok: false }, j))));
const extrasList = () => TEAM.map(([x]) => x).filter((x) => F.extras[x]);
function err(msg) { const e = root.querySelector('#nlkb-err'); if (e) { e.textContent = msg; e.hidden = false; } }
function send() {
  if (F.busy) return;
  keep();
  const name = String(F.name || '').trim(), phone = String(F.phone || '').trim();
  if (name.length < 2) return err(t('kb_err_name'));
  if (phone.replace(/\D/g, '').length < 9) return err(t('kb_err_phone'));
  if (!F.consent) return err(t('kb_err_consent'));
  F.busy = true; render();
  const extras = extrasList();
  // the lead, in buyflow.js's shape (source and message "rfp-v1"); the consent, its sentence and the unit as the endpoint's own fields
  const lead = {
    name, phone, source: 'rfp-v1', context: F.slug + ' ' + F.id,
    message: JSON.stringify({ kind: 'rfp-v1', project: F.slug, unit: F.id, label: exampleLabel(), floor: F.floor, rooms: '', sqm: '', finish: F.finish, extras, lang: L, url: location.href, studio: null }),
    consent: true, consent_text: t('kb_consent'), project_slug: F.slug, unit: F.id, floor: F.floor, building: F.tower,
  };
  if (F.bearing != null) lead.view_bearing = F.bearing;
  post('lead', lead).then((d) => {
    F.busy = false;
    if (!d || !d.ok) { render(); err(t('kb_err_send')); return; }
    F.leadId = d.lead_id || 0; F.name = name;
    try { sessionStorage.setItem(SK, JSON.stringify({ id: F.id, leadId: F.leadId, name })); } catch (e) { /* private mode */ }
    ga('offer_sent', { tower: F.tower, floor: F.floor, extras: extras.length, finish: F.finish });
    F.doc = 'wait'; F.step = 3; render(true);
    makeDoc();
  }).catch(() => { F.busy = false; render(); err(t('kb_err_send')); });
}
function makeDoc() { // the request document (inc/rfp.php); a retry makes the document only, never a second lead
  F.busy = true;
  post('rfp', { project: F.slug, unit: F.id, finish: F.finish, extras: extrasList(), lang: L, name: F.name, lead_id: F.leadId })
    .then((d) => {
      F.busy = false;
      const m = d && d.ok && d.url ? /\/rfp\/([a-z0-9]{16,32})/i.exec(d.url) : null;
      if (m) { F.doc = 'ready'; F.url = d.url; F.ref = d.ref || 'RFP-' + m[1].slice(0, 8).toUpperCase(); }
      else F.doc = 'failed';
      try { const s = JSON.parse(sessionStorage.getItem(SK) || 'null'); if (s && F.doc === 'ready') sessionStorage.setItem(SK, JSON.stringify(Object.assign(s, { url: F.url, ref: F.ref }))); } catch (e) { /* none */ }
      if (root && !root.hidden && F.step === 3) render();
    })
    .catch(() => { F.busy = false; F.doc = 'failed'; if (root && !root.hidden && F.step === 3) render(); });
}

function onClick(e) {
  const n = e.target.closest('[data-kb]'); if (!n) return;
  const a = n.dataset.kb;
  if (a === 'close') return close();
  if (a === 'basket') { close(); if (window.__nlBasket) window.__nlBasket.open(opener); return; }
  if (a === 'stage') { toApartment(); return; }
  if (a === 'next') return go(2);
  if (a === 'back') return go(1);
  if (a === 'send') return send();
  if (a === 'docretry') { if (!F.busy) { F.doc = 'wait'; render(); makeDoc(); } return; }
  if (a === 'doc') { F.docOpened = true; n.classList.remove('nlkb-pulse'); ga('offer_doc_open', {}); return; }
  if (a === 'home') { ga('offer_home', {}); return toApartment(); }
  if (a === 'wa') { ga('offer_wa', { step: F.step }); return; }
  if (a === 'video') { // the showroom's own video button (a room now, or the booking band): the same tap as under the tower
    ga('offer_video', { step: F.step });
    const v = document.querySelector('.nlsr a.nlsr-call') || document.querySelector('.nlck-call') || document.querySelector('a[data-nlps-ev="hero-video"]');
    close(); if (v) v.click(); else { const s = document.getElementById('nlsch'); if (s) s.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth' }); }
  }
}

/** Open the offer from My selection. state: window.__nlBasket.state; cfg: the basket's config; from: the button (focus returns to it). */
export function open({ state, cfg, from } = {}) {
  const next = fromSelection(state, cfg);
  opener = from || document.activeElement;
  let sent = null; try { sent = JSON.parse(sessionStorage.getItem(SK) || 'null'); } catch (e) { /* none */ }
  if (F && F.step === 3 && F.id === next.id && next.ok) { render(true); return; } // this apartment's request is already on its way
  F = Object.assign(next, { step: 1, busy: false, name: (F && F.name) || '', phone: (F && F.phone) || '', consent: false, doc: null });
  if (sent && sent.id === F.id && F.ok) { // sent earlier in this tab: the confirmation, never a second lead
    Object.assign(F, { step: 3, leadId: sent.leadId, name: sent.name, doc: sent.url ? 'ready' : 'failed', url: sent.url || '', ref: sent.ref || '' });
  }
  render(true);
  ga('offer_open', { tower: F.tower, floor: F.floor, from_sent: F.step === 3 });
}
export default { open };
