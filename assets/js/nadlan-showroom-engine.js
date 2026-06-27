(function () {
	'use strict';

	var state = {
		projects: [],
		project: null,
		unit: null,
		tab: 'plan',
		lang: 'he'
	};
	var script = document.currentScript;
	var rootConfig = document.querySelector('[data-nle-home-showroom], [data-nle-engine-config]');
	var projectsUrl = script && script.dataset.projects ? script.dataset.projects : rootConfig && rootConfig.dataset.nleProjects ? rootConfig.dataset.nleProjects : 'assets/engine/projects.json';
	var assetBase = script && script.dataset.assetBase ? script.dataset.assetBase : rootConfig && rootConfig.dataset.nleAssetBase ? rootConfig.dataset.nleAssetBase : './';
	var langMeta = {
		he: { dir: 'rtl' },
		en: { dir: 'ltr' },
		fr: { dir: 'ltr' },
		ru: { dir: 'ltr' },
		ar: { dir: 'rtl' }
	};
	var copy = {
		he: {
			project_count: 'פרויקטים לבחירה',
			no_value: 'לפי פנייה',
			floor: 'קומה',
			rooms: 'חדרים',
			area: 'שטח',
			view: 'נוף',
			estimate: 'אומדן',
			plan: 'תוכנית',
			unit_view: 'מבט',
			tour: 'סיור',
			quick_pick: 'בחירת דירה מהירה',
			quick_pick_note: 'בחרו קומה או דירה כדי לראות שטח, חדרים, נוף, אומדן ותוכנית לפני פנייה.',
			contact_title: 'רוצים לבדוק את הדירה?',
			contact_button: 'שליחת פנייה על הדירה',
			contact_note: 'הפנייה תישלח עם פרטי הדירה שנבחרה. הנתונים להמחשה ויש לאמת מחיר וזמינות מול היזם.',
			name: 'שם מלא',
			phone: 'טלפון',
			available: 'זמינה',
			reserved: 'בבדיקת זמינות',
			sold: 'נמכרה',
			unit_prefix: 'דירה',
			penthouse: 'פנטהאוז',
			floor_word: 'קומה',
			room_word: 'חדרים',
			sqm: 'מ״ר',
			price: 'אומדן לפי פנייה',
			plan_prefix: 'תוכנית דירה: ',
			plan_fallback: 'כאן תוצג תוכנית הדירה לאחר העלאת תוכנית מכר מאושרת.',
			view_prefix: 'מבט מהדירה: ',
			view_fallback: 'יוצג לאחר חיבור שכבת מפה או תמונת נוף מאושרת.',
			tour_text: 'כאן יוצגו סיור פנים, וידאו או גלריית תמונות כאשר החומר המאושר זמין.',
			feedback: 'קיבלנו את הפנייה עם פרטי הדירה שנבחרה. נציג יחזור אליכם בהמשך.',
			sea_view: 'ים וקו חוף',
			city_view: 'רובע שדה דב ותל אביב',
			courtyard_view: 'חצר פנימית וסביבה שקטה',
			park_view: 'פארק ושכונה',
			search: 'שם פרויקט או אזור'
		},
		en: {
			project_count: 'projects to compare',
			no_value: 'By request',
			floor: 'Floor',
			rooms: 'Rooms',
			area: 'Area',
			view: 'View',
			estimate: 'Estimate',
			plan: 'Plan',
			unit_view: 'View',
			tour: 'Tour',
			quick_pick: 'Quick apartment picker',
			quick_pick_note: 'Choose an apartment to see floor, rooms, area, view, estimate and plan before asking for details.',
			contact_title: 'Want to check this apartment?',
			contact_button: 'Send request for this apartment',
			contact_note: 'The request includes the selected apartment. Prices and availability must be confirmed with the representative.',
			name: 'Full name',
			phone: 'Phone',
			available: 'Available',
			reserved: 'Under review',
			sold: 'Sold',
			unit_prefix: 'Apartment',
			penthouse: 'Penthouse',
			floor_word: 'floor',
			room_word: 'rooms',
			sqm: 'sqm',
			price: 'Estimate by request',
			plan_prefix: 'Apartment plan: ',
			plan_fallback: 'The approved sales plan will appear here when available.',
			view_prefix: 'View from the apartment: ',
			view_fallback: 'Available after a verified map layer or approved view image is connected.',
			tour_text: 'Interior tour, video or photo gallery will appear here when approved material is available.',
			feedback: 'We received the request with the selected apartment. A representative will contact you.',
			sea_view: 'Sea and coastline',
			city_view: 'Sde Dov district and Tel Aviv',
			courtyard_view: 'Inner courtyard and quiet surroundings',
			park_view: 'Park and neighborhood',
			search: 'Project or area'
		},
		fr: {
			project_count: 'projets à comparer',
			no_value: 'Sur demande',
			floor: 'Étage',
			rooms: 'Pièces',
			area: 'Surface',
			view: 'Vue',
			estimate: 'Estimation',
			plan: 'Plan',
			unit_view: 'Vue',
			tour: 'Visite',
			quick_pick: 'Choix rapide d’appartement',
			quick_pick_note: 'Choisissez un appartement pour voir l’étage, les pièces, la surface, la vue, l’estimation et le plan.',
			contact_title: 'Vous souhaitez vérifier cet appartement ?',
			contact_button: 'Demander des détails',
			contact_note: 'La demande inclut l’appartement choisi. Le prix et la disponibilité doivent être confirmés avec un représentant.',
			name: 'Nom complet',
			phone: 'Téléphone',
			available: 'Disponible',
			reserved: 'En vérification',
			sold: 'Vendu',
			unit_prefix: 'Appartement',
			penthouse: 'Penthouse',
			floor_word: 'étage',
			room_word: 'pièces',
			sqm: 'm²',
			price: 'Estimation sur demande',
			plan_prefix: 'Plan de l’appartement : ',
			plan_fallback: 'Le plan de vente approuvé apparaîtra ici lorsqu’il sera disponible.',
			view_prefix: 'Vue depuis l’appartement : ',
			view_fallback: 'Disponible après connexion d’une couche de carte vérifiée ou d’une image approuvée.',
			tour_text: 'La visite intérieure, la vidéo ou la galerie apparaîtra ici lorsque les supports approuvés seront disponibles.',
			feedback: 'Nous avons reçu la demande avec l’appartement choisi. Un représentant vous contactera.',
			sea_view: 'Mer et littoral',
			city_view: 'Quartier Sde Dov et Tel Aviv',
			courtyard_view: 'Cour intérieure et environnement calme',
			park_view: 'Parc et quartier',
			search: 'Projet ou quartier'
		},
		ru: {
			project_count: 'проектов для сравнения',
			no_value: 'По запросу',
			floor: 'Этаж',
			rooms: 'Комнаты',
			area: 'Площадь',
			view: 'Вид',
			estimate: 'Оценка',
			plan: 'План',
			unit_view: 'Вид',
			tour: 'Тур',
			quick_pick: 'Быстрый выбор квартиры',
			quick_pick_note: 'Выберите квартиру, чтобы увидеть этаж, комнаты, площадь, вид, оценку цены и план.',
			contact_title: 'Хотите проверить эту квартиру?',
			contact_button: 'Отправить запрос',
			contact_note: 'Запрос включает выбранную квартиру. Цену и доступность нужно подтвердить с представителем.',
			name: 'Полное имя',
			phone: 'Телефон',
			available: 'Доступна',
			reserved: 'Проверяется',
			sold: 'Продана',
			unit_prefix: 'Квартира',
			penthouse: 'Пентхаус',
			floor_word: 'этаж',
			room_word: 'комнат',
			sqm: 'м²',
			price: 'Оценка по запросу',
			plan_prefix: 'План квартиры: ',
			plan_fallback: 'Утвержденный план продажи появится здесь, когда будет доступен.',
			view_prefix: 'Вид из квартиры: ',
			view_fallback: 'Появится после подключения проверенного слоя карты или утвержденного изображения вида.',
			tour_text: 'Внутренний тур, видео или галерея появятся здесь после получения утвержденных материалов.',
			feedback: 'Мы получили запрос по выбранной квартире. Представитель свяжется с вами.',
			sea_view: 'Море и береговая линия',
			city_view: 'Квартал Sde Dov и Тель-Авив',
			courtyard_view: 'Внутренний двор и спокойная среда',
			park_view: 'Парк и район',
			search: 'Проект или район'
		},
		ar: {
			project_count: 'مشاريع للمقارنة',
			no_value: 'حسب الطلب',
			floor: 'الطابق',
			rooms: 'الغرف',
			area: 'المساحة',
			view: 'الإطلالة',
			estimate: 'تقدير',
			plan: 'المخطط',
			unit_view: 'الإطلالة',
			tour: 'جولة',
			quick_pick: 'اختيار سريع للشقة',
			quick_pick_note: 'اختاروا شقة لرؤية الطابق، الغرف، المساحة، الإطلالة، التقدير والمخطط قبل طلب التفاصيل.',
			contact_title: 'هل تريدون فحص هذه الشقة؟',
			contact_button: 'إرسال طلب حول هذه الشقة',
			contact_note: 'سيشمل الطلب الشقة المختارة. يجب تأكيد السعر والتوفر مع ممثل المشروع.',
			name: 'الاسم الكامل',
			phone: 'الهاتف',
			available: 'متاحة',
			reserved: 'قيد الفحص',
			sold: 'مباعة',
			unit_prefix: 'شقة',
			penthouse: 'بنتهاوس',
			floor_word: 'الطابق',
			room_word: 'غرف',
			sqm: 'م²',
			price: 'تقدير حسب الطلب',
			plan_prefix: 'مخطط الشقة: ',
			plan_fallback: 'سيظهر مخطط البيع المعتمد هنا عندما يكون متاحا.',
			view_prefix: 'الإطلالة من الشقة: ',
			view_fallback: 'تظهر بعد ربط طبقة خريطة موثقة أو صورة إطلالة معتمدة.',
			tour_text: 'ستظهر الجولة الداخلية أو الفيديو أو معرض الصور عندما تكون المواد المعتمدة متاحة.',
			feedback: 'استلمنا الطلب مع الشقة المختارة. سيتواصل معكم ممثل المشروع.',
			sea_view: 'البحر والساحل',
			city_view: 'حي سديه دوف وتل أبيب',
			courtyard_view: 'فناء داخلي ومحيط هادئ',
			park_view: 'حديقة وحي سكني',
			search: 'مشروع أو منطقة'
		}
	};

	function qs(sel, root) {
		return (root || document).querySelector(sel);
	}

	function qsa(sel, root) {
		return Array.prototype.slice.call((root || document).querySelectorAll(sel));
	}

	function statusColor(status) {
		if (status === 'reserved' || status === 'in_review') return '#f0c450';
		if (status === 'sold') return '#98a1a1';
		return '#35d886';
	}

	function t(key) {
		return (copy[state.lang] && copy[state.lang][key]) || copy.he[key] || key;
	}

	function dir() {
		return (langMeta[state.lang] && langMeta[state.lang].dir) || 'rtl';
	}

	function localized(item, key) {
		if (!item) return '';
		if (state.lang !== 'he' && item.i18n && item.i18n[state.lang] && item.i18n[state.lang][key]) {
			return item.i18n[state.lang][key];
		}
		return item[key];
	}

	function planLabel(value) {
		var labels = {
			he: {
				'plan-penthouse': 'תוכנית פנטהאוז',
				'plan-5br': 'תוכנית דירת 5 חדרים',
				'plan-4br': 'תוכנית דירת 4 חדרים',
				'plan-3br': 'תוכנית דירת 3 חדרים',
				'plan-boutique': 'תוכנית דירת בוטיק'
			},
			en: {
				'plan-penthouse': 'Penthouse plan',
				'plan-5br': '5-room apartment plan',
				'plan-4br': '4-room apartment plan',
				'plan-3br': '3-room apartment plan',
				'plan-boutique': 'Boutique apartment plan'
			},
			fr: {
				'plan-penthouse': 'Plan du penthouse',
				'plan-5br': 'Plan appartement 5 pièces',
				'plan-4br': 'Plan appartement 4 pièces',
				'plan-3br': 'Plan appartement 3 pièces',
				'plan-boutique': 'Plan appartement boutique'
			},
			ru: {
				'plan-penthouse': 'План пентхауса',
				'plan-5br': 'План квартиры 5 комнат',
				'plan-4br': 'План квартиры 4 комнаты',
				'plan-3br': 'План квартиры 3 комнаты',
				'plan-boutique': 'План бутик-квартиры'
			},
			ar: {
				'plan-penthouse': 'مخطط البنتهاوس',
				'plan-5br': 'مخطط شقة 5 غرف',
				'plan-4br': 'مخطط شقة 4 غرف',
				'plan-3br': 'مخطط شقة 3 غرف',
				'plan-boutique': 'مخطط شقة بوتيك'
			}
		};
		return (labels[state.lang] && labels[state.lang][value]) || labels.he[value] || value;
	}

	function text(el, value) {
		if (el) el.textContent = value == null || value === '' ? t('no_value') : String(value);
	}

	function assetUrl(value) {
		if (!value) return '';
		if (/^(https?:)?\/\//.test(value) || value[0] === '/') return value;
		return new URL(value, new URL(assetBase, window.location.href)).href;
	}

	function translatedStatus(unit) {
		if (unit.status === 'reserved' || unit.status === 'in_review') return t('reserved');
		if (unit.status === 'sold') return t('sold');
		return t('available');
	}

	function translatedTitle(unit) {
		var stored = localized(unit, 'title');
		if (state.lang === 'he' && stored) return stored;
		var prefix = unit.plan === 'plan-penthouse' ? t('penthouse') : t('unit_prefix');
		return prefix + ' ' + (unit.label || unit.floor) + ' · ' + unit.rooms + ' ' + t('room_word') + ' · ' + t('floor_word') + ' ' + unit.floor;
	}

	function translatedView(unit) {
		var stored = localized(unit, 'view');
		if (state.lang === 'he' && stored) return stored;
		var raw = [unit.view || '', unit.dir || ''].join(' ');
		if (/ים|west|sea|coast/i.test(raw)) return t('sea_view');
		if (/חצר|courtyard|garden/i.test(raw)) return t('courtyard_view');
		if (/פארק|park/i.test(raw)) return t('park_view');
		return t('city_view');
	}

	function translatedPrice(unit) {
		var stored = localized(unit, 'price_estimate');
		if (state.lang === 'he' && stored) return stored;
		return t('price');
	}

	function applyLanguageChrome() {
		var scope = document.querySelector('.nle-catalog');
		var showroom = document.querySelector('.nle-showroom');
		[scope, showroom].forEach(function (el) {
			if (!el) return;
			el.setAttribute('lang', state.lang);
			el.setAttribute('dir', dir());
		});
		qsa('[data-nle-lang]').forEach(function (button) {
			button.classList.toggle('is-active', button.dataset.nleLang === state.lang);
			if (button.dataset.nleLang === state.lang) {
				button.setAttribute('aria-pressed', 'true');
			} else {
				button.setAttribute('aria-pressed', 'false');
			}
		});
		qsa('[data-nle-label]').forEach(function (el) {
			text(el, t(el.dataset.nleLabel));
		});
		qsa('[data-nle-placeholder]').forEach(function (el) {
			el.setAttribute('placeholder', t(el.dataset.nlePlaceholder));
		});
		var search = qs('[data-nle-search]');
		if (search) search.setAttribute('placeholder', t('search'));
	}

	function setLanguage(lang) {
		if (!copy[lang]) return;
		state.lang = lang;
		applyLanguageChrome();
		renderCatalog();
		renderShowroom();
	}

	function setActiveProject(slug) {
		var project = state.projects.find(function (item) { return item.slug === slug; }) || state.projects[0];
		state.project = project;
		state.unit = project.units[0];
		state.tab = 'plan';
		renderCatalog();
		renderShowroom();
	}

	function setUnit(unitId) {
		var unit = state.project.units.find(function (item) { return item.id === unitId; }) || state.project.units[0];
		state.unit = unit;
		renderUnit();
		var model = qs('#nle-model-viewer');
		if (model && unit.orbit) {
			try { model.cameraOrbit = unit.orbit; } catch (err) {}
		}
		if (model && unit.position) {
			try { model.cameraTarget = unit.position; } catch (err) {}
		}
	}

	function renderCatalog() {
		var grid = qs('[data-nle-project-grid]');
		var count = qs('[data-nle-project-count]');
		var query = (qs('[data-nle-search]')?.value || '').trim().toLowerCase();
		var projects = state.projects.filter(function (project) {
			var haystack = [localized(project, 'name'), localized(project, 'sub'), localized(project, 'location'), project.name, project.sub, project.location].join(' ').toLowerCase();
			return !query || haystack.indexOf(query) !== -1;
		});
		if (count) count.textContent = projects.length + ' ' + t('project_count');
		if (!grid) return;
		grid.innerHTML = projects.map(function (project) {
			return '<button class="nle-project-card ' + (state.project && state.project.slug === project.slug ? 'is-active' : '') + '" type="button" data-nle-project="' + project.slug + '">' +
				'<img src="' + assetUrl(project.poster) + '" alt="' + localized(project, 'name') + '">' +
				'<div><strong>' + localized(project, 'name') + '</strong><span>' + localized(project, 'sub') + '</span><span>' + localized(project, 'investor_note') + '</span></div>' +
			'</button>';
		}).join('');
		qsa('[data-nle-project]').forEach(function (button) {
			button.addEventListener('click', function () { setActiveProject(button.dataset.nleProject); });
		});
	}

	function renderShowroom() {
		var project = state.project;
		if (!project) return;
		text(qs('[data-nle-project-title]'), localized(project, 'name'));
		text(qs('[data-nle-project-sub]'), localized(project, 'sub'));
		text(qs('[data-nle-project-location]'), localized(project, 'location'));
		text(qs('[data-nle-model-note]'), localized(project, 'model_note'));
		text(qs('[data-nle-project-floors]'), project.floors);
		text(qs('[data-nle-project-units]'), project.units.length);
		var modelWrap = qs('[data-nle-model-wrap]');
		if (modelWrap) {
			modelWrap.innerHTML =
				'<model-viewer id="nle-model-viewer" src="' + assetUrl(project.model_glb) + '" poster="' + assetUrl(project.poster) + '" alt="' + localized(project, 'name') + '" camera-controls auto-rotate auto-rotate-delay="2600" rotation-per-second="12deg" min-camera-orbit="-Infinity 64deg auto" max-camera-orbit="Infinity 78deg auto" camera-orbit="26deg 72deg auto" field-of-view="28deg" reveal="auto" loading="auto" shadow-intensity="1" exposure="1.15">' +
				project.units.map(function (unit) {
					return '<button class="nle-hotspot ' + (unit.recommended ? 'is-recommended ' : '') + '" style="--nle-status:' + statusColor(unit.status) + '" type="button" slot="hotspot-' + unit.id + '" data-position="' + unit.position + '" data-normal="' + unit.normal + '" data-nle-unit-button="' + unit.id + '" aria-label="' + translatedTitle(unit) + '"></button>';
				}).join('') +
				'</model-viewer>';
		}
		renderFacade();
		renderUnit();
	}

	function renderFacade() {
		var grid = qs('[data-nle-facade-grid]');
		if (!grid || !state.project) return;
		grid.innerHTML = state.project.units.map(function (unit) {
			return '<button class="nle-facade-cell" type="button" style="--nle-status:' + statusColor(unit.status) + '" data-nle-unit-button="' + unit.id + '">' +
				'<span>' + (unit.label || unit.floor) + '</span>' +
			'</button>';
		}).join('');
		qsa('[data-nle-unit-button]').forEach(function (button) {
			button.addEventListener('click', function () { setUnit(button.dataset.nleUnitButton); });
		});
	}

	function renderUnit() {
		var unit = state.unit;
		if (!unit) return;
		qsa('[data-nle-unit-button]').forEach(function (button) {
			button.classList.toggle('is-active', button.dataset.nleUnitButton === unit.id);
		});
		var status = qs('[data-nle-unit-status]');
		text(status, translatedStatus(unit));
		if (status) status.style.setProperty('--nle-status', statusColor(unit.status));
		text(qs('[data-nle-unit-title]'), translatedTitle(unit));
		text(qs('[data-nle-unit-floor]'), unit.floor);
		text(qs('[data-nle-unit-rooms]'), unit.rooms);
		text(qs('[data-nle-unit-sqm]'), unit.sqm ? unit.sqm + ' ' + t('sqm') : '');
		text(qs('[data-nle-unit-view]'), translatedView(unit));
		text(qs('[data-nle-unit-price]'), translatedPrice(unit));
		text(qs('[data-nle-selected-unit]'), unit.id);
		renderPanel();
	}

	function renderPanel() {
		var unit = state.unit;
		var panel = qs('[data-nle-panel]');
		if (!panel || !unit) return;
		if (state.tab === 'view') {
			panel.textContent = t('view_prefix') + (translatedView(unit) || t('view_fallback'));
		} else if (state.tab === 'tour') {
			panel.textContent = t('tour_text');
		} else {
			panel.textContent = unit.plan ? t('plan_prefix') + planLabel(unit.plan) : t('plan_fallback');
		}
		qsa('[data-nle-tab]').forEach(function (button) {
			button.classList.toggle('is-active', button.dataset.nleTab === state.tab);
		});
	}

	function init() {
		fetch(projectsUrl)
			.then(function (res) { return res.json(); })
			.then(function (data) {
				state.projects = data.projects || [];
				applyLanguageChrome();
				setActiveProject(state.projects[0] && state.projects[0].slug);
			});
		var search = qs('[data-nle-search]');
		if (search) search.addEventListener('input', renderCatalog);
		qsa('[data-nle-lang]').forEach(function (button) {
			button.addEventListener('click', function () {
				setLanguage(button.dataset.nleLang || 'he');
			});
		});
		qsa('[data-nle-tab]').forEach(function (button) {
			button.addEventListener('click', function () {
				state.tab = button.dataset.nleTab || 'plan';
				renderPanel();
			});
		});
		var form = qs('[data-nle-form]');
		if (form) {
			form.addEventListener('submit', function (event) {
				event.preventDefault();
				text(qs('[data-nle-feedback]'), t('feedback'));
			});
		}
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
