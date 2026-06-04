# Mobile Responsiveness Audit: Recent Articles

Date: 2026-06-04
Viewport target: 390px mobile visual viewport.
Method: headless Chrome via DevTools Protocol with mobile user agent and device metrics override.
Source set: newest 10 `wp/v2/pages` entries because `wp/v2/posts` currently returns an empty list.

## Executive Summary

The last 10 article pages share the same mobile problems:

- Data tables are the dominant issue. They create layout widths wider than the 390px visual viewport and make financial/legal comparison content hard to read.
- A fixed `.nlfab` WhatsApp/call bar appears on every page and can sit awkwardly against the expanded layout.
- The mobile navigation hamburger is `24x24`, below the 44px tap target standard.
- Brand/nav/footer links often have heights around 25-38px, below the target.
- Table header text is often 13px, below the 14px minimum requested for meaningful text.
- No major image or hero crop breakage was detected by the automated pass.
- The first audited page title appears as question marks in REST/browser output. That is not a responsiveness bug, but it should be checked separately because it affects page quality and identification.

Important technical observation: Chrome reported a 390px `visualViewport`, but many pages expanded the layout viewport beyond 390px. The worst cases were 630px and 677px layout widths. That indicates fixed-width or unwrapped content is forcing mobile expansion.

## Per-URL Issues

### 1. ×’×¨×™×¨×ª ×ž×©×›× ×ª× 2026: ××™×š ×œ×”×¢×‘×™×¨ ×ž×©×›× ×ª× ×ž×“×™×¨×” ×œ×“×™×¨×”

URL: `https://nad-lan.co.il/mortgage-calculator/mortgage-porting/`
Chrome result: visual viewport 390px, layout viewport 630px, scroll width 631px.

| URL | Element | Severity | What's wrong | Suggested fix |
| --- | --- | --- | --- | --- |
| `/mortgage-calculator/mortgage-porting/` | `table` | Blocker | Main comparison table is about 605px wide and forces the page beyond the 390px phone viewport. | Convert comparison tables on mobile into stacked cards or a horizontally scrollable table wrapper with visible affordance and preserved RTL. |
| `/mortgage-calculator/mortgage-porting/` | `th` | Major | Table headers render at 13px. | Raise meaningful table text to at least 14px, preferably 15-16px for financial examples. |
| `/mortgage-calculator/mortgage-porting/` | `div.nlfab` | Major | Fixed WhatsApp/call bar is 177x42 and is positioned against the expanded layout, not the 390px visual viewport. | Re-anchor to the visual viewport/safe area, or convert to a full-width mobile CTA bar with 44px height. |
| `/mortgage-calculator/mortgage-porting/` | `button.wp-block-navigation__responsive-container-open` | Major | Mobile menu tap target is 24x24. | Increase hit area to at least 44x44 while keeping the icon visually balanced. |
| `/mortgage-calculator/mortgage-porting/` | `h1` / REST title | Minor | Audit output showed the title as `????? ?????? 2026...`, suggesting an encoding/title storage issue. | Verify the saved page title and REST output encoding for this page. |

### 2. ××™×©×•×¨ ×¢×§×¨×•× ×™ ×œ×ž×©×›× ×ª× 2026: ×ž×” ×”×‘× ×§ ×‘××ž×ª ×ž××©×¨

URL: `https://nad-lan.co.il/mortgage-calculator/mortgage-pre-approval/`
Chrome result: visual viewport 390px, layout viewport 433px, scroll width 434px.

| URL | Element | Severity | What's wrong | Suggested fix |
| --- | --- | --- | --- | --- |
| `/mortgage-calculator/mortgage-pre-approval/` | `table` | Major | Main table is about 408px wide and still expands beyond a 390px phone viewport. | Use mobile card rows for comparison data or wrap the table with overflow and edge fades. |
| `/mortgage-calculator/mortgage-pre-approval/` | `th` | Major | Table header text is 13px. | Set mobile table headers/body to at least 14px and reduce columns through stacking. |
| `/mortgage-calculator/mortgage-pre-approval/` | `div.nlfab` | Minor | Fixed CTA bar is present on top of content flow risk. | Ensure it has safe-area spacing and does not obscure final paragraphs or footer links. |
| `/mortgage-calculator/mortgage-pre-approval/` | `button.wp-block-navigation__responsive-container-open` | Major | Hamburger button is 24x24. | Enlarge touch target to 44x44. |

