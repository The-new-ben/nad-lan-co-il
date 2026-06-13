#!/usr/bin/env python3
"""Generate the Rainbow Tel Aviv illustrative showroom model package.

This deliberately creates a lightweight, original architectural massing model.
It is not official developer BIM and should be replaced by approved source
material when the developer supplies it.
"""

from __future__ import annotations

import json
import math
import os
import struct
import zlib
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "projects" / "rainbow-tel-aviv"
BRANCH = "codex/rainbow-prototype-model-1631"
RAW_BASE = f"https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/{BRANCH}/assets/projects/rainbow-tel-aviv"


MATERIALS = [
    {
        "name": "deep blueprint glass",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.035, 0.18, 0.18, 0.92],
            "metallicFactor": 0.05,
            "roughnessFactor": 0.28,
        },
        "alphaMode": "BLEND",
        "doubleSided": False,
    },
    {
        "name": "warm champagne frame",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.86, 0.69, 0.39, 1.0],
            "metallicFactor": 0.35,
            "roughnessFactor": 0.42,
        },
    },
    {
        "name": "soft concrete shell",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.72, 0.70, 0.64, 1.0],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.68,
        },
    },
    {
        "name": "clear window rhythm",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.26, 0.63, 0.72, 0.72],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.18,
        },
        "alphaMode": "BLEND",
    },
    {
        "name": "lagoon water",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.04, 0.42, 0.55, 0.86],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.2,
        },
        "alphaMode": "BLEND",
        "doubleSided": True,
    },
    {
        "name": "site landscape",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.18, 0.28, 0.20, 1.0],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.8,
        },
    },
]


class MeshBuilder:
    def __init__(self) -> None:
        self.positions: list[list[float]] = [[] for _ in MATERIALS]
        self.normals: list[list[float]] = [[] for _ in MATERIALS]
        self.indices: list[list[int]] = [[] for _ in MATERIALS]

    def add_box(
        self,
        material: int,
        center: tuple[float, float, float],
        size: tuple[float, float, float],
        rot_y: float = 0.0,
    ) -> None:
        cx, cy, cz = center
        sx, sy, sz = (s / 2.0 for s in size)
        corners = [
            (-sx, -sy, -sz),
            (sx, -sy, -sz),
            (sx, sy, -sz),
            (-sx, sy, -sz),
            (-sx, -sy, sz),
            (sx, -sy, sz),
            (sx, sy, sz),
            (-sx, sy, sz),
        ]
        faces = [
            ((0, 1, 2, 3), (0, 0, -1)),
            ((5, 4, 7, 6), (0, 0, 1)),
            ((4, 0, 3, 7), (-1, 0, 0)),
            ((1, 5, 6, 2), (1, 0, 0)),
            ((3, 2, 6, 7), (0, 1, 0)),
            ((4, 5, 1, 0), (0, -1, 0)),
        ]
        cos_r = math.cos(rot_y)
        sin_r = math.sin(rot_y)

        def transform(p: tuple[float, float, float]) -> tuple[float, float, float]:
            x, y, z = p
            return (cx + x * cos_r + z * sin_r, cy + y, cz - x * sin_r + z * cos_r)

        def rotate_n(n: tuple[float, float, float]) -> tuple[float, float, float]:
            x, y, z = n
            return (x * cos_r + z * sin_r, y, -x * sin_r + z * cos_r)

        for face, normal in faces:
            base = len(self.positions[material]) // 3
            rn = rotate_n(normal)
            for idx in face:
                self.positions[material].extend(transform(corners[idx]))
                self.normals[material].extend(rn)
            self.indices[material].extend([base, base + 1, base + 2, base, base + 2, base + 3])

    def add_plane(
        self,
        material: int,
        center: tuple[float, float, float],
        size: tuple[float, float],
        rot_y: float = 0.0,
    ) -> None:
        sx, sz = size[0] / 2, size[1] / 2
        self.add_box(material, center, (size[0], 0.08, size[1]), rot_y=rot_y)


