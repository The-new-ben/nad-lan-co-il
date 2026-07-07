/* ============================================================================
   NADLAN APARTMENT STUDIO v1 (owner order 2026-07-07): the buyer designs the
   apartment BEFORE buying - drag real-size furniture on a scaled schematic
   plan built from THIS unit's real data (rooms, sqm, direction), test
   accessibility clearances (wheelchair turning circle 150cm, door clear
   width 80cm - Israeli SI 1918 language), attach notes, and send the whole
   plan to the contractor inside the RFP. Vanilla JS, RTL-aware, HE/EN via
   the engine's i18n (nlst_* keys). Honesty law: the plan is labeled a
   schematic illustration, never a sale plan.
   Opens from [data-act="studio"] in the unit panel; the engine passes
   context via window.NLStudio.open(ctx).
============================================================================ */
(function () {
  "use strict";

  /* furniture catalog - real average dimensions in cm (w x d) */
  var CATALOG = [
    { id: "sofa2", w: 160, d: 90, icon: "🛋" },
    { id: "sofa3", w: 220, d: 95, icon: "🛋" },
    { id: "bed_double", w: 160, d: 200, icon: "🛏" },
    { id: "bed_single", w: 90, d: 200, icon: "🛏" },
    { id: "table4", w: 120, d: 80, icon: "🍽" },
    { id: "table6", w: 180, d: 90, icon: "🍽" },
    { id: "wardrobe", w: 240, d: 60, icon: "🚪" },
    { id: "fridge", w: 70, d: 70, icon: "❄" },
    { id: "washer", w: 60, d: 60, icon: "🌀" },
    { id: "desk", w: 120, d: 60, icon: "💻" },
    { id: "crib", w: 70, d: 130, icon: "🍼" },
    { id: "bath", w: 170, d: 75, icon: "🛁" },
    /* accessibility templates (SI 1918 planning language) */
    { id: "wheel", w: 150, d: 150, round: true, a11y: true, icon: "♿" },
    { id: "door80", w: 80, d: 12, a11y: true, icon: "🚪" }
  ];

  var S = { ctx: null, items: [], notes: "", scale: 1, sel: null, drag: null, plan: null };

  function t(k, vars) { return S.ctx && S.ctx.t ? S.ctx.t(k, vars) : k; }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function key() { return "nlstudio:" + S.ctx.projectKey + ":" + S.ctx.unit.id; }
  function save() { try { localStorage.setItem(key(), JSON.stringify({ v: 1, items: S.items, notes: S.notes })); } catch (e) {} }
  function load() { try { return JSON.parse(localStorage.getItem(key())) || null; } catch (e) { return null; } }

  /* schematic envelope from real sqm: rooms packed in two bands, like the
     walk-inside generator - an honest illustration, not a sale plan. */
  function planRooms() {
    var u = S.ctx.unit;
    var count = Math.max(1, Math.min(8, parseFloat(u.rooms) || 4));
    var sqm = Math.max(30, parseInt(u.sqm, 10) || 85);
    var bedrooms = Math.max(0, Math.ceil(count) - 1);
    var rooms = [];
    rooms.push({ k: "salon", a: sqm * 0.42 });
    rooms.push({ k: "kitchen", a: sqm * 0.13 });
    for (var i = 1; i <= bedrooms; i++) { rooms.push({ k: i === 1 ? "master" : "bed", n: i, a: (sqm * 0.36) / bedrooms }); }
    rooms.push({ k: "bathwc", a: sqm * 0.09 });
    return rooms;
  }
  function label(r) {
    var map = { salon: "nlst_salon", kitchen: "nlst_kitchen", master: "nlst_master", bed: "nlst_bed", bathwc: "nlst_bath" };
    return t(map[r.k]) + (r.k === "bed" && r.n > 1 ? " " + r.n : "");
  }

  function open(ctx) {
    S.ctx = ctx;
    var st = load();
    S.items = (st && st.items) || [];
    S.notes = (st && st.notes) || "";
    S.sel = null;
    render();
    document.body.classList.add("nlst-lock");
  }
  function close() {
    var el = document.getElementById("nlst");
    if (el) el.remove();
    document.body.classList.remove("nlst-lock");
  }

  function render() {
    close();
    var u = S.ctx.unit;
    var pal = CATALOG.map(function (c) {
      return '<button class="nlst-pi' + (c.a11y ? " nlst-pi--a11y" : "") + '" data-add="' + c.id + '" type="button">' +
        '<span class="nlst-pi__ic">' + c.icon + '</span><span>' + esc(t("nlst_it_" + c.id)) + '</span><i>' + c.w + "×" + c.d + " " + esc(t("nlst_cm")) + "</i></button>";
    }).join("");
    var el = document.createElement("div");
    el.id = "nlst";
    el.dir = document.documentElement.dir || "rtl";
    el.innerHTML =
      '<div class="nlst-head">' +
        '<div><b>' + esc(t("nlst_title")) + '</b><span class="nlst-sub">' + esc(t("unit_short", { label: u.label, floor: u.floor })) + " · " + esc(u.sqm) + " " + esc(t("sqm_unit")) + '</span></div>' +
        '<span class="nlst-honest">' + esc(t("nlst_honest")) + '</span>' +
        '<button class="nlst-x" data-st="close" aria-label="' + esc(t("btn_close")) + '">✕</button>' +
      "</div>" +
      '<div class="nlst-body">' +
        '<aside class="nlst-pal"><div class="nlst-pal__t">' + esc(t("nlst_palette")) + "</div>" + pal +
          '<div class="nlst-pal__t" style="margin-top:14px">' + esc(t("nlst_notes")) + "</div>" +
          '<textarea id="nlst-notes" placeholder="' + esc(t("nlst_notes_ph")) + '">' + esc(S.notes) + "</textarea>" +
          '<a class="nlst-pros" href="' + esc((S.ctx.homeUrl || "") + "/professionals/") + '">' + esc(t("nlst_pros")) + " ←</a>" +
        "</aside>" +
        '<div class="nlst-stage"><div class="nlst-plan" id="nlst-plan"></div>' +
          '<div class="nlst-tools">' +
            '<button data-st="rotate" type="button">' + esc(t("nlst_rotate")) + "</button>" +
            '<button data-st="note" type="button">' + esc(t("nlst_note")) + "</button>" +
            '<button data-st="del" type="button">' + esc(t("nlst_delete")) + "</button>" +
            '<button data-st="clear" type="button">' + esc(t("nlst_clear")) + "</button>" +
          "</div></div>" +
      "</div>" +
      '<div class="nlst-foot">' +
        '<button class="nl-btn nl-btn--gold" data-st="rfp" type="button">' + esc(t("nlst_send_rfp")) + "</button>" +
        '<a class="nl-btn nlst-wa" data-st="wa" href="#" target="_blank" rel="noopener">' + esc(t("nlst_send_wa")) + "</a>" +
        '<button class="nl-btn" data-st="video" type="button">' + esc(t("nlst_video")) + "</button>" +
        '<span class="nlst-count" id="nlst-count"></span>' +
      "</div>";
    document.body.appendChild(el);
    drawPlan();
    S.items.forEach(placeItem);
    count();
    wire(el);
  }

  function drawPlan() {
    var plan = document.getElementById("nlst-plan");
    var u = S.ctx.unit;
    var sqm = Math.max(30, parseInt(u.sqm, 10) || 85);
    var envW = Math.sqrt(sqm * 1.45), envH = sqm / envW; // meters
    var maxW = Math.min(880, plan.parentElement.clientWidth - 8);
    var pxm = Math.min(maxW / envW, 560 / envH);
    S.scale = pxm / 100; // px per cm
    plan.style.width = Math.round(envW * pxm) + "px";
    plan.style.height = Math.round(envH * pxm) + "px";
    S.plan = { w: envW * 100, h: envH * 100 };
    // rooms in two bands, widths proportional to area
    var rooms = planRooms();
    var top = rooms.slice(0, 2), bottom = rooms.slice(2);
    var html = "";
    [["t", top], ["b", bottom]].forEach(function (band) {
      var arr = band[1];
      var total = arr.reduce(function (m, r) { return m + r.a; }, 0) || 1;
      var x = 0;
      arr.forEach(function (r) {
        var w = (r.a / total) * 100;
        html += '<div class="nlst-room" style="inset-inline-start:' + x + "%;width:" + w + "%;" + (band[0] === "t" ? "top:0;height:52%" : "bottom:0;height:48%") + '">' +
          '<span>' + esc(label(r)) + " · " + (Math.round(r.a * 10) / 10) + " " + esc(t("sqm_unit")) + "</span></div>";
        x += w;
      });
    });
    html += '<span class="nlst-scale">' + esc(t("nlst_scale", { m: Math.round(envW * 10) / 10 + "×" + Math.round(envH * 10) / 10 })) + "</span>";
    plan.innerHTML = html;
  }

  function cat(idOf) { return CATALOG.filter(function (c) { return c.id === idOf; })[0]; }

  function placeItem(it) {
    var plan = document.getElementById("nlst-plan"), c = cat(it.type);
    if (!plan || !c) return;
    var el = document.createElement("div");
    el.className = "nlst-it" + (c.round ? " nlst-it--round" : "") + (c.a11y ? " nlst-it--a11y" : "");
    el.dataset.uid = it.uid;
    var w = (it.rot % 180 === 0 ? c.w : c.d), h = (it.rot % 180 === 0 ? c.d : c.w);
    el.style.width = Math.round(w * S.scale) + "px";
    el.style.height = Math.round(h * S.scale) + "px";
    el.style.left = Math.round(it.x * S.scale) + "px";
    el.style.top = Math.round(it.y * S.scale) + "px";
    el.innerHTML = "<b>" + esc(t("nlst_it_" + it.type)) + "</b>" + (it.note ? '<i class="nlst-it__note" title="' + esc(it.note) + '">✎</i>' : "");
    plan.appendChild(el);
  }
  function redraw() {
    drawPlan();
    S.items.forEach(placeItem);
    select(S.sel);
    count();
    save();
  }
  function count() {
    var el = document.getElementById("nlst-count");
    if (el) el.textContent = t("nlst_count", { n: S.items.length });
  }
  function select(uid) {
    S.sel = uid || null;
    document.querySelectorAll(".nlst-it").forEach(function (n) { n.classList.toggle("is-sel", n.dataset.uid === S.sel); });
  }
  function item(uid) { return S.items.filter(function (i) { return i.uid === uid; })[0]; }

  function addItem(type) {
    var c = cat(type); if (!c) return;
    var it = { uid: "i" + Math.random().toString(36).slice(2, 8), type: type, x: Math.max(4, S.plan.w / 2 - c.w / 2), y: Math.max(4, S.plan.h / 2 - c.d / 2), rot: 0, note: "" };
    S.items.push(it);
    placeItem(it);
    select(it.uid);
    count(); save();
  }

  function summaryText() {
    var u = S.ctx.unit, lines = [];
    lines.push(t("nlst_sum_head", { label: u.label, floor: u.floor, project: S.ctx.projectName }));
    S.items.forEach(function (it) {
      var c = cat(it.type);
      lines.push("- " + t("nlst_it_" + it.type) + " (" + c.w + "×" + c.d + " " + t("nlst_cm") + ")" + (it.note ? ": " + it.note : ""));
    });
    if (S.notes) lines.push(t("nlst_notes") + ": " + S.notes);
    lines.push(location.origin + location.pathname + "?project=" + encodeURIComponent(S.ctx.projectKey) + "&unit=" + encodeURIComponent(u.id));
    return lines.join("\n");
  }

  function wire(root) {
    root.addEventListener("click", function (e) {
      var add = e.target.closest("[data-add]");
      if (add) { addItem(add.dataset.add); return; }
      var st = e.target.closest("[data-st]");
      if (st) {
        var a = st.dataset.st;
        if (a === "close") { S.notes = (document.getElementById("nlst-notes") || {}).value || S.notes; save(); close(); }
        else if (a === "rotate" && S.sel) { var it = item(S.sel); it.rot = (it.rot + 90) % 360; redraw(); }
        else if (a === "del" && S.sel) { S.items = S.items.filter(function (i) { return i.uid !== S.sel; }); S.sel = null; redraw(); }
        else if (a === "clear") { S.items = []; S.sel = null; redraw(); }
        else if (a === "note" && S.sel) {
          var it2 = item(S.sel);
          var v = window.prompt(t("nlst_note_ph"), it2.note || "");
          if (v !== null) { it2.note = String(v).slice(0, 200); redraw(); }
        }
        else if (a === "rfp") { finishNotes(); save(); close(); var b = document.querySelector('[data-act="rfp"][data-id="' + S.ctx.unit.id.replace(/["\\]/g, "\\$&") + '"]'); if (b) b.click(); }
        else if (a === "video") {
          finishNotes(); save();
          try {
            fetch(S.ctx.leadEndpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ source: "apartment-studio", context: "studio-video-call", name: "", phone: "", message: summaryText(), url: location.href }) });
          } catch (err) {}
          if (S.ctx.whatsapp) { window.open("https://wa.me/" + S.ctx.whatsapp + "?text=" + encodeURIComponent(t("nlst_video_msg") + "\n" + summaryText()), "_blank"); }
        }
        return;
      }
      var itEl = e.target.closest(".nlst-it");
      if (itEl) { select(itEl.dataset.uid); return; }
      if (e.target.closest("#nlst-plan")) select(null);
    });
    // WhatsApp share link stays fresh
    var wa = root.querySelector('[data-st="wa"]');
    if (wa) {
      wa.addEventListener("mousedown", function () { finishNotes(); wa.href = "https://wa.me/?text=" + encodeURIComponent(summaryText()); });
      wa.addEventListener("touchstart", function () { finishNotes(); wa.href = "https://wa.me/?text=" + encodeURIComponent(summaryText()); }, { passive: true });
    }
    var notesEl = root.querySelector("#nlst-notes");
    if (notesEl) notesEl.addEventListener("change", function () { S.notes = notesEl.value; save(); });
    // dragging (pointer events; keeps items inside the plan)
    var plan = root.querySelector("#nlst-plan");
    plan.addEventListener("pointerdown", function (e) {
      var el = e.target.closest(".nlst-it"); if (!el) return;
      select(el.dataset.uid);
      var it = item(el.dataset.uid); if (!it) return;
      var r = plan.getBoundingClientRect();
      S.drag = { it: it, el: el, dx: e.clientX - r.left - it.x * S.scale * (el.dir === "rtl" ? 1 : 1), dy: e.clientY - r.top - it.y * S.scale };
      // recompute dx precisely from the element box (dir-proof)
      var er = el.getBoundingClientRect();
      S.drag.dx = e.clientX - er.left; S.drag.dy = e.clientY - er.top;
      el.setPointerCapture && el.setPointerCapture(e.pointerId);
      e.preventDefault();
    });
    plan.addEventListener("pointermove", function (e) {
      if (!S.drag) return;
      var r = plan.getBoundingClientRect();
      var c = cat(S.drag.it.type);
      var w = (S.drag.it.rot % 180 === 0 ? c.w : c.d), h = (S.drag.it.rot % 180 === 0 ? c.d : c.w);
      var x = (e.clientX - r.left - S.drag.dx) / S.scale, y = (e.clientY - r.top - S.drag.dy) / S.scale;
      x = Math.max(0, Math.min(S.plan.w - w, x)); y = Math.max(0, Math.min(S.plan.h - h, y));
      S.drag.it.x = x; S.drag.it.y = y;
      S.drag.el.style.left = Math.round(x * S.scale) + "px";
      S.drag.el.style.top = Math.round(y * S.scale) + "px";
    });
    ["pointerup", "pointercancel"].forEach(function (ev) {
      plan.addEventListener(ev, function () { if (S.drag) { S.drag = null; save(); } });
    });
    window.addEventListener("resize", function () { if (document.getElementById("nlst")) redraw(); });
  }
  function finishNotes() { var n = document.getElementById("nlst-notes"); if (n) S.notes = n.value; }

  /* what buyflow reads to attach the design to the RFP */
  function exportFor(projectKey, unitId) {
    try {
      var raw = localStorage.getItem("nlstudio:" + projectKey + ":" + unitId);
      if (!raw) return null;
      var st = JSON.parse(raw);
      if (!st || (!st.items.length && !st.notes)) return null;
      return st;
    } catch (e) { return null; }
  }

  window.NLStudio = { open: open, exportFor: exportFor };
})();
