// Renders the district plot map of sdplan.js once, for the page's static figure (no script needed to see it): node render_static_map.js
// Writes ../data/sdplan-static-map.svg. The interactive bits (tabindex, role=button, data-sdplot) are removed; the clip id is renamed.
const fs = require('fs'), path = require('path'), vm = require('vm');
const D = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'sdplan.json'), 'utf8'));
const LOC = 'he-IL', nf0 = new Intl.NumberFormat(LOC, { maximumFractionDigits: 0 });
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const win = { NadLanInstruments: { register: () => {}, fmt: { num: n => nf0.format(n || 0), ils: n => '₪' + nf0.format(n || 0) }, esc } };
vm.runInContext(fs.readFileSync(path.join(__dirname, 'sdplan.js'), 'utf8'), vm.createContext({ window: win, document: { addEventListener: () => {} }, Intl, Math, JSON, Event: function () {} }));
let svg = win.NLSD.map(D, '', null);
svg = svg.replace(/ tabindex="0" role="button"/g, '').replace(/ data-sdplot="[^"]*"/g, '').replace(/ class="sdp"/g, '').replace(/ aria-label="[^"]*"(?=><path)/g, '')
  .replace(/sdclip-all/g, 'sdclip-static').replace(/<style>.*?<\/style>/, '');
fs.writeFileSync(path.join(__dirname, '..', 'data', 'sdplan-static-map.svg'), svg);
console.log('static map', svg.length, 'bytes;', (svg.match(/<path/g) || []).length, 'paths');