### 3. ×ž×¡×•×¨×‘×™ ×ž×©×›× ×ª× 2026: ×œ×ž×” ×”×‘× ×§ ×ž×¡×¨×‘ ×•×ž×” ×¢×•×©×™×

URL: `https://nad-lan.co.il/mortgage-calculator/mortgage-refusal/`
Chrome result: visual viewport 390px, layout viewport 527px, scroll width 528px.

| URL | Element | Severity | What's wrong | Suggested fix |
| --- | --- | --- | --- | --- |
| `/mortgage-calculator/mortgage-refusal/` | `table` | Blocker | Main table is about 502px wide and expands the layout substantially past 390px. | Replace dense matrix tables with stacked decision cards on mobile. |
| `/mortgage-calculator/mortgage-refusal/` | `th` | Major | Table headers are 13px and wrap into tall cells. | Increase mobile table text size and reduce each mobile row to label/value pairs. |
| `/mortgage-calculator/mortgage-refusal/` | `div.nlfab` | Major | Fixed CTA bar sits in a layout that is already wider than the visual viewport. | Anchor to viewport and give it bottom spacing; test with footer visible. |
| `/mortgage-calculator/mortgage-refusal/` | nav/footer links | Major | Several links are about 25px high. | Give all interactive links in mobile nav/footer a minimum 44px line box or padding. |

### 4. ×ž×©×›× ×ª× ×œ×›×œ ×ž×˜×¨×” 2026: ×”×œ×•×•××” ×›× ×’×“ ×“×™×¨×” ×§×™×™×ž×ª

URL: `https://nad-lan.co.il/mortgage-calculator/mortgage-for-any-purpose/`
Chrome result: visual viewport 390px, layout viewport 677px, scroll width 678px.

| URL | Element | Severity | What's wrong | Suggested fix |
| --- | --- | --- | --- | --- |
| `/mortgage-calculator/mortgage-for-any-purpose/` | `table` | Blocker | Main table is about 652px wide, the worst overflow in this audit. | Use a mobile-specific card/table transform for mortgage calculation examples. |
| `/mortgage-calculator/mortgage-for-any-purpose/` | `th` | Major | Headers are 13px and cells are very tall due wrapping. | Increase table text and collapse columns into readable sections. |
| `/mortgage-calculator/mortgage-for-any-purpose/` | `div.nlfab` | Major | Fixed CTA bar is positioned far outside the 390px visual context in the audit geometry. | Position relative to visual viewport and avoid fixed horizontal offsets that depend on layout width. |
| `/mortgage-calculator/mortgage-for-any-purpose/` | nav links | Major | Several nav/footer links are below 44px height. | Normalize mobile link padding across header, breadcrumbs, related links, and footer. |

### 5. ×”×œ×•×•××ª ×’×™×©×•×¨ ×œ×“×™×¨×” 2026: ×§×•× ×™× ×œ×¤× ×™ ×©×ž×•×›×¨×™× ×‘×œ×™ ×œ×”×¡×ª×›×Ÿ

URL: `https://nad-lan.co.il/mortgage-calculator/bridge-loan-apartment/`
Chrome result: visual viewport 390px, layout viewport 511px, scroll width 512px.

