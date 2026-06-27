#!/usr/bin/env node
import { mkdirSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';

const ROOT = process.cwd();
const DEFAULT_OUT = 'docs/qa/ashira-full-preflight-report.json';

function argValue(name, fallback) {
	const index = process.argv.indexOf(name);
	if (index === -1) return fallback;
	const value = process.argv[index + 1];
	return value && !value.startsWith('--') ? value : fallback;
}

function resolve(file) {
	return path.resolve(ROOT, file);
}

function npmBin() {
	return process.platform === 'win32' ? 'npm.cmd' : 'npm';
}

function npmCommand(script) {
	if (process.platform === 'win32') {
		return {
			command: 'cmd.exe',
			args: ['/d', '/s', '/c', 'npm', 'run', script],
		};
	}
	return {
		command: npmBin(),
		args: ['run', script],
	};
}

function clip(text, limit = 1800) {
	const value = String(text || '').trim();
	return value.length > limit ? `${value.slice(0, limit)}\n... [truncated ${value.length - limit} chars]` : value;
}

function runScript(script) {
	const started = Date.now();
	const npm = npmCommand(script);
	const result = spawnSync(npm.command, npm.args, {
		cwd: ROOT,
		encoding: 'utf8',
		shell: false,
		env: process.env,
		timeout: 300000,
	});
	return {
		script,
		ok: result.status === 0,
		exit_code: result.status,
		error: result.error ? result.error.message : '',
		timed_out: result.error?.code === 'ETIMEDOUT',
		duration_ms: Date.now() - started,
		stdout: clip(result.stdout),
		stderr: clip(result.stderr),
	};
}

const outFile = argValue('--out', DEFAULT_OUT);
const groups = [
	{
		name: 'research_and_architecture',
		scripts: [
			'qa:ashira-research-dossier',
			'qa:ashira-i18n-architecture',
		],
	},
	{
		name: 'content_depth',
		scripts: [
			'qa:ashira-content-depth',
			'qa:ashira-en-content-depth',
			'qa:ashira-fr-content-depth',
			'qa:ashira-ru-content-depth',
			'qa:ashira-ar-content-depth',
		],
	},
	{
		name: 'visual_showroom_screenshots',
		scripts: [
			'qa:showroom-v2-preview',
			'qa:showroom-v2-en-preview',
			'qa:showroom-v2-fr-preview',
			'qa:showroom-v2-ru-preview',
			'qa:showroom-v2-ar-preview',
		],
	},
	{
		name: 'project_factory_and_import',
		scripts: [
			'qa:ashira-factory-readiness',
			'qa:ashira-draft-readiness',
			'build:project-hreflang-artifact',
			'qa:project-hreflang-artifact',
			'qa:project-draft-import-dry-run',
			'qa:project-publication-readiness',
			'qa:ashira-publication-readiness',
		],
	},
	{
		name: 'homepage_dependency',
		scripts: [
			'qa:home-showroom-pattern',
			'qa:home-showroom-preview',
			'qa:home-chrome',
			'qa:home-seo-schema',
			'qa:home-publication-readiness',
		],
	},
	{
		name: 'next_project_factory',
		scripts: [
			'qa:project-factory-smoke',
		],
	},
];

const started = new Date();
const results = [];
let stoppedAt = '';

for (const group of groups) {
	for (const script of group.scripts) {
		const result = { group: group.name, ...runScript(script) };
		results.push(result);
		if (!result.ok) {
			stoppedAt = script;
			break;
		}
	}
	if (stoppedAt) break;
}

const failed = results.filter((item) => !item.ok);
const report = {
	ok: failed.length === 0,
	generated_at: new Date().toISOString(),
	started_at: started.toISOString(),
	duration_ms: Date.now() - started.getTime(),
	mode: 'preflight-only-no-wordpress-import-no-live-deploy',
	total_scripts: results.length,
	stopped_at: stoppedAt,
	failed: failed.map((item) => item.script),
	results,
};

mkdirSync(path.dirname(resolve(outFile)), { recursive: true });
writeFileSync(resolve(outFile), `${JSON.stringify(report, null, 2)}\n`, 'utf8');

console.log(JSON.stringify({
	ok: report.ok,
	failures: failed.length,
	total_scripts: results.length,
	out: outFile,
	stopped_at: stoppedAt,
}, null, 2));

if (process.argv.includes('--strict') && failed.length) {
	process.exitCode = 1;
}
