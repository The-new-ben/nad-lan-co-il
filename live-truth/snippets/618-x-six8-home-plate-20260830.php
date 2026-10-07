add_action('wp_head', function () {
    if (is_front_page()) {
        echo '<style id="nl-six8-home-plate-20260830">'
            . 'body.home a.nlhv2-proj-media[href="https://nad-lan.co.il/projects/six-8-herbert-samuel-tel-aviv/"] {'
            . 'background-image:url("https://nad-lan.co.il/wp-content/uploads/2026/08/six8-herbert-samuel-plate-capsules.jpg") !important;'
            . 'background-size:contain !important;background-position:center center !important;'
            . 'background-repeat:no-repeat !important;background-color:#15130f !important;}'
            . '</style>';
    }

    if (is_singular('nadlan_project') && (int) get_queried_object_id() === 7219) {
        echo '<style id="nl-six8-journey">'
            . '.nl-six8-facilities{margin:18px auto 28px;max-width:1180px;padding:0 18px;direction:rtl}'
            . '.nl-six8-facilities h2{margin:0 0 12px;font-size:clamp(20px,2.2vw,30px);color:#fff}'
            . '.nl-six8-facilities__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}'
            . '.nl-six8-facility{min-height:150px;padding:15px;border:1px solid rgba(255,255,255,.18);border-radius:16px;background-color:#1f2937;background-position:center;background-size:cover;color:#fff;display:flex;flex-direction:column;justify-content:flex-end;box-shadow:inset 0 -90px 70px rgba(0,0,0,.72)}.nl-six8-facility strong{display:block;margin-bottom:8px;font-size:15px}.nl-six8-facility small{display:block;line-height:1.65;font-size:13px;color:rgba(255,255,255,.84)}'
            . '.postid-7219 .nl-recent,.postid-7219 .nl-chip:not(:first-child){display:none!important}.postid-7219 #nla11y{position:fixed!important;right:14px!important;left:auto!important;bottom:86px!important;top:auto!important;width:52px!important;height:52px!important;transform:none!important;z-index:2147483646!important}body.postid-7219.nl-unit-v2-active #nla11y #nla11y-btn{position:fixed!important;top:auto!important;left:auto!important;right:14px!important;bottom:86px!important;inset-inline-start:auto!important;inset-inline-end:14px!important;width:52px!important;height:52px!important;transform:none!important}.nl-six8-identity{display:flex;gap:8px 18px;flex-wrap:wrap;margin-top:12px;color:rgba(255,255,255,.86);font-size:13px}.nl-six8-identity strong{color:#fff}.postid-7219 .nl-spinner{display:none!important}.nl-six8-more,.nl-six8-context{max-width:1180px;margin:22px auto;padding:0 18px;direction:rtl}.nl-six8-more>summary,.nl-six8-context>summary{cursor:pointer;list-style:none;padding:15px 18px;border:1px solid rgba(0,0,0,.14);border-radius:14px;background:#fff;font-weight:800;color:#1f2937}.nl-six8-more>summary:after,.nl-six8-context>summary:after{content:"+";float:left;font-size:22px}.nl-six8-more[open]>summary:after,.nl-six8-context[open]>summary:after{content:"–"}.nl-six8-more[open]>summary,.nl-six8-context[open]>summary{margin-bottom:16px}'
            . '@media(max-width:760px){.nl-six8-facilities__grid{grid-template-columns:1fr}.nl-six8-facility{min-height:120px;padding:11px 12px}.postid-7219 .nlfb-row{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;overflow:visible!important}.postid-7219 .nlfb-i{min-width:0!important;width:auto!important}.postid-7219 .nl-sticky__main{font-size:13px!important;line-height:1.2!important}}'
            . '</style>';
    }
}, 99);

