/**
 * WordPress-compatible, framework-free reference renderer.
 * Uses the same Pannellum version already lazy-loaded by the live showroom engine.
 * Semantic model/floor clicks must dispatch nadlan:facility-selected with a real facility_id.
 */
(function (window, document) {
  'use strict';
  const PANNELLUM_JS = 'https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js';
  const PANNELLUM_CSS = 'https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css';
  let loader;

  function loadPannellum() {
    if (window.pannellum) return Promise.resolve(window.pannellum);
    if (loader) return loader;
    loader = new Promise((resolve, reject) => {
      if (!document.querySelector(`link[href="${PANNELLUM_CSS}"]`)) {
        const link = document.createElement('link'); link.rel = 'stylesheet'; link.href = PANNELLUM_CSS; document.head.appendChild(link);
      }
      const script = document.createElement('script'); script.src = PANNELLUM_JS; script.async = true;
      script.onload = () => resolve(window.pannellum); script.onerror = reject; document.head.appendChild(script);
    });
    return loader;
  }

  function mount(root, options) {
    if (!root || !Array.isArray(options?.facilities)) throw new TypeError('mount(root, { facilities }) is required');
    const facilities = options.facilities;
    root.innerHTML = `
      <section class="nlfac" aria-labelledby="nlfac-title">
        <header class="nlfac__head"><p class="nlfac__eyebrow">החיים בבניין</p><h2 id="nlfac-title">מתקנים שנועדו לשימוש אמיתי</h2></header>
        <div class="nlfac__layout">
          <nav class="nlfac__list" aria-label="בחירת מתקן"></nav>
          <article class="nlfac__detail" aria-live="polite"><div class="nlfac__pano" id="nlfac-pano"></div><div class="nlfac__copy"></div></article>
        </div>
      </section>`;
    const list = root.querySelector('.nlfac__list');
    const copy = root.querySelector('.nlfac__copy');
    let viewer = null;

    for (const facility of facilities) {
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'nlfac__item'; button.dataset.facilityId = facility.id;
      button.innerHTML = `<strong>${facility.nameHe}</strong><span>${facility.level} · כ-${facility.areaSqm} מ״ר · עד ${facility.capacity} אורחים</span>`;
      button.addEventListener('click', () => select(facility.id, 'list'));
      list.appendChild(button);
    }

    async function select(facilityId, source) {
      const facility = facilities.find(item => item.id === facilityId);
      if (!facility) return;
      root.querySelectorAll('.nlfac__item').forEach(button => button.setAttribute('aria-current', String(button.dataset.facilityId === facilityId)));
      copy.innerHTML = `<h3>${facility.nameHe}</h3><p>${facility.summaryHe}</p><dl><div><dt>מפלס</dt><dd>${facility.level}</dd></div><div><dt>שטח</dt><dd>כ-${facility.areaSqm} מ״ר</dd></div><div><dt>קיבולת</dt><dd>עד ${facility.capacity}</dd></div></dl><h4>מה נמצא כאן</h4><ul>${facility.equipment.map(item => `<li>${item}</li>`).join('')}</ul><div class="nlfac__actions"><button type="button" data-facility-action="map">הצגה במפת המתחם</button><button type="button" data-facility-action="contact">שיחה עם נציג</button></div>`;
      if (viewer?.destroy) viewer.destroy();
      const pannellum = await loadPannellum();
      viewer = pannellum.viewer('nlfac-pano', { type: 'equirectangular', panorama: facility.asset, autoLoad: true, showControls: true, keyboardZoom: true, compass: false });
      window.NLUnitJourney?.selectFacility(facilityId, `facility-${source}`);
      window.dispatchEvent(new CustomEvent('nadlan:facility-opened', { detail: { facilityId, source } }));
    }

    window.addEventListener('nadlan:facility-selected', event => select(event.detail?.facilityId, event.detail?.source || 'semantic-anchor'));
    root.addEventListener('click', event => {
      const action = event.target.closest('[data-facility-action]')?.dataset.facilityAction;
      const facilityId = window.NLUnitJourney?.getState().facilityId;
      if (!action || !facilityId) return;
      window.dispatchEvent(new CustomEvent(`nadlan:facility-${action}`, { detail: { facilityId } }));
    });
    if (facilities[0]) select(facilities[0].id, 'initial');
    return { select, destroy: () => viewer?.destroy?.() };
  }

  window.NLFacilitiesExperience = Object.freeze({ mount });
})(window, document);
