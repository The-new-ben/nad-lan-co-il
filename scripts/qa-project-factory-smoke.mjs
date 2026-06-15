import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = process.cwd();

function parseArgs(argv) {
  const out = {
    slug: `codex-factory-smoke-${Date.now()}`,
    keep: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--slug') out.slug = argv[++i] || out.slug;
    else if (arg === '--keep') out.keep = true;
    else if (arg === '--help' || arg === '-h') {
      console.log(`Usage:
  node scripts/qa-project-factory-smoke.mjs
  node scripts/qa-project-factory-smoke.mjs --slug codex-temp-showroom --keep

Creates a temporary showroom project folder, builds showroom-payload.json, validates it, and removes
the folder unless --keep is passed. This proves the next-project factory path works without touching
WordPress or the live site.`);
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(out.slug)) {
    throw new Error('Smoke-test slug must be ASCII lowercase words separated by hyphens.');
  }
  return out;
}

function runStep(name, command, args) {
  const proc = spawnSync(command, args, {
    cwd: ROOT,
    encoding: 'utf8',
  });
  return {
    name,
    command: [path.basename(command), ...args].join(' '),
    exit_code: proc.status,
    ok: proc.status === 0,
    stdout_tail: String(proc.stdout || '').slice(-3000),
    stderr_tail: String(proc.stderr || '').slice(-3000),
  };
}

function main() {
  const args = parseArgs(process.argv);
  const folder = path.join(ROOT, 'assets', 'projects', args.slug);
  if (fs.existsSync(folder)) {
    throw new Error(`Smoke-test folder already exists: ${path.relative(ROOT, folder)}. Pick another --slug or remove it first.`);
  }

  const report = {
    generated_at: new Date().toISOString(),
    slug: args.slug,
    folder: path.relative(ROOT, folder).replace(/\\/g, '/'),
    keep: args.keep,
    steps: [],
  };
  const expectedFiles = [
    'source-notes.md',
    'unit-map.json',
    'drawings.json',
    'environment.json',
    'view-layer-config.json',
    'project-meta-example.json',
    'material-intake-template.json',
    'showroom-payload.json',
    'qa.md',
  ];

  try {
    report.steps.push(runStep('syntax check initializer', process.execPath, ['--check', 'scripts/init-project-showroom.mjs']));
    report.steps.push(runStep('init project showroom folder', process.execPath, [
      'scripts/init-project-showroom.mjs',
      args.slug,
      '--post-id',
      '0',
      '--title',
      'Codex Factory Smoke',
    ]));
    report.steps.push(runStep('build showroom payload', process.execPath, [
      'scripts/build-project-showroom-payload.mjs',
      args.slug,
      '--write',
    ]));
    report.steps.push(runStep('validate showroom payload', process.execPath, [
      'scripts/validate-project-showroom-payload.mjs',
      '--payload',
      `assets/projects/${args.slug}/showroom-payload.json`,
    ]));
    const missing = expectedFiles.filter((file) => !fs.existsSync(path.join(folder, file)));
    report.generated_files = expectedFiles.filter((file) => fs.existsSync(path.join(folder, file)));
    report.steps.push({
      name: 'expected scaffold files exist',
      command: `check ${path.relative(ROOT, folder).replace(/\\/g, '/')}`,
      exit_code: missing.length ? 1 : 0,
      ok: missing.length === 0,
      stdout_tail: missing.length ? '' : expectedFiles.join('\n'),
      stderr_tail: missing.length ? `Missing: ${missing.join(', ')}` : '',
    });
  } finally {
    if (!args.keep && fs.existsSync(folder)) {
      fs.rmSync(folder, { recursive: true, force: true });
      report.cleaned_up = true;
    }
  }

  report.expected_files = expectedFiles;
  report.summary = {
    passed: report.steps.filter((step) => step.ok).length,
    failed: report.steps.filter((step) => !step.ok).length,
    factory_ready: report.steps.every((step) => step.ok),
  };

  console.log(JSON.stringify(report, null, 2));
  if (!report.summary.factory_ready) process.exit(1);
}

try {
  main();
} catch (err) {
  console.error(err.message);
  process.exit(1);
}
