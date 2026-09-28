<?php
/**
 * ProNetwork v98 (design system ProCard, 28.9.2026): the professional card of the network, its facts and its privacy.
 *
 * The owner, 28.9: "professionals still look very basic with this circle and a letter ... we talked about a social network".
 * Codex (28.9, docs: scratchpad codex consult): every card gets a deliberate identity (a cover band with an abstract
 * architectural pattern, a portrait or a designed monogram), the strongest register fact first, and separate trust labels
 * (in the register / licence in the brokers' register / managed by its owner); paying never buys a label. Save is a private
 * shortlist in the browser. Nothing invented: the facts are the contractors register's (data/register-facts.json, built by
 * scripts/pros/build_plugin_facts.py from data.gov.il) or the profile's own.
 *
 * Privacy (found 28.9): the register's private-person records carried a home address, a phone and an e-mail onto the public
 * page, the search data and the REST API. A private person who has not taken over the profile shows the city only.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_pc_facts' ) ) {
	/** The register's business facts of a contractor card: array( y => since, b => [ [branch, class, unlimited] ], r => recognised, co => company ), or null. */
	function nadlan_pc_facts( $id ) {
		static $all = null;
		if ( 'kablan' !== (string) get_post_meta( $id, 'profession', true ) ) { return null; }
		if ( null === $all ) {
			$p   = dirname( __DIR__ ) . '/data/register-facts.json';
			$d   = is_readable( $p ) ? json_decode( (string) file_get_contents( $p ), true ) : null;
			$all = is_array( $d ) && isset( $d['f'] ) ? (array) $d['f'] : array();
		}
		$k = (string) get_post_meta( $id, 'registry_number', true );
		return ( '' !== $k && isset( $all[ $k ] ) ) ? $all[ $k ] : null;
	}
}

if ( ! function_exists( 'nadlan_pc_is_private' ) ) {
	/** A private person from a public register who has not taken over the profile: the city only, never address/phone/e-mail. */
	function nadlan_pc_is_private( $id ) {
		if ( 'nadlan_professional' !== get_post_type( $id ) ) { return false; }
		// one switch back, without a release: option nadlan_register_contacts = show (28.9: hidden by default)
		if ( 'show' === (string) get_option( 'nadlan_register_contacts', 'hide' ) ) { return false; }
		if ( 'verified' === (string) get_post_meta( $id, 'claim_status', true ) ) { return false; }
		$src = (string) get_post_meta( $id, 'source', true );
		if ( ! in_array( $src, array( 'pinkas_hakablanim', 'metavhim' ), true ) ) { return false; }
		$f = nadlan_pc_facts( $id );
		if ( $f && ! empty( $f['co'] ) ) { return false; }
		return ! preg_match( '/בע["״”]?מ|בעמ\b|חברה|\bltd\b/iu', (string) get_the_title( $id ) );
	}
}

if ( ! function_exists( 'nadlan_pc_mono' ) ) {
	/** Two letters for the designed monogram: the first letters of the first two words of the name. */
	function nadlan_pc_mono( $name ) {
		$w = preg_split( '/\s+/u', trim( preg_replace( '/[^\p{L}\s]/u', ' ', (string) $name ) ) );
		$a = isset( $w[0] ) ? mb_substr( $w[0], 0, 1 ) : '';
		$b = isset( $w[1] ) ? mb_substr( $w[1], 0, 1 ) : '';
		return $a . $b;
	}
}

if ( ! function_exists( 'nadlan_pc_fact' ) ) {
	/** The strongest fact of the card: array( label, value ), or null. */
	function nadlan_pc_fact( $id, $prof_key ) {
		if ( 'kablan' === $prof_key ) {
			$f = nadlan_pc_facts( $id );
			if ( $f && ! empty( $f['b'] ) ) {
				$parts = array();
				foreach ( array_slice( (array) $f['b'], 0, 2 ) as $b ) { $parts[] = trim( $b[0] . ' ' . $b[1] ); }
				$more  = count( (array) $f['b'] ) > 2 ? ' ועוד ענף' : '';
				$label = ! empty( $f['y'] ) ? 'רשום בפנקס הקבלנים מאז ' . (int) $f['y'] : 'בפנקס הקבלנים';
				return array( $label, implode( ' · ', $parts ) . $more );
			}
			$cls = nadlan_meta_norm( get_post_meta( $id, 'classification', true ) );
			return '' !== $cls ? array( 'בפנקס הקבלנים', mb_strlen( $cls ) > 70 ? mb_substr( $cls, 0, 70 ) . '…' : $cls ) : null;
		}
		if ( 'metavech' === $prof_key ) {
			$ln = nadlan_meta_norm( get_post_meta( $id, 'license_number', true ) );
			$ln = '' !== $ln ? $ln : nadlan_meta_norm( get_post_meta( $id, 'registry_number', true ) );
			return '' !== $ln ? array( 'רישיון תיווך', $ln ) : null;
		}
		$pc  = (int) get_post_meta( $id, 'project_count', true );
		$yr  = (int) get_post_meta( $id, 'years_active', true );
		$bits = array();
		if ( $pc > 0 ) { $bits[] = number_format_i18n( $pc ) . ' פרויקטים'; }
		if ( $yr > 1800 && $yr <= (int) gmdate( 'Y' ) ) { $bits[] = 'פעילה מאז ' . $yr; }
		if ( $bits ) { return array( 'editorial' === (string) get_post_meta( $id, 'source', true ) ? 'לפי פרסומי החברה' : 'מהפרופיל', implode( ' · ', $bits ) ); }
		$reg = nadlan_meta_norm( get_post_meta( $id, 'registry_number', true ) );
		return '' !== $reg ? array( 'מספר רישום', $reg ) : null;
	}
}

