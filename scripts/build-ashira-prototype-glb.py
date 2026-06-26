import json
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


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "assets" / "projects" / "ashira-sde-dov" / "model-prototype.glb"
    out.parent.mkdir(parents=True, exist_ok=True)

    # Unit cube centered at origin. Public showroom model uses scaled nodes.
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

    chunks = []
    offsets = {}
    for name, blob in (
        ("positions", pack_floats(positions)),
        ("normals", pack_floats(normals)),
        ("indices", pack_uint16(indices)),
    ):
        offsets[name] = sum(len(c) for c in chunks)
        chunks.append(pad4(blob, b"\x00"))
    bin_blob = b"".join(chunks)

    nodes = [
        {"name": "ashira_context_base", "mesh": 0, "translation": [0, -0.15, 0], "scale": [24, 0.3, 20]},
        {"name": "ashira_tower_main", "mesh": 0, "translation": [0, 14, 0], "scale": [5.2, 28, 4.2]},
        {"name": "ashira_balcony_band_west", "mesh": 0, "translation": [-3.05, 14, 0.05], "scale": [0.55, 27, 4.8]},
        {"name": "ashira_balcony_band_east", "mesh": 0, "translation": [3.05, 14, 0.05], "scale": [0.55, 27, 4.8]},
        {"name": "ashira_podium", "mesh": 0, "translation": [0, 2.25, 0], "scale": [11, 4.5, 8]},
        {"name": "ashira_low_rise_west", "mesh": 0, "translation": [-10, 4, -4], "scale": [5, 8, 5]},
        {"name": "ashira_low_rise_east", "mesh": 0, "translation": [10, 3.5, 5], "scale": [4.5, 7, 5]},
        {"name": "ashira_sea_plane", "mesh": 0, "translation": [-18, 0.01, -4], "scale": [9, 0.04, 22]},
        {"name": "ashira_sun_marker", "mesh": 0, "translation": [-16, 22, -10], "scale": [1.8, 1.8, 1.8]},
    ]

    gltf = {
        "asset": {"version": "2.0", "generator": "NadLan Ashira prototype builder"},
        "scene": 0,
        "scenes": [{"nodes": list(range(len(nodes)))}],
        "nodes": nodes,
        "meshes": [
            {
                "name": "prototype_cube_mesh",
                "primitives": [
                    {
                        "attributes": {"POSITION": 0, "NORMAL": 1},
                        "indices": 2,
                        "material": 0,
                    }
                ],
            }
        ],
        "materials": [
            {
                "name": "warm_tower_concept",
                "pbrMetallicRoughness": {
                    "baseColorFactor": [0.82, 0.72, 0.55, 1.0],
                    "metallicFactor": 0.05,
                    "roughnessFactor": 0.45,
                },
            }
        ],
        "buffers": [{"byteLength": len(bin_blob)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": offsets["positions"], "byteLength": len(pack_floats(positions)), "target": 34962},
            {"buffer": 0, "byteOffset": offsets["normals"], "byteLength": len(pack_floats(normals)), "target": 34962},
            {"buffer": 0, "byteOffset": offsets["indices"], "byteLength": len(pack_uint16(indices)), "target": 34963},
        ],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": 24, "type": "VEC3", "min": [-0.5, -0.5, -0.5], "max": [0.5, 0.5, 0.5]},
            {"bufferView": 1, "componentType": 5126, "count": 24, "type": "VEC3"},
            {"bufferView": 2, "componentType": 5123, "count": 36, "type": "SCALAR", "min": [0], "max": [23]},
        ],
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
