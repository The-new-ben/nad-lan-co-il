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
BRANCH = os.getenv("RAINBOW_MODEL_REF", "main")
RAW_BASE = f"https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/{BRANCH}/assets/projects/rainbow-tel-aviv"
PLAN_BASE = f"{RAW_BASE}/plans"
RAINBOW_INDICATIVE_AVG_PRICE_PER_SQM = 76000
RAINBOW_PRICE_SOURCE_NOTE = (
    "אומדן לא מחייב לפי מחיר ממוצע למ\"ר שמוצג במדלן לפרויקט/סביבה, "
    "נבדק 14.6.2026. לא הצעה ולא התחייבות; יש לאמת מחיר, זמינות ותנאים מול היזם."
)
RAINBOW_LAT = 32.1108
RAINBOW_LNG = 34.7805
RAINBOW_GROUND_ELEVATION_M = 8.0
RAINBOW_FLOOR_HEIGHT_M = 3.05


MATERIALS = [
    {
        "name": "deep teal low iron glass",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.025, 0.20, 0.21, 0.9],
            "metallicFactor": 0.02,
            "roughnessFactor": 0.18,
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
        "name": "warm stone shell",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.82, 0.78, 0.68, 1.0],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.62,
        },
    },
    {
        "name": "sea reflection glazing",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.38, 0.72, 0.78, 0.62],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.12,
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
            "baseColorFactor": [0.16, 0.25, 0.19, 1.0],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.8,
        },
    },
    {
        "name": "pool deck porcelain",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.80, 0.74, 0.62, 1.0],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.5,
        },
    },
    {
        "name": "soft shadow massing",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.05, 0.09, 0.08, 0.58],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.9,
        },
        "alphaMode": "BLEND",
        "doubleSided": True,
    },
    {
        "name": "champagne facade glow",
        "pbrMetallicRoughness": {
            "baseColorFactor": [1.0, 0.82, 0.45, 1.0],
            "metallicFactor": 0.28,
            "roughnessFactor": 0.32,
        },
    },
    {
        "name": "coastal sand",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.72, 0.66, 0.52, 1.0],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.82,
        },
    },
    {
        "name": "promenade paving",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.42, 0.47, 0.43, 1.0],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.72,
        },
    },
    {
        "name": "future district silhouette",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.08, 0.18, 0.18, 0.42],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.78,
        },
        "alphaMode": "BLEND",
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
    # Public sources describe the tower as spiral-shaped. This is a stylized,
    # original massing curve, not a traced or official facade.
    angle = floor * 0.145
    sx = 16.2 + 2.0 * math.sin(angle * 0.9)
    sz = 10.6 + 1.1 * math.cos(angle * 0.7)
    x = 1.85 * math.sin(angle * 0.82)
    z = 1.25 * math.cos(angle * 0.72)
    rot = angle * 0.58
    return sx, sz, x, z, rot


def add_tower(builder: MeshBuilder) -> None:
    floor_h = 3.05
    base_y = 7.0
    floors = 42

    # Double-height resort lobby and podium base.
    builder.add_box(2, (0, 2.0, 0), (34, 4.0, 20), rot_y=0.04)
    builder.add_box(6, (0, 4.4, 0), (29, 1.0, 17), rot_y=0.04)
    builder.add_box(0, (0.3, base_y + floors * floor_h / 2, 0.1), (12.7, floors * floor_h, 7.9), rot_y=0.18)
    builder.add_box(7, (0.8, 1.8, -2.8), (42, 0.12, 31), rot_y=0.04)

    for floor in range(1, floors + 1):
        y = base_y + floor * floor_h
        sx, sz, x, z, rot = floor_shape(floor)
        slab_h = 0.13 if floor % 3 else 0.19
        builder.add_box(1, (x, y, z), (sx, slab_h, sz), rot_y=rot)

        if floor % 4 == 0:
            builder.add_box(2, (x, y + 0.18, z), (sx * 0.78, 0.09, sz * 0.72), rot_y=rot)

        # Horizontal balcony rails and window rhythm. The west/east bands are
        # deliberately stronger than the old fallback so the model reads as a
        # residential tower at first glance.
        for side in (-1, 1):
            for bay in (-0.38, -0.13, 0.13, 0.38):
                builder.add_box(3, (x + bay * sx, y + 1.38, z + side * (sz / 2 + 0.06)), (sx * 0.13, 1.62, 0.08), rot_y=rot)
            builder.add_box(1, (x, y + 2.08, z + side * (sz / 2 + 0.18)), (sx * 0.92, 0.07, 0.18), rot_y=rot)
            builder.add_box(3, (x, y + 0.62, z + side * (sz / 2 + 0.2)), (sx * 0.82, 0.42, 0.08), rot_y=rot)

        for side in (-1, 1):
            for bay in (-0.36, -0.12, 0.12, 0.36):
                builder.add_box(3, (x + side * (sx / 2 + 0.07), y + 1.32, z + bay * sz), (0.08, 1.45, sz * 0.12), rot_y=rot)

        if floor % 2 == 0:
            # Thin champagne ribs keep the schematic tower readable while spinning.
            builder.add_box(8, (x - sx / 2 - 0.12, y + 1.35, z), (0.12, 2.35, sz * 0.72), rot_y=rot)
            builder.add_box(8, (x + sx / 2 + 0.12, y + 1.35, z), (0.12, 2.35, sz * 0.72), rot_y=rot)

        if floor in {8, 16, 24, 31, 38}:
            # Demo-unit bands align with the CMS hotspot set without claiming real inventory.
            builder.add_box(8, (x, y + 1.62, z + sz / 2 + 0.38), (sx * 0.55, 0.26, 0.18), rot_y=rot)

    top_y = base_y + floors * floor_h
    # Rooftop crown and amenity terrace.
    builder.add_box(1, (0.6, top_y + 0.9, 0.2), (18.5, 1.1, 13.2), rot_y=0.44)
    builder.add_box(6, (0.6, top_y + 1.62, 0.2), (16.8, 0.38, 11.2), rot_y=0.44)
    builder.add_box(4, (3.8, top_y + 1.9, -1.2), (7.8, 0.12, 3.0), rot_y=0.44)
    builder.add_box(1, (0.6, top_y + 2.65, 0.2), (15.8, 0.78, 10.8), rot_y=0.44)


