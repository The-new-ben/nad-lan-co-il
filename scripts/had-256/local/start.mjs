#!/usr/bin/env node
/**
 * HAD-256 local bench: WordPress Playground sites (SQLite, PHP 8.3, 6 workers), synthetic data only, 127.0.0.1 only.
 *
 *   node scripts/had-256/local/start.mjs after              # the builder's site: this worktree's code, hot, :9401
 *   node scripts/had-256/local/start.mjs before             # the base code of 6e9cf930, for before/after runs, :9411
 *   node scripts/had-256/local/start.mjs qa <commit> [port] # a PINNED QA snapshot of <commit> (default port 9402):
 *        an immutable `git archive` copy of that commit (plugin modules + bench mu-plugin + loopback preload),
 *        its own SQLite site, its own mail sink, its own QA accounts (qa.a / qa.b @example.test). Never updated in
 *        place: a newer slice gets a new port (9403, 9404, ...).
 *   node scripts/had-256/local/start.mjs theme [commit] [port] # open item 4: <commit> (default 2ce0a741) inside the site's
 *        REAL theme (nadlan-revenue + nadlan-platform-child, the child's platform.css = live bytes) and the REAL
 *        nadlan-config plugin, with the live Code Snippets; default port 9405 (9401-9404 refused). See docs/qa/had-256/theme.
 *   add --fresh (after/before/theme) to throw the site away and install again
 *
 * Nothing here touches nad-lan.co.il: the sites live under scripts/had-256/local/.runtime/ (git-ignored), every
 * outbound HTTP request from PHP is blocked, every email goes to wp-content/mail-sink/*.json, AI is off, and every
 * listen() of the bench processes is pinned to 127.0.0.1 (loopback.cjs; the CLI has no bind option).
 */
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '..', '..', '..');
const RUNTIME = path.join(HERE, '.runtime');
const BASE_COMMIT = '6e9cf930';
const CLI = '@wp-playground/cli@3.1.56';
const WP = '7.1.2';
const MODULES = ['broker-drop.php', 'owner-wizard.php', 'funnel.php', 'auth.php', 'property-owner.php', 'conversion-cta.php'];

const args = process.argv.slice(2);
const fresh = args.includes('--fresh');
const mode = args[0] || 'after';

function fwd(p) { return p.split(path.sep).join('/'); }

