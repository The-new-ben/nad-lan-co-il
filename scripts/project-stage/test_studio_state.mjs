/** UnitDesignRequest (design system v102, HAD-346 Batch 2): the branch's 2D studio (assets/showroom-engine/studio.js) against
 * Codex's acceptance for Batch 2 (handoff 29.9, "סבב2: גם היסטוריית הפעולות חייבת להיות שייכת לדירה"). Memory only: DOM and
 * storage doubles in the style of Codex's scripts/labs/audit-studio-state.mjs (which characterizes the OLD file and stays
 * locked to it); no browser, network, WordPress or real storage. Not visual or browser acceptance.
 *   node scripts/project-stage/test_studio_state.mjs
 */
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const here = path.dirname(fileURLToPath(import.meta.url));
const file = path.join(here, '..', '..', 'plugins', 'nadlan-config', 'assets', 'showroom-engine', 'studio.js');
const source = await readFile(file, 'utf8');

function harness(storage = new Map(), opts = {}) {
  const elements = new Map(), windowEvents = new Map(), prompts = [];
  class Element {
    constructor() { this.style = {}; this.dataset = {}; this.listeners = new Map(); this.children = []; this.value = ''; this.textContent = ''; this.className = ''; this.parentElement = {clientWidth: 900}; this.classList = {add() {}, remove() {}, toggle() {}}; }
    set id(v) { this._id = v; elements.set(v, this); } get id() { return this._id; }
    set innerHTML(v) {
      this._html = v; for (const m of v.matchAll(/\bid="([^"]+)"/g)) { const e = new Element(); e.id = m[1]; } this.children = [];
      // a browser fills a textarea from its content: so does this double (the studio renders its notes there)
      for (const m of v.matchAll(/<textarea id="([^"]+)"[^>]*>([\s\S]*?)<\/textarea>/g)) elements.get(m[1]).value = m[2].replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&amp;/g, '&');
    }
    get innerHTML() { return this._html || ''; }
    appendChild(e) { this.children.push(e); return e; }
    remove() { if (elements.get(this.id) === this) elements.delete(this.id); }
    focus() {}
    querySelector(s) { if (s.startsWith('#')) return elements.get(s.slice(1)); if (s === '[data-st="wa"]') return this.wa || (this.wa = new Element()); throw Error('Unhandled selector ' + s); }
    addEventListener(k, fn) { if (!this.listeners.has(k)) this.listeners.set(k, []); this.listeners.get(k).push(fn); }
  }
  const document = {body: new Element(), documentElement: {dir: 'rtl'}, createElement: () => new Element(), getElementById: (id) => elements.get(id) || null,
    querySelectorAll: () => [], querySelector: () => null};
  const window = {addEventListener(k, fn) { if (!windowEvents.has(k)) windowEvents.set(k, []); windowEvents.get(k).push(fn); },
    open() { throw Error('External navigation forbidden'); }, prompt() { return prompts.length ? prompts.shift() : null; }};
  const localStorage = {
    getItem: (k) => (storage.has(k) ? storage.get(k) : null),
    setItem: (k, v) => { if (opts.full) throw Error('QuotaExceededError'); storage.set(k, String(v)); },
    key: (i) => [...storage.keys()][i] ?? null, get length() { return storage.size; }};
  const sandbox = {document, window, localStorage, location: {origin: 'https://example.invalid', pathname: '/projects/fixture/'}, fetch() { throw Error('Network forbidden'); }};
  vm.runInNewContext(source, sandbox, {timeout: 1000, filename: 'studio.js'});
  const T = (k) => k;
  const open = (unit = 'fixture-A', project = 'fixture-project', sqm = 120) => window.NLStudio.open({projectKey: project, projectName: 'Synthetic', unit: {id: unit, label: unit, floor: 13, rooms: 4, sqm}, t: T});
  const click = (kind, value) => {
    const root = elements.get('nlst'); assert.ok(root, 'open the studio first');
    const sel = kind === 'add' ? '[data-add]' : '[data-st]';
    for (const fn of root.listeners.get('click') || []) fn({target: {closest: (s) => (s === sel ? {dataset: {[kind === 'add' ? 'add' : 'st']: value}} : null)}});
  };
  const exported = (unit = 'fixture-A', project = 'fixture-project') => { const v = window.NLStudio.exportFor(project, unit); return v === null ? null : JSON.parse(JSON.stringify(v)); };
  const pagehide = () => { for (const fn of windowEvents.get('pagehide') || []) fn(); };
  return {open, click, exported, elements, storage, prompts, pagehide, opts};
}
const types = (d) => (d ? d.layers.plan2d.items.map((x) => x.type) : null);
const results = [];
function check(id, what, run) {
  try { run(); results.push({id, pass: true, what}); } catch (e) { results.push({id, pass: false, what, error: String(e.message || e).slice(0, 300)}); }
}

