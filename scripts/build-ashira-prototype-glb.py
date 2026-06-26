import json
import math
import struct
from pathlib import Path


def pad4(data: bytes, pad: bytes = b" ") -> bytes:
    while len(data) % 4:
        data += pad
    return data


def pack_floats(values):
    return struct.pack("<" + "f" * len(values), *values)


def pack_uint16(values):
    return struct.pack("<" + "H" * len(values), *values)


def unit_box():
    positions = [
        -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5, -0.5, 0.5, 0.5,
        0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5,
        -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5, -0.5,
        0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5,
        -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, 0.5, -0.5,
        -0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5, -0.5, -0.5, 0.5,
    ]
    normals = [
        0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,
        0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1,
        -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0,
        1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0,
        0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
        0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0,
    ]
    indices = [
        0, 1, 2, 0, 2, 3,
        4, 5, 6, 4, 6, 7,
        8, 9, 10, 8, 10, 11,
        12, 13, 14, 12, 14, 15,
        16, 17, 18, 16, 18, 19,
        20, 21, 22, 20, 22, 23,
    ]
    return positions, normals, indices


def unit_cylinder(segments=36):
    positions = []
    normals = []
    indices = []

    def add_vertex(x, y, z, nx, ny, nz):
        positions.extend([x, y, z])
        normals.extend([nx, ny, nz])
        return len(positions) // 3 - 1

    for i in range(segments):
        a0 = 2 * math.pi * i / segments
        a1 = 2 * math.pi * (i + 1) / segments
        x0, z0 = math.cos(a0) * 0.5, math.sin(a0) * 0.5
        x1, z1 = math.cos(a1) * 0.5, math.sin(a1) * 0.5
        v0 = add_vertex(x0, -0.5, z0, math.cos(a0), 0, math.sin(a0))
        v1 = add_vertex(x1, -0.5, z1, math.cos(a1), 0, math.sin(a1))
        v2 = add_vertex(x1, 0.5, z1, math.cos(a1), 0, math.sin(a1))
        v3 = add_vertex(x0, 0.5, z0, math.cos(a0), 0, math.sin(a0))
        indices.extend([v0, v1, v2, v0, v2, v3])

        top = add_vertex(0, 0.5, 0, 0, 1, 0)
        t0 = add_vertex(x0, 0.5, z0, 0, 1, 0)
        t1 = add_vertex(x1, 0.5, z1, 0, 1, 0)
        indices.extend([top, t0, t1])

        bottom = add_vertex(0, -0.5, 0, 0, -1, 0)
        b0 = add_vertex(x0, -0.5, z0, 0, -1, 0)
        b1 = add_vertex(x1, -0.5, z1, 0, -1, 0)
        indices.extend([bottom, b1, b0])

    return positions, normals, indices


def unit_uv_sphere(segments=24, rings=12):
    positions = []
    normals = []
    indices = []
    for ring in range(rings + 1):
        phi = math.pi * ring / rings
        y = math.cos(phi) * 0.5
        r = math.sin(phi) * 0.5
        for seg in range(segments):
            theta = 2 * math.pi * seg / segments
            x = math.cos(theta) * r
            z = math.sin(theta) * r
            length = math.sqrt(x * x + y * y + z * z) or 1
            positions.extend([x, y, z])
            normals.extend([x / length, y / length, z / length])

    for ring in range(rings):
        for seg in range(segments):
            a = ring * segments + seg
            b = ring * segments + (seg + 1) % segments
            c = (ring + 1) * segments + (seg + 1) % segments
            d = (ring + 1) * segments + seg
            indices.extend([a, b, c, a, c, d])
    return positions, normals, indices


