// NadLan apartment designer: the shared call (HAD-706). A real video call INSIDE the designer: the buyer, the sales rep and
// an invited interior designer see the same plan and 3D apartment, talk, and pass "the pen" (who may change the design).
//
//   import { joinCall, livekitTransport } from '.../assets/designer/call.js';
//   const call = await joinCall(designer, { container, transport: livekitTransport({ url, token }), room, identity, name, role, lang, onLeave });
//   call.give(id); call.ask(); call.follow(true); call.leave();
//
// The module talks to the network only through a small transport (connect, disconnect, publishData, onData, participants,
// onParticipants, setMicrophone, setCamera, switchCamera, shareScreen, attach, onQuality, onSpeaking, onState), so the same
// logic runs on LiveKit in production and on a BroadcastChannel stand-in (call-mock.js) in the local checks.
//
// Data topics (JSON, one object per message):
//   sys          reliable  hello / state (the pen, the hands, the design revision) for a newcomer
//   pen          reliable  set {holder, seq} / ask / ack: exactly one person holds the pen; seq orders the handovers
//   design       reliable  op {op, rev, by (a ROLE, never a name), g (gesture), at}: the pen holder's changes, applied remote
//   design-snap  reliable  ask / snap {design}: the whole design for a late joiner or after a missed change
//   view         lossy     the presenter's (the pen holder's) camera, about 10 a second
//   ptr          lossy     a pointer the others see on the plan and on the 3D
//   chat, hand   reliable  short text messages and raised hands
// Nothing is recorded and nothing personal is stored: the design log keeps the role only.

const LK_LIB = 'https://cdn.jsdelivr.net/npm/livekit-client@2.22.3/dist/livekit-client.esm.mjs'; // the same build the TogetherRoom loads
const BASE = new URL('.', import.meta.url).href;
const now = () => performance.timeOrigin + performance.now(); // one clock across the tabs of one browser (the local checks)
const ROLES = ['buyer', 'rep', 'designer', 'family'];
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const STR = {
  he: {
    dir: 'rtl',
    roles: { buyer: 'קונה', rep: 'נציג המכירות', designer: 'מעצב הפנים', family: 'משפחה' },
    you: 'את/ה', youTag: 'אני',
    penMine: 'העט אצלך: השינויים שלך מופיעים אצל כולם.',
    penOf: (n) => 'העט אצל ' + n,
    refuse: (n) => 'העט אצל ' + n + ' כרגע, ורק מי שמחזיק אותו משנה את העיצוב.',
    ask: 'לבקש את העט', asked: 'ביקשת את העט. מחכים לתשובה.', take: 'לקחת את העט',
    give: 'להעביר את העט', giveTo: (n) => 'להעביר ל' + n, asks: (n) => n + ' מבקש/ת את העט', notNow: 'לא עכשיו',
    gotPen: 'העט אצלך עכשיו. אפשר לשנות את העיצוב.', penMoved: (n) => 'העט עבר ל' + n + '.',
    mic: 'מיקרופון', micOff: 'להשתיק', micOn: 'להפעיל את המיקרופון',
    cam: 'מצלמה', camOff: 'לכבות את המצלמה', camOn: 'להפעיל את המצלמה',
    flip: 'להחליף בין המצלמה הקדמית לאחורית', share: 'להציג את המסך', shareStop: 'להפסיק להציג את המסך',
    more: 'עוד', moreLabel: 'עוד אפשרויות', leave: 'לצאת', leaveLabel: 'לצאת מהשיחה',
    follow: (n) => 'רואים את מה ש' + n + ' רואה', alone: 'מסתכלים לבד', back: (n) => 'לחזור למבט של ' + n, backShort: 'לחזור',
    hand: 'להרים יד', handDown: 'להוריד יד', handUp: (n) => n + ' הרים/ה יד',
    chat: 'הודעות', chatPh: 'כתבו הודעה לכולם', send: 'לשלוח',
    invite: 'להזמין מעצב פנים או בן משפחה', copy: 'להעתיק קישור', copied: 'הקישור הועתק. אין בו פרטים אישיים.',
    noRec: 'השיחה לא מוקלטת.',
    connecting: 'מתחברים…', reconnecting: 'החיבור נקטע, מתחברים שוב…', connected: 'מחוברים', lost: 'השיחה נותקה.',
    q: { excellent: 'קליטה טובה', good: 'קליטה סבירה', poor: 'קליטה חלשה', lost: 'אין קליטה', unknown: 'בודקים קליטה' },
    audio: 'להפעלת השמע לחצו כאן', people: 'בשיחה', sharing: (n) => n + ' מציג/ה את המסך', denied: 'אין גישה למצלמה או למיקרופון. אפשר לאשר בהגדרות הדפדפן.',
    callBar: 'שיחת וידאו', tiles: 'המשתתפים',
  },
  en: {
    dir: 'ltr',
    roles: { buyer: 'Buyer', rep: 'Sales rep', designer: 'Interior designer', family: 'Family' },
    you: 'you', youTag: 'Me',
    penMine: 'You hold the pen: your changes appear for everyone.',
    penOf: (n) => 'The pen is with ' + n,
    refuse: (n) => 'The pen is with ' + n + ' right now, and only the person holding it changes the design.',
    ask: 'Ask for the pen', asked: 'You asked for the pen. Waiting for an answer.', take: 'Take the pen',
    give: 'Hand over the pen', giveTo: (n) => 'Hand to ' + n, asks: (n) => n + ' asks for the pen', notNow: 'Not now',
    gotPen: 'You hold the pen now. You can change the design.', penMoved: (n) => 'The pen moved to ' + n + '.',
    mic: 'Microphone', micOff: 'Mute', micOn: 'Unmute',
    cam: 'Camera', camOff: 'Turn camera off', camOn: 'Turn camera on',
    flip: 'Switch between front and back camera', share: 'Show my screen', shareStop: 'Stop showing my screen',
    more: 'More', moreLabel: 'More options', leave: 'Leave', leaveLabel: 'Leave the call',
    follow: (n) => 'Seeing what ' + n + ' sees', alone: 'Looking around alone', back: (n) => 'Back to ' + n + '’s view', backShort: 'Back',
    hand: 'Raise hand', handDown: 'Lower hand', handUp: (n) => n + ' raised a hand',
    chat: 'Messages', chatPh: 'Write to everyone', send: 'Send',
    invite: 'Invite an interior designer or family', copy: 'Copy link', copied: 'Link copied. It holds no personal details.',
    noRec: 'This call is not recorded.',
    connecting: 'Connecting…', reconnecting: 'Connection lost, reconnecting…', connected: 'Connected', lost: 'The call ended.',
    q: { excellent: 'Good signal', good: 'Fair signal', poor: 'Weak signal', lost: 'No signal', unknown: 'Checking signal' },
    audio: 'Tap here to turn on sound', people: 'In the call', sharing: (n) => n + ' is showing a screen', denied: 'No access to the camera or microphone. You can allow it in the browser settings.',
    callBar: 'Video call', tiles: 'Participants',
  },
};