check('S2-01 (STUDIO-STATE-03)', "A: sofa + bed, close, open empty B, undo: B stays empty and nothing of A is saved under B; A intact", () => {
  const h = harness(); h.open(); h.click('add', 'sofa3'); h.click('add', 'bed_double'); h.click('action', 'close');
  const a = JSON.stringify(h.exported()); h.open('fixture-B'); h.click('action', 'undo');
  assert.equal(h.exported('fixture-B'), null); assert.equal([...h.storage.keys()].filter((k) => k.includes(':fixture-B:') && JSON.parse(h.storage.get(k)).items.length).length, 0);
  assert.equal(JSON.stringify(h.exported()), a);
});
check('S2-02 (STUDIO-STATE-04)', 'the same unit id in another project: its own document, undo does not cross projects', () => {
  const h = harness(); h.open('fixture-A', 'project-one'); h.click('add', 'sofa3'); h.click('add', 'bed_double'); h.click('action', 'close');
  h.open('fixture-A', 'project-two'); h.click('action', 'undo'); assert.equal(h.exported('fixture-A', 'project-two'), null);
  assert.deepEqual(types(h.exported('fixture-A', 'project-one')), ['sofa3', 'bed_double']);
});
check('S2-03 (STUDIO-STATE-02)', 'undo inside one unit restores its previous state', () => {
  const h = harness(); h.open(); h.click('add', 'sofa3'); h.click('add', 'bed_double'); h.click('action', 'undo'); assert.deepEqual(types(h.exported()), ['sofa3']);
});
check('S2-04', "back to A after B: undo removes only A's last action", () => {
  const h = harness(); h.open(); h.click('add', 'sofa3'); h.click('add', 'bed_double'); h.open('fixture-B'); h.click('add', 'desk'); h.open('fixture-A'); h.click('action', 'undo');
  assert.deepEqual(types(h.exported()), ['sofa3']); assert.deepEqual(types(h.exported('fixture-B')), ['desk']);
});
check('S2-05', 'redo brings back what undo took, in the same unit', () => {
  const h = harness(); h.open(); h.click('add', 'sofa3'); h.click('add', 'bed_double'); h.click('action', 'undo'); h.click('action', 'redo'); assert.deepEqual(types(h.exported()), ['sofa3', 'bed_double']);
});
check('S2-06 (STUDIO-STATE-05)', 'a note typed without change/close is in the export, and kept across a pagehide + reload', () => {
  const h = harness(); h.open(); h.click('add', 'sofa3'); h.elements.get('nlst-notes').value = 'Synthetic wider-opening request';
  assert.equal(h.exported().notes[0].text, 'Synthetic wider-opening request');
  h.elements.get('nlst-notes').value = 'Synthetic wider-opening request, 90 cm'; h.pagehide();
  const r = harness(h.storage); r.open(); assert.equal(r.exported().notes[0].text, 'Synthetic wider-opening request, 90 cm');
});
check('S2-07', 'eight notes (one general + seven on items), with the unit identity, in one export', () => {
  const h = harness(); h.open(); h.elements.get('nlst-notes').value = 'General: synthetic wider opening';
  for (let i = 0; i < 7; i++) { h.click('add', 'armchair'); h.prompts.push('Synthetic item note ' + (i + 1)); h.click('action', 'note'); }
  const d = h.exported(); assert.equal(d.notes.length, 8); assert.equal(d.unit_id, 'fixture-A'); assert.equal(d.project, 'fixture-project');
  assert.equal(d.schema, 'nadlan-unit-design'); assert.equal(d.source, 'studio-2d'); assert.equal(d.layers.plan2d.units, 'cm'); assert.match(d.geometry_revision, /^schematic-v1:4:120$/);
});
check('S2-08', "a geometry revision change opens a new document and keeps the old one", () => {
  const h = harness(); h.open('fixture-A', 'fixture-project', 120); h.click('add', 'sofa3'); h.open('fixture-A', 'fixture-project', 95);
  assert.equal(h.exported(), null); // the export follows the open document: the 95 sqm plan is new and empty
  assert.ok(h.storage.has('nlstudio:fixture-project:fixture-A:schematic-v1:4:120'));
  assert.deepEqual(JSON.parse(h.storage.get('nlstudio:fixture-project:fixture-A:schematic-v1:4:120')).items.map((x) => x.type), ['sofa3']);
});
check('S2-09', 'an export is a frozen copy: later edits never change a request already built', () => {
  const h = harness(); h.open(); h.click('add', 'sofa3'); const before = h.exported(); const frozen = JSON.stringify(before); h.click('add', 'bed_double');
  assert.equal(JSON.stringify(before), frozen); assert.deepEqual(types(h.exported()), ['sofa3', 'bed_double']);
});
check('S2-10', 'a draft that cannot be read is set aside, not deleted, and said', () => {
  const st = new Map([['nlstudio:fixture-project:fixture-A:schematic-v1:4:120', '{broken']]); const h = harness(st); h.open();
  assert.equal([...st.keys()].filter((k) => k.includes(':unreadable:')).length, 1); assert.equal(h.elements.get('nlst-save').textContent, 'nlst_corrupt');
});
check('S2-11', 'a failed save is visible, not silent', () => {
  const h = harness(new Map(), {full: true}); h.open(); h.click('add', 'sofa3'); assert.equal(h.elements.get('nlst-save').textContent, 'nlst_save_failed');
  assert.equal(h.elements.get('nlst-save').className, 'nlst-save is-bad');
});
check('S2-12', 'a plan saved before revisions existed is read, and its key is not deleted', () => {
  const st = new Map([['nlstudio:fixture-project:fixture-A', JSON.stringify({v: 1, items: [{uid: 'i1', type: 'sofa3', x: 10, y: 10, rot: 0, note: ''}], notes: 'old'})]]);
  const h = harness(st); h.open(); assert.deepEqual(types(h.exported()), ['sofa3']); assert.ok(st.has('nlstudio:fixture-project:fixture-A'));
});