def floor_shape(floor: int) -> tuple[float, float, float, float, float]:
    angle = floor * 0.085
    sx = 18.0 + 1.2 * math.sin(angle)
    sz = 12.6 + 0.8 * math.cos(angle * 0.8)
    x = 1.3 * math.sin(angle * 0.9)
    z = 0.9 * math.cos(angle * 0.7)
    rot = angle * 0.38
    return sx, sz, x, z, rot


def add_tower(builder: MeshBuilder) -> None:
    floor_h = 3.05
    base_y = 6.2

    builder.add_box(2, (0, 2.15, 0), (28, 4.3, 18), rot_y=0.04)
    builder.add_box(0, (0, base_y + 58, 0), (14.8, 112, 9.8), rot_y=0.18)

    for floor in range(1, 40):
        y = base_y + floor * floor_h
        sx, sz, x, z, rot = floor_shape(floor)
        builder.add_box(1, (x, y, z), (sx, 0.16, sz), rot_y=rot)

        if floor % 2 == 0:
            builder.add_box(2, (x, y + 0.18, z), (sx * 0.92, 0.12, sz * 0.9), rot_y=rot)

        for side in (-1, 1):
            for bay in (-0.32, 0.0, 0.32):
                builder.add_box(3, (x + bay * sx, y + 1.35, z + side * (sz / 2 + 0.04)), (sx * 0.18, 1.55, 0.06), rot_y=rot)
            builder.add_box(1, (x, y + 2.15, z + side * (sz / 2 + 0.13)), (sx * 0.86, 0.08, 0.16), rot_y=rot)

        for side in (-1, 1):
            for bay in (-0.28, 0.28):
                builder.add_box(3, (x + side * (sx / 2 + 0.04), y + 1.35, z + bay * sz), (0.06, 1.55, sz * 0.22), rot_y=rot)

    top_y = base_y + 40 * floor_h
    builder.add_box(1, (0.6, top_y + 1.2, 0.2), (18.5, 2.2, 13.2), rot_y=0.34)
    builder.add_box(0, (0.6, top_y + 2.7, 0.2), (15.5, 0.9, 10.8), rot_y=0.34)


def add_boutique_ring(builder: MeshBuilder) -> None:
    # Six 8-9 floor boutique blocks around the inner court, matching public project language.
    blocks = [
        (-42, 18, 30, 12, -0.08),
        (-23, 37, 28, 12, 0.18),
        (20, 39, 32, 12, -0.12),
        (44, 16, 26, 12, 0.1),
        (28, -32, 34, 12, 0.2),
        (-27, -33, 34, 12, -0.18),
    ]
    for idx, (x, z, sx, sz, rot) in enumerate(blocks):
        floors = 8 if idx in (1, 4) else 9
        h = floors * 3.05
        builder.add_box(2, (x, h / 2 + 2.0, z), (sx, h, sz), rot_y=rot)
        for floor in range(1, floors + 1):
            y = 2.0 + floor * 3.05
            builder.add_box(1, (x, y, z), (sx * 1.02, 0.12, sz * 1.05), rot_y=rot)
            for side in (-1, 1):
                builder.add_box(3, (x, y + 1.2, z + side * (sz / 2 + 0.05)), (sx * 0.72, 1.35, 0.06), rot_y=rot)


def add_site(builder: MeshBuilder) -> None:
    builder.add_box(5, (0, -0.08, 0), (110, 0.12, 95), rot_y=0)
    builder.add_box(4, (0, 0.03, 0), (42, 0.1, 22), rot_y=0.03)
    for x, z in [(-29, 0), (-18, 15), (17, -14), (31, 3), (0, 23), (0, -24)]:
        builder.add_box(1, (x, 0.7, z), (0.7, 1.4, 0.7), rot_y=0)


