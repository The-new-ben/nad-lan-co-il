<?php
/**
 * Showroom support - the living remains of project-3d.php (retired v1.70.1).
 *
 * The OLD showroom renderer is gone (the new showroom-engine renders every
 * project). What survives here is everything the NEW engine and the authoring
 * flow still depend on:
 *  1. the script_loader_tag filter that loads model-viewer as an ES module;
 *  2. register_post_meta for all project_3d_* showroom fields (REST exposure
 *     engine.js relies on) with their sanitizers;
 *  3. the admin metabox - the only authoring UI for units/facade/environment/
 *     price meta - and its save handler;
 *  4. the /nadlan/v1/project-showroom/<id> payload API (agent tooling).
 * Also: no-op tombstones for shortcodes whose providers were deleted
 * (orchestrator plugin, legacy homepage module) so no raw shortcode text can
 * ever leak into a rendered page from stale templates or content.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/* Tombstones: providers deleted in the v1.70.1 kill list. */
add_action( 'init', function () {
	foreach ( array( 'nadlan_platform_home_projects', 'nadlan_platform_project_catalog', 'nadlan_platform_showroom', 'nadlan_platform_interior', 'nadlan_home_sections', 'nadlan_hero_search' ) as $dead ) {
		if ( ! shortcode_exists( $dead ) ) {
			add_shortcode( $dead, '__return_empty_string' );
		}
	}
}, 20 );

if ( ! function_exists( 'nadlan_p3d_enabled' ) ) {
	function nadlan_p3d_enabled() {
		return (bool) apply_filters( 'nadlan_p3d_enabled', get_option( 'nadlan_feature_project_3d', '0' ) === '1' );
	}
}

if ( ! function_exists( 'nadlan_p3d_status_label' ) ) {
	function nadlan_p3d_status_label( $status ) {
		$labels = array(
			'available' => 'זמינה לפנייה',
			'reserved'  => 'בתהליך בדיקה',
			'sold'      => 'לא זמינה',
			'unknown'   => 'סטטוס לבירור מול היזם',
		);
		return $labels[ $status ] ?? $labels['unknown'];
	}
}

if ( ! function_exists( 'nadlan_p3d_sanitize_decimal' ) ) {
	function nadlan_p3d_sanitize_decimal( $value ) {
		return is_numeric( $value ) ? (float) $value : 0.0;
	}
}

if ( ! function_exists( 'nadlan_p3d_clean_material_items' ) ) {
	function nadlan_p3d_clean_material_items( $items ) {
		if ( ! is_array( $items ) ) {
			return array();
		}

		if ( isset( $items['items'] ) && is_array( $items['items'] ) ) {
			$items = $items['items'];
		}

		if ( isset( $items['layers'] ) && is_array( $items['layers'] ) ) {
			$flat = array();
			foreach ( $items['layers'] as $layer ) {
				if ( ! is_array( $layer ) || empty( $layer['items'] ) || ! is_array( $layer['items'] ) ) {
					continue;
				}
				$layer_id    = isset( $layer['id'] ) ? sanitize_key( (string) $layer['id'] ) : '';
				$layer_label = isset( $layer['label'] ) ? sanitize_text_field( (string) $layer['label'] ) : '';
				foreach ( $layer['items'] as $item ) {
					if ( ! is_array( $item ) ) {
						continue;
					}
					if ( ! isset( $item['label'] ) && isset( $item['name'] ) ) {
						$item['label'] = $item['name'];
					}
					if ( ! isset( $item['url'] ) && isset( $item['source_url'] ) ) {
						$item['url'] = $item['source_url'];
					}
					if ( ! isset( $item['source'] ) ) {
						$item['source'] = $item['source_note'] ?? ( $item['notes'] ?? '' );
					}
					if ( ! isset( $item['type'] ) && $layer_id !== '' ) {
						$item['type'] = $layer_id;
					}
					if ( ! isset( $item['category'] ) && $layer_id !== '' ) {
						$item['category'] = $layer_id;
					}
					if ( ! isset( $item['detail'] ) ) {
						$detail_bits = array_filter(
							array(
								$layer_label,
								$item['status'] ?? '',
								$item['distance'] ?? '',
							)
						);
						$item['detail'] = implode( ' · ', $detail_bits );
					}
					$flat[] = $item;
				}
			}
			$items = $flat;
		}

		$out = array();
		foreach ( $items as $item ) {
			if ( ! is_array( $item ) ) {
				continue;
			}

			$clean = array();
			foreach ( array( 'label', 'name', 'title' ) as $key ) {
				if ( isset( $item[ $key ] ) ) {
					$clean[ $key ] = sanitize_text_field( (string) $item[ $key ] );
				}
			}
			foreach ( array( 'detail', 'source', 'note' ) as $key ) {
				if ( isset( $item[ $key ] ) ) {
					$clean[ $key ] = sanitize_textarea_field( (string) $item[ $key ] );
				}
			}
			if ( isset( $item['type'] ) ) {
				$clean['type'] = sanitize_key( (string) $item['type'] );
			}
			if ( isset( $item['category'] ) ) {
				$clean['category'] = sanitize_key( (string) $item['category'] );
			}
			if ( isset( $item['url'] ) ) {
				$clean['url'] = esc_url_raw( (string) $item['url'] );
			}
			if ( isset( $item['distance'] ) ) {
				$clean['distance'] = sanitize_text_field( (string) $item['distance'] );
			}
			if ( isset( $item['lat'] ) && is_numeric( $item['lat'] ) ) {
				$clean['lat'] = (float) $item['lat'];
			}
			if ( isset( $item['lng'] ) && is_numeric( $item['lng'] ) ) {
				$clean['lng'] = (float) $item['lng'];
			}

			if ( array_filter( $clean ) ) {
				$out[] = $clean;
			}
			if ( count( $out ) >= 40 ) {
				break;
			}
		}

		return $out;
	}
}

if ( ! function_exists( 'nadlan_p3d_sanitize_material_json' ) ) {
	function nadlan_p3d_sanitize_material_json( $raw ) {
		$raw = trim( (string) $raw );
		if ( $raw === '' ) {
			return '';
		}
		$decoded = json_decode( $raw, true );
		if ( ! is_array( $decoded ) ) {
			return '';
		}
		$clean = nadlan_p3d_clean_material_items( $decoded );
		return $clean ? wp_json_encode( $clean, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) : '';
	}
}

if ( ! function_exists( 'nadlan_p3d_clean_facade_images' ) ) {
	function nadlan_p3d_clean_facade_images( $items ) {
		if ( ! is_array( $items ) ) {
			return array();
		}

		$out = array();
		foreach ( $items as $item ) {
			if ( ! is_array( $item ) ) {
				continue;
			}
			$src = esc_url_raw( (string) ( $item['src'] ?? $item['url'] ?? '' ) );
			if ( $src === '' ) {
				continue;
			}
			$facade = array(
				'building' => sanitize_text_field( (string) ( $item['building'] ?? $item['label'] ?? '' ) ),
				'label'    => sanitize_text_field( (string) ( $item['label'] ?? $item['building'] ?? '' ) ),
				'src'      => $src,
				'viewbox'  => preg_replace( '/[^0-9,. \-]/', '', (string) ( $item['viewbox'] ?? '0 0 1000 1000' ) ),
			);
			foreach ( array( 'alt', 'source', 'notice', 'kind' ) as $text_key ) {
				if ( isset( $item[ $text_key ] ) ) {
					$facade[ $text_key ] = sanitize_text_field( (string) $item[ $text_key ] );
				}
			}
			if ( isset( $item['concept'] ) ) {
				$facade['concept'] = ! empty( $item['concept'] ) && $item['concept'] !== '0' && $item['concept'] !== 'false';
			}
			if ( isset( $item['approved'] ) ) {
				$facade['approved'] = ! empty( $item['approved'] ) && $item['approved'] !== '0' && $item['approved'] !== 'false';
			}
			$out[] = $facade;
			if ( count( $out ) >= 12 ) {
				break;
			}
		}

		return $out;
	}
}