const ICON = {
  mic: '<path d="M12 3a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V6a3 3 0 0 1 3-3zM5 11a7 7 0 0 0 14 0M12 18v3"/>',
  micOff: '<path d="M12 3a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V6a3 3 0 0 1 3-3zM5 11a7 7 0 0 0 14 0M12 18v3M4 4l16 16"/>',
  cam: '<path d="M3 7h12v10H3zM15 10l6-3v10l-6-3"/>',
  camOff: '<path d="M3 7h12v10H3zM15 10l6-3v10l-6-3M3 3l18 18"/>',
  flip: '<path d="M4 8h12l-3-3M20 16H8l3 3"/>',
  share: '<path d="M3 4h18v12H3zM8 20h8M12 13V7M9 10l3-3 3 3"/>',
  pen: '<path d="M4 20l4-1 11-11-3-3L5 16zM14 6l3 3"/>',
  eye: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
  more: '<circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/>',
  leave: '<path d="M3 15c5-5 13-5 18 0l-3 3-3-2v-3c-2-1-4-1-6 0v3l-3 2z"/>',
  hand: '<path d="M8 13V5a1.5 1.5 0 0 1 3 0v6M11 11V4a1.5 1.5 0 0 1 3 0v7M14 11V5.5a1.5 1.5 0 0 1 3 0V14c0 4-3 7-6.5 7S5 18 4 15l-1.5-4a1.5 1.5 0 0 1 2.7-1.2L8 13"/>',
};
const svg = (k) => '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + ICON[k] + '</svg>';

function ensureCss(shadow) {
  if (shadow.querySelector('link[data-ndc-css]')) return Promise.resolve();
  const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = BASE + 'call.css?v=1'; l.setAttribute('data-ndc-css', '');
  shadow.appendChild(l);
  return new Promise((r) => { l.addEventListener('load', r, { once: true }); l.addEventListener('error', r, { once: true }); setTimeout(r, 3000); });
}
const pct = (arr, p) => { if (!arr.length) return null; const s = [...arr].sort((a, b) => a - b); return s[Math.min(s.length - 1, Math.floor((p / 100) * s.length))]; };

