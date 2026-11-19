/* ProjectShell row (HAD-794, inc/project-shell.php): the live call sheet, the film player, the 360 link and the basket
 * slot's events, on every developer project page in every language. Contracts: package 2 (the call lives at
 * /tour/designer/?project=&call=1&lang=, call.js is theirs), package 4 (fills [data-nl-slot="basket"], listens to
 * nadlan:shell-ready and nadlan:unit-picked), package 5 (window.nlTrack). */
(function () {
  'use strict';
  var row = document.querySelector('.nlsh');
  if (!row) return;
  var sheet = document.getElementById('nlsh-sheet');
  var project = row.getAttribute('data-project') || '';
  var lang = row.getAttribute('lang') || 'he';
  var slot = row.querySelector('[data-nl-slot="basket"]');
  var picked = null;
  function track(n, d) { try { if (window.nlTrack) window.nlTrack(n, d || {}); } catch (e) { /* optional */ } }
  function ga(n, d) { try { if (window.nadlanGA) window.nadlanGA(n, d || {}); } catch (e) { /* optional */ } }
  function withUnit(href) {
    if (!picked || !picked.unit || href.indexOf('/tour/designer/') < 0) return href;
    try { var u = new URL(href, location.href); u.searchParams.set('unit', picked.unit); return u.toString(); } catch (e) { return href; }
  }
  function openSheet(src) {
    track('call_open', { k: 'video', src: src || 'row' });
    ga('call_open', { project: project, source: src || 'row' });
    if (!sheet || typeof sheet.showModal !== 'function') { var a = row.querySelector('[data-nlsh="call"]'); if (a) location.href = withUnit(a.href); return; }
    var go = sheet.querySelector('[data-nlsh="call-go"]');
    if (go) go.href = withUnit(go.getAttribute('href'));
    sheet.showModal();
    if (go) go.focus();
  }
  function openFilm(btn) {
    var d = document.getElementById('nlsh-film');
    if (!d) {
      d = document.createElement('dialog');
      d.id = 'nlsh-film';
      d.className = 'nlsh-film';
      d.setAttribute('dir', row.getAttribute('dir') || 'rtl');
      var f = document.createElement('form'); f.method = 'dialog'; f.className = 'nlsh-x';
      var x = document.createElement('button'); x.type = 'submit'; var cl = sheet && sheet.querySelector('.nlsh-x button'); x.setAttribute('aria-label', cl ? cl.getAttribute('aria-label') : 'Close'); x.innerHTML = '&times;';
      f.appendChild(x); d.appendChild(f);
      var v = document.createElement('video');
      v.controls = true; v.playsInline = true; v.preload = 'metadata';
      v.setAttribute('playsinline', ''); v.poster = btn.getAttribute('data-poster') || '';
      v.src = btn.getAttribute('data-src');
      d.appendChild(v);
      d.addEventListener('close', function () { try { v.pause(); } catch (e) { /* closed */ } });
      document.body.appendChild(d);
    }
    if (typeof d.showModal === 'function') d.showModal(); else d.setAttribute('open', '');
    var vid = d.querySelector('video');
    if (vid) { var p = vid.play(); if (p && p.catch) p.catch(function () {}); }
    track('film_open', { project: project });
    ga('film_open', { project: project, source: 'shell' });
  }

  row.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-nlsh]') : null;
    if (!b) return;
    var k = b.getAttribute('data-nlsh');
    if (k === 'call') { e.preventDefault(); openSheet('row'); }
    else if (k === 'design') { b.href = withUnit(b.href); track('designer_open', { project: project }); ga('designer_open', { project: project, source: 'shell' }); }
    else if (k === 'film') { e.preventDefault(); openFilm(b); }
    else if (k === 'tour') {
      var t = document.querySelector('.rbs-act[data-act="inside"]') || document.querySelector('[data-nlps-step="inside"]');
      if (t) { t.click(); track('tour_open', { project: project }); }
    }
  });
  if (sheet) {
    sheet.addEventListener('click', function (e) {
      if (e.target === sheet) { sheet.close(); return; } // a tap outside the sheet
      var b = e.target.closest ? e.target.closest('[data-nlsh]') : null;
      if (!b) return;
      var k = b.getAttribute('data-nlsh');
      if (k === 'call-go') { track('call_start', { k: 'video', unit: picked && picked.unit || '' }); ga('call_start', { project: project }); }
      else if (k === 'book') { e.preventDefault(); sheet.close(); var s = document.getElementById('nlsch'); if (s) s.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  }
  // the page's own "video call with a representative" button (the stage hero's) opens the same sheet: now, or a booked time
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[data-nlps-ev="hero-video"], a.nlps-hero__video') : null;
    if (!a || !sheet) return;
    // the TogetherRoom's own chooser (inc/together.php) owns this button where it is printed: never take its click
    if (document.getElementById('nadlan-together-chooser-js')) return;
    e.preventDefault();
    openSheet('hero');
  }, true);

  // 360: only where the page has the inside view
  var tourBtn = row.querySelector('[data-nlsh="tour"]');
  function hasTour() { return !!(document.querySelector('.rbs-act[data-act="inside"]') || document.querySelector('[data-nlps-step="inside"]')); }
  if (tourBtn) {
    if (hasTour()) tourBtn.hidden = false;
    else setTimeout(function () { if (hasTour()) tourBtn.hidden = false; }, 4000);
  }

  // the basket slot (package 4): the page's apartment, as soon as one is picked
  window.addEventListener('nl:facing', function (e) {
    var d = e.detail || {};
    if (d.floor == null) return;
    picked = { unit: String(d.unit || ''), floor: d.floor, bearing: d.bearing };
    if (slot) slot.setAttribute('data-unit', picked.unit);
    window.dispatchEvent(new CustomEvent('nadlan:unit-picked', { detail: { project: project, lang: lang, unit: picked.unit, floor: d.floor, tower: '', bearing: d.bearing } }));
  });
  window.dispatchEvent(new CustomEvent('nadlan:shell-ready', { detail: { project: project, lang: lang, slot: slot } }));
}());