if ( ! function_exists( 'nadlan_p3d_matches_dimri_yama' ) ) {
	function nadlan_p3d_matches_dimri_yama( $title, $developer = '', $city = '', $address = '' ) {
		$haystack = trim( implode( ' ', array( (string) $title, (string) $developer, (string) $city, (string) $address ) ) );
		$haystack = function_exists( 'mb_strtolower' ) ? mb_strtolower( $haystack ) : strtolower( $haystack );
		if ( $haystack === '' ) {
			return false;
		}
		$has_dimri = false !== strpos( $haystack, 'dimri' ) || false !== strpos( $haystack, 'דמרי' );
		$has_yama  = false !== strpos( $haystack, 'yama' ) || false !== strpos( $haystack, 'ימה' ) || false !== strpos( $haystack, 'sde dov' ) || false !== strpos( $haystack, 'שדה דב' );
		return $has_dimri && $has_yama;
	}
}

if ( ! function_exists( 'nadlan_p3d_dimri_yama_concept_facade_images' ) ) {
	function nadlan_p3d_dimri_yama_concept_facade_images() {
		return array(
			array(
				'building' => 'DIMRI YAMA',
				'label'    => 'חזית קונספט פרימיום · להמחשה בלבד',
				'alt'      => 'הדמיית קונספט מקורית של חזית דמרי ימה לבחירת דירות - לא חומר רשמי של היזם',
				'src'      => esc_url_raw( plugins_url( '../assets/projects/dimri-yama/dimri-yama-premium-facade-concept.jpg', __FILE__ ) ),
				'viewbox'  => '0 0 1200 900',
				'kind'     => 'generated-concept',
				'concept'  => true,
				'approved' => false,
				'notice'   => 'הדמיית קונספט מקורית עד לקבלת חזית רשמית מהיזם',
				'source'   => 'Original generated asset packaged in nadlan-config 1.68.2; replace with official developer elevation when available.',
			),
		);
	}
}

if ( ! function_exists( 'nadlan_p3d_clean_site_plan_polygons' ) ) {
	function nadlan_p3d_clean_site_plan_polygons( $items ) {
		if ( ! is_array( $items ) ) {
			return array();
		}

		$out = array();
		foreach ( $items as $item ) {
			if ( ! is_array( $item ) ) {
				continue;
			}
			$points = preg_replace( '/[^0-9,. \-]/', '', (string) ( $item['points'] ?? '' ) );
			if ( $points === '' ) {
				continue;
			}
			$out[] = array(
				'building' => sanitize_text_field( (string) ( $item['building'] ?? $item['label'] ?? '' ) ),
				'label'    => sanitize_text_field( (string) ( $item['label'] ?? $item['building'] ?? '' ) ),
				'points'   => $points,
			);
			if ( count( $out ) >= 30 ) {
				break;
			}
		}

		return $out;
	}
}

if ( ! function_exists( 'nadlan_p3d_clean_unit_items' ) ) {
	function nadlan_p3d_clean_unit_items( $units ) {
		if ( ! is_array( $units ) || ! $units ) {
			return array();
		}

		$out = array();
		foreach ( $units as $u ) {
			if ( ! is_array( $u ) || empty( $u['id'] ) ) {
				continue;
			}

			/* Audit 2026-08-10 (fail-open coercion): missing or unrecognized
			 * status must NEVER become "available" - that fabricates
			 * inventory certainty. Unknown stays unknown, data and screen. */
			$status = sanitize_key( (string) ( $u['status'] ?? 'unknown' ) );
			if ( ! in_array( $status, array( 'available', 'reserved', 'sold', 'unknown' ), true ) ) {
				$status = 'unknown';
			}
			$price_note = sanitize_textarea_field( (string) ( $u['price_note'] ?? '' ) );

			$out[] = array(
				'id'      => sanitize_key( (string) $u['id'] ),
				'title'   => sanitize_text_field( (string) ( $u['title'] ?? '' ) ),
				'points'  => preg_replace( '/[^0-9,. \-]/', '', (string) ( $u['points'] ?? '' ) ),
				'stage_x' => ( isset( $u['stage_x'] ) && $u['stage_x'] !== '' ) ? max( 0, min( 100, (float) $u['stage_x'] ) ) : '',
				'stage_y' => ( isset( $u['stage_y'] ) && $u['stage_y'] !== '' ) ? max( 0, min( 100, (float) $u['stage_y'] ) ) : '',
				'stage_w' => ( isset( $u['stage_w'] ) && $u['stage_w'] !== '' ) ? max( 0, min( 100, (float) $u['stage_w'] ) ) : '',
				'stage_h' => ( isset( $u['stage_h'] ) && $u['stage_h'] !== '' ) ? max( 0, min( 100, (float) $u['stage_h'] ) ) : '',
				'floor'   => max( 0, (int) ( $u['floor'] ?? 0 ) ),
				'rooms'   => nadlan_p3d_sanitize_decimal( $u['rooms'] ?? 0 ),
				'sqm'     => nadlan_p3d_sanitize_decimal( $u['sqm'] ?? 0 ),
				'balcony' => nadlan_p3d_sanitize_decimal( $u['balcony'] ?? 0 ),
				'label'   => sanitize_text_field( (string) ( $u['label'] ?? '' ) ),
				'dir'     => sanitize_text_field( (string) ( $u['dir'] ?? '' ) ),
				'line'    => sanitize_text_field( (string) ( $u['line'] ?? '' ) ),
				'view'    => sanitize_text_field( (string) ( $u['view'] ?? '' ) ),
				'hotspot_position' => nadlan_p3d_hotspot_vector( $u['hotspot_position'] ?? ( $u['model_position'] ?? '' ) ),
				'hotspot_normal'   => nadlan_p3d_hotspot_vector( $u['hotspot_normal'] ?? ( $u['model_normal'] ?? '' ) ),
				'camera_orbit'     => sanitize_text_field( (string) ( $u['camera_orbit'] ?? '' ) ),
				'building'      => sanitize_text_field( (string) ( $u['building'] ?? '' ) ),
				'availability'  => sanitize_text_field( (string) ( $u['availability'] ?? '' ) ),
				'note'          => sanitize_textarea_field( (string) ( $u['note'] ?? '' ) ),
				'market_note'   => sanitize_textarea_field( (string) ( $u['market_note'] ?? $price_note ) ),
				'source_note'   => sanitize_textarea_field( (string) ( $u['source_note'] ?? '' ) ),
				'price'          => nadlan_p3d_sanitize_decimal( $u['price'] ?? 0 ),
				'price_estimate' => nadlan_p3d_sanitize_decimal( $u['price_estimate'] ?? 0 ),
				'price_source'   => sanitize_text_field( (string) ( $u['price_source'] ?? $price_note ) ),
				'price_note'     => $price_note,
				'interior_url'    => esc_url_raw( (string) ( $u['interior_url'] ?? '' ) ),
				'tour_url'        => esc_url_raw( (string) ( $u['tour_url'] ?? '' ) ),
				'view_note'       => sanitize_textarea_field( (string) ( $u['view_note'] ?? '' ) ),
				'recommended'     => ! empty( $u['recommended'] ) || ! empty( $u['is_recommended'] ),
				'status'  => $status,
				'plan'    => esc_url_raw( (string) ( $u['plan'] ?? '' ) ),
			);
		}

		return $out;
	}
}

if ( ! function_exists( 'nadlan_p3d_sanitize_units_json' ) ) {
	function nadlan_p3d_sanitize_units_json( $raw ) {
		$raw = trim( (string) wp_unslash( $raw ) );
		if ( $raw === '' ) {
			return '';
		}
		$decoded = json_decode( $raw, true );
		if ( ! is_array( $decoded ) ) {
			return '';
		}
		$clean = nadlan_p3d_clean_unit_items( $decoded );
		return $clean ? wp_json_encode( $clean, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) : '';
	}
}

