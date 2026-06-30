(function () {
	'use strict';
	var toggle = document.querySelector('.nlpc-nav-toggle');
	var header = document.querySelector('.nlpc-site-header');
	if (!toggle || !header) return;

	function isOpen() { return header.classList.contains('is-nav-open'); }
	function setOpen(open) {
		header.classList.toggle('is-nav-open', open);
		toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
	}

	toggle.addEventListener('click', function () { setOpen(!isOpen()); });

	document.addEventListener('keydown', function (e) {
		if (e.key === 'Escape' && isOpen()) setOpen(false);
	});

	document.addEventListener('click', function (e) {
		if (isOpen() && !header.contains(e.target)) setOpen(false);
	});

	document.querySelectorAll('.nlpc-primary-nav a').forEach(function (a) {
		a.addEventListener('click', function () { setOpen(false); });
	});

	window.addEventListener('resize', function () {
		if (window.innerWidth > 760 && isOpen()) setOpen(false);
	});
})();
