// nadlan-room-token: LiveKit entry tokens for nad-lan.co.il's shared viewing room (TogetherRoom, inc/together.php).
// Reuses this project's LiveKit secrets server-side; nobody outside the function ever sees them.
// The caller is nad-lan's WordPress server only: every request carries an HMAC (NADLAN_ROOM_SECRET) over room|identity|ts,
// fresh within five minutes. Rooms are confined to the "nadlan-" prefix, so this function can never open a courtroom.
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { AccessToken } from 'https://esm.sh/livekit-server-sdk@2.18.0';

const url = Deno.env.get('LIVEKIT_SERVER_URL') ?? '';
const key = Deno.env.get('LIVEKIT_API_KEY') ?? '';
const secret = Deno.env.get('LIVEKIT_API_SECRET') ?? '';
const shared = Deno.env.get('NADLAN_ROOM_SECRET') ?? '';
const ROLES = new Set(['rep', 'buyer', 'partner', 'friend', 'designer', 'engineer', 'lawyer']);
const enc = new TextEncoder();

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });

async function hmacHex(msg: string): Promise<string> {
  const k = await crypto.subtle.importKey('raw', enc.encode(shared), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = new Uint8Array(await crypto.subtle.sign('HMAC', k, enc.encode(msg)));
  return Array.from(sig, (b) => b.toString(16).padStart(2, '0')).join('');
}
function sameHex(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

serve(async (req) => {
  if (req.method !== 'POST') return json({ error: 'method' }, 405);
  if (!url || !key || !secret || shared.length < 32) return json({ error: 'not_configured' }, 503);
  const b = await req.json().catch(() => null) as Record<string, unknown> | null;
  if (!b) return json({ error: 'bad_json' }, 400);
  const room = String(b.room ?? ''), identity = String(b.identity ?? ''), role = String(b.role ?? 'buyer');
  const name = String(b.name ?? '').slice(0, 60), ts = Number(b.ts ?? 0), sig = String(b.sig ?? '').toLowerCase();
  if (!/^nadlan-[a-z0-9-]{4,80}$/i.test(room) || !/^[a-z0-9_-]{1,64}$/i.test(identity) || !ROLES.has(role)) return json({ error: 'bad_input' }, 400);
  if (!Number.isFinite(ts) || Math.abs(Date.now() / 1000 - ts) > 300) return json({ error: 'stale' }, 401);
  if (!sameHex(await hmacHex(`${room}|${identity}|${ts}`), sig)) return json({ error: 'signature' }, 401);
  const at = new AccessToken(key, secret, { identity, name, ttl: '2h', metadata: JSON.stringify({ role, site: 'nad-lan.co.il' }) });
  at.addGrant({ room, roomJoin: true, canPublish: true, canSubscribe: true, canPublishData: true });
  return json({ url, token: await at.toJwt() });
});
