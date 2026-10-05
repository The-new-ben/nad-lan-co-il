# -*- coding: utf-8 -*-
"""Builds the cy-prus.co.il plugin `cy-project-experience`: the plan journey mounted on ONE Cyprus Atlas project page.
Usage: python cyprus/local/build_plugin.py --register <private register> --media-dir <web-media folder> --place-id <atlas id> --out <folder>
The atlas page keeps its own h1, description, facts, map, nearby list and WhatsApp card; this module mounts right after
`.atlas-facts`, follows the page language (html lang he* = Hebrew, anything else English), uses the site's brand tokens,
and sends the chosen home to the page's own WhatsApp link. No brand or developer name may appear in any built file."""
import argparse, hashlib, io, json, os, re, shutil, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from serve import project_packet  # noqa: E402
from build_embed import read, rep, ids_of, prefix_ids, scope_css  # noqa: E402
sys.path.insert(0, os.path.join(HERE, 'advertise'))
import plugin_parts  # noqa: E402  (the "Advertise with us" page, button and assets)

SLUG = 'cy-project-experience'
VERSION = '1.5.0'
BUNDLE = 'villas-aa'
IMAGES = {  # local web-media name -> published name, and the plan-data key it replaces
    'agios-athanasios-villas-site-plan.webp': ('site-plan.webp', '/media/site.png'),
    'villas-type-a-ground-floor.webp': ('type-a-ground.webp', '/media/a-ground.png'),
    'villas-type-a-upper-floor.webp': ('type-a-upper.webp', '/media/a-upper.png'),
    'villas-type-b-ground-floor.webp': ('type-b-ground.webp', '/media/b-ground.png'),
    'villas-type-b-upper-floor.webp': ('type-b-upper.webp', '/media/b-upper.png'),
    'villas-street-view-visual.webp': ('street-view.webp', '/media/architect-exterior.jpg'),
}
# The local palette -> the site's brand tokens (brand.css: navy, stone cream, sea teal, terracotta; no gold).
COLOURS = [('#c3a3745c', '#B85C3852'), ('#c3a37433', '#B85C3829'), ('#c3a374', 'var(--cy-terracotta,#B85C38)'),
           ('#8c5f2c', 'var(--cy-terracotta,#B85C38)'), ('#7a4f20', '#8E4426'), ('#af783d', 'var(--cy-teal,#178076)'),
           ('#f1e7d6', '#F6E9E1'), ('#23392f55', '#12293E55'), ('#23392f00', '#12293E00'), ('#23392f23', '#12293E23'),
           ('#23392f', 'var(--cy-navy,#12293E)'), ('#eeece4', 'var(--cy-cream,#F4EFE6)'), ('#e4e2d8', '#ECE5D8'),
           ('#efede5', '#F6F1E8'), ('#a8ada0', '#C9BFAD'), ('#bbc1b3', '#D5CCBB'), ('#fbfaf6', 'var(--cy-surface,#FBF8F2)'),
           ('#15261ed9', '#0C1C2Bd9'), ('#f5f2ebb8', '#FBF8F2c4'), ('#f5f2eb', 'var(--cy-surface,#FBF8F2)'), ('#636b60', 'var(--cy-muted,#5A6B76)')]

