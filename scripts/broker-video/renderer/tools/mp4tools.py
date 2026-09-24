"""Pure-Python MP4 helpers (no installs): inspect a file, and turn Chrome's fragmented MediaRecorder MP4
into a regular progressive MP4 (ftyp + moov with full sample tables + mdat, moov first = "faststart").

Why: MediaRecorder writes fragmented MP4 (moof/mdat pairs, empty sample tables, duration unknown in the
header). Some players and apps show no duration or cannot seek such files. The remux copies the encoded
H.264 samples byte for byte, it never re-encodes.
"""
import struct

CONTAINERS = {b"moov", b"trak", b"mdia", b"minf", b"stbl", b"mvex", b"moof", b"traf", b"edts", b"dinf", b"udta"}


def iter_boxes(buf, start=0, end=None):
    end = len(buf) if end is None else end
    i = start
    while i + 8 <= end:
        size, typ = struct.unpack_from(">I4s", buf, i)
        hdr = 8
        if size == 1:
            size = struct.unpack_from(">Q", buf, i + 8)[0]; hdr = 16
        elif size == 0:
            size = end - i
        if size < hdr or i + size > end:
            break
        yield typ, i, size, hdr
        i += size


def find(buf, path, start=0, end=None):
    """First box along a path like [b'moov', b'trak', b'mdia']; returns (offset, size, hdr) or None."""
    s, e = start, end
    found = None
    for name in path:
        found = None
        for typ, off, size, hdr in iter_boxes(buf, s, e):
            if typ == name:
                found = (off, size, hdr); break
        if not found:
            return None
        s, e = found[0] + found[2], found[0] + found[1]
    return found


def box(typ, payload):
    return struct.pack(">I4s", 8 + len(payload), typ) + payload


def full_box(typ, version, flags, payload):
    return box(typ, struct.pack(">I", (version << 24) | flags) + payload)


def is_fragmented(path):
    with open(path, "rb") as f:
        buf = f.read()
    return any(t == b"moof" for t, *_ in iter_boxes(buf)) or find(buf, [b"moov", b"mvex"]) is not None


def _samples_from_fragments(buf):
    """Walk moof/mdat pairs (single video track). Returns list of fragments, each a list of samples
    (offset, size, duration, is_sync, cts_offset)."""
    trex = find(buf, [b"moov", b"mvex", b"trex"])
    d_dur = d_size = d_flags = 0
    if trex:
        o = trex[0] + trex[2]
        _, _tid, _sdi, d_dur, d_size, d_flags = struct.unpack_from(">IIIIII", buf, o)
    frags = []
    for typ, moof_off, moof_size, moof_hdr in iter_boxes(buf):
        if typ != b"moof":
            continue
        for ttyp, traf_off, traf_size, traf_hdr in iter_boxes(buf, moof_off + moof_hdr, moof_off + moof_size):
            if ttyp != b"traf":
                continue
            base = moof_off
            dur, size, flags = d_dur, d_size, d_flags
            samples = []
            for btyp, b_off, b_size, b_hdr in iter_boxes(buf, traf_off + traf_hdr, traf_off + traf_size):
                p = b_off + b_hdr
                if btyp == b"tfhd":
                    vf = struct.unpack_from(">I", buf, p)[0]; tf = vf & 0xFFFFFF; p += 8  # skip track_ID
                    if tf & 0x1: base = struct.unpack_from(">Q", buf, p)[0]; p += 8
                    if tf & 0x2: p += 4
                    if tf & 0x8: dur = struct.unpack_from(">I", buf, p)[0]; p += 4
                    if tf & 0x10: size = struct.unpack_from(">I", buf, p)[0]; p += 4
                    if tf & 0x20: flags = struct.unpack_from(">I", buf, p)[0]; p += 4
                elif btyp == b"trun":
                    vf = struct.unpack_from(">I", buf, p)[0]; version, tf = vf >> 24, vf & 0xFFFFFF; p += 4
                    count = struct.unpack_from(">I", buf, p)[0]; p += 4
                    data_off = 0
                    if tf & 0x1: data_off = struct.unpack_from(">i", buf, p)[0]; p += 4
                    first_flags = None
                    if tf & 0x4: first_flags = struct.unpack_from(">I", buf, p)[0]; p += 4
                    cur = base + data_off
                    for k in range(count):
                        s_dur, s_size, s_flags, s_cts = dur, size, flags, 0
                        if tf & 0x100: s_dur = struct.unpack_from(">I", buf, p)[0]; p += 4
                        if tf & 0x200: s_size = struct.unpack_from(">I", buf, p)[0]; p += 4
                        if tf & 0x400: s_flags = struct.unpack_from(">I", buf, p)[0]; p += 4
                        if tf & 0x800:
                            s_cts = struct.unpack_from(">i" if version else ">I", buf, p)[0]; p += 4
                        if k == 0 and first_flags is not None:
                            s_flags = first_flags
                        is_sync = not (s_flags & 0x10000)          # sample_is_non_sync_sample bit
                        samples.append((cur, s_size, s_dur, is_sync, s_cts))
                        cur += s_size
            if samples:
                frags.append(samples)
    return frags