class GlbBuilder:
    def __init__(self):
        self.bin_chunks = []
        self.buffer_views = []
        self.accessors = []
        self.meshes = []
        self.nodes = []

    def add_accessor(self, blob, component_type, count, accessor_type, target, min_value=None, max_value=None):
        offset = sum(len(chunk) for chunk in self.bin_chunks)
        self.bin_chunks.append(pad4(blob, b"\x00"))
        view_index = len(self.buffer_views)
        self.buffer_views.append({"buffer": 0, "byteOffset": offset, "byteLength": len(blob), "target": target})
        accessor = {
            "bufferView": view_index,
            "componentType": component_type,
            "count": count,
            "type": accessor_type,
        }
        if min_value is not None:
            accessor["min"] = min_value
        if max_value is not None:
            accessor["max"] = max_value
        self.accessors.append(accessor)
        return len(self.accessors) - 1

    def add_mesh(self, name, positions, normals, indices, material):
        coords = list(zip(*(iter(positions),) * 3))
        min_value = [min(axis) for axis in zip(*coords)]
        max_value = [max(axis) for axis in zip(*coords)]
        position_accessor = self.add_accessor(
            pack_floats(positions), 5126, len(positions) // 3, "VEC3", 34962, min_value, max_value
        )
        normal_accessor = self.add_accessor(pack_floats(normals), 5126, len(normals) // 3, "VEC3", 34962)
        index_accessor = self.add_accessor(pack_uint16(indices), 5123, len(indices), "SCALAR", 34963, [0], [max(indices)])
        self.meshes.append(
            {
                "name": name,
                "primitives": [
                    {
                        "attributes": {"POSITION": position_accessor, "NORMAL": normal_accessor},
                        "indices": index_accessor,
                        "material": material,
                    }
                ],
            }
        )
        return len(self.meshes) - 1

    def add_node(self, name, mesh, translation, scale=None, rotation=None):
        node = {"name": name, "mesh": mesh, "translation": translation}
        if scale is not None:
            node["scale"] = scale
        if rotation is not None:
            node["rotation"] = rotation
        self.nodes.append(node)


def quat_y(degrees):
    radians = math.radians(degrees)
    return [0, math.sin(radians / 2), 0, math.cos(radians / 2)]


def material(name, color, metallic=0.02, roughness=0.58, alpha_mode=None, double_sided=False, emissive=None):
    mat = {
        "name": name,
        "pbrMetallicRoughness": {
            "baseColorFactor": color,
            "metallicFactor": metallic,
            "roughnessFactor": roughness,
        },
    }
    if alpha_mode:
        mat["alphaMode"] = alpha_mode
    if double_sided:
        mat["doubleSided"] = True
    if emissive:
        mat["emissiveFactor"] = emissive
    return mat


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "assets" / "projects" / "ashira-sde-dov" / "model-prototype.glb"
    out.parent.mkdir(parents=True, exist_ok=True)

    materials = [
        material("sde_dov_land_plot", [0.58, 0.63, 0.48, 1.0], roughness=0.72),
        material("tel_aviv_sea_west", [0.08, 0.42, 0.55, 0.72], roughness=0.3, alpha_mode="BLEND", double_sided=True),
        material("ashira_champagne_glass", [0.82, 0.77, 0.63, 0.86], metallic=0.04, roughness=0.36, alpha_mode="BLEND"),
        material("ashira_warm_frame", [0.94, 0.79, 0.46, 1.0], metallic=0.08, roughness=0.44),
        material("ashira_balcony_slab", [0.9, 0.86, 0.74, 1.0], roughness=0.55),
        material("ashira_podium_stone", [0.69, 0.62, 0.49, 1.0], roughness=0.68),
        material("neighbor_massing_soft_white", [0.78, 0.82, 0.8, 0.62], roughness=0.65, alpha_mode="BLEND"),
        material("promenade_and_roads", [0.22, 0.27, 0.27, 1.0], roughness=0.75),
        material("reading_stack_reference", [0.72, 0.63, 0.52, 1.0], roughness=0.6),
        material("golden_sun_orientation", [1.0, 0.78, 0.24, 1.0], metallic=0.0, roughness=0.25, emissive=[0.95, 0.58, 0.08]),
        material("window_shadow_lines", [0.08, 0.21, 0.22, 0.9], roughness=0.36, alpha_mode="BLEND"),
    ]

    builder = GlbBuilder()
    box_pos, box_norm, box_idx = unit_box()
    cyl_pos, cyl_norm, cyl_idx = unit_cylinder(48)
    sun_pos, sun_norm, sun_idx = unit_uv_sphere(28, 14)

    cube_meshes = [
        builder.add_mesh(f"box_{mat['name']}", box_pos, box_norm, box_idx, index)
        for index, mat in enumerate(materials)
    ]
    tower_mesh = builder.add_mesh("rounded_ashira_tower_shell", cyl_pos, cyl_norm, cyl_idx, 2)
    chimney_mesh = builder.add_mesh("reading_power_station_chimney_reference", cyl_pos, cyl_norm, cyl_idx, 8)
    sun_mesh = builder.add_mesh("sun_angle_sphere", sun_pos, sun_norm, sun_idx, 9)

    # Coordinate convention for the prototype: west/sea is negative X, north is positive Z.
    builder.add_node("sde_dov_land_platform", cube_meshes[0], [0, -0.16, 0], [28, 0.28, 22])
    builder.add_node("west_coast_sea_plane", cube_meshes[1], [-20, -0.08, 0], [12, 0.06, 25])
    builder.add_node("coastline_promenade_strip", cube_meshes[7], [-11.9, 0.05, 0], [0.55, 0.08, 24])
    builder.add_node("future_sde_dov_street_grid_east_west", cube_meshes[7], [2.2, 0.06, -6.8], [20, 0.05, 0.42])
    builder.add_node("future_sde_dov_street_grid_north_south", cube_meshes[7], [7.5, 0.07, 0], [0.42, 0.05, 19])

    builder.add_node("ashira_main_34_floor_tower", tower_mesh, [0, 17.2, 0], [5.4, 34.4, 3.8])
    builder.add_node("ashira_core_shadow_reveal", cube_meshes[10], [0, 17.6, 2.02], [4.6, 31.4, 0.12])
    builder.add_node("ashira_roof_crown", cube_meshes[3], [0, 34.85, 0], [6.25, 0.45, 4.55])
    builder.add_node("ashira_ground_lobby", cube_meshes[5], [0, 1.8, 0.2], [8.2, 3.6, 5.9])

    for floor in range(3, 35):
        y = floor * 0.94 + 1.2
        width = 5.85 + math.sin(floor * 0.65) * 0.28
        depth = 4.25 + math.cos(floor * 0.45) * 0.18
        builder.add_node(f"ashira_floor_plate_{floor:02d}", cube_meshes[4], [0, y, 0], [width, 0.065, depth])
        if floor % 2 == 0:
            builder.add_node(f"ashira_west_window_band_{floor:02d}", cube_meshes[10], [-2.74, y + 0.18, 0], [0.08, 0.42, 3.35])
            builder.add_node(f"ashira_sea_facing_balcony_{floor:02d}", cube_meshes[3], [-3.05, y + 0.05, 0], [0.22, 0.11, 3.9])
        if floor % 3 == 0:
            builder.add_node(f"ashira_city_facing_balcony_{floor:02d}", cube_meshes[3], [3.02, y + 0.05, 0], [0.18, 0.1, 3.35])

    # Boutique buildings around the tower, matching the public 7/8/15-storey project structure.
    boutique_specs = [
        ("north_boutique_15_storey", 15, -6.8, 7.0, 0),
        ("east_boutique_8_storey", 8, 7.2, 4.2, 8),
        ("south_boutique_7_storey", 7, 5.5, -7.2, -6),
    ]
    for name, floors, x, z, rotation in boutique_specs:
        height = floors * 0.95
        builder.add_node(name, cube_meshes[5], [x, height / 2, z], [5.8, height, 3.7], quat_y(rotation))
        for floor in range(2, floors + 1):
            builder.add_node(f"{name}_floor_line_{floor:02d}", cube_meshes[3], [x, floor * 0.95, z + 1.9], [5.95, 0.055, 0.08], quat_y(rotation))

    # Nearby context is low-emphasis: it orients the buyer but does not pretend survey accuracy.
    context_blocks = [
        ("rainbow_reference_massing", -5.8, -8.7, 12.5, 4.2, 12.0, 3.2),
        ("dimri_yama_reference_massing", 9.6, -8.2, 9.0, 3.8, 8.6, 3.0),
        ("gindi_vogue_reference_massing", 11.0, 8.7, 11.0, 4.2, 10.6, 3.2),
        ("future_sde_dov_massing_north", -2.7, 10.2, 8.0, 4.0, 7.4, 3.0),
    ]
    for name, x, z, height, sx, sy, sz in context_blocks:
        builder.add_node(name, cube_meshes[6], [x, height / 2, z], [sx, sy, sz])

    builder.add_node("reading_power_station_landmark_south", chimney_mesh, [-15.2, 5.5, -10.2], [1.15, 11.0, 1.15])
    builder.add_node("reading_power_station_base", cube_meshes[8], [-15.2, 0.5, -10.2], [3.0, 1.0, 2.0])
    builder.add_node("golden_sun_over_west_sea", sun_mesh, [-14.5, 23.5, -8.5], [2.2, 2.2, 2.2])

    bin_blob = b"".join(builder.bin_chunks)
    gltf = {
        "asset": {"version": "2.0", "generator": "NadLan Ashira prototype builder 2.0 product-view"},
        "scene": 0,
        "scenes": [{"nodes": list(range(len(builder.nodes)))}],
        "nodes": builder.nodes,
        "meshes": builder.meshes,
        "materials": materials,
        "buffers": [{"byteLength": len(bin_blob)}],
        "bufferViews": builder.buffer_views,
        "accessors": builder.accessors,
    }

    json_blob = pad4(json.dumps(gltf, separators=(",", ":")).encode("utf-8"))
    bin_blob = pad4(bin_blob, b"\x00")
    total_len = 12 + 8 + len(json_blob) + 8 + len(bin_blob)
    glb = [
        struct.pack("<III", 0x46546C67, 2, total_len),
        struct.pack("<I4s", len(json_blob), b"JSON"),
        json_blob,
        struct.pack("<I4s", len(bin_blob), b"BIN\x00"),
        bin_blob,
    ]
    out.write_bytes(b"".join(glb))
    print(out)


if __name__ == "__main__":
    main()
