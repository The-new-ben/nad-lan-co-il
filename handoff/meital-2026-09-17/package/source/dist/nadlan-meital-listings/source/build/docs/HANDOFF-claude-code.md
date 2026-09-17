# Handoff: Meital Katzir listings for nad-lan.co.il

For: Claude Code (repo and WordPress access). Owner: Ben. Prepared 16 Sep 2026.

This package holds 11 listing pages, each in Hebrew and English, built for the `nadlan_property` post type. Nothing has been uploaded. Your job is to integrate the stylesheet, create **drafts**, wire the translations and stop. Publishing waits for Ben's slug approval, Meital Katzir's written approval of each page, and her photos.

## 0. Ground rules

1. Create drafts only. Never set `status` to `publish`, `future` or `private`. The import script has no publish path; keep it that way.
2. Authenticate with an Application Password for an administrator account. Ask Ben to create it and to put it in the environment himself. Never type, store or log his login password.
3. Files named `brief-he.md` are internal (pricing assessment, cross-listings on other agencies' sites, open questions). Never paste their contents into post content, excerpts, meta or commit messages.
4. Slugs are proposals. Ben approves every new URL (`data/slugs-for-approval.csv`). Create the drafts with the proposed slugs, then change them if he edits the sheet.
5. Copy rules for any text you touch: no en dash or em dash characters (U+2013, U+2014) anywhere; no emoji in visible copy; in Hebrew, write the Hebrew term and give the English professional term in parentheses on first use only.
6. Every figure on the pages is sourced (numbered footnotes) or labeled as broker-stated or computed. If you change a number, change its source or label with it, or leave it alone and report it.

## 1. What is in the package

```
nadlan-meital-listings/
  README-HE.md                    short Hebrew guide for Ben
  HANDOFF-claude-code.md          this file
  assets/nlx-prestige.css         the only stylesheet the blocks need (scoped to .nlx)
  listings/Lxx/
    block-he.html, block-en.html      raw block markup (for inspection and diffing)
    content-he.html, content-en.html  the same markup wrapped in <!-- wp:html --> for post_content
    wp-he.json, wp-en.json            REST payload: title, slug, excerpt, meta, terms, Yoast values
    schema-he.jsonld, schema-en.jsonld  RealEstateListing + Offer + FAQPage (also inline in the block)
    seo.json                          titles, descriptions, focus keyphrases, slugs, hreflang pairs
    shotlist.md                       photo list with file names and alt text in both languages
    brief-he.md                       INTERNAL: assessment, confirm list, cross-listings, risks, gaps
  catalog/                        cards for an index page, HE and EN (block and wrapped content)
  data/listings.json              machine-readable index of all 11 listings and their files
  data/slugs-for-approval.csv     proposed slugs for Ben (UTF-8 with BOM, opens in Excel)
  data/pre-publish-checklist.csv  one row per page, one column per publishing gate
  preview/index.html              open locally to review every page in both languages
  scripts/create_drafts.py        REST importer, dry run by default, drafts only
  scripts/verify_package.py       mechanical checks (dashes, JSON, files, draft status)
  broker/                         broker profile page for Meital Katzir (section 12)
    broker-he.html, broker-en.html            raw page markup
    content-broker-he.html, content-broker-en.html  wrapped in <!-- wp:html --> for a WordPress page
    nlb-broker.css                            stylesheet for the page (scoped to .nlb)
    wp-page-he.json, wp-page-en.json          REST payload for /wp/v2/pages, status draft
    schema-broker-he.jsonld, schema-broker-en.jsonld  RealEstateAgent + ItemList
    seo-broker.json                           titles, descriptions, focus keyphrases, proposed slugs
    cards.json                                card data for the 11 listings (single source for the page)
    claude-design-canvas/                     Claude Design canvas source (.dc.html artboards) and its link
    screenshots/                              desktop and mobile previews of the page
    CLAUDE-DESIGN-BRIEF.md, AI-IMAGE-PROMPTS-HE.md
  media/                          Instagram media manifest per listing (65 posts and reels); photos arrive later
  source/                         generator: editorial JSON, research dossiers, templates, build scripts
```

The listings:

| ID | Deal | Page (EN title) | Price or rent | Status note |
|---|---|---|---|---|
| L01 | Sale | A Private Estate of 700 sqm on a 1.1-Dunam Plot, Herzliya Pituach | On request | Price and street to confirm |
| L07 | Sale | New Mini Penthouse with 80 sqm of Terraces, Kochav HaTzafon | NIS 18,000,000 | Confirm price still valid |
| L08 | Sale | 4.5 Rooms in a Pool and Spa Complex, Migdalei Ne'eman | NIS 5,900,000 | Confirm fee and floor |
| L05 | Sale | Furnished 3.5 Rooms with a Tenant in Place, Eliyahu Berlin Street | NIS 5,000,000 | Price last posted Nov 2025 |
| L04 | Sale | Three Rooms with Two Parking Spaces, Eliyahu Berlin Street | NIS 4,650,000 | Floor 2 or 3 to confirm |
| L06 | Rent | Double-Height Mini Penthouse Facing the Sea, Tzukei Aviv | NIS 27,000 (12 months upfront) | Availability to confirm |
| L02 | Rent | Designer-Finished 4.5 Rooms with a Sea-View Balcony, B.S.R Sarona | On request | Rent to confirm |
| L03 | Rent | Five Rooms on a High Floor with a Sea View, B.S.R Sarona | NIS 15,500 | Confirm current rent |
| L09 | Rent | Five-Room Mini Penthouse with a Sea View, Nofei Yam | On request | **Last post 17 Jun 2026, likely let. Import only after Meital confirms.** |
| L10 | Rent | Three Rooms with a 20 sqm Balcony and Two Parking Spaces, Nofei Yam | NIS 9,500 | Street not published by choice |
| L11 | Rent | Five Rooms on a High Floor in a Complex with a Pool, Ramat Aviv | On request | **Complex unidentified, single post. Import only after Meital confirms.** |

## 2. Preflight on the site (read-only)

Run these before writing anything, and record the answers at the top of your report to Ben.

1. **Post type and REST.**
   `wp post-type get nadlan_property --fields=name,rest_base,has_archive,supports,taxonomies`
   Expected: REST base `nadlan_property`, archive `/properties/`, taxonomy `nadlan_city`.
2. **Meta keys and their types.** The payloads use the keys the REST API exposed on 16 Sep 2026:
   `listing_type, property_type, price, price_per_sqm, rooms, floor, total_floors, size_sqm, balcony_sqm, parking, elevator, ac, protected_room, street, building_number, lat, lng, status, photos_csv, city, neighborhood, arnona_monthly, vaad_bayit_monthly, storage, condition` (the site also has `source, is_sponsored, claim_status, owner_user_id`, which the payloads leave untouched).
   Confirm with `wp eval 'print_r(array_keys(get_registered_meta_keys("post","nadlan_property")));'` and the `OPTIONS /wp-json/wp/v2/nadlan_property` schema. Check allowed values for enumerations:
   - `property_type`: payloads use `apartment`, `penthouse` (L06, L07, L09) and `villa` (L01). If the site uses other slugs, map them and tell Ben.
   - `condition`: payloads use `new`, `good` or null.
   - `status`: payloads send `active`. L09 and L11 must not be imported until confirmed.
   - `source`: leave unset unless the site requires it; if required, ask Ben which value marks broker partnership listings (known values: `owner_wizard`, `demo_seed`).
   - `photos_csv`: inspect an existing post to learn whether it holds attachment IDs or URLs.
   - L01 carries `plot_sqm: 1100` in `source/editorial/L01.json` (`wp` block) but the importer sends only registered keys; if there is no plot field, the plot stays in the page content only.
3. **City terms.** `wp term list nadlan_city --fields=term_id,name,slug`. Payloads name `תל אביב-יפו` and `הרצליה` (and `Tel Aviv-Yafo`, `Herzliya` in the English payloads). Do not create terms without Ben's approval; map to existing ones.
4. **Multilingual system behind `/en/`.** Identify it (`wp plugin list --status=active`): Polylang, WPML, TranslatePress or custom. Section 7 depends on the answer.
5. **HTML capability.** The blocks contain `<svg>`, `<input type="radio">` (CSS-only tabs), `<details>` and `<script type="application/ld+json">`. These survive only for a user with `unfiltered_html`.
   `wp cap list administrator | grep unfiltered_html`, and check that `DISALLOW_UNFILTERED_HTML` is not defined in `wp-config.php`. On multisite only super admins have it. If it is not available, use section 4B.
6. **Single template.** Find the template that renders `nadlan_property` (`single-nadlan_property.php` in `nadlan-revenue` or `nadlan-platform-child`, or a block template). List what it prints outside `the_content()`: title H1, gallery, price box, fact table, contact form, breadcrumbs, related listings. Section 5 decides what to hide.
7. **Yoast.** Yoast SEO 28.5 is active. Look at Search Appearance for `nadlan_property`: does the title template append `%%sep%% %%sitename%%`? Are `_yoast_wpseo_*` keys REST-writable on this site (usually not)?
8. **Fonts.** Skin A should already load `Noto Serif Hebrew` (600) and `Assistant`. Confirm in the page head; the CSS falls back to Georgia and Segoe UI if not.

## 3. Install the stylesheet

Copy `assets/nlx-prestige.css` to the child theme, for example `wp-content/themes/nadlan-platform-child/assets/css/nlx-prestige.css`, commit it, and enqueue it after the Skin A stylesheet:

```php
// nadlan-platform-child/functions.php
add_action('wp_enqueue_scripts', function () {
    $needs = is_singular('nadlan_property');
    if (!$needs && is_singular()) {
        $post  = get_post();
        $needs = $post && strpos((string) $post->post_content, 'class="nlx') !== false; // catalog block on a page
    }
    if (!$needs) {
        return;
    }
    $rel  = '/assets/css/nlx-prestige.css';
    $path = get_stylesheet_directory() . $rel;
    wp_enqueue_style('nlx-prestige', get_stylesheet_directory_uri() . $rel, array(), file_exists($path) ? (string) filemtime($path) : '1.0');
}, 30);
```

If Skin A registers a known handle, add it to the dependency array so the order is guaranteed. The stylesheet is scoped to `.nlx`, uses `!important` only where Skin A forces heading fonts and colors, and needs no JavaScript.

Tune two variables to the real header height (sticky price rail and anchor offsets):

```css
body.single-nadlan_property .nlx { --nlx-header-offset: 96px; } /* set to the fixed header height */
```

## 4. How the page content is stored

### 4A. Default: Custom HTML block in post content

`content-he.html` and `content-en.html` are ready for `post_content` (one `wp:html` block each). This requires the importing user to have `unfiltered_html` (section 2.5). After saving a draft, confirm nothing was stripped:

```bash
wp post get <ID> --field=post_content | grep -c 'type="radio"'        # tabs, expect 3 or more
wp post get <ID> --field=post_content | grep -c 'application/ld+json' # schema, expect 1
wp post get <ID> --field=post_content | wc -c                         # compare with the file size
```

### 4B. Fallback: render from meta if the editor or kses strips markup

Store the block in protected meta and render it from the child theme, so no editor or kses pass can touch it:

```php
// Save once per post (WP-CLI):
//   wp post meta update <ID> _nlx_block_html "$(cat listings/L10/block-he.html)"
add_filter('the_content', function ($content) {
    if (!is_singular('nadlan_property') || !in_the_loop() || !is_main_query()) {
        return $content;
    }
    $block = get_post_meta(get_the_ID(), '_nlx_block_html', true);
    return $block ? $block : $content; // trusted markup written by an administrator through WP-CLI
}, 20);
```

Leave `post_content` with a plain-text summary (the excerpt) so search and feeds still have text.

## 5. Theme integration checks

Open each draft preview at 390, 768 and 1280 px wide, in both languages, and resolve these:

1. **Duplicate headline.** The theme likely prints the post title as H1 and the block prints the same title in its masthead (H2). Recommended: keep the theme H1 for SEO and hide it visually on pages that carry the block.
   ```php
   add_filter('body_class', function ($classes) {
       if (is_singular('nadlan_property') && strpos((string) get_post()->post_content, 'class="nlx"') !== false) {
           $classes[] = 'has-nlx';
       }
       return $classes;
   });
   ```
   ```css
   .has-nlx .entry-title { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }
   ```
   Adjust the selector to the theme's real title element.
2. **Duplicate facts or price box.** If the template prints its own price box or fact table from meta, hide it under `.has-nlx`, or hide the block's rail with `.has-nlx .nlx-rail{display:none}`. Do not show two prices.
3. **Contact widgets.** The block has its own WhatsApp and call buttons (prefilled message naming the listing code) and a sticky mobile bar (`.nlx-mbar`). If the site adds a floating WhatsApp button, a cookie bar or a sticky footer, offset or suppress one of them on these pages.
4. **Width.** The block fills its container and caps itself at the content width. If the single template uses a narrow text column, give these pages the wide layout.
5. **Forced Skin A rules.** `.single-nadlan_property .entry-content h2/h3/p` rules must not override block typography; if they do, raise specificity inside the child theme rather than editing the block.
6. **RTL and LTR.** Every block sets its own `lang` and `dir`. The English page must render LTR even if the site shell stays RTL.

## 6. Create the drafts

Order: Hebrew first, then English, then link translations (section 7).

**Option A: REST importer (recommended).**

```bash
cd nadlan-meital-listings
python3 scripts/verify_package.py
export WP_URL=https://nad-lan.co.il WP_USER=<admin> WP_APP_PASSWORD='<set by Ben>'
python3 scripts/create_drafts.py --only L10 --lang he          # dry run: preflight report and payload summary
python3 scripts/create_drafts.py --only L10 --lang he --apply  # one draft, then inspect it in wp-admin
python3 scripts/create_drafts.py --only L01,L07,L08,L05,L04,L06,L02,L03,L10 --lang both --apply
```

The script refuses `--apply` if the user lacks `unfiltered_html`, drops meta keys the site does not register (and lists them), resolves `nadlan_city` terms by exact name, checks that tabs, SVG, details and JSON-LD survived the save, and writes `data/import-map.json` so a rerun with `--update` edits the same drafts. L09 and L11 stay out until Meital confirms them.

**Option B: WP-CLI.** Per page:

```bash
ID=$(wp post create listings/L10/content-he.html --post_type=nadlan_property --post_status=draft \
      --post_title="$(jq -r .title listings/L10/wp-he.json)" --post_name="$(jq -r .slug listings/L10/wp-he.json)" \
      --post_excerpt="$(jq -r .excerpt listings/L10/wp-he.json)" --porcelain)
jq -r '.meta | to_entries[] | select(.value != null) | "\(.key)\t\(.value)"' listings/L10/wp-he.json | \
  while IFS=$'\t' read -r k v; do wp post meta update "$ID" "$k" "$v"; done
wp post term set "$ID" nadlan_city <term-slug-from-preflight>
```

Booleans arrive as `true`/`false` strings this way; if the site stores `1`/`0` or `yes`/`no`, convert them first (check an existing post).

**Yoast fields** (either option), from `seo.json`:

```bash
wp post meta update "$ID" _yoast_wpseo_title    "$(jq -r .he.title listings/L10/seo.json)"
wp post meta update "$ID" _yoast_wpseo_metadesc "$(jq -r .he.metadesc listings/L10/seo.json)"
wp post meta update "$ID" _yoast_wpseo_focuskw  "$(jq -r .he.focus_keyphrase listings/L10/seo.json)"
```

If the site's title template appends the site name, store the title as `<title> %%sep%% %%sitename%%` to match other pages.

## 7. Translations and hreflang

The English page is a separate draft with its own slug (`en-...`). Link each pair (`translation_group` in `wp-*.json`):

- **Polylang:** `pll_set_post_language($he_id, 'he'); pll_set_post_language($en_id, 'en'); pll_save_post_translations(['he' => $he_id, 'en' => $en_id]);` Polylang then prints hreflang, and the `en-` prefix in the slug can be dropped if Polylang allows the same slug per language (ask Ben).
- **WPML:** set the language with `wpml_set_element_language_details` (element type `post_nadlan_property`), using the Hebrew post's `trid` for the English post.
- **TranslatePress or another string-translation layer:** there is no separate English post. Tell Ben before doing anything; the English block would need a language-conditional render (section 4B with `_nlx_block_html_en`).
- **None of these:** print hreflang yourself in `wp_head` for the pair, using the URLs in `seo.json`.

After the drafts exist, compare their real permalinks with `data/listings.json > url_pattern`. If they differ, set `URL_PATTERN` in `source/build/build.py`, rebuild (section 10) and update `post_content`, because the JSON-LD `url` and the catalog links use it.

## 8. Photos

Meital supplies the photos. `shotlist.md` in each listing folder gives the shot order, file names and alt text in both languages.

1. Upload to the media library with the listed file name and alt text (Hebrew alt on the Hebrew post's attachment; if attachments are shared across languages, use the Hebrew alt and put the English alt in the English post's gallery markup).
2. Shot 1 becomes the featured image (Yoast uses it for Open Graph).
3. Fill `photos_csv` in the format existing posts use.
4. Replace the drawing in the masthead. In the block, replace the whole `<figure class="nlx-plate ...">...</figure>` with:
   ```html
   <figure class="nlx-plate nlx-plate--photo"><img src="FEATURED_URL" alt="ALT" width="2400" height="1600" loading="eager" decoding="async"><span class="nlx-plate-name">PLATE NAME</span></figure>
   ```
   and remove the caption that says photos are still to come. The CSS for `.nlx-plate--photo` is already in the stylesheet.
5. Add an `image` array to the JSON-LD (`about.image`) with the uploaded URLs.
6. Do not use photos from other agencies' listings, and do not use AI-edited images. One cross-listing of L01 states that items were added to its photos with AI.

## 9. Before any page is published

Track each page in `data/pre-publish-checklist.csv`. A page is publishable only when every gate is done:

1. Meital approved the page text in writing, and every item under "לאשר מול מיטל" in `brief-he.md` has an answer.
2. Availability and price or rent re-confirmed within 7 days of publishing. L05's price was last posted in Nov 2025; L06, L09 and L11 may already be let.
3. Photos uploaded, masthead drawing replaced.
4. Ben approved the slug.
5. Visual check at 390, 768 and 1280 px in both languages; no duplicated title, price box or contact button.
6. JSON-LD passes Google's Rich Results Test and the Schema.org validator; `offers` price matches the page.
7. `python3 scripts/verify_package.py` passes on the regenerated files.
8. WhatsApp and call buttons open the right number (+972 52-363-1582) with the listing code in the message.
9. The disclaimer block and the sources list are present at the end of the page.

If a confirmation changes a fact, update `source/build/editorial/Lxx.json` (not the HTML) and rebuild.

## 10. Rebuilding after an edit

```bash
cd nadlan-meital-listings/source
pip install jinja2            # the only dependency
python3 build/build.py         # renders dist/blocks/Lxx/{he,en}.html, stops on any long dash
python3 build/package.py       # regenerates source/dist/nadlan-meital-listings/ (payloads, SEO, briefs, catalog, data)
python3 build/preview.py       # regenerates the preview
```

`build/constants.json` holds the dated economics used across pages (purchase tax brackets, Bank of Israel LTV limits, BOI rate, exchange rates of 15 Sep 2026, Tel Aviv and Herzliya arnona rates, Fair Rental thresholds). Update it when those change and rebuild every page.

Editorial fields worth knowing: `facts`, `spec`, `building` (rows with `basis` broker or calc and `src` source IDs), `numbers` (`tabs` for rentals, `scenarios` for a sale without a price, `bars`, `ledger`), `market` (`stats`, `sale_exclude`, `rent_exclude`, `where_override`, `stats_override`, `date_override`), `questions` (indices into the dossier), `faq`, `seo`, `wp`, `internal` (never rendered). Text tokens like `[[S12,G_LTV]]` become numbered footnotes; IDs resolve against the listing dossier, then `constants.json`.

## 11. Report back to Ben

In Hebrew, short: what was installed and where (file paths, commit), draft IDs and preview links per page, meta keys that were dropped or mapped, anything stripped on save, template elements you hid, and the open publishing gates per page. Include the broker page drafts from section 12. Do not publish.

## 12. Broker profile page (Meital Katzir)

A WordPress **page** (not the listing post type) in Hebrew and English. Same ground rules: drafts only, slugs are proposals.

1. **Stylesheet.** Install `broker/nlb-broker.css` the same way as section 3 (child theme enqueue preferred), loaded only on these two pages if the theme allows conditional enqueues. Everything is scoped to `.nlb`.
2. **Fonts.** The page uses Assistant 300 to 800 and Noto Serif Hebrew 300 to 500; the English page also uses Noto Serif Display 400 and italic 300. Add any missing weights to the existing Google Fonts request rather than a second request.
3. **Template.** Use a full-width template with no sidebar and no theme page title (the hero carries the H1). Check that the theme header does not overlap the hero and that no theme sticky element covers the mobile WhatsApp bar (`.nlb-mbar`, shown at 720 px and below).
4. **Parent page.** Proposed URLs are `/brokers/meital-katzir/` and `/en/brokers/meital-katzir/`. If a `brokers` page does not exist, do not create one on your own: the script leaves the page top-level and reports it; ask Ben.
5. **Create the drafts.**
   ```bash
   python3 scripts/create_drafts.py --broker --lang he            # dry run
   python3 scripts/create_drafts.py --broker --lang both --apply  # create both drafts
   ```
   The script requires `unfiltered_html` (the deal filter uses radio inputs and the page has inline SVG) and warns if markup was stripped on save.
6. **SEO and schema.** Set the Yoast title, description and focus keyphrase from `broker/seo-broker.json`. Add `schema-broker-{lang}.jsonld` as JSON-LD through the theme or Yoast schema API (it is not inline in the block). Link the two languages as translations (section 7).
7. **Photos.** Until Meital's photos arrive the page shows illustrations that depict no real property. When photos are in the media library, create `source/build/broker/images.json` with local paths or URLs for `hero`, `L01` to `L11` and an optional `gallery` list of `[path, caption]`, then rebuild (`python3 build/broker/build_broker.py` and `python3 build/package.py`). A gallery section appears automatically when `gallery` is set. AI images are allowed only as atmosphere (sky, sea, texture) and never on a listing card; see `broker/AI-IMAGE-PROMPTS-HE.md`.
8. **Card data.** `broker/cards.json` is the single source for the cards (price, price per sqm, specs, highlights, amenities, entry, last update, review flag). L09 and L11 carry the "availability being confirmed" badge until Meital confirms them; set `review` to false only after she does.
9. **Before publishing:** Meital approves the page text and the business card in writing; every listing link on the page points to a published listing (or the card links are removed); prices re-checked within 7 days; visual check at 390, 768, 1024 and 1440 px in both languages; WhatsApp, call and Instagram links tested; `python3 scripts/verify_package.py` passes.
10. **Design reference.** The Claude Design canvas (link in `broker/claude-design-canvas/README.md`) is the visual reference for this page, including the listing card states, the business card and a 1080x1350 share image.
