<?php
/**
 * Photorealistic Earth experience.
 *
 * Google's Photorealistic 3D Tiles rendered through CesiumJS, with our own
 * projects planted on top as clickable pins and every surrounding building
 * clickable for its own detail.
 *
 * Why CesiumJS and not the three.js pilot that already exists on the
 * somail branch: that pilot draws tiles and nothing else. The brief is to
 * click OUR project and also click anything around it. Cesium ships entity
 * picking and OSM Buildings (350M buildings carrying name, address, height,
 * opening hours) out of the box, so the surroundings become clickable without
 * us building a POI database. The three.js pilot stays on its branch.
 *
 * PINS ARE DOM, NOT CESIUM LABELS. Cesium's Label primitive lays glyphs out
 * left to right with no bidi shaping, so every Hebrew project name rendered
 * reversed (same bug class as Pillow in the plate stamping). The browser is
 * the only bidi engine we trust, so pins live in an HTML overlay projected
 * onto the scene every frame. That also buys hover cards and CSS instead of
 * canvas text.
 *
 * COST. Photorealistic 3D Tiles is an Enterprise SKU: 1,000 free root requests
 * a month, then $6 per 1,000. Only the ROOT request bills - the hundreds of
 * tiles streamed while somebody flies around are free - so one visit is one
 * request. The account quota is set to 85 root requests a day. That is plenty
 * for a demo link sent to a developer and nothing like enough for a public
 * page, which is why nadlan_earth_quota_guard() exists and why this is not
 * linked from anywhere public yet.
 *
 * The API key is injected server-side. It is never a query parameter: a key in
 * a URL travels into browser history, referrer headers and any forwarded link.
 * Browser keys are visible in page source by design; the protection is the
 * HTTP-referrer restriction on the key, not secrecy.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_earth_key' ) ) {
	function nadlan_earth_key() {
		return trim( (string) get_option( 'nadlan_gmaps_key', '' ) );
	}
}

if ( ! function_exists( 'nadlan_earth_scenes' ) ) {
	/**
	 * Allowlist of scenes. Nothing outside this map is served.
	 *
	 * radius_km bounds which projects get planted, so the Sde Dov scene does
	 * not quietly pull in the whole 978-project catalogue.
	 */
	function nadlan_earth_scenes() {
		return array(
			'sde-dov' => array(
				'title'     => 'רובע שדה דב',
				'lat'       => 32.1099,
				'lng'       => 34.7822,
				'height'    => 900.0,
				'heading'   => 20.0,
				'pitch'     => -32.0,
				'radius_km' => 2.2,
			),
			'somail'  => array(
				'title'     => 'מתחם סומייל',
				'lat'       => 32.0853,
				'lng'       => 34.7818,
				'height'    => 750.0,
				'heading'   => 340.0,
				'pitch'     => -30.0,
				'radius_km' => 1.4,
			),
		);
	}
}

if ( ! function_exists( 'nadlan_earth_quota_guard' ) ) {
	/**
	 * Daily load counter.
	 *
	 * Google stops serving the moment the daily quota is exhausted, which would
	 * mean a black screen in the middle of a demo. Stopping ourselves a little
	 * early lets us show an explanation instead, and gives us a real usage
	 * number to look at before asking for a higher quota.
	 *
	 * @return array{allowed:bool,used:int,cap:int}
	 */
	function nadlan_earth_quota_guard( $consume = true ) {
		$cap  = (int) apply_filters( 'nadlan_earth_daily_cap', 75 );
		$key  = 'nadlan_earth_loads_' . gmdate( 'Ymd' );
		$used = (int) get_transient( $key );
		if ( $used >= $cap ) {
			return array( 'allowed' => false, 'used' => $used, 'cap' => $cap );
		}
		if ( $consume ) {
			set_transient( $key, $used + 1, DAY_IN_SECONDS );
		}
		return array( 'allowed' => true, 'used' => $used + 1, 'cap' => $cap );
	}
}