def _rle(values):
    out = []
    for v in values:
        if out and out[-1][1] == v:
            out[-1][0] += 1
        else:
            out.append([1, v])
    return out


def _patch_duration(buf, off, hdr, kind, new_dur, new_timescale=None):
    """Return a copy of an mvhd/tkhd/mdhd box with its duration (and optionally timescale) replaced."""
    b = bytearray(buf[off:off + struct.unpack_from(">I", buf, off)[0]])
    version = b[hdr]
    p = hdr + 4
    if kind in (b"mvhd", b"mdhd"):
        p += 16 if version == 1 else 8          # creation + modification
        if new_timescale:
            struct.pack_into(">I", b, p, new_timescale)
        p += 4                                   # timescale
    else:  # tkhd
        p += 16 if version == 1 else 8
        p += 8                                   # track_ID + reserved
    if version == 1:
        struct.pack_into(">Q", b, p, new_dur)
    else:
        struct.pack_into(">I", b, p, min(new_dur, 0xFFFFFFFF))
    return bytes(b)


def _timescale(buf, off, hdr):
    version = buf[off + hdr]
    p = off + hdr + 4 + (16 if version == 1 else 8)
    return struct.unpack_from(">I", buf, p)[0]


def defragment(src, dst, cfr_fps=None):
    """Remux. With cfr_fps, every sample gets exactly 1/cfr_fps (use only when no frame was dropped)."""
    with open(src, "rb") as f:
        buf = f.read()
    ftyp = find(buf, [b"ftyp"])
    moov = find(buf, [b"moov"])
    mvhd = find(buf, [b"moov", b"mvhd"])
    trak = find(buf, [b"moov", b"trak"])
    tkhd = find(buf, [b"tkhd"], trak[0] + trak[2], trak[0] + trak[1])
    mdia = find(buf, [b"mdia"], trak[0] + trak[2], trak[0] + trak[1])
    mdhd = find(buf, [b"mdhd"], mdia[0] + mdia[2], mdia[0] + mdia[1])
    hdlr = find(buf, [b"hdlr"], mdia[0] + mdia[2], mdia[0] + mdia[1])
    minf = find(buf, [b"minf"], mdia[0] + mdia[2], mdia[0] + mdia[1])
    stbl = find(buf, [b"stbl"], minf[0] + minf[2], minf[0] + minf[1])
    stsd = find(buf, [b"stsd"], stbl[0] + stbl[2], stbl[0] + stbl[1])
    frags = _samples_from_fragments(buf)
    samples = [s for fr in frags for s in fr]
    if not samples:
        raise RuntimeError("no samples found")
    movie_ts = _timescale(buf, *mvhd[::2])
    track_ts = _timescale(buf, *mdhd[::2])
    new_track_ts = track_ts
    if cfr_fps:
        if track_ts % cfr_fps:
            new_track_ts = cfr_fps * 1000
        step = new_track_ts // cfr_fps
        samples = [(o, sz, step, sy, 0) for (o, sz, _d, sy, _c) in samples]
        frags = [[(o, sz, step, sy, 0) for (o, sz, _d, sy, _c) in fr] for fr in frags]
    track_ts = new_track_ts
    total = sum(s[2] for s in samples)
    movie_dur = total * movie_ts // track_ts

    runs = _rle([s[2] for s in samples])
    stts = full_box(b"stts", 0, 0, struct.pack(">I", len(runs)) + b"".join(struct.pack(">II", c, v) for c, v in runs))
    ctts = b""
    if any(s[4] for s in samples):
        cr = _rle([s[4] for s in samples])
        ctts = full_box(b"ctts", 0, 0, struct.pack(">I", len(cr)) + b"".join(struct.pack(">II", c, v & 0xFFFFFFFF) for c, v in cr))
    sync = [i + 1 for i, s in enumerate(samples) if s[3]]
    stss = b"" if len(sync) == len(samples) else full_box(b"stss", 0, 0, struct.pack(">I", len(sync)) + b"".join(struct.pack(">I", n) for n in sync))
    stsz = full_box(b"stsz", 0, 0, struct.pack(">II", 0, len(samples)) + b"".join(struct.pack(">I", s[1]) for s in samples))
    # one chunk per fragment
    per_chunk = [len(fr) for fr in frags]
    stsc_entries = []
    for idx, n in enumerate(per_chunk, start=1):
        if not stsc_entries or stsc_entries[-1][1] != n:
            stsc_entries.append((idx, n))
    stsc = full_box(b"stsc", 0, 0, struct.pack(">I", len(stsc_entries)) + b"".join(struct.pack(">III", a, n, 1) for a, n in stsc_entries))
    payload_size = sum(s[1] for s in samples)
    use64 = payload_size > 0xFFFFFFF0

    def build_moov(chunk_offsets):
        if use64:
            stco = full_box(b"co64", 0, 0, struct.pack(">I", len(chunk_offsets)) + b"".join(struct.pack(">Q", o) for o in chunk_offsets))
        else:
            stco = full_box(b"stco", 0, 0, struct.pack(">I", len(chunk_offsets)) + b"".join(struct.pack(">I", o) for o in chunk_offsets))
        new_stbl = box(b"stbl", buf[stsd[0]:stsd[0] + stsd[1]] + stts + ctts + stss + stsz + stsc + stco)
        minf_children = b""
        for typ, off, size, hdr in iter_boxes(buf, minf[0] + minf[2], minf[0] + minf[1]):
            minf_children += new_stbl if typ == b"stbl" else buf[off:off + size]
        new_minf = box(b"minf", minf_children)
        new_mdia = box(b"mdia", _patch_duration(buf, mdhd[0], mdhd[2], b"mdhd", total, track_ts) + buf[hdlr[0]:hdlr[0] + hdlr[1]] + new_minf)
        trak_children = _patch_duration(buf, tkhd[0], tkhd[2], b"tkhd", movie_dur)
        for typ, off, size, hdr in iter_boxes(buf, trak[0] + trak[2], trak[0] + trak[1]):
            if typ in (b"tkhd", b"mdia"):
                continue
            trak_children += buf[off:off + size]
        new_trak = box(b"trak", trak_children + new_mdia)
        return box(b"moov", _patch_duration(buf, mvhd[0], mvhd[2], b"mvhd", movie_dur) + new_trak)

    new_ftyp = box(b"ftyp", b"isom" + struct.pack(">I", 512) + b"isomiso2avc1mp41")
    rel, acc = [], 0
    for fr in frags:
        rel.append(acc); acc += sum(s[1] for s in fr)
    moov_probe = build_moov([0] * len(frags))
    mdat_hdr = struct.pack(">I4s", 1, b"mdat") + struct.pack(">Q", 16 + payload_size) if use64 else struct.pack(">I4s", 8 + payload_size, b"mdat")
    base = len(new_ftyp) + len(moov_probe) + len(mdat_hdr)
    new_moov = build_moov([base + r for r in rel])
    assert len(new_moov) == len(moov_probe)
    with open(dst, "wb") as f:
        f.write(new_ftyp); f.write(new_moov); f.write(mdat_hdr)
        for s in samples:
            f.write(buf[s[0]:s[0] + s[1]])
    return {"samples": len(samples), "fragments": len(frags), "duration_s": total / track_ts, "cfr": bool(cfr_fps)}


