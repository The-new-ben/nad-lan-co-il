<?php
/**
 * smart-form.php - the conversational form engine (owner order 2026-07-12).
 *
 * "The best form in the world... viral, shareable, easy, AI inside."
 * Research-grounded (Typeform pattern, 650K-submission studies): one
 * question per screen converts 25-40% better than flat forms; progress
 * feedback and late-stage contact questions lift completion further.
 *
 * The engine: config-driven instances (auction seller intake, urban
 * renewal check-in, buyer profile) rendered as an animated one-question
 * card - chips, slide transitions, gold progress bar, back, enter-to-
 * continue, success burst + WhatsApp share. Submissions land in the
 * EXISTING lead machinery (/nadlan/v1/lead) with structured fields, so
 * routing, the inbox and the AI qualify pipeline (when its flag is on)
 * score every submission - the honest "AI inside", not theater.
 * Attach points: [nadlan_smart_form id=x] shortcode + auto-band on the
 * urban-renewal pillar and the buying-apartment guide + /sell-by-auction/.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_sf_configs' ) ) {
	function nadlan_sf_configs() {
		return apply_filters( 'nadlan_sf_configs', array(
			'auction' => array(
				'goal'   => 'auction-seller',
				'kicker' => 'מכירה בהצעות',
				'title'  => 'בואו נכיר את הדירה שלכם',
				'sub'    => 'שמונה שאלות קצרות, בלי טפסים אפורים. בסוף נחזור אליכם עם הצעד הבא.',
				'share'  => 'מוכרים דירה? ככה מקבלים הצעות אמיתיות מקונים, בחינם:',
				'steps'  => array(
					array( 'k' => 'city', 'q' => 'באיזו עיר הדירה?', 't' => 'text', 'ph' => 'תל אביב, חיפה, באר שבע...' ),
					array( 'k' => 'rooms', 'q' => 'כמה חדרים?', 't' => 'chips', 'o' => array( '2', '3', '4', '5', '6+' ) ),
					array( 'k' => 'sqm', 'q' => 'כמה מטרים (בערך)?', 't' => 'number', 'ph' => '85' ),
					array( 'k' => 'condition', 'q' => 'מה מצב הדירה?', 't' => 'chips', 'o' => array( 'חדשה מקבלן', 'משופצת', 'שמורה', 'דרוש שיפוץ' ) ),
					array( 'k' => 'budget', 'q' => 'כמה הייתם רוצים לקבל עליה?', 't' => 'text', 'ph' => '₪2,400,000 (אפשר טווח)' ),
					array( 'k' => 'timeline', 'q' => 'מתי הייתם רוצים למכור?', 't' => 'chips', 'o' => array( 'כמה שיותר מהר', 'בחצי שנה הקרובה', 'לא לחוץ, בודק שוק' ) ),
					array( 'k' => 'message', 'q' => 'משהו שחשוב שנדע על הדירה?', 't' => 'textarea', 'ph' => 'קומה, מרפסת, חניה, נוף, שכנים...', 'opt' => true ),
				),
			),
			'renewal' => array(
				'goal'   => 'renewal-form',
				'kicker' => 'התחדשות עירונית',
				'title'  => 'בדקו איפה הבניין שלכם עומד',
				'sub'    => 'שש שאלות קצרות, ותקבלו כיוון ראשוני. חינם ובלי התחייבות.',
				'share'  => 'גרים בבניין ישן? ככה בודקים בחינם אם מגיעה לכם התחדשות עירונית:',
				'steps'  => array(
					array( 'k' => 'city', 'q' => 'באיזו עיר הבניין?', 't' => 'text', 'ph' => 'רמת גן, חולון, ירושלים...' ),
					array( 'k' => 'building', 'q' => 'בן כמה הבניין (בערך)?', 't' => 'chips', 'o' => array( 'לפני 1980', '1980-2000', 'אחרי 2000', 'לא יודעים' ) ),
					array( 'k' => 'units', 'q' => 'כמה דירות יש בבניין?', 't' => 'number', 'ph' => '12' ),
					array( 'k' => 'rooms', 'q' => 'איפה אתם בתהליך?', 't' => 'chips', 'o' => array( 'רק חושבים', 'יש התארגנות שכנים', 'יזם פנה אלינו', 'יש חתימות' ) ),
					array( 'k' => 'message', 'q' => 'מה הכי חשוב לכם לדעת?', 't' => 'textarea', 'ph' => 'כדאיות, זכויות, איך מתחילים...', 'opt' => true ),
				),
			),
			'buy' => array(
				'goal'   => 'buyer-profile',
				'kicker' => 'קונים דירה',
				'title'  => 'ספרו לנו מה אתם מחפשים',
				'sub'    => 'שש שאלות, ונכוון אתכם לפרויקטים ולדירות שבאמת מתאימים.',
				'share'  => 'מחפשים דירה? הטופס הזה חוסך שבועות של חיפוש:',
				'steps'  => array(
					array( 'k' => 'city', 'q' => 'איפה אתם רוצים לגור?', 't' => 'text', 'ph' => 'עיר או אזור' ),
					array( 'k' => 'budget', 'q' => 'מה התקציב?', 't' => 'chips', 'o' => array( 'עד ₪1.5M', '₪1.5-2.5M', '₪2.5-4M', 'מעל ₪4M' ) ),
					array( 'k' => 'rooms', 'q' => 'כמה חדרים?', 't' => 'chips', 'o' => array( '2', '3', '4', '5+' ) ),
					array( 'k' => 'goal2', 'q' => 'למגורים או להשקעה?', 't' => 'chips', 'o' => array( 'למגורים', 'להשקעה', 'גם וגם' ) ),
					array( 'k' => 'timeline', 'q' => 'מתי תרצו לקנות?', 't' => 'chips', 'o' => array( 'בחודשים הקרובים', 'תוך שנה', 'רק מתחילים לבדוק' ) ),
					array( 'k' => 'message', 'q' => 'עוד משהו שחשוב לכם?', 't' => 'textarea', 'ph' => 'מרפסת, קומה, ליד בית ספר...', 'opt' => true ),
				),
			),
		) );
	}
}

if ( ! function_exists( 'nadlan_sf_render' ) ) {
	function nadlan_sf_render( $form_id ) {
		$configs = nadlan_sf_configs();
		if ( ! isset( $configs[ $form_id ] ) ) { return ''; }
		$c = $configs[ $form_id ];
		static $printed_engine = false;
		ob_start();
		?>
<div class="nlsf" id="nlsf-<?php echo esc_attr( $form_id ); ?>" dir="rtl"
	data-goal="<?php echo esc_attr( $c['goal'] ); ?>"
	data-share="<?php echo esc_attr( $c['share'] ); ?>"
	data-steps="<?php echo esc_attr( wp_json_encode( $c['steps'], JSON_UNESCAPED_UNICODE ) ); ?>"
	data-rest="<?php echo esc_url( rest_url( 'nadlan/v1/lead' ) ); ?>">
	<p class="nlsf-kicker"><?php echo esc_html( $c['kicker'] ); ?></p>
	<h2 class="nlsf-title"><?php echo esc_html( $c['title'] ); ?></h2>
	<p class="nlsf-sub"><?php echo esc_html( $c['sub'] ); ?></p>
	<div class="nlsf-card">
		<div class="nlsf-progress"><i></i></div>
		<div class="nlsf-stage"></div>
	</div>
</div>
		<?php
		if ( ! $printed_engine ) {
			$printed_engine = true;
			?>
<style>
.nlsf{max-width:640px;margin:30px auto;font-family:Heebo,sans-serif;color:#1B1A17}
.nlsf-kicker{font:700 12.5px Heebo;letter-spacing:.06em;color:#9C7A3C;text-transform:uppercase;margin:0 0 6px;text-align:center}
.nlsf-title{font-family:"Frank Ruhl Libre",Georgia,serif;font-size:clamp(1.35rem,3vw,1.8rem);margin:0 0 6px;text-align:center}
.nlsf-sub{font:400 14px/1.65 Heebo;color:#51483A;margin:0 0 18px;text-align:center}
.nlsf-card{position:relative;background:#fff;border:1px solid #E2DCD0;border-radius:22px;padding:34px 28px 30px;min-height:280px;box-shadow:0 24px 60px -34px rgba(27,26,23,.3);overflow:hidden}
.nlsf-progress{position:absolute;top:0;left:0;right:0;height:5px;background:#F3EEE3}
.nlsf-progress i{display:block;height:100%;width:0;background:linear-gradient(90deg,#9C7A3C,#D6C189);transition:width .45s cubic-bezier(.22,1,.36,1)}
.nlsf-q{animation:nlsfIn .4s cubic-bezier(.22,1,.36,1)}
.nlsf-q.out{animation:nlsfOut .25s ease forwards}
@keyframes nlsfIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes nlsfOut{to{opacity:0;transform:translateY(-14px)}}
.nlsf-count{font:700 11.5px Heebo;color:#9C7A3C;margin:0 0 8px}
.nlsf-q h3{font-family:"Frank Ruhl Libre",serif;font-size:clamp(1.25rem,2.6vw,1.6rem);margin:0 0 18px;line-height:1.35}
.nlsf-chips{display:flex;gap:10px;flex-wrap:wrap}
.nlsf-chip{border:1.5px solid #E2DCD0;background:#FAF7F1;border-radius:14px;padding:14px 20px;font:600 15px Heebo;color:#1B1A17;cursor:pointer;transition:border-color .15s,transform .15s}
.nlsf-chip:hover{border-color:#9C7A3C;transform:translateY(-1px)}
.nlsf-input{width:100%;box-sizing:border-box;background:#FAF7F1;border:1.5px solid #E2DCD0;border-radius:12px;padding:15px;font:400 16px Heebo;color:#1B1A17}
.nlsf-input:focus{outline:none;border-color:#9C7A3C}
textarea.nlsf-input{min-height:90px;resize:vertical}
.nlsf-nav{display:flex;align-items:center;gap:12px;margin-top:20px}
.nlsf-next{background:#C2563A;color:#FAF7F1;border:0;border-radius:12px;padding:14px 30px;font:700 15px Heebo;cursor:pointer;box-shadow:0 14px 30px -14px rgba(194,86,58,.55)}
.nlsf-next[disabled]{opacity:.55;cursor:default}
.nlsf-back{background:none;border:0;color:#A79E8D;font:600 13px Heebo;cursor:pointer;padding:8px}
.nlsf-hint{font:400 11.5px Heebo;color:#A79E8D;margin-inline-start:auto}
.nlsf-done{text-align:center;padding:16px 0;animation:nlsfIn .5s cubic-bezier(.22,1,.36,1)}
.nlsf-check{width:64px;height:64px;border-radius:50%;background:#517048;color:#FAF7F1;font:800 30px/64px Heebo;margin:0 auto 14px;position:relative}
.nlsf-check::before,.nlsf-check::after{content:"";position:absolute;inset:-8px;border-radius:50%;border:2px solid #51704855;animation:nlsfPulse 1.4s ease-out infinite}
.nlsf-check::after{animation-delay:.5s}
@keyframes nlsfPulse{from{transform:scale(.8);opacity:1}to{transform:scale(1.5);opacity:0}}
.nlsf-done h3{font-family:"Frank Ruhl Libre",serif;margin:0 0 6px}
.nlsf-done p{font:400 14px/1.6 Heebo;color:#51483A;margin:0 0 16px}
.nlsf-share{display:inline-block;background:#fff;border:1.5px solid #9C7A3C;color:#9C7A3C;border-radius:12px;padding:12px 22px;font:700 13.5px Heebo;text-decoration:none}
</style>
<script>
(function(){
	function boot(root){
		var steps=[];try{steps=JSON.parse(root.dataset.steps)}catch(e){return}
		steps=steps.concat([{k:"name",q:"איך קוראים לכם?",t:"text",ph:"שם מלא"},{k:"phone",q:"ומה הטלפון לחזרה?",t:"tel",ph:"050-0000000"}]);
		var stage=root.querySelector(".nlsf-stage"),bar=root.querySelector(".nlsf-progress i");
		var answers={},idx=0;
		function esc(s){var d=document.createElement("div");d.textContent=s;return d.innerHTML}
		function render(){
			bar.style.width=Math.round(idx/steps.length*100)+"%";
			if(idx>=steps.length){return submit()}
			var s=steps[idx];
			var html='<div class="nlsf-q"><p class="nlsf-count">'+(idx+1)+" / "+steps.length+'</p><h3>'+esc(s.q)+"</h3>";
			if(s.t==="chips"){
				html+='<div class="nlsf-chips">'+s.o.map(function(o){return '<button type="button" class="nlsf-chip">'+esc(o)+"</button>"}).join("")+"</div>";
			}else{
				var tag=s.t==="textarea"?"textarea":"input";
				html+="<"+tag+' class="nlsf-input" '+(tag==="input"?'type="'+(s.t==="number"?"number":s.t==="tel"?"tel":"text")+'"':"")+' placeholder="'+esc(s.ph||"")+'"></'+tag+">";
			}
			html+='<div class="nlsf-nav">'+(idx>0?'<button type="button" class="nlsf-back">→ חזרה</button>':"")
				+(s.t!=="chips"?'<button type="button" class="nlsf-next">המשך</button>':"")
				+(s.opt?'<button type="button" class="nlsf-back nlsf-skip">דלגו</button>':"")
				+'<span class="nlsf-hint">Enter ↵</span></div></div>';
			stage.innerHTML=html;
			var input=stage.querySelector(".nlsf-input");
			if(input){input.focus();if(answers[s.k])input.value=answers[s.k];}
			stage.querySelectorAll(".nlsf-chip").forEach(function(ch){ch.addEventListener("click",function(){answers[s.k]=ch.textContent;go(1)})});
			var next=stage.querySelector(".nlsf-next");
			if(next){next.addEventListener("click",function(){
				var v=input?input.value.trim():"";
				if(!v&&!s.opt){input.style.borderColor="#C2563A";input.focus();return}
				if(s.k==="phone"&&v.replace(/\D/g,"").length<9){input.style.borderColor="#C2563A";return}
				answers[s.k]=v;go(1);
			});}
			if(input){input.addEventListener("keydown",function(e){if(e.key==="Enter"&&s.t!=="textarea"){e.preventDefault();(next||{click:function(){}}).click()}})}
			var back=stage.querySelector(".nlsf-back:not(.nlsf-skip)");
			if(back){back.addEventListener("click",function(){go(-1)})}
			var skip=stage.querySelector(".nlsf-skip");
			if(skip){skip.addEventListener("click",function(){answers[s.k]="";go(1)})}
		}
		function go(d){
			var q=stage.querySelector(".nlsf-q");
			if(q){q.classList.add("out");setTimeout(function(){idx+=d;render()},200)}else{idx+=d;render()}
		}
		function submit(){
			bar.style.width="100%";
			var body={name:answers.name||"",phone:answers.phone||"",goal:root.dataset.goal,source:"smart-form",
				city:answers.city||"",budget:answers.budget||"",rooms:answers.rooms||"",sqm:answers.sqm||"",
				timeline:answers.timeline||"",building:answers.building||"",unit:answers.units||"",
				message:[answers.condition,answers.goal2,answers.message].filter(Boolean).join(" | "),company:""};
			fetch(root.dataset.rest,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)})
			.then(function(r){return r.json()}).then(function(j){
				var share=root.dataset.share+" "+location.href.split("#")[0];
				stage.innerHTML='<div class="nlsf-done"><div class="nlsf-check">✓</div><h3>קיבלנו, תודה!</h3><p>נחזור אליכם בהקדם. בינתיים - מכירים מישהו שזה רלוונטי אליו?</p><a class="nlsf-share" target="_blank" rel="noopener" href="https://wa.me/?text='+encodeURIComponent(share)+'">שיתוף בוואטסאפ</a></div>';
			}).catch(function(){
				stage.innerHTML='<div class="nlsf-done"><p>משהו השתבש. נסו שוב בעוד רגע.</p></div>';
			});
		}
		render();
	}
	document.querySelectorAll(".nlsf").forEach(boot);
})();
</script>
			<?php
		}
		return ob_get_clean();
	}
}

add_shortcode( 'nadlan_smart_form', function ( $atts ) {
	$atts = shortcode_atts( array( 'id' => 'buy' ), (array) $atts );
	return nadlan_sf_render( sanitize_key( $atts['id'] ) );
} );

/* attach the forms to the pillar surfaces (owner: "attach a form to urban
   renewal and to buying apartments") - appended at the end of the content */
add_filter( 'the_content', function ( $content ) {
	if ( is_admin() || ! is_page() || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$slug = get_post_field( 'post_name', get_the_ID() );
	if ( 'urban-renewal' === $slug ) { return $content . nadlan_sf_render( 'renewal' ); }
	if ( 'buying-apartment' === $slug ) { return $content . nadlan_sf_render( 'buy' ); }
	return $content;
}, 32 );
