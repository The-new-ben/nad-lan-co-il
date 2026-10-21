/* CY-PRUS Instruments: bank-documents wizard UI. Mounts on <section data-cyx-tool="bank-docs">.
   The server printed the example checklist; this script rebuilds it when an answer changes. */
(function () {
  'use strict';
  var E = window.CYXBankDocs;
  if (!E) { return; }

  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (text !== undefined) { e.textContent = text; } return e; }

  function mount(root) {
    var R = JSON.parse(root.getAttribute('data-rules'));
    var T = JSON.parse(root.getAttribute('data-text'));
    var a = JSON.parse(root.getAttribute('data-example'));
    var out = root.querySelector('[data-out="list"]');

    function setChips(name, value) {
      var c = root.querySelectorAll('[data-chip="' + name + '"]'), i;
      for (i = 0; i < c.length; i += 1) { c[i].setAttribute('aria-checked', String(c[i].getAttribute('data-value') === String(value))); }
    }

    function render() {
      var r = E.checklist(a, R), i, j, g, ol, li, h, tbl, tb, tr, f, frag = document.createDocumentFragment();
      root.querySelector('[data-out="count"]').textContent = T.count.replace('{n}', r.count);
      for (i = 0; i < r.groups.length; i += 1) {
        g = r.groups[i];
        frag.appendChild(el('h3', 'cyx-list__title', T.groups[g.key]));
        ol = el('ul', 'cyx-list');
        for (j = 0; j < g.items.length; j += 1) {
          li = el('li', 'cyx-list__item', g.items[j].text);
          if (g.items[j].who) { li.appendChild(el('span', 'cyx-list__who', g.items[j].who)); }
          ol.appendChild(li);
        }
        frag.appendChild(ol);
      }
      frag.appendChild(el('h3', 'cyx-list__title', T.h_channels));
      ol = el('ul', 'cyx-list');
      for (i = 0; i < r.channels.length; i += 1) {
        li = el('li', 'cyx-list__item'); li.appendChild(el('strong', null, r.channels[i].bank + ': ')); li.appendChild(document.createTextNode(r.channels[i].text)); ol.appendChild(li);
      }
      frag.appendChild(ol);
      frag.appendChild(el('h3', 'cyx-list__title', T.h_fees));
      h = el('div', 'cyx-break-wrap'); tbl = el('table', 'cyx-break');
      tbl.innerHTML = '<thead><tr><th scope="col"></th><th scope="col"></th><th scope="col"></th><th scope="col"></th></tr></thead>';
      var ths = tbl.querySelectorAll('th'); ths[0].textContent = T.th_bank; ths[1].textContent = T.th_open; ths[2].textContent = T.th_keep; ths[3].textContent = T.th_table;
      tb = el('tbody');
      for (i = 0; i < r.fees.length; i += 1) {
        f = r.fees[i]; tr = el('tr', 'cyx-row');
        var th = el('th', null, f.bank); th.setAttribute('scope', 'row'); tr.appendChild(th);
        tr.appendChild(el('td', 'cyx-rule', f.open)); tr.appendChild(el('td', 'cyx-rule', f.keep)); tr.appendChild(el('td', 'cyx-num', f.table));
        tb.appendChild(tr);
      }
      tbl.appendChild(tb); h.appendChild(tbl); frag.appendChild(h);
      if (r.basic) { frag.appendChild(el('h3', 'cyx-list__title', T.h_basic)); frag.appendChild(el('p', 'cyx-list__note', r.basic)); }
      for (i = 0; i < r.always.length; i += 1) { frag.appendChild(el('p', 'cyx-list__note', r.always[i])); }
      out.textContent = ''; out.appendChild(frag);
    }

    root.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-chip]'), btn = ev.target.closest('[data-copy]'), n, v, text, note;
      if (chip) {
        n = chip.getAttribute('data-chip'); v = chip.getAttribute('data-value');
        a[n] = n === 'hebrew' ? v === 'yes' : v;
        setChips(n, v); render();
      }
      if (btn) {
        text = out.innerText;
        note = root.querySelector('[data-out="copied"]');
        try {
          navigator.clipboard.writeText(text).then(function () { note.hidden = false; }, function () { note.hidden = true; });
        } catch (err) { note.hidden = true; }
      }
    });
    render();
  }

  function boot() {
    var n = document.querySelectorAll('[data-cyx-tool="bank-docs"]'), i;
    for (i = 0; i < n.length; i += 1) { try { mount(n[i]); } catch (err) { /* fail open: the printed checklist stays */ } }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
