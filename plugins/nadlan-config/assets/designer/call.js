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
// Open mode (the studio's call, the default) draws the designed interface (joinOpen below, call-design.md): per-piece holds
// on the 'hold' topic {t:'on'|'off', k}, ordered design ops {k, q, live}, 'follow' {t:'on'|'off'}, laser strokes on 'ptr'
// {t:'l', s, p, end}, and 'sys' {t:'summon'|'end'} from the host (the first one in). Mic and camera start OFF.

const LK_LIB = 'https://cdn.jsdelivr.net/npm/livekit-client@2.22.3/dist/livekit-client.esm.mjs'; // the same build the TogetherRoom loads
const BASE = new URL('.', import.meta.url).href;
const now = () => performance.timeOrigin + performance.now(); // one clock across the tabs of one browser (the local checks)
const ROLES = ['buyer', 'rep', 'designer', 'family', 'host', 'guest'];
const OPEN_MS = 1500; // open mode: whoever changed something in the last 1.5 s keeps the turn; after that anyone may change
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const STR = {
  he: {
    dir: 'rtl',
    roles: { buyer: 'קונה', rep: 'נציג המכירות', designer: 'מעצב הפנים', family: 'משפחה', host: 'פתח/ה את השיחה', guest: 'מוזמן/ת' },
    editing: (n) => n + ' עורך/ת עכשיו', busy: (n) => n + ' עורך/ת עכשיו. אפשר לשנות בעוד רגע.',
    joined: (n) => n + ' הצטרף/ה לשיחה', left: (n) => n + ' יצא/ה מהשיחה. העיצוב נשאר אצלך.',
    inviteBtn: 'הזמנת משתתפים', inviteH: 'הזמנת משתתפים לשיחה', inviteSub: 'מי שפותח את הקישור מצטרף לשיחה ורואה את אותה דירה.',
    wa: 'שיתוף בוואטסאפ', waText: 'הצטרפו אליי לשיחת וידאו על הדירה:',
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
    more: 'עוד', moreLabel: 'עוד אפשרויות', leave: 'סיום שיחה', leaveLabel: 'סיום שיחה',
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
    roles: { buyer: 'Buyer', rep: 'Sales rep', designer: 'Interior designer', family: 'Family', host: 'Opened the call', guest: 'Invited' },
    editing: (n) => n + ' is editing now', busy: (n) => n + ' is editing now. You can change it in a moment.',
    joined: (n) => n + ' joined the call', left: (n) => n + ' left the call. The design stays with you.',
    inviteBtn: 'Invite people', inviteH: 'Invite people to the call', inviteSub: 'Whoever opens the link joins the call and sees the same apartment.',
    wa: 'Share on WhatsApp', waText: 'Join my video call about the apartment:',
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
    more: 'More', moreLabel: 'More options', leave: 'End call', leaveLabel: 'End call',
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
  invite: '<path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM2 21c0-4 3-7 7-7s7 3 7 7M19 8v6M16 11h6"/>',
  hand: '<path d="M8 13V5a1.5 1.5 0 0 1 3 0v6M11 11V4a1.5 1.5 0 0 1 3 0v7M14 11V5.5a1.5 1.5 0 0 1 3 0V14c0 4-3 7-6.5 7S5 18 4 15l-1.5-4a1.5 1.5 0 0 1 2.7-1.2L8 13"/>',
};
const svg = (k) => '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + ICON[k] + '</svg>';

function ensureCss(shadow) {
  if (shadow.querySelector('link[data-ndc-css]')) return Promise.resolve();
  const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = BASE + 'call.css?v=' + encodeURIComponent(new URL(import.meta.url).searchParams.get('v') || '2'); l.setAttribute('data-ndc-css', '');
  shadow.appendChild(l);
  return new Promise((r) => { l.addEventListener('load', r, { once: true }); l.addEventListener('error', r, { once: true }); setTimeout(r, 3000); });
}
const pct = (arr, p) => { if (!arr.length) return null; const s = [...arr].sort((a, b) => a - b); return s[Math.min(s.length - 1, Math.floor((p / 100) * s.length))]; };

/** Joins the call inside a mounted designer. Resolves once connected; the pen settles a moment later (call.ready). */
export async function joinCall(designer, opts = {}) {
  if (opts.mode !== 'pen') return joinOpen(designer, opts); // the open call (the studio's): the designed interface below
  const T = STR[opts.lang === 'en' ? 'en' : 'he'], tr = opts.transport, me = String(opts.identity), myRole = ROLES.includes(opts.role) ? opts.role : 'buyer';
  if (!tr) throw new Error('joinCall: a transport is required');
  // 'open' (the default since HAD-706 round 2): anyone changes the design at once, unless someone else changed something in the
  // last 1.5 s ("X is editing now"); everybody looks around on his own. 'pen': the older rule, one pen holder edits and presents.
  const OPEN = opts.mode !== 'pen';
  const store = designer.store, container = opts.container, shadow = container.getRootNode(), host = shadow.host || document.body;
  await ensureCss(shadow);
  const root = shadow.querySelector('.nd');
  const offs = [], timers = [];
  const on = (el, ev, fn, o) => { el.addEventListener(ev, fn, o); offs.push(() => el.removeEventListener(ev, fn, o)); };

  const S = {
    pen: { holder: null, seq: 0 }, people: new Map(), speaking: new Set(), quality: {}, hands: new Set(), following: true,
    ptrs: new Map(), chat: [], state: 'connecting', asked: 0, askFrom: null, snapAsked: 0, alive: true, mic: false, cam: false, screen: false,
    facing: 'user', panel: null, lastView: '', lastViewAt: 0, refusedAt: 0, joinedAt: now(),
    editor: null, editorAt: 0, snapFrom: null, names: new Map(),
  };
  const stats = { op: [], opApply: [], pen: [], penRtt: [], view: [], snap: null, refused: 0, ignored: 0, resync: 0, sent: { design: 0, view: 0, ptr: 0 } };
  let readyRes; const ready = new Promise((r) => (readyRes = r));

  const person = (id) => S.people.get(id) || null;
  const roleOf = (id) => { const p = person(id); return p && ROLES.includes(p.role) ? p.role : 'buyer'; };
  const nameOf = (id) => {
    if (id === me) return T.you; const p = person(id);
    if (!p) return S.names.get(id) || T.roles.buyer;
    if (OPEN) return p.name || T.roles[p.role] || T.roles.guest;
    const r = T.roles[p.role] || ''; return p.name ? p.name + (r ? ' (' + r + ')' : '') : r;
  };
  const send = (topic, obj, reliable = true, to) => { try { return tr.publishData(topic, { ...obj, from: me }, { reliable, to }); } catch (e) { return false; } };
  const editing = () => OPEN && S.editor && S.editor !== me && now() - S.editorAt < OPEN_MS && S.people.has(S.editor) ? S.editor : null;

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
    (OPEN ? '<button class="ndc-b ndc-pb ndc-inv" data-ndc="invite" aria-label="' + T.inviteBtn + '">' + svg('invite') + '<span>' + T.inviteBtn + '</span></button>'
      : '<button class="ndc-b ndc-pb" data-ndc="pen">' + svg('pen') + '<span data-ndc="pentext"></span></button>') +
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
      const stale = !v.srcObject || !(v.srcObject.getVideoTracks && v.srcObject.getVideoTracks().some((t) => t.readyState === 'live'));
      if (wantV && (el.dataset.v !== wantV || stale)) { try { if (tr.attach(p.id, wantV, v) !== false) el.dataset.v = wantV; } catch (e) { /* the track is not there yet */ } }
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
    $('conn').textContent = S.state === 'connected' ? '' : T[S.state] || '';
    if (OPEN) { // no pen, no presenter: one line says who is changing the design right now
      const ed = editing();
      $('penline').textContent = ed ? T.editing(nameOf(ed)) : '';
      $('follow').hidden = true; $('followline').hidden = true;
      if (S.panel) paintPanel();
      layout(); return;
    }
    const mine = S.pen.holder === me, pt = $('pentext'), pb = $('pen');
    pt.textContent = mine ? T.give : myRole === 'rep' ? T.take : T.ask;
    pb.classList.toggle('ndc-go', !mine && Date.now() - S.asked > 8000);
    pb.setAttribute('aria-label', pt.textContent);
    $('penline').textContent = !S.pen.holder ? '' : mine ? T.penMine : T.penOf(nameOf(S.pen.holder));
    const fl = $('followline'), fb = $('follow'), lead = S.pen.holder && S.pen.holder !== me;
    fb.hidden = !lead || S.following;
    if (lead) { fb.setAttribute('aria-label', T.back(nameOf(S.pen.holder))); fb.title = fb.getAttribute('aria-label'); }
    fl.hidden = !lead; fl.textContent = lead ? (S.following ? T.follow(nameOf(S.pen.holder)) : T.alone) : '';
    if (S.panel) paintPanel();
    layout();
  }

  /* ---------------- the pen ---------------- */
  const guard = OPEN
    ? () => { const ed = editing(); return ed ? { code: 'call.busy', reason: T.busy(nameOf(ed)) } : null; }
    : (op, meta) => (S.pen.holder === me ? null : { code: 'call.pen', reason: T.refuse(S.pen.holder ? nameOf(S.pen.holder) : T.roles.rep) });
  store.setGuard(guard);
  let edT = 0;
  function sawEdit(id) { // open mode: someone changed the design; the line clears itself when the 1.5 s turn is over
    S.editor = id; S.editorAt = now();
    if (id !== me) { paintCtl(); clearTimeout(edT); edT = setTimeout(() => { if (S.alive) paintCtl(); }, OPEN_MS + 50); }
  }
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
  function askSnap(force, from) {
    const src = from || S.pen.holder;
    if (!src || src === me || (!force && now() - S.snapAsked < 1500)) return;
    S.snapAsked = now(); S.snapFrom = src; stats.resync++;
    send('design-snap', { t: 'ask', at: S.snapAsked }, true, [src]);
  }
  const offStore = store.on((e) => {
    if (e.type === 'reject' && (e.code === 'call.pen' || e.code === 'call.busy')) {
      stats.refused++;
      if (Date.now() - S.refusedAt > 2000) {
        S.refusedAt = Date.now(); designer.toast(e.reason, 'stop');
        const b = $(OPEN ? 'penline' : 'pen'); b.classList.add('ndc-flash'); setTimeout(() => b.classList.remove('ndc-flash'), 1200);
      }
      return;
    }
    if (e.type !== 'change' || e.remote || !S.alive || (!OPEN && S.pen.holder !== me)) return;
    if (OPEN) sawEdit(me);
    stats.sent.design++;
    send('design', { t: 'op', op: e.op, g: e.gesture, rev: store.design.rev, by: OPEN ? 'buyer' : myRole, at: now() });
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
  function inviteLink() { // this page, the room, and only the page's own plain choices (which project page); never a name
    const u = new URL(opts.inviteBase || location.href), keep = new URLSearchParams();
    for (const k of ['project', 'pn', 'ul', 'unit']) { const v = u.searchParams.get(k); if (v) keep.set(k, v.slice(0, 80)); }
    keep.set('room', opts.room || '');
    if (opts.design) keep.set('design', opts.design);
    return u.origin + u.pathname + '?' + keep.toString();
  }
  const waLink = () => 'https://wa.me/?text=' + encodeURIComponent(T.waText + ' ' + inviteLink());
  async function copyLink(el) { const v = inviteLink(); try { await navigator.clipboard.writeText(v); } catch (e) { const i = el.querySelector('.ndc-link'); if (i) i.select(); try { document.execCommand('copy'); } catch (x) { /* none */ } } say(T.copied); }
  function paintPanel() {
    const el = $('panel'); el.hidden = !S.panel; $('more').setAttribute('aria-expanded', String(S.panel === 'more'));
    if (OPEN) $('invite').setAttribute('aria-expanded', String(S.panel === 'invite'));
    if (!S.panel) return;
    if (S.panel === 'invite') {
      el.innerHTML = '<h3>' + T.inviteH + '</h3><p class="ndc-sub">' + T.inviteSub + '</p>' +
        '<div class="ndc-row"><input class="ndc-link mono" readonly value="' + esc(inviteLink()) + '" aria-label="' + T.inviteH + '"><button class="ndc-b" data-ndc="copy">' + T.copy + '</button></div>' +
        '<a class="ndc-b ndc-go ndc-wa" data-ndc="wa" href="' + esc(waLink()) + '" target="_blank" rel="noopener">' + T.wa + '</a>' +
        '<p class="ndc-fine">' + T.noRec + '</p>';
      el.querySelector('[data-ndc="copy"]').onclick = () => copyLink(el);
      return;
    }
    const mine = S.pen.holder === me, canGive = !OPEN && (mine || myRole === 'rep');
    const ppl = [...S.people.values()].map((p) => '<li><span>' + esc(p.local ? T.youTag : p.name || T.roles[p.role]) + (OPEN ? '' : ' <small>' + esc(T.roles[p.role] || '') + '</small>') + '</span>' +
      (canGive && p.id !== S.pen.holder ? '<button class="ndc-b ndc-sm" data-give="' + esc(p.id) + '">' + svg('pen') + '<span>' + esc(T.giveTo(p.local ? T.you : p.name || T.roles[p.role])) + '</span></button>' : S.pen.holder === p.id ? '<b class="ndc-hold">' + svg('pen') + '</b>' : '') + '</li>').join('');
    const msgs = S.chat.slice(-30).map((m) => '<li><b>' + esc(m.who) + '</b> ' + esc(m.text) + '</li>').join('');
    el.innerHTML =
      '<div class="ndc-row"><button class="ndc-b ndc-wide" data-ndc="hand" aria-pressed="' + S.hands.has(me) + '">' + svg('hand') + '<span>' + (S.hands.has(me) ? T.handDown : T.hand) + '</span></button></div>' +
      '<h3>' + T.people + '</h3><ul class="ndc-ppl">' + ppl + '</ul>' +
      '<h3>' + T.chat + '</h3><ul class="ndc-msgs" data-ndc="msgs" aria-live="polite">' + msgs + '</ul>' +
      '<form class="ndc-form" data-ndc="form"><input data-ndc="chatin" maxlength="300" autocomplete="off" aria-label="' + T.chatPh + '" placeholder="' + T.chatPh + '"><button class="ndc-b ndc-go">' + T.send + '</button></form>' +
      '<h3>' + (OPEN ? T.inviteH : T.invite) + '</h3><div class="ndc-row"><input class="ndc-link mono" readonly value="' + esc(inviteLink()) + '" aria-label="' + T.invite + '"><button class="ndc-b" data-ndc="copy">' + T.copy + '</button></div>' +
      (OPEN ? '<a class="ndc-b ndc-go ndc-wa" href="' + esc(waLink()) + '" target="_blank" rel="noopener">' + T.wa + '</a>' : '') +
      '<p class="ndc-fine">' + T.noRec + '</p>';
    el.querySelector('[data-ndc="hand"]').onclick = () => hand(!S.hands.has(me));
    el.querySelectorAll('[data-give]').forEach((b) => (b.onclick = () => { give(b.dataset.give); }));
    el.querySelector('[data-ndc="form"]').onsubmit = (ev) => { ev.preventDefault(); const i = el.querySelector('[data-ndc="chatin"]'); chat(i.value); i.value = ''; };
    el.querySelector('[data-ndc="copy"]').onclick = () => copyLink(el);
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
    if (OPEN) {
      switch (topic) {
        case 'design':
          if (m.t !== 'op' || !m.op) return;
          { const t0 = now();
            sawEdit(from);
            const r = store.apply(m.op, { by: 'buyer', remote: true, gesture: m.g || null });
            const t1 = now(); stats.opApply.push(t1 - t0); if (m.at) stats.op.push(t1 - m.at);
            // two people changed at the very same moment: the one with the larger id takes the other's whole design
            if ((!r.ok || (typeof m.rev === 'number' && store.design.rev !== m.rev)) && String(me) > String(from)) askSnap(false, from); }
          return;
        case 'design-snap':
          if (m.t === 'ask') send('design-snap', { t: 'snap', design: designer.getDesign(), at: now(), at0: m.at }, true, [from]);
          else if (m.t === 'snap' && m.design && from === S.snapFrom) {
            store.load(m.design); S.snapGot = true; S.snapFrom = null;
            stats.snap = { ms: m.at0 ? Math.round(now() - m.at0) : null, rev: m.design.rev, items: (m.design.items || []).length, bytes: JSON.stringify(m.design).length };
          }
          return;
        case 'plan': // a newcomer asks for the apartment: the plan and the design go to him alone, on the data channel only
          if (m.t === 'ask' && opts.share) { const sh = opts.share() || {}; if (sh.plan) { stats.planSent = (stats.planSent || 0) + 1; send('plan', { t: 'plan', plan: sh.plan, title: sh.title || '', unitLabel: sh.unitLabel || '', mine: !!sh.mine, design: designer.getDesign(), at: now(), at0: m.at }, true, [from]); } }
          return;
        case 'ptr': if (m.t === 'p' && isFinite(m.x) && isFinite(m.y)) gotPtr(from, m); return;
        case 'chat': if (m.t === 'm' && m.text) { S.chat.push({ who: nameOf(from), text: String(m.text).slice(0, 300), from }); if (S.panel === 'more') paintPanel(); else say(nameOf(from) + ': ' + String(m.text).slice(0, 80)); } return;
        case 'hand': if (m.t === 'h') { if (m.up) { S.hands.add(from); say(T.handUp(nameOf(from))); } else S.hands.delete(from); paintTiles(); } return;
      }
      return;
    }
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
    const before = new Map([...S.people].map(([id, p]) => [id, p.name || '']));
    paintTiles();
    for (const h of [...S.hands]) if (!S.people.has(h)) S.hands.delete(h);
    if (OPEN && S.state === 'connected') { // say who came and who went; the design stays with everyone who is still here
      for (const [id, p] of S.people) { S.names.set(id, p.name || ''); if (!before.has(id) && before.size && id !== me) say(T.joined(p.name || T.roles.guest)); }
      for (const [id, n] of before) if (!S.people.has(id) && id !== me) { stats.left = (stats.left || 0) + 1; say(T.left(n || T.roles.guest)); }
      return;
    }
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
  if (OPEN) $('invite').onclick = () => { S.panel = S.panel === 'invite' ? null : 'invite'; paintPanel(); layout(); };
  else $('pen').onclick = () => { if (S.pen.holder === me) { S.panel = 'more'; paintPanel(); } else ask(); };
  $('follow').onclick = () => follow(true);
  $('more').onclick = () => { S.panel = S.panel === 'more' ? null : 'more'; paintPanel(); layout(); };
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
    clearTimeout(goneT); clearTimeout(toastT); clearTimeout(edT);
    dock.remove(); ptrLayer.remove(); audioBox.remove();
    if (root && prevStyle) { root.style.top = prevStyle.top; root.style.insetInlineEnd = prevStyle.end; }
    if (opts.onLeave) opts.onLeave(api);
  }

  const api = {
    stats, ready, el: dock,
    get pen() { return { ...S.pen, mine: S.pen.holder === me }; },
    get following() { return S.following; },
    get state() { return S.state; },
    get editor() { return editing(); },
    mode: OPEN ? 'open' : 'pen',
    get alive() { return S.alive; },
    participants: () => [...S.people.values()],
    give, ask, follow, leave, chat, hand, inviteLink, waLink,
    openPanel(k) { S.panel = k === 'invite' && OPEN ? 'invite' : k ? 'more' : null; paintPanel(); layout(); },
    summary() {
      const r = (a) => (a == null ? null : Math.round(a * 10) / 10);
      return { op_p50: r(pct(stats.op, 50)), op_p95: r(pct(stats.op, 95)), op_n: stats.op.length, pen_p50: r(pct(stats.pen, 50)), pen_p95: r(pct(stats.pen, 95)), pen_n: stats.pen.length, view_p95: r(pct(stats.view, 95)), refused: stats.refused, ignored: stats.ignored, resync: stats.resync, snap: stats.snap };
    },
  };

  /* ---------------- connect ---------------- */
  S.state = 'connecting'; paintTiles();
  await tr.connect(); // a transport the newcomer already connected (to receive the apartment) resolves at once
  S.state = 'connected';
  for (const p of tr.participants()) S.names.set(p.id, p.name || '');
  if (opts.mic !== false) { try { await tr.setMicrophone(true); } catch (e) { say(T.denied); } }
  if (opts.camera !== false) { try { await tr.setCamera(true); } catch (e) { say(T.denied); } }
  paintTiles();
  if (OPEN) { readyRes(api); layout(); return api; }
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

/* ================================================================ the open call: the designed interface (HAD-712 call design) */
// The look and the words follow docs/design-lab/apartment-designer/call-design/call-design.md and its boards 01-12.
// Ink #0F2233 behind video and model, paper for bars and sheets, blueprint blue for action and live state, red for leaving
// only, and one technical-pen colour per person (join order). The model never moves to make room for a face.
// What changed against the first open call: a touch on a piece of furniture HOLDS that piece only (two people move two
// different pieces at the same time), the hold shows in the holder's colour, and it lets go when the finger lifts or after
// 6 s without a sign of life. Live drag updates go lossy and the final position reliable, ordered per piece.

const PENS = ['#1F5FA8', '#1C7A4E', '#B0307A', '#0F7C8A', '#5B4BB7', '#46596A'];
const HOLD_MS = 6000, BEAT_MS = 2000, BACK_MS = 5000, HIDE_MS = 4000, SELF_MS = 10000, SUMMON_S = 3;
const EN_SKU = { sofa3: 'sofa', armchair: 'armchair', coffee: 'coffee table', dining6: 'dining table', chair: 'chair', tv: 'TV console', rug: 'rug', bed160: 'bed', bedset: 'bed', bedside: 'bedside table', bed120: 'bed', wardrobe: 'wardrobe', wardrobe2: 'wardrobe', desk: 'desk', lamp: 'lamp', kitchen: 'kitchen', island: 'island', plant: 'plant' };
const HE_FIX = { 'שידת': 'שידה', 'מנורת': 'מנורה' };

const UI = {
  he: {
    dir: 'rtl', product: 'שיחת וידאו על הדירה',
    sub: (n, m2, f) => [n ? 'דירת ' + n + ' חדרים' : '', m2 ? m2 + ' מ״ר' : '', f != null && f !== '' ? 'קומה ' + f : ''].filter(Boolean).join(' · '),
    mic: 'מיקרופון', muted: 'מושתק', micBlocked: 'חסום', cam: 'מצלמה', camOff: 'כבויה', camBlocked: 'חסומה',
    follow: 'מעקב', following: 'עוקבים', point: 'הצבעה', invite: 'הזמנה', more: 'עוד', leave: 'יציאה',
    tour: 'סיור', arrange: 'סידור', talk: 'שיחה', layouts: 'פריסה',
    followFrame: (n) => 'עוקבים אחרי ' + n + ' · הקישו לעצור', back: (n) => 'חזרה ל' + n,
    followOne: (n) => 'לעקוב אחרי ' + n, jumpOnce: 'לקפוץ אליה פעם אחת', bigPic: 'תמונה גדולה',
    holdChip: (n, o) => n + ' מזיז/ה את ' + o, holdRefused: (n, o) => n + ' מחזיק/ה את ' + o + '. נסו שוב בעוד רגע.',
    undoMine: 'בטל את שלי', undoOther: (n) => 'זה כבר שונה על ידי ' + n + ', אז לא ביטלנו.', undoNone: 'אין עוד שינוי שלך לבטל.',
    pill: (n, s) => n + ' בשיחה' + (s ? ' · ' + s + ' מדבר/ת' : ''),
    pointChip: (n) => n + ': כאן', pointHint: 'לחיצה ארוכה על התוכנית או על קיר מצביעה. הקו נעלם לבד.',
    summonBtn: 'כולם אליי', summonTitle: (n, r) => n + ' רוצה להראות לכולם את ' + r, summonSub: (s) => 'עוברים למבט שלו בעוד ' + s + ' שניות',
    summonGo: 'לעבור עכשיו', summonNo: 'לא עכשיו', theFlat: 'הדירה', viewers: (n) => n + ' צופים',
    controlsHint: 'הקישו על המסך כדי להחזיר את הכפתורים',
    listen: 'נכנסת כמאזין. שומעים ורואים הכול, ואפשר להצביע ולהזיז רהיטים.', permLink: 'איך לאשר מיקרופון',
    permTitle: 'לאשר מיקרופון בטלפון', iphone: 'אייפון', android: 'אנדרואיד',
    permIos: 'לוחצים על Aא בשורת הכתובת, הגדרות האתר, מיקרופון: לאפשר.', permAndroid: 'לוחצים על המנעול ליד הכתובת, הרשאות, מיקרופון: לאפשר.',
    permRetry: 'ניסיתי, לבדוק שוב', permListen: 'להמשיך כמאזין',
    inviteTitle: 'להזמין לשיחה', inviteSub: 'מי שמקבל את הקישור נכנס מהדפדפן, בלי הרשמה. הקישור עובד רק לשיחה הזאת.',
    wa: 'הזמנה בוואטסאפ', copy: 'העתקה', copied: 'הועתק', full: 'השיחה מלאה, 8 מתוך 8',
    inviteMsg: (h, n, f, url) => (h ? h + ' מזמין אותך' : 'הזמנה') + ' לשיחת וידאו על ' + (n ? 'דירת ' + n + ' חדרים' : 'הדירה') + (f != null && f !== '' ? ' בקומה ' + f : '') + '. רואים את הדירה ומעצבים יחד, בדפדפן, בלי הרשמה. ' + url,
    peopleTitle: 'בשיחה', followP: 'לעקוב', host: 'מארח', me: 'אני', you: 'אני',
    doing: { talk: 'מדבר/ת', listen: 'מאזין/ה, בלי מיקרופון', hold: (o) => 'מזיז/ה את ' + o },
    chat: 'הודעות', chatIn: 'כתבו הודעה', sendMsg: 'לשלוח', people: 'משתתפים',
    voice: 'קול בלבד', voiceSub: 'הווידאו נעצר, הדירה ממשיכה', flip: 'החלפת מצלמה', hideSelf: 'להסתיר את התמונה שלי', endAll: 'סיום לכולם',
    weak: 'החיבור חלש. עברנו לקול בלבד כדי שהשיחה תמשיך.', weakVideo: 'להחזיר וידאו',
    reconnect: 'מתחברים מחדש…', reconnectToast: 'הדירה ממשיכה לעבוד. השינויים שלכם יישלחו כשנחזור.', retry: 'להתחבר שוב', lost: 'השיחה נותקה.',
    audio: 'הקישו כדי לשמוע',
    battery: (p) => 'הסוללה ב־' + p + '%', batterySub: 'לעבור לקול בלבד? כך השיחה תחזיק יותר. הדירה ממשיכה לעבוד כרגיל.', batteryVoice: 'קול בלבד', batteryKeep: 'להמשיך עם וידאו',
    leaveTitle: 'לצאת מהשיחה?', leaveHostSub: 'אתם המארחים. אפשר לצאת ולתת לאחרים להמשיך, או לסיים לכולם.',
    leaveKeep: 'לצאת, השיחה ממשיכה', leaveKeepSub: (n) => n + ' יהיה/תהיה המארח/ת', leaveEnd: 'לסיים לכולם', cancel: 'ביטול',
    endTitle: 'השיחה הסתיימה. העיצוב שמור אצלכם.', before: 'לפני', after: 'אחרי', endShare: 'לשלוח את הסיכום בוואטסאפ', endAlone: 'להמשיך לעצב לבד',
    endFine: 'השיחה לא הוקלטה. נשמרו רק התוכנית, השינויים וההודעות.', endToast: 'השיחה הסתיימה. כל השינויים נשמרו בעיצוב שלכם.',
    endMeta: (t, len, n) => t + ' · ' + len + ' דק׳ · ' + n + ' משתתפים', noChanges: 'לא שונה דבר בשיחה.',
    chg: { 'item.move': 'הזזה', 'item.rot': 'סיבוב', 'item.add': 'הוספה', 'item.remove': 'הסרה', 'finish.set': 'ריצוף', 'wall.shift': 'הזזת קיר', 'partition.add': 'קיר חדש', 'partition.remove': 'הסרת קיר', 'partition.restore': 'קיר הוחזר', 'point.add': 'נקודה חדשה', 'point.move': 'הזזת נקודה', 'point.remove': 'הסרת נקודה', 'point.restore': 'נקודה הוחזרה', 'room.name': 'שם חדר' },
    endSummary: 'סיכום השיחה על הדירה:',
    modelKept: 'הדגם נשמר כמו שהוא', modelBack: 'חזרה לדגם', swap: 'להחליף בין התוכנית לתלת ממד',
    backToDesigner: 'חזרה למעצב, השיחה ממשיכה', backToCall: 'חזרה לשיחה', close: 'סגירה',
    joined: (n) => n + ' הצטרף/ה לשיחה', left: (n) => n + ' יצא/ה מהשיחה. העיצוב נשאר אצלך.', guest: 'אורח/ת',
    obj: { wall: 'הקיר', point: 'נקודת החשמל', floor: 'הריצוף', room: 'שם החדר', thing: 'הפריט' },
  },
  en: {
    dir: 'ltr', product: 'Video call about the apartment',
    sub: (n, m2, f) => [n ? n + '-room apartment' : '', m2 ? m2 + ' m²' : '', f != null && f !== '' ? 'floor ' + f : ''].filter(Boolean).join(' · '),
    mic: 'Mic', muted: 'Muted', micBlocked: 'Blocked', cam: 'Camera', camOff: 'Off', camBlocked: 'Blocked',
    follow: 'Follow', following: 'Following', point: 'Point', invite: 'Invite', more: 'More', leave: 'Leave',
    tour: 'Tour', arrange: 'Arrange', talk: 'Talk', layouts: 'Layout',
    followFrame: (n) => 'Following ' + n + ' · tap to stop', back: (n) => 'Back to ' + n,
    followOne: (n) => 'Follow ' + n, jumpOnce: 'Jump to her once', bigPic: 'Large picture',
    holdChip: (n, o) => n + ' is moving the ' + o, holdRefused: (n, o) => n + ' is holding the ' + o + '. Try again in a moment.',
    undoMine: 'Undo mine', undoOther: (n) => n + ' already changed it, so it was not undone.', undoNone: 'Nothing of yours left to undo.',
    pill: (n, s) => n + ' in the call' + (s ? ' · ' + s + ' speaking' : ''),
    pointChip: (n) => n + ': here', pointHint: 'Long-press the plan or a wall to point. The line fades by itself.',
    summonBtn: 'Everyone to me', summonTitle: (n, r) => n + ' wants to show everyone the ' + r, summonSub: (s) => 'Switching to his view in ' + s + ' seconds',
    summonGo: 'Go now', summonNo: 'Not now', theFlat: 'apartment', viewers: (n) => n + ' watching',
    controlsHint: 'Tap the screen to bring the buttons back',
    listen: 'You joined as a listener. You hear and see everything, and you can point and move furniture.', permLink: 'How to allow the microphone',
    permTitle: 'Allow the microphone on your phone', iphone: 'iPhone', android: 'Android',
    permIos: 'Tap Aa in the address bar, Website settings, Microphone: Allow.', permAndroid: 'Tap the lock next to the address, Permissions, Microphone: Allow.',
    permRetry: 'I tried, check again', permListen: 'Continue as a listener',
    inviteTitle: 'Invite to the call', inviteSub: 'Whoever gets the link joins from the browser, no sign-up. The link works for this call only.',
    wa: 'Invite on WhatsApp', copy: 'Copy', copied: 'Copied', full: 'The call is full, 8 of 8',
    inviteMsg: (h, n, f, url) => (h ? h + ' invites you' : 'You are invited') + ' to a video call about ' + (n ? 'a ' + n + '-room apartment' : 'the apartment') + (f != null && f !== '' ? ' on floor ' + f : '') + '. See the apartment and design together, in the browser, no sign-up. ' + url,
    peopleTitle: 'In the call', followP: 'Follow', host: 'Host', me: 'Me', you: 'Me',
    doing: { talk: 'speaking', listen: 'listening, no mic', hold: (o) => 'moving the ' + o },
    chat: 'Messages', chatIn: 'Write a message', sendMsg: 'Send', people: 'Participants',
    voice: 'Voice only', voiceSub: 'Video pauses, the apartment keeps working', flip: 'Switch camera', hideSelf: 'Hide my picture', endAll: 'End for everyone',
    weak: 'The connection is weak. We switched to voice only so the call continues.', weakVideo: 'Bring video back',
    reconnect: 'Reconnecting…', reconnectToast: 'The apartment keeps working. Your changes will be sent when we\'re back.', retry: 'Reconnect', lost: 'The call ended.',
    audio: 'Tap to hear',
    battery: (p) => 'Battery at ' + p + '%', batterySub: 'Switch to voice only? The call will last longer. The apartment keeps working as usual.', batteryVoice: 'Voice only', batteryKeep: 'Keep video',
    leaveTitle: 'Leave the call?', leaveHostSub: 'You\'re the host. You can leave and let the others continue, or end it for everyone.',
    leaveKeep: 'Leave, the call continues', leaveKeepSub: (n) => n + ' becomes the host', leaveEnd: 'End for everyone', cancel: 'Cancel',
    endTitle: 'The call has ended. Your design is saved.', before: 'Before', after: 'After', endShare: 'Send the summary on WhatsApp', endAlone: 'Keep designing on your own',
    endFine: 'The call was not recorded. Only the plan, the changes and the messages were saved.', endToast: 'The call has ended. All changes were saved to your design.',
    endMeta: (t, len, n) => t + ' · ' + len + ' min · ' + n + ' people', noChanges: 'Nothing was changed in the call.',
    chg: { 'item.move': 'Moved', 'item.rot': 'Turned', 'item.add': 'Added', 'item.remove': 'Removed', 'finish.set': 'Flooring', 'wall.shift': 'Wall moved', 'partition.add': 'New wall', 'partition.remove': 'Wall removed', 'partition.restore': 'Wall back', 'point.add': 'New point', 'point.move': 'Point moved', 'point.remove': 'Point removed', 'point.restore': 'Point back', 'room.name': 'Room name' },
    endSummary: 'Summary of the call about the apartment:',
    modelKept: 'The model is kept as it is', modelBack: 'Back to the model', swap: 'Swap the plan and the 3D',
    backToDesigner: 'Back to the designer, the call goes on', backToCall: 'Back to the call', close: 'Close',
    joined: (n) => n + ' joined the call', left: (n) => n + ' left the call. The design stays with you.', guest: 'Guest',
    obj: { wall: 'wall', point: 'electric point', floor: 'flooring', room: 'room name', thing: 'piece' },
  },
};

// our own line set: 24 px, 2 px stroke, square caps
const OI = {
  mic: '<path d="M12 3a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V6a3 3 0 0 1 3-3zM5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"/>',
  micOff: '<path d="M12 3a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V6a3 3 0 0 1 3-3zM5 11a7 7 0 0 0 14 0M12 18v3M9 21h6M3 3l18 18"/>',
  cam: '<path d="M3 7h12v10H3zM15 10.5l6-3.5v10l-6-3.5"/>',
  camOff: '<path d="M3 7h12v10H3zM15 10.5l6-3.5v10l-6-3.5M3 3l18 18"/>',
  eye: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><path d="M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z"/>',
  point: '<path d="M5 3l14 7-6 2-2 6z"/>',
  invite: '<path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM2 21c0-4 3-7 7-7s7 3 7 7M19 8v6M16 11h6"/>',
  more: '<path d="M4 11h3v3H4zM10.5 11h3v3h-3zM17 11h3v3h-3z" fill="currentColor"/>',
  leave: '<path d="M2 14c5-5 15-5 20 0l-3 3-3-2v-3c-2.5-1-5.5-1-8 0v3l-3 2z" fill="currentColor"/>',
  chev: '<path d="M9 5l7 7-7 7"/>',
  people: '<path d="M8 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM2 20c0-3.5 2.7-6 6-6s6 2.5 6 6M16 4a3.5 3.5 0 0 1 0 7M18 14c2.4.6 4 2.8 4 6"/>',
  swap: '<path d="M4 8h14l-3-3M20 16H6l3 3"/>',
  cube: '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9zM4 7.5l8 4.5 8-4.5M12 12v9"/>',
  grid: '<path d="M4 4h16v16H4zM4 12h16M12 4v16"/>',
  talk: '<path d="M8 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM16 20a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM10.5 9.5l3 5"/>',
  hand: '<path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V11M11 11V4a1.5 1.5 0 0 1 3 0v7M14 11V5.5a1.5 1.5 0 0 1 3 0V14c0 4-3 7-6.5 7S5 18 4 15l-1.5-4a1.5 1.5 0 0 1 2.7-1.2L8 13"/>',
  undo: '<path d="M9 6l-6 6 6 6M3 12h12a6 6 0 0 1 6 6"/>',
  chat: '<path d="M3 4h18v13H8l-5 4z"/>',
  voice: '<path d="M4 9h4l5-4v14l-5-4H4zM16 9c1.5 1.5 1.5 4.5 0 6M19 6c3 3 3 9 0 12"/>',
  flip: '<path d="M4 8h12l-3-3M20 16H8l3 3"/>',
  person: '<path d="M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
  x: '<path d="M6 6l12 12M18 6L6 18"/>',
  check: '<path d="M4 12l5 5L20 6"/>',
  signal: '<path d="M4 20v-3M9 20v-7M14 20V9M19 20V4"/>',
  battery: '<path d="M3 8h15v8H3zM20 11v2" /><path d="M5 10h3v4H5z" fill="currentColor"/>',
  send: '<path d="M15 6l-6 6 6 6"/>',
  copy: '<path d="M8 8h12v12H8zM4 16V4h12"/>',
};
const oi = (k, s = 24) => '<svg aria-hidden="true" width="' + s + '" height="' + s + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter">' + OI[k] + '</svg>';

const keyOf = (op) => {
  switch (op && op.op) {
    case 'item.add': return 'i:' + (op.item && op.item.id);
    case 'item.move': case 'item.rot': case 'item.remove': return 'i:' + op.id;
    case 'wall.shift': case 'partition.remove': case 'partition.restore': return 'w:' + op.id;
    case 'partition.add': return 'w:' + (op.wall && op.wall.id);
    case 'point.add': return 'p:' + (op.point && op.point.id);
    case 'point.move': case 'point.remove': case 'point.restore': return 'p:' + op.id;
    case 'finish.set': return 'f:' + op.key;
    case 'room.name': return 'r:' + (op.at || []).join(',');
    default: return 'x:' + (op && op.op);
  }
};

async function joinOpen(designer, opts) {
  const lang = opts.lang === 'en' ? 'en' : 'he', T = UI[lang], tr = opts.transport, me = String(opts.identity);
  if (!tr) throw new Error('joinCall: a transport is required');
  const store = designer.store, container = opts.container, shadow = container.getRootNode(), host = shadow.host || document.body;
  await ensureCss(shadow);
  let CAT = null; import('./catalog.js').then((m) => (CAT = m)).catch(() => {});
  const root = shadow.querySelector('.nd');
  const offs = [], timers = [];
  const on = (el, ev, fn, o) => { if (!el) return; el.addEventListener(ev, fn, o); offs.push(() => el.removeEventListener(ev, fn, o)); };
  const every = (fn, ms) => { const t = setInterval(fn, ms); timers.push(() => clearInterval(t)); return t; };
  const reduce = typeof matchMedia !== 'undefined' && matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarse = typeof matchMedia !== 'undefined' && matchMedia('(pointer:coarse)').matches;

  const S = {
    people: new Map(), seen: new Map(), pen: new Map(), speaking: new Set(), quality: {}, poorSince: 0,
    state: 'connecting', alive: true, mic: false, cam: false, micBlocked: !!(opts.blocked && opts.blocked.mic), camBlocked: !!(opts.blocked && opts.blocked.cam),
    facing: 'user', lay: 'a', swapped: false, pinned: false, auto: false, backT: 0, sheet: null, sheetArg: null, chat: [], unread: 0, names: new Map(),
    holds: new Map(), mine: new Set(), lastSeq: new Map(), seq: 0, lastOp: new Map(), lastMover: new Map(), down: false, beat: 0, refusedAt: 0,
    following: null, lostFollow: null, followers: new Set(), views: new Map(), target: null, lastView: '', lastViewAt: 0,
    voice: false, voiceAuto: false, camBefore: false, hideSelf: false, selfOpenAt: Date.now(), selfCorner: 'top-end', barHidden: false, hinted: false, lastTouch: Date.now(),
    lasers: new Map(), pointMode: false, queue: [], recAt: 0, startedAt: Date.now(), changes: [], min: false, wasRe: false, peek: 0,
    summon: null, battAsked: false, banner: null, sideTab: 'people', undoAt: 0, snapFrom: null, joinedAt: now(),
  };
  const stats = { op: [], opApply: [], view: [], snap: null, refused: 0, ignored: 0, resync: 0, sent: { design: 0, view: 0, ptr: 0 }, left: 0 };
  let readyRes; const ready = new Promise((r) => (readyRes = r));

  const person = (id) => S.people.get(id) || null;
  const joinedTs = new Map();
  const rank = (p) => (p && typeof p.joined === 'number' && p.joined > 0 ? p.joined : joinedTs.has(p.id) ? joinedTs.get(p.id) : 1e15 + (S.seen.get(p.id) || 0));
  const sorted = () => [...S.people.values()].sort((a, b) => rank(a) - rank(b) || (a.id < b.id ? -1 : 1));
  const hostId = () => { const s = sorted(); return s.length ? s[0].id : me; };
  const isHost = () => hostId() === me;
  const nameOf = (id) => { if (id === me) return T.me; const p = person(id); return (p && p.name) || S.names.get(id) || T.guest; };
  const penOf = (id) => { const i = S.pen.has(id) ? S.pen.get(id) : 0; return PENS[i % PENS.length]; };
  const dashed = (id) => (S.pen.get(id) || 0) >= PENS.length;
  const send = (topic, obj, reliable = true, to) => { try { return tr.publishData(topic, { ...obj, from: me }, { reliable, to }); } catch (e) { return false; } };
  const objName = (key) => {
    const [k, id] = [key.slice(0, 1), key.slice(2)];
    if (k === 'i') {
      const it = store.item(id), c = it && CAT && CAT.ITEMS[it.sku];
      if (!c) return T.obj.thing;
      if (lang === 'en') return EN_SKU[String(it.sku).replace(/^gen\./, '')] || T.obj.thing;
      if (it.sku === 'gen.kitchen') return 'ארונות המטבח';
      const w = c.he.split(' ')[0]; return 'ה' + (HE_FIX[w] || w);
    }
    return k === 'w' ? T.obj.wall : k === 'p' ? T.obj.point : k === 'f' ? T.obj.floor : k === 'r' ? T.obj.room : T.obj.thing;
  };

  /* ---------------- the frame: header, stage layer, bar, sheets, side panel ---------------- */
  const ui = document.createElement('section');
  ui.className = 'ndo'; ui.dir = T.dir; ui.lang = lang; ui.dataset.lay = 'a';
  ui.setAttribute('aria-label', T.product);
  const seg = (cls) => '<div class="ndo-seg ' + cls + '" role="group" aria-label="' + T.layouts + '">' +
    [['a', 'cube', T.tour], ['b', 'grid', T.arrange], ['c', 'talk', T.talk]].map(([k, ic, l]) => '<button type="button" data-lay="' + k + '" aria-pressed="false">' + oi(ic, 18) + '<span>' + l + '</span></button>').join('') + '</div>';
  const barBtn = (k, ic, label) => '<button type="button" class="ndo-b" data-ndc="' + k + '"><span class="ndo-ic">' + oi(ic) + '</span><span class="ndo-lb">' + label + '</span></button>';
  ui.innerHTML =
    '<header class="ndo-head"><button type="button" class="ndo-hb" data-ndc="back" aria-label="' + T.backToDesigner + '" title="' + T.backToDesigner + '">' + oi('chev', 22) + '</button>' +
    '<div class="ndo-ttl"><h2>' + T.product + '</h2><p data-ndc="sub"></p></div>' + seg('ndo-seg-head') +
    '<div class="ndo-live" role="status"><i class="ndo-sq"></i><span class="ndo-mono" data-ndc="timer">00:00</span><span class="ndo-cnt">' + oi('people', 16) + '<b class="ndo-mono" data-ndc="count">1</b></span></div></header>' +
    '<div class="ndo-stage" data-ndc="stage">' +
    '<div class="ndo-frame" data-ndc="frame" hidden></div>' +
    '<div class="ndo-faces" data-ndc="faces" role="list"></div><div class="ndo-selfbox" data-ndc="selfbox"></div>' +
    '<button type="button" class="ndo-pill" data-ndc="pill" hidden><span class="ndo-minis" data-ndc="minis"></span><span data-ndc="pilltext"></span></button>' +
    seg('ndo-seg-stage') +
    '<button type="button" class="ndo-swap" data-ndc="swap" aria-label="' + T.swap + '" title="' + T.swap + '" hidden>' + oi('swap', 20) + '</button>' +
    '<div class="ndo-talkm" data-ndc="talkm" hidden><span>' + T.modelKept + '</span><button type="button" class="ndo-btn ndo-sec" data-ndc="modelback">' + oi('cube', 18) + '<span>' + T.modelBack + '</span></button></div>' +
    '<button type="button" class="ndo-tab" data-ndc="followtab" hidden></button>' +
    '<button type="button" class="ndo-chip ndo-chip-o" data-ndc="backchip" hidden></button>' +
    '<button type="button" class="ndo-undo" data-ndc="undo" hidden>' + oi('undo', 18) + '<span>' + T.undoMine + '</span></button>' +
    '<div class="ndo-banners" data-ndc="banners"></div>' +
    '<div class="ndo-toasts"><div class="ndo-toast" data-ndc="toast" role="status" hidden></div></div>' +
    '</div>' +
    '<div class="ndo-ov" data-ndc="ov" aria-hidden="true"><svg class="ndo-ovs" data-ndc="ovs"></svg></div>' +
    '<nav class="ndo-bar" data-ndc="bar" role="toolbar" aria-label="' + T.product + '"><div class="ndo-bar-in">' +
    barBtn('mic', 'micOff', T.muted) + barBtn('cam', 'camOff', T.camOff) + '<i class="ndo-gap ndo-gap-desk"></i>' + barBtn('follow', 'eye', T.follow) + barBtn('point', 'point', T.point) + barBtn('invite', 'invite', T.invite) + barBtn('more', 'more', T.more) +
    '<i class="ndo-rule"></i><button type="button" class="ndo-b ndo-leave" data-ndc="leave" aria-label="' + T.leave + '"><span class="ndo-ic">' + oi('leave') + '</span><span class="ndo-lb">' + T.leave + '</span></button></div></nav>' +
    '<aside class="ndo-side" data-ndc="side" hidden><div class="ndo-tabs" role="tablist"><button type="button" role="tab" data-side="people"></button><button type="button" role="tab" data-side="chat"></button></div><div class="ndo-sidebody" data-ndc="sidebody"></div></aside>' +
    '<button type="button" class="ndo-mini" data-ndc="mini" hidden>' + oi('people', 18) + '<span>' + T.backToCall + '</span></button>' +
    '<div class="ndo-scrim" data-ndc="scrim" hidden></div><div class="ndo-sheet" data-ndc="sheet" role="dialog" aria-modal="true" hidden></div>';
  container.appendChild(ui);
  const $ = (k) => ui.querySelector('[data-ndc="' + k + '"]');
  const audioBox = document.createElement('div'); audioBox.hidden = true; container.appendChild(audioBox);
  const spaceEl = shadow.querySelector('[data-nd="space"]'), planHost = shadow.querySelector('[data-nd="plan"]'), navEl = root && root.querySelector(':scope > nav');
  const planEl = () => shadow.querySelector('.nd-plan');
  const beforeSvg = (() => { const s = planEl(); return s ? s.cloneNode(true) : null; })();

  let toastT = 0;
  function say(msg, o = {}) {
    const t = $('toast'); t.className = 'ndo-toast' + (o.dark ? ' ndo-dark' : '');
    t.innerHTML = (o.icon ? oi(o.icon, 18) : '') + '<span></span>' + (o.link ? '<button type="button" class="ndo-link">' + esc(o.link) + '</button>' : '');
    t.querySelector('span').textContent = msg;
    if (o.link) t.querySelector('.ndo-link').onclick = (ev) => { ev.stopPropagation(); t.hidden = true; o.onLink && o.onLink(); };
    t.hidden = false; clearTimeout(toastT); toastT = setTimeout(() => (t.hidden = true), o.ms || 3400);
  }

  /* ---------------- where everything sits ---------------- */
  const prev = root ? { top: root.style.top, bottom: root.style.bottom, end: root.style.insetInlineEnd } : null;
  if (root) root.classList.add('ndc-in');
  // the surface behind the 3D turns ink for the call (call-design.md, --ink) and returns to the designer's own on leaving
  const stageInk = (c) => { try { const sp = designer.space; if (sp && sp.setStage) sp.setStage(c); } catch (e) { /* the view is gone */ } };
  if (designer.ready3d && designer.ready3d.then) designer.ready3d.then(() => { if (S.alive) stageInk(0x0F2233); }, () => {}); else stageInk(0x0F2233);
  const wide = () => host.clientWidth >= 900 && innerWidth >= 900;
  function layout() {
    if (!S.alive) return;
    const W = wide();
    ui.classList.toggle('ndo-wide', W); ui.classList.toggle('ndo-min', S.min); ui.classList.toggle('ndo-barhid', S.barHidden && !W);
    ui.dataset.lay = S.lay; ui.classList.toggle('ndo-swapped', S.swapped);
    $('side').hidden = !W || S.min; $('mini').hidden = !S.min;
    if (!root) return;
    root.classList.toggle('ndc-lay-a', !S.min && S.lay === 'a' && !W); root.classList.toggle('ndc-lay-b', !S.min && S.lay === 'b' && !W);
    root.classList.toggle('ndc-lay-c', !S.min && S.lay === 'c' && !W); root.classList.toggle('ndc-swapped', !S.min && S.swapped && S.lay === 'b' && !W);
    root.classList.toggle('ndc-wide', !S.min && W); root.classList.toggle('ndc-in', !S.min && !W);
    if (S.min) { root.style.top = prev.top; root.style.bottom = prev.bottom; root.style.insetInlineEnd = prev.end; return; }
    if (W) {
      const strip = S.lay === 'c' ? Math.round((host.clientHeight - 136) * 0.45) : 120;
      ui.style.setProperty('--strip', strip + 'px');
      root.style.top = 56 + strip + 'px'; root.style.bottom = '80px'; root.style.insetInlineEnd = '340px';
    } else {
      const bar = S.barHidden ? 'env(safe-area-inset-bottom, 0px)' : 'calc(76px + env(safe-area-inset-bottom, 0px))';
      const stageH = host.clientHeight - 56 - 76, facesH = Math.max(200, Math.round(stageH * 0.6));
      ui.style.setProperty('--facesh', facesH + 'px');
      root.style.top = (S.lay === 'c' ? 56 + facesH : 56) + 'px'; root.style.bottom = bar; root.style.insetInlineEnd = '';
    }
    paintSeg();
  }
  const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(() => layout()) : null;
  if (ro) ro.observe(host);
  function paintSeg() { ui.querySelectorAll('.ndo-seg button').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.lay === S.lay))); $('swap').hidden = S.lay !== 'b' || wide() || S.min; $('talkm').hidden = S.lay !== 'c' || S.min; }
  function setLay(k, how) { // how: 'hand' (the person chose), 'auto'
    if (!['a', 'b', 'c'].includes(k)) return;
    if (how === 'hand') { S.pinned = k !== 'a'; S.auto = false; } else S.auto = k === 'b';
    if (k !== 'b' || how === 'hand') S.swapped = false;
    if (S.lay === k && how !== 'hand') return;
    const was = S.lay; S.lay = k;
    placeSelf(); layout(); paintFaces();
    if (was !== k) designer.space && requestAnimationFrame(() => ovLoop());
  }
  function autoArrange(from3d) { // a touch on furniture: the plan comes forward (or the 3D stays big when the touch was in it)
    clearTimeout(S.backT);
    if (wide() || S.lay === 'c' || (S.pinned && S.lay !== 'a')) return;
    if (S.lay !== 'b') { S.swapped = !!from3d; setLay('b', 'auto'); }
  }
  function maybeBack() { // 5 s after the last piece was put down, back to the tour
    clearTimeout(S.backT);
    if (!S.auto || S.lay !== 'b') return;
    S.backT = setTimeout(() => { if (!S.alive || S.down || liveHolds().length || S.lay !== 'b' || !S.auto) return; setLay('a', 'auto'); }, BACK_MS);
  }

  /* ---------------- the faces ---------------- */
  const faces = new Map();
  function faceEl(p) {
    let el = faces.get(p.id);
    if (el) return el;
    el = document.createElement('div'); el.className = 'ndo-face' + (p.local ? ' ndo-me' : ''); el.dataset.id = p.id; el.setAttribute('role', 'listitem'); el.tabIndex = 0;
    el.innerHTML = '<span class="ndo-disc"><video playsinline autoplay muted></video><b class="ndo-ini"></b></span><span class="ndo-stamp"><b></b></span>' +
      '<i class="ndo-bmute">' + oi('micOff', 12) + '</i><i class="ndo-bq">' + oi('signal', 12) + '</i><i class="ndo-thost">' + T.host + '</i><i class="ndo-tview"></i>' +
      (p.local ? '<span class="ndo-mepill">' + T.me + '</span>' : '');
    faces.set(p.id, el);
    let lp = 0, moved = false, sx = 0, sy = 0;
    el.addEventListener('pointerdown', (ev) => { moved = false; sx = ev.clientX; sy = ev.clientY; clearTimeout(lp); lp = setTimeout(() => { lp = 0; if (!moved && !p.local) bigPicture(p.id); }, 550); if (p.local && !wide()) dragSelf(ev); });
    el.addEventListener('pointermove', (ev) => { if (Math.hypot(ev.clientX - sx, ev.clientY - sy) > 8) { moved = true; clearTimeout(lp); } });
    el.addEventListener('pointerup', () => { if (lp) { clearTimeout(lp); lp = 0; if (moved) return; if (p.local) { S.selfOpenAt = Date.now(); paintFaces(); } else openSheet('face', p.id); } });
    el.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); if (!p.local) openSheet('face', p.id); } });
    return el;
  }
  function placeSelf() { // in the tour my own picture is a small disc of its own; everywhere else it sits with the others
    const mine = faces.get(me); if (!mine) return;
    const want = S.lay === 'a' && !wide() ? $('selfbox') : $('faces');
    if (mine.parentNode !== want) { if (want === $('faces')) want.insertBefore(mine, want.firstChild && [...want.children].find((c) => rankOf(c.dataset.id) > rankOf(me)) || null); else want.appendChild(mine); const v = mine.querySelector('video'); if (v && v.srcObject) { const pr = v.play(); if (pr && pr.catch) pr.catch(() => {}); } }
  }
  const rankOf = (id) => { const p = person(id); return p ? rank(p) : 0; };
  function paintFaces() {
    const list = sorted(), box = $('faces');
    for (const [id, el] of faces) if (!S.people.has(id)) { el.remove(); faces.delete(id); }
    let idx = 0;
    for (const p of list) {
      const el = faceEl(p);
      if (!p.local || !(S.lay === 'a' && !wide())) { if (el.parentNode !== box || box.children[idx] !== el) box.insertBefore(el, box.children[idx] || null); idx++; }
      else if (el.parentNode !== $('selfbox')) $('selfbox').appendChild(el);
      el.style.setProperty('--pen', penOf(p.id)); el.classList.toggle('ndo-dash', dashed(p.id));
      const v = el.querySelector('video'), wantV = !S.voice && (p.screen ? 'screen' : p.cam ? 'video' : '');
      const stale = !v.srcObject || !(v.srcObject.getVideoTracks && v.srcObject.getVideoTracks().some((t) => t.readyState === 'live'));
      if (wantV && (el.dataset.v !== wantV || stale)) { try { if (tr.attach(p.id, wantV, v) !== false) el.dataset.v = wantV; } catch (e) { /* the track is not there yet */ } }
      if (!wantV) { el.dataset.v = ''; v.removeAttribute('src'); v.srcObject = null; }
      el.classList.toggle('ndo-hasv', !!wantV);
      el.classList.toggle('ndo-mirror', !!(p.local && p.cam && !p.screen && S.facing === 'user'));
      el.querySelector('.ndo-ini').textContent = ((p.local ? p.name : p.name) || nameOf(p.id) || '?').trim().charAt(0);
      el.querySelector('.ndo-stamp b').textContent = p.local ? T.me : nameOf(p.id);
      el.classList.toggle('ndo-muted', !p.mic);
      const q = S.quality[p.id] || p.quality || 'unknown';
      el.classList.toggle('ndo-poor', q === 'poor' || q === 'lost');
      el.classList.toggle('ndo-host', p.id === hostId() && S.people.size > 1);
      el.classList.toggle('ndo-speaking', S.speaking.has(p.id));
      el.classList.toggle('ndo-re', S.state === 'reconnecting');
      el.classList.toggle('ndo-hide', !!(p.local && S.hideSelf));
      el.classList.toggle('ndo-collapsed', !!(p.local && S.lay === 'a' && !wide() && Date.now() - S.selfOpenAt > SELF_MS));
      el.classList.toggle('ndo-led', S.following === p.id);
      const vw = p.local ? S.followers.size : (S.views.get(p.id) && S.views.get(p.id).n) || 0;
      el.querySelector('.ndo-tview').textContent = vw ? T.viewers(vw) : ''; el.classList.toggle('ndo-viewed', !!vw);
      el.setAttribute('aria-label', (p.local ? T.me : nameOf(p.id)) + (p.mic ? '' : ' · ' + T.muted) + (S.speaking.has(p.id) ? ' · ' + T.doing.talk : ''));
    }
    $('selfbox').dataset.corner = S.selfCorner;
    // the pill of the arrange layout: little faces and who speaks
    const spk = list.find((p) => S.speaking.has(p.id) && !p.local);
    $('pilltext').textContent = T.pill(list.length, spk ? nameOf(spk.id) : '');
    $('minis').innerHTML = list.slice(0, 4).map((p) => '<i style="--pen:' + penOf(p.id) + '">' + esc(((p.name || nameOf(p.id)) || '?').trim().charAt(0)) + '</i>').join('');
    $('pill').hidden = !(S.lay === 'b' && !wide()) || S.min;
    ui.classList.toggle('ndo-peek', Date.now() < S.peek);
    ui.classList.toggle('ndo-voice', S.voice);
    ui.dataset.n = String(list.length);
  }
  function dragSelf(ev) { // my own disc goes to any corner of the stage
    const box = $('selfbox'), st = $('stage').getBoundingClientRect(); let moved = false;
    const mv = (e) => { if (Math.hypot(e.clientX - ev.clientX, e.clientY - ev.clientY) < 10 && !moved) return; moved = true; box.style.transform = 'translate(' + (e.clientX - ev.clientX) + 'px,' + (e.clientY - ev.clientY) + 'px)'; };
    const up = (e) => {
      removeEventListener('pointermove', mv, true); removeEventListener('pointerup', up, true); box.style.transform = '';
      if (!moved) return;
      const top = e.clientY < st.top + st.height / 2, left = e.clientX < st.left + st.width / 2, startIsLeft = T.dir === 'rtl' ? false : true;
      S.selfCorner = (top ? 'top' : 'bottom') + '-' + (left === startIsLeft ? 'start' : 'end'); paintFaces();
    };
    addEventListener('pointermove', mv, true); addEventListener('pointerup', up, true);
  }
  function bigPicture(id) { // five seconds of one face, large
    const el = faces.get(id); if (!el) return;
    el.classList.add('ndo-big'); setTimeout(() => el.classList.remove('ndo-big'), 5000);
  }

  /* ---------------- header, bar ---------------- */
  function paintHead() {
    const a = store.apt || {}, u = a.unit || {};
    let m2 = ''; try { m2 = designer.quantities().net.toFixed(0); } catch (e) { m2 = ''; }
    $('sub').textContent = T.sub(u.rooms, m2, u.floor);
    $('count').textContent = String(S.people.size || 1);
  }
  every(() => { const s = Math.floor((Date.now() - S.startedAt) / 1000), h = Math.floor(s / 3600), mm = Math.floor((s % 3600) / 60), ss = s % 60; $('timer').textContent = (h ? h + ':' + String(mm).padStart(2, '0') : String(mm).padStart(2, '0')) + ':' + String(ss).padStart(2, '0'); }, 1000);
  function paintBar() {
    const lp = S.people.get(me) || {};
    S.mic = !!lp.mic; S.cam = !!lp.cam;
    const set = (k, ic, label, state) => { const b = $(k); b.querySelector('.ndo-ic').innerHTML = oi(ic); b.querySelector('.ndo-lb').textContent = label; b.dataset.state = state || ''; b.setAttribute('aria-label', label); };
    set('mic', S.mic ? 'mic' : 'micOff', S.micBlocked ? T.micBlocked : S.mic ? T.mic : T.muted, S.micBlocked ? 'blocked' : S.mic ? '' : 'off');
    $('mic').setAttribute('aria-pressed', String(!S.mic));
    if (!$('mic').querySelector('.ndo-lv')) $('mic').insertAdjacentHTML('beforeend', '<span class="ndo-lv"><i></i></span>');
    set('cam', S.cam ? 'cam' : 'camOff', S.camBlocked ? T.camBlocked : S.cam ? T.cam : T.camOff, S.camBlocked ? 'blocked' : S.cam ? '' : 'off');
    $('cam').setAttribute('aria-pressed', String(!S.cam));
    set('follow', 'eye', S.following ? T.following : T.follow, S.following ? 'on' : '');
    $('follow').setAttribute('aria-pressed', String(!!S.following));
    set('point', 'point', T.point, S.pointMode ? 'on' : ''); $('point').setAttribute('aria-pressed', String(S.pointMode));
    set('more', 'more', T.more, S.sheet === 'more' ? 'on' : '');
    const mb = $('more'); let c = mb.querySelector('.ndo-count'); if (S.unread) { if (!c) { c = document.createElement('b'); c.className = 'ndo-count ndo-mono'; mb.appendChild(c); } c.textContent = String(S.unread); } else if (c) c.remove();
    $('invite').dataset.state = S.sheet === 'invite' ? 'on' : '';
    $('invite').setAttribute('aria-expanded', String(S.sheet === 'invite'));
    paintHead(); paintFollow();
  }
  function paintFollow() {
    const f = S.following, tab = $('followtab'), chip = $('backchip'), fr = $('frame');
    fr.hidden = !f; tab.hidden = !f;
    if (f) { const c = penOf(f); fr.style.setProperty('--pen', c); tab.style.setProperty('--pen', c); tab.textContent = T.followFrame(nameOf(f)); }
    const lost = !f && S.lostFollow && S.people.has(S.lostFollow);
    chip.hidden = !lost;
    if (lost) { chip.style.setProperty('--pen', penOf(S.lostFollow)); chip.innerHTML = '<i class="ndo-mini-face" style="--pen:' + penOf(S.lostFollow) + '">' + esc(nameOf(S.lostFollow).charAt(0)) + '</i><span>' + esc(T.back(nameOf(S.lostFollow))) + '</span>'; }
  }

  /* ---------------- sheets ---------------- */
  function closeSheet() { S.sheet = null; S.sheetArg = null; $('sheet').hidden = true; $('scrim').hidden = true; $('sheet').innerHTML = ''; paintBar(); }
  function openSheet(kind, arg) {
    if (S.sheet === kind && arg === S.sheetArg && kind !== 'summon') { closeSheet(); return; }
    if (wide() && (kind === 'people' || kind === 'chat')) { S.sideTab = kind; paintSide(); closeSheet(); if (kind === 'chat') { const i = ui.querySelector('.ndo-side [data-ndc="chatin"]'); if (i) i.focus(); } return; }
    S.sheet = kind; S.sheetArg = arg; wake();
    const el = $('sheet'); el.hidden = false; $('scrim').hidden = false; el.className = 'ndo-sheet ndo-sh-' + kind;
    const head = (title, sub) => '<div class="ndo-shh"><h3 id="ndo-sh-t">' + esc(title) + '</h3><button type="button" class="ndo-x" data-ndc="shx" aria-label="' + T.close + '">' + oi('x', 22) + '</button></div>' + (sub ? '<p class="ndo-shsub">' + esc(sub) + '</p>' : '');
    el.setAttribute('aria-labelledby', 'ndo-sh-t');
    if (kind === 'more') {
      const row = (k, ic, title, sub, right) => '<button type="button" class="ndo-row" data-more="' + k + '"><span class="ndo-ric">' + oi(ic, 22) + '</span><span class="ndo-rt"><b>' + esc(title) + '</b>' + (sub ? '<small>' + esc(sub) + '</small>' : '') + '</span>' + (right || '') + '</button>';
      const sw = (on) => '<span class="ndo-sw" data-on="' + on + '"><i></i></span>';
      el.innerHTML = head(T.more, isHost() ? nameOf(me) + ' · ' + T.host : '') +
        row('chat', 'chat', T.chat, S.chat.length ? String(S.chat.length) : '', S.unread ? '<b class="ndo-count ndo-mono">' + S.unread + '</b>' : '') +
        row('people', 'people', T.people, T.pill(S.people.size, ''), '') +
        row('voice', 'voice', T.voice, T.voiceSub, sw(S.voice)) +
        (coarse ? row('flip', 'flip', T.flip, '', '') : '') +
        row('hideself', 'person', T.hideSelf, '', sw(S.hideSelf)) +
        row('undo', 'undo', T.undoMine, '', '') +
        (isHost() && S.people.size > 1 ? row('summon', 'eye', T.summonBtn, '', '') + row('endall', 'leave', T.endAll, '', '') : '');
      el.querySelectorAll('[data-more]').forEach((b) => (b.onclick = () => moreDo(b.dataset.more)));
    } else if (kind === 'invite') {
      const link = inviteLink(), full = S.people.size >= 8;
      el.innerHTML = head(T.inviteTitle, T.inviteSub) + (full ? '<p class="ndo-full">' + T.full + '</p>' :
        '<a class="ndo-btn ndo-pri ndo-wide" data-ndc="wa" href="' + esc(waLink()) + '" target="_blank" rel="noopener">' + oi('chat', 20) + '<span>' + T.wa + '</span></a>' +
        '<div class="ndo-linkrow"><input class="ndo-link ndo-mono" data-ndc="link" readonly value="' + esc(link) + '" aria-label="' + T.inviteTitle + '"><button type="button" class="ndo-btn ndo-dark" data-ndc="copy">' + oi('copy', 18) + '<span>' + T.copy + '</span></button></div>');
      const cb = el.querySelector('[data-ndc="copy"]'); if (cb) cb.onclick = () => copyLink(cb);
    } else if (kind === 'people') {
      el.innerHTML = head(T.peopleTitle + ' ' + S.people.size, '') + '<div class="ndo-plist">' + peopleRows() + '</div>';
      wirePeople(el);
    } else if (kind === 'chat') {
      el.innerHTML = head(T.chat, '') + chatHtml();
      wireChat(el); S.unread = 0;
    } else if (kind === 'face') {
      const id = arg, nm = nameOf(id);
      el.innerHTML = '<div class="ndo-fhead"><span class="ndo-fdisc" style="--pen:' + penOf(id) + '">' + esc(nm.charAt(0)) + '</span><span><b>' + esc(nm) + '</b><small>' + esc(doingOf(id)) + '</small></span><button type="button" class="ndo-x" data-ndc="shx" aria-label="' + T.close + '">' + oi('x', 22) + '</button></div>' +
        '<button type="button" class="ndo-btn ndo-pri ndo-wide" data-ndc="fol">' + oi('eye', 20) + '<span>' + esc(T.followOne(nm)) + '</span></button>' +
        '<div class="ndo-two"><button type="button" class="ndo-btn" data-ndc="jump">' + T.jumpOnce + '</button><button type="button" class="ndo-btn" data-ndc="big">' + T.bigPic + '</button></div>';
      el.querySelector('[data-ndc="fol"]').onclick = () => { closeSheet(); follow(id); };
      el.querySelector('[data-ndc="jump"]').onclick = () => { closeSheet(); const v = S.views.get(id); if (v) { stopFollow(false); designer.setView(v.v); } };
      el.querySelector('[data-ndc="big"]').onclick = () => { closeSheet(); bigPicture(id); };
    } else if (kind === 'leave') {
      const others = sorted().filter((p) => p.id !== me), host = isHost() && others.length;
      el.innerHTML = head(T.leaveTitle, host ? T.leaveHostSub : '') + (host
        ? '<button type="button" class="ndo-btn ndo-wide ndo-keep" data-ndc="keep"><span>' + T.leaveKeep + '</span><small>' + esc(T.leaveKeepSub(nameOf(others[0].id))) + '</small></button>' +
          '<button type="button" class="ndo-btn ndo-danger ndo-wide" data-ndc="endall">' + T.leaveEnd + '</button>'
        : '<button type="button" class="ndo-btn ndo-danger ndo-wide" data-ndc="keep">' + T.leave + '</button>') +
        '<button type="button" class="ndo-btn ndo-plain ndo-wide" data-ndc="cancel">' + T.cancel + '</button>';
      el.querySelector('[data-ndc="keep"]').onclick = () => leave();
      const ea = el.querySelector('[data-ndc="endall"]'); if (ea) ea.onclick = () => endForAll();
      el.querySelector('[data-ndc="cancel"]').onclick = closeSheet;
    } else if (kind === 'perm') {
      el.innerHTML = head(T.permTitle, '') + '<div class="ndo-two ndo-perm"><div><b>' + T.iphone + '</b><p>' + esc(T.permIos) + '</p></div><div><b>' + T.android + '</b><p>' + esc(T.permAndroid) + '</p></div></div>' +
        '<div class="ndo-two"><button type="button" class="ndo-btn ndo-pri" data-ndc="retry">' + T.permRetry + '</button><button type="button" class="ndo-btn" data-ndc="listen">' + T.permListen + '</button></div>';
      el.querySelector('[data-ndc="retry"]').onclick = async () => { closeSheet(); await toggleMic(true); };
      el.querySelector('[data-ndc="listen"]').onclick = closeSheet;
    } else if (kind === 'battery') {
      el.innerHTML = head(T.battery(arg), T.batterySub) + '<div class="ndo-two"><button type="button" class="ndo-btn ndo-pri" data-ndc="bv">' + oi('voice', 18) + '<span>' + T.batteryVoice + '</span></button><button type="button" class="ndo-btn" data-ndc="bk">' + T.batteryKeep + '</button></div>';
      el.querySelector('[data-ndc="bv"]').onclick = () => { closeSheet(); setVoice(true); };
      el.querySelector('[data-ndc="bk"]').onclick = closeSheet;
    } else if (kind === 'summon') {
      const sm = S.summon; if (!sm) { closeSheet(); return; }
      el.className = 'ndo-sheet ndo-card';
      el.innerHTML = '<div class="ndo-sumhead"><span class="ndo-ring" data-ndc="ring"><svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="27"/><circle class="ndo-ringv" cx="32" cy="32" r="27"/></svg><b class="ndo-mono" data-ndc="sec">' + SUMMON_S + '</b></span>' +
        '<span><b id="ndo-sh-t">' + esc(T.summonTitle(nameOf(sm.from), sm.room)) + '</b><small data-ndc="sumsub">' + esc(T.summonSub(SUMMON_S)) + '</small></span></div>' +
        '<div class="ndo-two"><button type="button" class="ndo-btn ndo-pri" data-ndc="sgo">' + T.summonGo + '</button><button type="button" class="ndo-btn" data-ndc="sno">' + T.summonNo + '</button></div>';
      el.querySelector('[data-ndc="sgo"]').onclick = () => summonAnswer(true);
      el.querySelector('[data-ndc="sno"]').onclick = () => summonAnswer(false);
    }
    const x = el.querySelector('[data-ndc="shx"]'); if (x) x.onclick = closeSheet;
    paintBar();
    const f = el.querySelector('button,a,input'); if (f && !coarse) try { f.focus({ preventScroll: true }); } catch (e) { /* none */ }
  }
  $('scrim').onclick = () => { if (S.sheet !== 'summon') closeSheet(); };
  ui.addEventListener('keydown', (ev) => { if (ev.key === 'Escape' && S.sheet && S.sheet !== 'summon') closeSheet(); });
  function moreDo(k) {
    if (k === 'chat' || k === 'people') { openSheet(k); return; }
    if (k === 'voice') { setVoice(!S.voice); openSheet('more'); openSheet('more'); return; }
    if (k === 'hideself') { S.hideSelf = !S.hideSelf; paintFaces(); closeSheet(); openSheet('more'); return; }
    if (k === 'flip') { closeSheet(); flip(); return; }
    if (k === 'undo') { closeSheet(); undoMine(); return; }
    if (k === 'summon') { closeSheet(); summonAll(); return; }
    if (k === 'endall') { closeSheet(); openSheet('leave'); }
  }
  const doingOf = (id) => {
    const h = [...S.holds.entries()].find(([, v]) => v.by === id && fresh(v));
    if (h) return T.doing.hold(objName(h[0]));
    if (S.speaking.has(id)) return T.doing.talk;
    const p = person(id); if (p && !p.mic) return T.doing.listen;
    return '';
  };
  function peopleRows() {
    return sorted().map((p) => '<div class="ndo-prow" style="--pen:' + penOf(p.id) + '"><span class="ndo-pdisc">' + esc(((p.name || nameOf(p.id)) || '?').trim().charAt(0)) + '</span>' +
      '<span class="ndo-pt"><b>' + esc(p.local ? (p.name || T.me) + ' (' + T.me + ')' : nameOf(p.id)) + (p.id === hostId() ? ' <i class="ndo-htag">' + T.host + '</i>' : '') + '</b><small>' + esc(doingOf(p.id)) + '</small></span>' +
      '<span class="ndo-pmic">' + oi(p.mic ? 'mic' : 'micOff', 18) + '</span>' +
      (p.local ? '' : '<button type="button" class="ndo-btn ndo-sec" data-fol="' + esc(p.id) + '">' + oi('eye', 18) + '<span>' + T.followP + '</span></button>') + '</div>').join('');
  }
  function wirePeople(el) { el.querySelectorAll('[data-fol]').forEach((b) => (b.onclick = () => { closeSheet(); follow(b.dataset.fol); })); }
  const chatHtml = () => '<ul class="ndo-msgs" data-ndc="msgs" aria-live="polite">' + S.chat.slice(-60).map((m) => '<li><b style="color:' + penOf(m.from) + '">' + esc(m.who) + '</b> <span class="ndo-mono">' + esc(m.t || '') + '</span><p>' + esc(m.text) + '</p></li>').join('') + '</ul>' +
    '<form class="ndo-form" data-ndc="form"><input data-ndc="chatin" maxlength="300" autocomplete="off" enterkeyhint="send" aria-label="' + T.chatIn + '" placeholder="' + T.chatIn + '"><button class="ndo-btn ndo-pri ndo-sendb" aria-label="' + T.sendMsg + '">' + oi('send', 20) + '</button></form>';
  function wireChat(el) {
    el.querySelector('[data-ndc="form"]').onsubmit = (ev) => { ev.preventDefault(); const i = el.querySelector('[data-ndc="chatin"]'); chat(i.value); i.value = ''; };
    const ml = el.querySelector('.ndo-msgs'); ml.scrollTop = ml.scrollHeight;
  }
  function paintSide() {
    if (!wide()) return;
    const tabs = ui.querySelectorAll('.ndo-side [data-side]');
    tabs[0].innerHTML = T.people + ' <b class="ndo-mono">' + S.people.size + '</b>'; tabs[1].innerHTML = T.chat + (S.unread ? ' <b class="ndo-count ndo-mono">' + S.unread + '</b>' : '');
    tabs.forEach((b) => { b.setAttribute('aria-selected', String(b.dataset.side === S.sideTab)); b.onclick = () => { S.sideTab = b.dataset.side; if (S.sideTab === 'chat') S.unread = 0; paintSide(); paintBar(); }; });
    const body = $('sidebody'), keep = body.querySelector('[data-ndc="chatin"]'), draft = keep ? keep.value : '', had = keep && shadow.activeElement === keep;
    if (S.sideTab === 'people') { body.innerHTML = '<div class="ndo-plist">' + peopleRows() + '</div><h4>' + T.chat + '</h4>' + chatHtml(); wirePeople(body); }
    else body.innerHTML = chatHtml();
    wireChat(body);
    const ni = body.querySelector('[data-ndc="chatin"]'); if (ni) { ni.value = draft; if (had) ni.focus(); }
    if (S.sideTab === 'chat') S.unread = 0;
  }

  /* ---------------- invite ---------------- */
  function inviteLink() { // this page, the room, and only the page's own plain choices (which project page); never a name
    const u = new URL(opts.inviteBase || location.href), keep = new URLSearchParams();
    for (const k of ['project', 'pn', 'ul', 'unit']) { const v = u.searchParams.get(k); if (v) keep.set(k, v.slice(0, 80)); }
    keep.set('room', opts.room || '');
    if (opts.design) keep.set('design', opts.design);
    return u.origin + u.pathname + '?' + keep.toString();
  }
  const waText = () => { const u = (store.apt && store.apt.unit) || {}; const mine = person(me); return T.inviteMsg(mine && mine.name, u.rooms, u.floor, inviteLink()); };
  const waLink = () => 'https://wa.me/?text=' + encodeURIComponent(waText());
  async function copyLink(btn) {
    const v = inviteLink();
    try { await navigator.clipboard.writeText(v); } catch (e) { const i = $('sheet').querySelector('.ndo-link'); if (i) i.select(); try { document.execCommand('copy'); } catch (x) { /* none */ } }
    if (btn) { btn.querySelector('span').textContent = T.copied; btn.innerHTML = oi('check', 18) + '<span>' + T.copied + '</span>'; btn.classList.add('ndo-done'); setTimeout(() => { if (btn.isConnected) { btn.innerHTML = oi('copy', 18) + '<span>' + T.copy + '</span>'; btn.classList.remove('ndo-done'); } }, 2000); }
  }

  /* ---------------- chat ---------------- */
  const clock = () => new Date().toTimeString().slice(0, 5);
  function chat(text) {
    text = String(text || '').replace(/\s+/g, ' ').trim().slice(0, 300); if (!text) return false;
    S.chat.push({ who: (person(me) && person(me).name) || T.me, text, from: me, t: clock() }); send('chat', { t: 'm', text, at: now() });
    if (S.sheet === 'chat') openSheet('chat', null), openSheet('chat', null); paintSide(); return true;
  }

  /* ---------------- holding a piece, and the design ---------------- */
  const fresh = (h) => !!h && (h.by === me || (now() - h.at < HOLD_MS && S.people.has(h.by)));
  const liveHolds = () => [...S.holds.entries()].filter(([, h]) => h.by !== me && fresh(h));
  const heldByOther = (key) => { const h = S.holds.get(key); return h && h.by !== me && fresh(h) ? h : null; };
  store.setGuard((op, meta) => {
    const key = keyOf(op), h = heldByOther(key);
    if (h) return { code: 'call.hold', reason: T.holdRefused(nameOf(h.by), objName(key)), key, by: h.by };
    if (meta && meta.replay) { const lm = S.lastMover.get(key); if (lm && lm !== me && S.people.has(lm)) return { code: 'call.undo', reason: T.undoOther(nameOf(lm)), key }; }
    return null;
  });
  function claim(key) {
    if (S.mine.has(key)) return true;
    const h = heldByOther(key);
    if (h) { refused(key, h.by); return false; }
    S.mine.add(key); S.holds.set(key, { by: me, at: now() });
    send('hold', { t: 'on', k: key }, true);
    ovLoop(); return true;
  }
  function release() {
    if (!S.mine.size) return;
    for (const key of S.mine) {
      const op = S.lastOp.get(key);
      if (op) sendOp(op, true, null);
      send('hold', { t: 'off', k: key }, true);
      S.holds.delete(key); S.lastOp.delete(key);
    }
    S.mine.clear(); maybeBack(); ovLoop();
  }
  function refused(key, by) {
    stats.refused++;
    if (Date.now() - S.refusedAt > 1800) { S.refusedAt = Date.now(); say(T.holdRefused(nameOf(by), objName(key)), { icon: 'hand' }); }
    const box = ui.querySelector('.ndo-hold[data-k="' + CSS.escape(key) + '"]');
    if (box && !reduce) { box.classList.remove('ndo-shake'); void box.offsetWidth; box.classList.add('ndo-shake'); }
  }
  function sendOp(op, reliable, gesture) {
    const key = keyOf(op);
    S.seq += 1; stats.sent.design++;
    const m = { t: 'op', op, g: gesture, rev: store.design.rev, by: 'buyer', at: now(), k: key, q: S.seq, live: !reliable };
    if (S.state !== 'connected') { S.queue.push(op); return; }
    send('design', m, reliable);
  }
  const offStore = store.on((e) => {
    if (e.type === 'reject' && (e.code === 'call.hold' || e.code === 'call.undo')) {
      if (e.code === 'call.hold') refused(e.key || keyOf(e.op), e.by); else say(e.reason, { icon: 'undo' });
      return;
    }
    if (e.type !== 'change' || !S.alive || e.op.op === 'design.load') return;
    const key = keyOf(e.op), by = e.remote ? e.from || null : me;
    if (!e.remote) {
      S.lastMover.set(key, me); S.changes.push({ by: me, key, op: e.op.op });
      const live = S.down && !!e.gesture;
      if (live) { if (!claim(key)) return; S.lastOp.set(key, e.op); sendOp(e.op, false, e.gesture); }
      else sendOp(e.op, true, e.gesture);
      if (!e.replay) { S.undoAt = Date.now(); showUndo(); }
      if (key.startsWith('i:')) autoArrange(false);
    } else if (by) S.lastMover.set(key, by);
    paintHead();
  });
  let undoT = 0;
  function showUndo() { const u = $('undo'); u.hidden = false; clearTimeout(undoT); undoT = setTimeout(() => (u.hidden = true), 8000); }
  $('undo').onclick = () => undoMine();
  function undoMine() {
    if (!store.canUndo()) { say(T.undoNone); return false; }
    return store.undo();
  }

  // touches: a finger on a piece holds it at once (the answer is local, under 200 ms), the layout follows
  let selAtDown = null;
  const downCap = (ev) => {
    if (S.barHidden && !wide() && !ev.composedPath().some((n) => n === ui)) { ev.stopPropagation(); ev.preventDefault(); wake(); return; } // the tap that brings the buttons back does nothing else
    S.down = true; S.lastTouch = Date.now(); selAtDown = designer.selection; wake(); };
  on(host, 'pointerdown', downCap, true);
  const upCap = () => { if (!S.down) return; S.down = false; setTimeout(() => { if (!S.down) release(); }, 0); armHide(); };
  on(window, 'pointerup', upCap, true); on(window, 'pointercancel', upCap, true);
  const touched = (from3d) => (ev) => {
    if (S.pointMode) return;
    let id = null;
    if (!from3d) { const t = ev.target && ev.target.closest && ev.target.closest('[data-item]'); id = t ? t.dataset.item : null; }
    else { const s = designer.selection; if (s && s.type === 'item' && s !== selAtDown) id = s.id; }
    if (!id) return;
    const key = 'i:' + id;
    if (claim(key)) autoArrange(from3d);
  };
  on(planHost, 'pointerdown', touched(false)); on(spaceEl, 'pointerdown', touched(true));
  every(() => { // heartbeat while I hold; others' holds run out after 6 s without a sign of life
    if (S.down && S.mine.size) for (const k of S.mine) send('hold', { t: 'on', k }, true);
    let gone = false;
    for (const [k, h] of S.holds) if (h.by !== me && !fresh(h)) { S.holds.delete(k); gone = true; }
    if (gone) { ovLoop(); maybeBack(); }
  }, BEAT_MS);

  /* ---------------- follow, views, summon ---------------- */
  const r2 = (x) => Math.round(x * 100) / 100, r4 = (x) => Math.round(x * 1e4) / 1e4;
  every(() => {
    if (!S.alive || S.state !== 'connected') return;
    const v = designer.getView(); if (!v) return;
    const t = now(), fast = S.followers.size > 0;
    if (!fast && t - S.lastViewAt < 450) return;
    const key = [v.mode, r2(v.x), r2(v.y), r2(v.z), r4(v.yaw), r4(v.pitch), S.followers.size].join(',');
    if (key === S.lastView && t - S.lastViewAt < (fast ? 1000 : 4000)) return;
    S.lastView = key; S.lastViewAt = t; stats.sent.view++;
    send('view', { t: 'v', v: { mode: v.mode, x: r2(v.x), y: r2(v.y), z: r2(v.z), yaw: r4(v.yaw), pitch: r4(v.pitch), fov: v.fov }, n: S.followers.size, at: t }, false);
  }, 100);
  function follow(id) {
    if (id === false || id === null) { stopFollow(false); return; }
    if (id === true || id === undefined) id = S.lostFollow || (hostId() !== me ? hostId() : (sorted().find((p) => p.id !== me) || {}).id);
    if (!id || id === me || !S.people.has(id)) return;
    if (S.following && S.following !== id) send('follow', { t: 'off' }, true, [S.following]);
    S.following = id; S.lostFollow = null;
    send('follow', { t: 'on' }, true, [id]);
    const v = S.views.get(id); if (v) { S.target = v.v; ovLoop(); }
    if (S.lay === 'b') setLay('a', 'auto');
    paintBar(); paintFaces();
  }
  function stopFollow(byTouch) {
    if (!S.following) return;
    send('follow', { t: 'off' }, true, [S.following]);
    if (byTouch) S.lostFollow = S.following;
    S.following = null; S.target = null; paintBar(); paintFaces();
  }
  const lookAway = (ev) => { if (!ev.isTrusted || !S.following) return; stopFollow(true); };
  on(spaceEl, 'pointerdown', lookAway, true); on(spaceEl, 'wheel', lookAway, { capture: true, passive: true }); on(planHost, 'pointerdown', lookAway, true);
  $('backchip').onclick = () => follow(S.lostFollow);
  $('followtab').onclick = () => stopFollow(false);
  function easeView() { // the leader's camera, eased (0.35 a frame, snapped under a hair)
    const tg = S.target; if (!tg || !S.following) return false;
    const cur = designer.getView(); if (!cur) return false;
    if (cur.mode !== tg.mode || reduce) { designer.setView(tg); S.target = null; return false; }
    let dy = tg.yaw - cur.yaw; while (dy > Math.PI) dy -= 2 * Math.PI; while (dy < -Math.PI) dy += 2 * Math.PI;
    const k = 0.35, d = Math.abs(tg.x - cur.x) + Math.abs(tg.y - cur.y) + Math.abs((tg.z || 0) - (cur.z || 0)), small = d < 2 && Math.abs(dy) < 0.004;
    if (small) { designer.setView(tg); S.target = null; return false; }
    designer.setView({ mode: tg.mode, x: cur.x + (tg.x - cur.x) * k, y: cur.y + (tg.y - cur.y) * k, z: (cur.z || 0) + ((tg.z || 0) - (cur.z || 0)) * k, yaw: cur.yaw + dy * k, pitch: (cur.pitch || 0) + ((tg.pitch || 0) - (cur.pitch || 0)) * k });
    return true;
  }
  function roomNameHere() {
    const v = designer.getView(), sel = designer.selection;
    try {
      let id = sel && sel.type === 'room' ? sel.id : null;
      if (!id && v && v.mode === 'walk') id = store.roomAt(v.x, v.y);
      const f = id && store.derived.faceBy[id];
      if (f && f.room && f.room.name_he && lang === 'he') return f.room.name_he.startsWith('ה') ? f.room.name_he : 'ה' + f.room.name_he;
    } catch (e) { /* none */ }
    return T.theFlat;
  }
  function summonAll() { if (!isHost()) return; send('sys', { t: 'summon', room: roomNameHere() }, true); say(T.summonBtn); }
  let sumT = 0;
  function gotSummon(from, room) {
    if (from !== hostId()) return;
    clearInterval(sumT);
    S.summon = { from, room: String(room || T.theFlat).slice(0, 40), left: SUMMON_S };
    openSheet('summon');
    sumT = setInterval(() => {
      if (!S.summon) { clearInterval(sumT); return; }
      S.summon.left -= 1;
      const s = $('sheet').querySelector('[data-ndc="sec"]'), sub = $('sheet').querySelector('[data-ndc="sumsub"]');
      if (s) s.textContent = String(Math.max(0, S.summon.left)); if (sub) sub.textContent = T.summonSub(Math.max(0, S.summon.left));
      $('sheet').style.setProperty('--left', String(S.summon.left / SUMMON_S));
      if (S.summon.left <= 0) summonAnswer(true);
    }, 1000);
    timers.push(() => clearInterval(sumT));
  }
  function summonAnswer(yes) {
    const sm = S.summon; clearInterval(sumT); S.summon = null; closeSheet();
    if (!sm) return;
    if (yes) follow(sm.from); else { S.lostFollow = sm.from; paintFollow(); }
  }

  /* ---------------- pointing: a line in my pen colour that fades ---------------- */
  const planScreen = (x, y) => { const s = planEl(); if (!s || !s.getScreenCTM() || !s.getBoundingClientRect().width) return null; const p = new DOMPoint(x, y).matrixTransform(s.getScreenCTM()); return [p.x, p.y]; };
  function screenToFloor(cx, cy) {
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
  const toPlan = (ev, src) => { if (src === 'plan') { const s = planEl(); if (!s || !s.getScreenCTM()) return null; const q = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(s.getScreenCTM().inverse()); return [Math.round(q.x), Math.round(q.y)]; } return screenToFloor(ev.clientX, ev.clientY); };
  let stroke = null, lpT = 0, lpAt = null;
  function startStroke(ev, src) {
    const p = toPlan(ev, src); if (!p) return;
    stroke = { s: Math.random().toString(36).slice(2, 8), src, pts: [p], sent: 0, at: 0 };
    gotLaser(me, { s: stroke.s, p: [p] });
    const mv = (e) => { const q = toPlan(e, src); if (!q) return; const l = stroke.pts[stroke.pts.length - 1]; if (Math.hypot(q[0] - l[0], q[1] - l[1]) < 4) return; stroke.pts.push(q); gotLaser(me, { s: stroke.s, p: [q] }); if (now() - stroke.at > 50) { stroke.at = now(); stats.sent.ptr++; send('ptr', { t: 'l', s: stroke.s, p: stroke.pts.slice(stroke.sent) }, false); stroke.sent = stroke.pts.length; } };
    const up = () => { removeEventListener('pointermove', mv, true); removeEventListener('pointerup', up, true); removeEventListener('pointercancel', up, true); if (!stroke) return; send('ptr', { t: 'l', s: stroke.s, p: stroke.pts.slice(stroke.sent), end: 1 }, true); gotLaser(me, { s: stroke.s, p: [], end: 1 }); stroke = null; };
    addEventListener('pointermove', mv, true); addEventListener('pointerup', up, true); addEventListener('pointercancel', up, true);
  }
  const pointDown = (src) => (ev) => {
    if (S.pointMode) { ev.stopPropagation(); ev.preventDefault(); startStroke(ev, src); return; }
    if (src !== 'plan') return;
    const t = ev.target && ev.target.closest && ev.target.closest('[data-item],.grip,[data-cam]'); if (t) return;
    lpAt = [ev.clientX, ev.clientY]; clearTimeout(lpT);
    lpT = setTimeout(() => { lpT = 0; if (lpAt) startStroke({ clientX: lpAt[0], clientY: lpAt[1] }, 'plan'); }, 520);
  };
  on(planHost, 'pointerdown', pointDown('plan'), true); on(spaceEl, 'pointerdown', pointDown('space'), true);
  on(planHost, 'pointermove', (ev) => { if (lpAt && Math.hypot(ev.clientX - lpAt[0], ev.clientY - lpAt[1]) > 10) { clearTimeout(lpT); lpAt = null; } }, true);
  on(window, 'pointerup', () => { clearTimeout(lpT); lpAt = null; }, true);
  function gotLaser(from, m) {
    let L = S.lasers.get(from);
    if (!L || L.s !== m.s) { L = { s: m.s, pts: [], end: 0 }; S.lasers.set(from, L); }
    for (const p of m.p || []) if (Array.isArray(p) && isFinite(p[0]) && isFinite(p[1])) L.pts.push([+p[0], +p[1]]);
    if (L.pts.length > 400) L.pts.splice(0, L.pts.length - 400);
    L.at = now(); if (m.end) L.end = now();
    ovLoop();
  }

  /* ---------------- the overlay: held pieces, lasers, view cones ---------------- */
  let ovOn = false;
  function ovLoop() { if (!ovOn && S.alive) { ovOn = true; requestAnimationFrame(ovFrame); } }
  function ovFrame() {
    ovOn = false; if (!S.alive) return;
    const more = paintOv() | easeView();
    if (more) ovLoop();
  }
  const ns = 'http://www.w3.org/2000/svg';
  function paintOv() {
    const ov = $('ov'), svgEl = $('ovs'), hr = host.getBoundingClientRect(), t = now();
    let active = false;
    const planVis = planHost && planHost.offsetParent && planHost.getBoundingClientRect().width > 60;
    const sp = designer.space, spR = spaceEl && spaceEl.getBoundingClientRect();
    const in3d = (xy) => xy && spR && xy[0] >= spR.left && xy[0] <= spR.right && xy[1] >= spR.top && xy[1] <= spR.bottom;
    // held pieces (by others)
    const seen = new Set();
    for (const [key, h] of liveHolds()) {
      active = true; seen.add(key);
      let box = ov.querySelector('.ndo-hold[data-k="' + CSS.escape(key) + '"]');
      if (!box) { box = document.createElement('div'); box.className = 'ndo-hold'; box.dataset.k = key; box.innerHTML = '<i class="ndo-hface"></i><span class="ndo-chip"><i class="ndo-mini-face"></i><b></b></span>'; ov.appendChild(box); }
      box.style.setProperty('--pen', penOf(h.by));
      box.querySelector('.ndo-hface').textContent = nameOf(h.by).charAt(0); box.querySelector('.ndo-mini-face').textContent = nameOf(h.by).charAt(0);
      box.querySelector('b').textContent = T.holdChip(nameOf(h.by), objName(key));
      let r = null;
      if (planVis && key.startsWith('i:')) { const e = planHost.querySelector('[data-item="' + CSS.escape(key.slice(2)) + '"] rect'); if (e) { const b = e.getBoundingClientRect(); if (b.width) r = { l: b.left, t: b.top, w: b.width, h: b.height }; } }
      if (!r && key.startsWith('i:') && sp && sp.screenOf) { const it = store.item(key.slice(2)); if (it) { const c = sp.screenOf(it.x, it.y, 60); if (in3d(c)) r = { l: c[0] - 22, t: c[1] - 22, w: 44, h: 44, d3: true }; } }
      box.hidden = !r;
      if (r) {
        box.classList.toggle('ndo-h3', !!r.d3); box.style.transform = 'translate(' + (r.l - hr.left - 6).toFixed(1) + 'px,' + (r.t - hr.top - 6).toFixed(1) + 'px)'; box.style.width = r.w + 12 + 'px'; box.style.height = r.h + 12 + 'px';
        const ch = box.querySelector('.ndo-chip'); ch.style.transform = ''; const cr = ch.getBoundingClientRect();
        const dx = cr.left < hr.left + 6 ? hr.left + 6 - cr.left : cr.right > hr.right - 6 ? hr.right - 6 - cr.right : 0; if (dx) ch.style.transform = 'translateX(' + dx.toFixed(1) + 'px)';
      }
    }
    ov.querySelectorAll('.ndo-hold').forEach((b) => { if (!seen.has(b.dataset.k)) b.remove(); });
    // lasers and cones, drawn in screen pixels
    let g = '';
    const toS = (p) => (planVis ? planScreen(p[0], p[1]) : null) || (sp && sp.screenOf ? (() => { const s = sp.screenOf(p[0], p[1], 0); return in3d(s) ? s : null; })() : null);
    const px = (p) => (p[0] - hr.left).toFixed(1) + ',' + (p[1] - hr.top).toFixed(1);
    for (const [id, L] of S.lasers) {
      const age = L.end ? t - L.end : 0;
      if (L.end && age > 1200) { S.lasers.delete(id); ov.querySelectorAll('.ndo-lchip[data-id="' + CSS.escape(id) + '"]').forEach((c) => c.remove()); continue; }
      active = true;
      const op = L.end ? Math.max(0, 1 - age / 1200) : 1, col = penOf(id), sc = L.pts.map(toS).filter(Boolean);
      if (!sc.length) continue;
      const scale = (() => { const a = toS(L.pts[L.pts.length - 1]), b = toS([L.pts[L.pts.length - 1][0] + 100, L.pts[L.pts.length - 1][1]]); return a && b ? Math.max(0.05, Math.hypot(b[0] - a[0], b[1] - a[1]) / 100) : 0.3; })();
      const last = sc[sc.length - 1];
      g += '<g opacity="' + op.toFixed(2) + '"><polyline points="' + sc.map(px).join(' ') + '" fill="none" stroke="' + col + '" stroke-opacity=".55" stroke-width="' + Math.max(4, 10 * scale).toFixed(1) + '" stroke-linecap="round" stroke-linejoin="round"/>' +
        '<circle cx="' + px(last).split(',')[0] + '" cy="' + px(last).split(',')[1] + '" r="' + Math.max(6, 11 * scale).toFixed(1) + '" fill="' + col + '"/>' +
        '<circle cx="' + px(last).split(',')[0] + '" cy="' + px(last).split(',')[1] + '" r="' + Math.max(12, 22 * scale).toFixed(1) + '" fill="none" stroke="' + col + '" stroke-width="2" stroke-opacity=".6"/>' +
        '<circle cx="' + px(last).split(',')[0] + '" cy="' + px(last).split(',')[1] + '" r="' + Math.max(18, 35 * scale).toFixed(1) + '" fill="none" stroke="' + col + '" stroke-width="1.5" stroke-opacity=".3"/></g>';
      let chip = ov.querySelector('.ndo-lchip[data-id="' + CSS.escape(id) + '"]');
      if (!chip) { chip = document.createElement('span'); chip.className = 'ndo-chip ndo-lchip'; chip.dataset.id = id; chip.innerHTML = '<i class="ndo-mini-face"></i><b></b>'; ov.appendChild(chip); }
      chip.style.setProperty('--pen', col); chip.style.opacity = op.toFixed(2);
      chip.querySelector('i').textContent = nameOf(id).charAt(0); chip.querySelector('b').textContent = T.pointChip(id === me ? T.me : nameOf(id));
      chip.style.transform = 'translate(' + (last[0] - hr.left + 14).toFixed(1) + 'px,' + (last[1] - hr.top + 14).toFixed(1) + 'px)';
    }
    ov.querySelectorAll('.ndo-lchip').forEach((c) => { if (!S.lasers.has(c.dataset.id)) c.remove(); });
    for (const [id, v] of S.views) { // the others' view cones on the floor, only while they walk inside
      if (!S.people.has(id) || id === S.following || !v.v || v.v.mode !== 'walk' || t - v.at > 15000) continue;
      const half = ((v.v.fov || 60) * Math.PI) / 360, R = 150, a = [v.v.x, v.v.y], b = [v.v.x + R * Math.cos(v.v.yaw - half), v.v.y + R * Math.sin(v.v.yaw - half)], c = [v.v.x + R * Math.cos(v.v.yaw + half), v.v.y + R * Math.sin(v.v.yaw + half)];
      const draw = (f) => { const A = f(a), B = f(b), C = f(c); if (!A || !B || !C) return ''; const col = penOf(id); return '<polygon points="' + [A, B, C].map(px).join(' ') + '" fill="' + col + '" fill-opacity=".28" stroke="' + col + '" stroke-width="1.5"/><rect x="' + (A[0] - hr.left - 9).toFixed(1) + '" y="' + (A[1] - hr.top - 9).toFixed(1) + '" width="18" height="18" fill="#fff" stroke="' + col + '" stroke-width="2"/>'; };
      if (planVis) g += draw((p) => planScreen(p[0], p[1]));
      if (sp && sp.screenOf && spR && spR.width > 200) g += draw((p) => { const s = sp.screenOf(p[0], p[1], 0); return in3d(s) ? s : null; });
    }
    svgEl.innerHTML = g;
    return active;
  }

  /* ---------------- media ---------------- */
  async function toggleMic(force) {
    const want = force === undefined ? !S.mic : !!force;
    try { await tr.setMicrophone(want); S.micBlocked = false; }
    catch (e) { if (want) { S.micBlocked = true; say(T.listen, { link: T.permLink, onLink: () => openSheet('perm'), ms: 7000 }); } }
    sync();
  }
  async function toggleCam(force) {
    const want = force === undefined ? !S.cam : !!force;
    if (want && S.voice) setVoice(false);
    try { await tr.setCamera(want); S.camBlocked = false; }
    catch (e) { if (want) { S.camBlocked = true; say(T.listen, { link: T.permLink, onLink: () => openSheet('perm'), ms: 7000 }); } }
    sync();
  }
  async function flip() { try { const f = await tr.switchCamera(); S.facing = f || (S.facing === 'user' ? 'environment' : 'user'); } catch (e) { /* no second camera */ } sync(); }
  function setVoice(onv, auto) {
    S.voice = !!onv; S.voiceAuto = !!(onv && auto);
    if (onv) { S.camBefore = S.cam; if (S.cam) tr.setCamera(false).catch(() => {}); }
    else if (S.camBefore) { S.camBefore = false; tr.setCamera(true).catch(() => {}); }
    try { if (tr.setVideoReceive) tr.setVideoReceive(!onv); } catch (e) { /* none */ }
    banner(onv && auto ? 'weak' : S.banner === 'weak' ? null : S.banner);
    paintFaces(); paintBar();
  }
  // the mic level beside the mic button
  every(() => { const b = $('mic').querySelector('.ndo-lv i'); if (!b) return; let l = 0; try { l = S.mic && tr.level ? tr.level(me) : S.mic && S.speaking.has(me) ? 0.6 : 0; } catch (e) { l = 0; } b.style.height = Math.round(Math.min(1, l * 3) * 100) + '%'; }, 150);

  /* ---------------- banners: reconnect, sound, weak ---------------- */
  let recT = 0;
  function banner(kind) {
    S.banner = kind; const box = $('banners'); clearInterval(recT);
    if (!kind) { box.innerHTML = ''; return; }
    if (kind === 'reconnect' || kind === 'lost') {
      box.innerHTML = '<div class="ndo-ban ndo-ban-re" role="status"><i class="ndo-spin"></i><b>' + (kind === 'lost' ? T.lost : T.reconnect) + '</b><span class="ndo-mono" data-ndc="recs">00:00</span><button type="button" class="ndo-btn ndo-sec" data-ndc="retry" hidden>' + T.retry + '</button></div>';
      const t0 = S.recAt || Date.now();
      const tick = () => { const s = Math.floor((Date.now() - t0) / 1000), c = box.querySelector('[data-ndc="recs"]'); if (!c) return; c.textContent = String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0'); const r = box.querySelector('[data-ndc="retry"]'); if (r) r.hidden = !(kind === 'lost' || s >= 30); };
      tick(); recT = setInterval(tick, 1000);
      box.querySelector('[data-ndc="retry"]').onclick = () => rejoin();
    } else if (kind === 'audio') {
      box.innerHTML = '<button type="button" class="ndo-ban ndo-ban-audio" data-ndc="audio">' + oi('voice', 22) + '<span>' + T.audio + '</span></button>';
      box.querySelector('[data-ndc="audio"]').onclick = () => { try { tr.startAudio && tr.startAudio(); } catch (e) { /* none */ } banner(null); };
    } else if (kind === 'weak') {
      box.innerHTML = '<div class="ndo-ban ndo-ban-weak" role="status">' + oi('signal', 18) + '<b>' + T.weak + '</b><button type="button" class="ndo-linkb" data-ndc="weakv">' + T.weakVideo + '</button></div>';
      box.querySelector('[data-ndc="weakv"]').onclick = () => { S.poorSince = 0; setVoice(false); banner(null); };
    }
  }
  async function rejoin() {
    try { if (tr.reconnect) await tr.reconnect(); else await tr.connect(); } catch (e) { /* the button stays */ }
  }

  /* ---------------- incoming ---------------- */
  function askSnap(from) {
    if (!from || from === me) return;
    S.snapFrom = from; stats.resync++;
    send('design-snap', { t: 'ask', at: now() }, true, [from]);
  }
  tr.onData((topic, m, from) => {
    if (!S.alive || !m || typeof m !== 'object') return;
    from = String(from || m.from || ''); if (from === me) return;
    switch (topic) {
      case 'design': {
        if (m.t !== 'op' || !m.op) return;
        const key = m.k || keyOf(m.op), sk = from + '|' + key;
        if (typeof m.q === 'number') { if (m.q <= (S.lastSeq.get(sk) || 0)) { stats.ignored++; return; } S.lastSeq.set(sk, m.q); }
        const h = S.holds.get(key);
        if (h && h.by !== from && fresh(h)) { stats.ignored++; if (h.by === me) send('hold', { t: 'on', k: key }, true, [from]); return; } // someone else holds it: their hand wins
        if (m.live) S.holds.set(key, { by: from, at: now() });
        const t0 = now(), r = store.apply(m.op, { by: 'buyer', remote: true, gesture: m.g || null });
        const t1 = now(); stats.opApply.push(t1 - t0); if (m.at) stats.op.push(t1 - m.at);
        S.lastMover.set(key, from); S.changes.push({ by: from, key, op: m.op.op });
        if (!r.ok && !m.live) askSnap(from);
        if (m.live && key.startsWith('i:')) autoArrange(false);
        ovLoop();
        return;
      }
      case 'hold':
        if (m.t === 'on' && m.k) {
          const mineToo = S.mine.has(m.k);
          if (mineToo) { if (String(from) < me) { S.mine.delete(m.k); S.lastOp.delete(m.k); S.holds.set(m.k, { by: from, at: now() }); refused(m.k, from); } else send('hold', { t: 'on', k: m.k }, true, [from]); }
          else S.holds.set(m.k, { by: from, at: now() });
          if (String(m.k).startsWith('i:')) autoArrange(false);
        } else if (m.t === 'off' && m.k) { const h = S.holds.get(m.k); if (h && h.by === from) S.holds.delete(m.k); maybeBack(); }
        ovLoop(); if (S.sheet === 'people') openSheet('people'), openSheet('people');
        return;
      case 'design-snap':
        if (m.t === 'ask') send('design-snap', { t: 'snap', design: designer.getDesign(), at: now(), at0: m.at }, true, [from]);
        else if (m.t === 'snap' && m.design && from === S.snapFrom) {
          store.load(m.design); S.snapFrom = null;
          stats.snap = { ms: m.at0 ? Math.round(now() - m.at0) : null, rev: m.design.rev, items: (m.design.items || []).length, bytes: JSON.stringify(m.design).length };
          const q = S.queue.splice(0); for (const op of q) store.apply(op, { by: 'buyer' }); // what I changed while away goes on top
        }
        return;
      case 'plan':
        if (m.t === 'ask' && opts.share) { const sh = opts.share() || {}; if (sh.plan) { stats.planSent = (stats.planSent || 0) + 1; send('plan', { t: 'plan', plan: sh.plan, title: sh.title || '', unitLabel: sh.unitLabel || '', mine: !!sh.mine, design: designer.getDesign(), at: now(), at0: m.at }, true, [from]); } }
        return;
      case 'view':
        if (m.t !== 'v' || !m.v) return;
        S.views.set(from, { v: m.v, at: now(), n: m.n || 0 });
        if (S.following === from) { S.target = m.v; if (m.at) stats.view.push(now() - m.at); }
        ovLoop(); if (m.n !== undefined) paintFaces();
        return;
      case 'follow':
        if (m.t === 'on') S.followers.add(from); else S.followers.delete(from);
        S.lastView = ''; paintFaces(); return;
      case 'ptr': if (m.t === 'l' && m.s) gotLaser(from, m); return;
      case 'chat':
        if (m.t === 'm' && m.text) {
          S.chat.push({ who: nameOf(from), text: String(m.text).slice(0, 300), from, t: clock() });
          const seen = S.sheet === 'chat' || (wide() && S.sideTab === 'chat');
          if (!seen) { S.unread++; say(nameOf(from) + ': ' + String(m.text).slice(0, 80), { icon: 'chat' }); }
          if (S.sheet === 'chat') { openSheet('chat'); openSheet('chat'); }
          paintSide(); paintBar();
        }
        return;
      case 'sys':
        if (m.t === 'hi' && isFinite(m.j)) { const had = joinedTs.has(from); joinedTs.set(from, +m.j); if (!m.re) send('sys', { t: 'hi', j: joinedTs.get(me), re: 1 }, true, [from]); if (!had) { S.pen.clear(); sync(); } }
        else if (m.t === 'summon') gotSummon(from, m.room);
        else if (m.t === 'end' && from === hostId()) leave(true);
        return;
    }
  });
  let peopleT = 0;
  function sync() {
    const before = new Map([...S.people].map(([id, p]) => [id, p.name || '']));
    const list = tr.participants();
    for (const p of [...list.filter((x) => !x.local), ...list.filter((x) => x.local)]) if (!S.seen.has(p.id)) S.seen.set(p.id, S.seen.size);
    S.people = new Map(list.map((p) => [p.id, p]));
    for (const p of sorted()) if (!S.pen.has(p.id)) S.pen.set(p.id, S.pen.size);
    for (const [id, p] of S.people) if (p.name) S.names.set(id, p.name);
    for (const id of [...S.followers]) if (!S.people.has(id)) S.followers.delete(id);
    if (S.following && !S.people.has(S.following)) { S.following = null; S.target = null; }
    paintFaces(); paintBar(); paintSide();
    if (S.sheet === 'people' || S.sheet === 'invite') { const k = S.sheet; clearTimeout(peopleT); peopleT = setTimeout(() => { if (S.sheet === k) { openSheet(k); openSheet(k); } }, 60); }
    if (S.state === 'connected' && before.size) {
      for (const [id, p] of S.people) if (!before.has(id) && id !== me) say(T.joined(p.name || T.guest), { icon: 'person' });
      for (const [id, n] of before) if (!S.people.has(id) && id !== me && S.state === 'connected') { stats.left++; say(T.left(n || T.guest)); }
    }
  }
  tr.onParticipants(() => { if (S.alive) sync(); });
  const spkOff = new Map();
  tr.onSpeaking((ids) => {
    const now2 = new Set(ids || []);
    for (const id of now2) { clearTimeout(spkOff.get(id)); spkOff.delete(id); S.speaking.add(id); }
    for (const id of [...S.speaking]) if (!now2.has(id) && !spkOff.has(id)) spkOff.set(id, setTimeout(() => { spkOff.delete(id); S.speaking.delete(id); paintFaces(); }, 800));
    paintFaces();
  });
  tr.onQuality((id, q) => {
    S.quality[id] = q;
    if (id === me) {
      if (q === 'poor' || q === 'lost') { S.poorSince = S.poorSince || Date.now(); }
      else { S.poorSince = 0; }
    }
    paintFaces();
  });
  every(() => { if (S.poorSince && Date.now() - S.poorSince > 10000 && !S.voice) setVoice(true, true); }, 1000);
  tr.onState((s) => {
    if (!S.alive) return;
    if (s === 'audio-blocked') { banner('audio'); return; }
    const was = S.state; S.state = s;
    if (s === 'reconnecting') { if (!S.wasRe) { S.wasRe = true; S.recAt = Date.now(); banner('reconnect'); say(T.reconnectToast, { dark: true, ms: 5000 }); } }
    else if (s === 'connected') {
      if (S.wasRe || was === 'disconnected') { S.wasRe = false; S.recAt = 0; banner(S.voiceAuto ? 'weak' : null); const src = hostId() !== me ? hostId() : (sorted().find((p) => p.id !== me) || {}).id; if (src) askSnap(src); else { const q = S.queue.splice(0); for (const op of q) sendOp(op, true, null); } }
    } else if (s === 'disconnected') { S.recAt = S.recAt || Date.now(); banner('lost'); }
    paintFaces(); paintBar();
  });

  /* ---------------- the controls hide after 4 s on a phone ---------------- */
  let hideT = 0;
  function wake() { S.lastTouch = Date.now(); if (S.barHidden) { S.barHidden = false; layout(); } armHide(); }
  function armHide() {
    clearTimeout(hideT);
    hideT = setTimeout(() => {
      if (!S.alive || wide() || S.down || S.sheet || S.min || S.state !== 'connected' || opts.autoHide === false) { if (S.alive && !wide()) armHide(); return; }
      S.barHidden = true; layout();
      if (!S.hinted) { S.hinted = true; say(T.controlsHint, { dark: true }); }
    }, HIDE_MS);
  }
  every(() => { if (faces.get(me) && S.lay === 'a') paintFaces(); }, 2500); // my own disc folds into "אני" after 10 s

  /* ---------------- buttons ---------------- */
  $('mic').onclick = () => toggleMic();
  $('cam').onclick = () => toggleCam();
  $('follow').onclick = () => { if (S.following) stopFollow(false); else { const others = sorted().filter((p) => p.id !== me); if (others.length === 1) follow(others[0].id); else if (S.lostFollow) follow(S.lostFollow); else openSheet('people'); } };
  $('point').onclick = () => { S.pointMode = !S.pointMode; if (S.pointMode) { say(T.pointHint, { ms: 4500 }); if (S.lay === 'a' && !wide()) setLay('b', 'hand'); } paintBar(); };
  $('invite').onclick = () => openSheet('invite');
  $('more').onclick = () => openSheet('more');
  $('leave').onclick = () => openSheet('leave');
  $('back').onclick = () => { S.min = true; closeSheet(); layout(); };
  $('mini').onclick = () => { S.min = false; layout(); paintFaces(); };
  $('pill').onclick = () => { S.peek = Date.now() + 5000; paintFaces(); setTimeout(() => paintFaces(), 5100); };
  $('swap').onclick = () => { S.swapped = !S.swapped; S.pinned = true; layout(); };
  $('modelback').onclick = () => setLay('a', 'hand');
  ui.querySelectorAll('.ndo-seg button').forEach((b) => (b.onclick = () => setLay(b.dataset.lay, 'hand')));
  on(document, 'keydown', (ev) => { // desktop shortcuts: M mic, V camera, F follow
    if (!wide() || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const tg = ev.composedPath()[0]; if (tg && (tg.tagName === 'INPUT' || tg.tagName === 'TEXTAREA' || tg.isContentEditable)) return;
    const k = ev.key.toLowerCase();
    if (k === 'm') toggleMic(); else if (k === 'v') toggleCam(); else if (k === 'f') $('follow').click();
  });

  /* ---------------- leaving, ending, the summary ---------------- */
  async function endForAll() { send('sys', { t: 'end' }, true); await new Promise((r) => setTimeout(r, 120)); leave(); }
  async function leave(ended) {
    if (!S.alive) return;
    closeSheet();
    for (const k of S.mine) send('hold', { t: 'off', k }, true);
    if (S.following) send('follow', { t: 'off' }, true, [S.following]);
    const peopleN = Math.max(S.pen.size, S.people.size), changes = S.changes.slice(), after = planEl() ? planEl().cloneNode(true) : null;
    S.alive = false;
    await new Promise((r) => setTimeout(r, 60));
    try { await tr.disconnect(); } catch (e) { /* already gone */ }
    store.setGuard(null); offStore(); offs.forEach((f) => f()); timers.forEach((f) => f()); if (ro) ro.disconnect();
    clearTimeout(toastT); clearTimeout(hideT); clearTimeout(S.backT); clearTimeout(undoT); clearInterval(recT); clearInterval(sumT);
    ui.remove(); audioBox.remove(); stageInk(null);
    if (root && prev) { root.style.top = prev.top; root.style.bottom = prev.bottom; root.style.insetInlineEnd = prev.end; root.classList.remove('ndc-in', 'ndc-lay-a', 'ndc-lay-b', 'ndc-lay-c', 'ndc-swapped', 'ndc-wide'); }
    summary({ peopleN, changes, after, ended: !!ended });
    if (opts.onLeave) opts.onLeave(api);
  }
  function summary(o) {
    const el = document.createElement('section'); el.className = 'ndo-end'; el.dir = T.dir; el.lang = lang; el.setAttribute('role', 'dialog'); el.setAttribute('aria-labelledby', 'ndo-end-t');
    const mins = Math.max(1, Math.round((Date.now() - S.startedAt) / 60000));
    const last = new Map(); for (const c of o.changes) last.set(c.by + '|' + c.key, c);
    const byP = new Map(); for (const c of last.values()) { if (!byP.has(c.by)) byP.set(c.by, []); byP.get(c.by).push(c); }
    const lines = [...byP.entries()].flatMap(([by, cs]) => cs.slice(-6).map((c) => '<li style="--pen:' + penOf(by) + '"><b>' + esc((T.chg[c.op] || c.op) + ': ' + objName(c.key)) + '</b><small>' + esc(by === me ? (person(me) && person(me).name) || T.me : nameOf(by)) + '</small></li>'));
    const txt = T.endSummary + '\n' + [...last.values()].map((c) => '· ' + (T.chg[c.op] || c.op) + ': ' + objName(c.key)).join('\n');
    el.innerHTML = '<div class="ndo-endin"><p class="ndo-meta">' + esc(T.endMeta(clock(), mins, o.peopleN)) + '</p><h2 id="ndo-end-t">' + T.endTitle + '</h2>' +
      '<div class="ndo-ba"><figure data-ndc="bef"><figcaption>' + T.before + '</figcaption></figure><figure data-ndc="aft"><figcaption>' + T.after + '</figcaption></figure></div>' +
      '<ul class="ndo-chg">' + (lines.join('') || '<li class="ndo-none">' + T.noChanges + '</li>') + '</ul>' +
      '<div class="ndo-endbtns"><a class="ndo-btn ndo-pri ndo-wide" data-ndc="share" href="https://wa.me/?text=' + encodeURIComponent(txt) + '" target="_blank" rel="noopener">' + oi('chat', 20) + '<span>' + T.endShare + '</span></a>' +
      '<button type="button" class="ndo-btn ndo-wide" data-ndc="alone">' + T.endAlone + '</button><p class="ndo-fine">' + T.endFine + '</p></div></div>';
    const put = (k, svgN) => { if (!svgN) return; svgN.removeAttribute('style'); svgN.setAttribute('aria-hidden', 'true'); el.querySelector('[data-ndc="' + k + '"]').prepend(svgN); };
    put('bef', beforeSvg ? beforeSvg.cloneNode(true) : null); put('aft', o.after);
    shadow.appendChild(el);
    el.querySelector('[data-ndc="alone"]').onclick = () => { el.remove(); try { designer.toast(T.endToast); } catch (e) { /* none */ } };
  }

  const api = {
    stats, ready, el: ui, mode: 'open',
    get pen() { return { holder: null, seq: 0, mine: false }; },
    get following() { return !!S.following; }, get followingId() { return S.following; },
    get state() { return S.state; }, get editor() { const h = liveHolds()[0]; return h ? h[1].by : null; },
    get alive() { return S.alive; }, get layout() { return S.lay; }, get controlsHinted() { return S.hinted; }, get host() { return hostId(); },
    get holds() { return [...S.holds.entries()].filter(([, h]) => fresh(h)).map(([k, h]) => ({ key: k, by: h.by })); },
    participants: () => [...S.people.values()],
    give: () => false, ask: () => false, hand: () => false,
    follow, leave: (o) => leave(o === true), endForAll, chat, inviteLink, waLink, summon: summonAll, undoMine, setLayout: (k) => setLay(k, 'hand'), wake, setVoice,
    openPanel(k) { if (!k) closeSheet(); else openSheet(k === 'invite' ? 'invite' : k === 'leave' ? 'leave' : 'more'); },
    summary() { const r = (a) => (a == null ? null : Math.round(a * 10) / 10); return { op_p50: r(pct(stats.op, 50)), op_p95: r(pct(stats.op, 95)), op_n: stats.op.length, view_p95: r(pct(stats.view, 95)), refused: stats.refused, ignored: stats.ignored, resync: stats.resync, snap: stats.snap }; },
  };

  /* ---------------- connect ---------------- */
  S.state = 'connecting'; layout(); sync();
  await tr.connect(); // a transport the newcomer already connected (to receive the apartment) resolves at once
  S.state = 'connected';
  joinedTs.set(me, opts.role === 'host' ? Date.now() - 1 : Date.now());
  send('sys', { t: 'hi', j: joinedTs.get(me) }, true);
  sync();
  // the camera and the microphone stay OFF unless the person turned them on in the sheet
  if (opts.mic === true) await toggleMic(true);
  if (opts.camera === true) await toggleCam(true);
  if ((S.micBlocked || S.camBlocked) && !S.mic) say(T.listen, { link: T.permLink, onLink: () => openSheet('perm'), ms: 7000 });
  try { if (tr.room && !tr.room.canPlaybackAudio) banner('audio'); } catch (e) { /* none */ }
  if (navigator.getBattery) navigator.getBattery().then((b) => { const chk = () => { if (S.alive && !S.battAsked && !b.charging && b.level < 0.2) { S.battAsked = true; openSheet('battery', Math.round(b.level * 100)); } }; chk(); b.addEventListener('levelchange', chk); }).catch(() => {});
  layout(); paintBar(); armHide();
  readyRes(api);
  return api;
}

/* ================================================================ LiveKit transport */

/** The production transport: livekit-client loaded from the CDN only now (after the join click), token from together.php. */
export function livekitTransport({ url, token, lib = LK_LIB, chunk = 4000 }) { // chunk in characters: 4000 Hebrew characters stay under the 15 KiB limit as UTF-8
  let LK = null, room = null, facing = 'user', people2 = () => {};
  const L = { data: new Set(), parts: new Set(), quality: new Set(), speaking: new Set(), state: new Set() };
  const fire = (k, ...a) => L[k].forEach((f) => { try { f(...a); } catch (e) { /* a listener failed: the call goes on */ } });
  const audios = new Map(), parts = new Map();
  const enc = new TextEncoder(), dec = new TextDecoder();
  const roleOf = (p) => { try { const a = p.attributes && p.attributes.role; if (a) return a; return JSON.parse(p.metadata || '{}').role || 'buyer'; } catch (e) { return 'buyer'; } };
  // together.php's roles (rep, buyer, partner, friend, designer, engineer, lawyer) in the call's four groups
  const GROUP = { rep: 'rep', buyer: 'buyer', partner: 'family', friend: 'family', family: 'family', designer: 'designer', engineer: 'designer', lawyer: 'designer', host: 'host', guest: 'guest' };
  const view = (p, local) => ({
    id: p.identity, name: p.name || '', role: GROUP[roleOf(p)] || 'buyer', local,
    mic: !!p.isMicrophoneEnabled, cam: !!p.isCameraEnabled, screen: !!p.isScreenShareEnabled, quality: p.connectionQuality || 'unknown', speaking: !!p.isSpeaking,
    joined: p.joinedAt && p.joinedAt.getTime ? p.joinedAt.getTime() : 0, // join order: the first one in is the host, pen colours follow it
  });
  let videoIn = true; // voice only: other people's video is paused (the call keeps the sound)
  const videoPubs = (fn) => { if (!room) return; for (const p of room.remoteParticipants.values()) for (const pub of p.trackPublications.values()) if (pub.kind === 'video' && pub.setEnabled) { try { fn(pub); } catch (e) { /* not subscribed yet */ } } };
  const T = {
    kind: 'livekit',
    async connect() {
      if (room) return; // already in the room (the newcomer connects first to receive the apartment)
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
      people2 = people;
      room
        .on(E.ParticipantConnected, people).on(E.ParticipantDisconnected, people)
        .on(E.ParticipantMetadataChanged, people).on(E.ParticipantAttributesChanged, people)
        .on(E.TrackPublished, people).on(E.TrackUnpublished, people)
        .on(E.TrackSubscribed, (track, pub, p) => { if (track.kind === 'audio') { const el = track.attach(); el.hidden = true; document.body.appendChild(el); audios.set(track.sid, el); } else if (!videoIn && pub.setEnabled) pub.setEnabled(false); people(); })
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
      const pub = (bytes) => { const r = room.localParticipant.publishData(bytes, opt); if (r && r.catch) r.catch(() => {}); }; // a message to someone who just left is dropped quietly
      if (!o.reliable || s.length <= chunk) { pub(enc.encode(s)); return true; }
      const id = Math.random().toString(36).slice(2, 10), n = Math.ceil(s.length / chunk); // 15 KiB is the reliable limit: split
      for (let i = 0; i < n; i++) pub(enc.encode(JSON.stringify({ __c: id, i, n, d: s.slice(i * chunk, (i + 1) * chunk) })));
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
    level(id) { if (!room) return 0; const p = id === room.localParticipant.identity ? room.localParticipant : room.remoteParticipants.get(id); return p ? p.audioLevel || 0 : 0; },
    setVideoReceive(on) { videoIn = !!on; videoPubs((pub) => pub.setEnabled(videoIn)); },
    async reconnect() { if (!room) return T.connect(); if (room.state === 'connected') return; try { await room.disconnect(); } catch (e) { /* already apart */ } await room.connect(url, token); fire('state', 'connected'); people2(); },
    onQuality: (f) => L.quality.add(f), onSpeaking: (f) => L.speaking.add(f), onState: (f) => L.state.add(f),
    get room() { return room; },
  };
  return T;
}

/* ================================================================ the start and join sheet, and the apartment for a newcomer */

const SHEET = {
  he: { dir: 'rtl', startH: 'שיחת וידאו על הדירה',
    startSub: (n) => 'מזמינים את מי שצריך ומעצבים יחד את ' + (n ? 'דירת ' + n + ' החדרים' : 'הדירה') + '. כולם רואים את אותה תוכנית בזמן אמת.',
    joinH: 'להצטרף לשיחה על הדירה', joinSub: (h) => (h ? h + ' מזמין אותך. ' : '') + 'נכנסים עם מצלמה כבויה, ומפעילים כשרוצים.',
    name: 'איך לקרוא לך?', start: 'להתחיל שיחה', join: 'כניסה', note: 'השיחה לא מוקלטת. הדפדפן יבקש רשות למצלמה ולמיקרופון רק כשתלחצו.', close: 'סגירה', notNow: 'לא עכשיו',
    cam: 'מצלמה', camSub: 'אפשר לכבות בכל רגע', mic: 'מיקרופון', micSub: 'אפשר להשתיק בכל רגע', meter: 'דברו, והקו זז. כך יודעים שישמעו אתכם.', you: 'התמונה שלך',
    blocked: 'הדפדפן לא נתן גישה. אפשר להיכנס כמאזין ולאשר אחר כך.',
    noName: 'כתבו שם כדי שהאחרים ידעו מי בשיחה.', wait: 'מתחברים לשיחה…', waitPlan: 'מקבלים את הדירה ממי שבשיחה…', empty: 'עוד אין אף אחד בשיחה. מחכים למי שהזמין אתכם…',
    fail: 'לא הצלחנו להתחבר לשיחה. נסו שוב בעוד רגע.', off: 'שיחת וידאו לא זמינה כרגע.', full: 'השיחה מלאה, 8 מתוך 8', gone: 'השיחה הזו כבר הסתיימה.', rate: 'נפתחו הרבה שיחות בזמן קצר. נסו שוב בעוד כמה דקות.',
    noPlan: 'לא קיבלנו את הדירה ממי שבשיחה. נסו להיכנס שוב מהקישור.' },
  en: { dir: 'ltr', startH: 'Video call about the apartment',
    startSub: (n) => 'Invite whoever you need and design ' + (n ? 'the ' + n + '-room apartment' : 'the apartment') + ' together. Everyone sees the same plan live.',
    joinH: 'Join the call about the apartment', joinSub: (h) => (h ? h + ' invited you. ' : '') + 'You join with the camera off and turn it on when you like.',
    name: 'What should we call you?', start: 'Start the call', join: 'Join', note: 'The call is not recorded. The browser asks for camera and mic only when you tap.', close: 'Close', notNow: 'Not now',
    cam: 'Camera', camSub: 'Turn it off any time', mic: 'Microphone', micSub: 'Mute any time', meter: 'Speak and the line moves. That\'s how you know they\'ll hear you.', you: 'Your picture',
    blocked: 'The browser did not allow it. You can join as a listener and allow it later.',
    noName: 'Write a name so the others know who is in the call.', wait: 'Connecting…', waitPlan: 'Receiving the apartment from the call…', empty: 'Nobody is in the call yet. Waiting for the person who invited you…',
    fail: 'Could not connect to the call. Please try again shortly.', off: 'Video calls are not available right now.', full: 'The call is full, 8 of 8', gone: 'This call has already ended.', rate: 'Many calls were opened in a short time. Please try again in a few minutes.',
    noPlan: 'The apartment did not arrive from the call. Please open the link again.' },
};
const NAME_KEY = 'nl-call-name';

/** The sheet that starts a call (mode 'start') or joins one from a link (mode 'join'). container sits in a shadow root.
 *  api.media = { mic, cam, blocked: { mic, cam } }: what the person switched on (both OFF by default). */
export async function callSheet(container, o = {}) {
  const T = SHEET[o.lang === 'en' ? 'en' : 'he'], shadow = container.getRootNode();
  import(o.lib || LK_LIB).catch(() => {}); // the call library starts loading while the visitor types a name (it was asked for: the call button)
  if (shadow && shadow.querySelector && shadow !== document) await ensureCss(shadow);
  const el = document.createElement('section');
  const join = o.mode === 'join';
  el.className = 'ndo-sheetwrap ndc-sheet'; el.dir = T.dir; el.lang = o.lang === 'en' ? 'en' : 'he'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-labelledby', 'ndc-sheet-h');
  const sw = (k, ic, label, sub) => '<label class="ndo-swrow"><span class="ndo-ric">' + oi(ic, 22) + '</span><span class="ndo-rt"><b>' + label + '</b><small>' + sub + '</small></span>' +
    '<input type="checkbox" role="switch" class="ndo-swin" data-ndc="' + k + '"><span class="ndo-sw" aria-hidden="true"><i></i></span></label>';
  el.innerHTML = '<div class="ndo-card ndo-entry"><div class="ndo-shh"><h2 id="ndc-sheet-h">' + (join ? T.joinH : T.startH) + '</h2>' +
    '<button type="button" class="ndo-x" data-ndc="x" aria-label="' + T.close + '" title="' + T.close + '">' + oi('x', 22) + '</button></div>' +
    '<p class="ndo-shsub">' + esc(join ? T.joinSub(o.host || '') : T.startSub(o.rooms || 0)) + '</p>' +
    '<div class="ndo-prev"><span class="ndo-pv" data-ndc="pv"><video playsinline autoplay muted></video>' + oi('person', 40) + '<small>' + T.you + '</small></span>' +
    '<span class="ndo-pm"><b>' + oi('mic', 18) + '<span data-ndc="mlabel">' + T.mic + '</span></b><span class="ndo-meter" data-ndc="meter">' + '<i></i>'.repeat(14) + '</span><small>' + T.meter + '</small></span></div>' +
    '<form data-ndc="form" novalidate><label class="ndo-lbl" for="ndc-name">' + T.name + '</label><input id="ndc-name" class="ndo-field" data-ndc="name" maxlength="40" autocomplete="given-name" enterkeyhint="go">' +
    sw('cam', 'cam', T.cam, T.camSub) + sw('mic', 'mic', T.mic, T.micSub) +
    '<button class="ndo-btn ndo-pri ndo-wide ndo-big" data-ndc="go" type="submit"><span>' + (join ? T.join : T.start) + '</span></button></form>' +
    '<p class="ndo-fine">' + T.note + '</p><p class="ndo-msg" data-ndc="msg" role="status" aria-live="polite"></p>' +
    (join ? '<button type="button" class="ndo-btn ndo-plain ndo-wide" data-ndc="no">' + T.notNow + '</button>' : '') + '</div>';
  container.appendChild(el);
  const $ = (k) => el.querySelector('[data-ndc="' + k + '"]'), input = $('name');
  let saved = ''; try { saved = localStorage.getItem(NAME_KEY) || ''; } catch (e) { saved = ''; }
  input.value = o.name || saved || '';
  const msg = (t, bad) => { $('msg').textContent = t || ''; $('msg').classList.toggle('ndo-bad', !!bad); };
  const media = { mic: false, cam: false, blocked: { mic: false, cam: false } };
  let vStream = null, aStream = null, actx = null, meterT = 0, busy = false;
  const stopV = () => { if (vStream) vStream.getTracks().forEach((t) => t.stop()); vStream = null; const v = $('pv').querySelector('video'); v.srcObject = null; $('pv').classList.remove('ndo-on'); };
  const stopA = () => { cancelAnimationFrame(meterT); if (aStream) aStream.getTracks().forEach((t) => t.stop()); aStream = null; if (actx) actx.close().catch(() => {}); actx = null; $('meter').querySelectorAll('i').forEach((i) => i.classList.remove('ndo-lit')); };
  const stopAll = () => { stopV(); stopA(); };
  async function wantCam(onv) {
    media.cam = onv; if (!onv) { stopV(); return; }
    try { vStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } }); const v = $('pv').querySelector('video'); v.srcObject = vStream; v.play().catch(() => {}); $('pv').classList.add('ndo-on'); media.blocked.cam = false; }
    catch (e) { media.cam = false; media.blocked.cam = true; $('cam').checked = false; msg(T.blocked, true); }
  }
  async function wantMic(onv) {
    media.mic = onv; if (!onv) { stopA(); return; }
    try {
      aStream = await navigator.mediaDevices.getUserMedia({ audio: true }); media.blocked.mic = false;
      const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
      actx = new AC(); const an = actx.createAnalyser(); an.fftSize = 512; actx.createMediaStreamSource(aStream).connect(an);
      const buf = new Uint8Array(an.fftSize), bars = [...$('meter').querySelectorAll('i')];
      const loop = () => { an.getByteTimeDomainData(buf); let s = 0; for (const b of buf) s += ((b - 128) / 128) ** 2; const lvl = Math.min(1, Math.sqrt(s / buf.length) * 6), n = Math.round(lvl * bars.length); bars.forEach((b, i) => b.classList.toggle('ndo-lit', i < n)); meterT = requestAnimationFrame(loop); };
      loop();
    } catch (e) { media.mic = false; media.blocked.mic = true; $('mic').checked = false; msg(T.blocked, true); }
  }
  $('cam').onchange = () => wantCam($('cam').checked);
  $('mic').onchange = () => wantMic($('mic').checked);
  const api = {
    el, msg, media,
    close() { stopAll(); el.remove(); },
    busy(on, t) { busy = !!on; $('go').disabled = busy; input.disabled = busy; if (t !== undefined) msg(t); },
    error(code) { api.busy(false); msg(T[code] || T.fail, true); },
    release: stopAll, // the preview hands the camera and the microphone back before the call takes them
    T,
  };
  const closeIt = () => { stopAll(); if (o.onClose) o.onClose(); el.remove(); };
  $('x').onclick = closeIt;
  if ($('no')) $('no').onclick = closeIt;
  el.addEventListener('keydown', (ev) => { if (ev.key === 'Escape' && !busy) closeIt(); });
  $('form').onsubmit = async (ev) => {
    ev.preventDefault();
    if (busy) return;
    const name = input.value.replace(/\s+/g, ' ').trim().slice(0, 40);
    if (!name) { msg(T.noName, true); input.focus(); return; }
    try { localStorage.setItem(NAME_KEY, name); } catch (e) { /* storage blocked: the name lasts for this call */ }
    stopAll();
    api.busy(true, T.wait);
    try { await o.onGo(name, api); } catch (e) { api.error(e && e.code ? e.code : 'fail'); }
  };
  setTimeout(() => { try { if (!input.value) input.focus({ preventScroll: true }); } catch (e) { /* none */ } }, 30);
  return api;
}

