import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'assets', 'projects', 'dimri-yama', 'model-prototype.glb');

function pad4(n) {
  return (4 - (n % 4)) % 4;
}

function pushFloat32(values, chunks) {
  const b = Buffer.alloc(values.length * 4);
  values.forEach((v, i) => b.writeFloatLE(v, i * 4));
  const offset = chunks.length ? chunks.reduce((sum, c) => sum + c.length, 0) : 0;
  chunks.push(b);
  const pad = pad4(b.length);
  if (pad) chunks.push(Buffer.alloc(pad));
  return { byteOffset: offset, byteLength: b.length };
}

function pushUint16(values, chunks) {
  const b = Buffer.alloc(values.length * 2);
  values.forEach((v, i) => b.writeUInt16LE(v, i * 2));
  const offset = chunks.length ? chunks.reduce((sum, c) => sum + c.length, 0) : 0;
  chunks.push(b);
  const pad = pad4(b.length);
  if (pad) chunks.push(Buffer.alloc(pad));
  return { byteOffset: offset, byteLength: b.length };
}

function boxGeometry(cx, cy, cz, sx, sy, sz) {
  const x0 = cx - sx / 2, x1 = cx + sx / 2;
  const y0 = cy, y1 = cy + sy;
  const z0 = cz - sz / 2, z1 = cz + sz / 2;
  const faces = [
    { n: [0, 0, 1], v: [[x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]] },
    { n: [0, 0, -1], v: [[x1, y0, z0], [x0, y0, z0], [x0, y1, z0], [x1, y1, z0]] },
    { n: [1, 0, 0], v: [[x1, y0, z1], [x1, y0, z0], [x1, y1, z0], [x1, y1, z1]] },
    { n: [-1, 0, 0], v: [[x0, y0, z0], [x0, y0, z1], [x0, y1, z1], [x0, y1, z0]] },
    { n: [0, 1, 0], v: [[x0, y1, z1], [x1, y1, z1], [x1, y1, z0], [x0, y1, z0]] },
    { n: [0, -1, 0], v: [[x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1]] },
  ];
  const positions = [];
  const normals = [];
  const indices = [];
  faces.forEach((face, fi) => {
    const base = fi * 4;
    face.v.forEach((p) => positions.push(...p));
    for (let i = 0; i < 4; i += 1) normals.push(...face.n);
    indices.push(base, base + 1, base + 2, base, base + 2, base + 3);
  });
  return { positions, normals, indices };
}