| URL | Element | Severity | What's wrong | Suggested fix |
| --- | --- | --- | --- | --- |
| `/mortgage-calculator/bridge-loan-apartment/` | `table` | Blocker | Main table is about 486px wide and pushes layout past mobile width. | Turn scenario tables into stacked cards with scenario title, numbers, and risk note. |
| `/mortgage-calculator/bridge-loan-apartment/` | `th` | Major | Financial table labels render at 13px. | Increase mobile table type size and use fewer visible columns. |
| `/mortgage-calculator/bridge-loan-apartment/` | `div.nlfab` | Major | Fixed CTA bar is present and may not align with the visual viewport. | Use bottom-safe sticky CTA behavior and retest at 390px. |
| `/mortgage-calculator/bridge-loan-apartment/` | `button.wp-block-navigation__responsive-container-open` | Major | Hamburger target is 24x24. | Expand hit area to 44x44. |

### 6. ×ž×›×™×¨×ª ×“×™×¨×” ×‘×ž×›×¨×– 2026: ×”×¦×¢×•×ª, ×ž×—×™×¨ ×©×ž×•×¨ ×•×¡×™× ×•×Ÿ ×§×•× ×™×

URL: `https://nad-lan.co.il/selling-apartment/real-estate-auction-sale/`
Chrome result: visual viewport 390px, layout viewport 494px, scroll width 495px.

| URL | Element | Severity | What's wrong | Suggested fix |
| --- | --- | --- | --- | --- |
| `/selling-apartment/real-estate-auction-sale/` | `table` | Blocker | Main table is about 469px wide and causes mobile expansion. | Convert sale-method comparison table into cards or use an accessible scroll wrapper. |
| `/selling-apartment/real-estate-auction-sale/` | `th` | Major | Header cells are 13px. | Increase text size and improve mobile table spacing. |
| `/selling-apartment/real-estate-auction-sale/` | `div.nlfab` | Minor | Fixed CTA bar appears on mobile. | Ensure it does not overlap footer/legal links and has 44px height. |
| `/selling-apartment/real-estate-auction-sale/` | nav/footer links | Major | Several links are below 44px tap height. | Apply shared mobile tap target rule to all link clusters. |

### 7. ×¨×›×™×©×ª ×§×¨×§×¢ 2026: ×‘×“×™×§×•×ª, ×–×›×•×™×•×ª, ×ª×‘"×¢ ×•×ž×¡×™× ×œ×¤× ×™ ×—×ª×™×ž×”

URL: `https://nad-lan.co.il/real-estate-lawyer/land-purchase-checklist/`
Chrome result: visual viewport 390px, layout viewport 396px, scroll width 397px.

| URL | Element | Severity | What's wrong | Suggested fix |
| --- | --- | --- | --- | --- |
| `/real-estate-lawyer/land-purchase-checklist/` | `table` | Major | Table is about 371px wide, just under the visual width, but creates near-edge clipping and a 397px scroll width. | Add mobile-safe table padding and stacked rows for dense legal checklists. |
| `/real-estate-lawyer/land-purchase-checklist/` | `th` | Major | Headers are 13px. | Increase to at least 14px and reduce column count on mobile. |
| `/real-estate-lawyer/land-purchase-checklist/` | `.nadlan-gloss-link` | Major | Inline glossary/taxonomy links can be 45x23 or similar, below 44px height. | Increase line-height/padding for inline tappable glossary links on mobile. |
| `/real-estate-lawyer/land-purchase-checklist/` | `button.wp-block-navigation__responsive-container-open` | Major | Hamburger target is 24x24. | Expand hit area to 44x44. |

### 8. ×“×™×¨×ª ×¤×¨×™×¡×™×™×œ 2026: ×ž×—×™×¨ ××ž×™×ª×™, 20/80 ×•×‘×“×™×§×•×ª ×œ×¤× ×™ ×—×ª×™×ž×”

URL: `https://nad-lan.co.il/new-projects/presale-apartment/`
Chrome result: visual viewport 390px, layout viewport 421px, scroll width 422px.