/** Joins the call inside a mounted designer. Resolves once connected; the pen settles a moment later (call.ready). */
export async function joinCall(designer, opts = {}) {
  const T = STR[opts.lang === 'en' ? 'en' : 'he'], tr = opts.transport, me = String(opts.identity), myRole = ROLES.includes(opts.role) ? opts.role : 'buyer';
  if (!tr) throw new Error('joinCall: a transport is required');
  const store = designer.store, container = opts.container, shadow = container.getRootNode(), host = shadow.host || document.body;
  await ensureCss(shadow);
  const root = shadow.querySelector('.nd');
  const offs = [], timers = [];
  const on = (el, ev, fn, o) => { el.addEventListener(ev, fn, o); offs.push(() => el.removeEventListener(ev, fn, o)); };

  const S = {
    pen: { holder: null, seq: 0 }, people: new Map(), speaking: new Set(), quality: {}, hands: new Set(), following: true,
    ptrs: new Map(), chat: [], state: 'connecting', asked: 0, askFrom: null, snapAsked: 0, alive: true, mic: false, cam: false, screen: false,
    facing: 'user', panel: null, lastView: '', lastViewAt: 0, refusedAt: 0, joinedAt: now(),
  };
  const stats = { op: [], opApply: [], pen: [], penRtt: [], view: [], snap: null, refused: 0, ignored: 0, resync: 0, sent: { design: 0, view: 0, ptr: 0 } };
  let readyRes; const ready = new Promise((r) => (readyRes = r));

  const person = (id) => S.people.get(id) || null;
  const roleOf = (id) => { const p = person(id); return p && ROLES.includes(p.role) ? p.role : 'buyer'; };
  const nameOf = (id) => { if (id === me) return T.you; const p = person(id); if (!p) return T.roles.buyer; const r = T.roles[p.role] || ''; return p.name ? p.name + (r ? ' (' + r + ')' : '') : r; };
  const send = (topic, obj, reliable = true, to) => { try { return tr.publishData(topic, { ...obj, from: me }, { reliable, to }); } catch (e) { return false; } };

  /* ---------------- the dock ---------------- */
  const dock = document.createElement('section');
  dock.className = 'ndc'; dock.dir = T.dir; dock.lang = opts.lang === 'en' ? 'en' : 'he';
  dock.setAttribute('aria-label', T.callBar);
  dock.innerHTML =
    '<div class="ndc-top"><div class="ndc-tiles" data-ndc="tiles" role="list" aria-label="' + T.tiles + '"></div>' +
    '<div class="ndc-status"><p class="ndc-pen" data-ndc="penline" aria-live="polite"></p><p class="ndc-follow" data-ndc="followline" hidden></p><p class="ndc-norec">' + T.noRec + '</p><p class="ndc-conn" data-ndc="conn" role="status"></p></div></div>' +
    '<div class="ndc-ask" data-ndc="askbar" hidden><span data-ndc="asktext"></span><button class="ndc-b ndc-go" data-ndc="askgive"></button><button class="ndc-b" data-ndc="askno">' + T.notNow + '</button></div>' +
    '<div class="ndc-ctl" role="toolbar" aria-label="' + T.callBar + '">' +
    '<button class="ndc-b" data-ndc="mic">' + svg('mic') + '</button>' +
    '<button class="ndc-b" data-ndc="cam">' + svg('cam') + '</button>' +
    '<button class="ndc-b" data-ndc="flip" aria-label="' + T.flip + '" title="' + T.flip + '" hidden>' + svg('flip') + '</button>' +
    '<button class="ndc-b" data-ndc="share" hidden>' + svg('share') + '</button>' +
    '<button class="ndc-b ndc-pb" data-ndc="pen">' + svg('pen') + '<span data-ndc="pentext"></span></button>' +
    '<button class="ndc-b" data-ndc="follow" hidden>' + svg('eye') + '<span>' + T.backShort + '</span></button>' +
    '<button class="ndc-b" data-ndc="more" aria-label="' + T.moreLabel + '" title="' + T.moreLabel + '" aria-expanded="false">' + svg('more') + '</button>' +
    '<button class="ndc-b ndc-stop" data-ndc="leave" aria-label="' + T.leaveLabel + '" title="' + T.leaveLabel + '">' + svg('leave') + '</button></div>' +
    '<div class="ndc-panel" data-ndc="panel" hidden></div>' +
    '<div class="ndc-toast" data-ndc="toast" role="status" hidden></div>';
  container.appendChild(dock);
  const ptrLayer = document.createElement('div'); ptrLayer.className = 'ndc-ptrs'; ptrLayer.setAttribute('aria-hidden', 'true'); container.appendChild(ptrLayer);
  const audioBox = document.createElement('div'); audioBox.hidden = true; container.appendChild(audioBox);
  const $ = (k) => dock.querySelector('[data-ndc="' + k + '"]');
  let toastT = 0;
  const say = (msg) => { const t = $('toast'); t.textContent = msg; t.hidden = false; clearTimeout(toastT); toastT = setTimeout(() => (t.hidden = true), 3200); };

  // the phone: a strip above the designer that never covers the 3D or the plan controls; wide screens: a column at the side
  const prevStyle = root ? { top: root.style.top, end: root.style.insetInlineEnd } : null;
  function layout() {
    if (!root || !S.alive) return;
    const wide = host.clientWidth >= 900 && innerWidth >= 900;
    dock.classList.toggle('ndc-side', wide);
    if (wide) { root.style.top = ''; root.style.insetInlineEnd = dock.offsetWidth + 'px'; }
    else { root.style.insetInlineEnd = ''; root.style.top = dock.offsetHeight + 'px'; } // the panel and the toasts float; only the strip itself counts
  }
  const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(() => layout()) : null;
  if (ro) ro.observe(host);

  /* ---------------- tiles ---------------- */
  const tiles = new Map();
  function paintTiles() {
    const box = $('tiles'), list = tr.participants();
    S.people = new Map(list.map((p) => [p.id, p]));
    for (const [id, el] of tiles) if (!S.people.has(id)) { el.remove(); tiles.delete(id); }
    for (const p of list) {
      let el = tiles.get(p.id);
      if (!el) {
        el = document.createElement('div'); el.className = 'ndc-tile' + (p.local ? ' ndc-me' : ''); el.setAttribute('role', 'listitem'); el.dataset.id = p.id;
        el.innerHTML = '<video playsinline autoplay muted></video><b class="ndc-ini"></b><span class="ndc-name"></span><i class="ndc-q" aria-hidden="true"><s></s><s></s><s></s></i><em class="ndc-mark"></em>';
        el.onclick = () => { if (p.screen) el.classList.toggle('ndc-big'); };
        tiles.set(p.id, el); box.appendChild(el);
      }
      const v = el.querySelector('video'), wantV = p.screen ? 'screen' : p.cam ? 'video' : '';
      if (wantV && el.dataset.v !== wantV) { try { if (tr.attach(p.id, wantV, v) !== false) el.dataset.v = wantV; } catch (e) { /* the track is not there yet */ } }
      if (!wantV) { el.dataset.v = ''; v.removeAttribute('src'); v.srcObject = null; }
      el.classList.toggle('ndc-has-v', !!wantV);
      el.classList.toggle('ndc-mirror', !!(p.local && p.cam && !p.screen && S.facing === 'user'));
      el.querySelector('.ndc-ini').textContent = (p.name || T.roles[p.role] || '?').trim().charAt(0);
      el.querySelector('.ndc-name').textContent = p.local ? T.youTag : p.name || T.roles[p.role] || '';
      const q = S.quality[p.id] || p.quality || 'unknown';
      el.querySelector('.ndc-q').className = 'ndc-q ndc-q-' + q; el.querySelector('.ndc-q').title = T.q[q] || '';
      const marks = [];
      if (S.pen.holder === p.id) marks.push('<span class="ndc-m-pen" title="' + esc(T.penOf(nameOf(p.id))) + '">' + svg('pen') + '</span>');
      if (S.hands.has(p.id)) marks.push('<span class="ndc-m-hand">' + svg('hand') + '</span>');
      if (!p.mic) marks.push('<span class="ndc-m-mute">' + svg('micOff') + '</span>');
      el.querySelector('.ndc-mark').innerHTML = marks.join('');
      el.classList.toggle('ndc-speaking', S.speaking.has(p.id));
      el.classList.toggle('ndc-pen-on', S.pen.holder === p.id);
      el.setAttribute('aria-label', (p.local ? T.youTag : nameOf(p.id)) + (S.pen.holder === p.id ? ' · ' + T.penOf(p.local ? T.you : nameOf(p.id)) : '') + (p.mic ? '' : ' · ' + T.micOn) + ' · ' + (T.q[q] || ''));
    }
    paintCtl();
  }
  function paintCtl() {
    const lp = S.people.get(me) || {};
    S.mic = !!lp.mic; S.cam = !!lp.cam; S.screen = !!lp.screen;
    const mic = $('mic'), cam = $('cam'), sh = $('share');
    mic.innerHTML = svg(S.mic ? 'mic' : 'micOff'); mic.setAttribute('aria-label', S.mic ? T.micOff : T.micOn); mic.title = mic.getAttribute('aria-label'); mic.setAttribute('aria-pressed', String(!S.mic)); mic.classList.toggle('ndc-off', !S.mic);
    cam.innerHTML = svg(S.cam ? 'cam' : 'camOff'); cam.setAttribute('aria-label', S.cam ? T.camOff : T.camOn); cam.title = cam.getAttribute('aria-label'); cam.setAttribute('aria-pressed', String(!S.cam)); cam.classList.toggle('ndc-off', !S.cam);
    sh.setAttribute('aria-label', S.screen ? T.shareStop : T.share); sh.title = sh.getAttribute('aria-label'); sh.setAttribute('aria-pressed', String(S.screen));
    const mine = S.pen.holder === me, pt = $('pentext'), pb = $('pen');
    pt.textContent = mine ? T.give : myRole === 'rep' ? T.take : T.ask;
    pb.classList.toggle('ndc-go', !mine && Date.now() - S.asked > 8000);
    pb.setAttribute('aria-label', pt.textContent);
    $('penline').textContent = !S.pen.holder ? '' : mine ? T.penMine : T.penOf(nameOf(S.pen.holder));
    $('conn').textContent = S.state === 'connected' ? '' : T[S.state] || '';
    const fl = $('followline'), fb = $('follow'), lead = S.pen.holder && S.pen.holder !== me;
    fb.hidden = !lead || S.following;
    if (lead) { fb.setAttribute('aria-label', T.back(nameOf(S.pen.holder))); fb.title = fb.getAttribute('aria-label'); }
    fl.hidden = !lead; fl.textContent = lead ? (S.following ? T.follow(nameOf(S.pen.holder)) : T.alone) : '';
    if (S.panel) paintPanel();
    layout();
  }

  /* ---------------- the pen ---------------- */
  const guard = (op, meta) => (S.pen.holder === me ? null : { code: 'call.pen', reason: T.refuse(S.pen.holder ? nameOf(S.pen.holder) : T.roles.rep) });
  store.setGuard(guard);
  function setPen(holder, seq, msg) {
    const prev = S.pen.holder;
    S.pen = { holder, seq };
    if (holder === me && prev !== me) {
      S.asked = 0;
      if (msg && msg.from !== me) { send('pen', { t: 'ack', seq, at0: msg.at }, true, [msg.from]); say(T.gotPen); }
    } else if (prev === me && holder !== me) say(T.penMoved(nameOf(holder)));
    if (msg && msg.at && msg.from !== me) stats.pen.push(now() - msg.at);
    if (S.askFrom && (holder !== me || S.askFrom === holder)) hideAsk();
    S.lastView = ''; // the new presenter sends the view at once
    paintTiles();
  }
  const penAuthorized = (msg) => {
    const cur = S.pen.holder;
    return !cur || msg.from === cur || roleOf(msg.from) === 'rep' || !S.people.has(cur) || (msg.holder === msg.from && !S.people.has(cur));
  };
  // two people who joined at the same moment may both claim the first pen: the same rule everywhere picks one (the smaller id)
  const wins = (holder, seq) => seq > S.pen.seq || !S.pen.holder || (seq === S.pen.seq && String(holder) < String(S.pen.holder));
  const conflict = (seq) => seq === S.pen.seq && !!S.pen.holder;
  function give(to) {
    if (S.pen.holder !== me && myRole !== 'rep') return false;
    if (!to || !S.people.has(to)) return false;
    const seq = S.pen.seq + 1, at = now();
    setPen(to, seq);
    send('pen', { t: 'set', holder: to, seq, at });
    return true;
  }
  function ask() {
    if (S.pen.holder === me) return false;
    if (myRole === 'rep') return give(me);
    S.asked = Date.now(); send('pen', { t: 'ask', at: now() }, true, S.pen.holder ? [S.pen.holder] : undefined); say(T.asked); paintCtl(); return true;
  }
  function showAsk(from) {
    S.askFrom = from; $('asktext').textContent = T.asks(nameOf(from)); $('askgive').textContent = T.giveTo(nameOf(from)); $('askbar').hidden = false; layout();
  }
  function hideAsk() { S.askFrom = null; $('askbar').hidden = true; layout(); }
  const successor = (without) => {
    const ids = [...S.people.keys()].filter((id) => id !== without).sort();
    return ids.find((id) => roleOf(id) === 'rep') || ids[0] || null;
  };

  /* ---------------- design sync ---------------- */
  function askSnap(force) {
    if (!S.pen.holder || S.pen.holder === me || (!force && now() - S.snapAsked < 1500)) return;
    S.snapAsked = now(); stats.resync++;
    send('design-snap', { t: 'ask', at: S.snapAsked }, true, [S.pen.holder]);
  }
  const offStore = store.on((e) => {
    if (e.type === 'reject' && e.code === 'call.pen') {
      stats.refused++;
      if (Date.now() - S.refusedAt > 2000) { S.refusedAt = Date.now(); designer.toast(e.reason, 'stop'); $('pen').classList.add('ndc-flash'); setTimeout(() => $('pen').classList.remove('ndc-flash'), 1200); }
      return;
    }
    if (e.type !== 'change' || e.remote || S.pen.holder !== me || !S.alive) return;
    stats.sent.design++;
    send('design', { t: 'op', op: e.op, g: e.gesture, rev: store.design.rev, by: myRole, at: now() });
  });

  /* ---------------- follow me (the pen holder presents) ---------------- */
  const viewTimer = setInterval(() => {
    if (!S.alive || S.pen.holder !== me || S.state !== 'connected') return;
    const v = designer.getView(); if (!v) return;
    const r = (x) => Math.round(x * 100) / 100, key = [v.mode, r(v.x), r(v.y), r(v.z), r(v.yaw), r(v.pitch)].join(',');
    if (key === S.lastView && now() - S.lastViewAt < 1000) return;
    S.lastView = key; S.lastViewAt = now(); stats.sent.view++;
    send('view', { t: 'v', v: { mode: v.mode, x: r(v.x), y: r(v.y), z: r(v.z), yaw: Math.round(v.yaw * 1e4) / 1e4, pitch: Math.round(v.pitch * 1e4) / 1e4 }, at: now() }, false);
  }, 100);
  timers.push(() => clearInterval(viewTimer));
  const spaceEl = shadow.querySelector('[data-nd="space"]');
  const lookAway = (ev) => { if (!ev.isTrusted || S.pen.holder === me || !S.following) return; S.following = false; paintCtl(); };
  if (spaceEl) { on(spaceEl, 'pointerdown', lookAway, true); on(spaceEl, 'wheel', lookAway, { capture: true, passive: true }); }
  function follow(onf) { S.following = !!onf; S.lastViewMsg && S.following && designer.setView(S.lastViewMsg); paintCtl(); }

  /* ---------------- pointers ---------------- */
  const planEl = () => shadow.querySelector('.nd-plan');
  function planToScreen(x, y) { const s = planEl(); if (!s || !s.getScreenCTM()) return null; const p = new DOMPoint(x, y).matrixTransform(s.getScreenCTM()); return [p.x, p.y]; }
  function screenToFloor(cx, cy) { // inverts the 3D view's screenOf on the floor plane (a few Newton steps)
    const sp = designer.space; if (!sp || !sp.screenOf) return null;
    const vb = planEl() && planEl().viewBox.baseVal; let x = vb ? vb.x + vb.width / 2 : 500, y = vb ? vb.y + vb.height / 2 : 500;
    for (let i = 0; i < 10; i++) {
      const s = sp.screenOf(x, y), fx = s[0] - cx, fy = s[1] - cy;
      if (Math.hypot(fx, fy) < 1) return [Math.round(x), Math.round(y)];
      const a = sp.screenOf(x + 10, y), b = sp.screenOf(x, y + 10);
      const j11 = (a[0] - s[0]) / 10, j21 = (a[1] - s[1]) / 10, j12 = (b[0] - s[0]) / 10, j22 = (b[1] - s[1]) / 10, det = j11 * j22 - j12 * j21;
      if (!isFinite(det) || Math.abs(det) < 1e-6) return null;
      x -= (j22 * fx - j12 * fy) / det; y -= (-j21 * fx + j11 * fy) / det;
    }
    return null;
  }
  let ptrAt = 0;
  const ptrMove = (src) => (ev) => {
    if (now() - ptrAt < 66) return; ptrAt = now();
    let p = null;
    if (src === 'plan') { const s = planEl(); if (s && s.getScreenCTM()) { const q = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(s.getScreenCTM().inverse()); p = [Math.round(q.x), Math.round(q.y)]; } }
    else p = screenToFloor(ev.clientX, ev.clientY);
    if (!p) return;
    stats.sent.ptr++;
    send('ptr', { t: 'p', x: p[0], y: p[1] }, false);
  };
  const planHost = shadow.querySelector('[data-nd="plan"]');
  if (planHost) on(planHost, 'pointermove', ptrMove('plan'));
  if (spaceEl) on(spaceEl, 'pointermove', ptrMove('space'));
  function paintPtrs() {
    if (!S.alive) return;
    const hr = host.getBoundingClientRect(), t = now();
    for (const [id, p] of S.ptrs) {
      if (t - p.t > 4000 || !S.people.has(id)) { p.a.remove(); p.b.remove(); S.ptrs.delete(id); continue; }
      const sp = designer.space, a = planToScreen(p.x, p.y), b = sp && sp.screenOf ? sp.screenOf(p.x, p.y, 0) : null;
      const put = (el, xy, box) => { const ok = xy && box && xy[0] >= box.left && xy[0] <= box.right && xy[1] >= box.top && xy[1] <= box.bottom; el.hidden = !ok; if (ok) el.style.transform = 'translate(' + (xy[0] - hr.left).toFixed(1) + 'px,' + (xy[1] - hr.top).toFixed(1) + 'px)'; };
      put(p.a, a, planHost && planHost.getBoundingClientRect()); put(p.b, b, spaceEl && spaceEl.getBoundingClientRect());
    }
    if (S.ptrs.size) requestAnimationFrame(paintPtrs); else S.ptrLoop = false;
  }
  function gotPtr(from, m) {
    let p = S.ptrs.get(from);
    if (!p) {
      const mk = () => { const d = document.createElement('div'); d.className = 'ndc-ptr ndc-r-' + roleOf(from); d.innerHTML = '<i></i><span></span>'; d.querySelector('span').textContent = (person(from) && person(from).name) || T.roles[roleOf(from)]; ptrLayer.appendChild(d); return d; };
      p = { a: mk(), b: mk() }; S.ptrs.set(from, p);
    }
    Object.assign(p, { x: m.x, y: m.y, t: now() });
    if (!S.ptrLoop) { S.ptrLoop = true; requestAnimationFrame(paintPtrs); }
  }

  /* ---------------- panel: hand, messages, invite, people ---------------- */
  function inviteLink() {
    const u = new URL(opts.inviteBase || location.href);
    return u.origin + u.pathname + '?room=' + encodeURIComponent(opts.room || '') + (opts.design ? '&design=' + encodeURIComponent(opts.design) : '');
  }
  function paintPanel() {
    const el = $('panel'); el.hidden = !S.panel; $('more').setAttribute('aria-expanded', String(!!S.panel));
    if (!S.panel) return;
    const mine = S.pen.holder === me, canGive = mine || myRole === 'rep';
    const ppl = [...S.people.values()].map((p) => '<li><span>' + esc(p.local ? T.youTag : p.name || T.roles[p.role]) + ' <small>' + esc(T.roles[p.role] || '') + '</small></span>' +
      (canGive && p.id !== S.pen.holder ? '<button class="ndc-b ndc-sm" data-give="' + esc(p.id) + '">' + svg('pen') + '<span>' + esc(T.giveTo(p.local ? T.you : p.name || T.roles[p.role])) + '</span></button>' : S.pen.holder === p.id ? '<b class="ndc-hold">' + svg('pen') + '</b>' : '') + '</li>').join('');
    const msgs = S.chat.slice(-30).map((m) => '<li><b>' + esc(m.who) + '</b> ' + esc(m.text) + '</li>').join('');
    el.innerHTML =
      '<div class="ndc-row"><button class="ndc-b ndc-wide" data-ndc="hand" aria-pressed="' + S.hands.has(me) + '">' + svg('hand') + '<span>' + (S.hands.has(me) ? T.handDown : T.hand) + '</span></button></div>' +
      '<h3>' + T.people + '</h3><ul class="ndc-ppl">' + ppl + '</ul>' +
      '<h3>' + T.chat + '</h3><ul class="ndc-msgs" data-ndc="msgs" aria-live="polite">' + msgs + '</ul>' +
      '<form class="ndc-form" data-ndc="form"><input data-ndc="chatin" maxlength="300" autocomplete="off" aria-label="' + T.chatPh + '" placeholder="' + T.chatPh + '"><button class="ndc-b ndc-go">' + T.send + '</button></form>' +
      '<h3>' + T.invite + '</h3><div class="ndc-row"><input class="ndc-link mono" readonly value="' + esc(inviteLink()) + '" aria-label="' + T.invite + '"><button class="ndc-b" data-ndc="copy">' + T.copy + '</button></div>' +
      '<p class="ndc-fine">' + T.noRec + '</p>';
    el.querySelector('[data-ndc="hand"]').onclick = () => hand(!S.hands.has(me));
    el.querySelectorAll('[data-give]').forEach((b) => (b.onclick = () => { give(b.dataset.give); }));
    el.querySelector('[data-ndc="form"]').onsubmit = (ev) => { ev.preventDefault(); const i = el.querySelector('[data-ndc="chatin"]'); chat(i.value); i.value = ''; };
    el.querySelector('[data-ndc="copy"]').onclick = async () => { const v = inviteLink(); try { await navigator.clipboard.writeText(v); } catch (e) { el.querySelector('.ndc-link').select(); try { document.execCommand('copy'); } catch (x) { /* none */ } } say(T.copied); };
    const ml = el.querySelector('.ndc-msgs'); ml.scrollTop = ml.scrollHeight;
  }
  function chat(text) {
    text = String(text || '').replace(/\s+/g, ' ').trim().slice(0, 300); if (!text) return false;
    S.chat.push({ who: T.youTag, text, from: me }); send('chat', { t: 'm', text, at: now() }); if (S.panel) paintPanel(); return true;
  }
  function hand(up) { if (up) S.hands.add(me); else S.hands.delete(me); send('hand', { t: 'h', up: !!up }); paintTiles(); }

  /* ---------------- incoming ---------------- */
  tr.onData((topic, m, from) => {
    if (!S.alive || !m || typeof m !== 'object' || from === me) return;
    from = String(from || m.from || '');
    switch (topic) {
      case 'sys':
        if (m.t === 'hello') send('sys', { t: 'state', pen: S.pen, hands: [...S.hands], rev: store.design.rev }, true, [from]);
        else if (m.t === 'state' && m.pen && m.pen.holder && typeof m.pen.seq === 'number' && wins(m.pen.holder, m.pen.seq)) {
          (m.hands || []).forEach((h) => S.hands.add(h));
          const clash = conflict(m.pen.seq);
          setPen(String(m.pen.holder), m.pen.seq);
          if (m.pen.holder !== me && (!S.snapGot || clash)) askSnap(true);
        }
        return;
      case 'pen':
        if (m.t === 'set') {
          if (typeof m.seq !== 'number' || !m.holder || !wins(m.holder, m.seq) || !(penAuthorized(m) || (conflict(m.seq) && m.holder === from))) {
            stats.ignored++;
            if (conflict(m.seq) && m.holder !== S.pen.holder) send('sys', { t: 'state', pen: S.pen, hands: [...S.hands], rev: store.design.rev }, true, [from]); // tell the other claimant who won
            return;
          }
          const clash = conflict(m.seq);
          setPen(String(m.holder), m.seq, m);
          if (m.holder !== me && (!S.snapGot || clash)) askSnap(true);
        } else if (m.t === 'ask' && S.pen.holder === me) showAsk(from);
        else if (m.t === 'ack' && m.at0) stats.penRtt.push(now() - m.at0);
        return;
      case 'design':
        if (m.t !== 'op' || !m.op) return;
        if (from !== S.pen.holder) { stats.ignored++; return; } // only the pen holder's changes count
        { const t0 = now(), by = ROLES.includes(m.by) ? m.by : roleOf(from);
          const r = store.apply(m.op, { by, remote: true, gesture: m.g || null });
          const t1 = now(); stats.opApply.push(t1 - t0); if (m.at) stats.op.push(t1 - m.at);
          if (!r.ok || (typeof m.rev === 'number' && store.design.rev !== m.rev)) askSnap(); }
        return;
      case 'design-snap':
        if (m.t === 'ask' && S.pen.holder === me) send('design-snap', { t: 'snap', design: designer.getDesign(), at: now(), at0: m.at }, true, [from]);
        else if (m.t === 'snap' && m.design && from === S.pen.holder) {
          store.load(m.design); S.snapGot = true;
          stats.snap = { ms: m.at0 ? Math.round(now() - m.at0) : null, rev: m.design.rev, items: (m.design.items || []).length, bytes: JSON.stringify(m.design).length };
        }
        return;
      case 'view':
        if (m.t !== 'v' || from !== S.pen.holder || !m.v) return;
        S.lastViewMsg = m.v;
        if (S.following) { designer.setView(m.v); if (m.at) stats.view.push(now() - m.at); }
        return;
      case 'ptr': if (m.t === 'p' && isFinite(m.x) && isFinite(m.y)) gotPtr(from, m); return;
      case 'chat': if (m.t === 'm' && m.text) { S.chat.push({ who: (person(from) && person(from).name) || T.roles[roleOf(from)], text: String(m.text).slice(0, 300), from }); if (S.panel) paintPanel(); else say((person(from) && person(from).name || T.roles[roleOf(from)]) + ': ' + String(m.text).slice(0, 80)); } return;
      case 'hand': if (m.t === 'h') { if (m.up) { S.hands.add(from); say(T.handUp(nameOf(from))); } else S.hands.delete(from); paintTiles(); } return;
    }
  });
  let goneT = 0;
  tr.onParticipants(() => {
    if (!S.alive) return;
    paintTiles();
    for (const h of [...S.hands]) if (!S.people.has(h)) S.hands.delete(h);
    // the holder left without handing over: the rep (or else the first in order) takes the pen, and says so
    clearTimeout(goneT);
    if (S.pen.holder && !S.people.has(S.pen.holder)) goneT = setTimeout(() => {
      if (!S.alive || S.people.has(S.pen.holder)) return;
      const next = successor(S.pen.holder);
      if (next === me) { const seq = S.pen.seq + 1; setPen(me, seq); send('pen', { t: 'set', holder: me, seq, at: now() }); }
    }, 400);
  });
  tr.onSpeaking((ids) => { S.speaking = new Set(ids || []); for (const [id, el] of tiles) el.classList.toggle('ndc-speaking', S.speaking.has(id)); });
  tr.onQuality((id, q) => { S.quality[id] = q; const el = tiles.get(id); if (el) { const b = el.querySelector('.ndc-q'); b.className = 'ndc-q ndc-q-' + q; b.title = T.q[q] || ''; } });
  tr.onState((s) => {
    if (s === 'audio-blocked') { const b = document.createElement('button'); b.className = 'ndc-b ndc-go ndc-audio'; b.textContent = T.audio; b.onclick = () => { try { tr.startAudio && tr.startAudio(); } catch (e) { /* none */ } b.remove(); }; dock.appendChild(b); return; }
    S.state = s; paintCtl();
    if (s === 'connected' && S.wasReconnecting) { S.wasReconnecting = false; send('sys', { t: 'hello' }); }
    if (s === 'reconnecting') S.wasReconnecting = true;
    if (s === 'disconnected' && S.alive) say(T.lost);
  });

  /* ---------------- controls ---------------- */
  const coarse = typeof matchMedia !== 'undefined' && matchMedia('(pointer:coarse)').matches;
  $('flip').hidden = !coarse;
  $('share').hidden = coarse || !(navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia);
  $('mic').onclick = async () => { try { await tr.setMicrophone(!S.mic); } catch (e) { say(T.denied); } paintTiles(); };
  $('cam').onclick = async () => { try { await tr.setCamera(!S.cam); } catch (e) { say(T.denied); } paintTiles(); };
  $('flip').onclick = async () => { try { const f = await tr.switchCamera(); S.facing = f || (S.facing === 'user' ? 'environment' : 'user'); } catch (e) { say(T.denied); } paintTiles(); };
  $('share').onclick = async () => { try { await tr.shareScreen(!S.screen); } catch (e) { /* the person closed the browser's chooser */ } paintTiles(); };
  $('pen').onclick = () => { if (S.pen.holder === me) { S.panel = 'more'; paintPanel(); } else ask(); };
  $('follow').onclick = () => follow(true);
  $('more').onclick = () => { S.panel = S.panel ? null : 'more'; paintPanel(); layout(); };
  $('askgive').onclick = () => { if (S.askFrom) give(S.askFrom); hideAsk(); };
  $('askno').onclick = () => hideAsk();
  $('leave').onclick = () => leave();

  async function leave() {
    if (!S.alive) return;
    if (S.pen.holder === me) { const next = successor(me); if (next) { send('pen', { t: 'set', holder: next, seq: S.pen.seq + 1, at: now() }); } }
    if (S.hands.has(me)) send('hand', { t: 'h', up: false });
    S.alive = false;
    await new Promise((r) => setTimeout(r, 60)); // let the last messages leave
    try { await tr.disconnect(); } catch (e) { /* already gone */ }
    store.setGuard(null); offStore(); offs.forEach((f) => f()); timers.forEach((f) => f()); if (ro) ro.disconnect();
    clearTimeout(goneT); clearTimeout(toastT);
    dock.remove(); ptrLayer.remove(); audioBox.remove();
    if (root && prevStyle) { root.style.top = prevStyle.top; root.style.insetInlineEnd = prevStyle.end; }
    if (opts.onLeave) opts.onLeave(api);
  }

  const api = {
    stats, ready, el: dock,
    get pen() { return { ...S.pen, mine: S.pen.holder === me }; },
    get following() { return S.following; },
    get state() { return S.state; },
    get alive() { return S.alive; },
    participants: () => [...S.people.values()],
    give, ask, follow, leave, chat, hand, inviteLink,
    summary() {
      const r = (a) => (a == null ? null : Math.round(a * 10) / 10);
      return { op_p50: r(pct(stats.op, 50)), op_p95: r(pct(stats.op, 95)), op_n: stats.op.length, pen_p50: r(pct(stats.pen, 50)), pen_p95: r(pct(stats.pen, 95)), pen_n: stats.pen.length, view_p95: r(pct(stats.view, 95)), refused: stats.refused, ignored: stats.ignored, resync: stats.resync, snap: stats.snap };
    },
  };

  /* ---------------- connect ---------------- */
  S.state = 'connecting'; paintTiles();
  await tr.connect();
  if (opts.mic !== false) { try { await tr.setMicrophone(true); } catch (e) { say(T.denied); } }
  if (opts.camera !== false) { try { await tr.setCamera(true); } catch (e) { say(T.denied); } }
  paintTiles();
  send('sys', { t: 'hello' });
  // alone in the room: I hold the pen. Others present but silent (a slow phone): ask again, up to three times, then the
  // same rule everywhere picks one (the rep, else the smaller id); a later answer from a real holder still wins (see wins()).
  let tries = 0, settle = 0;
  const settleStep = () => {
    if (!S.alive) return;
    if (!S.pen.holder) {
      const alone = S.people.size <= 1;
      if (!alone && tries < 3) { tries++; send('sys', { t: 'hello' }); settle = setTimeout(settleStep, opts.settleMs || 900); return; }
      if (alone || successor(null) === me) { setPen(me, 1); send('pen', { t: 'set', holder: me, seq: 1, at: now() }); }
    }
    readyRes(api);
  };
  settle = setTimeout(settleStep, opts.settleMs || 900);
  timers.push(() => clearTimeout(settle));
  layout();
  return api;
}

