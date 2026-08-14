/*
 * NADLAN SELECTED-UNIT ACCEPTANCE HELPERS
 * PROPOSAL ONLY / NOT APPLIED
 *
 * Paste the complete file into DevTools Console on the SANDBOX page only.
 * It defines window.NLUnitAudit and does not click buttons, submit forms,
 * alter classes, rewrite attributes, or change application state.
 *
 * Console checks complement — never replace — physical iOS/Android testing.
 */

(function () {
  "use strict";

  function visible(el) {
    if (!el || el.hidden) return false;
    var style = getComputedStyle(el);
    var rect = el.getBoundingClientRect();
    return (
      style.display !== "none" &&
      style.visibility !== "hidden" &&
      rect.width > 0 &&
      rect.height > 0
    );
  }

  function label(el) {
    if (!el) return "";
    var id = el.id ? "#" + el.id : "";
    var classes = Array.from(el.classList || []).slice(0, 4);
    return el.tagName.toLowerCase() + id +
      (classes.length ? "." + classes.join(".") : "");
  }

  function rectOf(el) {
    if (!el) return null;
    var rect = el.getBoundingClientRect();
    return {
      x: Math.round(rect.x * 10) / 10,
      y: Math.round(rect.y * 10) / 10,
      width: Math.round(rect.width * 10) / 10,
      height: Math.round(rect.height * 10) / 10,
      right: Math.round(rect.right * 10) / 10,
      bottom: Math.round(rect.bottom * 10) / 10
    };
  }

  function viewport() {
    var vv = window.visualViewport;
    return {
      width: vv ? vv.width : window.innerWidth,
      height: vv ? vv.height : window.innerHeight,
      offsetLeft: vv ? vv.offsetLeft : 0,
      offsetTop: vv ? vv.offsetTop : 0,
      scale: vv ? vv.scale : 1,
      innerWidth: window.innerWidth,
      innerHeight: window.innerHeight,
      devicePixelRatio: window.devicePixelRatio
    };
  }

  function selectedScope() {
    var dialog = document.getElementById("nl-unit-tool");
    if (dialog && dialog.open) return dialog;

    var screen = document.getElementById("nl-unit-screen");
    if (visible(screen)) return screen;

    var panel = document.getElementById("nl-panel");
    if (panel && panel.classList.contains("nl-panel--unit-summary")) {
      return panel;
    }

    return document.getElementById("nl-root");
  }

  function nestedScrollers(scope) {
    scope = scope || selectedScope();
    if (!scope) return [];

    return Array.from(scope.querySelectorAll("*")).filter(visible).map(function (el) {
      var css = getComputedStyle(el);
      var scrollY = /(auto|scroll)/.test(css.overflowY);
      var scrollX = /(auto|scroll)/.test(css.overflowX);
      var leaksY = scrollY && el.scrollHeight > el.clientHeight + 1;
      var leaksX = scrollX && el.scrollWidth > el.clientWidth + 1;

      if (!leaksY && !leaksX) return null;

      return {
        element: label(el),
        overflowX: css.overflowX,
        overflowY: css.overflowY,
        clientWidth: el.clientWidth,
        scrollWidth: el.scrollWidth,
        clientHeight: el.clientHeight,
        scrollHeight: el.scrollHeight,
        excessX: el.scrollWidth - el.clientWidth,
        excessY: el.scrollHeight - el.clientHeight
      };
    }).filter(Boolean);
  }

  function viewportFit() {
    var vp = viewport();
    var theater = document.querySelector(".nl-theater--unit-selected");
    var screen = document.getElementById("nl-unit-screen");
    var dialog = document.getElementById("nl-unit-tool");
    var target = dialog && dialog.open ? dialog : theater;
    var rect = rectOf(target);

    return {
      state: dialog && dialog.open ? "tool" : theater ? "selected-unit" : "building",
      target: label(target),
      targetRect: rect,
      selectedScreenRect: rectOf(screen),
      viewport: vp,
      widthDelta: rect ? Math.round((rect.width - vp.width) * 10) / 10 : null,
      heightDelta: rect ? Math.round((rect.height - vp.height) * 10) / 10 : null,
      fullyVisible: rect ? (
        rect.x >= vp.offsetLeft - 1 &&
        rect.y >= vp.offsetTop - 1 &&
        rect.right <= vp.offsetLeft + vp.width + 1 &&
        rect.bottom <= vp.offsetTop + vp.height + 1
      ) : false
    };
  }

  function fixedContainingBlocks() {
    var dialog = document.getElementById("nl-unit-tool");
    if (!dialog) return { dialogExists: false, pass: false, ancestors: [] };

    var ancestors = [];
    var el = dialog.parentElement;

    while (el && el !== document.documentElement) {
      var css = getComputedStyle(el);
      if (
        css.transform !== "none" ||
        css.perspective !== "none" ||
        css.filter !== "none" ||
        css.contain !== "none"
      ) {
        ancestors.push({
          element: label(el),
          transform: css.transform,
          perspective: css.perspective,
          filter: css.filter,
          contain: css.contain
        });
      }
      el = el.parentElement;
    }

    return {
      dialogExists: true,
      parentIsBody: dialog.parentElement === document.body,
      nativeOpen: dialog.open,
      ancestors: ancestors,
      pass: dialog.parentElement === document.body && ancestors.length === 0
    };
  }

  function clippedContent() {
    var scope = selectedScope();
    if (!scope) return [];

    return Array.from(scope.querySelectorAll(
      ".nl-unit-summary__head, .nl-unit-beam, .nl-unit-facts, " +
      ".nl-unit-doors, .nl-unit-quick, .nl-unit-offer, .nl-unit-tool__body"
    )).filter(visible).map(function (el) {
      var rect = el.getBoundingClientRect();
      var parent = el.parentElement && el.parentElement.getBoundingClientRect();
      var clipped = parent && (
        rect.top < parent.top - 1 ||
        rect.left < parent.left - 1 ||
        rect.right > parent.right + 1 ||
        rect.bottom > parent.bottom + 1
      );

      return {
        element: label(el),
        rect: rectOf(el),
        parentRect: parent ? rectOf(el.parentElement) : null,
        clippedByImmediateParent: !!clipped
      };
    }).filter(function (item) {
      return item.clippedByImmediateParent;
    });
  }

  function smallTargets() {
    var scope = selectedScope();
    if (!scope) return [];

    return Array.from(scope.querySelectorAll(
      'button, a[href], input:not([type="hidden"]), [role="button"], [tabindex="0"]'
    )).filter(visible).map(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.width >= 44 && rect.height >= 44) return null;

      return {
        element: label(el),
        text: (el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 80),
        width: Math.round(rect.width * 10) / 10,
        height: Math.round(rect.height * 10) / 10
      };
    }).filter(Boolean);
  }

  function focusState() {
    var dialog = document.getElementById("nl-unit-tool");
    var screen = document.getElementById("nl-unit-screen");
    var active = document.activeElement;
    var expectedScope = dialog && dialog.open ? dialog : visible(screen) ? screen : null;

    return {
      activeElement: label(active),
      activeText: active ? (active.textContent || "").trim().slice(0, 100) : "",
      expectedScope: label(expectedScope),
      activeInsideExpectedScope: !!(
        expectedScope && active && expectedScope.contains(active)
      ),
      rootInertWhileToolOpen: !!(
        dialog && dialog.open && document.getElementById("nl-root") &&
        document.getElementById("nl-root").inert
      )
    };
  }

  function directionState() {
    var html = document.documentElement;
    var summary = document.querySelector(".nl-unit-summary");
    var dialog = document.getElementById("nl-unit-tool");
    var beam = document.querySelector(".nl-unit-beam");

    return {
      htmlLang: html.lang,
      htmlDir: html.dir,
      summaryDirection: summary ? getComputedStyle(summary).direction : null,
      dialogDirAttribute: dialog ? dialog.getAttribute("dir") : null,
      beamBearing: beam ? Number(beam.dataset.bearing) : null,
      visibleDoorCopy: Array.from(document.querySelectorAll(".nl-unit-doors > button"))
        .filter(visible)
        .map(function (button) {
          return (button.textContent || "").trim().replace(/\s+/g, " ");
        })
    };
  }

  function mapResources() {
    return {
      mapboxCanvases: document.querySelectorAll(".mapboxgl-canvas").length,
      mapboxMapsInSelectedSurface: document.querySelectorAll(
        ".nl-unit-beam .mapboxgl-map, .nl-window-tool .mapboxgl-map"
      ).length,
      scripts: Array.from(document.scripts).map(function (script) {
        return script.src;
      }).filter(function (src) {
        return /mapbox|leaflet/i.test(src);
      }),
      stylesheets: Array.from(document.styleSheets).map(function (sheet) {
        return sheet.href;
      }).filter(function (href) {
        return href && /mapbox|leaflet/i.test(href);
      }),
      heapBytes: performance.memory ? performance.memory.usedJSHeapSize : null
    };
  }

  var capturedModel = null;

  function captureModelIdentity() {
    capturedModel = document.getElementById("nl-mv");
    return {
      captured: !!capturedModel,
      element: label(capturedModel),
      src: capturedModel && capturedModel.getAttribute("src")
    };
  }

  function checkModelIdentity() {
    var current = document.getElementById("nl-mv");
    return {
      capturedPreviously: !!capturedModel,
      currentExists: !!current,
      sameDomNode: !!capturedModel && capturedModel === current,
      currentConnected: !!current && current.isConnected,
      currentSrc: current && current.getAttribute("src")
    };
  }

  function startReadOnlyLifecycleLog() {
    var rows = [];
    var dialog = document.getElementById("nl-unit-tool");

    if (!dialog) {
      return {
        error: "#nl-unit-tool does not exist yet; open one tool, close it, and retry",
        rows: rows,
        stop: function () { return rows; }
      };
    }

    /* Read-only observer: it records mutations and never writes an attribute. */
    var observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        rows.push({
          at: performance.now(),
          attribute: mutation.attributeName,
          open: dialog.open,
          activeElement: label(document.activeElement),
          mapboxCanvases: document.querySelectorAll(".mapboxgl-canvas").length,
          heapBytes: performance.memory ? performance.memory.usedJSHeapSize : null
        });
      });
    });

    observer.observe(dialog, {
      attributes: true,
      attributeFilter: ["open"]
    });

    return {
      rows: rows,
      stop: function () {
        observer.disconnect();
        return rows.slice();
      }
    };
  }

  function report() {
    var scope = selectedScope();
    var nested = nestedScrollers(scope);
    var fit = viewportFit();
    var blocks = fixedContainingBlocks();
    var clipped = clippedContent();
    var targets = smallTargets();

    var result = {
      generatedAt: new Date().toISOString(),
      url: location.href,
      userAgent: navigator.userAgent,
      scope: label(scope),
      nestedScrollers: nested,
      viewportFit: fit,
      fixedContainingBlocks: blocks,
      clippedContent: clipped,
      smallTargets: targets,
      focus: focusState(),
      direction: directionState(),
      maps: mapResources(),
      pass: {
        zeroNestedScrollers: nested.length === 0,
        noImmediateClipping: clipped.length === 0,
        touchTargetsAtLeast44: targets.length === 0,
        viewportSurfaceVisible: fit.fullyVisible,
        dialogAttachedToBody: !document.getElementById("nl-unit-tool") || blocks.pass
      }
    };

    console.group("NadLan selected-unit acceptance report");
    console.log(result);
    console.table(nested);
    console.table(clipped);
    console.table(targets);
    console.groupEnd();

    return result;
  }

  window.NLUnitAudit = Object.freeze({
    report: report,
    nestedScrollers: nestedScrollers,
    viewportFit: viewportFit,
    fixedContainingBlocks: fixedContainingBlocks,
    clippedContent: clippedContent,
    smallTargets: smallTargets,
    focusState: focusState,
    directionState: directionState,
    mapResources: mapResources,
    captureModelIdentity: captureModelIdentity,
    checkModelIdentity: checkModelIdentity,
    startReadOnlyLifecycleLog: startReadOnlyLifecycleLog
  });

  console.info(
    "NLUnitAudit is ready. Run NLUnitAudit.report() in building, selected-unit, " +
    "plan, view and tour states. No page actions were performed."
  );
}());

/*
 * MANUAL PHYSICAL-PHONE SEQUENCE — do not automate:
 *
 * 1. Cold-load the sandbox and run NLUnitAudit.captureModelIdentity().
 * 2. Select from a building hotspot. Confirm map+beam+facts+doors are visible.
 * 3. Run NLUnitAudit.report(); zeroNestedScrollers must be true.
 * 4. Return to building, scroll to inventory, select a card. The theater must
 *    enter the viewport; the selected screen must not open above it.
 * 5. Open each tool, run report, close with visible Back, Escape where
 *    available, and Android/browser Back. Focus must return to its door.
 * 6. Rotate portrait/landscape and repeat at 200% text size.
 * 7. Run NLUnitAudit.checkModelIdentity(); sameDomNode must stay true.
 * 8. Repeat for HE/AR and EN/FR/RU; inspect directionState and all copy.
 * 9. Repeat 20 open/close cycles while sampling mapResources. Canvas count and
 *    heap should return near baseline after garbage collection opportunities.
 * 10. Real-device visual acceptance by the owner is the release gate.
 */