if ( ! function_exists( 'nadlan_earth_projects' ) ) {
	/**
	 * Projects near a scene, as pin data.
	 *
	 * Language variants are dropped with the same rule already used by
	 * nadlan_hv2_image_projects() in home-v2.php - without it utopia and duo
	 * would each plant four identical pins on top of each other.
	 *
	 * A project carrying project_model_glb also ships the model URL plus three
	 * optional placement metas (earth_heading, earth_scale, earth_alt) so a
	 * badly rotated or floating model can be calibrated per project from the
	 * admin without touching code.
	 */
	function nadlan_earth_projects( $scene ) {
		/* Bounding box in SQL, not a LIMIT in PHP. 978 projects carry
		   coordinates; pulling an arbitrary first N and filtering afterwards
		   silently dropped Ashira and Dimri Yama - both inside the radius -
		   because they sat outside that window. */
		$dlat = $scene['radius_km'] / 110.57;
		$dlng = $scene['radius_km'] / ( 111.32 * max( 0.1, cos( deg2rad( $scene['lat'] ) ) ) );

		$posts = get_posts( array(
			'post_type'      => 'nadlan_project',
			'post_status'    => 'publish',
			'posts_per_page' => 200,
			'no_found_rows'  => true,
			'meta_query'     => array( // phpcs:ignore WordPress.DB.SlowDBQuery
				'relation' => 'AND',
				array(
					'key'     => 'lat',
					'value'   => array( $scene['lat'] - $dlat, $scene['lat'] + $dlat ),
					'type'    => 'DECIMAL(10,6)',
					'compare' => 'BETWEEN',
				),
				array(
					'key'     => 'lng',
					'value'   => array( $scene['lng'] - $dlng, $scene['lng'] + $dlng ),
					'type'    => 'DECIMAL(10,6)',
					'compare' => 'BETWEEN',
				),
			),
		) );

		$out = array();
		foreach ( $posts as $p ) {
			if ( preg_match( '/-(en|fr|ru|ar)$/', $p->post_name ) ) {
				continue;
			}
			$lat = (float) get_post_meta( $p->ID, 'lat', true );
			$lng = (float) get_post_meta( $p->ID, 'lng', true );
			if ( ! $lat || ! $lng ) {
				continue;
			}
			/* equirectangular approximation - accurate enough at city scale and
			   far cheaper than haversine across 400 rows */
			$dx = ( $lng - $scene['lng'] ) * 111.32 * cos( deg2rad( $scene['lat'] ) );
			$dy = ( $lat - $scene['lat'] ) * 110.57;
			if ( sqrt( $dx * $dx + $dy * $dy ) > $scene['radius_km'] ) {
				continue;
			}
			$glb = trim( (string) get_post_meta( $p->ID, 'project_model_glb', true ) );
			$row = array(
				'name'  => get_the_title( $p ),
				'dev'   => (string) get_post_meta( $p->ID, 'developer_name', true ),
				'city'  => (string) get_post_meta( $p->ID, 'city', true ),
				'lat'   => $lat,
				'lng'   => $lng,
				'url'   => get_permalink( $p ),
				'model' => '' !== $glb,
			);
			if ( '' !== $glb ) {
				$row['glb'] = esc_url_raw( $glb );
				foreach ( array( 'hdg' => 'earth_heading', 'scl' => 'earth_scale', 'alt' => 'earth_alt' ) as $k => $meta ) {
					$v = get_post_meta( $p->ID, $meta, true );
					if ( '' !== $v && is_numeric( $v ) ) {
						$row[ $k ] = (float) $v;
					}
				}
			}
			$out[] = $row;
		}
		/* projects carrying a 3D model are the ones worth flying to, so they
		   draw last and therefore sit on top when pins overlap */
		usort( $out, function ( $a, $b ) {
			return ( $a['model'] === $b['model'] ) ? 0 : ( $a['model'] ? 1 : -1 );
		} );
		return $out;
	}
}

