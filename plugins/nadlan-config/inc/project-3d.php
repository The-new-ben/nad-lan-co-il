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

			$status = sanitize_key( (string) ( $u['status'] ?? 'available' ) );
			if ( ! in_array( $status, array( 'available', 'reserved', 'sold' ), true ) ) {
				$status = 'available';
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
		$has_real_facade_asset = ! empty( $meta['facade_images'] );
		$has_embedded_facade = $has_real_facade_asset || ! empty( $meta['site_plan_image'] ) || ! empty( $meta['site_plan_polygons'] );
		// No silent fallbacks: emit the legacy facade only when it is the intentional primary surface.
		$image_is_placeholder = $image !== '' && (bool) preg_match( '/(?:prototype|placeholder|rainbow-facade-demo|facade-demo)/i', $image );
		$render_legacy_facade = $image !== '' && ! $has_embedded_facade && ! $image_is_placeholder;
		$showroom_poster = esc_url( (string) ( $meta['model_poster'] ?? '' ) );
		$project_title = $meta['title'] ? (string) $meta['title'] : 'הפרויקט';
		$project_place = $meta['address'] ? (string) $meta['address'] : ( $meta['city'] ? (string) $meta['city'] : '' );
		$project_place_phrase = $project_place !== '' ? ' באזור ' . $project_place : '';
		$project_developer_sentence = $meta['developer'] ? ' היזם: ' . (string) $meta['developer'] . '.' : '';
		$project_kicker = $project_title . ( $project_place !== '' ? ' · ' . $project_place : '' );
		$project_intro_copy = $project_title . ' מוצג כאן כסיור פרויקט חי' . $project_place_phrase . '. רואים את הבניין, בוחרים דירה, בודקים קומה, כיוון ונוף, ושולחים פנייה עם הדירה המדויקת שנבחרה.' . $project_developer_sentence;
		$project_lead_copy = 'סיור הפרויקט של ' . $project_title . $project_place_phrase . ' מחבר בין מודל הבניין, בחירת דירה, מבט מהדירה, תוכניות וליווי מקצועי. כאשר היזם מעלה חומרים רשמיים, הם מתחברים לאותה דירה ולאותה פנייה.';

		$camera_min_polar = esc_attr( (string) ( $meta['camera_min_polar'] ?? '78deg' ) );
		$camera_max_polar = esc_attr( (string) ( $meta['camera_max_polar'] ?? '85deg' ) );
		$camera_mid_polar = esc_attr( (string) ( $meta['camera_mid_polar'] ?? '81.5deg' ) );
		$camera_rotation  = esc_attr( (string) ( $meta['camera_rotation_per_second'] ?? '8deg' ) );
		$camera_auto      = ! empty( $meta['camera_auto_rotate'] );

		ob_start();
		?>
<!-- nlp3d-start -->
<?php if ( $showroom_poster ) : ?>
<figure class="nlp3d-hero-media" dir="rtl" aria-label="תמונת פרויקט עם תצוגת דירות">
	<img src="<?php echo $showroom_poster; ?>" alt="<?php echo esc_attr( $meta['title'] . ' - הדמיית פרויקט ובחירת דירה בתלת ממד' ); ?>" loading="eager" fetchpriority="high">
	<figcaption><strong><?php echo esc_html( $meta['title'] ); ?></strong><span>מודל תלת ממדי ובחירת דירה זמינים בעמוד</span></figcaption>
</figure>
<?php endif; ?>
<section class="nadlan-guide nlp3d-intro" dir="rtl" aria-label="פתיחת תצוגת דירות">
	<div class="wrap">
		<span class="eyebrow">סיור פרויקט למשקיעים ולרוכשים</span>
		<h2><?php echo esc_html( $project_title ); ?>: בוחרים דירה מתוך הפרויקט</h2>
		<p><?php echo esc_html( $project_intro_copy ); ?></p>
		<p class="nlp3d-intro-cta"><a href="#nlp3d-stage" class="btn">בחרו דירה עכשיו</a></p>
	</div>
</section>
<section class="nlp3d nlp3d-premium alignfull" dir="rtl" data-project="<?php echo esc_attr( $post_id ); ?>" aria-labelledby="<?php echo esc_attr( $uid ); ?>-title">
	<div class="nlp3d-grid" aria-hidden="true"></div>
	<div class="nlp3d-shell">
		<div class="nlp3d-copy">
			<p class="nlp3d-kicker"><?php echo esc_html( $project_kicker ); ?></p>
			<h2 id="<?php echo esc_attr( $uid ); ?>-title">סיור בפרויקט <?php echo esc_html( $meta['title'] ); ?></h2>
			<p class="nlp3d-lead-text"><?php echo esc_html( $project_lead_copy ); ?></p>
			<div class="nlp3d-shop-path" aria-label="תהליך בחירה">
				<span>1. רואים את הבניין</span>
				<span>2. בוחרים דירה</span>
				<span>3. בודקים נוף ותוכנית</span>
				<span>4. מבקשים שיחה</span>
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

		<div class="nlp3d-stage-wrap" id="nlp3d-stage">
			<div class="nlp3d-toolbar" aria-label="שליטה במודל">
				<button type="button" class="nlp3d-angle is-active" data-angle="-32" data-action="angle-facade">מבט ראשי</button>
				<button type="button" class="nlp3d-angle" data-angle="0" data-action="angle-sea">ים</button>
				<button type="button" class="nlp3d-angle" data-angle="32" data-action="angle-city">עיר</button>
				<button type="button" class="nlp3d-orbit" data-orbit="1" data-action="orbit-building">סובב מודל</button>
				<button type="button" class="nlp3d-zoom" data-zoom="in" data-action="zoom-in">קרב</button>
				<button type="button" class="nlp3d-zoom" data-zoom="out" data-action="zoom-out">הרחק</button>
				<span class="nlp3d-drag-note">בחרו דירה על המגדל</span>
				<button type="button" class="nlp3d-fp-restore" data-action="facade-restore" hidden>הצג חזית</button>
			</div>
			<div class="nlp3d-scene<?php echo $has_model_viewer ? ' has-model-viewer' : ''; ?>" style="--angle:-32deg" role="group" aria-label="מודל תלת ממדי סכמטי של מגדל מגורים">
				<?php if ( $has_model_viewer ) : ?>
					<model-viewer
						class="nlp3d-model-viewer"
						src="<?php echo esc_url( $meta['model_glb'] ); ?>"
						<?php if ( ! empty( $meta['model_poster'] ) ) : ?>poster="<?php echo esc_url( $meta['model_poster'] ); ?>"<?php endif; ?>
						<?php if ( ! empty( $meta['model_usdz'] ) ) : ?>ios-src="<?php echo esc_url( $meta['model_usdz'] ); ?>"<?php endif; ?>
						alt="<?php echo esc_attr( 'מודל תלת ממדי של ' . $meta['title'] ); ?>"
						reveal="auto"
						loading="auto"
						camera-controls
						<?php if ( $camera_auto ) : ?>
						auto-rotate
						auto-rotate-delay="3500"
						rotation-per-second="<?php echo $camera_rotation; ?>"
						<?php endif; ?>
						min-camera-orbit="-Infinity <?php echo $camera_min_polar; ?> auto"
						max-camera-orbit="Infinity <?php echo $camera_max_polar; ?> auto"
						camera-orbit="34deg <?php echo $camera_mid_polar; ?> 32m"
						field-of-view="18deg"
						camera-target="0m 56m 0m"
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
							$unit_status       = sanitize_key( (string) ( $unit['status'] ?? 'available' ) );
							$unit_status_label = nadlan_p3d_status_label( $unit_status );
							$hotspot_title = $unit['title'] ? $unit['title'] : $unit['id'];
							?>
							<button
								type="button"
								class="nlp3d-mv-hotspot nlp3d-hotspot-hit nlp3d-status-<?php echo esc_attr( $unit_status ); ?> is-<?php echo esc_attr( $unit_status ); ?><?php echo ! empty( $unit['recommended'] ) ? ' is-recommended' : ''; ?>"
								slot="<?php echo esc_attr( 'hotspot-' . sanitize_html_class( (string) $unit['id'] ) ); ?>"
								data-position="<?php echo esc_attr( $hotspot_position ); ?>"
								data-normal="<?php echo esc_attr( $hotspot_normal ); ?>"
								data-visibility-attribute="visible"
								data-unit="<?php echo esc_attr( $unit['id'] ); ?>"
								aria-hidden="true"
								tabindex="-1"
								aria-label="<?php echo esc_attr( sprintf( 'דירה %s, קומה %s, %s חדרים, %s', $unit['id'], $unit['floor'] ?? '', $unit['rooms'] ?? '', $unit_status_label ) ); ?>"
								<?php echo $unit_status === 'sold' ? 'aria-disabled="true"' : ''; ?>>
								<span class="nlp3d-hotspot-dot" aria-hidden="true"></span>
								<span class="nlp3d-mv-label nlp3d-hotspot-tag"><?php echo esc_html( $hotspot_title ); ?></span>
								<span class="nlp3d-hotspot-tip" role="tooltip">
									<strong><?php echo esc_html( $hotspot_title ); ?> · <?php echo esc_html( $unit['rooms'] ?? '' ); ?> חד׳</strong>
									<small><?php echo esc_html( $unit['sqm'] ?? '' ); ?> מ"ר · <?php echo esc_html( $unit['view'] ?? ( $unit['dir'] ?? '' ) ); ?></small>
									<small><?php echo esc_html( $unit_status_label ); ?><?php echo ! empty( $unit['recommended'] ) ? ' · ' . esc_html( $unit['recommended_label'] ?? 'פופולרי' ) : ''; ?></small>
									<?php if ( ! empty( $unit['price_estimate'] ) ) : ?><small class="nlp3d-price">אומדן <?php echo esc_html( (string) $unit['price_estimate'] ); ?> · לא מחייב</small><?php endif; ?>
								</span>
							</button>
						<?php endforeach; ?>
					</model-viewer>
					<div class="nlp3d-model-error" role="status" aria-live="polite" hidden>התצוגה התלת ממדית לא נטענה כרגע. נציג חומר מאושר כאשר יעלה לפרויקט.</div>
				<?php endif; ?>
				<div class="nlp3d-horizon"></div>
				<div class="nlp3d-sea"></div>
				<div class="nlp3d-park"></div>
				<div class="nlp3d-runway"></div>
				<div class="nlp3d-tower" role="group" aria-label="בחירת קומה ישירות מהמגדל"></div>
				<div class="nlp3d-shadow" aria-hidden="true"></div>
				<?php if ( $render_legacy_facade ) : ?>
					<figure class="nlp3d-facade" data-viewbox="<?php echo esc_attr( $viewbox ); ?>">
						<button type="button" class="nlp3d-fp-close" data-action="facade-dismiss" aria-label="הסתר חזית">×</button>
						<img src="<?php echo $image; ?>" alt="<?php echo esc_attr( $image_alt ); ?>" loading="lazy">
						<svg class="nlp3d-facade-hotspots" viewBox="<?php echo esc_attr( $viewbox ); ?>" preserveAspectRatio="none" aria-label="בחירת דירה על גבי החזית"></svg>
						<figcaption><?php echo esc_html( $image_cap ); ?></figcaption>
					</figure>
				<?php endif; ?>
				<p class="nlp3d-context-caption">הדמיית סביבת שדה דב, להמחשה.</p>
				<div class="nlp3d-sun-orbit" aria-hidden="true"><span class="nlp3d-sun-dot"></span></div>
				<?php
				$context_items = array_slice( (array) ( $meta['environment'] ?? array() ), 0, 4 );
				if ( $context_items ) :
					?>
					<div class="nlp3d-context-pins" aria-hidden="true">
						<?php foreach ( $context_items as $index => $item ) : ?>
							<span class="nlp3d-context-pin nlp3d-context-pin-<?php echo esc_attr( (string) ( $index + 1 ) ); ?>"><?php echo esc_html( (string) ( $item['label'] ?? $item['name'] ?? $item['title'] ?? 'סביבה' ) ); ?></span>
						<?php endforeach; ?>
					</div>
				<?php endif; ?>
			</div>
			<div class="nlp3d-viewframe nlp3d-stage-viewframe" hidden>
				<div class="nlp3d-view-sky"></div>
				<div class="nlp3d-view-lines"></div>
				<div class="nlp3d-view-map" hidden aria-label="מבט חי מגובה הדירה"></div>
				<span class="nlp3d-view-badge" hidden>מבט חי · גרירה לסיבוב</span>
				<button type="button" class="nlp3d-stage-return" data-action="return-model">חזרה למודל</button>
				<p class="nlp3d-view-copy"></p>
			</div>
			<div class="nlp3d-stage-card" aria-live="polite" hidden>
				<button type="button" class="nlp3d-stage-card-close" data-action="stage-card-close" aria-label="סגירת פרטי הדירה">×</button>
				<span class="nlp3d-stage-kicker">הדירה שנבחרה</span>
				<strong class="nlp3d-stage-card-title">בחרו דירה על הבניין</strong>
				<small class="nlp3d-stage-card-meta">בחרו קומה ודירה כדי לראות מחיר, נוף ותוכנית כאשר הם זמינים.</small>
				<div class="nlp3d-stage-card-tags" aria-label="סימוני דירה"></div>
				<div class="nlp3d-stage-card-stats" aria-label="פרטי דירה נבחרת">
					<span class="nlp3d-stage-price">לפי פנייה</span>
					<span class="nlp3d-stage-status">בחירה פתוחה</span>
					<span class="nlp3d-stage-view">מבט לפי כיוון</span>
				</div>
				<p class="nlp3d-stage-card-note">בחרו דירה כדי לראות את פעולות ההמשך.</p>
				<div class="nlp3d-stage-card-actions">
					<button type="button" class="nlp3d-stage-details" data-action="stage-details">פרטים מלאים</button>
					<button type="button" class="nlp3d-stage-view-btn" data-action="stage-view">מבט מהדירה</button>
					<button type="button" class="nlp3d-stage-tour" data-action="stage-tour">תוכניות וסיור</button>
					<button type="button" class="nlp3d-stage-inquiry" data-action="stage-inquiry">דברו עם היזם</button>
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
				<p class="nlp3d-legal">הפנייה נשמרת עם הדירה שנבחרה. נציג יחזור עם זמינות, מחיר ותנאים כפי שיימסרו מהיזם.</p>
				<p class="nlp3d-ok" hidden></p>
			</form>
		</aside>
	</div>
	<div class="nlp3d-showcase" aria-label="תצוגת עומק לפרויקט">
		<div class="nlp3d-showcase-copy">
			<p class="nlp3d-kicker">מעמוד פרויקט לעמדת בחירה</p>
			<h3>כל החלטה מתחילה ממבט ברור יותר על הדירה</h3>
			<p>העמוד מחבר בין מודל הבניין, בחירת דירה, מבט מהדירה, שעות שמש, השוואת יחידות ובקשת ליווי מקצועי. הכל נבנה כדי שהרוכש יבין את הדירה לפני השיחה, והיזם יקבל פנייה מדויקת יותר.</p>
		</div>
		<div class="nlp3d-showcase-cards" aria-label="יכולות תצוגה">
			<article>
				<span>01</span>
				<strong>בחירת דירה</strong>
				<p>בחירת קומה ודירה מתוך הפרויקט, כולל קו, שטח, כיוון ונוף.</p>
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

if ( ! function_exists( 'nadlan_p3d_lovable_showroom_v1690_css' ) ) {
	function nadlan_p3d_lovable_showroom_v1690_css() {
		return <<<'CSS'
/* v1.69.6: public showroom surface. */
@font-face{font-family:"Frank Ruhl Libre";font-style:normal;font-weight:400;font-display:swap;src:url("/wp-content/themes/nadlan-revenue/assets/fonts/frank-ruhl-libre/frl-400.woff2") format("woff2")}
@font-face{font-family:"Frank Ruhl Libre";font-style:normal;font-weight:500;font-display:swap;src:url("/wp-content/themes/nadlan-revenue/assets/fonts/frank-ruhl-libre/frl-500.woff2") format("woff2")}
@font-face{font-family:"Frank Ruhl Libre";font-style:normal;font-weight:700;font-display:swap;src:url("/wp-content/themes/nadlan-revenue/assets/fonts/frank-ruhl-libre/frl-700.woff2") format("woff2")}
@font-face{font-family:"Heebo";font-style:normal;font-weight:300;font-display:swap;src:url("/wp-content/themes/nadlan-revenue/assets/fonts/heebo/heebo-300.woff2") format("woff2")}
@font-face{font-family:"Heebo";font-style:normal;font-weight:400;font-display:swap;src:url("/wp-content/themes/nadlan-revenue/assets/fonts/heebo/heebo-400.woff2") format("woff2")}
@font-face{font-family:"Heebo";font-style:normal;font-weight:500;font-display:swap;src:url("/wp-content/themes/nadlan-revenue/assets/fonts/heebo/heebo-500.woff2") format("woff2")}
@font-face{font-family:"Heebo";font-style:normal;font-weight:700;font-display:swap;src:url("/wp-content/themes/nadlan-revenue/assets/fonts/heebo/heebo-700.woff2") format("woff2")}
.nlp3d.nlp3d-premium{
--cream:#FAF7F1;
--ink:#1B1A17;
--gold:#9C7A3C;
--terracotta:#C2563A;
--sage:#7A8F6A;
--background:#FAF7F1;
--foreground:#1B1A17;
--card:#FBF9F4;
--card-foreground:#1B1A17;
--muted:#EFEAE0;
--muted-foreground:#6B6457;
--border:#D9D2C4;
--radius:0.25rem;
--shadow-card:0 8px 24px -12px rgba(27,26,23,.18);
--font-serif-he:"Frank Ruhl Libre","Frank Ruehl CLM",Georgia,serif;
--font-sans-he:"Heebo","Assistant",system-ui,sans-serif;
--lh-tight:1.15;
--tracking-tight:-0.01em;
--nlp3d-cream:#faf7f1;
--nlp3d-paper:#fffdf8;
--nlp3d-ink:#1b1a17;
--nlp3d-muted:#645c4e;
--nlp3d-line:#ded4c4;
--nlp3d-gold:#9c7a3c;
--nlp3d-terracotta:#c2563a;
--nlp3d-sage:#7a8f6a;
background:var(--nlp3d-cream)!important;
color:var(--nlp3d-ink)!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:6px!important;
box-shadow:0 22px 70px rgba(42,34,22,.12)!important;
overflow:hidden!important;
font-family:var(--font-sans-he)!important;
font-feature-settings:"ss01","kern";
-webkit-font-smoothing:antialiased;
}
.entry-content>.nlp3d.nlp3d-premium,
.wp-block-post-content>.nlp3d.nlp3d-premium{
width:min(1180px,calc(100vw - 32px))!important;
max-width:none!important;
margin:24px auto 52px!important;
transform:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-grid,
.nlp3d.nlp3d-premium .nlp3d-horizon,
.nlp3d.nlp3d-premium .nlp3d-sea,
.nlp3d.nlp3d-premium .nlp3d-park,
.nlp3d.nlp3d-premium .nlp3d-runway,
.nlp3d.nlp3d-premium .nlp3d-shadow,
.nlp3d.nlp3d-premium .nlp3d-sun-orbit,
.nlp3d.nlp3d-premium .nlp3d-tower{display:none!important}
.nlp3d.nlp3d-premium .nlp3d-shell{
display:grid!important;
grid-template-columns:minmax(0,1fr) minmax(300px,360px)!important;
grid-template-areas:"copy copy" "stage console"!important;
gap:20px!important;
padding:28px!important;
min-height:0!important;
align-items:start!important;
}
.nlp3d.nlp3d-premium .nlp3d-copy{
grid-area:copy!important;
display:grid!important;
grid-template-columns:minmax(0,1fr) minmax(260px,.38fr)!important;
gap:10px 28px!important;
align-items:end!important;
padding:0 0 22px!important;
border-bottom:1px solid var(--nlp3d-line)!important;
color:var(--nlp3d-ink)!important;
}
.nlp3d.nlp3d-premium .nlp3d-kicker{
grid-column:1!important;
margin:0!important;
color:var(--nlp3d-gold)!important;
font-size:12px!important;
font-weight:700!important;
letter-spacing:0!important;
}
.nlp3d.nlp3d-premium h2{
grid-column:1!important;
max-width:22ch!important;
margin:4px 0 0!important;
color:var(--nlp3d-ink)!important;
font-family:var(--font-serif-he)!important;
font-size:clamp(34px,4.2vw,58px)!important;
font-weight:500!important;
line-height:1.04!important;
text-shadow:none!important;
letter-spacing:var(--tracking-tight)!important;
}
.nlp3d.nlp3d-premium .nlp3d-lead-text{
grid-column:1!important;
max-width:72ch!important;
margin:0!important;
color:#3e392f!important;
font-size:16px!important;
line-height:1.75!important;
}
.nlp3d.nlp3d-premium .nlp3d-shop-path,
.nlp3d.nlp3d-premium .nlp3d-metrics,
.nlp3d.nlp3d-premium .nlp3d-demo-note{
grid-column:2!important;
}
.nlp3d.nlp3d-premium .nlp3d-shop-path{
display:grid!important;
grid-template-columns:1fr!important;
gap:7px!important;
margin:0!important;
}
.nlp3d.nlp3d-premium .nlp3d-shop-path span,
.nlp3d.nlp3d-premium .nlp3d-metrics span{
width:100%!important;
min-height:34px!important;
border:1px solid var(--nlp3d-line)!important;
background:var(--nlp3d-paper)!important;
color:#342f27!important;
padding:7px 10px!important;
font-size:12.5px!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-metrics{
display:grid!important;
gap:7px!important;
margin:0!important;
}
.nlp3d.nlp3d-premium .nlp3d-demo-note{
margin:0!important;
border-right:2px solid var(--nlp3d-gold)!important;
color:#604b22!important;
font-size:12px!important;
line-height:1.55!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-wrap{
grid-area:stage!important;
display:block!important;
min-height:0!important;
height:auto!important;
overflow:visible!important;
isolation:isolate!important;
background:var(--nlp3d-cream)!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene{
position:relative!important;
inset:auto!important;
display:grid!important;
grid-template-columns:minmax(0,1fr) minmax(300px,360px)!important;
height:clamp(500px,45vw,650px)!important;
min-height:0!important;
overflow:hidden!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:4px!important;
background:linear-gradient(180deg,#fffaf2,#f4eadc)!important;
box-shadow:none!important;
cursor:auto!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene:after{display:none!important}
.nlp3d.nlp3d-premium .nlp3d-model-viewer{
position:relative!important;
inset:auto!important;
left:auto!important;
right:auto!important;
top:auto!important;
bottom:auto!important;
display:block!important;
width:100%!important;
height:100%!important;
min-height:0!important;
background:#fffaf2!important;
background-color:#fffaf2!important;
--poster-color:#fffaf2;
border:0!important;
border-inline-end:1px solid var(--nlp3d-line)!important;
opacity:1!important;
}
.nlp3d.nlp3d-premium .nlp3d-facade-plane{
position:relative!important;
inset:auto!important;
left:auto!important;
right:auto!important;
top:auto!important;
bottom:auto!important;
width:100%!important;
height:100%!important;
max-width:none!important;
transform:none!important;
border:0!important;
border-radius:0!important;
box-shadow:none!important;
z-index:4!important;
}
.nlp3d.nlp3d-premium .nlp3d-facade-plane.nlp3d-facade-missing{
display:grid!important;
align-content:center!important;
justify-items:start!important;
gap:12px!important;
padding:30px 24px!important;
background:linear-gradient(180deg,#fffaf1,#f7efe2)!important;
color:var(--nlp3d-ink)!important;
border-inline-start:1px solid var(--nlp3d-line)!important;
}
.nlp3d.nlp3d-premium .nlp3d-facade-plane.nlp3d-facade-missing strong{
max-width:13ch!important;
color:var(--nlp3d-ink)!important;
font-family:var(--font-serif-he)!important;
font-size:clamp(25px,2.7vw,38px)!important;
font-weight:500!important;
line-height:1.08!important;
}
.nlp3d.nlp3d-premium .nlp3d-facade-plane.nlp3d-facade-missing p,
.nlp3d.nlp3d-premium .nlp3d-facade-plane.nlp3d-facade-missing small{
max-width:38ch!important;
margin:0!important;
color:#4f4739!important;
font-size:14.5px!important;
line-height:1.7!important;
text-align:right!important;
}
.nlp3d.nlp3d-premium .nlp3d-fp-close{
top:16px!important;
left:16px!important;
width:40px!important;
height:40px!important;
border:1px solid var(--nlp3d-line)!important;
background:var(--nlp3d-paper)!important;
color:var(--nlp3d-ink)!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-facade-plane.nlp3d-facade-missing .nlp3d-fp-close{
display:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-context-caption{
left:16px!important;
right:16px!important;
bottom:12px!important;
color:#7c715f!important;
text-shadow:none!important;
font-size:12px!important;
}
.nlp3d.nlp3d-premium .nlp3d-context-caption,
.nlp3d.nlp3d-premium .nlp3d-context-pins{
display:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-toolbar{
position:relative!important;
top:auto!important;
right:auto!important;
left:auto!important;
z-index:20!important;
display:flex!important;
align-items:center!important;
justify-content:flex-start!important;
flex-wrap:wrap!important;
gap:8px!important;
margin:0 0 10px!important;
pointer-events:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-toolbar button{
pointer-events:auto!important;
}
.nlp3d.nlp3d-premium .nlp3d-drag-note{
display:inline-flex!important;
align-items:center!important;
min-height:44px!important;
padding:8px 10px!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:3px!important;
background:var(--nlp3d-paper)!important;
color:var(--nlp3d-ink)!important;
font-size:12px!important;
font-weight:700!important;
line-height:1.3!important;
}
.nlp3d.nlp3d-premium .nlp3d-angle,
.nlp3d.nlp3d-premium .nlp3d-orbit,
.nlp3d.nlp3d-premium .nlp3d-zoom,
.nlp3d.nlp3d-premium .nlp3d-fp-restore{
min-width:44px!important;
min-height:44px!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:3px!important;
background:rgba(255,253,248,.92)!important;
color:var(--nlp3d-ink)!important;
padding:8px 10px!important;
box-shadow:none!important;
font-size:12px!important;
font-weight:700!important;
}
.nlp3d.nlp3d-premium .nlp3d-angle.is-active,
.nlp3d.nlp3d-premium .nlp3d-orbit.is-active{
background:var(--nlp3d-ink)!important;
color:var(--nlp3d-cream)!important;
}
.nlp3d.nlp3d-premium .nlp3d-console{
grid-area:console!important;
display:flex!important;
flex-direction:column!important;
max-height:none!important;
overflow:hidden!important;
gap:14px!important;
padding:18px!important;
background:var(--nlp3d-paper)!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:4px!important;
box-shadow:none!important;
color:var(--nlp3d-ink)!important;
backdrop-filter:none!important;
min-width:0!important;
max-width:100%!important;
}
.nlp3d.nlp3d-premium .nlp3d-console-head{
border-bottom:1px solid var(--nlp3d-line)!important;
}
.nlp3d.nlp3d-premium .nlp3d-console-head p,
.nlp3d.nlp3d-premium .nlp3d-selected-title,
.nlp3d.nlp3d-premium .nlp3d-form-title,
.nlp3d.nlp3d-premium .nlp3d-owner-title{
color:var(--nlp3d-ink)!important;
font-family:var(--font-serif-he)!important;
font-weight:500!important;
}
.nlp3d.nlp3d-premium .nlp3d-status-chip,
.nlp3d.nlp3d-premium .nlp3d-floor,
.nlp3d.nlp3d-premium .nlp3d-unit-card,
.nlp3d.nlp3d-premium .nlp3d-tool,
.nlp3d.nlp3d-premium .nlp3d-compare-add{
border:1px solid var(--nlp3d-line)!important;
border-radius:3px!important;
background:#fffaf2!important;
color:var(--nlp3d-ink)!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-floor.is-active,
.nlp3d.nlp3d-premium .nlp3d-unit-card.is-active,
.nlp3d.nlp3d-premium .nlp3d-tool.is-active,
.nlp3d.nlp3d-premium .nlp3d-floor:hover,
.nlp3d.nlp3d-premium .nlp3d-unit-card:hover,
.nlp3d.nlp3d-premium .nlp3d-tool:hover{
background:var(--nlp3d-ink)!important;
color:var(--nlp3d-cream)!important;
border-color:var(--nlp3d-ink)!important;
}
.nlp3d.nlp3d-premium .nlp3d-unit-card span,
.nlp3d.nlp3d-premium .nlp3d-facts dt,
.nlp3d.nlp3d-premium .nlp3d-legal,
.nlp3d.nlp3d-premium .nlp3d-tool-panel p,
.nlp3d.nlp3d-premium .nlp3d-owner-form p,
.nlp3d.nlp3d-premium .nlp3d-dock-meta{
color:var(--nlp3d-muted)!important;
}
.nlp3d.nlp3d-premium .nlp3d-detail,
.nlp3d.nlp3d-premium .nlp3d-tool-panel,
.nlp3d.nlp3d-premium .nlp3d-selection-dock,
.nlp3d.nlp3d-premium .nlp3d-compare-tray,
.nlp3d.nlp3d-premium .nlp3d-showcase-copy,
.nlp3d.nlp3d-premium .nlp3d-showcase-cards,
.nlp3d.nlp3d-premium .nlp3d-owner-form{
background:#fffaf2!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:4px!important;
box-shadow:none!important;
color:var(--nlp3d-ink)!important;
min-width:0!important;
max-width:100%!important;
overflow-wrap:break-word!important;
}
.nlp3d.nlp3d-premium .nlp3d-units,
.nlp3d.nlp3d-premium .nlp3d-unit-card,
.nlp3d.nlp3d-premium .nlp3d-selected-title,
.nlp3d.nlp3d-premium .nlp3d-facts,
.nlp3d.nlp3d-premium .nlp3d-facts div,
.nlp3d.nlp3d-premium .nlp3d-facts dd{
min-width:0!important;
max-width:100%!important;
overflow-wrap:break-word!important;
word-break:normal!important;
}
.nlp3d.nlp3d-premium .nlp3d-facts dd{
color:var(--nlp3d-ink)!important;
}
.nlp3d.nlp3d-premium .nlp3d-plan,
.nlp3d.nlp3d-premium .nlp3d-tool-panel strong,
.nlp3d.nlp3d-premium .nlp3d-showcase-cards span,
.nlp3d.nlp3d-premium .nlp3d-showcase-cards strong{
color:var(--nlp3d-gold)!important;
}
.nlp3d.nlp3d-premium .nlp3d-lead-form input,
.nlp3d.nlp3d-premium .nlp3d-lead-form select,
.nlp3d.nlp3d-premium .nlp3d-owner-form input{
border:1px solid var(--nlp3d-line)!important;
border-radius:3px!important;
background:#fff!important;
color:var(--nlp3d-ink)!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-send,
.nlp3d.nlp3d-premium .nlp3d-wnext,
.nlp3d.nlp3d-premium .nlp3d-dock-actions .nlp3d-dock-action,
.nlp3d.nlp3d-premium .nlp3d-stage-card-actions .nlp3d-stage-inquiry,
.nlp3d.nlp3d-premium .nlp3d-owner-form button{
border:1px solid var(--nlp3d-ink)!important;
border-radius:3px!important;
background:var(--nlp3d-ink)!important;
color:var(--nlp3d-cream)!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-send-alt,
.nlp3d.nlp3d-premium .nlp3d-dock-actions button{
background:#fffaf2!important;
color:var(--nlp3d-ink)!important;
}
.nlp3d.nlp3d-premium .nlp3d-showcase{
grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr) minmax(300px,.8fr)!important;
padding:0 28px 28px!important;
}
.nlp3d.nlp3d-premium .nlp3d-showcase-copy h3{
color:var(--nlp3d-ink)!important;
text-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-showcase-copy p:last-child,
.nlp3d.nlp3d-premium .nlp3d-showcase-cards p{
color:#4f4739!important;
}
.nlp3d.nlp3d-premium .nlp3d-copy h2,
.nlp3d.nlp3d-premium .nlp3d-showcase-copy h3{
color:var(--nlp3d-ink)!important;
text-shadow:none!important;
background:none!important;
opacity:1!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene:before,
.nlp3d.nlp3d-premium .nlp3d-scene:after{
display:none!important;
content:none!important;
background:none!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene.has-model-viewer,
.nlp3d.nlp3d-premium .nlp3d-model-viewer,
.nlp3d.nlp3d-premium .nlp3d-model-viewer model-viewer{
background:linear-gradient(180deg,#fffaf2,#f1e6d8)!important;
background-color:#fffaf2!important;
--poster-color:#fffaf2;
color:var(--nlp3d-ink)!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene .nlp3d-facade-plane.nlp3d-facade-missing{
position:relative!important;
inset:auto!important;
left:auto!important;
right:auto!important;
top:auto!important;
bottom:auto!important;
align-self:stretch!important;
justify-self:stretch!important;
width:auto!important;
min-width:0!important;
height:auto!important;
min-height:100%!important;
transform:none!important;
}
@media(max-width:1100px){
.nlp3d.nlp3d-premium .nlp3d-shell{
grid-template-columns:1fr!important;
grid-template-areas:"copy" "stage" "console"!important;
}
.nlp3d.nlp3d-premium .nlp3d-copy{
grid-template-columns:1fr!important;
}
.nlp3d.nlp3d-premium .nlp3d-shop-path,
.nlp3d.nlp3d-premium .nlp3d-metrics,
.nlp3d.nlp3d-premium .nlp3d-demo-note{
grid-column:1!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene{
height:auto!important;
min-height:0!important;
grid-template-columns:1fr!important;
grid-template-rows:minmax(300px,48vw) auto!important;
overflow:visible!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-viewer{
height:100%!important;
border-inline-end:0!important;
border-bottom:1px solid var(--nlp3d-line)!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene .nlp3d-model-viewer{
grid-row:1!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene .nlp3d-facade-plane,
.nlp3d.nlp3d-premium .nlp3d-scene .nlp3d-facade-plane.nlp3d-facade-missing{
grid-row:2!important;
height:auto!important;
min-height:250px!important;
}
.nlp3d.nlp3d-premium .nlp3d-showcase{
grid-template-columns:1fr!important;
}
}
@media(max-width:900px){
.entry-content>.nlp3d.nlp3d-premium,
.wp-block-post-content>.nlp3d.nlp3d-premium{
width:calc(100vw - 44px)!important;
max-width:calc(100vw - 44px)!important;
margin-left:auto!important;
margin-right:auto!important;
}
}
@media(max-width:760px){
.entry-content>.nlp3d.nlp3d-premium,
.wp-block-post-content>.nlp3d.nlp3d-premium{
width:calc(100vw - 34px)!important;
max-width:calc(100vw - 34px)!important;
margin:18px auto 36px!important;
transform:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-shell{
gap:12px!important;
padding:12px!important;
width:100%!important;
max-width:100%!important;
min-width:0!important;
grid-template-columns:minmax(0,1fr)!important;
grid-template-areas:"copy" "stage" "console"!important;
overflow:visible!important;
}
.nlp3d.nlp3d-premium .nlp3d-copy,
.nlp3d.nlp3d-premium .nlp3d-stage-wrap,
.nlp3d.nlp3d-premium .nlp3d-console{
min-width:0!important;
max-width:100%!important;
}
.nlp3d.nlp3d-premium h2{
font-size:clamp(28px,8vw,36px)!important;
max-width:100%!important;
}
.nlp3d.nlp3d-premium .nlp3d-lead-text{
font-size:14.5px!important;
line-height:1.65!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-wrap,
.nlp3d.nlp3d-premium .nlp3d-scene{
width:100%!important;
max-width:100%!important;
min-width:0!important;
margin:0!important;
transform:none!important;
}
.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-stage-wrap,
.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-scene{
position:relative!important;
inset:auto!important;
left:auto!important;
right:auto!important;
width:100%!important;
max-width:100%!important;
min-width:0!important;
margin:0!important;
transform:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene{
grid-template-rows:300px auto!important;
overflow:hidden!important;
}
.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-scene{
display:grid!important;
grid-template-columns:1fr!important;
grid-template-rows:300px auto!important;
height:auto!important;
min-height:0!important;
overflow:hidden!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-viewer{
height:300px!important;
width:100%!important;
max-width:100%!important;
min-width:0!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene .nlp3d-facade-plane.nlp3d-facade-missing{
min-height:260px!important;
padding:28px 16px 18px!important;
}
.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-scene .nlp3d-facade-plane,
.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-scene .nlp3d-facade-plane.nlp3d-facade-missing{
position:relative!important;
inset:auto!important;
left:auto!important;
right:auto!important;
top:auto!important;
bottom:auto!important;
width:100%!important;
max-width:100%!important;
min-width:0!important;
height:auto!important;
min-height:260px!important;
margin:0!important;
transform:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-facade-plane.nlp3d-facade-missing strong{
font-size:28px!important;
max-width:12ch!important;
}
.nlp3d.nlp3d-premium .nlp3d-toolbar{
position:absolute!important;
top:10px!important;
right:10px!important;
left:10px!important;
display:flex!important;
flex-wrap:wrap!important;
}
.nlp3d.nlp3d-premium .nlp3d-angle,
.nlp3d.nlp3d-premium .nlp3d-orbit,
.nlp3d.nlp3d-premium .nlp3d-zoom{
font-size:11px!important;
min-width:44px!important;
min-height:44px!important;
padding:8px!important;
}
.nlp3d.nlp3d-premium .nlp3d-drag-note{
display:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-card:not([hidden]){
position:relative!important;
left:auto!important;
right:auto!important;
bottom:auto!important;
top:auto!important;
width:100%!important;
max-height:none!important;
margin:10px 0 0!important;
transform:none!important;
border-radius:4px!important;
}
.nlp3d.nlp3d-premium .nlp3d-console{
padding:14px!important;
}
.nlp3d.nlp3d-premium .nlp3d-view-toggle,
.nlp3d.nlp3d-premium .nlp3d-tool,
.nlp3d.nlp3d-premium .nlp3d-wnext,
.nlp3d.nlp3d-premium .nlp3d-owner-form button{
min-width:44px!important;
min-height:44px!important;
padding:9px 12px!important;
}
.nlp3d.nlp3d-premium .nlp3d-showcase{
padding:0 12px 16px!important;
}
}
.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-scene .nlp3d-model-viewer{
position:relative!important;
inset:auto!important;
left:auto!important;
right:auto!important;
top:auto!important;
bottom:auto!important;
grid-row:1!important;
width:100%!important;
height:100%!important;
}
.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-scene .nlp3d-facade-plane.nlp3d-facade-missing{
position:relative!important;
inset:auto!important;
left:auto!important;
right:auto!important;
top:auto!important;
bottom:auto!important;
grid-row:2!important;
width:auto!important;
max-width:none!important;
height:auto!important;
min-height:260px!important;
transform:none!important;
}
@media(max-width:760px){
.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-scene .nlp3d-model-viewer{
height:300px!important;
}
.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-scene .nlp3d-facade-plane.nlp3d-facade-missing{
min-height:260px!important;
padding:28px 16px 18px!important;
}
}
/* Core public cream-luxury component surfaces. */
.nlp3d.nlp3d-premium,
.nlp3d.nlp3d-premium *{
letter-spacing:0!important;
}
.nlp3d.nlp3d-premium h2,
.nlp3d.nlp3d-premium h3,
.nlp3d.nlp3d-premium .nlp3d-console-head p,
.nlp3d.nlp3d-premium .nlp3d-selected-title,
.nlp3d.nlp3d-premium .nlp3d-stage-card-title,
.nlp3d.nlp3d-premium .nlp3d-owner-title,
.nlp3d.nlp3d-premium .nlp3d-showcase-copy h3,
.nlp3d.nlp3d-premium .nlp3d-dock-title,
.nlp3d-intro h2{
font-family:var(--font-serif-he)!important;
font-weight:500!important;
line-height:var(--lh-tight)!important;
color:var(--nlp3d-ink)!important;
text-shadow:none!important;
}
.nlp3d.nlp3d-premium,
.nlp3d.nlp3d-premium .nlp3d-shell,
.nlp3d.nlp3d-premium .nlp3d-copy{
background:var(--nlp3d-cream)!important;
color:var(--nlp3d-ink)!important;
}
.nlp3d.nlp3d-premium .nlp3d-scene,
.nlp3d.nlp3d-premium .nlp3d-model-viewer,
.nlp3d.nlp3d-premium .nlp3d-model-viewer model-viewer,
.nlp3d.nlp3d-premium .nlp3d-facade-plane,
.nlp3d.nlp3d-premium .nlp3d-stage-viewframe{
--poster-color:#fffaf2!important;
background:linear-gradient(180deg,#fffaf2,#f1e6d8)!important;
background-color:#fffaf2!important;
color:var(--nlp3d-ink)!important;
border-color:var(--nlp3d-line)!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-console,
.nlp3d.nlp3d-premium .nlp3d-detail,
.nlp3d.nlp3d-premium .nlp3d-tool-panel,
.nlp3d.nlp3d-premium .nlp3d-selection-dock,
.nlp3d.nlp3d-premium .nlp3d-stage-card,
.nlp3d.nlp3d-premium .nlp3d-compare-tray,
.nlp3d.nlp3d-premium .nlp3d-overlay-box,
.nlp3d.nlp3d-premium .nlp3d-showcase-copy,
.nlp3d.nlp3d-premium .nlp3d-showcase-cards,
.nlp3d.nlp3d-premium .nlp3d-showcase-cards article,
.nlp3d.nlp3d-premium .nlp3d-owner-form,
.nlp3d.nlp3d-premium .nlp3d-facts div,
.nlp3d.nlp3d-premium .nlp3d-viewframe{
background:var(--nlp3d-paper)!important;
color:var(--nlp3d-ink)!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:var(--radius)!important;
box-shadow:var(--shadow-card)!important;
backdrop-filter:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-card:not([hidden]){
display:grid!important;
gap:10px!important;
padding:16px!important;
align-items:start!important;
position:relative!important;
}
body.nadlan-p3d-stage-active .nlfab,
body.nadlan-p3d-stage-active #nlcta,
body.nadlan-p3d-stage-active #nlai .nlai-fab{
opacity:0!important;
pointer-events:none!important;
transform:translateY(14px)!important;
}
.nlp3d.nlp3d-premium .nlp3d-view-toggle,
.nlp3d.nlp3d-premium .nlp3d-tool,
.nlp3d.nlp3d-premium .nlp3d-wnext,
.nlp3d.nlp3d-premium .nlp3d-owner-form button{
display:inline-flex!important;
align-items:center!important;
justify-content:center!important;
min-width:44px!important;
min-height:44px!important;
padding:9px 12px!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-kicker,
.nlp3d.nlp3d-premium .nlp3d-kicker,
.nlp3d.nlp3d-premium .nlp3d-plan,
.nlp3d.nlp3d-premium .nlp3d-tool-panel strong,
.nlp3d.nlp3d-premium .nlp3d-showcase-cards span,
.nlp3d.nlp3d-premium .nlp3d-selection-dock span{
color:var(--nlp3d-gold)!important;
}
.nlp3d.nlp3d-premium .nlp3d-lead-text,
.nlp3d.nlp3d-premium .nlp3d-stage-card-meta,
.nlp3d.nlp3d-premium .nlp3d-stage-card-note,
.nlp3d.nlp3d-premium .nlp3d-dock-meta,
.nlp3d.nlp3d-premium .nlp3d-legal,
.nlp3d.nlp3d-premium .nlp3d-facts dt,
.nlp3d.nlp3d-premium .nlp3d-tool-panel p,
.nlp3d.nlp3d-premium .nlp3d-showcase-copy p,
.nlp3d.nlp3d-premium .nlp3d-showcase-cards p,
.nlp3d.nlp3d-premium .nlp3d-owner-form p,
.nlp3d.nlp3d-premium .nlp3d-context-caption,
.nlp3d.nlp3d-premium .nlp3d-view-copy,
.nlp3d.nlp3d-premium .nlp3d-compare-label,
.nlp3d.nlp3d-premium .nlp3d-stage-status{
color:var(--nlp3d-muted)!important;
text-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-facts dd,
.nlp3d.nlp3d-premium .nlp3d-ok,
.nlp3d.nlp3d-premium .nlp3d-stage-price,
.nlp3d.nlp3d-premium .nlp3d-stage-status,
.nlp3d.nlp3d-premium .nlp3d-stage-program,
.nlp3d.nlp3d-premium .nlp3d-stage-view{
color:var(--nlp3d-ink)!important;
}
.nlp3d.nlp3d-premium .nlp3d-status-chip,
.nlp3d.nlp3d-premium .nlp3d-floor,
.nlp3d.nlp3d-premium .nlp3d-unit-card,
.nlp3d.nlp3d-premium .nlp3d-tool,
.nlp3d.nlp3d-premium .nlp3d-compare-add,
.nlp3d.nlp3d-premium .nlp3d-compare-chip,
.nlp3d.nlp3d-premium .nlp3d-stage-tabs button,
.nlp3d.nlp3d-premium .nlp3d-stage-card-stats span,
.nlp3d.nlp3d-premium .nlp3d-stage-card-tags span,
.nlp3d.nlp3d-premium .nlp3d-deal-steps span{
background:#fffaf2!important;
color:var(--nlp3d-ink)!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:var(--radius)!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-card-tags,
.nlp3d.nlp3d-premium .nlp3d-stage-card-stats,
.nlp3d.nlp3d-premium .nlp3d-stage-card-actions,
.nlp3d.nlp3d-premium .nlp3d-stage-tabs,
.nlp3d.nlp3d-premium .nlp3d-dock-actions{
display:flex!important;
flex-wrap:wrap!important;
gap:8px!important;
align-items:stretch!important;
}
.nlp3d.nlp3d-premium .nlp3d-floor.is-active,
.nlp3d.nlp3d-premium .nlp3d-unit-card.is-active,
.nlp3d.nlp3d-premium .nlp3d-tool.is-active,
.nlp3d.nlp3d-premium .nlp3d-stage-tabs button.is-active,
.nlp3d.nlp3d-premium .nlp3d-compare-add.is-on{
background:var(--nlp3d-ink)!important;
color:var(--nlp3d-cream)!important;
border-color:var(--nlp3d-ink)!important;
}
.nlp3d.nlp3d-premium .nlp3d-send,
.nlp3d.nlp3d-premium .nlp3d-wnext,
.nlp3d.nlp3d-premium .nlp3d-dock-actions .nlp3d-dock-action,
.nlp3d.nlp3d-premium .nlp3d-stage-card-actions .nlp3d-stage-inquiry,
.nlp3d.nlp3d-premium .nlp3d-owner-form button,
.nlp3d.nlp3d-premium .nlp3d-compare-open,
.nlp3d.nlp3d-premium .nlp3d-compare-pick{
background:var(--nlp3d-ink)!important;
color:var(--nlp3d-cream)!important;
border:1px solid var(--nlp3d-ink)!important;
border-radius:var(--radius)!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-send-alt,
.nlp3d.nlp3d-premium .nlp3d-dock-actions button,
.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button,
.nlp3d.nlp3d-premium .nlp3d-stage-card-close,
.nlp3d.nlp3d-premium .nlp3d-overlay-close,
.nlp3d.nlp3d-premium .nlp3d-wback,
.nlp3d.nlp3d-premium .nlp3d-angle,
.nlp3d.nlp3d-premium .nlp3d-orbit,
.nlp3d.nlp3d-premium .nlp3d-zoom,
.nlp3d.nlp3d-premium .nlp3d-fp-restore{
background:#fffaf2!important;
color:var(--nlp3d-ink)!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:var(--radius)!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-angle.is-active,
.nlp3d.nlp3d-premium .nlp3d-orbit.is-active{
background:var(--nlp3d-ink)!important;
color:var(--nlp3d-cream)!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button,
.nlp3d.nlp3d-premium .nlp3d-dock-actions button,
.nlp3d.nlp3d-premium .nlp3d-stage-card-close,
.nlp3d.nlp3d-premium .nlp3d-floor,
.nlp3d.nlp3d-premium .nlp3d-compare-add,
.nlp3d.nlp3d-premium .nlp3d-plan{
display:inline-flex!important;
align-items:center!important;
justify-content:center!important;
min-height:44px!important;
padding:10px 14px!important;
line-height:1.25!important;
text-align:center!important;
white-space:normal!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-card-close{
width:44px!important;
min-width:44px!important;
padding:0!important;
justify-self:start!important;
position:absolute!important;
inset-block-start:14px!important;
inset-inline-start:14px!important;
z-index:2!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-kicker,
.nlp3d.nlp3d-premium .nlp3d-stage-card-title,
.nlp3d.nlp3d-premium .nlp3d-stage-card-meta{
padding-inline-start:54px!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-card-tags span,
.nlp3d.nlp3d-premium .nlp3d-stage-card-stats span{
min-height:34px!important;
padding:7px 10px!important;
line-height:1.25!important;
overflow-wrap:anywhere!important;
}
.nlp3d.nlp3d-premium .nlp3d-lead-form input,
.nlp3d.nlp3d-premium .nlp3d-lead-form select,
.nlp3d.nlp3d-premium .nlp3d-owner-form input{
background:#fff!important;
color:var(--nlp3d-ink)!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:var(--radius)!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-pick,
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot{
background:#fffaf2!important;
color:var(--nlp3d-ink)!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:var(--radius)!important;
box-shadow:var(--shadow-card)!important;
}
.nlp3d.nlp3d-premium.has-model-picker .nlp3d-scene{
grid-template-columns:1fr!important;
}
.nlp3d.nlp3d-premium.has-model-picker .nlp3d-model-viewer{
grid-column:1!important;
grid-row:1!important;
width:100%!important;
height:100%!important;
border-inline-end:0!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks{
position:absolute!important;
inset:54px 16px 18px!important;
z-index:12!important;
pointer-events:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-stage-pick{
position:absolute!important;
display:inline-flex!important;
align-items:center!important;
justify-content:center!important;
gap:6px!important;
min-width:54px!important;
min-height:44px!important;
padding:6px 9px!important;
border-radius:999px!important;
pointer-events:auto!important;
transform:translate(-50%,-50%)!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-pick-label{
display:inline-flex!important;
align-items:center!important;
gap:4px!important;
font-size:12px!important;
font-weight:800!important;
line-height:1!important;
white-space:nowrap!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-pick-label span{
font-weight:700!important;
color:var(--nlp3d-muted)!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-hotspot-tip{
position:absolute!important;
top:calc(100% + 8px)!important;
right:50%!important;
min-width:190px!important;
max-width:240px!important;
padding:10px!important;
opacity:0!important;
pointer-events:none!important;
transform:translateX(50%) translateY(4px)!important;
transition:opacity .12s ease,transform .12s ease!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-stage-pick:hover .nlp3d-hotspot-tip,
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-stage-pick:focus-visible .nlp3d-hotspot-tip,
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-stage-pick.is-open .nlp3d-hotspot-tip{
opacity:1!important;
transform:translateX(50%) translateY(0)!important;
}
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot{
display:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-mv-label{
position:absolute!important;
top:calc(100% + 8px)!important;
right:50%!important;
max-width:140px!important;
padding:5px 8px!important;
border:1px solid var(--nlp3d-line)!important;
border-radius:999px!important;
background:rgba(255,250,242,.96)!important;
color:var(--nlp3d-ink)!important;
font-size:11px!important;
font-weight:700!important;
line-height:1.2!important;
white-space:nowrap!important;
box-shadow:var(--shadow-card)!important;
opacity:0!important;
pointer-events:none!important;
transform:translateX(50%) translateY(4px)!important;
transition:opacity .12s ease,transform .12s ease!important;
}
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot:hover .nlp3d-mv-label,
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot:focus-visible .nlp3d-mv-label,
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot.is-active .nlp3d-mv-label{
opacity:1!important;
transform:translateX(50%) translateY(0)!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-pick:before,
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot:before,
.nlp3d.nlp3d-premium .nlp3d-stage-pick.is-available .nlp3d-hotspot-dot,
.nlp3d.nlp3d-premium .nlp3d-hotspot-hit.is-available .nlp3d-hotspot-dot{
background:var(--nlp3d-sage)!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-pick.is-reserved:before,
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot.is-reserved:before,
.nlp3d.nlp3d-premium .nlp3d-stage-pick.is-reserved .nlp3d-hotspot-dot,
.nlp3d.nlp3d-premium .nlp3d-hotspot-hit.is-reserved .nlp3d-hotspot-dot{
background:var(--nlp3d-gold)!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-pick.is-sold:before,
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot.is-sold:before,
.nlp3d.nlp3d-premium .nlp3d-stage-pick.is-sold .nlp3d-hotspot-dot,
.nlp3d.nlp3d-premium .nlp3d-hotspot-hit.is-sold .nlp3d-hotspot-dot{
background:#B8B1A2!important;
box-shadow:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-pick:hover,
.nlp3d.nlp3d-premium .nlp3d-stage-pick:focus-visible,
.nlp3d.nlp3d-premium .nlp3d-stage-pick.is-open,
.nlp3d.nlp3d-premium .nlp3d-stage-pick.is-active,
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot:hover,
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot:focus-visible,
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot.is-active{
border-color:var(--nlp3d-gold)!important;
box-shadow:0 0 0 3px rgba(156,122,60,.16),var(--shadow-card)!important;
}
.nlp3d.nlp3d-premium .nlp3d-hotspot-tip,
.nlp3d.nlp3d-premium .nlp3d-map-error{
background:var(--nlp3d-paper)!important;
color:var(--nlp3d-ink)!important;
border:1px solid var(--nlp3d-line)!important;
box-shadow:var(--shadow-card)!important;
}
.nlp3d.nlp3d-premium .nlp3d-overlay{
background:rgba(27,26,23,.28)!important;
}
.nlp3d.nlp3d-premium .nlp3d-view-badge,
.nlp3d.nlp3d-premium .nlp3d-stage-card-stats span[data-kind="estimate"],
.nlp3d.nlp3d-premium .nlp3d-wdots span.is-on{
background:var(--nlp3d-terracotta)!important;
color:var(--nlp3d-cream)!important;
border-color:var(--nlp3d-terracotta)!important;
}
@media(max-width:760px){
.nlp3d.nlp3d-premium .nlp3d-model-picks{
inset:64px 10px 16px!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-stage-pick{
min-width:48px!important;
min-height:44px!important;
padding:5px 7px!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-pick-room-count{
display:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-stage-pick{
width:44px!important;
min-width:44px!important;
padding:0!important;
gap:0!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-stage-pick.is-active{
width:48px!important;
min-width:48px!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-pick-label{
font-size:11px!important;
justify-content:center!important;
width:100%!important;
}
.nlp3d.nlp3d-premium .nlp3d-model-picks .nlp3d-hotspot-tip{
display:none!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-card:not([hidden]){
position:relative!important;
inset:auto!important;
width:100%!important;
max-height:none!important;
overflow:visible!important;
transform:none!important;
margin:10px 0 0!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-card-actions{
display:grid!important;
grid-template-columns:repeat(2,minmax(0,1fr))!important;
gap:8px!important;
}
.nlp3d.nlp3d-premium .nlp3d-stage-card-actions button{
width:100%!important;
}
}
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
	function selectedTitle(u){if(!u){return 'בחרו דירה'}var base=u.title || ('קו '+(u.line||u.id));var floor=u.floor||'-';return (floor!=='-'&&base.indexOf('קומה '+floor)>-1)?base:base+' · קומה '+floor}
	function unitText(u){var parts=[];if(u.rooms){parts.push(u.rooms+' חדרים')}if(u.sqm){parts.push(fmt(u.sqm)+' מ"ר')}if(u.view){parts.push(u.view)}return parts.join(' · ')}
	function unitSummaryText(u){var text=unitText(u);if(!u||!u.rooms||!text){return text}var parts=text.split(' · ');return String(parts[0]||'').indexOf(String(u.rooms))===0?parts.slice(1).join(' · '):text}
	function unitBuyerTags(u,meta){
		var tags=[];
		if(!u){return tags}
		if(isRecommendedUnit(u)){tags.push(u.recommended_label||'מומלצת לבדיקה')}
		if(u.plan){tags.push('תוכנית זמינה')}
		if(u.tour_url||u.interior_url){tags.push('סיור או הדמיה זמינים')}
		return tags.slice(0,3);
	}
	function unitBuyerNote(u,meta){
		if(!u){return 'בחרו דירה על המגדל כדי לראות מחיר, נוף, כיוון ופעולות המשך.'}
		var priceInfo=unitPriceInfo(u,meta);
		if(u.status==='sold'){return 'הדירה מסומנת כלא זמינה. אפשר להשתמש בה להשוואה ולבחור יחידה פנויה אחרת.'}
		if(u.status==='reserved'){return 'הדירה בתהליך בדיקה. אפשר להשאיר פרטים כדי לוודא זמינות או לקבל חלופה דומה.'}
		if(priceInfo.kind==='estimate'){return 'האומדן עוזר להשוואה ראשונית בלבד. המחיר, הזמינות ותנאי העסקה יאומתו מול היזם לפני כל התקדמות.'}
		return 'בדקו קומה, כיוון ונוף, ואז בקשו שיחה עם היזם על הדירה שנבחרה.';
	}
	function isRecommendedUnit(u){
		if(!u){return false}
		return !!(u.recommended||u.is_recommended);
	}
	function stageTipText(u,meta){
		if(!u){return ''}
		var price=unitPriceText(u,meta);
		var parts=[statusLabel(u.status)];
		if(u.rooms){parts.push(u.rooms+' חד׳')}
		if(u.sqm){parts.push(fmt(u.sqm)+' מ"ר')}
		if(u.view){parts.push(u.view)}
		if(price){parts.push(price)}
		return parts.join(' · ');
	}
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
	function assetUrl(url){
		if(!url){return ''}
		try{
			var u=new URL(String(url),window.location.origin);
			return /^https?:$/.test(u.protocol)?u.href:'';
		}catch(e){return ''}
	}
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
		var modelError=root.querySelector('.nlp3d-model-error');
		var modelHotspots=[].slice.call(root.querySelectorAll('.nlp3d-mv-hotspot'));
		var stagePicks=null;
		var facadePlane=null;
		var facadeAssets=(Array.isArray(meta.facade_images)?meta.facade_images:[]).filter(function(item){
			return item&&assetUrl(item.src||item.url||item.image);
		});
		var primaryFacade=facadeAssets[0]||null;
		var primaryFacadeUrl=primaryFacade?assetUrl(primaryFacade.src||primaryFacade.url||primaryFacade.image):'';
		var hasRealFacade=!!primaryFacadeUrl;
		if(scene){
			if(hasRealFacade){
				/* Precision selector: a real facade/elevation image owns apartment picking.
				   No real image means no fake facade is rendered. */
				facadePlane=document.createElement('div');
				facadePlane.className='nlp3d-facade-plane has-real-facade';
				var closeBtn=document.createElement('button');
				closeBtn.type='button';
				closeBtn.className='nlp3d-fp-close';
				closeBtn.dataset.action='facade-dismiss';
				closeBtn.setAttribute('aria-label','הסתר חזית');
				closeBtn.textContent='×';
				var titleEl=document.createElement('span');
				titleEl.className='nlp3d-fp-title';
				titleEl.textContent=primaryFacade.label||'בחירת דירות על חזית הפרויקט';
				var imageEl=document.createElement('img');
				imageEl.className='nlp3d-fp-image';
				imageEl.src=primaryFacadeUrl;
				imageEl.alt=primaryFacade.alt||primaryFacade.label||((meta.title||'הפרויקט')+' - חזית לבחירת דירות');
				imageEl.loading='lazy';
				imageEl.addEventListener('error',function(){
					if(modelViewer){
						if(facadePlane){facadePlane.remove()}
						if(stagePicks){stagePicks.remove()}
						if(fpLegend){fpLegend.hidden=true}
						root.classList.add('is-dual-showroom');
						root.classList.remove('is-facade-asset-missing');
						return;
					}
					root.classList.add('is-facade-asset-missing');
					facadePlane.classList.remove('has-real-facade');
					facadePlane.classList.add('nlp3d-facade-missing');
					facadePlane.innerHTML='<button type="button" class="nlp3d-fp-close" data-action="facade-dismiss" aria-label="הסתר הודעת חזית">×</button><strong>ממתין לחזית מאושרת</strong><p>קובץ החזית של הפרויקט לא נטען כרגע. נציג חזית מאושרת בלבד כדי שהדירות יוצגו מול הבניין הנכון.</p>';
					if(stagePicks){stagePicks.remove()}
					if(fpLegend){fpLegend.hidden=true}
				});
				facadePlane.appendChild(closeBtn);
				facadePlane.appendChild(titleEl);
				facadePlane.appendChild(imageEl);
				stagePicks=document.createElement('div');
				stagePicks.className='nlp3d-cells';
				stagePicks.setAttribute('role','group');
				stagePicks.setAttribute('aria-label','בחירת דירה על חזית הבניין');
				facadePlane.appendChild(stagePicks);
				scene.appendChild(facadePlane);
				var fpLegend=document.createElement('div');
				fpLegend.className='nlp3d-fp-legend';
				fpLegend.setAttribute('aria-hidden','true');
				fpLegend.innerHTML='<span><i style="background:#3ddc84"></i>זמינה</span><span><i style="background:#f2c14e"></i>בבדיקה</span><span><i style="background:#d94a43"></i>לא זמינה</span>';
				scene.appendChild(fpLegend);
				root.classList.add(modelViewer?'is-dual-showroom':'is-facade-select');
			}else if(modelViewer){
				stagePicks=document.createElement('div');
				stagePicks.className='nlp3d-model-picks';
				stagePicks.setAttribute('role','group');
				stagePicks.setAttribute('aria-label','בחירת דירה על המודל');
				scene.appendChild(stagePicks);
				root.classList.add('is-dual-showroom');
				root.classList.add('has-model-picker');
				root.classList.remove('is-facade-asset-missing');
			}else{
				facadePlane=document.createElement('div');
				facadePlane.className='nlp3d-facade-plane nlp3d-facade-missing';
				facadePlane.innerHTML='<button type="button" class="nlp3d-fp-close" data-action="facade-dismiss" aria-label="הסתר הודעת חזית">×</button><strong>ממתין לחזית ותוכניות מהיזם</strong><p>המודל התלת ממדי מוצג, אבל בחירת דירה על חזית הבניין תיפתח רק אחרי העלאת חזית מאושרת ותוכניות רשמיות.</p><small>קבלנים ויזמים יכולים להעביר חזית, תוכניות ומלאי כדי להפוך את הסיור לעמוד מכירה מלא.</small>';
				scene.appendChild(facadePlane);
				root.classList.add('is-facade-asset-missing');
			}
		}
		function fitMobileShowroom(){
			if(!root){return}
			root.style.setProperty('--nlp3d-mobile-nudge','0px');
			root.classList.remove('is-mobile-edge-fixed');
		}
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
		var stageCardTags=root.querySelector('.nlp3d-stage-card-tags');
		var stageCardPrice=root.querySelector('.nlp3d-stage-price');
		var stageCardStatus=root.querySelector('.nlp3d-stage-status');
		var stageCardView=root.querySelector('.nlp3d-stage-view');
		var stageCardNote=root.querySelector('.nlp3d-stage-card-note');
		var stageCardClose=root.querySelector('.nlp3d-stage-card-close');
		var stageDetails=root.querySelector('.nlp3d-stage-details');
		var stageViewBtn=root.querySelector('.nlp3d-stage-view-btn');
		var stageTour=root.querySelector('.nlp3d-stage-tour');
		var stageInquiry=root.querySelector('.nlp3d-stage-inquiry');
		var facadeRestore=root.querySelector('.nlp3d-fp-restore');
		var facadeClose=facadePlane?facadePlane.querySelector('.nlp3d-fp-close'):root.querySelector('.nlp3d-fp-close');
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
		var facadeDismissKey=storeKey+'-facade-dismissed';
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
		var suppressUnitClickUntil=0;
		var stageCardDismissed=false;
		var activeTool='spec';
		var cameraLock=(meta.camera_lock||'horizontal').toString();
		var horizontalCamera=cameraLock!=='free';
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
		function setFacadeDismissed(on,source){
			root.classList.toggle('nlp3d-facade-dismissed',!!on);
			if(facadePlane){facadePlane.hidden=!!on}
			if(facadeRestore){facadeRestore.hidden=!on}
			try{sessionStorage.setItem(facadeDismissKey,on?'1':'0')}catch(e){}
			if(source){track('facade_visibility',{hidden:!!on,source:source})}
			window.requestAnimationFrame(fitMobileShowroom);
		}
		try{if(sessionStorage.getItem(facadeDismissKey)==='1'){setFacadeDismissed(true,'restore-session')}}catch(e){}
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
					var typeLabels={plan:'תוכנית',tour:'סיור',video:'וידאו',interior:'פנים','3d-city':'תצוגת עיר'};
					chip.textContent=typeLabels[item.type]||item.category||item.type;
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
			hit.addEventListener('click',function(e){e.stopPropagation();if(Date.now()<suppressUnitClickUntil){e.preventDefault();return}selectUnit(u.id,'facade-hit')});
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
		function stagePickOffset(u){
			var id=String(u&&u.id||'').toLowerCase();
			var sceneWidth=scene?scene.getBoundingClientRect().width:740;
			var scale=Math.max(.42,Math.min(1,sceneWidth/740));
			if(id.indexOf('boutique')>-1){return Math.round(-245*scale)}
			if(id.indexOf('sw')>-1){return Math.round(-128*scale)}
			if(id.indexOf('nw')>-1){return Math.round(-92*scale)}
			if(id.indexOf('se')>-1){return Math.round(118*scale)}
			if(id.indexOf('-w')>-1){return Math.round(-112*scale)}
			return 0;
		}
		function closeStagePickTips(except){
			if(!stagePicks){return}
			stagePicks.querySelectorAll('.nlp3d-stage-pick.is-open').forEach(function(node){
				if(node!==except){node.classList.remove('is-open')}
			});
		}
		function selectNearestModelPickFromPoint(p,source){
			if(!stagePicks||!p){return false}
			var sceneRect=scene?scene.getBoundingClientRect():null;
			if(sceneRect&&(p.x<sceneRect.left||p.x>sceneRect.right||p.y<sceneRect.top||p.y>sceneRect.bottom)){return false}
			var baseLimit=(window.innerWidth&&window.innerWidth<=480)?92:76;
			var best=null,bestScore=Infinity;
			stagePicks.querySelectorAll('.nlp3d-stage-pick,.nlp3d-cell').forEach(function(node){
				if(node.getAttribute('aria-disabled')==='true'){return}
				var cs=window.getComputedStyle(node);
				if(cs.display==='none'||cs.visibility==='hidden'){return}
				var r=node.getBoundingClientRect();
				if(r.width<1||r.height<1){return}
				var cx=r.left+(r.width/2),cy=r.top+(r.height/2);
				var dx=p.x-cx,dy=p.y-cy;
				var ax=Math.abs(dx),ay=Math.abs(dy);
				var distance=Math.sqrt(dx*dx+dy*dy);
				var limit=Math.max(baseLimit,Math.min(104,Math.max(r.width,r.height)*1.35));
				var score=(ay*3)+ax+(distance*.12);
				if(distance<=limit&&score<bestScore){best=node;bestScore=score}
			});
			if(!best||!best.dataset||!best.dataset.unit){return false}
			var unit=unitById(best.dataset.unit);
			if(!unit||unit.status==='sold'){return false}
			activateStagePick(best,unit,source||'model-near-pick');
			return true;
		}
		function activateStagePick(button,u,source){
			if(!button||!u||u.status==='sold'||button.getAttribute('aria-disabled')==='true'){
				if(button){button.classList.remove('is-open')}
				return;
			}
			closeStagePickTips(button);
			button.classList.add('is-open');
			track('stage_pick_preview',{unit:u.id,source:source||'stage-pick'});
			selectUnit(u.id,source||'stage-pick');
		}
		function nlpClamp(v,a,b){v=parseFloat(v);if(isNaN(v)){return null}return Math.max(a,Math.min(b,v))}
		function renderApartmentCells(){
			stagePicks.innerHTML='';
			var span=Math.max(1,maxFloor-minFloor);
			var byFloor={};
			units.forEach(function(u){var f=parseInt(u.floor||minFloor,10)||minFloor;(byFloor[f]=byFloor[f]||[]).push(u)});
			var rowH=Math.max(3.2,86/Math.max(1,(floors.length||1)));
			units.forEach(function(u){
				var floor=parseInt(u.floor||minFloor,10)||minFloor;
				var sib=byFloor[floor]||[u];var ci=sib.indexOf(u);if(ci<0){ci=0}var cn=sib.length||1;
				var status=u.status||'available';
				var recommended=isRecommendedUnit(u);
				var w=nlpClamp(u.stage_w,4,96);if(w===null){w=Math.min(30,(92/cn)*0.84)}
				var cx=nlpClamp(u.stage_x,1,99);if(cx===null){var slot=92/cn;cx=4+slot*(ci+0.5)}
				var left=Math.max(1,Math.min(99-w,cx-w/2));
				var h=nlpClamp(u.stage_h,3,30);if(h===null){h=Math.max(3,rowH*0.82)}
				var top=nlpClamp(u.stage_y,1,99);
				if(top===null){var norm=(floor-minFloor)/span;top=Math.max(3,Math.min(92,90-norm*84))}
				top=Math.max(1,Math.min(99-h,top));
				var b=document.createElement('button');
				b.type='button';
				b.className='nlp3d-cell nlp3d-status-'+status+(recommended?' is-recommended':'')+(activeUnit&&u.id===activeUnit.id?' is-active':'');
				b.dataset.unit=u.id;
				b.dataset.action='select-unit-cell';
				b.style.left=left+'%';b.style.top=top+'%';b.style.width=w+'%';b.style.height=h+'%';
				var priceInfo=unitPriceInfo(u,meta);
				b.setAttribute('aria-label',selectedTitle(u)+' · '+statusLabel(status)+(priceInfo&&priceInfo.kind!=='empty'?' · '+priceInfo.text:''));
				b.setAttribute('aria-pressed',activeUnit&&u.id===activeUnit.id?'true':'false');
				if(status==='sold'){b.setAttribute('aria-disabled','true');b.tabIndex=-1}
				var tag=document.createElement('span');
				tag.className='nlp3d-cell-tag';
				var tagMain=document.createElement('strong');
				var tagSub=document.createElement('small');
				tagMain.textContent=(u.line||u.label||u.id)+' · '+(u.floor||'-');
				var cellInfo=(u.rooms?u.rooms+' חד׳':'דירה')+(u.sqm?' · '+fmt(u.sqm)+' מ"ר':'');
				if(status!=='available'){cellInfo=statusLabel(status)+' - '+cellInfo}
				tagSub.textContent=cellInfo;
				tag.appendChild(tagMain);
				tag.appendChild(tagSub);
				b.appendChild(tag);
				b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();if(status==='sold'){return}selectUnit(u.id,'facade-cell')});
				b.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();if(status!=='sold'){selectUnit(u.id,'facade-cell-key')}}});
				stagePicks.appendChild(b);
			});
		}
		function renderStagePicks(){
			if(!stagePicks){return}
			if(facadePlane){renderApartmentCells();return}
			stagePicks.innerHTML='';
			var span=Math.max(1,maxFloor-minFloor);
			units.forEach(function(u){
				var floor=parseInt(u.floor||minFloor,10)||minFloor;
				var norm=(floor-minFloor)/span;
				var mobileMarkerSpread=window.innerWidth&&window.innerWidth<=480;
				var markerTopMin=mobileMarkerSpread?14:20;
				var markerTopMax=mobileMarkerSpread?84:76;
				var top=Math.max(markerTopMin,Math.min(markerTopMax,markerTopMax-(norm*(markerTopMax-markerTopMin))));
				var recommended=isRecommendedUnit(u);
				var label=u.label||u.title||('קומה '+(u.floor||'-'));
				var status=u.status||'available';
				var b=document.createElement('button');
				b.type='button';
				b.className='nlp3d-stage-pick nlp3d-status-'+status+' is-'+status+(recommended?' is-recommended':'')+(activeUnit&&u.id===activeUnit.id?' is-active':'');
				b.dataset.unit=u.id;
				b.dataset.action='select-unit-stage';
				b.style.top=top+'%';
				b.style.left='calc(50% + '+stagePickOffset(u)+'px)';
				b.setAttribute('aria-label',selectedTitle(u)+' · '+stageTipText(u,meta));
				if(status==='sold'){
					b.setAttribute('aria-disabled','true');
					b.setAttribute('tabindex','-1');
				}
				var hit=document.createElement('span');
				hit.className='nlp3d-hotspot-hit';
				hit.setAttribute('aria-hidden','true');
				var dot=document.createElement('span');
				dot.className='nlp3d-hotspot-dot';
				dot.setAttribute('aria-hidden','true');
				var text=document.createElement('span');
				text.className='nlp3d-pick-label';
				var strong=document.createElement('strong');
				strong.textContent=u.floor||'';
				var small=document.createElement('span');
				small.className='nlp3d-pick-room-count';
				small.textContent=u.rooms?u.rooms+' ח':'דירה';
				text.appendChild(strong);
				text.appendChild(small);
				var tip=document.createElement('span');
				tip.className='nlp3d-hotspot-tip';
				var tipTitle=document.createElement('strong');
				var tipMeta=document.createElement('small');
				var tipStatus=document.createElement('small');
				tipTitle.textContent=label+' · '+(u.rooms?u.rooms+' חד׳':'דירה');
				tipMeta.textContent=(u.sqm?fmt(u.sqm)+' מ"ר · ':'')+(u.view||u.dir||'מבט לפי כיוון');
				tipStatus.textContent=statusLabel(status)+(recommended?' · '+(u.recommended_label||'פופולרי'):'');
				tip.appendChild(tipTitle);
				tip.appendChild(tipMeta);
				tip.appendChild(tipStatus);
				var priceInfo=unitPriceInfo(u,meta);
				if(priceInfo&&priceInfo.kind!=='empty'){
					var tipPrice=document.createElement('small');
					tipPrice.className='nlp3d-price';
					tipPrice.textContent=priceInfo.text+' · לא מחייב';
					tip.appendChild(tipPrice);
				}
				b.appendChild(hit);
				b.appendChild(dot);
				b.appendChild(text);
				b.appendChild(tip);
				b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();if(Date.now()<suppressUnitClickUntil){return}activateStagePick(b,u,'stage-pick')});
				stagePicks.appendChild(b);
			});
		}
		function syncStagePicks(){
			if(!stagePicks){return}
			stagePicks.querySelectorAll('.nlp3d-stage-pick,.nlp3d-cell').forEach(function(p){
				var on=!!(activeUnit&&p.dataset.unit===activeUnit.id);
				p.classList.toggle('is-active',on);
				p.setAttribute('aria-pressed',on?'true':'false');
			});
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
				var tipMeta=unitSummaryText(u);
				t.textContent=selectedTitle(u)+(tipMeta?' · '+tipMeta:'');
				poly.appendChild(t);
				poly.addEventListener('click',function(e){e.stopPropagation();if(Date.now()<suppressUnitClickUntil){e.preventDefault();return}selectUnit(u.id,'facade')});
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
			if(activeUnit&&activeUnit.id){
				root.dataset.activeUnit=activeUnit.id;
			}else{
				root.removeAttribute('data-active-unit');
				if(modelViewer){modelViewer.removeAttribute('data-active-unit')}
			}
		}
		function syncModelViewerCamera(){
			if(!modelViewer||!activeUnit){return}
			if(activeUnit.camera_orbit){
				modelViewer.setAttribute('camera-orbit',activeUnit.camera_orbit);
			}
			var target=activeUnit.hotspot_position||'';
			if(!target){
				var hotspot=modelHotspots.find(function(h){return h.dataset.unit===activeUnit.id});
				if(hotspot&&hotspot.dataset.position){target=hotspot.dataset.position}
			}
			if(target){modelViewer.setAttribute('camera-target',target)}
			if(modelViewer.jumpCameraToGoal){modelViewer.jumpCameraToGoal()}
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
				var summaryText=unitSummaryText(u);
				var unitTitle=document.createElement('strong');
				unitTitle.textContent=selectedTitle(u)+(summaryText?' ·':'');
				var unitMeta=document.createElement('span');
				unitMeta.textContent=(summaryText?summaryText+' · ':'')+statusLabel(u.status);
				b.appendChild(unitTitle);
				b.appendChild(unitMeta);
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
				chip.textContent=(u.title||u.id)+' ?';
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
			if(!activeUnit){return}
			var metaText=unitSummaryText(activeUnit);
			if(dockTitle){dockTitle.textContent=selectedTitle(activeUnit)+(metaText?' ·':'')}
			if(dockMeta){
				dockMeta.textContent=(metaText?metaText+' · ':'')+statusLabel(activeUnit.status);
			}
			renderStageCard();
		}
		function renderStageCard(){
			if(!stageCard||!activeUnit){return}
			stageCard.hidden=!hasStageSelection||stageCardDismissed;
			if(stageWrap){stageWrap.classList.toggle('has-stage-selection',hasStageSelection)}
			root.classList.toggle('has-stage-selection',hasStageSelection);
			if(!hasStageSelection||stageCardDismissed){return}
			stageCard.dataset.status=activeUnit.status||'available';
			stageCard.dataset.recommended=isRecommendedUnit(activeUnit)?'1':'0';
			var metaText=unitSummaryText(activeUnit);
			if(stageCardTitle){stageCardTitle.textContent=selectedTitle(activeUnit)+(metaText?' ·':'')}
			if(stageCardMeta){
				stageCardMeta.textContent=metaText||'פרטי דירה לפי בחירה';
			}
			if(stageCardTags){
				stageCardTags.innerHTML='';
				unitBuyerTags(activeUnit,meta).forEach(function(tag){
					var chip=document.createElement('span');
					chip.textContent=tag;
					stageCardTags.appendChild(chip);
				});
			}
			var priceInfo=unitPriceInfo(activeUnit,meta);
			if(stageCardPrice){
				stageCardPrice.textContent=priceInfo.text;
				stageCardPrice.dataset.kind=priceInfo.kind;
				stageCardPrice.title=priceInfo.kind==='estimate'?(priceInfo.note||'אומדן לא מחייב'):'';
			}
			if(stageCardStatus){
				stageCardStatus.textContent=statusLabel(activeUnit.status);
				stageCardStatus.dataset.status=activeUnit.status||'available';
			}
			if(stageCardView){stageCardView.textContent=activeUnit.view||activeUnit.dir||'מבט לפי כיוון'}
			if(stageCardNote){stageCardNote.textContent=unitBuyerNote(activeUnit,meta)}
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
		function keepStageInView(){
			if(!stageWrap){return}
			window.requestAnimationFrame(function(){
				var rect=stageWrap.getBoundingClientRect();
				if(rect.top<72||rect.top>window.innerHeight*.45){
					stageWrap.scrollIntoView({behavior:'smooth',block:'start'});
				}
			});
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
				keepStageInView();
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
				modelViewer.setAttribute('camera-orbit',Math.round(currentAngle)+'deg '+(meta.camera_mid_polar||'81.5deg')+' auto');
			}
		}
		function setTilt(tilt){
			if(horizontalCamera){
				currentTilt=62;
				scene.style.setProperty('--tilt',currentTilt+'deg');
				return;
			}
			currentTilt=Math.max(48,Math.min(72,tilt));
			scene.style.setProperty('--tilt',currentTilt+'deg');
		}
		function setZoom(zoom){
			currentZoom=Math.max(0.86,Math.min(1.34,zoom));
			scene.style.setProperty('--model-zoom',currentZoom);
			scene.classList.toggle('is-zoomed',currentZoom>1.04);
			if(modelViewer){
				modelViewer.setAttribute('field-of-view',Math.round(24/currentZoom)+'deg');
			}
		}
		function selectFloor(f){
			activeFloor=f;
			var next=unitForFloor(f);
			if(next){activeUnit=next}
			hasStageSelection=!!activeUnit;
			renderAll(false);
			syncModelViewerCamera();
			if(modelViewer){
				var y=(Number(meta.ground_elevation_m)||0)+((Number(f)||1)-1)*(Number(meta.floor_height_m)||3.05);
				modelViewer.setAttribute('camera-target','0m '+(Math.round(y*10)/10)+'m 0m');
				if(modelViewer.jumpCameraToGoal){modelViewer.jumpCameraToGoal()}
			}
			if(activeUnit){storageSet(storeKey+'-unit',activeUnit.id)}
			track('select_floor',{floor:f,unit:activeUnit&&activeUnit.id});
		}
		function selectUnit(id,source){
			var next=unitById(id);
			if(next){activeUnit=next;activeFloor=parseInt(next.floor||activeFloor,10)}
			hasStageSelection=!!next||hasStageSelection;
			if(next){stageCardDismissed=false}
			closeStagePickTips();
			renderAll(false);
			syncModelViewerCamera();
			if(activeUnit){storageSet(storeKey+'-unit',activeUnit.id)}
			track('select_unit',{floor:activeFloor,unit:id,source:source||'unknown'});
		}
		function renderAll(includeTower){
			if(includeTower){renderTower();renderFacade();renderStagePicks()}else{root.querySelectorAll('.nlp3d-plate').forEach(function(p){p.classList.toggle('is-active',parseInt(p.dataset.floor,10)===activeFloor)});syncFacade();syncStagePicks()}
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
		if(stageTour){
			stageTour.addEventListener('click',function(){
				setLiveView(false,'stage-tour');
				activeTool='media';
				toolButtons.forEach(function(x){x.classList.toggle('is-active',x.dataset.tool==='media')});
				renderToolPanel();
				if(detail){detail.scrollIntoView({behavior:'smooth',block:'center'})}
				track('stage_tour',{unit:activeUnit&&activeUnit.id});
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
		if(facadeClose){
			facadeClose.addEventListener('click',function(e){
				e.preventDefault();
				e.stopPropagation();
				setFacadeDismissed(true,'close-button');
			});
		}
		if(facadeRestore){
			facadeRestore.addEventListener('click',function(e){
				e.preventDefault();
				e.stopPropagation();
				setFacadeDismissed(false,'restore-button');
			});
		}
		if(stageCardClose&&stageCard){
			stageCardClose.addEventListener('click',function(e){
				e.preventDefault();
				e.stopPropagation();
				stageCardDismissed=true;
				stageCard.hidden=true;
				track('stage_card_close',{unit:activeUnit&&activeUnit.id});
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
				if(Date.now()<suppressUnitClickUntil){return}
				if(h.getAttribute('aria-disabled')==='true'){return}
				selectUnit(h.dataset.unit,'model-viewer-hotspot');
			});
		});
		if(modelViewer){
			modelViewer.addEventListener('load',function(){root.classList.add('has-model-viewer-loaded');root.classList.remove('has-model-viewer-error');if(modelError){modelError.hidden=true}syncModelViewerCamera();track('model_viewer_load',{model:true})});
			modelViewer.addEventListener('error',function(){root.classList.add('has-model-viewer-error');if(modelError){modelError.hidden=false}track('model_viewer_error',{model:true})});
			modelViewer.addEventListener('click',function(e){
				if(Date.now()<suppressUnitClickUntil){return}
				if(e.target&&e.target.closest&&e.target.closest('.nlp3d-mv-hotspot')){return}
				if(selectNearestModelPickFromPoint(eventPoint(e),'model-surface-tap')){
					e.preventDefault();
					e.stopPropagation();
				}
			});
		}
		function eventPoint(e){
			var t=e.touches&&e.touches[0]?e.touches[0]:(e.changedTouches&&e.changedTouches[0]?e.changedTouches[0]:e);
			return {x:t.clientX,y:t.clientY};
		}
		function pointHitsStageReturn(e){
			if(!stageReturn||!viewFrame||viewFrame.hidden){return false}
			var p=eventPoint(e);
			var r=stageReturn.getBoundingClientRect();
			return p.x>=r.left&&p.x<=r.right&&p.y>=r.top&&p.y<=r.bottom;
		}
		function forceReturnFromEvent(e,source){
			if(!pointHitsStageReturn(e)){return false}
			e.preventDefault();
			e.stopPropagation();
			if(e.stopImmediatePropagation){e.stopImmediatePropagation()}
			setLiveView(false,source);
			return true;
		}
		if(stageReturn){
			stageReturn.addEventListener('click',function(e){forceReturnFromEvent(e,'return')||setLiveView(false,'return')});
		}
		if(viewFrame&&stageReturn){
			['pointerdown','mousedown','touchstart','click'].forEach(function(type){
				document.addEventListener(type,function(e){forceReturnFromEvent(e,'return-document-capture')},true);
			});
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
			if(e.key==='Escape'){closeCompare();closePlan();closeStagePickTips()}
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
		function dragExcludedTarget(target){
			if(target&&target.closest&&target.closest('.nlp3d-stage-pick,.nlp3d-hotspot,.nlp3d-hotspot-hit')){return false}
			return target&&target.closest&&target.closest('button,a,input,.nlp3d-model-viewer,.nlp3d-mv-hotspot,.nlp3d-stage-card,.nlp3d-stage-viewframe');
		}
		function startDragAt(p,id,target){
			var unitNode=target&&target.closest?target.closest('[data-unit]'):null;
			dragState={x:p.x,y:p.y,angle:currentAngle,tilt:currentTilt,id:id||0,unitId:unitNode&&unitNode.dataset?unitNode.dataset.unit:'',lastX:p.x,lastT:Date.now(),vx:0};
			scene.classList.add('is-dragging');
			scene.classList.remove('is-orbit');
			if(orbit){orbit.classList.remove('is-active')}
		}
		function moveDragAt(p){
			if(!dragState){return}
			var t=Date.now();
			var dt=Math.max(16,t-dragState.lastT);
			dragState.vx=(p.x-dragState.lastX)/dt;
			dragState.lastX=p.x;
			dragState.lastT=t;
			setAngle(dragState.angle+(p.x-dragState.x)*0.22);
			if(!horizontalCamera){setTilt(dragState.tilt-(p.y-dragState.y)*0.08)}
		}
		function endDragAt(p){
			if(!dragState){return}
			var moved=Math.abs(p.x-dragState.x)+Math.abs(p.y-dragState.y);
			var momentum=Math.max(-120,Math.min(120,(dragState.vx||0)*180));
			var tappedUnit=dragState.unitId||'';
			dragState=null;
			scene.classList.remove('is-dragging');
			var now=Date.now();
			if(moved>=8){suppressUnitClickUntil=now+450}
			if(moved<8&&tappedUnit){selectUnit(tappedUnit,'stage-pick-tap');return}
			if(moved<8&&selectNearestModelPickFromPoint(p,'stage-near-pick')){lastTapAt=now;return}
			if(moved<8&&now-lastTapAt<320){
				setZoom(currentZoom>1.05?1:1.22);
				track('model_double_tap_zoom',{zoom:Math.round(currentZoom*100)/100});
			}
			if(moved<8){lastTapAt=now}
			if(moved>=8&&Math.abs(momentum)>4){setAngle(currentAngle+momentum)}
			if(moved>=8){track('drag',{angle:currentAngle})}
		}
		scene.addEventListener('pointerdown',function(e){
			if((facadePlane&&!modelViewer)||dragExcludedTarget(e.target)){return}
			startDragAt({x:e.clientX,y:e.clientY},e.pointerId,e.target);
			if(scene.setPointerCapture){scene.setPointerCapture(e.pointerId)}
		});
		scene.addEventListener('pointermove',function(e){
			moveDragAt({x:e.clientX,y:e.clientY});
		});
		function endDrag(e){
			if(!dragState){return}
			if(scene.releasePointerCapture){try{scene.releasePointerCapture(dragState.id)}catch(err){}}
			endDragAt({x:e.clientX,y:e.clientY});
		}
		scene.addEventListener('pointerup',endDrag);
		scene.addEventListener('pointercancel',endDrag);
		scene.addEventListener('touchstart',function(e){
			if((facadePlane&&!modelViewer)||dragExcludedTarget(e.target)||!e.touches||!e.touches[0]){return}
			e.preventDefault();
			startDragAt(eventPoint(e),0,e.target);
		},{passive:false});
		scene.addEventListener('touchmove',function(e){
			if(!dragState){return}
			e.preventDefault();
			moveDragAt(eventPoint(e));
		},{passive:false});
		scene.addEventListener('touchend',function(e){
			if(!dragState){return}
			e.preventDefault();
			endDragAt(eventPoint(e));
		},{passive:false});
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
		fitMobileShowroom();
		window.requestAnimationFrame(fitMobileShowroom);
		window.setTimeout(fitMobileShowroom,500);
		window.addEventListener('resize',fitMobileShowroom,{passive:true});
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

		wp_register_style( 'nadlan-p3d', '', array(), '1.69.14' );
		wp_enqueue_style( 'nadlan-p3d' );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_lovable_showroom_v1690_css() );

		$post_id = is_singular( 'nadlan_project' ) ? (int) get_queried_object_id() : 0;
		if ( $post_id > 0 && get_post_meta( $post_id, 'project_model_glb', true ) !== '' ) {
			wp_register_script( 'nadlan-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js', array(), '4.3.1', true );
			wp_script_add_data( 'nadlan-model-viewer', 'type', 'module' );
			wp_enqueue_script( 'nadlan-model-viewer' );
		}

		wp_register_script( 'nadlan-p3d', '', array(), '1.69.14', true );
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
			'renderer'         => 'premium_showroom_v10_buyer_product',
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
			'model_full_360'   => false,
			'camera_lock_default' => 'horizontal',
			'camera_lock_cms_v1680' => true,
			'model_viewer_ready' => true,
			'model_viewer_module_tag' => true,
			'model_viewer_reveal' => 'auto',
			'model_viewer_loading' => 'auto',
			'model_viewer_version' => '4.3.1',
			'model_viewer_lazy' => true,
			'model_viewer_hotspots' => true,
			'model_viewer_hotspots_hidden_when_overlay_picks_v1694' => true,
			'model_surface_tap_select_v1695' => true,
			'model_surface_tap_floor_bias_v1696' => true,
			'toolbar_empty_space_tap_passthrough_v1697' => true,
			'mobile_marker_clarity_v1699' => true,
			'mobile_marker_spread_v16910' => true,
			'selection_dock_separator_v16911' => true,
			'selection_dock_inline_separator_v16912' => true,
			'selection_summary_text_v16913' => true,
			'product_selector_v1641' => true,
			'status_colored_unit_picks' => true,
			'recommended_unit_pulse' => true,
			'stage_intro_above_model' => true,
			'generic_project_copy_v1675' => true,
			'facade_dismissible_v1680' => true,
			'facade_restore_v1680' => true,
			'legacy_facade_not_emitted_in_dual_v1680' => true,
			'no_silent_showroom_fallbacks_v1680' => true,
			'model_error_notice_v1680' => true,
			'facade_polygons_compounds_v1680' => true,
			'facade_plane_mobile_overflow_v1681' => true,
			'real_facade_asset_required_v1681' => true,
			'fake_facade_grid_removed_v1681' => true,
			'dimri_yama_concept_facade_v1682' => true,
			'concept_facade_label_v1682' => true,
			'public_showroom_surface_v1690' => true,
			'public_language_cleanup_v1690' => true,
			'visual_qa_preview_v1690' => true,
			'unit_panel_tabs_v1680' => true,
			'stage_return_capture_fix' => true,
			'mobile_containment_v1642' => true,
			'headline_contrast_v1642' => true,
			'return_document_capture_v1642' => true,
			'mobile_hotspot_declutter_v1643' => true,
			'mobile_safe_width_v1643' => true,
			'mobile_model_drag_fallback_v1643' => true,
			'premium_dot_markers_v1644' => true,
			'mobile_touch_drag_v1644' => true,
			'hotspot_drag_passthrough_v1645' => true,
			'stage_pick_drag_v1646' => true,
			'stage_pick_tap_select_v1647' => true,
			'mobile_edge_guard_v1648' => true,
			'buyer_card_v1649' => true,
			'admin_unit_builder_v1650' => true,
			'admin_callback_clean_v1651' => true,
			'rest_showroom_fields_v1651' => true,
			'showroom_payload_api_v1652' => true,
			'stage_card_render_v1653' => true,
			'serp_intro_copy_v1653' => true,
			'model_fallback_hides_after_glb_v1653' => true,
			'hotspot_tap_preview_v1653' => true,
			'heading_contrast_v1653' => true,
			'apartment_cell_selector_v1655' => true,
			'mobile_cell_polish_v1656' => true,
			'dual_showroom_v1661' => true,
			'embedded_selector_with_glb_v1661' => true,
			'stage_xywh_fields_v1661' => true,
			'showroom_dna_v1664' => true,
			'facade_picker_side_by_side_v1664' => true,
			'stage_card_dismiss_v1664' => true,
			'context_pins_v1664' => true,
			'poster_social_v1664' => true,
			'mobile_containment_v1668' => true,
			'inventory_status_semantics_v1669' => true,
			'showroom_hierarchy_v1670' => true,
			'article_alignment_v1671'  => true,
			'page_finishing_layer_v1673' => true,
			'page_finishing_dedupe_v1674' => true,
			'compact_actions_v1672'    => true,
			'showroom_payload_fields' => count( nadlan_p3d_showroom_fields() ),
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
			'stage_card_single_action_group_v16914' => true,
			'projects_with_3d' => (int) $q->found_posts,
			'projects_with_glb' => (int) $model_q->found_posts,
		);
		wp_reset_postdata();
		return $out;
	}
);