def add_boutique_ring(builder: MeshBuilder) -> None:
    # Six 8-floor boutique blocks around the inner court, matching the public
    # developer language while keeping this as an original schematic massing.
    blocks = [
        (-42, 18, 30, 12, -0.08),
        (-23, 37, 28, 12, 0.18),
        (20, 39, 32, 12, -0.12),
        (44, 16, 26, 12, 0.1),
        (28, -32, 34, 12, 0.2),
        (-27, -33, 34, 12, -0.18),
    ]
    for idx, (x, z, sx, sz, rot) in enumerate(blocks):
        floors = 8
        h = floors * 3.05
        builder.add_box(2, (x, h / 2 + 2.0, z), (sx, h, sz), rot_y=rot)
        builder.add_box(0, (x, h / 2 + 2.1, z + 0.08), (sx * 0.82, h * 0.96, sz * 0.78), rot_y=rot)
        for floor in range(1, floors + 1):
            y = 2.0 + floor * 3.05
            builder.add_box(1, (x, y, z), (sx * 1.02, 0.12, sz * 1.05), rot_y=rot)
            for side in (-1, 1):
                builder.add_box(3, (x, y + 1.2, z + side * (sz / 2 + 0.05)), (sx * 0.72, 1.35, 0.06), rot_y=rot)
            for side in (-1, 1):
                builder.add_box(3, (x + side * (sx / 2 + 0.05), y + 1.15, z), (0.06, 1.25, sz * 0.58), rot_y=rot)
        builder.add_box(6, (x, h + 3.0, z), (sx * 1.04, 0.22, sz * 1.08), rot_y=rot)
        builder.add_box(4, (x + sx * 0.18, h + 3.18, z - sz * 0.14), (sx * 0.24, 0.08, sz * 0.22), rot_y=rot)
        builder.add_box(8, (x, 2.1, z + sz / 2 + 0.35), (sx * 0.72, 0.18, 0.16), rot_y=rot)


def add_site(builder: MeshBuilder) -> None:
    builder.add_box(5, (0, -0.08, 0), (120, 0.12, 104), rot_y=0)
    builder.add_box(7, (0, -0.01, 0), (104, 0.06, 84), rot_y=0)

    # Central lagoon / pool court plus a coastal water strip behind the complex.
    builder.add_box(4, (0, 0.04, 0), (46, 0.1, 24), rot_y=0.03)
    builder.add_box(4, (-9, 0.06, 3), (22, 0.1, 13), rot_y=0.45)
    builder.add_box(4, (24, 0.05, -7), (12, 0.1, 4.5), rot_y=-0.22)
    builder.add_box(4, (0, 0.02, 64), (154, 0.08, 26), rot_y=0)
    builder.add_box(9, (0, 0.055, 49.5), (142, 0.08, 8.5), rot_y=0)
    builder.add_box(10, (0, 0.10, 41.8), (120, 0.08, 4.2), rot_y=0)
    builder.add_box(5, (-37, 0.12, 35), (32, 0.08, 5.5), rot_y=0.08)
    builder.add_box(5, (38, 0.12, 35), (34, 0.08, 5.0), rot_y=-0.07)
    builder.add_box(10, (-58, 0.13, -4), (3.2, 0.08, 86), rot_y=-0.05)
    builder.add_box(10, (58, 0.13, -6), (3.2, 0.08, 82), rot_y=0.06)

    # Low surrounding district masses frame the project without fake exact pins.
    for x, z, sx, sz, h, rot in [
        (-72, -18, 18, 16, 22, 0.04),
        (-70, 18, 22, 14, 28, -0.05),
        (72, -20, 20, 15, 24, -0.04),
        (74, 17, 24, 14, 30, 0.05),
        (-26, -58, 30, 12, 18, 0.02),
        (24, -58, 32, 12, 20, -0.02),
    ]:
        builder.add_box(11, (x, h / 2, z), (sx, h, sz), rot_y=rot)
        for floor_y in range(5, int(h), 7):
            builder.add_box(7, (x, floor_y, z + sz / 2 + 0.08), (sx * 0.72, 0.18, 0.08), rot_y=rot)

    # Entry court, deck seams and water-edge lines make the model read as an
    # inspectable showroom object rather than an isolated tower icon.
    for offset in (-20, -10, 10, 20):
        builder.add_box(10, (offset, 0.16, -39), (1.2, 0.08, 36), rot_y=0.22)
    for offset in (-16, 0, 16):
        builder.add_box(8, (offset, 0.22, 13), (18, 0.08, 0.28), rot_y=0.03)

    # Landscape markers / palm-like verticals. Abstract enough to avoid clip-art,
    # but enough to cue the resort setting at model-viewer scale.
    for x, z in [(-36, -5), (-29, 0), (-18, 15), (17, -14), (31, 3), (38, -18), (0, 23), (0, -24), (14, 22), (-12, -18)]:
        builder.add_box(1, (x, 0.72, z), (0.55, 1.45, 0.55), rot_y=0)
        builder.add_box(5, (x, 1.55, z), (1.65, 0.26, 1.65), rot_y=0.35)


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


