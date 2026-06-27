import fs from 'node:fs/promises';
import path from 'node:path';

function usage() {
	return `Usage:
  node scripts/build-project-showroom-draft.mjs --pattern patterns/project-showroom-ashira-v2.php --slug ashira-sde-dov --title "Ashira Sde Dov" --yoast-title "Ashira Sde Dov - בחירת דירה ומודל תלת ממד" --yoast-description "Ashira Sde Dov בשדה דב: בחירת דירה על חזית הפרויקט, מודל תלת ממד, נתוני דירה ואומדן לא מחייב עד אימות מול היזם." --focus-keyword "Ashira Sde Dov" --out docs/wp-drafts/ashira-sde-dov-v2-draft.json

Builds a WordPress REST draft payload from a theme showroom pattern.
The payload is safe to inspect and import later. It does not contact WordPress.`;
}

function parseArgs(argv) {
	const args = {
		pattern: '',
		slug: '',
		title: '',
		out: '',
		site: 'https://nad-lan.co.il',
		theme: 'nadlan-revenue',
		status: 'draft',
		typeEndpoint: '/wp-json/wp/v2/nadlan_project',
		yoastTitle: '',
		yoastDescription: '',
		focusKeyword: '',
		expectedLanguage: 'he',
	};
	for (let i = 2; i < argv.length; i += 1) {
		const arg = argv[i];
		if (arg === '--pattern') args.pattern = argv[++i] || '';
		else if (arg === '--slug') args.slug = argv[++i] || '';
		else if (arg === '--title') args.title = argv[++i] || '';
		else if (arg === '--out') args.out = argv[++i] || '';
		else if (arg === '--site') args.site = (argv[++i] || args.site).replace(/\/+$/, '');
		else if (arg === '--theme') args.theme = argv[++i] || args.theme;
		else if (arg === '--status') args.status = argv[++i] || args.status;
		else if (arg === '--type-endpoint') args.typeEndpoint = argv[++i] || args.typeEndpoint;
		else if (arg === '--yoast-title') args.yoastTitle = argv[++i] || '';
		else if (arg === '--yoast-description') args.yoastDescription = argv[++i] || '';
		else if (arg === '--focus-keyword') args.focusKeyword = argv[++i] || '';
		else if (arg === '--expected-language') args.expectedLanguage = argv[++i] || args.expectedLanguage;
		else if (arg === '--help' || arg === '-h') {
			console.log(usage());
			process.exit(0);
		} else {
			throw new Error(`Unknown argument: ${arg}`);
		}
	}
	for (const key of ['pattern', 'slug', 'title', 'out']) {
		if (!args[key]) throw new Error(`Missing --${key}`);
	}
	if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(args.slug)) {
		throw new Error('Slug must be ASCII lowercase words separated by hyphens.');
	}
	return args;
}

function extractWpHtmlBlock(patternSource) {
	const start = patternSource.indexOf('<!-- wp:html -->');
	const endMarker = '<!-- /wp:html -->';
	const end = patternSource.indexOf(endMarker);
	if (start < 0 || end < 0 || end <= start) {
		throw new Error('Pattern does not contain a wp:html block.');
	}
	return patternSource.slice(start, end + endMarker.length);
}

function fillRuntimeValues(content, args) {
	const assetBase = `${args.site}/wp-content/themes/${args.theme}/assets/projects/${args.slug}/`;
	return content
		.replace(/<\?php echo esc_url\( \$asset_base \. '([^']+)' \); \?>/g, (_m, file) => `${assetBase}${file}`)
		.replace(/<\?php echo esc_url\( rest_url\( 'nadlan\/v1\/lead' \) \); \?>/g, `${args.site}/wp-json/nadlan/v1/lead`);
}

function publicTextChecks(payload, args) {
	const raw = JSON.stringify(payload);
	const content = typeof payload.content === 'string' ? payload.content : payload.content && payload.content.raw ? payload.content.raw : '';
	const errors = [];
	if (args.expectedLanguage === 'he' && !/[\u0590-\u05FF]/.test(raw)) errors.push('payload has no Hebrew text');
	if (args.expectedLanguage !== 'he' && !/[A-Za-z]/.test(raw)) errors.push('payload has no Latin text');
	if (/[\u00c2\u00c3]/.test(raw)) errors.push('payload contains mojibake markers');
	if (/לידים|פאנל|משפך|CRM|funnel|lead panel|monetization|paid placement/i.test(raw)) {
		errors.push('payload leaks internal/public-inappropriate wording');
	}
	if (!content.includes('data-nlps-showroom') && !content.includes('data-nlv2-showroom')) errors.push('missing supported showroom root marker');
	if (!content.includes('/wp-json/nadlan/v1/lead')) errors.push('missing lead endpoint');
	return errors;
}

const args = parseArgs(process.argv);
const patternPath = path.resolve(args.pattern);
const pattern = await fs.readFile(patternPath, 'utf8');
const rawContent = fillRuntimeValues(extractWpHtmlBlock(pattern), args);
const seoTitle = args.yoastTitle || `${args.title} - בחירת דירה, מודל תלת ממד ומידע למשקיעים`;
const seoDescription = args.yoastDescription || `${args.title}: בחירת דירה על חזית הפרויקט, מודל תלת ממד ומידע למשפחות ולמשקיעים. הנתונים להמחשה עד אימות מול היזם.`;
const focusKeyword = args.focusKeyword || args.title;

const payload = {
	endpoint: `${args.site}${args.typeEndpoint}`,
	method: 'POST',
	body: {
		status: args.status,
		slug: args.slug,
		title: args.title,
		content: rawContent,
		comment_status: 'closed',
		ping_status: 'closed',
		meta: {
			_yoast_wpseo_title: seoTitle,
			_yoast_wpseo_metadesc: seoDescription,
			_yoast_wpseo_focuskw: focusKeyword,
			_yoast_wpseo_is_cornerstone: '0',
		},
	},
	notes: [
		'Create as draft first. Do not publish until official BIM/GLB, inventory, prices, plans, contact details, and legal/public-copy approval exist.',
		'If the REST endpoint differs on live, inspect /wp-json/wp/v2/types/nadlan_project before applying.',
		`After applying, import assets/projects/${args.slug}/showroom-payload.json only after a real post ID exists.`,
	],
};

const errors = publicTextChecks(payload.body, args);
if (errors.length) {
	throw new Error(`Draft payload failed checks:\n${errors.map((e) => `- ${e}`).join('\n')}`);
}

await fs.mkdir(path.dirname(path.resolve(args.out)), { recursive: true });
await fs.writeFile(path.resolve(args.out), `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
	ok: true,
	out: args.out,
	endpoint: payload.endpoint,
	status: payload.body.status,
	slug: payload.body.slug,
	content_chars: payload.body.content.length,
	meta_fields: Object.keys(payload.body.meta).length,
}, null, 2));
