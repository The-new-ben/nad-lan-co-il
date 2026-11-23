// HAD-803 round 2 (23.11.2026, LOCAL): dresses the lab as the Claude Design board v2 (LabV2 and Phone artboards). It only MOVES and
// re-dresses the page's own elements (their ids, handlers and numbers stay with index.html and climate.js): a bottom instrument dock
// with the three round modes, the clock, play, the quick dates and a day timeline coloured from sunrise to sunset; a collapsible
// answers panel where each answer opens with one big figure; the title as a small glass card.
import { solar, ilToUtc } from './climate.js';
const $ = (id) => document.getElementById(id), Y = 2026, mq = matchMedia('(max-width:899px)');
const I = {
  sun: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.4M12 19.1v2.4M2.5 12h2.4M19.1 12h2.4M5.3 5.3l1.7 1.7M17 17l1.7 1.7M5.3 18.7L7 17M17 7l1.7-1.7"/></svg>',
  wind: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M3 8.5h11.5a2.8 2.8 0 1 0-2.8-2.8"/><path d="M3 12.5h15.5a2.8 2.8 0 1 1-2.8 2.8"/><path d="M3 16.5h7"/></svg>',
  rain: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M7 14.5a4 4 0 0 1-.4-8 5.5 5.5 0 0 1 10.6 1.5 3.3 3.3 0 0 1 .3 6.5Z"/><path d="M9 17.5l-1 2.5M13 17.5l-1 2.5M17 17.5l-1 2.5"/></svg>',
  play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg>',
  pause: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.5 5.5h3v13h-3zM13.5 5.5h3v13h-3z" fill="currentColor"/></svg>',
  right: '<svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>',
  left: '<svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg>',
  north: '<svg class="north" viewBox="0 0 44 44" role="img" aria-label="חץ הצפון לפי תוכנית המכר, 11 מעלות"><circle cx="22" cy="22" r="20" fill="none" stroke="rgba(255,255,255,.28)" stroke-width="1"/><g transform="rotate(11 22 22)"><path d="M22 6 L27 24 L22 21 L17 24 Z" fill="#EEF2F5"/><path d="M22 38 L22 26" stroke="rgba(255,255,255,.45)" stroke-width="1"/></g></svg>',
};
document.body.classList.add('v2', 'm-sun'); if (mq.matches) document.body.classList.add('panel-closed');
const header = document.querySelector('header'), stage = $('stage'), aside = document.querySelector('aside'), tabs = document.querySelector('.tabs');
header.querySelector('.ttl').insertAdjacentHTML('afterend', I.north);
// ---- the modes: round buttons with the word under them ----
const WORD = { sun: 'שמש', wind: 'רוח', rain: 'גשם' };
for (const b of [...tabs.querySelectorAll('button')]) {
  const m = b.dataset.m, wrap = document.createElement('div'); wrap.className = 'mb';
  b.innerHTML = I[m]; b.setAttribute('aria-label', WORD[m]); b.replaceWith(wrap); wrap.append(b); wrap.insertAdjacentHTML('beforeend', `<span>${WORD[m]}</span>`);
}
// ---- the dock ----
const dock = document.createElement('div'); dock.id = 'dock'; dock.setAttribute('aria-label', 'שעה, יום ומה רואים');
dock.innerHTML = `<span class="sep"></span><div class="row1"><div class="clock"><span class="slot-time"></span><span class="sub"><span class="slot-date"></span> · <span id="v2preset"></span></span></div><span class="slot-play"></span></div>
<div class="tlcol"><div class="quick"><div class="slot-marks" data-only="sun wind"></div><div class="slot-wind" data-only="wind"></div>
<div class="phases" data-only="rain" style="gap:8px;align-items:center"><span style="font-size:14px;color:#A7B3BE">שלב בסערה</span><button class="phase" data-s="0.12">דרום־מערב</button><button class="phase" data-s="0.5">מערב</button><button class="phase" data-s="0.92">צפון־מערב</button></div>
<span class="legend"><i></i>זריחה ושקיעה</span></div>
<div class="bar48"><div class="grad"></div><span class="mk rise"></span><span class="mk set"></span><span class="slot-min"></span></div><div class="hours"></div>
<div class="slot-storm" data-only="rain" style="flex-direction:column;gap:2px"></div></div>`;
stage.append(dock);
dock.prepend(tabs);
tabs.insertAdjacentHTML('beforeend', `<button class="sheetbtn" type="button">${I.left}<span>תשובות קצרות</span></button>`);
const put = (sel, el) => { if (el) dock.querySelector(sel).replaceWith(el); };
put('.slot-time', $('timeL')); put('.slot-date', $('dateL')); put('.slot-play', $('play')); put('.slot-min', $('min'));
put('.slot-marks', $('markChips')); $('markChips').dataset.only = 'sun wind';
put('.slot-wind', $('windChips')); $('windChips').dataset.only = 'wind';
{ const st = $('storm'), scale = st && st.nextElementSibling; const slot = dock.querySelector('.slot-storm'); if (st) { slot.append(st); if (scale) slot.append(scale); } }
// in wind mode the quick row shows the wind cases; the dates move to the panel's date slider
$('markChips').dataset.only = 'sun';
// play: an icon, its words become the label
const play = $('play');
const setPlay = () => { const t = play.textContent.trim(); if (t) { const stop = /עצירה/.test(t); play.setAttribute('aria-label', stop ? 'עצירה' : 'הפעלת היום'); play.innerHTML = stop ? I.pause : I.play; } };
new MutationObserver(setPlay).observe(play, { childList: true, characterData: true, subtree: true }); setPlay();
dock.querySelector('.phases').addEventListener('click', (ev) => { const b = ev.target.closest('.phase'); if (!b) return; const st = $('storm'); st.value = b.dataset.s; st.dispatchEvent(new Event('input', { bubbles: true })); });
// ---- the answers panel ----
aside.insertAdjacentHTML('afterbegin', `<div class="panelbar"><h2>תשובות קצרות על הדירה</h2><button class="rb" id="v2close" type="button" aria-label="סגירת התשובות">${I.right}</button></div>`);
stage.insertAdjacentHTML('beforeend', `<button class="openpanel" id="v2open" type="button">${I.left}<span>תשובות קצרות</span><span class="mono" style="color:#A7B3BE">6</span></button>`);
stage.append(header);
const toggle = () => document.body.classList.toggle('panel-closed');
$('v2close').onclick = toggle; $('v2open').onclick = toggle; dock.querySelector('.sheetbtn').onclick = toggle;
// each answer opens with one big figure, taken from the answer itself
function bigOf(card) {
  const sp = card.querySelector('span'); if (!sp) return null;
  const em = sp.querySelector('em'), txt = sp.textContent.trim(), id = card.dataset.c;
  if (id === 'cook') { const part = txt.split('.')[0]; return { w: /פנימה/.test(part) ? 'פנימה' : /החוצה/.test(part) ? 'החוצה' : 'לאורך', u: 'בצהרי הקיץ' }; }
  const src = em ? em.textContent.trim() : txt.split(/[.:]/)[0].trim();
  const m = src.match(/^(\D*?)(\d+(?:\.\d+)?)(.*)$/);
  if (m) return { n: m[2], u: (m[1] + ' ' + m[3]).replace(/\s+/g, ' ').trim() };
  return { w: src.length > 14 ? src.split(' ').slice(0, 2).join(' ') : src, u: '' };
}
function bigs() {
  for (const c of document.querySelectorAll('#cards .card')) {
    if (c.querySelector('.big')) continue; const b = bigOf(c); if (!b) continue;
    c.querySelector('b').insertAdjacentHTML('afterend', `<div class="big">${b.n ? `<i>${b.n}</i>` : `<i class="word">${b.w}</i>`}<u>${b.u}</u></div>`);
  }
  const n = document.querySelectorAll('#cards .card').length; const o = $('v2open'); if (o && n) o.lastElementChild.textContent = n;
}
new MutationObserver(bigs).observe($('cards'), { childList: true }); bigs();
// close the sheet on a phone after an answer is picked
$('cards').addEventListener('click', () => { if (mq.matches) document.body.classList.add('panel-closed'); });
// ---- the day timeline: coloured from sunrise to sunset of the chosen day, with the two marks ----
const MARKS = { '3-20': 'אביב', '6-21': 'היום הארוך', '9-23': 'סתיו', '12-21': 'היום הקצר' };
const hours = dock.querySelector('.hours'), MIN0 = 300, MIN1 = 1260, pos = (t) => ((t - MIN0) / (MIN1 - MIN0)) * 100;
hours.innerHTML = [6, 9, 12, 15, 18, 21].map((h) => `<span style="right:${pos(h * 60).toFixed(2)}%">${String(h).padStart(2, '0')}</span>`).join('');
let lastDoy = -1, lastMode = '';
function tick() {
  const doy = +$('doy').value;
  if (doy !== lastDoy) {
    lastDoy = doy; const t = new Date(Date.UTC(Y, 0, doy)), m = t.getUTCMonth() + 1, d = t.getUTCDate();
    let rise = 330, set = 1170;
    for (let x = 240; x <= 1290; x += 2) { const a = solar(ilToUtc(Y, m, d, x)).alt; if (a > -0.83 && rise === 330 && x < 720) rise = x; if (x > 720 && a < -0.83) { set = x; break; } }
    const c = (x, col) => `${col} ${Math.max(0, Math.min(100, pos(x))).toFixed(2)}%`;
    dock.querySelector('.grad').style.background = `linear-gradient(to left, ${[c(MIN0, '#18242F'), c(rise - 50, '#18242F'), c(rise, '#4A6377'), c(rise + 70, '#A8C2D3'), c((rise + set) / 2, '#DDE8EF'), c(set - 70, '#A8C2D3'), c(set, '#4A6377'), c(set + 50, '#18242F'), c(MIN1, '#121B24')].join(', ')})`;
    dock.querySelector('.mk.rise').style.right = `calc(${pos(rise).toFixed(2)}% - 1px)`; dock.querySelector('.mk.set').style.right = `calc(${pos(set).toFixed(2)}% - 1px)`;
  }
  const pressed = tabs.querySelector('button[aria-pressed=true]'), mode = pressed ? pressed.dataset.m : 'sun';
  if (mode !== lastMode) { lastMode = mode; document.body.classList.remove('m-sun', 'm-wind', 'm-rain'); document.body.classList.add('m-' + mode); }
  if (mode === 'rain') { const v = +$('storm').value; for (const b of dock.querySelectorAll('.phase')) b.setAttribute('aria-pressed', Math.abs(v - +b.dataset.s) < 0.2); }
  const pre = $('v2preset'), t0 = new Date(Date.UTC(Y, 0, doy)), mk = MARKS[(t0.getUTCMonth() + 1) + '-' + t0.getUTCDate()], r = document.querySelector('#ribbon .top span');
  const want = mk || (r ? r.textContent : ''); if (pre.textContent !== want) pre.textContent = want; // the day's name, or the hours of sun in the room you stand in
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