/**
 * A newcomer (opened the invite link) is in the room but has no apartment yet: ask the people in the call, one at a time,
 * for the plan and the design. Resolves { plan, design, title, unitLabel, mine, from, ms }; rejects { code: 'noPlan' } after timeoutMs.
 */
export function receivePlan(tr, o = {}) {
  const t0 = now(), every = o.everyMs || 2500, limit = o.timeoutMs || 90000;
  return new Promise((resolve, reject) => {
    let done = false, k = 0, timer = 0;
    const finish = (fn, v) => { if (done) return; done = true; clearInterval(timer); fn(v); };
    tr.onData((topic, m, from) => {
      if (done || topic !== 'plan' || !m || m.t !== 'plan' || !m.plan || typeof m.plan !== 'object') return;
      finish(resolve, { plan: m.plan, design: m.design && typeof m.design === 'object' ? m.design : null, title: String(m.title || '').slice(0, 80), unitLabel: String(m.unitLabel || '').slice(0, 80), mine: !!m.mine, from, ms: Math.round(now() - t0) });
    });
    const ask = () => {
      if (done) return;
      if (now() - t0 > limit) { finish(reject, { code: 'noPlan' }); return; }
      const others = tr.participants().filter((p) => !p.local);
      if (!others.length) { if (o.onStatus) o.onStatus('empty'); return; }
      if (o.onStatus) o.onStatus('waitPlan');
      others.sort((a, b) => (a.role === 'host') - (b.role === 'host') || String(a.id).localeCompare(String(b.id))).reverse(); // the one who opened the call first
      const to = others[k++ % others.length];
      tr.publishData('plan', { t: 'ask', at: now() }, { reliable: true, to: [to.id] });
    };
    tr.onParticipants(() => { if (!done && !k) ask(); });
    timer = setInterval(ask, every);
    ask();
  });
}