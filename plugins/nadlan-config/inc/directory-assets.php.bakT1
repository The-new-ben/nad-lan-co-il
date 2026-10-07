<?php
/**
 * nadlan-config - Premium directory CSS + JS (v1.31.0)
 * Split out of directory.php for readability. Vanilla JS, no dependencies.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_dir_css' ) ) {
	function nadlan_dir_css() {
		return <<<'CSS'
<style id="nldir-css">
.nldir{--cream:#FAF7F1;--surface:#FFFDFC;--band:#F3EEE3;--ink:#1B1A17;--muted:#6D665C;--gold:#9C7A3C;--terracotta:#C2563A;--line:#E2DCD0;--line-strong:#C9C0AE;font-family:var(--font-sans,Heebo,system-ui,sans-serif);color:var(--ink);background:var(--cream);max-width:1280px;margin:0 auto;padding:0 20px 60px;direction:rtl;-webkit-font-smoothing:antialiased}

/* ---------- HERO ---------- */
.nldir-hero{position:relative;margin:0 -20px 30px;padding:46px 24px 40px;text-align:center;color:var(--ink);overflow:hidden;border:1px solid var(--line);border-radius:8px;background:linear-gradient(180deg,rgba(250,247,241,.98),rgba(243,238,227,.96));box-shadow:0 18px 46px rgba(27,26,23,.08)}
.nldir-hero::after{content:"";position:absolute;inset:auto 10% 0;height:1px;background:linear-gradient(90deg,transparent,rgba(156,122,60,.32),transparent);pointer-events:none}
.nldir-crumbs{position:relative;font-size:12.5px;color:var(--muted);margin-bottom:16px}
.nldir-crumbs a{color:var(--ink);text-decoration:none}
.nldir-hero h1{position:relative;font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500;font-size:clamp(28px,4.4vw,46px);margin:0 0 12px;letter-spacing:0;line-height:1.1}
.nldir-lead{position:relative;font-size:clamp(14px,2vw,17px);color:var(--muted);margin:0 auto 24px;max-width:620px;line-height:1.6}
.nldir-lead strong{color:var(--gold)}
/* search */
.nldir-search{position:relative;display:flex;gap:8px;max-width:680px;margin:0 auto;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:8px;box-shadow:0 12px 30px rgba(27,26,23,.08)}
.nldir-search input{flex:1;border:0;padding:14px 16px;font:inherit;font-size:15px;border-radius:6px;color:var(--ink);background:transparent;min-width:0}
.nldir-search input[name=city]{flex:.6;border-inline-start:1px solid var(--line)}
.nldir-search button{border:0;border-radius:6px;padding:0 30px;font:inherit;font-weight:700;font-size:15px;color:var(--cream);cursor:pointer;background:var(--ink);transition:filter .2s,transform .15s}
.nldir-search button:hover{filter:brightness(1.08);transform:translateY(-1px)}
/* pills */
.nldir-pills{position:relative;display:flex;flex-wrap:wrap;gap:9px;justify-content:center;margin-top:22px}
.nldir-pill{--pc:var(--ink);--ps:var(--band);display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:var(--surface);color:var(--ink);padding:9px 15px;border-radius:999px;font:inherit;font-size:13.5px;font-weight:600;cursor:pointer;transition:transform .15s,background .2s,border-color .2s}
.nldir-pill span{font-size:15px;line-height:1}
.nldir-pill i{font-style:normal;font-size:11px;opacity:.7;background:var(--band);padding:1px 7px;border-radius:20px}
.nldir-pill:hover{transform:translateY(-2px);background:var(--band);border-color:var(--gold)}
.nldir-pill.is-on{background:var(--ink);color:var(--cream);border-color:var(--ink)}
.nldir-pill.is-on i{background:var(--ps,#eee);opacity:1}

/* ---------- BODY LAYOUT ---------- */
.nldir-body{display:grid;grid-template-columns:240px 1fr;gap:26px;align-items:start}
.nldir-side{position:sticky;top:20px;display:flex;flex-direction:column;gap:22px}
.nldir-fgroup h4{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin:0 0 12px;font-weight:700}
.nldir-check{display:flex;align-items:center;gap:9px;font-size:14px;cursor:pointer;padding:10px 12px;border:1px solid var(--line);border-radius:10px;transition:border-color .2s,background .2s}
.nldir-check:hover{border-color:var(--gold);background:#FBF9F5}
.nldir-check input{accent-color:#059669;width:17px;height:17px}
.nldir-cities{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:3px}
.nldir-cityb{display:flex;justify-content:space-between;width:100%;align-items:center;background:none;border:0;border-radius:8px;padding:9px 11px;font:inherit;font-size:14px;color:var(--ink);cursor:pointer;text-align:start;transition:background .15s,color .15s}
.nldir-cityb i{font-style:normal;font-size:12px;color:#9a9a9a}
.nldir-cityb:hover,.nldir-cityb.is-on{background:#FBF9F5;color:var(--gold)}
.nldir-cityb.is-on{font-weight:700}

/* ---------- RESULTS BAR ---------- */
.nldir-main{min-width:0}
.nldir-bar{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid var(--line)}
.nldir-count{font-size:15px}.nldir-count strong{font-size:19px;color:var(--gold)}
.nldir-chips{display:flex;gap:7px;flex-wrap:wrap;flex:1}
.nldir-chip{display:inline-flex;align-items:center;gap:6px;background:#FBF9F5;border:1px solid var(--line);border-radius:20px;padding:5px 12px;font-size:12.5px;font-weight:600}
.nldir-chip button{border:0;background:none;cursor:pointer;font-size:14px;line-height:1;color:#b00;padding:0}
.nldir-sortw{font-size:13px;color:#6b6b6b;display:flex;align-items:center;gap:7px}
.nldir-sortw select{border:1px solid var(--line);border-radius:8px;padding:8px 10px;font:inherit;background:#fff;cursor:pointer}

/* ---------- CARDS GRID ---------- */
.nldir-results{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:16px;transition:opacity .18s}
.nldir-results.is-loading{opacity:.45;pointer-events:none}
.nldc{position:relative;display:flex;flex-direction:column;gap:11px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px;text-decoration:none;color:inherit;overflow:hidden;
	transition:transform .22s cubic-bezier(.2,.8,.2,1),box-shadow .22s,border-color .22s;animation:nldcIn .4s both}
.nldc::before{content:"";position:absolute;inset-block-start:0;inset-inline-start:0;width:100%;height:4px;background:var(--pc,#9C7A3C);opacity:.9}
.nldc:hover{transform:translateY(-6px);box-shadow:0 20px 40px rgba(27,26,23,.13);border-color:var(--pc,#9C7A3C)}
.nldc.is-featured{border-color:var(--pc);box-shadow:0 10px 30px color-mix(in srgb,var(--pc) 22%,transparent)}
.nldc-sponsor{position:absolute;inset-block-start:14px;inset-inline-end:14px;background:linear-gradient(135deg,#9C7A3C,#D4AF63);color:#fff;font-size:10px;font-weight:700;letter-spacing:.08em;padding:3px 10px;border-radius:20px}
.nldc-top{display:flex;gap:13px;align-items:flex-start}
.nldc-av{flex:none;width:50px;height:50px;border-radius:14px;display:grid;place-items:center;font-size:24px;background:var(--ps,#FBF6EE);box-shadow:inset 0 0 0 1.5px color-mix(in srgb,var(--pc) 30%,transparent)}
.nldc-id{min-width:0;flex:1}
.nldc-name{font-family:var(--font-serif,serif);font-weight:600;font-size:17px;margin:0 0 7px;line-height:1.25;color:var(--ink);overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.nldc-pill{display:inline-block;background:var(--ps,#FBF6EE);color:var(--pc,#9C7A3C);font-size:11.5px;font-weight:700;padding:3px 10px;border-radius:20px}
.nldc-vf{display:inline-block;margin-inline-start:5px;color:#059669;font-size:11.5px;font-weight:700}
.nldc-rate{display:flex;align-items:center;gap:6px;font-size:13px}
.nldc-stars{color:#F5A623;letter-spacing:1px;font-size:14px}
.nldc-rate b{color:var(--ink)}.nldc-rev{color:#9a9a9a;font-size:12px}.nldc-demo{display:inline-block;font-size:10px;font-weight:600;color:#8a7444;background:#F3EEE3;border:1px solid #D6C189;border-radius:5px;padding:1px 6px}
.nldc-norate{color:#b9b4a9;font-size:12px;font-style:italic}
.nldc-meta{display:flex;flex-direction:column;gap:5px;font-size:13px;color:#5a5a5a}
.nldc-city{font-weight:600;color:var(--ink)}
.nldc-distance{display:inline-flex;align-items:center;width:max-content;border:1px solid color-mix(in srgb,var(--pc,#9C7A3C) 24%,transparent);background:var(--ps,#FBF6EE);color:var(--pc,#9C7A3C);border-radius:999px;padding:2px 9px;font-size:11.5px;font-weight:700}
.nldc-cls{line-height:1.45;color:#6b6b6b}
.nldc-foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:8px;padding-top:11px;border-top:1px solid var(--line)}
.nldc-reg{font-size:10.5px;color:#7a7a7a;font-weight:600}
.nldc-go{color:var(--pc,#9C7A3C);font-weight:700;font-size:13px;white-space:nowrap}a.nldc-go{text-decoration:none}.nldc-sponsored-spot{cursor:default}
@keyframes nldcIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}

/* load more + empty */
.nldir-more-wrap{text-align:center;margin-top:30px}
.nldir-more{background:var(--ink);color:#fff;border:0;border-radius:10px;padding:14px 40px;font:inherit;font-weight:700;cursor:pointer;transition:background .2s,transform .15s}
.nldir-more:hover{background:var(--gold);transform:translateY(-2px)}
.nldir-empty{grid-column:1/-1;text-align:center;padding:60px 20px;color:#6b6b6b}
.nldir-empty p:first-child{font-size:18px;color:var(--ink);font-weight:600}

/* ---------- RESPONSIVE ---------- */
@media(max-width:900px){.nldir-body{grid-template-columns:1fr}.nldir-side{position:static;flex-direction:row;flex-wrap:wrap;gap:16px;border-bottom:1px solid var(--line);padding-bottom:18px}.nldir-fgroup{flex:1;min-width:160px}.nldir-cities{flex-direction:row;flex-wrap:wrap}.nldir-cityb{width:auto;border:1px solid var(--line);border-radius:20px}}
@media(max-width:560px){.nldir-search{flex-wrap:wrap}.nldir-search input,.nldir-search input[name=city]{flex:1 1 100%;border-inline-start:0}.nldir-search button{flex:1 1 100%;padding:13px}.nldir-results{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}.nldc{padding:16px}}

/* ---------- PROJECT MAGAZINE CARD (v1.69.69) - Lovable MagazineCard port, scoped to .nldc-project only ---------- */
.nldir-results:has(.nldc-project){grid-template-columns:repeat(auto-fill,minmax(272px,1fr))}
.nldir-results .nldc-project{padding:0!important;overflow:hidden;display:flex;flex-direction:column}
.nldir-results .nldc-project::before{display:none!important}
.nldc-project .nldc-media{position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--band);margin:0;border-radius:0}
.nldc-project .nldc-media img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s cubic-bezier(.2,.8,.2,1)}
.nldc-project:hover .nldc-media img{transform:scale(1.03)}
.nldc-project .nldcp-badge{position:absolute;inset-block-start:12px;inset-inline-start:12px;background:var(--pc,var(--gold));color:#fff;font-size:10px;font-weight:700;letter-spacing:.08em;padding:4px 9px;border-radius:4px}
.nldc-project .nldcp-type{position:absolute;inset-block-end:12px;inset-inline-start:12px;background:rgba(255,255,255,.92);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);color:var(--ink);font-size:11px;font-weight:600;padding:4px 10px;border-radius:999px;border:1px solid var(--line)}
.nldc-project .nldcp-body{padding:16px 18px 18px;display:flex;flex-direction:column;flex:1}
.nldc-project .nldcp-head{display:flex;align-items:baseline;justify-content:space-between;gap:10px}
.nldc-project .nldcp-name{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:700;font-size:1.16rem;line-height:1.25;margin:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;unicode-bidi:plaintext;text-align:start}
.nldc-project .nldcp-city{flex-shrink:0;font-size:11px;letter-spacing:.05em;color:var(--muted)}
.nldc-project .nldcp-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:14px 0 0;padding-top:13px;border-top:1px solid var(--line)}
.nldc-project .nldcp-stats>div{min-width:0}
.nldc-project .nldcp-stats dt{margin:0;font-size:11px;color:var(--muted)}
.nldc-project .nldcp-stats dd{margin:2px 0 0;font-size:14px;font-weight:600;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nldc-project .nldcp-foot{display:flex;align-items:center;gap:12px;margin-top:auto;padding-top:16px}
.nldc-project .nldcp-cta{flex:1;text-align:center;background:var(--ink);color:#fff;font-weight:600;font-size:13.5px;padding:9px 12px;border-radius:6px;transition:background .18s}
.nldc-project:hover .nldcp-cta{background:#000}
.nldc-project .nldcp-reg{display:inline-flex;align-items:center;gap:4px;font-size:11px;color:var(--muted);white-space:nowrap}
.nldc-project .nldcp-reg .nl-ico{width:13px;height:13px}
.nldc-project.is-featured{border-color:var(--pc,var(--gold))!important}
</style>
CSS;
	}
}

if ( ! function_exists( 'nadlan_dir_js' ) ) {
	function nadlan_dir_js() {
		return <<<'JS'
<script id="nldir-js">
(function(){
	var root=document.querySelector('.nldir');if(!root)return;
	var REST=root.dataset.rest;
	var state=JSON.parse(root.dataset.state||'{}');
	var results=root.querySelector('#nldir-results');
	var totalEl=root.querySelector('#nldir-total');
	var chipsEl=root.querySelector('#nldir-chips');
	var moreBtn=root.querySelector('#nldir-more');
	var sortSel=root.querySelector('#nldir-sort');
	var qIn=root.querySelector('.nldir-search input[name=q]');
	var cityIn=root.querySelector('.nldir-search input[name=city]');
	var form=root.querySelector('.nldir-search');
	var verChk=root.querySelector('#nldir-verified');
	var PROF={kablan:'קבלן',shamai:'שמאי',bedek_bait:'בדק בית',mashkanta:'יועץ משכנתאות',architect:'אדריכל',lawyer:'עו״ד',mefakeach:'מפקח',metavech:'מתווך'};
	var t=null,reqId=0;

	function qs(){var p=new URLSearchParams();
		if(state.q)p.set('q',state.q);
		if(state.city)p.set('city',state.city);
		if(state.profession)p.set('profession',state.profession);
		if(state.verified)p.set('verified','1');
		if(state.sort&&state.sort!=='featured')p.set('sort',state.sort);
		return p;}

	function syncURL(){var p=qs();var u=location.pathname+(p.toString()?'?'+p:'');history.replaceState(null,'',u);}

	function renderChips(){
		var c=[];
		if(state.profession&&PROF[state.profession])c.push(['profession',PROF[state.profession]]);
		if(state.city)c.push(['city',state.city]);
		if(state.q)c.push(['q','"'+state.q+'"']);
		if(state.verified)c.push(['verified','מאומתים בלבד']);
		chipsEl.innerHTML=c.map(function(x){return '<span class="nldir-chip">'+x[1]+'<button data-clr="'+x[0]+'" aria-label="הסר">×</button></span>';}).join('');
		chipsEl.querySelectorAll('button[data-clr]').forEach(function(b){
			b.addEventListener('click',function(){var k=b.dataset.clr;
				if(k==='profession'){state.profession='';setPills();}
				else if(k==='verified'){state.verified=0;if(verChk)verChk.checked=false;}
				else if(k==='q'){state.q='';if(qIn)qIn.value='';}
				else if(k==='city'){state.city='';if(cityIn)cityIn.value='';setCityActive();}
				state.paged=1;load();});
		});
	}
	function setPills(){root.querySelectorAll('.nldir-pill').forEach(function(p){p.classList.toggle('is-on',(p.dataset.prof||'')===(state.profession||''));});}
	function setCityActive(){root.querySelectorAll('.nldir-cityb').forEach(function(b){b.classList.toggle('is-on',b.dataset.city===state.city);});}

	function load(append){
		var my=++reqId;
		results.classList.add('is-loading');
		var p=qs();p.set('paged',state.paged||1);p.set('per_page',state.per_page||24);
		fetch(REST+'?'+p.toString(),{headers:{'Accept':'application/json'}})
			.then(function(r){return r.json();})
			.then(function(d){
				if(my!==reqId)return;
				results.classList.remove('is-loading');
				if(!d||!d.ok)return;
				if(append){results.insertAdjacentHTML('beforeend',d.html);}else{results.innerHTML=d.html;}
				if(totalEl)totalEl.textContent=Number(d.total).toLocaleString('he-IL');
				moreBtn.style.display=(d.paged<d.pages)?'':'none';
				renderChips();syncURL();
				if(!append)results.scrollIntoView({behavior:'smooth',block:'nearest'});
			})
			.catch(function(){results.classList.remove('is-loading');});
	}

	// profession pills
	root.querySelectorAll('.nldir-pill').forEach(function(pill){
		pill.addEventListener('click',function(){state.profession=pill.dataset.prof||'';state.paged=1;setPills();load();});
	});
	// city buttons
	root.querySelectorAll('.nldir-cityb').forEach(function(b){
		b.addEventListener('click',function(){state.city=(state.city===b.dataset.city)?'':b.dataset.city;if(cityIn)cityIn.value=state.city;state.paged=1;setCityActive();load();});
	});
	// search form
	if(form)form.addEventListener('submit',function(e){e.preventDefault();state.q=qIn?qIn.value.trim():'';state.city=cityIn?cityIn.value.trim():'';state.paged=1;setCityActive();load();});
	// live search debounce
	if(qIn)qIn.addEventListener('input',function(){clearTimeout(t);t=setTimeout(function(){state.q=qIn.value.trim();state.paged=1;load();},420);});
	// verified
	if(verChk)verChk.addEventListener('change',function(){state.verified=verChk.checked?1:0;state.paged=1;load();});
	// sort
	if(sortSel)sortSel.addEventListener('change',function(){state.sort=sortSel.value;state.paged=1;load();});
	// load more
	if(moreBtn)moreBtn.addEventListener('click',function(){state.paged=(state.paged||1)+1;load(true);});

	renderChips();
})();
</script>
JS;
	}
}
