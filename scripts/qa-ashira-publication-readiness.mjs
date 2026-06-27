#!/usr/bin/env node
import { spawnSync } from 'node:child_process';

const args = [
	'scripts/qa-project-publication-readiness.mjs',
	'--manifest',
	'docs/plans/2026-06-27-ashira-publication-manifest.json',
	'--out',
	'docs/qa/ashira-publication-readiness-report.json',
	...process.argv.slice(2),
];

const result = spawnSync(process.execPath, args, {
	stdio: 'inherit',
	shell: false,
});

if (typeof result.status === 'number') {
	process.exit(result.status);
}

if (result.error) {
	console.error(result.error);
}

process.exit(1);
