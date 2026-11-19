/* NadLan Instruments · mquick v1 (1.72.587; v2 1.72.588: the amount field first, id-scoped rules over the theme, the tools switcher; HAD-675, Ben 5.11.2026): the quick mortgage calculator at the top of
   /mortgage-calculator/. Three ways in (the loan, the price and equity, or the payment you can carry), a term and whose average
   mix: all the banks or one bank. The answer is the first monthly payment (or the loan that payment carries), the total repaid and
   the interest, at the Bank of Israel average track mix and effective rates of the latest month (data boi-mortgage.json,
   by_bank: TamInt010.xls). Spitzer schedule per track, monthly rate = (1 + e)^(1/12) - 1, CPI tracks with the index unchanged.
   1,000,000 ILS over 25 years at the system mix of 2026-09 gives 5,428 ILS (the page states the same number). Pure math in NLMQ.
   v3 (HAD-675, English twin /en/mortgage-calculator/): when the tool's section says lang="en" (NadLanInstruments.langOf), every
   word is English, the surface is LTR (shekel sign before the number), bank names come from by_bank.banks[].en, months are English,
   numbers en-US, and the two buttons point at the English page's own anchors (#amortization-schedule, #mortgage-market). An extra
   style block (#nlmq-css-en) is added only in English. The Hebrew surface is byte-identical to v2.
   v4 (round E, HAD-675, 6.11.2026; benchmark row 23 "local defaults"): in "לפי מחיר והון עצמי" a compact select "עיר (מחיר חציוני,
   4 חדרים)" lists homes.medians of boi-mortgage.json (the Tax Authority's closed-deal medians): Israel first, then the 24 cities by
   name. A city puts its median 4-room price in the price field and shows its quarter ("חציון 1-3.2026, רשות המסים"); typing another
   price clears the city. Default: no city, so the example 1,600,000 / 400,000 and every other line stay as in v3. English names
   (the data has none) are the map of the English market block (inc/mortgage-market.php nadlan_mm_city_en, live since 1.72.589); a
   name missing from it stays Hebrew with lang="he". Pure part: NLMQ.cityList / NLMQ.quarterEn (node test).
   v5 (round G, T8, HAD-675, 6.11.2026; benchmark row "taxes, insurance or HOA inside the monthly figure"): under the result, two
   optional fields, "ביטוח חיים ומבנה" and "ארנונה וועד בית" (monthly, in shekels). They start EMPTY: there is no official price
   table for mortgage insurance, so no number is invented and no zero is shown. Once a sum is typed, "העלות החודשית של הדירה" = the
   payment + the typed costs, with only the typed parts in the breakdown, in all three modes; the copied text adds the line. A note
   names the Capital Market Authority's comparison calculators (life.cma.gov.il, dira.cma.gov.il; both checked 6.11.2026). Pure part:
   NLMQ.fullCost(pay, ins, arn) (node test). Everything else is v4. */
/* v6 (HAD-793, 19.11.2026, gap 23 of the long film): French and Russian twins (/fr/mortgage-calculator/, /ru/mortgage-calculator/).
   The section's own lang (fr | ru, printed by inc/instruments.php) picks a third and fourth dictionary: every word, the number format
   (fr-FR, ru-RU: "5 428 ₪"), months, quarters, bank and city names. LTR like English. Hebrew and English output unchanged. */
