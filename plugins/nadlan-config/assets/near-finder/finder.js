/* NadLan near finder v1 (HAD-672 / HAD-673, release 1.72.584, owner orders 4.11.2026 with addenda 1-3).
   Design: Claude Design "NadLan Instruments" (Main / Card / Desktop). Vanilla, no build step.
   Data: GET /wp-json/nadlan/v1/near-finder (inc/near-finder.php); on a broker's page ?broker=ID (her listings only).
   Distance first: every result shows its air distance from the visitor ("בקו אווירי") and from the sea; travel times are a
   secondary estimate without traffic. The visitor's location and places stay in this page and this browser (localStorage,
   wrapped): never in a URL, never sent to the site. The deep link is #lidi, never a location.
   Map: Mapbox GL v3.7.0 (the same loader and token as /projects/), loaded only when needed; cooperative gestures, so the
   page never sticks while scrolling. No token or no map: the list works alone.
   Opens inline (/properties/) or, since 6.11.2026 (owner: no floating button on any page, ever), in place inside the page's
   own map or listings section: a quiet switch there ("פרויקטים חדשים" | "דירות לידי" on the home page, "רשימה" | "על המפה"
   on the rent page and on a broker's site) puts the app where the projects map or the listing grid was. "מסך מלא" inside the
   app opens the full-screen dialog (Back or Escape returns it to its place); #lidi chooses the map in place and scrolls to it.
   v2 (release 1.72.585): alerts by email (inc/near-alerts.php), on portal pages only (the page prints #nlna-cfg; a broker's
   page does not): the quiet "התריעו לי על האזור הזה" sheet (Claude Design project/Alerts.dc.html), the heart "שמרו" on a
   listing's card (price drops) and "עקבו" on a project's card. Saved and followed items stay in this browser
   (nlnf_saved_v1); a request made here keeps only its row id and its signed key (nlnf_alert_v1), never the email. The
   area is sent rounded to 0.001° (about 100 m), in the body of a POST, never in a URL.
   v3 (release 1.72.586, the counted benchmark of 4.11.2026): "ציירו אזור" (a freehand zone, simplified to 60 points at most;
   on a phone it is drawn inside the dialog only, on a pad that exists only while drawing, so the page itself never captures
   a touch or the wheel), "סינון נוסף" (rooms from-to with the halves the data has, price from-to per sale and rent, m², floor,
   elevator, parking, balcony, only where listings state them, and a live count on the button), "זמן נסיעה" (the Mapbox
   Isochrone API with the site's public token, drive / walk / cycle, 10 / 20 / 30 minutes from a saved place or from me, called
   only when the visitor presses the button, cached per point + mode + minutes in sessionStorage; that one call is the only
   place a point leaves the browser, rounded to 0.001°; on a failure the air-distance estimate, labelled as one), and on a
   phone inside the dialog a bottom sheet with three snaps (peek, half, full) dragged by its handle, which is also a button. */
