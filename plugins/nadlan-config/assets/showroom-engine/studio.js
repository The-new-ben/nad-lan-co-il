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
    { id: "tvunit", w: 180, d: 45, icon: "📺" },
    { id: "armchair", w: 85, d: 85, icon: "🪑" },
    { id: "dresser", w: 120, d: 50, icon: "🗄" },
    { id: "rug", w: 200, d: 140, soft: true, icon: "▭" },
    { id: "plant", w: 45, d: 45, round: true, icon: "🌿" },
    { id: "bench", w: 140, d: 40, icon: "🪵" },
    /* accessibility templates (SI 1918 planning language) */
    { id: "wheel", w: 150, d: 150, round: true, a11y: true, icon: "♿" },
    { id: "door80", w: 80, d: 12, a11y: true, icon: "🚪" }
  ];

  var S = { ctx: null, items: [], notes: "", scale: 1, sel: null, drag: null, plan: null, undo: [] };

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
            '<button data-st="auto" type="button" class="nlst-auto" title="' + esc(t("nlst_auto_note")) + '">' + esc(t("nlst_auto")) + "</button>" +
            '<button data-st="undo" type="button">' + esc(t("nlst_undo")) + "</button>" +
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

  /* top-view schematic symbols (ink lines, architect-plan language) */
  var SYM = {
    sofa2: '<rect x="4" y="16" width="92" height="80" rx="10"/><rect x="4" y="4" width="92" height="18" rx="7"/><line x1="50" y1="22" x2="50" y2="94"/>',
    sofa3: '<rect x="4" y="16" width="92" height="80" rx="10"/><rect x="4" y="4" width="92" height="18" rx="7"/><line x1="36" y1="22" x2="36" y2="94"/><line x1="66" y1="22" x2="66" y2="94"/>',
    bed_double: '<rect x="4" y="4" width="92" height="92" rx="5"/><rect x="10" y="8" width="36" height="20" rx="5"/><rect x="54" y="8" width="36" height="20" rx="5"/><line x1="4" y1="38" x2="96" y2="38"/>',
    bed_single: '<rect x="4" y="4" width="92" height="92" rx="5"/><rect x="22" y="8" width="56" height="20" rx="5"/><line x1="4" y1="38" x2="96" y2="38"/>',
    table4: '<rect x="14" y="18" width="72" height="64" rx="6"/><circle cx="8" cy="50" r="7"/><circle cx="92" cy="50" r="7"/><circle cx="50" cy="10" r="7"/><circle cx="50" cy="90" r="7"/>',
    table6: '<rect x="14" y="18" width="72" height="64" rx="6"/><circle cx="8" cy="34" r="6"/><circle cx="8" cy="66" r="6"/><circle cx="92" cy="34" r="6"/><circle cx="92" cy="66" r="6"/><circle cx="36" cy="10" r="6"/><circle cx="64" cy="90" r="6"/>',
    wardrobe: '<rect x="4" y="10" width="92" height="80"/><line x1="50" y1="10" x2="50" y2="90"/><line x1="10" y1="24" x2="44" y2="24"/><line x1="56" y1="24" x2="90" y2="24"/>',
    fridge: '<rect x="8" y="8" width="84" height="84" rx="8"/><line x1="8" y1="42" x2="92" y2="42"/><circle cx="78" cy="26" r="4"/>',
    washer: '<rect x="8" y="8" width="84" height="84" rx="8"/><circle cx="50" cy="52" r="26"/><circle cx="50" cy="52" r="12"/>',
    desk: '<rect x="4" y="8" width="92" height="52" rx="4"/><circle cx="50" cy="82" r="13"/>',
    crib: '<rect x="6" y="6" width="88" height="88" rx="8"/><line x1="24" y1="6" x2="24" y2="94"/><line x1="42" y1="6" x2="42" y2="94"/><line x1="60" y1="6" x2="60" y2="94"/><line x1="78" y1="6" x2="78" y2="94"/>',
    bath: '<rect x="4" y="8" width="92" height="84" rx="22"/><circle cx="26" cy="50" r="5"/>',
    tvunit: '<rect x="4" y="30" width="92" height="42" rx="4"/><line x1="14" y1="24" x2="86" y2="24"/>',
    armchair: '<rect x="10" y="18" width="80" height="72" rx="12"/><rect x="10" y="6" width="80" height="16" rx="7"/>',
    dresser: '<rect x="4" y="12" width="92" height="76" rx="4"/><line x1="4" y1="50" x2="96" y2="50"/><circle cx="50" cy="32" r="3"/><circle cx="50" cy="68" r="3"/>',
    rug: '<rect x="4" y="4" width="92" height="92" rx="6" stroke-dasharray="7 5"/><rect x="18" y="18" width="64" height="64" rx="4" stroke-dasharray="4 4"/>',
    plant: '<circle cx="50" cy="50" r="42"/><path d="M50 78 C40 56 40 40 50 22 C60 40 60 56 50 78Z"/>',
    bench: '<rect x="4" y="22" width="92" height="56" rx="6"/><line x1="30" y1="22" x2="30" y2="78"/><line x1="70" y1="22" x2="70" y2="78"/>',
    wheel: '<circle cx="50" cy="50" r="44"/><line x1="50" y1="6" x2="50" y2="94"/><line x1="6" y1="50" x2="94" y2="50"/>',
    door80: '<line x1="4" y1="90" x2="96" y2="90"/><path d="M4 90 A 92 92 0 0 1 96 6" stroke-dasharray="6 5"/>'
  };
  function sym(type) {
    if (!SYM[type]) return "";
    return '<svg viewBox="0 0 100 100" preserveAspectRatio="none" fill="none" stroke="currentColor" stroke-width="3" vector-effect="non-scaling-stroke" aria-hidden="true">' + SYM[type] + "</svg>";
  }

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
    el.innerHTML = sym(it.type) + "<b>" + esc(t("nlst_it_" + it.type)) + "</b>" + (it.note ? '<i class="nlst-it__note" title="' + esc(it.note) + '">✎</i>' : "");
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
  function snapshot() { S.undo.push(JSON.stringify(S.items)); if (S.undo.length > 30) S.undo.shift(); }
  function undo() { if (!S.undo.length) return; S.items = JSON.parse(S.undo.pop()); S.sel = null; redraw(); }

  function addItem(type) {
    var c = cat(type); if (!c) return;
    snapshot();
    // cascade spawn so consecutive items never stack on one spot
    var off = (S.items.length % 6) * 30;
    var it = { uid: "i" + Math.random().toString(36).slice(2, 8), type: type,
      x: Math.max(4, Math.min(S.plan.w - c.w - 4, S.plan.w / 2 - c.w / 2 + off)),
      y: Math.max(4, Math.min(S.plan.h - c.d - 4, S.plan.h / 2 - c.d / 2 + off)), rot: 0, note: "" };
    S.items.push(it);
    placeItem(it);
    select(it.uid);
    count(); save();
  }

  /* AUTO-ARRANGE (2026 room-planner table stakes): a deterministic starting
     layout from the unit's real rooms - anchor piece on the top wall, its
     counterpart opposite, extras along the side. Honest: skips anything that
     does not fit; always labeled a starting point, never a design. */
  function roomRects() {
    var rooms = planRooms(), top = rooms.slice(0, 2), bottom = rooms.slice(2), rects = [];
    [[top, 0, 0.52], [bottom, 0.52, 0.48]].forEach(function (band) {
      var arr = band[0], total = arr.reduce(function (m, r) { return m + r.a; }, 0) || 1, x = 0;
      arr.forEach(function (r) {
        var w = (r.a / total) * S.plan.w;
        rects.push({ k: r.k, x: x, y: band[1] * S.plan.h, w: w, h: band[2] * S.plan.h });
        x += w;
      });
    });
    return rects;
  }
  var AUTO = { salon: ["sofa3", "tvunit", "rug", "plant"], kitchen: ["fridge"], master: ["bed_double", "wardrobe"], bed: ["bed_single", "desk"], bathwc: ["bath"] };
  function autoArrange() {
    snapshot();
    S.items = [];
    roomRects().forEach(function (r) {
      (AUTO[r.k] || []).forEach(function (type, idx) {
        var c = cat(type); if (!c) return;
        var rot = (c.w > r.w - 16 && c.w <= r.h - 16) ? 90 : 0;
        var w = rot ? c.d : c.w, h = rot ? c.w : c.d;
        if (w > r.w - 12 || h > r.h - 12) return;
        var x, y;
        if (idx === 0) { x = r.x + (r.w - w) / 2; y = r.y + 6; }
        else if (idx === 1) { x = r.x + (r.w - w) / 2; y = r.y + r.h - h - 6; }
        else { x = r.x + 8 + (idx - 2) * (w + 12); y = r.y + (r.h - h) / 2; }
        x = Math.max(r.x + 4, Math.min(r.x + r.w - w - 4, x));
        y = Math.max(r.y + 4, Math.min(r.y + r.h - h - 4, y));
        // skip on overlap with an already placed piece (honest, no stacking)
        var hit = S.items.some(function (o) {
          var oc = cat(o.type), ow = (o.rot % 180 === 0 ? oc.w : oc.d), oh = (o.rot % 180 === 0 ? oc.d : oc.w);
          return x < o.x + ow && o.x < x + w && y < o.y + oh && o.y < y + h;
        });
        if (hit && type !== "rug") return;
        S.items.push({ uid: "i" + Math.random().toString(36).slice(2, 8), type: type, x: x, y: y, rot: rot, note: "" });
      });
    });
    S.sel = null;
    redraw();
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
        else if (a === "rotate" && S.sel) { snapshot(); var it = item(S.sel); it.rot = (it.rot + 90) % 360; redraw(); }
        else if (a === "del" && S.sel) { snapshot(); S.items = S.items.filter(function (i) { return i.uid !== S.sel; }); S.sel = null; redraw(); }
        else if (a === "clear") { snapshot(); S.items = []; S.sel = null; redraw(); }
        else if (a === "undo") { undo(); }
        else if (a === "auto") { autoArrange(); }
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
      snapshot();
      var badge = document.createElement("span"); badge.className = "nlst-dist"; el.appendChild(badge); S.drag.badge = badge;
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
      // wall magnetism (Sweet Home 3D pattern): snap flush within 15cm
      if (x < 15) x = 0; if (S.plan.w - w - x < 15) x = S.plan.w - w;
      if (y < 15) y = 0; if (S.plan.h - h - y < 15) y = S.plan.h - h;
      S.drag.it.x = x; S.drag.it.y = y;
      if (S.drag.badge) {
        var dh = Math.round(Math.min(x, S.plan.w - w - x)), dv = Math.round(Math.min(y, S.plan.h - h - y));
        S.drag.badge.textContent = dh + " / " + dv + " " + t("nlst_cm");
      }
      S.drag.el.style.left = Math.round(x * S.scale) + "px";
      S.drag.el.style.top = Math.round(y * S.scale) + "px";
    });
    ["pointerup", "pointercancel"].forEach(function (ev) {
      plan.addEventListener(ev, function () { if (S.drag) { if (S.drag.badge) S.drag.badge.remove(); S.drag = null; save(); } });
    });
    root.addEventListener("keydown", function (e) { if ((e.ctrlKey || e.metaKey) && e.key === "z") { e.preventDefault(); undo(); } });
    root.tabIndex = -1; root.focus();
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
