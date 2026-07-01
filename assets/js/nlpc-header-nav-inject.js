/* Injects a working hamburger toggle into the child theme header, since the
 * child theme's own header.html can't be deployed from here right now
 * (see assets/css/nlpc-header-parent-override.css for why). Safe to remove
 * once the child theme has its own working Git deploy and platform-nav.js
 * is confirmed live. */
(function () {
	'use strict';
	var header = document.querySelector('.nlpc-site-header');
	if (!header) return;
	var inner = header.querySelector('.nlpc-site-header__inner');
	var nav = header.querySelector('.nlpc-primary-nav');
	if (!inner || !nav) return;

	// Don't double-inject if the child theme's own toggle ever does deploy.
	if (header.querySelector('.nlpc-nav-toggle')) return;

	var toggle = document.createElement('button');
	toggle.type = 'button';
	toggle.className = 'nlpc-nav-toggle-injected';
	toggle.setAttribute('aria-expanded', 'false');
	toggle.setAttribute('aria-controls', 'nlpc-primary-nav-injected');
	toggle.setAttribute('aria-label', 'פתיחת תפריט ניווט');
	toggle.innerHTML = '<span></span><span></span><span></span>';
	inner.appendChild(toggle);
	nav.id = nav.id || 'nlpc-primary-nav-injected';

	function isOpen() { return header.classList.contains('is-nav-open-injected'); }
	function setOpen(open) {
		header.classList.toggle('is-nav-open-injected', open);
		toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
	}

	toggle.addEventListener('click', function () { setOpen(!isOpen()); });
	document.addEventListener('keydown', function (e) {
		if (e.key === 'Escape' && isOpen()) setOpen(false);
	});
	document.addEventListener('click', function (e) {
		if (isOpen() && !header.contains(e.target)) setOpen(false);
	});
	nav.querySelectorAll('a').forEach(function (a) {
		a.addEventListener('click', function () { setOpen(false); });
	});
	window.addEventListener('resize', function () {
		if (window.innerWidth > 760 && isOpen()) setOpen(false);
	});
})();