(function () {
	'use strict';
	var root = document.getElementById('nlnf-app');
	if (!root || root.getAttribute('data-nlnf-on')) { return; }
	root.setAttribute('data-nlnf-on', '1');

	/* Israel's Mediterranean coastline, Rosh HaNikra to Zikim: OpenStreetMap natural=coastline (Overpass API, 4.11.2026),
	   stitched and simplified (Douglas-Peucker, 60 m). [[lat, lng], ...] per stretch. Used for "מרחק מהים" only. */
	var COAST = [[[33.0943,35.10356],[33.09245,35.10416],[33.09177,35.106],[33.09051,35.10504],[33.08276,35.10569],[33.06661,35.10458],[33.05737,35.10311],[33.05497,35.10169],[33.05054,35.10185],[33.04808,35.09992],[33.04729,35.10081],[33.04355,35.10004],[33.04307,35.09804],[33.04129,35.09693],[33.03948,35.09765],[33.01265,35.08935],[33.01303,35.08845],[33.01148,35.08902],[33.01166,35.08833],[33.01001,35.08746],[33.01021,35.0887],[33.00898,35.08751],[33.00834,35.08812],[33.0009,35.08603],[32.98758,35.08118],[32.98382,35.08169],[32.98327,35.07979],[32.98325,35.08062],[32.98153,35.08073],[32.96919,35.07667],[32.95885,35.0746],[32.94935,35.07428],[32.93418,35.0721],[32.93083,35.06987],[32.92089,35.06645],[32.91999,35.06529],[32.91906,35.06632],[32.91882,35.07045],[32.9195,35.06917],[32.92159,35.07166],[32.91905,35.07823],[32.9136,35.08058],[32.89842,35.07985],[32.88435,35.07602],[32.86194,35.06766],[32.84479,35.05911],[32.82937,35.04801],[32.82563,35.0442],[32.82395,35.04044],[32.82339,35.03811],[32.83113,35.03185],[32.83169,35.02349],[32.83146,35.02621],[32.82429,35.02729],[32.82482,35.03201],[32.81871,35.03424],[32.81603,35.02565],[32.81507,35.02788],[32.81589,35.03055],[32.81257,35.03193],[32.81385,35.03592],[32.81182,35.03675],[32.8086,35.02884],[32.80701,35.02878],[32.80631,35.03194],[32.80436,35.0313],[32.80622,35.02751],[32.81211,35.02796],[32.81468,35.02479],[32.81365,35.0252],[32.81499,35.02287],[32.81346,35.02362],[32.81273,35.01961],[32.8141,35.01995],[32.81603,35.0229],[32.81435,35.02002],[32.81238,35.01923],[32.81235,35.01773],[32.82105,35.01555],[32.8207,35.0129],[32.8145,35.01405],[32.81413,35.01144],[32.82281,35.00943],[32.82239,35.00687],[32.82274,35.00817],[32.82158,35.007],[32.81821,35.00681],[32.82182,35.00544],[32.81819,35.00654],[32.81811,35.0057],[32.82066,35.00478],[32.81809,35.00549],[32.81802,35.00432],[32.82339,34.9992],[32.82609,34.99149],[32.82722,34.9923],[32.82677,34.99418],[32.82869,34.9906],[32.8294,34.99093],[32.829,34.99201],[32.82966,34.99057],[32.83025,34.99169],[32.82859,34.99686],[32.82727,34.99677],[32.8282,34.99739],[32.82777,34.9982],[32.82689,34.99778],[32.82776,34.99832],[32.82668,34.99838],[32.82749,34.99895],[32.82718,34.99981],[32.82625,34.99952],[32.82728,35.00068],[32.8254,35.00807],[32.82671,35.01458],[32.82746,35.01644],[32.82982,35.01814],[32.83503,35.01913],[32.83057,35.01804],[32.8277,35.01608],[32.82554,35.00722],[32.82853,34.99779],[32.83192,34.99866],[32.83031,34.99802],[32.83062,34.99716],[32.8298,34.99666],[32.83086,34.99648],[32.83014,34.99582],[32.83099,34.99611],[32.83025,34.9954],[32.83112,34.99574],[32.83037,34.99504],[32.83124,34.99538],[32.8305,34.99467],[32.83137,34.99502],[32.83057,34.99448],[32.83173,34.99199],[32.83272,34.99199],[32.83365,35.00005],[32.83331,34.99082],[32.83251,34.99105],[32.8321,34.98971],[32.83568,34.98595],[32.8366,34.98002],[32.83522,34.97887],[32.83546,34.97772],[32.83626,34.97792],[32.83347,34.97549],[32.8304,34.96328],[32.82616,34.95863],[32.82613,34.95607],[32.82434,34.95449],[32.81365,34.95434],[32.80813,34.95601],[32.80537,34.9543],[32.80453,34.95613],[32.80286,34.95651],[32.79671,34.95494],[32.79654,34.95571],[32.79221,34.95548],[32.72761,34.94662],[32.70983,34.94164],[32.70605,34.93796],[32.70572,34.93527],[32.70685,34.93381],[32.70618,34.93227],[32.70463,34.93199],[32.70474,34.93394],[32.70348,34.93537],[32.69993,34.93437],[32.69843,34.93142],[32.69937,34.92798],[32.69817,34.92974],[32.69786,34.92737],[32.69543,34.92775],[32.69249,34.92666],[32.69074,34.92849],[32.68951,34.92776],[32.68859,34.92905],[32.68737,34.92731],[32.68653,34.92814],[32.68568,34.92629],[32.68385,34.92811],[32.68278,34.92769],[32.68297,34.92664],[32.68148,34.92758],[32.67983,34.92591],[32.67894,34.92609],[32.67876,34.92844],[32.67407,34.92922],[32.66938,34.92755],[32.66572,34.92777],[32.66537,34.92666],[32.66493,34.92753],[32.66234,34.92713],[32.6608,34.92627],[32.66092,34.92417],[32.65954,34.92655],[32.65832,34.92699],[32.65008,34.92561],[32.6476,34.9245],[32.64771,34.92282],[32.64683,34.92212],[32.64535,34.92206],[32.64478,34.92422],[32.64352,34.92365],[32.64364,34.92192],[32.64231,34.92097],[32.64109,34.9229],[32.63877,34.92345],[32.63683,34.92076],[32.63524,34.92217],[32.63438,34.92124],[32.63172,34.92142],[32.62978,34.91915],[32.62997,34.92052],[32.62909,34.92081],[32.62867,34.91885],[32.62794,34.92],[32.62615,34.91854],[32.62506,34.91945],[32.62445,34.91835],[32.62425,34.91964],[32.62317,34.91878],[32.62221,34.92037],[32.62052,34.918],[32.62107,34.91678],[32.61888,34.91694],[32.61626,34.91499],[32.61552,34.91541],[32.61589,34.91729],[32.61463,34.91763],[32.61358,34.91654],[32.61434,34.91487],[32.61325,34.91406],[32.61249,34.91631],[32.60844,34.91585],[32.60689,34.9171],[32.5991,34.91635],[32.56162,34.90882],[32.55769,34.90754],[32.55441,34.90494],[32.54941,34.90529],[32.54115,34.90323],[32.53909,34.90072],[32.53747,34.90173],[32.53495,34.9014],[32.52576,34.89938],[32.52471,34.89834],[32.51727,34.89762],[32.51374,34.89552],[32.51175,34.89609],[32.50896,34.89511],[32.50502,34.89076],[32.50414,34.891],[32.50379,34.88937],[32.50249,34.89107],[32.50187,34.89068],[32.50291,34.8888],[32.50009,34.89053],[32.49783,34.88977],[32.49708,34.88795],[32.49672,34.88953],[32.49404,34.88988],[32.49347,34.88918],[32.49435,34.88862],[32.49416,34.88689],[32.49314,34.88837],[32.49223,34.88679],[32.49289,34.88829],[32.49194,34.88857],[32.48399,34.88812],[32.47307,34.88418],[32.4732,34.88114],[32.473,34.88225],[32.47221,34.88218],[32.4728,34.88284],[32.47234,34.88524],[32.46768,34.88332],[32.46802,34.88114],[32.47348,34.8792],[32.46787,34.88067],[32.46632,34.88346],[32.46442,34.88379],[32.45067,34.87898],[32.44897,34.87924],[32.44904,34.87832],[32.4461,34.87777],[32.44423,34.87853],[32.44212,34.87674],[32.44074,34.87765],[32.43291,34.87495],[32.431,34.87528],[32.43123,34.87415],[32.42798,34.87438],[32.42597,34.87327],[32.41838,34.87223],[32.40319,34.86584],[32.40338,34.86687],[32.40253,34.86601],[32.40247,34.86693],[32.40164,34.86616],[32.40283,34.86566],[32.40176,34.8651],[32.39852,34.86612],[32.39302,34.86497],[32.33091,34.84844],[32.33035,34.84682],[32.32852,34.84807],[32.32741,34.84577],[32.32618,34.84724],[32.30037,34.84058],[32.24309,34.82388],[32.22188,34.81678],[32.19548,34.80604],[32.1733,34.80022],[32.16922,34.79743],[32.16795,34.79778],[32.16734,34.79651],[32.16536,34.79702],[32.16467,34.79319],[32.16265,34.79628],[32.1617,34.79491],[32.15928,34.79438],[32.1617,34.79457],[32.16305,34.79362],[32.15845,34.79305],[32.16011,34.79156],[32.16586,34.7926],[32.15963,34.79136],[32.1586,34.792],[32.15784,34.79463],[32.15299,34.79386],[32.12257,34.78309],[32.12184,34.7821],[32.12241,34.78163],[32.12101,34.78077],[32.11997,34.78188],[32.11263,34.77927],[32.1091,34.77735],[32.10835,34.77444],[32.1085,34.77578],[32.10753,34.77668],[32.10696,34.77508],[32.10657,34.77767],[32.10503,34.7772],[32.1059,34.77633],[32.10526,34.77554],[32.10914,34.7733],[32.10761,34.77325],[32.10446,34.77605],[32.10252,34.77585],[32.09895,34.77233],[32.09866,34.77371],[32.0967,34.7732],[32.09864,34.77188],[32.09812,34.77278],[32.09478,34.77197],[32.09441,34.76958],[32.09174,34.77061],[32.09081,34.76976],[32.09084,34.76821],[32.08879,34.76962],[32.08715,34.76903],[32.08734,34.76708],[32.08711,34.76824],[32.08512,34.76753],[32.08578,34.76651],[32.08771,34.76648],[32.08555,34.76642],[32.08477,34.76802],[32.08375,34.76658],[32.08023,34.76634],[32.07757,34.76462],[32.07631,34.76512],[32.07312,34.76327],[32.06934,34.76262],[32.06863,34.76121],[32.06221,34.75981],[32.05691,34.7562],[32.05566,34.75442],[32.05507,34.75116],[32.0513,34.74845],[32.05576,34.75006],[32.05227,34.7482],[32.05053,34.74828],[32.04749,34.74521],[32.04491,34.74421],[32.04394,34.74592],[32.03937,34.74465],[32.03822,34.74519],[32.03027,34.74067],[32.01093,34.73574],[31.94252,34.70798],[31.93517,34.7041],[31.9324,34.70052],[31.9248,34.69573],[31.92296,34.69307],[31.89936,34.68285],[31.84906,34.65836],[31.8481,34.65721],[31.84852,34.64464],[31.84779,34.64271],[31.84276,34.64255],[31.84278,34.65101],[31.84468,34.65098],[31.84549,34.65192],[31.84542,34.65631],[31.84324,34.65317],[31.84431,34.65564],[31.84185,34.65432],[31.84136,34.65269],[31.84084,34.65369],[31.83869,34.65267],[31.8439,34.65199],[31.83778,34.65203],[31.83881,34.65052],[31.83879,34.64679],[31.83606,34.64394],[31.83417,34.64395],[31.83423,34.65031],[31.83197,34.6503],[31.83144,34.63982],[31.8275,34.64788],[31.82633,34.64721],[31.82877,34.64127],[31.8269,34.64113],[31.82502,34.64572],[31.82382,34.64499],[31.82569,34.64046],[31.82482,34.63996],[31.82119,34.64397],[31.82034,34.643],[31.82185,34.64095],[31.82021,34.64283],[31.81836,34.64047],[31.82042,34.63714],[31.82542,34.63483],[31.82888,34.63525],[31.83427,34.63806],[31.83715,34.63673],[31.84411,34.63811],[31.84975,34.63736],[31.84974,34.63661],[31.84364,34.63755],[31.83738,34.63631],[31.83391,34.63722],[31.82569,34.63443],[31.82081,34.63644],[31.81788,34.64011],[31.81622,34.6398],[31.80088,34.63238],[31.79679,34.62876],[31.79626,34.62584],[31.79679,34.62759],[31.79606,34.62935],[31.79391,34.62881],[31.79309,34.62678],[31.79552,34.62562],[31.79834,34.62584],[31.79511,34.62532],[31.79247,34.62707],[31.75666,34.60758],[31.71537,34.58141],[31.68876,34.56331],[31.68813,34.56204],[31.68884,34.56166],[31.68795,34.56107],[31.6872,34.56195],[31.68692,34.56069],[31.68573,34.56091],[31.68554,34.55955],[31.68452,34.55964],[31.68346,34.55804],[31.68388,34.55609],[31.68248,34.55736],[31.68007,34.5555],[31.68146,34.55387],[31.68516,34.5559],[31.68172,34.55363],[31.67937,34.55454],[31.67711,34.55201],[31.67062,34.54894],[31.64573,34.53041],[31.64353,34.5274],[31.64262,34.52797],[31.63887,34.52403],[31.63849,34.52323],[31.63955,34.5212],[31.63844,34.52092],[31.63774,34.52373],[31.63677,34.5233],[31.6376,34.52096],[31.63665,34.52182],[31.63524,34.5204],[31.63701,34.51737],[31.63769,34.51895],[31.63804,34.51811],[31.64064,34.51989],[31.63714,34.51693],[31.63646,34.51782],[31.63417,34.51761],[31.63341,34.5194],[31.62868,34.51498],[31.60931,34.50203],[31.60159,34.49536]]];

	var D = root.dataset;
	var BROKER = D.mode === 'broker';
	var RM = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
	function wide() { return !!(window.matchMedia && window.matchMedia('(min-width:1024px)').matches); }

	/* ------------------------------------------------------------ small helpers */
	function lsGet(k) { try { var v = window.localStorage.getItem(k); return v ? JSON.parse(v) : null; } catch (e) { return null; } }
	function lsSet(k, v) { try { window.localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode: the page still works */ } }
	function ev(name, extra) { // analytics: the kind of action only, never a place, a listing or a person
		try {
			if (window.dataLayer && typeof window.dataLayer.push === 'function') {
				var o = { event: 'nf_' + name, nf_mode: BROKER ? 'broker' : 'portal' };
				if (extra) { for (var k in extra) { if (Object.prototype.hasOwnProperty.call(extra, k)) { o['nf_' + k] = extra[k]; } } }
				window.dataLayer.push(o);
			}
		} catch (e) { /* never break the page for analytics */ }
	}
	function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
	function norm(s) { return String(s || '').replace(/[־‐‑-]+/g, ' ').replace(/\s+/g, ' ').trim(); }
	function grp(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
	function nis(n) { return grp(n) + ' ₪'; }
	function mil(n) { return String(Math.round(n / 1e4) / 100); } // v3 fix: the old .replace(/\.?0+$/) turned 10, 20 and 30 million into "1", "2" and "3"
	function shortPrice(n, deal) {
		if (!(n > 0)) { return ''; }
		if (deal === 'rent') { return nis(n); }
		if (n >= 1e6) { return mil(n) + ' מ׳ ₪'; }
		return grp(Math.round(n / 1e3)) + ' אלף ₪';
	}
	function priceRange(list, deal) {
		var ps = list.map(function (x) { return x.price; }).filter(function (p) { return p > 0; });
		if (!ps.length) { return ''; }
		var lo = Math.min.apply(null, ps), hi = Math.max.apply(null, ps);
		if (lo === hi) { return shortPrice(lo, deal); }
		if (deal === 'rent') { return grp(lo) + '-' + grp(hi) + ' ₪'; }
		if (lo >= 1e6) { return mil(lo) + '-' + mil(hi) + ' מ׳ ₪'; }
		return shortPrice(lo, deal) + ' ומעלה';
	}
	function num(n) { return (Math.floor(n) === n) ? String(n) : String(Math.round(n * 10) / 10); }
	function cut(s, n) { s = String(s || ''); return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, '') + '…' : s; }

	/* distance: air distance first. Travel (secondary, the Better Law estimate): air km x 1.35 = road km; speed by road km
	   (<4: 20, <15: 28, <40: 45, else 70 km/h) + 4 minutes parking, rounded to 5, at least 5. Walking: road km at 4.8 km/h. */
	function km(a, b) {
		var R = 6371, t = Math.PI / 180, dLa = (b.lat - a.lat) * t, dLn = (b.lng - a.lng) * t;
		var x = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(a.lat * t) * Math.cos(b.lat * t) * Math.sin(dLn / 2) * Math.sin(dLn / 2);
		return 2 * R * Math.asin(Math.min(1, Math.sqrt(x)));
	}
	function driveRaw(air) { var road = air * 1.35; var v = road < 4 ? 20 : road < 15 ? 28 : road < 40 ? 45 : 70; return road / v * 60 + 4; }
	function r5(m) { return Math.max(5, Math.round(m / 5) * 5); }
	function drive(air) { return r5(driveRaw(air)); }
	function walk(air) { return r5(air * 1.35 / 4.8 * 60); }
	function dist(d) { // "850 מ׳", "2.4 ק״מ", "18 ק״מ"
		if (d < 1) { return Math.max(10, Math.round(d * 100) * 10) + ' מ׳'; }
		return (d < 10 ? String(Math.round(d * 10) / 10) : String(Math.round(d))) + ' ק״מ';
	}
	var seaCache = {};
	function seaKm(p) { // point to the coastline polyline, km (local flat projection; fine at these distances)
		var key = p.lat.toFixed(4) + ',' + p.lng.toFixed(4);
		if (seaCache[key] != null) { return seaCache[key]; }
		var best = 1e9, kx = 111.32 * Math.cos(p.lat * Math.PI / 180), ky = 110.54;
		for (var c = 0; c < COAST.length; c++) {
			var ch = COAST[c];
			for (var i = 0; i < ch.length - 1; i++) {
				var ax = (ch[i][1] - p.lng) * kx, ay = (ch[i][0] - p.lat) * ky, bx = (ch[i + 1][1] - p.lng) * kx, by = (ch[i + 1][0] - p.lat) * ky;
				var dx = bx - ax, dy = by - ay, L = dx * dx + dy * dy, t = L ? -(ax * dx + ay * dy) / L : 0;
				t = t < 0 ? 0 : t > 1 ? 1 : t;
				var x = ax + t * dx, y = ay + t * dy, d = Math.sqrt(x * x + y * y);
				if (d < best) { best = d; }
			}
		}
		seaCache[key] = best;
		return best;
	}
	function seaText(p) { // only within ~15 km of the coast; the coastline is simplified, so always "about"
		if (!COAST.length || !p || !isFinite(p.lat)) { return ''; }
		var d = seaKm(p);
		if (d > 15) { return ''; }
		return 'כ-' + (d < 1 ? Math.max(50, Math.round(d * 20) * 50) + ' מ׳' : dist(d)) + ' מהים';
	}

	/* ------------------------------------------------------------ state */
	var SLOTS = [
		{ k: 'work', name: 'עבודה', from: 'מהעבודה', add: 'עבודה' },
		{ k: 'parents', name: 'ההורים', from: 'מההורים', add: 'ההורים' },
		{ k: 'school', name: 'גן או בית ספר', from: 'מהגן או מבית הספר', add: 'גן או בית ספר' }
	];
	var STATUS = { marketing: 'בשיווק', construction: 'בבנייה', planning: 'בתכנון' };
	var PRICES = {
		sale: [[0, 'מחיר עד'], [3000000, 'עד 3 מ׳ ₪'], [5000000, 'עד 5 מ׳ ₪'], [8000000, 'עד 8 מ׳ ₪'], [15000000, 'עד 15 מ׳ ₪']],
		rent: [[0, 'מחיר עד'], [6000, 'עד 6,000 ₪'], [10000, 'עד 10,000 ₪'], [15000, 'עד 15,000 ₪'], [25000, 'עד 25,000 ₪']]
	};
	function fBlank() { return { mamad: false, rooms: 0, rmax: 0, smin: 0, smax: 0, fmin: null, fmax: null, elev: false, park: false, balc: false, mkt: false, near: 0 }; }
	var S = {
		tab: D.deal === 'rent' ? 'rent' : 'sale',
		L: [], P: [], byKey: {}, loaded: false,
		origin: null,
		f: fBlank(),
		fp: { sale: { min: 0, max: 0 }, rent: { min: 0, max: 0 } }, // v3: the price range, kept apart for sale and for rent
		zone: null, iso: null, sh: null, // v3: the drawn zone, the travel-time area, the open side sheet ('f' filters | 't' travel)
		anchors: {}, visit: [],
		bounds: null, group: null, shown: 30,
		picking: null, measure: null, map: null, mapState: 'off', places: [], card: null, opener: null, dropUntil: 0
	};
	(function () {
		var a = lsGet('nlnf_places_v1');
		if (a && typeof a === 'object') { SLOTS.forEach(function (s) { var p = a[s.k]; if (p && isFinite(p.lat) && isFinite(p.lng)) { S.anchors[s.k] = { lat: +p.lat, lng: +p.lng }; } }); }
		var v = lsGet('nlnf_visit_v1');
		if (Array.isArray(v)) { S.visit = v.filter(function (k) { return typeof k === 'string'; }).slice(0, 6); }
	})();
	/* v2: alerts (portal pages only) */
	var NA = (function () {
		var c = document.getElementById('nlna-cfg');
		if (!c || BROKER || !window.fetch) { return null; }
		try { var j = JSON.parse(c.textContent || '{}'); return j && j.api && j.items ? j : null; } catch (e) { return null; }
	})();
	var SAVE = !BROKER; // the heart: a device-only saved list on portal pages, with or without email alerts (alerts ship dormant)
	S.saved = (function () { var v = lsGet('nlnf_saved_v1'); return Array.isArray(v) ? v.filter(function (k) { return typeof k === 'string' && /^[lp]\d+$/.test(k); }).slice(0, 60) : []; })();
	S.sub = (function () { var v = lsGet('nlnf_alert_v1'); return v && v.s > 0 && typeof v.k === 'string' ? { s: +v.s, k: v.k } : null; })();
	function saveSaved() { lsSet('nlnf_saved_v1', S.saved); }
	function isSaved(key) { return S.saved.indexOf(key) > -1; }
	function savedIds(t) { return S.saved.filter(function (k) { return k.charAt(0) === t; }).map(function (k) { return +k.slice(1); }); }
	function saveAnchors() { lsSet('nlnf_places_v1', S.anchors); }
	function saveVisit() { lsSet('nlnf_visit_v1', S.visit); }
	function firstAnchor() { for (var i = 0; i < SLOTS.length; i++) { if (S.anchors[SLOTS[i].k]) { return SLOTS[i]; } } return null; }
	function drop() { if (!RM) { S.dropUntil = Date.now() + 1400; } }

	/* ------------------------------------------------------------ the frame */
	var ICON_SEARCH = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true" focusable="false"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-4-4"></path></svg>';
	var ICON_ME = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v4M12 18v4M2 12h4M18 12h4"></path></svg>';
	function bell(s) { s = s || 18; return '<svg width="' + s + '" height="' + s + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true" focusable="false"><path d="M6 17v-6a6 6 0 0 1 12 0v6l2 2H4z"></path><path d="M10 21h4"></path></svg>'; }
	function heart(on, s) { s = s || 20; return '<svg width="' + s + '" height="' + s + '" viewBox="0 0 24 24" fill="' + (on ? 'currentColor' : 'none') + '" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M12 20.5l-1.2-1.1C6 15.1 3 12.4 3 9.1 3 6.4 5.1 4.3 7.8 4.3c1.5 0 3 .7 4.2 1.9 1.2-1.2 2.7-1.9 4.2-1.9 2.7 0 4.8 2.1 4.8 4.8 0 3.3-3 6-7.8 10.3z"></path></svg>'; }
	root.removeAttribute('aria-busy');
	root.innerHTML =
		'<div class="nlnf__ctrl">'
		+ '<div class="nlnf__search">'
		+ '<label class="nlnf__box"><span class="nlnf__sr">עיר או שכונה</span>' + ICON_SEARCH
		+ '<input type="search" id="nlnf-q" placeholder="עיר או שכונה" autocomplete="off" spellcheck="false" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="nlnf-sug"></label>'
		+ '<button type="button" class="nlnf__me" id="nlnf-me">' + ICON_ME + '<span>המיקום שלי</span></button>'
		+ '<ul class="nlnf__sug" id="nlnf-sug" role="listbox" aria-label="ערים ושכונות" hidden></ul>'
		+ '</div>'
		+ '<p class="nlnf__msg" id="nlnf-msg" role="status" aria-live="polite" hidden></p>'
		+ '<div class="nlnf__tabs' + (BROKER ? ' nlnf__tabs--2' : '') + '" role="tablist" aria-label="מה מחפשים">'
		+ '<button type="button" role="tab" id="nlnf-t-sale" data-tab="sale">למכירה</button>'
		+ '<button type="button" role="tab" id="nlnf-t-rent" data-tab="rent">להשכרה</button>'
		+ (BROKER ? '' : '<button type="button" role="tab" id="nlnf-t-new" data-tab="new">פרויקטים חדשים</button>')
		+ '</div>'
		+ '<div class="nlnf__chips" id="nlnf-chips" role="group" aria-label="סינון"></div>'
		+ '<div class="nlnf__places" id="nlnf-places" role="group" aria-labelledby="nlnf-places-l"></div>'
		+ '</div>'
		+ '<div class="nlnf__mapwrap" id="nlnf-mapwrap">'
		+ '<div class="nlnf__map" id="nlnf-map" role="region" aria-label="מפת הדירות"></div>'
		+ '<button type="button" class="nlnf__area" id="nlnf-area" hidden>חפשו באזור הזה</button>'
		+ '<div class="nlnf__tools" id="nlnf-tools"><button type="button" class="nlnf__ruler" id="nlnf-ruler" aria-pressed="false">מדדו מרחק</button>'
		+ '<button type="button" class="nlnf__ruler nlnf__draw" id="nlnf-draw" aria-pressed="false">ציירו אזור</button>'
		+ '<button type="button" class="nlnf__ruler nlnf__fs" id="nlnf-fs" aria-haspopup="dialog" aria-controls="nlnf-dlg" hidden>מסך מלא</button></div>'
		+ '<div class="nlnf__pad" id="nlnf-pad" hidden><svg aria-hidden="true" focusable="false"><polyline id="nlnf-pad-l" points=""></polyline></svg></div>'
		+ '<div class="nlnf__pick" id="nlnf-pick" hidden><span id="nlnf-pick-t"></span><button type="button" id="nlnf-pick-x">ביטול</button></div>'
		+ '<div class="nlnf__pick nlnf__pick--m" id="nlnf-drw" hidden><span id="nlnf-drw-t" aria-live="polite"></span><button type="button" id="nlnf-drw-x">ביטול</button></div>'
		+ '<div class="nlnf__pick nlnf__pick--m" id="nlnf-meas" hidden><span id="nlnf-meas-t" aria-live="polite"></span><button type="button" id="nlnf-meas-x">סיום</button></div>'
		+ '<div class="nlnf__legend" id="nlnf-legend" aria-hidden="true"></div>'
		+ '</div>'
		+ '<div class="nlnf__panel" id="nlnf-panel" role="tabpanel" aria-labelledby="nlnf-t-sale">'
		+ '<button type="button" class="nlnf__grab" id="nlnf-grab" aria-controls="nlnf-panel" tabindex="-1" aria-hidden="true"><span></span></button>'
		+ '<div class="nlnf__listhead"><h3 class="nlnf__count" id="nlnf-count" aria-live="polite"></h3><span class="nlnf__sort" id="nlnf-sort"></span></div>'
		+ '<div class="nlnf__scope" id="nlnf-scope"></div>'
		+ (NA ? '<div class="nlnf__alert" id="nlnf-alrow" hidden><button type="button" class="nlnf-alertbtn" data-al="open" aria-haspopup="dialog">' + bell() + '<span>התריעו לי על האזור הזה</span></button></div>' : '')
		+ (SAVE ? '<div class="nlnf__savedgo" id="nlnf-savedgo" hidden><button type="button" class="nlnf-link" data-saved="go"></button></div>' : '')
		+ '<ol class="nlnf__list" id="nlnf-list"></ol>'
		+ '<div class="nlnf__empty" id="nlnf-empty" hidden></div>'
		+ '<div class="nlnf__few" id="nlnf-few" hidden></div>'
		+ '<button type="button" class="nlnf__more" id="nlnf-more" hidden>הציגו עוד</button>'
		+ (SAVE ? '<section class="nlnf__visit nlnf__saved" id="nlnf-saved" aria-labelledby="nlnf-saved-h" hidden></section>' : '')
		+ '<section class="nlnf__visit" id="nlnf-visit" aria-labelledby="nlnf-visit-h" hidden></section>'
		+ '<p class="nlnf__note">המרחקים בקו אווירי. זמני נסיעה והליכה בכרטיס: הערכה, בלי פקקים. המיקום שלכם נשאר במכשיר. רק כשתבקשו סינון לפי זמן נסיעה, הנקודה שבחרתם נשלחת ל־Mapbox: זמני הנסיעה מחושבים אצל Mapbox.</p>'
		+ '</div>'
		+ '<div class="nlnf__card" id="nlnf-card" role="dialog" aria-labelledby="nlnf-card-t" hidden></div>'
		+ (NA ? '<div class="nlnf__al" id="nlnf-al" role="dialog" aria-labelledby="nlnf-al-t" hidden></div>' : '')
		+ '<div class="nlnf__al nlnf__sh" id="nlnf-sh" role="dialog" aria-labelledby="nlnf-sh-t" hidden></div>';
	function $(id) { return document.getElementById(id); }
	var el = {
		q: $('nlnf-q'), me: $('nlnf-me'), sug: $('nlnf-sug'), msg: $('nlnf-msg'), chips: $('nlnf-chips'), places: $('nlnf-places'),
		mapwrap: $('nlnf-mapwrap'), map: $('nlnf-map'), area: $('nlnf-area'), ruler: $('nlnf-ruler'), pick: $('nlnf-pick'), pickT: $('nlnf-pick-t'), pickX: $('nlnf-pick-x'),
		meas: $('nlnf-meas'), measT: $('nlnf-meas-t'), measX: $('nlnf-meas-x'),
		legend: $('nlnf-legend'), panel: $('nlnf-panel'), count: $('nlnf-count'), sort: $('nlnf-sort'), scope: $('nlnf-scope'),
		list: $('nlnf-list'), empty: $('nlnf-empty'), more: $('nlnf-more'), visit: $('nlnf-visit'), card: $('nlnf-card'),
		alrow: $('nlnf-alrow'), al: $('nlnf-al'), saved: $('nlnf-saved'), savedgo: $('nlnf-savedgo'),
		draw: $('nlnf-draw'), pad: $('nlnf-pad'), padL: $('nlnf-pad-l'), drw: $('nlnf-drw'), drwT: $('nlnf-drw-t'), drwX: $('nlnf-drw-x'),
		grab: $('nlnf-grab'), sh: $('nlnf-sh'), tools: $('nlnf-tools'), fs: $('nlnf-fs'), few: $('nlnf-few')
	};
	// the owners' quiet line (printed by the server next to the app, portal pages only) moves into the list's footer
	var holder = root.closest('.nlnf');
	var own = holder && holder.querySelector('.nlnf__own');
	if (own) { el.panel.appendChild(own); }
	function say(t) { if (!t) { el.msg.hidden = true; el.msg.textContent = ''; return; } el.msg.textContent = t; el.msg.hidden = false; }

	/* ------------------------------------------------------------ data */
	function prep(d) {
		S.L = (d.listings || []).map(function (x) {
			var o = {}; for (var k in x) { o[k] = x[k]; }
			o.t = 'l'; o.key = 'l' + x.id;
			o.has = x.lat != null && x.lng != null && isFinite(x.lat) && isFinite(x.lng);
			o.place = x.hood || x.city || '';
			o.near = x.approx === 'hood' || x.approx === 'city'; // placed at the neighbourhood or the city: distances are "about"
			if (BROKER) { o.promoted = false; } // a broker's own page carries no ads
			return o;
		});
		S.P = BROKER ? [] : (d.projects || []).map(function (x) {
			var o = {}; for (var k in x) { o[k] = x[k]; }
			o.t = 'p'; o.key = 'p' + x.id; o.has = isFinite(x.lat) && isFinite(x.lng); o.near = !x.exact;
			return o;
		});
		/* v4 (HAD-793, 19.11.2026): the city medians the server sends (Tax Authority closed deals, the site's own value.json) */
		S.A = BROKER ? [] : (d.areas || []).filter(function (a) { return a && a.n && isFinite(a.lat) && isFinite(a.lng) && a.r4 > 0; });
		S.asrc = d.areas_src || null;
		S.byKey = {};
		S.L.concat(S.P).forEach(function (x) { S.byKey[x.key] = x; });
		S.visit = S.visit.filter(function (k) { return !!S.byKey[k]; });
		// the place box: the data's own neighbourhoods and cities only (no free-text lookup)
		var m = {};
		function add(name, kind, sub, lat, lng) {
			var k = kind + '|' + norm(name);
			if (!name || !isFinite(lat) || !isFinite(lng)) { return; }
			if (!m[k]) { m[k] = { name: name, kind: kind, sub: sub, la: 0, ln: 0, n: 0 }; }
			m[k].la += lat; m[k].ln += lng; m[k].n++;
		}
		S.L.forEach(function (x) {
			if (!x.has) { return; }
			if (x.approx === 'hood' && x.area) { add(x.area, 'hood', x.city, x.lat, x.lng); }
			else if (!x.approx && x.hood) { add(x.hood, 'hood', x.city, x.lat, x.lng); }
			if (x.city) { add(x.city, 'city', '', x.lat, x.lng); }
		});
		S.P.forEach(function (x) { if (x.has && x.city) { add(x.city, 'city', '', x.lat, x.lng); } });
		S.places = Object.keys(m).map(function (k) { var p = m[k]; return { name: p.name, kind: p.kind, sub: p.sub, lat: p.la / p.n, lng: p.ln / p.n, n: p.n }; })
			.sort(function (a, b) { return (a.kind === b.kind ? 0 : a.kind === 'hood' ? -1 : 1) || b.n - a.n; });
		S.loaded = true;
	}

	/* ------------------------------------------------------------ what is shown */
	function pool() { return S.tab === 'new' ? S.P : S.L.filter(function (x) { return x.deal === S.tab; }); }
	function inBounds(x) { var b = S.bounds; return x.has && x.lat >= b.s && x.lat <= b.n && x.lng >= b.w && x.lng <= b.e; }
	function passes(x, noScope) { // a fact the listing does not state never passes a filter on that fact
		if (x.t === 'l') {
			var F = S.f, pp = S.fp[x.deal] || {};
			if (F.mamad && !x.mamad) { return false; }
			if (F.rooms && !(x.rooms >= F.rooms)) { return false; }
			if (F.rmax && !(x.rooms > 0 && x.rooms <= F.rmax)) { return false; }
			if (pp.min && !(x.price > 0 && x.price >= pp.min)) { return false; }
			if (pp.max && !(x.price > 0 && x.price <= pp.max)) { return false; }
			if (F.smin && !(x.sqm > 0 && x.sqm >= F.smin)) { return false; }
			if (F.smax && !(x.sqm > 0 && x.sqm <= F.smax)) { return false; }
			if (F.fmin != null && !(x.floor != null && x.floor >= F.fmin)) { return false; }
			if (F.fmax != null && !(x.floor != null && x.floor <= F.fmax)) { return false; }
			if (F.elev && x.elevator !== true) { return false; }
			if (F.park && x.parking !== true) { return false; }
			if (F.balc && !(x.balcony > 0)) { return false; }
		} else if (S.f.mkt && x.status !== 'marketing') { return false; }
		if (S.f.near) { var a = firstAnchor(); if (a && !(x.has && km(x, S.anchors[a.k]) <= S.f.near)) { return false; } }
		if (S.zone && !(x.has && inRing(x, S.zone))) { return false; } // v3: the drawn zone and the travel-time area filter the map too
		if (S.iso && !(x.has && inIso(x))) { return false; }
		if (!noScope) {
			if (S.bounds && !inBounds(x)) { return false; }
			if (S.group && S.group.keys.indexOf(x.key) < 0) { return false; }
		}
		return true;
	}
	function metric(x) { // distance first: from me (or the chosen place), else from my first place
		if (S.origin) { return x.has ? km(x, S.origin) : 1e9; }
		var a = firstAnchor();
		if (a) { return x.has ? km(x, S.anchors[a.k]) : 1e9; }
		return null;
	}
	var SR = { marketing: 0, construction: 1, planning: 2 };
	function results() {
		var a = pool().filter(function (x) { return passes(x); });
		var withM = a.map(function (x, i) { return { x: x, i: i, m: metric(x) }; });
		withM.sort(function (p, q) {
			if (!!p.x.promoted !== !!q.x.promoted) { return p.x.promoted ? -1 : 1; } // a paid listing first, inside what the visitor chose
			if (p.m != null && q.m != null && p.m !== q.m) { return p.m - q.m; }
			if (p.x.t === 'p') {
				var ps = SR[p.x.status] != null ? SR[p.x.status] : 3, qs = SR[q.x.status] != null ? SR[q.x.status] : 3;
				if (ps !== qs) { return ps - qs; }
				if (p.x.units !== q.x.units) { return (q.x.units || 0) - (p.x.units || 0); }
			}
			return p.i - q.i;
		});
		return withM.map(function (w) { return w.x; });
	}
	function fromText(x) { // the main fact: how far
		var ab = x.near ? 'כ-' : '';
		if (S.origin && x.has) { return ab + dist(km(x, S.origin)) + (S.origin.kind === 'me' ? ' ממך' : ' מ' + S.origin.label); }
		var a = firstAnchor();
		if (a && x.has) { return ab + dist(km(x, S.anchors[a.k])) + ' ' + a.from; }
		return '';
	}
	var AD = '<span class="nlnf-ad">מודעה מקודמת</span>';
	function sideOf(x) {
		if (x.t === 'l') {
			if (!(x.price > 0)) { return ''; }
			var sub = x.deal === 'rent' ? 'לחודש' : (x.psqm > 0 ? nis(x.psqm) + ' למ״ר' : (x.sqm > 0 ? nis(x.price / x.sqm) + ' למ״ר' : ''));
			return '<bdi class="nlnf-row__p">' + esc(nis(x.price)) + '</bdi>' + (sub ? '<bdi class="nlnf-row__s">' + esc(sub) + '</bdi>' : '');
		}
		if (x.psqm > 0) { return '<bdi class="nlnf-row__p">' + esc(nis(x.psqm)) + '</bdi><bdi class="nlnf-row__s">למ״ר, מחיר מוערך</bdi>'; }
		return '';
	}
	function metaOf(x) {
		var parts = [];
		if (x.t === 'l') { parts.push(x.place); }
		else { parts.push(x.city); if (STATUS[x.status]) { parts.push(STATUS[x.status]); } }
		var fr = fromText(x);
		if (fr) { parts.push(fr); } else if (x.t === 'l') { parts.push(x.ptype); } else if (x.units > 0) { parts.push(x.units + ' דירות'); }
		var sea = x.has ? seaText(x) : '';
		if (sea) { parts.push(sea); }
		return parts.filter(Boolean).map(esc).join(' · ');
	}
	function countText(n) {
		var t;
		if (S.tab === 'new') { t = n === 1 ? 'פרויקט אחד' : grp(n) + ' פרויקטים'; }
		else { t = (n === 1 ? 'נכס אחד ' : grp(n) + ' נכסים ') + (S.tab === 'rent' ? 'להשכרה' : 'למכירה'); }
		return t + (S.zone ? ' באזור שציירתם' : (S.bounds ? ' באזור הזה' : ''));
	}
	function sortText() {
		if (S.origin) { return (S.origin.kind === 'me' ? 'לפי המרחק ממך' : 'לפי המרחק מ' + S.origin.label) + ', בקו אווירי'; }
		var a = firstAnchor();
		if (a) { return 'לפי המרחק ' + a.from + ', בקו אווירי'; }
		return '';
	}

	/* v4 (HAD-793, gap 25/31 of the long film): while the site holds only a few listings, the map of the whole country looked empty.
	   With FEW or fewer listings of the open tab (before any filter) the map also shows what the site really has: the new projects as a
	   quiet background layer, the median deal price of a 4-room home per city (sale tab), and the list ends with "what else is here".
	   Nothing is invented: every label is a real project or a published median, and the block counts only real items. */
	var FEW = 8;
	function few() { return !BROKER && S.loaded && S.tab !== 'new' && pool().length <= FEW; }
	var QM = { '1-3': 'ינואר עד מרץ', '4-6': 'אפריל עד יוני', '7-9': 'יולי עד ספטמבר', '10-12': 'אוקטובר עד דצמבר' };
	function qText(q) { var m = /^(\d{1,2}-\d{1,2})\.(\d{4})$/.exec(String(q || '')); return m && QM[m[1]] ? QM[m[1]] + ' ' + m[2] : String(q || ''); }
	function projOnMap() { return S.P.filter(function (x) { return x.has; }); }
	function renderFew() {
		if (!el.few) { return; }
		if (!few()) { el.few.hidden = true; el.few.innerHTML = ''; return; }
		var np = projOnMap().length, q = S.A.length ? qText(S.A[0].q) : '';
		var h = '<p class="nlnf-few__h">המודעות באתר רק מתחילות. בינתיים, מה עוד יש על המפה</p><ul class="nlnf-few__l">';
		if (np) { h += '<li><button type="button" class="nlnf-few__go" data-few="new"><span>פרויקטים חדשים על המפה</span><b class="nlnf-few__n">' + grp(np) + '</b></button></li>'; }
		if (S.tab === 'sale' && S.A.length) { h += '<li><a class="nlnf-few__go" href="/apartment-prices/"><span>מחירי דירות לפי עיר</span><small>חציון 4 חדרים, ' + esc(q) + '</small></a></li>'; }
		if (NA) { h += '<li><button type="button" class="nlnf-few__go" data-al="open" aria-haspopup="dialog"><span>התריעו לי כשתעלה כאן דירה</span>' + bell(16) + '</button></li>'; }
		h += '<li><a class="nlnf-few__go is-pri" href="/post-listing/"><span>יש לכם דירה? פרסמו בחינם</span></a></li></ul>';
		if (S.tab === 'sale' && S.A.length && S.asrc) { h += '<p class="nlnf-few__src">המחירים על המפה: ' + esc(S.asrc) + '.</p>'; }
		el.few.innerHTML = h; el.few.hidden = false;
	}
	function renderList() {
		var r = results();
		el.panel.setAttribute('aria-labelledby', 'nlnf-t-' + S.tab);
		el.sort.textContent = sortText();
		var sc = '';
		if (S.bounds) { sc += '<button type="button" class="nlnf-scope" data-scope="bounds">רק מה שעל המפה <span aria-hidden="true">×</span><span class="nlnf__sr">, ביטול</span></button>'; }
		if (S.group) { sc += '<button type="button" class="nlnf-scope" data-scope="group">' + esc(S.group.label) + ' <span aria-hidden="true">×</span><span class="nlnf__sr">, ביטול</span></button>'; }
		if (S.zone) { sc += '<button type="button" class="nlnf-scope" data-scope="zone">באזור שציירתם <span aria-hidden="true">×</span><span class="nlnf__sr">, ניקוי אזור</span></button>'; }
		if (S.iso) { sc += '<button type="button" class="nlnf-scope" data-scope="iso">' + esc(isoText(S.iso)) + ' <span aria-hidden="true">×</span><span class="nlnf__sr">, ביטול</span></button>'; }
		el.scope.innerHTML = sc;
		el.scope.hidden = !sc;
		if (el.alrow) { el.alrow.hidden = !S.loaded; }
		if (!S.loaded) { return r; }
		if (!r.length) {
			el.count.textContent = S.tab === 'new' ? 'פרויקטים' : (S.tab === 'rent' ? 'נכסים להשכרה' : 'נכסים למכירה');
			el.list.innerHTML = '';
			el.more.hidden = true;
			el.empty.hidden = false;
			renderFew();
			el.empty.innerHTML = (S.tab === 'new' || BROKER)
				? '<p>לא מצאנו כאן התאמה. הרחיבו את האזור או נקו את הסינון.</p><div class="nlnf-empty__go"><button type="button" class="nlnf-btn" data-empty="wide">הרחיבו את האזור</button></div>'
				: '<p>לא מצאנו כאן התאמה. הרחיבו את האזור או עברו לפרויקטים חדשים.</p><div class="nlnf-empty__go"><button type="button" class="nlnf-btn" data-empty="wide">הרחיבו את האזור</button><button type="button" class="nlnf-btn" data-empty="new">לפרויקטים חדשים</button></div>';
			return r;
		}
		el.empty.hidden = true;
		el.count.textContent = countText(r.length);
		var h = '';
		r.slice(0, S.shown).forEach(function (x) {
			h += '<li><button type="button" class="nlnf-row' + (S.card && S.card.key === x.key ? ' is-on' : '') + '" data-key="' + esc(x.key) + '">'
				+ '<span class="nlnf-row__main"><span class="nlnf-row__t">' + (SAVE && isSaved(x.key) && (x.t === 'l' || NA) ? '<span class="nlnf-row__sv">' + (x.t === 'l' ? heart(true, 14) : bell(14)) + '<span class="nlnf__sr">' + (x.t === 'l' ? 'שמור, ' : 'במעקב, ') + '</span></span>' : '') + esc(x.title) + '</span>'
				+ '<span class="nlnf-row__m">' + metaOf(x) + (x.promoted ? ' ' + AD : '') + '</span></span>'
				+ '<span class="nlnf-row__side">' + sideOf(x) + '</span></button></li>';
		});
		el.list.innerHTML = h;
		el.more.hidden = r.length <= S.shown;
		renderFew();
		return r;
	}

	/* ------------------------------------------------------------ controls */
	function opt(list, val) { return list.map(function (o) { return '<option value="' + o[0] + '"' + (o[0] === val ? ' selected' : '') + '>' + esc(o[1]) + '</option>'; }).join(''); }
	function withVal(list, val, label) { // a quick list that also holds a value the full filters chose
		if (!val || list.some(function (o) { return o[0] === val; })) { return list; }
		return list.concat([[val, label]]).sort(function (a, b) { return a[0] - b[0]; });
	}
	function priceLabel(n, deal) { return deal === 'rent' ? nis(n) : shortPrice(n, 'sale'); }
	function moreCount() { // the filters that live only in the full sheet (the quick chips show the rest)
		var F = S.f, pp = S.fp[S.tab] || {};
		return (F.rmax ? 1 : 0) + (pp.min ? 1 : 0) + (F.smin || F.smax ? 1 : 0) + (F.fmin != null || F.fmax != null ? 1 : 0) + (F.elev ? 1 : 0) + (F.park ? 1 : 0) + (F.balc ? 1 : 0);
	}
	function renderChips() {
		var h = '';
		if (S.tab !== 'new') {
			var pm = S.fp[S.tab].max, more = moreCount();
			h += '<button type="button" class="nlnf-chip" data-f="mamad" aria-pressed="' + (S.f.mamad ? 'true' : 'false') + '">ממ״ד</button>';
			h += '<label class="nlnf-chip nlnf-chip--sel' + (S.f.rooms ? ' is-on' : '') + '"><span class="nlnf__sr">חדרים</span><select data-f="rooms">' + opt(withVal([[0, 'חדרים'], [3, '3 חדרים ומעלה'], [4, '4 חדרים ומעלה'], [5, '5 חדרים ומעלה']], S.f.rooms, num(S.f.rooms) + ' חדרים ומעלה'), S.f.rooms) + '</select></label>';
			h += '<label class="nlnf-chip nlnf-chip--sel' + (pm ? ' is-on' : '') + '"><span class="nlnf__sr">מחיר עד</span><select data-f="pmax">' + opt(withVal(PRICES[S.tab], pm, 'עד ' + priceLabel(pm, S.tab)), pm) + '</select></label>';
			h += '<button type="button" class="nlnf-chip' + (more ? ' is-on' : '') + '" data-sh="f" aria-haspopup="dialog">סינון נוסף' + (more ? '<span class="nlnf-chip__n">' + more + '</span><span class="nlnf__sr"> סינונים פעילים</span>' : '') + '</button>';
		} else {
			h += '<button type="button" class="nlnf-chip" data-f="mkt" aria-pressed="' + (S.f.mkt ? 'true' : 'false') + '">בשיווק עכשיו</button>';
		}
		h += '<button type="button" class="nlnf-chip' + (S.iso ? ' is-on' : '') + '" data-sh="t" aria-haspopup="dialog">זמן נסיעה</button>';
		var a = firstAnchor();
		if (a) {
			h += '<label class="nlnf-chip nlnf-chip--sel' + (S.f.near ? ' is-on' : '') + '"><span class="nlnf__sr">מרחק ' + esc(a.from) + '</span><select data-f="near">'
				+ opt([[0, 'מרחק ' + a.from], [1, 'עד 1 ק״מ ' + a.from], [2, 'עד 2 ק״מ ' + a.from], [5, 'עד 5 ק״מ ' + a.from], [10, 'עד 10 ק״מ ' + a.from]], S.f.near) + '</select></label>';
		} else { S.f.near = 0; }
		el.chips.innerHTML = h;
	}
	function renderPlaces() {
		var h = '<span class="nlnf__label" id="nlnf-places-l">המקומות שלי</span>';
		SLOTS.forEach(function (s) {
			if (S.anchors[s.k]) {
				h += '<span class="nlnf-place is-set"><button type="button" class="nlnf-place__b" data-slot="' + s.k + '" title="סמנו מחדש">' + esc(s.name) + '</button>'
					+ '<button type="button" class="nlnf-place__x" data-unslot="' + s.k + '" aria-label="הסירו: ' + esc(s.name) + '">×</button></span>';
			} else {
				h += '<button type="button" class="nlnf-place" data-slot="' + s.k + '">+ ' + esc(s.add) + '</button>';
			}
		});
		el.places.innerHTML = h;
	}
	function renderTabs() {
		[].forEach.call(root.querySelectorAll('[role=tab]'), function (b) {
			var on = b.getAttribute('data-tab') === S.tab;
			b.setAttribute('aria-selected', on ? 'true' : 'false');
			b.tabIndex = on ? 0 : -1;
		});
	}
	function renderLegend() {
		var h = S.tab === 'new' ? '<span><i class="nlnf-lg nlnf-lg--new"></i>פרויקט חדש</span>'
			: (S.tab === 'rent' ? '<span><i class="nlnf-lg nlnf-lg--rent"></i>להשכרה</span>' : '<span><i class="nlnf-lg nlnf-lg--sale"></i>למכירה</span>')
			+ '<span><i class="nlnf-lg nlnf-lg--area"></i>המיקום לפי השכונה</span>';
		if (few()) {
			h += '<span><i class="nlnf-lg nlnf-lg--ctx"></i>פרויקט חדש</span>';
			if (S.tab === 'sale' && S.A.length) { h += '<span><i class="nlnf-lg nlnf-lg--med"></i>חציון 4 חד׳ בעיר</span>'; }
		}
		if (firstAnchor()) { h += '<span><i class="nlnf-lg nlnf-lg--anc"></i>המקומות שלכם</span>'; }
		if (S.zone) { h += '<span><i class="nlnf-lg nlnf-lg--zone"></i>האזור שציירתם</span>'; }
		if (S.iso) { h += '<span><i class="nlnf-lg nlnf-lg--iso"></i>' + (S.iso.est ? 'זמן נסיעה, הערכה' : 'זמן נסיעה') + '</span>'; }
		el.legend.innerHTML = h;
	}
	function renderVisit() {
		if (!S.visit.length) { el.visit.hidden = true; el.visit.innerHTML = ''; return; }
		var items = S.visit.map(function (k) { return S.byKey[k]; }).filter(Boolean);
		// nearest neighbour from me (or the chosen place), else from the first one added
		var left = items.filter(function (x) { return x.has; }), order = [], at = S.origin, tot = 0, totKm = 0, first = 0;
		if (!at && left.length) { at = left.shift(); order.push(at); }
		while (left.length) {
			var bi = 0, bd = 1e9;
			for (var i = 0; i < left.length; i++) { var dd = km(at, left[i]); if (dd < bd) { bd = dd; bi = i; } }
			if (order.length) { tot += driveRaw(bd); totKm += bd; } else { first = bd; } // the leg from me is not "between them"
			at = left.splice(bi, 1)[0];
			order.push(at);
		}
		order = order.concat(items.filter(function (x) { return !x.has; }));
		var h = '<div class="nlnf-visit__head"><h3 id="nlnf-visit-h">יום ביקורים · ' + order.length + '</h3><button type="button" class="nlnf-link" data-visit="clear">ניקוי</button></div><ol class="nlnf-visit__list">';
		order.forEach(function (x, i) {
			var go = x.t === 'p' && x.exact && x.has
				? '<a class="nlnf-link nlnf-link--s" href="https://waze.com/ul?ll=' + x.lat + ',' + x.lng + '&amp;navigate=yes" target="_blank" rel="noopener" data-waze="1">נווטו ב-Waze</a>'
				: (x.t === 'l' ? '<span class="nlnf-visit__fine">כתובת מדויקת מהמפרסם</span>' : '');
			h += '<li><span class="nlnf-visit__n">' + (i + 1) + '</span><span class="nlnf-visit__t"><a href="' + esc(x.url) + '">' + esc(cut(x.title, 60)) + '</a>' + go + '</span>'
				+ '<button type="button" class="nlnf-visit__x" data-unvisit="' + esc(x.key) + '" aria-label="הסירו מיום הביקורים: ' + esc(cut(x.title, 40)) + '">×</button></li>';
		});
		h += '</ol>';
		var placed = order.filter(function (x) { return x.has; }).length;
		if (placed > 1 && totKm > 0) { h += '<p class="nlnf-visit__tot"><bdi>' + dist(totKm) + ' בין כולם, בקו אווירי</bdi> · כ-' + r5(tot) + ' דק׳ נסיעה, הערכה בלי פקקים</p>'; }
		else if (placed === 1 && S.origin && first > 0) { h += '<p class="nlnf-visit__tot"><bdi>' + dist(first) + (S.origin.kind === 'me' ? ' ממך' : ' מ' + esc(S.origin.label)) + ', בקו אווירי</bdi> · כ-' + drive(first) + ' דק׳ נסיעה, הערכה</p>'; }
		el.visit.innerHTML = h;
		el.visit.hidden = false;
	}
	function renderSaved() { // "השמורים שלי": the hearts saved on this device (a project only while alerts are on); never sent anywhere
		if (!el.saved) { return; }
		var items = S.saved.map(function (k) { return S.byKey[k]; }).filter(function (x) { return x && (x.t === 'l' || NA); });
		if (el.savedgo) { el.savedgo.hidden = !items.length; el.savedgo.firstChild.textContent = 'השמורים שלי · ' + items.length; }
		if (!items.length) { el.saved.hidden = true; el.saved.innerHTML = ''; return; }
		var h = '<div class="nlnf-visit__head"><h3 id="nlnf-saved-h" tabindex="-1">השמורים שלי · ' + items.length + '</h3></div><ol class="nlnf-visit__list">';
		items.forEach(function (x) {
			var fact = x.t === 'l' ? (x.price > 0 ? nis(x.price) + (x.deal === 'rent' ? ' לחודש' : '') : '') : (STATUS[x.status] || '');
			var sub = [x.t === 'l' ? x.place : x.city, fact].filter(Boolean).join(' · ');
			h += '<li><span class="nlnf-saved__i" aria-hidden="true">' + (x.t === 'l' ? heart(true, 16) : bell(16)) + '</span><span class="nlnf-visit__t">'
				+ '<button type="button" class="nlnf-saved__open" data-key="' + esc(x.key) + '">' + esc(cut(x.title, 60)) + '</button>' + (sub ? '<span class="nlnf-visit__fine">' + esc(sub) + '</span>' : '') + '</span>'
				+ '<button type="button" class="nlnf-visit__x" data-unsave="' + esc(x.key) + '" aria-label="הסירו מהשמורים: ' + esc(cut(x.title, 40)) + '">×</button></li>';
		});
		el.saved.innerHTML = h + '</ol><p class="nlnf-visit__tot">נשמר במכשיר הזה בלבד.</p>';
		el.saved.hidden = false;
	}
	function renderAll() { renderTabs(); renderChips(); renderPlaces(); renderLegend(); var r = renderList(); renderSaved(); renderVisit(); drawMap(r); }

	/* ------------------------------------------------------------ the card */
	function openCard(x, opener) {
		S.card = x; S.opener = opener || null;
		ev('card', { type: x.t === 'l' ? 'listing' : 'project' });
		var facts = [];
		if (x.t === 'l') {
			if (x.rooms > 0) { facts.push(num(x.rooms) + ' חדרים'); }
			if (x.sqm > 0) { facts.push(grp(x.sqm) + ' מ״ר'); }
			if (x.mamad) { facts.push('ממ״ד'); }
			if (x.floor != null) { facts.push(x.floor === 0 ? 'קומת קרקע' : 'קומה ' + x.floor); } // v3: only what the listing states
			if (x.elevator === true) { facts.push('מעלית'); }
			if (x.parking === true) { facts.push('חניה'); }
			if (x.balcony > 0) { facts.push('מרפסת ' + grp(x.balcony) + ' מ״ר'); }
			facts.push(x.deal === 'rent' ? 'להשכרה' : 'למכירה');
		} else {
			if (STATUS[x.status]) { facts.push(STATUS[x.status]); }
			if (x.units > 0) { facts.push(x.units + ' דירות'); }
		}
		var kick = x.t === 'l' ? [x.ptype, [x.hood, x.city].filter(Boolean).join(', ')].filter(Boolean).join(' · ') : x.city;
		var big = '', sub = '';
		if (x.t === 'l' && x.price > 0) { big = nis(x.price); sub = x.deal === 'rent' ? 'לחודש' : (x.psqm > 0 ? nis(x.psqm) + ' למ״ר' : (x.sqm > 0 ? nis(x.price / x.sqm) + ' למ״ר' : '')); }
		if (x.t === 'p' && x.psqm > 0) { big = nis(x.psqm); sub = 'למ״ר, מחיר מוערך'; }
		var ab = x.near ? 'כ-' : '';
		var dists = '';
		if (x.has && S.origin) { dists += '<div class="nlnf-card__row"><span>' + (S.origin.kind === 'me' ? 'ממך' : 'מ' + esc(S.origin.label)) + '</span><bdi>' + ab + dist(km(x, S.origin)) + ' בקו אווירי</bdi></div>'; }
		var sea = x.has ? seaText(x) : '';
		if (sea) { dists += '<div class="nlnf-card__row"><span>מהים</span><bdi>' + esc(sea.replace(/ מהים$/, '')) + '</bdi></div>'; }
		var rows = '';
		SLOTS.forEach(function (s) {
			var a = S.anchors[s.k];
			if (a && x.has) {
				var d = km(x, a), w = walk(d);
				rows += '<div class="nlnf-card__row nlnf-card__row--2"><span>' + esc(s.name) + '</span><span class="nlnf-card__v"><bdi>' + ab + dist(d) + ' בקו אווירי</bdi><small>כ-' + drive(d) + ' דק׳ ברכב' + (w <= 40 ? ' · כ-' + w + ' דק׳ הליכה' : '') + '</small></span></div>';
			} else if (!a) {
				rows += '<div class="nlnf-card__row"><span class="is-mute">' + esc(s.name) + '</span><button type="button" class="nlnf-btn nlnf-btn--s" data-slot="' + s.k + '">הוסיפו</button></div>';
			}
		});
		var inVisit = S.visit.indexOf(x.key) > -1;
		var waze = x.t === 'p' && x.exact && x.has ? '<a class="nlnf-link nlnf-link--s" href="https://waze.com/ul?ll=' + x.lat + ',' + x.lng + '&amp;navigate=yes" target="_blank" rel="noopener" data-waze="1">נווטו ב-Waze</a>' : '';
		el.card.innerHTML =
			'<div class="nlnf-card__bar"><button type="button" class="nlnf-card__back" data-close="1"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true" focusable="false"><path d="M9 6l6 6-6 6"></path></svg>' + (wide() ? 'חזרה לרשימה' : 'חזרה למפה') + '</button>'
			+ (SAVE && (x.t === 'l' || NA) ? saveBtn(x) : '') + '</div>'
			+ (x.img ? '<div class="nlnf-card__media"><img src="' + esc(x.img) + '" alt="" loading="lazy" decoding="async"></div>' : '')
			+ '<div class="nlnf-card__in">'
			+ '<div class="nlnf-card__top">' + (kick ? '<p class="nlnf-card__kick">' + esc(kick) + '</p>' : '') + '<h3 id="nlnf-card-t" tabindex="-1">' + esc(x.title) + '</h3>'
			+ (big ? '<p class="nlnf-card__price"><bdi class="nlnf-card__big">' + esc(big) + '</bdi>' + (sub ? '<bdi class="nlnf-card__sub">' + esc(sub) + '</bdi>' : '') + '</p>' : '')
			+ '</div>'
			+ (SAVE ? '<div class="nlnf-card__note" id="nlnf-card-note" role="status" aria-live="polite"></div>' : '')
			+ (facts.length ? '<ul class="nlnf-card__facts">' + facts.map(function (f) { return '<li>' + esc(f) + '</li>'; }).join('') + '</ul>' : '')
			+ ((x.promoted || (x.t === 'l' && x.near)) ? '<p class="nlnf-card__fine">' + (x.promoted ? AD : '') + (x.t === 'l' && x.approx === 'hood' ? '<span>המיקום לפי השכונה</span>' : '') + (x.t === 'l' && x.approx === 'city' ? '<span>המיקום לפי העיר</span>' : '') + '</p>' : '')
			+ (dists ? '<section class="nlnf-card__places" aria-labelledby="nlnf-card-d"><h4 id="nlnf-card-d">המרחק</h4>' + dists + '</section>' : '')
			+ (x.has ? '<section class="nlnf-card__places" aria-labelledby="nlnf-card-p"><h4 id="nlnf-card-p">המקומות שלכם</h4>' + rows + '<p class="nlnf-card__fine">זמני נסיעה והליכה: הערכה, בלי פקקים</p></section>' : '')
			+ '<div class="nlnf-card__go"><a class="nlnf-btn nlnf-btn--pri" href="' + esc(x.url) + '" data-go="1">' + (x.t === 'l' ? 'לעמוד הנכס' : 'לעמוד הפרויקט') + '</a>'
			+ '<button type="button" class="nlnf-btn" data-visit="' + (inVisit ? 'remove' : 'add') + '" aria-pressed="' + (inVisit ? 'true' : 'false') + '">' + (inVisit ? 'ביום הביקורים ✓' : 'הוסיפו ליום ביקורים') + '</button></div>'
			+ (waze ? '<p class="nlnf-card__fine">' + waze + '</p>' : '')
			+ '</div>';
		el.card.hidden = false;
		el.card.setAttribute('aria-modal', wide() ? 'false' : 'true');
		root.classList.add('is-card');
		var t = $('nlnf-card-t'); if (t) { try { t.focus({ preventScroll: wide() }); } catch (e) { t.focus(); } }
		if (!wide()) { el.card.scrollTop = 0; }
		markActive();
		if (S.map && x.has && wide()) { S.map.easeTo({ center: [x.lng, x.lat], duration: RM ? 0 : 500 }); }
	}
	function closeCard() {
		if (el.card.hidden) { return false; }
		el.card.hidden = true; el.card.innerHTML = ''; root.classList.remove('is-card');
		S.card = null; markActive();
		if (S.opener && document.body.contains(S.opener)) { try { S.opener.focus({ preventScroll: true }); } catch (e) { /* gone */ } }
		return true;
	}

	/* ------------------------------------------------------------ v2: saved, followed, the alerts sheet */
	var CHEV = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true" focusable="false"><path d="M9 6l6 6-6 6"></path></svg>';
	function saveBtn(x) { // the heart on a listing's card, "עקבו" on a project's card
		var on = isSaved(x.key);
		if (x.t === 'l') {
			return '<button type="button" class="nlnf-card__save" data-save="' + esc(x.key) + '" aria-pressed="' + (on ? 'true' : 'false') + '">' + heart(on) + '<span>' + (on ? 'נשמר' : 'שמרו') + '</span></button>';
		}
		return '<button type="button" class="nlnf-card__save nlnf-card__follow" data-save="' + esc(x.key) + '" aria-pressed="' + (on ? 'true' : 'false') + '">' + bell() + '<span>' + (on ? 'במעקב' : 'עקבו') + '</span></button>';
	}
	var syncQ = { add: [], del: [] }, syncT = 0;
	function syncItems(x, on) { // only when this device made a request: its row id and signed key, never the email
		if (!S.sub || !NA) { return; }
		var it = { t: x.t, id: x.id }, q = on ? syncQ.add : syncQ.del, other = on ? syncQ.del : syncQ.add;
		for (var i = other.length - 1; i >= 0; i--) { if (other[i].t === it.t && other[i].id === it.id) { other.splice(i, 1); } }
		q.push(it);
		clearTimeout(syncT);
		syncT = setTimeout(function () {
			var body = { s: S.sub.s, k: S.sub.k, add: syncQ.add, del: syncQ.del };
			syncQ = { add: [], del: [] };
			fetch(NA.items, { method: 'POST', credentials: 'omit', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(body) })
				.then(function (r) { return r.json(); })
				.then(function (j) { if (j && j.gone) { S.sub = null; lsSet('nlnf_alert_v1', null); } })
				.catch(function () { /* the device still keeps the item */ });
		}, 1200);
	}
	function noteFor(x, on) {
		var n = $('nlnf-card-note');
		if (!n) { return; }
		var t, go = '';
		if (x.t === 'l') {
			if (!on) { t = 'הסרנו מהשמורים.'; }
			else if (NA && S.sub) { t = 'שמרנו. אם המחיר יורד, נשלח לכם מייל.'; }
			else if (NA) { t = 'שמרנו את הנכס במכשיר הזה.'; go = '<button type="button" class="nlnf-link" data-al="drop">התריעו לי אם המחיר יורד</button>'; }
			else { t = 'שמרנו את הנכס במכשיר הזה. תמצאו אותו ב״השמורים שלי״, מתחת לרשימה.'; }
		} else if (!on) { t = 'הפסקנו לעקוב אחרי הפרויקט.'; }
		else if (S.sub) { t = 'עוקבים. כשמשהו משתנה בפרויקט, נשלח לכם מייל.'; }
		else { t = 'הפרויקט במעקב במכשיר הזה.'; go = '<button type="button" class="nlnf-link" data-al="proj">קבלו עדכונים במייל</button>'; }
		n.innerHTML = '<p>' + esc(t) + '</p>' + go;
	}
	function toggleSave(key) {
		var x = S.byKey[key];
		if (!x) { return; }
		var on = !isSaved(key);
		if (on && S.saved.length >= 60) { var n0 = $('nlnf-card-note'); if (n0) { n0.innerHTML = '<p>שמרתם כבר הרבה. הסירו אחד כדי לשמור עוד.</p>'; } return; }
		S.saved = on ? S.saved.concat([key]) : S.saved.filter(function (k) { return k !== key; });
		saveSaved();
		var old = el.card.querySelector('[data-save]');
		if (old) { old.outerHTML = saveBtn(x); var nb = el.card.querySelector('[data-save]'); if (nb) { try { nb.focus({ preventScroll: true }); } catch (e) { nb.focus(); } } }
		noteFor(x, on);
		syncItems(x, on);
		renderList(); renderSaved(); markActive();
		ev(x.t === 'l' ? 'save' : 'follow', { on: on ? 1 : 0 });
	}

	var RADII = [1, 1.5, 2, 3, 5];
	var AL = { area: null, r: 1.5, freq: 'day', email: '', step: 'form', want: null, opener: null, sending: false };
	function nearPlace(lat, lng) { // the data's own neighbourhood (1.5 km) or city (5 km) nearest a point: the sheet's wording only
		var best = null, bd = 1e9;
		S.places.forEach(function (p) {
			var d = km({ lat: lat, lng: lng }, p), sc = p.kind === 'hood' ? d : d + 10;
			if (d <= (p.kind === 'hood' ? 1.5 : 5) && sc < bd) { bd = sc; best = p; }
		});
		return best;
	}
	function snapR(k) { for (var i = 0; i < RADII.length; i++) { if (k <= RADII[i] + 0.01) { return RADII[i]; } } return RADII[RADII.length - 1]; }
	function alertArea() { // the zone the visitor drew, else the place chosen, else me, else what the map shows; null = nothing chosen yet
		if (S.zone) { var zc = ringCentre(S.zone), npz = nearPlace(zc.lat, zc.lng); return { lat: zc.lat, lng: zc.lng, kind: 'zone', name: npz ? npz.name : '', r: 0 }; }
		var o = S.origin, b = S.bounds;
		if (o) {
			var np = o.kind === 'place' ? null : nearPlace(o.lat, o.lng);
			return { lat: o.lat, lng: o.lng, kind: o.kind === 'me' ? 'me' : 'place', name: o.kind === 'place' ? o.label : (np ? np.name : ''), r: o.kind === 'place' && o.pkind === 'city' ? 3 : 1.5 };
		}
		if (!b && S.map && S.mapState === 'on') { try { var mb = S.map.getBounds(); b = { w: mb.getWest(), s: mb.getSouth(), e: mb.getEast(), n: mb.getNorth() }; } catch (e) { b = null; } }
		if (!b) { return null; }
		var c = { lat: (b.s + b.n) / 2, lng: (b.w + b.e) / 2 }, np2 = nearPlace(c.lat, c.lng);
		return { lat: c.lat, lng: c.lng, kind: 'map', name: np2 ? np2.name : '', r: snapR(Math.max(1, Math.min(km(c, { lat: b.n, lng: c.lng }), km(c, { lat: c.lat, lng: b.e })))) };
	}
	function filtText() {
		var a = [S.tab === 'rent' ? 'להשכרה' : (S.tab === 'sale' ? 'למכירה' : 'למכירה ולהשכרה')];
		if (S.tab !== 'new') { // the same wording as the mail (inc/near-alerts.php nadlan_na_filters_text)
			var F = S.f, pp = S.fp[S.tab], pl = function (n) { return priceLabel(n, S.tab); };
			if (F.rooms && F.rmax) { a.push((F.rooms === F.rmax ? num(F.rooms) : num(F.rooms) + ' עד ' + num(F.rmax)) + ' חדרים'); }
			else if (F.rooms) { a.push(num(F.rooms) + ' חדרים ומעלה'); }
			else if (F.rmax) { a.push('עד ' + num(F.rmax) + ' חדרים'); }
			if (pp.min && pp.max) { a.push('מ־' + pl(pp.min) + ' עד ' + pl(pp.max)); }
			else if (pp.min) { a.push('מ־' + pl(pp.min)); }
			else if (pp.max) { a.push('עד ' + pl(pp.max)); }
			if (F.smin && F.smax) { a.push(grp(F.smin) + ' עד ' + grp(F.smax) + ' מ״ר'); }
			else if (F.smin) { a.push('מ־' + grp(F.smin) + ' מ״ר'); }
			else if (F.smax) { a.push('עד ' + grp(F.smax) + ' מ״ר'); }
			var fn = function (f) { return f === 0 ? 'קרקע' : String(f); };
			if (F.fmin != null && F.fmax != null) { a.push(F.fmin === F.fmax ? (F.fmin === 0 ? 'קומת קרקע' : 'קומה ' + F.fmin) : 'קומות ' + fn(F.fmin) + ' עד ' + fn(F.fmax)); }
			else if (F.fmin != null) { a.push(F.fmin === 0 ? 'מקומת קרקע' : 'מקומה ' + F.fmin); }
			else if (F.fmax != null) { a.push(F.fmax === 0 ? 'קומת קרקע' : 'עד קומה ' + F.fmax); }
			if (F.mamad) { a.push('עם ממ״ד'); }
			if (F.elev) { a.push('עם מעלית'); }
			if (F.park) { a.push('עם חניה'); }
			if (F.balc) { a.push('עם מרפסת'); }
		}
		return a.length > 1 ? a.join(' · ') : a[0] + ', בכל מחיר ובכל מספר חדרים';
	}
	function alBar() { return '<div class="nlnf-card__bar"><button type="button" class="nlnf-card__back" data-al="close">' + CHEV + (wide() ? 'חזרה לרשימה' : 'חזרה') + '</button></div>'; }
	function alertHtml() {
		if (AL.step === 'done') {
			return alBar() + '<div class="nlnf-al__in nlnf-al__done"><h3 class="nlnf-al__h" id="nlnf-al-t" tabindex="-1">בדקו את המייל</h3>'
				+ '<p class="nlnf-al__lead">שלחנו מייל לאישור אל <bdi dir="ltr">' + esc(AL.email) + '</bdi>. ההתראות יתחילו אחרי שתלחצו על הכפתור שבמייל, ועד אז לא נשלח שום התראה.</p>'
				+ '<p class="nlnf-al__fine">לא הגיע תוך כמה דקות? בדקו גם בתיקיית הספאם.</p>'
				+ '<button type="button" class="nlnf-btn nlnf-btn--pri nlnf-al__go" data-al="close">חזרה לרשימה</button></div>';
		}
		var A = AL.area, deal = S.tab, w = AL.want, nL = savedIds('l').length, nP = savedIds('p').length;
		var where = A.kind === 'me' ? 'סביב המיקום שלכם' : (A.kind === 'map' ? 'על האזור שעל המפה' + (A.name ? ', סביב ' + esc(A.name) : '')
			: (A.kind === 'zone' ? 'על האזור שציירתם במפה' + (A.name ? ', סביב ' + esc(A.name) : '') : 'על האזור שבחרתם: ' + esc(A.name)));
		var opts = [
			['new', deal === 'rent' ? 'דירה חדשה להשכרה עלתה באזור' : (deal === 'sale' ? 'נכס חדש למכירה עלה באזור' : 'נכס חדש עלה באזור'), filtText(), !w],
			['drop', 'ירד המחיר בנכס ששמרתם', 'המחיר הקודם, המחיר החדש והפער בשקלים · ' + (nL ? (nL === 1 ? 'שמרתם נכס אחד' : nL + ' נכסים שמורים') : 'שומרים בלב שבכרטיס הנכס'), !w || w === 'drop'],
			['proj', 'עדכון בפרויקט שאתם עוקבים אחריו', 'מחיר מוערך למ״ר, שלב הפרויקט או מספר הדירות · ' + (nP ? (nP === 1 ? 'עוקבים אחרי פרויקט אחד' : nP + ' פרויקטים במעקב') : 'עוקבים בכפתור שבכרטיס הפרויקט'), !w || w === 'proj']
		];
		return alBar() + '<form class="nlnf-al__in" id="nlnf-al-f" novalidate>'
			+ '<div class="nlnf-al__head"><h3 class="nlnf-al__h" id="nlnf-al-t" tabindex="-1">התריעו לי</h3>'
			+ '<p class="nlnf-al__lead">' + where + (A.kind === 'zone' ? '.' : ', ברדיוס <label class="nlnf-al__r"><span class="nlnf__sr">רדיוס</span><select name="r" data-al="r">'
			+ RADII.map(function (r) { return '<option value="' + r + '"' + (r === AL.r ? ' selected' : '') + '>' + r + ' ק״מ</option>'; }).join('')
			+ '</select></label>' + (A.kind === 'me' ? '. נשמור רק את האזור, לא את המיקום המדויק שלכם.' : '.')) + '</p></div>'
			+ '<fieldset class="nlnf-al__what"><legend class="nlnf__sr">על מה להתריע</legend>'
			+ opts.map(function (o) { return '<label class="nlnf-al__opt"><input type="checkbox" name="what" value="' + o[0] + '"' + (o[3] ? ' checked' : '') + '><span><b>' + esc(o[1]) + '</b><small>' + esc(o[2]) + '</small></span></label>'; }).join('')
			+ '</fieldset>'
			+ '<div class="nlnf-al__grp"><span class="nlnf-al__lab" id="nlnf-al-fl">באיזו תדירות</span><div class="nlnf-al__seg" role="radiogroup" aria-labelledby="nlnf-al-fl">'
			+ [['now', 'מיד'], ['day', 'פעם ביום'], ['week', 'פעם בשבוע']].map(function (f) { return '<label><input type="radio" name="freq" value="' + f[0] + '"' + (AL.freq === f[0] ? ' checked' : '') + '><span>' + f[1] + '</span></label>'; }).join('')
			+ '</div></div>'
			+ '<label class="nlnf-al__grp nlnf-al__mail"><span class="nlnf-al__lab">מייל</span><input type="email" name="email" inputmode="email" autocomplete="email" spellcheck="false" placeholder="name@example.com" dir="ltr" value="' + esc(AL.email) + '" required></label>'
			+ '<input type="text" name="company" class="nlnf-al__hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
			+ '<button type="submit" class="nlnf-btn nlnf-btn--pri nlnf-al__go">הפעילו התראות</button>'
			+ '<p class="nlnf-al__err" id="nlnf-al-err" role="alert" hidden></p>'
			+ '<p class="nlnf-al__fine">נשתמש במייל רק כדי לשלוח את ההתראות שבחרתם. קודם יגיע מייל לאישור, ובכל מייל יש קישור לביטול בלחיצה אחת.</p>'
			+ '<p class="nlnf-al__fine">נשמור רק את המייל, את האזור (מרכזו בעיגול של כ־100 מ׳, ואם ציירתם אזור, גם קווי האזור), את הסינון ואת התדירות, עד שתבטלו. המייל יוצא דרך ספק השליחה של האתר ולא נמסר לאף גורם אחר. מסירת המייל אינה חובה, אבל בלי מייל לא נוכל לשלוח התראות. את הפרטים מחזיק נדלן (nad-lan.co.il); לעיון, לתיקון או למחיקה: info@nad-lan.co.il. <a href="' + esc(NA.privacy) + '" target="_blank" rel="noopener">מדיניות הפרטיות</a></p>'
			+ '</form>';
	}
	function openAlert(want, opener) {
		if (!NA || !el.al) { return; }
		var A = alertArea();
		if (!A) { say('בחרו קודם עיר או שכונה, או לחצו על "המיקום שלי", ונתריע לכם על האזור.'); try { el.q.focus(); } catch (e) { /* focus */ } return; }
		var back = S.card ? S.opener : null;
		closeCard(); measureOff(); endPick(); closeSh(); drawOff(); say('');
		AL.area = A; AL.r = A.r; AL.step = 'form'; AL.want = want || null; AL.sending = false;
		AL.opener = opener && document.body.contains(opener) && !el.card.contains(opener) ? opener : back;
		el.al.innerHTML = alertHtml();
		el.al.hidden = false;
		el.al.setAttribute('aria-modal', wide() ? 'false' : 'true');
		root.classList.add('is-al');
		if (!wide()) { el.al.scrollTop = 0; }
		var t = $('nlnf-al-t'); if (t) { try { t.focus({ preventScroll: wide() }); } catch (e) { t.focus(); } }
		drawAlertArea(true);
		ev('alert_open', { from: want || 'area' });
	}
	function closeAlert() {
		if (!el.al || el.al.hidden) { return false; }
		el.al.hidden = true; el.al.innerHTML = ''; root.classList.remove('is-al');
		drawAlertArea(false);
		var o = AL.opener; AL.opener = null;
		if (!(o && document.body.contains(o)) && el.alrow) { o = el.alrow.querySelector('button'); }
		if (o) { try { o.focus({ preventScroll: true }); } catch (e) { /* gone */ } }
		return true;
	}
	function drawAlertArea(fit) { // the alert's circle on the map while the sheet is open (seen beside it on a computer)
		if (!S.map || S.mapState !== 'on' || !S.map.getSource('nf-alert')) { return; }
		var A = el.al && !el.al.hidden ? AL.area : null;
		if (A && A.kind === 'zone') { // v3: the drawn zone is already on the map; no circle
			try { S.map.getSource('nf-alert').setData({ type: 'FeatureCollection', features: [] }); } catch (e) { return; }
			if (fit && wide() && S.zone) { fitBox(S.zone.bbox, 15); }
			return;
		}
		try {
			S.map.getSource('nf-alert').setData({ type: 'FeatureCollection', features: A ? [{ type: 'Feature', properties: { r0: AL.r * 1000 / (78271.517 * Math.cos(A.lat * Math.PI / 180)) }, geometry: { type: 'Point', coordinates: [A.lng, A.lat] } }] : [] });
		} catch (e) { return; }
		if (A && fit && wide()) {
			var dLa = AL.r / 110.574, dLn = AL.r / (111.32 * Math.cos(A.lat * Math.PI / 180));
			try { S.map.fitBounds([[A.lng - dLn, A.lat - dLa], [A.lng + dLn, A.lat + dLa]], { padding: camPad(56), maxZoom: 15, duration: RM ? 0 : 600 }); } catch (e) { /* keep the view */ }
			userMoved = false; el.area.hidden = true;
		}
	}
	function alErr(t) { var e = $('nlnf-al-err'); if (!e) { return; } e.textContent = t || ''; e.hidden = !t; }
	function r3(v) { return Math.round(v * 1000) / 1000; } // about 100 m: the area, never the visitor's exact place
	function r4(v) { return Math.round(v * 1e4) / 1e4; } // a drawn zone's corners: about 11 m
	function sendAlert(f) {
		if (AL.sending) { return; }
		var email = String(f.elements.email.value || '').trim();
		var what = [].filter.call(f.querySelectorAll('input[name=what]'), function (i) { return i.checked; }).map(function (i) { return i.value; });
		var fr = f.querySelector('input[name=freq]:checked');
		AL.email = email; AL.freq = fr ? fr.value : 'day';
		if (!what.length) { alErr('בחרו לפחות התראה אחת.'); return; }
		if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 100) { alErr('בדקו את כתובת המייל.'); try { f.elements.email.focus(); } catch (e) { /* focus */ } return; }
		alErr('');
		var A = AL.area, tab = S.tab, go = f.querySelector('.nlnf-al__go'), Lt = tab !== 'new', F = S.f, pp = Lt ? S.fp[tab] : { min: 0, max: 0 };
		var body = { email: email, lat: r3(A.lat), lng: r3(A.lng), r: AL.r, place: A.name || '', deal: Lt ? tab : '',
			rooms: Lt ? F.rooms : 0, rmax: Lt ? F.rmax : 0, pmin: pp.min, pmax: pp.max, smin: Lt ? F.smin : 0, smax: Lt ? F.smax : 0,
			mamad: Lt && !!F.mamad, elev: Lt && !!F.elev, park: Lt && !!F.park, balc: Lt && !!F.balc, what: what, freq: AL.freq,
			items: what.indexOf('drop') > -1 ? savedIds('l') : [], follow: what.indexOf('proj') > -1 ? savedIds('p') : [], company: f.elements.company.value || '', v: NA.v };
		if (Lt && F.fmin != null) { body.fmin = F.fmin; }
		if (Lt && F.fmax != null) { body.fmax = F.fmax; }
		if (A.kind === 'zone' && S.zone) { body.poly = S.zone.ring.slice(0, -1).map(function (c) { return [r4(c[1]), r4(c[0])]; }); } // [lat, lng], 4 decimals (about 11 m)
		AL.sending = true; go.disabled = true; go.textContent = 'שולחים…';
		function back(msg) { AL.sending = false; go.disabled = false; go.textContent = 'הפעילו התראות'; alErr(msg); }
		fetch(NA.api, { method: 'POST', credentials: 'omit', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(body) })
			.then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { st: r.status, j: j || {} }; }); })
			.then(function (x) {
				if (x.j.ok) {
					AL.sending = false;
					if (x.j.s && x.j.k) { S.sub = { s: x.j.s, k: x.j.k }; lsSet('nlnf_alert_v1', S.sub); }
					AL.step = 'done'; el.al.innerHTML = alertHtml();
					var t = $('nlnf-al-t'); if (t) { try { t.focus({ preventScroll: true }); } catch (e) { t.focus(); } }
					ev('alert_sent', { freq: AL.freq, kinds: what.length });
					return;
				}
				var er = x.j.error;
				back(er === 'email' ? 'בדקו את כתובת המייל.' : er === 'what' ? 'בחרו לפחות התראה אחת.' : er === 'area' ? 'בחרו עיר, שכונה או את המיקום שלכם בישראל.'
					: x.st === 429 ? 'כבר נשלחו כמה בקשות מהמכשיר הזה או למייל הזה. נסו שוב בעוד שעה.' : 'לא הצלחנו לשלוח עכשיו. נסו שוב בעוד רגע.');
			})
			.catch(function () { back('לא הצלחנו לשלוח עכשיו. בדקו את החיבור ונסו שוב.'); });
	}

	/* ------------------------------------------------------------ the map */
	var markers = {}, meMarker = null, ancMarkers = {}, measMarker = null, userMoved = false, MB = null, mapWanted = false;
	function loadScript(src) { // 6.11.2026: never a second copy of Mapbox GL. The home page's projects map (the section the app sits in there) loads the
		// same file when it comes into view: if its script is on the way, wait for it; inside that section, give it up to 3 seconds to start first
		return new Promise(function (res, rej) {
			var t0 = Date.now(), grace = root.closest('#nldrone') ? 3000 : 0;
			(function look() {
				if (window.mapboxgl) { return res(); }
				var old = document.querySelector('script[src="' + src + '"]');
				if (old) {
					var n = 0, iv = setInterval(function () { if (window.mapboxgl) { clearInterval(iv); res(); } else if (++n > 200) { clearInterval(iv); rej(new Error('timeout')); } }, 100);
					old.addEventListener('error', function () { clearInterval(iv); rej(new Error('load')); });
					return;
				}
				if (Date.now() - t0 < grace) { setTimeout(look, 100); return; }
				var s = document.createElement('script'); s.src = src; s.async = true; s.onload = res; s.onerror = rej; document.head.appendChild(s);
			})();
		});
	}
	function rtlSettled() { // two maps that start while the right-to-left text plugin is still loading make Mapbox load it twice in its shared workers
		// (an uncaught "RTL text plugin already registered", seen on the live home page too): the finder's map waits, 4 seconds at most, and
		// when it did wait, 1.5 seconds more after "loaded" (the other map's workers are still finishing then)
		return new Promise(function (res) {
			var n = 0;
			(function w() {
				var st = '';
				try { st = MB.getRTLTextPluginStatus ? MB.getRTLTextPluginStatus() : ''; } catch (e) { st = ''; }
				var busy = st === 'loading' || st === 'requested' || (st === 'deferred' && !!document.querySelector('.mapboxgl-map'));
				if (busy && ++n <= 40) { setTimeout(w, 100); return; }
				if (n > 0 && st === 'loaded' && document.querySelector('.mapboxgl-map')) { setTimeout(res, 1500); return; }
				res();
			})();
		});
	}
	function loadCss(href) { if (document.querySelector('link[href="' + href + '"]')) { return; } var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = href; document.head.appendChild(l); }
	function noMap(why) {
		S.mapState = 'fail'; root.classList.add('nlnf--nomap'); el.mapwrap.hidden = true;
		if (why) { say(why); }
	}
	function startMap() {
		if (mapWanted) { return; }
		mapWanted = true;
		if (!D.mb) { noMap(''); return; }
		S.mapState = 'loading';
		loadCss(D.glcss);
		loadScript(D.gl).then(function () {
			MB = window.mapboxgl;
			if (!MB || (MB.supported && !MB.supported())) { throw new Error('unsupported'); }
			return rtlSettled();
		}).then(function () {
			try { if (MB.getRTLTextPluginStatus && MB.getRTLTextPluginStatus() === 'unavailable') { MB.setRTLTextPlugin(D.rtl, null, true); } } catch (e) { /* the labels stay readable without it */ }
			MB.accessToken = D.mb;
			var m = new MB.Map({
				container: el.map, style: 'mapbox://styles/mapbox/light-v11', center: [34.79, 32.09], zoom: 10.5,
				cooperativeGestures: true, dragRotate: false, pitchWithRotate: false, touchPitch: false, language: 'he', attributionControl: true,
				locale: {
					'ScrollZoomBlocker.CtrlMessage': 'כדי להגדיל או להקטין, החזיקו Ctrl וגללו',
					'ScrollZoomBlocker.CmdMessage': 'כדי להגדיל או להקטין, החזיקו ⌘ וגללו',
					'TouchPanBlocker.Message': 'הזיזו את המפה בשתי אצבעות',
					'NavigationControl.ZoomIn': 'הגדלה', 'NavigationControl.ZoomOut': 'הקטנה', 'NavigationControl.ResetBearing': 'צפון למעלה',
					'AttributionControl.ToggleAttribution': 'זכויות המפה', 'Map.Title': 'מפה'
				}
			});
			S.map = m;
			try { m.touchZoomRotate.disableRotation(); } catch (e) { /* older build */ }
			m.addControl(new MB.NavigationControl({ showCompass: false }), 'top-left');
			m.on('error', function () { /* a tile that failed is not a broken page */ });
			m.on('load', function () {
				m.addSource('nf-area', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });
				m.addLayer({ id: 'nf-area', type: 'circle', source: 'nf-area', minzoom: 8, paint: {
					'circle-radius': ['interpolate', ['exponential', 2], ['zoom'], 0, ['get', 'r0'], 22, ['*', ['get', 'r0'], 4194304]],
					'circle-color': '#2F6F86', 'circle-opacity': 0.1, 'circle-stroke-color': '#2F6F86', 'circle-stroke-width': 1.5, 'circle-stroke-opacity': 0.45 } });
				m.addSource('nf-alert', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } }); // v2: the alert's circle, while the sheet is open
				m.addLayer({ id: 'nf-alert', type: 'circle', source: 'nf-alert', minzoom: 7, paint: {
					'circle-radius': ['interpolate', ['exponential', 2], ['zoom'], 0, ['get', 'r0'], 22, ['*', ['get', 'r0'], 4194304]],
					'circle-color': '#2F6F86', 'circle-opacity': 0.08, 'circle-stroke-color': '#1F4B5C', 'circle-stroke-width': 2, 'circle-stroke-opacity': 0.75 } });
				m.addSource('nf-iso', { type: 'geojson', data: EMPTY }); // v3: the travel-time area, a soft sea tint (dashed edge = the distance estimate)
				m.addLayer({ id: 'nf-iso-f', type: 'fill', source: 'nf-iso', paint: { 'fill-color': '#2F6F86', 'fill-opacity': 0.12 } });
				m.addLayer({ id: 'nf-iso-l', type: 'line', source: 'nf-iso', filter: ['!=', ['get', 'est'], 1], paint: { 'line-color': '#2F6F86', 'line-width': 1.5, 'line-opacity': 0.7 } });
				m.addLayer({ id: 'nf-iso-e', type: 'line', source: 'nf-iso', filter: ['==', ['get', 'est'], 1], paint: { 'line-color': '#2F6F86', 'line-width': 1.5, 'line-opacity': 0.8, 'line-dasharray': [3, 2] } });
				m.addSource('nf-zone', { type: 'geojson', data: EMPTY }); // v3: the zone the visitor drew
				m.addLayer({ id: 'nf-zone-f', type: 'fill', source: 'nf-zone', paint: { 'fill-color': '#2F6F86', 'fill-opacity': 0.08 } });
				m.addLayer({ id: 'nf-zone-l', type: 'line', source: 'nf-zone', paint: { 'line-color': '#1F4B5C', 'line-width': 2 } });
				m.addSource('nf-meas', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });
				m.addLayer({ id: 'nf-meas-l', type: 'line', source: 'nf-meas', filter: ['==', ['geometry-type'], 'LineString'], paint: { 'line-color': '#12202A', 'line-width': 2, 'line-dasharray': [2, 1.5] } });
				m.addLayer({ id: 'nf-meas-p', type: 'circle', source: 'nf-meas', filter: ['==', ['geometry-type'], 'Point'], paint: { 'circle-radius': 6, 'circle-color': '#FFFFFF', 'circle-stroke-color': '#12202A', 'circle-stroke-width': 2 } });
				/* v4: the context layers of the few-listings state (under the pins, which are DOM markers) */
				m.addSource('nf-ctx-p', { type: 'geojson', data: EMPTY });
				m.addLayer({ id: 'nf-ctx-p', type: 'circle', source: 'nf-ctx-p', paint: {
					'circle-radius': ['interpolate', ['linear'], ['zoom'], 6, 2, 9, 3, 12, 4.5, 15, 6], 'circle-color': '#F2D15A',
					'circle-stroke-color': '#12202A', 'circle-stroke-width': 1, 'circle-stroke-opacity': 0.7 } });
				m.addSource('nf-ctx-a', { type: 'geojson', data: EMPTY });
				m.addLayer({ id: 'nf-ctx-a', type: 'symbol', source: 'nf-ctx-a', layout: {
					'text-field': ['format', ['get', 'n'], { 'font-scale': 0.92 }, '\n', {}, ['get', 'p'], { 'font-scale': 1.08, 'text-font': ['literal', ['DIN Pro Bold', 'Arial Unicode MS Bold']] }],
					'text-font': ['DIN Pro Medium', 'Arial Unicode MS Regular'], 'text-size': 13, 'text-line-height': 1.15, 'text-padding': 4,
					'text-variable-anchor': ['bottom', 'top', 'right', 'left'], 'text-radial-offset': 0.55, 'text-justify': 'auto',
					'symbol-sort-key': ['get', 'rank'], 'text-allow-overlap': false, 'text-ignore-placement': false },
					paint: { 'text-color': '#12202A', 'text-halo-color': '#FFFFFF', 'text-halo-width': 2.6 } });
				['nf-ctx-p', 'nf-ctx-a'].forEach(function (id) {
					m.on('mouseenter', id, function () { m.getCanvas().style.cursor = 'pointer'; });
					m.on('mouseleave', id, function () { m.getCanvas().style.cursor = ''; });
				});
				m.on('click', 'nf-ctx-p', function (e) {
					var f = e.features && e.features[0], x = f && S.byKey[f.properties.key];
					if (x && !S.picking && !S.measure) { openCard(x, null); ev('few', { go: 'project' }); }
				});
				m.on('click', 'nf-ctx-a', function (e) {
					var f = e.features && e.features[0];
					if (f && f.properties.u && !S.picking && !S.measure) { ev('few', { go: 'prices' }); window.location.href = f.properties.u; }
				});
				m.addSource('nf-pts', { type: 'geojson', data: { type: 'FeatureCollection', features: [] }, cluster: true, clusterMaxZoom: 14, clusterRadius: 60, clusterProperties: { n: ['+', ['get', 'n']] } });
				m.addLayer({ id: 'nf-pts-h', type: 'circle', source: 'nf-pts', paint: { 'circle-radius': 1, 'circle-opacity': 0 } });
				S.mapState = 'on';
				m.on('moveend', function () { sync(); if (userMoved && !S.picking && !S.measure && !root.classList.contains('is-draw')) { el.area.hidden = false; } });
				m.on('sourcedata', function (e) { if (e && e.sourceId === 'nf-pts' && e.isSourceLoaded) { sync(); } });
				['dragstart', 'zoomstart'].forEach(function (n) { m.on(n, function (e) { if (e && e.originalEvent) { userMoved = true; } }); });
				m.on('click', function (e) {
					if (S.picking) { setAnchor(S.picking, e.lngLat.lat, e.lngLat.lng); return; }
					if (S.measure) { measureTap(e.lngLat.lat, e.lngLat.lng); }
				});
				drawMap(results(), true);
				drawAnchors();
				if (S.origin) { drawMe(); }
				drawAlertArea(true);
				drawZone(); drawIso();
			});
		}).catch(function () { noMap('המפה לא נטענה כרגע. כל הרשימה כאן, ואפשר לבחור עיר או שכונה.'); });
	}
	var LAST = { fit: false };
	function featuresFor(list) {
		var pts = [], areas = [], groups = {};
		list.forEach(function (x) {
			if (!x.has) { return; }
			if (x.t === 'l' && x.near) {
				var gk = x.deal + '|' + x.lat + ',' + x.lng;
				if (!groups[gk]) { groups[gk] = { key: 'g' + gk, items: [], lat: x.lat, lng: x.lng, approx: x.approx, label: x.area || x.place, deal: x.deal }; }
				groups[gk].items.push(x);
				return;
			}
			pts.push({ type: 'Feature', properties: { key: x.key, n: 1 }, geometry: { type: 'Point', coordinates: [x.lng, x.lat] } });
		});
		S.groups = {};
		Object.keys(groups).forEach(function (gk) {
			var g = groups[gk]; S.groups[g.key] = g;
			g.keys = g.items.map(function (x) { return x.key; });
			pts.push({ type: 'Feature', properties: { key: g.key, n: g.items.length }, geometry: { type: 'Point', coordinates: [g.lng, g.lat] } });
			var meters = g.approx === 'city' ? 1800 : 450;
			areas.push({ type: 'Feature', properties: { r0: meters / (78271.517 * Math.cos(g.lat * Math.PI / 180)) }, geometry: { type: 'Point', coordinates: [g.lng, g.lat] } });
		});
		return { pts: pts, areas: areas };
	}
	function drawMap(list, first) {
		if (!S.map || S.mapState !== 'on') { return; }
		var base = pool().filter(function (x) { return passes(x, true); }); // what the filters keep, before the area / group scope
		var f = featuresFor(base);
		S.order = {}; (list || []).forEach(function (x, i) { S.order[x.key] = i; });
		try {
			S.map.getSource('nf-pts').setData({ type: 'FeatureCollection', features: f.pts });
			S.map.getSource('nf-area').setData({ type: 'FeatureCollection', features: S.tab === 'new' ? [] : f.areas });
		} catch (e) { return; }
		drawCtx();
		clearMarkers();
		if ((first || LAST.fit) && S.loaded) { fitTo(base); LAST.fit = false; }
		setTimeout(sync, 60);
	}
	function drawCtx() {
		if (!S.map || S.mapState !== 'on') { return; }
		var on = few(), P = [], A = [];
		if (on) {
			projOnMap().forEach(function (x) { P.push({ type: 'Feature', properties: { key: x.key }, geometry: { type: 'Point', coordinates: [x.lng, x.lat] } }); });
			if (S.tab === 'sale') {
				var rk = S.A.slice().sort(function (a, b) { return (b.big || 0) - (a.big || 0); });
				rk.forEach(function (a, i) {
					A.push({ type: 'Feature', properties: { n: a.n, p: '4 חד׳ · ' + shortPrice(a.r4, 'sale'), u: a.url || '', rank: i }, geometry: { type: 'Point', coordinates: [a.lng, a.lat] } });
				});
			}
		}
		try { S.map.getSource('nf-ctx-p').setData({ type: 'FeatureCollection', features: P }); S.map.getSource('nf-ctx-a').setData({ type: 'FeatureCollection', features: A }); } catch (e) { /* the map is not ready */ }
	}
	function fitTo(list) {
		if (!S.map) { return; }
		if (S.origin) { flyTo(S.origin.lat, S.origin.lng, S.origin.zoom || 13); return; }
		var xs = list.filter(function (x) { return x.has; });
		if (!xs.length) { return; }
		var w = 180, s = 90, e = -180, n = -90;
		xs.forEach(function (x) { w = Math.min(w, x.lng); e = Math.max(e, x.lng); s = Math.min(s, x.lat); n = Math.max(n, x.lat); });
		try { S.map.fitBounds([[w, s], [e, n]], { padding: camPad(48), maxZoom: 13, duration: RM ? 0 : 600 }); } catch (err) { /* keep the view */ }
		userMoved = false; el.area.hidden = true;
	}
	function flyTo(lat, lng, z) {
		if (!S.map) { return; }
		var o = { center: [lng, lat], zoom: z, offset: [0, -Math.round(shv() / 2)] }; // above the phone sheet
		if (RM) { S.map.jumpTo(o); } else { S.map.flyTo(Object.assign({ duration: 900 }, o)); }
		userMoved = false; el.area.hidden = true;
	}
	function clearMarkers() { Object.keys(markers).forEach(function (k) { markers[k].remove(); }); markers = {}; }
	function factOf(x) { return shortPrice(x.price, x.deal) || (x.rooms > 0 ? num(x.rooms) + ' חד׳' : '') || (x.sqm > 0 ? grp(x.sqm) + ' מ״ר' : ''); }
	function pinFor(key) {
		if (S.groups && S.groups[key]) {
			var g = S.groups[key];
			if (g.items.length === 1) { var one = g.items[0]; return { cls: one.deal === 'rent' ? 'rent' : 'sale', text: g.label + (factOf(one) ? ' · ' + factOf(one) : ''), ad: one.promoted, aria: one.title }; }
			var pr = priceRange(g.items, g.deal);
			return { cls: g.deal === 'rent' ? 'rent' : 'sale', text: g.label + ' · ' + (pr || g.items.length + ' נכסים'), aria: g.label + ', ' + g.items.length + ' נכסים' };
		}
		var x = S.byKey[key];
		if (!x) { return null; }
		if (x.t === 'p') {
			var fact = STATUS[x.status] || (x.units > 0 ? x.units + ' דירות' : '');
			return { cls: 'new', text: cut(x.title, 26) + (fact ? ' · ' + fact : ''), ad: x.promoted, aria: x.title };
		}
		return { cls: x.deal === 'rent' ? 'rent' : 'sale', text: x.place + (factOf(x) ? ' · ' + factOf(x) : ''), ad: x.promoted, aria: x.title };
	}
	function sync() {
		var m = S.map;
		if (!m || S.mapState !== 'on' || !m.getSource('nf-pts')) { return; }
		var feats;
		try { feats = m.querySourceFeatures('nf-pts'); } catch (e) { return; }
		var seen = {}, cand = [], cw = el.map.clientWidth, ch = el.map.clientHeight;
		feats.forEach(function (f) {
			var p = f.properties || {}, id = p.cluster ? 'c' + p.cluster_id : p.key;
			if (!id || seen[id]) { return; }
			seen[id] = 1;
			var c = f.geometry.coordinates; // on screen is decided below, in pixels (getBounds() leaves out the camera padding)
			var pin;
			if (p.cluster) { var n = p.n || p.point_count; pin = { cls: 'cl', text: grp(n) + (S.tab === 'new' ? ' פרויקטים' : ' נכסים'), aria: grp(n) + (S.tab === 'new' ? ' פרויקטים' : ' נכסים') + ', הגדלה' }; }
			else { pin = pinFor(p.key); }
			if (!pin) { return; }
			var pt = m.project(c);
			var hot = S.card && (S.card.key === p.key || (S.groups && S.groups[p.key] && S.groups[p.key].keys.indexOf(S.card.key) > -1));
			var pri = hot ? 0 : p.cluster ? 1 : (pin.ad ? 2 : 3 + ((S.order && S.order[p.key]) != null ? S.order[p.key] / 1e4 : 0.9));
			cand.push({ id: id, f: f, c: c, pin: pin, x: pt.x, y: pt.y, w: 22 + pin.text.length * 6.7, h: 30, pri: pri });
		});
		cand.sort(function (a, b) { return a.pri - b.pri; });
		var boxes = [], keep = {}, born = 0, dropping = Date.now() < S.dropUntil;
		cand.forEach(function (k) {
			var x0 = k.x - k.w / 2, y0 = k.y - k.h / 2;
			if (x0 < -k.w / 2 || y0 < -10 || x0 > cw || y0 > ch) { return; }
			for (var i = 0; i < boxes.length; i++) { var b = boxes[i]; if (x0 < b[2] + 4 && x0 + k.w + 4 > b[0] && y0 < b[3] + 3 && y0 + k.h + 3 > b[1]) { return; } }
			boxes.push([x0, y0, x0 + k.w, y0 + k.h]);
			keep[k.id] = 1;
			if (markers[k.id]) { return; }
			var b2 = document.createElement('button');
			b2.type = 'button';
			b2.className = 'nlnf-pin nlnf-pin--' + k.pin.cls + (dropping ? ' is-drop' : '');
			if (dropping) { b2.style.setProperty('--nf-d', Math.min(born * 30, 600) + 'ms'); born++; } // settle in, 30 ms apart, 600 ms at most
			b2.setAttribute('aria-label', k.pin.aria || k.pin.text);
			b2.innerHTML = '<span class="nlnf-pin__t">' + esc(k.pin.text) + '</span>' + (k.pin.ad ? '<span class="nlnf-pin__ad">מודעה מקודמת</span>' : '');
			var props = k.f.properties;
			b2.addEventListener('click', function (e) {
				e.stopPropagation();
				if (S.picking) { setAnchor(S.picking, k.c[1], k.c[0]); return; }
				if (S.measure) { measureTap(k.c[1], k.c[0]); return; }
				if (props.cluster) {
					m.getSource('nf-pts').getClusterExpansionZoom(props.cluster_id, function (err, z) { if (!err) { m.easeTo({ center: k.c, zoom: Math.min(z + 0.3, 16), duration: RM ? 0 : 500 }); } });
					return;
				}
				var g = S.groups && S.groups[props.key];
				if (g && g.items.length > 1) {
					S.group = { keys: g.keys, label: g.label }; S.shown = 30; renderList(); markActive();
					if (root.classList.contains('is-sheet')) { setSnap('half', true); el.panel.scrollTop = 0; } // v3: the phone sheet rises
					else if (!wide()) { el.panel.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' }); }
					return;
				}
				var x = g ? g.items[0] : S.byKey[props.key];
				if (x) { openCard(x, b2); }
			});
			markers[k.id] = new MB.Marker({ element: b2, anchor: 'center' }).setLngLat(k.c).addTo(m);
		});
		Object.keys(markers).forEach(function (id) { if (!keep[id]) { markers[id].remove(); delete markers[id]; } });
		markActive();
	}
	function markActive() {
		Object.keys(markers).forEach(function (id) {
			var on = !!S.card && (id === S.card.key || (S.groups && S.groups[id] && S.groups[id].keys.indexOf(S.card.key) > -1));
			markers[id].getElement().classList.toggle('is-on', on);
		});
		[].forEach.call(el.list.querySelectorAll('.nlnf-row'), function (r) { r.classList.toggle('is-on', !!S.card && r.getAttribute('data-key') === S.card.key); });
	}
	function burst(lat, lng) { // rings spread from the visitor's dot, once (never under reduced motion)
		if (RM || !S.map || S.mapState !== 'on') { return; }
		var d = document.createElement('div');
		d.className = 'nlnf-burst'; d.setAttribute('aria-hidden', 'true'); d.innerHTML = '<i></i><i></i><i></i>';
		var mk = new MB.Marker({ element: d, anchor: 'center' }).setLngLat(lat != null ? [lng, lat] : S.map.getCenter()).addTo(S.map);
		setTimeout(function () { mk.remove(); }, 2000);
	}
	function drawMe() {
		if (!S.map || S.mapState !== 'on') { return; }
		if (meMarker) { meMarker.remove(); meMarker = null; }
		if (!S.origin) { return; }
		var d = document.createElement('div');
		d.className = S.origin.kind === 'me' ? 'nlnf-me' : 'nlnf-here';
		d.setAttribute('aria-hidden', 'true');
		if (S.origin.kind !== 'me') { d.textContent = S.origin.label; }
		d.addEventListener('click', function (e) { if (S.measure) { e.stopPropagation(); measureTap(S.origin.lat, S.origin.lng); } });
		meMarker = new MB.Marker({ element: d, anchor: 'center' }).setLngLat([S.origin.lng, S.origin.lat]).addTo(S.map);
	}
	function drawAnchors() {
		Object.keys(ancMarkers).forEach(function (k) { ancMarkers[k].remove(); }); ancMarkers = {};
		if (!S.map || S.mapState !== 'on') { return; }
		SLOTS.forEach(function (s) {
			var a = S.anchors[s.k];
			if (!a) { return; }
			var d = document.createElement('div');
			d.className = 'nlnf-anc'; d.textContent = s.name; d.setAttribute('aria-hidden', 'true');
			d.addEventListener('click', function (e) { if (S.measure) { e.stopPropagation(); measureTap(a.lat, a.lng); } });
			ancMarkers[s.k] = new MB.Marker({ element: d, anchor: 'bottom' }).setLngLat([a.lng, a.lat]).addTo(S.map);
		});
	}

	/* ------------------------------------------------------------ measuring: two taps, the line and the distance */
	function measureOn() {
		if (S.mapState !== 'on') { return; }
		endPick(); closeCard(); closeSh(); drawOff();
		if (root.classList.contains('is-sheet')) { setSnap('peek', true); }
		S.measure = { a: null, b: null };
		el.ruler.setAttribute('aria-pressed', 'true');
		el.area.hidden = true; el.meas.hidden = false;
		el.measT.textContent = 'הקישו על שתי נקודות: המיקום שלכם, נכס או כל מקום במפה';
		S.map.getCanvas().style.cursor = 'crosshair';
		root.classList.add('is-measure');
		ev('measure');
	}
	function measureOff() {
		S.measure = null;
		el.ruler.setAttribute('aria-pressed', 'false');
		el.meas.hidden = true;
		root.classList.remove('is-measure');
		if (S.map) { S.map.getCanvas().style.cursor = ''; try { S.map.getSource('nf-meas').setData({ type: 'FeatureCollection', features: [] }); } catch (e) { /* not loaded */ } }
		if (measMarker) { measMarker.remove(); measMarker = null; }
	}
	function measureTap(lat, lng) {
		var M = S.measure; if (!M) { return; }
		if (!M.a || M.b) { M.a = { lat: lat, lng: lng }; M.b = null; } else { M.b = { lat: lat, lng: lng }; }
		var f = [{ type: 'Feature', properties: {}, geometry: { type: 'Point', coordinates: [M.a.lng, M.a.lat] } }];
		if (measMarker) { measMarker.remove(); measMarker = null; }
		if (M.b) {
			f.push({ type: 'Feature', properties: {}, geometry: { type: 'Point', coordinates: [M.b.lng, M.b.lat] } });
			f.push({ type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: [[M.a.lng, M.a.lat], [M.b.lng, M.b.lat]] } });
			var d = km(M.a, M.b), txt = dist(d) + ' בקו אווירי' + (d <= 8 ? ' · כ-' + walk(d) + ' דק׳ הליכה' : ' · כ-' + drive(d) + ' דק׳ נסיעה');
			el.measT.textContent = txt;
			var lab = document.createElement('div');
			lab.className = 'nlnf-mlabel'; lab.setAttribute('aria-hidden', 'true'); lab.textContent = dist(d);
			measMarker = new MB.Marker({ element: lab, anchor: 'center' }).setLngLat([(M.a.lng + M.b.lng) / 2, (M.a.lat + M.b.lat) / 2]).addTo(S.map);
		} else {
			el.measT.textContent = 'ועכשיו הנקודה השנייה';
		}
		try { S.map.getSource('nf-meas').setData({ type: 'FeatureCollection', features: f }); } catch (e) { /* not loaded */ }
	}
	el.ruler.addEventListener('click', function () { if (S.measure) { measureOff(); } else { measureOn(); } });
	el.measX.addEventListener('click', measureOff);

	/* ------------------------------------------------------------ v3: geometry */
	var EMPTY = { type: 'FeatureCollection', features: [] };
	function inRingLL(lng, lat, ring) { // even-odd rule; ring = [[lng, lat], ...]
		var inside = false;
		for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {
			var xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
			if (((yi > lat) !== (yj > lat)) && (lng < (xj - xi) * (lat - yi) / ((yj - yi) || 1e-12) + xi)) { inside = !inside; }
		}
		return inside;
	}
	function inBox(x, b) { return x.lat >= b.s && x.lat <= b.n && x.lng >= b.w && x.lng <= b.e; }
	function inRing(x, z) { return inBox(x, z.bbox) && inRingLL(x.lng, x.lat, z.ring); }
	function inGeom(lng, lat, g) { // a GeoJSON Polygon or MultiPolygon: inside an outer ring and not in one of its holes
		var polys = g.type === 'Polygon' ? [g.coordinates] : (g.type === 'MultiPolygon' ? g.coordinates : []);
		for (var p = 0; p < polys.length; p++) {
			var rings = polys[p];
			if (rings.length && inRingLL(lng, lat, rings[0])) {
				var hole = false;
				for (var h = 1; h < rings.length; h++) { if (inRingLL(lng, lat, rings[h])) { hole = true; break; } }
				if (!hole) { return true; }
			}
		}
		return false;
	}
	function inIso(x) { var I = S.iso; return !!I && inBox(x, I.bbox) && inGeom(x.lng, x.lat, I.geom); }
	function bboxOf(cs) { var b = { w: 1e9, s: 1e9, e: -1e9, n: -1e9 }; cs.forEach(function (c) { b.w = Math.min(b.w, c[0]); b.e = Math.max(b.e, c[0]); b.s = Math.min(b.s, c[1]); b.n = Math.max(b.n, c[1]); }); return b; }
	function geomCoords(g) { var out = []; (g.type === 'Polygon' ? [g.coordinates] : g.coordinates).forEach(function (p) { (p[0] || []).forEach(function (c) { out.push(c); }); }); return out; }
	function ringCentre(z) { var r = z.ring.slice(0, -1), la = 0, ln = 0; r.forEach(function (c) { ln += c[0]; la += c[1]; }); return { lat: la / r.length, lng: ln / r.length }; }
	function dp(pts, eps) { // Douglas-Peucker on [x, y] points
		if (pts.length < 3) { return pts.slice(); }
		var keep = [], stack = [[0, pts.length - 1]];
		keep[0] = keep[pts.length - 1] = true;
		while (stack.length) {
			var s = stack.pop(), a = pts[s[0]], b = pts[s[1]], dx = b[0] - a[0], dy = b[1] - a[1], L = dx * dx + dy * dy, md = -1, mi = -1;
			for (var i = s[0] + 1; i < s[1]; i++) {
				var p = pts[i], t = L ? ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L : 0;
				t = t < 0 ? 0 : t > 1 ? 1 : t;
				var ex = a[0] + t * dx - p[0], ey = a[1] + t * dy - p[1], d = ex * ex + ey * ey;
				if (d > md) { md = d; mi = i; }
			}
			if (mi > -1 && md > eps * eps) { keep[mi] = true; stack.push([s[0], mi], [mi, s[1]]); }
		}
		return pts.filter(function (p, i) { return keep[i]; });
	}
	function simplifyTo(pts, max, eps) { var out = dp(pts, eps); while (out.length > max && eps < 1e6) { eps *= 1.6; out = dp(pts, eps); } return out; }
	function circleGeom(c, rKm) {
		var ring = [], kx = 111.32 * Math.cos(c.lat * Math.PI / 180), ky = 110.574;
		for (var i = 0; i <= 64; i++) { var a = i / 64 * 2 * Math.PI; ring.push([c.lng + rKm * Math.cos(a) / kx, c.lat + rKm * Math.sin(a) / ky]); }
		ring[64] = ring[0].slice();
		return { type: 'Polygon', coordinates: [ring] };
	}
	function slimGeom(g) { // the isochrone as the browser keeps it: 400 points a ring at most, 5 decimals
		function ring(r) { var s = r.length > 400 ? simplifyTo(r, 400, 0.00005) : r; return s.map(function (c) { return [Math.round(c[0] * 1e5) / 1e5, Math.round(c[1] * 1e5) / 1e5]; }); }
		if (g.type === 'Polygon') { return { type: 'Polygon', coordinates: g.coordinates.map(ring) }; }
		return { type: 'MultiPolygon', coordinates: g.coordinates.map(function (p) { return p.map(ring); }) };
	}
	function shv() { return root.classList.contains('is-sheet') ? (SH.vis || 0) : 0; } // the phone sheet's height over the map
	function camPad(p) { return { top: p, left: p, right: p, bottom: p + shv() }; }
	function fitBox(b, maxZ) {
		if (!S.map || !b) { return; }
		try { S.map.fitBounds([[b.w, b.s], [b.e, b.n]], { padding: camPad(48), maxZoom: maxZ || 15, duration: RM ? 0 : 600 }); } catch (e) { /* keep the view */ }
		userMoved = false; el.area.hidden = true;
	}
	var DLG = { can: false, isOpen: function () { return false; }, open: function () {} }; // the full-screen dialog ("מסך מלא"), when the page has one
	root.classList.add('nlnf--nodraw'); // until a dialog is there: on a phone the zone is drawn inside the dialog only

	/* ------------------------------------------------------------ v3: draw a zone */
	var DR = null;
	function drawLabel() {
		var on = root.classList.contains('is-draw');
		el.draw.textContent = S.zone && !on ? 'ניקוי אזור' : 'ציירו אזור';
		el.draw.setAttribute('aria-pressed', on ? 'true' : 'false');
		el.draw.classList.toggle('has-zone', !!S.zone && !on);
	}
	function drawOn() {
		if (S.mapState !== 'on') { return; }
		if (!wide() && DLG.can && !DLG.isOpen()) { DLG.open(); setTimeout(drawOn, RM ? 80 : 450); return; } // a phone draws inside the dialog only
		if (!wide() && !DLG.can) { return; }
		endPick(); measureOff(); closeCard(); closeAlert(); closeSh();
		if (root.classList.contains('is-sheet')) { setSnap('peek', true); }
		root.classList.add('is-draw');
		el.pad.hidden = false; el.padL.setAttribute('points', '');
		el.drw.hidden = false; el.area.hidden = true;
		el.drwT.textContent = window.matchMedia && window.matchMedia('(pointer:coarse)').matches ? 'ציירו באצבע קו סביב האזור שמעניין אתכם' : 'ציירו בעכבר קו סביב האזור שמעניין אתכם';
		drawLabel();
		ev('zone_start');
	}
	function drawOff() {
		if (!root.classList.contains('is-draw')) { return; }
		DR = null;
		root.classList.remove('is-draw');
		el.pad.hidden = true; el.drw.hidden = true; el.padL.setAttribute('points', '');
		drawLabel();
	}
	function padXY(e) { var r = el.pad.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
	el.pad.addEventListener('pointerdown', function (e) { // the pad exists only while drawing: it is the only element that takes the touch
		if ((e.button && e.button > 0) || DR) { return; }
		e.preventDefault();
		try { el.pad.setPointerCapture(e.pointerId); } catch (err) { /* old browser */ }
		DR = { id: e.pointerId, pts: [padXY(e)] };
		el.padL.setAttribute('points', DR.pts[0].join(','));
	});
	el.pad.addEventListener('pointermove', function (e) {
		if (!DR || e.pointerId !== DR.id) { return; }
		e.preventDefault();
		var p = padXY(e), q = DR.pts[DR.pts.length - 1];
		if (Math.abs(p[0] - q[0]) + Math.abs(p[1] - q[1]) < 3 || DR.pts.length > 4000) { return; }
		DR.pts.push(p);
		el.padL.setAttribute('points', DR.pts.map(function (z) { return Math.round(z[0]) + ',' + Math.round(z[1]); }).join(' '));
	});
	function padEnd(e) {
		if (!DR || e.pointerId !== DR.id) { return; }
		var pts = DR.pts, b = bboxOf(pts);
		DR = null;
		var sp = pts.length >= 6 && (b.e - b.w) >= 24 && (b.n - b.s) >= 24 ? simplifyTo(pts, 60, 2) : [];
		if (sp.length > 3 && sp[0][0] === sp[sp.length - 1][0] && sp[0][1] === sp[sp.length - 1][1]) { sp.pop(); }
		if (sp.length < 3) { // too short: still drawing
			el.padL.setAttribute('points', '');
			el.drwT.textContent = 'ציירו קו סגור סביב האזור, בלי להרים את האצבע או את העכבר';
			return;
		}
		var ring = sp.map(function (p) { var ll = S.map.unproject(p); return [Math.round(ll.lng * 1e5) / 1e5, Math.round(ll.lat * 1e5) / 1e5]; });
		ring.push(ring[0].slice());
		S.zone = { ring: ring, bbox: bboxOf(ring) };
		drawOff();
		S.bounds = null; S.group = null; S.shown = 30;
		renderAll(); drawZone();
		fitBox(S.zone.bbox, 16);
		if (root.classList.contains('is-sheet')) { setSnap('half', true); }
		ev('zone', { points: ring.length - 1 });
	}
	el.pad.addEventListener('pointerup', padEnd);
	el.pad.addEventListener('pointercancel', function () { DR = null; el.padL.setAttribute('points', ''); });
	function drawZone() {
		if (!S.map || S.mapState !== 'on' || !S.map.getSource('nf-zone')) { return; }
		try { S.map.getSource('nf-zone').setData(S.zone ? { type: 'Feature', properties: {}, geometry: { type: 'Polygon', coordinates: [S.zone.ring] } } : EMPTY); } catch (e) { /* not loaded */ }
	}
	function clearZone() { if (!S.zone) { return; } S.zone = null; S.shown = 30; drawZone(); renderAll(); drawLabel(); ev('zone_clear'); }
	el.draw.addEventListener('click', function () { if (root.classList.contains('is-draw')) { drawOff(); } else if (S.zone) { clearZone(); } else { drawOn(); } });
	el.drwX.addEventListener('click', drawOff);

	/* ------------------------------------------------------------ v3: travel time (Mapbox Isochrone, only on the visitor's request) */
	var MODES = { driving: 'ברכב', walking: 'ברגל', cycling: 'באופניים' };
	var TT = { from: '', mode: 'driving', min: 20, busy: false };
	function ttFroms() { // where a travel time can start: me (when the location is known), then my places
		var a = [];
		if (S.origin && S.origin.kind === 'me') { a.push({ k: 'me', name: 'המיקום שלי', from: 'ממך', lat: S.origin.lat, lng: S.origin.lng }); }
		SLOTS.forEach(function (s) { var p = S.anchors[s.k]; if (p) { a.push({ k: s.k, name: s.name, from: s.from, lat: p.lat, lng: p.lng }); } });
		return a;
	}
	function isoText(I) { return 'עד ' + I.min + ' דק׳ ' + MODES[I.mode] + ' ' + I.from + (I.est ? ' · הערכה לפי מרחק' : ''); }
	function estKm(mode, min) { // the finder's own air-distance estimate, inverted (the honest fallback)
		if (mode === 'walking') { return min / 60 * 4.8 / 1.35; }
		if (mode === 'cycling') { return min / 60 * 15 / 1.35; }
		var lo = 0, hi = 150;
		for (var i = 0; i < 40; i++) { var mid = (lo + hi) / 2; if (driveRaw(mid) <= min) { lo = mid; } else { hi = mid; } }
		return lo;
	}
	function ssGet(k) { try { var v = window.sessionStorage.getItem(k); return v ? JSON.parse(v) : null; } catch (e) { return null; } }
	function ssSet(k, v) { try { window.sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* full or blocked: the next request asks again */ } }
	function isoKey(lat, lng, mode, min) { return 'nlnf_iso_v1:' + lat.toFixed(3) + ',' + lng.toFixed(3) + ':' + mode + ':' + min; }
	function drawIso() {
		if (!S.map || S.mapState !== 'on' || !S.map.getSource('nf-iso')) { return; }
		try { S.map.getSource('nf-iso').setData(S.iso ? { type: 'Feature', properties: { est: S.iso.est ? 1 : 0 }, geometry: S.iso.geom } : EMPTY); } catch (e) { /* not loaded */ }
	}
	function setIso(I) {
		S.iso = I; S.shown = 30;
		closeSh(); closeCard();
		renderAll(); drawIso();
		if (I) { fitBox(I.bbox, 15); if (root.classList.contains('is-sheet')) { setSnap('half', true); } }
	}
	function clearIso() { if (!S.iso) { return; } S.iso = null; S.shown = 30; drawIso(); renderAll(); }
	function ttErr(t) { var e = $('nlnf-tt-err'); if (e) { e.textContent = t || ''; e.hidden = !t; } }
	function ttBusy(on) { var b = el.sh.querySelector('[data-tt=go]'); if (b) { b.disabled = !!on; b.textContent = on ? 'מחשבים…' : 'הציגו את האזור'; } }
	function travelGo() {
		if (TT.busy) { return; }
		var fr = ttFroms().filter(function (x) { return x.k === TT.from; })[0];
		if (!fr) { ttErr('בחרו מאיפה לחשב.'); return; }
		var lat = r3(fr.lat), lng = r3(fr.lng), mode = MODES[TT.mode] ? TT.mode : 'driving', min = [10, 20, 30].indexOf(TT.min) > -1 ? TT.min : 20; // about 100 m
		var base = { mode: mode, min: min, from: fr.from, fromK: fr.k, lat: lat, lng: lng };
		function est() { var g = circleGeom({ lat: lat, lng: lng }, estKm(mode, min)); setIso(Object.assign({}, base, { est: true, geom: g, bbox: bboxOf(g.coordinates[0]) })); }
		var key = isoKey(lat, lng, mode, min), hit = ssGet(key);
		if (hit && (hit.type === 'Polygon' || hit.type === 'MultiPolygon')) { setIso(Object.assign({}, base, { est: false, geom: hit, bbox: bboxOf(geomCoords(hit)) })); ev('travel', { mode: mode, min: min, result: 'cache' }); return; }
		if (!D.mb || !window.fetch) { est(); ev('travel', { mode: mode, min: min, result: 'est' }); return; }
		TT.busy = true; ttBusy(true); ttErr('');
		var ctl = window.AbortController ? new AbortController() : null, tm = setTimeout(function () { if (ctl) { ctl.abort(); } }, 9000);
		// the one call that carries a point out of the browser: the chosen place or my location, rounded to 0.001°, to Mapbox only
		var url = 'https://api.mapbox.com/isochrone/v1/mapbox/' + mode + '/' + lng.toFixed(3) + ',' + lat.toFixed(3) + '?contours_minutes=' + min + '&polygons=true&denoise=1&generalize=30&access_token=' + encodeURIComponent(D.mb);
		fetch(url, { credentials: 'omit', signal: ctl ? ctl.signal : undefined })
			.then(function (r) { if (!r.ok) { throw new Error('http ' + r.status); } return r.json(); })
			.then(function (j) {
				var g = j && j.features && j.features[0] && j.features[0].geometry;
				if (!g || (g.type !== 'Polygon' && g.type !== 'MultiPolygon') || !geomCoords(g).length) { throw new Error('shape'); }
				g = slimGeom(g);
				ssSet(key, g);
				TT.busy = false;
				setIso(Object.assign({}, base, { est: false, geom: g, bbox: bboxOf(geomCoords(g)) }));
				ev('travel', { mode: mode, min: min, result: 'ok' });
			})
			.catch(function () { TT.busy = false; est(); ev('travel', { mode: mode, min: min, result: 'est' }); })
			.then(function () { clearTimeout(tm); TT.busy = false; ttBusy(false); });
	}

	/* ------------------------------------------------------------ v3: the side sheets (the full filters, the travel time) */
	var SALE_STEPS = [500000, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000, 4500000, 5000000, 6000000, 7000000, 8000000, 10000000, 12000000, 15000000, 20000000, 30000000];
	var RENT_STEPS = [2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000, 12000, 15000, 20000, 25000, 30000];
	var SQM_STEPS = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 140, 160, 180, 200, 250, 300, 400, 500];
	var SHK = null;
	function have() { // which facts this tab's listings state: a filter shows only when one does
		var h = { sqm: false, floor: false, elev: false, park: false, balc: false, halves: {}, ftop: 0 };
		S.L.forEach(function (x) { if (x.rooms > 0 && x.rooms % 1) { h.halves[x.rooms] = 1; } });
		pool().forEach(function (x) {
			if (x.sqm > 0) { h.sqm = true; }
			if (x.floor != null) { h.floor = true; h.ftop = Math.max(h.ftop, x.floor); }
			if (x.elevator === true) { h.elev = true; }
			if (x.parking === true) { h.park = true; }
			if (x.balcony > 0) { h.balc = true; }
		});
		return h;
	}
	function roomSteps(h) { var a = []; for (var r = 1; r <= 10; r += 0.5) { if (r % 1 === 0 || h.halves[r]) { a.push(r); } } return a; }
	function fsel(name, lab, steps, val, fmt, isFloor) { // one "from" or "to" select; the empty choice is "הכול"
		var none = isFloor ? val == null : !val;
		return '<label class="nlnf-fs__sel"><span class="nlnf-fs__k">' + lab + '</span><select data-ff="' + name + '"><option value=""' + (none ? ' selected' : '') + '>הכול</option>'
			+ steps.map(function (v) { return '<option value="' + v + '"' + (!none && val === v ? ' selected' : '') + '>' + esc(fmt(v)) + '</option>'; }).join('') + '</select></label>';
	}
	function fpair(title, id, a, b) { return '<div class="nlnf-fs__grp" role="group" aria-labelledby="' + id + '"><span class="nlnf-al__lab" id="' + id + '">' + title + '</span><div class="nlnf-fs__pair">' + a + b + '</div></div>'; }
	function fchk(k, label, on) { return '<label class="nlnf-al__opt"><input type="checkbox" data-ff="' + k + '"' + (on ? ' checked' : '') + '><span><b>' + label + '</b></span></label>'; }
	function shBar() { return '<div class="nlnf-card__bar"><button type="button" class="nlnf-card__back" data-sh="close">' + CHEV + (wide() ? 'חזרה לרשימה' : 'חזרה') + '</button></div>'; }
	function floorName(f) { return f === 0 ? 'קרקע' : String(f); }
	function filtersHtml() {
		var h = have(), deal = S.tab, pp = S.fp[deal], F = S.f, rs = roomSteps(h);
		var steps = deal === 'rent' ? RENT_STEPS : SALE_STEPS, pf = function (v) { return priceLabel(v, deal); }, sq = function (v) { return grp(v) + ' מ״ר'; };
		var fl = []; for (var i = 0; i <= Math.min(60, Math.max(10, h.ftop)); i++) { fl.push(i); }
		return shBar() + '<div class="nlnf-al__in nlnf-fs">'
			+ '<div class="nlnf-al__head"><h3 class="nlnf-al__h" id="nlnf-sh-t" tabindex="-1">סינון</h3><p class="nlnf-al__lead">' + (deal === 'rent' ? 'דירות להשכרה' : 'דירות למכירה') + ': בחרו מה חשוב לכם. המפה והרשימה מתעדכנות מיד.</p></div>'
			+ fpair('חדרים', 'nlnf-fs-r', fsel('rooms', 'מ־', rs, F.rooms, num), fsel('rmax', 'עד', rs, F.rmax, num))
			+ fpair(deal === 'rent' ? 'שכר דירה לחודש' : 'מחיר', 'nlnf-fs-p', fsel('pmin', 'מ־', steps, pp.min, pf), fsel('pmax', 'עד', steps, pp.max, pf))
			+ (h.sqm ? fpair('גודל', 'nlnf-fs-s', fsel('smin', 'מ־', SQM_STEPS, F.smin, sq), fsel('smax', 'עד', SQM_STEPS, F.smax, sq)) : '')
			+ (h.floor ? fpair('קומה', 'nlnf-fs-f', fsel('fmin', 'מ־', fl, F.fmin, floorName, true), fsel('fmax', 'עד', fl, F.fmax, floorName, true)) : '')
			+ '<div class="nlnf-fs__grp"><span class="nlnf-al__lab" id="nlnf-fs-c">בבית</span><fieldset class="nlnf-al__what" aria-labelledby="nlnf-fs-c"><legend class="nlnf__sr">בבית</legend>'
			+ fchk('mamad', 'ממ״ד', F.mamad) + (h.elev ? fchk('elev', 'מעלית', F.elev) : '') + (h.park ? fchk('park', 'חניה', F.park) : '') + (h.balc ? fchk('balc', 'מרפסת', F.balc) : '')
			+ '</fieldset></div>'
			+ '<p class="nlnf-al__fine">נכס שהמפרסם לא ציין בו גודל, קומה, מעלית, חניה או מרפסת לא יופיע כשתסננו לפי הפרט הזה.</p>'
			+ '<div class="nlnf-fs__foot"><button type="button" class="nlnf-btn" data-sh="reset">ניקוי</button><button type="button" class="nlnf-btn nlnf-btn--pri" data-sh="close" id="nlnf-fs-go"></button></div>'
			+ '<p class="nlnf__sr" id="nlnf-fs-n" role="status" aria-live="polite"></p>'
			+ '</div>';
	}
	function fsCount() { // the live count on the button; never "0"
		var n = results().length, t = n ? 'הציגו ' + (n === 1 ? 'נכס אחד' : grp(n) + ' נכסים') : 'אין נכסים בסינון הזה, נסו להרחיב';
		var b = $('nlnf-fs-go'); if (b) { b.textContent = t; b.classList.toggle('nlnf-btn--pri', n > 0); b.classList.toggle('is-none', !n); }
		var s = $('nlnf-fs-n'); if (s) { s.textContent = t; }
	}
	function ffSet(name, v) { var s = el.sh.querySelector('[data-ff="' + name + '"]'); if (s) { s.value = v == null || v === 0 && name.charAt(0) !== 'f' ? '' : String(v); } }
	function ffChange(s) {
		var k = s.getAttribute('data-ff'), F = S.f, pp = S.fp[S.tab];
		var v = s.type === 'checkbox' ? s.checked : (s.value === '' ? null : +s.value);
		if (k === 'pmin' || k === 'pmax') { pp[k === 'pmin' ? 'min' : 'max'] = v || 0; }
		else if (k === 'fmin' || k === 'fmax') { F[k] = v; }
		else if (s.type === 'checkbox') { F[k] = !!v; }
		else { F[k] = v || 0; }
		// a "from" above the "to" (or the reverse): the other end follows the one just changed
		if (F.rooms && F.rmax && F.rooms > F.rmax) { if (k === 'rooms') { F.rmax = F.rooms; ffSet('rmax', F.rmax); } else { F.rooms = F.rmax; ffSet('rooms', F.rooms); } }
		if (pp.min && pp.max && pp.min > pp.max) { if (k === 'pmin') { pp.max = pp.min; ffSet('pmax', pp.max); } else { pp.min = pp.max; ffSet('pmin', pp.min); } }
		if (F.smin && F.smax && F.smin > F.smax) { if (k === 'smin') { F.smax = F.smin; ffSet('smax', F.smax); } else { F.smin = F.smax; ffSet('smin', F.smin); } }
		if (F.fmin != null && F.fmax != null && F.fmin > F.fmax) { if (k === 'fmin') { F.fmax = F.fmin; ffSet('fmax', F.fmax); } else { F.fmin = F.fmax; ffSet('fmin', F.fmin); } }
		S.shown = 30;
		renderAll(); fsCount();
		ev('filter', { name: k });
	}
	function fsReset() {
		S.f = Object.assign(fBlank(), { mkt: S.f.mkt, near: S.f.near });
		S.fp[S.tab] = { min: 0, max: 0 };
		S.shown = 30;
		renderAll();
		el.sh.innerHTML = filtersHtml(); fsCount();
		var b = el.sh.querySelector('[data-sh=reset]'); if (b) { try { b.focus({ preventScroll: true }); } catch (e) { b.focus(); } }
		ev('filter', { name: 'reset' });
	}
	function travelHtml() {
		var fs = ttFroms();
		var h = shBar() + '<div class="nlnf-al__in nlnf-tt">'
			+ '<div class="nlnf-al__head"><h3 class="nlnf-al__h" id="nlnf-sh-t" tabindex="-1">זמן נסיעה</h3><p class="nlnf-al__lead">נכסים שמגיעים מהם בזמן שתבחרו, לפי הכבישים והשבילים, מהמקום שחשוב לכם.</p></div>';
		if (!fs.length) {
			h += '<p class="nlnf-al__lead">סמנו קודם מקום ב״המקומות שלי״, או לחצו על ״המיקום שלי״.</p><div class="nlnf-empty__go">'
				+ '<button type="button" class="nlnf-btn nlnf-btn--pri" data-tt="me">המיקום שלי</button>'
				+ SLOTS.map(function (s) { return '<button type="button" class="nlnf-btn" data-slot="' + s.k + '">+ ' + esc(s.add) + '</button>'; }).join('') + '</div>';
		} else {
			h += '<div class="nlnf-al__grp"><span class="nlnf-al__lab" id="nlnf-tt-fl">מאיפה</span><div class="nlnf-tt__from" role="radiogroup" aria-labelledby="nlnf-tt-fl">'
				+ fs.map(function (x) { return '<label><input type="radio" name="ttfrom" value="' + x.k + '"' + (TT.from === x.k ? ' checked' : '') + '><span>' + esc(x.name) + '</span></label>'; }).join('') + '</div></div>'
				+ '<div class="nlnf-al__grp"><span class="nlnf-al__lab" id="nlnf-tt-ml">איך</span><div class="nlnf-al__seg" role="radiogroup" aria-labelledby="nlnf-tt-ml">'
				+ ['driving', 'walking', 'cycling'].map(function (m) { return '<label><input type="radio" name="ttmode" value="' + m + '"' + (TT.mode === m ? ' checked' : '') + '><span>' + MODES[m] + '</span></label>'; }).join('') + '</div></div>'
				+ '<div class="nlnf-al__grp"><span class="nlnf-al__lab" id="nlnf-tt-nl">תוך כמה זמן</span><div class="nlnf-al__seg" role="radiogroup" aria-labelledby="nlnf-tt-nl">'
				+ [10, 20, 30].map(function (n) { return '<label><input type="radio" name="ttmin" value="' + n + '"' + (TT.min === n ? ' checked' : '') + '><span>' + n + ' דק׳</span></label>'; }).join('') + '</div></div>'
				+ '<button type="button" class="nlnf-btn nlnf-btn--pri nlnf-al__go" data-tt="go">הציגו את האזור</button>'
				+ '<p class="nlnf-al__err" id="nlnf-tt-err" role="alert" hidden></p>';
		}
		return h + (S.iso ? '<button type="button" class="nlnf-btn" data-tt="clear">ניקוי זמן הנסיעה</button>' : '')
			+ '<p class="nlnf-al__fine">זמני הנסיעה מחושבים אצל Mapbox לפי הכבישים והשבילים, בלי פקקים של הרגע. לשם כך נשלחת ל־Mapbox רק הנקודה שבחרתם, בעיגול של כ־100 מ׳; אלינו היא לא נשלחת. אם החישוב לא זמין, נציג הערכה לפי מרחק.</p></div>';
	}
	function openSh(kind, opener) {
		closeCard(); closeAlert(); measureOff(); endPick(); drawOff(); say('');
		S.sh = kind; SHK = kind;
		if (kind === 't') { var fs = ttFroms(); if (!fs.some(function (x) { return x.k === TT.from; })) { TT.from = fs.length ? fs[0].k : ''; } }
		root.style.setProperty('--nf-wa', waInset() + 'px');
		el.sh.innerHTML = kind === 'f' ? filtersHtml() : travelHtml();
		el.sh.hidden = false;
		el.sh.setAttribute('aria-modal', wide() ? 'false' : 'true');
		root.classList.add('is-sh');
		if (!wide()) { el.sh.scrollTop = 0; }
		var t = $('nlnf-sh-t'); if (t) { try { t.focus({ preventScroll: wide() }); } catch (e) { t.focus(); } }
		if (kind === 'f') { fsCount(); }
		ev(kind === 'f' ? 'filters_open' : 'travel_open');
	}
	function closeSh() {
		if (!el.sh || el.sh.hidden) { return false; }
		el.sh.hidden = true; el.sh.innerHTML = ''; root.classList.remove('is-sh'); S.sh = null;
		var o = el.chips.querySelector('[data-sh="' + SHK + '"]'); // the chips are drawn again on every change: back to the chip that opened it
		if (o) { try { o.focus({ preventScroll: true }); } catch (e) { /* gone */ } }
		return true;
	}

	/* ------------------------------------------------------------ v3: the phone sheet (inside the dialog only): peek, half, full */
	var SH = { snap: 'peek', vis: 0, drag: null, moved: false };
	var SNAPS = ['peek', 'half', 'full'];
	var SNAP_T = { peek: 'הגדילו את רשימת הנכסים', half: 'הרשימה בחצי מסך. לחצו למסך מלא', full: 'הקטינו את רשימת הנכסים' };
	function waInset() { // the wide WhatsApp bar stays above the dialog: the sheet keeps its content above it (measured, never moved)
		var o = document.getElementById('nlcta');
		if (!o) { return 0; }
		var r = o.getBoundingClientRect(), cs = window.getComputedStyle(o), vh = window.innerHeight;
		if (!(r.width > 0 && r.height > 0) || cs.display === 'none' || cs.visibility === 'hidden' || r.top < vh * 0.5 || r.top >= vh) { return 0; }
		return Math.max(0, Math.round(vh - r.top));
	}
	function snapPx(n) {
		var H = el.mapwrap.offsetHeight || 400, peek = Math.min(H, 124 + waInset());
		if (n === 'full') { return H; }
		if (n === 'half') { return Math.min(H, Math.max(Math.round(H * 0.58), peek + 130)); }
		return peek;
	}
	function applyVis(v, anim) {
		SH.vis = Math.round(v);
		el.panel.classList.toggle('is-anim', !!anim && !RM);
		el.panel.style.height = SH.vis + 'px';
		root.style.setProperty('--nf-shv', SH.vis + 'px');
	}
	function setSnap(n, anim) {
		if (!root.classList.contains('is-sheet')) { return; }
		SH.snap = n;
		applyVis(snapPx(n), anim);
		root.classList.toggle('is-full', n === 'full');
		el.grab.setAttribute('aria-label', SNAP_T[n]);
	}
	function updateSheet() {
		var on = !!root.closest('.nlnf-dlg') && !wide(), was = root.classList.contains('is-sheet'), db = document.getElementById('nlnf-dlg-body');
		root.classList.toggle('is-sheet', on);
		if (db) { db.classList.toggle('is-sheet', on); }
		if (on) {
			root.style.setProperty('--nf-wa', waInset() + 'px');
			el.grab.removeAttribute('aria-hidden'); el.grab.tabIndex = 0;
			setSnap(was ? SH.snap : 'peek', false);
		} else if (was) {
			el.grab.setAttribute('aria-hidden', 'true'); el.grab.tabIndex = -1; el.grab.removeAttribute('aria-label');
			el.panel.style.height = ''; el.panel.classList.remove('is-anim');
			root.style.removeProperty('--nf-shv'); root.classList.remove('is-full');
			SH.vis = 0; SH.drag = null;
		}
	}
	el.grab.addEventListener('click', function () {
		if (SH.moved) { SH.moved = false; return; } // the end of a drag, not a press
		if (!root.classList.contains('is-sheet')) { return; }
		setSnap(SNAPS[(SNAPS.indexOf(SH.snap) + 1) % 3], true);
		ev('sheet', { snap: SH.snap, by: 'press' });
	});
	el.grab.addEventListener('keydown', function (e) {
		if (!root.classList.contains('is-sheet')) { return; }
		var i = SNAPS.indexOf(SH.snap);
		if (e.key === 'ArrowUp' && i < 2) { setSnap(SNAPS[i + 1], true); e.preventDefault(); }
		else if (e.key === 'ArrowDown' && i > 0) { setSnap(SNAPS[i - 1], true); e.preventDefault(); }
	});
	el.grab.addEventListener('pointerdown', function (e) { // the handle only (touch-action: none on it alone, inside the dialog)
		if (!root.classList.contains('is-sheet') || (e.button && e.button > 0)) { return; }
		SH.drag = { id: e.pointerId, y0: e.clientY, v0: SH.vis, y1: e.clientY, t1: Date.now(), vy: 0 };
		SH.moved = false;
		try { el.grab.setPointerCapture(e.pointerId); } catch (err) { /* old browser */ }
		el.panel.classList.remove('is-anim');
	});
	el.grab.addEventListener('pointermove', function (e) {
		var G = SH.drag;
		if (!G || e.pointerId !== G.id) { return; }
		if (!SH.moved && Math.abs(G.y0 - e.clientY) < 6) { return; }
		SH.moved = true;
		e.preventDefault();
		var now = Date.now();
		G.vy = (G.y1 - e.clientY) / Math.max(1, now - G.t1); G.y1 = e.clientY; G.t1 = now;
		applyVis(Math.max(snapPx('peek') * 0.7, Math.min(snapPx('full'), G.v0 + G.y0 - e.clientY)), false);
	});
	function grabEnd(e) {
		var G = SH.drag;
		if (!G || e.pointerId !== G.id) { return; }
		SH.drag = null;
		if (!SH.moved) { return; } // a press: the click moves one step
		var v = SH.vis + Math.max(-1.5, Math.min(1.5, G.vy || 0)) * 160, best = 'peek', bd = 1e9; // a flick carries on a little
		SNAPS.forEach(function (n) { var d = Math.abs(snapPx(n) - v); if (d < bd) { bd = d; best = n; } });
		setSnap(best, true);
		ev('sheet', { snap: best, by: 'drag' });
	}
	el.grab.addEventListener('pointerup', grabEnd);
	el.grab.addEventListener('pointercancel', grabEnd);

	/* ------------------------------------------------------------ places: me, a city or neighbourhood, my places */
	function setOrigin(o, quiet) {
		S.origin = o; S.bounds = null; S.group = null; S.shown = 30;
		closeAlert(); closeCard();
		drop();
		renderAll();
		if (S.sh === 't' && o && o.kind === 'me') { TT.from = 'me'; el.sh.innerHTML = travelHtml(); } // "המיקום שלי" pressed inside the travel sheet
		drawMe();
		if (o && S.map) { flyTo(o.lat, o.lng, o.zoom || 13); if (o.kind === 'me') { setTimeout(function () { burst(o.lat, o.lng); }, RM ? 0 : 950); } }
		if (!quiet && o) { ev(o.kind === 'me' ? 'locate' : 'place', o.kind === 'me' ? { result: 'ok' } : { kind: o.pkind || 'city' }); }
	}
	function locate(auto) {
		if (!navigator.geolocation) { if (!auto) { say('הדפדפן לא נותן מיקום. בחרו עיר או שכונה, והרשימה תסתדר לפיה.'); } return; }
		el.me.setAttribute('aria-busy', 'true');
		say('מחפשים את המיקום שלכם…');
		navigator.geolocation.getCurrentPosition(function (p) {
			el.me.removeAttribute('aria-busy'); say('');
			el.q.value = '';
			setOrigin({ kind: 'me', label: 'המיקום שלי', lat: p.coords.latitude, lng: p.coords.longitude, zoom: 13 });
		}, function (err) {
			el.me.removeAttribute('aria-busy');
			say(err && err.code === 1 ? 'לא קיבלנו את המיקום. בחרו עיר או שכונה, והרשימה תסתדר לפיה.' : 'המיקום לא התקבל הפעם. נסו שוב, או בחרו עיר או שכונה.');
			ev('locate', { result: err && err.code === 1 ? 'denied' : 'fail' });
		}, { enableHighAccuracy: false, timeout: 8000, maximumAge: 300000 });
	}
	el.me.addEventListener('click', function () { locate(false); });
	var sugIdx = -1, sugList = [];
	function showSug() {
		var v = norm(el.q.value);
		sugList = (v ? S.places.filter(function (p) { return norm(p.name).indexOf(v) > -1; }) : S.places).slice(0, 8);
		sugIdx = -1;
		if (!sugList.length || document.activeElement !== el.q) { el.sug.hidden = true; el.q.setAttribute('aria-expanded', 'false'); return; }
		el.sug.innerHTML = sugList.map(function (p, i) { return '<li role="option" id="nlnf-sug-' + i + '" data-i="' + i + '" aria-selected="false"><b>' + esc(p.name) + '</b><span>' + esc(p.kind === 'hood' ? 'שכונה' + (p.sub ? ', ' + p.sub : '') : 'עיר') + '</span></li>'; }).join('');
		el.sug.hidden = false; el.q.setAttribute('aria-expanded', 'true');
	}
	function pickSug(i) {
		var p = sugList[i]; if (!p) { return; }
		el.q.value = p.name; el.sug.hidden = true; el.q.setAttribute('aria-expanded', 'false');
		if (S.picking) { setAnchor(S.picking, p.lat, p.lng); return; }
		setOrigin({ kind: 'place', pkind: p.kind, label: p.name, lat: p.lat, lng: p.lng, zoom: p.kind === 'hood' ? 14 : 12 });
	}
	el.q.addEventListener('input', function () { showSug(); if (!el.q.value && S.origin && S.origin.kind === 'place') { setOrigin(null, true); } });
	el.q.addEventListener('focus', showSug);
	el.q.addEventListener('blur', function () { setTimeout(function () { el.sug.hidden = true; el.q.setAttribute('aria-expanded', 'false'); }, 160); });
	el.q.addEventListener('keydown', function (e) {
		if (el.sug.hidden) { if (e.key === 'ArrowDown') { showSug(); } return; }
		if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
			e.preventDefault();
			sugIdx = (sugIdx + (e.key === 'ArrowDown' ? 1 : -1) + sugList.length) % sugList.length;
			[].forEach.call(el.sug.children, function (li, i) { li.setAttribute('aria-selected', i === sugIdx ? 'true' : 'false'); });
			el.q.setAttribute('aria-activedescendant', 'nlnf-sug-' + sugIdx);
		} else if (e.key === 'Enter') { e.preventDefault(); pickSug(sugIdx > -1 ? sugIdx : 0); }
		else if (e.key === 'Escape') { e.stopPropagation(); el.sug.hidden = true; el.q.setAttribute('aria-expanded', 'false'); }
	});
	el.sug.addEventListener('mousedown', function (e) { var li = e.target.closest('li[data-i]'); if (li) { e.preventDefault(); pickSug(+li.getAttribute('data-i')); } });

	function startPick(slot) {
		var s = SLOTS.filter(function (z) { return z.k === slot; })[0]; if (!s) { return; }
		closeCard(); measureOff(); closeSh(); drawOff();
		S.picking = slot;
		if (S.mapState === 'on') {
			el.pickT.textContent = 'הקישו על המפה במקום: ' + s.name;
			el.pick.hidden = false; el.area.hidden = true;
			S.map.getCanvas().style.cursor = 'crosshair';
			if (root.classList.contains('is-sheet')) { setSnap('peek', true); } else { el.mapwrap.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'center' }); }
		} else { // no map: the place box chooses it
			say('בחרו עיר או שכונה עבור: ' + s.name);
			el.q.value = ''; el.q.focus(); showSug();
		}
	}
	function endPick() { S.picking = null; el.pick.hidden = true; if (S.map && !S.measure) { S.map.getCanvas().style.cursor = ''; } }
	function setAnchor(slot, lat, lng) {
		S.anchors[slot] = { lat: Math.round(lat * 1e5) / 1e5, lng: Math.round(lng * 1e5) / 1e5 };
		saveAnchors(); endPick(); say('');
		ev('anchor', { slot: slot });
		S.shown = 30;
		renderAll(); drawAnchors();
	}
	el.pickX.addEventListener('click', function () { endPick(); });

	/* ------------------------------------------------------------ events */
	root.addEventListener('click', function (e) {
		var t = e.target.closest('button, a');
		if (!t || !root.contains(t)) { return; }
		var a;
		if ((a = t.getAttribute('data-sh'))) { // v3: the full filters and the travel time
			if (a === 'close') { closeSh(); } else if (a === 'reset') { fsReset(); } else { openSh(a, t); }
			return;
		}
		if ((a = t.getAttribute('data-tt'))) {
			if (a === 'go') { travelGo(); } else if (a === 'clear') { clearIso(); closeSh(); } else if (a === 'me') { locate(false); }
			return;
		}
		if ((a = t.getAttribute('data-al'))) { if (a === 'close') { closeAlert(); } else { openAlert(a === 'open' ? null : a, t); } return; }
		if ((a = t.getAttribute('data-save'))) { toggleSave(a); return; }
		if ((a = t.getAttribute('data-unsave'))) {
			S.saved = S.saved.filter(function (k) { return k !== a; }); saveSaved();
			if (S.byKey[a]) { syncItems(S.byKey[a], false); }
			if (S.card && S.card.key === a) { var sb = el.card.querySelector('[data-save]'); if (sb) { sb.outerHTML = saveBtn(S.card); } }
			renderList(); renderSaved(); markActive();
			var nx = el.saved && el.saved.querySelector('[data-unsave]'); if (nx) { try { nx.focus({ preventScroll: true }); } catch (e) { nx.focus(); } }
			ev('save', { on: 0, from: 'list' }); return;
		}
		if (t.getAttribute('data-saved') === 'go') { if (el.saved) { el.saved.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' }); var sh = $('nlnf-saved-h'); if (sh) { try { sh.focus({ preventScroll: true }); } catch (e) { /* focus */ } } } return; }
		if ((a = t.getAttribute('data-tab'))) {
			if (a === S.tab) { return; }
			S.tab = a; S.group = null; S.bounds = null; S.shown = 30; LAST.fit = !S.origin && !S.zone && !S.iso; // v3: the sale and the rent price ranges are kept apart
			closeCard(); drop(); renderAll(); ev('tab', { tab: a }); return;
		}
		if ((a = t.getAttribute('data-f'))) { if (t.tagName === 'BUTTON') { S.f[a] = !S.f[a]; S.shown = 30; renderAll(); ev('filter', { name: a }); } return; }
		if ((a = t.getAttribute('data-slot'))) { startPick(a); return; }
		if ((a = t.getAttribute('data-unslot'))) { if (S.iso && S.iso.fromK === a) { S.iso = null; drawIso(); } delete S.anchors[a]; saveAnchors(); renderAll(); drawAnchors(); return; }
		if ((a = t.getAttribute('data-key'))) { var x = S.byKey[a]; if (x) { openCard(x, t); } return; }
		if ((a = t.getAttribute('data-scope'))) {
			if (a === 'zone') { clearZone(); return; }
			if (a === 'iso') { clearIso(); return; }
			if (a === 'bounds') { S.bounds = null; } else { S.group = null; }
			S.shown = 30; renderList(); markActive(); return;
		}
		if ((a = t.getAttribute('data-few'))) {
			if (a === 'new') { S.tab = 'new'; S.group = null; S.bounds = null; S.shown = 30; LAST.fit = !S.origin && !S.zone && !S.iso; closeCard(); drop(); renderAll(); ev('few', { go: 'new' }); }
			return;
		}
		if ((a = t.getAttribute('data-empty'))) { // widen: the area scopes, the drawn zone, the travel time and every filter go
			S.bounds = null; S.group = null; S.f = fBlank(); S.fp = { sale: { min: 0, max: 0 }, rent: { min: 0, max: 0 } };
			S.zone = null; S.iso = null; drawZone(); drawIso(); drawLabel();
			if (a === 'new' && !BROKER) { S.tab = 'new'; }
			LAST.fit = true; drop(); renderAll(); return;
		}
		if (t.getAttribute('data-close')) { closeCard(); return; }
		if ((a = t.getAttribute('data-visit'))) {
			if (a === 'clear') { S.visit = []; saveVisit(); renderVisit(); return; }
			if (!S.card) { return; }
			var i = S.visit.indexOf(S.card.key);
			if (a === 'add' && i < 0) {
				if (S.visit.length >= 6) { say('ביום הביקורים יש כבר 6 מקומות. הסירו אחד כדי להוסיף.'); return; }
				S.visit.push(S.card.key); ev('visit_add', { type: S.card.t === 'l' ? 'listing' : 'project' });
			} else if (a === 'remove' && i > -1) { S.visit.splice(i, 1); }
			saveVisit(); renderVisit(); openCard(S.card, S.opener); return;
		}
		if ((a = t.getAttribute('data-unvisit'))) { S.visit = S.visit.filter(function (k) { return k !== a; }); saveVisit(); renderVisit(); return; }
		if (t.getAttribute('data-waze')) { ev('waze'); return; }
		if (t.getAttribute('data-go')) { ev('go', { type: S.card && S.card.t === 'p' ? 'project' : 'listing' }); return; }
	});
	root.addEventListener('change', function (e) {
		var s = e.target;
		if (s && s.getAttribute && s.getAttribute('data-al') === 'r') { AL.r = +s.value || 1.5; drawAlertArea(true); return; }
		if (s && s.getAttribute && s.getAttribute('data-ff')) { ffChange(s); return; } // v3: the full filters, applied at once
		if (s && s.name === 'ttfrom') { TT.from = s.value; ttErr(''); return; }
		if (s && s.name === 'ttmode') { TT.mode = s.value; return; }
		if (s && s.name === 'ttmin') { TT.min = +s.value || 20; return; }
		var k = s && s.getAttribute('data-f');
		if (!k || s.tagName !== 'SELECT') { return; }
		if (k === 'pmax') { S.fp[S.tab].max = +s.value || 0; } else { S.f[k] = +s.value || 0; }
		S.shown = 30; renderAll(); ev('filter', { name: k });
	});
	root.addEventListener('submit', function (e) { if (e.target && e.target.id === 'nlnf-al-f') { e.preventDefault(); sendAlert(e.target); } });
	root.addEventListener('keydown', function (e) {
		var t = e.target;
		if (t && t.getAttribute && t.getAttribute('role') === 'tab' && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) {
			var tabs = [].slice.call(root.querySelectorAll('[role=tab]')), i = tabs.indexOf(t);
			var n = tabs[(i + (e.key === 'ArrowLeft' ? 1 : -1) + tabs.length) % tabs.length]; // RTL: left is the next tab
			n.focus(); n.click(); e.preventDefault();
		}
	});
	function escape() { // one step back per Escape: a side sheet, the alert sheet, the drawing, the measuring, the picking, the card; false when nothing was open
		if (closeSh()) { return true; }
		if (closeAlert()) { return true; }
		if (root.classList.contains('is-draw')) { drawOff(); return true; }
		if (S.measure) { measureOff(); return true; }
		if (S.picking) { endPick(); return true; }
		return closeCard();
	}
	root.addEventListener('keydown', function (e) { if (e.key === 'Escape' && escape()) { e.stopPropagation(); } });
	el.more.addEventListener('click', function () { S.shown += 30; renderList(); ev('more'); });
	el.area.addEventListener('click', function () {
		if (!S.map) { return; }
		var b = S.map.getBounds();
		S.bounds = { w: b.getWest(), s: b.getSouth(), e: b.getEast(), n: b.getNorth() };
		S.group = null; S.shown = 30; el.area.hidden = true; userMoved = false;
		renderList(); markActive(); ev('area');
	});
	function resize() { updateSheet(); if (S.map) { try { S.map.resize(); } catch (e) { /* hidden */ } setTimeout(sync, 80); } }
	window.addEventListener('resize', resize);

	/* ------------------------------------------------------------ start */
	var started = false, dataP = null;
	function data() {
		if (dataP) { return dataP; }
		dataP = fetch(D.api, { credentials: 'omit', headers: { Accept: 'application/json' } })
			.then(function (r) { if (!r.ok) { throw new Error('http ' + r.status); } return r.json(); })
			.then(function (d) { if (!d || !d.ok) { throw new Error('data'); } return d; });
		dataP.catch(function () { dataP = null; });
		return dataP;
	}
	function start() {
		if (started) { return; }
		started = true;
		ev('view');
		renderTabs(); renderChips(); renderPlaces(); renderLegend();
		el.count.textContent = 'הדירות נטענות…';
		startMap();
		data().then(function (d) {
			prep(d);
			if (D.city) {
				var c = norm(D.city), hit = S.places.filter(function (p) { return norm(p.name) === c; })[0] || S.places.filter(function (p) { return norm(p.name).indexOf(c) > -1 || c.indexOf(norm(p.name)) > -1; })[0];
				if (hit) { el.q.value = hit.name; S.origin = { kind: 'place', pkind: hit.kind, label: hit.name, lat: hit.lat, lng: hit.lng, zoom: hit.kind === 'hood' ? 14 : 12 }; }
			}
			LAST.fit = true; drop();
			renderAll();
			drawMe();
		}).catch(function () { el.count.textContent = ''; say('הרשימה לא נטענה כרגע. רעננו את העמוד ונסו שוב.'); });
	}
	var held = !!root.closest('.nlnf-hold'); // 6.11.2026: printed in the footer's hidden holder, it waits for its place in the page's own section
	var inline = !held && !root.closest('.nlnf-dlg');
	if (inline) {
		if ('IntersectionObserver' in window) {
			var io = new IntersectionObserver(function (es) { if (es.some(function (x) { return x.isIntersecting; })) { io.disconnect(); start(); } }, { rootMargin: '600px 0px' });
			io.observe(root);
		} else { start(); }
	}

	/* ------------------------------------------------------------ in place (owner 6.11.2026: no floating button on any page, ever)
	   The page's own map or listings section (data-host on #nlnf-lidi) gets a quiet two-way switch; the map opens there, in the
	   same place, and only then loads Mapbox and the data. The switch's height is held by finder.css from the first paint, so
	   nothing on the page moves when it arrives. "מסך מלא" inside the app opens the full-screen dialog (drawing a zone on a phone
	   needs it too); Back or Escape returns the app to its place. #lidi chooses the map in place and scrolls to it. */
	var wrap = document.getElementById('nlnf-lidi');
	if (!wrap) { return; }
	var dlg = document.getElementById('nlnf-dlg'), body = document.getElementById('nlnf-dlg-body'), xBtn = document.getElementById('nlnf-dlg-x');
	var isOpen = false, lastFocus = null, home = null, askedLoc = false, SW = null, touched = false;

	function plan(h) { // where the switch and the app go in this host; null = not a known section (then nothing shows)
		if (!h) { return null; }
		if (h.id === 'nldrone') { // the home page's projects map: the switch above its stage, the app in the stage's place
			var st = h.querySelector('.nldrone-stage');
			if (!st) { return null; }
			return { kind: 'proj', near: true, res: h, ctl: st.id || '', t: ['פרויקטים חדשים', 'דירות לידי'], aria: 'מה מוצג על המפה',
				put: function (row) { h.insertBefore(row, st); }, box: function (b) { st.parentNode.insertBefore(b, st.nextSibling); },
				hide: function () { return [st]; } };
		}
		var grid = h.querySelector('.nlb-grid'), hd = h.querySelector('.nlb-listings-head');
		if (grid && hd) { // a broker's own site, section "הנכסים": the switch under its heading, the app in the grid's place (her listings only)
			return { kind: 'nlb', near: false, res: hd, ctl: '', t: ['רשימה', 'על המפה'], aria: 'איך להציג את הנכסים',
				put: function (row) { hd.appendChild(row); }, box: function (b) { grid.parentNode.insertBefore(b, grid.nextSibling); },
				hide: function () { return [grid].concat([].slice.call(h.querySelectorAll('.nlb-filters'))); } };
		}
		var n = h.nextElementSibling; // the rent page: h2#listings, its paragraph, then the listing block .nlrh-list
		while (n && !n.classList.contains('nlrh-list') && !/^H[1-3]$/.test(n.tagName)) { n = n.nextElementSibling; }
		if (n && n.classList.contains('nlrh-list')) {
			var L = n;
			return { kind: 'list', near: !BROKER, res: L, ctl: '', t: ['רשימה', BROKER ? 'על המפה' : 'על המפה, לידי'], aria: 'איך להציג את הדירות',
				put: function (row) { L.insertBefore(row, L.firstChild); }, box: function (b) { L.appendChild(b); },
				hide: function () { return [].filter.call(L.children, function (c) { return c !== SW.row && c !== SW.box; }); } };
		}
		return null;
	}
	function mountSwitch(P) {
		var row = document.createElement('div');
		row.className = 'nlnf nlnf-sw nlnf-sw--' + P.kind;
		row.setAttribute('dir', 'rtl'); row.setAttribute('lang', 'he');
		row.innerHTML = '<div class="nlnf-sw__in" role="group" aria-label="' + esc(P.aria) + '">'
			+ '<button type="button" class="nlnf-sw__b" data-v="list" aria-pressed="true"' + (P.ctl ? ' aria-controls="' + esc(P.ctl) + '"' : '') + '>' + esc(P.t[0]) + '</button>'
			+ '<button type="button" class="nlnf-sw__b" data-v="map" aria-pressed="false" aria-controls="nlnf-app">' + esc(P.t[1]) + '</button></div>';
		P.put(row);
		P.res.classList.add('nlnf-ready'); // the height finder.css held for the switch is now the switch itself
		SW = { P: P, row: row, btns: row.querySelectorAll('.nlnf-sw__b'), box: null, on: false };
		row.addEventListener('click', function (e) {
			var b = e.target.closest('.nlnf-sw__b');
			if (b) { choose(b.getAttribute('data-v'), 'switch'); }
		});
		row.addEventListener('keydown', function (e) { // RTL: the arrows move between the two, like the site's other tabs
			if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') { return; }
			var b = e.target.closest('.nlnf-sw__b'); if (!b) { return; }
			var o = SW.btns[0] === b ? SW.btns[1] : SW.btns[0];
			o.focus(); choose(o.getAttribute('data-v'), 'switch'); e.preventDefault();
		});
		var mb = SW.btns[1]; // the list is ready the moment the map is chosen (the data only, never Mapbox before the choice)
		['pointerenter', 'focus', 'touchstart'].forEach(function (k) { mb.addEventListener(k, function () { data().catch(function () {}); }, { passive: true, once: true }); });
	}
	function choose(v, from) {
		if (!SW) { return; }
		var map = v === 'map';
		if (map === SW.on) { return; }
		SW.on = map;
		if (map && !SW.box) {
			var box = document.createElement('div');
			box.className = 'nlnf nlnf--host nlnf--host-' + SW.P.kind;
			box.setAttribute('dir', 'rtl'); box.setAttribute('lang', 'he');
			SW.box = box;
			SW.P.box(box);
			box.appendChild(root);
		}
		[].forEach.call(SW.btns, function (b) { b.setAttribute('aria-pressed', (b.getAttribute('data-v') === 'map') === map ? 'true' : 'false'); });
		SW.P.hide().forEach(function (x) { x.classList.toggle('nlnf-off', map); });
		if (SW.box) { SW.box.classList.toggle('nlnf-off', !map); }
		SW.P.res.classList.toggle('nlnf-map', map);
		if (map) {
			var was = started;
			start(); drop();
			if (was) { renderAll(); }
			setTimeout(resize, 30); setTimeout(resize, 320);
			if (!was && SW.P.near && !S.origin && !askedLoc) { askedLoc = true; locate(true); } // "לידי": the visitor asked for near
			ev('open', { from: from || 'switch' });
		} else {
			closeSh(); closeAlert(); closeCard(); measureOff(); endPick(); drawOff();
			try { window.dispatchEvent(new Event('resize')); } catch (e) { /* old browser: the projects map keeps its size */ }
			ev('list', { from: from || 'switch' });
		}
	}

	if (held) {
		var hostSel = wrap.getAttribute('data-host') || '', hostEl = null;
		try { hostEl = hostSel ? document.querySelector(hostSel) : null; } catch (e) { hostEl = null; }
		var P = plan(hostEl);
		if (!P) { document.documentElement.classList.add('nlnf-nohost'); return; } // no section to hold it: nothing new on the page, the held height goes
		mountSwitch(P);
	}

	function open(fromPop, from) { // full screen: the same app, moved into the dialog and back
		if (isOpen || !dlg || !body) { return; }
		isOpen = true; lastFocus = document.activeElement;
		home = document.createComment('nlnf-home'); root.parentNode.insertBefore(home, root);
		body.appendChild(root);
		dlg.hidden = false;
		document.documentElement.classList.add('nlnf-open');
		document.body.style.overflow = 'hidden';
		updateSheet(); // v3: on a phone the list becomes the sheet over the map
		if (!fromPop) { try { history.pushState({ nlnf: 1 }, '', '#lidi'); } catch (e) { /* old browser */ } }
		var was = started;
		start();
		drop();
		if (was) { renderAll(); }
		setTimeout(resize, 30); setTimeout(resize, 320);
		if (!S.origin && !askedLoc) { askedLoc = true; locate(true); } else if (S.origin && S.map) { setTimeout(function () { burst(S.origin.lat, S.origin.lng); }, 300); }
		if (!S.origin && S.map) { setTimeout(function () { burst(null, null); }, 300); }
		try { dlg.focus({ preventScroll: true }); } catch (e) { /* focus */ } // the dialog itself (tabindex -1); Tab reaches the close button first
		ev('open', { from: from || 'fullscreen' });
	}
	function close(fromPop) {
		if (!isOpen) { return; }
		isOpen = false;
		closeSh(); closeAlert(); closeCard(); measureOff(); endPick(); drawOff();
		dlg.hidden = true;
		document.documentElement.classList.remove('nlnf-open');
		document.body.style.overflow = '';
		if (home && home.parentNode) { home.parentNode.insertBefore(root, home); home.parentNode.removeChild(home); }
		home = null;
		updateSheet(); // v3: back on the page, the list is a plain list again
		setTimeout(resize, 30);
		if (fromPop !== true && history.state && history.state.nlnf) { try { history.back(); } catch (e) { /* stays */ } }
		if (lastFocus && lastFocus.focus) { try { lastFocus.focus({ preventScroll: true }); } catch (e) { /* gone */ } }
	}
	if (dlg && body) {
		DLG.can = true; DLG.isOpen = function () { return isOpen; }; DLG.open = function () { open(false, 'draw'); }; // v3: "ציירו אזור" on a phone opens the full screen first
		root.classList.remove('nlnf--nodraw');
		el.fs.hidden = false;
		el.fs.addEventListener('click', function () { open(false, 'fullscreen'); });
		if (xBtn) { xBtn.addEventListener('click', function () { close(); }); }
		dlg.addEventListener('keydown', function (e) {
			if (e.key === 'Escape') { if (!escape()) { close(); } e.preventDefault(); return; }
			if (e.key !== 'Tab') { return; }
			var f = [].filter.call(dlg.querySelectorAll('a[href],button:not([disabled]),input,select,[tabindex]:not([tabindex="-1"])'), function (n) { return n.offsetParent !== null || n === document.activeElement; });
			if (!f.length) { return; }
			var a = f[0], z = f[f.length - 1];
			if (e.shiftKey && document.activeElement === a) { z.focus(); e.preventDefault(); } else if (!e.shiftKey && document.activeElement === z) { a.focus(); e.preventDefault(); }
		});
		window.addEventListener('popstate', function () {
			var want = !!(history.state && history.state.nlnf); // our own full-screen entry, never a bare #lidi
			if (isOpen && !want) { close(true); } else if (!isOpen && want && (inline || (SW && SW.on))) { open(true, 'fullscreen'); }
		});
		window.addEventListener('pagehide', function () { document.body.style.overflow = ''; document.documentElement.classList.remove('nlnf-open'); });
	}

	/* #lidi: the map in place, scrolled to (no dialog on load), below the site's sticky header (measured, never assumed);
	   again on window load unless the visitor already moved */
	function topCover() {
		var max = 0;
		try {
			[].forEach.call(document.elementsFromPoint(window.innerWidth / 2, 2) || [], function (n) {
				for (var e = n; e && e !== document.body && e !== document.documentElement; e = e.parentElement) {
					var p = window.getComputedStyle(e).position;
					if (p === 'fixed' || p === 'sticky') { var r = e.getBoundingClientRect(); if (r.top <= 2 && r.bottom > max && r.bottom < window.innerHeight / 2) { max = r.bottom; } break; }
				}
			});
		} catch (e) { /* old browser: no offset */ }
		return max;
	}
	function scrollToEl(t) { window.scrollTo(0, Math.max(0, Math.round(t.getBoundingClientRect().top + window.pageYOffset - topCover() - 12))); }
	function lidi(from) {
		var target = SW ? SW.row : (inline ? document.getElementById('nlnf') || root : null);
		if (!target) { return; }
		scrollToEl(target); // first, so the section's own map (the projects map on the home page) starts before the finder's
		if (SW) { choose('map', from); } else if (inline) { start(); ev('open', { from: from }); }
	}
	['wheel', 'touchstart', 'keydown', 'pointerdown'].forEach(function (k) { window.addEventListener(k, function () { touched = true; }, { passive: true, once: true }); });
	window.addEventListener('hashchange', function () { if (location.hash === '#lidi' && !isOpen && !(history.state && history.state.nlnf)) { lidi('link'); } });
	if (location.hash === '#lidi') {
		lidi('link');
		window.addEventListener('load', function () { // pictures above may have changed the page's height meanwhile
			if (touched) { return; }
			var t = SW ? SW.row : document.getElementById('nlnf');
			if (t) { scrollToEl(t); }
		});
	}
})();
