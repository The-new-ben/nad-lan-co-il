/*!
 * nad-lan accessibility widget — IS 5568 / WCAG-oriented, self-contained.
 * No dependencies. Injects its own styles + a floating toggle (the standard
 * accessibility person icon). Preferences persist in localStorage.
 */
(function () {
	'use strict';
	if (window.__nadlanA11yLoaded) return;
	window.__nadlanA11yLoaded = true;

	var KEY = 'nadlan_a11y_v1';
	var state = {};
	try { state = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { state = {}; }

	var STEPS = ['fontUp', 'fontDown', 'contrast', 'invert', 'grayscale', 'links', 'readable', 'bigCursor', 'pause', 'spacing'];

	// ---- styles ----
	var css = ''
		+ '#nla-btn{position:fixed;bottom:20px;inset-inline-start:20px;z-index:99995;width:54px;height:54px;border-radius:50%;border:0;cursor:pointer;background:linear-gradient(135deg,#11110F,#2B2924);box-shadow:0 10px 28px rgba(0,0,0,.35);display:grid;place-items:center;transition:transform .2s}'
		+ '#nla-btn:hover{transform:translateY(-3px)}'
		+ '#nla-btn svg{width:30px;height:30px;fill:#fff}'
		+ '#nla-btn:focus-visible{outline:3px solid #9C7A3C;outline-offset:3px}'
		+ '#nla-panel{position:fixed;bottom:84px;inset-inline-start:20px;z-index:99996;width:300px;max-width:calc(100vw - 40px);max-height:78vh;overflow:auto;background:#fff;color:#11110F;border-radius:16px;box-shadow:0 24px 60px rgba(0,0,0,.32);font-family:Heebo,system-ui,sans-serif;direction:rtl;padding:16px;display:none}'
		+ '#nla-panel.open{display:block}'
		+ '#nla-panel h2{font-size:16px;margin:0 0 4px;font-weight:700}'
		+ '#nla-panel p.sub{font-size:12px;color:#6D665C;margin:0 0 12px}'
		+ '.nla-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}'
		+ '.nla-grid button{font:inherit;font-size:13px;font-weight:600;padding:11px 8px;border:1px solid #DDD6C8;border-radius:10px;background:#FAF8F3;color:#11110F;cursor:pointer;min-height:44px;display:flex;align-items:center;justify-content:center;gap:6px;text-align:center;transition:border-color .15s,background .15s}'
		+ '.nla-grid button:hover{border-color:#9C7A3C;background:#F3EFE7}'
		+ '.nla-grid button.on{background:#11110F;color:#fff;border-color:#11110F}'
		+ '.nla-grid button:focus-visible{outline:3px solid #9C7A3C;outline-offset:2px}'
		+ '#nla-reset{margin-top:10px;width:100%;font:inherit;font-weight:700;padding:12px;border:1px solid #11110F;border-radius:10px;background:#fff;cursor:pointer;min-height:44px}'
		+ '#nla-reset:hover{background:#F3EFE7}'
		+ '#nla-close{position:absolute;inset-inline-end:12px;inset-block-start:12px;border:0;background:none;font-size:22px;line-height:1;cursor:pointer;color:#6D665C;width:32px;height:32px;border-radius:50%}'
		+ '#nla-close:hover{background:#F3EFE7}'
		// effect classes on <html>
		+ 'html.nla-contrast body{background:#000 !important}'
		+ 'html.nla-contrast body, html.nla-contrast body *:not(svg):not(path):not(#nla-panel):not(#nla-panel *):not(#nla-btn):not(#nla-btn *){background-color:#000 !important;color:#ffff00 !important;border-color:#ffff00 !important}'
		+ 'html.nla-invert{filter:invert(1) hue-rotate(180deg)}'
		+ 'html.nla-invert #nla-btn,html.nla-invert #nla-panel{filter:invert(1) hue-rotate(180deg)}'
		+ 'html.nla-grayscale{filter:grayscale(1)}'
		+ 'html.nla-grayscale.nla-invert{filter:grayscale(1) invert(1) hue-rotate(180deg)}'
		+ 'html.nla-links a{text-decoration:underline !important;outline:2px solid #9C7A3C !important;outline-offset:1px}'
		+ 'html.nla-readable body, html.nla-readable body *:not(.nla-grid *):not(#nla-btn *){font-family:Arial,Helvetica,sans-serif !important;letter-spacing:.02em}'
		+ 'html.nla-bigcursor, html.nla-bigcursor *{cursor:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'48\' height=\'48\' viewBox=\'0 0 48 48\'%3E%3Cpath fill=\'%23000\' stroke=\'%23fff\' stroke-width=\'2\' d=\'M8 4l28 16-12 3-3 13z\'/%3E%3C/svg%3E") 4 4, auto !important}'
		+ 'html.nla-spacing body, html.nla-spacing p, html.nla-spacing li{letter-spacing:.08em !important;word-spacing:.16em !important;line-height:2 !important}'
		+ 'html.nla-pause *{animation-play-state:paused !important;transition:none !important}'
		+ '@media (max-width:520px){#nla-btn{bottom:14px;inset-inline-start:14px;width:50px;height:50px}#nla-panel{bottom:74px;inset-inline-start:14px}}';

	var st = document.createElement('style');
	st.id = 'nla-style';
	st.textContent = css;
	document.head.appendChild(st);

	// ---- button ----
	var btn = document.createElement('button');
	btn.id = 'nla-btn';
	btn.setAttribute('aria-label', 'תפריט נגישות');
	btn.setAttribute('aria-expanded', 'false');
	btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="3.5" r="2"/><path d="M21 7c-2.6.9-5.4 1.4-9 1.4S5.6 7.9 3 7l-.5 1.9c2 .7 4.2 1.2 6.5 1.4l-.8 5.3L6.7 22l1.9.5 1.6-5.1c.3-1 .5-1 .8 0l1.6 5.1 1.9-.5-1.5-6.4-.8-5.3c2.3-.2 4.5-.7 6.5-1.4z"/></svg>';
	document.body.appendChild(btn);

	// ---- panel ----
	var panel = document.createElement('div');
	panel.id = 'nla-panel';
	panel.setAttribute('role', 'dialog');
	panel.setAttribute('aria-label', 'אפשרויות נגישות');
	panel.innerHTML = ''
		+ '<button id="nla-close" aria-label="סגירה">×</button>'
		+ '<h2>נגישות</h2><p class="sub">התאמת התצוגה לצרכים שלך. ההעדפות נשמרות.</p>'
		+ '<div class="nla-grid">'
		+ '<button data-act="fontUp">הגדלת טקסט</button>'
		+ '<button data-act="fontDown">הקטנת טקסט</button>'
		+ '<button data-act="contrast">ניגודיות גבוהה</button>'
		+ '<button data-act="invert">היפוך צבעים</button>'
		+ '<button data-act="grayscale">גווני אפור</button>'
		+ '<button data-act="links">הדגשת קישורים</button>'
		+ '<button data-act="readable">גופן קריא</button>'
		+ '<button data-act="spacing">ריווח אותיות</button>'
		+ '<button data-act="bigCursor">סמן גדול</button>'
		+ '<button data-act="pause">עצירת אנימציות</button>'
		+ '</div>'
		+ '<button id="nla-reset">איפוס הגדרות</button>';
	document.body.appendChild(panel);

	var fontScale = state.fontScale || 0;

	function applyFont() {
		var pct = 100 + fontScale * 10;
		document.documentElement.style.fontSize = fontScale ? pct + '%' : '';
	}
	function applyToggles() {
		document.documentElement.classList.toggle('nla-contrast', !!state.contrast);
		document.documentElement.classList.toggle('nla-invert', !!state.invert);
		document.documentElement.classList.toggle('nla-grayscale', !!state.grayscale);
		document.documentElement.classList.toggle('nla-links', !!state.links);
		document.documentElement.classList.toggle('nla-readable', !!state.readable);
		document.documentElement.classList.toggle('nla-bigcursor', !!state.bigCursor);
		document.documentElement.classList.toggle('nla-spacing', !!state.spacing);
		document.documentElement.classList.toggle('nla-pause', !!state.pause);
		panel.querySelectorAll('.nla-grid button').forEach(function (b) {
			var a = b.getAttribute('data-act');
			b.classList.toggle('on', a === 'fontUp' ? fontScale > 0 : a === 'fontDown' ? fontScale < 0 : !!state[a]);
		});
	}
	function save() {
		state.fontScale = fontScale;
		try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
	}
	function openPanel(o) {
		panel.classList.toggle('open', o);
		btn.setAttribute('aria-expanded', o ? 'true' : 'false');
		if (o) panel.querySelector('.nla-grid button').focus();
	}

	btn.addEventListener('click', function () { openPanel(!panel.classList.contains('open')); });
	panel.querySelector('#nla-close').addEventListener('click', function () { openPanel(false); btn.focus(); });
	document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && panel.classList.contains('open')) { openPanel(false); btn.focus(); } });

	panel.querySelectorAll('.nla-grid button').forEach(function (b) {
		b.addEventListener('click', function () {
			var a = b.getAttribute('data-act');
			if (a === 'fontUp') { fontScale = Math.min(5, fontScale + 1); applyFont(); }
			else if (a === 'fontDown') { fontScale = Math.max(-3, fontScale - 1); applyFont(); }
			else { state[a] = !state[a]; }
			save(); applyToggles();
		});
	});
	panel.querySelector('#nla-reset').addEventListener('click', function () {
		state = {}; fontScale = 0; applyFont(); save();
		document.documentElement.style.fontSize = '';
		applyToggles();
	});

	applyFont();
	applyToggles();
})();
