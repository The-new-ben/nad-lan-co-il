# Two patches (not applied)

Made 26.10.2026 against the repo copies of the files (branch claude/apartment-experience-b1). Both apply cleanly in order (`git apply --check`), every touched PHP file passes `php -l` (PHP 8.3), and the tiers module was rendered through a stub harness in Chrome at 390 and 1280 px with no console errors. Nothing was deployed.

**Before shipping:** the repo is not the live site for every file (memory: nadlan-repo-not-live-files). Read each touched file from the live server first and rebuild the hunks on the live copy: `inc/pro-cards.php`, `inc/profile-extras.php`, `inc/placements.php`, `inc/brokers-list.php`, `inc/advertiser-orders.php`, `nadlan-config.php`. Then the usual release ritual (source_audit before and after, rainbow and h-infinity spot checks, PHP_RELS listing the hunked files).

## 01-seo-safety.patch (apply first: before anything is sold)

- New `inc/ad-safety.php`: `nadlan_ad_is_paid()`, `nadlan_ad_rel()` (paid → `sponsored noopener`), `nadlan_ad_free_page()` (post meta `nadlan_ad_free = 1` or a path in option `nadlan_ad_free_paths`), `nadlan_ad_slot_take()` (option `nadlan_ad_paid_cap`, default 3), and the label "פרופיל ממומן · הפרטים והתוכן נמסרו על ידי העסק ובאחריותו" on a paying advertiser's own profile.
- `inc/profile-extras.php`: the website and social links of a paid profile get `rel="sponsored noopener"` (today: `noopener` only, a followed paid link; found in adams-research.md). The section carries `data-paid="1"`.
- `inc/pro-cards.php`: the WhatsApp link of a paid card gets `sponsored`; paid cards beyond the cap are dropped (free cards stay); ad-free pages get no cards; `data-paid="1"` on paid cards.
- `inc/placements.php` + `inc/brokers-list.php`: a placement's outbound links are `sponsored noopener` (new `rel` argument on the feature card); a placement counts toward the cap and never renders on an ad-free page.
- New `tools/seo/paid_link_check.py`: reads public pages and fails on a paid outbound link without `sponsored`, a paid card without "ממומן"/"פרסומת", a paid profile without its label, or more paid cards than the cap. Run it on the touched pages after the release.
- Unpaid business links keep `noopener`. To make them `nofollow ugc noopener`, hook the filter `nadlan_ad_rel_unpaid` (Ben's call; it touches thousands of cards, so it needs his OK on scale and pace).
- No title, H1, slug, noindex, robots or redirect change.

## 02-advertise-tiers.patch

- New `inc/advertise-tiers.php`: the section "מסלולי פרסום ומחירים" on the existing /advertise/ page, inserted before its "נדבר?" chapter (no new URL). Three tracks (בעלי מקצוע, התחדשות עירונית, פרויקטים ונכסים), an exposure ladder, add-ons, a summary with the total, "how it works", "ככה זה נשאר הוגן", and the invoice form. Prices come from the shop products when they exist.
- Self-serve link `?nladt_pick=477,5403&nladt_track=renewal`: login, the user's own card attached (for the urban-renewal track a draft "ארגון דיירים" card is opened if they have none, and published only when the payment activates it), the cart, checkout. Activation, auto-expiry and renewal invoices are the existing code.
- Options: `nadlan_adt_checkout_live` ('1' only after the Morning reconnect; until then every choice opens "הזמנה בחשבונית"), `nadlan_adt_area_product` and `nadlan_adt_story_product` (0 until Ben creates those products; meanwhile they are invoice-only), `nadlan_adt_enabled` (kill switch).
- `inc/advertiser-orders.php`: the area product (when set) is a Premier tier for 30 days on a professional card, so it lapses and renews like the others; on activation a **draft** placement is opened for the admin with the dates filled, and the chosen cities are kept on the order line.
- `inc/placements.php`: a placement for a non-broker (an organizer, a lawyer) shows the professional card under "פרסומת", never the broker card with "מתווך" and a licence line.
- `inc/pro-cards.php`: new sponsorship domain "ליווי דיירים" (profession `organizer`) and its content tokens; showcase cards (`is_demo`, "פרופיל לדוגמה") no longer appear as experts inside real content (today the matching query does not exclude them).
- Language checked against language-dna (no tech words, no long dashes); new anchors checked with kw_guard ("מרכז הפרסום", "כל המסלולים והמחירים": OK).