if ( ! function_exists( 'nadlan_earth_screen' ) ) {
	/** Minimal full-screen message, used for every failure path. */
	function nadlan_earth_screen( $title, $body, $status = 200 ) {
		status_header( $status );
		header( 'Content-Type: text/html; charset=utf-8' );
		echo '<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
			. '<meta name="viewport" content="width=device-width,initial-scale=1">'
			. '<meta name="robots" content="noindex,nofollow">'
			. '<title>' . esc_html( $title ) . ' · nad-lan.co.il</title><style>'
			. 'html,body{margin:0;height:100%;background:#14130F;color:#F4EEDE;'
			. 'font-family:Heebo,system-ui,sans-serif;display:flex;align-items:center;justify-content:center}'
			. '.b{max-width:520px;padding:32px;text-align:center}'
			. 'h1{font-size:20px;margin:0 0 12px}p{color:#9B948A;font-size:14.5px;line-height:1.75;margin:0}'
			. 'a{color:#D8C79A}</style></head><body><div class="b"><h1>' . esc_html( $title ) . '</h1>'
			. '<p>' . wp_kses( $body, array( 'a' => array( 'href' => array() ), 'br' => array() ) ) . '</p>'
			. '</div></body></html>';
		exit;
	}
}

add_action( 'init', function () {
	add_rewrite_rule( '^earth/([a-z0-9-]+)/?$', 'index.php?nadlan_earth=$matches[1]', 'top' );
	if ( get_option( 'nadlan_earth_routes_flushed' ) !== NADLAN_CONFIG_VERSION ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_earth_routes_flushed', NADLAN_CONFIG_VERSION );
	}
} );

add_filter( 'query_vars', function ( $vars ) {
	$vars[] = 'nadlan_earth';
	return $vars;
} );