def count_samples(path):
    with open(path, "rb") as f:
        buf = f.read()
    return sum(len(fr) for fr in _samples_from_fragments(buf))


def describe(path):
    with open(path, "rb") as f:
        buf = f.read()
    out = {"file": path, "bytes": len(buf), "top": [t.decode("latin1") for t, *_ in iter_boxes(buf)]}
    mvhd = find(buf, [b"moov", b"mvhd"])
    if mvhd:
        v = buf[mvhd[0] + mvhd[2]]
        p = mvhd[0] + mvhd[2] + 4 + (16 if v else 8)
        ts = struct.unpack_from(">I", buf, p)[0]
        d = struct.unpack_from(">Q" if v else ">I", buf, p + 4)[0]
        out["movie_timescale"], out["movie_duration_s"] = ts, round(d / ts, 3) if ts else None
    stsd = find(buf, [b"moov", b"trak", b"mdia", b"minf", b"stbl", b"stsd"])
    if stsd:
        e = stsd[0] + stsd[2] + 8
        size, typ = struct.unpack_from(">I4s", buf, e)
        out["codec"] = typ.decode("latin1")
        w, h = struct.unpack_from(">HH", buf, e + 8 + 24)
        out["coded_size"] = f"{w}x{h}"
        avcc = find(buf, [b"avcC"], e + 8 + 78, e + size)
        if avcc:
            prof, compat, level = buf[avcc[0] + avcc[2] + 1], buf[avcc[0] + avcc[2] + 2], buf[avcc[0] + avcc[2] + 3]
            names = {66: "Baseline", 77: "Main", 88: "Extended", 100: "High"}
            out["h264_profile"] = names.get(prof, str(prof)) + (" (constrained)" if prof == 66 and compat & 0x40 else "")
            out["h264_level"] = level / 10
    mdhd = find(buf, [b"moov", b"trak", b"mdia", b"mdhd"])
    track_ts = _timescale(buf, mdhd[0], mdhd[2]) if mdhd else None
    if any(t == b"moof" for t, *_ in iter_boxes(buf)):
        samples = [s for fr in _samples_from_fragments(buf) for s in fr]
        out["layout"] = "fragmented"
    else:
        samples = []
        stts = find(buf, [b"moov", b"trak", b"mdia", b"minf", b"stbl", b"stts"])
        if stts:
            p = stts[0] + stts[2] + 4
            n = struct.unpack_from(">I", buf, p)[0]
            for k in range(n):
                c, dlt = struct.unpack_from(">II", buf, p + 4 + 8 * k)
                samples += [(0, 0, dlt, True, 0)] * c
        stss = find(buf, [b"moov", b"trak", b"mdia", b"minf", b"stbl", b"stss"])
        out["layout"] = "progressive"
        if stss:
            out["keyframes"] = struct.unpack_from(">I", buf, stss[0] + stss[2] + 4)[0]
    if samples and track_ts:
        durs = [s[2] for s in samples]
        total = sum(durs)
        out["frames"] = len(samples)
        out["duration_s"] = round(total / track_ts, 3)
        out["avg_fps"] = round(len(samples) / (total / track_ts), 3)
        out["frame_ms_min_max"] = [round(min(durs) / track_ts * 1000, 2), round(max(durs) / track_ts * 1000, 2)]
        long_ = sum(1 for d in durs if d / track_ts > 1.5 / 30)
        out["frames_longer_than_1.5x_33ms"] = long_
    return out


if __name__ == "__main__":
    import json, sys
    print(json.dumps(describe(sys.argv[1]), indent=1))
