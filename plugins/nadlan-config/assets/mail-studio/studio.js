/* Mail studio, "דיוור נדל״ן" (HAD-687): live preview, test send, send, list sync and import. */
(function () {
	'use strict';
	var C = window.NLMS || {};
	function $(s, r) { return (r || document).querySelector(s); }
	function call(path, data) {
		return fetch(C.root + path, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-WP-Nonce': C.nonce }, body: JSON.stringify(data || {}) })
			.then(function (r) { return r.json().then(function (j) { if (!r.ok) { throw new Error(j && j.message ? j.message : 'שגיאה ' + r.status); } return j; }); });
	}
	function say(el, t, bad) { if (!el) { return; } el.textContent = t; el.className = bad ? 'nlms-bad' : 'nlms-ok'; }

	var form = $('#nlms-form');
	if (form) {
		var frame = $('#nlms-frame'), meta = $('#nlms-meta'), msg = $('#nlms-msg'), timer = null, last = null;
		var data = function () {
			var o = {};
			new FormData(form).forEach(function (v, k) { o[k] = v; });
			o.sign = $('[name=sign]', form).checked ? 1 : '';
			return o;
		};
		var sync = function () {
			var d = data(), dist = d.kind === 'dist', inv = d.kind === 'invite';
			$('.nlms-personal', form).hidden = dist || inv;
			$('.nlms-dist-note', form).hidden = !dist;
			$('.nlms-invite-note', form).hidden = !inv;
			$('.nlms-seg', form).hidden = !(dist || inv);
			$('.nlms-update', form).hidden = d.look !== 'update' || inv;
			$('.nlms-items', form).hidden = inv;
			$('.nlms-filmbox', form).hidden = inv;
			$('#nlms-send').textContent = inv ? 'שליחת ההזמנות' : (dist ? 'שליחה לרשימה' : 'שליחה');
		};
		/* the recommended wording: an invitation asks only for consent (no pitch, no film); the offer goes after a "yes" */
		var INVITE = {
			developer: ['שאלה קצרה מנדל״ן', 'האם תשמחו לקבל מאיתנו הצעות לחשיפת הפרויקטים של {חברה}?', 'שלום {שם},', 'אני בן מנדל״ן (nad-lan.co.il), אתר מידע על פרויקטים חדשים ונדל״ן בישראל.\n\nהאם תשמחו שאשלח אליכם מדי פעם עדכונים והצעות לחשיפת הפרויקטים של {חברה} באתר?\n\nלחיצה על "כן, אשמח לקבל" מאשרת קבלת עדכונים, הצעות ופרסומים מנדל״ן במייל. אפשר להסיר בכל רגע.'],
			broker: ['שאלה קצרה מנדל״ן', 'האם תשמח/י לקבל מאיתנו הצעות לשיתוף פעולה?', 'שלום {שם},', 'אני בן מנדל״ן (nad-lan.co.il), אתר מידע על נדל״ן בישראל.\n\nהאם תשמח/י שאשלח מדי פעם עדכונים והצעות לחשיפת הנכסים שלך באתר ולשיתוף פעולה?\n\nלחיצה על "כן, אשמח לקבל" מאשרת קבלת עדכונים, הצעות ופרסומים מנדל״ן במייל. אפשר להסיר בכל רגע.'],
			pro: ['שאלה קצרה מנדל״ן', 'האם תשמח/י לקבל מאיתנו הצעות לחשיפת השירות שלך?', 'שלום {שם},', 'אני בן מנדל״ן (nad-lan.co.il), אתר מידע על נדל״ן בישראל, שקונים ומוכרים בודקים בו לפני עסקה.\n\nהאם תשמח/י שאשלח מדי פעם עדכונים והצעות לחשיפת השירות שלך באתר?\n\nלחיצה על "כן, אשמח לקבל" מאשרת קבלת עדכונים, הצעות ופרסומים מנדל״ן במייל. אפשר להסיר בכל רגע.']
		};
		var fill = $('#nlms-fill');
		if (fill) {
			fill.addEventListener('click', function () {
				var seg = $('[name=seg]', form).value, t = INVITE[seg] || INVITE.developer;
				if (!INVITE[seg]) { $('[name=seg]', form).value = 'developer'; }
				$('[name=subject]', form).value = t[0]; $('[name=pre]', form).value = t[1]; $('[name=title]', form).value = '';
				$('[name=greeting]', form).value = t[2]; $('[name=body]', form).value = t[3];
				sync(); preview();
			});
		}
		var preview = function () {
			clearTimeout(timer);
			timer = setTimeout(function () {
				call('ms/preview', data()).then(function (j) {
					last = j;
					frame.srcdoc = j.html;
					meta.textContent = 'נושא: ' + (j.subject || '(אין עדיין)') + ' · ' + Math.round(j.bytes / 1024) + 'KB' + (j.items ? ' · ' + j.items + ' נכסים' : '') + (data().kind === 'dist' ? ' · ברשימה: ' + j.audience : '');
				}).catch(function (e) { meta.textContent = e.message; });
			}, 350);
		};
		form.addEventListener('input', function () { sync(); preview(); });
		form.addEventListener('change', function () { sync(); preview(); });
		document.querySelectorAll('.nlms-pv-bar [data-w]').forEach(function (b) {
			b.addEventListener('click', function () { frame.style.width = b.getAttribute('data-w') + 'px'; });
		});
		$('#nlms-test').addEventListener('click', function () {
			var to = window.prompt('לאיזו כתובת לשלוח את הבדיקה?', C.me || '');
			if (!to) { return; }
			var d = data(); d.test_to = to;
			say(msg, 'שולח בדיקה...');
			call('ms/test', d).then(function (j) { say(msg, j.ok ? 'נשלחה בדיקה אל ' + j.to : 'לא נשלח: ' + j.err, !j.ok); }).catch(function (e) { say(msg, e.message, true); });
		});
		$('#nlms-send').addEventListener('click', function () {
			var d = data();
			if (!d.subject) { say(msg, 'חסר נושא', true); return; }
			if (d.kind === 'dist' || d.kind === 'invite') {
				var n = last ? last.audience : 0;
				if (!window.confirm((d.kind === 'invite' ? 'לשלוח הזמנה אחת אל ' + n + ' עסקים שעוד לא הוזמנו?' : 'לשלוח את "' + (last ? last.subject : d.subject) + '" אל ' + n + ' אנשים ברשימת התפוצה?') + ' אי אפשר לבטל אחרי השליחה.')) { return; }
				d.confirm = 1;
			} else if (!window.confirm('לשלוח אל ' + d.to + '?')) { return; }
			say(msg, 'שולח...');
			call('ms/send', d).then(function (j) {
				if (d.kind === 'personal') { say(msg, j.ok ? 'נשלח אל ' + d.to : 'לא נשלח: ' + j.err, !j.ok); return; }
				say(msg, 'ההפצה יצאה לדרך: ' + j.total + ' נמענים. אפשר לראות את ההתקדמות בלשונית "נשלחו".');
				var left = j.total - j.first_batch, tick = function () {
					if (left <= 0) { return; }
					call('ms/tick', {}).then(function (t) { left -= t.sent; if (t.cap) { say(msg, 'הגענו למכסה היומית. השאר יישלחו מחר מעצמם.'); return; } setTimeout(tick, 60000); }).catch(function () { setTimeout(tick, 60000); });
				};
				setTimeout(tick, 60000);
			}).catch(function (e) { say(msg, e.message, true); });
		});
		sync();
		preview();
	}

	var syncBtn = $('#nlms-sync');
	if (syncBtn) {
		syncBtn.addEventListener('click', function () {
			var m = $('#nlms-sync-msg');
			say(m, 'מייבא...');
			call('ms/sync', {}).then(function (j) { say(m, 'חדשים: ' + j.new + ' · עודכנו: ' + j.up + ' · כבר ברשימה: ' + j.same + (j.bad ? ' · כתובות לא תקינות: ' + j.bad : '')); setTimeout(function () { location.reload(); }, 1500); })
				.catch(function (e) { say(m, e.message, true); });
		});
	}
	var imp = $('#nlms-import');
	if (imp) {
		$('#nlms-import-go').addEventListener('click', function () {
			var m = $('#nlms-import-msg'), o = {};
			new FormData(imp).forEach(function (v, k) { o[k] = v; });
			if (o.basis === 'business' ? !o.business_ok : !o.consent_ok) { say(m, o.basis === 'business' ? 'צריך לאשר שאלה כתובות של עסקים' : 'צריך לאשר שיש לכולם הסכמה מתועדת', true); return; }
			say(m, 'מייבא...');
			call('ms/import', o).then(function (j) { say(m, 'חדשים: ' + j.new + ' · עודכנו: ' + j.up + ' · כבר ברשימה: ' + j.same + ' · לא תקינים: ' + j.bad); setTimeout(function () { location.reload(); }, 1800); })
				.catch(function (e) { say(m, e.message, true); });
		});
	}
})();
