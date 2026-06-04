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
