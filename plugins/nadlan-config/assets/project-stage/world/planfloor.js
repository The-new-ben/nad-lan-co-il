/* Kikar HaMedina: the floor's four apartments as a clean, tappable plan (HAD-712, Ben 11.11.2026 night: "the plan must blink so
 * people understand they can tap it"). A drawing, not a published plan: the tower's plate (a rounded square), the core, the party
 * walls on the diagonals (4 apartments a floor: 453 apartments over 117 floors), one apartment on each side of the plate, and the
 * north arrow. The plate turns 1.25 degrees a floor (the twist), so the drawing turns with the chosen floor and each apartment is
 * named by the direction its side really faces on that floor (the same 8 words the showroom uses).
 *
 *   const p = planFloor(host, { lang, plate: deg, pick: (side) => {}, names: (bearing) => 'north-east', title, hint });
 *   p.set({ plate, side, pulse });  p.destroy();     side = 0..3, the side facing plate + side*90 degrees */
const NS = 'http://www.w3.org/2000/svg';
const T = {
  he: { aria: 'תוכנית הקומה: ארבע דירות, אחת בכל צד. הקישו על דירה.', north: 'צ', core: 'ליבה', ill: 'שרטוט להמחשה, לא תוכנית רשמית' },
  en: { aria: 'Floor plan: four apartments, one on each side. Tap an apartment.', north: 'N', core: 'core', ill: 'Illustrative drawing, not an official plan' },
  fr: { aria: 'Plan de l’étage : quatre appartements, un sur chaque côté. Touchez un appartement.', north: 'N', core: 'noyau', ill: 'Dessin indicatif, pas un plan officiel' },
};
let CSS_DONE = false;
function css() {
  if (CSS_DONE) return; CSS_DONE = true;
  const s = document.createElement('style'); s.id = 'nlpf-css';
  s.textContent = '.nlpf{position:relative;width:100%;max-width:340px;margin:0 auto}.nlpf svg{display:block;width:100%;height:auto}'
    + '.nlpf__apt{cursor:pointer;transition:fill .2s}.nlpf__apt:focus{outline:none}.nlpf__apt:focus-visible{stroke:#14212b;stroke-width:3}'
    + '@keyframes nlpfPulse{0%,100%{stroke-opacity:1;stroke-width:3}50%{stroke-opacity:.35;stroke-width:7}}'
    + '.nlpf__apt--pulse{animation:nlpfPulse 1.4s ease-in-out infinite}'
    + '@media (prefers-reduced-motion:reduce){.nlpf__apt--pulse{animation:none;stroke-width:4}}'
    + '.nlpf__ill{font:400 11.5px/1.3 Assistant,Heebo,system-ui,sans-serif;color:#4a5a66;text-align:center;margin-top:4px}';
  document.head.appendChild(s);
}
const el = (n, a) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); return e; };

export function planFloor(host, opt) {
  css();
  const L = T[opt.lang] || T.he;
  const wrap = document.createElement('div'); wrap.className = 'nlpf';
  const svg = el('svg', { viewBox: '0 0 300 300', role: 'group', 'aria-label': L.aria });
  wrap.appendChild(svg);
  const ill = document.createElement('div'); ill.className = 'nlpf__ill'; ill.textContent = L.ill; wrap.appendChild(ill);
  host.appendChild(wrap);
  let st = { plate: opt.plate || 0, side: null, pulse: true };

  function draw() {
    svg.textContent = '';
    const c = 150, R = 118, core = 34;
    const g = el('g', { transform: `rotate(${st.plate} ${c} ${c})` }); // the plate turned to its true bearing (north is up)
    // the four apartments: one quarter each, between the diagonal party walls; side 0 faces plate+0 (up before turning)
    for (let s = 0; s < 4; s++) {
      const a0 = (s * 90 - 45 - 90) * Math.PI / 180, a1 = (s * 90 + 45 - 90) * Math.PI / 180; // screen angles (0 = east)
      const p = (a, r) => `${c + r * Math.cos(a)},${c + r * Math.sin(a)}`;
      const d = `M${p(a0, core)} L${p(a0, R)} A${R} ${R} 0 0 1 ${p(a1, R)} L${p(a1, core)} A${core} ${core} 0 0 0 ${p(a0, core)} Z`;
      const on = st.side === s;
      const apt = el('path', { d, class: 'nlpf__apt' + (st.pulse && st.side == null ? ' nlpf__apt--pulse' : ''), tabindex: '0', role: 'button',
        fill: on ? '#7fd3e6' : '#eaf2f5', stroke: on ? '#2f6f86' : '#7fd3e6', 'stroke-width': on ? 3 : 2 });
      const bearing = (st.plate + s * 90 + 360) % 360;
      const name = opt.names ? opt.names(bearing) : String(Math.round(bearing));
      apt.setAttribute('aria-label', name); apt.setAttribute('aria-pressed', on ? 'true' : 'false');
      const go = () => { st.side = s; st.pulse = false; draw(); if (opt.pick) opt.pick(s, bearing); };
      apt.addEventListener('click', go);
      apt.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
      g.appendChild(apt);
      // the label stays upright: placed in the turned frame, drawn unturned
      const am = (s * 90 - 90) * Math.PI / 180, lr = (R + core) / 2;
      const lx = c + lr * Math.cos(am), ly = c + lr * Math.sin(am);
      const t = el('text', { x: lx, y: ly, 'text-anchor': 'middle', 'dominant-baseline': 'middle', transform: `rotate(${-st.plate} ${lx} ${ly})`,
        fill: '#14212b', 'font-size': 15, 'font-weight': 700, 'font-family': 'Assistant,Heebo,system-ui,sans-serif', 'pointer-events': 'none' });
      t.textContent = name; g.appendChild(t);
    }
    g.appendChild(el('circle', { cx: c, cy: c, r: core, fill: '#14212b' }));
    const ct = el('text', { x: c, y: c, 'text-anchor': 'middle', 'dominant-baseline': 'middle', transform: `rotate(${-st.plate} ${c} ${c})`,
      fill: '#ffffff', 'font-size': 11.5, 'font-family': 'Assistant,Heebo,system-ui,sans-serif', 'pointer-events': 'none' });
    ct.textContent = L.core; g.appendChild(ct);
    svg.appendChild(g);
    // the north arrow (fixed: the drawing turns, north stays up)
    svg.appendChild(el('path', { d: 'M276 30 L284 48 L276 43 L268 48 Z', fill: '#2f6f86' }));
    const nt = el('text', { x: 276, y: 22, 'text-anchor': 'middle', 'font-size': 12, 'font-weight': 700, fill: '#2f6f86', 'font-family': 'Assistant,Heebo,system-ui,sans-serif' });
    nt.textContent = L.north; svg.appendChild(nt);
  }
  draw();
  return {
    set(v) { st = Object.assign(st, v); draw(); },
    destroy() { wrap.remove(); },
  };
}