if ( ! function_exists( 'nadlan_p3d_units' ) ) {
	function nadlan_p3d_units( $post_id ) {
		$raw   = trim( (string) get_post_meta( (int) $post_id, 'project_3d_units', true ) );
		$units = $raw !== '' ? json_decode( $raw, true ) : array();
		return nadlan_p3d_clean_unit_items( $units );
	}
}

if ( ! function_exists( 'nadlan_p3d_demo_units' ) ) {
	function nadlan_p3d_demo_units() {
		return array(
			array(
				'id'      => 'demo-12-a',
				'title'   => 'קו A',
				'floor'   => 12,
				'rooms'   => 4,
				'sqm'     => 105,
				'balcony' => 12,
				'dir'     => 'צפון מערב',
				'line'    => 'A',
				'view'    => 'ים ושדרה ירוקה',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'להמחשה, זמינות ומחיר לפי אישור יזם',
				'note'          => 'טיפוס דירה מערבי נמוך יחסית, מתאים להשוואת כיוון אוויר, מרפסת ונגישות למתחם הפנימי.',
				'market_note'   => 'אין מחיר רשמי במערכת. כאשר יוזן מקור מאושר, השדה יכול לשאת מחיר, עסקה אחרונה או טווח שיווק.',
				'source_note'   => 'הדגמה מקורית על בסיס נתוני פרויקט ציבוריים: מגדל גבוה, בנייני בוטיק, חצר פנימית וקרבה לים.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '408,578 486,578 486,594 408,594',
			),
			array(
				'id'      => 'demo-18-b',
				'title'   => 'קו B',
				'floor'   => 18,
				'rooms'   => 5,
				'sqm'     => 132,
				'balcony' => 16,
				'dir'     => 'מערב',
				'line'    => 'B',
				'view'    => 'חזית לים',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'להמחשה, נדרש אימות מלאי',
				'note'          => 'דירת חמישה חדרים בקו מערבי, מוצגת כטיפוס משפחתי עם מרפסת ונוף פתוח יותר מהקומות הנמוכות.',
				'market_note'   => 'מחיר לפי פנייה בלבד. ניתן לקשור כאן עסקאות מדלן או נתוני יזם לאחר הרשאה ואימות.',
				'source_note'   => 'הקומות והכיוונים הם הדגמה תכנונית, לא תכנית מכר.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '492,479 570,479 570,495 492,495',
			),
			array(
				'id'      => 'demo-24-c',
				'title'   => 'קו C',
				'floor'   => 24,
				'rooms'   => 4,
				'sqm'     => 118,
				'balcony' => 14,
				'dir'     => 'דרום מערב',
				'line'    => 'C',
				'view'    => 'קו החוף והמרינה',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'בתהליך בדיקה',
				'note'          => 'קו דרום מערבי להמחשה, מתאים לבדיקת נוף, חשיפה לשמש ומיקום ביחס לקו החוף.',
				'market_note'   => 'אפשר להציג כאן עסקה דומה, מחיר למ"ר או הערת זמינות כאשר מקור מאושר מוזן למערכת.',
				'source_note'   => 'הדגמה בלבד, ללא מחיר רשמי.',
				'price'   => 0,
				'status'  => 'reserved',
				'plan'    => '',
				'points'  => '576,380 654,380 654,396 576,396',
			),
			array(
				'id'      => 'demo-30-d',
				'title'   => 'קו D',
				'floor'   => 30,
				'rooms'   => 5,
				'sqm'     => 146,
				'balcony' => 20,
				'dir'     => 'מערב',
				'line'    => 'D',
				'view'    => 'ים פתוח וקו רקיע',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'זמינות לפי פנייה',
				'note'          => 'קומה גבוהה יותר, מיועדת להמחיש את שכבת הנוף ואת מעבר המשתמש מהחזית אל מבט מהדירה.',
				'market_note'   => 'שדה מחיר נשאר ריק עד קבלת מלאי מאומת.',
				'source_note'   => 'לא תכנית מכר ולא הבטחת זמינות.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '492,281 570,281 570,297 492,297',
			),
			array(
				'id'      => 'demo-34-e',
				'title'   => 'קו E',
				'floor'   => 34,
				'rooms'   => 5,
				'sqm'     => 158,
				'balcony' => 22,
				'dir'     => 'צפון מערב',
				'line'    => 'E',
				'view'    => 'ים, פארק ושדה דב',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'זמינות לפי פנייה',
				'note'          => 'קומה גבוהה בקו צפוני מערבי, להמחשת חיבור בין הים, הפארק והמתחם החדש.',
				'market_note'   => 'נתוני שוק יוצגו רק לאחר הזנת מקור מורשה.',
				'source_note'   => 'המחשה תכנונית לממשק בלבד.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '408,215 486,215 486,231 408,231',
			),
			array(
				'id'      => 'demo-38-p',
				'title'   => 'פנטהאוז הדגמה',
				'floor'   => 38,
				'rooms'   => 6,
				'sqm'     => 214,
				'balcony' => 44,
				'dir'     => 'מערב וצפון',
				'line'    => 'P',
				'view'    => 'קו ראשון לים',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'להמחשה בלבד',
				'note'          => 'קומת פרימיום להמחשת תרחיש רכישה מתקדם, בדיקת ליווי מקצועי ואיסוף עניין ממוקד.',
				'market_note'   => 'מחיר וזמינות אינם מוצגים ללא אישור מקור.',
				'source_note'   => 'לא מלאי רשמי.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '408,149 654,149 654,179 408,179',
			),
			array(
				'id'      => 'demo-07-g',
				'title'   => 'בניין בוטיק · קו G',
				'floor'   => 7,
				'rooms'   => 3,
				'sqm'     => 86,
				'balcony' => 10,
				'dir'     => 'מזרח',
				'line'    => 'G',
				'view'    => 'חצר פנימית ומרחבי המתחם',
				'building'      => 'בניין בוטיק',
				'availability'  => 'זמינות לפי פנייה',
				'note'          => 'דירת בוטיק נמוכה יותר להמחשת ששת המבנים המרקמיים והחצר הפנימית של המתחם.',
				'market_note'   => 'אפשר לשייך כאן מכירה דומה או טווח מחיר כאשר מקור מאומת זמין.',
				'source_note'   => 'הדגמה שמטרתה להראות שהפרויקט כולל גם בנייני בוטיק, לא רק מגדל.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '705,705 790,705 790,730 705,730',
			),
		);
	}
}

if ( ! function_exists( 'nadlan_p3d_json_meta' ) ) {
	function nadlan_p3d_json_meta( $post_id, $key, $fallback = array() ) {
		$raw = trim( (string) get_post_meta( (int) $post_id, (string) $key, true ) );
		if ( $raw === '' ) {
			return $fallback;
		}
		$decoded = json_decode( $raw, true );
		return is_array( $decoded ) ? $decoded : $fallback;
	}
}

if ( ! function_exists( 'nadlan_p3d_sanitize_model_type' ) ) {
	function nadlan_p3d_sanitize_model_type( $value ) {
		$value   = sanitize_key( (string) $value );
		$allowed = array( 'procedural', 'facade', 'sprite360', 'gltf', 'bim' );
		return in_array( $value, $allowed, true ) ? $value : 'procedural';
	}
}

if ( ! function_exists( 'nadlan_p3d_hotspot_vector' ) ) {
	function nadlan_p3d_hotspot_vector( $value ) {
		$value = trim( preg_replace( '/\s+/', ' ', (string) $value ) );
		if ( $value === '' ) {
			return '';
		}
		return preg_match( '/^-?\d+(?:\.\d+)?\s+-?\d+(?:\.\d+)?\s+-?\d+(?:\.\d+)?$/', $value ) ? $value : '';
	}
}

if ( ! function_exists( 'nadlan_p3d_sanitize_json_text' ) ) {
	function nadlan_p3d_sanitize_json_text( $value ) {
		$raw = trim( (string) wp_unslash( $value ) );
		if ( $raw === '' ) {
			return '';
		}
		$decoded = json_decode( $raw, true );
		return is_array( $decoded ) ? $raw : '';
	}
}

