/* NadLan "we will rent it out meanwhile" (HAD-795, package 6, 19.11.2026).
 * One shared component, five languages (he en fr ru ar), phone first:
 *   window.NadlanEarn.mount(el, opts)   inline (the /my-rentals/ page)
 *   window.NadlanEarn.open(opts)        a sheet over any page (project pages, after an apartment is picked)
 * opts: { lang, area, rooms, project:{slug,title,id}, unit:{id,label,floor}, price, data (url of the CBS json), lead (REST url), my (rentals page url) }
 * Every number on screen is either the CBS table (Table 4.9, Price Statistics Monthly 10/2026, quarter VII-IX 2026, with its sampling
 * error), the Tax Authority's 2026 exemption ceiling, or a number the visitor typed. Nothing is invented; an unknown cell is omitted.
 * Basket hand-off (package 4): localStorage 'nl-rent-plan:v1' + window event 'nadlan:rent-plan' (schema nadlan-rent-plan v1). */
(function () {
	'use strict';
	if (window.NadlanEarn) { return; }
	var TAX_CEIL = 5654; // ILS a month, 2026 exemption ceiling for residential rent (Israel Tax Authority)
	var ROOMS = ['r1', 'r3', 'r4', 'r5'];
	var RL = { r1: '1-2', r3: '2.5-3', r4: '3.5-4', r5: '4.5+' };
	var LOC = { he: 'he-IL', en: 'en-GB', fr: 'fr-FR', ru: 'ru-RU', ar: 'ar-EG' };
	var T = {
		he: {
			k: 'השכרה בינתיים', h: 'כמה הדירה תכניס בשכירות?', city: 'עיר או מחוז', rooms: 'חדרים',
			month: 'לחודש', to: 'עד',
			what: 'שכר הדירה הממוצע של דירות {r} חדרים ב{a}, {q}, בתוך טווח הטעות של הלמ"ס.',
			q: 'יולי עד ספטמבר 2026', yago: 'לפני שנה {v}', up: 'עלייה של {p}%', down: 'ירידה של {p}%',
			fallback: 'ללמ"ס אין נתון נפרד ל{c}, לכן מוצג הממוצע של {a}.',
			newb: 'הממוצע כולל את כל הדירות המושכרות באזור, ישנות כחדשות. אין מקור רשמי שמודד דירות חדשות לבד, לכן לא הוספנו מספר משלנו. את שכר הדירה אפשר לתקן כאן למטה.',
			none: 'ללמ"ס אין נתון לגודל הזה באזור הזה. בחרו גודל אחר או הקלידו שכר דירה משלכם.',
			calc: 'החשבון שלכם', rent: 'שכר דירה לחודש', price: 'מחיר הדירה', opt: 'לא חובה', empty: 'חודשים ריקים בשנה', fee: 'דמי ניהול %', self: '0 = מנהלים לבד',
			gross: 'בשנה, לפני מס', afterf: 'אחרי חודשים ריקים ודמי ניהול', ten: 'מסלול 10%', left: 'נשאר אצלכם במסלול 10%',
			exempt: 'מסלול הפטור: החלק החייב במס', exempt0: 'מסלול הפטור: פטור מלא', exemptN: 'עד {c} לחודש פטור מלא, כשזו ההכנסה היחידה שלכם משכירות למגורים',
			yld: 'תשואה ברוטו', yldn: 'תשואה אחרי 10%', src: 'מקור: הלשכה המרכזית לסטטיסטיקה, ירחון סטטיסטיקה של מחירים 10/2026, לוח 4.9, רבעון יולי עד ספטמבר 2026. מס: רשות המסים, תקרת הפטור 2026. אומדן בלבד, לא ייעוץ מס.',
			who: 'מי ינהל את הדירה', selfgo: 'מנהלים לבד, חינם, בניהול ההשכרות של נדלן', selfsub: 'שוכרים, תשלומים, חוזה, מדד ותיקונים במקום אחד. בלי עמלות ובלי סליקה.',
			mgr: 'רוצים שמישהו ינהל בשבילכם?', mgrsub: 'השאירו פרטים ונחזור אליכם עם אפשרויות לניהול הדירה.',
			name: 'שם', phone: 'טלפון', email: 'אימייל (לא חובה)', consent: 'אני מסכים שיחזרו אליי בנושא ניהול הדירה. ', privacy: 'מדיניות הפרטיות', send: 'שליחה', sending: 'שולחים...',
			sent: 'קיבלנו. נחזור אליכם בהקדם.', err: 'השליחה לא עברה. נסו שוב או כתבו לנו בוואטסאפ.', need: 'צריך שם וטלפון או אימייל, וסימון ההסכמה.',
			basket: 'הוספה לסל שלי', added: 'נוסף לסל', close: 'סגירה', svcSelf: 'ניהול השכירות בעצמי (חינם)', svcMgr: 'בקשה לאפשרויות ניהול',
			open: 'כמה דירה כזו מכניסה בשכירות?', opensub: 'לפי נתוני הלמ"ס, עם החשבון שלכם', unitL: 'דירה {u}', floorL: 'קומה {f}'
		},
		en: {
			k: 'Rent it out meanwhile', h: 'How much will the apartment earn when rented?', city: 'City or district', rooms: 'Rooms',
			month: 'a month', to: 'to',
			what: 'The average rent of {r} room apartments in {a}, {q}, within the Central Bureau of Statistics margin.',
			q: 'July to September 2026', yago: 'a year earlier {v}', up: 'up {p}%', down: 'down {p}%',
			fallback: 'The Bureau publishes no separate figure for {c}, so this is the average for {a}.',
			newb: 'The average covers every rented apartment in the area, old and new. No official source measures new apartments on their own, so we add no number of our own. You can correct the rent below.',
			none: 'The Bureau has no figure for this size in this area. Pick another size or type your own rent.',
			calc: 'Your numbers', rent: 'Monthly rent', price: 'Apartment price', opt: 'optional', empty: 'Empty months a year', fee: 'Management fee %', self: '0 = you manage',
			gross: 'A year, before tax', afterf: 'After empty months and fee', ten: '10% tax route', left: 'Left with you on the 10% route',
			exempt: 'Exemption route: the taxable part', exempt0: 'Exemption route: fully exempt', exemptN: 'Up to {c} a month is fully exempt when this is your only residential rent income',
			yld: 'Gross yield', yldn: 'Yield after 10%', src: 'Source: Central Bureau of Statistics, Price Statistics Monthly 10/2026, Table 4.9, quarter July to September 2026. Tax: Israel Tax Authority, 2026 exemption ceiling. An estimate, not tax advice.',
			who: 'Who will manage it', selfgo: 'Manage it yourself, free, with NadLan rental management', selfsub: 'Tenants, payments, lease, CPI and repairs in one place. No fees, no payment processing.',
			mgr: 'Want someone to manage it for you?', mgrsub: 'Leave your details and we will come back to you with options for managing the apartment.',
			name: 'Name', phone: 'Phone', email: 'E-mail (optional)', consent: 'I agree to be contacted about managing this apartment. ', privacy: 'Privacy policy', send: 'Send', sending: 'Sending...',
			sent: 'Received. We will be in touch soon.', err: 'It did not go through. Try again or write to us on WhatsApp.', need: 'A name and a phone or e-mail, and the consent box, are needed.',
			basket: 'Add to my basket', added: 'Added to the basket', close: 'Close', svcSelf: 'Managing the rental myself (free)', svcMgr: 'Request for management options',
			open: 'How much does an apartment like this earn when rented?', opensub: 'From Central Bureau of Statistics data, with your own numbers', unitL: 'Apartment {u}', floorL: 'Floor {f}'
		},
		fr: {
			k: 'Le louer en attendant', h: "Combien l'appartement rapportera-t-il en location ?", city: 'Ville ou district', rooms: 'Pièces',
			month: 'par mois', to: 'à',
			what: "Le loyer moyen des appartements de {r} pièces à {a}, {q}, dans la marge d'erreur du Bureau central des statistiques.",
			q: 'juillet à septembre 2026', yago: 'un an plus tôt {v}', up: 'hausse de {p} %', down: 'baisse de {p} %',
			fallback: "Le Bureau ne publie pas de chiffre séparé pour {c} : voici la moyenne de {a}.",
			newb: "La moyenne couvre tous les appartements loués de la zone, anciens et neufs. Aucune source officielle ne mesure le neuf à part, nous n'ajoutons donc aucun chiffre de notre cru. Vous pouvez corriger le loyer ci-dessous.",
			none: "Le Bureau n'a pas de chiffre pour cette taille dans cette zone. Choisissez une autre taille ou saisissez votre loyer.",
			calc: 'Vos chiffres', rent: 'Loyer mensuel', price: "Prix de l'appartement", opt: 'facultatif', empty: 'Mois vides par an', fee: 'Frais de gestion %', self: '0 = vous gérez',
			gross: 'Par an, avant impôt', afterf: 'Après mois vides et frais', ten: 'Régime à 10 %', left: 'Ce qui vous reste au régime à 10 %',
			exempt: "Régime d'exonération : la part imposable", exempt0: "Régime d'exonération : totalement exonéré", exemptN: "Jusqu'à {c} par mois, exonération totale si c'est votre seul revenu locatif résidentiel",
			yld: 'Rendement brut', yldn: 'Rendement après 10 %', src: "Source : Bureau central des statistiques d'Israël, Price Statistics Monthly 10/2026, tableau 4.9, trimestre juillet à septembre 2026. Impôt : Autorité fiscale israélienne, plafond d'exonération 2026. Estimation, pas un conseil fiscal.",
			who: 'Qui gérera le bien', selfgo: 'Gérer vous-même, gratuitement, avec la gestion locative NadLan', selfsub: 'Locataires, paiements, bail, indexation et réparations au même endroit. Sans frais, sans encaissement.',
			mgr: "Vous voulez qu'on le gère pour vous ?", mgrsub: 'Laissez vos coordonnées, nous revenons vers vous avec des options de gestion.',
			name: 'Nom', phone: 'Téléphone', email: 'E-mail (facultatif)', consent: "J'accepte d'être contacté au sujet de la gestion de cet appartement. ", privacy: 'Politique de confidentialité', send: 'Envoyer', sending: 'Envoi...',
			sent: 'Bien reçu. Nous revenons vers vous très vite.', err: "L'envoi n'a pas abouti. Réessayez ou écrivez-nous sur WhatsApp.", need: 'Il faut un nom et un téléphone ou un e-mail, et cocher le consentement.',
			basket: 'Ajouter à mon panier', added: 'Ajouté au panier', close: 'Fermer', svcSelf: 'Je gère la location moi-même (gratuit)', svcMgr: 'Demande d’options de gestion',
			open: 'Combien rapporte un appartement comme celui-ci en location ?', opensub: 'Données du Bureau central des statistiques, avec vos chiffres', unitL: 'Appartement {u}', floorL: 'Étage {f}'
		},
		ru: {
			k: 'Сдать, пока', h: 'Сколько квартира принесёт при сдаче?', city: 'Город или округ', rooms: 'Комнаты',
			month: 'в месяц', to: 'до',
			what: 'Средняя аренда квартир {r} комнат, {a}, {q}, в пределах погрешности Центрального статистического бюро.',
			q: 'июль–сентябрь 2026', yago: 'год назад {v}', up: 'рост {p}%', down: 'снижение {p}%',
			fallback: 'Бюро не публикует отдельную цифру для {c}, поэтому показано среднее для: {a}.',
			newb: 'Среднее охватывает все сдаваемые квартиры района, старые и новые. Официального источника только по новостройкам нет, поэтому своих цифр мы не добавляем. Аренду можно исправить ниже.',
			none: 'У Бюро нет цифры для этого размера в этом районе. Выберите другой размер или введите свою аренду.',
			calc: 'Ваш расчёт', rent: 'Аренда в месяц', price: 'Цена квартиры', opt: 'необязательно', empty: 'Пустых месяцев в году', fee: 'Плата за управление %', self: '0 = управляете сами',
			gross: 'В год, до налога', afterf: 'После пустых месяцев и платы', ten: 'Режим 10%', left: 'Остаётся вам в режиме 10%',
			exempt: 'Режим освобождения: облагаемая часть', exempt0: 'Режим освобождения: полностью освобождено', exemptN: 'До {c} в месяц полностью освобождено, если это ваш единственный доход от жилой аренды',
			yld: 'Валовая доходность', yldn: 'Доходность после 10%', src: 'Источник: Центральное статистическое бюро Израиля, Price Statistics Monthly 10/2026, таблица 4.9, квартал июль–сентябрь 2026. Налог: Налоговое управление Израиля, порог освобождения 2026. Оценка, не налоговая консультация.',
			who: 'Кто будет управлять квартирой', selfgo: 'Управлять самому, бесплатно, в системе аренды NadLan', selfsub: 'Жильцы, платежи, договор, индексация и ремонт в одном месте. Без комиссий и без приёма платежей.',
			mgr: 'Хотите, чтобы кто-то управлял за вас?', mgrsub: 'Оставьте контакты, и мы вернёмся к вам с вариантами управления квартирой.',
			name: 'Имя', phone: 'Телефон', email: 'E-mail (необязательно)', consent: 'Я согласен, чтобы со мной связались по поводу управления квартирой. ', privacy: 'Политика конфиденциальности', send: 'Отправить', sending: 'Отправляем...',
			sent: 'Получили. Скоро свяжемся.', err: 'Не отправилось. Попробуйте ещё раз или напишите нам в WhatsApp.', need: 'Нужны имя и телефон или e-mail, и отметка согласия.',
			basket: 'Добавить в мою корзину', added: 'Добавлено в корзину', close: 'Закрыть', svcSelf: 'Управляю арендой сам (бесплатно)', svcMgr: 'Запрос вариантов управления',
			open: 'Сколько приносит такая квартира при сдаче?', opensub: 'По данным Центрального статистического бюро, с вашими цифрами', unitL: 'Квартира {u}', floorL: 'Этаж {f}'
		},
		ar: {
			k: 'نؤجّرها في الأثناء', h: 'كم ستدرّ الشقة عند تأجيرها؟', city: 'مدينة أو منطقة', rooms: 'غرف',
			month: 'شهريًا', to: 'إلى',
			what: 'متوسط إيجار شقق {r} غرف في {a}، {q}، ضمن هامش الخطأ لدائرة الإحصاء المركزية.',
			q: 'يوليو إلى سبتمبر 2026', yago: 'قبل عام {v}', up: 'ارتفاع {p}%', down: 'انخفاض {p}%',
			fallback: 'لا تنشر الدائرة رقمًا منفصلًا لـ{c}، لذا يظهر متوسط {a}.',
			newb: 'يشمل المتوسط كل الشقق المؤجرة في المنطقة، القديمة والجديدة. لا يوجد مصدر رسمي يقيس الشقق الجديدة وحدها، لذلك لم نضف رقمًا من عندنا. يمكنكم تعديل الإيجار أدناه.',
			none: 'لا يوجد لدى الدائرة رقم لهذا الحجم في هذه المنطقة. اختاروا حجمًا آخر أو اكتبوا إيجارًا خاصًا بكم.',
			calc: 'حسابكم', rent: 'الإيجار الشهري', price: 'سعر الشقة', opt: 'اختياري', empty: 'أشهر فارغة في السنة', fee: 'رسوم الإدارة %', self: '0 = تديرونها بأنفسكم',
			gross: 'في السنة، قبل الضريبة', afterf: 'بعد الأشهر الفارغة والرسوم', ten: 'مسار 10%', left: 'ما يبقى لكم في مسار 10%',
			exempt: 'مسار الإعفاء: الجزء الخاضع للضريبة', exempt0: 'مسار الإعفاء: إعفاء كامل', exemptN: 'حتى {c} شهريًا إعفاء كامل عندما يكون هذا دخلكم الوحيد من إيجار سكني',
			yld: 'العائد الإجمالي', yldn: 'العائد بعد 10%', src: 'المصدر: دائرة الإحصاء المركزية الإسرائيلية، Price Statistics Monthly 10/2026، الجدول 4.9، ربع يوليو إلى سبتمبر 2026. الضريبة: سلطة الضرائب الإسرائيلية، سقف الإعفاء 2026. تقدير فقط وليس استشارة ضريبية.',
			who: 'من سيدير الشقة', selfgo: 'أديروها بأنفسكم مجانًا بنظام إدارة الإيجارات في NadLan', selfsub: 'المستأجرون والدفعات والعقد والربط بالمؤشر والإصلاحات في مكان واحد. بلا عمولات وبلا تحصيل.',
			mgr: 'تريدون أن يديرها أحد عنكم؟', mgrsub: 'اتركوا تفاصيلكم وسنعود إليكم بخيارات لإدارة الشقة.',
			name: 'الاسم', phone: 'الهاتف', email: 'البريد الإلكتروني (اختياري)', consent: 'أوافق على التواصل معي بشأن إدارة هذه الشقة. ', privacy: 'سياسة الخصوصية', send: 'إرسال', sending: 'جارٍ الإرسال...',
			sent: 'وصلنا طلبكم. سنعود إليكم قريبًا.', err: 'لم يتم الإرسال. حاولوا مرة أخرى أو راسلونا عبر واتساب.', need: 'مطلوب اسم وهاتف أو بريد إلكتروني، مع تحديد الموافقة.',
			basket: 'إضافة إلى سلّتي', added: 'أضيف إلى السلة', close: 'إغلاق', svcSelf: 'أدير الإيجار بنفسي (مجانًا)', svcMgr: 'طلب خيارات إدارة',
			open: 'كم تدرّ شقة كهذه عند تأجيرها؟', opensub: 'حسب بيانات دائرة الإحصاء المركزية، مع أرقامكم', unitL: 'شقة {u}', floorL: 'الطابق {f}'
		}
	};
	var DATA = null, DATA_P = null;
	function load(url) {
		if (DATA) { return Promise.resolve(DATA); }
		if (!DATA_P) { DATA_P = fetch(url, { credentials: 'omit' }).then(function (r) { if (!r.ok) { throw new Error('data'); } return r.json(); }).then(function (j) { DATA = j; return j; }); }
		return DATA_P;
	}
	function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
	function tpl(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
	function num(v) { var n = parseFloat(String(v == null ? '' : v).replace(/[^\d.]/g, '')); return isFinite(n) ? n : null; }
	function guessLang() { var l = (document.documentElement.lang || 'he').slice(0, 2).toLowerCase(); return T[l] ? l : 'he'; }

	function build(host, o, inSheet) {
		var L = T[o.lang] ? o.lang : guessLang(); var t = T[L]; var rtl = (L === 'he' || L === 'ar');
		var nf = new Intl.NumberFormat(LOC[L], { maximumFractionDigits: 0 });
		var pf = new Intl.NumberFormat(LOC[L], { maximumFractionDigits: 1 });
		function ils(n) { return '₪' + nf.format(Math.round(n)); }
		var S = { area: o.area || 'tel-aviv', rooms: ROOMS.indexOf(o.rooms) > -1 ? o.rooms : 'r4', rent: null, rentTyped: false, price: num(o.price), empty: 0, fee: null };
		var root = document.createElement('div');
		root.className = 'nlre' + (inSheet ? ' nlre--sheet' : '');
		root.setAttribute('dir', rtl ? 'rtl' : 'ltr'); root.setAttribute('lang', L);
		host.appendChild(root);
		var ctx = '';
		if (o.project && o.project.title) {
			ctx = esc(o.project.title);
			if (o.unit && o.unit.label) { ctx += ' · ' + esc(o.unit.label); } else if (o.unit && o.unit.id) { ctx += ' · ' + esc(tpl(t.unitL, { u: o.unit.id })); }
			if (o.unit && o.unit.floor != null && o.unit.floor !== '') { ctx += ' · ' + esc(tpl(t.floorL, { f: o.unit.floor })); }
		}
		root.innerHTML =
			'<div class="nlre-card nlre-top">' +
			(inSheet ? '<button type="button" class="nlre-x" aria-label="' + esc(t.close) + '">×</button>' : '') +
			'<p class="nlre-k">' + (ctx || esc(t.k)) + '</p>' +
			'<h2 class="nlre-h">' + esc(t.h) + '</h2>' +
			'<div class="nlre-pick"><label class="nlre-f">' + esc(t.city) + '<select class="nlre-area"></select></label>' +
			'<fieldset class="nlre-rooms"><legend>' + esc(t.rooms) + '</legend>' + ROOMS.map(function (r) { return '<button type="button" data-r="' + r + '" aria-pressed="false"><span dir="ltr">' + RL[r] + '</span></button>'; }).join('') + '</fieldset></div>' +
			'<div class="nlre-res" aria-live="polite"></div>' +
			'</div>' +
			'<div class="nlre-card nlre-calc"><h3>' + esc(t.calc) + '</h3><div class="nlre-grid">' +
			'<label class="nlre-f">' + esc(t.rent) + '<input inputmode="numeric" class="nlre-rent" dir="ltr"></label>' +
			'<label class="nlre-f">' + esc(t.price) + '<input inputmode="numeric" class="nlre-price" dir="ltr" placeholder="' + esc(t.opt) + '"></label>' +
			'<label class="nlre-f">' + esc(t.empty) + '<input inputmode="numeric" class="nlre-empty" dir="ltr" value="0"></label>' +
			'<label class="nlre-f">' + esc(t.fee) + '<input inputmode="decimal" class="nlre-fee" dir="ltr" placeholder="' + esc(t.self) + '"></label>' +
			'</div><dl class="nlre-sum"></dl><p class="nlre-src"></p></div>' +
			'<div class="nlre-card nlre-who"><h3>' + esc(t.who) + '</h3>' +
			'<a class="nlre-btn nlre-btn--go" href="' + esc(o.my || '/my-rentals/') + '"><b>' + esc(t.selfgo) + '</b><span>' + esc(t.selfsub) + '</span></a>' +
			'<details class="nlre-mgr"><summary class="nlre-btn nlre-btn--line"><b>' + esc(t.mgr) + '</b><span>' + esc(t.mgrsub) + '</span></summary>' +
			'<form class="nlre-form" novalidate><div class="nlre-grid">' +
			'<label class="nlre-f">' + esc(t.name) + '<input name="name" autocomplete="name" required></label>' +
			'<label class="nlre-f">' + esc(t.phone) + '<input name="phone" type="tel" autocomplete="tel" dir="ltr"></label>' +
			'<label class="nlre-f nlre-f--wide">' + esc(t.email) + '<input name="email" type="email" autocomplete="email" dir="ltr"></label>' +
			'</div><input name="company" class="nlre-hp" tabindex="-1" autocomplete="off" aria-hidden="true">' +
			'<label class="nlre-ok"><input type="checkbox" name="consent"> <span>' + esc(t.consent) + '<a href="/privacy/" target="_blank" rel="noopener">' + esc(t.privacy) + '</a></span></label>' +
			'<button type="submit" class="nlre-btn nlre-btn--go nlre-send">' + esc(t.send) + '</button><p class="nlre-msg" aria-live="polite"></p></form></details>' +
			'<button type="button" class="nlre-basket">' + esc(t.basket) + '</button></div>';
		var q = function (s) { return root.querySelector(s); };
		var sel = q('.nlre-area'), res = q('.nlre-res'), sum = q('.nlre-sum');
		q('.nlre-src').textContent = t.src;

		function cell() {
			var A = DATA.areas[S.area]; if (!A) { return null; }
			var c = A.rooms && A.rooms[S.rooms];
			return c ? { avg: c[0], se: c[1], yago: c[2], area: A } : null;
		}
		function paintRes() {
			var c = cell(), A = DATA.areas[S.area];
			var aname = A ? A[L] || A.en : '';
			if (!c) { res.innerHTML = '<p class="nlre-none">' + esc(t.none) + '</p>'; return; }
			var lo = c.avg - 2 * c.se, hi = c.avg + 2 * c.se;
			var ch = (c.avg / c.yago - 1) * 100;
			var h = '<p class="nlre-big" dir="ltr"><span>' + ils(lo) + '</span> <i>' + esc(t.to) + '</i> <span>' + ils(hi) + '</span></p>' +
				'<p class="nlre-per">' + esc(t.month) + '</p>' +
				'<div class="nlre-band" aria-hidden="true"><i style="--a:' + Math.max(0, Math.min(100, (lo / 14000) * 100)).toFixed(1) + '%;--b:' + Math.max(1, ((hi - lo) / 14000) * 100).toFixed(1) + '%"></i><b style="--m:' + Math.min(100, (c.avg / 14000) * 100).toFixed(1) + '%"></b></div>' +
				'<p class="nlre-what">' + esc(tpl(t.what, { r: RL[S.rooms], a: aname, q: t.q })) + '</p>' +
				'<p class="nlre-ago">' + esc(tpl(t.yago, { v: ils(c.yago) })) + ' · ' + esc(tpl(ch >= 0 ? t.up : t.down, { p: pf.format(Math.abs(ch)) })) + '</p>';
			if (o.cityLabel && o.areaFallback) { h += '<p class="nlre-note">' + esc(tpl(t.fallback, { c: o.cityLabel, a: aname })) + '</p>'; }
			h += '<p class="nlre-note">' + esc(t.newb) + '</p>';
			res.innerHTML = h;
		}
		function paintSum() {
			var c = cell();
			if (!S.rentTyped) { S.rent = c ? Math.round(c.avg) : null; q('.nlre-rent').value = S.rent != null ? nf.format(S.rent) : ''; }
			var rent = S.rent;
			if (rent == null || rent <= 0) { sum.innerHTML = ''; return; }
			var months = Math.max(0, Math.min(12, 12 - (S.empty || 0)));
			var gross = rent * months, fee = S.fee ? Math.max(0, Math.min(50, S.fee)) : 0;
			var net = gross * (1 - fee / 100), ten = gross * 0.10;
			var taxable = rent <= TAX_CEIL ? 0 : (rent >= 2 * TAX_CEIL ? rent : 2 * (rent - TAX_CEIL));
			var rows = [[t.gross, ils(gross)]];
			if (S.empty || fee) { rows.push([t.afterf, ils(net)]); }
			rows.push([t.ten, '−' + ils(ten)]);
			rows.push([t.left, ils(net - ten)]);
			rows.push([taxable ? t.exempt : t.exempt0, taxable ? ils(taxable * months) : ils(0)]);
			if (S.price && S.price > 10000) { rows.push([t.yld, pf.format(gross / S.price * 100) + '%']); rows.push([t.yldn, pf.format((net - ten) / S.price * 100) + '%']); }
			sum.innerHTML = rows.map(function (r, i) { return '<div' + (i === 3 ? ' class="is-key"' : '') + '><dt>' + esc(r[0]) + '</dt><dd dir="ltr">' + esc(r[1]) + '</dd></div>'; }).join('') +
				'<p class="nlre-tax">' + esc(tpl(t.exemptN, { c: ils(TAX_CEIL) })) + '</p>';
		}
		function paint() {
			sel.value = S.area;
			root.querySelectorAll('.nlre-rooms button').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-r') === S.rooms ? 'true' : 'false'); });
			paintRes(); paintSum();
		}
		function plan(svc) {
			var c = cell(), A = DATA.areas[S.area];
			var p = {
				schema: 'nadlan-rent-plan', v: 1, created: new Date().toISOString(), lang: L,
				project: o.project ? { slug: o.project.slug || '', title: o.project.title || '' } : { slug: '', title: '' },
				unit: o.unit ? { id: o.unit.id || '', label: o.unit.label || '', rooms: RL[S.rooms] } : { id: '', label: '', rooms: RL[S.rooms] },
				city: { key: S.area, label: A ? (A[L] || A.en) : '' },
				service: svc === 'mgr' ? { id: 'rent-managed-quote', label: t.svcMgr } : { id: 'rent-self', label: t.svcSelf },
				link: (o.my || '/my-rentals/') + (String(o.my || '').indexOf('?') > -1 ? '&' : '?') + 'earn=' + encodeURIComponent(S.area + '.' + S.rooms) + '#earn'
			};
			if (c) { p.estimate = { low: Math.round(c.avg - 2 * c.se), mid: Math.round(c.avg), high: Math.round(c.avg + 2 * c.se), currency: 'ILS', period: 'month', basis: 'cbs-t4.9-' + DATA.source.quarter + '-' + S.area + '-' + S.rooms, source_label: DATA.source.publisher + ', ' + DATA.source.issue + ', ' + DATA.source.table.split(':')[0], source_url: DATA.source.url, as_of: DATA.source.quarter }; }
			p.id = 'rp-' + (p.project.slug || 'own') + '-' + (p.unit.id || S.rooms) + '-' + Date.now().toString(36);
			return p;
		}
		function toBasket(svc) {
			var p = plan(svc), k = (p.project.slug || 'own') + '|' + (p.unit.id || S.area + '.' + S.rooms);
			try { var st = JSON.parse(localStorage.getItem('nl-rent-plan:v1') || 'null') || { plans: {} }; st.plans = st.plans || {}; st.plans[k] = p; st.last = k; localStorage.setItem('nl-rent-plan:v1', JSON.stringify(st)); } catch (e) { /* private mode: the event still goes out */ }
			window.dispatchEvent(new CustomEvent('nadlan:rent-plan', { detail: p }));
			return p;
		}
		load(o.data).then(function () {
			var keys = Object.keys(DATA.areas);
			var cities = keys.filter(function (k) { return DATA.areas[k].district; }).sort(function (a, b) { return String(DATA.areas[a][L]).localeCompare(String(DATA.areas[b][L]), LOC[L]); });
			var dist = keys.filter(function (k) { return !DATA.areas[k].district; });
			sel.innerHTML = cities.concat(dist).map(function (k) { return '<option value="' + k + '">' + esc(DATA.areas[k][L] || DATA.areas[k].en) + '</option>'; }).join('');
			if (!DATA.areas[S.area]) { S.area = 'israel'; }
			paint();
		}).catch(function () { res.innerHTML = '<p class="nlre-none">' + esc(t.err) + '</p>'; });
		sel.addEventListener('change', function () { S.area = sel.value; S.rentTyped = false; o.areaFallback = false; paint(); });
		q('.nlre-rooms').addEventListener('click', function (e) { var b = e.target.closest('button[data-r]'); if (!b) { return; } S.rooms = b.getAttribute('data-r'); S.rentTyped = false; paint(); });
		q('.nlre-rent').addEventListener('input', function (e) { S.rent = num(e.target.value); S.rentTyped = true; paintSum(); });
		q('.nlre-price').addEventListener('input', function (e) { S.price = num(e.target.value); paintSum(); });
		q('.nlre-empty').addEventListener('input', function (e) { S.empty = Math.min(12, num(e.target.value) || 0); paintSum(); });
		q('.nlre-fee').addEventListener('input', function (e) { S.fee = num(e.target.value); paintSum(); });
		if (S.price) { q('.nlre-price').value = nf.format(S.price); }
		var bk = q('.nlre-basket');
		bk.addEventListener('click', function () { toBasket('self'); bk.textContent = t.added; bk.classList.add('is-on'); });
		q('.nlre-form').addEventListener('submit', function (e) {
			e.preventDefault();
			var f = e.target, m = q('.nlre-msg'), btn = q('.nlre-send');
			var name = f.name.value.trim(), phone = f.phone.value.trim(), email = f.email.value.trim();
			if (!name || (!phone && !email) || !f.consent.checked) { m.textContent = t.need; return; }
			var p = plan('mgr'), c = p.estimate;
			var lines = ['Rent management request (' + L + ')', 'Area: ' + p.city.label + ' · rooms ' + p.unit.rooms];
			if (p.project.title) { lines.push('Project: ' + p.project.title + (p.unit.label || p.unit.id ? ' · ' + (p.unit.label || p.unit.id) : '')); }
			if (c) { lines.push('CBS ' + c.as_of + ' average ' + c.mid + ' ILS (range ' + c.low + ' to ' + c.high + ')'); }
			if (S.rentTyped && S.rent) { lines.push('Visitor rent: ' + S.rent); }
			if (S.price) { lines.push('Visitor price: ' + S.price); }
			btn.disabled = true; m.textContent = t.sending;
			var body = { name: name, phone: phone, email: email, company: f.company.value, consent: true, source: 'rent_earn', goal: 'rent-management', topic: 'rent-management', rooms: RL[S.rooms], unit: p.unit.id || '', building: p.project.title || '', message: lines.join('\n'), lang: L, page: location.href.split('#')[0] };
			if (o.project && o.project.id) { body.card_id = o.project.id; }
			fetch(o.lead || '/wp-json/nadlan/v1/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
				.then(function (r) { if (!r.ok) { throw new Error(String(r.status)); } return r.json(); })
				.then(function () { m.textContent = t.sent; f.querySelectorAll('input,button').forEach(function (x) { x.disabled = true; }); toBasket('mgr'); try { if (window.gtag) { window.gtag('event', 'generate_lead', { source: 'rent_earn' }); } } catch (x) { /* analytics is optional */ } })
				.catch(function () { m.textContent = t.err; btn.disabled = false; });
		});
		return root;
	}

	function mount(el, o) { if (!el || el.getAttribute('data-nlre')) { return null; } el.setAttribute('data-nlre', '1'); return build(el, o || {}, false); }
	function open(o) {
		o = o || {};
		var old = document.querySelector('.nlre-veil'); if (old) { old.remove(); }
		var veil = document.createElement('div'); veil.className = 'nlre-veil';
		var box = document.createElement('div'); box.className = 'nlre-dialog'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true');
		var L = T[o.lang] ? o.lang : guessLang(); box.setAttribute('aria-label', T[L].h);
		veil.appendChild(box); document.body.appendChild(veil);
		var prev = document.activeElement, bodyOv = document.body.style.overflow;
		document.body.style.overflow = 'hidden';
		var root = build(box, o, true);
		function shut() { veil.remove(); document.body.style.overflow = bodyOv; document.removeEventListener('keydown', onKey); if (prev && prev.focus) { prev.focus(); } }
		function onKey(e) { if (e.key === 'Escape') { shut(); } }
		document.addEventListener('keydown', onKey);
		veil.addEventListener('click', function (e) { if (e.target === veil) { shut(); } });
		root.querySelector('.nlre-x').addEventListener('click', shut);
		setTimeout(function () { var x = root.querySelector('.nlre-x'); if (x) { x.focus(); } }, 30);
		return root;
	}
	window.NadlanEarn = { mount: mount, open: open, strings: T };

	/* auto: <div data-nadlan-earn='{json opts}'> mounts inline; [data-nadlan-earn-open] buttons open the sheet with the same opts */
	function auto() {
		document.querySelectorAll('[data-nadlan-earn]').forEach(function (el) { var o = {}; try { o = JSON.parse(el.getAttribute('data-nadlan-earn') || '{}'); } catch (e) { /* defaults */ } mount(el, o); });
		document.querySelectorAll('[data-nadlan-earn-open]').forEach(function (b) {
			if (b.getAttribute('data-nlre-wired')) { return; } b.setAttribute('data-nlre-wired', '1');
			b.addEventListener('click', function (e) { e.preventDefault(); var o = {}; try { o = JSON.parse(b.getAttribute('data-nadlan-earn-open') || '{}'); } catch (x) { /* defaults */ } if (b.__nlrePick) { o.unit = b.__nlrePick; } open(o); });
		});
	}
	if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', auto); } else { auto(); }
	window.addEventListener('nl:facing', function (e) {
		var d = e.detail || {}; var u = { id: d.unit || '', label: d.label || '', floor: d.floor != null ? d.floor : '' };
		document.querySelectorAll('[data-nadlan-earn-open]').forEach(function (b) { b.__nlrePick = u; var s = b.querySelector('.nlre-pickline'); if (s) { s.textContent = (u.label || (u.id ? u.id : '')) + (u.floor !== '' ? ' · ' + u.floor : ''); s.hidden = false; } });
	});
})();
