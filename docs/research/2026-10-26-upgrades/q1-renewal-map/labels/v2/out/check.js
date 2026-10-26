
/* renewal map v2 (proposal of 26.10.2026). Every city gets a tag that says something: its name and, where there is room, the facts
   the chips choose (complexes and approved plans, homes added, apartment prices, what moved), with a strip of its stages along the
   bottom. Tags never overlap: the most important cities get the richest tags, the rest a name or a dot until you zoom in. A mouse
   over a tag previews the city, a tap or click opens it in the panel beside the map (under it on a phone) with every number's
   source and date and the full list of its complexes, each with a link to its page and to "יומן המתחמים". Data: the tracker file
   the page already loads (stages, units, moves on the authority's map), the price medians the site already shows (value.json,
   printed by PHP), the city list of /renewal-map-data. Without the tracker file the map falls back to today's counts and today's
   list (renewal-lookup), with an honest message when its hourly limit answers. One finger still scrolls the page over the map. */
(function(){
	var host=document.getElementById("nlurm-map");if(!host||host.dataset.wired)return;host.dataset.wired="1";
	var BOOT={"px":{"אשדוד":{"r3":[1603300,"1-3.2026"],"r4":[2130200,"1-3.2026"],"r5":[2784800,"1-3.2026"],"page":"/ashdod-apartment-prices/"},"אשקלון":{"r3":[918100,"1-3.2026"],"r4":[1405800,"1-3.2026"],"r5":[1891000,"1-3.2026"],"page":"/ashkelon-apartment-prices/"},"בת ים":{"r3":[1823700,"1-3.2026"],"r4":[2692600,"1-3.2026"],"r5":[3468600,"1-3.2026"],"page":"/bat-yam-apartment-prices/"},"באר שבע":{"r3":[808800,"1-3.2026"],"r4":[1203200,"1-3.2026"],"r5":[1766500,"7-9.2025"],"page":"/beer-sheva-apartment-prices/"},"בני ברק":{"r3":[2028000,"1-3.2026"],"r4":[2491200,"1-3.2026"],"r5":[3034100,"1-3.2026"],"page":"/bnei-brak-apartment-prices/"},"אילת":{"r3":[1516100,"1-3.2026"],"r4":[1719300,"1-3.2026"],"r5":[2587900,"1-3.2026"],"page":"/eilat-apartment-prices/"},"גבעתיים":{"r3":[2815300,"1-3.2026"],"r4":[4158900,"1-3.2026"],"r5":[4960000,"1-3.2026"],"page":"/givatayim-apartment-prices/"},"חיפה":{"r3":[1135100,"1-3.2026"],"r4":[1597500,"1-3.2026"],"r5":[2638000,"1-3.2026"],"page":"/haifa-apartment-prices/"},"הרצליה":{"r3":[2793600,"1-3.2026"],"r4":[3272800,"1-3.2026"],"r5":[4251200,"1-3.2026"],"page":"/herzliya-apartment-prices/"},"הוד השרון":{"r3":[2647000,"1-3.2026"],"r4":[3264800,"1-3.2026"],"r5":[4245600,"1-3.2026"],"page":"/hod-hasharon-apartment-prices/"},"חולון":{"r3":[1918700,"1-3.2026"],"r4":[2428500,"1-3.2026"],"r5":[3142700,"1-3.2026"],"page":"/holon-apartment-prices/"},"ירושלים":{"r3":[2376700,"1-3.2026"],"r4":[2882400,"1-3.2026"],"r5":[3934400,"1-3.2026"],"page":"/jerusalem-apartment-prices/"},"כפר סבא":{"r3":[1941300,"10-12.2025"],"r4":[2817000,"10-12.2025"],"r5":[3544700,"1-3.2026"],"page":"/kfar-saba-apartment-prices/"},"קריית אונו":{"r3":[2635400,"1-3.2026"],"r4":[3197900,"1-3.2026"],"r5":[3533500,"1-3.2026"],"page":"/kiryat-ono-apartment-prices/"},"מודיעין מכבים רעות":{"r3":[2039500,"10-12.2025"],"r4":[2559800,"1-3.2026"],"r5":[3648800,"1-3.2026"],"page":"/modiin-apartment-prices/"},"נתניה":{"r3":[1791300,"10-12.2025"],"r4":[2676100,"1-3.2026"],"r5":[3365300,"1-3.2026"],"page":"/netanya-apartment-prices/"},"פתח תקווה":{"r3":[2057000,"1-3.2026"],"r4":[2444100,"1-3.2026"],"r5":[3322600,"1-3.2026"],"page":"/petah-tikva-apartment-prices/"},"רעננה":{"r3":[2814000,"1-3.2026"],"r4":[3289900,"1-3.2026"],"r5":[4199400,"1-3.2026"],"page":"/raanana-apartment-prices/"},"רמת גן":{"r3":[2701700,"1-3.2026"],"r4":[3330400,"1-3.2026"],"r5":[4636200,"1-3.2026"],"page":"/ramat-gan-apartment-prices/"},"רמת השרון":{"r3":[3544800,"1-3.2026"],"r4":[3809600,"1-3.2026"],"r5":[4663600,"1-3.2026"],"page":"/ramat-hasharon-apartment-prices/"},"רחובות":{"r3":[1921100,"1-3.2026"],"r4":[2345500,"1-3.2026"],"r5":[3290000,"1-3.2026"],"page":"/rehovot-apartment-prices/"},"ראשון לציון":{"r3":[1936700,"1-3.2026"],"r4":[2392600,"1-3.2026"],"r5":[3631900,"1-3.2026"],"page":"/rishon-lezion-apartment-prices/"},"תל אביב יפו":{"r3":[4225800,"1-3.2026"],"r4":[5229800,"1-3.2026"],"r5":[7497700,"1-3.2026"],"page":"/tel-aviv-apartment-prices/"},"יבנה":{"r3":[1990300,"1-3.2026"],"r4":[2473700,"1-3.2026"],"r5":[2863300,"1-3.2026"],"page":""}},"pxsrc":{"source":"עסקאות סגורות לפי רשות המסים, קובצי הסיכום הציבוריים של אתר נדל״ן הממשלתי (חציון לפי מספר חדרים ורבעון)","url":"https://www.nadlan.gov.il/","file":"20.8.2026"},"cent":{"תל אביב":[34.7818,32.0853],"תל אביב-יפו":[34.7818,32.0853],"ירושלים":[35.2137,31.7683],"חיפה":[34.9896,32.794],"ראשון לציון":[34.7894,31.973],"פתח תקווה":[34.8878,32.0871],"אשדוד":[34.6553,31.8014],"נתניה":[34.8532,32.3215],"באר שבע":[34.7913,31.253],"בני ברק":[34.8338,32.0807],"חולון":[34.7722,32.0158],"רמת גן":[34.8114,32.0684],"בת ים":[34.7519,32.0171],"רחובות":[34.8113,31.8928],"הרצליה":[34.8434,32.1663],"כפר סבא":[34.9068,32.175],"חדרה":[34.9196,32.434],"לוד":[34.8903,31.9514],"רמלה":[34.8722,31.9293],"גבעתיים":[34.81,32.0723],"קרית אונו":[34.8555,32.0636],"רעננה":[34.8708,32.1836],"קרית ים":[35.0691,32.8497],"קרית ביאליק":[35.0856,32.8275],"קרית מוצקין":[35.0777,32.8369],"עכו":[35.0818,32.9281],"נהריה":[35.0925,33.0058],"טבריה":[35.5312,32.7922],"אשקלון":[34.5715,31.6688],"דימונה":[35.032,31.0658],"אילת":[34.9482,29.5581],"בית שמש":[34.9886,31.7304],"הוד השרון":[34.8878,32.1556],"רמת השרון":[34.8395,32.1461],"יהוד":[34.8907,32.0331],"אור יהודה":[34.85,32.0292],"גבעת שמואל":[34.848,32.0781],"קרית גת":[34.7642,31.61],"נצרת":[35.2985,32.7021],"עפולה":[35.2908,32.6078],"גבעתים":[34.81,32.0723],"פתח תקוה":[34.8878,32.0871],"אבן יהודה":[34.887,32.263],"אור עקיבא":[34.917,32.506],"אזור":[34.806,32.024],"אריאל":[35.187,32.106],"באר יעקב":[34.831,31.945],"בית דגן":[34.83,32.002],"בית שאן":[35.497,32.497],"בנימינה גבעת עדה":[34.949,32.514],"גדרה":[34.779,31.814],"זכרון יעקב":[34.952,32.573],"חצור הגלילית":[35.543,32.981],"טירה":[34.95,32.233],"טירת כרמל":[34.972,32.76],"יבנה":[34.74,31.878],"יקנעם עילית":[35.089,32.659],"כפר יונה":[34.935,32.317],"כפר קאסם":[34.977,32.114],"כרמיאל":[35.295,32.919],"מבשרת ציון":[35.15,31.801],"מגדל העמק":[35.24,32.675],"מזכרת בתיה":[34.837,31.853],"מעלה אדומים":[35.298,31.777],"נוף הגליל":[35.32,32.702],"נס ציונה":[34.8,31.93],"נשר":[35.045,32.766],"נתיבות":[34.588,31.422],"סחנין":[35.297,32.864],"עתלית":[34.94,32.688],"פרדס חנה כרכור":[34.977,32.474],"צורן קדימה":[34.936,32.284],"צפת":[35.495,32.965],"קרית אתא":[35.106,32.811],"קרית טבעון":[35.127,32.716],"קרית מלאכי":[34.748,31.729],"קרית עקרון":[34.821,31.86],"קרית שמונה":[35.57,33.207],"שדרות":[34.596,31.525],"שלומי":[35.144,33.075],"תל מונד":[34.917,32.25],"ערד":[35.2126,31.2589]},"pulled":"13.7.2026"}||{};
	var REST="https://nad-lan.co.il/wp-json/nadlan/v1/renewal-map-data",LOOK="https://nad-lan.co.il/wp-json/nadlan/v1/renewal-lookup";
	var ST=["ללא שלב","תכנון ראשוני","תכנון סטטוטורי","תכנית מאושרת","במימוש","אחרי רישוי"],SC=["#D3DCE2","#9DB7C3","#5C93A8","#2F6F86","#1F4B5C","#12202A"];
	var KIND={"new":"נוסף","up":"עלה שלב","down":"ירד שלב","chg":"השלב השתנה","gone":"ירד מהרשימה","back":"חזר לרשימה","trk":"המסלול השתנה","renum":"מספר מתחם חדש"};
	var ORD={up:0,"new":1,down:2,chg:3,trk:4,renum:5,back:6,gone:7};
	var MODES=[["all","מתחמים"],["ap","תכניות מאושרות"],["un","דירות חדשות"],["px","מחירי דירות"],["mv","מה זז"]];
	var GUIDE={"תל אביב יפו":"/urban-renewal/pinui-binui-tel-aviv/"};
	var touch=!!(window.matchMedia&&matchMedia("(hover: none), (pointer: coarse)").matches);
	function fail(){
		// no WebGL / blocked script: never leave a black box - the crawlable city directory below carries the same data
		var box=(host.closest&&host.closest(".nlurm-v2"))||host;box.style.display="none";
		var n=document.createElement("p");n.className="nlurm-note";
		n.textContent="המפה לא נטענה בדפדפן הזה. רשימת הערים והמתחמים המלאה מוצגת מטה.";
		box.parentNode.insertBefore(n,box.nextSibling);
	}
	function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
	function fold(s){return String(s||"").replace(/־/g," ").replace(/[֑-ׇ]/g,"").replace(/[-‐-―,.;:!?"'׳״()\[\]\/\\+]/g," ").replace(/\s+/g," ").trim().replace(/יי/g,"י").replace(/וו/g,"ו")}
	function n0(x){return String(Math.round(x||0)).replace(/\B(?=(\d{3})+(?!\d))/g,",")}
	function mil(v,dg){var s=(v/1e6).toFixed(dg==null?2:dg);if(s.indexOf(".")>-1)s=s.replace(/0+$/,"").replace(/\.$/,"");return s}
	function dd(iso){var p=String(iso||"").split("-");return p.length===3?(+p[2])+"."+(+p[1])+"."+p[0]:String(iso||"")}
	function N(x){return '<b class="n">'+n0(x)+'</b>'}
	function Q(q){return '<bdi class="n">'+esc(q)+'</bdi>'} // a quarter like 1-3.2026 keeps its order inside a Hebrew line
	function pl(x,one,many){return N(x)+" "+(x===1?one:many)}
	function txt(h){var d=document.createElement("div");d.innerHTML=h;return d.textContent.replace(/\s+/g," ").trim()}
	function slug(s){return encodeURIComponent(s).replace(/%[0-9A-F]{2}/g,function(x){return x.toLowerCase()})}
	/* ---------- the layout around the map: bar (search + chips), map, side panel ---------- */
	var wrap=document.createElement("div");wrap.className="nlurm-v2"+(touch?" is-touch":"");wrap.setAttribute("dir","rtl");
	host.parentNode.insertBefore(wrap,host);
	var bar=document.createElement("div");bar.className="nlurm-bar";
	bar.innerHTML='<div class="nlurm-q"><label class="nlurm-sr" for="nlurm-qi">חיפוש עיר, מתחם או מספר תכנית</label><input id="nlurm-qi" type="search" autocomplete="off" enterkeyhint="search" placeholder="חפשו עיר, מתחם או מספר תכנית"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg><div class="nlurm-res" hidden></div></div><div class="nlurm-chips" role="group" aria-label="מה התוויות במפה מציגות"></div>';
	wrap.appendChild(bar);wrap.appendChild(host);
	var side=document.createElement("div");side.className="nlurm-side";side.setAttribute("role","region");side.setAttribute("aria-label","הערים והמתחמים");wrap.appendChild(side);
	var live=document.createElement("p");live.className="nlurm-sr";live.setAttribute("aria-live","polite");wrap.appendChild(live);
	function isWide(){return wrap.classList.contains("is-wide")}
	function wide(){var w=wrap.clientWidth>=820;if(isWide()!==w){wrap.classList.toggle("is-wide",w);if(map){map.resize();if(CITY.length&&CITY[0].el)measure();if(S.sel)peek(w?null:S.sel)}}}
	wide();if(window.ResizeObserver){new ResizeObserver(function(){wide();soon()}).observe(wrap)}else{window.addEventListener("resize",function(){wide();soon()})}
	var map=null,D=null,LM=-1,MAPD="",CITY=[],BYF={},S={mode:"all",sel:null,hi:null,sort:"st",grp:"*",more:0,list:0},raf=0;
	/* ---------- data ---------- */
	function trackerUrl(){var t=document.querySelector('[data-nli="urtrack"]'),a=t&&t.getAttribute("data-nli-data");if(!a)return "";var u=a.split(",").filter(function(x){return x.indexOf("renewal-track")>-1})[0];return u||""}
	function getJSON(u){return u?fetch(u,{credentials:"omit",cache:"force-cache"}).then(function(r){if(!r.ok)throw 0;return r.json()}).catch(function(){return null}):Promise.resolve(null)}
	function build(md,T){
		var cent={},px={},k;for(k in(BOOT.cent||{}))cent[fold(k)]=BOOT.cent[k];for(k in(BOOT.px||{}))px[fold(k)]=BOOT.px[k];
		var C={},list=[];
		function get(name){var f=fold(name);if(!C[f]){C[f]={name:name,f:f,ll:cent[f]||null,n:0,off:0,st:[0,0,0,0,0,0],ap:0,im:0,e:0,p:0,un:0,add:0,up:0,gone:0,down:0,chg:0,renum:0,mv:0,last:null,px:px[f]||null,recs:[],c0:0};list.push(C[f])}return C[f]}
		((md&&md.cities)||[]).forEach(function(c){var x=get(c.city);x.c0=c.count;if(!x.ll&&c.lnglat)x.ll=c.lnglat});
		if(T&&T.recs&&T.snaps){
			for(var i=T.snaps.length-1;i>=0;i--){if(T.snaps[i].k==="map"){LM=i;break}}
			MAPD=LM>-1?T.snaps[LM].d:"";
			T.recs.forEach(function(r){
				var x=get(r.c),s=LM>-1?r.s[LM]:-1;x.recs.push(r);
				(r.ch||[]).forEach(function(c){if(!x.last||c[0]>x.last.c[0]||(c[0]===x.last.c[0]&&(ORD[c[1]]||9)<(ORD[x.last.c[1]]||9)))x.last={r:r,c:c}});
				if(s==null||s<0){x.off++;return}
				x.n++;x.st[s]++;if(s>=3)x.ap++;if(s>=4)x.im++;
				if(r.u===LM&&r.e&&r.p){x.e+=r.e;x.p+=r.p;x.un++} // homes today and after: only the authority map's own figures, one source and one date
			});
			var A=(T.agg&&T.agg.cities)||{};for(k in A){var y=get(k),a=A[k];y.add=a.add||0;y.up=a.up||0;y.gone=a.gone||0;y.down=a.down||0;y.chg=a.chg||0;y.renum=a.renum||0;y.mv=y.add+y.up+y.gone+y.down+y.chg+y.renum}
			D=T;
		}
		list=list.filter(function(x){return x.ll&&(D?x.n>0:x.c0>0)});
		list.forEach(function(x){BYF[x.f]=x});
		return list;
	}
	function cnt(x){return D?x.n:x.c0}
	function metric(x,m){m=m||S.mode;if(m==="ap")return x.ap;if(m==="un")return Math.max(0,x.p-x.e);if(m==="px")return x.px?cnt(x)+1:0;if(m==="mv")return x.mv;return cnt(x)}
	function rooms(x){var k=["r3","r4","r5"].filter(function(r){return x.px&&x.px[r]}),a=k.map(function(r){return x.px[r][0]});if(!k.length)return null;var lo=Math.min.apply(0,a),hi=Math.max.apply(0,a);
		return{rl:k.length>1?k[0].slice(1)+"-"+k[k.length-1].slice(1)+" חד׳":k[0].slice(1)+" חד׳",rg:lo===hi?mil(lo,1):mil(lo,1)+"-"+mil(hi,1)}}
	function moved(x,max){var p=[];if(x.add)p.push(pl(x.add,"נוסף","נוספו"));if(x.up)p.push(pl(x.up,"עלה שלב","עלו שלב"));if(x.down)p.push(pl(x.down,"ירד שלב","ירדו שלב"));if(x.chg)p.push(pl(x.chg,"שינה שלב","שינו שלב"));if(x.gone)p.push(pl(x.gone,"ירד מהרשימה","ירדו מהרשימה"));if(x.renum)p.push(pl(x.renum,"קיבל מספר חדש","קיבלו מספר חדש"));return max?p.slice(0,max):p}
	function lines(x,m){
		var c=cnt(x),r=rooms(x);m=m||S.mode;
		if(m==="ap")return[pl(x.ap,"תכנית מאושרת","תכניות מאושרות"),x.im?N(x.im)+" במימוש · מתוך "+pl(c,"מתחם","מתחמים"):"מתוך "+pl(c,"מתחם","מתחמים")];
		if(m==="un")return x.un?['<b class="n" dir="ltr">+'+n0(x.p-x.e)+'</b> דירות אחרי הבנייה',"היום "+N(x.e)+" ← "+N(x.p)]:["",""];
		if(m==="px")return r?['<b class="n">'+r.rg+'</b> מיליון ₪',r.rl+" · חציון עסקאות"]:["",""];
		if(m==="mv")return x.mv?[moved(x,2).join(" · "),x.last?esc(KIND[x.last.c[1]]||"")+": "+esc(x.last.r.n):""]:["",""];
		return[pl(c,"מתחם","מתחמים")+(D&&x.ap?" · "+pl(x.ap,"מאושרת","מאושרות"):""),r?r.rl+" · "+'<b class="n">'+r.rg+'</b> מיליון ₪':(x.un&&x.p>x.e?'<b class="n" dir="ltr">+'+n0(x.p-x.e)+'</b> דירות חדשות':"")];
	}
	function strip(x,cls){if(!D||!x.n)return "";var h="";[5,4,3,2,1,0].forEach(function(s){if(x.st[s])h+='<i style="flex:'+x.st[s]+' 0 0;background:'+SC[s]+'"></i>'});return'<span class="'+(cls||"sb")+'" aria-hidden="true">'+h+'</span>'}
	function short(x,l){var m=S.mode,c=cnt(x);if(m==="all")return pl(c,"מתחם","מתחמים");if(m==="un"&&x.un)return'<b class="n" dir="ltr">+'+n0(x.p-x.e)+'</b> דירות';if(m==="mv"&&x.mv)return moved(x,1)[0];if(m==="ap")return pl(x.ap,"מאושרת","מאושרות");return l[0]}
	function tagHTML(x){var l=lines(x),nm='<span class="nm">'+esc(x.name)+'</span>',sb=strip(x),o={S:nm},m1=isWide()?l[0]:(l[0]?short(x,l):"");
		o.M=m1?nm+'<span class="f">'+m1+'</span>'+sb:null;o.L=l[0]&&l[1]?nm+'<span class="f">'+l[0]+'</span><span class="f">'+l[1]+'</span>'+sb:null;
		o.aria=x.name+(l[0]?": "+txt(l[0])+(l[1]?", "+txt(l[1]):""):"")+". פתיחת פרטי העיר";return o}
	/* ---------- the tags on the map ---------- */
	function makeTags(){
		CITY.forEach(function(x){
			var el=document.createElement("div");el.className="nlurm-lb";
			el.innerHTML='<i class="ld"></i><span class="dt"></span><button type="button" class="tg" style="display:none"></button>';
			x.el=el;x.btn=el.lastChild;x.ld=el.firstChild;
			x.btn.addEventListener("click",function(e){e.stopPropagation();select(x,{from:"tag"})});
			if(!touch){x.btn.addEventListener("mouseenter",function(){S.hov=x;hiRow(x,1);pop(x)});x.btn.addEventListener("mouseleave",function(){S.hov=null;hiRow(x,0);pop(null)})}
			x.btn.addEventListener("focus",function(){if(!touch)pop(x)});x.btn.addEventListener("blur",function(){pop(null)});
			x.mk=new mapboxgl.Marker({element:el,anchor:"center"}).setLngLat(x.ll).addTo(map);
		});
		measure();
	}
	function measure(){
		var box=document.createElement("div");box.className="nlurm-lb";box.style.cssText="position:absolute;left:-9999px;top:0;visibility:hidden";host.appendChild(box);
		var probes=[];
		CITY.forEach(function(x){x.html=tagHTML(x);x.sz={};["L","M","S"].forEach(function(t){if(!x.html[t])return;var b=document.createElement("button");b.type="button";b.className="tg t"+t+" is-n";b.innerHTML=x.html[t];box.appendChild(b);probes.push([x,t,b])})});
		probes.forEach(function(p){var r=p[2].getBoundingClientRect();p[0].sz[p[1]]=[Math.ceil(r.width),Math.ceil(r.height)]});
		host.removeChild(box);
		CITY.forEach(function(x){x.el._k="";x.btn.setAttribute("aria-label",x.html.aria)});
	}
	function hit(a,b){return a[0]<b[2]&&a[2]>b[0]&&a[1]<b[3]&&a[3]>b[1]}
	/* the sea as the margin: every dense renewal city is on the coast, so a tag that has no room by its city may float over the sea
	   to the west, joined to the city by a thin line. The coastline here is coarse on purpose (the bay of Haifa counts as land). */
	var COAST=[[33.30,35.19],[33.10,35.105],[33.00,35.087],[32.92,35.068],[32.83,34.955],[32.70,34.938],[32.61,34.915],[32.50,34.888],[32.45,34.872],[32.33,34.848],[32.17,34.800],[32.10,34.770],[32.05,34.748],[32.00,34.733],[31.93,34.692],[31.80,34.630],[31.67,34.548],[31.59,34.490],[31.50,34.420],[31.32,34.220]];
	function coast(lat){for(var i=1;i<COAST.length;i++){var a=COAST[i-1],b=COAST[i];if(lat<=a[0]&&lat>=b[0])return b[1]+(a[1]-b[1])*(lat-b[0])/(a[0]-b[0])}return null}
	var seaRow={};  // per layout: the screen x of the coastline for each 4 px row (one unproject per row, not per corner)
	function sea(px,py){var k=Math.round(py/4),cx=seaRow[k];if(cx===undefined){var lat=map.unproject([0,k*4]).lat,c=coast(lat);cx=seaRow[k]=c===null?-1e9:map.project([c-0.008,lat]).x}return px<cx}
	var COFF=[];[26,44,64,86,110,136,164,196].forEach(function(d){[0,-22,22,-44,44,-66,66,-92,92,-120,120].forEach(function(dy){COFF.push([d,dy,d+1.4*Math.abs(dy)])})});COFF.sort(function(a,b){return a[2]-b[2]});
	function cands(x,t){
		var w=x.sz[t][0],h=x.sz[t][1],X=x.qx,Y=x.qy,g=t==="S"?7:11;
		function mk(sd,l,tp,ld){var b=[X+l,Y+tp,X+l+w,Y+tp+h];if(t!=="S"&&sd!=="c"){if(sd==="n")b[3]+=6;else if(sd==="s")b[1]-=6;else if(sd==="w")b[2]+=6;else b[0]-=6}return{sd:sd,l:l,t:tp,ld:ld||null,bx:b}} // the box keeps the tick: no tag covers another tag's pointer
		var n=mk("n",-w/2,-g-h),s=mk("s",-w/2,g),W=mk("w",-g-w,-h/2),E=mk("e",g,-h/2),o=t==="S"?[W,E,n,s]:[n,s,W,E];
		if(t!=="S"&&x.coastal)COFF.forEach(function(q){var d=q[0],dy=q[1];o.push(mk("c",-d-w,dy-h/2,[-d,Math.max(dy-h/2+6,Math.min(dy+h/2-6,0))]))});
		return o;
	}
	var lastLay=0,lastZ=0,zt=0,geo=null;
	/* the map's size and the boxes of its buttons and of the peek card, read once and kept until a resize or the peek changes:
	   reading them on every placement would force the browser to lay the whole page out again while the map zooms */
	function geom(){if(geo)return geo;var cr=host.getBoundingClientRect(),pad=4,block=[];
		[].forEach.call(host.querySelectorAll(".mapboxgl-ctrl-top-right .mapboxgl-ctrl,.mapboxgl-ctrl-top-left .mapboxgl-ctrl,.mapboxgl-ctrl-bottom-left .mapboxgl-ctrl,.mapboxgl-ctrl-bottom-right .mapboxgl-ctrl,.nlurm-peek"),function(c){if(c.hidden||c.style.display==="none")return;var b=c.getBoundingClientRect();if(b.width&&b.height)block.push([b.left-cr.left-pad,b.top-cr.top-pad,b.right-cr.left+pad,b.bottom-cr.top+pad])});
		return(geo={W:host.clientWidth,H:host.clientHeight,block:block})}
	function soon(){if(!raf&&map)raf=requestAnimationFrame(layout)}
	/* while zooming in, points only move apart, so the placement stays valid and is redone when the zoom ends; while zooming out,
	   at most one placement every 110 ms keeps tags from meeting (the markers themselves move every frame either way) */
	var quick=false;
	function soonZoom(){if(map.getZoom()>=lastZ-0.001)return;quick=true;var d=performance.now()-lastLay;if(d>=110)soon();else if(!zt)zt=setTimeout(function(){zt=0;soon()},110-d)}
	function layout(){
		raf=0;if(!CITY.length||!map)return;lastLay=performance.now();lastZ=map.getZoom();seaRow={};
		var G=geom(),W=G.W,H=G.H,pad=4,placed=[],block=G.block,isQuick=quick&&map.isZooming();quick=false;
		var order=CITY.slice().sort(function(a,b){return(metric(b)-metric(a))||(cnt(b)-cnt(a))});
		if(isQuick){  // zooming out: each tag keeps its place beside its point, a tag that now meets a more important one hides; the full placement follows when the zoom ends
			var qb=[];order.forEach(function(x){var q=map.project(x.ll);x.qx=q.x;x.qy=q.y;x.vis=q.x>-60&&q.y>-60&&q.x<W+60&&q.y<H+60;if(!x.t||!x.cd||!x.vis){x.t=null;return}
				var sz=x.sz[x.t],bx=[x.qx+x.cd.l,x.qy+x.cd.t,x.qx+x.cd.l+sz[0],x.qy+x.cd.t+sz[1]];
				if(qb.some(function(b){return hit(bx,b)})){x.t=null;return}qb.push(bx)});
			CITY.forEach(paint);return;
		}
		order.forEach(function(x,i){var q=map.project(x.ll),c=coast(x.ll[1]);x.qx=q.x;x.qy=q.y;x.vis=q.x>-60&&q.y>-60&&q.x<W+60&&q.y<H+60;x.t=null;x.cd=null;x.pi=-1;x.rank=i;x.coastal=c!==null&&x.ll[0]-c<0.3});
		var lines=[];  // the leader lines of sea tags, by the same index as placed: a later tag may not cover an earlier line
		function segIn(s,bx){if(Math.max(s[0],s[2])<bx[0]-4||Math.min(s[0],s[2])>bx[2]+4||Math.max(s[1],s[3])<bx[1]-4||Math.min(s[1],s[3])>bx[3]+4)return false;var L=Math.hypot(s[2]-s[0],s[3]-s[1]),k,px,py;for(k=5;k<L-1;k+=2){px=s[0]+(s[2]-s[0])*k/L;py=s[1]+(s[3]-s[1])*k/L;if(px>bx[0]-4&&px<bx[2]+4&&py>bx[1]-4&&py<bx[3]+4)return true}return false}
		var guard=0,dots=order.filter(function(x){return x.vis&&metric(x)>0});  // a tag never hides the point of a more important city (the chosen one: of the top 20)
		function fits(bx,skip,me){if(bx[0]<pad||bx[1]<pad||bx[2]>W-pad||bx[3]>H-pad)return false;var i;for(i=0;i<block.length;i++)if(hit(bx,block[i]))return false;for(i=0;i<placed.length;i++){if(i===skip)continue;if(placed[i]&&hit(bx,placed[i]))return false;if(lines[i]&&segIn(lines[i],bx))return false}
			if(me){var lim=guard?20:me.rank;for(i=0;i<dots.length&&dots[i].rank<lim;i++){var d=dots[i];if(d!==me&&d.qx>bx[0]-4&&d.qx<bx[2]+4&&d.qy>bx[1]-4&&d.qy<bx[3]+4)return false}}return true}
		function cross(a,b){function o(p,q,r){return(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])}var p1=[a[0],a[1]],p2=[a[2],a[3]],q1=[b[0],b[1]],q2=[b[2],b[3]];return o(p1,p2,q1)*o(p1,p2,q2)<0&&o(q1,q2,p1)*o(q1,q2,p2)<0}
		function lineFree(x,c,skip){if(Math.hypot(c.ld[0],c.ld[1])>170)return false;var me=[x.qx,x.qy,x.qx+c.ld[0],x.qy+c.ld[1]];for(var j=0;j<lines.length;j++){if(j!==skip&&lines[j]&&cross(me,lines[j]))return false}return lineFree0(x,c,skip)}
		function lineFree0(x,c,skip){var x2=x.qx+c.ld[0],y2=x.qy+c.ld[1],L=Math.hypot(x2-x.qx,y2-x.qy),k,i,px,py;for(k=5;k<L-2;k+=2){px=x.qx+(x2-x.qx)*k/L;py=x.qy+(y2-x.qy)*k/L;for(i=0;i<placed.length;i++){var b=placed[i];if(i!==skip&&b&&px>b[0]-4&&px<b[2]+4&&py>b[1]-4&&py<b[3]+4)return false}}return true}
		function seaBox(bx){return sea(bx[0],bx[1])&&sea(bx[2],bx[1])&&sea(bx[0],bx[3])&&sea(bx[2],bx[3])}
		function put(x,t,c){if(x.pi<0){x.pi=placed.length;placed.push(null);tagged.push(x)}placed[x.pi]=c.bx;lines[x.pi]=c.ld?[x.qx,x.qy,x.qx+c.ld[0],x.qy+c.ld[1]]:null;x.t=t;x.cd=c;return true}
		/* one tag, one point: a tag never sits nearer to another tagged city's point than to its own, and its own point is never
		   crowded by another tag; the bare point of a city without a tag that sits right against a tag steps aside at this zoom */
		var tagged=[];
		function dist(d,bx){var dx=Math.max(bx[0]-d.qx,0,d.qx-bx[2]),dy=Math.max(bx[1]-d.qy,0,d.qy-bx[3]);return Math.sqrt(dx*dx+dy*dy)}
		function near(bx,me,g){for(var i=0;i<tagged.length;i++){var d=tagged[i];if(d!==me&&dist(d,bx)<g-1)return true}
			for(i=0;i<order.length&&order[i].rank<16;i++){var q=order[i];if(q!==me&&q.vis&&!q.t&&Math.hypot(q.qx-me.qx,q.qy-me.qy)>=9&&dist(q,bx)<g-1)return true} /* nor nearer to an important city's point that is still bare */
			for(i=0;i<placed.length;i++){if(i!==me.pi&&placed[i]&&dist(me,placed[i])<10)return true}return false}
		// leave room: among the places that fit, a tag takes the one that crowds the fewest points of the next important cities still
		// waiting for a tag (a city sitting on top of this one does not count: it can never have its own tag here)
		function crowd(bx,me){var n=0;for(var i=0;i<order.length&&order[i].rank<16;i++){var d=order[i];if(d.rank>me.rank&&!d.t&&d.vis&&metric(d)>0&&Math.hypot(d.qx-me.qx,d.qy-me.qy)>=24&&dist(d,bx)<16)n+=16-d.rank}return n}
		function tryT(x,t,force){if(!x.sz[t])return false;var c=cands(x,t),g=t==="S"?7:11,best=null,bp=1e9,i,pn;
			for(i=0;i<c.length;i++){if(fits(c[i].bx,x.pi,x)&&!near(c[i].bx,x,g)&&(c[i].sd!=="c"||(seaBox(c[i].bx)&&lineFree(x,c[i],x.pi)))){pn=crowd(c[i].bx,x);if(pn<bp){bp=pn;best=c[i];if(!pn)break}}}
			if(best)return put(x,t,best);
			return force?put(x,t,c[0]):false}
		var lead=order.filter(function(x){return x===S.sel||x===S.hi}),rest=order.filter(function(x){return x!==S.sel&&x!==S.hi});
		lead.forEach(function(x){if(!x.vis)return;guard=1;var ok=tryT(x,"L")||tryT(x,"M");guard=0;ok||tryT(x,"L")||tryT(x,"M")||tryT(x,x.sz.M?"M":"S",true)});
		rest.forEach(function(x){if(x.vis&&metric(x)>0)tryT(x,"M")});                        // 1. a named tag with one fact for as many cities as fit
		rest.forEach(function(x){if(x.t==="M"){var keep=placed[x.pi],kl=lines[x.pi],kc=x.cd;placed[x.pi]=null;lines[x.pi]=null;if(!tryT(x,"L")){placed[x.pi]=keep;lines[x.pi]=kl;x.t="M";x.cd=kc}}}); // 2. a second fact where there is room
		rest.forEach(function(x){if(x.vis&&!x.t&&(metric(x)>0||S.mode==="all"))tryT(x,"S")});  // 3. the name alone
		order.forEach(function(x){x.hd=false;if(!x.vis||x.t)return;for(var j=0;j<tagged.length;j++){if(Math.hypot(tagged[j].qx-x.qx,tagged[j].qy-x.qy)<9){x.hd=true;return}}if(x.rank<16)return;for(var i=0;i<placed.length;i++){if(placed[i]&&dist(x,placed[i])<12){x.hd=true;break}}}); // 4. bare points against a tag wait for the zoom
		CITY.forEach(paint);
		clearTimeout(layout.dt);layout.dt=setTimeout(dedupe,250);
	}
	function paint(x){
		var b=x.btn,t=x.vis?x.t:null,c=x.cd,on=x===S.sel,hi=x===S.hi,key=t?t+c.sd+Math.round(c.l)+","+Math.round(c.t)+S.mode+on+hi:"-";
		var zi=String(on?3000:hi?2990:t?(t==="S"?1200:2000)+Math.max(0,700-x.rank):Math.max(0,700-x.rank));if(x.el._z!==zi){x.el._z=zi;x.el.style.zIndex=zi}
		x.el.classList.toggle("is-zero",!metric(x)&&!on);x.el.classList.toggle("is-hd",!!x.hd&&!t);
		if(x.el._k===key)return;x.el._k=key;
		if(!t){b.style.display="none";x.ld.style.display="none";return}
		var sz=x.sz[t];
		b.className="tg t"+t+" is-"+c.sd+(on?" is-on":"")+(hi?" is-hi":"");b.innerHTML=x.html[t];
		b.style.cssText="display:block;left:"+Math.round(c.l)+"px;top:"+Math.round(c.t)+"px;width:"+sz[0]+"px;height:"+sz[1]+"px";
		b.setAttribute("aria-pressed",on?"true":"false");
		if(c.ld){var L=Math.hypot(c.ld[0],c.ld[1]);x.ld.style.cssText="display:block;width:"+L.toFixed(1)+"px;transform:rotate("+Math.atan2(c.ld[1],c.ld[0]).toFixed(4)+"rad)"}else x.ld.style.display="none";
	}
	/* one name per place: the base map's own label for a city that has a tag here steps aside (checked when the map rests) */
	var baseF={},hidden="";
	function dedupe(){
		if(!map||!map.isStyleLoaded())return;
		if(map.isMoving()){clearTimeout(layout.dt);layout.dt=setTimeout(dedupe,300);return} // a base-map restyle waits until the map rests
		try{
			if(!dedupe.m){dedupe.m=1;["country-label","state-label","settlement-major-label","settlement-minor-label","settlement-subdivision-label"].forEach(function(id){if(map.getLayer(id)&&map.getPaintProperty(id,"text-opacity")==null)map.setPaintProperty(id,"text-opacity",.6)})}
			var own={};CITY.forEach(function(x){if(x.vis&&x.t)own[x.f]=1});
			var names=[];map.querySourceFeatures("composite",{sourceLayer:"place_label"}).forEach(function(f){var p=f.properties||{};[p.name,p.name_he,p["name_he"]].forEach(function(n){if(n&&own[fold(n)]&&names.indexOf(n)<0)names.push(n)})});
			var key=names.sort().join("|");if(key===hidden)return;hidden=key;
			var flt=names.length?["!",["any",["in",["coalesce",["get","name"],""],["literal",names]],["in",["coalesce",["get","name_he"],""],["literal",names]]]]:null;
			["settlement-major-label","settlement-minor-label","settlement-subdivision-label"].forEach(function(id){if(!map.getLayer(id))return;if(!(id in baseF))baseF[id]=map.getFilter(id)||null;var f0=baseF[id];map.setFilter(id,flt?(f0?["all",f0,flt]:flt):f0)});
		}catch(e){}
	}
	/* ---------- preview (mouse) and peek (touch) ---------- */
	var popEl=null,peekEl=null;
	function top3(x){return x.recs.filter(function(r){return LM>-1&&r.s[LM]>=0}).sort(function(a,b){return(b.s[LM]-a.s[LM])||((b.p||0)-(a.p||0))}).slice(0,3)}
	function legend(x){if(!D||!x.n)return "";var h="";[4,3,2,1,0,5].forEach(function(s){if(x.st[s])h+='<span style="--c:'+SC[s]+'">'+esc(s===3?"מאושרת":ST[s])+' <b class="n">'+x.st[s]+'</b></span>'});return'<div class="nlurm-big" aria-hidden="true">'+strip(x,"x").replace(/^<span class="x" aria-hidden="true">|<\/span>$/g,"")+'</div><div class="nlurm-leg">'+h+'</div>'}
	function summary(x){
		var r=rooms(x),h='<span class="ct">'+esc(x.name)+'</span>';
		h+=D?'<span class="k">'+pl(x.n,"מתחם","מתחמים")+' במפת הרשות, '+esc(dd(MAPD))+'</span>':'<span class="k">'+pl(x.c0,"מתחם","מתחמים")+' במאגר, '+esc(BOOT.pulled||"")+'</span>';
		h+=legend(x);
		if(x.un)h+='<span class="k">דירות: היום '+N(x.e)+' ← אחרי הבנייה '+N(x.p)+'</span>';
		if(r)h+='<span class="k">'+r.rl+': חציון עסקאות <b class="n">'+r.rg+'</b> מיליון ₪, רבעון '+Q(x.px.r4?x.px.r4[1]:x.px[Object.keys(x.px).filter(function(k){return k[0]==="r"})[0]][1])+'</span>';
		if(D&&x.mv)h+='<span class="k">מאז '+esc(dd(D.agg.since))+': '+moved(x).join(", ")+'</span>';
		return h;
	}
	function pop(x){
		if(!x||touch){if(popEl)popEl.style.display="none";return}
		if(!popEl){popEl=document.createElement("div");popEl.className="nlurm-pop";popEl.setAttribute("aria-hidden","true");host.appendChild(popEl)}
		var t3=top3(x);
		popEl.innerHTML=summary(x)+(t3.length?'<ul class="nlurm-top3">'+t3.map(function(r){return'<li>'+esc(r.n)+' <small>· '+esc(ST[r.s[LM]]||"")+(r.p?' · '+n0(r.p)+' דירות אחרי הבנייה':'')+'</small></li>'}).join("")+'</ul>':"")+'<span class="hint">לחיצה פותחת את העיר ואת רשימת המתחמים שלה</span>';
		popEl.style.display="block";
		var W=host.clientWidth,H=host.clientHeight,pw=popEl.offsetWidth,ph=popEl.offsetHeight,b=x.btn.getBoundingClientRect(),cr=host.getBoundingClientRect();
		var bx=[b.left-cr.left,b.top-cr.top,b.right-cr.left,b.bottom-cr.top],left=(bx[0]+bx[2])/2-pw/2,top=bx[1]-ph-8;
		if(top<8)top=bx[3]+8;if(top+ph>H-8){top=Math.max(8,(bx[1]+bx[3])/2-ph/2);left=bx[0]-pw-10<8?bx[2]+10:bx[0]-pw-10}
		popEl.style.left=Math.round(Math.max(8,Math.min(W-pw-8,left)))+"px";popEl.style.top=Math.round(Math.max(8,Math.min(H-ph-8,top)))+"px";
	}
	function peek(x){
		if(!x||isWide()){if(peekEl&&peekEl.style.display!=="none"){peekEl.style.display="none";geo=null;soon()}return}
		if(!peekEl){peekEl=document.createElement("div");peekEl.className="nlurm-peek";peekEl.setAttribute("role","dialog");host.appendChild(peekEl)}
		var l=lines(x,"all"),acts='<div class="nlurm-acts"><button type="button" class="pri go-list">המתחמים בעיר</button>'+(document.querySelector('#nlur2-track select[id$="-city"]')?'<button type="button" class="go-trk">יומן המתחמים</button>':'')+'</div>';
		peekEl.setAttribute("aria-label",x.name);
		peekEl.innerHTML='<button type="button" class="nlurm-x" aria-label="סגירה">×</button><span class="ct">'+esc(x.name)+'</span><span class="k">'+l[0]+'</span>'+(l[1]?'<span class="k">'+l[1]+'</span>':'')+(D&&x.n?'<div class="nlurm-big" aria-hidden="true">'+strip(x,"x").replace(/^<span class="x" aria-hidden="true">|<\/span>$/g,"")+'</div>':'')+acts;
		peekEl.style.display="block";geo=null;
		peekEl.querySelector(".nlurm-x").addEventListener("click",function(){select(null)});
		peekEl.querySelector(".go-list").addEventListener("click",function(){to(side,90)});
		var gt=peekEl.querySelector(".go-trk");if(gt)gt.addEventListener("click",function(){toTracker(x.name)});
		soon();
	}
	/* ---------- the side panel ---------- */
	function to(el,padTop){window.scrollTo({top:el.getBoundingClientRect().top+window.pageYOffset-padTop,behavior:"smooth"})} // clear of the sticky site header
	function toTracker(city,cx){
		var box=document.getElementById("nlur2-track");if(!box)return false;
		var seg=[].filter.call(box.querySelectorAll(".nli__seg button"),function(b){return b.textContent.trim()==="מתחם אחד"})[0];
		if(cx&&seg&&seg.getAttribute("aria-pressed")!=="true")seg.click();
		var sel=box.querySelector('select[id$="-city"]');if(!sel)return false;
		var f=fold(city),o=[].filter.call(sel.options,function(q){return fold(q.value)===f})[0];
		if(o&&sel.value!==o.value){sel.value=o.value;sel.dispatchEvent(new Event("change",{bubbles:true}))}
		if(cx){var s2=box.querySelector('select[id$="-cx"]');if(s2&&[].some.call(s2.options,function(q){return q.value===cx})){s2.value=cx;s2.dispatchEvent(new Event("change",{bubbles:true}))}}
		to(sel,140);return true;
	}
	function inView(){if(!map)return CITY;var b=map.getBounds();return CITY.filter(function(x){return b.contains(x.ll)})}
	function rowHTML(x){var l=lines(x);return'<li><button type="button" class="ctr" data-f="'+esc(x.f)+'"><span class="nm">'+esc(x.name)+'</span><span class="f">'+(l[0]||lines(x,"all")[0])+'</span>'+strip(x)+'</button></li>'}
	function listView(){
		var v=inView().sort(function(a,b){return(metric(b)-metric(a))||(cnt(b)-cnt(a))}),all=v.length===CITY.length,max=touch&&!S.list?8:999;
		var tot=0;CITY.forEach(function(x){tot+=cnt(x)});
		var h='<h3>'+(all?"כל הערים במפה":"ערים בתצוגה: "+v.length+" מתוך "+CITY.length)+'</h3>';
		h+='<p class="lede">'+(D?pl(tot,"מתחם","מתחמים")+" ב-"+N(CITY.length)+" ערים במפת הרשות הממשלתית להתחדשות עירונית, "+esc(dd(MAPD))+". ":"")+(all?"התקרבו במפה כדי לצמצם את הרשימה לאזור.":"הרשימה מתעדכנת כשמזיזים את המפה.")+'</p>';
		if(D)h+='<div class="nlurm-leg" aria-label="פס השלבים בתחתית כל תווית">'+[4,3,2,1,0].map(function(s){return'<span style="--c:'+SC[s]+'">'+esc(s===3?"מאושרת":ST[s])+'</span>'}).join("")+'</div>';
		h+=v.length?'<ul class="nlurm-rows">'+v.slice(0,max).map(rowHTML).join("")+'</ul>':'<p class="nlurm-msg">אין ערים עם מתחמים באזור הזה. הזיזו את המפה או לחצו על כל הארץ.</p>';
		if(v.length>max)h+='<button type="button" class="nlurm-more" data-a="list">כל '+v.length+' הערים בתצוגה</button>';
		h+=srcLine();
		side.innerHTML=h;
	}
	function srcLine(){var s=[];if(D)s.push('<a href="https://www.gov.il/he/departments/topics/mapa-renewal" target="_blank" rel="noopener">מפת הרשות הממשלתית להתחדשות עירונית</a> ('+esc(dd(MAPD))+')','<a href="https://data.gov.il/dataset/urban_renewal" target="_blank" rel="noopener">קובץ המתחמים ב-data.gov.il</a> ('+esc(dd(D.agg.since))+')');
		if(BOOT.pxsrc&&BOOT.pxsrc.source)s.push('<a href="'+esc(BOOT.pxsrc.url||"https://www.nadlan.gov.il/")+'" target="_blank" rel="noopener">רשות המסים, אתר נדל״ן הממשלתי</a> (קובץ '+esc(BOOT.pxsrc.file||"")+')');
		return s.length?'<p class="nlurm-src">מקורות: '+s.join(" · ")+'</p>':""}
	function cxRows(x){
		var R=x.recs.slice(),lm=LM;
		var g=S.grp;R=R.filter(function(r){var s=lm>-1?r.s[lm]:-1;return g==="*"||(g==="ap"&&s>=3)||(g==="pl"&&(s===1||s===2))||(g==="no"&&s===0)||(g==="off"&&s<0)});
		var sc=function(r){return lm>-1?r.s[lm]:-1},lc=function(r){var c=r.ch&&r.ch[r.ch.length-1];return c?c[0]:""};
		R.sort(S.sort==="un"?function(a,b){return((b.p||0)-(b.e||0))-((a.p||0)-(a.e||0))||a.n.localeCompare(b.n,"he")}:S.sort==="nm"?function(a,b){return a.n.localeCompare(b.n,"he")}:S.sort==="ch"?function(a,b){return lc(b)<lc(a)?-1:lc(b)>lc(a)?1:a.n.localeCompare(b.n,"he")}:function(a,b){return(sc(b)-sc(a))||((b.p||0)-(a.p||0))||a.n.localeCompare(b.n,"he")});
		return R;
	}
	function cityView(x,focusKey){
		var r=rooms(x),h='<button type="button" class="nlurm-back" data-a="back">→ כל הערים</button>';
		h+='<span class="ct" tabindex="-1">'+esc(x.name)+'</span>';
		h+=D?'<span class="k">'+pl(x.n,"מתחם","מתחמים")+' במפת הרשות, '+esc(dd(MAPD))+(x.off?' · ועוד '+N(x.off)+' שלא מופיעים בה היום':'')+'</span>':'<span class="k">'+pl(x.c0,"מתחם","מתחמים")+' במאגר, כפי שנמשך ב-'+esc(BOOT.pulled||"")+'</span>';
		h+=legend(x);
		h+='<dl class="nlurm-dl">';
		if(D){
			h+='<div><dt>תכניות מאושרות ובמימוש<small>מפת הרשות, '+esc(dd(MAPD))+'</small></dt><dd>'+N(x.ap)+(x.im?' (במימוש '+N(x.im)+')':'')+'</dd></div>';
			if(x.un)h+='<div><dt>דירות היום ← אחרי הבנייה<small>מפת הרשות, '+esc(dd(MAPD))+', '+pl(x.un,"מתחם","מתחמים")+' עם שני הנתונים</small></dt><dd>'+N(x.e)+' ← '+N(x.p)+'</dd></div>';
			h+='<div><dt>מה זז מאז '+esc(dd(D.agg.since))+'<small>קובץ data.gov.il מול מפת הרשות של '+esc(dd(D.agg.to))+'</small></dt><dd>'+(x.mv?moved(x).join(", "):"לא נמצא שינוי")+'</dd></div>';
			if(x.last)h+='<div><dt>השינוי האחרון<small>'+esc(x.last.r.n)+'</small></dt><dd>'+esc(KIND[x.last.c[1]]||"")+' '+esc(dd(x.last.c[0]))+'</dd></div>';
		}
		if(r)["r3","r4","r5"].forEach(function(k){if(x.px[k])h+='<div><dt>דירת '+k.slice(1)+' חדרים, חציון מחיר עסקה<small>רשות המסים, רבעון '+Q(x.px[k][1])+'</small></dt><dd>'+N(x.px[k][0])+' ₪</dd></div>'});
		if(x.c0)h+='<div><dt>עמודי מתחמים באתר<small>מהקובץ הרשמי, כפי שנמשך ב-'+esc(BOOT.pulled||"")+'</small></dt><dd>'+N(x.c0)+'</dd></div>';
		h+='</dl>';
		var trk=!!document.querySelector('#nlur2-track select[id$="-city"]');
		h+='<div class="nlurm-acts">'+(trk?'<button type="button" class="pri" data-a="trk">יומן המתחמים ב'+esc(x.name)+'</button>':'')+(x.px&&x.px.page?'<a href="'+esc(x.px.page)+'">מחירי הדירות ב'+esc(x.name)+'</a>':'')+(GUIDE[x.name]?'<a href="'+esc(GUIDE[x.name])+'">פינוי בינוי ב'+esc(x.name)+'</a>':'')+'</div>';
		if(D){
			var cn=function(f){return x.recs.filter(function(q){var s=LM>-1?q.s[LM]:-1;return f(s)}).length},gs=[["*","הכול",x.recs.length],["ap","מאושרות ובמימוש",cn(function(s){return s>=3})],["pl","בתכנון",cn(function(s){return s===1||s===2})],["no","ללא שלב",cn(function(s){return s===0})],["off","לא במפה היום",cn(function(s){return s<0})]].filter(function(q){return q[2]>0});
			if(!gs.some(function(q){return q[0]===S.grp}))S.grp="*";
			var R=cxRows(x),max=S.more?9999:(touch?12:40);if(focusKey){for(var fi=0;fi<R.length;fi++){if(R[fi].k===focusKey){if(fi>=max)max=fi+1;break}}}
			h+='<div class="nlurm-cxh"><h3>המתחמים ב'+esc(x.name)+'</h3><select data-a="sort" aria-label="סדר הרשימה"><option value="st"'+(S.sort==="st"?" selected":"")+'>לפי שלב</option><option value="un"'+(S.sort==="un"?" selected":"")+'>לפי דירות שיתווספו</option><option value="ch"'+(S.sort==="ch"?" selected":"")+'>לפי שינוי אחרון</option><option value="nm"'+(S.sort==="nm"?" selected":"")+'>לפי שם</option></select>'
				+'<div class="nlurm-chips" role="group" aria-label="סינון לפי שלב">'+gs.map(function(q){return'<button type="button" class="nlurm-chip" data-a="grp" data-g="'+q[0]+'" aria-pressed="'+(S.grp===q[0])+'">'+esc(q[1])+' <span class="n">'+q[2]+'</span></button>'}).join("")+'</div></div>';
			h+='<ul class="nlurm-cx">'+R.slice(0,max).map(function(q){
				var s=LM>-1?q.s[LM]:-1,c=q.ch&&q.ch[q.ch.length-1],meta=[s<0?"לא במפת הרשות היום":ST[s]];
				if(q.p)meta.push(q.e?"היום "+n0(q.e)+" ← "+n0(q.p)+" דירות":n0(q.p)+" דירות אחרי הבנייה");if(c)meta.push((KIND[c[1]]||"")+" "+dd(c[0]));
				var inner='<b>'+esc(q.n)+'</b><span>'+esc(meta.join(" · "))+'</span>';
				return'<li data-k="'+esc(q.k)+'"'+(q.k===focusKey?' class="is-hi"':'')+'><span class="sq" style="background:'+(s<0?"#fff;box-shadow:inset 0 0 0 1px #C42550":SC[s])+'"></span>'+(q.w?'<a class="cxm" href="/projects/'+esc(slug(q.w))+'/">'+inner+'</a>':'<div class="cxm">'+inner+'</div>')+(trk?'<button type="button" class="cxt" data-a="cx" data-k="'+esc(q.k)+'" aria-label="'+esc(q.n)+' ביומן המתחמים">ביומן</button>':'')+'</li>'}).join("")+'</ul>';
			if(R.length>max)h+='<button type="button" class="nlurm-more" data-a="more">הציגו את כל '+R.length+' המתחמים</button>';
		}else{h+='<div class="nlurm-look"></div>'}
		h+='<div class="nlurm-acts"><button type="button" data-a="link">העתיקו קישור לעיר</button></div>'+srcLine();
		side.innerHTML=h;
		if(!D)lookup(x,side.querySelector(".nlurm-look"));
		if(focusKey){var li=side.querySelector('li[data-k="'+focusKey.replace(/"/g,"")+'"]');if(li)li.scrollIntoView({block:"nearest"})}
	}
	function lookup(x,box){ // the fallback when the tracker file is not on the page: today's list, with an honest message at the hourly limit
		box.innerHTML='<p class="nlurm-msg">טוענים את מתחמי '+esc(x.name)+'...</p>';
		fetch(LOOK+"?city="+encodeURIComponent(x.name)).then(function(r){if(r.status===429)throw{lim:1};if(!r.ok)throw{};return r.json()}).then(function(j){
			box.innerHTML=(j.matches||[]).map(function(m){var t=m.project_type==="pinui_binui"?"פינוי בינוי":(m.project_type==="tama38"?"תמא 38":"התחדשות");return'<div class="nlur-hit"><b>'+esc(m.title)+'</b> · '+t+(m.plan_number?' · תכנית '+esc(m.plan_number):'')+' · <a href="'+esc(m.url)+'">לעמוד המתחם</a></div>'}).join("")||'<p class="nlurm-msg">לא נמצאו מתחמים לעיר הזו ברשימה.</p>';
		}).catch(function(e){box.innerHTML='<p class="nlurm-msg">'+(e&&e.lim?"הגעתם למספר הבדיקות המרבי לשעה מהחיבור הזה. נסו שוב בעוד כמה דקות; רשימת הערים והמתחמים המלאה מוצגת גם מטה בעמוד.":"הרשימה לא נטענה כרגע. נסו שוב בעוד רגע.")+'</p>'})}
	function panel(focusKey){if(S.sel)cityView(S.sel,focusKey);else listView()}
	function hiRow(x,on){var b=side.querySelector('.ctr[data-f="'+x.f+'"]');if(b)b.classList.toggle("is-hi",!!on)}
	side.addEventListener("click",function(e){
		var t=e.target.closest("[data-a],.ctr");if(!t)return;var a=t.getAttribute("data-a");
		if(t.classList.contains("ctr")){var x=BYF[t.getAttribute("data-f")];if(x)select(x,{fly:true,from:"list"});return}
		if(a==="back")select(null);else if(a==="list"){S.list=1;listView()}else if(a==="more"){S.more=1;panel()}
		else if(a==="grp"){S.grp=t.getAttribute("data-g");S.more=0;panel()}
		else if(a==="trk"&&S.sel)toTracker(S.sel.name);else if(a==="cx"&&S.sel)toTracker(S.sel.name,t.getAttribute("data-k"));
		else if(a==="link"&&S.sel){var u=location.origin+location.pathname+"#nlurm="+encodeURIComponent(S.sel.name);var done=function(){t.textContent="הקישור הועתק"};if(navigator.clipboard)navigator.clipboard.writeText(u).then(done,function(){window.prompt("העתיקו את הקישור",u)});else window.prompt("העתיקו את הקישור",u)}
	});
	side.addEventListener("change",function(e){if(e.target.getAttribute("data-a")==="sort"){S.sort=e.target.value;S.more=0;panel()}});
	if(!touch){side.addEventListener("mouseover",function(e){var t=e.target.closest(".ctr");var x=t&&BYF[t.getAttribute("data-f")];if(x!==S.hi){S.hi=x||null;soon()}});side.addEventListener("mouseleave",function(){if(S.hi){S.hi=null;soon()}})}
	/* ---------- choosing a city ---------- */
	function select(x,o){
		o=o||{};S.sel=x;S.more=0;S.grp="*";S.hi=null;pop(null);
		if(x){
			var b=map.getBounds(),z=map.getZoom();
			if(o.fly||!b.contains(x.ll))map.easeTo({center:x.ll,zoom:Math.max(z,o.zoom||(z<9?9.5:z)),duration:600});
			live.textContent="נבחרה "+x.name+": "+txt(lines(x,"all")[0]);
		}else live.textContent="";
		panel(o.cx);peek(x);soon();
		if(x&&o.from==="list"&&!touch){var ct=side.querySelector(".ct");if(ct)ct.focus({preventScroll:true})}
		if(x&&o.from==="search"&&!isWide())to(host,100);
	}
	/* ---------- chips and search ---------- */
	function chips(){var c=bar.querySelector(".nlurm-chips");c.innerHTML=MODES.filter(function(m){return D||m[0]==="all"||m[0]==="px"}).map(function(m){return'<button type="button" class="nlurm-chip" data-m="'+m[0]+'" aria-pressed="'+(S.mode===m[0])+'">'+esc(m[1])+'</button>'}).join("")}
	bar.querySelector(".nlurm-chips").addEventListener("click",function(e){var b=e.target.closest(".nlurm-chip");if(!b||!CITY.length)return;S.mode=b.getAttribute("data-m");chips();measure();soon();panel()});
	var qi=bar.querySelector("input"),res=bar.querySelector(".nlurm-res");
	function search(q){
		var f=fold(q),out=[];if(f.replace(/ /g,"").length<2){res.hidden=true;return}
		CITY.forEach(function(x){if(x.f.indexOf(f)>-1)out.push({t:"c",x:x})});
		if(D){var toks=f.split(" "),qc=f.replace(/ /g,"");D.recs.forEach(function(r){if(out.length>=14)return;var hs=r.__h||(r.__h=fold(r.n+" "+r.c+" "+(r.pl||""))),pp=r.__p||(r.__p=fold(r.pl||"").replace(/ /g,""));if(toks.every(function(w){return hs.indexOf(w)>-1})||(qc.length>=4&&pp.indexOf(qc)>-1)){var x=BYF[fold(r.c)];if(x)out.push({t:"x",x:x,r:r})}})}
		res.innerHTML=out.length?out.slice(0,14).map(function(o,i){return o.t==="c"?'<button type="button" role="option" data-i="'+i+'">'+esc(o.x.name)+'<small>עיר · '+txt(lines(o.x,"all")[0])+'</small></button>':'<button type="button" role="option" data-i="'+i+'">'+esc(o.r.n)+'<small>'+esc(o.x.name)+(o.r.pl?' · תכנית '+esc(o.r.pl):'')+(LM>-1&&o.r.s[LM]>=0?' · '+esc(ST[o.r.s[LM]]):' · לא במפת הרשות היום')+'</small></button>'}).join(""):'<p>לא מצאנו עיר או מתחם בשם הזה. נסו שם רחוב, שם מתחם או מספר תכנית.</p>';
		res.hidden=false;res._o=out;
	}
	function pick(o){res.hidden=true;qi.value=o.t==="c"?o.x.name:o.r.n;if(o.t==="x"&&o.r.s[LM]<0)S.grp="*";select(o.x,{fly:true,zoom:10.5,cx:o.t==="x"?o.r.k:null,from:"search"})}
	qi.addEventListener("input",function(){search(qi.value)});
	qi.addEventListener("keydown",function(e){if(e.key==="Enter"&&res._o&&res._o.length&&!res.hidden){e.preventDefault();pick(res._o[0])}else if(e.key==="ArrowDown"){var f=res.querySelector("button");if(f){e.preventDefault();f.focus()}}else if(e.key==="Escape"){res.hidden=true}});
	res.addEventListener("click",function(e){var b=e.target.closest("button");if(b&&res._o)pick(res._o[+b.getAttribute("data-i")])});
	res.addEventListener("keydown",function(e){var b=e.target.closest("button");if(!b)return;if(e.key==="ArrowDown"&&b.nextElementSibling){e.preventDefault();b.nextElementSibling.focus()}else if(e.key==="ArrowUp"){e.preventDefault();(b.previousElementSibling||qi).focus()}else if(e.key==="Escape"){res.hidden=true;qi.focus()}});
	document.addEventListener("click",function(e){if(!bar.contains(e.target))res.hidden=true});
	document.addEventListener("keydown",function(e){if(e.key==="Escape"&&S.sel&&!bar.contains(e.target)){var x=S.sel;select(null);if(x.btn&&x.btn.style.display!=="none")x.btn.focus({preventScroll:true})}});
	/* ---------- the map ---------- */
	function boot(){
		try{
			/* Hebrew base-map labels: the RTL text plugin (fetched only when Hebrew text appears) + the map language */
			try{if(mapboxgl.getRTLTextPluginStatus()==="unavailable"){mapboxgl.setRTLTextPlugin("https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js",null,true)}}catch(e){}
			mapboxgl.accessToken="pk.REDACTED";
			map=new mapboxgl.Map({container:"nlurm-map",style:"mapbox://styles/mapbox/light-v11",language:"he",center:[34.9,31.9],zoom:7,attributionControl:true,cooperativeGestures:true,
				locale:{"CooperativeGesturesHandler.WindowsHelpText":"לחצו Ctrl וגללו כדי להתקרב במפה","CooperativeGesturesHandler.MacHelpText":"לחצו ⌘ וגללו כדי להתקרב במפה","TouchPanBlocker.Message":"הזיזו את המפה בשתי אצבעות"}});
		}catch(e){fail();return}
		map.addControl(new mapboxgl.NavigationControl());
		map.addControl({onAdd:function(){var d=document.createElement("div");d.className="mapboxgl-ctrl mapboxgl-ctrl-group nlurm-home";d.innerHTML='<button type="button" aria-label="הצגת כל הארץ">כל הארץ</button>';
			d.firstChild.addEventListener("click",function(){var b=new mapboxgl.LngLatBounds();CITY.forEach(function(x){b.extend(x.ll)});if(CITY.length)map.fitBounds(b,{padding:30,duration:600})});return d},onRemove:function(){}},"top-right");
		map.on("click",function(e){
			var p=e.point,best=null,bd=1e9;
			CITY.forEach(function(x){if(!x.vis||x.hd)return;var d=Math.hypot(x.qx-p.x,x.qy-p.y);if(x.t==="S"&&x.cd){var b=x.cd.bx,dx=Math.max(b[0]-p.x,0,p.x-b[2]),dy=Math.max(b[1]-p.y,0,p.y-b[3]);if(dx<=6&&dy<=14)d=Math.min(d,Math.hypot(dx,dy))}if(d<bd){bd=d;best=x}});
			if(best&&bd<=22){select(best,{from:"map"});return} // forgiving taps on names and points, without buttons that overlap
			if(S.sel&&!isWide())select(null);
		});
		var ready=Promise.all([getJSON(REST),getJSON(trackerUrl())]);
		map.on("load",function(){ready.then(function(v){
			CITY=build(v[0],v[1]);if(!CITY.length)return;
			chips();makeTags();panel();
			var h=decodeURIComponent((location.hash.match(/nlurm=([^&]+)/)||[])[1]||""),hx=h&&BYF[fold(h)];if(hx)select(hx,{fly:true,zoom:10});
			map.on("zoom",soonZoom);map.on("zoomend",soon);var lvT=0;map.on("moveend",function(){soon();clearTimeout(lvT);lvT=setTimeout(function(){if(!S.sel&&!map.isMoving())listView()},180)});map.on("idle",function(){if(!dedupe.m)dedupe()});map.on("resize",function(){geo=null;soon()});map.on("movestart",function(){pop(null)});
			if(document.fonts&&document.fonts.load){Promise.all([document.fonts.load('600 14px "IBM Plex Sans Hebrew"',"רמת גן"),document.fonts.load('500 12px "IBM Plex Mono"',"0123")]).then(function(){measure();soon()},function(){})}
			soon();
		})});
	}
	if(window.mapboxgl){boot();return}
	var l=document.createElement("link");l.rel="stylesheet";l.href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css";document.head.appendChild(l);
	var s=document.createElement("script");s.src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js";s.onload=boot;s.onerror=fail;document.head.appendChild(s);
})();
