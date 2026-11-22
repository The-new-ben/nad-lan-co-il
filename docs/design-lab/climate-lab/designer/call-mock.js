// A stand-in transport for the designer's call (HAD-706): the same interface as livekitTransport in call.js, built on a
// BroadcastChannel, so several tabs of ONE browser form a room with no server. Video tiles are drawn on a canvas and sent
// through captureStream, so the page handles them exactly like real video. For local checks only; never loaded on the site.
//   mockTransport({ room, identity, name, role, loss: 0 })   loss = share of lossy messages dropped (0..1), to test the view topic

const COLORS = { buyer: '#1F5FA8', rep: '#0F2233', designer: '#1C7A4E', family: '#46596A' };

export function mockTransport({ room, identity, name = '', role = 'buyer', loss = 0 }) {
  const id = String(identity);
  const L = { data: new Set(), parts: new Set(), quality: new Set(), speaking: new Set(), state: new Set() };
  const fire = (k, ...a) => L[k].forEach((f) => { try { f(...a); } catch (e) { console.error(e); } });
  const me = { id, name, role, local: true, mic: false, cam: false, screen: false, quality: 'excellent', speaking: false };
  const peers = new Map(); // id -> { ...view, seen }
  const timers = [];
  let ch = null, alive = false, facing = 'user', spk = new Set();
  const post = (m) => { if (ch) ch.postMessage(JSON.stringify({ ...m, src: id })); };
  const info = () => ({ k: 'here', p: { id, name, role, mic: me.mic, cam: me.cam, screen: me.screen, speaking: me.speaking } });
  const streams = new Map();

  function canvasStream(pid, label, colour) { // a moving picture so the tile is a real playing video element
    const c = document.createElement('canvas'); c.width = 160; c.height = 120;
    const g = c.getContext('2d'); let n = 0;
    const draw = () => { g.fillStyle = colour; g.fillRect(0, 0, 160, 120); g.fillStyle = '#F2F5F7'; g.font = '700 48px "IBM Plex Sans Hebrew",Arial'; g.textAlign = 'center'; g.fillText(label, 80, 76); g.fillRect((n++ * 4) % 160, 112, 24, 4); };
    draw(); const t = setInterval(draw, 120); timers.push(() => clearInterval(t));
    return c.captureStream ? c.captureStream(8) : null;
  }

  const T = {
    kind: 'mock',
    async connect() {
      fire('state', 'connecting');
      ch = new BroadcastChannel('ndc-mock-' + room); alive = true;
      ch.onmessage = (ev) => {
        let m; try { m = JSON.parse(ev.data); } catch (e) { return; }
        if (!alive || m.src === id) return;
        if (m.k === 'hi') { post(info()); }
        if (m.k === 'hi' || m.k === 'here') {
          const had = peers.get(m.src), p = m.p || { id: m.src };
          const nv = { id: m.src, name: p.name || '', role: p.role || 'buyer', local: false, mic: !!p.mic, cam: !!p.cam, screen: !!p.screen, quality: 'excellent', speaking: !!p.speaking, seen: Date.now() };
          const changed = !had || had.mic !== nv.mic || had.cam !== nv.cam || had.screen !== nv.screen || had.name !== nv.name || had.speaking !== nv.speaking;
          peers.set(m.src, nv);
          if (!had) fire('quality', m.src, 'excellent');
          if (nv.speaking) spk.add(m.src); else spk.delete(m.src);
          if (changed) { fire('parts'); fire('speaking', [...spk]); }
        }
        if (m.k === 'bye') { if (peers.delete(m.src)) { spk.delete(m.src); fire('parts'); } }
        if (m.k === 'd') {
          if (m.to && !m.to.includes(id)) return;
          if (!m.reliable && loss > 0 && Math.random() < loss) return;
          fire('data', m.topic, m.obj, m.src);
        }
      };
      post({ k: 'hi', p: info().p });
      const hb = setInterval(() => {
        post(info());
        const t = Date.now(); let gone = false;
        for (const [k, p] of peers) if (t - p.seen > 5000) { peers.delete(k); gone = true; }
        if (gone) fire('parts');
      }, 1000);
      timers.push(() => clearInterval(hb));
      // a person "speaks" now and then while the microphone is on (active-speaker highlight)
      const talk = setInterval(() => {
        const s = me.mic && Math.random() < 0.35;
        if (s !== me.speaking) { me.speaking = s; if (s) spk.add(id); else spk.delete(id); post(info()); fire('speaking', [...spk]); }
      }, 1300);
      timers.push(() => clearInterval(talk));
      const onHide = () => post({ k: 'bye' });
      addEventListener('pagehide', onHide); timers.push(() => removeEventListener('pagehide', onHide));
      await new Promise((r) => setTimeout(r, 40));
      fire('state', 'connected'); fire('quality', id, 'excellent'); fire('parts');
    },
    async disconnect() {
      alive = false; post({ k: 'bye' });
      timers.forEach((f) => f()); timers.length = 0;
      streams.forEach((s) => s.getTracks().forEach((t) => t.stop())); streams.clear();
      if (ch) ch.close(); ch = null; peers.clear();
      fire('state', 'disconnected');
    },
    publishData(topic, obj, o = {}) {
      if (!alive) return false;
      post({ k: 'd', topic, obj: JSON.parse(JSON.stringify(obj)), reliable: !!o.reliable, to: o.to || null });
      return true;
    },
    onData: (f) => L.data.add(f),
    participants: () => [{ ...me }, ...[...peers.values()].map(({ seen, ...p }) => p)],
    onParticipants: (f) => L.parts.add(f),
    async setMicrophone(on) { me.mic = !!on; post(info()); fire('parts'); },
    async setCamera(on) { me.cam = !!on; post(info()); fire('parts'); },
    async switchCamera() { facing = facing === 'user' ? 'environment' : 'user'; fire('parts'); return facing; },
    async shareScreen(on) { me.screen = !!on; post(info()); fire('parts'); },
    attach(pid, kind, el) {
      const p = pid === id ? me : peers.get(pid); if (!p) return false;
      const key = pid + ':' + kind;
      let s = streams.get(key);
      if (!s) { s = canvasStream(pid, kind === 'screen' ? '▭' : (p.name || p.role || '?').charAt(0), kind === 'screen' ? '#46596A' : COLORS[p.role] || '#1F5FA8'); if (!s) return false; streams.set(key, s); }
      el.srcObject = s; el.muted = true; const pr = el.play && el.play(); if (pr && pr.catch) pr.catch(() => {});
      return true;
    },
    startAudio() {},
    onQuality: (f) => L.quality.add(f), onSpeaking: (f) => L.speaking.add(f), onState: (f) => L.state.add(f),
    // for checks: a dropped and restored connection
    async simulateReconnect(ms = 800) { fire('state', 'reconnecting'); await new Promise((r) => setTimeout(r, ms)); fire('state', 'connected'); },
  };
  return T;
}