add_action( 'template_redirect', function () {
	$slug = (string) get_query_var( 'nadlan_earth' );
	if ( '' === $slug ) {
		return;
	}
	$scenes = nadlan_earth_scenes();
	if ( ! isset( $scenes[ $slug ] ) ) {
		nadlan_earth_screen( 'לא נמצא', 'החוויה המבוקשת אינה קיימת.', 404 );
	}
	$key = nadlan_earth_key();
	if ( '' === $key ) {
		nadlan_earth_screen( 'החוויה אינה מוגדרת', 'חסר מפתח Google Maps Platform. יש להגדיר את האופציה nadlan_gmaps_key.', 503 );
	}
	$quota = nadlan_earth_quota_guard();
	if ( ! $quota['allowed'] ) {
		nadlan_earth_screen(
			'החוויה בתחזוקה',
			'הגענו למכסת הצפיות היומית בחוויה הפוטוריאליסטית. היא תיפתח מחדש מחר.<br>'
			. 'בינתיים אפשר לצפות ב<a href="' . esc_url( home_url( '/tour/sde-dov/' ) ) . '">סיור התלת ממדי</a>.',
			503
		);
	}

	$scene    = $scenes[ $slug ];
	$projects = nadlan_earth_projects( $scene );

	header( 'Content-Type: text/html; charset=utf-8' );
	?><!DOCTYPE html>
<html lang="he" dir="rtl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title><?php echo esc_html( $scene['title'] ); ?> · תלת ממד פוטוריאליסטי | nad-lan.co.il</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/cesium@1.143.0/Build/Cesium/Widgets/widgets.css">
<style>
html,body{margin:0;height:100%;overflow:hidden;background:#14130F;font-family:Heebo,system-ui,sans-serif}
#cesium{position:fixed;inset:0}
/* Google's attributions render here. Kept legible against photography rather
   than left as Cesium's default grey-on-transparent. */
.cesium-viewer-bottom{bottom:4px!important;inset-inline-start:8px}
.cesium-widget-credits{color:#EDE7DA!important;font-family:Heebo,system-ui,sans-serif!important;
 font-size:11px!important;text-shadow:0 1px 3px rgba(0,0,0,.9)!important;background:rgba(20,19,15,.42);
 padding:3px 8px;border-radius:7px;direction:ltr}
.cesium-widget-credits a{color:#E8C572!important}
/* DOM pin layer. The container swallows no input; each pin does. */
#pins{position:fixed;inset:0;z-index:10;pointer-events:none;overflow:hidden}
.nlpin{position:absolute;top:0;left:0;pointer-events:auto;cursor:pointer;display:flex;
 flex-direction:column;align-items:center;gap:2px;user-select:none;-webkit-user-select:none;
 -webkit-tap-highlight-color:transparent}
.nlpin .nm{font:500 12.5px/1.3 Heebo,sans-serif;color:#C9C2B4;white-space:nowrap;
 direction:rtl;unicode-bidi:plaintext;transition:opacity .25s;
 text-shadow:0 0 4px #14130F,0 1px 2px rgba(0,0,0,.95),0 -1px 2px rgba(0,0,0,.95)}
.nlpin .dot{width:12px;height:12px;border-radius:50%;background:#9B948A;border:3px solid #14130F;
 box-shadow:0 1px 5px rgba(0,0,0,.6);transition:transform .15s}
.nlpin.gold .nm{font:700 14px/1.3 Heebo,sans-serif;color:#FFF}
.nlpin.gold .dot{width:17px;height:17px;background:#E8C572}
.nlpin:hover .dot{transform:scale(1.18)}
#hud{position:fixed;top:14px;inset-inline-start:14px;z-index:20;background:rgba(20,19,15,.86);
 border:1px solid rgba(216,193,137,.35);border-radius:14px;padding:12px 16px;color:#F4EEDE;max-width:min(78vw,360px)}
#hud b{display:block;font-size:15.5px;font-weight:800;margin-bottom:4px}
#hud span{display:block;font-size:12.5px;color:#C9C2B4;line-height:1.6}
#card{position:fixed;inset-inline-end:14px;bottom:14px;z-index:21;background:rgba(20,19,15,.94);
 border:1px solid rgba(216,193,137,.4);border-radius:16px;padding:16px 18px;color:#F4EEDE;
 max-width:min(88vw,340px);display:none}
#card h2{margin:0 0 6px;font-size:16px;font-weight:800}
#card p{margin:0 0 10px;font-size:13px;color:#C9C2B4;line-height:1.7}
#card a{display:inline-block;background:#B85410;color:#fff;text-decoration:none;font-weight:800;
 font-size:13.5px;border-radius:9px;padding:9px 16px;margin-inline-end:8px}
#card a.ghost{background:transparent;border:1px solid rgba(216,193,137,.5);color:#D8C79A}
#card button{position:absolute;top:10px;inset-inline-start:12px;background:none;border:0;color:#9B948A;
 font-size:19px;cursor:pointer;line-height:1}
#tourbar{position:fixed;bottom:calc(14px + env(safe-area-inset-bottom));left:50%;
 transform:translateX(-50%);z-index:22;background:rgba(20,19,15,.9);
 border:1px solid rgba(216,193,137,.4);border-radius:999px;padding:9px 10px 9px 18px;color:#F4EEDE;
 display:none;align-items:center;gap:11px;font-size:13.5px;white-space:nowrap;max-width:94vw}
#tourbar b{font-weight:800;color:#E8C572}
#tourbar span{overflow:hidden;text-overflow:ellipsis;max-width:44vw}
#tourbar button{background:transparent;border:1px solid rgba(216,193,137,.5);color:#D8C79A;
 border-radius:999px;padding:5px 13px;font:600 12.5px Heebo,sans-serif;cursor:pointer}
#boot{position:fixed;inset:0;z-index:30;background:#14130F;color:#F4EEDE;display:flex;
 align-items:center;justify-content:center;text-align:center;font-size:14.5px;padding:24px}
#boot small{display:block;color:#9B948A;margin-top:8px;font-size:12.5px}
@media(max-width:640px){#hud{max-width:70vw;padding:10px 13px}#hud b{font-size:14px}
 #card{bottom:calc(64px + env(safe-area-inset-bottom))}}
</style>
</head><body>
<div id="cesium"></div>
<div id="pins" aria-hidden="true"></div>
<div id="hud">
  <b><?php echo esc_html( $scene['title'] ); ?></b>
  <span id="hudTip">העולם נטען, הסיור האוטומטי יתחיל מיד.</span>
</div>
<div id="card"><button id="cardX" aria-label="סגירה">×</button><div id="cardBody"></div></div>
<div id="tourbar"><b id="tourNum"></b><span id="tourName"></span><button id="tourSkip">לשליטה ידנית</button></div>
<div id="boot">טוען את העולם התלת ממדי…<small>הנתונים מוזרמים מגוגל, זה עשוי לקחת רגע</small></div>

<script src="https://cdn.jsdelivr.net/npm/cesium@1.143.0/Build/Cesium/Cesium.js"></script>
<script>
(function () {
  "use strict";
  var KEY      = <?php echo wp_json_encode( $key ); ?>;
  var SCENE    = <?php echo wp_json_encode( $scene ); ?>;
  var PROJECTS = <?php echo wp_json_encode( $projects ); ?>;

  /* Touch means no hover anywhere, so cards open on tap there instead. */
  var TOUCH = window.matchMedia && matchMedia('(hover: none), (pointer: coarse)').matches;
  var TIP_FREE = TOUCH
    ? 'נוגעים בסימן זהב כדי לראות פרויקט ולטוס אליו. כל בניין אחר נלחץ ומספר מה הוא.'
    : 'מרחפים מעל סימן כדי לראות פרטים ולוחצים עליו כדי לטוס אליו. כל בניין אחר נלחץ ומספר מה הוא.';
  var TIP_TOUR = 'סיור אוטומטי מתחיל. נגיעה אחת בעולם עוצרת אותו ומעבירה אליכם את השליטה.';

  function die(msg) {
    var b = document.getElementById('boot');
    b.innerHTML = msg + '<small>אם זה חוזר, כדאי לרענן</small>';
    b.style.display = 'flex';
  }

  /* No Cesium ion: the tiles come straight from Google with our own key, so
     an ion token would be a second dependency for nothing. Clearing the
     default token stops Cesium asking for one. */
  Cesium.Ion.defaultAccessToken = undefined;
  Cesium.GoogleMaps.defaultApiKey = KEY;

  var viewer;
  try {
    viewer = new Cesium.Viewer('cesium', {
      globe: false, geocoder: false, baseLayerPicker: false, homeButton: false,
      sceneModePicker: false, navigationHelpButton: false, animation: false,
      timeline: false, fullscreenButton: false, infoBox: false, selectionIndicator: false
    });
  } catch (e) {
    die('לא הצלחנו לאתחל את התצוגה.'); return;
  }
  viewer.scene.skyAtmosphere.show = true;

  var START = {
    destination: Cesium.Cartesian3.fromDegrees(SCENE.lng, SCENE.lat, SCENE.height),
    orientation: {
      heading: Cesium.Math.toRadians(SCENE.heading),
      pitch: Cesium.Math.toRadians(SCENE.pitch),
      roll: 0
    }
  };
  viewer.camera.setView(START);

  /* ---------------- card ---------------- */
  var card = document.getElementById('card'), body = document.getElementById('cardBody');
  var hudTip = document.getElementById('hudTip');
  var hideT = 0, autoT = 0;
  function hideCard() { card.style.display = 'none'; }
  document.getElementById('cardX').onclick = hideCard;
  /* Nothing may stay stuck on screen: hover cards die when the pointer leaves
     pin and card, click cards die on their own after a few seconds, and both
     die on an empty click or Escape. */
  function show(html, autoMs) {
    clearTimeout(hideT); clearTimeout(autoT);
    body.innerHTML = html; card.style.display = 'block';
    if (autoMs) { autoT = setTimeout(hideCard, autoMs); }
  }
  function scheduleHide(ms) { clearTimeout(hideT); hideT = setTimeout(hideCard, ms); }
  card.addEventListener('mouseenter', function () { clearTimeout(hideT); clearTimeout(autoT); });
  card.addEventListener('mouseleave', function () { scheduleHide(500); });
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function projectCard(p) {
    var meta = [p.dev, p.city].filter(Boolean).join(' · ');
    return '<h2>' + esc(p.name) + '</h2>'
      + (meta ? '<p>' + esc(meta) + '</p>' : '')
      + '<a href="' + esc(p.url) + '">לעמוד הפרויקט</a>'
      + (p.model ? '<a class="ghost" href="' + esc(p.url) + '#showroom">למודל התלת ממד</a>' : '');
  }

  function flyToProject(p) {
    viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(p.lng, p.lat - 0.0022, 260),
      orientation: { heading: 0, pitch: Cesium.Math.toRadians(-26), roll: 0 },
      duration: 2.2
    });
  }

  /* ---------------- DOM pins ----------------
     A project with a 3D model is somewhere you can actually walk into, so it
     reads as gold and larger. Everything else is a quieter marker. Names are
     real text nodes, so the browser shapes the Hebrew correctly. */
  var pinsWrap = document.getElementById('pins');
  var pins = [];
  PROJECTS.forEach(function (p) {
    var el = document.createElement('div');
    el.className = 'nlpin' + (p.model ? ' gold' : '');
    var nm = document.createElement('span'); nm.className = 'nm'; nm.textContent = p.name;
    var dot = document.createElement('span'); dot.className = 'dot';
    el.appendChild(nm); el.appendChild(dot);
    el.style.display = 'none';
    if (!TOUCH) {
      el.addEventListener('mouseenter', function () { show(projectCard(p)); });
      el.addEventListener('mouseleave', function () { scheduleHide(600); });
    }
    el.addEventListener('click', function (ev) {
      ev.stopPropagation();
      endTour(true);
      if (TOUCH) { show(projectCard(p), 14000); }
      flyToProject(p);
    });
    pinsWrap.appendChild(el);
    pins.push({
      p: p, el: el, nm: nm,
      pos: Cesium.Cartesian3.fromDegrees(p.lng, p.lat, 40),
      /* the dot's centre, not the element's edge, must sit on the anchor */
      anchor: 'translate(-50%,-100%) translateY(' + (p.model ? 11.5 : 9) + 'px)',
      scratch: new Cesium.Cartesian2()
    });
  });

  var toWin = Cesium.SceneTransforms.worldToWindowCoordinates
    ? Cesium.SceneTransforms.worldToWindowCoordinates.bind(Cesium.SceneTransforms)
    : Cesium.SceneTransforms.wgs84ToWindowCoordinates.bind(Cesium.SceneTransforms);

  viewer.scene.postRender.addEventListener(function () {
    var cam = viewer.camera.positionWC;
    var W = window.innerWidth, H = window.innerHeight;
    for (var i = 0; i < pins.length; i++) {
      var pin = pins[i];
      var w = toWin(viewer.scene, pin.pos, pin.scratch);
      var d = Cesium.Cartesian3.distance(cam, pin.pos);
      if (!w || isNaN(w.x) || w.x < -80 || w.x > W + 80 || w.y < -60 || w.y > H + 60 || d > 12000) {
        pin.el.style.display = 'none'; continue;
      }
      pin.el.style.display = '';
      pin.el.style.transform = 'translate(' + w.x.toFixed(1) + 'px,' + w.y.toFixed(1) + 'px) ' + pin.anchor;
      /* nearer pins stack above farther ones; gold outranks grey on ties */
      pin.el.style.zIndex = Math.max(1, 12000 - Math.round(d)) + (pin.p.model ? 3000 : 0);
      var nearD = pin.p.model ? 900 : 500, farD = pin.p.model ? 3200 : 1800;
      pin.nm.style.opacity = d <= nearD ? 1 : (d >= farD ? 0 : (farD - d) / (farD - nearD));
    }
  });

  /* ---------------- auto tour ----------------
     The first thing the page does is fly the visitor over the projects, then
     hand the controls over. Any real input on the world (or the button, or
     Escape) stops it at once and leaves the camera where it is. */
  var cesiumEl = document.getElementById('cesium');
  var tourbar = document.getElementById('tourbar');
  var tourNum = document.getElementById('tourNum');
  var tourName = document.getElementById('tourName');
  var tour = { on: false, t: 0 };
  function onUserGrab() { endTour(true); }
  function endTour(byUser) {
    if (!tour.on) { return; }
    tour.on = false; clearTimeout(tour.t);
    try { viewer.camera.cancelFlight(); } catch (e) {}
    tourbar.style.display = 'none';
    hudTip.textContent = TIP_FREE;
    ['pointerdown', 'wheel', 'touchstart'].forEach(function (ev) {
      cesiumEl.removeEventListener(ev, onUserGrab, true);
    });
    if (!byUser) {
      viewer.camera.flyTo({ destination: START.destination, orientation: START.orientation, duration: 3.2 });
    }
  }
  document.getElementById('tourSkip').onclick = function () { endTour(true); };
  /* nearest-neighbour walk from the scene centre, so the camera sweeps the
     quarter instead of zigzagging across it */
  function orderTour(list) {
    var rest = list.slice(), out = [], cur = { lat: SCENE.lat, lng: SCENE.lng };
    while (rest.length) {
      var bi = 0, bd = Infinity;
      for (var i = 0; i < rest.length; i++) {
        var dl = rest[i].lat - cur.lat, dg = rest[i].lng - cur.lng, dd = dl * dl + dg * dg;
        if (dd < bd) { bd = dd; bi = i; }
      }
      cur = rest.splice(bi, 1)[0]; out.push(cur);
    }
    return out;
  }
  function autoTour() {
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) {
      hudTip.textContent = TIP_FREE; return;
    }
    var stops = PROJECTS.filter(function (p) { return p.model; });
    if (stops.length < 2) { stops = PROJECTS.slice(0, 4); }
    stops = orderTour(stops).slice(0, 5);
    if (stops.length < 2) { hudTip.textContent = TIP_FREE; return; }
    tour.on = true;
    hudTip.textContent = TIP_TOUR;
    tourbar.style.display = 'flex';
    ['pointerdown', 'wheel', 'touchstart'].forEach(function (ev) {
      cesiumEl.addEventListener(ev, onUserGrab, true);
    });
    var i = 0;
    function leg() {
      if (!tour.on) { return; }
      if (i >= stops.length) { endTour(false); return; }
      var p = stops[i]; i++;
      tourNum.textContent = i + '/' + stops.length;
      tourName.textContent = p.name;
      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(p.lng, p.lat - 0.0022, 260),
        orientation: { heading: 0, pitch: Cesium.Math.toRadians(-26), roll: 0 },
        duration: 3.0,
        complete: function () { if (tour.on) { tour.t = setTimeout(leg, 1700); } }
      });
    }
    leg();
  }

  /* ---------------- our models in the world ----------------
     Projects that own a GLB get the real thing planted at their coordinates.
     Ground height comes from sampling the photogrammetry; earth_alt,
     earth_heading and earth_scale metas correct individual models. */
  function placeModels() {
    var withGlb = PROJECTS.filter(function (p) { return p.glb; });
    if (!withGlb.length) { return; }
    var carto = withGlb.map(function (p) { return Cesium.Cartographic.fromDegrees(p.lng, p.lat); });
    function place(heights) {
      withGlb.forEach(function (p, i) {
        var h = 10;
        if (heights && heights[i] && typeof heights[i].height === 'number' && !isNaN(heights[i].height)) {
          h = heights[i].height;
        }
        h += (p.alt || 0);
        var pos = Cesium.Cartesian3.fromDegrees(p.lng, p.lat, h);
        var hpr = new Cesium.HeadingPitchRoll(Cesium.Math.toRadians(p.hdg || 0), 0, 0);
        var e = viewer.entities.add({
          position: pos,
          orientation: Cesium.Transforms.headingPitchRollQuaternion(pos, hpr),
          model: { uri: p.glb, scale: p.scl || 1 }
        });
        e.nlProject = p;
      });
    }
    if (viewer.scene.sampleHeightSupported) {
      viewer.scene.sampleHeightMostDetailed(carto).then(place).catch(function () { place(null); });
    } else {
      place(null);
    }
  }

  Cesium.createGooglePhotorealistic3DTileset({ onlyUsingWithGoogleGeocoder: true })
    .then(function (tiles) {
      /* Google's terms require the attributions the tileset returns to be
         visible. Cesium defaults them into the "Data attribution" lightbox,
         where nobody sees them. Passing showCreditsOnScreen through the
         factory does NOT work - verified live, the option is dropped - but
         setting it on the instance does, and Google appears on screen. */
      tiles.showCreditsOnScreen = true;
      viewer.scene.primitives.add(tiles);
      window.NL_EARTH = { viewer: viewer, tiles: tiles, projects: PROJECTS, pins: pins, endTour: endTour };
      document.getElementById('boot').style.display = 'none';
      placeModels();
      setTimeout(autoTour, 900);
    })
    .catch(function () {
      die('טעינת האריחים של גוגל נכשלה.<br>ייתכן שהמכסה היומית נגמרה או שהמפתח מוגבל לדומיין אחר.');
    });

  /* Surroundings. OSM Buildings carries per-building metadata, so a school or
     a cafe becomes clickable without us maintaining a POI database. */
  Cesium.createOsmBuildingsAsync()
    .then(function (osm) { viewer.scene.primitives.add(osm); })
    .catch(function () { /* the scene is still usable without it */ });

  new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas).setInputAction(function (click) {
    var picked = viewer.scene.pick(click.position);
    if (!Cesium.defined(picked)) { hideCard(); return; }

    /* a planted project model is still our project */
    var p = picked.id && picked.id.nlProject;
    if (p) {
      show(projectCard(p), 10000);
      flyToProject(p);
      return;
    }

    if (picked.getProperty) {
      var name = picked.getProperty('name') || picked.getProperty('addr:housename');
      var road = picked.getProperty('addr:street'), num = picked.getProperty('addr:housenumber');
      var kind = picked.getProperty('building'), hrs = picked.getProperty('opening_hours');
      var addr = [road, num].filter(Boolean).join(' ');
      if (name || addr || (kind && kind !== 'yes')) {
        var rows = [addr, (kind && kind !== 'yes') ? kind : '', hrs].filter(Boolean).join(' · ');
        show('<h2>' + esc(name || addr || 'בניין') + '</h2>'
           + (rows ? '<p>' + esc(rows) + '</p>' : '')
           + '<p style="font-size:11.5px;color:#8E877A;margin:0">מקור: OpenStreetMap</p>', 10000);
        return;
      }
    }
    hideCard();
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

  window.addEventListener('keydown', function (ev) {
    if ('Escape' === ev.key) { hideCard(); endTour(true); }
  });
})();
</script>
</body></html>
	<?php
	exit;
} );