function plan() {
  if (mode === 'after') {
    const root = path.join(RUNTIME, 'after');
    return { name: 'after', port: 9401, root, site: path.join(root, 'site'), code: path.join(REPO, 'plugins', 'nadlan-config', 'inc'), mu: path.join(HERE, 'mu-plugins'), loop: path.join(HERE, 'loopback.cjs'), seed: path.join(HERE, 'seed.json'), label: 'this worktree (hot)', allowFresh: true };
  }
  if (mode === 'private') {
    // the new code with the draft photos OUTSIDE the web root: NL_OWNER_PRIVATE_DIR=/nl-private (a host folder mounted
    // beside /wordpress, never under it, so no URL reaches it), its own site, 127.0.0.1:9431
    const root = path.join(RUNTIME, 'private');
    fs.mkdirSync(path.join(root, 'outside'), { recursive: true });
    return { name: 'private', port: 9431, root, site: path.join(root, 'site'), code: path.join(REPO, 'plugins', 'nadlan-config', 'inc'), mu: path.join(HERE, 'mu-plugins'), loop: path.join(HERE, 'loopback.cjs'), seed: path.join(HERE, 'seed.json'), label: 'this worktree, private photos outside the web root', allowFresh: true,
      extra: ['--mount-dir', fwd(path.join(root, 'outside')), '/nl-private', '--define', 'NL_OWNER_PRIVATE_DIR', '/nl-private'] };
  }
  if (mode === 'before') {
    const root = path.join(RUNTIME, 'before');
    const code = path.join(root, 'code');
    fs.mkdirSync(code, { recursive: true });
    for (const m of MODULES) {
      fs.writeFileSync(path.join(code, m), execFileSync('git', ['-C', REPO, 'show', `${BASE_COMMIT}:plugins/nadlan-config/inc/${m}`], { maxBuffer: 64 * 1024 * 1024 }));
    }
    return { name: 'before', port: 9411, root, site: path.join(root, 'site'), code, mu: path.join(HERE, 'mu-plugins'), loop: path.join(HERE, 'loopback.cjs'), seed: path.join(HERE, 'seed.json'), label: BASE_COMMIT + ' (base)', allowFresh: true };
  }
  if (mode === 'roll') {
    // L17 rollback drill: ONE site (its own data), started with the new code or with the base code of 6e9cf930
    const codeOf = args[1] === 'before' ? 'before' : 'after';
    const root = path.join(RUNTIME, 'roll');
    fs.mkdirSync(root, { recursive: true });
    let code = path.join(REPO, 'plugins', 'nadlan-config', 'inc');
    if (codeOf === 'before') {
      code = path.join(root, 'code-before');
      fs.mkdirSync(code, { recursive: true });
      for (const m of MODULES) {
        fs.writeFileSync(path.join(code, m), execFileSync('git', ['-C', REPO, 'show', `${BASE_COMMIT}:plugins/nadlan-config/inc/${m}`], { maxBuffer: 64 * 1024 * 1024 }));
      }
    }
    return { name: 'roll-' + codeOf, port: 9421, root, site: path.join(root, 'site'), code, mu: path.join(HERE, 'mu-plugins'), loop: path.join(HERE, 'loopback.cjs'), seed: path.join(HERE, 'seed.json'), label: codeOf === 'before' ? BASE_COMMIT + ' (rolled back)' : 'this worktree', allowFresh: true };
  }
  if (mode === 'qa') {
    const commit = (args[1] || '').trim();
    if (!/^[0-9a-f]{7,40}$/.test(commit)) { throw new Error('usage: start.mjs qa <commit> [port]'); }
    const port = Number(args[2] || 9402);
    const root = path.join(RUNTIME, 'qa-' + commit);
    const snap = path.join(root, 'snapshot');
    if (!fs.existsSync(snap)) {
      fs.mkdirSync(snap, { recursive: true });
      // every file of those paths, byte for byte as committed (git show; no checkout, no index change)
      const files = execFileSync('git', ['-C', REPO, 'ls-tree', '-r', '--name-only', commit, 'plugins/nadlan-config/inc', 'scripts/had-256/local/mu-plugins', 'scripts/had-256/local/loopback.cjs']).toString().split('\n').filter(Boolean);
      for (const f of files) {
        const dst = path.join(snap, ...f.split('/'));
        fs.mkdirSync(path.dirname(dst), { recursive: true });
        fs.writeFileSync(dst, execFileSync('git', ['-C', REPO, 'show', `${commit}:${f}`], { maxBuffer: 64 * 1024 * 1024 }));
      }
      // the QA accounts: local-only synthetic test credentials (also in docs/qa/had-256/QA-SNAPSHOT.md)
      fs.writeFileSync(path.join(root, 'qa-seed.json'), JSON.stringify({
        _note: 'HAD-256 QA snapshot ' + commit + ': synthetic accounts for a local Playground site on 127.0.0.1 only.',
        users: [
          { key: 'qa_a', login: 'qa_a', email: 'qa.a@example.test', name: 'קיו איי', password: 'QA-Local-A-2026!', role: 'subscriber' },
          { key: 'qa_b', login: 'qa_b', email: 'qa.b@example.test', name: 'קיו בי', password: 'QA-Local-B-2026!', role: 'subscriber' },
          { key: 'qa_admin', login: 'qa_admin', email: 'qa.admin@example.test', name: 'QA Admin', password: 'QA-Local-Admin-2026!', role: 'administrator' },
        ],
        whatsapp_stub: '972000000000',
      }, null, 1));
    }
    return { name: 'qa-' + commit, port, root, site: path.join(root, 'site'), code: path.join(snap, 'plugins', 'nadlan-config', 'inc'), mu: path.join(snap, 'scripts', 'had-256', 'local', 'mu-plugins'), loop: path.join(snap, 'scripts', 'had-256', 'local', 'loopback.cjs'), seed: path.join(root, 'qa-seed.json'), label: 'pinned ' + commit, allowFresh: false };
  }
  if (mode === 'theme') {
    // open item 4: the code of <commit> inside the site's REAL theme (nadlan-revenue + nadlan-platform-child) and the REAL
    // nadlan-config plugin, with the live Code Snippets (x-skin-a 638 as read live; x-broker-drop, x-broker-join 699 and
    // x-owner-wizard 707 from <commit>). A pinned git-archive copy, its own SQLite site; never ports 9401-9404.
    const commit = (args[1] || '2ce0a741').trim();
    if (!/^[0-9a-f]{7,40}$/.test(commit)) { throw new Error('usage: start.mjs theme <commit> [port]'); }
    const port = Number(args[2] || 9405);
    if (port >= 9401 && port <= 9404) { throw new Error('ports 9401-9404 are the pinned QA / builder benches; use 9405+'); }
    const root = path.join(RUNTIME, 'theme-' + commit);
    const snap = path.join(root, 'snapshot');
    if (!fs.existsSync(path.join(snap, '.complete'))) {
      fs.rmSync(snap, { recursive: true, force: true });
      fs.mkdirSync(snap, { recursive: true });
      const unpack = (dest, paths) => {
        fs.mkdirSync(dest, { recursive: true });
        const tar = path.join(dest, 'nlj-part.tar');
        execFileSync('git', ['-C', REPO, '-c', 'core.autocrlf=false', 'archive', '--format=tar', '-o', tar, commit, '--', ...paths]);   // LF bytes, as committed (and as the live snippets hold them)
        // relative names in the tar's own folder: GNU tar reads "C:\..." as a remote host
        execFileSync('tar', ['-xf', 'nlj-part.tar'], { cwd: dest });
        fs.rmSync(tar);
      };
      // the parent theme is the repo root (style.css "Theme Name: NadLan Revenue"); only its theme files
      unpack(path.join(snap, 'nadlan-revenue'), ['style.css', 'style.min.css', 'functions.php', 'theme.json', 'screenshot.png', 'readme.txt', 'templates', 'parts', 'patterns', 'styles', 'assets']);
      unpack(snap, ['plugins/nadlan-config', 'themes/nadlan-platform-child', 'scripts/had-256/local/mu-plugins', 'scripts/had-256/local/loopback.cjs', 'scripts/had-256/local/seed.json', 'scripts/broker-drop/pages/post-listing-he.html', 'docs/qa/v8-traffic/x-skin-a-638.20261002T201851Z.live.php']);
      // the child's platform.css: the LIVE public bytes (the repo copy differs from live; docs/qa/had-256/theme/live-ref)
      fs.copyFileSync(path.join(REPO, 'docs', 'qa', 'had-256', 'theme', 'live-ref', 'platform.css'), path.join(snap, 'themes', 'nadlan-platform-child', 'assets', 'css', 'platform.css'));
      // the live Code Snippets (Code Snippets stores them without the opening tag; a required file needs it)
      const sn = path.join(snap, 'snippets');
      fs.mkdirSync(sn, { recursive: true });
      const inc = path.join(snap, 'plugins', 'nadlan-config', 'inc');
      fs.writeFileSync(path.join(sn, 'x-skin-a-638.php'), '<?php\n' + fs.readFileSync(path.join(snap, 'docs', 'qa', 'v8-traffic', 'x-skin-a-638.20261002T201851Z.live.php'), 'utf8'));
      fs.copyFileSync(path.join(inc, 'broker-drop.php'), path.join(sn, 'x-broker-drop.php'));
      fs.copyFileSync(path.join(inc, 'broker-join.php'), path.join(sn, 'x-broker-join-699.php'));
      fs.copyFileSync(path.join(inc, 'owner-wizard.php'), path.join(sn, 'x-owner-wizard-707.php'));
      // the bench helpers of <commit> without its stubs, its module loader and its font link (the real plugin, the real
      // snippets and the skin load those here); every cut is anchored and checked
      const mu = path.join(snap, 'mu');
      fs.mkdirSync(mu, { recursive: true });
      let b = fs.readFileSync(path.join(snap, 'scripts', 'had-256', 'local', 'mu-plugins', 'nlj-bench.php'), 'utf8');
      const cut = (from, to) => {
        const i = b.indexOf(from), j = b.indexOf(to, i + 1);
        if (i < 0 || j < 0 || b.indexOf(from, i + 1) >= 0) { throw new Error('nlj-bench.php anchor not found once: ' + from.slice(0, 50)); }
        b = b.slice(0, i) + b.slice(j);
      };
      cut('/* ---------------- stubs ---------------- */', '/* ---------------- nothing leaves the machine ---------------- */');
      cut("/* the design system's two families", '/* ---------------- the synthetic site ---------------- */');
      b = b.replace('<?php\n', '<?php\n/* DERIVED by start.mjs theme from nlj-bench.php of ' + commit + ': stubs, module loader and font link cut (the real plugin, snippets and skin are loaded). */\n');
      fs.writeFileSync(path.join(mu, 'nlj-bench.php'), b);
      fs.copyFileSync(path.join(HERE, 'theme', 'nlj-theme.php'), path.join(mu, 'nlj-theme.php'));
      fs.writeFileSync(path.join(snap, '.complete'), new Date().toISOString() + ' ' + commit + '\n');
    }
    const site = path.join(root, 'site');
    return { name: 'theme-' + commit, port, root, site, code: path.join(snap, 'plugins', 'nadlan-config', 'inc'), mu: path.join(snap, 'mu'), loop: path.join(snap, 'scripts', 'had-256', 'local', 'loopback.cjs'), seed: path.join(snap, 'scripts', 'had-256', 'local', 'seed.json'), label: 'theme bench ' + commit, allowFresh: true,
      theme: { liveText: path.join(snap, 'scripts', 'broker-drop', 'pages', 'post-listing-he.html'), skin: path.join(snap, 'nadlan-revenue', 'assets', 'skin-a', 'skin-a.css') },
      extra: ['--mount-dir', fwd(path.join(snap, 'plugins', 'nadlan-config')), '/wordpress/wp-content/plugins/nadlan-config',
        '--mount-dir', fwd(path.join(snap, 'nadlan-revenue')), '/wordpress/wp-content/themes/nadlan-revenue',
        '--mount-dir', fwd(path.join(snap, 'themes', 'nadlan-platform-child')), '/wordpress/wp-content/themes/nadlan-platform-child',
        '--mount-dir', fwd(path.join(snap, 'snippets')), '/wordpress/wp-content/nlj-snippets'] };
  }
  throw new Error('mode: after | before | qa <commit> [port] | theme <commit> [port]');
}