# The area section and the long-form article are printed by the server (search engines read them without JavaScript).
# The area section goes in before the page's map, the article before the page's own WhatsApp card; each falls back to the
# next marker and then to </main>. Markers are matched by class token, so attribute order does not matter; if none is
# found, the page is left exactly as it was.
ARTICLE_PHP = r"""
/* ------------------------------------------------------- the projects of an area (area pages), from the atlas itself */

/**
 * Point in polygon (ring of [lon, lat]).
 *
 * @param float $x   Longitude.
 * @param float $y   Latitude.
 * @param array $ring Outer ring.
 * @return bool
 */
function cypx_in_ring( $x, $y, $ring ) {
	$in = false;
	$n  = count( $ring );
	for ( $i = 0, $j = $n - 1; $i < $n; $j = $i++ ) {
		$xi = (float) $ring[ $i ][0];
		$yi = (float) $ring[ $i ][1];
		$xj = (float) $ring[ $j ][0];
		$yj = (float) $ring[ $j ][1];
		$dy = $yj - $yi;
		if ( ( $yi > $y ) !== ( $yj > $y ) && $x < ( $xj - $xi ) * ( $y - $yi ) / ( 0.0 == $dy ? 1e-12 : $dy ) + $xi ) { // phpcs:ignore Universal.Operators.StrictComparisons
			$in = ! $in;
		}
	}
	return $in;
}

/**
 * The atlas project records inside the area boundary, as a list section (cached for an hour). '' when none or on error.
 *
 * @param array  $cfg  bbox [minLon, minLat, maxLon, maxLat], ring, text[he|en][eyebrow|title|lead].
 * @param string $lang he|en.
 * @return string
 */
function cypx_area_projects_html( $cfg, $lang ) {
	if ( ! function_exists( 'rest_do_request' ) || empty( $cfg['bbox'] ) || empty( $cfg['ring'] ) || empty( $cfg['text'][ $lang ] ) ) {
		return '';
	}
	$key   = 'cypx_ap_' . md5( wp_json_encode( $cfg['bbox'] ) . '|' . $lang . '|' . CYPX_VERSION );
	$items = get_transient( $key );
	if ( ! is_array( $items ) ) {
		$items  = array();
		$params = array( 'kind' => 'project', 'bbox' => implode( ',', array_map( 'floatval', $cfg['bbox'] ) ), 'limit' => 200 );
		if ( 'en' === $lang ) {
			$params['lang'] = 'en';
		}
		$req = new WP_REST_Request( 'GET', '/cyprus-atlas/v1/places' );
		$req->set_query_params( $params );
		$res = rest_do_request( $req );
		if ( $res->is_error() ) {
			return '';
		}
		$data = $res->get_data();
		foreach ( ( isset( $data['features'] ) && is_array( $data['features'] ) ) ? $data['features'] : array() as $f ) {
			$c = isset( $f['geometry']['coordinates'] ) ? $f['geometry']['coordinates'] : null;
			$p = isset( $f['properties'] ) ? $f['properties'] : array();
			if ( ! is_array( $c ) || count( $c ) < 2 || empty( $p['url'] ) || empty( $p['name'] ) || ! cypx_in_ring( (float) $c[0], (float) $c[1], $cfg['ring'] ) ) {
				continue;
			}
			$items[] = array(
				'name'  => (string) $p['name'],
				'url'   => (string) $p['url'],
				'stage' => isset( $p['stage'] ) ? (string) $p['stage'] : '',
				'slug'  => isset( $p['slug'] ) ? (string) $p['slug'] : '',
			);
		}
		set_transient( $key, $items, HOUR_IN_SECONDS );
	}
	if ( empty( $items ) ) {
		return '';
	}
	// pages with a full project experience first, then the atlas order
	$rich = cypx_bundles();
	usort(
		$items,
		function ( $a, $b ) use ( $rich ) {
			return (int) empty( $rich[ $a['slug'] ] ) - (int) empty( $rich[ $b['slug'] ] );
		}
	);
	$t   = $cfg['text'][ $lang ];
	$out = '<section class="cyx-projects" lang="' . esc_attr( $lang ) . '" dir="' . ( 'he' === $lang ? 'rtl' : 'ltr' ) . '" aria-labelledby="cyx-projects-h">'
		. '<p class="cyx-area-eyebrow">' . esc_html( $t['eyebrow'] ) . '</p><h2 id="cyx-projects-h">' . esc_html( $t['title'] ) . '</h2>'
		. '<p class="cyx-area-lead">' . esc_html( $t['lead'] ) . '</p><ul class="cyx-projects-list">';
	foreach ( $items as $it ) {
		$url  = 'en' === $lang ? add_query_arg( 'lang', 'en', $it['url'] ) : $it['url'];
		$out .= '<li><a href="' . esc_url( $url ) . '"><span class="cyx-projects-name">' . esc_html( $it['name'] ) . '</span>'
			. ( '' !== $it['stage'] ? '<span class="cyx-projects-stage">' . esc_html( $it['stage'] ) . '</span>' : '' ) . '</a></li>';
	}
	return $out . '</ul></section>' . "\n";
}

/* ------------------------------------------------------- the area section and the long-form article on mapped project pages */

add_action(
	'template_redirect',
	function () {
		$bundle = cypx_bundle();
		if ( '' === $bundle ) {
			return;
		}
		$dir   = plugin_dir_path( __FILE__ ) . 'assets/' . $bundle . '/';
		$lang  = cypx_lang();
		$map   = '/<div\b[^>]*\bclass="[^"]*\batlas-map-wrap\b/';
		$wa    = '/<div\b[^>]*\bclass="[^"]*\batlas-wa-wrap\b/';
		$main  = '/<\/main>/';
		$parts = array();
		if ( file_exists( $dir . 'projects-list.json' ) ) {
			$cfg  = json_decode( (string) file_get_contents( $dir . 'projects-list.json' ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions
			$list = is_array( $cfg ) ? cypx_area_projects_html( $cfg, $lang ) : '';
			if ( '' !== $list ) {
				$parts[] = array( $list, array( $map, $wa, $main ) );
			}
		}
		foreach ( array( 'area-' . $lang . '.html' => array( $map, $wa, $main ), 'article-' . $lang . '.html' => array( $wa, $main ) ) as $file => $markers ) {
			if ( file_exists( $dir . $file ) ) {
				$parts[] = array( (string) file_get_contents( $dir . $file ), $markers ); // phpcs:ignore WordPress.WP.AlternativeFunctions
			}
		}
		if ( empty( $parts ) ) {
			return;
		}
		ob_start(
			function ( $html ) use ( $parts ) {
				foreach ( $parts as $part ) {
					foreach ( $part[1] as $marker ) {
						if ( preg_match( $marker, $html, $m, PREG_OFFSET_CAPTURE ) ) {
							$at   = $m[0][1];
							$html = substr( $html, 0, $at ) . $part[0] . substr( $html, $at );
							break;
						}
					}
				}
				return $html;
			}
		);
	},
	5 // before the atlas route (template_redirect, 10) includes its template and exits
);
"""
ARTICLE_CSS = (
    '.cyx-article{max-width:780px;margin:44px auto 36px;color:var(--cy-ink,#1B2833);font-family:var(--cy-font-body,"Assistant"),Arial,sans-serif;font-size:17.5px;line-height:1.85}'
    '.cyx-article h2{font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif;color:var(--cy-navy,#12293E);font-size:clamp(24px,3vw,31px);line-height:1.3;margin:44px 0 14px}'
    '.cyx-article h2:first-child{margin-top:0;padding-top:28px;border-top:1px solid var(--cy-line,#E3DCCE)}'
    '.cyx-article h3{font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif;color:var(--cy-navy,#12293E);font-size:21px;line-height:1.35;margin:30px 0 10px}'
    '.cyx-article p{margin:0 0 16px}.cyx-article ol{margin:0 0 18px;padding-inline-start:1.4em}.cyx-article li{margin-bottom:10px}'
    'body .cyx-article a{color:var(--cy-teal,#178076);text-decoration:underline;text-underline-offset:4px}body .cyx-article a:hover{color:var(--cy-terracotta,#B85C38)}'
    '.cyx-table{overflow-x:auto;margin:18px 0 26px;border:1px solid var(--cy-line,#E3DCCE);border-radius:6px}'
    '.cyx-table table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.5}.cyx-table--wide table{min-width:620px}'
    '.cyx-table th{background:var(--cy-cream,#F4EFE6);color:var(--cy-navy,#12293E);text-align:start;padding:10px 12px;font-weight:700}'
    '.cyx-table td{padding:9px 12px;border-top:1px solid var(--cy-line,#E3DCCE);vertical-align:top}'
    '@media(max-width:600px){.cyx-article{font-size:16.5px;margin-top:32px}.cyx-table table{font-size:14px}}'
)

