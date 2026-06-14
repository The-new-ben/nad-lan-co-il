<?php
/**
 * nadlan-config - premium interactive project model and apartment picker.
 *
 * Tier 1 stays fast and practical: an architectural massing model from
 * project/unit metadata, routed into the existing /nadlan/v1/lead funnel.
 * Real developer drawings can replace demo units later without changing the
 * public journey.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

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
		);
		return $labels[ $status ] ?? $labels['available'];
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

			$status = sanitize_key( (string) ( $u['status'] ?? 'available' ) );
			if ( ! in_array( $status, array( 'available', 'reserved', 'sold' ), true ) ) {
				$status = 'available';
			}
			$price_note = sanitize_textarea_field( (string) ( $u['price_note'] ?? '' ) );

			$out[] = array(
				'id'      => sanitize_key( (string) $u['id'] ),
				'title'   => sanitize_text_field( (string) ( $u['title'] ?? '' ) ),
				'points'  => preg_replace( '/[^0-9,. \-]/', '', (string) ( $u['points'] ?? '' ) ),
				'floor'   => max( 0, (int) ( $u['floor'] ?? 0 ) ),
				'rooms'   => nadlan_p3d_sanitize_decimal( $u['rooms'] ?? 0 ),
				'sqm'     => nadlan_p3d_sanitize_decimal( $u['sqm'] ?? 0 ),
				'balcony' => nadlan_p3d_sanitize_decimal( $u['balcony'] ?? 0 ),
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

add_action(
	'init',
	function () {
		$auth = function ( $allowed, $meta_key, $post_id ) {
			unset( $allowed, $meta_key );
			return current_user_can( 'edit_post', (int) $post_id );
		};

		$fields = array(
			'project_3d_model_type'       => 'nadlan_p3d_sanitize_model_type',
			'project_model_glb'           => 'esc_url_raw',
			'project_model_usdz'          => 'esc_url_raw',
			'project_model_poster'        => 'esc_url_raw',
			'project_3d_video_url'        => 'esc_url_raw',
			'project_3d_tour_url'         => 'esc_url_raw',
			'project_3d_cesium_tiles_url' => 'esc_url_raw',
			'project_3d_drawings_json'    => 'nadlan_p3d_sanitize_material_json',
			'project_3d_environment_json' => 'nadlan_p3d_sanitize_material_json',
			'project_3d_units'            => 'nadlan_p3d_sanitize_units_json',
		);

		foreach ( $fields as $key => $sanitize_callback ) {
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
			'video_url'          => $video_url,
			'tour_url'           => $tour_url,
			'cesium_tiles_url'   => $cesium_url,
			'drawings'           => nadlan_p3d_clean_material_items( nadlan_p3d_json_meta( $post_id, 'project_3d_drawings_json', array() ) ),
			'environment'        => nadlan_p3d_clean_material_items( nadlan_p3d_json_meta( $post_id, 'project_3d_environment_json', array() ) ),
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

if ( ! function_exists( 'nadlan_p3d_insert_after_project_header' ) ) {
	function nadlan_p3d_insert_after_project_header( $content, $block ) {
		if ( strpos( $content, 'nlp3d-premium' ) !== false ) {
			return $content;
		}

		$header_pos = false;
		if ( preg_match( '/<div\s+class=["\']nlpf\b/i', $content, $m, PREG_OFFSET_CAPTURE ) ) {
			$header_pos = (int) $m[0][1];
		}
		if ( $header_pos === false ) {
			return $block . $content;
		}

		return substr( $content, 0, $header_pos ) . $block . substr( $content, $header_pos );
	}
}

if ( ! function_exists( 'nadlan_p3d_render' ) ) {
	function nadlan_p3d_render( $post_id ) {
		if ( ! nadlan_p3d_enabled() ) {
			return '';
		}

		$post_id = (int) $post_id;
		$image   = esc_url( (string) get_post_meta( $post_id, 'project_3d_image', true ) );
		$viewbox = sanitize_text_field( (string) get_post_meta( $post_id, 'project_3d_viewbox', true ) );
		if ( $viewbox === '' ) {
			$viewbox = '0 0 1000 1000';
		}
		$units   = nadlan_p3d_units( $post_id );
		$demo    = false;
		if ( ! $units ) {
			$units = nadlan_p3d_demo_units();
			$demo  = true;
		}
		if ( $image === '' && $demo ) {
			$image = esc_url( plugins_url( '../assets/concept/rainbow-facade-demo.svg', __FILE__ ) );
		}
		$image_alt = $demo ? 'המחשת חזית מקורית של מגדל ובנייני בוטיק לבחירת דירה' : 'חומר מקור של הפרויקט';
		$image_cap = $demo ? 'המחשה מקורית, לא תכנית מכר רשמית' : 'חומר מקור';

		$meta      = nadlan_p3d_meta( $post_id, $demo );
		$uid       = 'nlp3d-' . $post_id;
		$unit_json = nadlan_p3d_json( $units, '[]' );
		$meta_json = nadlan_p3d_json( $meta, '{}' );
		$has_model_viewer = ! empty( $meta['model_glb'] );

		ob_start();
		?>
<!-- nlp3d-start -->
<section class="nlp3d nlp3d-premium" dir="rtl" data-project="<?php echo esc_attr( $post_id ); ?>" aria-labelledby="<?php echo esc_attr( $uid ); ?>-title">
	<div class="nlp3d-grid" aria-hidden="true"></div>
	<div class="nlp3d-shell">
		<div class="nlp3d-copy">
			<p class="nlp3d-kicker">Rainbow תל אביב · שדה דב</p>
			<h2 id="<?php echo esc_attr( $uid ); ?>-title">דירות למכירה ב-<?php echo esc_html( $meta['title'] ); ?>: בחירת דירה בתלת ממד</h2>
			<p class="nlp3d-lead-text">פרויקט Rainbow Tel Aviv של ישראל קנדה במתחם שדה דב מציג בחירה אינטראקטיבית של קומה, כיוון, שטח, אור ונוף. המחירים והזמינות מוצגים כאומדן לא מחייב ודורשים אימות מול היזם לפני כל התקדמות.</p>
			<div class="nlp3d-shop-path" aria-label="תהליך בחירה">
				<span>1. מסובבים</span>
				<span>2. בוחרים דירה</span>
				<span>3. בודקים ליווי</span>
				<span>4. מבקשים התקדמות</span>
			</div>
			<div class="nlp3d-metrics" aria-label="פרטי פרויקט">
				<span><?php echo $meta['developer'] ? esc_html( $meta['developer'] ) : 'יזם יימסר בפנייה'; ?></span>
				<span><?php echo $meta['status'] ? esc_html( $meta['status'] ) : 'סטטוס בבדיקה'; ?></span>
				<span><?php echo $meta['units'] ? esc_html( $meta['units'] ) . ' יחידות' : 'מלאי לפי פנייה'; ?></span>
			</div>
			<?php if ( $demo ) : ?>
				<p class="nlp3d-demo-note">תצוגת הדגמה. הדירות, המחירים והזמינות אינם נתוני מכירה רשמיים. הנתונים האמיתיים יוזנו כאשר היזם או מנהל הפרויקט יאשרו מלאי ותוכניות.</p>
			<?php endif; ?>
		</div>

		<div class="nlp3d-stage-wrap">
			<div class="nlp3d-toolbar" aria-label="שליטה במודל">
				<button type="button" class="nlp3d-angle is-active" data-angle="-32" data-action="angle-facade">חזית</button>
				<button type="button" class="nlp3d-angle" data-angle="0" data-action="angle-sea">ים</button>
				<button type="button" class="nlp3d-angle" data-angle="32" data-action="angle-city">עיר</button>
				<button type="button" class="nlp3d-orbit" data-orbit="1" data-action="orbit-building">סיבוב</button>
				<button type="button" class="nlp3d-zoom" data-zoom="in" data-action="zoom-in">קרב</button>
				<button type="button" class="nlp3d-zoom" data-zoom="out" data-action="zoom-out">הרחק</button>
				<span class="nlp3d-drag-note">אפשר לגרור את המודל</span>
			</div>
			<div class="nlp3d-scene<?php echo $has_model_viewer ? ' has-model-viewer' : ''; ?>" style="--angle:-32deg" role="group" aria-label="מודל תלת ממדי סכמטי של מגדל מגורים">
				<?php if ( $has_model_viewer ) : ?>
					<model-viewer
						class="nlp3d-model-viewer"
						src="<?php echo esc_url( $meta['model_glb'] ); ?>"
						<?php if ( ! empty( $meta['model_poster'] ) ) : ?>poster="<?php echo esc_url( $meta['model_poster'] ); ?>"<?php endif; ?>
						<?php if ( ! empty( $meta['model_usdz'] ) ) : ?>ios-src="<?php echo esc_url( $meta['model_usdz'] ); ?>"<?php endif; ?>
						alt="<?php echo esc_attr( $meta['title'] . ' 3D model' ); ?>"
						reveal="auto"
						loading="auto"
						camera-controls
						auto-rotate
						auto-rotate-delay="2500"
						rotation-per-second="18deg"
						min-camera-orbit="-Infinity 0deg auto"
						max-camera-orbit="Infinity 180deg auto"
						field-of-view="30deg"
						camera-target="0m 68m 0m"
						environment-image="neutral"
						exposure="1.45"
						shadow-intensity="1"
						shadow-softness=".7"
						ar
						ar-modes="webxr scene-viewer quick-look">
						<?php foreach ( $units as $unit ) : ?>
							<?php
							$hotspot_position = nadlan_p3d_hotspot_vector( $unit['hotspot_position'] ?? '' );
							if ( $hotspot_position === '' ) {
								continue;
							}
							$hotspot_normal = nadlan_p3d_hotspot_vector( $unit['hotspot_normal'] ?? '' );
							if ( $hotspot_normal === '' ) {
								$hotspot_normal = '0 0 1';
							}
							$hotspot_title = $unit['title'] ? $unit['title'] : $unit['id'];
							?>
							<button
								type="button"
								class="nlp3d-mv-hotspot"
								slot="<?php echo esc_attr( 'hotspot-' . sanitize_html_class( (string) $unit['id'] ) ); ?>"
								data-position="<?php echo esc_attr( $hotspot_position ); ?>"
								data-normal="<?php echo esc_attr( $hotspot_normal ); ?>"
								data-visibility-attribute="visible"
								data-unit="<?php echo esc_attr( $unit['id'] ); ?>">
								<span class="nlp3d-mv-label"><?php echo esc_html( $hotspot_title ); ?></span>
							</button>
						<?php endforeach; ?>
					</model-viewer>
				<?php endif; ?>
				<div class="nlp3d-horizon"></div>
				<div class="nlp3d-sea"></div>
				<div class="nlp3d-park"></div>
				<div class="nlp3d-runway"></div>
				<div class="nlp3d-tower" role="group" aria-label="בחירת קומה ישירות מהמגדל"></div>
				<div class="nlp3d-shadow" aria-hidden="true"></div>
				<?php if ( $image ) : ?>
					<figure class="nlp3d-facade" data-viewbox="<?php echo esc_attr( $viewbox ); ?>">
						<img src="<?php echo $image; ?>" alt="<?php echo esc_attr( $image_alt ); ?>" loading="lazy">
						<svg class="nlp3d-facade-hotspots" viewBox="<?php echo esc_attr( $viewbox ); ?>" preserveAspectRatio="none" aria-label="בחירת דירה על גבי החזית"></svg>
						<figcaption><?php echo esc_html( $image_cap ); ?></figcaption>
					</figure>
				<?php endif; ?>
			</div>
			<div class="nlp3d-viewframe nlp3d-stage-viewframe" hidden>
				<div class="nlp3d-view-sky"></div>
				<div class="nlp3d-view-lines"></div>
				<div class="nlp3d-view-map" hidden aria-label="מבט חי מגובה הדירה"></div>
				<span class="nlp3d-view-badge" hidden>3D חי · גרירה לסיבוב</span>
				<button type="button" class="nlp3d-stage-return" data-action="return-model">חזרה למודל</button>
				<p class="nlp3d-view-copy"></p>
			</div>
			<div class="nlp3d-stage-card" aria-live="polite" hidden>
				<span class="nlp3d-stage-kicker">הדירה שנבחרה</span>
				<strong class="nlp3d-stage-card-title">בחרו דירה על הבניין</strong>
				<small class="nlp3d-stage-card-meta">גררו לסיבוב, בחרו קומה והתקדמו רק כאשר הפרטים מתאימים.</small>
				<div class="nlp3d-stage-card-stats" aria-label="פרטי דירה נבחרת">
					<span class="nlp3d-stage-price">לפי פנייה</span>
					<span class="nlp3d-stage-status">בחירה פתוחה</span>
					<span class="nlp3d-stage-view">מבט לפי כיוון</span>
				</div>
				<div class="nlp3d-stage-card-actions">
					<button type="button" class="nlp3d-stage-details" data-action="stage-details">פרטים</button>
					<button type="button" class="nlp3d-stage-view-btn" data-action="stage-view">מבט</button>
					<button type="button" class="nlp3d-stage-inquiry" data-action="stage-inquiry">התקדמות</button>
				</div>
			</div>
		</div>

		<aside class="nlp3d-console" aria-label="בחירת דירה">
			<div class="nlp3d-selection-dock" aria-live="polite">
				<span>בחירה נוכחית</span>
				<strong class="nlp3d-dock-title">בחרו דירה</strong>
				<small class="nlp3d-dock-meta"></small>
				<div class="nlp3d-dock-actions">
					<button type="button" class="nlp3d-dock-spin" data-action="dock-360">סיבוב 360</button>
					<button type="button" class="nlp3d-dock-action" data-action="dock-inquiry">התקדמות</button>
				</div>
			</div>
			<div class="nlp3d-console-head">
				<p>בחרו קומה ודירה</p>
				<span class="nlp3d-status-chip">מודל פעיל</span>
			</div>
			<div class="nlp3d-floor-strip" aria-label="קומות זמינות"></div>
			<div class="nlp3d-units" aria-label="דירות בקומה"></div>
			<div class="nlp3d-detail" aria-live="polite">
				<h3 class="nlp3d-selected-title">בחרו דירה</h3>
				<dl class="nlp3d-facts"></dl>
				<a class="nlp3d-plan" href="#" target="_blank" rel="noopener" hidden>פתיחת תוכנית דירה</a>
				<button type="button" class="nlp3d-view-toggle" data-action="view-from-unit">מבט מהדירה</button>
				<div class="nlp3d-tools" aria-label="מידע נוסף על הדירה">
					<button type="button" class="nlp3d-tool is-active" data-tool="spec" data-action="unit-spec">מפרט</button>
					<button type="button" class="nlp3d-tool" data-tool="drawing" data-action="unit-drawing">תוכנית</button>
					<button type="button" class="nlp3d-tool" data-tool="view" data-action="unit-view">מבט</button>
					<button type="button" class="nlp3d-tool" data-tool="sun" data-action="unit-sun">אור ושמש</button>
					<button type="button" class="nlp3d-tool" data-tool="surroundings" data-action="unit-surroundings">סביבה</button>
					<button type="button" class="nlp3d-tool" data-tool="media" data-action="unit-media">מדיה</button>
					<button type="button" class="nlp3d-tool" data-tool="advisors" data-action="unit-advisors">יועצים</button>
				</div>
				<div class="nlp3d-tool-panel" aria-live="polite"></div>
				<div class="nlp3d-deal-steps" aria-label="מסלול בדיקת רכישה">
					<span data-step="select">בחירה</span>
					<span data-step="verify">אימות</span>
					<span data-step="advisors">ליווי</span>
					<span data-step="developer">אישור יזם</span>
				</div>
			</div>
			<div class="nlp3d-compare-tray" hidden aria-label="דירות להשוואה">
				<span class="nlp3d-compare-label">השוואה:</span>
				<span class="nlp3d-compare-chips"></span>
				<button type="button" class="nlp3d-compare-open" data-action="open-compare">השוו דירות</button>
			</div>
			<form class="nlp3d-lead-form">
				<p class="nlp3d-form-title">רוצים להתקדם עם הדירה הזו?</p>
				<div class="nlp3d-wdots" aria-hidden="true"><span class="is-on"></span><span></span></div>
				<div class="nlp3d-wstep" data-wstep="1">
					<input type="text" name="name" placeholder="שם מלא" autocomplete="name" required>
					<input type="tel" name="phone" placeholder="טלפון" autocomplete="tel" required>
					<input type="email" name="email" placeholder="אימייל" autocomplete="email">
					<button type="button" class="nlp3d-wnext" data-action="wizard-next">המשך לפרטי ההתקדמות</button>
				</div>
				<div class="nlp3d-wstep" data-wstep="2" hidden>
					<input type="text" name="budget" placeholder="מסגרת תקציב, אם ידועה">
					<input type="text" name="timeline" placeholder="מתי רלוונטי להתקדם?">
					<fieldset class="nlp3d-advisors">
						<legend>ליווי מקצועי לצירוף, אפשר לסמן כמה</legend>
						<label><input type="checkbox" name="advisors" value="עורך דין רכישה"> עורך דין רכישה</label>
						<label><input type="checkbox" name="advisors" value="יועץ משכנתאות"> יועץ משכנתאות</label>
						<label><input type="checkbox" name="advisors" value="בדק בית"> בדק בית</label>
						<label><input type="checkbox" name="advisors" value="מעצב פנים"> מעצב פנים</label>
					</fieldset>
					<div class="nlp3d-actions">
						<button type="submit" class="nlp3d-send" data-intent="callback" data-action="lead-callback">דברו איתי על הדירה</button>
						<button type="submit" class="nlp3d-send nlp3d-send-alt" data-intent="purchase" data-action="nonbinding-purchase-check">התחל בדיקת רכישה - לא מחייב</button>
					</div>
					<button type="button" class="nlp3d-wback" data-action="wizard-back">חזרה לפרטי הקשר</button>
				</div>
				<input type="text" name="company" class="nlp3d-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
				<p class="nlp3d-legal">הפנייה אינה עסקה מחייבת, אינה זכרון דברים ואינה שריון רשמי. נציג יאמת זמינות, מחיר ותנאים עם היזם לפני כל התקדמות.</p>
				<p class="nlp3d-ok" hidden></p>
			</form>
		</aside>
	</div>
	<div class="nlp3d-showcase" aria-label="תצוגת עומק לפרויקט">
		<div class="nlp3d-showcase-copy">
			<p class="nlp3d-kicker">מעמוד פרויקט לעמדת בחירה</p>
			<h3>כל החלטה מתחילה ממבט ברור יותר על הדירה</h3>
			<p>העמוד מחבר בין חזית לחיצה, מבט מגובה הדירה, שעות שמש, השוואת יחידות ובקשת ליווי מקצועי. המידע מוצג כשכבה תכנונית עדינה, עם סימון ברור של נתונים שמחייבים אימות מול היזם.</p>
		</div>
		<div class="nlp3d-showcase-cards" aria-label="יכולות תצוגה">
			<article>
				<span>01</span>
				<strong>חזית לחיצה</strong>
				<p>בחירת קומה ודירה ישירות מהמודל, כולל קו, שטח, כיוון ונוף.</p>
			</article>
			<article>
				<span>02</span>
				<strong>מבט מהדירה</strong>
				<p>מצלמה חיה לפי גובה הקומה וכיוון הדירה, כאשר נתוני המפה זמינים.</p>
			</article>
			<article>
				<span>03</span>
				<strong>בדיקת אור ושמש</strong>
				<p>חישוב עונתי של שמש ישירה לפי מיקום הפרויקט וכיוון החזית.</p>
			</article>
			<article>
				<span>04</span>
				<strong>מסלול התקדמות</strong>
				<p>פנייה ממוקדת עם הדירה שנבחרה, תקציב, מועד וליווי מקצועי רצוי.</p>
			</article>
		</div>
		<form class="nlp3d-owner-form" aria-label="בקשה להצגת פרויקט">
			<div>
				<p class="nlp3d-owner-title">מציגים פרויקט חדש?</p>
				<p>אפשר לבנות עמוד תצוגה דומה לפרויקט שלכם, עם קומות, דירות, מבט מהדירה ופנייה מסודרת למתעניינים.</p>
			</div>
			<input type="text" name="name" placeholder="שם מלא" autocomplete="name" required>
			<input type="tel" name="phone" placeholder="טלפון" autocomplete="tel" required>
			<input type="email" name="email" placeholder="אימייל" autocomplete="email">
			<input type="text" name="project_name" placeholder="שם הפרויקט">
			<input type="text" name="city" placeholder="עיר או אזור">
			<input type="text" name="company" class="nlp3d-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
			<button type="submit" data-action="owner-showcase-request">בדיקת התאמה לפרויקט</button>
			<p class="nlp3d-owner-ok" hidden></p>
		</form>
	</div>
	<div class="nlp3d-overlay nlp3d-compare-overlay" hidden role="dialog" aria-modal="true" aria-label="השוואת דירות">
		<div class="nlp3d-overlay-box">
			<button type="button" class="nlp3d-overlay-close" data-action="close-compare" aria-label="סגירה">×</button>
			<h3>השוואת דירות</h3>
			<div class="nlp3d-compare-table"></div>
		</div>
	</div>
	<div class="nlp3d-overlay nlp3d-plan-overlay" hidden role="dialog" aria-modal="true" aria-label="תוכנית דירה">
		<div class="nlp3d-overlay-box">
			<button type="button" class="nlp3d-overlay-close" data-action="close-plan" aria-label="סגירה">×</button>
			<h3 class="nlp3d-plan-title">תוכנית דירה</h3>
			<div class="nlp3d-plan-body"></div>
		</div>
	</div>
	<script type="application/json" class="nlp3d-data"><?php echo $unit_json; ?></script>
	<script type="application/json" class="nlp3d-meta"><?php echo $meta_json; ?></script>
</section>
<!-- nlp3d-end -->
		<?php
		return ob_get_clean();
	}
}

add_shortcode(
	'nadlan_project_3d',
	function ( $atts ) {
		$atts = shortcode_atts( array( 'id' => get_the_ID() ), $atts );
		return nadlan_p3d_render( (int) $atts['id'] );
	}
);

if ( ! function_exists( 'nadlan_p3d_is_project_profile' ) ) {
	function nadlan_p3d_is_project_profile() {
		if ( ! nadlan_p3d_enabled() || ! is_singular( 'nadlan_project' ) ) {
			return false;
		}
		$post_id = (int) get_queried_object_id();
		return $post_id > 0 && nadlan_p3d_has_data( $post_id );
	}
}

if ( ! function_exists( 'nadlan_p3d_seo_title' ) ) {
	function nadlan_p3d_seo_title( $title ) {
		if ( ! nadlan_p3d_is_project_profile() ) {
			return $title;
		}
		$name = wp_strip_all_tags( get_the_title( get_queried_object_id() ) );
		return sprintf( '%s | בחירת דירות, מבט מהדירה ושדה דב | נדלן חכם', $name );
	}
}

if ( ! function_exists( 'nadlan_p3d_seo_description' ) ) {
	function nadlan_p3d_seo_description( $description ) {
		if ( ! nadlan_p3d_is_project_profile() ) {
			return $description;
		}
		$name = wp_strip_all_tags( get_the_title( get_queried_object_id() ) );
		return sprintf( '%s: בחירת דירות אינטראקטיבית, מבט מהדירה, אור ושמש, השוואת יחידות וליווי רכישה ראשוני בשדה דב תל אביב.', $name );
	}
}

add_filter( 'wpseo_title', 'nadlan_p3d_seo_title', 20 );
add_filter( 'pre_get_document_title', 'nadlan_p3d_seo_title', 20 );
add_filter( 'wpseo_metadesc', 'nadlan_p3d_seo_description', 20 );
add_filter( 'wpseo_opengraph_desc', 'nadlan_p3d_seo_description', 20 );
add_filter( 'wpseo_twitter_description', 'nadlan_p3d_seo_description', 20 );

if ( ! function_exists( 'nadlan_p3d_inline_css' ) ) {
	function nadlan_p3d_inline_css() {
		return <<<'CSS'
.nlp3d,.nlp3d *{box-sizing:border-box}.nlp3d{--ink:#f6efe2;--muted:#c9bd9f;--gold:#c4a15a;--gold2:#ead8a3;--deep:#071817;--teal:#103b3b;--panel:rgba(7,15,16,.72);width:100%;margin:42px auto;color:var(--ink);position:relative;overflow:hidden;background:radial-gradient(circle at 18% 8%,rgba(25,105,105,.55),transparent 31%),linear-gradient(135deg,#061313,#102d2d 54%,#17140e);box-shadow:0 28px 80px rgba(0,0,0,.24);isolation:isolate}.nlp3d-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(234,216,163,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(234,216,163,.07) 1px,transparent 1px);background-size:34px 34px;opacity:.8;pointer-events:none}.nlp3d-shell{position:relative;z-index:1;display:grid;grid-template-columns:minmax(260px,.86fr) minmax(360px,1.35fr) minmax(300px,.82fr);gap:22px;min-height:680px;padding:34px}.nlp3d-copy{align-self:end;padding-bottom:22px}.nlp3d-kicker{margin:0 0 12px;color:var(--gold2);font-size:13px}.nlp3d h2{font-size:clamp(30px,4.4vw,58px);line-height:1.02;margin:0 0 18px;font-family:Georgia,"Times New Roman",serif;font-weight:500;letter-spacing:0;max-width:11ch}.nlp3d-lead-text{color:rgba(246,239,226,.84);font-size:17px;line-height:1.75;max-width:34ch;margin:0 0 18px}.nlp3d-metrics{display:grid;gap:8px;margin:18px 0}.nlp3d-metrics span{display:inline-flex;width:max-content;max-width:100%;min-height:34px;align-items:center;border:1px solid rgba(234,216,163,.22);background:rgba(255,255,255,.055);padding:7px 12px;color:#fff7e6;font-size:13px}.nlp3d-demo-note{margin:16px 0 0;color:#f1dba0;font-size:13px;line-height:1.55;border-right:2px solid var(--gold);padding-right:12px}.nlp3d-stage-wrap{position:relative;min-height:620px}.nlp3d-toolbar{position:absolute;z-index:8;top:12px;right:12px;display:flex;gap:8px;flex-wrap:wrap}.nlp3d button{font:inherit;min-width:44px;min-height:44px}.nlp3d-angle,.nlp3d-orbit{border:1px solid rgba(234,216,163,.34);background:rgba(7,24,24,.72);color:var(--ink);padding:8px 14px;cursor:pointer}.nlp3d-angle.is-active,.nlp3d-orbit.is-active{background:linear-gradient(135deg,var(--gold),#7c5e27);color:#10100c;border-color:rgba(255,255,255,.42)}.nlp3d-scene{position:absolute;inset:0;border:1px solid rgba(234,216,163,.2);background:linear-gradient(180deg,rgba(15,48,50,.4),rgba(8,18,18,.86));overflow:hidden;perspective:1100px}.nlp3d-horizon{position:absolute;inset:14% -8% auto;height:1px;background:linear-gradient(90deg,transparent,rgba(234,216,163,.32),transparent)}.nlp3d-sea{position:absolute;left:-12%;right:52%;bottom:8%;height:44%;background:linear-gradient(135deg,rgba(43,119,139,.5),rgba(7,31,42,.08));transform:skewY(-10deg)}.nlp3d-park{position:absolute;right:-8%;bottom:20%;width:56%;height:24%;background:linear-gradient(135deg,rgba(93,127,83,.26),rgba(196,161,90,.08));transform:skewY(10deg)}.nlp3d-runway{position:absolute;right:8%;left:18%;bottom:24%;height:46px;border-top:1px solid rgba(234,216,163,.18);border-bottom:1px solid rgba(234,216,163,.18);transform:rotate(-7deg);opacity:.7}.nlp3d-shadow{position:absolute;right:27%;bottom:14%;width:44%;height:10%;background:radial-gradient(ellipse,rgba(0,0,0,.44),transparent 72%);filter:blur(9px)}.nlp3d-tower{position:absolute;right:50%;bottom:118px;width:min(230px,40%);height:420px;transform-style:preserve-3d;transform:translateX(50%) rotateX(62deg) rotateZ(var(--angle,-32deg));transition:transform .55s cubic-bezier(.2,.8,.2,1)}.nlp3d-scene.is-orbit .nlp3d-tower{animation:nlp3dOrbit 14s linear infinite}.nlp3d-plate{position:absolute;right:0;left:0;height:12px;border:1px solid rgba(234,216,163,.24);background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(196,161,90,.12));box-shadow:0 3px 0 rgba(0,0,0,.16);transform:translateZ(calc(var(--i)*3px));transition:background .18s,border-color .18s,box-shadow .18s}.nlp3d-plate.has-units{background:linear-gradient(135deg,rgba(234,216,163,.34),rgba(255,255,255,.08))}.nlp3d-plate.is-active{border-color:#fff0b8;background:linear-gradient(135deg,#f4dd98,rgba(255,255,255,.2));box-shadow:0 0 0 2px rgba(234,216,163,.2),0 0 24px rgba(234,216,163,.22)}.nlp3d-plate.is-sold{opacity:.42}.nlp3d-reference{position:absolute;left:16px;bottom:16px;width:min(170px,28%);margin:0;border:1px solid rgba(234,216,163,.22);background:rgba(0,0,0,.35);padding:6px}.nlp3d-reference img{display:block;width:100%;height:auto}.nlp3d-reference figcaption{font-size:11px;color:var(--muted);margin-top:4px}.nlp3d-console{align-self:stretch;background:var(--panel);border:1px solid rgba(234,216,163,.24);backdrop-filter:blur(16px);padding:20px;display:flex;flex-direction:column;gap:16px;box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}.nlp3d-console-head{display:flex;justify-content:space-between;align-items:center;gap:12px;border-bottom:1px solid rgba(234,216,163,.16);padding-bottom:12px}.nlp3d-console-head p{font-family:Georgia,"Times New Roman",serif;font-size:22px;margin:0}.nlp3d-status-chip{border:1px solid rgba(234,216,163,.3);color:#fff3c0;padding:5px 9px;font-size:12px}.nlp3d-floor-strip{display:flex;flex-wrap:wrap;gap:8px}.nlp3d-floor{border:1px solid rgba(234,216,163,.24);background:rgba(255,255,255,.055);color:var(--ink);padding:7px 11px;cursor:pointer}.nlp3d-floor.is-active,.nlp3d-floor:hover,.nlp3d-floor:focus-visible{background:#ead8a3;color:#16140f;outline:none}.nlp3d-units{display:grid;gap:9px}.nlp3d-unit-card{width:100%;min-height:58px;text-align:right;border:1px solid rgba(234,216,163,.2);background:rgba(255,255,255,.055);color:var(--ink);padding:11px 12px;cursor:pointer}.nlp3d-unit-card strong{display:block;font-size:15px}.nlp3d-unit-card span{display:block;color:var(--muted);font-size:12px;margin-top:4px}.nlp3d-unit-card.is-active,.nlp3d-unit-card:hover,.nlp3d-unit-card:focus-visible{outline:none;border-color:#ead8a3;background:rgba(234,216,163,.18)}.nlp3d-unit-card.is-sold{opacity:.55}.nlp3d-detail{background:rgba(255,255,255,.06);border:1px solid rgba(234,216,163,.16);padding:16px}.nlp3d-selected-title{margin:0 0 12px;font-size:21px;font-family:Georgia,"Times New Roman",serif;font-weight:500}.nlp3d-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:0}.nlp3d-facts div{border-top:1px solid rgba(234,216,163,.18);padding-top:8px}.nlp3d-facts dt{font-size:12px;color:var(--muted)}.nlp3d-facts dd{margin:2px 0 0;color:#fff;font-weight:700}.nlp3d-plan{display:inline-flex;margin-top:12px;color:#ffe8a6;text-decoration:none;border-bottom:1px solid currentColor}.nlp3d-lead-form{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:auto}.nlp3d-form-title,.nlp3d-legal,.nlp3d-ok{grid-column:1/-1;margin:0}.nlp3d-form-title{font-weight:700;color:#fff}.nlp3d-lead-form input{min-height:46px;border:1px solid rgba(234,216,163,.26);background:rgba(255,255,255,.9);color:#16140f;padding:10px 12px;border-radius:0}.nlp3d-lead-form input:focus{outline:2px solid #ead8a3;outline-offset:2px}.nlp3d-actions{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:10px}.nlp3d-send{border:0;background:linear-gradient(135deg,#ead8a3,#b99043);color:#15120c;font-weight:800;padding:13px 14px;cursor:pointer;box-shadow:0 12px 28px rgba(0,0,0,.22)}.nlp3d-send-alt{background:transparent;color:#ffe8a6;border:1px solid rgba(234,216,163,.42);box-shadow:none}.nlp3d-send:hover,.nlp3d-send:focus-visible{filter:brightness(1.05);outline:2px solid rgba(255,255,255,.7);outline-offset:2px}.nlp3d-send:disabled{opacity:.55;cursor:not-allowed}.nlp3d-legal{font-size:12px;color:var(--muted);line-height:1.45}.nlp3d-ok{font-weight:700;color:#fff2b9}.nlp3d-hp{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(1px,1px,1px,1px)!important;clip-path:inset(50%)!important;white-space:nowrap!important}.nlp3d-status-available{color:#dff8dc}.nlp3d-status-reserved{color:#ffe2a7}.nlp3d-status-sold{color:#c6c6c6}@keyframes nlp3dOrbit{from{transform:translateX(50%) rotateX(62deg) rotateZ(-40deg)}to{transform:translateX(50%) rotateX(62deg) rotateZ(320deg)}}@media(max-width:1240px){.nlp3d-shell{grid-template-columns:1fr 1.2fr;min-height:auto}.nlp3d-console{grid-column:1/-1}.nlp3d-copy{align-self:start;padding-bottom:0}.nlp3d h2{max-width:16ch}.nlp3d-stage-wrap{min-height:560px}}@media(max-width:900px){.nlp3d{margin:28px 0}.nlp3d-shell{grid-template-columns:1fr;padding:22px}.nlp3d-stage-wrap{min-height:520px}.nlp3d-copy{order:1}.nlp3d-stage-wrap{order:2}.nlp3d-console{order:3}.nlp3d h2{max-width:none}.nlp3d-reference{display:none}}@media(max-width:600px){.nlp3d-shell{padding:16px;gap:16px}.nlp3d-stage-wrap{min-height:460px}.nlp3d-toolbar{position:relative;top:auto;right:auto;margin-bottom:10px}.nlp3d-scene{position:relative;height:430px}.nlp3d-tower{width:210px;height:360px;bottom:92px}.nlp3d-facts,.nlp3d-lead-form,.nlp3d-actions{grid-template-columns:1fr}.nlp3d h2{font-size:32px}.nlp3d-lead-text{font-size:15px}.nlp3d-console{padding:16px}.nlp3d-floor{padding:8px 10px}.nlp3d-actions .nlp3d-send{width:100%}}@media(max-width:390px){.nlp3d-shell{padding:14px}.nlp3d-scene{height:400px}.nlp3d-tower{width:190px;height:330px}.nlp3d-toolbar{gap:6px}.nlp3d-angle,.nlp3d-orbit{padding:7px 10px}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_experience_css' ) ) {
	function nadlan_p3d_experience_css() {
		return <<<'CSS'
.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:min(1180px,calc(100vw - 48px));max-width:none;margin-block:22px 38px;margin-inline:calc(50% - min(590px,calc(50vw - 24px)));border-radius:28px}.nlp3d{border:1px solid rgba(234,216,163,.2)}.nlp3d-shop-path{display:grid;grid-template-columns:1fr;gap:7px;margin:16px 0 0}.nlp3d-shop-path span{display:flex;align-items:center;min-height:34px;width:max-content;max-width:100%;padding:6px 11px;border:1px solid rgba(234,216,163,.2);background:rgba(255,255,255,.06);color:#fff3d0;font-size:12.5px}.nlp3d-tools{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin-top:14px}.nlp3d-tool{border:1px solid rgba(234,216,163,.24);background:rgba(255,255,255,.06);color:#ffe8a6;padding:8px 10px;cursor:pointer}.nlp3d-tool.is-active,.nlp3d-tool:hover,.nlp3d-tool:focus-visible{background:rgba(234,216,163,.2);color:#fff;outline:2px solid rgba(234,216,163,.42);outline-offset:2px}.nlp3d-tool-panel{margin-top:10px;border:1px solid rgba(234,216,163,.16);background:rgba(0,0,0,.18);padding:12px 13px;color:#f7edd2;line-height:1.55}.nlp3d-tool-panel strong{display:block;color:#fff3bd;margin-bottom:4px}.nlp3d-tool-panel p{margin:0;font-size:13px}.nlp3d-lead-form select{min-height:46px;border:1px solid rgba(234,216,163,.26);background:rgba(255,255,255,.9);color:#16140f;padding:10px 12px;border-radius:0;font:inherit}.nlp3d-lead-form select:focus{outline:2px solid #ead8a3;outline-offset:2px}.nlp3d-send-alt{font-weight:800}@media(max-width:900px){.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:min(100%,calc(100vw - 28px));margin-inline:calc(50% - min(50%,calc(50vw - 14px)));border-radius:22px}.nlp3d-shop-path{grid-template-columns:repeat(2,minmax(0,1fr))}.nlp3d-shop-path span{width:100%}}@media(max-width:600px){.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:calc(100vw - 22px);margin-inline:calc(50% - 50vw + 11px);margin-block:18px 30px;border-radius:18px}.nlp3d-tools{grid-template-columns:1fr}.nlp3d-shop-path{grid-template-columns:1fr}.nlp3d-tool-panel{font-size:13px}.nlp3d-lead-form select{width:100%}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_flagship_css' ) ) {
	function nadlan_p3d_flagship_css() {
		return <<<'CSS'
.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:min(1380px,calc(100vw - 32px));margin-inline:calc(50% - min(690px,calc(50vw - 16px)));border-radius:30px;background:radial-gradient(circle at 72% 8%,rgba(234,216,163,.18),transparent 24%),radial-gradient(circle at 18% 18%,rgba(55,139,142,.38),transparent 30%),linear-gradient(135deg,#061313,#102d2d 54%,#17140e)}.nlp3d:before{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.06),transparent 28%,rgba(234,216,163,.08) 62%,transparent 76%);pointer-events:none}.nlp3d-shell{grid-template-columns:minmax(260px,.86fr) minmax(560px,1.35fr) minmax(360px,.96fr);grid-template-areas:"copy stage console";gap:24px}.nlp3d-copy{grid-area:copy}.nlp3d-stage-wrap{grid-area:stage;min-height:820px}.nlp3d-console{grid-area:console;background:linear-gradient(180deg,rgba(7,15,16,.84),rgba(7,15,16,.68));box-shadow:inset 0 1px 0 rgba(255,255,255,.1),0 18px 46px rgba(0,0,0,.18)}.nlp3d-viewframe{min-height:clamp(320px,30vw,480px);border-color:rgba(234,216,163,.42);background:radial-gradient(circle at 18% 20%,rgba(255,255,255,.18),transparent 24%),linear-gradient(135deg,rgba(31,91,108,.72),rgba(7,20,22,.94));box-shadow:0 24px 62px rgba(0,0,0,.36)}.nlp3d-view-map[hidden]{display:none!important}.nlp3d-viewframe:not([hidden]) .nlp3d-view-map{display:block!important;position:absolute;inset:0;width:100%!important;height:100%!important;min-height:100%;z-index:2}.nlp3d-viewframe:not([hidden]) .mapboxgl-canvas-container,.nlp3d-viewframe:not([hidden]) .mapboxgl-canvas{width:100%!important;height:100%!important}.nlp3d-viewframe:not([hidden]) .mapboxgl-control-container{position:absolute;inset:0;z-index:5;pointer-events:none}.nlp3d-viewframe:not([hidden]) .mapboxgl-control-container *{pointer-events:auto}.nlp3d-view-badge{border-radius:999px}.nlp3d-showcase{position:relative;z-index:1;display:grid;grid-template-columns:minmax(260px,.82fr) minmax(420px,1.1fr) minmax(320px,.86fr);gap:18px;padding:0 28px 30px;align-items:stretch}.nlp3d-showcase-copy,.nlp3d-showcase-cards,.nlp3d-owner-form{border:1px solid rgba(234,216,163,.22);background:linear-gradient(135deg,rgba(255,255,255,.085),rgba(255,255,255,.035));box-shadow:inset 0 1px 0 rgba(255,255,255,.07);backdrop-filter:blur(14px)}.nlp3d-showcase-copy{padding:22px}.nlp3d-showcase-copy h3{margin:0 0 12px;font-family:Georgia,"Times New Roman",serif;font-size:clamp(24px,2.4vw,38px);font-weight:500;line-height:1.15;color:#fff7df}.nlp3d-showcase-copy p:last-child{margin:0;color:#f5ead0;line-height:1.75}.nlp3d-showcase-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;padding:1px;background:rgba(234,216,163,.18)}.nlp3d-showcase-cards article{padding:18px;background:rgba(7,21,21,.82)}.nlp3d-showcase-cards span{display:block;color:#c4a15a;font-family:Georgia,"Times New Roman",serif;font-size:21px;margin-bottom:10px}.nlp3d-showcase-cards strong{display:block;color:#fff3c8;font-size:16px;margin-bottom:8px}.nlp3d-showcase-cards p{margin:0;color:#d8ccb0;font-size:13px;line-height:1.55}.nlp3d-owner-form{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:20px}.nlp3d-owner-form>div{grid-column:1/-1}.nlp3d-owner-title{margin:0 0 6px;font-family:Georgia,"Times New Roman",serif;font-size:25px;color:#fff7df}.nlp3d-owner-form p{margin:0;color:#e9ddc2;line-height:1.55}.nlp3d-owner-form input{min-height:46px;border:1px solid rgba(234,216,163,.24);background:rgba(255,255,255,.93);color:#15120c;padding:10px 12px;font:inherit;min-width:0}.nlp3d-owner-form button{grid-column:1/-1;border:0;background:linear-gradient(135deg,#ead8a3,#b99043);color:#15120c;font-weight:800;min-height:48px;cursor:pointer}.nlp3d-owner-form button:hover,.nlp3d-owner-form button:focus-visible{filter:brightness(1.05);outline:2px solid rgba(255,255,255,.7);outline-offset:2px}.nlp3d-owner-ok{grid-column:1/-1;margin:0;color:#fff2b9;font-weight:700}.nlp3d-owner-form input:disabled,.nlp3d-owner-form button:disabled{opacity:.68}@media(max-width:1240px){.nlp3d-shell{grid-template-columns:1fr 1.15fr;grid-template-areas:"copy stage" "console console"}.nlp3d-console{display:grid;grid-template-columns:minmax(260px,.72fr) minmax(420px,1fr);align-items:start}.nlp3d-showcase{grid-template-columns:1fr 1fr}.nlp3d-owner-form{grid-column:1/-1}}@media(max-width:760px){.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:calc(100vw - 18px);margin-inline:calc(50% - 50vw + 9px);border-radius:20px}.nlp3d-shell{grid-template-columns:1fr;grid-template-areas:"copy" "stage" "console"}.nlp3d-stage-wrap{min-height:600px}.nlp3d-console{display:flex}.nlp3d-viewframe{min-height:330px}.nlp3d-showcase{grid-template-columns:1fr;padding:0 16px 20px}.nlp3d-showcase-cards{grid-template-columns:1fr}.nlp3d-owner-form{grid-template-columns:1fr}.nlp3d h2{font-size:clamp(31px,9vw,46px)}}@media(max-width:420px){.nlp3d-viewframe{min-height:280px}.nlp3d-showcase-copy,.nlp3d-owner-form{padding:16px}.nlp3d-showcase-cards article{padding:15px}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_stability_css' ) ) {
	function nadlan_p3d_stability_css() {
		return <<<'CSS'
@media(max-width:1411px){.nlp3d.nlp3d-premium{width:calc(100vw - 32px)!important;max-width:none!important;margin-left:calc(50% - 50vw + 16px)!important;margin-right:calc(50% - 50vw + 16px)!important}}@media(min-width:1412px){.nlp3d.nlp3d-premium{width:1380px!important;max-width:1380px!important;margin-left:calc(50% - 690px)!important;margin-right:calc(50% - 690px)!important}}.nlp3d.nlp3d-premium{margin-block:24px 46px!important;border-radius:30px!important;overflow:hidden!important}.nlp3d.nlp3d-premium .nlp3d-shell{grid-template-columns:minmax(230px,.78fr) minmax(520px,1.24fr) minmax(320px,.92fr)!important;grid-template-areas:"copy stage console"!important;gap:18px!important;padding:28px!important;align-items:start!important}.nlp3d.nlp3d-premium .nlp3d-copy,.nlp3d.nlp3d-premium .nlp3d-stage-wrap,.nlp3d.nlp3d-premium .nlp3d-console{min-width:0!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{position:relative!important;min-height:min(820px,68vw)!important;overflow:hidden!important;isolation:isolate!important}.nlp3d.nlp3d-premium .nlp3d-console{max-height:min(820px,68vw)!important;overflow:auto!important;overscroll-behavior:contain;align-self:start!important}.nlp3d.nlp3d-premium .nlp3d-detail,.nlp3d.nlp3d-premium .nlp3d-lead-form,.nlp3d.nlp3d-premium .nlp3d-selection-dock{width:100%!important;max-width:100%!important}.nlp3d.nlp3d-premium .nlp3d-stage-viewframe{position:absolute!important;inset:0!important;z-index:12!important;width:100%!important;height:100%!important;min-height:0!important;margin:0!important;contain:layout paint;isolation:isolate;border:1px solid rgba(234,216,163,.42)!important;background:radial-gradient(circle at 18% 20%,rgba(255,255,255,.16),transparent 24%),linear-gradient(135deg,rgba(31,91,108,.72),rgba(7,20,22,.96))!important;box-shadow:0 24px 62px rgba(0,0,0,.36)!important}.nlp3d.nlp3d-premium .nlp3d-stage-viewframe[hidden]{display:none!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap.is-live-view .nlp3d-scene{opacity:0!important;pointer-events:none!important}.nlp3d.nlp3d-premium .nlp3d-stage-viewframe .nlp3d-view-map,.nlp3d.nlp3d-premium .nlp3d-stage-viewframe .mapboxgl-map,.nlp3d.nlp3d-premium .nlp3d-stage-viewframe .mapboxgl-canvas-container,.nlp3d.nlp3d-premium .nlp3d-stage-viewframe .mapboxgl-canvas{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;max-width:100%!important}.nlp3d.nlp3d-premium .nlp3d-stage-return{position:absolute;z-index:6;top:14px;left:62px;border:1px solid rgba(234,216,163,.42);background:rgba(7,15,16,.78);color:#ffe8a6;min-height:40px;padding:8px 13px;font-weight:800;cursor:pointer;backdrop-filter:blur(12px)}.nlp3d.nlp3d-premium .nlp3d-stage-return:hover,.nlp3d.nlp3d-premium .nlp3d-stage-return:focus-visible{outline:2px solid rgba(255,255,255,.68);outline-offset:2px;background:rgba(234,216,163,.18)}.nlp3d-map-error{position:absolute;inset:0;z-index:3;display:grid;place-items:center;text-align:center;padding:22px;color:#fff3c8;background:linear-gradient(135deg,rgba(7,20,22,.92),rgba(17,14,8,.86));font-size:14px;line-height:1.6}.nlp3d.nlp3d-premium .nlp3d-facade{inset:46px 6% 42px!important}.nlp3d.nlp3d-premium .nlp3d-facade img{max-width:100%;max-height:100%;object-fit:contain!important}.nlp3d.nlp3d-premium .nlp3d-tower{height:min(520px,58vw);bottom:92px;filter:drop-shadow(0 26px 32px rgba(0,0,0,.34))}.nlp3d.nlp3d-premium .nlp3d-tower:before{content:"";position:absolute;left:4%;right:4%;bottom:-44px;height:54px;border:1px solid rgba(234,216,163,.28);background:linear-gradient(180deg,rgba(234,216,163,.15),rgba(12,30,30,.72));box-shadow:inset 0 1px 0 rgba(255,255,255,.12);transform:translateZ(18px) skewX(-8deg)}.nlp3d.nlp3d-premium .nlp3d-tower:after{content:"";position:absolute;left:15%;right:15%;top:-28px;height:30px;border:1px solid rgba(234,216,163,.34);background:linear-gradient(90deg,rgba(234,216,163,.18),rgba(255,255,255,.08),rgba(234,216,163,.12));box-shadow:0 0 22px rgba(234,216,163,.12);transform:translateZ(80px) skewX(-6deg)}.nlp3d.nlp3d-premium .nlp3d-plate{height:13px;border-color:rgba(234,216,163,.34);box-shadow:inset 1px 0 rgba(255,255,255,.18),inset -1px 0 rgba(234,216,163,.22),0 4px 10px rgba(0,0,0,.25)}.nlp3d.nlp3d-premium .nlp3d-plate:after{opacity:.72!important;background:repeating-linear-gradient(90deg,rgba(234,216,163,.72) 0 5px,rgba(255,255,255,.18) 5px 7px,transparent 7px 13px)!important}.nlp3d.nlp3d-premium .nlp3d-plate:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(255,255,255,.28),transparent 18%,transparent 76%,rgba(234,216,163,.24));pointer-events:none}.nlp3d.nlp3d-premium .nlp3d-floor-strip{max-height:156px;overflow:auto;padding-inline-end:3px}.nlp3d.nlp3d-premium .nlp3d-units{max-height:260px;overflow:auto;padding-inline-end:3px}@media(max-width:1180px){.nlp3d.nlp3d-premium{width:calc(100vw - 26px)!important;margin-left:calc(50% - 50vw + 13px)!important;margin-right:calc(50% - 50vw + 13px)!important}.nlp3d.nlp3d-premium .nlp3d-shell{grid-template-columns:1fr minmax(420px,.95fr)!important;grid-template-areas:"copy stage" "console console"!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:620px!important}.nlp3d.nlp3d-premium .nlp3d-console{display:grid!important;grid-template-columns:minmax(240px,.72fr) minmax(360px,1fr)!important;max-height:none!important;overflow:visible!important}.nlp3d.nlp3d-premium .nlp3d-selection-dock,.nlp3d.nlp3d-premium .nlp3d-console-head,.nlp3d.nlp3d-premium .nlp3d-floor-strip,.nlp3d.nlp3d-premium .nlp3d-units{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-detail,.nlp3d.nlp3d-premium .nlp3d-lead-form{grid-column:2!important}}@media(max-width:760px){.nlp3d.nlp3d-premium{width:calc(100vw - 16px)!important;margin-left:calc(50% - 50vw + 8px)!important;margin-right:calc(50% - 50vw + 8px)!important;border-radius:20px!important}.nlp3d.nlp3d-premium .nlp3d-shell{display:grid!important;grid-template-columns:1fr!important;grid-template-areas:"copy" "stage" "console"!important;padding:14px!important;gap:14px!important}.nlp3d.nlp3d-premium .nlp3d-copy{grid-area:copy!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{grid-area:stage!important;min-height:540px!important}.nlp3d.nlp3d-premium .nlp3d-console{grid-area:console!important;display:flex!important;max-height:none!important;overflow:visible!important}.nlp3d.nlp3d-premium .nlp3d-scene{height:540px!important}.nlp3d.nlp3d-premium .nlp3d-facade{inset:58px 4% 42px!important}.nlp3d.nlp3d-premium .nlp3d-stage-viewframe{min-height:0!important}.nlp3d.nlp3d-premium .nlp3d-floor-strip,.nlp3d.nlp3d-premium .nlp3d-units{max-height:none!important;overflow:visible!important}.nlp3d.nlp3d-premium .nlp3d-showcase{padding:0 14px 18px!important}}@media(max-width:420px){.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:500px!important}.nlp3d.nlp3d-premium .nlp3d-scene{height:500px!important}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_app_selector_css' ) ) {
	function nadlan_p3d_app_selector_css() {
		return <<<'CSS'
.nlp3d.nlp3d-premium{--stage-glow:rgba(234,216,163,.26);--stage-shadow:rgba(0,0,0,.42)}.nlp3d.nlp3d-premium .nlp3d-shell{grid-template-columns:minmax(640px,1fr) minmax(330px,.46fr)!important;grid-template-areas:"copy copy" "stage console"!important;align-items:start!important;gap:18px!important}.nlp3d.nlp3d-premium .nlp3d-copy{display:grid!important;grid-template-columns:minmax(0,1.2fr) minmax(310px,.8fr)!important;gap:12px 22px!important;align-items:end!important;padding:0!important}.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-kicker,.nlp3d.nlp3d-premium .nlp3d-copy h2,.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-lead-text{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-shop-path,.nlp3d.nlp3d-premium .nlp3d-metrics,.nlp3d.nlp3d-premium .nlp3d-demo-note{grid-column:2!important}.nlp3d.nlp3d-premium .nlp3d-shop-path{grid-template-columns:repeat(2,minmax(0,1fr))!important;margin:0!important}.nlp3d.nlp3d-premium .nlp3d-shop-path span{width:100%!important;min-height:32px!important}.nlp3d.nlp3d-premium .nlp3d-metrics{display:flex!important;flex-wrap:wrap!important;gap:8px!important;margin:8px 0 0!important}.nlp3d.nlp3d-premium .nlp3d-metrics span{width:auto!important}.nlp3d.nlp3d-premium h2{max-width:22ch!important;font-size:clamp(32px,3.2vw,52px)!important}.nlp3d.nlp3d-premium .nlp3d-lead-text{max-width:68ch!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:min(760px,62vw)!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap:not(.is-live-view) .nlp3d-stage-viewframe{display:none!important}.nlp3d.nlp3d-premium .nlp3d-stage-card{position:absolute;z-index:11;right:18px;bottom:18px;width:min(382px,calc(100% - 36px));padding:16px;border:1px solid rgba(234,216,163,.36);background:linear-gradient(145deg,rgba(8,20,20,.86),rgba(7,13,12,.72));box-shadow:0 22px 48px var(--stage-shadow),inset 0 1px 0 rgba(255,255,255,.1);backdrop-filter:blur(18px);display:grid;gap:9px;color:#fff7df}.nlp3d.nlp3d-premium .nlp3d-stage-wrap.is-live-view .nlp3d-stage-card{display:none!important}.nlp3d.nlp3d-premium .nlp3d-stage-kicker{color:#c4a15a;font-size:12px;font-weight:800;letter-spacing:.04em}.nlp3d.nlp3d-premium .nlp3d-stage-card-title{font-family:Georgia,"Times New Roman",serif;font-size:clamp(22px,2vw,30px);font-weight:500;line-height:1.12}.nlp3d.nlp3d-premium .nlp3d-stage-card-meta{color:#dfd2b6;line-height:1.45;font-size:13px}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats span{min-height:44px;border:1px solid rgba(234,216,163,.2);background:rgba(255,255,255,.055);display:flex;align-items:center;justify-content:center;text-align:center;padding:6px 8px;color:#fff3c8;font-size:12px;line-height:1.25}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats span[data-kind="estimate"]{border-color:rgba(234,216,163,.42);background:linear-gradient(135deg,rgba(234,216,163,.2),rgba(255,255,255,.06));color:#fff8dc}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats span[data-kind="estimate"]:after{content:"לא מחייב";display:inline-flex;margin-inline-start:5px;font-size:10px;color:#d8ccb0}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button{border:1px solid rgba(234,216,163,.36);background:rgba(255,255,255,.06);color:#ffe8a6;font-weight:800;min-height:42px;cursor:pointer}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions .nlp3d-stage-inquiry{border:0;background:linear-gradient(135deg,#ead8a3,#b99043);color:#15120c}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button:hover,.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button:focus-visible{outline:2px solid rgba(255,255,255,.68);outline-offset:2px;filter:brightness(1.06)}.nlp3d.nlp3d-premium .nlp3d-console,.nlp3d.nlp3d-premium .nlp3d-floor-strip,.nlp3d.nlp3d-premium .nlp3d-units,.nlp3d.nlp3d-premium .nlp3d-facts,.nlp3d.nlp3d-premium .nlp3d-tool-panel{max-height:none!important;overflow:visible!important;scrollbar-width:none!important}.nlp3d.nlp3d-premium .nlp3d-console::-webkit-scrollbar,.nlp3d.nlp3d-premium .nlp3d-floor-strip::-webkit-scrollbar,.nlp3d.nlp3d-premium .nlp3d-units::-webkit-scrollbar,.nlp3d.nlp3d-premium .nlp3d-facts::-webkit-scrollbar,.nlp3d.nlp3d-premium .nlp3d-tool-panel::-webkit-scrollbar{display:none!important}.nlp3d.nlp3d-premium .nlp3d-console{align-self:start!important;overflow:visible!important}.nlp3d.nlp3d-premium .nlp3d-floor-strip{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important}.nlp3d.nlp3d-premium .nlp3d-floor{width:100%!important}.nlp3d.nlp3d-premium .nlp3d-tool-panel{min-height:126px}.nlp3d.nlp3d-premium .nlp3d-facade{border:0!important;background:transparent!important;box-shadow:none!important;inset:58px 4% 74px!important}.nlp3d.nlp3d-premium .nlp3d-facade img{filter:drop-shadow(0 22px 42px rgba(0,0,0,.48)) saturate(.94) contrast(1.08)!important}.nlp3d.nlp3d-premium .nlp3d-facade figcaption{right:auto!important;left:14px!important;bottom:14px!important;width:max-content;max-width:calc(100% - 28px);padding:5px 8px;border:1px solid rgba(234,216,163,.24);background:rgba(7,15,16,.68);backdrop-filter:blur(10px)}.nlp3d.nlp3d-premium .nlp3d-scene.has-facade .nlp3d-tower{opacity:.28!important}.nlp3d.nlp3d-premium .nlp3d-plate{border-radius:3px!important}.nlp3d.nlp3d-premium .nlp3d-plate.has-units:before{background:linear-gradient(90deg,rgba(255,255,255,.34),transparent 18%,transparent 76%,rgba(234,216,163,.3))!important}.nlp3d.nlp3d-premium .nlp3d-plate-label{position:absolute;right:-46px;top:-5px;min-width:34px;color:#ffe9ad;font-size:11px;text-align:left;opacity:.72;transform:rotateZ(calc(var(--angle, -32deg) * -1));pointer-events:none}.nlp3d.nlp3d-premium .nlp3d-plate:not(.is-active):not(:hover) .nlp3d-plate-label{opacity:.32}.nlp3d.nlp3d-premium .nlp3d-plate-dot{position:absolute;left:10px;top:50%;width:7px;height:7px;border-radius:999px;background:#ead8a3;box-shadow:0 0 12px var(--stage-glow);transform:translateY(-50%)}.nlp3d.nlp3d-premium .nlp3d-scene{touch-action:none!important;overscroll-behavior:contain;background:radial-gradient(circle at 50% 22%,rgba(234,216,163,.1),transparent 30%),linear-gradient(180deg,rgba(15,48,50,.48),rgba(8,18,18,.9))!important}.nlp3d.nlp3d-premium .nlp3d-scene.is-zoomed .nlp3d-tower,.nlp3d.nlp3d-premium .nlp3d-scene.is-zoomed .nlp3d-facade{filter:drop-shadow(0 30px 54px rgba(0,0,0,.5)) saturate(1.04)}@media(max-width:1180px){.nlp3d.nlp3d-premium .nlp3d-shell{grid-template-columns:1fr!important;grid-template-areas:"copy" "stage" "console"!important}.nlp3d.nlp3d-premium .nlp3d-copy{grid-template-columns:1fr!important}.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-kicker,.nlp3d.nlp3d-premium .nlp3d-copy h2,.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-lead-text,.nlp3d.nlp3d-premium .nlp3d-shop-path,.nlp3d.nlp3d-premium .nlp3d-metrics,.nlp3d.nlp3d-premium .nlp3d-demo-note{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:640px!important}.nlp3d.nlp3d-premium .nlp3d-console{display:grid!important;grid-template-columns:minmax(250px,.68fr) minmax(380px,1fr)!important;gap:14px!important}.nlp3d.nlp3d-premium .nlp3d-selection-dock,.nlp3d.nlp3d-premium .nlp3d-console-head,.nlp3d.nlp3d-premium .nlp3d-floor-strip,.nlp3d.nlp3d-premium .nlp3d-units{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-detail,.nlp3d.nlp3d-premium .nlp3d-lead-form,.nlp3d.nlp3d-premium .nlp3d-compare-tray{grid-column:2!important}}@media(max-width:760px){.nlp3d.nlp3d-premium .nlp3d-shell{padding:12px!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:560px!important}.nlp3d.nlp3d-premium .nlp3d-scene{height:560px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card{right:10px;left:10px;bottom:10px;width:auto;padding:12px}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats{grid-template-columns:1fr 1fr}.nlp3d.nlp3d-premium .nlp3d-stage-view{grid-column:1/-1}.nlp3d.nlp3d-premium .nlp3d-console{display:flex!important}.nlp3d.nlp3d-premium .nlp3d-floor-strip{grid-template-columns:repeat(2,minmax(0,1fr))!important}.nlp3d.nlp3d-premium .nlp3d-shop-path{grid-template-columns:1fr!important}.nlp3d.nlp3d-premium .nlp3d-facade{inset:64px 2% 138px!important}.nlp3d.nlp3d-premium .nlp3d-toolbar{z-index:13}}@media(max-width:420px){.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:520px!important}.nlp3d.nlp3d-premium .nlp3d-scene{height:520px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions{grid-template-columns:1fr}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats{grid-template-columns:1fr}.nlp3d.nlp3d-premium .nlp3d-facade{inset:68px 0 190px!important}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_showroom_css' ) ) {
	function nadlan_p3d_showroom_css() {
		return <<<'CSS'
.nlp3d.nlp3d-premium{margin-block:16px 52px!important;border-radius:28px!important;box-shadow:0 34px 96px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.08)!important}.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:min(1420px,calc(100vw - 28px))!important;margin-inline:calc(50% - min(710px,calc(50vw - 14px)))!important}.nlp3d.nlp3d-premium .nlp3d-shell{grid-template-columns:minmax(0,1fr) minmax(320px,.38fr)!important;grid-template-areas:"stage console" "copy copy"!important;gap:18px!important;padding:20px!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{grid-area:stage!important;min-height:clamp(620px,58vw,840px)!important}.nlp3d.nlp3d-premium .nlp3d-console{grid-area:console!important;max-height:clamp(620px,58vw,840px)!important;overflow-y:auto!important;overflow-x:hidden!important;padding:16px!important;overscroll-behavior:contain;scrollbar-width:thin;scrollbar-color:rgba(234,216,163,.46) rgba(255,255,255,.06)}.nlp3d.nlp3d-premium .nlp3d-console::-webkit-scrollbar{width:8px}.nlp3d.nlp3d-premium .nlp3d-console::-webkit-scrollbar-track{background:rgba(255,255,255,.05)}.nlp3d.nlp3d-premium .nlp3d-console::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#ead8a3,#8b7139);border-radius:999px}.nlp3d.nlp3d-premium .nlp3d-copy{grid-area:copy!important;display:grid!important;grid-template-columns:minmax(0,1fr) minmax(260px,.46fr)!important;gap:10px 20px!important;align-items:center!important;border-top:1px solid rgba(234,216,163,.18);padding-top:16px!important}.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-kicker,.nlp3d.nlp3d-premium .nlp3d-copy h2,.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-lead-text{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-copy h2{font-size:clamp(28px,3vw,44px)!important;max-width:30ch!important;margin-bottom:8px!important}.nlp3d.nlp3d-premium .nlp3d-lead-text{font-size:15px!important;line-height:1.65!important;margin-bottom:0!important;max-width:76ch!important}.nlp3d.nlp3d-premium .nlp3d-shop-path,.nlp3d.nlp3d-premium .nlp3d-metrics,.nlp3d.nlp3d-premium .nlp3d-demo-note{grid-column:2!important}.nlp3d.nlp3d-premium .nlp3d-demo-note{font-size:12px!important;margin:4px 0 0!important}.nlp3d.nlp3d-premium .nlp3d-stage-card{right:14px!important;left:14px!important;bottom:14px!important;width:auto!important;display:grid!important;grid-template-columns:minmax(190px,1.2fr) minmax(240px,.9fr) minmax(210px,.8fr)!important;gap:9px 12px!important;align-items:center!important;padding:12px 14px!important}.nlp3d.nlp3d-premium .nlp3d-stage-kicker{display:none!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-title,.nlp3d.nlp3d-premium .nlp3d-stage-card-meta{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-title{font-size:clamp(20px,1.8vw,28px)!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats{grid-column:2!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions{grid-column:3!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button{min-height:44px!important}.nlp3d.nlp3d-premium .nlp3d-toolbar{max-width:calc(100% - 24px)}.nlp3d.nlp3d-premium .nlp3d-facade{inset:54px 3.5% 104px!important}.nlp3d.nlp3d-premium .nlp3d-facade figcaption{bottom:62px!important}.nlp3d.nlp3d-premium .nlp3d-tower{bottom:150px!important;height:min(570px,54vw)!important}.nlp3d.nlp3d-premium .nlp3d-plate{height:14px!important}.nlp3d.nlp3d-premium .nlp3d-floor,.nlp3d.nlp3d-premium .nlp3d-unit-card,.nlp3d.nlp3d-premium .nlp3d-tool,.nlp3d.nlp3d-premium .nlp3d-compare-add,.nlp3d.nlp3d-premium .nlp3d-lead-form input{border-radius:10px!important}.nlp3d.nlp3d-premium .nlp3d-viewframe{position:absolute!important;inset:0!important}.nlp3d.nlp3d-premium .nlp3d-stage-return{left:70px!important}.nlp3d.nlp3d-premium .nlp3d-showcase{padding-top:6px!important}@media(max-width:1100px){.nlp3d.nlp3d-premium .nlp3d-shell{grid-template-columns:1fr!important;grid-template-areas:"stage" "console" "copy"!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:640px!important}.nlp3d.nlp3d-premium .nlp3d-console{display:grid!important;grid-template-columns:minmax(230px,.62fr) minmax(360px,1fr)!important;gap:14px!important;max-height:780px!important}.nlp3d.nlp3d-premium .nlp3d-selection-dock,.nlp3d.nlp3d-premium .nlp3d-console-head,.nlp3d.nlp3d-premium .nlp3d-floor-strip,.nlp3d.nlp3d-premium .nlp3d-units{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-detail,.nlp3d.nlp3d-premium .nlp3d-lead-form,.nlp3d.nlp3d-premium .nlp3d-compare-tray{grid-column:2!important}.nlp3d.nlp3d-premium .nlp3d-copy{grid-template-columns:1fr!important}.nlp3d.nlp3d-premium .nlp3d-shop-path,.nlp3d.nlp3d-premium .nlp3d-metrics,.nlp3d.nlp3d-premium .nlp3d-demo-note{grid-column:1!important}}@media(max-width:760px){.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:calc(100vw - 14px)!important;margin-inline:calc(50% - 50vw + 7px)!important}.nlp3d.nlp3d-premium{border-radius:18px!important}.nlp3d.nlp3d-premium .nlp3d-shell{padding:10px!important;gap:12px!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:min(640px,128vw)!important}.nlp3d.nlp3d-premium .nlp3d-scene{height:min(620px,126vw)!important}.nlp3d.nlp3d-premium .nlp3d-toolbar{right:8px!important;left:8px!important;top:8px!important;gap:6px!important}.nlp3d.nlp3d-premium .nlp3d-angle,.nlp3d.nlp3d-premium .nlp3d-orbit{padding:7px 9px!important;font-size:12px!important}.nlp3d.nlp3d-premium .nlp3d-drag-note{font-size:11px!important;min-height:24px!important}.nlp3d.nlp3d-premium .nlp3d-facade{inset:58px 1% 190px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card{right:8px!important;left:8px!important;bottom:8px!important;grid-template-columns:1fr!important;max-height:180px!important;overflow:hidden!important;padding:10px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-meta{font-size:12px!important;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats,.nlp3d.nlp3d-premium .nlp3d-stage-card-actions{grid-column:1!important;grid-template-columns:repeat(3,minmax(0,1fr))!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats span{min-height:36px!important;font-size:11px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button{min-height:40px!important;font-size:12px!important}.nlp3d.nlp3d-premium .nlp3d-console{display:flex!important;padding:12px!important;max-height:760px!important;overflow-y:auto!important;overflow-x:hidden!important}.nlp3d.nlp3d-premium .nlp3d-copy h2{font-size:28px!important;line-height:1.18!important}.nlp3d.nlp3d-premium .nlp3d-copy,.nlp3d.nlp3d-premium .nlp3d-copy *{max-width:100%;overflow-wrap:anywhere}.nlp3d.nlp3d-premium .nlp3d-showcase{padding-inline:10px!important}.nlp3d.nlp3d-premium .nlp3d-stage-return{left:58px!important;top:10px!important;min-height:38px!important}}@media(max-width:420px){.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:600px!important}.nlp3d.nlp3d-premium .nlp3d-scene{height:590px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card{max-height:190px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions{grid-template-columns:1fr!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats{grid-template-columns:1fr 1fr!important}.nlp3d.nlp3d-premium .nlp3d-stage-view{grid-column:1/-1!important}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_showroom_v162_css' ) ) {
	function nadlan_p3d_showroom_v162_css() {
		return <<<'CSS'
.nlp3d.nlp3d-premium{--model-zoom:1;--tilt:62deg;margin-block:12px 42px!important}.nlp3d.nlp3d-premium .nlp3d-shell{grid-template-columns:minmax(0,1fr)!important;grid-template-areas:"copy" "stage" "console"!important;gap:16px!important;padding:18px!important}.nlp3d.nlp3d-premium .nlp3d-copy{grid-area:copy!important;display:grid!important;grid-template-columns:minmax(0,1fr) minmax(260px,.42fr)!important;gap:10px 18px!important;align-items:end!important;border-top:0!important;border-bottom:1px solid rgba(234,216,163,.16);padding:0 0 14px!important}.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-kicker,.nlp3d.nlp3d-premium .nlp3d-copy h2,.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-lead-text{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-copy h2{max-width:28ch!important}.nlp3d.nlp3d-premium .nlp3d-shop-path,.nlp3d.nlp3d-premium .nlp3d-metrics,.nlp3d.nlp3d-premium .nlp3d-demo-note{grid-column:2!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{grid-area:stage!important;min-height:clamp(560px,54vw,760px)!important}.nlp3d.nlp3d-premium .nlp3d-scene{height:100%!important;min-height:inherit!important}.nlp3d.nlp3d-premium .nlp3d-console{grid-area:console!important;display:grid!important;grid-template-columns:minmax(220px,.68fr) minmax(360px,1fr) minmax(280px,.72fr)!important;gap:14px!important;max-height:none!important;overflow:visible!important;scrollbar-width:none!important;padding:16px!important}.nlp3d.nlp3d-premium .nlp3d-console::-webkit-scrollbar,.nlp3d.nlp3d-premium .nlp3d-floor-strip::-webkit-scrollbar,.nlp3d.nlp3d-premium .nlp3d-units::-webkit-scrollbar,.nlp3d.nlp3d-premium .nlp3d-facts::-webkit-scrollbar,.nlp3d.nlp3d-premium .nlp3d-tool-panel::-webkit-scrollbar{display:none!important}.nlp3d.nlp3d-premium .nlp3d-selection-dock,.nlp3d.nlp3d-premium .nlp3d-console-head,.nlp3d.nlp3d-premium .nlp3d-floor-strip,.nlp3d.nlp3d-premium .nlp3d-units{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-detail,.nlp3d.nlp3d-premium .nlp3d-compare-tray{grid-column:2!important}.nlp3d.nlp3d-premium .nlp3d-lead-form{grid-column:3!important;align-self:start!important;margin-top:0!important}.nlp3d.nlp3d-premium .nlp3d-facts,.nlp3d.nlp3d-premium .nlp3d-floor-strip,.nlp3d.nlp3d-premium .nlp3d-tool-panel,.nlp3d.nlp3d-premium .nlp3d-units{max-height:none!important;overflow:visible!important}.nlp3d.nlp3d-premium .nlp3d-tools{grid-template-columns:repeat(4,minmax(0,1fr))!important}.nlp3d.nlp3d-premium .nlp3d-angle,.nlp3d.nlp3d-premium .nlp3d-orbit,.nlp3d.nlp3d-premium .nlp3d-zoom{border-radius:999px!important;border:1px solid rgba(234,216,163,.34)!important;background:rgba(7,24,24,.72)!important;color:#f6efe2!important;padding:8px 13px!important;cursor:pointer!important}.nlp3d.nlp3d-premium .nlp3d-zoom:hover,.nlp3d.nlp3d-premium .nlp3d-zoom:focus-visible{outline:2px solid rgba(255,255,255,.68);outline-offset:2px;background:rgba(234,216,163,.18)!important}.nlp3d.nlp3d-premium .nlp3d-tower{transform:translateX(50%) rotateX(var(--tilt,62deg)) rotateZ(var(--angle,-32deg)) scale(var(--model-zoom,1))!important;transform-origin:center bottom!important;will-change:transform!important}.nlp3d.nlp3d-premium .nlp3d-facade{transform:scale(var(--model-zoom,1))!important;transform-origin:center bottom!important;will-change:transform!important}.nlp3d.nlp3d-premium .nlp3d-hotspot-hit{fill:rgba(255,255,255,0);stroke:rgba(255,255,255,0);stroke-width:28;vector-effect:non-scaling-stroke;cursor:pointer;pointer-events:stroke}.nlp3d.nlp3d-premium .nlp3d-hotspot-hit:hover+.nlp3d-hotspot,.nlp3d.nlp3d-premium .nlp3d-hotspot-hit:focus-visible+.nlp3d-hotspot{fill:rgba(234,216,163,.28);stroke:#fff2ba;filter:drop-shadow(0 0 10px rgba(234,216,163,.52))}.nlp3d.nlp3d-premium .nlp3d-hotspot-hit:focus-visible{outline:none}.nlp3d.nlp3d-premium .nlp3d-stage-card:not([hidden]){right:18px!important;left:auto!important;bottom:18px!important;top:auto!important;width:min(390px,calc(100% - 36px))!important;max-height:none!important;overflow:visible!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions{grid-template-columns:repeat(3,minmax(0,1fr))!important}.nlp3d.nlp3d-premium .nlp3d-showcase{padding-top:0!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap.is-live-view .nlp3d-scene{opacity:0!important;pointer-events:none!important}.nlp3d.nlp3d-premium .nlp3d-stage-viewframe{inset:0!important}.nlp3d.nlp3d-premium .nlp3d-view-copy{unicode-bidi:plaintext}@media(max-width:980px){.nlp3d.nlp3d-premium .nlp3d-console{grid-template-columns:minmax(220px,.72fr) minmax(320px,1fr)!important}.nlp3d.nlp3d-premium .nlp3d-selection-dock,.nlp3d.nlp3d-premium .nlp3d-console-head,.nlp3d.nlp3d-premium .nlp3d-floor-strip,.nlp3d.nlp3d-premium .nlp3d-units{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-detail,.nlp3d.nlp3d-premium .nlp3d-compare-tray,.nlp3d.nlp3d-premium .nlp3d-lead-form{grid-column:2!important}.nlp3d.nlp3d-premium .nlp3d-lead-form{margin-top:0!important}}@media(max-width:760px){.nlp3d.nlp3d-premium .nlp3d-shell{padding:10px!important;gap:12px!important}.nlp3d.nlp3d-premium .nlp3d-copy{grid-template-columns:1fr!important}.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-kicker,.nlp3d.nlp3d-premium .nlp3d-copy h2,.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-lead-text,.nlp3d.nlp3d-premium .nlp3d-shop-path,.nlp3d.nlp3d-premium .nlp3d-metrics,.nlp3d.nlp3d-premium .nlp3d-demo-note{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:min(590px,130vw)!important}.nlp3d.nlp3d-premium .nlp3d-scene{height:100%!important;min-height:min(560px,126vw)!important}.nlp3d.nlp3d-premium .nlp3d-console{display:grid!important;grid-template-columns:1fr!important;max-height:none!important;overflow:visible!important;padding:12px!important}.nlp3d.nlp3d-premium .nlp3d-selection-dock,.nlp3d.nlp3d-premium .nlp3d-console-head,.nlp3d.nlp3d-premium .nlp3d-floor-strip,.nlp3d.nlp3d-premium .nlp3d-units,.nlp3d.nlp3d-premium .nlp3d-detail,.nlp3d.nlp3d-premium .nlp3d-compare-tray,.nlp3d.nlp3d-premium .nlp3d-lead-form{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-tools{grid-template-columns:repeat(2,minmax(0,1fr))!important}.nlp3d.nlp3d-premium .nlp3d-toolbar{right:8px!important;left:8px!important;top:8px!important;gap:6px!important}.nlp3d.nlp3d-premium .nlp3d-angle,.nlp3d.nlp3d-premium .nlp3d-orbit,.nlp3d.nlp3d-premium .nlp3d-zoom{padding:7px 9px!important;font-size:12px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card:not([hidden]){position:relative!important;right:auto!important;left:auto!important;top:auto!important;bottom:auto!important;width:auto!important;margin-top:10px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats{grid-template-columns:1fr 1fr!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions{grid-template-columns:1fr!important}.nlp3d.nlp3d-premium .nlp3d-facade{inset:64px 1% 124px!important}}@media(max-width:420px){.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:520px!important}.nlp3d.nlp3d-premium .nlp3d-scene{min-height:500px!important}.nlp3d.nlp3d-premium .nlp3d-facade{inset:68px 0 164px!important}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_showroom_v162_mobile_card_css' ) ) {
	function nadlan_p3d_showroom_v162_mobile_card_css() {
		return <<<'CSS'
@media(max-width:760px){.nlp3d.nlp3d-premium .nlp3d-stage-wrap.has-stage-selection{min-height:min(780px,172vw)!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap.has-stage-selection .nlp3d-scene{bottom:224px!important;height:auto!important;min-height:0!important}.nlp3d.nlp3d-premium .nlp3d-stage-card:not([hidden]){position:absolute!important;right:10px!important;left:10px!important;top:auto!important;bottom:10px!important;width:auto!important;max-height:none!important;overflow:visible!important;margin-top:0!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button{min-height:44px!important}}@media(max-width:420px){.nlp3d.nlp3d-premium .nlp3d-stage-wrap.has-stage-selection{min-height:780px!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap.has-stage-selection .nlp3d-scene{bottom:250px!important}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_showroom_v162_material_css' ) ) {
	function nadlan_p3d_showroom_v162_material_css() {
		return <<<'CSS'
.nlp3d.nlp3d-premium .nlp3d-material-links{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:10px}.nlp3d.nlp3d-premium .nlp3d-material-card{position:relative;display:grid;gap:4px;min-height:62px;padding:10px 11px;border:1px solid rgba(234,216,163,.22);background:linear-gradient(135deg,rgba(255,255,255,.075),rgba(255,255,255,.035));color:#fff3c8;text-decoration:none}.nlp3d.nlp3d-premium .nlp3d-material-card strong{font-size:13px;line-height:1.3;color:#fff7df}.nlp3d.nlp3d-premium .nlp3d-material-card small{font-size:11.5px;line-height:1.35;color:#d8ccb0}.nlp3d.nlp3d-premium .nlp3d-material-card em{position:absolute;top:7px;left:8px;font-style:normal;font-size:10px;color:#15120c;background:linear-gradient(135deg,#ead8a3,#b99043);padding:2px 6px;border-radius:999px}.nlp3d.nlp3d-premium a.nlp3d-material-card:hover,.nlp3d.nlp3d-premium a.nlp3d-material-card:focus-visible{outline:2px solid rgba(255,255,255,.68);outline-offset:2px;border-color:rgba(234,216,163,.55);background:linear-gradient(135deg,rgba(234,216,163,.16),rgba(255,255,255,.05))}@media(max-width:760px){.nlp3d.nlp3d-premium .nlp3d-material-links{grid-template-columns:1fr}.nlp3d.nlp3d-premium .nlp3d-material-card{min-height:58px}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_showroom_v1621_css' ) ) {
	function nadlan_p3d_showroom_v1621_css() {
		return <<<'CSS'
/* v1.62.1: make the showroom the first product impression and keep fixed widgets away from the stage. */
.single-nadlan_project .wp-block-post-featured-image{display:none!important}.single-nadlan_project .entry-content>.nlp3d,.single-nadlan_project .wp-block-post-content>.nlp3d{margin-top:8px!important}.single-nadlan_project .nlpf{box-sizing:border-box!important;float:none!important;clear:both!important;width:min(920px,calc(100vw - 32px))!important;max-width:calc(100vw - 32px)!important;margin:34px auto!important}.nlp3d.nlp3d-premium{margin-block:10px 52px!important}.nlp3d.nlp3d-premium .nlp3d-shell{grid-template-columns:minmax(0,1fr)!important;grid-template-areas:"stage" "copy" "console"!important;gap:16px!important;padding:18px!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{grid-area:stage!important;min-height:clamp(660px,78vh,900px)!important}.nlp3d.nlp3d-premium .nlp3d-scene{height:100%!important;min-height:inherit!important}.nlp3d.nlp3d-premium .nlp3d-copy{grid-area:copy!important;display:grid!important;grid-template-columns:minmax(0,1fr) minmax(250px,.36fr)!important;gap:10px 18px!important;align-items:start!important;border-top:1px solid rgba(234,216,163,.16)!important;border-bottom:0!important;padding:16px 0 0!important}.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-kicker,.nlp3d.nlp3d-premium .nlp3d-copy h2,.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-lead-text{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-copy h2{font-size:clamp(27px,2.6vw,42px)!important;max-width:34ch!important;margin:0 0 8px!important;line-height:1.13!important}.nlp3d.nlp3d-premium .nlp3d-lead-text{font-size:14.5px!important;line-height:1.62!important;max-width:78ch!important;margin:0!important}.nlp3d.nlp3d-premium .nlp3d-shop-path,.nlp3d.nlp3d-premium .nlp3d-metrics,.nlp3d.nlp3d-premium .nlp3d-demo-note{grid-column:2!important}.nlp3d.nlp3d-premium .nlp3d-shop-path{margin:0!important}.nlp3d.nlp3d-premium .nlp3d-metrics{margin:8px 0 0!important}.nlp3d.nlp3d-premium .nlp3d-demo-note{font-size:12px!important;line-height:1.45!important;margin:4px 0 0!important}.nlp3d.nlp3d-premium .nlp3d-console{grid-area:console!important;max-height:none!important;overflow:visible!important}.nlp3d.nlp3d-premium .nlp3d-toolbar{top:14px!important;right:auto!important;left:14px!important;max-width:calc(100% - 28px)!important;justify-content:flex-start!important;z-index:14!important}.nlp3d.nlp3d-premium .nlp3d-facade{inset:50px 2.5% 72px!important}.nlp3d.nlp3d-premium .nlp3d-facade img{padding:4px!important;filter:drop-shadow(0 26px 44px rgba(0,0,0,.5)) saturate(1.02) contrast(1.08)!important}.nlp3d.nlp3d-premium .nlp3d-stage-card:not([hidden]){right:18px!important;left:auto!important;bottom:18px!important;top:auto!important;max-width:390px!important}.single-nadlan_project .entry-content>h2,.single-nadlan_project .wp-block-post-content>h2,.single-nadlan_project .entry-content>h3,.single-nadlan_project .wp-block-post-content>h3{float:none!important;clear:both!important;display:block!important;width:min(840px,calc(100vw - 36px))!important;margin:34px auto 12px!important;text-align:right!important;line-height:1.24!important;color:#1f1a13!important}.single-nadlan_project .entry-content>h2,.single-nadlan_project .wp-block-post-content>h2{font-size:clamp(26px,2.25vw,38px)!important}.single-nadlan_project .entry-content>h3,.single-nadlan_project .wp-block-post-content>h3{font-size:clamp(20px,1.7vw,27px)!important}.single-nadlan_project .entry-content>p,.single-nadlan_project .wp-block-post-content>p,.single-nadlan_project .entry-content>ul,.single-nadlan_project .wp-block-post-content>ul,.single-nadlan_project .entry-content>ol,.single-nadlan_project .wp-block-post-content>ol{float:none!important;clear:both!important;width:min(820px,calc(100vw - 36px))!important;margin:0 auto 16px!important;text-align:right!important;line-height:1.82!important}.single-nadlan_project .entry-content>.wp-block-table,.single-nadlan_project .wp-block-post-content>.wp-block-table,.single-nadlan_project .entry-content>table,.single-nadlan_project .wp-block-post-content>table{float:none!important;clear:both!important;width:min(920px,calc(100vw - 36px))!important;margin:22px auto!important}.single-nadlan_project .nlfab{right:auto!important;left:18px!important;bottom:18px!important;top:auto!important;z-index:8880!important}.single-nadlan_project #nla-btn{right:auto!important;left:18px!important;bottom:207px!important;top:auto!important;z-index:8890!important}.single-nadlan_project #nlai{right:auto!important;left:18px!important;bottom:273px!important;top:auto!important;z-index:8885!important}@media(max-width:760px){.nlp3d.nlp3d-premium{width:calc(100vw - 12px)!important;margin-left:calc(50% - 50vw + 6px)!important;margin-right:calc(50% - 50vw + 6px)!important}.nlp3d.nlp3d-premium .nlp3d-shell{grid-template-areas:"stage" "copy" "console"!important;padding:10px!important;gap:12px!important}.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:min(660px,148vw)!important}.nlp3d.nlp3d-premium .nlp3d-copy{grid-template-columns:1fr!important;padding-top:12px!important}.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-kicker,.nlp3d.nlp3d-premium .nlp3d-copy h2,.nlp3d.nlp3d-premium .nlp3d-copy .nlp3d-lead-text,.nlp3d.nlp3d-premium .nlp3d-shop-path,.nlp3d.nlp3d-premium .nlp3d-metrics,.nlp3d.nlp3d-premium .nlp3d-demo-note{grid-column:1!important}.nlp3d.nlp3d-premium .nlp3d-copy h2{font-size:27px!important}.nlp3d.nlp3d-premium .nlp3d-toolbar{right:8px!important;left:8px!important;top:8px!important;gap:6px!important}.nlp3d.nlp3d-premium .nlp3d-facade{inset:58px 0 136px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card:not([hidden]){position:relative!important;right:auto!important;left:auto!important;bottom:auto!important;top:auto!important;width:auto!important;max-width:none!important;margin-top:10px!important}.single-nadlan_project .nlfab{left:10px!important;right:auto!important;bottom:10px!important;max-width:154px!important;transform:scale(.92);transform-origin:bottom left}.single-nadlan_project #nla-btn{left:10px!important;right:auto!important;bottom:145px!important}.single-nadlan_project #nlai{left:10px!important;right:auto!important;bottom:205px!important}.single-nadlan_project .entry-content>h2,.single-nadlan_project .wp-block-post-content>h2,.single-nadlan_project .entry-content>h3,.single-nadlan_project .wp-block-post-content>h3,.single-nadlan_project .entry-content>p,.single-nadlan_project .wp-block-post-content>p,.single-nadlan_project .entry-content>ul,.single-nadlan_project .wp-block-post-content>ul,.single-nadlan_project .entry-content>ol,.single-nadlan_project .wp-block-post-content>ol{width:calc(100vw - 32px)!important}}@media(max-width:420px){.nlp3d.nlp3d-premium .nlp3d-stage-wrap{min-height:min(620px,166vw)!important}.nlp3d.nlp3d-premium .nlp3d-facade{inset:64px 0 168px!important}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_model_viewer_css' ) ) {
	function nadlan_p3d_model_viewer_css() {
		return <<<'CSS'
.nlp3d.nlp3d-premium .nlp3d-scene.has-model-viewer{background:radial-gradient(circle at 50% 24%,rgba(234,216,163,.2),transparent 34%),linear-gradient(180deg,rgba(18,66,65,.72),rgba(5,14,14,.94))!important;cursor:auto!important}.nlp3d.nlp3d-premium .nlp3d-model-viewer{position:absolute;inset:0;z-index:8;width:100%;height:100%;min-height:100%;--poster-color:transparent;background:radial-gradient(circle at 50% 36%,rgba(234,216,163,.14),transparent 38%),linear-gradient(180deg,rgba(22,76,76,.42),rgba(4,13,13,.82));outline:none}.nlp3d.nlp3d-premium.has-model-viewer-loaded .nlp3d-scene.has-model-viewer .nlp3d-horizon,.nlp3d.nlp3d-premium.has-model-viewer-loaded .nlp3d-scene.has-model-viewer .nlp3d-sea,.nlp3d.nlp3d-premium.has-model-viewer-loaded .nlp3d-scene.has-model-viewer .nlp3d-park,.nlp3d.nlp3d-premium.has-model-viewer-loaded .nlp3d-scene.has-model-viewer .nlp3d-runway,.nlp3d.nlp3d-premium.has-model-viewer-loaded .nlp3d-scene.has-model-viewer .nlp3d-shadow,.nlp3d.nlp3d-premium.has-model-viewer-loaded .nlp3d-scene.has-model-viewer .nlp3d-tower,.nlp3d.nlp3d-premium.has-model-viewer-loaded .nlp3d-scene.has-model-viewer .nlp3d-facade{opacity:0!important;pointer-events:none!important}.nlp3d.nlp3d-premium.has-model-viewer-error .nlp3d-model-viewer{opacity:.08;pointer-events:none}.nlp3d.nlp3d-premium .nlp3d-mv-hotspot{position:relative;display:inline-grid;place-items:center;width:44px;height:44px;border-radius:999px;border:1px solid rgba(234,216,163,.62);background:radial-gradient(circle at 35% 28%,#fff9dd,#d4ad5d 46%,#6d5126 100%);box-shadow:0 0 0 6px rgba(234,216,163,.12),0 12px 28px rgba(0,0,0,.34);color:#16140f;cursor:pointer;transition:transform .16s ease,box-shadow .16s ease,opacity .16s ease}.nlp3d.nlp3d-premium .nlp3d-mv-hotspot:before{content:"";width:10px;height:10px;border-radius:999px;background:#12100b;box-shadow:0 0 0 3px rgba(255,255,255,.42)}.nlp3d.nlp3d-premium .nlp3d-mv-hotspot:not([data-visible]){opacity:0;pointer-events:none}.nlp3d.nlp3d-premium .nlp3d-mv-hotspot:hover,.nlp3d.nlp3d-premium .nlp3d-mv-hotspot:focus-visible,.nlp3d.nlp3d-premium .nlp3d-mv-hotspot.is-active{transform:scale(1.08);outline:none;box-shadow:0 0 0 8px rgba(234,216,163,.2),0 18px 38px rgba(0,0,0,.42)}.nlp3d.nlp3d-premium .nlp3d-mv-hotspot.is-active{border-color:#fff4be;background:radial-gradient(circle at 35% 28%,#fff,#f3df9d 46%,#b98e3d 100%)}.nlp3d.nlp3d-premium .nlp3d-mv-label{position:absolute;inset-inline-start:36px;top:50%;transform:translateY(-50%);white-space:nowrap;max-width:190px;overflow:hidden;text-overflow:ellipsis;border:1px solid rgba(234,216,163,.28);background:rgba(6,15,15,.78);color:#fff4c7;padding:6px 9px;font-size:12px;line-height:1.2;box-shadow:0 10px 24px rgba(0,0,0,.26);backdrop-filter:blur(10px)}.nlp3d.nlp3d-premium .nlp3d-model-viewer::part(default-progress-bar){height:3px;background:linear-gradient(90deg,#ead8a3,#b99043)}@media(max-width:760px){.nlp3d.nlp3d-premium .nlp3d-mv-label{display:none}.nlp3d.nlp3d-premium .nlp3d-mv-hotspot{width:48px;height:48px}.nlp3d.nlp3d-premium .nlp3d-model-viewer{min-height:inherit}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_showroom_v1631_a11y_css' ) ) {
	function nadlan_p3d_showroom_v1631_a11y_css() {
		return <<<'CSS'
.nlp3d.nlp3d-premium .nlp3d-hotspot{pointer-events:none!important;cursor:default!important}.nlp3d.nlp3d-premium .nlp3d-hotspot-hit{fill:rgba(255,255,255,.001)!important;stroke:transparent!important;stroke-width:0!important;vector-effect:non-scaling-stroke;pointer-events:all!important;cursor:pointer!important}.nlp3d.nlp3d-premium .nlp3d-hotspot-hit:hover+.nlp3d-hotspot,.nlp3d.nlp3d-premium .nlp3d-hotspot-hit:focus-visible+.nlp3d-hotspot{fill:rgba(234,216,163,.3)!important;stroke:#fff2ba!important;filter:drop-shadow(0 0 12px rgba(234,216,163,.58))}.nlp3d.nlp3d-premium .nlp3d-hotspot-hit:focus-visible{outline:none!important;filter:drop-shadow(0 0 16px rgba(255,242,186,.72))}.nlp3d.nlp3d-premium .nlp3d-plate:not(.is-selectable){cursor:grab!important}.nlp3d.nlp3d-premium .nlp3d-plate.is-selectable{z-index:var(--i);height:44px!important;min-height:44px!important;background:transparent!important;border-color:transparent!important;box-shadow:none!important;display:flex!important;align-items:center!important;justify-content:center!important;cursor:pointer!important}.nlp3d.nlp3d-premium .nlp3d-plate.is-selectable:before{content:"";position:absolute;left:0;right:0;top:15px;height:14px;border:1px solid rgba(234,216,163,.34);border-radius:3px;background:linear-gradient(135deg,rgba(234,216,163,.34),rgba(255,255,255,.08));box-shadow:inset 1px 0 rgba(255,255,255,.18),inset -1px 0 rgba(234,216,163,.22),0 4px 10px rgba(0,0,0,.25)}.nlp3d.nlp3d-premium .nlp3d-plate.is-selectable.is-active:before{border-color:#fff0b8;background:linear-gradient(135deg,#f4dd98,rgba(255,255,255,.2));box-shadow:0 0 0 2px rgba(234,216,163,.2),0 0 24px rgba(234,216,163,.22)}.nlp3d.nlp3d-premium .nlp3d-plate.is-selectable:after{top:18px!important;height:8px!important;bottom:auto!important}.nlp3d.nlp3d-premium .nlp3d-plate-label,.nlp3d.nlp3d-premium .nlp3d-plate-dot{pointer-events:none!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button,.nlp3d.nlp3d-premium .nlp3d-dock-actions button,.nlp3d.nlp3d-premium .nlp3d-stage-return,.nlp3d.nlp3d-premium .nlp3d-overlay-close,.nlp3d.nlp3d-premium .nlp3d-tool,.nlp3d.nlp3d-premium .nlp3d-compare-add,.nlp3d.nlp3d-premium .nlp3d-compare-open,.nlp3d.nlp3d-premium .nlp3d-compare-chip,.nlp3d.nlp3d-premium .nlp3d-advisors label{min-height:44px!important}.nlp3d.nlp3d-premium .nlp3d-overlay-close{min-width:44px!important;width:44px!important;height:44px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button{padding-block:9px!important}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_showroom_v1633_contact_css' ) ) {
	function nadlan_p3d_showroom_v1633_contact_css() {
		return <<<'CSS'
body.single-nadlan_project{--nlp3d-float-left:max(12px,calc(env(safe-area-inset-left,0px) + 8px));--nlp3d-float-bottom:calc(env(safe-area-inset-bottom,0px) + 14px)}body.nadlan-p3d-stage-active.single-nadlan_project .nlfab,body.nadlan-p3d-stage-active.single-nadlan_project #nlai,body.nadlan-p3d-stage-active.single-nadlan_project #nla-btn{transition:opacity .18s ease,transform .18s ease,filter .18s ease!important;will-change:transform,opacity}body.nadlan-p3d-stage-active.single-nadlan_project .nlfab{left:var(--nlp3d-float-left)!important;right:auto!important;bottom:var(--nlp3d-float-bottom)!important;top:auto!important;width:54px!important;max-width:54px!important;display:grid!important;grid-template-columns:1fr!important;gap:8px!important;padding:0!important;background:transparent!important;box-shadow:none!important;z-index:8860!important;transform:translateX(-38px) scale(.92);opacity:.7}body.nadlan-p3d-stage-active.single-nadlan_project .nlfab:hover,body.nadlan-p3d-stage-active.single-nadlan_project .nlfab:focus-within{transform:none;opacity:1;filter:none}body.nadlan-p3d-stage-active.single-nadlan_project .nlfab-btn{position:relative!important;width:52px!important;min-width:52px!important;height:52px!important;min-height:52px!important;border-radius:999px!important;padding:0!important;display:grid!important;place-items:center!important;overflow:visible!important;border:1px solid rgba(234,216,163,.42)!important;background:linear-gradient(135deg,rgba(21,19,14,.94),rgba(46,41,30,.9))!important;color:#fff4ca!important;box-shadow:0 14px 32px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.12)!important;text-decoration:none!important}.single-nadlan_project .nlfab-wa:before{content:"WA";font-size:11px;font-weight:900;letter-spacing:.02em}.single-nadlan_project .nlfab-btn[href^="tel:"]:before{content:"TEL";font-size:10px;font-weight:900;letter-spacing:.03em}.single-nadlan_project .nlfab-btn:not(.nlfab-wa):not([href^="tel:"]):before{content:"+";font-size:17px;font-weight:900}.single-nadlan_project .nlfab-btn .dot{display:none!important}body.nadlan-p3d-stage-active.single-nadlan_project .nlfab-btn .t,body.nadlan-p3d-stage-active.single-nadlan_project #nlai .nlai-fab span{position:absolute!important;left:calc(100% + 9px)!important;right:auto!important;top:50%!important;transform:translateY(-50%) translateX(-4px)!important;white-space:nowrap!important;max-width:210px!important;overflow:hidden!important;text-overflow:ellipsis!important;border:1px solid rgba(234,216,163,.3)!important;background:rgba(9,16,15,.88)!important;color:#fff4ca!important;border-radius:999px!important;padding:7px 11px!important;font-size:12px!important;line-height:1.1!important;box-shadow:0 14px 34px rgba(0,0,0,.28)!important;opacity:0!important;pointer-events:none!important}.single-nadlan_project .nlfab-btn:hover .t,.single-nadlan_project .nlfab-btn:focus-visible .t,.single-nadlan_project #nlai .nlai-fab:hover span,.single-nadlan_project #nlai .nlai-fab:focus-visible span{opacity:1!important;transform:translateY(-50%)!important}body.nadlan-p3d-stage-active.single-nadlan_project #nlai{left:var(--nlp3d-float-left)!important;right:auto!important;bottom:calc(var(--nlp3d-float-bottom) + 188px)!important;top:auto!important;z-index:8865!important;transform:translateX(-38px) scale(.92);opacity:.7}body.nadlan-p3d-stage-active.single-nadlan_project #nlai:hover,body.nadlan-p3d-stage-active.single-nadlan_project #nlai:focus-within,body.nadlan-p3d-stage-active.single-nadlan_project #nlai:has(.nlai-panel:not([hidden])){transform:none;opacity:1}body.nadlan-p3d-stage-active.single-nadlan_project #nlai .nlai-fab{position:relative!important;width:52px!important;min-width:52px!important;height:52px!important;min-height:52px!important;border-radius:999px!important;padding:0!important;display:grid!important;place-items:center!important}body.nadlan-p3d-stage-active.single-nadlan_project #nlai .nlai-fab svg{width:22px!important;height:22px!important}body.nadlan-p3d-stage-active.single-nadlan_project #nla-btn{left:var(--nlp3d-float-left)!important;right:auto!important;bottom:calc(var(--nlp3d-float-bottom) + 126px)!important;top:auto!important;width:52px!important;min-width:52px!important;height:52px!important;min-height:52px!important;border-radius:999px!important;z-index:8870!important;transform:translateX(-38px) scale(.92);opacity:.7;box-shadow:0 14px 32px rgba(0,0,0,.3)!important}body.nadlan-p3d-stage-active.single-nadlan_project #nla-btn:hover,body.nadlan-p3d-stage-active.single-nadlan_project #nla-btn:focus-within{transform:none;opacity:1}@media(max-width:760px){body.single-nadlan_project{--nlp3d-float-left:max(10px,calc(env(safe-area-inset-left,0px) + 6px));--nlp3d-float-bottom:calc(env(safe-area-inset-bottom,0px) + 10px)}body.nadlan-p3d-stage-active.single-nadlan_project .nlfab,body.nadlan-p3d-stage-active.single-nadlan_project #nlai,body.nadlan-p3d-stage-active.single-nadlan_project #nla-btn{transform:translateX(-40px) scale(.88);opacity:.62}.single-nadlan_project .nlp3d.nlp3d-premium{scroll-margin-top:84px}.single-nadlan_project .nlp3d.nlp3d-premium .nlp3d-stage-wrap{overflow:hidden!important}.single-nadlan_project .nlp3d.nlp3d-premium .nlp3d-copy{padding-inline:2px!important}.single-nadlan_project .nlp3d.nlp3d-premium .nlp3d-shop-path{gap:6px!important}.single-nadlan_project .nlp3d.nlp3d-premium .nlp3d-shop-path span{min-width:0!important;overflow:hidden!important;text-overflow:ellipsis!important}.single-nadlan_project .nlp3d.nlp3d-premium .nlp3d-lead-text{font-size:14px!important;line-height:1.65!important}}@media(prefers-reduced-motion:reduce){body.single-nadlan_project .nlfab,body.single-nadlan_project #nlai,body.single-nadlan_project #nla-btn{transition:none!important}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_inline_js' ) ) {
	function nadlan_p3d_inline_js( $rest_url ) {
		$js = <<<'JS'
(function(){
	function readJson(node,fallback){try{return JSON.parse(node ? node.textContent : '')}catch(e){return fallback}}
	function fmt(n){return new Intl.NumberFormat('he-IL').format(n)}
	function statusLabel(status){return status==='sold'?'לא זמינה':(status==='reserved'?'בתהליך בדיקה':'זמינה לפנייה')}
	function firstAvailable(units){return units.find(function(u){return u.status!=='sold'}) || units[0] || null}
	function selectedTitle(u){if(!u){return 'בחרו דירה'}var base=u.title || ('קו '+(u.line||u.id));return base+' · קומה '+(u.floor||'-')}
	function unitText(u){var parts=[];if(u.rooms){parts.push(u.rooms+' חדרים')}if(u.sqm){parts.push(fmt(u.sqm)+' מ"ר')}if(u.view){parts.push(u.view)}return parts.join(' · ')}
	function unitPriceInfo(u,meta){
		if(!u){return {text:'לפי פנייה',kind:'none',note:''}}
		if(!meta.demo&&u.price){return {text:'₪'+fmt(u.price),kind:'official',note:u.source_note||''}}
		if(u.price_estimate){return {text:'אומדן ₪'+fmt(u.price_estimate),kind:'estimate',note:u.price_source||u.source_note||'אומדן לא מחייב'}}
		var avg=Number(meta.avg_price_per_sqm||0)||0;
		var sqm=Number(u.sqm||0)||0;
		if(avg>0&&sqm>0){return {text:'אומדן ₪'+fmt(Math.round(avg*sqm)),kind:'estimate',note:meta.price_source_note||'לפי ממוצע אזורי, לא הצעה מחייבת'}}
		return {text:'לפי פנייה',kind:'none',note:''};
	}
	function unitPriceText(u,meta){return unitPriceInfo(u,meta).text}
	function detailRows(u,meta){
		var priceInfo=unitPriceInfo(u,meta);
		var price=priceInfo.text+(priceInfo.kind==='estimate'?' · לא מחייב':'');
		var rows=[['סטטוס',statusLabel(u.status)],['בניין',u.building||'לפי פנייה'],['קו',u.line||'לפי פנייה'],['חדרים',u.rooms?u.rooms:'לפי פנייה'],['שטח',u.sqm?fmt(u.sqm)+' מ"ר':'לפי פנייה'],['מרפסת',u.balcony?fmt(u.balcony)+' מ"ר':'לפי פנייה'],['כיוון',u.dir||'לפי פנייה'],['נוף',u.view||'לפי פנייה'],['מחיר',price],['זמינות',u.availability||'לא מאומתת'],['יזם',meta.developer||'לפי פנייה']];
		if(priceInfo.kind==='estimate'&&priceInfo.note){rows.push(['הערת מחיר',priceInfo.note])}
		if(u.market_note){rows.push(['נתוני שוק',u.market_note])}
		if(u.source_note){rows.push(['מקור',u.source_note])}
		return rows;
	}
	function bearingForDirection(dir){
		dir=(dir||'').toString();
		var north=dir.indexOf('צפון')>-1,south=dir.indexOf('דרום')>-1,east=dir.indexOf('מזרח')>-1,west=dir.indexOf('מערב')>-1;
		if(north&&west){return 315} if(south&&west){return 225} if(north&&east){return 45} if(south&&east){return 135}
		if(west){return 270} if(east){return 90} if(south){return 180} return 0;
	}
	function cameraParams(u,meta){
		var floor=Math.max(1,parseInt(u&&u.floor||1,10));
		var floorHeight=Number(meta.floor_height_m||3.05)||3.05;
		var ground=Number(meta.ground_elevation_m||0)||0;
		var altitude=ground+4+((floor-1)*floorHeight)+1.55;
		return {lat:Number(meta.lat||0)||0,lng:Number(meta.lng||0)||0,bearing:bearingForDirection(u&&u.dir),altitude_m:Math.round(altitude*10)/10,floor_height_m:floorHeight};
	}
	var RAD=Math.PI/180;
	function sunPosition(date,lat,lng){
		var d=date.getTime()/86400000-0.5+2440588-2451545;
		var M=RAD*(357.5291+0.98560028*d);
		var L=M+RAD*(1.9148*Math.sin(M)+0.02*Math.sin(2*M)+0.0003*Math.sin(3*M))+RAD*102.9372+Math.PI;
		var e=RAD*23.4397;
		var dec=Math.asin(Math.sin(L)*Math.sin(e));
		var ra=Math.atan2(Math.sin(L)*Math.cos(e),Math.cos(L));
		var H=RAD*(280.16+360.9856235*d)-RAD*(-lng)-ra;
		var phi=RAD*lat;
		var elevation=Math.asin(Math.sin(phi)*Math.sin(dec)+Math.cos(phi)*Math.cos(dec)*Math.cos(H));
		var az=Math.atan2(Math.sin(H),Math.cos(H)*Math.sin(phi)-Math.tan(dec)*Math.cos(phi));
		return {elevation:elevation/RAD,bearing:((az/RAD)+180+360)%360};
	}
	function bearingDiff(a,b){var diff=Math.abs(a-b)%360;return diff>180?360-diff:diff}
	function sunWindow(lat,lng,facadeBearing,isoDay,utcOffset){
		var first=null,last=null;
		for(var m=0;m<1440;m+=10){
			var hh=Math.floor(m/60),mm=m%60;
			var date=new Date(Date.UTC(2026,isoDay[0],isoDay[1],hh-utcOffset,mm,0));
			var pos=sunPosition(date,lat,lng);
			if(pos.elevation>8&&bearingDiff(pos.bearing,facadeBearing)<70){
				if(first===null){first=m}
				last=m;
			}
		}
		function clock(m){return ('0'+Math.floor(m/60)).slice(-2)+':'+('0'+(m%60)).slice(-2)}
		if(first===null){return null}
		return {from:clock(first),to:clock(last+10>1430?1430:last+10),minutes:last-first+10};
	}
	function sunSummary(u,meta){
		var lat=Number(meta.lat||0)||0,lng=Number(meta.lng||0)||0;
		if(!lat||!lng){return null}
		var bearing=bearingForDirection(u&&u.dir);
		var summer=sunWindow(lat,lng,bearing,[5,21],3);
		var winter=sunWindow(lat,lng,bearing,[11,21],2);
		return {bearing:bearing,summer:summer,winter:winter};
	}
	var mapboxLoading=false,mapboxQueue=[];
	function loadMapboxGl(cb){
		if(window.mapboxgl){cb();return}
		mapboxQueue.push(cb);
		if(mapboxLoading){return}
		mapboxLoading=true;
		var css=document.createElement('link');
		css.rel='stylesheet';
		css.href='https://api.mapbox.com/mapbox-gl-js/v3.14.0/mapbox-gl.css';
		document.head.appendChild(css);
		var s=document.createElement('script');
		s.src='https://api.mapbox.com/mapbox-gl-js/v3.14.0/mapbox-gl.js';
		s.onload=function(){mapboxQueue.forEach(function(fn){try{fn()}catch(e){}});mapboxQueue=[]};
		s.onerror=function(){mapboxQueue=[]};
		document.head.appendChild(s);
	}
	function storageGet(key){try{return window.localStorage.getItem(key)}catch(e){return null}}
	function storageSet(key,value){try{window.localStorage.setItem(key,value)}catch(e){}}
	function init(root){
		var units=readJson(root.querySelector('.nlp3d-data'),[]);
		var meta=readJson(root.querySelector('.nlp3d-meta'),{});
		if(!Array.isArray(units)||!units.length){return}
		root.classList.add('is-model-first');
		var scene=root.querySelector('.nlp3d-scene');
		var tower=root.querySelector('.nlp3d-tower');
		var facade=root.querySelector('.nlp3d-facade');
		var hotspots=root.querySelector('.nlp3d-facade-hotspots');
		var modelViewer=root.querySelector('.nlp3d-model-viewer');
		var modelHotspots=[].slice.call(root.querySelectorAll('.nlp3d-mv-hotspot'));
		var floors=units.map(function(u){return parseInt(u.floor||0,10)}).filter(function(v,i,arr){return v>0&&arr.indexOf(v)===i}).sort(function(a,b){return b-a});
		var maxFloor=Math.max.apply(null,floors.concat([39]));
		var minFloor=Math.max(1,Math.min.apply(null,floors.concat([1])));
		var activeUnit=firstAvailable(units);
		var activeFloor=activeUnit ? parseInt(activeUnit.floor||floors[0]||maxFloor,10) : maxFloor;
		var floorStrip=root.querySelector('.nlp3d-floor-strip');
		var unitList=root.querySelector('.nlp3d-units');
		var title=root.querySelector('.nlp3d-selected-title');
		var facts=root.querySelector('.nlp3d-facts');
		var plan=root.querySelector('.nlp3d-plan');
		var form=root.querySelector('.nlp3d-lead-form');
		var ok=root.querySelector('.nlp3d-ok');
		var ownerForm=root.querySelector('.nlp3d-owner-form');
		var ownerOk=root.querySelector('.nlp3d-owner-ok');
		var viewToggle=root.querySelector('.nlp3d-view-toggle');
		var viewFrame=root.querySelector('.nlp3d-viewframe');
		var viewCopy=root.querySelector('.nlp3d-view-copy');
		var stageWrap=root.querySelector('.nlp3d-stage-wrap');
		var stageReturn=root.querySelector('.nlp3d-stage-return');
		var stageCard=root.querySelector('.nlp3d-stage-card');
		var stageCardTitle=root.querySelector('.nlp3d-stage-card-title');
		var stageCardMeta=root.querySelector('.nlp3d-stage-card-meta');
		var stageCardPrice=root.querySelector('.nlp3d-stage-price');
		var stageCardStatus=root.querySelector('.nlp3d-stage-status');
		var stageCardView=root.querySelector('.nlp3d-stage-view');
		var stageDetails=root.querySelector('.nlp3d-stage-details');
		var stageViewBtn=root.querySelector('.nlp3d-stage-view-btn');
		var stageInquiry=root.querySelector('.nlp3d-stage-inquiry');
		var detail=root.querySelector('.nlp3d-detail');
		var toolPanel=root.querySelector('.nlp3d-tool-panel');
		var toolButtons=[].slice.call(root.querySelectorAll('.nlp3d-tool'));
		var viewMap=root.querySelector('.nlp3d-view-map');
		var liveMap=null;
		var compareTray=root.querySelector('.nlp3d-compare-tray');
		var compareChips=root.querySelector('.nlp3d-compare-chips');
		var compareOverlay=root.querySelector('.nlp3d-compare-overlay');
		var compareTable=root.querySelector('.nlp3d-compare-table');
		var planOverlay=root.querySelector('.nlp3d-plan-overlay');
		var planBody=root.querySelector('.nlp3d-plan-body');
		var dealSteps=root.querySelector('.nlp3d-deal-steps');
		var wdots=[].slice.call(root.querySelectorAll('.nlp3d-wdots span'));
		var dockTitle=root.querySelector('.nlp3d-dock-title');
		var dockMeta=root.querySelector('.nlp3d-dock-meta');
		var dockSpin=root.querySelector('.nlp3d-dock-spin');
		var dockInquiry=root.querySelector('.nlp3d-dock-action');
		var storeKey='nlp3d-'+root.dataset.project;
		var compareIds=[];
		var hasStageSelection=false;
		try{compareIds=JSON.parse(storageGet(storeKey+'-compare')||'[]')||[]}catch(e){compareIds=[]}
		compareIds=compareIds.filter(function(id){return units.some(function(u){return u.id===id})}).slice(0,3);
		var savedUnit=storageGet(storeKey+'-unit');
		var currentAngle=-32;
		var currentTilt=62;
		var currentZoom=1;
		var dragState=null;
		var lastTapAt=0;
		var activeTool='spec';
		if(savedUnit){
			var restored=units.find(function(u){return u.id===savedUnit});
			if(restored){activeUnit=restored;activeFloor=parseInt(restored.floor||activeFloor,10)}
		}
		function track(action,extra){
			window.dataLayer=window.dataLayer||[];
			var payload={event:'project_3d_interaction',action:action,card_id:parseInt(root.dataset.project,10)};
			if(extra){Object.keys(extra).forEach(function(k){payload[k]=extra[k]})}
			window.dataLayer.push(payload);
		}
		function watchShowroomContactRail(){
			if(!('IntersectionObserver' in window)||!document.body){return}
			var active=false;
			var observer=new IntersectionObserver(function(entries){
				entries.forEach(function(entry){
					if(entry.target!==root){return}
					active=entry.isIntersecting&&entry.intersectionRatio>0.12;
					document.body.classList.toggle('nadlan-p3d-stage-active',active);
				});
			},{threshold:[0,0.12,0.35,0.7]});
			observer.observe(root);
			window.addEventListener('pagehide',function(){document.body.classList.remove('nadlan-p3d-stage-active')},{once:true});
		}
		function safeUrl(url){
			if(!url){return ''}
			try{
				var u=new URL(String(url),window.location.origin);
				return /^https?:$/.test(u.protocol)?u.href:'';
			}catch(e){return ''}
		}
		function materialLabel(item,fallback){
			return (item&&(item.label||item.name||item.title))||fallback||'מידע נוסף';
		}
		function materialDetail(item){
			if(!item){return ''}
			var out=item.detail||item.note||item.source||'';
			if(item.distance){out+=(out?' · ':'')+item.distance}
			return out;
		}
		function appendMaterialCards(items,source){
			if(!toolPanel||!items||!items.length){return}
			var wrap=document.createElement('div');
			wrap.className='nlp3d-material-links';
			items.slice(0,6).forEach(function(item){
				var href=safeUrl(item.url);
				var el=document.createElement(href?'a':'span');
				el.className='nlp3d-material-card';
				if(href){
					el.href=href;
					el.target='_blank';
					el.rel='noopener';
				}
				var label=document.createElement('strong');
				var detail=document.createElement('small');
				label.textContent=materialLabel(item,'מידע נוסף');
				detail.textContent=materialDetail(item)||(href?'פתיחה בחלון חדש':'יופיע כאשר החומר יאושר');
				el.appendChild(label);
				el.appendChild(detail);
				if(item.type||item.category){
					var chip=document.createElement('em');
					chip.textContent=item.type||item.category;
					el.appendChild(chip);
				}
				if(href){
					el.addEventListener('click',function(){track('material_open',{source:source||activeTool,label:label.textContent})});
				}
				wrap.appendChild(el);
			});
			toolPanel.appendChild(wrap);
		}
		function floorHasUnits(f){return units.some(function(u){return parseInt(u.floor||0,10)===f})}
		function unitForFloor(f){return units.find(function(u){return parseInt(u.floor||0,10)===f&&u.status!=='sold'})||units.find(function(u){return parseInt(u.floor||0,10)===f})}
		function unitById(id){return units.find(function(u){return u.id===id})}
		function hasPoints(u){return u&&typeof u.points==='string'&&u.points.trim().split(/\s+/).length>=3}
		function pointBox(points){
			var coords=(points||'').trim().split(/\s+/).map(function(pair){
				var xy=pair.split(',');
				return {x:parseFloat(xy[0]),y:parseFloat(xy[1])};
			}).filter(function(p){return isFinite(p.x)&&isFinite(p.y)});
			if(!coords.length){return null}
			var minX=Math.min.apply(null,coords.map(function(p){return p.x}));
			var maxX=Math.max.apply(null,coords.map(function(p){return p.x}));
			var minY=Math.min.apply(null,coords.map(function(p){return p.y}));
			var maxY=Math.max.apply(null,coords.map(function(p){return p.y}));
			return {x:minX,y:minY,w:Math.max(1,maxX-minX),h:Math.max(1,maxY-minY)};
		}
		function makeHitPolygon(u){
			var box=pointBox(u.points);
			var hit=document.createElementNS('http://www.w3.org/2000/svg',box?'rect':'polygon');
			if(box){
				var minW=Math.max(96,box.w+28);
				var minH=Math.max(96,box.h+28);
				hit.setAttribute('x',Math.max(0,box.x+(box.w/2)-(minW/2)));
				hit.setAttribute('y',Math.max(0,box.y+(box.h/2)-(minH/2)));
				hit.setAttribute('width',minW);
				hit.setAttribute('height',minH);
				hit.setAttribute('rx','18');
				hit.setAttribute('ry','18');
			}else{
				hit.setAttribute('points',u.points);
			}
			hit.setAttribute('class','nlp3d-hotspot-hit nlp3d-status-'+u.status);
			hit.setAttribute('tabindex','0');
			hit.setAttribute('role','button');
			hit.setAttribute('aria-label',selectedTitle(u)+' · '+statusLabel(u.status));
			hit.dataset.unit=u.id;
			hit.dataset.action='select-unit-facade-hit';
			hit.addEventListener('click',function(e){e.stopPropagation();selectUnit(u.id,'facade-hit')});
			hit.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();selectUnit(u.id,'facade-hit-keyboard')}});
			return hit;
		}
		function renderTower(){
			tower.innerHTML='';
			var count=Math.max(22,Math.min(45,maxFloor));
			for(var i=1;i<=count;i++){
				var floor=Math.round(minFloor+((maxFloor-minFloor)*(i-1)/Math.max(1,count-1)));
				var b=document.createElement('div');
				var selectable=floorHasUnits(floor);
				b.className='nlp3d-plate'+(selectable?' has-units is-selectable':'')+(floor===activeFloor?' is-active':'');
				var uf=unitForFloor(floor);
				if(uf&&uf.status==='sold'){b.className+=' is-sold'}
				var stackRatio=(i-1)/Math.max(1,count-1);
				var plateWidth=78-(stackRatio*20);
				var plateOffset=9+(stackRatio*9);
				b.style.setProperty('--i',i);
				b.style.bottom=(i*8)+'px';
				b.style.width=plateWidth+'%';
				b.style.right=plateOffset+'%';
				b.dataset.floor=floor;
				b.dataset.action='select-floor';
				b.title='קומה '+floor;
				b.setAttribute('role','button');
				b.setAttribute('tabindex','0');
				b.setAttribute('aria-label','בחרו קומה '+floor);
				b.addEventListener('click',function(e){e.stopPropagation();selectFloor(parseInt(this.dataset.floor,10))});
				b.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();selectFloor(parseInt(this.dataset.floor,10))}});
				if(!selectable){
					b.removeAttribute('role');
					b.removeAttribute('tabindex');
					b.removeAttribute('aria-label');
					b.setAttribute('aria-hidden','true');
					b.style.pointerEvents='none';
				}
				if(floorHasUnits(floor)||floor===activeFloor||floor%5===0){
					var label=document.createElement('span');
					label.className='nlp3d-plate-label';
					label.textContent=floor;
					b.appendChild(label);
				}
				if(floorHasUnits(floor)){
					var dot=document.createElement('span');
					dot.className='nlp3d-plate-dot';
					b.appendChild(dot);
				}
				tower.appendChild(b);
			}
		}
		function renderFacade(){
			if(!hotspots){return}
			hotspots.innerHTML='';
			var any=false;
			units.filter(hasPoints).forEach(function(u){
				any=true;
				hotspots.appendChild(makeHitPolygon(u));
				var poly=document.createElementNS('http://www.w3.org/2000/svg','polygon');
				poly.setAttribute('points',u.points);
				poly.setAttribute('class','nlp3d-hotspot nlp3d-status-'+u.status+(activeUnit&&u.id===activeUnit.id?' is-active':''));
				poly.setAttribute('tabindex','0');
				poly.setAttribute('role','button');
				poly.setAttribute('aria-label',selectedTitle(u)+' · '+statusLabel(u.status));
				poly.dataset.unit=u.id;
				poly.dataset.action='select-unit-facade';
				var t=document.createElementNS('http://www.w3.org/2000/svg','title');
				t.textContent=selectedTitle(u)+' · '+unitText(u);
				poly.appendChild(t);
				poly.addEventListener('click',function(e){e.stopPropagation();selectUnit(u.id,'facade')});
				poly.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();selectUnit(u.id,'facade-keyboard')}});
				poly.removeAttribute('role');
				poly.removeAttribute('tabindex');
				poly.removeAttribute('aria-label');
				poly.setAttribute('aria-hidden','true');
				poly.style.pointerEvents='none';
				hotspots.appendChild(poly);
			});
			if(facade){facade.hidden=!any}
			scene.classList.toggle('has-facade',any);
		}
		function syncFacade(){
			root.querySelectorAll('.nlp3d-hotspot,.nlp3d-hotspot-hit').forEach(function(p){p.classList.toggle('is-active',activeUnit&&p.dataset.unit===activeUnit.id)});
			modelHotspots.forEach(function(p){p.classList.toggle('is-active',activeUnit&&p.dataset.unit===activeUnit.id)});
			if(modelViewer&&activeUnit){
				modelViewer.dataset.activeUnit=activeUnit.id;
			}
		}
		function syncModelViewerCamera(){
			if(!modelViewer||!activeUnit){return}
			if(activeUnit.camera_orbit){
				modelViewer.setAttribute('camera-orbit',activeUnit.camera_orbit);
				return;
			}
			var hotspot=modelHotspots.find(function(h){return h.dataset.unit===activeUnit.id});
			if(hotspot&&hotspot.dataset.position){
				modelViewer.setAttribute('camera-target',hotspot.dataset.position);
			}
		}
		function renderFloors(){
			floorStrip.innerHTML='';
			floors.forEach(function(f){
				var b=document.createElement('button');
				b.type='button';
				b.className='nlp3d-floor'+(f===activeFloor?' is-active':'');
				b.textContent='קומה '+f;
				b.dataset.floor=f;
				b.dataset.action='select-floor';
				b.addEventListener('click',function(){selectFloor(parseInt(this.dataset.floor,10))});
				floorStrip.appendChild(b);
			});
		}
		function renderUnits(){
			unitList.innerHTML='';
			units.filter(function(u){return parseInt(u.floor||0,10)===activeFloor}).forEach(function(u){
				var row=document.createElement('div');
				row.className='nlp3d-unit-row';
				var b=document.createElement('button');
				b.type='button';
				b.className='nlp3d-unit-card nlp3d-status-'+u.status+(activeUnit&&u.id===activeUnit.id?' is-active':'')+(u.status==='sold'?' is-sold':'');
				b.innerHTML='<strong>'+selectedTitle(u)+'</strong><span>'+unitText(u)+' · '+statusLabel(u.status)+'</span>';
				b.dataset.unit=u.id;
				b.dataset.action='select-unit-card';
				b.addEventListener('click',function(){selectUnit(u.id,'card')});
				var c=document.createElement('button');
				c.type='button';
				c.className='nlp3d-compare-add'+(compareIds.indexOf(u.id)>-1?' is-on':'');
				c.textContent=compareIds.indexOf(u.id)>-1?'בהשוואה':'השוו';
				c.dataset.action='toggle-compare';
				c.setAttribute('aria-label','הוספת '+selectedTitle(u)+' להשוואה');
				c.addEventListener('click',function(e){e.stopPropagation();toggleCompare(u.id)});
				row.appendChild(b);
				row.appendChild(c);
				unitList.appendChild(row);
			});
		}
		function renderCompareTray(){
			if(!compareTray||!compareChips){return}
			compareChips.innerHTML='';
			compareIds.forEach(function(id){
				var u=unitById(id);
				if(!u){return}
				var chip=document.createElement('button');
				chip.type='button';
				chip.className='nlp3d-compare-chip';
				chip.textContent=(u.title||u.id)+' ✕';
				chip.title='הסרה מההשוואה';
				chip.addEventListener('click',function(){toggleCompare(id)});
				compareChips.appendChild(chip);
			});
			compareTray.hidden=compareIds.length===0;
			var openBtn=compareTray.querySelector('.nlp3d-compare-open');
			if(openBtn){openBtn.disabled=compareIds.length<2;openBtn.textContent=compareIds.length<2?'בחרו עוד דירה להשוואה':'השוו '+compareIds.length+' דירות'}
			storageSet(storeKey+'-compare',JSON.stringify(compareIds));
		}
		function toggleCompare(id){
			var i=compareIds.indexOf(id);
			if(i>-1){compareIds.splice(i,1)}else{
				if(compareIds.length>=3){compareIds.shift()}
				compareIds.push(id);
			}
			renderCompareTray();
			renderUnits();
			track('compare_toggle',{unit:id,count:compareIds.length});
		}
		function sunHoursText(u){
			var s=sunSummary(u,meta);
			if(!s||!s.summer){return 'לפי חישוב'}
			return Math.round(s.summer.minutes/60*10)/10+' ש׳';
		}
		function buildCompareTable(){
			if(!compareTable){return}
			compareTable.innerHTML='';
			var list=compareIds.map(unitById).filter(Boolean);
			if(list.length<2){return}
			var table=document.createElement('table');
			var head=document.createElement('tr');
			head.appendChild(document.createElement('th'));
			list.forEach(function(u){
				var th=document.createElement('th');
				var pick=document.createElement('button');
				pick.type='button';
				pick.className='nlp3d-compare-pick';
				pick.textContent=selectedTitle(u);
				pick.addEventListener('click',function(){selectUnit(u.id,'compare');closeCompare()});
				th.appendChild(pick);
				head.appendChild(th);
			});
			table.appendChild(head);
			var rows=[
				['קומה',function(u){return u.floor||'-'}],
				['חדרים',function(u){return u.rooms||'-'}],
				['שטח',function(u){return u.sqm?fmt(u.sqm)+' מ"ר':'-'}],
				['מרפסת',function(u){return u.balcony?fmt(u.balcony)+' מ"ר':'-'}],
				['כיוון',function(u){return u.dir||'-'}],
				['נוף',function(u){return u.view||'-'}],
				['שמש ישירה בקיץ',sunHoursText],
				['סטטוס',function(u){return statusLabel(u.status)}]
			];
			rows.forEach(function(r){
				var tr=document.createElement('tr');
				var td0=document.createElement('td');
				td0.textContent=r[0];
				tr.appendChild(td0);
				list.forEach(function(u){
					var td=document.createElement('td');
					td.textContent=r[1](u);
					tr.appendChild(td);
				});
				table.appendChild(tr);
			});
			compareTable.appendChild(table);
		}
		function openCompare(){
			if(compareIds.length<2||!compareOverlay){return}
			buildCompareTable();
			compareOverlay.hidden=false;
			track('compare_open',{count:compareIds.length});
		}
		function closeCompare(){if(compareOverlay){compareOverlay.hidden=true}}
		function openPlan(url){
			if(!planOverlay||!planBody){return}
			planBody.innerHTML='';
			if(/\.(png|jpe?g|webp|gif|svg)(\?|#|$)/i.test(url)){
				var img=document.createElement('img');
				img.src=url;
				img.alt='תוכנית דירה';
				planBody.appendChild(img);
			}else{
				var fr=document.createElement('iframe');
				fr.src=url;
				fr.title='תוכנית דירה';
				planBody.appendChild(fr);
			}
			planOverlay.hidden=false;
			track('plan_open',{unit:activeUnit&&activeUnit.id});
		}
		function closePlan(){if(planOverlay){planOverlay.hidden=true;planBody.innerHTML=''}}
		function markDealStep(step){
			if(!dealSteps){return}
			var el=dealSteps.querySelector('[data-step="'+step+'"]');
			if(el){el.classList.add('is-done')}
		}
		function setWStep(n){
			root.querySelectorAll('.nlp3d-wstep').forEach(function(s){s.hidden=parseInt(s.dataset.wstep,10)!==n});
			wdots.forEach(function(d,i){d.classList.toggle('is-on',i<n)});
		}
		function renderSelectionDock(){
			if(!activeUnit||!dockTitle){return}
			dockTitle.textContent=selectedTitle(activeUnit);
			if(dockMeta){
				var metaText=unitText(activeUnit);
				dockMeta.textContent=(metaText?metaText+' · ':'')+statusLabel(activeUnit.status);
			}
			renderStageCard();
		}
		function renderStageCard(){
			if(!stageCard||!activeUnit){return}
			stageCard.hidden=!hasStageSelection;
			if(stageWrap){stageWrap.classList.toggle('has-stage-selection',hasStageSelection)}
			if(!hasStageSelection){return}
			stageCard.dataset.status=activeUnit.status||'available';
			if(stageCardTitle){stageCardTitle.textContent=selectedTitle(activeUnit)}
			if(stageCardMeta){
				var metaText=unitText(activeUnit);
				stageCardMeta.textContent=(metaText?metaText+' · ':'')+(activeUnit.availability||statusLabel(activeUnit.status));
			}
			var priceInfo=unitPriceInfo(activeUnit,meta);
			if(stageCardPrice){
				stageCardPrice.textContent=priceInfo.text;
				stageCardPrice.dataset.kind=priceInfo.kind;
				stageCardPrice.title=priceInfo.kind==='estimate'?(priceInfo.note||'אומדן לא מחייב'):'';
			}
			if(stageCardStatus){stageCardStatus.textContent=statusLabel(activeUnit.status)}
			if(stageCardView){stageCardView.textContent=activeUnit.view||activeUnit.dir||'מבט לפי כיוון'}
		}
		function renderDetail(){
			if(!activeUnit){return}
			title.textContent=selectedTitle(activeUnit);
			facts.innerHTML='';
			detailRows(activeUnit,meta).forEach(function(row){
				var wrap=document.createElement('div');
				var dt=document.createElement('dt');
				var dd=document.createElement('dd');
				dt.textContent=row[0];
				dd.textContent=row[1];
				wrap.appendChild(dt);
				wrap.appendChild(dd);
				facts.appendChild(wrap);
			});
			renderSelectionDock();
			if(activeUnit.plan){plan.href=activeUnit.plan;plan.hidden=false}else{plan.hidden=true}
			renderUnitView();
			renderToolPanel();
			ok.hidden=true;
			form.querySelectorAll('button[type="submit"]').forEach(function(b){b.disabled=false});
		}
		function renderToolPanel(){
			if(!toolPanel||!activeUnit){return}
			var materialItems=[];
			var headline='מפרט הדירה';
			var copy='הדירה שנבחרה מוצגת לפי נתוני ההמחשה: '+(activeUnit.rooms||'')+' חדרים, '+(activeUnit.sqm?fmt(activeUnit.sqm)+' מ"ר':'שטח לפי פנייה')+', קומה '+(activeUnit.floor||'לפי פנייה')+', '+(activeUnit.building||'בניין לפי פנייה')+'. '+(activeUnit.note||'מפרט רשמי יימסר לאחר בדיקת זמינות מול היזם.');
			if(activeTool==='drawing'){
				headline='תוכנית ומדידות';
				copy=activeUnit.plan?'ניתן לפתוח את תוכנית הדירה המקושרת ולבקש בדיקה של המידות, המרפסת והכיוונים.':'תוכנית רשמית עדיין לא נטענה לכרטיס. אפשר לשלוח בקשה ולקבל תוכנית, מדידות, כיווני אוויר וחומר מכירה כאשר הם זמינים ומאומתים. המערכת כבר שומרת את היחידה, הקומה והקו כדי לקשור אליהם תוכנית רשמית בהמשך.';
				if(activeUnit.plan){materialItems.push({label:'תוכנית הדירה שנבחרה',url:activeUnit.plan,type:'plan'})}
				if(Array.isArray(meta.drawings)){materialItems=materialItems.concat(meta.drawings)}
			}
			if(activeTool==='view'){
				headline='מבט מהדירה';
				var cam=cameraParams(activeUnit,meta);
				copy=(activeUnit.view_note||activeUnit.view||activeUnit.dir||'מבט לפי כיוון היחידה')+'. גובה מצלמה מחושב: '+cam.altitude_m+' מ׳, כיוון '+cam.bearing+'°. כאשר שכבת מפה או הדמיית עיר מאושרת זמינה, הכפתור "מבט מהדירה" מציג את הסביבה במצלמה חיה.';
				if(meta.cesium_tiles_url){materialItems.push({label:'שכבת עיר תלת ממדית עתידית',url:meta.cesium_tiles_url,type:'3d-city',detail:'מיועדת לחיבור Cesium / Google 3D Tiles כאשר החשבון וההרשאות מוכנים'})}
			}
			if(activeTool==='sun'){
				headline='אור ושמש בדירה';
				var sun=sunSummary(activeUnit,meta);
				if(!sun){
					copy='חישוב שעות השמש יופעל כאשר קואורדינטות הפרויקט יוזנו לכרטיס. הכיוון המוצהר של הדירה: '+(activeUnit.dir||'לפי פנייה')+'.';
				}else{
					var parts=['הדירה פונה לכיוון '+(activeUnit.dir||'')+' ('+sun.bearing+'°).'];
					parts.push(sun.summer?('שמש ישירה בקיץ (21.6): בערך '+sun.summer.from+'–'+sun.summer.to+', כ-'+Math.round(sun.summer.minutes/60*10)/10+' שעות.'):'בקיץ החזית כמעט ללא שמש ישירה.');
					parts.push(sun.winter?('שמש ישירה בחורף (21.12): בערך '+sun.winter.from+'–'+sun.winter.to+', כ-'+Math.round(sun.winter.minutes/60*10)/10+' שעות.'):'בחורף החזית כמעט ללא שמש ישירה.');
					parts.push('החישוב אסטרונומי לפי מיקום הפרויקט וכיוון החזית, שעון ישראל, ללא הצללות מבניינים שכנים.');
					copy=parts.join(' ');
				}
			}
			if(activeTool==='surroundings'){
				headline='סביבה ושירותים סביב הפרויקט';
				var env=Array.isArray(meta.environment)?meta.environment:[];
				if(env.length){
					copy=env.slice(0,5).map(function(item){return (item.label||item.name||'נקודת עניין')+(item.detail?' - '+item.detail:'')}).join(' · ');
					materialItems=env;
				}else{
					copy='שדה דב מתוכנן כרובע חופי חדש עם פארקים, שבילי הליכה, מסחר שכונתי, מוסדות ציבור, חיבור לים ולצירי תחבורה. בשלב הבא אפשר להזין נקודות עניין מאושרות: בתי ספר, גנים, תחבורה, פארקים ופרויקטים שכנים.';
				}
			}
			if(activeTool==='media'){
				headline='מדיה, סיור וחומרים';
				var bits=[];
				if(activeUnit.interior_url){materialItems.push({label:'המחשת פנים ליחידה',url:activeUnit.interior_url,type:'interior'})}
				if(activeUnit.tour_url){materialItems.push({label:'סיור 3D ליחידה',url:activeUnit.tour_url,type:'tour'})}
				if(meta.tour_url){materialItems.push({label:'סיור פרויקט',url:meta.tour_url,type:'tour'})}
				if(meta.video_url){materialItems.push({label:'סרטון פרויקט',url:meta.video_url,type:'video'})}
				if(activeUnit.tour_url||meta.tour_url){bits.push('סיור פנימי או קישור 3D זמין לפתיחה מתוך חומרי הפרויקט')}
				if(activeUnit.interior_url){bits.push('המחשת פנים מקושרת ליחידה שנבחרה')}
				if(meta.video_url){bits.push('סרטון מכירה או שיחת וידאו יכולים להופיע כאן')}
				if(Array.isArray(meta.drawings)&&meta.drawings.length){bits.push('נטענו '+meta.drawings.length+' חומרים ותוכניות לפרויקט')}
				copy=bits.length?bits.join(' · '):'כאן יופיעו סרטון מכירה, סיור פנימי, תוכנית קומתית, תוכנית דירה וחומרים מאושרים של היזם. אם אין חומרים מאושרים, המערכת מציגה בקשת חומרים ולא מייצרת תוכנית רשמית.';
			}
			if(activeTool==='advisors'){
				headline='ליווי מקצועי';
				copy='אפשר לבקש לצרף עורך דין רכישה, יועץ משכנתאות, בדק בית או מעצב פנים. הבקשה תישלח עם הדירה שנבחרה, כולל קומה, שטח, כיוון ונוף, כדי לחזור אליכם עם ליווי מתאים לפני כל התחייבות.';
			}
			toolPanel.innerHTML='';
			var strong=document.createElement('strong');
			var p=document.createElement('p');
			strong.textContent=headline;
			p.textContent=copy;
			toolPanel.appendChild(strong);
			toolPanel.appendChild(p);
			appendMaterialCards(materialItems,activeTool);
		}
		function canLiveView(){
			var cam=cameraParams(activeUnit,meta);
			return !!(meta.mapbox_token&&cam.lat&&cam.lng);
		}
		function applyLiveCamera(){
			if(!liveMap||!activeUnit){return}
			var cam=cameraParams(activeUnit,meta);
			try{
				var freeCam=liveMap.getFreeCameraOptions();
				freeCam.position=mapboxgl.MercatorCoordinate.fromLngLat({lng:cam.lng,lat:cam.lat},cam.altitude_m);
				var brg=cam.bearing*RAD,dist=900,R=6378137;
				var dLat=(dist*Math.cos(brg))/R/RAD;
				var dLng=(dist*Math.sin(brg))/(R*Math.cos(cam.lat*RAD))/RAD;
				freeCam.lookAtPoint({lng:cam.lng+dLng,lat:cam.lat+dLat});
				liveMap.setFreeCameraOptions(freeCam);
			}catch(err){}
		}
		function renderLiveView(){
			if(!viewMap||!viewFrame||viewFrame.hidden){return}
			if(!canLiveView()){viewMap.hidden=true;return}
			viewMap.hidden=false;
			viewMap.removeAttribute('hidden');
			viewMap.style.display='block';
			loadMapboxGl(function(){
				if(!window.mapboxgl){
					viewMap.hidden=false;
					viewMap.innerHTML='<div class="nlp3d-map-error">המפה התלת ממדית לא נטענה כרגע. אפשר עדיין לבחור דירה, להשוות נתונים ולשלוח פנייה.</div>';
					return;
				}
				try{
					if(!liveMap){
						viewMap.innerHTML='';
						mapboxgl.accessToken=meta.mapbox_token;
						if(mapboxgl.setRTLTextPlugin&&!window.nlp3dRtlTextPluginSet){
							try{mapboxgl.setRTLTextPlugin('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js',null,true);window.nlp3dRtlTextPluginSet=true;}catch(rtlErr){}
						}
						liveMap=new mapboxgl.Map({container:viewMap,style:'mapbox://styles/mapbox/standard',center:[Number(meta.lng),Number(meta.lat)],zoom:14.5,pitch:62,bearing:0,antialias:true,attributionControl:true,dragRotate:true,touchPitch:true,touchZoomRotate:true,pitchWithRotate:true});
						liveMap.addControl(new mapboxgl.NavigationControl({visualizePitch:true,showCompass:true,showZoom:true}),'top-left');
						liveMap.on('load',function(){
							try{
								if(liveMap.getSource&&liveMap.getSource('composite')&&!liveMap.getLayer('nlp3d-3d-buildings')){
									liveMap.addLayer({id:'nlp3d-3d-buildings',source:'composite','source-layer':'building',filter:['==','extrude','true'],type:'fill-extrusion',minzoom:13,paint:{'fill-extrusion-color':'#c9c0ad','fill-extrusion-height':['coalesce',['get','height'],14],'fill-extrusion-base':['coalesce',['get','min_height'],0],'fill-extrusion-opacity':0.7}});
								}
							}catch(e){}
							liveMap.resize();
							applyLiveCamera();
						});
					}else{
						liveMap.resize();
						applyLiveCamera();
					}
					window.requestAnimationFrame(function(){if(liveMap){liveMap.resize();applyLiveCamera()}});
					window.setTimeout(function(){if(liveMap){liveMap.resize();applyLiveCamera()}},260);
				}catch(err){
					viewMap.hidden=false;
					viewMap.innerHTML='<div class="nlp3d-map-error">המפה התלת ממדית לא נטענה כרגע. אפשר עדיין לבחור דירה, להשוות נתונים ולשלוח פנייה.</div>';
				}
			});
		}
		function renderUnitView(){
			if(!viewCopy||!activeUnit){return}
			var view=activeUnit.view||activeUnit.dir||'הסביבה הקרובה';
			var cam=cameraParams(activeUnit,meta);
			var live=canLiveView();
			var badge=root.querySelector('.nlp3d-view-badge');
			if(badge){badge.hidden=!live}
			if(live){
				viewCopy.textContent='גובה מצלמה '+cam.altitude_m+' מ׳, כיוון '+cam.bearing+'° ('+view+'). גררו לסיבוב, גללו או צבטו לזום. בניינים מסביב מבוססים על מודל מפה ציבורי.';
			}else{
				var cameraNote=(cam.lat&&cam.lng)?(' פרמטרי המבט מוכנים: גובה '+cam.altitude_m+' מ׳, כיוון '+cam.bearing+'°. המבט החי יופעל כאשר מפתח המפות יוזן במערכת.'):'';
				viewCopy.textContent='מבט המחשה מהיחידה: '+view+'. זהו מצב תצוגה תכנוני עד שיוזנו הדמיות ותוכניות מאושרות.'+cameraNote;
			}
			if(viewFrame){viewFrame.dataset.view=(activeUnit.view||'city').toLowerCase()}
			renderLiveView();
		}
		function setLiveView(open,source){
			if(!viewFrame||!stageWrap){return}
			viewFrame.hidden=!open;
			stageWrap.classList.toggle('is-live-view',open);
			root.classList.toggle('is-live-view',open);
			if(viewToggle){
				viewToggle.classList.toggle('is-active',open);
				viewToggle.setAttribute('aria-pressed',open?'true':'false');
				viewToggle.textContent=open?'\u05d7\u05d6\u05e8\u05d4 \u05dc\u05de\u05d5\u05d3\u05dc':'\u05de\u05d1\u05d8 \u05de\u05d4\u05d3\u05d9\u05e8\u05d4';
			}
			if(open){
				renderUnitView();
				window.requestAnimationFrame(function(){if(liveMap){liveMap.resize();applyLiveCamera()}});
				window.setTimeout(function(){if(liveMap){liveMap.resize();applyLiveCamera()}},120);
			}
			track('view_from_unit',{unit:activeUnit&&activeUnit.id,open:open,live:canLiveView(),source:source||'toggle'});
		}
		function setAngle(angle){
			currentAngle=((angle%360)+360)%360;
			scene.style.setProperty('--angle',currentAngle+'deg');
			if(modelViewer){
				modelViewer.removeAttribute('auto-rotate');
				modelViewer.setAttribute('camera-orbit',Math.round(currentAngle)+'deg 68deg auto');
			}
		}
		function setTilt(tilt){
			currentTilt=Math.max(48,Math.min(72,tilt));
			scene.style.setProperty('--tilt',currentTilt+'deg');
		}
		function setZoom(zoom){
			currentZoom=Math.max(0.86,Math.min(1.34,zoom));
			scene.style.setProperty('--model-zoom',currentZoom);
			scene.classList.toggle('is-zoomed',currentZoom>1.04);
			if(modelViewer){
				modelViewer.setAttribute('field-of-view',Math.round(30/currentZoom)+'deg');
			}
		}
		function selectFloor(f){
			activeFloor=f;
			var next=unitForFloor(f);
			if(next){activeUnit=next}
			hasStageSelection=!!activeUnit;
			renderAll(false);
			syncModelViewerCamera();
			if(activeUnit){storageSet(storeKey+'-unit',activeUnit.id)}
			track('select_floor',{floor:f,unit:activeUnit&&activeUnit.id});
		}
		function selectUnit(id,source){
			var next=unitById(id);
			if(next){activeUnit=next;activeFloor=parseInt(next.floor||activeFloor,10)}
			hasStageSelection=!!next||hasStageSelection;
			renderAll(false);
			syncModelViewerCamera();
			if(activeUnit){storageSet(storeKey+'-unit',activeUnit.id)}
			track('select_unit',{floor:activeFloor,unit:id,source:source||'unknown'});
		}
		function renderAll(includeTower){
			if(includeTower){renderTower();renderFacade()}else{root.querySelectorAll('.nlp3d-plate').forEach(function(p){p.classList.toggle('is-active',parseInt(p.dataset.floor,10)===activeFloor)});syncFacade()}
			renderFloors();
			renderUnits();
			renderDetail();
		}
		root.querySelectorAll('.nlp3d-angle').forEach(function(b){
			b.addEventListener('click',function(){
				root.querySelectorAll('.nlp3d-angle').forEach(function(x){x.classList.remove('is-active')});
				b.classList.add('is-active');
				setAngle(parseFloat(b.dataset.angle||'-32'));
				scene.classList.remove('is-orbit');
				var orbit=root.querySelector('.nlp3d-orbit');
				if(orbit){orbit.classList.remove('is-active')}
				track('angle',{angle:b.textContent});
			});
		});
		var orbit=root.querySelector('.nlp3d-orbit');
		if(orbit){orbit.addEventListener('click',function(){
			if(modelViewer){
				var active=!modelViewer.hasAttribute('auto-rotate');
				if(active){modelViewer.setAttribute('auto-rotate','')}else{modelViewer.removeAttribute('auto-rotate')}
				orbit.classList.toggle('is-active',active);
				track('orbit',{active:active,model_viewer:true});
				return;
			}
			scene.classList.toggle('is-orbit');orbit.classList.toggle('is-active');track('orbit',{active:scene.classList.contains('is-orbit')})
		})}
		root.querySelectorAll('.nlp3d-zoom').forEach(function(b){
			b.addEventListener('click',function(){
				setZoom(currentZoom+(b.dataset.zoom==='in'?0.12:-0.12));
				track('model_zoom',{zoom:Math.round(currentZoom*100)/100});
			});
		});
		if(dockSpin){
			dockSpin.addEventListener('click',function(){
				if(modelViewer){
					modelViewer.setAttribute('auto-rotate','');
					track('dock_360',{unit:activeUnit&&activeUnit.id,model_viewer:true});
					return;
				}
				scene.classList.add('is-orbit');
				var orbit=root.querySelector('.nlp3d-orbit');
				if(orbit){orbit.classList.add('is-active')}
				track('dock_360',{unit:activeUnit&&activeUnit.id});
			});
		}
		if(dockInquiry&&form){
			dockInquiry.addEventListener('click',function(){
				setWStep(2);
				form.scrollIntoView({behavior:'smooth',block:'center'});
				track('dock_inquiry',{unit:activeUnit&&activeUnit.id});
			});
		}
		if(stageDetails&&detail){
			stageDetails.addEventListener('click',function(){
				setLiveView(false,'stage-details');
				detail.scrollIntoView({behavior:'smooth',block:'center'});
				track('stage_details',{unit:activeUnit&&activeUnit.id});
			});
		}
		if(stageViewBtn&&viewFrame){
			stageViewBtn.addEventListener('click',function(){
				setLiveView(true,'stage-card');
				track('stage_view',{unit:activeUnit&&activeUnit.id,live:canLiveView()});
			});
		}
		if(stageInquiry&&form){
			stageInquiry.addEventListener('click',function(){
				setLiveView(false,'stage-inquiry');
				setWStep(2);
				form.scrollIntoView({behavior:'smooth',block:'center'});
				track('stage_inquiry',{unit:activeUnit&&activeUnit.id});
			});
		}
		if(viewToggle&&viewFrame){
			viewToggle.addEventListener('click',function(){
				setLiveView(viewFrame.hidden,'toggle');
			});
		}
		modelHotspots.forEach(function(h){
			h.addEventListener('click',function(e){
				e.preventDefault();
				e.stopPropagation();
				selectUnit(h.dataset.unit,'model-viewer-hotspot');
			});
		});
		if(modelViewer){
			modelViewer.addEventListener('load',function(){root.classList.add('has-model-viewer-loaded');syncModelViewerCamera();track('model_viewer_load',{model:true})});
			modelViewer.addEventListener('error',function(){root.classList.add('has-model-viewer-error');track('model_viewer_error',{model:true})});
		}
		if(stageReturn){
			stageReturn.addEventListener('click',function(){setLiveView(false,'return')});
		}
		var wnext=root.querySelector('.nlp3d-wnext');
		var wback=root.querySelector('.nlp3d-wback');
		if(wnext){
			wnext.addEventListener('click',function(){
				var nameInput=form.querySelector('[name="name"]');
				var phoneInput=form.querySelector('[name="phone"]');
				if(!nameInput.value.trim()){nameInput.reportValidity();nameInput.focus();return}
				if(!phoneInput.value.trim()){phoneInput.reportValidity();phoneInput.focus();return}
				setWStep(2);
				track('wizard_step',{step:2,unit:activeUnit&&activeUnit.id});
			});
		}
		if(wback){wback.addEventListener('click',function(){setWStep(1)})}
		var compareOpenBtn=root.querySelector('.nlp3d-compare-open');
		if(compareOpenBtn){compareOpenBtn.addEventListener('click',openCompare)}
		root.querySelectorAll('.nlp3d-overlay-close').forEach(function(b){
			b.addEventListener('click',function(){closeCompare();closePlan()});
		});
		root.querySelectorAll('.nlp3d-overlay').forEach(function(ov){
			ov.addEventListener('click',function(e){if(e.target===ov){closeCompare();closePlan()}});
		});
		document.addEventListener('keydown',function(e){
			if(e.key==='Escape'){closeCompare();closePlan()}
		});
		if(plan){
			plan.addEventListener('click',function(e){
				var href=plan.getAttribute('href');
				if(!href||href==='#'){e.preventDefault();return}
				e.preventDefault();
				openPlan(href);
			});
		}
		toolButtons.forEach(function(b){
			b.addEventListener('click',function(){
				activeTool=b.dataset.tool||'spec';
				toolButtons.forEach(function(x){x.classList.toggle('is-active',x===b)});
				renderToolPanel();
				track('tool_panel',{tool:activeTool,unit:activeUnit&&activeUnit.id});
			});
		});
		scene.addEventListener('pointerdown',function(e){
			if(e.target.closest('button,a,input,.nlp3d-hotspot,.nlp3d-hotspot-hit,.nlp3d-mv-hotspot,.nlp3d-stage-card,.nlp3d-stage-viewframe')){return}
			dragState={x:e.clientX,y:e.clientY,angle:currentAngle,tilt:currentTilt,id:e.pointerId,lastX:e.clientX,lastT:Date.now(),vx:0};
			scene.classList.add('is-dragging');
			scene.classList.remove('is-orbit');
			if(orbit){orbit.classList.remove('is-active')}
			if(scene.setPointerCapture){scene.setPointerCapture(e.pointerId)}
		});
		scene.addEventListener('pointermove',function(e){
			if(!dragState){return}
			var t=Date.now();
			var dt=Math.max(16,t-dragState.lastT);
			dragState.vx=(e.clientX-dragState.lastX)/dt;
			dragState.lastX=e.clientX;
			dragState.lastT=t;
			setAngle(dragState.angle+(e.clientX-dragState.x)*0.22);
			setTilt(dragState.tilt-(e.clientY-dragState.y)*0.08);
		});
		function endDrag(e){
			if(!dragState){return}
			var moved=Math.abs(e.clientX-dragState.x)+Math.abs(e.clientY-dragState.y);
			var momentum=Math.max(-120,Math.min(120,(dragState.vx||0)*180));
			if(scene.releasePointerCapture){try{scene.releasePointerCapture(dragState.id)}catch(err){}}
			dragState=null;
			scene.classList.remove('is-dragging');
			var now=Date.now();
			if(moved<8&&now-lastTapAt<320){
				setZoom(currentZoom>1.05?1:1.22);
				track('model_double_tap_zoom',{zoom:Math.round(currentZoom*100)/100});
			}
			if(moved<8){lastTapAt=now}
			if(moved>=8&&Math.abs(momentum)>4){setAngle(currentAngle+momentum)}
			if(moved>=8){track('drag',{angle:currentAngle})}
		}
		scene.addEventListener('pointerup',endDrag);
		scene.addEventListener('pointercancel',endDrag);
		form.addEventListener('submit',function(e){
			e.preventDefault();
			if(!activeUnit){return}
			var submitter=e.submitter || form.querySelector('.nlp3d-send');
			var intent=submitter&&submitter.dataset.intent==='purchase'?'purchase':'callback';
			var fd=new FormData(form);
			var intentText=intent==='purchase'?'בדיקת רכישה ושמירה':'בקשת שיחה';
			var advisorList=fd.getAll?fd.getAll('advisors'):[];
			var advisor=advisorList.length?advisorList.join(' + '):'לא נבחר';
			var timeline=fd.get('timeline')||'לא נמסר';
			var cam=cameraParams(activeUnit,meta);
			var reservationState=intent==='purchase'?'non_binding_inquiry':'lead_request';
			var message=intentText+' מתוך מודל תלת ממדי של '+(meta.title||'הפרויקט')+'. יחידה: '+selectedTitle(activeUnit)+'. '+unitText(activeUnit)+'. בניין: '+(activeUnit.building||'לא נמסר')+'. זמינות: '+(activeUnit.availability||'לא מאומתת')+'. תקציב: '+(fd.get('budget')||'לא נמסר')+'. מועד התקדמות: '+timeline+'. ליווי מבוקש: '+advisor+'. נא לאמת זמינות, מחיר ותנאים מול היזם לפני כל התקדמות. סטטוס: '+reservationState+'.';
			var payload={card_id:parseInt(root.dataset.project,10),name:fd.get('name'),phone:fd.get('phone'),email:fd.get('email'),goal:intentText,message:message,company:fd.get('company'),source:'project_3d',budget:fd.get('budget'),unit:activeUnit.id,floor:activeUnit.floor,rooms:activeUnit.rooms,sqm:activeUnit.sqm,building:activeUnit.building||'',availability:activeUnit.availability||'',market_note:activeUnit.market_note||'',timeline:timeline,advisor:advisor,purchase_intent:intent==='purchase',reservation_state:reservationState,view_bearing:cam.bearing,view_altitude_m:cam.altitude_m};
			track('submit',{intent:intent,unit:activeUnit.id,floor:activeUnit.floor,advisor:advisor,reservation_state:reservationState,view_bearing:cam.bearing,view_altitude_m:cam.altitude_m});
			form.querySelectorAll('button[type="submit"]').forEach(function(b){b.disabled=true});
			ok.textContent='שולחים את הפנייה...';
			ok.hidden=false;
			fetch('__NLP3D_REST__',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
				.then(function(r){if(!r.ok){throw new Error('lead failed')}return r.json()})
				.then(function(data){
					markDealStep('select');
					if(advisorList.length){markDealStep('advisors')}
					var ref=data&&(data.id||data.lead_id||'');
					ok.textContent='קיבלנו את הפנייה. נציג יחזור אליך בתוך 24 שעות עם בדיקת זמינות ונתונים מאומתים.'+(ref?' מספר פנייה: '+ref+'.':'');
				})
				.catch(function(){ok.textContent='השליחה נכשלה. אפשר לנסות שוב או לפנות דרך כפתור יצירת הקשר באתר.';form.querySelectorAll('button[type="submit"]').forEach(function(b){b.disabled=false})});
		});
		if(ownerForm){
			ownerForm.addEventListener('submit',function(e){
				e.preventDefault();
				var fd=new FormData(ownerForm);
				var projectName=(fd.get('project_name')||'').toString().trim();
				var city=(fd.get('city')||'').toString().trim();
				var payload={
					card_id:parseInt(root.dataset.project,10),
					name:fd.get('name'),
					phone:fd.get('phone'),
					email:fd.get('email'),
					company:fd.get('company'),
					source:'project_3d_showcase',
					goal:'בקשה להצגת פרויקט אינטראקטיבי',
					message:'בקשה לבדיקת התאמה לעמוד תצוגה אינטראקטיבי. פרויקט: '+(projectName||'לא נמסר')+'. אזור: '+(city||'לא נמסר')+'. מקור: עמוד '+(meta.title||'פרויקט')+'.'
				};
				track('owner_showcase_submit',{project_name:projectName,city:city});
				if(ownerOk){ownerOk.textContent='שולחים את הבקשה...';ownerOk.hidden=false}
				ownerForm.querySelectorAll('button,input').forEach(function(el){if(el.type!=='hidden'){el.disabled=true}});
				fetch('__NLP3D_REST__',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
					.then(function(r){if(!r.ok){throw new Error('owner lead failed')}return r.json()})
					.then(function(){if(ownerOk){ownerOk.textContent='קיבלנו את הפרטים. נחזור אליכם בתוך יום עסקים עם בדיקת התאמה ראשונית.'}})
					.catch(function(){if(ownerOk){ownerOk.textContent='השליחה נכשלה. אפשר לנסות שוב בעוד רגע.'}ownerForm.querySelectorAll('button,input').forEach(function(el){el.disabled=false})});
			});
		}
		setTilt(currentTilt);
		setZoom(currentZoom);
		watchShowroomContactRail();
		renderAll(true);
		syncModelViewerCamera();
		renderCompareTray();
	}
	function boot(){document.querySelectorAll('.nlp3d-premium').forEach(init)}
	if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',boot)}else{boot()}
})();
JS;
		return str_replace( '__NLP3D_REST__', esc_js( $rest_url ), $js );
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

add_action(
	'wp_enqueue_scripts',
	function () {
		if ( ! nadlan_p3d_enabled() ) {
			return;
		}

		wp_register_style( 'nadlan-p3d', '', array(), '1.63.8' );
		wp_enqueue_style( 'nadlan-p3d' );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_inline_css() );
		wp_add_inline_style( 'nadlan-p3d', '.nlp3d-drag-note{display:inline-flex;align-items:center;min-height:44px;color:rgba(246,239,226,.72);font-size:12px;padding:0 6px}.nlp3d-scene{touch-action:none;cursor:grab}.nlp3d-scene.is-dragging{cursor:grabbing}.nlp3d-actions{grid-template-columns:1fr}.nlp3d-view-toggle{margin-top:12px;border:1px solid rgba(234,216,163,.36);background:rgba(255,255,255,.06);color:#ffe8a6;padding:9px 12px;cursor:pointer}.nlp3d-view-toggle.is-active{background:rgba(234,216,163,.18);color:#fff}.nlp3d-viewframe{position:relative;margin-top:12px;min-height:150px;overflow:hidden;border:1px solid rgba(234,216,163,.18);background:linear-gradient(180deg,rgba(41,112,139,.58),rgba(8,25,25,.92));isolation:isolate}.nlp3d-view-sky{position:absolute;inset:0;background:radial-gradient(circle at 18% 22%,rgba(255,255,255,.24),transparent 18%),linear-gradient(135deg,rgba(39,107,130,.42),rgba(18,50,43,.1));opacity:.86}.nlp3d-view-lines{position:absolute;inset:auto -8% 18% -8%;height:46%;border-top:1px solid rgba(234,216,163,.28);background:linear-gradient(160deg,rgba(234,216,163,.1),transparent 54%);transform:skewY(-8deg)}.nlp3d-view-copy{position:absolute;right:14px;left:14px;bottom:12px;margin:0;color:#fff8dc;font-size:13px;line-height:1.5;text-shadow:0 1px 12px rgba(0,0,0,.55)}@media(max-width:600px){.nlp3d-drag-note{flex-basis:100%;min-height:24px}.nlp3d-viewframe{min-height:130px}}' );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_experience_css() );
		wp_add_inline_style( 'nadlan-p3d', '.nlp3d-facade{position:absolute;z-index:6;inset:58px 13% 54px;margin:0;display:block;border:1px solid rgba(234,216,163,.22);background:linear-gradient(135deg,rgba(4,16,18,.44),rgba(255,255,255,.04));box-shadow:0 24px 64px rgba(0,0,0,.34);overflow:hidden;pointer-events:none}.nlp3d-facade[hidden]{display:none}.nlp3d-facade img{display:block;width:100%;height:100%;object-fit:cover;filter:saturate(.82) contrast(1.08) sepia(.08);opacity:.86}.nlp3d-facade:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(234,216,163,.08),transparent 34%,rgba(0,0,0,.22));pointer-events:none}.nlp3d-facade figcaption{position:absolute;right:10px;bottom:9px;left:10px;z-index:3;color:#fff3c6;font-size:11px;line-height:1.4;text-shadow:0 1px 10px rgba(0,0,0,.72)}.nlp3d-facade-hotspots{position:absolute;z-index:2;inset:0;width:100%;height:100%;pointer-events:auto}.nlp3d-hotspot{fill:rgba(234,216,163,.08);stroke:rgba(234,216,163,.64);stroke-width:2;vector-effect:non-scaling-stroke;cursor:pointer;transition:fill .16s,stroke .16s,filter .16s}.nlp3d-hotspot:hover,.nlp3d-hotspot:focus-visible{fill:rgba(234,216,163,.24);stroke:#fff2ba;outline:none;filter:drop-shadow(0 0 8px rgba(234,216,163,.42))}.nlp3d-hotspot.is-active{fill:rgba(234,216,163,.34);stroke:#fff2ba;filter:drop-shadow(0 0 14px rgba(234,216,163,.5))}.nlp3d-scene.has-facade .nlp3d-tower{opacity:.34}.nlp3d-deal-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-top:12px}.nlp3d-deal-steps span{min-height:32px;display:flex;align-items:center;justify-content:center;border:1px solid rgba(234,216,163,.18);background:rgba(255,255,255,.045);color:#fff3c8;font-size:12px}.nlp3d-deal-steps span:first-child{background:rgba(234,216,163,.16);border-color:rgba(234,216,163,.36)}@media(max-width:900px){.nlp3d-facade{inset:62px 8% 42px}}@media(max-width:600px){.nlp3d-facade{inset:70px 7% 34px}.nlp3d-deal-steps{grid-template-columns:repeat(2,minmax(0,1fr))}}' );
		wp_add_inline_style( 'nadlan-p3d', '.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:min(1280px,calc(100vw - 36px));margin-inline:calc(50% - min(640px,calc(50vw - 18px)));overflow:clip}.nlp3d-shell{grid-template-columns:minmax(220px,.72fr) minmax(520px,1.45fr);grid-template-areas:"copy stage" "console stage";align-items:start;min-height:0;padding:28px}.nlp3d-copy{grid-area:copy;align-self:start;padding-bottom:0}.nlp3d-stage-wrap{grid-area:stage;min-height:760px}.nlp3d-console{grid-area:console;min-width:0}.nlp3d h2{max-width:15ch;font-size:clamp(28px,3vw,46px)}.nlp3d-lead-text{font-size:15px;line-height:1.65}.nlp3d-facade{inset:72px 5% 58px;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 32%,rgba(234,216,163,.08),transparent 42%),rgba(4,16,18,.55)}.nlp3d-facade img{object-fit:contain;object-position:center center;padding:12px;opacity:.97}.nlp3d-facade-hotspots{inset:12px;width:calc(100% - 24px);height:calc(100% - 24px)}.nlp3d-scene.has-facade .nlp3d-tower{opacity:.18}.nlp3d-detail{max-height:none}.nlp3d-facts{grid-template-columns:repeat(2,minmax(0,1fr));max-height:360px;overflow:auto;padding-inline-end:4px}.nlp3d-facts div:nth-last-child(-n+2){grid-column:1/-1}.nlp3d-facts dd{overflow-wrap:anywhere}.nlp3d-lead-form input,.nlp3d-lead-form select{min-width:0}.nlp3d-actions{gap:8px}.nlp3d-tool-panel{max-height:170px;overflow:auto}.nlp3d-tower:before{content:"";position:absolute;inset:-8px 6%;border:1px solid rgba(234,216,163,.22);background:linear-gradient(90deg,rgba(234,216,163,.05),transparent 45%,rgba(234,216,163,.08));transform:translateZ(-18px)}.nlp3d-plate{border-radius:2px}.nlp3d-plate:after{content:"";position:absolute;inset:3px 12%;background:repeating-linear-gradient(90deg,rgba(234,216,163,.45) 0 6px,transparent 6px 13px);opacity:.42}@media(max-width:1180px){.nlp3d-shell{grid-template-columns:1fr;grid-template-areas:"copy" "stage" "console"}.nlp3d-stage-wrap{min-height:680px}.nlp3d h2{max-width:100%}.nlp3d-lead-text{max-width:62ch}.nlp3d-console{display:grid;grid-template-columns:minmax(220px,.68fr) minmax(320px,1fr);align-items:start}.nlp3d-console-head,.nlp3d-floor-strip,.nlp3d-units{grid-column:1}.nlp3d-detail,.nlp3d-lead-form{grid-column:2}.nlp3d-detail{grid-row:1 / span 3}.nlp3d-lead-form{grid-row:4}}@media(max-width:760px){.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:calc(100vw - 18px);margin-inline:calc(50% - 50vw + 9px)}.nlp3d-shell{padding:16px}.nlp3d-stage-wrap{min-height:560px}.nlp3d-scene{height:540px}.nlp3d-facade{inset:64px 3% 46px}.nlp3d-facade img{padding:6px}.nlp3d-facade-hotspots{inset:6px;width:calc(100% - 12px);height:calc(100% - 12px)}.nlp3d-console{display:flex}.nlp3d-facts{grid-template-columns:1fr;max-height:none}.nlp3d-facts div:nth-last-child(-n+2){grid-column:auto}.nlp3d-toolbar{position:relative;top:auto;right:auto;margin-bottom:10px}.nlp3d-scene{position:relative}.nlp3d-copy{padding-inline:2px}.nlp3d-shop-path span{font-size:12px}}@media(max-width:420px){.nlp3d-stage-wrap{min-height:500px}.nlp3d-scene{height:500px}.nlp3d h2{font-size:28px}.nlp3d-metrics span{width:100%}}' );

		wp_add_inline_style( 'nadlan-p3d', '.nlp3d-plate{cursor:pointer}.nlp3d-plate:hover,.nlp3d-plate:focus-visible{border-color:#ffe9ad;background:linear-gradient(135deg,rgba(234,216,163,.5),rgba(255,255,255,.16));box-shadow:0 0 14px rgba(234,216,163,.3);outline:none}.nlp3d-scene:after{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 50% 38%,transparent 46%,rgba(2,10,10,.42) 100%)}.nlp3d-scene .nlp3d-horizon{box-shadow:0 0 38px 6px rgba(234,216,163,.1)}.nlp3d-viewframe{min-height:340px;border:1px solid rgba(234,216,163,.32);box-shadow:0 18px 48px rgba(0,0,0,.32)}.nlp3d-view-map{position:absolute;inset:0;z-index:2;cursor:grab}.nlp3d-view-map:active{cursor:grabbing}.nlp3d-view-map .mapboxgl-canvas{outline:none}.nlp3d-view-map .mapboxgl-cooperative-gesture-screen{display:none!important}.nlp3d-view-map .mapboxgl-ctrl-top-left{margin:10px}.nlp3d-view-map .mapboxgl-ctrl-group{background:rgba(7,15,16,.78);border:1px solid rgba(234,216,163,.34);box-shadow:0 4px 14px rgba(0,0,0,.42)}.nlp3d-view-map .mapboxgl-ctrl-group button{background:transparent;color:#fff;filter:invert(.92) hue-rotate(180deg)}.nlp3d-view-map .mapboxgl-ctrl-attrib{background:rgba(7,15,16,.62);color:#cfc29e;font-size:10px}.nlp3d-view-map .mapboxgl-ctrl-attrib a{color:#ffe8a6}.nlp3d-view-badge{position:absolute;z-index:4;top:10px;right:10px;background:linear-gradient(135deg,#ead8a3,#b99043);color:#15120c;font-weight:800;font-size:12px;padding:6px 10px;letter-spacing:.02em;box-shadow:0 6px 18px rgba(0,0,0,.42);pointer-events:none}.nlp3d-view-badge[hidden]{display:none}.nlp3d-view-copy{position:absolute;z-index:3;right:12px;left:12px;bottom:8px;margin:0;padding:9px 12px;background:linear-gradient(180deg,rgba(7,15,16,0),rgba(7,15,16,.82));color:#fff8dc;font-size:12.5px;line-height:1.5}.nlp3d-view-map .mapboxgl-canvas{outline:none}.nlp3d-viewframe{min-height:240px}.nlp3d-view-copy{z-index:3}.nlp3d-unit-row{display:grid;grid-template-columns:1fr auto;gap:7px;align-items:stretch}.nlp3d-compare-add{border:1px solid rgba(234,216,163,.26);background:rgba(255,255,255,.05);color:#e9dcb4;font-size:12px;padding:6px 9px;cursor:pointer;min-width:58px}.nlp3d-compare-add.is-on,.nlp3d-compare-add:hover,.nlp3d-compare-add:focus-visible{background:rgba(234,216,163,.22);color:#fff;outline:none}.nlp3d-compare-tray{display:flex;flex-wrap:wrap;align-items:center;gap:8px;border:1px solid rgba(234,216,163,.2);background:rgba(0,0,0,.18);padding:9px 11px;margin-top:2px}.nlp3d-compare-tray[hidden]{display:none}.nlp3d-compare-label{color:#cfc29e;font-size:12px}.nlp3d-compare-chip{border:1px solid rgba(234,216,163,.3);background:rgba(234,216,163,.14);color:#fff3c8;font-size:12px;padding:5px 9px;cursor:pointer}.nlp3d-compare-open{border:1px solid rgba(234,216,163,.4);background:linear-gradient(135deg,rgba(234,216,163,.28),rgba(185,144,67,.22));color:#fff;font-size:13px;padding:7px 12px;cursor:pointer;margin-inline-start:auto}.nlp3d-compare-open:disabled{opacity:.5;cursor:default}.nlp3d-overlay{position:fixed;inset:0;z-index:99990;display:flex;align-items:center;justify-content:center;background:rgba(4,12,12,.78);backdrop-filter:blur(6px);padding:18px}.nlp3d-overlay[hidden]{display:none}.nlp3d-overlay-box{position:relative;width:min(860px,100%);max-height:86vh;overflow:auto;background:linear-gradient(135deg,#0a1d1d,#13100b);border:1px solid rgba(234,216,163,.32);box-shadow:0 32px 90px rgba(0,0,0,.5);padding:22px;color:#f6efe2}.nlp3d-overlay-box h3{margin:0 0 14px;font-family:Georgia,"Times New Roman",serif;font-weight:500;font-size:24px;color:#ffe9ad}.nlp3d-overlay-close{position:absolute;top:10px;left:12px;border:1px solid rgba(234,216,163,.34);background:rgba(255,255,255,.06);color:#ffe8a6;width:38px;height:38px;font-size:19px;cursor:pointer}.nlp3d-compare-table table{width:100%;border-collapse:collapse}.nlp3d-compare-table th,.nlp3d-compare-table td{border:1px solid rgba(234,216,163,.18);padding:9px 10px;text-align:right;font-size:13.5px}.nlp3d-compare-table td:first-child{color:#cfc29e;font-size:12.5px;width:120px}.nlp3d-compare-pick{border:1px solid rgba(234,216,163,.36);background:rgba(234,216,163,.14);color:#fff;font-weight:700;padding:8px 10px;cursor:pointer;width:100%}.nlp3d-compare-pick:hover,.nlp3d-compare-pick:focus-visible{background:rgba(234,216,163,.3);outline:none}.nlp3d-plan-body img{display:block;width:100%;height:auto;background:#fff}.nlp3d-plan-body iframe{display:block;width:100%;height:64vh;border:0;background:#fff}.nlp3d-wdots{grid-column:1/-1;display:flex;gap:7px;margin:0 0 2px}.nlp3d-wdots span{width:26px;height:5px;background:rgba(234,216,163,.18)}.nlp3d-wdots span.is-on{background:linear-gradient(90deg,#ead8a3,#b99043)}.nlp3d-wstep{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:10px}.nlp3d-wstep[hidden]{display:none}.nlp3d-wnext{grid-column:1/-1;border:0;background:linear-gradient(135deg,#ead8a3,#b99043);color:#15120c;font-weight:800;padding:12px 14px;cursor:pointer}.nlp3d-wback{grid-column:1/-1;border:0;background:transparent;color:#cfc29e;font-size:12.5px;cursor:pointer;text-decoration:underline;padding:4px}.nlp3d-advisors{grid-column:1/-1;border:1px solid rgba(234,216,163,.2);padding:10px 12px;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:8px}.nlp3d-advisors legend{color:#e9dcb4;font-size:12.5px;padding:0 6px}.nlp3d-advisors label{display:flex;align-items:center;gap:7px;color:#fff3d0;font-size:13px;min-height:30px;cursor:pointer}.nlp3d-advisors input{width:17px;height:17px;accent-color:#c4a15a}.nlp3d-deal-steps span.is-done{background:rgba(120,180,120,.2);border-color:rgba(160,220,160,.45);color:#dfffe0}.nlp3d-deal-steps span.is-done:before{content:"✓ "}@media(max-width:600px){.nlp3d-wstep,.nlp3d-advisors{grid-template-columns:1fr}.nlp3d-overlay{padding:8px}.nlp3d-overlay-box{padding:16px;max-height:92vh}.nlp3d-compare-table th,.nlp3d-compare-table td{padding:7px 7px;font-size:12.5px}.nlp3d-viewframe{min-height:200px}}' );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_flagship_css() );
		wp_add_inline_style( 'nadlan-p3d', '.nlp3d-selection-dock{border:1px solid rgba(234,216,163,.24);background:linear-gradient(135deg,rgba(255,255,255,.09),rgba(255,255,255,.035));box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 16px 34px rgba(0,0,0,.16);padding:14px 14px;margin-bottom:14px;display:grid;grid-template-columns:1fr auto;gap:8px 12px;align-items:center}.nlp3d-selection-dock span{grid-column:1/-1;color:#c4a15a;font-size:12px;letter-spacing:.04em}.nlp3d-dock-title{font-family:Georgia,"Times New Roman",serif;color:#fff5cf;font-size:21px;font-weight:500;line-height:1.15}.nlp3d-dock-meta{display:block;color:#d8ccb0;line-height:1.45}.nlp3d-dock-actions{display:flex;gap:8px;align-items:center;justify-content:flex-end}.nlp3d-dock-actions button{border:1px solid rgba(234,216,163,.34);background:rgba(255,255,255,.055);color:#ffe8a6;min-height:38px;padding:7px 11px;cursor:pointer}.nlp3d-dock-actions .nlp3d-dock-action{background:linear-gradient(135deg,#ead8a3,#b99043);border:0;color:#15120c;font-weight:800}.nlp3d-dock-actions button:hover,.nlp3d-dock-actions button:focus-visible{outline:2px solid rgba(255,255,255,.68);outline-offset:2px;filter:brightness(1.06)}@media(max-width:760px){.nlp3d-selection-dock{grid-template-columns:1fr}.nlp3d-dock-actions{justify-content:stretch}.nlp3d-dock-actions button{flex:1}}' );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_stability_css() );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_app_selector_css() );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_showroom_css() );
		wp_add_inline_style( 'nadlan-p3d', '.nlp3d.nlp3d-premium .nlp3d-stage-card[hidden]{display:none!important}.nlp3d.nlp3d-premium .nlp3d-stage-card{pointer-events:none!important;top:76px!important;right:18px!important;left:auto!important;bottom:auto!important;width:min(360px,calc(100% - 36px))!important;grid-template-columns:1fr!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button,.nlp3d.nlp3d-premium .nlp3d-stage-card a{pointer-events:auto!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats,.nlp3d.nlp3d-premium .nlp3d-stage-card-actions{grid-column:1!important}@media(max-width:760px){.nlp3d.nlp3d-premium .nlp3d-stage-card:not([hidden]){position:relative!important;top:auto!important;right:auto!important;left:auto!important;bottom:auto!important;width:auto!important;max-height:none!important;overflow:visible!important;margin-top:10px!important}.nlp3d.nlp3d-premium .nlp3d-stage-card-stats,.nlp3d.nlp3d-premium .nlp3d-stage-card-actions{grid-template-columns:1fr!important}}' );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_showroom_v162_css() );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_showroom_v162_mobile_card_css() );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_showroom_v162_material_css() );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_showroom_v1621_css() );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_model_viewer_css() );
		wp_add_inline_style( 'nadlan-p3d', '.nlp3d.nlp3d-premium .nlp3d-scene.has-model-viewer .nlp3d-tower{z-index:10!important;opacity:.86!important;bottom:178px!important;pointer-events:none!important}.nlp3d.nlp3d-premium .nlp3d-scene.has-model-viewer .nlp3d-facade{z-index:10!important;opacity:.66!important;pointer-events:none!important}.nlp3d.nlp3d-premium.has-model-viewer-loaded .nlp3d-scene.has-model-viewer .nlp3d-tower{opacity:.86!important}.nlp3d.nlp3d-premium.has-model-viewer-loaded .nlp3d-scene.has-model-viewer .nlp3d-facade{opacity:.66!important}.nlp3d.nlp3d-premium .nlp3d-model-viewer{background:transparent!important;--interaction-prompt-display:none}.nlp3d.nlp3d-premium .nlp3d-model-viewer .nlp3d-mv-hotspot{pointer-events:auto!important}@media(max-width:760px){.nlp3d.nlp3d-premium .nlp3d-scene.has-model-viewer .nlp3d-tower{bottom:128px!important}}' );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_showroom_v1631_a11y_css() );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_showroom_v1633_contact_css() );

		$post_id = is_singular( 'nadlan_project' ) ? (int) get_queried_object_id() : 0;
		if ( $post_id > 0 && get_post_meta( $post_id, 'project_model_glb', true ) !== '' ) {
			wp_register_script( 'nadlan-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js', array(), '4.3.1', true );
			wp_script_add_data( 'nadlan-model-viewer', 'type', 'module' );
			wp_enqueue_script( 'nadlan-model-viewer' );
		}

		wp_register_script( 'nadlan-p3d', '', array(), '1.63.8', true );
		wp_enqueue_script( 'nadlan-p3d' );
		wp_add_inline_script( 'nadlan-p3d', nadlan_p3d_inline_js( esc_url_raw( rest_url( 'nadlan/v1/lead' ) ) ) );
	}
);

