#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const OUT_DIR = path.resolve('docs/qa/screenshots/showroom-destack-pr1');
const BASE_URL = process.env.NADLAN_BASE_URL || 'https://nad-lan.co.il';
const pages = [
	{ key: 'he', url: `${BASE_URL}/projects/ashira-sde-dov/?cb=destack-pr1`, expectLang: 'he' },
	{ key: 'en', url: `${BASE_URL}/projects/ashira-sde-dov-en/?cb=destack-pr1`, expectLang: 'en' },
];
const viewports = [
	{ key: 'desktop-1440', width: 1440, height: 1100, isMobile: false },
	{ key: 'mobile-390', width: 390, height: 900, isMobile: true },
];

fs.mkdirSync(OUT_DIR, { recursive: true });

function okLine(ok, name, detail = '') {
	return { ok, name, detail };
}

async function run() {
	const browser = await chromium.launch({
		channel: process.env.NADLAN_BROWSER_CHANNEL || 'chrome',
		headless: true,
	});
	const results = [];

	for (const vp of viewports) {
		const context = await browser.newContext({
			viewport: { width: vp.width, height: vp.height },
			deviceScaleFactor: vp.isMobile ? 2 : 1,
			isMobile: vp.isMobile,
			hasTouch: vp.isMobile,
			locale: 'he-IL',
		});

		for (const pageSpec of pages) {
			const page = await context.newPage();
			const errors = [];
			page.on('console', (msg) => {
				if (msg.type() === 'error') errors.push(msg.text());
			});
			page.on('pageerror', (err) => errors.push(err.message));

			await page.goto(pageSpec.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
			await page.waitForSelector('#nl-root', { timeout: 45000 });
			await page.waitForTimeout(2500);

			const metrics = await page.evaluate(() => {
				const article = document.querySelector('.nadlan-project-article.nadlan-guide');
				const h2 = article ? article.querySelector('h2') : null;
				const style = article ? getComputedStyle(article) : null;
				const h2Style = h2 ? getComputedStyle(h2) : null;
				return {
					lang: document.documentElement.lang || '',
					dir: document.documentElement.dir || '',
					nlv2Showroom: document.querySelectorAll('.nlv2-showroom').length,
					nlRoot: document.querySelectorAll('#nl-root').length,
					article: document.querySelectorAll('.nadlan-project-article.nadlan-guide').length,
					articleTextChars: article ? (article.innerText || '').trim().length : 0,
					articleFontSize: style ? style.fontSize : '',
					articleLineHeight: style ? style.lineHeight : '',
					h2Count: article ? article.querySelectorAll('h2').length : 0,
					h2FontFamily: h2Style ? h2Style.fontFamily : '',
					scrollWidth: document.documentElement.scrollWidth,
					clientWidth: document.documentElement.clientWidth,
				};
			});

			const checks = [
				okLine(metrics.nlv2Showroom === 0, '.nlv2-showroom count is 0', String(metrics.nlv2Showroom)),
				okLine(metrics.nlRoot === 1, '#nl-root count is 1', String(metrics.nlRoot)),
				okLine(metrics.article === 1, 'article wrapper exists once', String(metrics.article)),
				okLine(metrics.articleTextChars > 500, 'article preserved with real text', String(metrics.articleTextChars)),
				okLine(metrics.h2Count > 0, 'article headings render inside wrapper', String(metrics.h2Count)),
				okLine(!/^16px$/.test(metrics.articleFontSize), 'editorial article style applied', metrics.articleFontSize),
				okLine(metrics.scrollWidth <= metrics.clientWidth + 4, 'no horizontal overflow', `${metrics.scrollWidth}/${metrics.clientWidth}`),
				okLine(errors.length === 0, 'no browser console/page errors', errors.join(' | ')),
			];

			const screenshot = path.join(OUT_DIR, `${pageSpec.key}-${vp.key}.png`);
			await page.screenshot({ path: screenshot, fullPage: true });
			results.push({
				key: pageSpec.key,
				viewport: vp.key,
				url: pageSpec.url,
				screenshot,
				metrics,
				checks,
				ok: checks.every((check) => check.ok),
			});
			await page.close();
		}
		await context.close();
	}

	await browser.close();
	const report = {
		ok: results.every((result) => result.ok),
		generated_at: new Date().toISOString(),
		base_url: BASE_URL,
		results,
	};
	const reportPath = path.join(OUT_DIR, 'report.json');
	fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
	console.log(JSON.stringify({ ok: report.ok, reportPath, screenshots: results.map((r) => r.screenshot) }, null, 2));
	if (!report.ok) process.exit(2);
}

run().catch((err) => {
	console.error(err);
	process.exit(1);
});
