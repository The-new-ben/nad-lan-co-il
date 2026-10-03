#!/usr/bin/env node
/**
 * HAD-256 local bench: one command, two WordPress Playground sites (SQLite, PHP 8.3, 6 workers), synthetic data only.
 *
 *   node scripts/had-256/local/start.mjs            # both: AFTER (this worktree's code) on :9401, BEFORE (6e9cf930) on :9402
 *   node scripts/had-256/local/start.mjs after      # only the new code (the preview Maya tests)
 *   node scripts/had-256/local/start.mjs before     # only the base code, for before/after comparisons
 *   add --fresh to throw the sites away and install again
 *
 * Nothing here touches nad-lan.co.il: the sites live under scripts/had-256/local/.runtime/ (git-ignored), every
 * outbound HTTP request from PHP is blocked, every email goes to wp-content/mail-sink/*.json, AI is off.
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
const PORTS = { after: 9401, before: 9402 };

const args = process.argv.slice(2);
const fresh = args.includes('--fresh');
const which = args.find((a) => a === 'after' || a === 'before');
const variants = which ? [which] : ['after', 'before'];

function fwd(p) { return p.split(path.sep).join('/'); }

function prepare(variant) {
  const root = path.join(RUNTIME, variant);
  const site = path.join(root, 'site');
  if (fresh && fs.existsSync(site)) { fs.rmSync(site, { recursive: true, force: true }); }
  fs.mkdirSync(site, { recursive: true });
  let code = path.join(REPO, 'plugins', 'nadlan-config', 'inc');
  if (variant === 'before') {
    code = path.join(root, 'code');
    fs.mkdirSync(code, { recursive: true });
    for (const m of MODULES) {
      const txt = execFileSync('git', ['-C', REPO, 'show', `${BASE_COMMIT}:plugins/nadlan-config/inc/${m}`], { maxBuffer: 64 * 1024 * 1024 });
      fs.writeFileSync(path.join(code, m), txt);
    }
  }
  return { root, site, code };
}

function afterInstall(variant, site) {
  const wc = path.join(site, 'wp-content');
  if (!fs.existsSync(wc)) { return false; }
  fs.writeFileSync(path.join(wc, 'nlj-variant.txt'), variant);
  fs.copyFileSync(path.join(HERE, 'seed.json'), path.join(wc, 'nlj-seed.json'));
  fs.mkdirSync(path.join(wc, 'mail-sink'), { recursive: true });
  // PHP notices go to wp-content/debug.log, never to the page
  const cfg = path.join(site, 'wp-config.php');
  if (fs.existsSync(cfg)) {
    const txt = fs.readFileSync(cfg, 'utf8');
    if (txt.includes("define( 'WP_DEBUG', false );")) {
      fs.writeFileSync(cfg, txt.replace("define( 'WP_DEBUG', false );", "define( 'WP_DEBUG', true );\ndefine( 'WP_DEBUG_LOG', true );\ndefine( 'WP_DEBUG_DISPLAY', false );"));
    }
  }
  return true;
}

function start(variant) {
  const { root, site, code } = prepare(variant);
  const installed = fs.existsSync(path.join(site, 'wp-config.php'));
  if (installed) { afterInstall(variant, site); }
  const port = PORTS[variant];
  const log = fs.openSync(path.join(root, 'server.log'), 'a');
  const cliArgs = ['-y', CLI, 'server', '--port', String(port), '--php', '8.3', '--wp', WP, '--workers', '6',
    '--wordpress-install-mode', installed ? 'install-from-existing-files-if-needed' : 'download-and-install',
    '--mount-dir-before-install', fwd(site), '/wordpress',
    '--mount-dir', fwd(path.join(HERE, 'mu-plugins')), '/wordpress/wp-content/mu-plugins',
    '--mount-dir', fwd(code), '/wordpress/wp-content/nlj-code'];
  // loopback only: the CLI has no bind option, so every listen() in its processes is pinned to 127.0.0.1
  const env = Object.assign({}, process.env, { NODE_OPTIONS: ((process.env.NODE_OPTIONS || '') + ' --require "' + fwd(path.join(HERE, 'loopback.cjs')) + '"').trim() });
  const child = spawn(process.platform === 'win32' ? 'npx.cmd' : 'npx', cliArgs, { cwd: REPO, env, stdio: ['ignore', 'pipe', 'pipe'], shell: process.platform === 'win32' });
  const onData = (buf) => {
    fs.writeSync(log, buf);
    const s = buf.toString();
    if (/Ready!/.test(s)) {
      afterInstall(variant, site);
      console.log(`[${variant}] ready: http://127.0.0.1:${port}/post-listing/   (code: ${variant === 'after' ? 'this worktree' : BASE_COMMIT})`);
    }
    if (/Error|error:/i.test(s) && !/lockWholeFile/.test(s)) { process.stdout.write(`[${variant}] ${s}`); }
  };
  child.stdout.on('data', onData);
  child.stderr.on('data', onData);
  child.on('exit', (c) => { console.log(`[${variant}] stopped (${c})`); });
  return child;
}

const kids = variants.map(start);
const stop = () => { for (const k of kids) { try { k.kill(); } catch (e) { /* gone */ } } process.exit(0); };
process.on('SIGINT', stop);
process.on('SIGTERM', stop);