PROJECTS_CSS = (
    '.cyx-projects{margin:36px 0 8px;color:var(--cy-ink,#1B2833);font-family:var(--cy-font-body,"Assistant"),Arial,sans-serif}'
    'body .cyx-projects h2{font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif;color:var(--cy-navy,#12293E);font-size:clamp(24px,3vw,31px);line-height:1.25;margin:4px 0 10px}'
    '.cyx-projects-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}'
    'body .cyx-projects-list a{display:flex;flex-direction:column;gap:6px;height:100%;box-sizing:border-box;padding:14px 16px;background:#fff;'
    'border:1px solid var(--cy-line,#E3DCCE);border-radius:6px;text-decoration:none;color:var(--cy-navy,#12293E)}'
    'body .cyx-projects-list a:hover{border-color:var(--cy-teal,#178076)}'
    '.cyx-projects-name{font-weight:700;font-size:17px;line-height:1.35}'
    '.cyx-projects-stage{align-self:flex-start;padding:2px 9px;border-radius:12px;background:#E3F1EE;color:var(--cy-teal,#178076);font-size:13px;font-weight:700}'
    '@media(max-width:700px){.cyx-projects-list{grid-template-columns:1fr}}'
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--register', required=True)
    ap.add_argument('--media-dir', required=True)
    ap.add_argument('--place-slug', required=True, help='the atlas slug of the project page, e.g. semi-detached-villas')
    ap.add_argument('--out', required=True, help='folder that receives the plugin folder and the zip')
    ap.add_argument('--articles-dir', help='folder with article-he.md / article-en.md (the long-form body, rendered server-side)')
    ap.add_argument('--world-dir', help='the walkable 3D area folder (cyprus/local/world3d); adds the 3D card and full-screen tour')
    ap.add_argument('--area-project', action='append', default=[], metavar='SLUG=DIR',
                    help='another mapped project page that gets only the "what is close" section (atlas slug = its private area folder)')
    ap.add_argument('--with-advertise', action='store_true',
                    help='also ship the old "Advertise with us" page and button; OFF: since 4.10.2026 they live in the separate cyprus-advertisers plugin')
    ap.add_argument('--area-dir', help='the private area folder of the project (places.geojson + drive-osrm.json + area-spec.json); adds the server-rendered "what is close" section')
    a = ap.parse_args()
    extras = []  # (atlas slug, bundle folder, area folder) of the area-only project pages
    for spec in a.area_project:
        slug, _, adir = spec.partition('=')
        if not re.fullmatch(r'[a-z0-9-]+|id:[0-9]+', slug) or not os.path.isdir(adir):
            raise SystemExit(f'build_plugin: bad --area-project {spec!r}')
        extras.append((slug, 'p-' + slug.replace(':', '-')[:40], adir))
    bundles_php = ', '.join(f"'{sl}' => '{bd}'" for sl, bd in [(a.place_slug, BUNDLE)] + [(e[0], e[1]) for e in extras])
    packet = project_packet(__import__('pathlib').Path(a.register))
    for k in ('name', 'district', 'languages', 'contactEnabled', 'geometryMode', 'availabilityMode'):
        packet.pop(k, None)

    # ---------- markup: the local page minus its chrome and intro (the atlas page owns h1, description and contact) ----------
    html = read('index.html')
    body = html[html.index('<figure class="architecture">'):html.index('<footer>')]
    dialogs = html[html.index('<dialog id="conversation"'):html.index('<p class="load-error"')]
    dialogs = rep(dialogs, '<button class="primary" id="copy" data-t="copy"></button><p class="small" data-t="noSend"></p>',
                  '<a class="primary cyx-wa-send" id="wa-send" target="_blank" rel="noopener" data-t="sendWa"></a>'
                  '<button class="secondary" id="copy" data-t="copy"></button>')
    markup = body + dialogs + '<div class="toast" role="status" id="toast"></div>'
    markup = rep(markup, 'src="/media/architect-exterior.jpg"', 'src="__A__street-view.webp" loading="lazy" decoding="async"')
    ids = ids_of(markup)
    markup = prefix_ids(markup, ids)

    # ---------- data ----------
    plans = read('plan-data.js')
    plans = '\n'.join(l for l in plans.splitlines() if not l.startswith('//') and l.strip() != "'use strict';")
    plans = rep(plans, 'const DUNE_PLANS = ', 'const PLANS = ')
    for src, (dst, key) in IMAGES.items():
        if key in plans:
            plans = rep(plans, f"'{key}'", f"A+'{dst}'")

    # ---------- behaviour ----------
    js = read('app.js').replace("'use strict';\n", '', 1)
    js = rep(js, 'DUNE_PLANS', 'PLANS', n=js.count('DUNE_PLANS'))
    js, k = re.subn(r"exteriorAlt:'[^']*'", "exteriorAlt:''", js)
    if k != 2:
        raise SystemExit(f'exteriorAlt x{k}')
    js = rep(js, "const q=new URLSearchParams(location.search);\nlet data,lang=q.get('lang')==='en'?'en':'he',",
             "const q=new URLSearchParams(location.search);\n"
             "let data,lang=(document.documentElement.lang||'he').toLowerCase().startsWith('he')?'he':'en',")
    js = rep(js, 'const $=s=>document.querySelector(s)', "const $=s=>root.querySelector(s.replace(/#([a-z])/g,'#cyx-$1'))")
    js = rep(js, 'document.querySelectorAll(', 'root.querySelectorAll(', n=4)
    js = rep(js, 'document.documentElement.lang=lang;document.documentElement.dir=LOCALES[lang].dir;', 'root.lang=lang;root.dir=LOCALES[lang].dir;')
    js = rep(js, "$('#district').textContent=data.district;", '')
    js = rep(js, "from?.closest('#site-canvas')", "from?.closest('#cyx-site-canvas')")
    js = rep(js, "event.target.closest('#plan-canvas')", "event.target.closest('#cyx-plan-canvas')")
    js = rep(js, "document.addEventListener('click',", "root.addEventListener('click',")
    js = rep(js, "document.addEventListener('keydown',", "root.addEventListener('keydown',")
    js = rep(js, " if(b.dataset.lang){lang=b.dataset.lang;render();}\n", '')
    js = rep(js, "url.searchParams.set('lang',lang);", '')
    js = rep(js, "$('#brief').value=[data.name,u.id,", "$('#brief').value=[CFG.title,u.id,")
    js = rep(js, "$('#conversation').showModal();};",
             "$('#wa-send').href=waLink(t('waAsk')+'\\n'+$('#brief').value);$('#conversation').showModal();};")
    js = rep(js, "function toast(msg){",
             "function waLink(text){return 'https://wa.me/'+CFG.wa+'?text='+encodeURIComponent(t('waHello')+'\\n'+text+'\\n'+location.origin+location.pathname+(lang==='en'?'?lang=en&':'?')+'unit='+selected);}\nfunction toast(msg){")
    js = rep(js, "fetch('/api/project').then(r=>{if(!r.ok)throw Error('Local source unavailable');return r.json()}).then(packet=>{data=packet;",
             "Promise.resolve(CFG.packet).then(packet=>{data=packet;")
    js = rep(js, ".catch(()=>{['#residences','#plans','#compare'].forEach(s=>$(s).hidden=true);$('#load-error').textContent=t('loadError');$('#load-error').hidden=false;});",
             ".catch(()=>{root.hidden=true;});")
    copy = {
        'he': {'prepare': 'לקבלת פרטים נוספים בוואטסאפ', 'prepareBody': 'אלה פרטי הבית שבחרתם. שלחו אותם בוואטסאפ ונחזור אליכם, מענה בעברית.',
               'sendWa': 'שליחה בוואטסאפ', 'waHello': 'שלום, הגעתי מהאתר CY-PRUS.', 'waAsk': 'אשמח לפרטים על הבית הזה:',
               'exteriorAlt': 'הדמיה: שני זוגות בתים לבנים בני שתי קומות עם מסגרות עץ, מבט מהרחוב',
               'exteriorNote': 'הדמיה של שני זוגות הבתים מהרחוב.', 'areaNote': 'השטחים לפי מפרט הפרויקט.'},
        'en': {'prepare': 'Get more details on WhatsApp', 'prepareBody': 'These are the details of the home you chose. Send them on WhatsApp and we will get back to you.',
               'sendWa': 'Send on WhatsApp', 'waHello': 'Hello, I came from the CY-PRUS website.', 'waAsk': 'I would like details about this home:',
               'exteriorAlt': 'Visual: two pairs of white two-storey homes with timber frames, seen from the street',
               'exteriorNote': 'Visual of both pairs of homes from the street.', 'areaNote': 'Areas from the project specification.'}}
    js = rep(js, 'const AREAS=', 'for(const l of ["he","en"])Object.assign(COPY[l],' + json.dumps(copy, ensure_ascii=False) + '[l]);\nconst AREAS=')
    head = ("const host=document.querySelector('#atlas-main .atlas-facts')||document.querySelector('#atlas-main .atlas-map-wrap');\n"
            "if(!host||document.getElementById('cyx'))return;\n"
            "const A=(window.CYPX&&window.CYPX.assets)||'';\n"
            "const root=document.createElement('section');root.className='cyx';root.id='cyx';\n"
            "root.innerHTML=" + json.dumps(markup, ensure_ascii=False) + ".replace(/__A__/g,A);\n"
            "if(host.classList.contains('atlas-facts'))host.after(root);else host.before(root);\n"
            "const wa=(document.querySelector('a.atlas-wa')||{}).href||'';\n"
            "const CFG={wa:(wa.match(/wa\\.me\\/(\\d+)/)||[])[1]||'972525101555',title:((document.querySelector('#atlas-main h1')||{}).textContent||'').trim(),packet:"
            + json.dumps(packet, ensure_ascii=False) + "};\n")
    script = "(function(){'use strict';\n" + head + plans + '\n' + js + '\n/*W3*/\n})();\n'

    # ---------- style ----------
    css = scope_css(read('style.css'), ids)
    # placeholders first, so a replacement never re-matches its own output
    css = css.replace('Arial,"Segoe UI",sans-serif', '@@BODY@@').replace('Arial,sans-serif', '@@BODY@@').replace('Georgia,serif', '@@DISPLAY@@')
    css = re.sub(r'(?<![a-zA-Z0-9_-])Arial(?![a-zA-Z0-9_-])', '@@BODY@@', css)
    css = re.sub(r'(?<![a-zA-Z0-9_-])Georgia(?![a-zA-Z0-9_-])', '@@DISPLAY@@', css)
    css = css.replace('@@BODY@@', 'var(--cy-font-body,"Assistant"),Arial,sans-serif').replace('@@DISPLAY@@', 'var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif')
    for old, new in COLOURS:
        css = css.replace(old, new)
    css += ('.cyx{--paper:var(--cy-surface,#FBF8F2);--ink:var(--cy-navy,#12293E);--muted:var(--cy-muted,#5A6B76);--line:var(--cy-line,#E3DCCE);'
            '--accent:var(--cy-terracotta,#B85C38);--cream:var(--cy-cream,#F4EFE6);max-width:none;margin:32px 0 36px;padding:0;background:none;'
            'color:var(--cy-ink,#1B2833);font-family:var(--cy-font-body,"Assistant"),Arial,sans-serif;box-sizing:border-box}'
            '.cyx h2,.cyx h3{font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif;color:var(--cy-navy,#12293E);letter-spacing:normal;text-transform:none;line-height:1.25}'
            '.cyx button{font-family:inherit;letter-spacing:normal;text-transform:none;border-radius:0;box-shadow:none}'
            '.cyx figure{margin:0}.cyx img{max-width:100%}.cyx .architecture img{border-radius:2px}'
            '.cyx .explorer{background:var(--cy-surface,#FBF8F2);border:1px solid var(--cy-line,#E3DCCE);padding-inline:20px}'
            '.cyx .cyx-wa-send{display:flex;justify-content:center;align-items:center;text-decoration:none;min-height:48px;background:var(--cy-teal,#178076);color:#fff!important;border:0}'
            '.cyx[lang=he] .eyebrow{letter-spacing:.5px}'
            '@media(max-width:600px){.cyx .explorer{padding-inline:14px}}') + ARTICLE_CSS

    # ---------- PHP ----------
    php = f"""<?php
/**
 * Plugin Name: CY Project Experience
 * Description: Interactive site plan, floor plans and home comparison, the "what is close" section, the 3D area tour and long-form guides on selected Cyprus Atlas project pages (loaded only there).
 * Version: {VERSION}
 * Requires at least: 6.5
 * Requires PHP: 7.4
 * Author: CY-PRUS
 * License: Proprietary
 */

if ( ! defined( 'ABSPATH' ) ) {{
	exit;
}}

define( 'CYPX_VERSION', '{VERSION}' );

/**
 * Hebrew by default; English for ?lang=en and the site's other non-Hebrew languages.
 *
 * @return string he|en
 */
function cypx_lang() {{
	$l = isset( $_GET['lang'] ) ? sanitize_key( wp_unslash( $_GET['lang'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification
	return ( '' === $l || 'he' === $l ) ? 'he' : 'en';
}}

/**
 * Atlas slug (known before import) or "id:<atlas id>" (for an existing page, e.g. an area) => bundle folder under assets/.
 *
 * @return array<string,string>
 */
function cypx_bundles() {{
	return array( {bundles_php} );
}}

/**
 * The bundle folder of the current atlas place page: by its id ("id:256") first, then by its slug; '' if none.
 *
 * @return string
 */
function cypx_bundle() {{
	if ( 'place' !== get_query_var( 'ca_view' ) ) {{
		return '';
	}}
	$bundles = cypx_bundles();
	$id      = absint( get_query_var( 'ca_id' ) );
	if ( $id && ! empty( $bundles[ 'id:' . $id ] ) ) {{
		return $bundles[ 'id:' . $id ];
	}}
	$slug = sanitize_title( (string) get_query_var( 'ca_slug' ) );
	return ( '' !== $slug && ! empty( $bundles[ $slug ] ) ) ? $bundles[ $slug ] : '';
}}

add_action(
	'wp_enqueue_scripts',
	function () {{
		$bundle = cypx_bundle();
		if ( '' === $bundle ) {{
			return;
		}}
		$dir  = 'assets/' . $bundle . '/';
		$path = plugin_dir_path( __FILE__ ) . $dir;
		$url  = plugin_dir_url( __FILE__ ) . $dir;
		if ( ! file_exists( $path . 'app.js' ) || ! file_exists( $path . 'app.css' ) ) {{
			return;
		}}
		$ver    = CYPX_VERSION . '-' . substr( md5( (string) filemtime( $path . 'app.js' ) . (string) filemtime( $path . 'app.css' ) ), 0, 8 );
		$handle = 'cypx-' . $bundle;
		wp_enqueue_style( $handle, $url . 'app.css', array(), $ver );
		wp_enqueue_script( $handle, $url . 'app.js', array(), $ver, array( 'in_footer' => true, 'strategy' => 'defer' ) );
		wp_add_inline_script( $handle, 'window.CYPX=' . wp_json_encode( array( 'assets' => $url ) ) . ';', 'before' );
	}}
);
"""
    php += ARTICLE_PHP + (plugin_parts.adv_php() if a.with_advertise else '') + plugin_parts.viewport_php()
    # ---------- write the plugin folder + zip ----------
    root_dir = os.path.join(a.out, SLUG)
    if os.path.isdir(root_dir):
        shutil.rmtree(root_dir)
    bdir = os.path.join(root_dir, 'assets', BUNDLE)
    os.makedirs(bdir)
    io.open(os.path.join(root_dir, SLUG + '.php'), 'w', encoding='utf-8', newline='\n').write(php)
    if a.world_dir:
        import world_embed
        launcher, card_css = world_embed.pack(a.world_dir, bdir)
        script, css = script.replace('/*W3*/', launcher), css + card_css
    else:
        script = script.replace('/*W3*/', '')
    io.open(os.path.join(bdir, 'app.js'), 'w', encoding='utf-8', newline='\n').write(script)
    io.open(os.path.join(bdir, 'app.css'), 'w', encoding='utf-8', newline='\n').write(css)
    for src, (dst, _) in IMAGES.items():
        shutil.copyfile(os.path.join(a.media_dir, src), os.path.join(bdir, dst))
    if a.with_advertise:
        plugin_parts.write_assets(root_dir, HERE)
    if a.area_dir:
        import area_html
        for lang, frag in area_html.build(os.path.join(a.area_dir, 'places.geojson'), os.path.join(a.area_dir, 'drive-osrm.json'),
                                          os.path.join(a.area_dir, 'area-spec.json')).items():
            io.open(os.path.join(bdir, f'area-{lang}.html'), 'w', encoding='utf-8', newline='\n').write(frag)
        css += area_html.AREA_CSS
        io.open(os.path.join(bdir, 'app.css'), 'w', encoding='utf-8', newline='\n').write(css)
        end = script.rindex('})();')
        script = script[:end] + area_html.AREA_JS + script[end:]
        io.open(os.path.join(bdir, 'app.js'), 'w', encoding='utf-8', newline='\n').write(script)
    for slug, bname, adir in extras:  # area-only bundles: the section, its style and the phone fold
        import area_html
        edir = os.path.join(root_dir, 'assets', bname)
        os.makedirs(edir)
        for lang, frag in area_html.build(os.path.join(adir, 'places.geojson'), os.path.join(adir, 'drive-osrm.json'),
                                          os.path.join(adir, 'area-spec.json')).items():
            io.open(os.path.join(edir, f'area-{lang}.html'), 'w', encoding='utf-8', newline='\n').write(frag)
        ecss, ejs = area_html.AREA_CSS, area_html.AREA_JS
        if os.path.exists(os.path.join(adir, 'projects-list.json')):  # an area page: the atlas projects inside its boundary
            shutil.copyfile(os.path.join(adir, 'projects-list.json'), os.path.join(edir, 'projects-list.json'))
            ecss += PROJECTS_CSS
        if a.world_dir and os.path.isdir(os.path.join(adir, 'world')):  # its own 3D world: the card after the facts, the tour on request
            import world_embed
            launcher, card_css = world_embed.pack(a.world_dir, edir, os.path.join(adir, 'world'))
            ecss += card_css
            ejs = ("\nconst A=(window.CYPX&&window.CYPX.assets)||'';\n"
                   "const lang=(document.documentElement.lang||'he').toLowerCase().startsWith('he')?'he':'en';\n"
                   "const root=document.querySelector('#atlas-main .atlas-facts');\n"
                   "if(root){" + launcher + "}\n") + ejs
        io.open(os.path.join(edir, 'app.css'), 'w', encoding='utf-8', newline='\n').write(ecss)
        io.open(os.path.join(edir, 'app.js'), 'w', encoding='utf-8', newline='\n').write("(function(){'use strict';" + ejs + "})();\n")
    if a.articles_dir:
        from article_html import to_html
        labels = {'he': ('rtl', 'מדריך מלא: וילות למכירה באגיוס אתנסיוס'), 'en': ('ltr', 'Full guide: villas for sale in Agios Athanasios')}
        for lang, (d, label) in labels.items():
            src = os.path.join(a.articles_dir, f'article-{lang}.md')
            if os.path.exists(src):
                body = to_html(io.open(src, encoding='utf-8').read())
                io.open(os.path.join(bdir, f'article-{lang}.html'), 'w', encoding='utf-8', newline='\n').write(
                    f'<section class="cyx-article" lang="{lang}" dir="{d}" aria-label="{label}">\n{body}\n</section>\n')
    for dirpath, _, files in os.walk(root_dir):
        for f in files:
            p = os.path.join(dirpath, f)
            low = (f + (io.open(p, encoding='utf-8').read() if f.endswith(('.php', '.js', '.css', '.html')) else '')).lower()
            for banned in ('dune', 'mansions', '/media/', '127.0.0.1', 'localhost', 'units-source-register', 'brochureid', 'coveredaream2'):
                if banned in low:
                    raise SystemExit(f'build_plugin: banned text "{banned}" in {p}')
    zpath = os.path.join(a.out, f'{SLUG}-{VERSION}.zip')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for dirpath, _, files in os.walk(root_dir):
            for f in sorted(files):
                p = os.path.join(dirpath, f)
                z.write(p, os.path.relpath(p, a.out).replace(os.sep, '/'))
    print(f'wrote {zpath} ({os.path.getsize(zpath)} bytes); app.js {len(script.encode())} B, app.css {len(css.encode())} B; sha256 '
          + hashlib.sha256(open(zpath, 'rb').read()).hexdigest()[:16])


if __name__ == '__main__':
    main()
