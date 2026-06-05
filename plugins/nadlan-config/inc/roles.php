<?php
/**
 * nadlan-config - GAP 6 roles and listing capabilities.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_ROLES_VERSION = 1;

if ( ! function_exists( 'nadlan_roles_card_cpts' ) ) {
	function nadlan_roles_card_cpts() {
		return defined( 'NADLAN_CARD_CPTS' )
			? NADLAN_CARD_CPTS
			: array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' );
	}
}

if ( ! function_exists( 'nadlan_listing_capabilities' ) ) {
	function nadlan_listing_capabilities() {
		return array(
			'edit_post'              => 'edit_listing',
			'read_post'              => 'read',
			'delete_post'            => 'delete_listing',
			'edit_posts'             => 'edit_listings',
			'edit_others_posts'      => 'edit_others_listings',
			'delete_posts'           => 'delete_listings',
			'publish_posts'          => 'publish_listings',
			'read_private_posts'     => 'read_private_listings',
			'create_posts'           => 'publish_listings',
			'edit_published_posts'   => 'edit_published_listings',
			'delete_published_posts' => 'delete_published_listings',
			'edit_private_posts'     => 'edit_private_listings',
			'delete_private_posts'   => 'delete_private_listings',
			'delete_others_posts'    => 'delete_others_listings',
		);
	}
}

if ( ! function_exists( 'nadlan_roles_administrator_caps' ) ) {
	function nadlan_roles_administrator_caps() {
		return array(
			'edit_listings',
			'edit_others_listings',
			'edit_published_listings',
			'edit_private_listings',
			'publish_listings',
			'delete_listings',
			'delete_others_listings',
			'delete_published_listings',
			'delete_private_listings',
			'read_private_listings',
			'manage_advertisers',
		);
	}
}

if ( ! function_exists( 'nadlan_roles_assign_user' ) ) {
	function nadlan_roles_assign_user( $user_id, $owns_listing = null ) {
		$user_id = (int) $user_id;
		if ( $user_id < 1 ) { return false; }
		$user = new WP_User( $user_id );
		if ( ! $user || ! $user->exists() ) { return false; }
		if ( $owns_listing === null ) {
			$owned = get_posts( array(
				'post_type'      => nadlan_roles_card_cpts(),
				'post_status'    => 'any',
				'fields'         => 'ids',
				'posts_per_page' => 1,
				'meta_query'     => array( array( 'key' => 'owner_user_id', 'value' => $user_id ) ),
			) );
			$owns_listing = ! empty( $owned );
		}
		$user->add_role( $owns_listing ? 'nadlan_advertiser' : 'nadlan_buyer' );
		return true;
	}
}

if ( ! function_exists( 'nadlan_roles_migrate_existing_users' ) ) {
	function nadlan_roles_migrate_existing_users() {
		$users = get_users( array( 'fields' => array( 'ID' ) ) );
		foreach ( $users as $user ) {
			nadlan_roles_assign_user( (int) $user->ID, null );
		}
	}
}

if ( ! function_exists( 'nadlan_roles_setup' ) ) {
	function nadlan_roles_setup() {
		if ( (int) get_option( 'nadlan_roles_version', 0 ) >= NADLAN_ROLES_VERSION ) {
			return;
		}

		remove_role( 'nadlan_advertiser' );
		add_role( 'nadlan_advertiser', 'מפרסם נדל״ן', array(
			'read'                    => true,
			'edit_listings'           => true,
			'edit_published_listings' => true,
			'publish_listings'        => true,
			'delete_listings'         => true,
			'upload_files'            => true,
		) );

		add_role( 'nadlan_buyer', 'קונה', array( 'read' => true ) );

		$admin = get_role( 'administrator' );
		if ( $admin ) {
			foreach ( nadlan_roles_administrator_caps() as $cap ) {
				$admin->add_cap( $cap );
			}
		}

		nadlan_roles_migrate_existing_users();
		update_option( 'nadlan_roles_version', NADLAN_ROLES_VERSION, false );
	}
}

if ( ! function_exists( 'nadlan_roles_uninstall' ) ) {
	function nadlan_roles_uninstall() {
		$caps = array_unique( array_diff( array_merge(
			array_values( nadlan_listing_capabilities() ),
			nadlan_roles_administrator_caps(),
			array( 'manage_advertisers' )
		), array( 'read', 'upload_files' ) ) );
		if ( function_exists( 'wp_roles' ) ) {
			foreach ( array_keys( wp_roles()->roles ) as $role_name ) {
				$role = get_role( $role_name );
				if ( ! $role ) { continue; }
				foreach ( $caps as $cap ) {
					$role->remove_cap( $cap );
				}
			}
		}
		remove_role( 'nadlan_advertiser' );
		remove_role( 'nadlan_buyer' );
		delete_option( 'nadlan_roles_version' );
	}
}

register_activation_hook( dirname( __DIR__ ) . '/nadlan-config.php', 'nadlan_roles_setup' );
register_uninstall_hook( dirname( __DIR__ ) . '/nadlan-config.php', 'nadlan_roles_uninstall' );
add_action( 'admin_init', 'nadlan_roles_setup' );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$counts = count_users();
	$roles = (array) ( $counts['avail_roles'] ?? array() );
	$out['roles'] = array(
		'version'             => (int) get_option( 'nadlan_roles_version', 0 ),
		'nadlan_advertisers'  => (int) ( $roles['nadlan_advertiser'] ?? 0 ),
		'nadlan_buyers'       => (int) ( $roles['nadlan_buyer'] ?? 0 ),
	);
	return $out;
} );