function afterInstall(p) {
  const wc = path.join(p.site, 'wp-content');
  if (!fs.existsSync(wc)) { return false; }
  fs.writeFileSync(path.join(wc, 'nlj-variant.txt'), p.name);
  if (!fs.existsSync(path.join(wc, 'nlj-seed.json')) || p.allowFresh) { fs.copyFileSync(p.seed, path.join(wc, 'nlj-seed.json')); }
  fs.mkdirSync(path.join(wc, 'mail-sink'), { recursive: true });
  if (p.theme) {
    // the live page text of /post-listing/ (4958) and the skin's stylesheet where x-skin-a links it (uploads/nadlan-skin)
    fs.copyFileSync(p.theme.liveText, path.join(wc, 'nlj-post-listing.html'));
    fs.mkdirSync(path.join(wc, 'uploads', 'nadlan-skin'), { recursive: true });
    fs.copyFileSync(p.theme.skin, path.join(wc, 'uploads', 'nadlan-skin', 'skin-a.css'));
    // the copy variants of page 4958 (docs/qa/had-256/page-4958): POST /nlj-test/v1/page {variant: old|A|B}
    for (const [v, f] of [['old', 'old.html'], ['A', 'new-A.html'], ['B', 'new-B.html']]) {
      const src = path.join(REPO, 'docs', 'qa', 'had-256', 'page-4958', f);
      if (fs.existsSync(src)) { fs.copyFileSync(src, path.join(wc, 'nlj-page-' + v + '.html')); }
    }
  }
  // PHP notices go to wp-content/debug.log, never to the page
  const cfg = path.join(p.site, 'wp-config.php');
  if (fs.existsSync(cfg)) {
    const txt = fs.readFileSync(cfg, 'utf8');
    if (txt.includes("define( 'WP_DEBUG', false );")) {
      fs.writeFileSync(cfg, txt.replace("define( 'WP_DEBUG', false );", "define( 'WP_DEBUG', true );\ndefine( 'WP_DEBUG_LOG', true );\ndefine( 'WP_DEBUG_DISPLAY', false );"));
    }
  }
  return true;
}