function rectGeometry(cx, cy, cz, sx, sz) {
  const x0 = cx - sx / 2, x1 = cx + sx / 2;
  const z0 = cz - sz / 2, z1 = cz + sz / 2;
  return {
    positions: [x0, cy, z1, x1, cy, z1, x1, cy, z0, x0, cy, z0],
    normals: [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    indices: [0, 1, 2, 0, 2, 3],
  };
}

const objects = [
  { name: 'Tower B 39 floors', geom: boxGeometry(0, 0, 0, 8, 39, 8), material: 0 },
  { name: 'Building A 15 floors', geom: boxGeometry(-13, 0, 7, 12, 15, 7), material: 1 },
  { name: 'Building C 9 floors', geom: boxGeometry(14, 0, 7, 12, 9, 7), material: 1 },
  { name: 'Building D 9 floors', geom: boxGeometry(-8, 0, -12, 16, 9, 7), material: 1 },
  { name: 'Green courtyard', geom: rectGeometry(0, 0.05, 2, 34, 24), material: 2 },
  { name: 'Sea direction plane', geom: rectGeometry(0, -0.02, -35, 58, 12), material: 3 },
  { name: 'Sun marker', geom: boxGeometry(20, 28, -20, 2, 2, 2), material: 4 },
];

const bufferChunks = [];
const json = {
  asset: { version: '2.0', generator: 'NadLan Dimri Yama prototype massing generator' },
  scene: 0,
  scenes: [{ nodes: objects.map((_, i) => i) }],
  nodes: [],
  meshes: [],
  materials: [
    { name: 'champagne tower glass', pbrMetallicRoughness: { baseColorFactor: [0.9, 0.82, 0.62, 1], metallicFactor: 0.05, roughnessFactor: 0.42 } },
    { name: 'light residential massing', pbrMetallicRoughness: { baseColorFactor: [0.75, 0.83, 0.8, 1], metallicFactor: 0.03, roughnessFactor: 0.5 } },
    { name: 'courtyard green', pbrMetallicRoughness: { baseColorFactor: [0.16, 0.46, 0.34, 1], metallicFactor: 0, roughnessFactor: 0.75 } },
    { name: 'sea orientation', pbrMetallicRoughness: { baseColorFactor: [0.05, 0.36, 0.48, 0.95], metallicFactor: 0, roughnessFactor: 0.6 } },
    { name: 'sun marker gold', pbrMetallicRoughness: { baseColorFactor: [1, 0.73, 0.22, 1], metallicFactor: 0, roughnessFactor: 0.35 } },
  ],
  accessors: [],
  bufferViews: [],
  buffers: [],
};

objects.forEach((obj, idx) => {
  const { positions, normals, indices } = obj.geom;
  const posView = pushFloat32(positions, bufferChunks);
  const normalView = pushFloat32(normals, bufferChunks);
  const indexView = pushUint16(indices, bufferChunks);
  const posViewIndex = json.bufferViews.push({ buffer: 0, byteOffset: posView.byteOffset, byteLength: posView.byteLength, target: 34962 }) - 1;
  const normalViewIndex = json.bufferViews.push({ buffer: 0, byteOffset: normalView.byteOffset, byteLength: normalView.byteLength, target: 34962 }) - 1;
  const indexViewIndex = json.bufferViews.push({ buffer: 0, byteOffset: indexView.byteOffset, byteLength: indexView.byteLength, target: 34963 }) - 1;
  const xs = [], ys = [], zs = [];
  for (let i = 0; i < positions.length; i += 3) {
    xs.push(positions[i]); ys.push(positions[i + 1]); zs.push(positions[i + 2]);
  }
  const posAccessor = json.accessors.push({
    bufferView: posViewIndex,
    componentType: 5126,
    count: positions.length / 3,
    type: 'VEC3',
    min: [Math.min(...xs), Math.min(...ys), Math.min(...zs)],
    max: [Math.max(...xs), Math.max(...ys), Math.max(...zs)],
  }) - 1;
  const normalAccessor = json.accessors.push({
    bufferView: normalViewIndex,
    componentType: 5126,
    count: normals.length / 3,
    type: 'VEC3',
  }) - 1;
  const indexAccessor = json.accessors.push({
    bufferView: indexViewIndex,
    componentType: 5123,
    count: indices.length,
    type: 'SCALAR',
    min: [Math.min(...indices)],
    max: [Math.max(...indices)],
  }) - 1;
  json.meshes.push({
    name: obj.name,
    primitives: [{
      attributes: { POSITION: posAccessor, NORMAL: normalAccessor },
      indices: indexAccessor,
      material: obj.material,
    }],
  });
  json.nodes.push({ name: obj.name, mesh: idx });
});

const bin = Buffer.concat(bufferChunks);
json.buffers.push({ byteLength: bin.length });

let jsonChunk = Buffer.from(JSON.stringify(json), 'utf8');
jsonChunk = Buffer.concat([jsonChunk, Buffer.alloc(pad4(jsonChunk.length), 0x20)]);
let binChunk = bin;
binChunk = Buffer.concat([binChunk, Buffer.alloc(pad4(binChunk.length))]);

const totalLength = 12 + 8 + jsonChunk.length + 8 + binChunk.length;
const header = Buffer.alloc(12);
header.writeUInt32LE(0x46546c67, 0); // glTF
header.writeUInt32LE(2, 4);
header.writeUInt32LE(totalLength, 8);

const jsonHeader = Buffer.alloc(8);
jsonHeader.writeUInt32LE(jsonChunk.length, 0);
jsonHeader.writeUInt32LE(0x4e4f534a, 4); // JSON

const binHeader = Buffer.alloc(8);
binHeader.writeUInt32LE(binChunk.length, 0);
binHeader.writeUInt32LE(0x004e4942, 4); // BIN

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, Buffer.concat([header, jsonHeader, jsonChunk, binHeader, binChunk]));
console.log(JSON.stringify({ ok: true, out: path.relative(ROOT, OUT).replace(/\\/g, '/'), bytes: fs.statSync(OUT).size }, null, 2));
