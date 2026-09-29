<?php
/**
 * ConsultSheet (design system v101 ApartmentExperience-1, 29.9.2026): the site pill's short message sheet.
 *
 * The owner (29.9, through Codex's handoff): a wide "ייעוץ חינם" with the NadLan mark and WhatsApp on every page, and a smart
 * form that offers the context and lets the buyer edit it: the project, the floor and the direction picked on the stage, what
 * they want, when to call back. Nothing already chosen is asked again; the buyer can go straight to WhatsApp.
 *
 * Honest by construction:
 *  - the sheet only builds a message and opens WhatsApp with it; the buyer sends it. It never says "sent" or "received",
 *    stores nothing and calls no server (no new lead contract; the existing lead routing is untouched);
 *  - only what the buyer chose goes in: the page's clean address (no query string), the floor and direction from the stage,
 *    the chips, the note. The "מקור:" line is written here, so inc/wa-source.php does not stamp a second one;
 *  - broker and owner pages keep their own buttons and recipients: the site pill (and so this sheet) is not printed where the
 *    site number is empty (inc/conversion-cta.php, PublishPage v70).
 *
 * Markup, style and script printed once in the footer, after the pill (inc/conversion-cta.php at priority 90).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cta_sheet_strings' ) ) {
	function nadlan_cta_sheet_strings( $lang ) {
		$all = array(
			'he' => array(
				'title' => 'ייעוץ חינם בוואטסאפ', 'lead' => 'בחרו מה מעניין אתכם. ההודעה נכתבת כאן, ואפשר לשנות בה כל מילה.',
				'what' => 'במה אפשר לעזור?', 'when' => 'מתי נוח לחזור אליכם?', 'note' => 'הערה (לא חובה)', 'msg' => 'ההודעה שתיפתח בוואטסאפ',
				'go' => 'פתיחה בוואטסאפ', 'close' => 'סגירה', 'fine' => 'ההודעה נפתחת בוואטסאפ שלכם, ואתם שולחים אותה. שום דבר לא נשמר באתר.',
				'hello' => 'שלום, אשמח לייעוץ חינם.', 'floor' => 'קומה', 'example' => 'דירה לדוגמה', 'wants' => 'מה מעניין אותי', 'back' => 'נוח לחזור אליי',
				'src' => 'מקור', 'edited' => 'ערכתם את ההודעה בעצמכם; הבחירות למעלה כבר לא משנות אותה.',
				'proj' => array( 'תוכניות ומחירים', 'הנוף מהדירה', 'שינויים ועיצוב בדירה', 'פגישה עם נציג' ),
				'gen' => array( 'קנייה', 'מכירה', 'השכרה', 'משכנתא', 'פרויקט חדש' ),
				'time' => array( 'בבוקר', 'בצהריים', 'בערב' ),
			),
			'en' => array(
				'title' => 'Free consultation on WhatsApp', 'lead' => 'Choose what you need. The message is written here and you can change any word.',
				'what' => 'How can we help?', 'when' => 'When should we call back?', 'note' => 'A note (optional)', 'msg' => 'The message that opens in WhatsApp',
				'go' => 'Open in WhatsApp', 'close' => 'Close', 'fine' => 'The message opens in your WhatsApp and you send it. Nothing is saved on the site.',
				'hello' => 'Hi, I would like a free consultation.', 'floor' => 'Floor', 'example' => 'example apartment', 'wants' => 'I am interested in', 'back' => 'Best time to call',
				'src' => 'Source', 'edited' => 'You edited the message yourself; the choices above no longer change it.',
				'proj' => array( 'Plans and prices', 'The view from the apartment', 'Changes and design', 'A meeting with a representative' ),
				'gen' => array( 'Buying', 'Selling', 'Renting', 'Mortgage', 'A new project' ),
				'time' => array( 'Morning', 'Midday', 'Evening' ),
			),
			'fr' => array(
				'title' => 'Conseil gratuit sur WhatsApp', 'lead' => 'Choisissez ce qui vous intéresse. Le message s\'écrit ici et vous pouvez tout modifier.',
				'what' => 'Comment pouvons-nous aider ?', 'when' => 'Quand vous rappeler ?', 'note' => 'Une remarque (facultatif)', 'msg' => 'Le message qui s\'ouvre dans WhatsApp',
				'go' => 'Ouvrir dans WhatsApp', 'close' => 'Fermer', 'fine' => 'Le message s\'ouvre dans votre WhatsApp et c\'est vous qui l\'envoyez. Rien n\'est enregistré sur le site.',
				'hello' => 'Bonjour, je souhaite un conseil gratuit.', 'floor' => 'Étage', 'example' => 'appartement exemple', 'wants' => 'Ce qui m\'intéresse', 'back' => 'Me rappeler',
				'src' => 'Source', 'edited' => 'Vous avez modifié le message ; les choix ci-dessus ne le changent plus.',
				'proj' => array( 'Plans et prix', 'La vue depuis l\'appartement', 'Modifications et design', 'Un rendez-vous' ),
				'gen' => array( 'Achat', 'Vente', 'Location', 'Prêt immobilier', 'Un projet neuf' ),
				'time' => array( 'Le matin', 'À midi', 'Le soir' ),
			),
			'ru' => array(
				'title' => 'Бесплатная консультация в WhatsApp', 'lead' => 'Выберите, что вас интересует. Сообщение пишется здесь, его можно изменить.',
				'what' => 'Чем помочь?', 'when' => 'Когда вам перезвонить?', 'note' => 'Комментарий (необязательно)', 'msg' => 'Сообщение, которое откроется в WhatsApp',
				'go' => 'Открыть в WhatsApp', 'close' => 'Закрыть', 'fine' => 'Сообщение откроется в вашем WhatsApp, и вы отправите его сами. На сайте ничего не сохраняется.',
				'hello' => 'Здравствуйте, хочу получить бесплатную консультацию.', 'floor' => 'Этаж', 'example' => 'пример квартиры', 'wants' => 'Меня интересует', 'back' => 'Удобно перезвонить',
				'src' => 'Источник', 'edited' => 'Вы изменили сообщение сами; выбор выше его больше не меняет.',
				'proj' => array( 'Планы и цены', 'Вид из квартиры', 'Изменения и дизайн', 'Встреча с представителем' ),
				'gen' => array( 'Покупка', 'Продажа', 'Аренда', 'Ипотека', 'Новый проект' ),
				'time' => array( 'Утром', 'Днём', 'Вечером' ),
			),
			'ar' => array(
				'title' => 'استشارة مجانية على واتساب', 'lead' => 'اختاروا ما يهمكم. تُكتب الرسالة هنا ويمكن تعديل كل كلمة.',
				'what' => 'كيف يمكننا المساعدة؟', 'when' => 'متى يناسب الاتصال بكم؟', 'note' => 'ملاحظة (اختياري)', 'msg' => 'الرسالة التي ستفتح في واتساب',
				'go' => 'فتح في واتساب', 'close' => 'إغلاق', 'fine' => 'تُفتح الرسالة في واتساب لديكم وأنتم ترسلونها. لا يُحفظ شيء في الموقع.',
				'hello' => 'مرحبا، أرغب في استشارة مجانية.', 'floor' => 'الطابق', 'example' => 'شقة نموذجية', 'wants' => 'ما يهمني', 'back' => 'الوقت المناسب للاتصال',
				'src' => 'المصدر', 'edited' => 'عدّلتم الرسالة بأنفسكم؛ الخيارات أعلاه لم تعد تغيّرها.',
				'proj' => array( 'المخططات والأسعار', 'الإطلالة من الشقة', 'التعديلات والتصميم', 'لقاء مع ممثل' ),
				'gen' => array( 'شراء', 'بيع', 'إيجار', 'رهن عقاري', 'مشروع جديد' ),
				'time' => array( 'صباحا', 'ظهرا', 'مساء' ),
			),
		);
		return isset( $all[ $lang ] ) ? $all[ $lang ] : $all['he'];
	}
}

if ( ! function_exists( 'nadlan_cta_sheet_html' ) ) {
	/** The sheet for the pill of $wa (digits), in the page's language. */
	function nadlan_cta_sheet_html( $wa, $rtl, $lang ) {
		$t   = nadlan_cta_sheet_strings( $lang );
		$cfg = wp_json_encode( array( 'wa' => (string) $wa, 't' => $t ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
		ob_start(); ?>
<dialog id="nlcta-sheet" class="nlcs" dir="<?php echo $rtl ? 'rtl' : 'ltr'; ?>" aria-labelledby="nlcs-h" data-cfg="<?php echo esc_attr( $cfg ); ?>">
	<form method="dialog" class="nlcs-in">
		<div class="nlcs-top"><h2 id="nlcs-h" class="nlcs-h"><span class="nlcs-mark" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18" fill="#fff"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91C22.04 6.45 17.5 2 12.04 2z"/></svg></span><?php echo esc_html( $t['title'] ); ?></h2>
			<button type="submit" value="close" class="nlcs-x" aria-label="<?php echo esc_attr( $t['close'] ); ?>">&#10005;</button></div>
		<p class="nlcs-lead"><?php echo esc_html( $t['lead'] ); ?></p>
		<p class="nlcs-ctx" hidden></p>
		<fieldset class="nlcs-set"><legend><?php echo esc_html( $t['what'] ); ?></legend><div class="nlcs-chips" data-nlcs="what"></div></fieldset>
		<fieldset class="nlcs-set"><legend><?php echo esc_html( $t['when'] ); ?></legend><div class="nlcs-chips" data-nlcs="when"></div></fieldset>
		<label class="nlcs-lab"><?php echo esc_html( $t['note'] ); ?><input type="text" class="nlcs-note" maxlength="200" autocomplete="off"></label>
		<label class="nlcs-lab"><?php echo esc_html( $t['msg'] ); ?><textarea class="nlcs-msg" rows="6"></textarea></label>
		<p class="nlcs-edited" hidden><?php echo esc_html( $t['edited'] ); ?></p>
		<a class="nlcs-go" data-nl-whatsapp href="https://wa.me/<?php echo esc_attr( $wa ); ?>" target="_blank" rel="noopener"><?php echo esc_html( $t['go'] ); ?></a>
		<p class="nlcs-fine"><?php echo esc_html( $t['fine'] ); ?></p>
	</form>
</dialog>
<style id="nlcta-sheet-css">
.nlcs{position:fixed;inset:auto 0 var(--nlcs-kb,0px) auto;margin:0 16px 16px;width:min(400px,calc(100vw - 32px));max-height:calc(100dvh - 32px - var(--nlcs-kb,0px));padding:0;border:0;border-radius:18px;
  background:#FAF7F1;color:#14212B;box-shadow:0 24px 60px rgba(20,33,43,.30);overflow:auto;font-family:var(--font-sans,Heebo,system-ui,sans-serif);text-align:start}
.nlcs[dir=rtl]{inset:auto auto var(--nlcs-kb,0px) 0}
.nlcs::backdrop{background:rgba(20,19,15,.35)}
.nlcs-in{display:flex;flex-direction:column;gap:10px;padding:16px 16px 14px;margin:0}
.nlcs-top{display:flex;align-items:center;justify-content:space-between;gap:10px}
:root body .nlcs .nlcs-h{display:flex;align-items:center;gap:10px;margin:0!important;font:700 18px/1.25 var(--font-sans,Heebo,system-ui,sans-serif)!important;color:#14212B!important}
.nlcs-mark{display:grid;place-items:center;width:32px;height:32px;border-radius:50%;background:#0F7A63;flex:none}
.nlcs-x{width:44px;height:44px;border:0;border-radius:50%;background:#EEE9DD;color:#14212B;font:700 18px/44px sans-serif;cursor:pointer;padding:0;flex:none}
:root body .nlcs p{margin:0!important;max-width:none!important}
:root body .nlcs .nlcs-lead{font:400 14px/1.45 var(--font-sans,Heebo,sans-serif)!important;color:#3B4753!important}
:root body .nlcs .nlcs-ctx{padding:8px 12px;border-radius:12px;background:#fff;border:1px solid #E2DCD0;font:600 14px/1.4 var(--font-sans,Heebo,sans-serif)!important;color:#14212B!important}
.nlcs-set{margin:0;padding:0;border:0;min-width:0}
.nlcs-set legend{padding:0;margin:0 0 6px;font:700 13.5px/1.3 var(--font-sans,Heebo,sans-serif);color:#14212B}
.nlcs-chips{display:flex;flex-wrap:wrap;gap:6px}
.nlcs-chip{min-height:44px;padding:0 12px;border-radius:999px;border:1px solid #D9D2C3;background:#fff;color:#14212B;font:600 13.5px/1 var(--font-sans,Heebo,sans-serif);cursor:pointer}
.nlcs-chip[aria-pressed=true]{background:#1F4B5C;border-color:#1F4B5C;color:#fff}
.nlcs-chip:focus-visible,.nlcs-go:focus-visible,.nlcs-x:focus-visible,.nlcs-note:focus-visible,.nlcs-msg:focus-visible{outline:3px solid #C2563A;outline-offset:2px}
.nlcs-lab{display:flex;flex-direction:column;gap:5px;font:700 13.5px/1.3 var(--font-sans,Heebo,sans-serif);color:#14212B}
.nlcs-note,.nlcs-msg{width:100%;box-sizing:border-box;border:1px solid #D9D2C3;border-radius:12px;background:#fff;color:#14212B;padding:10px 12px;font:400 15px/1.45 var(--font-sans,Heebo,sans-serif)}
.nlcs-msg{resize:vertical;min-height:120px}
:root body .nlcs .nlcs-edited{font:500 12.5px/1.4 var(--font-sans,Heebo,sans-serif)!important;color:#8A6A2E!important}
.nlcs-go{display:flex;align-items:center;justify-content:center;min-height:50px;border-radius:999px;background:#0F7A63;color:#fff!important;font:800 16px/1 var(--font-sans,Heebo,sans-serif);text-decoration:none!important}
.nlcs-go:hover{filter:brightness(1.06)}
:root body .nlcs .nlcs-fine{font:400 12.5px/1.45 var(--font-sans,Heebo,sans-serif)!important;color:#6B6558!important}
@media(max-width:600px){.nlcs,.nlcs[dir=rtl]{inset:auto 0 var(--nlcs-kb,0px) 0;margin:0;width:100%;max-width:100%;border-radius:20px 20px 0 0;max-height:calc(100dvh - 24px - var(--nlcs-kb,0px))}
  .nlcs-in{padding-bottom:calc(14px + env(safe-area-inset-bottom,0px))}}
@media(prefers-reduced-motion:no-preference){.nlcs[open]{animation:nlcs-in .18s ease-out}@keyframes nlcs-in{from{transform:translateY(12px);opacity:.4}to{transform:none;opacity:1}}}
</style>
<script id="nlcta-sheet-js">
(function(){
	var d=document.getElementById('nlcta-sheet'),pill=document.querySelector('#nlcta .nlcta-wa');
	if(!d||!pill||!d.showModal)return;
	var C={};try{C=JSON.parse(d.getAttribute('data-cfg')||'{}')}catch(e){}
	var T=C.t||{},msg=d.querySelector('.nlcs-msg'),note=d.querySelector('.nlcs-note'),go=d.querySelector('.nlcs-go'),ctxEl=d.querySelector('.nlcs-ctx'),ed=d.querySelector('.nlcs-edited');
	var isProj=!!document.getElementById('nlps')||document.body.classList.contains('single-nadlan_project');
	/* v101.1 (Codex QA 29.9): one draft per unit. A message the buyer edited for 13-east stays with 13-east; choosing 25-west
	   opens 25-west's own draft (or a fresh one), so the header, the text and the link always name the same apartment */
	var drafts={},cur=null,key='page';
	function pick(){var p=window.__nlpsPick;return (isProj&&p&&p.floor!=null&&p.floor!=='')?p:null}
	function keyOf(p){return p?(p.unit?'u:'+p.unit:'f:'+p.floor):'page'}
	function pageName(){var c=document.getElementById('nlps');if(c){try{var n=JSON.parse(c.getAttribute('data-cfg')||'{}').name;if(n)return String(n)}catch(e){}}
		var h=document.querySelector('h1');return ((h&&h.textContent)||document.title.split('|')[0]||'').replace(/\s+/g,' ').trim().slice(0,90)}
	function tower(p){var k=document.querySelector('#nlps-pick .rbs-label.is-on .dus-label-kick');return (p&&p.unit&&/^[A-Za-z]/.test(p.unit)&&k&&k.textContent)?k.textContent.trim():''}
	function pickLine(p){if(!p)return '';var tw=tower(p);
		return (tw?tw+' · ':'')+(T.floor||'')+' '+p.floor+(p.facing?' · '+p.facing:'')+(p.example?' ('+(T.example||'')+(p.unit?', '+p.unit:'')+')':(p.unit?' ('+p.unit+')':''))}
	// the page's clean address; the only state it keeps is the chosen unit (?unit=, which the page opens again), never other parameters
	function link(p){return location.origin+location.pathname+(p&&p.unit?'?unit='+encodeURIComponent(p.unit):'')}
	function draft(k){if(!drafts[k])drafts[k]={what:[],when:'',note:'',msg:'',edited:false};return drafts[k]}
	function chips(k,list,multi){var box=d.querySelector('[data-nlcs='+k+']');box.textContent='';
		(list||[]).forEach(function(w){var b=document.createElement('button');b.type='button';b.className='nlcs-chip';b.textContent=w;b.setAttribute('aria-pressed','false');
			b.addEventListener('click',function(){if(multi){var i=cur.what.indexOf(w);if(i>-1)cur.what.splice(i,1);else cur.what.push(w)}else{cur.when=cur.when===w?'':w}paint();build()});
			box.appendChild(b)})}
	function paint(){d.querySelectorAll('[data-nlcs=what] .nlcs-chip').forEach(function(x){x.setAttribute('aria-pressed',cur.what.indexOf(x.textContent)>-1?'true':'false')});
		d.querySelectorAll('[data-nlcs=when] .nlcs-chip').forEach(function(x){x.setAttribute('aria-pressed',cur.when===x.textContent?'true':'false')})}
	function compose(){var p=pick(),name=pageName(),pl=pickLine(p),L=[T.hello||''];
		if(isProj&&name)L.push(name+(pl?' · '+pl:''));
		if(cur.what.length)L.push((T.wants||'')+': '+cur.what.join(', '));
		if(cur.when)L.push((T.back||'')+': '+cur.when);
		if(cur.note.trim())L.push(cur.note.trim());
		L.push('');L.push((T.src||'')+': '+(name||document.title.split('|')[0].trim()));L.push(link(p));
		return L.join(String.fromCharCode(10))}
	function href(){return 'https://wa.me/'+String(C.wa||'').replace(/[^0-9]/g,'')+'?text='+encodeURIComponent(msg.value)}
	function build(){if(!cur.edited)msg.value=compose();cur.msg=msg.value;go.setAttribute('href',href())}
	msg.addEventListener('input',function(){cur.edited=true;cur.msg=msg.value;ed.hidden=false;go.setAttribute('href',href())});
	note.addEventListener('input',function(){cur.note=note.value;build()});
	function open(e){if(e){e.preventDefault();e.stopPropagation()}
		var p=pick();key=keyOf(p);cur=draft(key);
		var pl=pickLine(p);ctxEl.hidden=!(isProj&&(pl||pageName()));ctxEl.textContent=pageName()+(pl?' · '+pl:'');
		note.value=cur.note;paint();ed.hidden=!cur.edited;
		if(cur.edited)msg.value=cur.msg;
		build();d.showModal();pill.setAttribute('aria-expanded','true');
		try{window.nadlanGA&&window.nadlanGA('whatsapp_sheet_open',{project:isProj?pageName():'',unit:p&&p.unit?p.unit:''})}catch(err){}
		var f=d.querySelector('.nlcs-chip');if(f)f.focus()}
	chips('what',isProj?T.proj:T.gen,true);chips('when',T.time,false);
	pill.setAttribute('aria-haspopup','dialog');pill.setAttribute('aria-controls','nlcta-sheet');pill.setAttribute('aria-expanded','false');
	pill.addEventListener('click',open);
	go.addEventListener('click',function(){go.setAttribute('href',href());try{window.nadlanGA&&window.nadlanGA('whatsapp_click',{source:'consult-sheet',edited:cur&&cur.edited?1:0,chips:cur?cur.what.length:0,unit:(pick()||{}).unit||''})}catch(err){}setTimeout(function(){d.close()},300)});
	d.addEventListener('close',function(){pill.setAttribute('aria-expanded','false');d.style.removeProperty('--nlcs-kb');pill.focus({preventScroll:true})});
	d.addEventListener('click',function(e){if(e.target===d)d.close()});
	// the keyboard on a phone: the sheet rises above it instead of hiding under it
	if(window.visualViewport){var vv=window.visualViewport,fit=function(){if(!d.open)return;var kb=Math.max(0,Math.round(window.innerHeight-vv.height-vv.offsetTop));d.style.setProperty('--nlcs-kb',kb+'px')};vv.addEventListener('resize',fit);vv.addEventListener('scroll',fit)}
})();
</script>
		<?php
		return ob_get_clean();
	}
}
