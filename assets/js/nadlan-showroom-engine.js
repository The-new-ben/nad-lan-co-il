(function () {
	'use strict';

	var state = {
		projects: [],
		project: null,
		unit: null,
		tab: 'plan'
	};
	var script = document.currentScript;
	var projectsUrl = script && script.dataset.projects ? script.dataset.projects : 'assets/engine/projects.json';
	var assetBase = script && script.dataset.assetBase ? script.dataset.assetBase : './';

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

	function planLabel(value) {
		var labels = {
			'plan-penthouse': 'תוכנית פנטהאוז',
			'plan-5br': 'תוכנית דירת 5 חדרים',
			'plan-4br': 'תוכנית דירת 4 חדרים',
			'plan-3br': 'תוכנית דירת 3 חדרים',
			'plan-boutique': 'תוכנית דירת בוטיק'
		};
		return labels[value] || value;
	}

	function text(el, value) {
		if (el) el.textContent = value == null || value === '' ? 'לפי פנייה' : String(value);
	}

	function assetUrl(value) {
		if (!value) return '';
		if (/^(https?:)?\/\//.test(value) || value[0] === '/') return value;
		return new URL(value, new URL(assetBase, window.location.href)).href;
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
			var haystack = [project.name, project.sub, project.location].join(' ').toLowerCase();
			return !query || haystack.indexOf(query) !== -1;
		});
		if (count) count.textContent = projects.length + ' פרויקטים לבחירה';
		if (!grid) return;
		grid.innerHTML = projects.map(function (project) {
			return '<button class="nle-project-card ' + (state.project && state.project.slug === project.slug ? 'is-active' : '') + '" type="button" data-nle-project="' + project.slug + '">' +
				'<img src="' + assetUrl(project.poster) + '" alt="תצוגת פרויקט ' + project.name + '">' +
				'<div><strong>' + project.name + '</strong><span>' + project.sub + '</span><span>' + project.investor_note + '</span></div>' +
			'</button>';
		}).join('');
		qsa('[data-nle-project]').forEach(function (button) {
			button.addEventListener('click', function () { setActiveProject(button.dataset.nleProject); });
		});
	}

	function renderShowroom() {
		var project = state.project;
		if (!project) return;
		text(qs('[data-nle-project-title]'), project.name);
		text(qs('[data-nle-project-sub]'), project.sub);
		text(qs('[data-nle-project-location]'), project.location);
		text(qs('[data-nle-model-note]'), project.model_note);
		text(qs('[data-nle-project-floors]'), project.floors);
		text(qs('[data-nle-project-units]'), project.units.length);
		var modelWrap = qs('[data-nle-model-wrap]');
		if (modelWrap) {
			modelWrap.innerHTML =
				'<model-viewer id="nle-model-viewer" src="' + assetUrl(project.model_glb) + '" poster="' + assetUrl(project.poster) + '" alt="מודל תלת ממד של ' + project.name + '" camera-controls auto-rotate auto-rotate-delay="2600" rotation-per-second="12deg" min-camera-orbit="-Infinity 64deg auto" max-camera-orbit="Infinity 78deg auto" camera-orbit="26deg 72deg auto" field-of-view="28deg" reveal="auto" loading="auto" shadow-intensity="1" exposure="1.15">' +
				project.units.map(function (unit) {
					return '<button class="nle-hotspot ' + (unit.recommended ? 'is-recommended ' : '') + '" style="--nle-status:' + statusColor(unit.status) + '" type="button" slot="hotspot-' + unit.id + '" data-position="' + unit.position + '" data-normal="' + unit.normal + '" data-nle-unit-button="' + unit.id + '" aria-label="' + unit.title + '"></button>';
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
			if (button.matches('.nle-hotspot')) {
				button.style.setProperty('--nle-status', statusColor(unit.status));
			}
		});
		var status = qs('[data-nle-unit-status]');
		text(status, unit.status_label);
		if (status) status.style.setProperty('--nle-status', statusColor(unit.status));
		text(qs('[data-nle-unit-title]'), unit.title);
		text(qs('[data-nle-unit-floor]'), unit.floor);
		text(qs('[data-nle-unit-rooms]'), unit.rooms);
		text(qs('[data-nle-unit-sqm]'), unit.sqm ? unit.sqm + ' מ״ר' : '');
		text(qs('[data-nle-unit-view]'), unit.view);
		text(qs('[data-nle-unit-price]'), unit.price_estimate);
		text(qs('[data-nle-selected-unit]'), unit.id);
		renderPanel();
	}

	function renderPanel() {
		var unit = state.unit;
		var panel = qs('[data-nle-panel]');
		if (!panel || !unit) return;
		if (state.tab === 'view') {
			panel.textContent = 'מבט מהדירה: ' + (unit.view || 'יוצג לאחר חיבור שכבת מפה או תמונת נוף מאושרת.');
		} else if (state.tab === 'tour') {
			panel.textContent = 'כאן יוצגו סיור פנים, וידאו או גלריית תמונות כאשר החומר המאושר זמין.';
		} else {
			panel.textContent = unit.plan ? 'תוכנית דירה: ' + planLabel(unit.plan) : 'כאן תוצג תוכנית הדירה לאחר העלאת תוכנית מכר מאושרת.';
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
				setActiveProject(state.projects[0] && state.projects[0].slug);
			});
		var search = qs('[data-nle-search]');
		if (search) search.addEventListener('input', renderCatalog);
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
				text(qs('[data-nle-feedback]'), 'קיבלנו את הפנייה עם פרטי הדירה שנבחרה. נציג יחזור אליכם בהמשך.');
			});
		}
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
