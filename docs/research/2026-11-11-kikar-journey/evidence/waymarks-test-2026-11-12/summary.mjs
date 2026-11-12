// prints the waymarks test results in short: node summary.mjs result-he.json
import fs from 'node:fs';
const r = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
for (const x of r.runs) {
  console.log(`=== ${x.L} ${x.w}x${x.h} ${x.error || ''} steps ok: ${x.ok}`);
  for (const s of x.steps) console.log(`${s.ok ? 'OK' : 'XX'} ${s.name} | pulses ${s.pulses} ${JSON.stringify(s.what)} | "${s.label}"${s.ok ? '' : ' expected "' + s.expected + '"'}`);
  const c = x.checks, j = (v) => JSON.stringify(v);
  console.log('world/three on load:', j(c.worldOnLoad), '| world before 3D tap:', c.worldBefore3d, '| three before inside:', c.threeBeforeInside);
  console.log('peek:', j(c.peek && { share: c.peek.share, cardH: c.peek.cardH, stageH: c.peek.stageH, title: c.peek.titleOneLine, bandVisible: c.peek.band && c.peek.band.visible, small: c.peek.small }));
  if (c.reach) console.log('reach:', j({ lowest: c.reach.lowest && c.reach.lowest.floor, highest: c.reach.highest && c.reach.highest.floor, floors: c.reach.floors, bandVisible: c.reach.bandAfter && c.reach.bandAfter.visible }));
  if (c.expanded) console.log('expanded:', j({ share: c.expanded.share, cardH: c.expanded.cardH, bandVisible: c.expanded.band && c.expanded.band.visible, aria: c.expanded.ariaExpanded, labels: c.expanded.labels, small: c.expanded.small }));
  if (c.fold) console.log('fold:', j(c.fold));
  if (c.desktop) console.log('desktop:', j(c.desktop && { beside: c.desktop.cardBesideTower, side: c.desktop.side, expect: c.desktop.expectSide, small: c.desktop.small, bandVisible: c.desktop.band && c.desktop.band.visible }));
  console.log('plan:', j(c.plan && { tapped: c.plan.tapped, changed: c.plan.changed, b0: c.plan.before && c.plan.before.bearing, b1: c.plan.after && c.plan.after.bearing, ev: c.plan.facingEvents, mapline: c.plan.mapline }));
  console.log('basket design:', j(c.basketDesign), 'after:', j(c.basketAfter));
  console.log('view details:', j(c.viewDetails && { labels: c.viewDetails.labels, names: c.viewDetails.names, off: c.viewDetails.toggleOff, on: c.viewDetails.toggleOn, small: c.viewDetails.small }));
  console.log('3D:', j(c.threeD));
  console.log('hscroll:', c.hscrollShowroom, c.hscrollCockpit, c.hscrollEnd, '| small cockpit:', j(c.smallCockpit), '| hebrew:', j(c.hebrew));
  console.log('errors:', j(x.errs), '| failed:', j(x.failed));
}