def write_png(path: Path, width: int = 1280, height: int = 800) -> None:
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        t = y / max(1, height - 1)
        top = np.array([8, 35, 39])
        mid = np.array([42, 65, 58])
        bottom = np.array([223, 199, 151])
        if t < 0.62:
            local = t / 0.62
            color = top * (1 - local) + mid * local
        else:
            local = (t - 0.62) / 0.38
            color = mid * (1 - local) + bottom * local
        canvas[y, :, :] = color.astype(np.uint8)

    # Subtle vignette so the poster feels like a showroom hero, not a flat icon.
    yy, xx = np.mgrid[0:height, 0:width]
    d = ((xx - width * 0.52) / (width * 0.72)) ** 2 + ((yy - height * 0.48) / (height * 0.86)) ** 2
    vignette = np.clip(1.18 - d * 0.5, 0.68, 1.0)
    canvas = np.clip(canvas.astype(float) * vignette[..., None], 0, 255).astype(np.uint8)

    sea_y = int(height * 0.55)
    canvas[sea_y : sea_y + 70, :, :] = np.array([20, 87, 105], dtype=np.uint8)
    canvas[sea_y + 6 : sea_y + 10, :, :] = np.array([79, 139, 148], dtype=np.uint8)

    def rect(x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
        x0 = int(round(x0 * width / 1600))
        x1 = int(round(x1 * width / 1600))
        y0 = int(round(y0 * height / 1000))
        y1 = int(round(y1 * height / 1000))
        x0, x1 = sorted((max(0, x0), min(width, x1)))
        y0, y1 = sorted((max(0, y0), min(height, y1)))
        canvas[y0:y1, x0:x1, :] = color

    # Main shadow / podium.
    rect(500, 718, 1040, 780, (28, 48, 42))
    rect(545, 690, 995, 724, (70, 82, 70))
    rect(585, 646, 955, 676, (179, 158, 103))

    # Boutique blocks, staggered around the inner court.
    for x, y0, w, h in [(255, 520, 132, 190), (405, 500, 130, 205), (1050, 500, 138, 205), (1210, 522, 130, 188), (350, 690, 168, 92), (1080, 690, 168, 92)]:
        rect(x + 12, y0 + 10, x + w + 12, y0 + h + 10, (65, 83, 77))
        rect(x, y0, x + w, y0 + h, (188, 176, 148))
        rect(x, y0, x + w, y0 + 5, (220, 184, 100))
        for yy2 in range(y0 + 24, y0 + h - 12, 26):
            rect(x + 12, yy2, x + w - 12, yy2 + 5, (225, 194, 121))
            rect(x + 28, yy2 + 7, x + w - 28, yy2 + 12, (66, 124, 132))

    # Lagoon / resort court.
    rect(590, 680, 950, 710, (22, 112, 125))
    rect(690, 650, 880, 674, (35, 139, 151))
    rect(735, 630, 825, 644, (236, 204, 128))

    # Main tower silhouette with a subtle spiral offset.
    for i in range(42):
        y = 704 - i * 11
        w = int(160 + math.sin(i * 0.24) * 20)
        x = int(770 + math.sin(i * 0.18) * 30 - w / 2)
        shade = 54 + int(i * 0.7)
        rect(x + 12, y + 3, x + w + 12, y + 12, (22, 43, 42))
        rect(x, y, x + w, y + 9, (34, shade, 70))
        rect(x, y, x + w, y + 2, (222, 178, 93))
        rect(x + 4, y + 3, x + 14, y + 8, (214, 199, 157))
        for bx in range(x + 24, x + w - 18, 30):
            rect(bx, y + 3, bx + 13, y + 8, (88, 157, 166))
    rect(682, 218, 875, 236, (223, 185, 102))
    rect(713, 236, 848, 246, (94, 126, 120))
    rect(708, 704, 850, 738, (55, 73, 64))

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
        ("unit-08-sw", 8, 3, 82, 10, "דרום מערב", "מבט לחצר ולים", "0 31 6", "45deg 66deg auto", "plan-3br.svg", "תוכנית המחשה מקורית לדירת 3 חדרים. יש להחליף בתוכנית מכר רשמית."),
        ("unit-16-w", 16, 4, 112, 14, "מערב", "קו החוף ושדה דב", "-5 55 7", "35deg 63deg auto", "plan-4br.svg", "תוכנית המחשה מקורית לדירת 4 חדרים עם מרפסת מערבית. יש להחליף בתוכנית מכר רשמית."),
        ("unit-24-nw", 24, 4, 128, 16, "צפון מערב", "ים, פארק וצפון תל אביב", "-6 80 5", "24deg 61deg auto", "plan-4br.svg", "תוכנית המחשה מקורית לדירת 4 חדרים גבוהה. יש להחליף בתוכנית מכר רשמית."),
        ("unit-31-se", 31, 5, 156, 22, "דרום מזרח", "קו הרקיע והחצר הפנימית", "6 101 -5", "310deg 64deg auto", "plan-5br.svg", "תוכנית המחשה מקורית לדירת 5 חדרים. יש להחליף בתוכנית מכר רשמית."),
        ("unit-38-penthouse", 38, 5, 210, 42, "מערב", "פנטהאוז גבוה לכיוון הים", "0 124 7", "32deg 58deg auto", "plan-penthouse.svg", "תוכנית פנטהאוז להמחשה בלבד. לא תוכנית מכר ולא התחייבות."),
        ("unit-boutique-07", 7, 4, 118, 18, "מערב", "בניין בוטיק סביב הלגונה", "-42 25 24", "55deg 67deg auto", "plan-boutique.svg", "תוכנית המחשה לבניין הבוטיק סביב הלגונה. יש להחליף בתוכנית מכר רשמית."),
    ]
    for uid, floor, rooms, sqm, balcony, direction, view, position, orbit, plan_file, view_note in seed:
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
                "plan": f"{PLAN_BASE}/{plan_file}",
                "interior_url": "",
                "tour_url": "",
                "view_note": view_note,
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