(function () {
  'use strict';
  var TR = ['fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi'];
  function payPer1(bb, bank, i, years) {  // the first payment on 1 ILS at a bank's average mix and rates of month index i
    var mix = bb.mix[bank], rate = bb.rate[bank], n = years * 12, tot = 0, pay = 0, k;
    if (!mix || !rate) return 0;
    for (k = 0; k < TR.length; k++) tot += +mix[TR[k]][i] || 0;
    if (!(tot > 0)) return 0;
    for (k = 0; k < TR.length; k++) {
      var p = (+mix[TR[k]][i] || 0) / tot, r = Math.pow(1 + (+rate[TR[k]][i] || 0) / 100, 1 / 12) - 1;
      pay += r > 0 ? p * r / (1 - Math.pow(1 + r, -n)) : p / n;
    }
    return pay;
  }
  function solve(v, bb) {
    var i = bb.months.length - 1, per1 = payPer1(bb, v.bank, i, v.years), loan, pay;
    if (v.mode === 'pay') { pay = Math.max(0, v.pay); loan = per1 > 0 ? pay / per1 : 0; }
    else { loan = v.mode === 'price' ? Math.max(0, v.price - v.equity) : Math.max(0, v.amount); pay = loan * per1; }
    var n = v.years * 12, total = pay * n;
    return { loan: loan, pay: pay, total: total, interest: Math.max(0, total - loan), ltv: v.mode === 'price' && v.price > 0 ? loan / v.price : null, month: bb.months[i], per1: per1 };
  }
  /* v4: the city list of the price mode, Israel first, then the cities by name (Hebrew order; English order in English) */
  var CITY_EN = {
    'ישראל': 'All of Israel', 'אילת': 'Eilat', 'אשדוד': 'Ashdod', 'אשקלון': 'Ashkelon', 'באר שבע': 'Beersheba', 'בני ברק': 'Bnei Brak',
    'בת ים': 'Bat Yam', 'גבעתיים': 'Givatayim', 'הוד השרון': 'Hod HaSharon', 'הרצליה': 'Herzliya', 'חולון': 'Holon', 'חיפה': 'Haifa',
    'יבנה': 'Yavne', 'ירושלים': 'Jerusalem', 'כפר סבא': 'Kfar Saba', 'מודיעין מכבים רעות': "Modi'in-Maccabim-Re'ut", 'נתניה': 'Netanya',
    'פתח תקווה': 'Petah Tikva', 'קריית אונו': 'Kiryat Ono', 'ראשון לציון': 'Rishon LeZion', 'רחובות': 'Rehovot', 'רמת גן': 'Ramat Gan',
    'רמת השרון': 'Ramat HaSharon', 'רעננה': "Ra'anana", 'תל אביב יפו': 'Tel Aviv-Yafo'
  };
  function cityList(D, en) {
    var M = D && D.homes && D.homes.medians, out = [], cs = [];
    if (!M) return out;
    function row(k, he, v) { return v && v.r4 && +v.r4.median > 0 ? { k: k, he: he, en: CITY_EN[he] || null, median: +v.r4.median, quarter: String(v.r4.quarter || '') } : null; }
    var il = row('il', 'ישראל', M.il); if (il) out.push(il);
    Object.keys(M.city || {}).forEach(function (c) { var r = row(c, c, M.city[c]); if (r) cs.push(r); });
    cs.sort(function (a, b) { return en ? (a.en || a.he).localeCompare(b.en || b.he, 'en') : a.he.localeCompare(b.he, 'he'); });
    return out.concat(cs);
  }
  var CITY_FR = { 'ישראל': 'Tout Israël', 'באר שבע': 'Beer-Sheva', 'ירושלים': 'Jérusalem', 'חיפה': 'Haïfa', 'פתח תקווה': 'Petah-Tikva', 'תל אביב יפו': 'Tel-Aviv-Jaffa', 'מודיעין מכבים רעות': "Modiin-Maccabim-Re'ut" };
  var CITY_RU = {
    'ישראל': 'Весь Израиль', 'אילת': 'Эйлат', 'אשדוד': 'Ашдод', 'אשקלון': 'Ашкелон', 'באר שבע': 'Беэр-Шева', 'בני ברק': 'Бней-Брак', 'בת ים': 'Бат-Ям',
    'גבעתיים': 'Гиватаим', 'הוד השרון': 'Ход-ха-Шарон', 'הרצליה': 'Герцлия', 'חולון': 'Холон', 'חיפה': 'Хайфа', 'יבנה': 'Явне', 'ירושלים': 'Иерусалим',
    'כפר סבא': 'Кфар-Саба', 'מודיעין מכבים רעות': 'Модиин-Маккабим-Реут', 'נתניה': 'Нетания', 'פתח תקווה': 'Петах-Тиква', 'קריית אונו': 'Кирьят-Оно',
    'ראשון לציון': 'Ришон-ле-Цион', 'רחובות': 'Реховот', 'רמת גן': 'Рамат-Ган', 'רמת השרון': 'Рамат-ха-Шарон', 'רעננה': 'Раанана', 'תל אביב יפו': 'Тель-Авив-Яффо'
  };
  function quarterX(q, l) { var m = /^(1-3|4-6|7-9|10-12)\.(\d{4})$/.exec(String(q)); if (!m) return String(q); var k = { '1-3': 1, '4-6': 2, '7-9': 3, '10-12': 4 }[m[1]]; return l === 'ru' ? ['I', 'II', 'III', 'IV'][k - 1] + ' кв. ' + m[2] : 'T' + k + ' ' + m[2]; }
  function quarterEn(q) { var m = /^(1-3|4-6|7-9|10-12)\.(\d{4})$/.exec(String(q)); return m ? { '1-3': 'Q1', '4-6': 'Q2', '7-9': 'Q3', '10-12': 'Q4' }[m[1]] + ' ' + m[2] : String(q); }
  /* v5: the full monthly cost; a part that was not typed (0, empty or not a number) stays out of the sum and of the breakdown */
  function fullCost(pay, ins, arn) { var a = ins > 0 ? ins : 0, b = arn > 0 ? arn : 0; return { total: (pay > 0 ? pay : 0) + a + b, ins: a, arn: b, any: a + b > 0 }; }
  window.NLMQ = { payPer1: payPer1, solve: solve, TR: TR, cityList: cityList, quarterEn: quarterEn, quarterX: quarterX, CITY_EN: CITY_EN, CITY_RU: CITY_RU, fullCost: fullCost };
  if (!window.NadLanInstruments) return;

  /* 1.72.588: the tools switcher on the mortgage page. Without scripts every panel shows (readers, search engines, AI answers);
     with scripts one panel at a time, chosen from the chips (MoneySavingExpert's pattern), never a table of contents. #tool-xxx opens a panel. */
  function wireSwitch() {
    ensureCss();
    [].forEach.call(document.querySelectorAll('.nlmx-sw:not([data-on])'), function (sw) {
      sw.setAttribute('data-on', '1');
      var bs = [].slice.call(sw.querySelectorAll('button[data-sw]')), ps = bs.map(function (b) { return document.getElementById(b.getAttribute('data-sw')); });
      function show(id, scroll) {
        bs.forEach(function (b, i) { var on = b.getAttribute('data-sw') === id; b.setAttribute('aria-pressed', String(on)); if (ps[i]) ps[i].hidden = !on; });
        if (scroll) { var p = document.getElementById(id); if (p && p.scrollIntoView) p.scrollIntoView({ block: 'start', behavior: 'smooth' }); }
      }
      bs.forEach(function (b) { b.addEventListener('click', function () { var id = b.getAttribute('data-sw'); show(id, false); try { history.replaceState(null, '', '#' + id); } catch (e) { /* file or sandbox */ } }); });
      var h = (location.hash || '').slice(1), first = bs.length ? bs[0].getAttribute('data-sw') : '';
      show(bs.some(function (b) { return b.getAttribute('data-sw') === h; }) ? h : first, !!h && h.indexOf('tool-') === 0);
      document.addEventListener('click', function (e) { var a = e.target && e.target.closest ? e.target.closest('a[href^="#tool-"]') : null; if (a) { var id = a.getAttribute('href').slice(1); if (document.getElementById(id)) { e.preventDefault(); show(id, true); } } });
    });
  }
  var NI = window.NadLanInstruments, esc = NI.esc;
  var nf = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function ils(x) { return nf.format(Math.round(x || 0)) + ' ₪'; }
  function num(s) { var n = parseFloat(String(s).replace(/[^\d.]/g, '')); return isFinite(n) ? n : NaN; }
  var HEM = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
  function month(ym) { var p = String(ym).split('-'); return p.length === 2 ? (HEM[+p[1] - 1] || p[1]) + ' ' + p[0] : ym; }
  var nfEn = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
  function ilsEn(x) { return '₪' + nfEn.format(Math.round(x || 0)); }
  var ENM = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  function monthEn(ym) { var p = String(ym).split('-'); return p.length === 2 ? (ENM[+p[1] - 1] || p[1]) + ' ' + p[0] : ym; }
 var nfFr = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 }), nfRu = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 0 });
  function ilsFr(x) { return nfFr.format(Math.round(x || 0)) + '\u00a0₪'; }
  function ilsRu(x) { return nfRu.format(Math.round(x || 0)) + '\u00a0₪'; }
  var FRM = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
  var RUM = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'];
  function monthL(ym, M) { var p = String(ym).split('-'); return p.length === 2 ? (M[+p[1] - 1] || p[1]) + ' ' + p[0] : ym; }
  var CMA = '<a href="https://life.cma.gov.il/" target="_blank" rel="noopener">', CMB = '<a href="https://dira.cma.gov.il/" target="_blank" rel="noopener">';
  /* v6: the French and Russian dictionaries; the sentence builders take the computed numbers already formatted */
  var XL = {
    fr: {
      T: { all: 'Toutes les banques', who_all: 'toutes les banques', h: 'Simulateur de crédit immobilier', amount: 'Montant du prêt', price: 'Prix du logement', equity: 'Apport personnel',
        pay: 'La mensualité qui vous convient', ml: 'Vous pouvez aussi calculer', m_amount: 'Par montant', m_price: 'Par prix et apport', m_pay: 'Par mensualité',
        tl: 'Durée', yr: ' ans', bl: 'Taux et répartition moyens de', principal: 'Capital', interest: 'Intérêts',
        cta: '<a class="nlmq__btn is-main" href="#regles">Les règles de la Banque d’Israël</a><a class="nlmq__btn" href="#questions">Questions fréquentes</a>',
        copy: 'Copier le résultat', copied: 'Copié', prompt: 'Copiez le résultat', city: 'Ville (prix médian, 4 pièces)', nocity: 'Choisir une ville',
        xl: 'Autres coûts mensuels, si vous les connaissez', ins: 'Assurance vie et habitation', arn: 'Arnona et charges de l’immeuble',
        tl2: 'Coût mensuel total du logement', tp: 'mensualité', ti: 'assurances', ta: 'arnona et charges',
        xn: 'La banque exige une assurance vie et une assurance du bâtiment, et c’est vous qui choisissez l’assureur. Comparez les prix auprès de l’Autorité des marchés de capitaux (en hébreu) : ' + CMA + 'assurance vie du prêt</a> · ' + CMB + 'assurance du bâtiment</a>.',
        cl: 'Coût mensuel total avec les coûts saisis : ' },
      IL: ilsFr, NF: nfFr, MO: function (ym) { return monthL(ym, FRM); }, bank: function (n) { return 'la banque ' + n; },
      banks: { hapoalim: 'Hapoalim', leumi: 'Leumi', discount: 'Discount', mizrahi: 'Mizrahi-Tefahot', fibi: 'Banque internationale (FIBI)', mercantile: 'Mercantile', jerusalem: 'Banque de Jérusalem' },
      city: function (c) { return CITY_FR[c.he] || c.en || c.he; }, cq: function (c) { return 'Médiane, ' + quarterX(c.quarter, 'fr') + ', Autorité fiscale israélienne'; },
      olPay: 'Le prêt que cette mensualité permet', olFirst: 'Première mensualité',
      sub: function (pay, tot, int, withPay) { return (withPay ? 'Mensualité <bdi>' + pay + '</bdi> · ' : '') + 'Total remboursé <bdi>' + tot + '</bdi> · dont intérêts <bdi>' + int + '</bdi>'; },
      ltv: function (pct, over) { return 'Quotité de financement <bdi>' + pct + '\u00a0%</bdi>' + (over ? ' : au-dessus de 75\u00a0%, le maximum de la Banque d’Israël pour un logement unique (70\u00a0% pour un logement de remplacement, 50\u00a0% pour un logement supplémentaire).' : ' (jusqu’à 75\u00a0% pour un logement unique, 70\u00a0% pour un logement de remplacement, 50\u00a0% pour un logement supplémentaire).'); },
      src: function (who, mon, link) { return 'Amortissement à mensualités constantes (Spitzer) ; les cinq tranches à la répartition et aux taux effectifs moyens de ' + who + ' en ' + mon + ', tranches indexées sans variation de l’indice. Source : ' + (link ? '<a href="' + link + '" target="_blank" rel="noopener">Banque d’Israël, comparaison des taux des prêts au logement</a>' : 'Banque d’Israël') + '. Une moyenne, pas une offre personnelle.'; },
      copyTx: function (loan, yrs, who, mon, pay, tot) { return 'Un prêt de ' + loan + ' sur ' + yrs + ' ans à la répartition moyenne de ' + who + ' en ' + mon + ' : première mensualité ' + pay + ', total remboursé ' + tot + '.'; },
      cityTx: function (c) { return ' Prix du logement : la médiane des ventes de 4 pièces à ' + (CITY_FR[c.he] || c.en || c.he) + ', ' + quarterX(c.quarter, 'fr') + ', Autorité fiscale israélienne.'; }
    },
    ru: {
      T: { all: 'Все банки', who_all: 'всех банков', h: 'Ипотечный калькулятор', amount: 'Сумма ипотеки', price: 'Цена квартиры', equity: 'Собственные средства',
        pay: 'Комфортный ежемесячный платёж', ml: 'Можно рассчитать и', m_amount: 'По сумме', m_price: 'По цене и взносу', m_pay: 'По платежу',
        tl: 'Срок', yr: ' лет', bl: 'Средние ставки и состав', principal: 'Основной долг', interest: 'Проценты',
        cta: '<a class="nlmq__btn is-main" href="#pravila">Правила Банка Израиля</a><a class="nlmq__btn" href="#voprosy">Частые вопросы</a>',
        copy: 'Скопировать результат', copied: 'Скопировано', prompt: 'Скопируйте результат', city: 'Город (медианная цена, 4 комнаты)', nocity: 'Выберите город',
        xl: 'Другие ежемесячные расходы, если вы их знаете', ins: 'Страхование жизни и строения', arn: 'Арнона и ваад байт',
        tl2: 'Полная ежемесячная стоимость жилья', tp: 'платёж', ti: 'страховки', ta: 'арнона и ваад байт',
        xn: 'Банк требует страхование жизни и страхование строения, а страховую компанию выбираете вы. Сравнить цены можно на сайте Управления рынка капитала (на иврите): ' + CMA + 'страхование жизни по ипотеке</a> · ' + CMB + 'страхование строения</a>.',
        cl: 'Полная ежемесячная стоимость с введёнными расходами: ' },
      IL: ilsRu, NF: nfRu, MO: function (ym) { return monthL(ym, RUM); }, bank: function (n) { return 'банка ' + n; },
      banks: { hapoalim: 'Апоалим', leumi: 'Леуми', discount: 'Дисконт', mizrahi: 'Мизрахи-Тфахот', fibi: 'Первый международный', mercantile: 'Меркантиль', jerusalem: 'Банк Иерусалим' },
      city: function (c) { return CITY_RU[c.he] || c.en || c.he; }, cq: function (c) { return 'Медиана, ' + quarterX(c.quarter, 'ru') + ', Налоговое управление Израиля'; },
      olPay: 'Ипотека, которую покрывает этот платёж', olFirst: 'Первый ежемесячный платёж',
      sub: function (pay, tot, int, withPay) { return (withPay ? 'Платёж <bdi>' + pay + '</bdi> · ' : '') + 'Всего выплат <bdi>' + tot + '</bdi> · из них проценты <bdi>' + int + '</bdi>'; },
      ltv: function (pct, over) { return 'Доля финансирования <bdi>' + pct + '%</bdi>' + (over ? ': выше 75%, максимума Банка Израиля для единственного жилья (70% при замене жилья, 50% для дополнительного жилья).' : ' (до 75% для единственного жилья, 70% при замене жилья, 50% для дополнительного жилья).'); },
      src: function (who, mon, link) { return 'Аннуитетный график (Шпицер); пять треков по среднему составу и эффективным ставкам ' + who + ' за ' + mon + ', индексируемые треки без изменения индекса. Источник: ' + (link ? '<a href="' + link + '" target="_blank" rel="noopener">Банк Израиля, сравнение ставок по жилищным кредитам</a>' : 'Банк Израиля') + '. Это среднее значение, а не персональное предложение.'; },
      copyTx: function (loan, yrs, who, mon, pay, tot) { return 'Ипотека ' + loan + ' на ' + yrs + ' лет по среднему составу ' + who + ' за ' + mon + ': первый платёж ' + pay + ', всего выплат ' + tot + '.'; },
      cityTx: function (c) { return ' Цена квартиры: медиана сделок с 4 комнатами, ' + (CITY_RU[c.he] || c.en || c.he) + ', ' + quarterX(c.quarter, 'ru') + ', Налоговое управление Израиля.'; }
    }
  };
  var CSS_EN = '#nlmq[dir="ltr"]{font-family:"IBM Plex Sans","IBM Plex Sans Hebrew",system-ui,sans-serif}'
    + '#nlmq[dir="ltr"] h2.nlmq__h{font-family:"IBM Plex Sans",system-ui,sans-serif!important}'
    + '#nlmq[dir="ltr"] .nlmq__in input{text-align:left}#nlmq[dir="ltr"] .nlmq__src{direction:ltr}';
  var CSS = '.nlmq{font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#12202A;background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:16px;display:flex;flex-direction:column;gap:16px;margin:8px 0 16px}'
    + '.nlmq *{box-sizing:border-box}.nlmq .nlmq__h{margin:0!important;font:600 18px/26px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}'
    + '.nlmq__lab{display:block;font-size:13px;line-height:18px;font-weight:500;color:#3E4C58;margin:0 0 8px}'
    + '.nlmq__seg{display:grid;gap:8px}.nlmq__seg--3{grid-template-columns:repeat(3,minmax(0,1fr))}.nlmq__seg--4{grid-template-columns:repeat(4,minmax(0,1fr))}'
    + '.nlmq button,.nlmq a.nlmq__btn{font-family:inherit;cursor:pointer}'
    + '.nlmq__seg button{min-height:44px;border-radius:2px;border:1px solid #D3DCE2;background:#fff;color:#3E4C58;font-size:14px;line-height:1.2;padding:4px 6px}'
    + '.nlmq__seg button[aria-pressed="true"]{background:#2F6F86;border-color:#2F6F86;color:#fff;font-weight:600}'
    + '.nlmq__chips{display:flex;flex-wrap:wrap;gap:8px}.nlmq__chips button{min-height:44px;padding:0 14px;border-radius:999px;border:1px solid #D3DCE2;background:#fff;color:#3E4C58;font-size:14px}'
    + '.nlmq__chips button[aria-pressed="true"]{background:#2F6F86;border-color:#2F6F86;color:#fff;font-weight:600}'
    + '.nlmq__in{display:flex;align-items:center;gap:8px;height:48px;padding:0 12px;border:1px solid #2F6F86;border-radius:2px;background:#fff}'
    + '.nlmq__in input{flex:1 1 auto;min-width:0;border:0!important;outline:0;background:transparent!important;font:400 20px/1 "IBM Plex Mono",ui-monospace,monospace!important;color:#12202A;text-align:right;padding:0!important;box-shadow:none!important;height:auto!important}'
    + '.nlmq__in span{font:400 16px/1 "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}'
    + '.nlmq__row{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:12px}'
    + '.nlmq__out{display:flex;flex-direction:column;gap:6px;border-top:1px solid #D3DCE2;padding-top:12px}'
    + '.nlmq__ol{font-size:13px;line-height:18px;font-weight:500;color:#3E4C58}.nlmq__fig{font:500 40px/44px "IBM Plex Mono",ui-monospace,monospace;color:#12202A}'
    + '.nlmq__sub{font:400 13px/20px "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}.nlmq__bar{display:flex;height:10px;border-radius:2px;overflow:hidden;background:#E7EEF2}'
    + '.nlmq__bar i{display:block;height:100%}.nlmq__bar i.p{background:#F2D15A}.nlmq__bar i.r{background:#8E7CC3}'
    + '.nlmq__key{display:flex;gap:16px;font-size:12px;line-height:16px;color:#5E6A75}.nlmq__key span{display:inline-flex;align-items:center;gap:4px}.nlmq__key b{display:inline-block;width:10px;height:10px}'
    + '.nlmq__ltv{font-size:14px;line-height:20px;color:#3E4C58}.nlmq__ltv.is-over bdi{text-decoration:underline;text-decoration-color:#C42550;text-decoration-thickness:2px;text-underline-offset:5px;color:#12202A}'
    + '.nlmq__src{margin:0;font:400 12px/18px "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}.nlmq__src a{color:#2F6F86}'
    + '.nlmq__cta{display:flex;flex-direction:column;gap:8px}@media (min-width:700px){.nlmq__cta{flex-direction:row;flex-wrap:wrap}}'
    + '.nlmq a.nlmq__btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 18px;border-radius:2px;border:1px solid #2F6F86;background:#fff;color:#2F6F86!important;text-decoration:none!important;font-weight:600;font-size:15px}'
    + '.nlmq a.nlmq__btn.is-main{background:#2F6F86;color:#fff!important}'
    + '.nlmq__copy{align-self:flex-start;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid #D3DCE2;background:#fff;color:#3E4C58;font-size:14px}'
    + '.nlmq button:focus-visible,.nlmq a:focus-visible,.nlmq__in:focus-within{outline:2px solid #2F6F86;outline-offset:2px}'
    + '@media (min-width:900px){.nlmq{padding:24px}}'
    + '#nlmq h2.nlmq__h{margin:0!important;padding:0!important;font-size:17px!important;line-height:24px!important;color:#3E4C58!important;border:0!important;font-weight:600!important}#nlmq h2.nlmq__h::before,#nlmq h2.nlmq__h::after{display:none!important}'
    + '#nlmq p.nlmq__src{margin:0!important;font:400 12px/18px "IBM Plex Mono",ui-monospace,monospace!important;color:#5E6A75!important}'
    + '#nlmq .nlmq__seg button{border-radius:2px!important;padding:4px 6px!important;min-height:44px!important;font-size:14px!important;box-shadow:none!important}#nlmq .nlmq__chips button,#nlmq button.nlmq__copy{border-radius:999px!important;box-shadow:none!important;min-height:44px!important}'
    + '#nlmq .nlmq__seg--3 button{font-size:13px!important}#nlmq .nlmq__modes{margin-top:-6px}'
    + '.nlmx-sw{margin:8px 0 18px}.nlmx-sw__chips{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 14px}.nlmx-sw__chips button{min-height:44px;padding:0 14px;border-radius:999px!important;border:1px solid #D3DCE2;background:#fff;color:#3E4C58;font:500 14px/1.2 "IBM Plex Sans Hebrew",system-ui,sans-serif;cursor:pointer;box-shadow:none!important}'
    + '.nlmx-sw__chips button[aria-pressed="true"]{background:#2F6F86;border-color:#2F6F86;color:#fff;font-weight:600}.nlmx-sw__chips button:focus-visible{outline:2px solid #2F6F86;outline-offset:2px}.nlmx-pane[hidden]{display:none!important}'
    /* v4: the city select (id-scoped with !important: the theme restyles plain selects) */
    + '#nlmq .nlmq__city{max-width:440px}#nlmq .nlmq__city[hidden],#nlmq .nlmq__cq[hidden]{display:none!important}#nlmq .nlmq__sel{padding:0 6px!important}'
    + '#nlmq .nlmq__sel select{flex:1 1 auto;min-width:0;width:100%!important;max-width:100%!important;height:46px!important;min-height:44px!important;margin:0!important;padding:0 6px!important;border:0!important;border-radius:0!important;outline:0;box-shadow:none!important;background:transparent!important;-webkit-appearance:menulist!important;appearance:auto!important;font:400 16px/1.2 "IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif!important;color:#12202A!important;cursor:pointer;text-overflow:ellipsis}'
    + '#nlmq .nlmq__cq{display:block;margin:6px 0 0!important;font:400 12px/18px "IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace!important;color:#5E6A75!important}'
    /* v5: the full monthly cost (two fields side by side, also on a phone) */
    + '#nlmq .nlmq__more{display:flex;flex-direction:column;gap:10px}#nlmq .nlmq__x2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;align-items:end}'
    + '#nlmq .nlmq__x2 .nlmq__in{height:46px;padding:0 10px}#nlmq .nlmq__x2 .nlmq__in input{font-size:18px!important}#nlmq .nlmq__x2 .nlmq__lab{margin:0 0 6px!important}'
    + '#nlmq .nlmq__tot{display:flex;flex-direction:column;gap:2px;background:#F6F8F9;border-inline-start:3px solid #2F6F86;padding:10px 12px}#nlmq .nlmq__tot[hidden]{display:none!important}'
    + '#nlmq .nlmq__tl{font-size:13px;line-height:18px;color:#3E4C58}#nlmq .nlmq__tf{font:500 26px/32px "IBM Plex Mono",ui-monospace,monospace;color:#12202A}#nlmq .nlmq__tb{font:400 12px/18px "IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace;color:#5E6A75}'
    + '#nlmq p.nlmq__xn{margin:0!important;font-size:12px!important;line-height:18px!important;color:#5E6A75!important}#nlmq p.nlmq__xn a{color:#2F6F86!important}'
    /* v5: the source sentence in the text face (the mono face fell back to a Courier-like font for running Hebrew and Latin text) */
    + '#nlmq p.nlmq__src{font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif!important}#nlmq[dir="ltr"] p.nlmq__src{font-family:"IBM Plex Sans",system-ui,sans-serif!important}';

  NI.register('mquick', {
    custom: function (root, data) {
      var D = data.boim || data.d0, bb = D && D.by_bank;
      if (!bb || !bb.months) return;
      ensureCss();
      var EN = !!(NI.langOf && NI.langOf(root) === 'en');  // v3: English on /en/ (the section's lang); Hebrew otherwise, unchanged
      var LS = root.closest ? root.closest('[lang]') : null, LX = LS ? String(LS.getAttribute('lang') || '').toLowerCase().slice(0, 2) : '';
      var X = !EN && XL[LX] ? XL[LX] : null, LTR = EN || !!X;  // v6: French or Russian
      if (LTR && !document.getElementById('nlmq-css-en')) { var st2 = document.createElement('style'); st2.id = 'nlmq-css-en'; st2.textContent = CSS_EN; document.head.appendChild(st2); }
      var IL = X ? X.IL : EN ? ilsEn : ils, NF = X ? X.NF : EN ? nfEn : nf, MO = X ? X.MO : EN ? monthEn : month;
      var T = X ? X.T : EN ? {
        all: 'All banks', who_all: 'all banks', h: 'Quick mortgage calculator', amount: 'Mortgage amount', price: 'Home price', equity: 'Your equity (down payment)',
        pay: 'The monthly payment that suits you', ml: 'You can also calculate', m_amount: 'By amount', m_price: 'By price and equity', m_pay: 'By monthly payment',
        tl: 'Term (years)', yr: '', bl: 'Average rate and mix of', principal: 'Principal', interest: 'Interest',
        cta: '<a class="nlmq__btn is-main" href="#amortization-schedule">Yearly amortization schedule</a><a class="nlmq__btn" href="#mortgage-market">Rates by bank this month</a>',
        copy: 'Copy the result', copied: 'Copied', prompt: 'Copy the result',
        city: 'City (median price, 4 rooms)', nocity: 'Choose a city',
        xl: 'Other monthly costs, if you know them', ins: 'Life and structure insurance', arn: 'Arnona and building fees',
        tl2: 'Full monthly cost of the home', tp: 'payment', ti: 'insurance', ta: 'arnona and building fees',
        xn: 'Banks require life and structure insurance, and you choose the insurer. Compare prices at the Capital Market Authority (in Hebrew): <a href="https://life.cma.gov.il/" target="_blank" rel="noopener">mortgage life insurance</a> · <a href="https://dira.cma.gov.il/" target="_blank" rel="noopener">structure insurance</a>.',
        cl: 'Full monthly cost with the costs I typed: '
      } : {
        all: 'כל הבנקים', who_all: 'כל הבנקים', h: 'מחשבון משכנתא מהיר', amount: 'סכום המשכנתא', price: 'מחיר הדירה', equity: 'הון עצמי',
        pay: 'ההחזר החודשי שמתאים לכם', ml: 'אפשר לחשב גם', m_amount: 'לפי סכום', m_price: 'לפי מחיר והון עצמי', m_pay: 'לפי החזר חודשי',
        tl: 'תקופה', yr: ' שנה', bl: 'ריבית ותמהיל ממוצעים לפי', principal: 'הקרן', interest: 'ריבית',
        cta: '<a class="nlmq__btn is-main" href="#mortgage-tool">תמהיל מלא, מסלולים ולוח סילוקין</a><a class="nlmq__btn" href="#bank-offer-check">יש לי הצעה מהבנק: לבדוק אותה</a>',
        copy: 'העתקת התוצאה', copied: 'הועתק', prompt: 'העתיקו את התוצאה',
        city: 'עיר (מחיר חציוני, 4 חדרים)', nocity: 'בחרו עיר',
        xl: 'עלויות נוספות בחודש, אם ידועות לכם', ins: 'ביטוח חיים ומבנה', arn: 'ארנונה וועד בית',
        tl2: 'העלות החודשית של הדירה', tp: 'החזר', ti: 'ביטוחים', ta: 'ארנונה וועד בית',
        xn: 'הבנק דורש ביטוח חיים וביטוח מבנה, ואתם בוחרים את חברת הביטוח. השוואת מחירים ברשות שוק ההון: <a href="https://life.cma.gov.il/" target="_blank" rel="noopener">ביטוח חיים למשכנתא</a> · <a href="https://dira.cma.gov.il/" target="_blank" rel="noopener">ביטוח מבנה</a>.',
        cl: 'העלות החודשית עם העלויות שהקלדתי: '
      };
      /* v4: the city select of the price mode; a city name without an English name stays Hebrew inside lang="he" */
      var CITIES = cityList(D, EN), cityBy = {}; CITIES.forEach(function (c) { cityBy[c.k] = c; });
      function cityName(c) { return X ? X.city(c) : EN ? (c.en || c.he) : c.he; }
      function cityQ(c) { return X ? X.cq(c) : EN ? 'Median, ' + quarterEn(c.quarter) + ', Israel Tax Authority' : 'חציון ' + c.quarter + ', רשות המסים'; }
      var citySel = CITIES.length ? '<div class="nlmq__city" data-f="price" hidden><label class="nlmq__lab" for="nlmq-c">' + T.city + '</label><div class="nlmq__in nlmq__sel"><select id="nlmq-c"><option value="">' + T.nocity + '</option>'
        + CITIES.map(function (c) { return '<option value="' + esc(c.k) + '"' + (LTR && cityName(c) === c.he ? ' lang="he"' : '') + '>' + esc(cityName(c)) + '</option>'; }).join('')
        + '</select></div><span class="nlmq__cq" hidden></span></div>' : '';
      // one money field; in English the shekel sign stands before the number (LTR), in Hebrew after it (as before)
      function fld(id, k, lab) { var inp = '<input id="' + id + '" inputmode="numeric" autocomplete="off" data-k="' + k + '">'; return '<div><label class="nlmq__lab" for="' + id + '">' + lab + '</label><div class="nlmq__in">' + (EN ? '<span>₪</span>' + inp : inp + '<span>₪</span>') + '</div></div>'; }
      var names = {}; (bb.banks || []).forEach(function (b) { names[b.k] = X ? (X.banks[b.k] || b.en || b.he) : EN ? ({ hapoalim: 'Hapoalim', leumi: 'Leumi', discount: 'Discount', mizrahi: 'Mizrahi-Tefahot', fibi: 'First International', mercantile: 'Mercantile', jerusalem: 'Jerusalem' }[b.k] || b.en || b.he) : b.he; }); names.system = T.all;
      var order = ['system'].concat(Object.keys(bb.rate).filter(function (k) { return k !== 'system'; }));
      var v = { mode: 'amount', amount: 1000000, price: 1600000, equity: 400000, pay: 6000, years: 25, bank: 'system', city: null, ins: 0, arn: 0 };
      var src = bb.src || {};
      var h = '<div class="nlmq" id="nlmq" dir="' + (LTR ? 'ltr' : 'rtl') + '" lang="' + (X ? LX : EN ? 'en' : 'he') + '">'
        + '<h2 class="nlmq__h">' + T.h + '</h2>'
        + '<div class="nlmq__row" data-f="amount">' + fld('nlmq-a', 'amount', T.amount) + '</div>'
        + citySel
        + '<div class="nlmq__row" data-f="price" hidden>' + fld('nlmq-p', 'price', T.price)
        + fld('nlmq-e', 'equity', T.equity) + '</div>'
        + '<div class="nlmq__row" data-f="pay" hidden>' + fld('nlmq-y', 'pay', T.pay) + '</div>'
        + '<div class="nlmq__modes"><span class="nlmq__lab" id="nlmq-ml">' + T.ml + '</span><div class="nlmq__seg nlmq__seg--3" role="group" aria-labelledby="nlmq-ml">'
        + '<button type="button" data-m="amount">' + T.m_amount + '</button><button type="button" data-m="price">' + T.m_price + '</button><button type="button" data-m="pay">' + T.m_pay + '</button></div></div>'
        + '<div><span class="nlmq__lab" id="nlmq-tl">' + T.tl + '</span><div class="nlmq__seg nlmq__seg--4" role="group" aria-labelledby="nlmq-tl">'
        + [15, 20, 25, 30].map(function (y) { return '<button type="button" data-y="' + y + '">' + y + T.yr + '</button>'; }).join('') + '</div></div>'
        + '<div><span class="nlmq__lab" id="nlmq-bl">' + T.bl + '</span><div class="nlmq__chips" role="group" aria-labelledby="nlmq-bl">'
        + order.map(function (k) { return '<button type="button" data-b="' + esc(k) + '">' + esc(names[k] || k) + '</button>'; }).join('') + '</div></div>'
        + '<div class="nlmq__out" aria-live="polite"><span class="nlmq__ol"></span><span class="nlmq__fig"></span><span class="nlmq__sub"></span>'
        + '<div class="nlmq__bar" aria-hidden="true"><i class="p"></i><i class="r"></i></div>'
        + '<div class="nlmq__key"><span><b style="background:#F2D15A"></b>' + T.principal + '</span><span><b style="background:#8E7CC3"></b>' + T.interest + '</span></div>'
        + '<span class="nlmq__ltv" hidden></span></div>'
        + '<div class="nlmq__more"><span class="nlmq__lab" id="nlmq-xl">' + T.xl + '</span><div class="nlmq__x2" role="group" aria-labelledby="nlmq-xl">'
        + fld('nlmq-xi', 'ins', T.ins).replace('data-k="', 'data-x="') + fld('nlmq-xa', 'arn', T.arn).replace('data-k="', 'data-x="') + '</div>'
        + '<div class="nlmq__tot" aria-live="polite" hidden><span class="nlmq__tl">' + T.tl2 + '</span><span class="nlmq__tf"></span><span class="nlmq__tb"></span></div>'
        + '<p class="nlmq__xn">' + T.xn + '</p></div>'
        + '<p class="nlmq__src"></p>'
        + '<div class="nlmq__cta">' + T.cta + '</div>'
        + '<button type="button" class="nlmq__copy">' + T.copy + '</button>'
        + '</div>';
      root.innerHTML = h;
      var q = function (s) { return root.querySelector(s); }, qa = function (s) { return [].slice.call(root.querySelectorAll(s)); };
      var last = null;
      function paint() {
        qa('[data-m]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-m') === v.mode)); });
        qa('[data-f]').forEach(function (r) { r.hidden = r.getAttribute('data-f') !== v.mode; });
        qa('[data-y]').forEach(function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-y') === v.years)); });
        qa('[data-b]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-b') === v.bank)); });
        var r = solve(v, bb); last = r;
        var who = v.bank === 'system' ? T.who_all : X ? X.bank(names[v.bank] || v.bank) : (EN ? '' : 'בנק ') + (names[v.bank] || v.bank);
        if (v.mode === 'pay') {
          q('.nlmq__ol').textContent = X ? X.olPay : EN ? 'The mortgage this payment carries' : 'המשכנתא שההחזר הזה נושא';
          q('.nlmq__fig').innerHTML = '<bdi>' + IL(r.loan) + '</bdi>';
        } else {
          q('.nlmq__ol').textContent = X ? X.olFirst : EN ? 'First monthly payment' : 'ההחזר החודשי הראשון';
          q('.nlmq__fig').innerHTML = '<bdi>' + IL(r.pay) + '</bdi>';
        }
        q('.nlmq__sub').innerHTML = X ? X.sub(IL(r.pay), IL(r.total), IL(r.interest), v.mode === 'pay') : EN
          ? (v.mode === 'pay' ? 'Payment <bdi>' + IL(r.pay) + '</bdi> · ' : '') + 'Total repaid <bdi>' + IL(r.total) + '</bdi> · of which interest <bdi>' + IL(r.interest) + '</bdi>'
          : (v.mode === 'pay' ? 'החזר <bdi>' + ils(r.pay) + '</bdi> · ' : '') + 'סך ההחזרים <bdi>' + ils(r.total) + '</bdi> · מזה ריבית <bdi>' + ils(r.interest) + '</bdi>';
        var tot = r.total > 0 ? r.total : 1;
        q('.nlmq__bar .p').style.width = (r.loan / tot * 100).toFixed(1) + '%';
        q('.nlmq__bar .r').style.width = (r.interest / tot * 100).toFixed(1) + '%';
        var lt = q('.nlmq__ltv');
        if (r.ltv != null) {
          var over = r.ltv > 0.75;
          lt.hidden = false; lt.className = 'nlmq__ltv' + (over ? ' is-over' : '');
          lt.innerHTML = X ? X.ltv(NF.format ? new Intl.NumberFormat(LX === 'fr' ? 'fr-FR' : 'ru-RU', { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(r.ltv * 100) : (r.ltv * 100).toFixed(1), over) : EN
            ? 'Loan to value <bdi>' + (r.ltv * 100).toFixed(1) + '%</bdi>' + (over ? ': above 75%, the Bank of Israel maximum for a single home (70% for a replacement home, 50% for an additional home).' : ' (up to 75% for a single home, 70% for a replacement home, 50% for an additional home).')
            : 'שיעור המימון <bdi>' + (r.ltv * 100).toFixed(1) + '%</bdi>' + (over ? ': מעל 75%, המימון המרבי של בנק ישראל לדירה יחידה (70% לדירה חלופית, 50% לדירה נוספת).' : ' (עד 75% לדירה יחידה, 70% לדירה חלופית, 50% לדירה נוספת).');
        } else { lt.hidden = true; }
        q('.nlmq__src').innerHTML = X ? X.src(esc(who), esc(MO(r.month)), (src.page_en || src.page) ? esc(src.page_en || src.page) : '') : EN
          ? 'Spitzer schedule; the five tracks at the average mix and effective rates of ' + esc(who) + ' in ' + esc(MO(r.month))
            + ', CPI-linked tracks with the index unchanged. Source: ' + ((src.page_en || src.page) ? '<a href="' + esc(src.page_en || src.page) + '" target="_blank" rel="noopener">Bank of Israel, interest rate comparisons for housing loans</a>' : 'Bank of Israel') + '. An average, not a personal offer.'
          : 'לוח שפיצר, חמשת המסלולים לפי התמהיל והריבית האפקטיבית הממוצעים של ' + esc(who) + ' ב' + esc(month(r.month))
            + ', במסלולים הצמודים בלי שינוי במדד. מקור: ' + (src.page ? '<a href="' + esc(src.page) + '" target="_blank" rel="noopener">בנק ישראל, השוואת ריביות בהלוואות לדיור</a>' : 'בנק ישראל') + '. ממוצע, לא הצעה אישית.';
        var fc = fullCost(r.pay, v.ins, v.arn), tb = q('.nlmq__tot');  // v5
        tb.hidden = !fc.any;
        if (fc.any) {
          q('.nlmq__tf').innerHTML = '<bdi>' + IL(fc.total) + '</bdi>';
          q('.nlmq__tb').innerHTML = [[T.tp, r.pay], [T.ti, fc.ins], [T.ta, fc.arn]].filter(function (x) { return x[1] > 0; })
            .map(function (x) { return x[0] + ' <bdi>' + NF.format(Math.round(x[1])) + '</bdi>'; }).join(' + ');
        }
      }
      qa('input[data-k]').forEach(function (inp) {
        var k = inp.getAttribute('data-k'); inp.value = NF.format(v[k]);
        inp.addEventListener('input', function () { var n = num(inp.value); if (isFinite(n)) { v[k] = n; if (k === 'price') cityOff(n); paint(); } });
        inp.addEventListener('blur', function () { inp.value = NF.format(v[k]); });
      });
      qa('input[data-x]').forEach(function (inp) {  // v5: empty until typed; an emptied field drops out of the sum
        var k = inp.getAttribute('data-x');
        inp.addEventListener('input', function () { var n = num(inp.value); v[k] = isFinite(n) && n > 0 ? n : 0; paint(); });
        inp.addEventListener('blur', function () { inp.value = v[k] > 0 ? NF.format(v[k]) : ''; });
      });
      /* v4: a city fills the price with its median 4-room deal; another typed price clears the city */
      var sel = q('#nlmq-c'), cq = q('.nlmq__cq');
      function cityOff(n) { if (v.city && cityBy[v.city] && n !== cityBy[v.city].median) { v.city = null; if (sel) sel.value = ''; if (cq) { cq.hidden = true; cq.textContent = ''; } } }
      if (sel) sel.addEventListener('change', function () {
        var c = cityBy[sel.value] || null; v.city = c ? c.k : null;
        if (c) { v.price = c.median; q('#nlmq-p').value = NF.format(c.median); cq.textContent = cityQ(c); cq.hidden = false; } else { cq.hidden = true; cq.textContent = ''; }
        paint();
      });
      root.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b || !root.contains(b)) return;
        if (b.hasAttribute('data-m')) { v.mode = b.getAttribute('data-m'); paint(); }
        else if (b.hasAttribute('data-y')) { v.years = +b.getAttribute('data-y'); paint(); }
        else if (b.hasAttribute('data-b')) { v.bank = b.getAttribute('data-b'); paint(); }
        else if (b.classList.contains('nlmq__copy') && last) {
          var who = v.bank === 'system' ? T.who_all : X ? X.bank(names[v.bank] || v.bank) : (EN ? '' : 'בנק ') + (names[v.bank] || v.bank);
          var cc = v.mode === 'price' && v.city ? cityBy[v.city] : null;  // v4: the city's median, when one was chosen
          var ct = !cc ? '' : X ? X.cityTx(cc) : EN ? ' Home price: the median 4-room deal in ' + cityName(cc) + ', ' + quarterEn(cc.quarter) + ', Israel Tax Authority.' : ' מחיר הדירה: חציון העסקאות של 4 חדרים ב' + cc.he + ', ' + cc.quarter + ', רשות המסים.';
          var tx = X ? X.copyTx(IL(last.loan), v.years, who, MO(last.month), IL(last.pay), IL(last.total)) + ct + '\n' + location.origin + location.pathname : EN
            ? 'A ' + IL(last.loan) + ' mortgage over ' + v.years + ' years at the average mix of ' + who + ' in ' + MO(last.month) + ': first payment ' + IL(last.pay) + ', total repaid ' + IL(last.total) + '.' + ct + '\n' + location.origin + location.pathname
            : 'משכנתא של ' + ils(last.loan) + ' ל־' + v.years + ' שנה, בתמהיל הממוצע של ' + who + ' ב' + month(last.month) + ': החזר ראשון ' + ils(last.pay) + ', סך ההחזרים ' + ils(last.total) + '.' + ct + '\n' + location.origin + location.pathname;
          var fx = fullCost(last.pay, v.ins, v.arn); if (fx.any) tx = tx.replace('\n' + location.origin, ' ' + T.cl + IL(fx.total) + '.\n' + location.origin);  // v5
          var done = function () { b.textContent = T.copied; setTimeout(function () { b.textContent = T.copy; }, 1600); };
          if (navigator.clipboard) navigator.clipboard.writeText(tx).then(done, function () { window.prompt(T.prompt, tx); }); else window.prompt(T.prompt, tx);
        }
      });
      paint();
    }
  });
  /* 1.72.590: the style is written once CSS is defined (1.72.588 ran the switcher before it and left an empty style element) */
  function ensureCss() { var s = document.getElementById('nlmq-css'); if (!s) { s = document.createElement('style'); s.id = 'nlmq-css'; document.head.appendChild(s); } if (!s.textContent) s.textContent = CSS; }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wireSwitch); else wireSwitch();
})();
