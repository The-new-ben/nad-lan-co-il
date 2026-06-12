<?php
/**
 * nadlan-config — Card schema + SEO guards (v1.5.0)
 *
 * 1) JSON-LD per card type (LocalBusiness/GeneralContractor, Residence/
 *    ApartmentComplex, RealEstateListing) — stats-rich, machine-readable, which
 *    is what AI answer-engines and Google reward.
 * 2) THIN-CONTENT NOINDEX guard: any card still at data_quality=stub (or with a
 *    body below the word floor) is noindex,follow. This is the anti-cannibalization
 *    + anti-thin-content safeguard from the research — stubs don't compete with
 *    keyword pages and don't dilute crawl budget. Once enriched (original ChatGPT
 *    prose pushed via import-enrich), the card becomes indexable.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_CARD_WORD_FLOOR = 80;

if ( ! function_exists( 'nadlan_card_is_indexable' ) ) {
	function nadlan_card_is_indexable( $post_id ) {
		if ( get_post_meta( $post_id, 'data_quality', true ) === 'enriched' ) { return true; }
		if ( get_post_meta( $post_id, 'claim_status', true ) === 'verified' ) { return true; }
		$words = str_word_count( wp_strip_all_tags( (string) get_post_field( 'post_content', $post_id ) ) );
		// Hebrew word_count is unreliable; also count by spaces.
		$alt = count( preg_split( '/\s+/', trim( wp_strip_all_tags( (string) get_post_field( 'post_content', $post_id ) ) ) ) );
		return max( $words, $alt ) >= NADLAN_CARD_WORD_FLOOR;
	}
}

/* ---- noindex stubs via wp_robots (WP 5.7+) ---- */
if ( ! function_exists( 'nadlan_card_robots' ) ) {
	function nadlan_card_robots( $robots ) {
		if ( ! is_singular( array( 'nadlan_project', 'nadlan_professional', 'nadlan_property' ) ) ) {
			return $robots;
		}
		if ( ! nadlan_card_is_indexable( get_queried_object_id() ) ) {
			$robots['noindex'] = true;
			$robots['follow']  = true;
			unset( $robots['index'] );
		}
		return $robots;
	}
}
add_filter( 'wp_robots', 'nadlan_card_robots', 20 );

/* Force the same through Yoast if it's controlling the robots meta */
add_filter( 'wpseo_robots', function ( $string ) {
	if ( is_singular( array( 'nadlan_project', 'nadlan_professional', 'nadlan_property' ) )
		&& ! nadlan_card_is_indexable( get_queried_object_id() ) ) {
		return 'noindex, follow';
	}
	return $string;
}, 20 );

