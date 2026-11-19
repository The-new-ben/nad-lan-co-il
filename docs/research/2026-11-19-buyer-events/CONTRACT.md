# Package 5 contract: buyer events (`window.nlTrack`), 19.11.2026

Owner: package 5 session (HAD-791). Files owned: `inc/visit-trail.php`, `inc/dev-report.php` (new), `assets/visit-trail/*`.
Storage: our own tables on nad-lan.co.il (`nadlan_visits`, `nadlan_visit_events`), first party, no IP, no field values,
Global Privacy Control / Do Not Track / the visitor's own opt-out respected. Feeds the developer funnel report.

## The one call

```js
// safe on every front page from release 1.72.7xx on; before trail.js loads the calls are queued
window.nlTrack && window.nlTrack('basket_add', { project: 'ashira', unit: 'E-4A', floor: 4 });
```

Or, with no dependency on load order, fire a window event (same effect):

```js
window.dispatchEvent(new CustomEvent('nl:track', { detail: { name: 'call_book', data: { project: 'rainbow' } } }));
```

Write `window.nlTrack && window.nlTrack(...)` (or the event) so a page without the tracker never throws.

## Names (use these exact keys; snake_case, object_action)

| name | when | useful data |
|---|---|---|
| `floor_select` | the buyer picks a floor (not an automatic default) | floor, tower |
| `direction_select` | picks a facing / side | floor, bearing (0-359), dir, unit |
| `unit_open` | opens one apartment's card or sheet | unit, floor, rooms |
| `view_open` | opens the view from a floor / window | floor, bearing, dir |
| `designer_open` | the apartment designer opens | unit, source ("project"/"mine"/"example") |
| `designer_action` | a design step | a: one of `finish`, `partition-add`, `partition-remove`, `point-add`, `point-move`, `item-add`, `note`, `walk`, `plan-load`, `scan` |
| `design_order` | "add to my basket" in the designer (the `nadlan:design-order` event is picked up automatically, no call needed) | unit |
| `mortgage_check` | the buyer changes a monthly payment / mortgage input (numbers are NOT sent) | k: which calculator |
| `basket_add` / `basket_remove` / `basket_open` | the shared basket | unit, v: items count |
| `call_open` / `call_book` / `call_join` | video call sheet opened / a time booked / the buyer joined a live call | k: "video" or "meeting" |
| `rfp_open` / `rfp_send` | the request-for-offer opened / sent | v: items count |
| `lang_switch` | the buyer moves to another language | to: he/en/fr/ru/ar |
| `favorite` / `share` | saved / shared an apartment | unit |

`data` keys kept (everything else is dropped, texts are cut short): `project` (slug or WordPress id: REQUIRED on pages
that are not the project's own page, e.g. `/tour/designer/`, the basket, the RFP page), `unit`, `floor`, `tower`, `bearing`,
`dir`, `rooms`, `a`, `k`, `v` (a small integer), `source`, `to`.
NEVER pass a name, phone, mail, typed text, price the buyer typed, or the design notes' text.

## Already picked up automatically (no work for you)
- every `window.nadlanGA(name, params)` call whose name starts with basket_, cockpit_, offer_, room_, tour_, journey_,
  showroom_, designer_, call_, rfp_, mortgage_ (the existing modules keep calling nadlanGA as today);
- the stage events nl:floor, nl:facing, nl:view, nl:tour, nl:example, nl:floor-action, ...;
- `nadlan:design-order` (package 2);
- the showroom engine pages (Rainbow, Ashira, DUO, H Infinity): read-only watch of `window.NadLanEngine.state`
  (unit picked, tool opened: plan / view / tour / studio / contact / compare), engine.js untouched;
- typing a number in a mortgage calculator (#nmc-*, .nlck, [data-nl-calc]) = `mortgage_check`, without the numbers.

To mark your own calculator: put `data-nl-calc="<key>"` on its root.