add_action('wp_footer', function () {
    $is_six8 = is_singular('nadlan_project') && (int) get_queried_object_id() === 7219;
    $designer = isset($_GET['project']) && sanitize_key(wp_unslash($_GET['project'])) === 'six-8-herbert-samuel-tel-aviv'
        && false !== strpos((string) ($_SERVER['REQUEST_URI'] ?? ''), '/tour/designer/');

    if (!$is_six8 && !$designer) {
        return;
    }
    ?>
    <script id="nl-six8-buyer-journey">
    (function(){
      const slug='six-8-herbert-samuel-tel-aviv';
      const isDesigner=<?php echo $designer ? 'true' : 'false'; ?>;

      function cleanRoomLabels(root=document){
        root.querySelectorAll('option,.nl-compare-card,.nl-compare-row,[class*="compare"]').forEach(el=>{
          if(/(?:^|\s)0\s*(?:חדרים|חד׳)/.test(el.textContent||'')){
            el.textContent=(el.textContent||'').replace(/(?:^|\s)0\s*(?:חדרים|חד׳)\s*[·|,]?/g,' ');
          }
        });
      }

      function patchProject(){
        if(!document.body.classList.contains('postid-7219')) return;

        const heroFacts=document.querySelector('.nl-hero__facts');
        if(heroFacts&&!document.querySelector('.nl-six8-identity')){
          const identity=document.createElement('div');
          identity.className='nl-six8-identity';
          identity.innerHTML='<span><strong>יזם:</strong> קבוצת אביב · לאני גרופ</span><span><strong>אדריכלות:</strong> משה צור</span><span><strong>עיצוב שטחים ציבוריים:</strong> פטרישיה אורקיולה</span>';
          heroFacts.insertAdjacentElement('afterend',identity);
        }

        const featureLinks=[...document.querySelectorAll('.nlfb a,a.nlfb-i')];
        featureLinks.forEach(a=>{
          const t=(a.textContent||'').trim();
          if(t.includes('בחירת דירה')){
            a.setAttribute('href','#inventory');
            if(!a.dataset.six8InventoryBound){
              a.dataset.six8InventoryBound='1';
              a.addEventListener('click',e=>{
                const target=document.querySelector('#inventory,.nl-inventory,.nl-invhead');
                if(target){e.preventDefault();e.stopImmediatePropagation();target.scrollIntoView({behavior:'smooth',block:'start'});}
              },true);
            }
          }
          if(t.includes('עיצוב')||t.includes('מעצב')){
            a.setAttribute('href','#studio');
            if(!a.dataset.six8StudioBound){
              a.dataset.six8StudioBound='1';
              a.addEventListener('click',e=>{
                const target=document.querySelector('.nl-studio-launch');
                if(target){e.preventDefault();e.stopImmediatePropagation();target.click();}
              },true);
            }
          }
        });

        if(!document.querySelector('.nl-six8-facilities')){
          const hero=document.querySelector('.nl-hero');
          if(hero){
            const box=document.createElement('section');
            box.className='nl-six8-facilities';
            box.setAttribute('aria-label','מתקני הפרויקט');
            box.innerHTML='<h2>החוויה של SIX-8</h2><div class="nl-six8-facilities__grid">'
              +'<div class="nl-six8-facility" style="background-image:url(https://nad-lan.co.il/wp-content/uploads/2026/08/six8-herbert-samuel-rooftop-pool-08-breichat-gag.jpg)"><strong>מים ובריאות</strong><small>בריכת גג · ספא · חדר כושר</small></div>'
              +'<div class="nl-six8-facility" style="background-image:url(https://nad-lan.co.il/wp-content/uploads/2026/08/six8-herbert-samuel-lobby-03-lobby-malon.jpg)"><strong>שירות ואירוח</strong><small>קונסיירז׳ · בר על הגג · מלון בוטיק</small></div>'
              +'<div class="nl-six8-facility" style="background-image:url(https://nad-lan.co.il/wp-content/uploads/2026/08/six8-herbert-samuel-aerial-hero-01-mabat-avir.jpg)"><strong>קהילה ומסחר</strong><small>מסחר בקומת הקרקע וחיבור ישיר לטיילת</small></div>'
              +'</div>';
            hero.insertAdjacentElement('afterend',box);
          }
        }

        const map=document.querySelector('#nlpjx-map');
        const world=document.querySelector('#world');
        if(map&&world&&!map.dataset.six8Moved){map.dataset.six8Moved='1';world.insertAdjacentElement('afterend',map);}

        const inventory=document.querySelector('#inventory');
        const media=document.querySelector('#media');
        const price=document.querySelector('#price');
        if(inventory&&media&&!media.dataset.six8Moved){media.dataset.six8Moved='1';inventory.insertAdjacentElement('afterend',media);}
        if(media&&price&&world&&map&&!document.querySelector('.nl-six8-context')){
          const context=document.createElement('details');
          context.className='nl-six8-context';
          context.innerHTML='<summary>מחירים, מיקום והסביבה</summary>';
          media.insertAdjacentElement('afterend',context);
          [price,world,map].forEach(el=>context.appendChild(el));
        }
        document.querySelectorAll("a[href='#price'],a[href='#world']").forEach(a=>{
          if(a.dataset.six8ContextBound) return;
          a.dataset.six8ContextBound='1';
          a.addEventListener('click',e=>{
            const context=document.querySelector('.nl-six8-context');
            const target=document.querySelector(a.getAttribute('href'));
            if(context&&target){e.preventDefault();e.stopImmediatePropagation();context.open=true;setTimeout(()=>target.scrollIntoView({behavior:'smooth',block:'start'}),30);}
          },true);
        });

        document.querySelectorAll('a[href="#world"]').forEach(a=>{
          if((a.textContent||'').includes('רובע שדה דב')) a.textContent='טיילת תל אביב והים';
        });

        document.querySelectorAll('button').forEach(b=>{
          if((b.textContent||'').includes('רוצים להרגיש את החלל')){
            b.textContent='רוצים לראות את חללי הפרויקט? פתחו סיור תמונות ‹';
            if(!b.dataset.six8MediaBound){
              b.dataset.six8MediaBound='1';
              b.addEventListener('click',e=>{
                const target=document.querySelector('#media');
                if(target){e.preventDefault();e.stopImmediatePropagation();target.scrollIntoView({behavior:'smooth',block:'start'});}
              },true);
            }
          }
          if((b.textContent||'').includes('פתחו את המעצב')){
            b.textContent='איך הדירה תיראה שלכם? פתחו סטודיו עיצוב ‹';
            if(!b.dataset.six8DesignerBound){
              b.dataset.six8DesignerBound='1';
              b.addEventListener('click',e=>{
                const target=document.querySelector('.nl-studio-launch');
                if(target){e.preventDefault();e.stopImmediatePropagation();target.click();}
              },true);
            }
          }
        });

        document.querySelectorAll('a[href*=\"/tour/designer/\"]').forEach(a=>{
          a.setAttribute('href','#studio');
          if(!a.dataset.six8DesignerBound){
            a.dataset.six8DesignerBound='1';
            a.addEventListener('click',e=>{
              const target=document.querySelector('.nl-studio-launch');
              if(target){e.preventDefault();e.stopImmediatePropagation();target.click();}
            },true);
          }
        });

        const firstChip=document.querySelector('.nl-chip');
        if(firstChip&&firstChip.textContent.trim()!=='2 דירות להמחשה') firstChip.textContent='2 דירות להמחשה';

        const liveCanvas=document.querySelector('.nl-stage canvas.show');
        const spinner=document.querySelector('.nl-spinner');
        if(liveCanvas&&spinner) spinner.classList.add('nl-six8-loaded');

        document.querySelectorAll('button').forEach(b=>{
          if((b.textContent||'').includes('שיתוף סיור חי')) b.style.display='none';
        });

        const phone=document.querySelector('input[type="tel"],input[name*="phone"],input[name*="tel"]');
        if(phone){phone.required=true;phone.setAttribute('aria-required','true');}

        const sticky=document.querySelector('.nl-sticky__main');
        if(sticky&&document.querySelector('.nl-unit-screen h3')&&sticky.textContent!=='קבלו פרטים על הדירה שבחרתם') sticky.textContent='קבלו פרטים על הדירה שבחרתם';

        const article=document.querySelector('.nadlan-project-article');
        if(article&&!document.querySelector('.nl-six8-more')){
          const more=document.createElement('details');
          more.className='nl-six8-more';
          more.innerHTML='<summary>מידע נוסף, מימון ותיאום ביקור</summary>';
          article.parentNode.insertBefore(more,article);
          const extra=[article,document.querySelector('#nlpjx-price'),document.querySelector('#nlpjx-finance'),document.querySelector('#nlpjx-world'),document.querySelector('#nlsch')];
          extra.filter(Boolean).forEach(el=>more.appendChild(el));
        }

        cleanRoomLabels();
      }

      function patchDesigner(){
        if(!isDesigner) return;
        document.title='מעצב הדירה | SIX-8 תל אביב';
        const replacements=[
          ['פרויקט שדה דב','SIX-8 תל אביב'],
          ['שדה דב','SIX-8'],
          ['דירה 1','דירת הדגמה — קומה 11'],
          ['מעצב הדירה','מעצב הדירה — SIX-8']
        ];
        document.querySelectorAll('h1,h2,h3,p,span,small,strong,button,a,label').forEach(el=>{
          if(el.children.length) return;
          let t=(el.textContent||'').trim();
          replacements.forEach(([from,to])=>{ if(t===from) t=to; });
          if(t && t!==(el.textContent||'').trim()) el.textContent=t;
        });
        document.querySelectorAll('a[href*="wa.me"],a[href*="whatsapp"]').forEach(a=>{
          try{
            const u=new URL(a.href);
            const txt='שלום, אני מתעניין/ת בקונספט עיצוב לדירת SIX-8';
            if(u.searchParams.has('text')) u.searchParams.set('text',txt);
            a.href=u.toString();
          }catch(e){}
        });
      }

      function run(){patchProject();patchDesigner();}
      if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run,{once:true}); else run();
      const mo=new MutationObserver(()=>{clearTimeout(window.__six8PatchTimer);window.__six8PatchTimer=setTimeout(run,80);});
      mo.observe(document.documentElement,{childList:true,subtree:true});
      setTimeout(run,1600);
      setTimeout(run,4000);
    })();
    </script>
    <?php
}, 99);