/* ================================================================ LiveKit transport */

/** The production transport: livekit-client loaded from the CDN only now (after the join click), token from together.php. */
export function livekitTransport({ url, token, lib = LK_LIB, chunk = 14000 }) {
  let LK = null, room = null, facing = 'user';
  const L = { data: new Set(), parts: new Set(), quality: new Set(), speaking: new Set(), state: new Set() };
  const fire = (k, ...a) => L[k].forEach((f) => { try { f(...a); } catch (e) { /* a listener failed: the call goes on */ } });
  const audios = new Map(), parts = new Map();
  const enc = new TextEncoder(), dec = new TextDecoder();
  const roleOf = (p) => { try { const a = p.attributes && p.attributes.role; if (a) return a; return JSON.parse(p.metadata || '{}').role || 'buyer'; } catch (e) { return 'buyer'; } };
  // together.php's roles (rep, buyer, partner, friend, designer, engineer, lawyer) in the call's four groups
  const GROUP = { rep: 'rep', buyer: 'buyer', partner: 'family', friend: 'family', family: 'family', designer: 'designer', engineer: 'designer', lawyer: 'designer' };
  const view = (p, local) => ({
    id: p.identity, name: p.name || '', role: GROUP[roleOf(p)] || 'buyer', local,
    mic: !!p.isMicrophoneEnabled, cam: !!p.isCameraEnabled, screen: !!p.isScreenShareEnabled, quality: p.connectionQuality || 'unknown', speaking: !!p.isSpeaking,
  });
  const T = {
    kind: 'livekit',
    async connect() {
      fire('state', 'connecting');
      LK = await import(lib);
      const E = LK.RoomEvent;
      room = new LK.Room({
        adaptiveStream: true, dynacast: true,
        videoCaptureDefaults: { resolution: LK.VideoPresets.h540.resolution, facingMode: 'user' },
        publishDefaults: { simulcast: true, videoSimulcastLayers: [LK.VideoPresets.h180, LK.VideoPresets.h360] },
        audioCaptureDefaults: { echoCancellation: true, noiseSuppression: true, autoGainControl: true },
      });
      const people = () => fire('parts');
      room
        .on(E.ParticipantConnected, people).on(E.ParticipantDisconnected, people)
        .on(E.ParticipantMetadataChanged, people).on(E.ParticipantAttributesChanged, people)
        .on(E.TrackPublished, people).on(E.TrackUnpublished, people)
        .on(E.TrackSubscribed, (track, pub, p) => { if (track.kind === 'audio') { const el = track.attach(); el.hidden = true; document.body.appendChild(el); audios.set(track.sid, el); } people(); })
        .on(E.TrackUnsubscribed, (track) => { track.detach().forEach((el) => el.remove()); audios.delete(track.sid); people(); })
        .on(E.LocalTrackPublished, people).on(E.LocalTrackUnpublished, people).on(E.TrackMuted, people).on(E.TrackUnmuted, people)
        .on(E.ActiveSpeakersChanged, (sp) => fire('speaking', sp.map((p) => p.identity)))
        .on(E.ConnectionQualityChanged, (q, p) => fire('quality', p.identity, q))
        .on(E.Reconnecting, () => fire('state', 'reconnecting')).on(E.SignalReconnecting, () => fire('state', 'reconnecting'))
        .on(E.Reconnected, () => { fire('state', 'connected'); people(); })
        .on(E.Disconnected, () => fire('state', 'disconnected'))
        .on(E.AudioPlaybackStatusChanged, () => { if (!room.canPlaybackAudio) fire('state', 'audio-blocked'); })
        .on(E.DataReceived, (payload, p, kind, topic) => {
          let m; try { m = JSON.parse(dec.decode(payload)); } catch (e) { return; }
          const from = p ? p.identity : '';
          if (m && m.__c) { // a long message (the whole design) arrives in parts
            const k = from + ':' + m.__c, buf = parts.get(k) || { n: m.n, got: 0, s: [] };
            if (buf.s[m.i] == null) { buf.s[m.i] = m.d; buf.got++; }
            parts.set(k, buf);
            if (buf.got < buf.n) return;
            parts.delete(k); try { m = JSON.parse(buf.s.join('')); } catch (e) { return; }
          }
          fire('data', topic, m, from);
        });
      await room.connect(url, token);
      if (!room.canPlaybackAudio) fire('state', 'audio-blocked');
      fire('state', 'connected'); people();
    },
    async disconnect() { if (room) await room.disconnect(); audios.forEach((el) => el.remove()); audios.clear(); },
    publishData(topic, obj, o = {}) {
      if (!room) return false;
      const s = JSON.stringify(obj), opt = { reliable: !!o.reliable, topic };
      if (o.to) opt.destinationIdentities = o.to;
      if (!o.reliable || s.length <= chunk) { room.localParticipant.publishData(enc.encode(s), opt); return true; }
      const id = Math.random().toString(36).slice(2, 10), n = Math.ceil(s.length / chunk); // 15 KiB is the reliable limit: split
      for (let i = 0; i < n; i++) room.localParticipant.publishData(enc.encode(JSON.stringify({ __c: id, i, n, d: s.slice(i * chunk, (i + 1) * chunk) })), opt);
      return true;
    },
    onData: (f) => L.data.add(f),
    participants() { if (!room) return []; return [view(room.localParticipant, true), ...[...room.remoteParticipants.values()].map((p) => view(p, false))]; },
    onParticipants: (f) => L.parts.add(f),
    setMicrophone: (on) => room.localParticipant.setMicrophoneEnabled(!!on),
    setCamera: (on) => room.localParticipant.setCameraEnabled(!!on, { facingMode: facing }),
    async switchCamera() {
      const pub = room.localParticipant.getTrackPublication(LK.Track.Source.Camera);
      facing = facing === 'user' ? 'environment' : 'user';
      if (pub && pub.track) await pub.track.restartTrack({ facingMode: facing });
      fire('parts'); return facing;
    },
    shareScreen: (on) => room.localParticipant.setScreenShareEnabled(!!on, { audio: false }),
    attach(id, kind, el) {
      const p = id === room.localParticipant.identity ? room.localParticipant : room.remoteParticipants.get(id);
      const pub = p && p.getTrackPublication(kind === 'screen' ? LK.Track.Source.ScreenShare : LK.Track.Source.Camera);
      if (!pub || !pub.track) return false;
      pub.track.attach(el); return true;
    },
    startAudio: () => room && room.startAudio(),
    onQuality: (f) => L.quality.add(f), onSpeaking: (f) => L.speaking.add(f), onState: (f) => L.state.add(f),
    get room() { return room; },
  };
  return T;
}