- Official/marketing sources describe Rainbow as a Sde Dov coastal project by Israel Canada with six boutique buildings, a spiral / spiral-like residential tower, lagoon/resort positioning and coastal views.
- Developer/architect sources describe 6 boutique buildings and a 42-story spiral-designed tower; press/planning-style sources describe a 40-story tower, 6 additional 8-floor buildings and 459 units. The public page must keep that truth-first discrepancy disclosure.
- Sde Dov/Rainbow public materials mention pools, spa, fitness, cafe/workspaces, sea proximity and resort-style positioning.
- For the prototype only, `project_3d_avg_price_per_sqm` uses a public Madlan-style average of 76,000 NIS per sqm as an indicative calculation basis. It is not official stock, not an offer and not a commitment.

## Sources To Recheck Before Public Claims

- https://rainbow-telaviv.com/
- https://www.blk.co.il/rainbow
- https://www.israel-canada.co.il/projects/tel-aviv/rainbow
- https://sdedov.co.il/project/rainbow/
- https://sdedov.co.il/projects/
- https://sdedov.co.il/faq/
- https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx
- https://www.gov.il/he/pages/sdedov-pr-22072020
- https://timeout.co.il/%D7%A8%D7%95%D7%91%D7%A2-%D7%A9%D7%93%D7%94-%D7%93%D7%91-%D7%A4%D7%90%D7%A8%D7%A7%D7%99%D7%9D/
- https://www.madlan.co.il/projects/%D7%97%D7%9C%D7%A7%D7%94_15_%D7%A9%D7%93%D7%94_%D7%93%D7%91_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91
- https://en.globes.co.il/en/article-eyal-waldman-buys-sde-dov-apartments-for-nis-50m-1001483936

## Environment Layer Sources

- Sde Dov information site project index: names the marketed projects used in
  `environment.json` (`Rainbow`, `DIMRI YAMA`, `GINDI VOGUE`, `ASHIRA BY AVISROR`,
  `FIRST BY HAGAG`, `זוהי`, `UTOPIA`).
- Tel Aviv municipality Sde Dov page: district scale, master-plan status, parks, transport,
  commerce/employment and public-services framing.
- Gov.il planning announcement: 16,000 homes and district-scale public/commercial/employment
  program.
- Time Out Tel Aviv parks report: public report on park design-plan approval for the coastal,
  runway and linear parks.

Do not turn nearby project names into exact map pins until their coordinates are verified from a
trusted map/source.

## Public Safety

- Label this model as illustrative until official developer material replaces it.
- The `plans/*.svg` files are original schematic showroom aids, not official sale plans.
- Do not present the demo units as available stock.
- Do not present exact prices unless the owner approves a public or licensed source.
- Any public estimate must carry the visible non-binding source note in `project_3d_price_source_note`.
- Keep `project_3d_video_url`, `project_3d_tour_url`, `project_3d_cesium_tiles_url`,
  and unit-level `interior_url`/`tour_url` empty until the owner or developer supplies
  approved material. Do not use fake tours, copied developer media, or stock interiors.
- Replace `project_model_glb` with an official BIM/GLB when Israel Canada or the project manager supplies one.

## Prototype Design Basis

- Tower massing: original 42-level spiral-inspired stack, based on public descriptions of a spiral-designed Rainbow tower. It is not traced from any render.
- Boutique ring: six 8-floor blocks around a central resort court, based on the public complex description.
- Resort layer: lagoon/pool court, roof amenity hints, landscape markers, coastal strip, promenade and park ribbons are schematic cues only.
- Context masses: low surrounding silhouettes suggest the future Sde Dov district scale, but are not exact neighboring project pins or approved 3D city data.
- Facade cues: champagne ribs and highlighted demo-unit bands are interaction/readability aids for the prototype spinner, not official sale elevations.
- No faces, no copied stock, no copied developer images, no official inventory claims.
"""
    (OUT / "source-notes.md").write_text(source_notes, encoding="utf-8")

    qa = """# Rainbow Prototype Model QA

## Generated Artifacts

- `model.glb`: original lightweight architectural massing of the Rainbow tower, boutique ring and central amenity court.
- `poster.png`: lightweight poster for `<model-viewer>` before the GLB reveals.
- `unit-map.json`: demo unit records with model-viewer hotspot coordinates.
- `project-meta-example.json`: copy/paste map for the CMS fields added in v1.63.0.
- `plans/*.svg`: original schematic unit/site plans for the prototype plan overlay.
- `drawings.json`: prototype drawing map plus slots for official elevation/floor/site drawings.
- `environment.json`: surroundings starter data to be replaced by the map/POI layer.
- `material-intake-template.json`: contractor/developer handoff checklist mapping each official
  material to its CMS field, accepted formats and public-use policy.
- `view-layer-config.json`: Mapbox-now / Cesium-ready view-from-apartment contract with
  camera formulas, per-unit altitude/bearing, overlays and cost controls.
- Media/tour slots: `project_3d_video_url`, `project_3d_tour_url`,
  `project_3d_cesium_tiles_url`, and per-unit `interior_url`/`tour_url` are present
  but intentionally blank until official or owner-approved material is supplied.

## Local Validation

Run:

```powershell
python scripts/generate-rainbow-prototype-model.py
node -e "const fs=require('fs'); const b=fs.readFileSync('assets/projects/rainbow-tel-aviv/model.glb'); console.log(b.subarray(0,4).toString(), b.readUInt32LE(4), b.readUInt32LE(8), b.length)"
```

Expected:

- Magic: `glTF`
- Version: `2`
- `model.glb` under 4 MB for the prototype massing.
- `poster.png` under 80 KB for a repo-committed lightweight poster.
- `project_3d_units` JSON has `hotspot_position`, `hotspot_normal`, `camera_orbit` and `plan` for each demo unit.
- Each unit has empty `interior_url` and `tour_url` keys so the CMS contract is ready
  for approved unit media without changing the data shape later.
