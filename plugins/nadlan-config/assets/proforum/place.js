/* nad-lan forum: the forum inside a place page (inc/pro-forum-place.php, Claude Design board 24). No library.
   A new discussion written on a place page (its ask box opens forum.js's own compose sheet), or on the list /forum/?place=,
   carries the place: the sheet shows one line saying so and one press undoes it for this message. The place goes out through
   the form's nlfExtra('topic'), which forum.js reads when it writes; another module's nlfExtra (media.js) is wrapped, never
   replaced. The label enters the page only through textContent. Nothing is sent by itself. */
(function () {
	'use strict';
	var P = window.NLFPL || {};
	if (!P.place) { return; }
	var cf = document.querySelector('[data-nlf-composeform]');
	if (!cf) { return; }
	var cur = P.place, prev = null;

	var line = document.createElement('div'), txt = document.createElement('span'), off = document.createElement('button');
	line.className = 'nlf-tobox nlfpl-on';
	off.type = 'button'; off.className = 'nlf-link'; off.textContent = 'לא לקשר';
	line.appendChild(txt); line.appendChild(off);
	var before = cf.querySelector('[data-nlf-tobox]') || cf.querySelector('button[type="submit"]');
	if (before && before.parentNode) { before.parentNode.insertBefore(line, before); } else { cf.appendChild(line); }
	function paint() { line.hidden = !cur; txt.textContent = cur ? 'השאלה תופיע גם בדף של ' + (P.label || '') : ''; }
	off.addEventListener('click', function () { cur = ''; paint(); });
	function reset() { cur = P.place; paint(); }

	function mine(path) {
		var o = prev ? prev.call(cf, path) : null;
		if (path !== 'topic' || !cur) { return o; }
		return Object.assign({}, o || {}, { place: cur });
	}
	/* capture phase: runs before forum.js's own handlers on the button and on the form */
	document.addEventListener('click', function (e) {
		if (e.target && e.target.closest && e.target.closest('[data-nlf-compose]')) { reset(); }
	}, true);
	document.addEventListener('submit', function (e) {
		var f = e.target;
		if (f && f.matches && f.matches('[data-nlf-ask]')) { reset(); }
		if (f === cf && cf.nlfExtra !== mine) { prev = cf.nlfExtra || null; cf.nlfExtra = mine; }
	}, true);
	paint();
})();