// Codex STUDIO-B2-EXPORT-STALE (29.9): the export is the CURRENT plan, whatever the storage did; the storage result is apart
check('S2-13 (STUDIO-B2-EXPORT-STALE)', 'A saved with 2 items, closed; the storage starts failing; A reopened, a 3rd chair and a note: the export has 3 items and the note, persisted=false, the failure shown', () => {
  const h = harness(); h.open(); h.click('add', 'sofa3'); h.click('add', 'bed_double'); h.click('action', 'close');
  h.opts.full = true; h.open(); h.click('add', 'armchair'); h.elements.get('nlst-notes').value = 'Synthetic new note';
  const d = h.exported(); assert.deepEqual(types(d), ['sofa3', 'bed_double', 'armchair']); assert.equal(d.notes[0].text, 'Synthetic new note'); assert.equal(d.persisted, false);
  assert.equal(h.elements.get('nlst-save').textContent, 'nlst_save_failed');
});
check('S2-14', 'no successful save ever (the storage fails from the start): the export still carries the plan, persisted=false', () => {
  const h = harness(new Map(), {full: true}); h.open(); h.click('add', 'desk'); const d = h.exported(); assert.deepEqual(types(d), ['desk']); assert.equal(d.persisted, false);
});
check('S2-15', 'A edited while the storage fails, then B opened, then A exported: A as it was left on this page, not the storage', () => {
  const h = harness(); h.open(); h.click('add', 'sofa3'); h.opts.full = true; h.click('add', 'crib'); h.elements.get('nlst-notes').value = 'Synthetic A note';
  h.open('fixture-B'); h.click('add', 'desk');
  const a = h.exported(); assert.deepEqual(types(a), ['sofa3', 'crib']); assert.equal(a.notes[0].text, 'Synthetic A note'); assert.equal(a.persisted, false);
  assert.deepEqual(types(h.exported('fixture-B')), ['desk']);
  h.open(); assert.deepEqual(types(h.exported()), ['sofa3', 'crib']); // reopening A on this page shows the newer state, not the stale storage
});
check('S2-16', 'recovery: the storage fails, then works again: the next change is kept, persisted=true, the storage has the current plan', () => {
  const h = harness(); h.open(); h.opts.full = true; h.click('add', 'sofa3'); h.opts.full = false; h.click('add', 'bed_single');
  const d = h.exported(); assert.equal(d.persisted, true); assert.equal(h.elements.get('nlst-save').textContent, 'nlst_saved');
  assert.deepEqual(JSON.parse(h.storage.get('nlstudio:fixture-project:fixture-A:schematic-v1:4:120')).items.map((x) => x.type), ['sofa3', 'bed_single']);
});
check('S2-17 (limit, said honestly)', 'pagehide while the storage fails: nothing throws and the page still exports the current plan, BUT a reload after it cannot bring back what the storage never took', () => {
  const h = harness(); h.open(); h.click('add', 'sofa3'); h.opts.full = true; h.click('add', 'crib'); h.pagehide();
  assert.deepEqual(types(h.exported()), ['sofa3', 'crib']);
  const r = harness(h.storage); r.open(); assert.deepEqual(types(r.exported()), ['sofa3']); // the limit: only a request (sent) keeps it
});
const failed = results.filter((r) => !r.pass);
console.log(JSON.stringify({mode: 'memory-only; the branch studio.js; synthetic units; NOT browser or visual acceptance', studio_js_sha256: createHash('sha256').update(source).digest('hex'),
  passed: results.length - failed.length, failed: failed.length, results}, null, 2));
process.exit(failed.length ? 1 : 0);
