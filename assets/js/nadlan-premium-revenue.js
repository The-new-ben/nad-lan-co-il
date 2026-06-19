(function () {
	'use strict';

	var doc = document;
	var root = doc.documentElement;

	function setViewportUnit() {
		root.style.setProperty('--nlrx-vh', (window.innerHeight * 0.01).toFixed(2) + 'px');
	}

	function tagMoneyLinks() {
		var links = doc.querySelectorAll('a[href*="add-to-cart="], a[href*="/cart"], a[href*="/checkout"], a[href*="/join-pro"]');
		links.forEach(function (link) {
			link.setAttribute('data-nlrx-money-link', 'true');
			if (!link.getAttribute('aria-label')) {
				link.setAttribute('aria-label', link.textContent.trim() || 'פתיחת מסלול פרסום');
			}
		});
	}

	function polishForms() {
		var fields = doc.querySelectorAll('.woocommerce input, .woocommerce select, .woocommerce textarea, .nlst-section input, .nlst-section select, .nlst-section textarea');
		fields.forEach(function (field) {
			var parent = field.closest('p, .form-row, label, .nlst-field, .wc-block-components-text-input');
			if (parent) {
				parent.classList.add('nlrx-field-ready');
			}
		});
	}

	function wireBusyButtons() {
		doc.addEventListener('click', function (event) {
			var button = event.target.closest('a[data-nlrx-money-link], .wc-block-components-button, .woocommerce button.button, .nlst-save');
			if (!button || button.getAttribute('aria-disabled') === 'true') {
				return;
			}
			button.classList.add('nlrx-is-busy');
			window.setTimeout(function () {
				button.classList.remove('nlrx-is-busy');
			}, 1800);
		}, { passive: true });
	}

	function init() {
		setViewportUnit();
		tagMoneyLinks();
		polishForms();
		wireBusyButtons();
		doc.body.classList.add('nlrx-ready');
	}

	if (doc.readyState === 'loading') {
		doc.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
	window.addEventListener('resize', setViewportUnit, { passive: true });
}());

/* Unified floating action rail: gathers WhatsApp, call, AI and accessibility into one launcher. */
(function () {
	'use strict';
	if (window.__nadlanActionRailLoaded) {
		return;
	}
	window.__nadlanActionRailLoaded = true;

	var doc = document;
	var labels = {
		region: '\u05e4\u05e2\u05d5\u05dc\u05d5\u05ea \u05d9\u05e6\u05d9\u05e8\u05ea \u05e7\u05e9\u05e8',
		open: '\u05e4\u05ea\u05d9\u05d7\u05ea \u05e4\u05e2\u05d5\u05dc\u05d5\u05ea \u05d9\u05e6\u05d9\u05e8\u05ea \u05e7\u05e9\u05e8',
		close: '\u05e1\u05d2\u05d9\u05e8\u05ea \u05e4\u05e2\u05d5\u05dc\u05d5\u05ea \u05d9\u05e6\u05d9\u05e8\u05ea \u05e7\u05e9\u05e8',
		a11y: '\u05e0\u05d2\u05d9\u05e9\u05d5\u05ea',
		launcher: '\u05d3\u05d1\u05e8\u05d5 \u05d0\u05d9\u05ea\u05e0\u05d5'
	};

	function ready(fn) {
		if (doc.readyState === 'loading') {
			doc.addEventListener('DOMContentLoaded', fn, { once: true });
			return;
		}
		fn();
	}

	function setOpen(rail, open) {
		var launcher = rail.querySelector('.nlrx-action-launcher');
		rail.classList.toggle('is-open', !!open);
		launcher.setAttribute('aria-expanded', open ? 'true' : 'false');
		launcher.setAttribute('aria-label', open ? labels.close : labels.open);
		if (!open) {
			var aiPanel = rail.querySelector('#nlai .nlai-panel');
			if (aiPanel) {
				aiPanel.hidden = true;
			}
			var a11yPanel = doc.getElementById('nla-panel');
			if (a11yPanel) {
				a11yPanel.classList.remove('open');
			}
			var a11yButton = doc.getElementById('nla-btn');
			if (a11yButton) {
				a11yButton.setAttribute('aria-expanded', 'false');
			}
		}
	}

	function mountRail() {
		if (doc.getElementById('nlrx-action-rail')) {
			return true;
		}

		var fab = doc.querySelector('.nlfab');
		var ai = doc.getElementById('nlai');
		var a11y = doc.getElementById('nla-btn');
		if (!fab && !ai && !a11y) {
			return false;
		}

		var rail = doc.createElement('div');
		rail.id = 'nlrx-action-rail';
		rail.className = 'nlrx-action-rail';
		rail.dir = 'rtl';
		rail.setAttribute('role', 'region');
		rail.setAttribute('aria-label', labels.region);

		var items = doc.createElement('div');
		items.id = 'nlrx-action-items';
		items.className = 'nlrx-action-items';

		var launcher = doc.createElement('button');
		launcher.type = 'button';
		launcher.className = 'nlrx-action-launcher';
		launcher.setAttribute('aria-controls', 'nlrx-action-items');
		launcher.setAttribute('aria-expanded', 'false');
		launcher.setAttribute('aria-label', labels.open);
		launcher.innerHTML = '<span class="nlrx-action-plus" aria-hidden="true">+</span><span class="nlrx-action-text">' + labels.launcher + '</span>';

		if (ai) {
			items.appendChild(ai);
		}
		if (fab) {
			Array.prototype.slice.call(fab.querySelectorAll('.nlfab-btn')).forEach(function (button) {
				items.appendChild(button);
			});
			fab.remove();
		}
		if (a11y) {
			a11y.setAttribute('data-nlrx-label', labels.a11y);
			items.appendChild(a11y);
		}

		rail.appendChild(items);
		rail.appendChild(launcher);
		doc.body.appendChild(rail);
		doc.body.classList.add('nlrx-action-rail-ready');

		launcher.addEventListener('click', function () {
			setOpen(rail, !rail.classList.contains('is-open'));
		});
		doc.addEventListener('keydown', function (event) {
			if (event.key === 'Escape' && rail.classList.contains('is-open')) {
				setOpen(rail, false);
				launcher.focus();
			}
		});
		doc.addEventListener('click', function (event) {
			if (!rail.classList.contains('is-open') || rail.contains(event.target)) {
				return;
			}
			if (event.target.closest('#nlai .nlai-panel, #nla-panel, .nlmodal')) {
				return;
			}
			setOpen(rail, false);
		});

		return true;
	}

	ready(function () {
		var attempts = 0;
		function tick() {
			if (mountRail()) {
				return;
			}
			attempts += 1;
			if (attempts < 32) {
				window.setTimeout(tick, 250);
			}
		}
		tick();
	});
}());
