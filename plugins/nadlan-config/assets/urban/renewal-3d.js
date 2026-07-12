/* ============================================================================
   NADLAN URBAN RENEWAL - wizard driver + instant 3D (L3, 2026-07-11).
   Standalone on purpose: engine.js is a full project-page app; this is a
   ~150-line wizard. The floor-badge placement ports the engine's unitPos
   fallback convention (26.4m building at origin, floor_h 3.05, y = f*fh +
   fh*0.4) so the standard-residential model lines up with zero authoring.
============================================================================ */
(function () {
  "use strict";
  var root = document.getElementById("nlurw");
  if (!root || root.dataset.nlurWired) return;
  root.dataset.nlurWired = "1";

  var state = { compound: "", booted3d: false };
  var LANG = root.dataset.lang || "he";
  var I = {};
  try { I = JSON.parse(root.dataset.i18n || "{}"); } catch (e) { I = {}; }
  function t(k, fb) { return I[k] || fb; }
  function el(id) { return document.getElementById(id); }
  function step(n) {
    root.querySelectorAll(".nlurw-step").forEach(function (s) { s.hidden = s.dataset.step !== String(n); });
    root.querySelectorAll(".nlurw-steps li").forEach(function (li, i) { li.classList.toggle("is-on", i === n - 1); });
    if (n === 4) advise();
    if (n === 5) boot3d();
  }
  root.addEventListener("click", function (e) {
    var b = e.target.closest(".nlurw-next"); if (!b) return;
    step(parseInt(b.dataset.go, 10));
  });

  /* step 1 -> declared-compound lookup */
  root.querySelector('[data-go="2"]').addEventListener("click", function () {
    var city = (el("nlurw-city").value || "").trim(), q = (el("nlurw-street").value || "").trim();
    var out = el("nlurw-lookupres");
    if (!city) { out.textContent = ""; return; }
    out.textContent = t("checking", "בודקים מול מאגר המתחמים...");
    fetch(root.dataset.lookup + "?city=" + encodeURIComponent(city) + "&q=" + encodeURIComponent(q))
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d && d.matches && d.matches.length) {
          var m = d.matches[0];
          state.compound = m.title + (m.plan_number ? ", תכנית " + m.plan_number : "") + (m.project_status ? ", סטטוס: " + m.project_status : "") + (m.project_type ? ", מסלול: " + m.project_type : "");
          out.textContent = t("found", "נמצא מתחם מוכרז קרוב: ") + m.title + t("found2", ". הנתונים יצורפו לניתוח.");
        } else {
          state.compound = "";
          out.textContent = t("notfound", "לא נמצא מתחם מוכרז תואם. זה לא אומר שאין פוטנציאל - מסלול בניין בודד לא מופיע במאגר.");
        }
      }).catch(function () { out.textContent = ""; });
  });

  /* step 3 - private upload */
  var file = el("nlurw-file");
  if (file) file.addEventListener("change", function () {
    if (!file.files || !file.files[0]) return;
    var msg = el("nlurw-filemsg");
    msg.textContent = t("uploading", "מעלים...");
    var fd = new FormData();
    fd.append("doc", file.files[0]);
    fetch(root.dataset.doc, { method: "POST", headers: { "X-WP-Nonce": root.dataset.nonce }, body: fd })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (x) {
        msg.textContent = x.ok ? t("uploaded", "הקובץ נשמר לתיק הבניין (קישור חסוי). זכרו: הניתוח קורא את הטקסט שתדביקו למטה.") : ((x.j && x.j.message) || t("upfail", "ההעלאה נכשלה"));
      }).catch(function () { msg.textContent = t("upfail", "ההעלאה נכשלה"); });
  });

  /* step 4 - advisory */
  var TRACKS = I.tracks || { pinui_binui: "פינוי בינוי", tama38_1: "חיזוק (תמא 38/1)", tama38_2: "הריסה ובנייה לבניין בודד", unclear: "דרוש בירור נוסף" };
  var PROS = I.prosmap || { lawyer: "עורך דין דיירים", shamai: "שמאי מקרקעין", mefakeach: "מפקח בנייה", organizer: "מארגן/מנהלת" };
  function advise() {
    var box = el("nlurw-adv");
    box.textContent = t("analyzing", "מנתחים את הנתונים...");
    fetch(root.dataset.advise, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-WP-Nonce": root.dataset.nonce },
      body: JSON.stringify({
        city: el("nlurw-city").value, floors: el("nlurw-floors").value, units: el("nlurw-units").value,
        year: el("nlurw-year").value, consents: el("nlurw-consents").value,
        lang: LANG, compound_facts: state.compound, text: el("nlurw-text").value
      })
    }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (x) {
        if (!x.ok) { box.textContent = (x.j && x.j.message) || t("unavailable", "הניתוח אינו זמין כרגע. הכלים והמדריך בעמוד ההתחדשות פתוחים תמיד."); return; }
        var a = x.j, h = "";
        h += "<h4>" + t("track", "המסלול המסתמן: ") + (TRACKS[a.track_fit] || TRACKS.unclear) + "</h4>";
        if (a.track_reason) h += "<p>" + esc(a.track_reason) + "</p>";
        if (a.consent_needed) h += "<p><b>" + t("consents", "הסכמות") + ":</b> " + esc(a.consent_needed) + "</p>";
        if (a.next_steps && a.next_steps.length) {
          h += "<p><b>" + t("steps", "הצעדים הבאים") + ":</b></p><ol>";
          a.next_steps.forEach(function (s) { h += "<li>" + esc(s) + "</li>"; });
          h += "</ol>";
        }
        if (a.professionals && a.professionals.length) {
          h += "<p><b>" + t("pros", "אנשי מקצוע רלוונטיים") + ":</b> " + a.professionals.map(function (p) { return PROS[p] || p; }).join(", ") + "</p>";
        }
        h += '<p class="d">' + esc(a.disclaimer || "") + "</p>";
        box.innerHTML = h;
      }).catch(function () { box.textContent = t("failed", "הניתוח נכשל, נסו שוב."); });
  }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* step 5 - instant 3D: standard model + a badge hotspot per floor */
  var FH = 3.05, HALF = 13.2;
  function boot3d() {
    if (state.booted3d) return;
    state.booted3d = true;
    var host = el("nlurw-3d"), glb = root.dataset.glb;
    if (!host || !glb) return;
    var build = function () {
      var floors = Math.max(1, Math.min(40, parseInt(el("nlurw-floors").value, 10) || 4));
      var mv = document.createElement("model-viewer");
      mv.setAttribute("src", glb);
      mv.setAttribute("camera-controls", ""); mv.setAttribute("auto-rotate", "");
      mv.setAttribute("rotation-per-second", "12deg"); mv.setAttribute("interaction-prompt", "none");
      mv.setAttribute("environment-image", "neutral"); mv.setAttribute("exposure", "0.95");
      mv.setAttribute("shadow-intensity", "0.5"); mv.setAttribute("touch-action", "pan-y");
      // frame the BUILDING, not the 96m site plate (mobile was a sliver)
      mv.setAttribute("camera-target", "0 " + Math.min(20, floors * FH * 0.45).toFixed(1) + " 0");
      mv.setAttribute("camera-orbit", "-28deg 76deg " + Math.max(40, floors * FH * 1.6).toFixed(0) + "m");
      mv.setAttribute("min-camera-orbit", "auto 48deg 26m");
      mv.setAttribute("max-camera-orbit", "auto 86deg 90m");
      mv.style.cssText = "width:100%;height:100%;direction:ltr;background:transparent";
      for (var f = 1; f <= floors; f++) {
        var b = document.createElement("button");
        b.setAttribute("slot", "hotspot-f" + f);
        // west facade, engine unitPos convention
        b.setAttribute("data-position", (-HALF).toFixed(2) + "m " + (f * FH + FH * 0.4).toFixed(2) + "m 0m");
        b.setAttribute("data-normal", "-1 0 0");
        b.setAttribute("data-visibility-attribute", "visible");
        b.className = "nlurw-hot";
        b.textContent = f;
        mv.appendChild(b);
      }
      var st = document.createElement("style");
      st.textContent = ".nlurw-hot{width:30px;height:30px;border-radius:50%;border:2px solid #C99C49;background:rgba(20,19,15,.7);color:#F5EFE2;font:700 12px Heebo;cursor:default}.nlurw-hot:not([data-visible]){opacity:0}";
      document.head.appendChild(st);
      host.innerHTML = "";
      host.appendChild(mv);
    };
    if (window.customElements && customElements.get("model-viewer")) { build(); return; }
    var s = document.createElement("script");
    s.type = "module";
    s.src = "https://unpkg.com/@google/model-viewer@3.5.0/dist/model-viewer.min.js";
    s.onload = build;
    document.head.appendChild(s);
  }
})();
