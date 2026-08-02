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
			$glb = (string) get_post_meta( $p->ID, 'project_model_glb', true );
			$out[] = array(
				'name'  => get_the_title( $p ),
				'dev'   => (string) get_post_meta( $p->ID, 'developer_name', true ),
				'city'  => (string) get_post_meta( $p->ID, 'city', true ),
				'lat'   => $lat,
				'lng'   => $lng,
				'url'   => get_permalink( $p ),
				'model' => '' !== $glb,
			);
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
#hud{position:fixed;top:14px;inset-inline-start:14px;z-index:20;background:rgba(20,19,15,.86);
 border:1px solid rgba(216,193,137,.35);border-radius:14px;padding:12px 16px;color:#F4EEDE;max-width:min(78vw,360px)}
#hud b{display:block;font-size:15.5px;font-weight:800;margin-bottom:4px}
#hud span{display:block;font-size:12.5px;color:#C9C2B4;line-height:1.6}
#card{position:fixed;inset-inline-end:14px;bottom:14px;z-index:20;background:rgba(20,19,15,.94);
 border:1px solid rgba(216,193,137,.4);border-radius:16px;padding:16px 18px;color:#F4EEDE;
 max-width:min(88vw,340px);display:none}
#card h2{margin:0 0 6px;font-size:16px;font-weight:800}
#card p{margin:0 0 10px;font-size:13px;color:#C9C2B4;line-height:1.7}
#card a{display:inline-block;background:#B85410;color:#fff;text-decoration:none;font-weight:800;
 font-size:13.5px;border-radius:9px;padding:9px 16px;margin-inline-end:8px}
#card a.ghost{background:transparent;border:1px solid rgba(216,193,137,.5);color:#D8C79A}
#card button{position:absolute;top:10px;inset-inline-start:12px;background:none;border:0;color:#9B948A;
 font-size:19px;cursor:pointer;line-height:1}
#boot{position:fixed;inset:0;z-index:30;background:#14130F;color:#F4EEDE;display:flex;
 align-items:center;justify-content:center;text-align:center;font-size:14.5px;padding:24px}
#boot small{display:block;color:#9B948A;margin-top:8px;font-size:12.5px}
@media(max-width:640px){#hud{max-width:70vw;padding:10px 13px}#hud b{font-size:14px}}
</style>
</head><body>
<div id="cesium"></div>
<div id="hud">
  <b><?php echo esc_html( $scene['title'] ); ?></b>
  <span>לוחצים על סימן זהב כדי לפתוח פרויקט, ועל כל בניין אחר כדי לראות מה ידוע עליו.</span>
</div>
<div id="card"><button id="cardX" aria-label="סגירה">×</button><div id="cardBody"></div></div>
<div id="boot">טוען את העולם התלת ממדי…<small>הנתונים מוזרמים מגוגל, זה עשוי לקחת רגע</small></div>

<script src="https://cdn.jsdelivr.net/npm/cesium@1.143.0/Build/Cesium/Cesium.js"></script>
<script>
(function () {
  "use strict";
  var KEY      = <?php echo wp_json_encode( $key ); ?>;
  var SCENE    = <?php echo wp_json_encode( $scene ); ?>;
  var PROJECTS = <?php echo wp_json_encode( $projects ); ?>;

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

  viewer.camera.setView({
    destination: Cesium.Cartesian3.fromDegrees(SCENE.lng, SCENE.lat, SCENE.height),
    orientation: {
      heading: Cesium.Math.toRadians(SCENE.heading),
      pitch: Cesium.Math.toRadians(SCENE.pitch),
      roll: 0
    }
  });

  var card = document.getElementById('card'), body = document.getElementById('cardBody');
  document.getElementById('cardX').onclick = function () { card.style.display = 'none'; };
  function show(html) { body.innerHTML = html; card.style.display = 'block'; }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* A project with a 3D model is somewhere you can actually walk into, so it
     reads as gold and larger. Everything else is a quieter marker - present,
     clickable, but not competing for the eye. */
  PROJECTS.forEach(function (p) {
    var gold = p.model;
    var e = viewer.entities.add({
      position: Cesium.Cartesian3.fromDegrees(p.lng, p.lat, 40),
      point: {
        pixelSize: gold ? 17 : 11,
        color: Cesium.Color.fromCssColorString(gold ? '#E8C572' : '#9B948A'),
        outlineColor: Cesium.Color.fromCssColorString('#14130F'),
        outlineWidth: 3,
        disableDepthTestDistance: Number.POSITIVE_INFINITY
      },
      label: {
        text: p.name,
        font: (gold ? '700 14px' : '500 12.5px') + ' Heebo, sans-serif',
        fillColor: gold ? Cesium.Color.WHITE : Cesium.Color.fromCssColorString('#C9C2B4'),
        outlineColor: Cesium.Color.fromCssColorString('#14130F'), outlineWidth: 4,
        style: Cesium.LabelStyle.FILL_AND_OUTLINE,
        pixelOffset: new Cesium.Cartesian2(0, gold ? -24 : -18),
        disableDepthTestDistance: Number.POSITIVE_INFINITY,
        translucencyByDistance: new Cesium.NearFarScalar(
          gold ? 900 : 500, 1.0, gold ? 3200 : 1800, 0.0)
      }
    });
    e.nlProject = p;
  });

  function flyToProject(p) {
    viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(p.lng, p.lat - 0.0022, 260),
      orientation: { heading: Cesium.Math.toRadians(0), pitch: Cesium.Math.toRadians(-26), roll: 0 },
      duration: 2.2
    });
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
      window.NL_EARTH = { viewer: viewer, tiles: tiles, projects: PROJECTS };
      document.getElementById('boot').style.display = 'none';
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
    if (!Cesium.defined(picked)) { card.style.display = 'none'; return; }

    var p = picked.id && picked.id.nlProject;
    if (p) {
      var meta = [p.dev, p.city].filter(Boolean).join(' · ');
      show('<h2>' + esc(p.name) + '</h2>'
         + (meta ? '<p>' + esc(meta) + '</p>' : '')
         + '<a href="' + esc(p.url) + '">לעמוד הפרויקט</a>'
         + (p.model ? '<a class="ghost" href="' + esc(p.url) + '#showroom">למודל התלת ממד</a>' : ''));
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
           + '<p style="font-size:11.5px;color:#8E877A;margin:0">מקור: OpenStreetMap</p>');
        return;
      }
    }
    card.style.display = 'none';
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
})();
</script>
</body></html>
	<?php
	exit;
} );