- `material-intake-template.json` lists at least eight handoff slots and keeps prototype material
  separate from official/developer-approved material.
- `view-layer-config.json` keeps the default state building-first, defines user-opened map/tiles
  behavior, and gives each unit a derived altitude and bearing for view-from-apartment QA.

## Browser Gate After v1.63.0 Is Installed

1. Upload `model.glb` and `poster.png` to WordPress Media or serve from GitHub raw/CDN.
2. Set `project_model_glb`, `project_model_poster`, `project_3d_units`, `project_3d_drawings_json` and `project_3d_environment_json` from `project-meta-example.json`.
3. Open `/projects/rainbow-tel-aviv/`.
4. Confirm the procedural fallback remains visible until the model loads.
5. Confirm the GLB becomes the stage, drag rotates the building, and each hotspot selects the matching unit.
6. Confirm the plan overlay opens the relevant schematic plan for each selected unit.
7. Confirm lead/compare/map actions still carry the selected unit.
8. Confirm mobile has no horizontal overflow and no nested gray scrollbars.

## Honest Boundary

This is a contractor-demo model package. It proves the CMS rail and interaction pattern; it is not a substitute for official developer BIM, official drawings, live inventory or binding price data.
"""
    (OUT / "qa.md").write_text(qa, encoding="utf-8")


def environment_payload() -> dict[str, object]:
    """Source-aware surroundings data for the prototype showroom.

    This intentionally separates sourced district/project facts from exact map
    pins. Nearby project names can render as cards/chips now; exact clickable
    coordinates must wait for verified pins.
    """

    sde_dov_projects_url = "https://sdedov.co.il/projects/"
    municipal_url = "https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx"
    return {
        "status": "prototype_sourced",
        "updated": "2026-06-14",
        "project": {
            "name": "Rainbow Tel Aviv",
            "district": "רובע שדה דב",
            "center": {
                "lat": 32.1108,
                "lng": 34.7805,
                "precision": "prototype",
                "source_note": "Approximate Sde Dov / Rainbow showroom center. Replace with verified project survey pin.",
            },
        },
        "source_policy": "Public district and marketing facts only. No paid-source transaction rows, no official inventory claims and no unsourced exact pins.",
        "district_context": {
            "planned_units": 16000,
            "planning_area_dunam": 1300,
            "planned_population": 40000,
            "planned_commerce_sqm": 126000,
            "planned_employment_sqm": 330000,
            "planned_hotel_rooms": 2000,
            "planning_status": "Master plan approved in August 2020; detailed plans and permits are project-specific.",
            "boundaries": {
                "west": "חוף הים",
                "north": "רחוב פרופס",
                "east": "רחוב לוי אשכול",
                "south": "רחוב ש\"י עגנון",
            },
            "sources": [
                {
                    "label": "עיריית תל אביב-יפו - רובע שדה דב",
                    "url": municipal_url,
                    "notes": "Master-plan scale, mixed-use program, parks, public buildings and transport principles.",
                },
                {
                    "label": "אתר המידע רובע שדה דב - שאלות ותשובות",
                    "url": "https://sdedov.co.il/faq/",
                    "notes": "District boundaries, 16,000 planned homes and division into Eshkol, Central and North areas.",
                },
                {
                    "label": "Gov.il - תכנית המתאר לרובע שדה דב",
                    "url": "https://www.gov.il/he/pages/sdedov-pr-22072020",
                    "notes": "Government planning announcement: 16,000 homes, public areas, commerce, employment, hotels and green areas.",
                },
            ],
        },
        "layers": [
            {
                "id": "neighbor_projects",
                "label": "פרויקטים בסביבה",
                "ui": "clickable_project_chips",
                "items": [
                    {
                        "id": "rainbow",
                        "name": "Rainbow Tel Aviv",
                        "area": "אשכול",
                        "status": "בשיווק / היתר בנייה לפי אתר המידע",
                        "map_status": "has_project_page",
                        "source_url": sde_dov_projects_url,
                        "source_note": "Listed by the Sde Dov information site as a marketed project.",
                    },
                    {
                        "id": "dimri-yama",
                        "name": "DIMRI YAMA",
                        "area": "אשכול",
                        "status": "בשיווק",
                        "map_status": "needs_precise_pin",
                        "source_url": sde_dov_projects_url,
                        "source_note": "Listed by the Sde Dov information site as a marketed project.",
                    },
                    {
                        "id": "gindi-vogue",
                        "name": "GINDI VOGUE",
                        "area": "מרכז",
                        "status": "בשיווק",
                        "map_status": "needs_precise_pin",
                        "source_url": sde_dov_projects_url,
                        "source_note": "Listed by the Sde Dov information site as a marketed project.",
                    },
                    {
                        "id": "ashira",
                        "name": "ASHIRA BY AVISROR",
                        "area": "אשכול",
                        "status": "בשיווק / הבנייה בעיצומה לפי אתר המידע",
                        "map_status": "needs_precise_pin",
                        "source_url": sde_dov_projects_url,
                        "source_note": "Listed by the Sde Dov information site as a marketed project.",
                    },
                    {
                        "id": "first-by-hagag",
                        "name": "FIRST BY HAGAG",
                        "area": "מרכז",
                        "status": "בשיווק",
                        "map_status": "needs_precise_pin",
                        "source_url": sde_dov_projects_url,
                        "source_note": "Listed by the Sde Dov information site as a marketed project.",
                    },
                    {
                        "id": "zohi",
                        "name": "זוהי",
                        "area": "אשכול",
                        "status": "בשיווק",
                        "map_status": "needs_precise_pin",
                        "source_url": sde_dov_projects_url,
                        "source_note": "Listed by the Sde Dov information site as a marketed project.",
                    },
                    {
                        "id": "utopia",
                        "name": "UTOPIA",
                        "area": "אשכול",
                        "status": "בשיווק",
                        "map_status": "needs_precise_pin",
                        "source_url": sde_dov_projects_url,
                        "source_note": "Listed by the Sde Dov information site as a marketed project.",
                    },
                ],
            },
            {
                "id": "parks_and_coast",
                "label": "ים, פארקים וטיילת",
                "ui": "environment_cards",
                "items": [
                    {
                        "id": "coastal_park",
                        "name": "פארק חופי",
                        "type": "planned_park",
                        "status": "מתוכנן",
                        "source_url": municipal_url,
                        "source_note": "The municipal district page describes a coastal park and a broad open-space network.",
                    },
                    {
                        "id": "runway_park",
                        "name": "פארק המסלול",
                        "type": "planned_park",
                        "status": "מתוכנן",
                        "source_url": "https://timeout.co.il/%D7%A8%D7%95%D7%91%D7%A2-%D7%A9%D7%93%D7%94-%D7%93%D7%91-%D7%A4%D7%90%D7%A8%D7%A7%D7%99%D7%9D/",
                        "source_note": "Public report on three approved park design plans, including the runway park.",
                    },
                    {
                        "id": "linear_park",
                        "name": "פארק ליניארי",
                        "type": "planned_park",
                        "status": "מתוכנן",
                        "source_url": municipal_url,
                        "source_note": "The municipal page lists the linear park among planned green spaces.",
                    },
                ],
            },
            {
                "id": "mobility",
                "label": "נגישות ותחבורה",
                "ui": "mobility_facts",
                "items": [
                    {
                        "id": "green_line",
                        "name": "הקו הירוק של הרכבת הקלה",
                        "type": "planned_light_rail",
                        "status": "מקודם / בעבודות הכנה לפי העירייה",
                        "source_url": municipal_url,
                        "source_note": "The municipal page says the Green Line is planned to cross the district south-north and connect toward Holon/Rishon, Herzliya and Ramat HaHayal.",
                    },
                    {
                        "id": "ibn_gabirol_extension",
                        "name": "המשך אבן גבירול",
                        "type": "planned_street_axis",
                        "status": "מתוכנן",
                        "source_url": municipal_url,
                        "source_note": "The municipal page describes the north-south axis and mixed movement options.",
                    },
                    {
                        "id": "walk_bike_grid",
                        "name": "רשת הליכה ואופניים",
                        "type": "public_realm",
                        "status": "מתוכנן",
                        "source_url": municipal_url,
                        "source_note": "The municipal page emphasizes walking, cycling and non-motorized mobility.",
                    },
                ],
            },
            {
                "id": "public_services",
                "label": "שירותים ציבוריים",
                "ui": "service_cards",
                "items": [
                    {
                        "id": "education_public_buildings",
                        "name": "חינוך ומבני ציבור",
                        "type": "planned_public_services",
                        "status": "מתוכנן ברמת רובע",
                        "source_url": municipal_url,
                        "source_note": "The municipal page lists public buildings including education, culture, leisure and neighborhood health services.",
                    },
                    {
                        "id": "commerce_employment",
                        "name": "מסחר ותעסוקה",
                        "type": "mixed_use",
                        "status": "מתוכנן",
                        "source_url": municipal_url,
                        "source_note": "The municipal page lists planned commerce and employment floorspace at district scale.",
                    },
                ],
            },
        ],
        "implementation_notes": [
            "Use `map_status: needs_precise_pin` to prevent fake clickable map pins.",
            "Promote only sourced, verified coordinates into Mapbox/Cesium pins.",
            "Render planned facilities with planned/future labels until built and verified.",
            "Keep this environment JSON separate from unit inventory and pricing.",
        ],
    }


def material_intake_payload() -> dict[str, object]:
    """Contractor/developer handoff map for replacing prototype material.

    The page can ship a prototype only because every future official replacement
    has a named field, accepted formats, and an honesty rule.
    """
    return {
        "project_slug": "rainbow-tel-aviv",
        "post_id": 4464,
        "version": 1,
        "purpose": "Developer handoff checklist for turning the prototype showroom into an official project showroom.",
        "current_public_state": "prototype_model_with_source_aware_demo_units",
        "url_rules": {
            "approved_https_only": True,
            "no_stock_interiors": True,
            "no_copied_developer_media_without_permission": True,
            "empty_slot_behavior": "Hide the control or show material pending; never render a broken button.",
            "cost_control": "Mapbox/Cesium/3D Tiles must stay lazy and user-opened.",
        },
        "official_materials": [
            {
                "id": "official_3d_model",
                "label": "Official BIM / optimized GLB",
                "cms_field": "project_model_glb",
                "accepted_formats": ["glb", "gltf", "ifc", "rvt", "fbx", "obj", "skp"],
                "current_status": "provided_prototype",
                "current_asset": f"{RAW_BASE}/model.glb",
                "public_policy": "Keep illustrative label until developer-approved model replaces the prototype.",
            },
            {
                "id": "model_poster",
                "label": "Official model poster / still frame",
                "cms_field": "project_model_poster",
                "accepted_formats": ["png", "jpg", "webp"],
                "current_status": "provided_prototype",
                "current_asset": f"{RAW_BASE}/poster.png",
                "public_policy": "Use as loading poster only; optimize before upload.",
            },
            {
                "id": "sales_video",
                "label": "Project sales video",
                "cms_field": "project_3d_video_url",
                "accepted_formats": ["youtube", "vimeo", "mp4_https"],
                "current_status": "pending_official",
                "current_asset": "",
                "public_policy": "Use only owner/developer-approved video. Do not scrape or copy embedded video.",
            },
            {
                "id": "virtual_tour",
                "label": "Interior or apartment virtual tour",
                "cms_field": "project_3d_tour_url",
                "accepted_formats": ["matterport", "kuula", "cloudpano", "custom_https"],
                "current_status": "pending_official",
                "current_asset": "",
                "public_policy": "Use only approved tours. Do not generate fake interiors for public unit claims.",
            },
            {
                "id": "photorealistic_city_view",
                "label": "Cesium / 3D Tiles city-view layer",
                "cms_field": "project_3d_cesium_tiles_url",
                "accepted_formats": ["3d_tiles_endpoint", "cesium_ion_asset", "google_p3dt_config"],
                "current_status": "pending_official",
                "current_asset": "",
                "public_policy": "Lazy-load only after user opens the view layer and cost governance is approved.",
            },
            {
                "id": "approved_drawings",
                "label": "Approved elevation, site plan and floor plans",
                "cms_field": "project_3d_drawings_json",
                "accepted_formats": ["pdf", "svg", "png", "jpg", "webp"],
                "current_status": "provided_prototype",
                "current_asset": "plans/*.svg",
                "public_policy": "Prototype drawings must keep illustrative labels until official sale plans arrive.",
            },
            {
                "id": "unit_inventory",
                "label": "Unit inventory and availability feed",
                "cms_field": "project_3d_units",
                "accepted_formats": ["json", "csv", "xlsx"],
                "current_status": "provided_prototype",
                "current_asset": "unit-map.json",
                "public_policy": "Do not show real prices or availability until source/license and owner approval are recorded.",
            },
            {
                "id": "unit_interiors",
                "label": "Per-unit interior media",
                "cms_field": "project_3d_units[].interior_url",
                "accepted_formats": ["image_gallery_https", "webp", "jpg", "png"],
                "current_status": "pending_official",
                "current_asset": "",
                "public_policy": "Leave empty unless the interior belongs to that unit/type and is approved for public use.",
            },
            {
                "id": "unit_tours",
                "label": "Per-unit tour links",
                "cms_field": "project_3d_units[].tour_url",
                "accepted_formats": ["matterport", "kuula", "cloudpano", "custom_https"],
                "current_status": "pending_official",
                "current_asset": "",
                "public_policy": "Leave empty unless the tour is official or owner-approved.",
            },
            {
                "id": "surroundings_and_pins",
                "label": "Nearby projects, parks, schools, transport and public services",
                "cms_field": "project_3d_environment_json",
                "accepted_formats": ["json", "csv", "geojson"],
                "current_status": "provided_prototype",
                "current_asset": "environment.json",
                "public_policy": "Use precise pins only when verified. Planned facilities need planned/future labels.",
            },
        ],
        "zillow_parity_map": {
            "building_spin": "project_model_glb + model hotspots",
            "unit_picker": "project_3d_units",
            "floor_plans": "project_3d_drawings_json and unit plan URLs",
            "video_and_tour": "project_3d_video_url, project_3d_tour_url, unit interior/tour URLs",
            "view_layer": "Mapbox now, Cesium/3D Tiles seam when approved",
            "surroundings": "project_3d_environment_json",
            "price_context": "project_3d_avg_price_per_sqm + project_3d_price_source_note or approved unit price",
            "lead_capture": "existing lead funnel with selected unit payload",
        },
        "owner_questions_before_official_launch": [
            "Which developer/project materials are approved for public use?",
            "Can project video/tour URLs be embedded publicly?",
            "Which unit rows are live inventory and which are examples?",
            "May approximate price context be shown, and from which source?",
            "Which surroundings pins have verified coordinates?",
        ],
    }


def bearing_for_direction(direction: str) -> int:
    """Approximate compass bearing for current Hebrew direction labels."""
    north = "צפון" in direction
    south = "דרום" in direction
    east = "מזרח" in direction
    west = "מערב" in direction
    if north and west:
        return 315
    if north and east:
        return 45
    if south and west:
        return 225
    if south and east:
        return 135
    if west:
        return 270
    if east:
        return 90
    if north:
        return 0
    if south:
        return 180
    return 270


def unit_view_records(units: list[dict[str, object]]) -> list[dict[str, object]]:
    records = []
    for unit in units:
        floor = float(unit.get("floor", 0) or 0)
        direction = str(unit.get("dir", ""))
        altitude = RAINBOW_GROUND_ELEVATION_M + 4.0 + max(0.0, floor - 1.0) * RAINBOW_FLOOR_HEIGHT_M + 1.55
        records.append(
            {
                "unit_id": unit.get("id"),
                "floor": unit.get("floor"),
                "direction": direction,
                "bearing_degrees": bearing_for_direction(direction),
                "altitude_m": round(altitude, 2),
                "camera_distance_m": 900,
                "camera_pitch_degrees": 65,
                "source_note": "Prototype camera params derived from unit floor/direction. Replace with survey/BIM view data when supplied.",
            }
        )
    return records


def view_layer_payload(units: list[dict[str, object]]) -> dict[str, object]:
    """Mapbox-now / Cesium-ready view-from-apartment contract."""
    return {
        "project_slug": "rainbow-tel-aviv",
        "post_id": 4464,
        "version": 1,
        "status": "mapbox_live_cesium_ready",
        "project_center": {
            "lat": RAINBOW_LAT,
            "lng": RAINBOW_LNG,
            "precision": "prototype",
            "source_note": "Approximate Sde Dov / Rainbow showroom center. Replace with verified survey pin before official launch.",
        },
        "cms_inputs": {
            "lat": RAINBOW_LAT,
            "lng": RAINBOW_LNG,
            "project_3d_units": "unit-map.json",
            "project_3d_environment_json": "environment.json",
            "project_3d_cesium_tiles_url": "",
        },
        "providers": {
            "mapbox": {
                "state": "current_live_provider",
                "load_policy": "user_open_only",
                "rtl_text_plugin_required": True,
                "camera_formula": "ground_elevation_m + 4.0 + (floor - 1) * floor_height_m + 1.55",
                "ground_elevation_m": RAINBOW_GROUND_ELEVATION_M,
                "floor_height_m": RAINBOW_FLOOR_HEIGHT_M,
                "camera_distance_m": 900,
                "pitch_degrees": 65,
                "bearing_source": "unit direction -> bearing_degrees",
            },
            "cesium": {
                "state": "ready_seam_pending_approved_tiles",
                "load_policy": "user_open_only",
                "tiles_url": "",
                "accepted_sources": ["Cesium ion asset", "Google Photorealistic 3D Tiles config", "approved 3D Tiles endpoint"],
                "public_policy": "Do not enable until token/cost governance and public-use rights are approved.",
            },
        },
        "cost_controls": {
            "instantiate_on_page_load": False,
            "lazy_on_user_gesture": True,
            "dedupe_per_session": True,
            "static_preview_fallback": True,
            "do_not_autoplay_tiles": True,
        },
        "unit_views": unit_view_records(units),
        "overlays": [
            {
                "id": "neighbor_projects",
                "source": "project_3d_environment_json",
                "render_policy": "Only show clickable pins for verified coordinates; otherwise show source-aware cards.",
            },
            {
                "id": "parks_and_coast",
                "source": "project_3d_environment_json",
                "render_policy": "Planned/future labels required until built and verified.",
            },
            {
                "id": "mobility",
                "source": "project_3d_environment_json",
                "render_policy": "Transport items must show current/planned status.",
            },
        ],
        "qa_requirements": [
            "Default page state remains building selector, not map/tiles.",
            "View layer opens only after buyer action.",
            "Hebrew map labels require RTL plugin before Mapbox init.",
            "Unit selection recomputes altitude and bearing from selected unit.",
            "Cesium/3D Tiles controls stay hidden or pending until an approved tiles URL exists.",
        ],
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    build_glb(OUT / "model.glb")
    write_png(OUT / "poster.png")
    units = unit_records()
    environment = environment_payload()
    write_json(OUT / "unit-map.json", units)
    write_json(
        OUT / "project-meta-example.json",
        {
            "project_model_glb": f"{RAW_BASE}/model.glb",
            "project_model_poster": f"{RAW_BASE}/poster.png",
            "project_model_usdz": "",
            "project_3d_video_url": "",
            "project_3d_tour_url": "",
            "project_3d_cesium_tiles_url": "",
            "project_3d_avg_price_per_sqm": RAINBOW_INDICATIVE_AVG_PRICE_PER_SQM,
            "project_3d_price_source_note": RAINBOW_PRICE_SOURCE_NOTE,
            "project_3d_units": units,
            "project_3d_drawings_json": [
                {
                    "label": "תרשים מיקום וסביבה",
                    "type": "site_orientation",
                    "url": f"{PLAN_BASE}/site-orientation.svg",
                    "source": "המחשה מקורית לא רשמית על בסיס מקורות פומביים",
                },
                {
                    "label": "תוכנית טיפוסית 4 חדרים",
                    "type": "floor_plan",
                    "url": f"{PLAN_BASE}/plan-4br.svg",
                    "source": "המחשה מקורית לא רשמית. להחלפה בתוכנית מכר רשמית",
                },
                {
                    "label": "תוכנית פנטהאוז",
                    "type": "floor_plan",
                    "url": f"{PLAN_BASE}/plan-penthouse.svg",
                    "source": "המחשה מקורית לא רשמית. להחלפה בתוכנית מכר רשמית",
                },
            ],
            "project_3d_environment_json": environment,
        },
    )
    write_json(
        OUT / "drawings.json",
        {
            "status": "prototype_schematic",
            "items": [
                {
                    "label": "תרשים מיקום וסביבה",
                    "type": "site_orientation",
                    "url": f"{PLAN_BASE}/site-orientation.svg",
                    "source": "המחשה מקורית לא רשמית על בסיס מקורות פומביים",
                },
                {
                    "label": "תוכנית 3 חדרים",
                    "type": "floor_plan",
                    "url": f"{PLAN_BASE}/plan-3br.svg",
                    "source": "המחשה מקורית לא רשמית. להחלפה בתוכנית מכר רשמית",
                },
                {
                    "label": "תוכנית 4 חדרים",
                    "type": "floor_plan",
                    "url": f"{PLAN_BASE}/plan-4br.svg",
                    "source": "המחשה מקורית לא רשמית. להחלפה בתוכנית מכר רשמית",
                },
                {
                    "label": "תוכנית 5 חדרים",
                    "type": "floor_plan",
                    "url": f"{PLAN_BASE}/plan-5br.svg",
                    "source": "המחשה מקורית לא רשמית. להחלפה בתוכנית מכר רשמית",
                },
                {
                    "label": "תוכנית פנטהאוז",
                    "type": "floor_plan",
                    "url": f"{PLAN_BASE}/plan-penthouse.svg",
                    "source": "המחשה מקורית לא רשמית. להחלפה בתוכנית מכר רשמית",
                },
                {
                    "label": "תוכנית בוטיק",
                    "type": "floor_plan",
                    "url": f"{PLAN_BASE}/plan-boutique.svg",
                    "source": "המחשה מקורית לא רשמית. להחלפה בתוכנית מכר רשמית",
                },
            ],
            "required_official_replacements": ["official_elevation", "typical_floor_plan", "site_plan", "unit_plan"],
            "note": "Attach only approved developer drawings or owner-licensed material before removing the illustrative labels.",
        },
    )
    write_json(OUT / "environment.json", environment)
    write_json(OUT / "material-intake-template.json", material_intake_payload())
    write_json(OUT / "view-layer-config.json", view_layer_payload(units))
    write_docs()
    size = os.path.getsize(OUT / "model.glb")
    print(f"Wrote {OUT / 'model.glb'} ({size:,} bytes)")
    print(f"Wrote {OUT / 'poster.png'} ({os.path.getsize(OUT / 'poster.png'):,} bytes)")


if __name__ == "__main__":
    main()