if ( ! function_exists( 'nadlan_pc_trust' ) ) {
	/** The trust labels, each a fact of its own; payment never makes one. Returns array( array( text, class ) ). */
	function nadlan_pc_trust( $id, $prof_key ) {
		$t = array();
		if ( 'verified' === (string) get_post_meta( $id, 'claim_status', true ) ) { $t[] = array( '✓ הפרופיל מנוהל בידי בעליו', 'is-owner' ); }
		$src = (string) get_post_meta( $id, 'source', true );
		if ( 'kablan' === $prof_key && ( 'pinkas_hakablanim' === $src || nadlan_pc_facts( $id ) ) ) { $t[] = array( '<b>✓</b> רשום בפנקס הקבלנים', '' ); }
		if ( 'metavech' === $prof_key && ( 'metavhim' === $src || '' !== (string) get_post_meta( $id, 'license_number', true ) ) ) { $t[] = array( '<b>✓</b> רישיון בפנקס המתווכים', '' ); }
		$f = 'kablan' === $prof_key ? nadlan_pc_facts( $id ) : null;
		if ( $f && ! empty( $f['r'] ) ) { $t[] = array( 'מוכר לעבודות ממשלתיות', '' ); }
		if ( $f && ! empty( $f['b'][0][2] ) ) { $t[] = array( 'ללא הגבלת היקף', '' ); }
		return $t;
	}
}

if ( ! function_exists( 'nadlan_pc_assets' ) ) {
	/** The card's style and the save list, once per page (never inside a REST answer: the page already has them). */
	function nadlan_pc_assets() {
		static $done = false;
		if ( $done || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) { return ''; }
		$done = true;
		$css  = plugins_url( 'assets/pronet/procard.css', dirname( __FILE__ ) ) . '?ver=' . rawurlencode( NADLAN_CONFIG_VERSION );
		$js   = <<<'JS'
(function(){var K='nl_saved_pros';function get(){try{return JSON.parse(localStorage.getItem(K)||'[]')||[]}catch(e){return[]}}function put(a){try{localStorage.setItem(K,JSON.stringify(a.slice(0,60)))}catch(e){}}
function chip(){var r=document.querySelector('.nldir-results');if(!r)return null;var c=document.querySelector('.nlpn-saved');if(!c){c=document.createElement('button');c.type='button';c.className='nlpn-saved';c.innerHTML='אנשי המקצוע ששמרתי <b></b>';c.addEventListener('click',sheet);r.parentNode.insertBefore(c,r)}return c}
function mark(){var s=get(),ids=s.map(function(x){return String(x.id)});document.querySelectorAll('.nlpn-save').forEach(function(b){var on=ids.indexOf(b.getAttribute('data-id'))>-1;b.setAttribute('aria-pressed',on?'true':'false');b.setAttribute('aria-label',on?'הסרה מהשמורים':'שמירה')});var c=chip();if(c){c.querySelector('b').textContent=s.length;c.classList.toggle('is-on',s.length>0)}}
function sheet(){var s=get(),d=document.getElementById('nlpn-sheet');if(!d){d=document.createElement('div');d.id='nlpn-sheet';d.className='nlpn-sheet';d.setAttribute('role','dialog');d.setAttribute('aria-label','אנשי המקצוע ששמרתי');document.body.appendChild(d)}d.textContent='';var x=document.createElement('button');x.type='button';x.className='nlpn-x';x.setAttribute('aria-label','סגירה');x.textContent='×';x.addEventListener('click',function(){d.hidden=true});var h=document.createElement('h2');h.textContent='אנשי המקצוע ששמרתי';var ul=document.createElement('ul');s.forEach(function(p){var li=document.createElement('li'),a=document.createElement('a');a.href=p.url;a.textContent=p.name;var sm=document.createElement('small');sm.textContent=p.role||'';a.appendChild(sm);li.appendChild(a);ul.appendChild(li)});var n=document.createElement('p');n.textContent='הרשימה שמורה רק בדפדפן הזה, ואף אחד לא רואה אותה.';d.append(x,h,ul,n);d.hidden=false;x.focus()}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.nlpn-save');if(!b)return;e.preventDefault();var s=get(),id=b.getAttribute('data-id'),i=-1;s.forEach(function(x,k){if(String(x.id)===id)i=k});if(i>-1)s.splice(i,1);else s.unshift({id:id,name:b.getAttribute('data-name'),url:b.getAttribute('data-url'),role:b.getAttribute('data-role')});put(s);mark()});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){var d=document.getElementById('nlpn-sheet');if(d&&!d.hidden)d.hidden=true}});
function boot(){mark();var r=document.querySelector('.nldir-results');if(r&&window.MutationObserver)new MutationObserver(mark).observe(r,{childList:true})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot()})();
JS;
		return '<link rel="stylesheet" id="nlpn-css" href="' . esc_url( $css ) . '"><script id="nlpn-js">' . $js . '</script>';
	}
}

if ( ! function_exists( 'nadlan_pc_save_icon' ) ) {
	function nadlan_pc_save_icon() {
		return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 3.5h11a1 1 0 0 1 1 1v16l-6.5-4.2-6.5 4.2v-16a1 1 0 0 1 1-1z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>';
	}
}