add_filter(
	'the_content',
	function ( $content ) {
		if ( ! nadlan_p3d_enabled() || ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}

		$pid = get_the_ID();
		if ( ! nadlan_p3d_has_data( $pid ) ) {
			return $content;
		}

		return nadlan_p3d_insert_after_project_header( $content, nadlan_p3d_render( $pid ) );
	},
	6
);

add_action(
	'add_meta_boxes',
	function () {
		if ( ! nadlan_p3d_enabled() ) {
			return;
		}

		add_meta_box(
			'nadlan-p3d',
			'בחירת דירות אינטראקטיבית',
			function ( $post ) {
				wp_nonce_field( 'nadlan_p3d_save', 'nadlan_p3d_nonce' );
				$img = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_image', true ) );
				$vb  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_viewbox', true ) );
				$fh  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_floor_height_m', true ) );
				$gm  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_ground_elevation_m', true ) );
				$ap  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_avg_price_per_sqm', true ) );
				$psn = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_price_source_note', true ) );
				$mt  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_model_type', true ) );
				$glb = esc_attr( (string) get_post_meta( $post->ID, 'project_model_glb', true ) );
				$usdz = esc_attr( (string) get_post_meta( $post->ID, 'project_model_usdz', true ) );
				$poster = esc_attr( (string) get_post_meta( $post->ID, 'project_model_poster', true ) );
				$vu  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_video_url', true ) );
				$tu  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_tour_url', true ) );
				$cu  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_cesium_tiles_url', true ) );
				$dr  = esc_textarea( (string) get_post_meta( $post->ID, 'project_3d_drawings_json', true ) );
				$env = esc_textarea( (string) get_post_meta( $post->ID, 'project_3d_environment_json', true ) );
				$js  = esc_textarea( (string) get_post_meta( $post->ID, 'project_3d_units', true ) );
				$dm  = get_post_meta( $post->ID, 'project_3d_demo', true ) === '1';
				echo '<p><label>כתובת תמונת מקור או הדמיה מאושרת<br><input type="url" name="project_3d_image" value="' . $img . '" class="widefat"></label></p>';
				echo '<p><label>viewBox למצב שכבת SVG ישנה, אם קיים<br><input type="text" name="project_3d_viewbox" value="' . $vb . '" class="widefat"></label></p>';
				echo '<p><label>גובה קומה במטרים לחישוב מבט מהדירה<br><input type="number" step="0.01" min="2.4" max="5" name="project_3d_floor_height_m" value="' . $fh . '" class="widefat" placeholder="3.05"></label></p>';
				echo '<p><label>גובה קרקע משוער במטרים, אם ידוע<br><input type="number" step="0.1" min="-50" max="400" name="project_3d_ground_elevation_m" value="' . $gm . '" class="widefat" placeholder="0"></label></p>';
				echo '<p><label>אומדן מחיר ממוצע למ"ר, אופציונלי בלבד<br><input type="number" step="1" min="0" name="project_3d_avg_price_per_sqm" value="' . $ap . '" class="widefat" placeholder="0"></label></p>';
				echo '<p><label>מקור/הערה לאומדן מחיר<br><input type="text" name="project_3d_price_source_note" value="' . $psn . '" class="widefat" placeholder="אומדן לא מחייב לפי מקור מאושר"></label></p>';
				echo '<p><label>Model type: procedural / facade / sprite360 / gltf / bim<br><input type="text" name="project_3d_model_type" value="' . $mt . '" class="widefat" placeholder="procedural"></label></p>';
				echo '<p><label>GLB model URL for real 3D showroom<br><input type="url" name="project_model_glb" value="' . $glb . '" class="widefat" placeholder="https://.../project.glb"></label></p>';
				echo '<p><label>USDZ model URL for iOS AR, optional<br><input type="url" name="project_model_usdz" value="' . $usdz . '" class="widefat" placeholder="https://.../project.usdz"></label></p>';
				echo '<p><label>Model poster image URL, optional lightweight WebP/JPG<br><input type="url" name="project_model_poster" value="' . $poster . '" class="widefat" placeholder="https://.../poster.webp"></label></p>';
				echo '<p><label>Sales video URL<br><input type="url" name="project_3d_video_url" value="' . $vu . '" class="widefat"></label></p>';
				echo '<p><label>Interior or 3D tour URL<br><input type="url" name="project_3d_tour_url" value="' . $tu . '" class="widefat"></label></p>';
				echo '<p><label>Future Cesium / Google 3D Tiles URL<br><input type="url" name="project_3d_cesium_tiles_url" value="' . $cu . '" class="widefat"></label></p>';
				echo '<p><label>Drawings JSON: [{"label":"...","url":"...","type":"plan"}]<br><textarea name="project_3d_drawings_json" rows="5" class="widefat code">' . $dr . '</textarea></label></p>';
				echo '<p><label>Environment JSON: [{"label":"...","detail":"...","url":"..."}]<br><textarea name="project_3d_environment_json" rows="5" class="widefat code">' . $env . '</textarea></label></p>';
				echo '<p><label>יחידות JSON: id, title, floor, rooms, sqm, balcony, dir, line, view, price, price_estimate, status, plan, interior_url, tour_url, view_note, hotspot_position, hotspot_normal, camera_orbit<br><textarea name="project_3d_units" rows="10" class="widefat code">' . $js . '</textarea></label></p>';
				echo '<p><label><input type="checkbox" name="project_3d_demo" value="1" ' . checked( $dm, true, false ) . '> הצג מודל הדגמה כאשר אין מלאי רשמי</label></p>';
				echo '<p class="description">במצב הדגמה המחיר מוצג "לפי פנייה" כדי לא להציג נתוני מכירה לא מאומתים.</p>';
			},
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
		update_post_meta( $post_id, 'project_3d_drawings_json', nadlan_p3d_sanitize_material_json( wp_unslash( $_POST['project_3d_drawings_json'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_environment_json', nadlan_p3d_sanitize_material_json( wp_unslash( $_POST['project_3d_environment_json'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_units', nadlan_p3d_sanitize_units_json( wp_unslash( $_POST['project_3d_units'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_demo', ! empty( $_POST['project_3d_demo'] ) ? '1' : '0' );
	}
);

add_filter(
	'nadlan_config_healthcheck',
	function ( $out ) {
		$q = new WP_Query(
			array(
				'post_type'      => 'nadlan_project',
				'post_status'    => 'any',
				'fields'         => 'ids',
				'posts_per_page' => 1,
				'meta_query'     => array(
					'relation' => 'OR',
					array( 'key' => 'project_3d_units', 'compare' => 'EXISTS' ),
					array( 'key' => 'project_model_glb', 'compare' => 'EXISTS' ),
					array( 'key' => 'project_3d_demo', 'value' => '1' ),
				),
			)
		);
		$model_q = new WP_Query(
			array(
				'post_type'      => 'nadlan_project',
				'post_status'    => 'any',
				'fields'         => 'ids',
				'posts_per_page' => 1,
				'meta_query'     => array(
					array(
						'key'     => 'project_model_glb',
						'value'   => '',
						'compare' => '!=',
					),
				),
			)
		);
		$out['project_3d'] = array(
			'enabled'          => nadlan_p3d_enabled(),
			'renderer'         => 'premium_showroom_v9_model_viewer',
			'lead_endpoint'    => '/nadlan/v1/lead',
			'facade_polygons'  => true,
			'lead_unit_payload' => true,
			'view_from_unit'   => trim( (string) get_option( 'nadlan_mapbox_token', '' ) ) !== '' ? 'mapbox_live' : 'awaiting_token',
			'mapbox_canvas_fix' => true,
			'mapbox_default'   => 'user_open_only',
			'layout_contained'  => true,
			'app_selector'     => true,
			'showroom_v2'      => true,
			'cms_material_fields' => true,
			'cms_material_cards'  => true,
			'cms_material_sanitized' => true,
			'unit_meta_rest' => true,
			'hit_targets'      => true,
			'tap_target_min_px' => 44,
			'model_zoom_tilt'  => true,
			'model_full_360'   => true,
			'model_viewer_ready' => true,
			'model_viewer_module_tag' => true,
			'model_viewer_reveal' => 'auto',
			'model_viewer_loading' => 'auto',
			'model_viewer_version' => '4.3.1',
			'model_viewer_lazy' => true,
			'model_viewer_hotspots' => true,
			'showroom_first_view' => true,
			'static_featured_image_suppressed' => true,
			'floating_actions_clear' => true,
			'floating_action_rail_v1633' => true,
			'cesium_ready'     => true,
			'zillow_parity'    => array(
				'floor_plans'  => true,
				'unit_picker'  => true,
				'view_layer'   => true,
				'media'        => true,
				'surroundings' => true,
			),
			'stage_unit_card'  => true,
			'nested_scrollbars' => false,
			'stage_live_view'   => true,
			'flagship_showcase' => true,
			'owner_request_form' => true,
			'selection_dock'   => true,
			'sun_insight'      => true,
			'unit_compare'     => true,
			'lead_wizard'      => true,
			'reservation_state' => 'non_binding_inquiry',
			'projects_with_3d' => (int) $q->found_posts,
			'projects_with_glb' => (int) $model_q->found_posts,
		);
		wp_reset_postdata();
		return $out;
	}
);