def build_glb(path: Path) -> None:
    builder = MeshBuilder()
    add_site(builder)
    add_boutique_ring(builder)
    add_tower(builder)

    buffer = bytearray()
    buffer_views = []
    accessors = []
    primitives = []

    def pad4() -> None:
        while len(buffer) % 4:
            buffer.append(0)

    for mat_idx, positions in enumerate(builder.positions):
        if not positions:
            continue
        pad4()
        pos_offset = len(buffer)
        pos_data = np.array(positions, dtype="<f4")
        buffer.extend(pos_data.tobytes())
        buffer_views.append({"buffer": 0, "byteOffset": pos_offset, "byteLength": pos_data.nbytes, "target": 34962})
        pos_view = len(buffer_views) - 1
        pos_reshaped = pos_data.reshape((-1, 3))
        accessors.append(
            {
                "bufferView": pos_view,
                "componentType": 5126,
                "count": int(pos_reshaped.shape[0]),
                "type": "VEC3",
                "min": [float(v) for v in pos_reshaped.min(axis=0)],
                "max": [float(v) for v in pos_reshaped.max(axis=0)],
            }
        )
        pos_accessor = len(accessors) - 1

        pad4()
        normal_offset = len(buffer)
        normal_data = np.array(builder.normals[mat_idx], dtype="<f4")
        buffer.extend(normal_data.tobytes())
        buffer_views.append({"buffer": 0, "byteOffset": normal_offset, "byteLength": normal_data.nbytes, "target": 34962})
        normal_view = len(buffer_views) - 1
        accessors.append(
            {
                "bufferView": normal_view,
                "componentType": 5126,
                "count": int(normal_data.size / 3),
                "type": "VEC3",
            }
        )
        normal_accessor = len(accessors) - 1

        pad4()
        index_offset = len(buffer)
        index_data = np.array(builder.indices[mat_idx], dtype="<u4")
        buffer.extend(index_data.tobytes())
        buffer_views.append({"buffer": 0, "byteOffset": index_offset, "byteLength": index_data.nbytes, "target": 34963})
        index_view = len(buffer_views) - 1
        accessors.append(
            {
                "bufferView": index_view,
                "componentType": 5125,
                "count": int(index_data.size),
                "type": "SCALAR",
                "min": [int(index_data.min())],
                "max": [int(index_data.max())],
            }
        )
        index_accessor = len(accessors) - 1

        primitives.append(
            {
                "attributes": {"POSITION": pos_accessor, "NORMAL": normal_accessor},
                "indices": index_accessor,
                "material": mat_idx,
            }
        )

    gltf = {
        "asset": {"version": "2.0", "generator": "NadLan Rainbow prototype generator 1.0"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "Rainbow Tel Aviv illustrative showroom massing"}],
        "meshes": [{"name": "Rainbow illustrative tower, boutique ring and amenity court", "primitives": primitives}],
        "materials": MATERIALS,
        "buffers": [{"byteLength": len(buffer)}],
        "bufferViews": buffer_views,
        "accessors": accessors,
    }
    json_chunk = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
    while len(json_chunk) % 4:
        json_chunk += b" "
    while len(buffer) % 4:
        buffer.append(0)

    total_len = 12 + 8 + len(json_chunk) + 8 + len(buffer)
    with path.open("wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, total_len))
        f.write(struct.pack("<I4s", len(json_chunk), b"JSON"))
        f.write(json_chunk)
        f.write(struct.pack("<I4s", len(buffer), b"BIN\0"))
        f.write(buffer)


def write_png(path: Path, width: int = 1600, height: int = 1000) -> None:
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        t = y / max(1, height - 1)
        top = np.array([12, 41, 45])
        bottom = np.array([218, 194, 143])
        canvas[y, :, :] = (top * (1 - t) + bottom * t).astype(np.uint8)

    horizon = int(height * 0.64)
    canvas[horizon:, :, :] = np.maximum(canvas[horizon:, :, :], np.array([28, 54, 45], dtype=np.uint8))
    sea_y = int(height * 0.55)
    canvas[sea_y : sea_y + 55, :, :] = np.array([25, 89, 106], dtype=np.uint8)

    def rect(x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
        x0, x1 = sorted((max(0, x0), min(width, x1)))
        y0, y1 = sorted((max(0, y0), min(height, y1)))
        canvas[y0:y1, x0:x1, :] = color

    # Boutique blocks.
    for x in [290, 420, 980, 1110, 1240]:
        rect(x, 505, x + 120, 700, (170, 160, 135))
        for yy in range(525, 690, 24):
            rect(x + 10, yy, x + 110, yy + 4, (218, 190, 120))

    # Main tower silhouette with a subtle spiral offset.
    for i in range(40):
        y = 685 - i * 11
        w = int(165 + math.sin(i * 0.2) * 12)
        x = int(720 + math.sin(i * 0.18) * 22 - w / 2)
        rect(x, y, x + w, y + 9, (42, 77, 77))
        rect(x, y, x + w, y + 2, (221, 177, 94))
        for bx in range(x + 18, x + w - 18, 28):
            rect(bx, y + 3, bx + 12, y + 8, (82, 145, 154))
    rect(675, 235, 840, 252, (221, 177, 94))
    rect(700, 700, 835, 730, (54, 68, 61))
    rect(540, 710, 980, 750, (37, 57, 47))

    raw = bytearray()
    for row in canvas:
        raw.append(0)
        raw.extend(row.tobytes())

    def chunk(name: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def unit_records() -> list[dict[str, object]]:
    records = []
    seed = [
        ("unit-08-sw", 8, 3, 82, 10, "דרום מערב", "מבט לחצר ולים", "0 31 6", "45deg 66deg auto"),
        ("unit-16-w", 16, 4, 112, 14, "מערב", "קו החוף ושדה דב", "-5 55 7", "35deg 63deg auto"),
        ("unit-24-nw", 24, 4, 128, 16, "צפון מערב", "ים, פארק וצפון תל אביב", "-6 80 5", "24deg 61deg auto"),
        ("unit-31-se", 31, 5, 156, 22, "דרום מזרח", "קו הרקיע והחצר הפנימית", "6 101 -5", "310deg 64deg auto"),
        ("unit-38-penthouse", 38, 5, 210, 42, "מערב", "פנטהאוז גבוה לכיוון הים", "0 124 7", "32deg 58deg auto"),
        ("unit-boutique-07", 7, 4, 118, 18, "מערב", "בניין בוטיק סביב הלגונה", "-42 25 24", "55deg 67deg auto"),
    ]
    for uid, floor, rooms, sqm, balcony, direction, view, position, orbit in seed:
        records.append(
            {
                "id": uid,
                "title": f"דירת {rooms} חדרים, קומה {floor}",
                "floor": floor,
                "rooms": rooms,
                "sqm": sqm,
                "balcony": balcony,
                "dir": direction,
                "line": uid.split("-")[-1].upper(),
                "view": view,
                "building": "Rainbow Tel Aviv",
                "status": "לפי פנייה",
                "availability": "זמינות להדגמה בלבד עד לקבלת מלאי רשמי מהיזם",
                "price_estimate": 0,
                "price_note": "אומדן מחיר יוצג רק לאחר אישור מקור נתונים. לא הצעה ולא התחייבות.",
                "note": "יחידת הדגמה למיפוי חוויית showroom. להחלפה בתוכנית מכר רשמית.",
                "source_note": "מודל אבטיפוס מקורי על בסיס מקורות פומביים, לא BIM רשמי.",
                "hotspot_position": position,
                "hotspot_normal": "0 0 1",
                "camera_orbit": orbit,
            }
        )
    return records


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_docs() -> None:
    source_notes = f"""# Rainbow Tel Aviv Prototype Model Source Notes

This folder is an **illustrative prototype package** for the approved v1.63.0 model-viewer rail.
It is not official Rainbow BIM, not an official sale plan and not live inventory.

## Public Facts Used

- Official/marketing sources describe Rainbow as a Sde Dov coastal project by Israel Canada with a tower and surrounding boutique buildings.
- Public sources disagree on exact counts: developer/marketing material commonly says 480 units; planning/Madlan-style sources show 459 units and 7 buildings / 8-40 floors. The public page must keep that truth-first discrepancy disclosure.
- Sde Dov/Rainbow public materials mention pools, spa, fitness, cafe/workspaces, sea proximity and resort-style positioning.

## Sources To Recheck Before Public Claims

- https://rainbow-telaviv.com/
- https://www.israel-canada.co.il/projects/tel-aviv/rainbow
- https://sdedov.co.il/project/rainbow/
- https://www.madlan.co.il/projects/%D7%97%D7%9C%D7%A7%D7%94_15_%D7%A9%D7%93%D7%94_%D7%93%D7%91_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91
- https://en.globes.co.il/en/article-eyal-waldman-buys-sde-dov-apartments-for-nis-50m-1001483936

## Public Safety

- Label this model as illustrative until official developer material replaces it.
- Do not present the demo units as available stock.
- Do not present exact prices unless the owner approves a public or licensed source.
- Replace `project_model_glb` with an official BIM/GLB when Israel Canada or the project manager supplies one.
"""
    (OUT / "source-notes.md").write_text(source_notes, encoding="utf-8")

    qa = """# Rainbow Prototype Model QA

## Generated Artifacts

- `model.glb`: original lightweight architectural massing of the Rainbow tower, boutique ring and central amenity court.
- `poster.png`: lightweight poster for `<model-viewer>` before the GLB reveals.
- `unit-map.json`: demo unit records with model-viewer hotspot coordinates.
- `project-meta-example.json`: copy/paste map for the CMS fields added in v1.63.0.
- `drawings.json`: placeholder slots for official elevation/floor/site drawings.
- `environment.json`: surroundings starter data to be replaced by the map/POI layer.

## Local Validation

Run:

```powershell
python scripts/generate-rainbow-prototype-model.py
node -e "const fs=require('fs'); const b=fs.readFileSync('assets/projects/rainbow-tel-aviv/model.glb'); console.log(b.subarray(0,4).toString(), b.readUInt32LE(4), b.readUInt32LE(8), b.length)"
```

Expected:

- Magic: `glTF`
- Version: `2`
- File size under 8 MB.
- `project_3d_units` JSON has `hotspot_position`, `hotspot_normal`, `camera_orbit` for each demo unit.

## Browser Gate After v1.63.0 Is Installed

1. Upload `model.glb` and `poster.png` to WordPress Media or serve from GitHub raw/CDN.
2. Set `project_model_glb`, `project_model_poster`, and `project_3d_units` from `project-meta-example.json`.
3. Open `/projects/rainbow-tel-aviv/`.
4. Confirm the procedural fallback remains visible until the model loads.
5. Confirm the GLB becomes the stage, drag rotates the building, and each hotspot selects the matching unit.
6. Confirm lead/compare/map actions still carry the selected unit.
7. Confirm mobile has no horizontal overflow and no nested gray scrollbars.

## Honest Boundary

This is a contractor-demo model package. It proves the CMS rail and interaction pattern; it is not a substitute for official developer BIM, official drawings, live inventory or binding price data.
"""
    (OUT / "qa.md").write_text(qa, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    build_glb(OUT / "model.glb")
    write_png(OUT / "poster.png")
    units = unit_records()
    write_json(OUT / "unit-map.json", units)
    write_json(
        OUT / "project-meta-example.json",
        {
            "project_model_glb": f"{RAW_BASE}/model.glb",
            "project_model_poster": f"{RAW_BASE}/poster.png",
            "project_model_usdz": "",
            "project_3d_units": units,
            "project_3d_drawings_json": [
                {
                    "label": "חזית מגדל",
                    "type": "elevation",
                    "url": "",
                    "source": "להשלמה מתוכנית מכר / חומר יזם",
                },
                {
                    "label": "תוכנית טיפוסית",
                    "type": "floor_plan",
                    "url": "",
                    "source": "להשלמה מתוכנית מכר / חומר יזם",
                },
            ],
        },
    )
    write_json(
        OUT / "drawings.json",
        {
            "status": "placeholder-slots",
            "required": ["official_elevation", "typical_floor_plan", "site_plan", "unit_plan"],
            "note": "Attach only approved developer drawings or owner-licensed material.",
        },
    )
    write_json(
        OUT / "environment.json",
        {
            "status": "starter",
            "location": {"lat": 32.1108, "lng": 34.7805, "source": "Sde Dov center placeholder"},
            "layers": ["sea", "future Sde Dov district", "light rail / transport", "schools and kindergartens", "parks"],
            "next_step": "Replace with sourced POI/map layer and Cesium/Google Photorealistic 3D Tiles view when approved.",
        },
    )
    write_docs()
    size = os.path.getsize(OUT / "model.glb")
    print(f"Wrote {OUT / 'model.glb'} ({size:,} bytes)")
    print(f"Wrote {OUT / 'poster.png'} ({os.path.getsize(OUT / 'poster.png'):,} bytes)")


if __name__ == "__main__":
    main()