| URL | Element | Severity | What's wrong | Suggested fix |
| --- | --- | --- | --- | --- |
| `/new-projects/presale-apartment/` | `table` | Major | Main table is about 396px wide and creates horizontal overflow on a 390px phone. | Use stacked cards for price/risk components or add an accessible scroll wrapper. |
| `/new-projects/presale-apartment/` | `th` | Major | Headers are 13px and comparison cells become very tall. | Increase type size and restructure table into mobile sections. |
| `/new-projects/presale-apartment/` | related/nav links | Major | Some links are 25px high, even when text is long. | Ensure 44px tap target through padding, not just text line-height. |
| `/new-projects/presale-apartment/` | `div.nlfab` | Minor | Fixed CTA bar appears on the page. | Verify it does not cover content at the bottom of long pages. |

### 9. ×§×‘×•×¦×ª ×¨×›×™×©×” 2026: ×¡×™×›×•× ×™×, ×ž×™×¡×•×™ ×•×”×‘×“×œ ×ž×¨×›×™×©×” ×ž×§×‘×œ×Ÿ

URL: `https://nad-lan.co.il/new-projects/purchasing-group/`
Chrome result: visual viewport 390px, layout viewport 429px, scroll width 430px.

| URL | Element | Severity | What's wrong | Suggested fix |
| --- | --- | --- | --- | --- |
| `/new-projects/purchasing-group/` | `table` | Major | Main table is about 404px wide and exceeds the visual viewport. | Use cardized comparison rows for mobile. |
| `/new-projects/purchasing-group/` | `th` | Major | Headers render at 13px. | Increase meaningful table labels to at least 14px. |
| `/new-projects/purchasing-group/` | `button.wp-block-navigation__responsive-container-open` | Major | Hamburger button is 24x24. | Enlarge touch target to 44x44. |
| `/new-projects/purchasing-group/` | footer/nav links | Major | Multiple links have 25px tap height. | Add shared mobile link padding in header/footer/related clusters. |

### 10. ×¢×¡×§×ª ×§×•×ž×‘×™× ×¦×™×” ×‘×ž×§×¨×§×¢×™×Ÿ 2026: ××—×•×–×™×, ×ž×™×¡×•×™ ×•×¡×™×›×•× ×™×

URL: `https://nad-lan.co.il/real-estate-lawyer/combination-deal/`
Chrome result: visual viewport 390px, layout viewport 414px, scroll width 415px.

| URL | Element | Severity | What's wrong | Suggested fix |
| --- | --- | --- | --- | --- |
| `/real-estate-lawyer/combination-deal/` | `table` | Major | Main table is about 389px wide and pushes total scroll width to 415px. | Add mobile-safe table treatment and avoid edge-to-edge clipping. |
| `/real-estate-lawyer/combination-deal/` | `th` | Major | Headers are 13px. | Increase mobile table text and use label/value presentation. |
| `/real-estate-lawyer/combination-deal/` | `.nadlan-gloss-link` | Major | Glossary link appears at about 118x26, below 44px height. | Increase inline interactive line-height/padding on mobile. |
| `/real-estate-lawyer/combination-deal/` | `div.nlfab` | Minor | Fixed CTA bar appears on mobile. | Recheck safe-area placement and footer overlap after table fixes. |

## Shared Fix Themes For Claude

- Add one reusable mobile table pattern for article content. The best default is stacked cards for tables with more than 3 columns.
- If horizontal scrolling remains, wrap tables in an accessible scroll region with visible cue, RTL-safe scroll behavior, and no body-level overflow.
- Set meaningful mobile table text to at least 14px.
- Give hamburger, header links, footer links, glossary links, and CTA links a minimum 44px tap target.
- Audit `.nlfab` at 390px after table fixes, because some positioning problems may disappear once page width is no longer forced wider than the phone.
- Add a regression check that compares `visualViewport.width` to document scroll width and flags any article with more than 1px horizontal overflow.

## What I Could Not Do And Why

- I did not apply fixes because this mission is docs-only.
- I did not generate screenshots because the deliverable asked for issue tables and described fixes, not replacement imagery.
- The first page title was corrupted in the audit output and REST response, so I inferred the Hebrew title from the slug and visible article intent. This should be verified separately in WordPress.
