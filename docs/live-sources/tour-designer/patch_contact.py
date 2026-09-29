# -*- coding: utf-8 -*-
"""WhatsAppBarEverywhere, design system v103 (29.9.2026, owner order): in the apartment designer the demo card form is
replaced by a contact step, "המשך — שיחה עם נציג". The payment infrastructure stays in the file, switched off by one
constant (PAY_DEMO = false).
  python patch_contact.py live    -> scratchpad/wa/designer-tour.live-contact.html  (the live source + this change only)
  python patch_contact.py branch  -> patches plugins/nadlan-config/assets/tours/designer-tour.html in place (Batch 2 + this)
Every anchor must match exactly once, or nothing is written."""
import hashlib, io, os, sys
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
SP = os.path.dirname(os.path.abspath(__file__))
LIVE_SRC = os.path.join(REPO, "docs", "live-sources", "tour-designer", "apartment-designer.html")
BRANCH = os.path.join(REPO, "plugins", "nadlan-config", "assets", "tours", "designer-tour.html")
LIVE_SHA = "09314eb5d755080e"

CSS = """  /* v103: the contact step (no card form; the demo checkout stays in the file, switched off by PAY_DEMO) */
  #contactCard{border-radius:18px;border:1px solid rgba(243,236,221,.12);background:rgba(243,236,221,.04);padding:13px 15px;
               display:flex;flex-direction:column;gap:6px;font-size:13.5px;font-weight:300;line-height:1.6;color:var(--txt)}
  .ctxt{margin:0;font-size:14px;font-weight:300;line-height:1.65;color:var(--txt)}
  #contactBtn{display:flex;align-items:center;justify-content:center;gap:10px;min-height:54px;border-radius:999px;width:100%;
              background:var(--wa);color:#fff;font-size:16px;font-weight:700;text-decoration:none;transition:transform .2s,filter .2s}
  #contactBtn:hover{transform:translateY(-1px);filter:brightness(1.06)}
  #contactBtn svg{width:20px;height:20px;fill:#fff}
"""
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.87 9.87 0 0 0 4.79 1.22c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Z"/></svg>'
SECTION = ("""      <section class="fstep" data-step="contact">
        <div class="fsec"><h3>איך ממשיכים</h3>
          <p class="ctxt">שלחו לנו את העיצוב בוואטסאפ: הבחירות, הריהוט וכל ההערות. נציג נדל״ן יחזור אליכם ויתאם את ההמשך מול היזם. אין תשלום באתר ואין התחייבות.</p>
          <div id="contactCard"><span id="contactSum"></span><span id="contactSum2"></span></div>
        </div>
        <a id="contactBtn" href="https://wa.me/972525101555" target="_blank" rel="noopener">""" + WA_SVG + """<span>שליחת העיצוב לנציג בוואטסאפ</span></a>
        <button class="fghost" id="backToDetails3">‹ חזרה לפרטים</button>
        <div class="legalRow">הדגמה · שום דבר לא נשלח עד הלחיצה</div>
      </section>
""")
JS = """
/* ---- v103 (29.9.2026, owner order): no card form. "המשך — שיחה עם נציג": the design goes to a NadLan representative on
   WhatsApp, with every choice and note. The demo checkout (#payCard, the 2,500 line, #payBtn, completeOrder) stays in the
   file, switched off here: set PAY_DEMO=true only when a developer approves taking payments. ---- */
const PAY_DEMO=false;
function buildContact(){
  if(!orderRef)orderRef='NDL-'+Date.now().toString(36).toUpperCase().slice(-6);
  $('#contactSum').textContent=CATS.map(c=>OPTS[c].label+': '+OPTS[c].items[choices[c]].n).join(' · ')+' · '+T.moodLabel+': '+T.moodNames[mood];
  $('#contactSum2').textContent='ריהוט שהוספתם: '+furniture.length+' · הערות: '+Object.keys(notes).length;
  buildWa();
  $('#contactBtn').href=$('#waBtn').href;}
$('#contactBtn').addEventListener('click',()=>{
  buildContact();
  payload=buildPayload();payload.demo=true;payload.payment={mode:'contact',charged:false};
  $('#okRef').textContent=T.waRef+': '+orderRef;
  $('#rfpJson').textContent=JSON.stringify(payload,null,2);
  const h=$('#okWrap h3'),p=$('#okWrap p');
  if(h)h.innerHTML='העיצוב <b>מוכן</b>';
  if(p)p.textContent='פתחנו לכם וואטסאפ עם העיצוב: הבחירות, הריהוט וההערות. אחרי השליחה נציג נדל״ן יחזור אליכם. אין תשלום באתר.';
  T.flowTitles.done='העיצוב <b>מוכן</b>';
  setTimeout(()=>setFlowStep('done'),60);});
$('#backToDetails3').addEventListener('click',()=>setFlowStep('details'));
"""