if ( ! function_exists( 'nadlan_p3d_sanitize_checkbox' ) ) {
	function nadlan_p3d_sanitize_checkbox( $value ) {
		return ! empty( $value ) && $value !== '0' && $value !== 'false' ? '1' : '0';
	}
}

if ( ! function_exists( 'nadlan_p3d_sanitize_camera_lock' ) ) {
	function nadlan_p3d_sanitize_camera_lock( $value ) {
		$value = sanitize_key( (string) $value );
		return in_array( $value, array( 'horizontal', 'free' ), true ) ? $value : 'horizontal';
	}
}

if ( ! function_exists( 'nadlan_p3d_sanitize_degree' ) ) {
	function nadlan_p3d_sanitize_degree( $value ) {
		$value = trim( (string) $value );
		if ( preg_match( '/^-?\d{1,3}(?:\.\d+)?deg$/', $value ) ) {
			return $value;
		}
		if ( is_numeric( $value ) ) {
			return max( -180, min( 180, (float) $value ) ) . 'deg';
		}
		return '';
	}
}

if ( ! function_exists( 'nadlan_p3d_degree_number' ) ) {
	function nadlan_p3d_degree_number( $value, $fallback ) {
		$value = nadlan_p3d_sanitize_degree( $value );
		if ( $value === '' ) {
			return (float) $fallback;
		}
		return (float) str_replace( 'deg', '', $value );
	}
}

if ( ! function_exists( 'nadlan_p3d_showroom_fields' ) ) {
	function nadlan_p3d_showroom_fields() {
		return array(
			'project_3d_image'              => 'esc_url_raw',
			'project_3d_viewbox'            => 'sanitize_text_field',
			'project_3d_floor_height_m'     => 'nadlan_p3d_sanitize_decimal',
			'project_3d_ground_elevation_m' => 'nadlan_p3d_sanitize_decimal',
			'project_3d_avg_price_per_sqm'  => 'nadlan_p3d_sanitize_decimal',
			'project_3d_price_source_note'  => 'sanitize_text_field',
			'project_3d_model_type'         => 'nadlan_p3d_sanitize_model_type',
			'project_model_glb'             => 'esc_url_raw',
			'project_model_usdz'            => 'esc_url_raw',
			'project_model_poster'          => 'esc_url_raw',
			'project_default_interior'      => 'esc_url_raw',
			'project_3d_camera_lock'        => 'nadlan_p3d_sanitize_camera_lock',
			'project_3d_camera_min_polar'   => 'nadlan_p3d_sanitize_degree',
			'project_3d_camera_max_polar'   => 'nadlan_p3d_sanitize_degree',
			'project_3d_camera_auto_rotate' => 'nadlan_p3d_sanitize_checkbox',
			'project_3d_camera_rotation_per_second' => 'nadlan_p3d_sanitize_degree',
			'project_3d_video_url'          => 'esc_url_raw',
			'project_3d_tour_url'           => 'esc_url_raw',
			'project_3d_cesium_tiles_url'   => 'esc_url_raw',
			'project_3d_drawings_json'      => 'nadlan_p3d_sanitize_material_json',
			'project_3d_environment_json'   => 'nadlan_p3d_sanitize_material_json',
			'project_3d_facade_images'      => 'nadlan_p3d_sanitize_json_text',
			'project_3d_site_plan_image'    => 'esc_url_raw',
			'project_3d_site_plan_polygons' => 'nadlan_p3d_sanitize_json_text',
			'project_3d_units'              => 'nadlan_p3d_sanitize_units_json',
			'project_3d_demo'               => 'nadlan_p3d_sanitize_checkbox',
		);
	}
}

add_action(
	'init',
	function () {
		$auth = function ( $allowed, $meta_key, $post_id ) {
			unset( $allowed, $meta_key );
			return current_user_can( 'edit_post', (int) $post_id );
		};

		foreach ( nadlan_p3d_showroom_fields() as $key => $sanitize_callback ) {
			register_post_meta(
				'nadlan_project',
				$key,
				array(
					'type'              => 'string',
					'single'            => true,
					'show_in_rest'      => true,
					'sanitize_callback' => $sanitize_callback,
					'auth_callback'     => $auth,
				)
			);
		}
	},
	12
);

if ( ! function_exists( 'nadlan_p3d_is_project' ) ) {
	function nadlan_p3d_is_project( $post_id ) {
		return (int) $post_id > 0 && get_post_type( (int) $post_id ) === 'nadlan_project';
	}
}

