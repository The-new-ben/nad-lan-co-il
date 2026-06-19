import fs from 'node:fs/promises';
import path from 'node:path';

const repo = path.resolve('.');
const targetUrl = 'http://127.0.0.1:8765/docs/previews/dimri-yama-showroom-preview.html?cdp=mobile390';
const response = await fetch('http://127.0.0.1:9333/json/new?' + encodeURIComponent('about:blank'), { method: 'PUT' });
const target = await response.json();

if (!globalThis.WebSocket) {
	throw new Error('This Node runtime does not expose WebSocket');
}

const ws = new WebSocket(target.webSocketDebuggerUrl);
const pending = new Map();
let nextId = 1;

function send(method, params = {}) {
	return new Promise((resolve, reject) => {
		const id = nextId++;
		pending.set(id, { resolve, reject });
		ws.send(JSON.stringify({ id, method, params }));
	});
}

await new Promise((resolve, reject) => {
	ws.onopen = resolve;
	ws.onerror = () => reject(new Error('WebSocket connection failed'));
});

ws.onmessage = (message) => {
	const data = JSON.parse(message.data);
	if (!data.id || !pending.has(data.id)) {
		return;
	}
	const item = pending.get(data.id);
	pending.delete(data.id);
	if (data.error) {
		item.reject(new Error(data.error.message));
	} else {
		item.resolve(data.result || {});
	}
};

await send('Page.enable');
await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', {
	width: 390,
	height: 1800,
	deviceScaleFactor: 1,
	mobile: true,
	screenWidth: 390,
	screenHeight: 1800,
});
await send('Emulation.setTouchEmulationEnabled', { enabled: true });
await send('Page.navigate', { url: targetUrl });
await new Promise((resolve) => setTimeout(resolve, 2500));

const metrics = await send('Runtime.evaluate', {
	expression: `(() => ({
		innerWidth,
		clientWidth: document.documentElement.clientWidth,
		scrollWidth: document.documentElement.scrollWidth,
		title: document.title,
		units: document.querySelectorAll('.unit-cell').length,
		form: !!document.querySelector('#lead-form'),
		overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
		leadVisible: document.querySelector('#lead-form') ? getComputedStyle(document.querySelector('#lead-form')).display : null
	}))()`,
	returnByValue: true,
});

const screenshot = await send('Page.captureScreenshot', {
	format: 'png',
	fromSurface: true,
	captureBeyondViewport: false,
});

const out = path.join(repo, 'docs/qa/screenshots/dimri-yama-preview/mobile-390-cdp-v1.png');
await fs.writeFile(out, Buffer.from(screenshot.data, 'base64'));

const journey = await send('Runtime.evaluate', {
	expression: `(() => {
		document.querySelector('[data-unit="b-15-05"]').click();
		document.querySelector('[name="name"]').value = 'בדיקת QA';
		document.querySelector('[name="phone"]').value = '0500000000';
		document.querySelector('#lead-form').requestSubmit();
		document.querySelector('#lead-form').scrollIntoView({ block: 'center' });
		return {
			activeTitle: document.querySelector('#unit-title').textContent,
			okText: document.querySelector('#lead-ok').textContent,
			overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth
		};
	})()`,
	returnByValue: true,
});
await new Promise((resolve) => setTimeout(resolve, 400));
const formScreenshot = await send('Page.captureScreenshot', {
	format: 'png',
	fromSurface: true,
	captureBeyondViewport: false,
});

const formOut = path.join(repo, 'docs/qa/screenshots/dimri-yama-preview/mobile-390-cdp-form-v1.png');
await fs.writeFile(formOut, Buffer.from(formScreenshot.data, 'base64'));
ws.close();

console.log(JSON.stringify({ metrics: metrics.result.value, journey: journey.result.value, out, formOut }, null, 2));
