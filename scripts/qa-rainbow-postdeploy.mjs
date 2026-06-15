import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const DEFAULT_SITE = 'https://nad-lan.co.il';
const DEFAULT_SLUG = 'rainbow-tel-aviv';
const DEFAULT_POST_ID = 4464;
const DEFAULT_VERSION = '1.66.3';

function parseArgs(argv) {
  const args = {
    site: DEFAULT_SITE,
    slug: DEFAULT_SLUG,
    postId: DEFAULT_POST_ID,
    version: DEFAULT_VERSION,
    out: '',
    visual: true,
    skipPackage: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--site') args.site = argv[++i] || args.site;
    else if (arg === '--slug') args.slug = argv[++i] || args.slug;
    else if (arg === '--post-id') args.postId = Number(argv[++i] || 0) || args.postId;
    else if (arg === '--version') args.version = argv[++i] || args.version;
    else if (arg === '--out') args.out = argv[++i] || args.out;
    else if (arg === '--no-visual') args.visual = false;
    else if (arg === '--skip-package') args.skipPackage = true;
    else if (arg === '--help' || arg === '-h') {
      console.log(`Usage:
  node scripts/qa-rainbow-postdeploy.mjs --version 1.66.3 --out docs/qa/rainbow-postdeploy-1.66.3.json
  node scripts/qa-rainbow-postdeploy.mjs --no-visual

Runs the post-deploy Rainbow template gate in the correct order:
1. local package verifier,
2. live structural showroom QA,
3. strict template gate with visual Chrome QA unless --no-visual is passed.

This script does not deploy anything. It proves whether the public page is ready to clone.`);
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  args.site = args.site.replace(/\/+$/, '');
  if (!args.out) args.out = `docs/qa/rainbow-postdeploy-${args.version}.json`;
  return args;
}

function runStep(name, command, stepArgs) {
  const started = new Date().toISOString();
  const proc = spawnSync(command, stepArgs, {
    encoding: 'utf8',
  });
  return {
    name,
    command: [command, ...stepArgs].join(' '),
    started_at: started,
    exit_code: proc.status,
    ok: proc.status === 0,
    stdout_tail: String(proc.stdout || '').slice(-5000),
    stderr_tail: String(proc.stderr || '').slice(-5000),
  };
}

function main() {
  const args = parseArgs(process.argv);
  const report = {
    generated_at: new Date().toISOString(),
    site: args.site,
    slug: args.slug,
    post_id: args.postId,
    version: args.version,
    visual: args.visual,
    steps: [],
  };

  if (!args.skipPackage) {
    report.steps.push(runStep('local plugin package verifier', 'python', [
      'scripts/verify-plugin-release.py',
      args.version,
    ]));
  }

  report.steps.push(runStep('live structural showroom QA', process.execPath, [
    'scripts/qa-project-showroom-live.mjs',
    '--site',
    args.site,
    '--slug',
    args.slug,
    '--post-id',
    String(args.postId),
    '--min-version',
    args.version,
    '--strict',
  ]));

  const templateArgs = [
    'scripts/qa-project-template-gate.mjs',
    '--site',
    args.site,
    '--slug',
    args.slug,
    '--post-id',
    String(args.postId),
    '--min-version',
    args.version,
    '--strict',
    '--out',
    `docs/qa/rainbow-template-gate-live-${args.version}.json`,
  ];
  if (args.visual) templateArgs.push('--visual');
  report.steps.push(runStep('strict template readiness gate', process.execPath, templateArgs));

  report.ok = report.steps.every((step) => step.ok);
  report.summary = {
    passed: report.steps.filter((step) => step.ok).length,
    failed: report.steps.filter((step) => !step.ok).length,
    template_ready: report.ok,
  };

  fs.mkdirSync(path.dirname(args.out), { recursive: true });
  fs.writeFileSync(args.out, `${JSON.stringify(report, null, 2)}\n`);
  console.log(JSON.stringify(report, null, 2));
  if (!report.ok) process.exit(1);
}

main();