if ( ! function_exists( 'nadlan_p3d_prepare_rest_value' ) ) {
	function nadlan_p3d_prepare_rest_value( $key, $value ) {
		if ( is_array( $value ) && in_array( $key, array( 'project_3d_units', 'project_3d_drawings_json', 'project_3d_environment_json', 'project_3d_facade_images', 'project_3d_site_plan_polygons' ), true ) ) {
			$value = wp_json_encode( $value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
		}
		return $value;
	}
}

if ( ! function_exists( 'nadlan_p3d_export_showroom_payload' ) ) {
	function nadlan_p3d_export_showroom_payload( $post_id ) {
		$post_id = (int) $post_id;
		$meta    = array();
		foreach ( array_keys( nadlan_p3d_showroom_fields() ) as $key ) {
			$meta[ $key ] = get_post_meta( $post_id, $key, true );
		}

		return array(
			'id'          => $post_id,
			'slug'        => get_post_field( 'post_name', $post_id ),
			'title'       => get_the_title( $post_id ),
			'permalink'   => get_permalink( $post_id ),
			'meta'        => $meta,
			'units_count' => count( nadlan_p3d_units( $post_id ) ),
			'fields'      => array_keys( nadlan_p3d_showroom_fields() ),
		);
	}
}

if ( ! function_exists( 'nadlan_p3d_apply_showroom_payload' ) ) {
	function nadlan_p3d_apply_showroom_payload( $post_id, $payload ) {
		$post_id = (int) $post_id;
		if ( ! is_array( $payload ) ) {
			return new WP_Error( 'invalid_payload', 'Invalid showroom payload.', array( 'status' => 400 ) );
		}

		$input   = isset( $payload['meta'] ) && is_array( $payload['meta'] ) ? $payload['meta'] : $payload;
		$updated = array();

		foreach ( nadlan_p3d_showroom_fields() as $key => $sanitize_callback ) {
			if ( ! array_key_exists( $key, $input ) ) {
				continue;
			}
			$value = nadlan_p3d_prepare_rest_value( $key, $input[ $key ] );
			if ( is_callable( $sanitize_callback ) ) {
				$value = call_user_func( $sanitize_callback, $value );
			}
			update_post_meta( $post_id, $key, $value );
			$updated[] = $key;
		}

		return $updated;
	}
}

add_action(
	'rest_api_init',
	function () {
		register_rest_route(
			'nadlan/v1',
			'/project-showroom/(?P<id>\d+)',
			array(
				array(
					'methods'             => 'GET',
					'permission_callback' => function ( $request ) {
						$post_id = (int) $request['id'];
						return nadlan_p3d_is_project( $post_id ) && current_user_can( 'edit_post', $post_id );
					},
					'callback'            => function ( $request ) {
						return rest_ensure_response( nadlan_p3d_export_showroom_payload( (int) $request['id'] ) );
					},
					'args'                => array(
						'id' => array(
							'sanitize_callback' => 'absint',
							'required'          => true,
						),
					),
				),
				array(
					'methods'             => 'POST',
					'permission_callback' => function ( $request ) {
						$post_id = (int) $request['id'];
						return nadlan_p3d_is_project( $post_id ) && current_user_can( 'edit_post', $post_id );
					},
					'callback'            => function ( $request ) {
						$post_id = (int) $request['id'];
						$params  = $request->get_json_params();
						$updated = nadlan_p3d_apply_showroom_payload( $post_id, is_array( $params ) ? $params : array() );
						if ( is_wp_error( $updated ) ) {
							return $updated;
						}
						$out              = nadlan_p3d_export_showroom_payload( $post_id );
						$out['updated']   = $updated;
						$out['updated_n'] = count( $updated );
						return rest_ensure_response( $out );
					},
					'args'                => array(
						'id' => array(
							'sanitize_callback' => 'absint',
							'required'          => true,
						),
					),
				),
			)
		);
	}
);

if ( ! function_exists( 'nadlan_p3d_meta' ) ) {
	function nadlan_p3d_meta( $post_id, $demo ) {
		$title     = wp_strip_all_tags( get_the_title( $post_id ) );
		$developer = sanitize_text_field( (string) get_post_meta( $post_id, 'developer_name', true ) );
		$status    = sanitize_text_field( (string) get_post_meta( $post_id, 'project_status', true ) );
		$units     = sanitize_text_field( (string) get_post_meta( $post_id, 'num_units', true ) );
		$city      = sanitize_text_field( (string) get_post_meta( $post_id, 'city', true ) );
		$address   = sanitize_text_field( (string) get_post_meta( $post_id, 'address', true ) );
		$lat       = nadlan_p3d_sanitize_decimal( get_post_meta( $post_id, 'lat', true ) );
		$lng       = nadlan_p3d_sanitize_decimal( get_post_meta( $post_id, 'lng', true ) );
		$floor_h   = nadlan_p3d_sanitize_decimal( get_post_meta( $post_id, 'project_3d_floor_height_m', true ) );
		if ( $floor_h <= 0 ) {
			$floor_h = 3.05;
		}
		$ground_m          = nadlan_p3d_sanitize_decimal( get_post_meta( $post_id, 'project_3d_ground_elevation_m', true ) );
		$avg_price_per_sqm = nadlan_p3d_sanitize_decimal( get_post_meta( $post_id, 'project_3d_avg_price_per_sqm', true ) );
		$price_source_note = sanitize_text_field( (string) get_post_meta( $post_id, 'project_3d_price_source_note', true ) );
		$token             = trim( (string) get_option( 'nadlan_mapbox_token', '' ) );
		$model_type        = nadlan_p3d_sanitize_model_type( get_post_meta( $post_id, 'project_3d_model_type', true ) );
		$model_glb         = esc_url_raw( (string) get_post_meta( $post_id, 'project_model_glb', true ) );
		$model_usdz        = esc_url_raw( (string) get_post_meta( $post_id, 'project_model_usdz', true ) );
		$model_poster      = esc_url_raw( (string) get_post_meta( $post_id, 'project_model_poster', true ) );
		$video_url         = esc_url_raw( (string) get_post_meta( $post_id, 'project_3d_video_url', true ) );
		$tour_url          = esc_url_raw( (string) get_post_meta( $post_id, 'project_3d_tour_url', true ) );
		$cesium_url        = esc_url_raw( (string) get_post_meta( $post_id, 'project_3d_cesium_tiles_url', true ) );
		$camera_lock       = nadlan_p3d_sanitize_camera_lock( get_post_meta( $post_id, 'project_3d_camera_lock', true ) );
		$preset_min        = $camera_lock === 'free' ? '0deg' : '78deg';
		$preset_max        = $camera_lock === 'free' ? '180deg' : '85deg';
		$camera_min_polar  = nadlan_p3d_sanitize_degree( get_post_meta( $post_id, 'project_3d_camera_min_polar', true ) );
		$camera_max_polar  = nadlan_p3d_sanitize_degree( get_post_meta( $post_id, 'project_3d_camera_max_polar', true ) );
		$camera_rotation   = nadlan_p3d_sanitize_degree( get_post_meta( $post_id, 'project_3d_camera_rotation_per_second', true ) );
		$camera_auto_raw   = get_post_meta( $post_id, 'project_3d_camera_auto_rotate', true );
		$camera_min_polar  = $camera_min_polar !== '' ? $camera_min_polar : $preset_min;
		$camera_max_polar  = $camera_max_polar !== '' ? $camera_max_polar : $preset_max;
		$camera_rotation   = $camera_rotation !== '' ? $camera_rotation : '8deg';
		$camera_auto       = $camera_auto_raw === '' ? $camera_lock === 'free' : nadlan_p3d_sanitize_checkbox( $camera_auto_raw ) === '1';
		$camera_mid        = ( nadlan_p3d_degree_number( $camera_min_polar, 78 ) + nadlan_p3d_degree_number( $camera_max_polar, 85 ) ) / 2;
		$site_plan_image   = esc_url_raw( (string) get_post_meta( $post_id, 'project_3d_site_plan_image', true ) );
		$facade_images     = nadlan_p3d_clean_facade_images( nadlan_p3d_json_meta( $post_id, 'project_3d_facade_images', array() ) );
		if ( ! $facade_images && nadlan_p3d_matches_dimri_yama( $title, $developer, $city, $address ) ) {
			$facade_images = nadlan_p3d_dimri_yama_concept_facade_images();
		}

		return array(
			'title'     => $title ?: 'הפרויקט',
			'developer' => $developer,
			'status'    => $status,
			'units'     => $units,
			'city'      => $city,
			'address'   => $address,
			'lat'       => $lat,
			'lng'       => $lng,
			'floor_height_m'     => $floor_h,
			'ground_elevation_m' => $ground_m,
			'avg_price_per_sqm'  => $avg_price_per_sqm,
			'price_source_note'  => $price_source_note,
			'mapbox_token'       => $token,
			'model_type'         => $model_type ?: 'procedural',
			'model_glb'          => $model_glb,
			'model_usdz'         => $model_usdz,
			'model_poster'       => $model_poster,
			'model_viewer'       => $model_glb !== '',
			'camera_lock'        => $camera_lock,
			'camera_min_polar'   => $camera_min_polar,
			'camera_max_polar'   => $camera_max_polar,
			'camera_mid_polar'   => rtrim( rtrim( number_format( $camera_mid, 1, '.', '' ), '0' ), '.' ) . 'deg',
			'camera_auto_rotate' => (bool) $camera_auto,
			'camera_rotation_per_second' => $camera_rotation,
			'video_url'          => $video_url,
			'tour_url'           => $tour_url,
			'cesium_tiles_url'   => $cesium_url,
			'drawings'           => nadlan_p3d_clean_material_items( nadlan_p3d_json_meta( $post_id, 'project_3d_drawings_json', array() ) ),
			'environment'        => nadlan_p3d_clean_material_items( nadlan_p3d_json_meta( $post_id, 'project_3d_environment_json', array() ) ),
			'facade_images'      => $facade_images,
			'site_plan_image'    => $site_plan_image,
			'site_plan_polygons' => nadlan_p3d_clean_site_plan_polygons( nadlan_p3d_json_meta( $post_id, 'project_3d_site_plan_polygons', array() ) ),
			'url'       => get_permalink( $post_id ),
			'demo'      => (bool) $demo,
		);
	}
}

if ( ! function_exists( 'nadlan_p3d_json' ) ) {
	function nadlan_p3d_json( $value, $fallback ) {
		$json = wp_json_encode( $value, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT );
		return is_string( $json ) && $json !== '' ? $json : $fallback;
	}
}

if ( ! function_exists( 'nadlan_p3d_has_data' ) ) {
	function nadlan_p3d_has_data( $post_id ) {
		$post_id = (int) $post_id;
		return get_post_meta( $post_id, 'project_3d_image', true ) !== ''
			|| get_post_meta( $post_id, 'project_3d_units', true ) !== ''
			|| get_post_meta( $post_id, 'project_model_glb', true ) !== ''
			|| get_post_meta( $post_id, 'project_3d_demo', true ) === '1';
	}
}

add_filter(
	'script_loader_tag',
	function ( $tag, $handle, $src ) {
		if ( 'nadlan-model-viewer' !== $handle ) {
			return $tag;
		}

		return '<script type="module" src="' . esc_url( $src ) . '" id="nadlan-model-viewer-js"></script>' . "\n";
	},
	10,
	3
);

/* mv-ux: the shared 3D control layer (no self-spin, angle detents, compass,
 * guidance hint) for EVERY model-viewer on the site - engine stages, intl
 * pickers, property viewers, wizard schematics, homepage showcase. Tiny and
 * self-guarding (does nothing on pages without a viewer), so it loads
 * site-wide and also catches viewers mounted later via MutationObserver. */
add_action( 'wp_enqueue_scripts', function () {
	if ( is_admin() ) { return; }
	wp_enqueue_script( 'nadlan-mv-ux', plugins_url( 'assets/showroom-engine/mv-ux.js', dirname( __FILE__ ) ), array(), NADLAN_CONFIG_VERSION, true );
}, 20 );

if ( ! function_exists( 'nadlan_p3d_render_admin_metabox' ) ) {
	function nadlan_p3d_render_admin_metabox( $post ) {
		wp_nonce_field( 'nadlan_p3d_save', 'nadlan_p3d_nonce' );

		$img    = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_image', true ) );
		$vb     = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_viewbox', true ) );
		$fh     = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_floor_height_m', true ) );
		$gm     = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_ground_elevation_m', true ) );
		$ap     = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_avg_price_per_sqm', true ) );
		$psn    = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_price_source_note', true ) );
		$mt     = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_model_type', true ) );
		$glb    = esc_attr( (string) get_post_meta( $post->ID, 'project_model_glb', true ) );
		$usdz   = esc_attr( (string) get_post_meta( $post->ID, 'project_model_usdz', true ) );
		$poster = esc_attr( (string) get_post_meta( $post->ID, 'project_model_poster', true ) );
		$vu     = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_video_url', true ) );
		$tu     = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_tour_url', true ) );
		$cu     = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_cesium_tiles_url', true ) );
		$cl     = nadlan_p3d_sanitize_camera_lock( get_post_meta( $post->ID, 'project_3d_camera_lock', true ) );
		$cmin   = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_camera_min_polar', true ) );
		$cmax   = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_camera_max_polar', true ) );
		$cauto  = get_post_meta( $post->ID, 'project_3d_camera_auto_rotate', true ) === '1';
		$crot   = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_camera_rotation_per_second', true ) );
		$dr     = esc_textarea( (string) get_post_meta( $post->ID, 'project_3d_drawings_json', true ) );
		$env    = esc_textarea( (string) get_post_meta( $post->ID, 'project_3d_environment_json', true ) );
		$fi     = esc_textarea( (string) get_post_meta( $post->ID, 'project_3d_facade_images', true ) );
		$spi    = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_site_plan_image', true ) );
		$spp    = esc_textarea( (string) get_post_meta( $post->ID, 'project_3d_site_plan_polygons', true ) );
		$js     = esc_textarea( (string) get_post_meta( $post->ID, 'project_3d_units', true ) );
		$dm     = get_post_meta( $post->ID, 'project_3d_demo', true ) === '1';
		?>
		<style>
			.nadlan-p3d-admin{direction:rtl;text-align:right;color:#1d2327}
			.nadlan-p3d-admin *{box-sizing:border-box}
			.nadlan-p3d-admin-hero{border:1px solid #d6c189;background:linear-gradient(135deg,#fffaf0,#f7f1df);padding:16px 18px;margin:0 0 14px}
			.nadlan-p3d-admin-hero h3{margin:0 0 6px;font-size:18px}
			.nadlan-p3d-admin-hero p{margin:0;color:#51483a}
			.nadlan-p3d-panel{border:1px solid #dcdcde;background:#fff;margin:12px 0}
			.nadlan-p3d-panel summary{cursor:pointer;font-weight:700;padding:12px 14px;background:#f6f7f7}
			.nadlan-p3d-panel-inner{padding:14px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
			.nadlan-p3d-admin label{font-weight:600}
			.nadlan-p3d-admin label span{display:block;margin-bottom:4px}
			.nadlan-p3d-admin .widefat{margin-top:3px}
			.nadlan-p3d-full{grid-column:1/-1}
			.nadlan-p3d-help{color:#646970;font-size:12px;margin:5px 0 0;line-height:1.45}
			.nadlan-p3d-builder{border:1px solid #c3c4c7;background:#fbfbfb;padding:12px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
			.nadlan-p3d-builder-actions{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
			.nadlan-p3d-unit-list{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:7px;margin-top:4px}
			.nadlan-p3d-unit-list button{border:1px solid #c3c4c7;background:#fff;padding:6px 9px;cursor:pointer}
			.nadlan-p3d-unit-list button:hover,.nadlan-p3d-unit-list button:focus{border-color:#8c6d23;box-shadow:0 0 0 1px #8c6d23;outline:none}
			.nadlan-p3d-json-status{font-weight:700}
			.nadlan-p3d-json-status.is-ok{color:#007017}
			.nadlan-p3d-json-status.is-bad{color:#b32d2e}
			@media(max-width:782px){.nadlan-p3d-panel-inner,.nadlan-p3d-builder{grid-template-columns:1fr}}
		</style>
		<div class="nadlan-p3d-admin" data-post-id="<?php echo esc_attr( (string) $post->ID ); ?>">
			<div class="nadlan-p3d-admin-hero">
				<h3>מרכז תצוגת הפרויקט</h3>
				<p>כאן מחברים מודל תלת ממד, תמונת פתיחה, תוכניות, סרטון, סביבת הפרויקט ודירות לבחירה. השדות נשמרים על הפרויקט ומפעילים את תצוגת הבחירה בעמוד הציבורי.</p>
			</div>

			<details class="nadlan-p3d-panel" open>
				<summary>1. מודל, תמונה וסרטון</summary>
				<div class="nadlan-p3d-panel-inner">
					<label><span>סוג תצוגה</span>
						<select name="project_3d_model_type" class="widefat">
							<?php
							$options = array(
								'procedural' => 'מודל בסיסי כאשר אין חומר רשמי',
								'facade'     => 'חזית דו ממדית עם נקודות בחירה',
								'sprite360'  => 'רצף תמונות 360',
								'gltf'       => 'GLB אמיתי לדפדפן',
								'bim'        => 'BIM רשמי של היזם',
							);
							foreach ( $options as $value => $label ) {
								echo '<option value="' . esc_attr( $value ) . '"' . selected( $mt, $value, false ) . '>' . esc_html( $label ) . '</option>';
							}
							?>
						</select>
					</label>
					<label><span>תמונת מקור או הדמיה מאושרת</span><input type="url" name="project_3d_image" value="<?php echo $img; ?>" class="widefat" placeholder="https://.../facade.webp"></label>
					<label class="nadlan-p3d-full"><span>קובץ GLB למודל מסתובב</span><input type="url" name="project_model_glb" value="<?php echo $glb; ?>" class="widefat" placeholder="https://.../rainbow.glb"><p class="nadlan-p3d-help">קישור ישיר לקובץ GLB. בעתיד מחליפים אותו בקובץ BIM/GLB רשמי מהיזם.</p></label>
					<label><span>Poster קל לפני טעינת המודל</span><input type="url" name="project_model_poster" value="<?php echo $poster; ?>" class="widefat" placeholder="https://.../poster.webp"></label>
					<label><span>USDZ לאייפון, אופציונלי</span><input type="url" name="project_model_usdz" value="<?php echo $usdz; ?>" class="widefat" placeholder="https://.../project.usdz"></label>
					<label><span>סרטון מכירה</span><input type="url" name="project_3d_video_url" value="<?php echo $vu; ?>" class="widefat" placeholder="https://youtube.com/..."></label>
					<label><span>סיור פנים או דירה לדוגמה</span><input type="url" name="project_3d_tour_url" value="<?php echo $tu; ?>" class="widefat" placeholder="https://..."></label>
				<p class="description" style="margin:4px 0 10px">סיור ייעודי בתמונות לפרויקט הזה: העלו לספריית המדיה תמונות עם כותרת <code>walk-<?php echo esc_html( $post->post_name ); ?>-&lt;חלל&gt;</code> (למשל <code>walk-<?php echo esc_html( $post->post_name ); ?>-lobby</code>, <code>-living-room</code>, <code>-exterior</code>) והסיור בעמוד יעבור אוטומטית מהסט הכללי לתמונות של הפרויקט. אין צורך בשמירה כאן.</p>
					<label class="nadlan-p3d-full"><span>Cesium / Google 3D Tiles עתידי</span><input type="url" name="project_3d_cesium_tiles_url" value="<?php echo $cu; ?>" class="widefat" placeholder="https://..."></label>
					<label><span>מצב סיבוב מודל</span>
						<select name="project_3d_camera_lock" class="widefat">
							<option value="horizontal" <?php selected( $cl, 'horizontal' ); ?>>אופקי בלבד, ברירת מחדל לבניין</option>
							<option value="free" <?php selected( $cl, 'free' ); ?>>סיבוב חופשי, רק אם יש מודל מתאים</option>
						</select>
						<p class="nadlan-p3d-help">בניין אינו נעל. ברירת המחדל נועלת את המצלמה לסיבוב אופקי כדי שלא יראו את תחתית המודל.</p>
					</label>
					<label><span>מהירות סיבוב</span><input type="text" name="project_3d_camera_rotation_per_second" value="<?php echo $crot; ?>" class="widefat" placeholder="10deg"></label>
					<label><span>זווית אנכית מינימלית</span><input type="text" name="project_3d_camera_min_polar" value="<?php echo $cmin; ?>" class="widefat" placeholder="78deg"></label>
					<label><span>זווית אנכית מקסימלית</span><input type="text" name="project_3d_camera_max_polar" value="<?php echo $cmax; ?>" class="widefat" placeholder="85deg"></label>
					<label class="nadlan-p3d-full"><input type="checkbox" name="project_3d_camera_auto_rotate" value="1" <?php checked( $cauto, true ); ?>> הפעל סיבוב אוטומטי עדין כאשר הפרויקט מבקש זאת</label>
				</div>
			</details>

			<details class="nadlan-p3d-panel" open>
				<summary>2. מחיר, גובה ומבט מהדירה</summary>
				<div class="nadlan-p3d-panel-inner">
					<label><span>גובה קומה במטרים</span><input type="number" step="0.01" min="2.4" max="5" name="project_3d_floor_height_m" value="<?php echo $fh; ?>" class="widefat" placeholder="3.05"></label>
					<label><span>גובה קרקע משוער במטרים</span><input type="number" step="0.1" min="-50" max="400" name="project_3d_ground_elevation_m" value="<?php echo $gm; ?>" class="widefat" placeholder="0"></label>
					<label><span>אומדן מחיר ממוצע למטר</span><input type="number" step="1" min="0" name="project_3d_avg_price_per_sqm" value="<?php echo $ap; ?>" class="widefat" placeholder="0"></label>
					<label><span>הערה גלויה לאומדן</span><input type="text" name="project_3d_price_source_note" value="<?php echo $psn; ?>" class="widefat" placeholder="אומדן לא מחייב לפי מקור מאושר"></label>
					<label class="nadlan-p3d-full"><span>viewBox לשכבת SVG ישנה</span><input type="text" name="project_3d_viewbox" value="<?php echo $vb; ?>" class="widefat" placeholder="0 0 1000 1000"></label>
				</div>
			</details>

			<details class="nadlan-p3d-panel" open>
				<summary>3. דירות לבחירה</summary>
				<div class="nadlan-p3d-panel-inner">
					<div class="nadlan-p3d-full nadlan-p3d-builder" data-p3d-builder>
						<label><span>מזהה</span><input type="text" class="widefat" data-u-field="id" placeholder="31A"></label>
						<label><span>כותרת</span><input type="text" class="widefat" data-u-field="title" placeholder="דירה 31A"></label>
						<label><span>קומה</span><input type="number" class="widefat" data-u-field="floor" placeholder="12"></label>
						<label><span>חדרים</span><input type="number" step="0.5" class="widefat" data-u-field="rooms" placeholder="5"></label>
						<label><span>מטרים</span><input type="number" class="widefat" data-u-field="sqm" placeholder="124"></label>
						<label><span>כיוון או נוף</span><input type="text" class="widefat" data-u-field="view" placeholder="מערב, נוף לים"></label>
						<label><span>אומדן מחיר</span><input type="number" class="widefat" data-u-field="price_estimate" placeholder="0"></label>
						<label><span>סטטוס</span><select class="widefat" data-u-field="status"><option value="available">זמינה</option><option value="reserved">בבדיקה</option><option value="sold">לא זמינה</option></select></label>
						<label><span>מיקום נקודה במודל</span><input type="text" class="widefat" data-u-field="hotspot_position" placeholder="0m 20m 0m"></label>
						<label><span>כיוון נקודה במודל</span><input type="text" class="widefat" data-u-field="hotspot_normal" placeholder="0m 0m 1m"></label>
						<label><span>תוכנית דירה</span><input type="url" class="widefat" data-u-field="plan" placeholder="https://..."></label>
						<label><span>דירה מומלצת</span><select class="widefat" data-u-field="recommended"><option value="">לא</option><option value="1">כן</option></select></label>
						<div class="nadlan-p3d-builder-actions">
							<button type="button" class="button button-primary" data-p3d-add-unit>הוסף או עדכן דירה</button>
							<button type="button" class="button" data-p3d-clear-unit>נקה טופס</button>
							<button type="button" class="button" data-p3d-check-json>בדוק JSON</button>
							<span class="nadlan-p3d-json-status" data-p3d-json-status></span>
						</div>
						<div class="nadlan-p3d-unit-list" data-p3d-unit-list></div>
					</div>
					<label class="nadlan-p3d-full"><span>יחידות JSON מתקדם</span><textarea name="project_3d_units" rows="10" class="widefat code" data-p3d-units-json><?php echo $js; ?></textarea><p class="nadlan-p3d-help">אפשר לערוך ידנית או להשתמש בטופס מעל. חובה לשמור מזהה, קומה, חדרים, מטרים, סטטוס ומיקום נקודה כדי שהדירה תהיה קליקה על המודל.</p></label>
				</div>
			</details>

			<details class="nadlan-p3d-panel">
				<summary>4. תוכניות, סביבת הפרויקט וחומרי שיווק</summary>
				<div class="nadlan-p3d-panel-inner">
					<label class="nadlan-p3d-full"><span>תוכניות JSON</span><textarea name="project_3d_drawings_json" rows="5" class="widefat code"><?php echo $dr; ?></textarea><p class="nadlan-p3d-help">מבנה: [{"label":"תוכנית קומה 12","url":"https://...","type":"plan"}]</p></label>
					<label class="nadlan-p3d-full"><span>סביבת הפרויקט JSON</span><textarea name="project_3d_environment_json" rows="5" class="widefat code"><?php echo $env; ?></textarea><p class="nadlan-p3d-help">מבנה: [{"label":"פארק החוף","detail":"מרחק הליכה","url":"https://..."}]</p></label>
					<label class="nadlan-p3d-full"><span>חזיתות לבחירת דירות JSON</span><textarea name="project_3d_facade_images" rows="5" class="widefat code"><?php echo $fi; ?></textarea><p class="nadlan-p3d-help">מבנה: [{"building":"A","label":"חזית מערבית","src":"https://...","viewbox":"0 0 1000 1200"}]</p></label>
					<label class="nadlan-p3d-full"><span>תוכנית מתחם או אתר</span><input type="url" name="project_3d_site_plan_image" value="<?php echo $spi; ?>" class="widefat" placeholder="https://.../site-plan.webp"></label>
					<label class="nadlan-p3d-full"><span>פוליגונים לתוכנית מתחם JSON</span><textarea name="project_3d_site_plan_polygons" rows="5" class="widefat code"><?php echo $spp; ?></textarea><p class="nadlan-p3d-help">מבנה: [{"building":"A","label":"בניין מערבי","points":"10,10 40,10 40,50 10,50"}]</p></label>
				</div>
			</details>

			<p><label><input type="checkbox" name="project_3d_demo" value="1" <?php checked( $dm, true ); ?>> הצג מודל הדגמה כאשר אין מלאי רשמי</label></p>
			<p class="description">במצב הדגמה המחיר מוצג כאומדן או לפי פנייה כדי לא להציג נתוני מכירה לא מאומתים.</p>
		</div>
		<script>
		(function(){
			var script = document.currentScript;
			var box = script ? script.previousElementSibling : null;
			if (!box || !box.classList.contains('nadlan-p3d-admin')) { return; }
			var textarea = box.querySelector('[data-p3d-units-json]');
			var status = box.querySelector('[data-p3d-json-status]');
			var list = box.querySelector('[data-p3d-unit-list]');
			var fields = box.querySelectorAll('[data-u-field]');
			function readUnits(){
				var raw = textarea.value.trim();
				if (!raw) { return []; }
				var parsed = JSON.parse(raw);
				return Array.isArray(parsed) ? parsed : [];
			}
			function writeUnits(units){
				textarea.value = JSON.stringify(units, null, 2);
				renderList();
				showStatus('JSON תקין, לא לשכוח לעדכן את הפרויקט', true);
			}
			function showStatus(text, ok){
				if (!status) { return; }
				status.textContent = text;
				status.className = 'nadlan-p3d-json-status ' + (ok ? 'is-ok' : 'is-bad');
			}
			function getField(name){
				return box.querySelector('[data-u-field="' + name + '"]');
			}
			function collectUnit(){
				var out = {};
				Array.prototype.forEach.call(fields, function(field){
					var key = field.getAttribute('data-u-field');
					var val = (field.value || '').trim();
					if (val === '') { return; }
					if (key === 'floor' || key === 'sqm' || key === 'price_estimate' || key === 'rooms') { val = parseFloat(val); }
					if (key === 'recommended') { val = val === '1'; }
					out[key] = val;
				});
				if (!out.id) { out.id = 'unit-' + Date.now(); }
				if (!out.title) { out.title = 'דירה ' + out.id; }
				if (!out.status) { out.status = 'available'; }
				return out;
			}
			function fillUnit(unit){
				Array.prototype.forEach.call(fields, function(field){
					var key = field.getAttribute('data-u-field');
					var val = unit[key];
					if (key === 'recommended') { field.value = val ? '1' : ''; return; }
					field.value = val === undefined || val === null ? '' : String(val);
				});
			}
			function clearUnit(){
				Array.prototype.forEach.call(fields, function(field){ field.value = ''; });
				var st = getField('status');
				if (st) { st.value = 'available'; }
			}
			function renderList(){
				if (!list) { return; }
				var units = [];
				try { units = readUnits(); } catch(e) { list.innerHTML = ''; return; }
				list.innerHTML = '';
				units.forEach(function(unit){
					var b = document.createElement('button');
					b.type = 'button';
					b.textContent = (unit.title || unit.id || 'דירה') + ' · ' + (unit.status || 'available');
					b.setAttribute('data-unit-id', unit.id || '');
					b.addEventListener('click', function(){ fillUnit(unit); });
					list.appendChild(b);
				});
			}
			var add = box.querySelector('[data-p3d-add-unit]');
			if (add) {
				add.addEventListener('click', function(){
					var units;
					try { units = readUnits(); } catch(e) { showStatus('JSON לא תקין, תקנו לפני הוספה', false); return; }
					var unit = collectUnit();
					var replaced = false;
					units = units.map(function(oldUnit){
						if (String(oldUnit.id) === String(unit.id)) { replaced = true; return unit; }
						return oldUnit;
					});
					if (!replaced) { units.push(unit); }
					writeUnits(units);
				});
			}
			var clear = box.querySelector('[data-p3d-clear-unit]');
			if (clear) { clear.addEventListener('click', clearUnit); }
			var check = box.querySelector('[data-p3d-check-json]');
			if (check) {
				check.addEventListener('click', function(){
					try { showStatus('JSON תקין: ' + readUnits().length + ' דירות', true); renderList(); }
					catch(e) { showStatus('JSON לא תקין: ' + e.message, false); }
				});
			}
			renderList();
		})();
		</script>
		<?php
	}
}

add_action(
	'add_meta_boxes',
	function () {
		if ( ! nadlan_p3d_enabled() ) {
			return;
		}

		add_meta_box(
			'nadlan-p3d',
			'בחירת דירות אינטראקטיבית',
			'nadlan_p3d_render_admin_metabox',
			'nadlan_project',
			'normal'
		);
	}
);

add_action(
	'save_post_nadlan_project',
	function ( $post_id ) {
		if ( ! isset( $_POST['nadlan_p3d_nonce'] ) || ! wp_verify_nonce( $_POST['nadlan_p3d_nonce'], 'nadlan_p3d_save' ) ) {
			return;
		}
		if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
			return;
		}
		if ( ! current_user_can( 'edit_post', $post_id ) ) {
			return;
		}

		update_post_meta( $post_id, 'project_3d_image', esc_url_raw( wp_unslash( $_POST['project_3d_image'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_viewbox', sanitize_text_field( wp_unslash( $_POST['project_3d_viewbox'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_floor_height_m', nadlan_p3d_sanitize_decimal( wp_unslash( $_POST['project_3d_floor_height_m'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_ground_elevation_m', nadlan_p3d_sanitize_decimal( wp_unslash( $_POST['project_3d_ground_elevation_m'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_avg_price_per_sqm', nadlan_p3d_sanitize_decimal( wp_unslash( $_POST['project_3d_avg_price_per_sqm'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_price_source_note', sanitize_text_field( wp_unslash( $_POST['project_3d_price_source_note'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_model_type', nadlan_p3d_sanitize_model_type( wp_unslash( $_POST['project_3d_model_type'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_model_glb', esc_url_raw( wp_unslash( $_POST['project_model_glb'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_model_usdz', esc_url_raw( wp_unslash( $_POST['project_model_usdz'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_model_poster', esc_url_raw( wp_unslash( $_POST['project_model_poster'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_video_url', esc_url_raw( wp_unslash( $_POST['project_3d_video_url'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_tour_url', esc_url_raw( wp_unslash( $_POST['project_3d_tour_url'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_cesium_tiles_url', esc_url_raw( wp_unslash( $_POST['project_3d_cesium_tiles_url'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_camera_lock', nadlan_p3d_sanitize_camera_lock( wp_unslash( $_POST['project_3d_camera_lock'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_camera_min_polar', nadlan_p3d_sanitize_degree( wp_unslash( $_POST['project_3d_camera_min_polar'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_camera_max_polar', nadlan_p3d_sanitize_degree( wp_unslash( $_POST['project_3d_camera_max_polar'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_camera_auto_rotate', ! empty( $_POST['project_3d_camera_auto_rotate'] ) ? '1' : '0' );
		update_post_meta( $post_id, 'project_3d_camera_rotation_per_second', nadlan_p3d_sanitize_degree( wp_unslash( $_POST['project_3d_camera_rotation_per_second'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_drawings_json', nadlan_p3d_sanitize_material_json( wp_unslash( $_POST['project_3d_drawings_json'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_environment_json', nadlan_p3d_sanitize_material_json( wp_unslash( $_POST['project_3d_environment_json'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_facade_images', nadlan_p3d_sanitize_json_text( wp_unslash( $_POST['project_3d_facade_images'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_site_plan_image', esc_url_raw( wp_unslash( $_POST['project_3d_site_plan_image'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_site_plan_polygons', nadlan_p3d_sanitize_json_text( wp_unslash( $_POST['project_3d_site_plan_polygons'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_units', nadlan_p3d_sanitize_units_json( wp_unslash( $_POST['project_3d_units'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_demo', ! empty( $_POST['project_3d_demo'] ) ? '1' : '0' );
	}
);

