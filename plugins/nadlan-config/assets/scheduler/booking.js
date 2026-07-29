/* NadLan scheduler widget - date strip + time grid + confirm form.
   Mount: #nlsch-mount (data-card, data-kind, data-lang, data-rest, data-i18n).
   2 taps to a slot, one form, WhatsApp-first confirmation. No new floating
   elements: a small anchor button is appended into the EXISTING CTA rows. */
(function () {
	'use strict';
	var mount = document.getElementById('nlsch-mount');
	if (!mount) { return; }
	var REST = mount.dataset.rest.replace(/\/$/, '');
	var CARD = parseInt(mount.dataset.card, 10);
	var LANG = mount.dataset.lang || 'he';
	var I = {};
	try { I = JSON.parse(mount.dataset.i18n || '{}'); } catch (e) { I = {}; }
	var state = { days: [], slotMin: 30, day: null, time: null };

	function el(tag, cls, text) {
		var n = document.createElement(tag);
		if (cls) { n.className = cls; }
		if (text) { n.textContent = text; }
		return n;
	}

	function dayLabel(d, idx) {
		if (idx === 0) { return I.today || ''; }
		if (idx === 1) { return I.tomorrow || ''; }
		return (I.day_names && I.day_names[d.dow]) || '';
	}

	function fmtDate(dateStr) {
		var p = dateStr.split('-');
		return p[2].replace(/^0/, '') + '.' + p[1].replace(/^0/, '');
	}

	function render() {
		mount.innerHTML = '';
		var withSlots = state.days.filter(function (d) { return d.slots.length; });
		if (!withSlots.length) {
			mount.appendChild(el('div', 'nlsch-empty', I.no_slots || ''));
			return;
		}
		if (!state.day || !state.days.some(function (d) { return d.date === state.day && d.slots.length; })) {
			state.day = withSlots[0].date;
		}
		mount.appendChild(el('p', 'nlsch-lbl', I.pick_day || ''));
		var strip = el('div', 'nlsch-days');
		state.days.forEach(function (d, idx) {
			var b = el('button', 'nlsch-day' + (d.slots.length ? '' : ' is-off') + (d.date === state.day ? ' is-on' : ''));
			b.type = 'button';
			b.appendChild(el('span', '', dayLabel(d, idx)));
			b.appendChild(el('b', '', fmtDate(d.date)));
			if (d.slots.length) {
				b.addEventListener('click', function () { state.day = d.date; state.time = null; render(); });
			} else {
				b.disabled = true;
				b.title = I.closed || '';
			}
			strip.appendChild(b);
		});
		mount.appendChild(strip);

		mount.appendChild(el('p', 'nlsch-lbl', I.pick_time || ''));
		var times = el('div', 'nlsch-times');
		var active = state.days.filter(function (d) { return d.date === state.day; })[0];
		(active ? active.slots : []).forEach(function (t) {
			var b = el('button', 'nlsch-time' + (t === state.time ? ' is-on' : ''), t);
			b.type = 'button';
			b.addEventListener('click', function () { state.time = t; render(); openForm(); });
			times.appendChild(b);
		});
		mount.appendChild(times);

		var form = buildForm();
		mount.appendChild(form);
		if (state.time) { form.classList.add('is-open'); }
	}

	var saved = { name: '', phone: '', email: '', note: '' };
	function buildForm() {
		var f = el('form', 'nlsch-form');
		var sel = el('p', 'nlsch-sel', (I.selected || '') + ': ' + (state.time ? fmtDate(state.day) + ' · ' + state.time + ' (' + state.slotMin + ' ' + (I.minutes || '') + ')' : ''));
		f.appendChild(sel);
		[['name', I.f_name, 'text'], ['phone', I.f_phone, 'tel'], ['email', I.f_email, 'email']].forEach(function (row) {
			var inp = el('input');
			inp.type = row[2];
			inp.name = row[0];
			inp.placeholder = row[1] || '';
			inp.value = saved[row[0]] || '';
			inp.addEventListener('input', function () { saved[row[0]] = inp.value; });
			if (row[0] !== 'email') { inp.required = true; }
			f.appendChild(inp);
		});
		var note = el('textarea');
		note.name = 'note';
		note.placeholder = I.f_note || '';
		note.value = saved.note || '';
		note.addEventListener('input', function () { saved.note = note.value; });
		f.appendChild(note);
		var hp = el('input');
		hp.type = 'text'; hp.name = 'company'; hp.tabIndex = -1; hp.autocomplete = 'off';
		hp.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;opacity:0';
		f.appendChild(hp);
		var go = el('button', 'nlsch-go', I.submit || '');
		go.type = 'submit';
		f.appendChild(go);
		var err = el('p', 'nlsch-err');
		f.appendChild(err);
		f.addEventListener('submit', function (e) {
			e.preventDefault();
			err.style.display = 'none';
			if (!saved.name.trim() || saved.phone.replace(/\D/g, '').length < 9) {
				err.textContent = I.err_fields || ''; err.style.display = 'block'; return;
			}
			go.disabled = true;
			go.textContent = I.sending || '';
			fetch(REST + '/appt-book', {
				method: 'POST', headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					card: CARD, start: state.day + ' ' + state.time, lang: LANG,
					name: saved.name, phone: saved.phone, email: saved.email, note: saved.note,
					company: hp.value
				})
			}).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, status: r.status, j: j }; }); })
			.then(function (res) {
				if (res.ok && res.j && res.j.ok) { showOk(res.j); return; }
				go.disabled = false; go.textContent = I.submit || '';
				if (res.status === 409) {
					err.textContent = I.err_taken || ''; err.style.display = 'block';
					load();
				} else {
					err.textContent = (res.j && res.j.message) || I.err_generic || ''; err.style.display = 'block';
				}
			}).catch(function () {
				go.disabled = false; go.textContent = I.submit || '';
				err.textContent = I.err_generic || ''; err.style.display = 'block';
			});
		});
		return f;
	}

	function gcalUrl(j) {
		return 'https://calendar.google.com/calendar/render?action=TEMPLATE'
			+ '&text=' + encodeURIComponent(j.card || 'NadLan')
			+ '&dates=' + j.utc_start + '/' + j.utc_end
			+ '&details=' + encodeURIComponent((I.ok_sub || '') + ' ' + j.ref)
			+ (j.url ? '&location=' + encodeURIComponent(j.url) : '');
	}

	function showOk(j) {
		try { localStorage.setItem('nlsch_last', JSON.stringify({ id: j.id, token: j.token, ref: j.ref })); } catch (e) {}
		mount.innerHTML = '';
		var ok = el('div', 'nlsch-ok is-open');
		ok.appendChild(el('h3', '', (I.ok_title || '') + ' ✓'));
		ok.appendChild(el('p', '', j.card + ' · ' + j.start + '. ' + (I.ok_sub || '') + ' ' + j.ref));
		var row = el('div', 'row');
		if (j.whatsapp) {
			var wa = el('a', 'btn wa', I.wa_btn || '');
			wa.href = j.whatsapp; wa.target = '_blank'; wa.rel = 'noopener';
			row.appendChild(wa);
		}
		var ics = el('a', 'btn lite', I.ics_btn || '');
		ics.href = j.ics;
		row.appendChild(ics);
		var g = el('a', 'btn lite', I.gcal_btn || '');
		g.href = gcalUrl(j); g.target = '_blank'; g.rel = 'noopener';
		row.appendChild(g);
		ok.appendChild(row);
		var cancel = el('button', 'nlsch-cancel', I.cancel_btn || '');
		cancel.type = 'button';
		cancel.addEventListener('click', function () {
			cancel.disabled = true;
			fetch(REST + '/appt-cancel', {
				method: 'POST', headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ id: j.id, token: j.token })
			}).then(function (r) {
				if (r.ok) {
					ok.innerHTML = '';
					ok.appendChild(el('p', '', I.cancelled || ''));
					state.time = null;
					load();
				} else { cancel.disabled = false; }
			});
		});
		ok.appendChild(cancel);
		mount.appendChild(ok);
	}

	function openForm() {
		var f = mount.querySelector('.nlsch-form');
		if (f) {
			f.classList.add('is-open');
			var first = f.querySelector('input[name="name"]');
			if (first && !first.value) { first.focus(); }
		}
	}

	function load() {
		fetch(REST + '/appt-slots?card=' + CARD).then(function (r) { return r.json(); }).then(function (j) {
			if (!j || !j.days) { return; }
			state.days = j.days;
			state.slotMin = j.slot_min || 30;
			render();
		}).catch(function () {
			mount.appendChild(el('div', 'nlsch-empty', I.err_generic || ''));
		});
	}

	// One-of-everything law: no new floating element. Add a quiet anchor
	// button into the EXISTING CTA rows so the booking band is reachable.
	function anchorInto() {
		var row = document.querySelector('.nlpp-ctas') || document.querySelector('.nlx-cta');
		if (!row || row.querySelector('.nlsch-jump')) { return; }
		var a = el('a', 'nlsch-jump', I.book_anchor || '');
		a.href = '#nlsch';
		a.style.cssText = 'display:inline-block;border:1.5px solid #9C7A3C;color:#9C7A3C;background:#fff;border-radius:12px;padding:11px 18px;font:700 13.5px Heebo,sans-serif;text-decoration:none';
		a.addEventListener('click', function (e) {
			e.preventDefault();
			var s = document.getElementById('nlsch');
			if (s) { s.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
		});
		row.appendChild(a);
	}

	load();
	anchorInto();
})();
