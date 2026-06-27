(function () {
	'use strict';

	var defaultPanelCopy = {
		plan: 'כאן תוצג תוכנית הדירה לאחר העלאת תוכנית מכר מאושרת.',
		view: 'כאן יוצג מבט מהדירה לפי קומה וכיוון כאשר נתוני המבט יהיו זמינים.',
		tour: 'כאן יוצגו סיור פנים, וידאו או גלריית תמונות כאשר החומר המאושר זמין.',
		contact: 'השאירו פרטים עם הדירה שנבחרה כדי לבדוק זמינות, מחיר ותוכנית עדכניים.'
	};
	var defaultSubmitMessage = 'הפנייה מוכנה לשליחה עם פרטי {{unit}}. נציג יחזור עם זמינות, מחיר ותוכנית עדכניים.';
	var defaultUnitTitle = 'הדירה שנבחרה';

	function text(node, value) {
		if (node) {
			node.textContent = value || '';
		}
	}

	function currentUnit(root) {
		return root.querySelector('[data-nlv2-unit].is-active') || root.querySelector('[data-nlv2-unit]');
	}

	function setStatusColor(root, unit) {
		var color = unit.dataset.statusColor || '#34d986';
		root.style.setProperty('--nlv2-active-status', color);
	}

	function selectUnit(root, unit) {
		var card = root.querySelector('[data-nlv2-card]');
		if (!unit || !card) {
			return;
		}

		root.querySelectorAll('[data-nlv2-unit]').forEach(function (button) {
			button.classList.toggle('is-active', button === unit);
			button.setAttribute('aria-pressed', button === unit ? 'true' : 'false');
		});

		setStatusColor(root, unit);
		card.hidden = false;
		text(card.querySelector('[data-nlv2-status]'), unit.dataset.status);
		text(card.querySelector('[data-nlv2-title]'), unit.dataset.title);
		text(card.querySelector('[data-nlv2-rooms]'), unit.dataset.rooms);
		text(card.querySelector('[data-nlv2-sqm]'), unit.dataset.sqm);
		text(card.querySelector('[data-nlv2-floor]'), unit.dataset.floor);
		text(card.querySelector('[data-nlv2-view]'), unit.dataset.view);
		text(card.querySelector('[data-nlv2-price]'), unit.dataset.price);
		text(card.querySelector('[data-nlv2-note]'), unit.dataset.note);

		var unitInput = root.querySelector('[data-nlv2-selected-unit]');
		if (unitInput) {
			unitInput.value = unit.dataset.unitId || unit.textContent || '';
		}
	}

	function setPanel(root, name) {
		var panel = root.querySelector('[data-nlv2-panel]');
		if (!panel) {
			return;
		}
		var copy = {
			plan: root.dataset.nlv2PanelPlan || defaultPanelCopy.plan,
			view: root.dataset.nlv2PanelView || defaultPanelCopy.view,
			tour: root.dataset.nlv2PanelTour || defaultPanelCopy.tour,
			contact: root.dataset.nlv2PanelContact || defaultPanelCopy.contact
		};

		root.querySelectorAll('[data-nlv2-tab]').forEach(function (tab) {
			var active = tab.dataset.nlv2Tab === name;
			tab.classList.toggle('is-active', active);
			tab.setAttribute('aria-selected', active ? 'true' : 'false');
		});

		text(panel, copy[name] || copy.plan);
	}

	function submit(root, form, event) {
		event.preventDefault();
		var ok = root.querySelector('[data-nlv2-feedback]');
		var unit = currentUnit(root);
		var unitTitle = unit ? unit.dataset.title : (root.dataset.nlv2SelectedUnitFallback || defaultUnitTitle);
		var message = root.dataset.nlv2SubmitMessage || defaultSubmitMessage;
		text(ok, message.replace('{{unit}}', unitTitle));
		if (ok) {
			ok.hidden = false;
		}
	}

	function init(root) {
		root.querySelectorAll('[data-nlv2-unit]').forEach(function (button) {
			button.addEventListener('click', function () {
				selectUnit(root, button);
			});
			button.addEventListener('mouseenter', function () {
				root.querySelectorAll('[data-nlv2-unit]').forEach(function (candidate) {
					candidate.classList.toggle('is-previewed', candidate === button);
				});
			});
		});

		root.querySelectorAll('[data-nlv2-tab]').forEach(function (button) {
			button.addEventListener('click', function () {
				setPanel(root, button.dataset.nlv2Tab || 'plan');
			});
		});

		var dismiss = root.querySelector('[data-nlv2-dismiss]');
		if (dismiss) {
			dismiss.addEventListener('click', function () {
				var card = root.querySelector('[data-nlv2-card]');
				if (card) {
					card.hidden = true;
				}
				root.querySelectorAll('[data-nlv2-unit]').forEach(function (button) {
					button.classList.remove('is-active');
					button.setAttribute('aria-pressed', 'false');
				});
			});
		}

		root.querySelectorAll('[data-nlv2-form]').forEach(function (form) {
			form.addEventListener('submit', submit.bind(null, root, form));
		});

		selectUnit(root, currentUnit(root));
		setPanel(root, 'plan');
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', function () {
			document.querySelectorAll('[data-nlv2-showroom]').forEach(init);
		});
	} else {
		document.querySelectorAll('[data-nlv2-showroom]').forEach(init);
	}
}());