/* ---- JSON-LD ---- */
if ( ! function_exists( 'nadlan_card_jsonld' ) ) {
	function nadlan_card_jsonld() {
		if ( ! is_singular( array( 'nadlan_project', 'nadlan_professional', 'nadlan_property', 'nadlan_auction' ) ) ) {
			return;
		}
		$id   = get_queried_object_id();
		$type = get_post_type( $id );
		$url  = get_permalink( $id );
		$name = get_the_title( $id );
		$g    = function ( $k ) use ( $id ) { return get_post_meta( $id, $k, true ); };
		$data = null;

		if ( $type === 'nadlan_professional' ) {
			$prof = (string) $g( 'profession' );
			$ld_type = ( $prof === 'kablan' ) ? 'GeneralContractor' : 'LocalBusiness';
			$data = array(
				'@context' => 'https://schema.org', '@type' => $ld_type,
				'name' => $name, 'url' => $url,
				'telephone' => $g( 'phone' ) ?: null,
				'email' => $g( 'email' ) ?: null,
				'identifier' => $g( 'registry_number' ) ? array(
					'@type' => 'PropertyValue', 'propertyID' => 'מספר רשם הקבלנים', 'value' => $g( 'registry_number' )
				) : null,
				'address' => array_filter( array(
					'@type' => 'PostalAddress',
					'streetAddress' => $g( 'address' ) ?: null,
					'addressLocality' => $g( 'city' ) ?: null,
					'addressCountry' => 'IL',
				) ),
				'areaServed' => $g( 'areas_served' ) ?: $g( 'city' ) ?: null,
			);
			if ( (float) $g( 'rating' ) > 0 && (int) $g( 'reviews_count' ) > 0 ) {
				$data['aggregateRating'] = array(
					'@type' => 'AggregateRating',
					'ratingValue' => (float) $g( 'rating' ), 'reviewCount' => (int) $g( 'reviews_count' ),
				);
			}
		} elseif ( $type === 'nadlan_project' ) {
			$lat = (float) $g( 'lat' );
			$lng = (float) $g( 'lng' );
			$amenities = array_filter( array_map( 'trim', explode( ',', (string) $g( 'amenities' ) ) ) );
			$same_as   = array_filter( array_map( 'trim', explode( ',', (string) $g( 'official_site_url' ) ) ) );
			$compound  = get_the_terms( $id, 'nadlan_compound' );
			$compound  = ( $compound && ! is_wp_error( $compound ) ) ? $compound[0] : null;
			$data = array_filter( array(
				'@context' => 'https://schema.org', '@type' => 'ApartmentComplex',
				'name' => $name, 'url' => $url,
				'description' => wp_strip_all_tags( get_the_excerpt( $id ) ) ?: null,
				'image' => get_the_post_thumbnail_url( $id, 'large' ) ?: null,
				'numberOfAccommodationUnits' => (int) $g( 'num_units' ) ?: null,
				'sameAs' => $same_as ?: null,
				'containedInPlace' => $compound ? array(
					'@type' => 'Place',
					'name'  => $compound->name,
					'url'   => get_term_link( $compound ),
				) : null,
				'geo' => ( $lat && $lng ) ? array(
					'@type' => 'GeoCoordinates', 'latitude' => $lat, 'longitude' => $lng,
				) : null,
				'amenityFeature' => $amenities ? array_map( function ( $a ) {
					return array( '@type' => 'LocationFeatureSpecification', 'name' => $a, 'value' => true );
				}, $amenities ) : null,
				'address' => array_filter( array(
					'@type' => 'PostalAddress',
					'streetAddress' => $g( 'address' ) ?: null,
					'addressLocality' => $g( 'city' ) ?: null,
					'addressCountry' => 'IL',
				) ),
			) );
			if ( $g( 'price_range' ) !== '' && $g( 'price_range' ) !== false ) {
				$data['offers'] = array(
					'@type'         => 'AggregateOffer',
					'priceCurrency' => 'ILS',
					'lowPrice'      => (float) $g( 'price_min' ) ?: null,
					'highPrice'     => (float) $g( 'price_max' ) ?: null,
					'description'   => sanitize_text_field( (string) $g( 'price_range' ) ),
					'availability'  => 'https://schema.org/InStock',
				);
				$data['offers'] = array_filter( $data['offers'] );
			}
			$faq_raw = (string) $g( 'project_faq_json' );
			if ( $faq_raw !== '' ) {
				$faq = json_decode( $faq_raw, true );
				if ( is_array( $faq ) && $faq ) {
					$entities = array();
					foreach ( $faq as $qa ) {
						if ( empty( $qa['q'] ) || empty( $qa['a'] ) ) { continue; }
						$entities[] = array(
							'@type' => 'Question',
							'name'  => sanitize_text_field( $qa['q'] ),
							'acceptedAnswer' => array(
								'@type' => 'Answer',
								'text'  => sanitize_text_field( $qa['a'] ),
							),
						);
					}
					if ( $entities ) {
						echo "\n<script type=\"application/ld+json\">" . wp_json_encode( array(
							'@context'   => 'https://schema.org',
							'@type'      => 'FAQPage',
							'mainEntity' => $entities,
						), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
					}
				}
			}
		} elseif ( $type === 'nadlan_property' ) {
			$data = function_exists( 'nadlan_build_real_estate_listing_jsonld' )
				? nadlan_build_real_estate_listing_jsonld( $id )
				: array_filter( array(
					'@context' => 'https://schema.org', '@type' => 'RealEstateListing',
					'name' => $name, 'url' => $url,
					'datePosted' => get_the_date( 'c', $id ),
				) );
		} elseif ( $type === 'nadlan_auction' ) {
			$data = array_filter( array(
				'@context' => 'https://schema.org', '@type' => 'Event',
				'name' => $name, 'url' => $url, 'eventStatus' => 'https://schema.org/EventScheduled',
				'startDate' => $g( 'start_time' ) ?: null, 'endDate' => $g( 'end_time' ) ?: null,
				'eventAttendanceMode' => 'https://schema.org/OnlineEventAttendanceMode',
			) );
		}

		if ( $data ) {
			$data = apply_filters( 'nadlan_card_jsonld', $data, $id, $type );
			do_action( 'nadlan_card_jsonld_ready', $data, $id, $type );
			echo "\n<script type=\"application/ld+json\">" . wp_json_encode( array_filter( $data ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
		}
	}
}
add_action( 'wp_head', 'nadlan_card_jsonld', 20 );