const p = plan();
if (fresh && p.allowFresh && fs.existsSync(p.site)) { fs.rmSync(p.site, { recursive: true, force: true }); }
fs.mkdirSync(p.site, { recursive: true });
const installed = fs.existsSync(path.join(p.site, 'wp-config.php'));
if (installed) { afterInstall(p); }
const log = fs.openSync(path.join(p.root, 'server.log'), 'a');
const cliArgs = ['-y', CLI, 'server', '--port', String(p.port), '--php', '8.3', '--wp', WP, '--workers', '6',
  '--wordpress-install-mode', installed ? 'install-from-existing-files-if-needed' : 'download-and-install',
  '--mount-dir-before-install', fwd(p.site), '/wordpress',
  '--mount-dir', fwd(p.mu), '/wordpress/wp-content/mu-plugins',
  '--mount-dir', fwd(p.code), '/wordpress/wp-content/nlj-code'].concat(p.extra || []);
const env = Object.assign({}, process.env, { NODE_OPTIONS: ((process.env.NODE_OPTIONS || '') + ' --require "' + fwd(p.loop) + '"').trim() });
const child = spawn(process.platform === 'win32' ? 'npx.cmd' : 'npx', cliArgs, { cwd: REPO, env, stdio: ['ignore', 'pipe', 'pipe'], shell: process.platform === 'win32' });
const onData = (buf) => {
  fs.writeSync(log, buf);
  const s = buf.toString();
  if (/Ready!/.test(s)) {
    afterInstall(p);
    console.log(`[${p.name}] ready: http://127.0.0.1:${p.port}/post-listing/   (code: ${p.label})`);
  }
  if (/Error|error:/i.test(s) && !/lockWholeFile/.test(s)) { process.stdout.write(`[${p.name}] ${s}`); }
};
child.stdout.on('data', onData);
child.stderr.on('data', onData);
child.on('exit', (c) => { console.log(`[${p.name}] stopped (${c})`); process.exit(0); });
const stop = () => { try { child.kill(); } catch (e) { /* gone */ } process.exit(0); };
process.on('SIGINT', stop);
process.on('SIGTERM', stop);
