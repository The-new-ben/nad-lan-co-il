import fs from 'node:fs/promises';
import path from 'node:path';

const port = Number(process.argv[2] || 9225);
const outDir = process.argv[3] || 'docs/qa/screenshots/rainbow-1671-cdp';
const url = process.argv[4] || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?cb=1671cdp';

async function cdpRequest(method, params = {}) {
  const res = await fetch(`http://127.0.0.1:${port}/json/${method}`, {
    method: 'PUT',
    body: JSON.stringify(params),
  });
  if (!res.ok) {
    throw new Error(`${method} failed: ${res.status} ${await res.text()}`);
  }
  return res.json();
}

async function listTabs() {
  const res = await fetch(`http://127.0.0.1:${port}/json`);
  if (!res.ok) {
    throw new Error(`tab list failed: ${res.status}`);
  }
  return res.json();
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

class CDP {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.nextId = 1;
    this.pending = new Map();
    this.events = [];
    this.ws.addEventListener('message', event => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(JSON.stringify(msg.error)));
        else resolve(msg.result || {});
      } else if (msg.method) {
        this.events.push(msg);
      }
    });
  }

  async ready() {
    if (this.ws.readyState === WebSocket.OPEN) return;
    await new Promise((resolve, reject) => {
      this.ws.addEventListener('open', resolve, { once: true });
      this.ws.addEventListener('error', reject, { once: true });
    });
  }

  async send(method, params = {}) {
    await this.ready();
    const id = this.nextId++;
    const promise = new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
    this.ws.send(JSON.stringify({ id, method, params }));
    return promise;
  }

  close() {
    this.ws.close();
  }
}

async function main() {
  await fs.mkdir(outDir, { recursive: true });
  const tab = await cdpRequest('new', { url: 'about:blank' });
  const cdp = new CDP(tab.webSocketDebuggerUrl);
  await cdp.ready();
  await cdp.send('Page.enable');
  await cdp.send('Runtime.enable');
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });

  const viewports = [
    { name: 'desktop-1440', width: 1440, height: 1100, mobile: false, deviceScaleFactor: 1 },
    { name: 'tablet-768', width: 768, height: 1100, mobile: false, deviceScaleFactor: 1 },
    { name: 'mobile-390', width: 390, height: 1200, mobile: true, deviceScaleFactor: 2 },
  ];

  const results = [];
  for (const vp of viewports) {
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: vp.width,
      height: vp.height,
      deviceScaleFactor: vp.deviceScaleFactor,
      mobile: vp.mobile,
      screenWidth: vp.width,
      screenHeight: vp.height,
    });
    await cdp.send('Page.navigate', { url: `${url}-${vp.name}` });
    await sleep(4500);
    const metrics = await cdp.send('Runtime.evaluate', {
      returnByValue: true,
      expression: `(() => {
        const rect = el => {
          if (!el) return null;
          const r = el.getBoundingClientRect();
          return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),bottom:Math.round(r.bottom),right:Math.round(r.right)};
        };
        const headings = [...document.querySelectorAll('.wp-block-post-content>h2,.wp-block-post-content>h3')].slice(0,8).map(h => {
          let n = h.nextElementSibling;
          while (n && !['P','UL','OL'].includes(n.tagName)) n = n.nextElementSibling;
          const hr = h.getBoundingClientRect();
          const nr = n ? n.getBoundingClientRect() : null;
          return {text:h.textContent.trim().slice(0,50), hx:Math.round(hr.x), hw:Math.round(hr.width), nx:nr&&Math.round(nr.x), nw:nr&&Math.round(nr.width)};
        });
        return {
          url: location.href,
          viewport: {w: innerWidth, h: innerHeight},
          overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          h1s: [...document.querySelectorAll('h1')].map(h => h.textContent.trim()).filter(Boolean),
          hero: rect(document.querySelector('.nlp3d-hero-media')),
          intro: rect(document.querySelector('.nlp3d-intro')),
          scene: rect(document.querySelector('.nlp3d-scene')),
          model: rect(document.querySelector('.nlp3d-model-viewer')),
          facade: rect(document.querySelector('.nlp3d-facade-plane')),
          card: rect(document.querySelector('.nlp3d-stage-card')),
          cells: [...document.querySelectorAll('.nlp3d-cell')].length,
          oldFloats: [...document.querySelectorAll('.nlp3d-hotspot,.nlp3d-marker,.nlp3d-stage-pick')].filter(el=>{const r=el.getBoundingClientRect(); return r.width>0&&r.height>0;}).length,
          headings
        };
      })()`,
    });
    const png = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false, fromSurface: true });
    await fs.writeFile(path.join(outDir, `${vp.name}.png`), Buffer.from(png.data, 'base64'));
    await cdp.send('Runtime.evaluate', {
      expression: `(() => {
        const cell = document.querySelector('.nlp3d-cell');
        if (cell) cell.scrollIntoView({block:'center', inline:'center'});
      })()`,
    });
    await sleep(700);
    const target = await cdp.send('Runtime.evaluate', {
      returnByValue: true,
      expression: `(() => {
        const cells = [...document.querySelectorAll('.nlp3d-cell')].filter(el => {
          const r = el.getBoundingClientRect();
          return r.width > 20 && r.height > 20 && r.bottom > 0 && r.top < innerHeight;
        });
        const el = cells[0];
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return {x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2), text: el.textContent.trim().slice(0, 80)};
      })()`,
    });
    if (target.result.value) {
      await cdp.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: target.result.value.x, y: target.result.value.y });
      await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: target.result.value.x, y: target.result.value.y, button: 'left', clickCount: 1 });
      await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: target.result.value.x, y: target.result.value.y, button: 'left', clickCount: 1 });
      await sleep(700);
    }
    const clickMetrics = await cdp.send('Runtime.evaluate', {
      returnByValue: true,
      expression: `(() => {
        const rect = el => {
          if (!el) return null;
          const r = el.getBoundingClientRect();
          return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),bottom:Math.round(r.bottom),right:Math.round(r.right)};
        };
        const scene = document.querySelector('.nlp3d-scene');
        const card = document.querySelector('.nlp3d-stage-card');
        const selected = document.querySelector('.nlp3d-cell.is-active, .nlp3d-cell[aria-pressed="true"]');
        return {
          clicked: ${JSON.stringify(null)},
          scene: rect(scene),
          card: rect(card),
          cardVisible: !!card && !card.hasAttribute('hidden') && getComputedStyle(card).display !== 'none' && card.getBoundingClientRect().height > 2,
          cardText: card ? card.textContent.replace(/\\s+/g,' ').trim().slice(0, 240) : null,
          selectedText: selected ? selected.textContent.replace(/\\s+/g,' ').trim().slice(0, 120) : null
        };
      })()`,
    });
    const clickedPng = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false, fromSurface: true });
    await fs.writeFile(path.join(outDir, `${vp.name}-clicked.png`), Buffer.from(clickedPng.data, 'base64'));
    results.push({ viewport: vp, metrics: metrics.result.value, clickTarget: target.result.value, clickMetrics: clickMetrics.result.value });
  }
  await fs.writeFile(path.join(outDir, 'metrics.json'), JSON.stringify(results, null, 2));
  cdp.close();
  console.log(JSON.stringify({ outDir, results }, null, 2));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
