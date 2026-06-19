(function () {
	'use strict';

	function selectUnit(root, button) {
		var card = root.querySelector('[data-nlps-card]');
		if (!card || !button) {
			return;
		}

		var title = card.querySelector('[data-nlps-title]');
		var status = card.querySelector('[data-nlps-status]');
		var rooms = card.querySelector('[data-nlps-rooms]');
		var sqm = card.querySelector('[data-nlps-sqm]');
		var floor = card.querySelector('[data-nlps-floor]');
		var view = card.querySelector('[data-nlps-view]');
		var note = card.querySelector('[data-nlps-note]');

		if (title) {
			title.textContent = button.dataset.title || button.textContent || '';
		}
		if (status) {
			status.textContent = button.dataset.status || '';
		}
		if (rooms) {
			rooms.textContent = button.dataset.rooms || '';
		}
		if (sqm) {
			sqm.textContent = button.dataset.sqm || '';
		}
		if (floor) {
			floor.textContent = button.dataset.floor || '';
		}
		if (view) {
			view.textContent = button.dataset.view || '';
		}
		if (note) {
			note.textContent = button.dataset.note || '';
		}

		card.hidden = false;
		root.querySelectorAll('[data-nlps-unit]').forEach(function (cell) {
			cell.classList.toggle('is-active', cell === button);
		});
	}

	function setPanel(root, key) {
		var panel = root.querySelector('[data-nlps-media-panel]');
		if (!panel) {
			return;
		}

		var copy = {
			plan: 'כאן תופיע תכנית הדירה המאושרת או תכנית אבטיפוס להמחשה.',
			tour: 'כאן יופיע סיור פנים בסגנון Matterport / Homes.com כאשר יוזן קישור מאושר.',
			view: 'כאן יופיע מבט מהדירה לפי קומה וכיוון, לאחר אימות מיקום וקואורדינטות.',
			contact: 'פנייה תישלח עם מזהה הדירה, קומה, חדרים, שטח וכיוון.'
		};

		panel.textContent = copy[key] || copy.plan;
	}

	function activeUnitButton(root) {
		return root.querySelector('[data-nlps-unit].is-active') || root.querySelector('[data-nlps-unit]');
	}

	function cardId(root) {
		var explicit = parseInt(root.dataset.nlpsCardId || root.dataset.project || '0', 10);
		if (explicit > 0) {
			return explicit;
		}
		var match = (document.body.className || '').match(/\b(?:postid|page-id)-(\d+)\b/);
		return match ? parseInt(match[1], 10) : 0;
	}

	function formPayload(root, form, intent) {
		var unit = activeUnitButton(root);
		var data = new FormData(form);
		var title = unit ? (unit.dataset.title || unit.textContent || '') : '';
		var status = unit ? (unit.dataset.status || '') : '';
		var timeline = data.get('timeline') || '';
		var budget = data.get('budget') || '';
		var message = 'פנייה מתוך תצוגת דירות של ' + (root.dataset.nlpsProjectTitle || document.title || 'הפרויקט') + '. ';
		message += 'דירה: ' + title + '. ';
		if (unit) {
			message += 'קומה: ' + (unit.dataset.floor || '') + ', חדרים: ' + (unit.dataset.rooms || '') + ', שטח: ' + (unit.dataset.sqm || '') + ', נוף: ' + (unit.dataset.view || '') + '. ';
		}
		message += 'זמינות: ' + status + '. ';
		message += 'תקציב: ' + (budget || 'לא נמסר') + '. מועד: ' + (timeline || 'לא נמסר') + '.';

		return {
			card_id: cardId(root),
			name: data.get('name') || '',
			phone: data.get('phone') || '',
			email: data.get('email') || '',
			company: data.get('company') || '',
			source: 'project_showroom_theme',
			goal: intent === 'purchase' ? 'בדיקת רכישה לא מחייבת' : 'בקשת שיחה על דירה',
			message: message,
			budget: budget,
			timeline: timeline,
			unit: unit ? (unit.dataset.unitId || unit.dataset.nlpsUnit || unit.textContent || '') : '',
			floor: unit ? (unit.dataset.floor || '') : '',
			rooms: unit ? (unit.dataset.rooms || '') : '',
			sqm: unit ? (unit.dataset.sqm || '') : '',
			building: unit ? (unit.dataset.building || '') : '',
			availability: status,
			market_note: 'נתוני אבטיפוס. יש לאמת מלאי, מחיר ותנאים מול היזם.',
			advisor: data.get('advisor') || '',
			purchase_intent: intent === 'purchase',
			reservation_state: intent === 'purchase' ? 'non_binding_inquiry' : 'lead_request'
		};
	}

	function submitLead(root, form, submitter) {
		var ok = root.querySelector('[data-nlps-ok]');
		var endpoint = root.dataset.nlpsEndpoint || '/wp-json/nadlan/v1/lead';
		var intent = submitter && submitter.dataset.nlpsIntent === 'purchase' ? 'purchase' : 'callback';
		var payload = formPayload(root, form, intent);

		if (!payload.name || (!payload.phone && !payload.email)) {
			if (ok) {
				ok.hidden = false;
				ok.textContent = 'יש למלא שם וטלפון או אימייל כדי שנוכל לחזור אליך.';
			}
			return;
		}

		form.querySelectorAll('button[type="submit"]').forEach(function (button) {
			button.disabled = true;
		});
		if (ok) {
			ok.hidden = false;
			ok.textContent = 'שולחים את הפנייה...';
		}

		fetch(endpoint, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(payload)
		}).then(function (response) {
			if (!response.ok) {
				throw new Error('lead failed');
			}
			return response.json();
		}).then(function (data) {
			var ref = data && (data.id || data.lead_id || '');
			if (ok) {
				ok.textContent = 'קיבלנו את הפנייה. נציג יחזור אליך בתוך 24 שעות' + (ref ? ' · מספר פנייה: ' + ref : '') + '.';
			}
		}).catch(function () {
			if (ok) {
				ok.textContent = 'השליחה נכשלה. אפשר לנסות שוב בעוד רגע.';
			}
			form.querySelectorAll('button[type="submit"]').forEach(function (button) {
				button.disabled = false;
			});
		});
	}

	function init(root) {
		var initial = root.querySelector('[data-nlps-unit].is-active') || root.querySelector('[data-nlps-unit]');
		if (initial) {
			selectUnit(root, initial);
		}

		root.querySelectorAll('[data-nlps-unit]').forEach(function (button) {
			button.addEventListener('click', function () {
				selectUnit(root, button);
			});
		});

		var dismiss = root.querySelector('[data-nlps-dismiss]');
		if (dismiss) {
			dismiss.addEventListener('click', function () {
				var card = root.querySelector('[data-nlps-card]');
				if (card) {
					card.hidden = true;
				}
			});
		}

		root.querySelectorAll('[data-nlps-tab]').forEach(function (button) {
			button.addEventListener('click', function () {
				root.querySelectorAll('[data-nlps-tab]').forEach(function (tab) {
					tab.classList.toggle('is-active', tab === button);
				});
				setPanel(root, button.dataset.nlpsTab);
			});
		});

		root.querySelectorAll('[data-nlps-lead-form]').forEach(function (form) {
			form.addEventListener('submit', function (event) {
				event.preventDefault();
				submitLead(root, form, event.submitter || form.querySelector('button[type="submit"]'));
			});
		});
	}

	document.addEventListener('DOMContentLoaded', function () {
		document.querySelectorAll('[data-nlps-showroom]').forEach(init);
	});
}());
