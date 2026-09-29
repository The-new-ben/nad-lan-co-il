/* ============================================================================
   NadLan buy-flow v1 - "build me an offer" (research spec 2026-07-05)
   ----------------------------------------------------------------------------
   Tesla-style configure > 2-field WhatsApp-first capture > honest Wolt-style
   dispatch animation > "what happens next" timeline. No payment, no invented
   prices: every money-shaped element is estimate-labeled or price-on-proposal.
   Self-contained: reads window.NADLAN_SHOWROOM, posts to nadlan/v1/lead with a
   structured context. Opens from any [data-act="rfp"][data-id=<unit>] button.
   ============================================================================ */
(function () {
  "use strict";
  var SR = window.NADLAN_SHOWROOM;
  if (!SR || !SR.config) return;

  var LANG = (document.documentElement.lang || "he").slice(0, 2);
  var T_ALL = {
    he: {
      title: "בנו לי הצעה", sub: "חינם, ללא התחייבות, לא נדרש תשלום",
      step_finish: "רמת גימור", step_extras: "מה לצרף להצעה?", step_contact: "לאן לשלוח?",
      finish_std: "מפרט היזם", finish_up: "משודרג", finish_prem: "פרימיום",
      finish_note: "התמחור המדויק יופיע בהצעה מהיזם, לפי מפרט המכר",
      ex_designer: "מעצב/ת פנים", ex_designer_d: "קונספט עיצוב ותקציב ריהוט לדירה הזו",
      ex_lawyer: "עו״ד מקרקעין", ex_lawyer_d: "בדיקת חוזה המכר והבטוחות",
      ex_mortgage: "יועץ משכנתא", ex_mortgage_d: "בדיקת מסגרת מימון ואישור עקרוני",
      ex_inspect: "בדק בית", ex_inspect_d: "בדיקת הדירה לפני מסירה",
      ex_furniture: "ריהוט", ex_furniture_d: "התעניינות בלבד, לא הזמנה",
      name: "שם פרטי", phone: "וואטסאפ / נייד",
      consent: "מסכים/ה שנדלן תעביר את הפנייה ליזם וליועצים שבחרתי",
      send: "שלחו את הבקשה", sending: "שולחים...",
      st1: "מנתחים את הבחירות שלך", st2: "מסמך הבקשה מוכן",
      st3: "נשלח לצוות נדלן לתיאום מול היזם", st4: "היועצים שבחרת יקבלו את הפנייה",
      done_t: "הבקשה בדרך", done_p: "ניצור קשר בוואטסאפ בדרך כלל תוך שעות ספורות, עם הצעה מסודרת לדירה שבחרת.",
      doc_view: "צפו במסמך הבקשה שלכם",
      next1: "הפנייה התקבלה במערכת", next2: "תיאום מול היזם", next3: "הצעה מרוכזת אליך",
      err: "השליחה נכשלה, נסו שוב או חייגו אלינו", close: "סגירה", back: "חזרה", cont: "המשך",
      unit: "דירה", floor: "קומה", skip: "דלגו, רק חברו אותי ליזם",
      est: "כל הנתונים הם אומדן בלבד ואינם הצעת מחיר מחייבת",
      doc_fail: "הפנייה התקבלה, אבל מסמך הבקשה לא נוצר. לא ניצור פנייה נוספת.", doc_retry: "ליצור את המסמך שוב", doc_pending: "המסמך בהכנה…", st2_wait: "מכינים את מסמך הבקשה"
    },
    en: {
      title: "Build me an offer", sub: "Free, no commitment, no payment required",
      step_finish: "Finish level", step_extras: "Add to your request?", step_contact: "Where to send it?",
      finish_std: "Developer spec", finish_up: "Upgraded", finish_prem: "Premium",
      finish_note: "Exact pricing appears in the developer's proposal, per the sale spec",
      ex_designer: "Interior designer", ex_designer_d: "Design concept and furniture budget for this unit",
      ex_lawyer: "Real estate lawyer", ex_lawyer_d: "Sale contract and guarantees review",
      ex_mortgage: "Mortgage advisor", ex_mortgage_d: "Financing check and pre-approval",
      ex_inspect: "Inspection (bedek)", ex_inspect_d: "Pre-delivery apartment inspection",
      ex_furniture: "Furniture", ex_furniture_d: "Interest only, not an order",
      name: "First name", phone: "WhatsApp / mobile",
      consent: "I agree that NadLan forwards my request to the developer and my chosen advisors",
      send: "Send my request", sending: "Sending...",
      st1: "Analyzing your choices", st2: "Request document ready",
      st3: "Sent to the NadLan team to coordinate with the developer", st4: "Your chosen advisors will receive the request",
      done_t: "Your request is on its way", done_p: "We usually reply on WhatsApp within a few hours with an organized proposal for your chosen apartment.",
      doc_view: "View your request document",
      next1: "Request received", next2: "Coordination with the developer", next3: "A consolidated proposal to you",
      err: "Sending failed, try again or call us", close: "Close", back: "Back", cont: "Continue",
      unit: "Apartment", floor: "Floor", skip: "Skip, just connect me to the developer",
      est: "All figures are estimates only and not a binding quote",
      doc_fail: "Your request was received, but the request document was not created. We will not create a second request.", doc_retry: "Create the document again", doc_pending: "The document is being prepared…", st2_wait: "Preparing the request document"
    },
    fr: {
      title: "Preparez-moi une offre", sub: "Gratuit, sans engagement, aucun paiement requis",
      step_finish: "Niveau de finition", step_extras: "Ajouter a votre demande ?", step_contact: "Ou l'envoyer ?",
      finish_std: "Spec promoteur", finish_up: "Ameliore", finish_prem: "Premium",
      finish_note: "Le prix exact figure dans la proposition du promoteur",
      ex_designer: "Architecte d'interieur", ex_designer_d: "Concept et budget mobilier pour ce logement",
      ex_lawyer: "Avocat immobilier", ex_lawyer_d: "Verification du contrat et des garanties",
      ex_mortgage: "Conseiller hypothecaire", ex_mortgage_d: "Verification du financement",
      ex_inspect: "Inspection", ex_inspect_d: "Inspection avant livraison",
      ex_furniture: "Mobilier", ex_furniture_d: "Interet seulement, pas une commande",
      name: "Prenom", phone: "WhatsApp / mobile",
      consent: "J'accepte que NadLan transmette ma demande au promoteur et aux conseillers choisis",
      send: "Envoyer ma demande", sending: "Envoi...",
      st1: "Analyse de vos choix", st2: "Document de demande pret",
      st3: "Envoye a l'equipe NadLan pour coordination avec le promoteur", st4: "Vos conseillers recevront la demande",
      done_t: "Votre demande est en route", done_p: "Nous repondons generalement sur WhatsApp en quelques heures avec une proposition organisee.",
      doc_view: "Voir votre document de demande",
      next1: "Demande recue", next2: "Coordination avec le promoteur", next3: "Une proposition consolidee pour vous",
      err: "Echec de l'envoi, reessayez", close: "Fermer", back: "Retour", cont: "Continuer",
      unit: "Logement", floor: "Etage", skip: "Passer, connectez-moi au promoteur",
      est: "Tous les chiffres sont des estimations, pas un devis contractuel",
      doc_fail: "Votre demande est recue, mais le document n'a pas ete cree. Aucune seconde demande ne sera creee.", doc_retry: "Creer le document a nouveau", doc_pending: "Le document est en preparation…", st2_wait: "Preparation du document"
    },
    ru: {
      title: "Подготовьте мне предложение", sub: "Бесплатно, без обязательств, без оплаты",
      step_finish: "Уровень отделки", step_extras: "Что добавить к запросу?", step_contact: "Куда отправить?",
      finish_std: "Спецификация застройщика", finish_up: "Улучшенная", finish_prem: "Премиум",
      finish_note: "Точная цена появится в предложении застройщика",
      ex_designer: "Дизайнер интерьера", ex_designer_d: "Концепция и бюджет мебели для этой квартиры",
      ex_lawyer: "Юрист по недвижимости", ex_lawyer_d: "Проверка договора и гарантий",
      ex_mortgage: "Ипотечный консультант", ex_mortgage_d: "Проверка финансирования",
      ex_inspect: "Приемка квартиры", ex_inspect_d: "Проверка перед передачей",
      ex_furniture: "Мебель", ex_furniture_d: "Только интерес, не заказ",
      name: "Имя", phone: "WhatsApp / телефон",
      consent: "Согласен, что NadLan передаст запрос застройщику и выбранным консультантам",
      send: "Отправить запрос", sending: "Отправка...",
      st1: "Анализируем ваш выбор", st2: "Документ запроса готов",
      st3: "Отправлено команде NadLan для координации с застройщиком", st4: "Выбранные консультанты получат запрос",
      done_t: "Запрос в пути", done_p: "Обычно отвечаем в WhatsApp в течение нескольких часов с организованным предложением.",
      doc_view: "Посмотреть документ запроса",
      next1: "Запрос получен", next2: "Координация с застройщиком", next3: "Консолидированное предложение вам",
      err: "Отправка не удалась, попробуйте снова", close: "Закрыть", back: "Назад", cont: "Далее",
      unit: "Квартира", floor: "Этаж", skip: "Пропустить, просто свяжите с застройщиком",
      est: "Все цифры - только оценка, не обязывающая цена",
      doc_fail: "Запрос получен, но документ не создан. Второй запрос не будет создан.", doc_retry: "Создать документ снова", doc_pending: "Документ готовится…", st2_wait: "Готовим документ запроса"
    },
    ar: {
      title: "جهزوا لي عرضا", sub: "مجانا، بدون التزام، لا حاجة للدفع",
      step_finish: "مستوى التشطيب", step_extras: "ماذا نضيف للطلب؟", step_contact: "اين نرسل؟",
      finish_std: "مواصفات المطور", finish_up: "محسن", finish_prem: "بريميوم",
      finish_note: "السعر الدقيق يظهر في عرض المطور حسب مواصفات البيع",
      ex_designer: "مصمم داخلي", ex_designer_d: "مفهوم تصميم وميزانية اثاث لهذه الشقة",
      ex_lawyer: "محامي عقارات", ex_lawyer_d: "فحص عقد البيع والضمانات",
      ex_mortgage: "مستشار رهن عقاري", ex_mortgage_d: "فحص التمويل والموافقة المبدئية",
      ex_inspect: "فحص الشقة", ex_inspect_d: "فحص قبل التسليم",
      ex_furniture: "اثاث", ex_furniture_d: "اهتمام فقط، ليس طلبية",
      name: "الاسم الشخصي", phone: "واتساب / جوال",
      consent: "اوافق ان تنقل نادلان طلبي للمطور والمستشارين الذين اخترتهم",
      send: "ارسلوا الطلب", sending: "جاري الارسال...",
      st1: "نحلل اختياراتك", st2: "مستند الطلب جاهز",
      st3: "ارسل لفريق نادلان للتنسيق مع المطور", st4: "المستشارون الذين اخترتهم سيستلمون الطلب",
      done_t: "طلبك في الطريق", done_p: "نرد عادة عبر واتساب خلال ساعات قليلة مع عرض منظم للشقة التي اخترت.",
      doc_view: "شاهدوا مستند طلبكم",
      next1: "استلم الطلب", next2: "تنسيق مع المطور", next3: "عرض موحد اليك",
      err: "فشل الارسال، حاولوا مجددا", close: "اغلاق", back: "رجوع", cont: "متابعة",
      unit: "شقة", floor: "طابق", skip: "تخطي، فقط اوصلوني بالمطور",
      est: "كل الارقام تقديرية فقط وليست عرض سعر ملزم",
      doc_fail: "استلمنا طلبك، لكن مستند الطلب لم ينشأ. لن ننشئ طلبا ثانيا.", doc_retry: "انشاء المستند مجددا", doc_pending: "المستند قيد التحضير…", st2_wait: "نحضر مستند الطلب"
    }
  };
  var T = T_ALL[LANG] || T_ALL.he;

  function project() {
    var key = new URLSearchParams(location.search).get("project") || SR.config.default_project;
    return (SR.projects && SR.projects[key]) || null;
  }
  function unitOf(id) {
    var p = project(); if (!p || !p.units) return null;
    for (var i = 0; i < p.units.length; i++) if (p.units[i].id === id) return p.units[i];
    return null;
  }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* UnitDesignRequest (design system v102, HAD-346 Batch 2): one request per unit. client_ref is made once per request; the
     lead is created once (its id and key kept); the document can be retried alone with the same client_ref (the server
     returns the same receipt, never a second document); the studio design is frozen when the buyer presses send. An answer
     that arrives for an older request never changes the screen of a newer one. */
  function ref() { var a = new Uint8Array(12); (window.crypto || {}).getRandomValues ? window.crypto.getRandomValues(a) : a.forEach(function (_, i) { a[i] = Math.random() * 256; }); return "b" + Array.prototype.map.call(a, function (x) { return ("0" + x.toString(16)).slice(-2); }).join(""); }
  function fresh(unit) { return { step: 1, unit: unit, finish: "std", extras: {}, busy: false, clientRef: ref(), leadId: 0, leadKey: "", design: null, doc: "", docUrl: "", docRef: "" }; }
  var state = fresh(null);

  var EXTRAS = [
    ["designer", "ex_designer", "ex_designer_d"],
    ["lawyer", "ex_lawyer", "ex_lawyer_d"],
    ["mortgage", "ex_mortgage", "ex_mortgage_d"],
    ["inspect", "ex_inspect", "ex_inspect_d"],
    ["furniture", "ex_furniture", "ex_furniture_d"]
  ];

  function overlay() {
    var el = document.getElementById("nlbuy");
    if (!el) {
      el = document.createElement("div");
      el.id = "nlbuy";
      el.setAttribute("dir", document.documentElement.dir || "rtl");
      document.body.appendChild(el);
      el.addEventListener("click", onClick);
    }
    return el;
  }
  function head(step) {
    var u = state.unit;
    var meta = u ? esc(T.unit) + " " + esc(u.label || u.id) + " · " + esc(T.floor) + " " + esc(u.floor) : "";
    return '<div class="nlbuy__head"><div><h3>' + esc(T.title) + "</h3><p>" + esc(T.sub) + '</p><small>' + meta + '</small></div>' +
      '<div class="nlbuy__dots">' + [1, 2, 3].map(function (i) { return '<i class="' + (i <= step ? "on" : "") + '"></i>'; }).join("") + "</div>" +
      '<button class="nlbuy__x" data-buy="close" aria-label="' + esc(T.close) + '">&#10005;</button></div>';
  }
  function render() {
    var el = overlay(), body = "";
    if (state.step === 1) {
      body = '<div class="nlbuy__cards">' + [["std", T.finish_std], ["up", T.finish_up], ["prem", T.finish_prem]].map(function (f) {
        return '<button class="nlbuy__card' + (state.finish === f[0] ? " on" : "") + '" data-buy="finish" data-v="' + f[0] + '"><b>' + esc(f[1]) + "</b></button>";
      }).join("") + "</div><p class='nlbuy__note'>" + esc(T.finish_note) + "</p>" +
      '<div class="nlbuy__nav"><button class="nlbuy__btn" data-buy="next">' + esc(T.cont) + "</button></div>";
    } else if (state.step === 2) {
      body = '<div class="nlbuy__list">' + EXTRAS.map(function (x) {
        var on = !!state.extras[x[0]];
        return '<button class="nlbuy__row' + (on ? " on" : "") + '" data-buy="extra" data-v="' + x[0] + '" aria-pressed="' + on + '"><span class="tick"></span><span><b>' + esc(T[x[1]]) + "</b><small>" + esc(T[x[2]]) + "</small></span></button>";
      }).join("") + "</div>" +
      '<div class="nlbuy__nav"><button class="nlbuy__btn nlbuy__btn--ghost" data-buy="back">' + esc(T.back) + '</button><button class="nlbuy__btn" data-buy="next">' + esc(T.cont) + '</button></div>' +
      '<button class="nlbuy__skip" data-buy="skipnext">' + esc(T.skip) + "</button>";
    } else if (state.step === 3) {
      body = '<div class="nlbuy__form">' +
        '<label><span>' + esc(T.name) + '</span><input type="text" id="nlbuy-name" autocomplete="given-name" required></label>' +
        '<label><span>' + esc(T.phone) + '</span><input type="tel" id="nlbuy-phone" autocomplete="tel" inputmode="tel" required dir="ltr"></label>' +
        '<label class="nlbuy__consent"><input type="checkbox" id="nlbuy-consent" checked><span>' + esc(T.consent) + "</span></label>" +
        '<p class="nlbuy__err" id="nlbuy-err" hidden>' + esc(T.err) + "</p></div>" +
        '<div class="nlbuy__nav"><button class="nlbuy__btn nlbuy__btn--ghost" data-buy="back">' + esc(T.back) + '</button>' +
        '<button class="nlbuy__btn nlbuy__btn--accent" data-buy="send" id="nlbuy-send">' + esc(T.send) + "</button></div>" +
        '<p class="nlbuy__note">' + esc(T.est) + "</p>";
    } else if (state.step === 4) {
      body = '<div class="nlbuy__stages" id="nlbuy-stages">' + [T.st1, T.st2, T.st3, T.st4].map(function (s, i) {
        return '<div class="nlbuy__stage" data-i="' + i + '"><span class="dot"></span><span>' + esc(s) + "</span></div>";
      }).join("") + "</div>";
    } else {
      var docBtn = state.doc === "ok" && state.docUrl ? '<a class="nlbuy__btn nlbuy__btn--accent" style="display:block;text-decoration:none;text-align:center;margin-bottom:9px;box-sizing:border-box" href="' + esc(state.docUrl) + '" target="_blank" rel="noopener">' + esc(T.doc_view) + "</a>"
        : state.doc === "failed" ? '<p class="nlbuy__err" role="alert" style="display:block">' + esc(T.doc_fail) + '</p><button class="nlbuy__btn nlbuy__btn--accent" data-buy="docretry" style="margin-bottom:9px"' + (state.busy ? " disabled" : "") + ">" + esc(state.busy ? T.sending : T.doc_retry) + "</button>"
        : state.doc === "pending" ? '<p class="nlbuy__note">' + esc(T.doc_pending) + "</p>" : "";
      body = '<div class="nlbuy__done"><h4>' + esc(T.done_t) + "</h4><p>" + esc(T.done_p) + "</p>" +
        '<ol class="nlbuy__next"><li class="on">' + esc(T.next1) + "</li><li>" + esc(T.next2) + "</li><li>" + esc(T.next3) + "</li></ol>" +
        docBtn +
        '<button class="nlbuy__btn" data-buy="close">' + esc(T.close) + "</button></div>";
    }
    var stepTitle = state.step === 1 ? T.step_finish : state.step === 2 ? T.step_extras : state.step === 3 ? T.step_contact : "";
    el.innerHTML = '<div class="nlbuy__scrim" data-buy="close"></div><div class="nlbuy__panel" role="dialog" aria-modal="true" aria-label="' + esc(T.title) + '">' +
      head(Math.min(state.step, 3)) + (stepTitle ? '<h4 class="nlbuy__step">' + esc(stepTitle) + "</h4>" : "") + body + "</div>";
    el.classList.add("is-open");
    var inp = document.getElementById("nlbuy-name");
    if (inp) inp.focus();
  }
  var opener = null; // the button that opened the dialog: the focus goes back to it
  function close() {
    var el = document.getElementById("nlbuy"); if (el) el.classList.remove("is-open");
    if (opener && document.contains(opener)) { try { opener.focus({ preventScroll: true }); } catch (e) {} }
  }

  function playStages(thenDone, mine) {
    var i = 0, waited = 0;
    function tick() {
      if (state.clientRef !== mine) return; // another request took the screen
      var rows = document.querySelectorAll("#nlbuy-stages .nlbuy__stage");
      // the second stage says "the request document is ready": it waits for the server's answer, and is never shown for a
      // document that failed
      if (i === 1 && state.doc === "pending" && waited < 12000) { waited += 300; setTimeout(tick, 300); return; }
      if (i === 1 && state.doc !== "ok") { setTimeout(thenDone, 300); return; }
      if (i < rows.length) { rows[i].classList.add("on"); i++; setTimeout(tick, 1100); }
      else { setTimeout(thenDone, 500); }
    }
    setTimeout(tick, 350);
  }
  function makeDoc(mine) {
    var p = project(), u = state.unit || {};
    state.doc = "pending";
    return fetch(SR.config.lead_endpoint.replace(/lead$/, "rfp"), {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        project: p ? p.slug.replace(/-(en|fr|ru|ar)$/, "") : "", unit: u.id || "",
        finish: state.finish, extras: Object.keys(state.extras).filter(function (k) { return state.extras[k]; }), lang: LANG,
        name: state.name || "", lead_id: state.leadId || 0, lead_key: state.leadKey || "",
        client_ref: mine, design: state.design
      })
    }).then(function (r2) { return r2.json().then(function (d2) { return { ok: r2.ok, d: d2 }; }); }).then(function (x) {
      if (state.clientRef !== mine) return; // a late answer for an older request: not this screen's
      if (x.ok && x.d && x.d.ok && x.d.url) { state.doc = "ok"; state.docUrl = x.d.url; state.docRef = x.d.ref || ""; }
      else { state.doc = "failed"; }
    }).catch(function () { if (state.clientRef === mine) state.doc = "failed"; });
  }

  function send() {
    if (state.busy) return;
    if (state.leadId) { docRetry(); return; } // the lead exists: never a second one
    var name = (document.getElementById("nlbuy-name") || {}).value || "";
    var phone = (document.getElementById("nlbuy-phone") || {}).value || "";
    var consent = (document.getElementById("nlbuy-consent") || {}).checked;
    var err = document.getElementById("nlbuy-err");
    if (name.trim().length < 2 || phone.replace(/\D/g, "").length < 9 || !consent) {
      if (err) { err.hidden = false; err.textContent = T.err; }
      return;
    }
    state.busy = true;
    var btn = document.getElementById("nlbuy-send"); if (btn) { btn.textContent = T.sending; btn.disabled = true; }
    var p = project(), u = state.unit || {};
    var extras = Object.keys(state.extras).filter(function (k) { return state.extras[k]; });
    var mine = state.clientRef;
    state.name = name.trim();
    // the studio design as it is NOW, frozen for this request (a later edit in the studio does not change it)
    state.design = (window.NLStudio && p) ? window.NLStudio.exportFor(p.slug, u.id || "") : null;
    var payload = {
      name: name.trim(), phone: phone.trim(),
      source: "rfp-v1",
      // the lead names its project and unit, so the server hands back the key that links the document to it
      project_slug: p ? p.slug.replace(/-(en|fr|ru|ar)$/, "") : "", unit: u.id || "", consent: consent ? 1 : 0,
      context: (p ? p.slug : "") + " " + (u.id || ""),
      message: JSON.stringify({
        kind: "rfp-v1", project: p ? p.slug : "", unit: u.id || "", label: u.label || "",
        floor: u.floor || "", rooms: u.rooms || "", sqm: u.sqm || "",
        finish: state.finish, extras: extras, lang: LANG, url: location.href,
        // apartment-studio design travels inside the RFP so the contractor
        // sees the buyer's furniture plan, clearances and special requests
        studio: state.design
      })
    };
    fetch(SR.config.lead_endpoint, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (state.clientRef !== mine) return;
      state.busy = false;
      if (d && d.ok) {
        state.leadId = d.lead_id || 0; state.leadKey = d.lead_key || "";
        state.step = 4; render();
        // phase 2: the real RFP document, generated server-side while the dispatch stages play; the done screen says
        // what really happened to it: ready (a link), still being prepared, or failed (with a retry that makes no new lead)
        makeDoc(mine).then(function () { if (state.clientRef === mine && state.step === 5) render(); });
        playStages(function () { if (state.clientRef === mine) { state.step = 5; render(); } }, mine);
      }
      else { if (err) err.hidden = false; if (btn) { btn.textContent = T.send; btn.disabled = false; } }
    }).catch(function () {
      if (state.clientRef !== mine) return;
      state.busy = false;
      if (err) err.hidden = false;
      if (btn) { btn.textContent = T.send; btn.disabled = false; }
    });
  }
  function docRetry() {
    if (state.busy) return;
    var mine = state.clientRef;
    state.busy = true; render();
    makeDoc(mine).then(function () { if (state.clientRef !== mine) return; state.busy = false; render(); });
  }

  function onClick(e) {
    var n = e.target.closest("[data-buy]"); if (!n) return;
    var act = n.dataset.buy;
    if (act === "close") { close(); }
    else if (act === "finish") { state.finish = n.dataset.v; render(); }
    else if (act === "extra") { state.extras[n.dataset.v] = !state.extras[n.dataset.v]; render(); }
    else if (act === "next") { state.step = Math.min(3, state.step + 1); render(); }
    else if (act === "skipnext") { state.extras = {}; state.step = 3; render(); }
    else if (act === "back") { state.step = Math.max(1, state.step - 1); render(); }
    else if (act === "send") { send(); }
    else if (act === "docretry") { docRetry(); }
  }

  document.addEventListener("click", function (e) {
    var n = e.target.closest('[data-act="rfp"]');
    if (!n) return;
    e.preventDefault();
    opener = n;
    state = fresh(unitOf(n.dataset.id));
    render();
  });
  // Escape closes the dialog and ends there: the engine's own Escape (which clears the selected unit) never sees it
  window.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var el = document.getElementById("nlbuy");
    if (!el || !el.classList.contains("is-open")) return;
    e.stopPropagation(); close();
  }, true);
})();
