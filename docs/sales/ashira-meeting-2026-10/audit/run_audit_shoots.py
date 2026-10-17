# -*- coding: utf-8 -*-
"""Complete automated press audit and screenshot runner for Ashira (A) vs Rainbow (B).
Runs Playwright on Chrome at 1440x900 and 390x844.
Tests every control requested in BRIEF-audit.md.
Saves screenshots to docs/sales/ashira-meeting-2026-10/audit/<page>-<w>-<control>.png.
"""
import os, sys, json, time, traceback
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))

PAGES = {
    "A": "https://nad-lan.co.il/projects/ashira-sde-dov/",
    "B": "https://nad-lan.co.il/projects/rainbow-tel-aviv/"
}
WIDTHS = [
    ("d", 1440, 900),
    ("m", 390, 844)
]

def run():
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
        )
        
        for key, url in PAGES.items():
            results[key] = {}
            for w_tag, w, h in WIDTHS:
                print(f"\n==================== Testing Page {key} at {w_tag} ({w}x{h}) ====================")
                context = browser.new_context(
                    viewport={"width": w, "height": h},
                    locale="he-IL",
                    device_scale_factor=1
                )
                page = context.new_page()
                page_results = {}
                
                # 0. Load page
                print(f"Loading {url}...")
                page.goto(url, wait_until="load", timeout=90000)
                page.wait_for_timeout(6000)
                
                # Helper for screenshot
                def shot(control_name, element=None):
                    filename = f"{key}-{w_tag}-{control_name}.png"
                    path = os.path.join(HERE, filename)
                    try:
                        if element:
                            element.screenshot(path=path)
                        else:
                            page.screenshot(path=path)
                        print(f"  [SHOT] {filename} saved")
                    except Exception as e:
                        print(f"  [SHOT ERR] {filename}: {e}")
                        try:
                            page.screenshot(path=path)
                        except Exception:
                            pass
                            
                # Helper for y coordinate
                def get_y(selector):
                    try:
                        return page.evaluate(f"""(sel) => {{
                            const el = document.querySelector(sel);
                            if (!el) return null;
                            const r = el.getBoundingClientRect();
                            return Math.round(r.top + window.scrollY);
                        }}""", selector)
                    except Exception:
                        return null

                # 1. Measure section order
                order = {
                    "h1": get_y("h1"),
                    "lead": get_y(".nl-lead"),
                    "ctas": get_y(".nlps-hero-actions, .nlps-hero__cta, [data-nlps-ev='hero-wa']"),
                    "stage": get_y("#nlps"),
                    "view": get_y("#nlps-view"),
                    "map": get_y("#nlpjx-map"),
                    "facts": get_y(".nlpf, #nlv2-ashira-info, .nlps-factswrap"),
                    "article": get_y("#nlv2-ashira-info h2, #nlpjx-price, article h2")
                }
                print(f"  Order on screen: {order}")
                page_results["order"] = order
                
                shot("top")

                # 2. Test Control: Floors
                # Select a floor: either via stage API or by clicking the stage / floor button
                print("  Testing Floors...")
                floor_res = page.evaluate("""() => {
                    try {
                        if (window.__nlpsStage && typeof window.__nlpsStage.selectFloor === 'function') {
                            window.__nlpsStage.selectFloor(13);
                            return { method: 'stageApi', floor: 13, ok: true };
                        }
                    } catch (e) {
                        return { ok: false, err: String(e) };
                    }
                    return { ok: false, err: 'no stage api' };
                }""")
                page.wait_for_timeout(2000)
                # Check if cardhost or label is shown
                card_text = page.evaluate("""() => {
                    const host = document.getElementById('nlps-pick') || document.querySelector('.rbs-cardhost') || document.querySelector('.rbs-label');
                    return host ? host.innerText.slice(0, 200) : null;
                }""")
                floor_res["card"] = card_text
                page_results["floor"] = floor_res
                print(f"    Floor result: {floor_res}")
                shot("floor")

                # 3. Test Control: Towers / Buildings
                print("  Testing Towers / Buildings...")
                tower_res = page.evaluate("""() => {
                    // Check for radio buttons in pricing calculator (tower vs boutique)
                    const towerRadio = document.querySelector('input[name=\"nlpg-m\"][value=\"tower\"], input[name=\"nlpg-m\"][value=\"boutique\"]');
                    // Check for stage tower proxies or API
                    const stageTowers = window.__nlpsStage && window.__nlpsStage.towers ? window.__nlpsStage.towers : null;
                    return {
                        hasTowerCalc: !!towerRadio,
                        stageTowers: stageTowers
                    };
                }""")
                # Try clicking boutique radio if exists in calc
                try:
                    boutique_btn = page.query_selector('label:has(input[value="boutique"]), input[value="boutique"]')
                    if boutique_btn:
                        boutique_btn.scroll_into_view_if_needed()
                        boutique_btn.click()
                        tower_res["clickedBoutique"] = True
                        page.wait_for_timeout(1000)
                except Exception as e:
                    tower_res["clickErr"] = str(e)
                page_results["tower"] = tower_res
                print(f"    Tower result: {tower_res}")
                shot("tower")

                # 4. Test Control: Directions
                print("  Testing Directions...")
                dir_res = page.evaluate("""() => {
                    // Try setting facing via stage API or finding direction chips
                    if (window.__nlpsStage && typeof window.__nlpsStage.setFacing === 'function') {
                        const ok = window.__nlpsStage.setFacing(270); // west / sea
                        return { method: 'stageApi', bearing: 270, ok: ok };
                    }
                    return { ok: false, err: 'no setFacing' };
                }""")
                page.wait_for_timeout(1500)
                page_results["directions"] = dir_res
                print(f"    Direction result: {dir_res}")
                shot("dir")

                # 5. Test Control: Example Apartment
                print("  Testing Example Apartment...")
                apt_res = page.evaluate("""() => {
                    // Check docked card or unit selector
                    const docked = document.querySelector('.rbs-label--docked, #nlps-pick .rbs-label');
                    const acts = document.querySelectorAll('.rbs-act, .nlps-step');
                    return {
                        dockedExists: !!docked,
                        dockedVisible: docked ? getComputedStyle(docked).display !== 'none' : false,
                        acts: Array.from(acts).map(a => a.innerText.trim()).filter(Boolean)
                    };
                }""")
                page_results["apartment"] = apt_res
                print(f"    Apartment result: {apt_res}")
                shot("apartment")

                # 6. Test Control: Rooms / 360 Tour
                print("  Testing Rooms / 360 Tour...")
                # Find tour button: either Step 3 "נכנסים לדירה", or [data-nlps-tour], or action button "להיכנס לדירה · 360°"
                tour_info = page.evaluate("""() => {
                    const stepInside = document.querySelector('button[data-nlps-step="inside"]');
                    const tourBtn = document.querySelector('[data-nlps-tour]');
                    const actInside = document.querySelector('.rbs-act[data-act="inside"], [data-act="inside"]');
                    return {
                        hasStepInside: !!stepInside,
                        hasTourBtn: !!tourBtn,
                        hasActInside: !!actInside
                    };
                }""")
                tour_action_result = "not_found"
                try:
                    # Look for button inside docked card or step
                    btn = page.query_selector('.rbs-act[data-act="inside"], button[data-nlps-step="inside"], [data-nlps-tour]')
                    if btn:
                        btn.scroll_into_view_if_needed()
                        btn.click(timeout=3000)
                        page.wait_for_timeout(3000)
                        # Check if modal or viewer opened
                        viewer_open = page.evaluate("""() => {
                            const v = document.querySelector('.nlat-viewer, .nl-tour-modal, .rbs-tour, dialog[open], [role=\"dialog\"]');
                            return v ? { open: true, cls: v.className } : { open: false };
                        }""")
                        tour_action_result = viewer_open
                    else:
                        tour_action_result = {"open": False, "reason": "No tour button found in DOM"}
                except Exception as e:
                    tour_action_result = {"open": False, "err": str(e)}
                page_results["tour"] = {"info": tour_info, "action": tour_action_result}
                print(f"    Tour result: {page_results['tour']}")
                shot("tour")

                # Close any opened tour modal
                try:
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(500)
                except Exception:
                    pass

                # 7. Test Control: Facilities
                print("  Testing Facilities...")
                fac_res = {}
                try:
                    fac_btn = page.query_selector('button[data-nlps-phase="facilities"], .nlps-facbtn')
                    if fac_btn:
                        fac_btn.scroll_into_view_if_needed()
                        fac_btn.click(timeout=3000)
                        page.wait_for_timeout(2000)
                        fac_card = page.evaluate("""() => {
                            const c = document.querySelector('.rbs-qcard, .nlps-faccard, .rbs-fac-pop, .rbs-card');
                            return c ? { on: c.classList.contains('is-on'), text: c.innerText.slice(0, 200) } : null;
                        }""")
                        fac_res = {"clicked": True, "card": fac_card}
                    else:
                        fac_res = {"clicked": False, "reason": "No facilities button found"}
                except Exception as e:
                    fac_res = {"clicked": False, "err": str(e)}
                page_results["facilities"] = fac_res
                print(f"    Facilities result: {fac_res}")
                shot("facilities")

                # Close qcard
                try:
                    page.evaluate("() => { const c = document.querySelector('.rbs-qcard'); if (c) c.classList.remove('is-on'); }")
                except Exception:
                    pass

                # 8. Test Control: Floor view (#nlps-view)
                print("  Testing Floor View (#nlps-view)...")
                view_res = {}
                try:
                    view_sec = page.query_selector('#nlps-view')
                    if view_sec:
                        view_sec.scroll_into_view_if_needed()
                        page.wait_for_timeout(2000)
                        view_info = page.evaluate("""() => {
                            const v = document.getElementById('nlps-view');
                            const map = document.getElementById('nlps-view-map');
                            const t = document.getElementById('nlps-view-t');
                            return {
                                hasView: !!v,
                                hasMap: !!map,
                                title: t ? t.innerText.trim() : null,
                                mapboxLoaded: !!window.mapboxgl
                            };
                        }""")
                        view_res = {"ok": True, "info": view_info}
                    else:
                        view_res = {"ok": False, "reason": "#nlps-view not found"}
                except Exception as e:
                    view_res = {"ok": False, "err": str(e)}
                page_results["view"] = view_res
                print(f"    View result: {view_res}")
                shot("view")

                # 9. Test Control: Area Map categories & pins (#nlpjx-map)
                print("  Testing Area Map categories & pins...")
                map_res = {}
                try:
                    map_sec = page.query_selector('#nlpjx-map')
                    if map_sec:
                        map_sec.scroll_into_view_if_needed()
                        page.wait_for_timeout(2000)
                        # Click on category button 'outdoors' or 'transport'
                        cat_btn = page.query_selector('button[data-g="outdoors"], button[data-g="transport"]')
                        if cat_btn:
                            cat_text = cat_btn.inner_text()
                            cat_btn.click()
                            page.wait_for_timeout(1000)
                            map_res["catClicked"] = cat_text
                        shot("map-cat")
                        
                        # Click on a map pin or comp
                        pin_clicked = page.evaluate("""() => {
                            const marker = document.querySelector('.mapboxgl-marker');
                            if (marker) {
                                marker.click();
                                return { clicked: true, cls: marker.className };
                            }
                            return { clicked: false };
                        }""")
                        page.wait_for_timeout(1000)
                        map_res["pinClicked"] = pin_clicked
                        shot("map-pin")
                    else:
                        map_res = {"ok": False, "reason": "#nlpjx-map not found"}
                except Exception as e:
                    map_res = {"err": str(e)}
                page_results["map"] = map_res
                print(f"    Map result: {map_res}")

                # 10. Test Control: Price Calculator (#nlpg)
                print("  Testing Price Calculator (#nlpg)...")
                calc_res = {}
                try:
                    calc_sec = page.query_selector('#nlpg')
                    if calc_sec:
                        calc_sec.scroll_into_view_if_needed()
                        page.wait_for_timeout(1500)
                        # Move area slider #nlpg-a
                        slider = page.query_selector('#nlpg-a')
                        if slider:
                            page.evaluate("() => { const s = document.getElementById('nlpg-a'); if (s) { s.value = 110; s.dispatchEvent(new Event('input')); s.dispatchEvent(new Event('change')); } }")
                            page.wait_for_timeout(1000)
                            calc_res["sliderMoved"] = True
                        shot("calc")
                    else:
                        calc_res = {"ok": False, "reason": "#nlpg not found"}
                except Exception as e:
                    calc_res = {"err": str(e)}
                page_results["calc"] = calc_res
                print(f"    Calc result: {calc_res}")

                # 11. Test Control: Design styles
                print("  Testing Design styles...")
                design_res = {}
                try:
                    # Look for design step button: [data-nlps-step="design"]
                    d_step = page.query_selector('button[data-nlps-step="design"]')
                    if d_step:
                        d_step.scroll_into_view_if_needed()
                        d_step.click()
                        page.wait_for_timeout(2000)
                        # Check where it navigated or what opened
                        loc = page.evaluate("() => ({ scrollY: window.scrollY, hash: location.hash })")
                        design_res = {"stepClicked": True, "loc": loc}
                    else:
                        design_res = {"stepClicked": False, "reason": "No design step found"}
                    shot("design")
                except Exception as e:
                    design_res = {"err": str(e)}
                page_results["design"] = design_res
                print(f"    Design result: {design_res}")

                # 12. Test Control: Basket ("סל הדירה")
                print("  Testing Basket...")
                basket_res = {}
                try:
                    b_btn = page.query_selector('.nlbk-step, button:has-text("סל הדירה")')
                    if b_btn:
                        b_btn.scroll_into_view_if_needed()
                        b_btn.click()
                        page.wait_for_timeout(2000)
                        drawer = page.evaluate("""() => {
                            const d = document.querySelector('.nlbk-drawer, .nlbk-modal, [class*=\"basket\"], [class*=\"nlbk\"]');
                            return d ? { exists: true, cls: d.className, visible: getComputedStyle(d).display !== 'none' } : null;
                        }""")
                        basket_res = {"clicked": True, "drawer": drawer}
                    else:
                        basket_res = {"clicked": False, "reason": "No basket button"}
                    shot("basket")
                except Exception as e:
                    basket_res = {"err": str(e)}
                page_results["basket"] = basket_res
                print(f"    Basket result: {basket_res}")

                # 13. Test Control: Video call ("שיחת וידאו עם נציג")
                print("  Testing Video call...")
                video_res = {}
                try:
                    v_btn = page.query_selector('[data-nlps-ev="hero-video"], a[href="#nlsch"]')
                    if v_btn:
                        v_btn.scroll_into_view_if_needed()
                        v_btn.click()
                        page.wait_for_timeout(2000)
                        sch_visible = page.evaluate("""() => {
                            const sch = document.getElementById('nlsch');
                            if (!sch) return null;
                            const r = sch.getBoundingClientRect();
                            return { inViewport: r.top >= 0 && r.top < window.innerHeight, top: r.top };
                        }""")
                        video_res = {"clicked": True, "scheduler": sch_visible}
                    else:
                        video_res = {"clicked": False, "reason": "No video call button"}
                    shot("video")
                except Exception as e:
                    video_res = {"err": str(e)}
                page_results["video"] = video_res
                print(f"    Video result: {video_res}")

                # 14. Test Control: WhatsApp bar (#nlcta)
                print("  Testing WhatsApp bar...")
                wa_res = {}
                try:
                    wa_el = page.query_selector('#nlcta, .nlcta-wa')
                    if wa_el:
                        wa_info = page.evaluate("""() => {
                            const el = document.getElementById('nlcta') || document.querySelector('.nlcta-wa');
                            if (!el) return null;
                            const a = el.matches('a') ? el : el.querySelector('a');
                            return {
                                visible: getComputedStyle(el).display !== 'none',
                                href: a ? a.href.slice(0, 100) : null,
                                text: el.innerText.trim()
                            };
                        }""")
                        wa_res = {"exists": True, "info": wa_info}
                    else:
                        wa_res = {"exists": False}
                    shot("whatsapp")
                except Exception as e:
                    wa_res = {"err": str(e)}
                page_results["whatsapp"] = wa_res
                print(f"    WhatsApp result: {wa_res}")

                # Save page run results
                results[key][w_tag] = page_results
                context.close()
                
        browser.close()
        
    with open(os.path.join(HERE, 'audit-results.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\nAll controls tested and audit-results.json written successfully!")

if __name__ == '__main__':
    run()