def once(s, old, new, label):
    n = s.count(old)
    if n != 1:
        sys.exit("anchor %s matched %d times, nothing written" % (label, n))
    return s.replace(old, new)


def apply(s, branch):
    s = once(s, "  .legalRow{font-size:11px;", CSS + "  .legalRow{font-size:11px;", "css")
    s = once(s, '      <section class="fstep" data-step="pay">', SECTION + '      <section class="fstep" data-step="pay">', "section")
    s = once(s, '<div class="fs" data-fs="3"><span class="d">4</span><span class="t">הזמנה</span></div>',
             '<div class="fs" data-fs="3"><span class="d">4</span><span class="t">המשך</span></div>', "bar label")
    s = once(s, '<div id="demoRibbon">הדגמה — לא מתבצע חיוב אמיתי</div>', '<div id="demoRibbon">הדגמה · אין תשלום באתר</div>', "ribbon")
    s = once(s, "pay:'הזמנה — <b>הדגמה</b>',", "pay:'הזמנה — <b>הדגמה</b>',contact:'המשך — <b>שיחה עם נציג</b>',", "title")
    if branch:
        s = once(s, "const stage=name==='done'?4:(name==='send'?3:FLOW_STEPS.indexOf(name)+1);",
                 "const stage=name==='done'?4:(name==='send'||name==='contact'?3:FLOW_STEPS.indexOf(name)+1);", "stage")
        s = once(s, "$('#toPay').addEventListener('click',()=>{if(validateDetails()){if(CTX){buildSend();setFlowStep('send');}else setFlowStep('pay');}});",
                 "$('#toPay').addEventListener('click',()=>{if(validateDetails()){if(CTX){buildSend();setFlowStep('send');}else if(PAY_DEMO)setFlowStep('pay');else{buildContact();setFlowStep('contact');}}});", "toPay")
    else:
        s = once(s, "const stage=name==='done'?4:FLOW_STEPS.indexOf(name)+1;",
                 "const stage=name==='done'?4:(name==='contact'?3:FLOW_STEPS.indexOf(name)+1);", "stage")
        s = once(s, "$('#toPay').addEventListener('click',()=>{if(validateDetails())setFlowStep('pay');});",
                 "$('#toPay').addEventListener('click',()=>{if(validateDetails()){if(PAY_DEMO)setFlowStep('pay');else{buildContact();setFlowStep('contact');}}});", "toPay")
        s = once(s, '<button class="fcta" id="toPay">המשך להזמנה ›</button>', '<button class="fcta" id="toPay">המשך ›</button>', "toPay label")
    s = once(s, "/* ---- mock payment (simulation only", JS.lstrip("\n") + "\n/* ---- mock payment (simulation only", "js")
    return s


mode = sys.argv[1] if len(sys.argv) > 1 else "live"
if mode == "live":
    raw = open(LIVE_SRC, "rb").read()
    if hashlib.sha256(raw).hexdigest()[:16] != LIVE_SHA:
        sys.exit("the live source changed")
    out = apply(raw.decode("utf-8"), False)
    dst = os.path.join(SP, "designer-tour.live-contact.html")
else:
    out = apply(io.open(BRANCH, encoding="utf-8", newline="").read(), True)
    dst = BRANCH
io.open(dst, "w", encoding="utf-8", newline="").write(out)
print("written", dst, hashlib.sha256(out.encode("utf-8")).hexdigest()[:16])
