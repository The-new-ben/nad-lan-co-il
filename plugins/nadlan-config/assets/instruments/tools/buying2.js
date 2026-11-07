/* NadLan Instruments · buying2 v1 (HAD-683 Phase 2, Ben 8.11.2026 "תבצע את זה"): six more tools of the /buying-apartment/ hub, one file
   ('file' => 'buying2', after prices-common.js and buying.js, whose math and helpers it reuses through window.NLBH).
   - bsell    (T10) buy before you sell: the bridge, the replacement-home tax window (ptax.json), the months with two mortgages, 3 months late
   - bdates   (T24) a signing date gives the dated legal deadlines (Tax Authority guide 2026, Ministry of Construction) + an .ics file
   - bcompare (T22) 2 to 4 flats side by side: all-in cost (ptax, cost.json), equity needed and the monthly payment (BoI average, nrm.json)
   - bvisit   (T21) a visit sheet: questions per visit, answers and notes kept in this browser, a print view
   - bwho     (T11) who pays what in a second-hand deal: only rows with an official source; contract items named, without a row
   - bhelp    (T19) the programmes for a buyer's status, each with its gov.il page and date; what could not be verified is said
   Pure logic in window.NLBH2 (tools/instruments/test_buying_hub.js). */
(function () {
  'use strict';
  var W = typeof window !== 'undefined' ? window : this, B = W.NLBH;
  if (!B) return;
  var X = W.NLBH2 = {}, n0 = B.n0, date = B.date, pc = B.pc;
  function utc(iso) { var p = String(iso).split('-'); return Date.UTC(+p[0], +p[1] - 1, +p[2]); }
  function iso(t) { var d = new Date(t); return d.getUTCFullYear() + '-' + ('0' + (d.getUTCMonth() + 1)).slice(-2) + '-' + ('0' + d.getUTCDate()).slice(-2); }
  X.addDays = function (s, n) { return iso(utc(s) + n * 864e5); };
  X.addMonths = function (s, n) { var p = String(s).split('-'), y = +p[0], m = +p[1] - 1 + n, d = +p[2]; y += Math.floor(m / 12); m = ((m % 12) + 12) % 12; var last = new Date(Date.UTC(y, m + 1, 0)).getUTCDate(); return iso(Date.UTC(y, m, Math.min(d, last))); };

  /* T24: the deadlines from a signing date; only rules with an official source */
  X.dates = function (M, sign, ty, s) {
    var PT = M.ptax, Pp = PT.pay, Z = M.zakaut, O = M.orechdin, guide = { label: Pp.label, url: PT.guide.url, date: PT.checked }, out = [];
    out.push({ id: 'declare', t: 'הצהרת רוכש לרשות המסים', d: X.addDays(sign, Pp.declare_days), when: 'בתוך ' + Pp.declare_days + ' יום מהעסקה', note: 'גם כשאין מס. איחור: ' + n0(Pp.decl_fine) + ' ₪ לכל שבועיים (' + date(Pp.fine_from) + ' עד ' + date(Pp.fine_to) + ').', src: guide });
    out.push({ id: 'paytax', t: 'תשלום מס הרכישה', d: X.addDays(sign, Pp.pay_days), when: 'בתוך ' + Pp.pay_days + ' יום מהעסקה', note: 'נדחה כשעוד לא קיבלתם חזקה, לא שילמתם יותר ממחצית המחיר ולא קיבלתם ייפוי כוח לרישום (סעיף 51).', src: guide });
    if (B.has(s, 'upgrader')) out.push({ id: 'sellby', t: 'מכירת הדירה הקיימת', d: X.addMonths(sign, PT.upgrader[0].months), when: 'בתוך ' + PT.upgrader[0].months + ' חודשים', note: 'כדי לשלם לפי המדרגות של דירה יחידה.', src: { label: PT.guide.label, url: PT.guide.url, date: PT.checked } });
    if (B.has(s, 'zakaut')) { var m = ty === 'new' ? Z.process.developer_months : Z.process.second_hand_months, zs = Z.sources[Z.process.src];
      out.push({ id: 'zakaut', t: 'מימוש הלוואת הזכאות', d: X.addMonths(sign, m), when: 'עד ' + m + ' חודשים מהחתימה (' + (ty === 'new' ? 'דירה מקבלן' : 'יד שנייה') + ')', note: 'תעודת הזכאות עצמה בתוקף ' + Z.process.certificate_valid_years + ' שנה מיום ההנפקה.', src: { label: 'משרד הבינוי והשיכון: ' + zs.title, url: zs.url, date: zs.updated || zs.published } }); }
    out.sort(function (a, b) { return a.d < b.d ? -1 : a.d > b.d ? 1 : 0; });
    out.push({ id: 'objection', t: 'השגה על שומת מס הרכישה', d: null, when: 'בתוך ' + Pp.objection_days + ' יום מיום קבלת השומה', note: '', src: guide });
    if (ty !== 'new') out.push({ id: 'cgt', t: 'מקדמה על מס שבח מתוך התשלומים למוכר', d: null, when: 'כשעברו ' + pc(O.cgt_advance.after_paid) + '% מהמחיר', note: pc(O.cgt_advance.rate) + '% מהמחיר, אלא אם המוכר הציג אישור אחר.', src: { label: O.sources.TAX.label, url: O.sources.TAX.url, date: O.checked } });
    return out;
  };
  function icsEsc(s) { return String(s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n'); }
  function fold(l) { var o = '', n = 0; for (var i = 0; i < l.length; i++) { var c = l.charCodeAt(i), b = c < 0x80 ? 1 : c < 0x800 ? 2 : (c >= 0xD800 && c <= 0xDBFF) ? 4 : (c >= 0xDC00 && c <= 0xDFFF) ? 0 : 3; if (n + b > 73) { o += '\r\n '; n = 1; } o += l[i]; n += b; } return o; }
  X.ics = function (items, now) {
    var st = (now || new Date().toISOString()).replace(/[-:]/g, '').replace(/\.\d+/, '').slice(0, 15) + 'Z', L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//nad-lan.co.il//buying-apartment//HE', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH'];
    items.filter(function (x) { return x.d; }).forEach(function (x) {
      var d = x.d.replace(/-/g, ''), e = X.addDays(x.d, 1).replace(/-/g, '');
      L.push('BEGIN:VEVENT', 'UID:' + x.id + '-' + d + '@nad-lan.co.il', 'DTSTAMP:' + st, 'DTSTART;VALUE=DATE:' + d, 'DTEND;VALUE=DATE:' + e, 'SUMMARY:' + icsEsc('קניית דירה: ' + x.t),
        'DESCRIPTION:' + icsEsc(x.when + '. ' + (x.note || '') + ' מקור: ' + x.src.label), 'BEGIN:VALARM', 'TRIGGER:-P3D', 'ACTION:DISPLAY', 'DESCRIPTION:' + icsEsc(x.t), 'END:VALARM', 'END:VEVENT');
    });
    L.push('END:VCALENDAR');
    return L.map(fold).join('\r\n') + '\r\n';
  };
  /* T10: buy before you sell */
  X.sell = function (o) {
    var ltv = o.NRM.ltv_by_status.cit_sell, taxRep = B.tax(o.newP, 'single', o.PT), taxExtra = B.tax(o.newP, 'extra', o.PT), law = o.newP * o.CO.lawyer.from / 100 * (1 + o.CO.vat);
    var need = o.newP * (1 - ltv) + taxRep + law, bridge = Math.max(0, need - (o.cash || 0)), mort = o.newP * ltv, newPay = B.pmt(mort, o.rate, o.years);
    var net = o.saleP - (o.oldLoan || 0), bi = o.bridgeRate > 0 ? bridge * o.bridgeRate / 1200 : null, extra = (o.oldPay || 0) + (bi || 0), win = o.PT.upgrader[0].months;
    return { ltv: ltv, taxRep: taxRep, taxExtra: taxExtra, law: law, need: need, bridge: bridge, mort: mort, newPay: newPay, net: net, left: net - bridge, bi: bi, monthly: newPay + extra,
      double: o.months * extra, win: win, late: { months: o.months + 3, extra: 3 * extra, taxJump: o.months + 3 > win ? taxExtra - taxRep : 0 }, inTime: o.months <= win };
  };
  /* T22: compare 2 to 4 flats */
  X.compare = function (flats, o) {
    return flats.map(function (f) {
      var P = Math.max(0, +f.price || 0), tax = B.tax(P, o.track, o.PT, o.dis), lawLo = P * o.CO.lawyer.from / 100 * (1 + o.CO.vat), lawHi = P * o.CO.lawyer.to / 100 * (1 + o.CO.vat), ap = o.CO.appraiser, ins = o.CO.inspection, mort = P * o.ltv;
      return { name: f.name, type: f.type, P: P, tax: tax, lawLo: lawLo, lawHi: lawHi, lo: P + tax + lawLo + ap[0] + ins[0], hi: P + tax + lawHi + ap[1] + ins[1], mort: mort, eq: P - mort + tax + lawLo, pay: B.pmt(mort, o.rate, o.years) };
    });
  };
  /* T11 and T19 */
  X.who = function (BU, M) {
    var O = M.orechdin, S = { ptax: { label: M.ptax.source, url: M.ptax.url, date: M.ptax.checked }, ptaxpay: { label: M.ptax.pay.label, url: M.ptax.guide.url, date: M.ptax.checked }, guide: { label: M.ptax.guide.label, url: M.ptax.guide.url, date: M.ptax.checked },
      tax15: { label: O.sources.TAX.label, url: O.sources.TAX.url, date: O.checked }, eth: { label: O.sources.ETH.label, url: O.sources.ETH.url, date: O.checked } };
    Object.keys(BU.laws).forEach(function (k) { S[k] = BU.laws[k]; });
    return BU.who.map(function (r) { return { t: r.t, who: r.who, d: B.fill(r.d, M), src: S[r.src] || null }; });
  };
  X.help = function (BU, s, tg, M) {
    return BU.help.filter(function (h) { return (!h.flag || B.has(s, h.flag)) && (!h.toggle || tg[h.toggle]); }).map(function (h) {
      var z = h.z ? M.zakaut.sources[h.z] : null;
      return { id: h.id, t: h.t, d: B.fill(h.d, M), href: h.href || (z ? z.url : M.ptax.url),
        src: z ? { label: 'משרד הבינוי והשיכון: ' + z.title, url: z.url, date: z.updated || z.published, read: z.checked } : h.p ? { label: M.ptax.source, url: M.ptax.url, date: M.ptax.checked } : null };
    });
  };
  X.visitCount = function (v) { var o = { y: 0, n: 0, q: 0 }; Object.keys((v && v.a) || {}).forEach(function (k) { if (o[v.a[k]] != null) o[v.a[k]]++; }); return o; };

  if (!W.NadLanInstruments || typeof document === 'undefined' || !W.NLPH || !W.NLPH.ui || !B.ui) return;
  /* ------------------------------------------------------------------ the surfaces ------------------------------------------------------------------ */
  var NI = W.NadLanInstruments, P = W.NLPH, U = P.ui, esc = U.esc, H = B.ui;
  function css() {
    if (document.getElementById('nlbh2-css')) return;
    var s = document.createElement('style'); s.id = 'nlbh2-css';
    s.textContent = [
      '.nlbh-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:12px 0 0;position:relative}@media (max-width:640px){.nlbh-cards{grid-template-columns:1fr}}',
      '.nlbh-card{border:1px solid var(--nli-line);border-top:3px solid var(--nli-sea);border-radius:var(--nli-r-s);background:#fff;padding:12px 14px;display:grid;gap:4px;align-content:start}',
      '.nlbh-card b{font:600 16px/22px var(--nli-sans);color:var(--nli-ink)}.nlbh-card p{margin:0 !important;font:400 14.5px/23px var(--nli-sans);color:var(--nli-ink2)}.nlbh-card small{font:400 12px/17px var(--nli-sans);color:var(--nli-mute)}',
      'html body .nli .nlbh-card a{color:var(--nli-sea) !important;text-decoration:underline;text-underline-offset:3px}',
      'html body .nli .nlbh .nlbh-tg button{min-height:40px;padding:8px 12px;border:1px solid var(--nli-line);border-radius:999px;background:#fff;color:var(--nli-ink2);font:500 13.5px/18px var(--nli-sans);cursor:pointer;margin:0;box-shadow:none}',
      'html body .nli .nlbh .nlbh-tg button[aria-pressed="true"]{background:var(--nli-sea);border-color:var(--nli-sea);color:#fff}.nlbh-tg{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 0}',
      '.nlbh-flats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:12px 0 0}@media (max-width:900px){.nlbh-flats{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:340px){.nlbh-flats{grid-template-columns:1fr}}',
      '.nlbh-flat{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:#fff;padding:10px;display:grid;gap:8px;position:relative;min-width:0}',
      'html body .nli .nlbh .nlbh-flat input[type=text],html body .nli .nlbh .nlbh-vtop input{font:500 15px/1.2 var(--nli-sans);border:1px solid var(--nli-line) !important;border-radius:var(--nli-r-s);padding:9px 10px;width:100%;min-width:0;margin:0;background:#fff !important;box-shadow:none !important;color:var(--nli-ink);height:auto}',
      'html body .nli .nlbh .nlbh-x{position:absolute;top:6px;left:6px;width:30px;height:30px;border:0;background:none;color:var(--nli-mute);font:500 20px/1 var(--nli-sans);cursor:pointer;padding:0;margin:0;box-shadow:none}',
      '.nlbh-vtop{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:10px;margin:12px 0 0}@media (max-width:520px){.nlbh-vtop{grid-template-columns:1fr}}',
      '.nlbh-vg summary{min-height:46px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;font:600 16px/22px var(--nli-sans);color:var(--nli-ink);border-bottom:1px solid var(--nli-line);list-style:none}.nlbh-vg summary::-webkit-details-marker{display:none}.nlbh-vg summary span{font:500 12.5px/1 var(--nli-mono);color:var(--nli-mute)}',
      '.nlbh-vq{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px 10px;align-items:center;padding:8px 0;border-bottom:1px dashed var(--nli-line)}.nlbh-vq p{margin:0 !important;font:400 14.5px/22px var(--nli-sans);color:var(--nli-ink)}',
      '@media (max-width:520px){.nlbh-vq{grid-template-columns:1fr}}.nlbh-ans3{display:flex;gap:4px}',
      'html body .nli .nlbh .nlbh-ans3 button{min-width:52px;min-height:36px;padding:4px 8px;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:#fff;color:var(--nli-ink2);font:500 13px/1 var(--nli-sans);cursor:pointer;margin:0;box-shadow:none}',
      'html body .nli .nlbh .nlbh-ans3 button[aria-pressed="true"][data-v="y"]{background:var(--ph-up);border-color:var(--ph-up);color:#fff}html body .nli .nlbh .nlbh-ans3 button[aria-pressed="true"][data-v="n"]{background:var(--ph-dn);border-color:var(--ph-dn);color:#fff}html body .nli .nlbh .nlbh-ans3 button[aria-pressed="true"][data-v="q"]{background:var(--nli-ink);border-color:var(--nli-ink);color:#fff}',
      'html body .nli .nlbh textarea.nlbh-note{width:100%;min-height:64px;margin:8px 0 12px;border:1px solid var(--nli-line) !important;border-radius:var(--nli-r-s);padding:8px 10px;font:400 14.5px/22px var(--nli-sans);background:#fff !important;box-shadow:none !important;color:var(--nli-ink)}'
    ].join('');
    document.head.appendChild(s);
  }
  function setup(root, kicker, name) { var M = B.model(arguments[3]); css(); var p = H.panel(root, kicker, name); return { M: M, p: p }; }
  function srcLine(list) { var e = U.el('p', 'nli__src'); e.innerHTML = 'מקורות: ' + list.map(H.src1).join(' · '); return e; }
  function acts(p, btns) { var a = U.el('div', 'nlbh-acts'); btns.forEach(function (b) { a.appendChild(b); }); p.appendChild(a); return a; }
  function btn(label, on) { var b = U.el('button', '', esc(label)); b.type = 'button'; b.addEventListener('click', on); return b; }
  function today() { var d = new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function getJ(k) { try { var s = W.localStorage.getItem(k); return s ? JSON.parse(s) : null; } catch (e) { return null; } }
  function putJ(k, v) { try { W.localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  /* ---------------- bsell (T10) ---------------- */
  NI.register('bsell', { custom: function (root, D0) {
    var o = setup(root, 'מחשבון · דירה חלופית', 'קניית דירה לפני מכירה: הלוואת הגישור, המס והחודשים הכפולים', D0), M = o.M, p = o.p, R = B.rate(M.boim), PH = M.phub;
    p.appendChild(U.el('p', 'nlph-sub', esc('קונים את הדירה החדשה לפני שהקיימת נמכרה: כמה גישור צריך, מה קורה למס הרכישה אם המכירה לא נסגרת בזמן, כמה עולים החודשים שבהם משלמים על שתי הדירות, ומה קורה אם המכירה מתאחרת ב־3 חודשים.')));
    var st = { newP: B.lastQ(PH.il.r5, PH.q).v, saleP: B.lastQ(PH.il.r4, PH.q).v, oldLoan: 500000, oldPay: null, cash: 150000, months: 6, bridgeRate: null, years: 25 };
    var f = U.el('div', 'nlbh-form'); p.appendChild(f);
    [['newP', 'מחיר הדירה החדשה', '₪', 1], ['saleP', 'מחיר המכירה הצפוי של הקיימת', '₪', 1], ['oldLoan', 'יתרת המשכנתא על הקיימת', '₪', 1], ['oldPay', 'ההחזר החודשי על הקיימת', '₪ בחודש', 1], ['cash', 'כסף זמין עכשיו', '₪', 1], ['months', 'חודשים עד שהקיימת נמכרת', 'חודשים', 0], ['bridgeRate', 'ריבית הלוואת הגישור (מההצעה)', '%', 0]].forEach(function (x) {
      f.appendChild(H.field(x[1], x[2], st[x[0]], function (v) { st[x[0]] = v; draw(); }, !!x[3])); });
    var out = U.el('div', ''); out.setAttribute('aria-live', 'polite'); p.appendChild(out); var txt = '';
    function draw() {
      var x = X.sell({ newP: st.newP || 0, saleP: st.saleP || 0, oldLoan: st.oldLoan || 0, oldPay: st.oldPay || 0, cash: st.cash || 0, months: st.months || 0, bridgeRate: st.bridgeRate, years: st.years, rate: R.rate, PT: M.ptax, NRM: M.nrm, CO: M.cost });
      var h = '<div class="nlph-ans"><div class="nlph-ans__head"><span>הגישור והחודשים הכפולים</span><small>' + esc('דירה חלופית · מימון עד ' + pc(x.ltv) + '%') + '</small></div><p class="nlph-ans__a"><b>' + esc(x.bridge > 0 ? 'צריך הלוואת גישור של כ־' + U.ils(x.bridge) : 'הכסף הזמין מכסה את החלק שלכם, בלי גישור') + '</b>' +
        esc(': החלק שהבנק לא מממן (' + pc(1 - x.ltv) + '%), מס רכישה ' + (x.taxRep < 1 ? 'פטור' : U.ils(x.taxRep)) + ' ועורך דין, יחד ' + U.ils(x.need) + '. ' + (x.left >= 0 ? 'המכירה מחזירה ' + U.ils(x.net) + ' אחרי המשכנתא הקיימת, ומכסה את הגישור עם ' + U.ils(x.left) + ' עודף.' : 'המכירה מחזירה ' + U.ils(x.net) + ' אחרי המשכנתא הקיימת, ולא מכסה את הגישור: חסרים ' + U.ils(-x.left) + '.')) + '</p>' +
        H.kpis([['גישור', H.big(x.bridge), 'עד שהקיימת נמכרת'], ['חודשים כפולים', String(st.months || 0), 'שתי דירות בבת אחת'], ['בחודש, בתקופה הכפולה', st.oldPay ? U.ils(x.monthly) : '·', st.oldPay ? 'חדשה + קיימת' + (x.bi != null ? ' + ריבית גישור' : '') : 'הקלידו את ההחזר הקיים'], ['מס אם המכירה לא בזמן', '+' + U.ils(x.taxExtra - x.taxRep), 'אחרי ' + x.win + ' חודשים', 'is-dn']]) + '</div>';
      h += '<div class="nlph-tw" style="margin-top:12px"><table class="nlph-t"><caption>' + esc('התרחישים. משכנתא חדשה ' + U.ils(x.mort) + ' ל־' + st.years + ' שנה בריבית ' + R.rate + '% (ממוצע בנק ישראל, ' + date(R.month) + ')') + '</caption><thead><tr><th scope="col">תרחיש</th><th scope="col" class="n">חודשים כפולים</th><th scope="col" class="n">עלות התקופה הכפולה</th><th scope="col" class="n">מס רכישה</th></tr></thead><tbody>' +
        '<tr class="is-nat"><th scope="row">לפי התוכנית</th><td class="n">' + (st.months || 0) + '</td><td class="n">' + (st.oldPay ? U.ils(x.double) : '·') + '</td><td class="n">' + (x.inTime ? U.ils(x.taxRep) : U.ils(x.taxExtra)) + '</td></tr>' +
        '<tr><th scope="row">המכירה מתאחרת ב־3 חודשים</th><td class="n">' + x.late.months + '</td><td class="n">' + (st.oldPay ? U.ils(x.double + x.late.extra) : '·') + '</td><td class="n">' + (x.late.months > x.win ? U.ils(x.taxExtra) : U.ils(x.taxRep)) + '</td></tr></tbody></table></div>';
      h += '<p class="nlph-fine">' + esc('עלות התקופה הכפולה: ההחזר על המשכנתא הקיימת' + (x.bi != null ? ' וריבית הגישור (ריבית בלבד, בלי החזר קרן)' : '') + ' לכל חודש עד המכירה, מעבר להחזר על החדשה (' + U.ils(x.newPay) + ' בחודש). לריבית על הלוואת גישור אין ממוצע מפורסם, ולכן אין מספר עד שמקלידים את ההצעה. מס הרכישה: מדרגות דירה יחידה אם הקיימת נמכרת בתוך ' + x.win + ' חודשים, ואחרת מדרגות דירה נוספת. בלי תיווך, מעבר ומס שבח על המכירה.') + '</p>';
      out.innerHTML = h;
      txt = 'קניית דירה לפני מכירה: גישור ' + U.ils(x.bridge) + ', ' + (st.months || 0) + ' חודשים כפולים. אם המכירה לא נסגרת בתוך ' + x.win + ' חודשים, מס הרכישה עולה ב־' + U.ils(x.taxExtra - x.taxRep) + '.';
    }
    draw();
    p.appendChild(srcLine([{ label: M.ptax.guide.label, url: M.ptax.guide.url, date: M.ptax.checked }, { label: M.nrm.ltv_source.label_he, url: M.nrm.ltv_source.url, date: M.nrm.checked }, R.src]));
    p.appendChild(U.share(function () { return txt; }));
  } });

  /* ---------------- bdates (T24) ---------------- */
  NI.register('bdates', { custom: function (root, D0) {
    var o = setup(root, 'יומן · מועדים בחוק', 'לוח זמנים לקניית דירה: המועדים שלכם ביומן', D0), M = o.M, p = o.p, BU = M.buying;
    p.appendChild(U.el('p', 'nlph-sub', esc('מקלידים את תאריך החתימה ומקבלים את התאריכים שהחוק קובע אחריה, כל אחד עם המקור שלו, וקובץ שנכנס ליומן בטלפון עם תזכורת 3 ימים לפני. מועד שלא מצאנו לו מקור רשמי לא נכנס.')));
    var st = { sign: today(), ty: 'used', s: H.load().s || 'first' };
    var f = U.el('div', 'nlbh-form'); p.appendChild(f);
    var df = U.el('div', 'nli__f'), dl = U.el('label', '', 'תאריך החתימה'), dib = U.el('div', 'nli__in'), di = document.createElement('input'); di.type = 'date'; di.id = 'nlbh-sign-' + Math.random().toString(36).slice(2, 7); dl.htmlFor = di.id; di.value = st.sign;
    di.addEventListener('change', function () { if (/^\d{4}-\d{2}-\d{2}$/.test(di.value)) { st.sign = di.value; draw(); } }); dib.appendChild(di); df.appendChild(dl); df.appendChild(dib); f.appendChild(df);
    f.appendChild(H.statusSelect(BU, st.s, function (v) { st.s = v; draw(); }));
    p.appendChild(H.tabs('דירה', [['used', 'יד שנייה'], ['new', 'מקבלן']], st.ty, function (v) { st.ty = v; draw(); }));
    var out = U.el('div', ''); out.setAttribute('aria-live', 'polite'); p.appendChild(out); var items = [];
    function draw() {
      items = X.dates(M, st.sign, st.ty, B.status(BU, st.s));
      out.innerHTML = '<div class="nlph-tw" style="margin-top:12px"><table class="nlph-t"><caption>' + esc('המועדים אחרי חתימה ב־' + date(st.sign)) + '</caption><thead><tr><th scope="col">מה</th><th scope="col" class="n">עד</th><th scope="col" class="nlph-dk">המקור</th></tr></thead><tbody>' +
        items.map(function (x) { return '<tr' + (x.d ? '' : ' class="is-nat"') + '><th scope="row">' + esc(x.t) + '<br><small style="font-weight:400;color:var(--nli-mute)">' + esc(x.when + (x.note ? '. ' + x.note : '')) + '</small><small class="nlph-ph" style="font-weight:400;color:var(--nli-mute)">מקור: ' + H.src1(x.src) + '</small></th><td class="n">' + (x.d ? esc(date(x.d)) : '·') + '</td><td class="nlph-dk" style="font-size:12.5px !important">' + H.src1(x.src) + '</td></tr>'; }).join('') + '</tbody></table></div>';
    }
    draw();
    var ics = btn('הוספה ליומן (קובץ ics)', function () { var blob = new Blob([X.ics(items)], { type: 'text/calendar;charset=utf-8' }), a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'kniyat-dira-moadim.ics'; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1500); });
    ics.className = 'nlbh-pdf'; ics.setAttribute('data-ics', '1');
    acts(p, [ics, H.printBtn(function () { return '<h2>' + esc('לוח זמנים לקניית דירה: חתימה ב־' + date(st.sign)) + '</h2><table><thead><tr><th>מה</th><th>עד</th><th>מקור</th></tr></thead><tbody>' + items.map(function (x) { return '<tr><td><b>' + esc(x.t) + '</b><br>' + esc(x.when + (x.note ? '. ' + x.note : '')) + '</td><td>' + (x.d ? esc(date(x.d)) : '') + '</td><td>' + esc(x.src.label) + '</td></tr>'; }).join('') + '</tbody></table>'; })]);
    p.appendChild(U.el('p', 'nlph-fine', esc('לא נכנסו, כי לא מצאנו מועד בחוק: רישום הערת האזהרה (נרשמת מיד אחרי החתימה, והכסף הראשון נשאר בנאמנות עד אז) ומועד המסירה, שנקבע בחוזה. מה שקובע במקרה שלכם הוא החוזה ועורך הדין.')));
  } });

  /* ---------------- bcompare (T22) ---------------- */
  NI.register('bcompare', { custom: function (root, D0) {
    var o = setup(root, 'השוואה · 2 עד 4 דירות', 'השוואה לפני קניית דירה: עלות כוללת, הון עצמי והחזר חודשי', D0), M = o.M, p = o.p, BU = M.buying, R = B.rate(M.boim), PH = M.phub, KEY = 'nlbh-compare-v1';
    p.appendChild(U.el('p', 'nlph-sub', esc('מכניסים 2 עד 4 דירות שאתם שוקלים, ורואים אותן זו לצד זו: כמה כל אחת עולה עם המס ועורך הדין, כמה הון עצמי צריך וכמה ההחזר החודשי. הרשימה נשמרת בדפדפן הזה.')));
    var il = function (r) { return B.lastQ(PH.il['r' + r], PH.q).v; };
    var st = getJ(KEY) || { s: H.load().s || 'first', years: 25, flats: [{ name: 'דירה א', price: il(3), type: 'used' }, { name: 'דירה ב', price: il(4), type: 'used' }] };
    var f = U.el('div', 'nlbh-form'); p.appendChild(f); f.appendChild(H.statusSelect(BU, st.s, function (v) { st.s = v; save(); draw(); }));
    p.appendChild(H.tabs('תקופת המשכנתא', [[20, '20 שנה'], [25, '25 שנה'], [30, '30 שנה']], st.years, function (v) { st.years = +v; save(); draw(); }));
    var fl = U.el('div', 'nlbh-flats'); p.appendChild(fl);
    var add = btn('הוספת דירה להשוואה', function () { if (st.flats.length < 4) { st.flats.push({ name: 'דירה ' + 'אבגד'[st.flats.length], price: il(4), type: 'used' }); save(); cards(); draw(); } });
    var out = U.el('div', ''); out.setAttribute('aria-live', 'polite');
    function save() { putJ(KEY, st); }
    function cards() {
      fl.innerHTML = '';
      st.flats.forEach(function (x, i) {
        var c = U.el('div', 'nlbh-flat'), n = document.createElement('input'); n.type = 'text'; n.value = x.name; n.setAttribute('aria-label', 'שם הדירה'); n.addEventListener('input', function () { x.name = n.value; save(); draw(); }); c.appendChild(n);
        c.appendChild(H.field('מחיר', '₪', x.price, function (v) { x.price = v || 0; save(); draw(); }, true));
        c.appendChild(H.select('סוג', [['used', 'יד שנייה'], ['new', 'מקבלן']], x.type, function (v) { x.type = v; save(); draw(); }));
        if (st.flats.length > 2) { var del = U.el('button', 'nlbh-x', '×'); del.type = 'button'; del.setAttribute('aria-label', 'הסרת ' + x.name); del.addEventListener('click', function () { st.flats.splice(i, 1); save(); cards(); draw(); }); c.appendChild(del); }
        fl.appendChild(c);
      });
      add.disabled = st.flats.length >= 4; add.style.display = st.flats.length >= 4 ? 'none' : '';
    }
    acts(p, [add]); p.appendChild(out);
    function draw() {
      var s = B.status(BU, st.s), l = B.ltv(s, M.nrm), rows = X.compare(st.flats, { ltv: l, track: s.ptax, dis: B.has(s, 'ptax_disabled'), PT: M.ptax, CO: M.cost, rate: R.rate, years: st.years });
      var best = rows.reduce(function (a, r, i) { return r.lo < rows[a].lo ? i : a; }, 0), k = function (n) { return U.k(n); };
      var line = function (lab, f, cls) { return '<tr' + (cls ? ' class="' + cls + '"' : '') + '><th scope="row">' + esc(lab) + '</th>' + rows.map(function (r, i) { return '<td class="n' + (i === best && cls ? ' fit' : '') + '">' + f(r) + '</td>'; }).join('') + '</tr>'; };
      out.innerHTML = '<div class="nlph-tw" style="margin-top:12px;overflow-x:auto"><table class="nlph-t"><caption>' + esc('באלפי ₪, ' + s.label + ', מימון עד ' + pc(l) + '%, ריבית ' + R.rate + '% ל־' + st.years + ' שנה (ממוצע בנק ישראל, ' + date(R.month) + ')') + '</caption><thead><tr><th scope="col"></th>' + rows.map(function (r) { return '<th scope="col" class="n">' + esc(r.name || '·') + '</th>'; }).join('') + '</tr></thead><tbody>' +
        line('מחיר', function (r) { return k(r.P); }) + line('מס רכישה', function (r) { return r.tax < 1 ? 'פטור' : k(r.tax); }) + line('עורך דין', function (r) { return k(r.lawLo) + '<br>עד ' + k(r.lawHi); }) +
        line('עלות כוללת', function (r) { return k(r.lo) + '<br>עד ' + k(r.hi); }, 'is-nat') + line('הון עצמי נדרש', function (r) { return k(r.eq); }) + line('משכנתא', function (r) { return k(r.mort); }) +
        line('החזר חודשי (₪)', function (r) { return U.num(r.pay); }) + '</tbody></table></div><p class="nlph-fine">' + esc('עלות כוללת: מחיר, מס רכישה, עורך דין ' + M.cost.lawyer.from + '% עד ' + M.cost.lawyer.to + '% ועוד מע״מ, שמאי ' + n0(M.cost.appraiser[0]) + ' עד ' + n0(M.cost.appraiser[1]) + ' ₪ ובדק בית ' + n0(M.cost.inspection[0]) + ' עד ' + n0(M.cost.inspection[1]) + ' ₪ (ביזפורטל, 6.8.2026). בלי תיווך, מעבר ושיפוץ. בדירה מקבלן המע״מ כלול במחיר, וההצמדה למדד באה בנוסף.') + '</p>';
    }
    cards(); draw();
    acts(p, [H.printBtn(function () { return '<h2>השוואה לפני קניית דירה</h2>' + out.innerHTML; })]);
    p.appendChild(srcLine([{ label: M.ptax.source, url: M.ptax.url, date: M.ptax.checked }, { label: M.nrm.ltv_source.label_he, url: M.nrm.ltv_source.url, date: M.nrm.checked }, R.src]));
  } });

  /* ---------------- bvisit (T21) ---------------- */
  NI.register('bvisit', { custom: function (root, D0) {
    var o = setup(root, 'דף ביקור · נשמר בדפדפן', 'שאלות לשאול כשרואים דירה: דף ביקור שנשמר', D0), M = o.M, p = o.p, BU = M.buying, KEY = 'nlbh-visit-v1';
    p.appendChild(U.el('p', 'nlph-sub', esc('פותחים דף לכל דירה שרואים, מסמנים כן, לא או לבדוק ליד כל שאלה, וכותבים הערות. הכול נשמר רק בדפדפן הזה, ואפשר להדפיס או לשמור כ־PDF ולהביא לעורך הדין או לבודק.')));
    var st = getJ(KEY) || { cur: 0, visits: [] }; if (!st.visits.length) st.visits.push({ name: 'הדירה הראשונה', date: today(), a: {}, n: {} });
    var top = U.el('div', 'nlbh-vtop'); p.appendChild(top); var body = U.el('div', ''); p.appendChild(body);
    function save() { putJ(KEY, st); }
    function V() { return st.visits[Math.min(st.cur, st.visits.length - 1)]; }
    function draw() {
      var v = V(); top.innerHTML = '';
      var sel = H.select('הדירה', st.visits.map(function (x, i) { return [i, x.name + ' · ' + date(x.date)]; }), st.cur, function (val) { st.cur = +val; save(); draw(); }); top.appendChild(sel);
      var nf = U.el('div', 'nli__f'), nl = U.el('label', '', 'שם או כתובת'), ni = document.createElement('input'); ni.type = 'text'; ni.value = v.name; ni.id = 'nlbh-vn-' + Math.random().toString(36).slice(2, 7); nl.htmlFor = ni.id;
      ni.addEventListener('change', function () { v.name = ni.value || v.name; save(); draw(); }); nf.appendChild(nl); nf.appendChild(ni); top.appendChild(nf);
      var c = X.visitCount(v), h = '<p class="nlph-sub" style="margin-top:10px">' + esc(c.y + ' כן · ' + c.n + ' לא · ' + c.q + ' לבדוק') + '</p>';
      body.innerHTML = h + BU.visit.map(function (g, gi) {
        return '<details class="nlbh-vg"' + (gi < 2 ? ' open' : '') + '><summary>' + esc(g.g) + '<span>' + g.q.filter(function (q, qi) { return v.a[gi + '.' + qi]; }).length + '/' + g.q.length + '</span></summary>' +
          g.q.map(function (q, qi) { var id = gi + '.' + qi, a = v.a[id] || ''; return '<div class="nlbh-vq"><p>' + esc(q) + '</p><div class="nlbh-ans3" role="group" aria-label="' + esc(q) + '">' + [['y', 'כן'], ['n', 'לא'], ['q', 'לבדוק']].map(function (b) { return '<button type="button" data-q="' + id + '" data-v="' + b[0] + '" aria-pressed="' + (a === b[0]) + '">' + b[1] + '</button>'; }).join('') + '</div></div>'; }).join('') +
          '<textarea class="nlbh-note" data-g="' + gi + '" aria-label="' + esc('הערות: ' + g.g) + '" placeholder="הערות">' + esc(v.n[gi] || '') + '</textarea></details>';
      }).join('');
      [].forEach.call(body.querySelectorAll('.nlbh-ans3 button'), function (b) { b.addEventListener('click', function () { var id = b.getAttribute('data-q'), val = b.getAttribute('data-v'); if (v.a[id] === val) delete v.a[id]; else v.a[id] = val; save(); var y = b.getBoundingClientRect().top; draw(); var nb = body.querySelector('button[data-q="' + id + '"][data-v="' + val + '"]'); if (nb) { var d = nb.getBoundingClientRect().top - y; if (Math.abs(d) > 1) W.scrollBy(0, d); } }); });
      [].forEach.call(body.querySelectorAll('textarea'), function (t) { t.addEventListener('input', function () { v.n[t.getAttribute('data-g')] = t.value; save(); }); });
    }
    draw();
    acts(p, [btn('דירה חדשה', function () { st.visits.push({ name: 'דירה ' + (st.visits.length + 1), date: today(), a: {}, n: {} }); st.cur = st.visits.length - 1; save(); draw(); }),
      H.printBtn(function () { var v = V(), W3 = { y: 'כן', n: 'לא', q: 'לבדוק' }; return '<h2>' + esc('דף ביקור: ' + v.name + ', ' + date(v.date)) + '</h2>' + BU.visit.map(function (g, gi) { return '<h3>' + esc(g.g) + '</h3><table><tbody>' + g.q.map(function (q, qi) { return '<tr><td>' + esc(q) + '</td><td style="width:70pt">' + esc(W3[v.a[gi + '.' + qi]] || '') + '</td></tr>'; }).join('') + '</tbody></table>' + (v.n[gi] ? '<p>הערות: ' + esc(v.n[gi]) + '</p>' : ''); }).join(''); }),
      btn('מחיקת הדף הזה', function () { if (st.visits.length > 1) { st.visits.splice(st.cur, 1); st.cur = 0; } else { st.visits[0] = { name: 'הדירה הראשונה', date: today(), a: {}, n: {} }; } save(); draw(); })]);
  } });

  /* ---------------- bwho (T11) ---------------- */
  NI.register('bwho', { custom: function (root, D0) {
    var o = setup(root, 'טבלה · קונה מול מוכר', 'מי משלם מה בעסקת דירה יד שנייה: הקונה מול המוכר', D0), M = o.M, p = o.p, BU = M.buying, rows = X.who(BU, M);
    p.appendChild(U.el('p', 'nlph-sub', esc('בעסקת יד שנייה חלק מהתשלומים נקבעים בחוק וחלק בחוזה. בטבלה רק מה שיש לו מקור רשמי; מה שנקבע בחוזה כתוב מתחתיה, בלי שורה.')));
    var tw = U.el('div', 'nlph-tw'); tw.innerHTML = '<table class="nlph-t"><caption>מי משלם מה, לפי החוק</caption><thead><tr><th scope="col">מה</th><th scope="col">מי משלם</th><th scope="col" class="nlph-dk">המקור</th></tr></thead><tbody>' +
      rows.map(function (r) { return '<tr><th scope="row">' + esc(r.t) + '<br><small style="font-weight:400;color:var(--nli-mute)">' + esc(r.d) + '</small><small class="nlph-ph" style="font-weight:400;color:var(--nli-mute)">מקור: ' + H.src1(r.src) + '</small></th><td><b>' + esc(r.who) + '</b></td><td class="nlph-dk" style="font-size:12.5px !important">' + H.src1(r.src) + '</td></tr>'; }).join('') + '</tbody></table>';
    p.appendChild(tw); p.appendChild(U.el('p', 'nlph-fine', esc(B.fill(BU.who_contract, M))));
    acts(p, [H.printBtn(function () { return '<h2>מי משלם מה בעסקת דירה יד שנייה</h2><table><thead><tr><th>מה</th><th>מי משלם</th><th>מקור</th></tr></thead><tbody>' + rows.map(function (r) { return '<tr><td><b>' + esc(r.t) + '</b><br>' + esc(r.d) + '</td><td>' + esc(r.who) + '</td><td>' + esc(r.src ? r.src.label : '') + '</td></tr>'; }).join('') + '</tbody></table><p>' + esc(B.fill(BU.who_contract, M)) + '</p>'; })]);
  } });

  /* ---------------- bhelp (T19) ---------------- */
  NI.register('bhelp', { custom: function (root, D0) {
    var o = setup(root, 'הטבות · לפי המצב שלכם', 'ההטבות לקונה לפי המצב שלכם: זכאות, תוספות ומענקים', D0), M = o.M, p = o.p, BU = M.buying;
    p.appendChild(U.el('p', 'nlph-sub', esc('בוחרים את המצב ומסמנים מה מתאים לכם. מקבלים את ההטבות הרשמיות, כל אחת עם הדף שלה ב־gov.il ותאריך העדכון שלו. הסכום הסופי נקבע בתעודת הזכאות.')));
    var st = { s: H.load().s || 'first', tg: {} };
    var f = U.el('div', 'nlbh-form'); p.appendChild(f); f.appendChild(H.statusSelect(BU, st.s, function (v) { st.s = v; draw(); }));
    var tg = U.el('div', 'nlbh-tg'); tg.setAttribute('role', 'group'); tg.setAttribute('aria-label', 'מה מתאים לכם'); p.appendChild(tg);
    BU.toggles.forEach(function (t) { var b = U.el('button', '', esc(t[1])); b.type = 'button'; b.setAttribute('aria-pressed', 'false'); b.setAttribute('data-t', t[0]); b.addEventListener('click', function () { st.tg[t[0]] = !st.tg[t[0]]; b.setAttribute('aria-pressed', String(!!st.tg[t[0]])); draw(); }); tg.appendChild(b); });
    var out = U.el('div', ''); out.setAttribute('aria-live', 'polite'); p.appendChild(out);
    function draw() {
      var s = B.status(BU, st.s), list = X.help(BU, s, st.tg, M);
      out.innerHTML = (list.length ? '<div class="nlbh-cards">' + list.map(function (h) { return '<div class="nlbh-card"><b>' + esc(h.t) + '</b><p>' + esc(h.d) + '</p><small>' + (h.src ? H.src1(h.src) + (h.src.read ? ' · נקרא ' + esc(date(h.src.read)) : '') : '<a href="' + esc(h.href) + '">התנאים בעמוד</a>') + '</small></div>'; }).join('') + '</div>'
        : '<p class="nlph-sub" style="margin-top:12px">' + esc('ההטבות של משרד הבינוי והשיכון מיועדות למי שאין לו דירה. ל' + s.label + ' חלים מס הרכישה ושיעור המימון שבתוכנית שלמעלה.') + '</p>') +
        '<p class="nlph-fine">' + esc(BU.help_out) + '</p>';
    }
    draw();
  } });
})();
