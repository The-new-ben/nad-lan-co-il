/* CY-PRUS Instruments: title-deeds risk UI. Mounts on <section data-cyx-tool="title-risk">. */
(function () {
  'use strict';
  var E = window.CYXTitleRisk;
  if (!E) { return; }

  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (text !== undefined) { e.textContent = text; } return e; }

  function mount(root) {
    var R = JSON.parse(root.getAttribute('data-rules'));
    var T = JSON.parse(root.getAttribute('data-text'));
    var a = JSON.parse(root.getAttribute('data-example'));
    var q = function (s) { return root.querySelector(s); };

    function setChips(name, value) {
      var c = root.querySelectorAll('[data-chip="' + name + '"]'), i;
      for (i = 0; i < c.length; i += 1) { c[i].setAttribute('aria-checked', String(c[i].getAttribute('data-value') === String(value))); }
    }
    function render() {
      var r = E.assess(a, R), fl = q('[data-out="flags"]'), ll = q('[data-out="list"]'), i, li;
      q('[data-out="level"]').textContent = T.levels[r.level];
      q('.cyx-result').setAttribute('data-level', r.level);
      fl.textContent = '';
      if (!r.flags.length) { fl.appendChild(el('li', 'cyx-check cyx-check--ok', T.none)); }
      for (i = 0; i < r.flags.length; i += 1) {
        li = el('li', 'cyx-check ' + (r.flags[i].level === 'high' ? 'cyx-check--no' : 'cyx-check--warn'));
        li.appendChild(el('span', 'cyx-check__why', T.flags[r.flags[i].id]));
        fl.appendChild(li);
      }
      ll.textContent = '';
      for (i = 0; i < r.lawyerList.length; i += 1) { ll.appendChild(el('li', null, r.lawyerList[i])); }
    }
    root.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-chip]'), btn = ev.target.closest('[data-copy]'), n, v, note;
      if (chip) { n = chip.getAttribute('data-chip'); v = chip.getAttribute('data-value'); a[n] = v; setChips(n, v); render(); }
      if (btn) {
        note = q('[data-out="copied"]');
        try { navigator.clipboard.writeText(q('[data-out="list"]').innerText).then(function () { note.hidden = false; }, function () { note.hidden = true; }); }
        catch (err) { note.hidden = true; }
      }
    });
    render();
  }

  function boot() {
    var n = document.querySelectorAll('[data-cyx-tool="title-risk"]'), i;
    for (i = 0; i < n.length; i += 1) { try { mount(n[i]); } catch (err) { /* fail open */ } }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
