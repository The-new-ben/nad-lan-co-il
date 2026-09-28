"""MP4 with several tracks (the narrated cut: H.264 video + AAC audio from Chrome's MediaRecorder).

  defragment_multi(src, dst, video_cfr_fps)  fragmented -> progressive MP4 (moov first), samples copied byte for byte
                                             in their original interleave; video optionally stamped at exactly 1/fps
  count_samples_multi(path)                  {'vide': n, 'soun': n}
  describe_multi(path)                       every track: handler, codec, timescale, samples, duration, start offset,
                                             video size / fps, audio channels / sample rate

Pure Python, no installs, no re-encode. Builds on mp4tools.py (the single-track helpers, copied from broker-video).
"""
import struct

from mp4tools import iter_boxes, find, box, full_box, _rle, _patch_duration, _timescale


def _u32(buf, o):
    return struct.unpack_from(">I", buf, o)[0]


def _tracks(buf):
    moov = find(buf, [b"moov"])
    tracks = {}
    for typ, off, size, hdr in iter_boxes(buf, moov[0] + moov[2], moov[0] + moov[1]):
        if typ != b"trak":
            continue
        tkhd = find(buf, [b"tkhd"], off + hdr, off + size)
        v = buf[tkhd[0] + tkhd[2]]
        tid = _u32(buf, tkhd[0] + tkhd[2] + 4 + (16 if v == 1 else 8))
        mdia = find(buf, [b"mdia"], off + hdr, off + size)
        mdhd = find(buf, [b"mdhd"], mdia[0] + mdia[2], mdia[0] + mdia[1])
        hdlr = find(buf, [b"hdlr"], mdia[0] + mdia[2], mdia[0] + mdia[1])
        minf = find(buf, [b"minf"], mdia[0] + mdia[2], mdia[0] + mdia[1])
        stbl = find(buf, [b"stbl"], minf[0] + minf[2], minf[0] + minf[1])
        stsd = find(buf, [b"stsd"], stbl[0] + stbl[2], stbl[0] + stbl[1])
        handler = buf[hdlr[0] + hdlr[2] + 8: hdlr[0] + hdlr[2] + 12].decode("latin1")
        tracks[tid] = {"id": tid, "handler": handler, "timescale": _timescale(buf, mdhd[0], mdhd[2]), "trak": (off, size, hdr),
                       "tkhd": tkhd, "mdhd": mdhd, "hdlr": hdlr, "minf": minf, "stbl": stbl, "stsd": stsd,
                       "trex": (0, 0, 0), "chunks": [], "start": None}
    mvex = find(buf, [b"moov", b"mvex"])
    if mvex:
        for typ, off, size, hdr in iter_boxes(buf, mvex[0] + mvex[2], mvex[0] + mvex[1]):
            if typ == b"trex":
                _, tid, _sdi, d_dur, d_size, d_flags = struct.unpack_from(">IIIIII", buf, off + hdr)
                if tid in tracks:
                    tracks[tid]["trex"] = (d_dur, d_size, d_flags)
    return tracks


def _fragments(buf, tracks):
    """Each traf's samples are one chunk of its track; returns the chunks' file order. Records each track's first tfdt."""
    order = []
    for typ, moof_off, moof_size, moof_hdr in iter_boxes(buf):
        if typ != b"moof":
            continue
        for ttyp, traf_off, traf_size, traf_hdr in iter_boxes(buf, moof_off + moof_hdr, moof_off + moof_size):
            if ttyp != b"traf":
                continue
            base, tid, samples = moof_off, None, []
            dur = size = flags = 0
            for btyp, b_off, b_size, b_hdr in iter_boxes(buf, traf_off + traf_hdr, traf_off + traf_size):
                p = b_off + b_hdr
                if btyp == b"tfhd":
                    tf = _u32(buf, p) & 0xFFFFFF; tid = _u32(buf, p + 4); p += 8
                    dur, size, flags = tracks[tid]["trex"]
                    if tf & 0x1: base = struct.unpack_from(">Q", buf, p)[0]; p += 8
                    if tf & 0x2: p += 4
                    if tf & 0x8: dur = _u32(buf, p); p += 4
                    if tf & 0x10: size = _u32(buf, p); p += 4
                    if tf & 0x20: flags = _u32(buf, p); p += 4
                elif btyp == b"tfdt":
                    t0 = struct.unpack_from(">Q", buf, p + 4)[0] if buf[p] == 1 else _u32(buf, p + 4)
                    if tracks[tid]["start"] is None:
                        tracks[tid]["start"] = t0
                elif btyp == b"trun":
                    vf = _u32(buf, p); version, tf = vf >> 24, vf & 0xFFFFFF; p += 4
                    count = _u32(buf, p); p += 4
                    data_off = 0
                    if tf & 0x1: data_off = struct.unpack_from(">i", buf, p)[0]; p += 4
                    first_flags = None
                    if tf & 0x4: first_flags = _u32(buf, p); p += 4
                    cur = base + data_off
                    for k in range(count):
                        s_dur, s_size, s_flags, s_cts = dur, size, flags, 0
                        if tf & 0x100: s_dur = _u32(buf, p); p += 4
                        if tf & 0x200: s_size = _u32(buf, p); p += 4
                        if tf & 0x400: s_flags = _u32(buf, p); p += 4
                        if tf & 0x800: s_cts = struct.unpack_from(">i" if version else ">I", buf, p)[0]; p += 4
                        if k == 0 and first_flags is not None:
                            s_flags = first_flags
                        samples.append((cur, s_size, s_dur, not (s_flags & 0x10000), s_cts))
                        cur += s_size
            if tid is not None and samples:
                tracks[tid]["chunks"].append(samples)
                order.append((tid, len(tracks[tid]["chunks"]) - 1))
    return order


def count_samples_multi(path):
    with open(path, "rb") as f:
        buf = f.read()
    tr = _tracks(buf)
    _fragments(buf, tr)
    return {t["handler"]: sum(len(c) for c in t["chunks"]) for t in tr.values()}


def starts_multi(path):
    """First tfdt of each track in seconds (fragmented files): the recorder's own A/V offset."""
    with open(path, "rb") as f:
        buf = f.read()
    tr = _tracks(buf)
    _fragments(buf, tr)
    return {t["handler"]: round((t["start"] or 0) / t["timescale"], 4) for t in tr.values()}


def defragment_multi(src, dst, video_cfr_fps=None, trim_to_video=True):
    with open(src, "rb") as f:
        buf = f.read()
    tracks = _tracks(buf)
    order = _fragments(buf, tracks)
    mvhd = find(buf, [b"moov", b"mvhd"])
    movie_ts = _timescale(buf, mvhd[0], mvhd[2])
    info = {}
    for t in tracks.values():
        ts = t["timescale"]
        start = t["start"] or 0
        if t["handler"] == "vide" and video_cfr_fps:
            ts_out = ts if ts % video_cfr_fps == 0 else video_cfr_fps * 1000
            step = ts_out // video_cfr_fps
            t["chunks"] = [[(o, sz, step, sy, c) for (o, sz, _d, sy, c) in ch] for ch in t["chunks"]]
            start = start * ts_out // ts
        else:
            ts_out = ts
        t["ts_out"] = ts_out
        t["samples"] = [s for ch in t["chunks"] for s in ch]
        t["total"] = sum(s[2] for s in t["samples"])
        t["movie_dur"] = t["total"] * movie_ts // ts_out
        t["movie_start"] = start * movie_ts // ts_out
        info[t["handler"]] = {"samples": len(t["samples"]), "chunks": len(t["chunks"]),
                              "duration_s": round(t["total"] / ts_out, 3), "start_s": round(start / ts_out, 4)}
    # the recorder keeps the sound running while it flushes the last video frames: end the sound with the picture
    vid = next((t for t in tracks.values() if t["handler"] == "vide"), None)
    if vid and trim_to_video:
        vend = (vid["movie_start"] + vid["movie_dur"]) / movie_ts
        for t in tracks.values():
            if t is vid:
                continue
            ts_out, acc, keep = t["ts_out"], t["movie_start"] / movie_ts, []
            for ch in t["chunks"]:
                kept = []
                for smp in ch:
                    if acc < vend - 1e-6:
                        kept.append(smp)
                    acc += smp[2] / ts_out
                if kept:
                    keep.append(kept)
            dropped = len(t["samples"]) - sum(len(c) for c in keep)
            t["chunks"] = keep
            t["samples"] = [s for ch in keep for s in ch]
            t["total"] = sum(s[2] for s in t["samples"])
            t["movie_dur"] = t["total"] * movie_ts // ts_out
            info[t["handler"]]["trimmed_samples"] = dropped
            info[t["handler"]]["duration_s"] = round(t["total"] / ts_out, 3)
        # the file order must only list chunks that still exist
        order = [(tid, ci) for tid, ci in order if ci < len(tracks[tid]["chunks"])]
    # if every track starts late by the same amount there is nothing to keep: shift all to 0
    common = min(t["movie_start"] for t in tracks.values())
    for t in tracks.values():
        t["movie_start"] -= common
    payload = sum(s[1] for t in tracks.values() for s in t["samples"])
    use64 = payload > 0xFFFFFFF0

    def stbl_for(t, offsets):
        smp = t["samples"]
        runs = _rle([s[2] for s in smp])
        stts = full_box(b"stts", 0, 0, struct.pack(">I", len(runs)) + b"".join(struct.pack(">II", c, v) for c, v in runs))
        ctts = b""
        if any(s[4] for s in smp):
            cr = _rle([s[4] for s in smp])
            ctts = full_box(b"ctts", 0, 0, struct.pack(">I", len(cr)) + b"".join(struct.pack(">II", c, v & 0xFFFFFFFF) for c, v in cr))
        sync = [i + 1 for i, s in enumerate(smp) if s[3]]
        stss = b"" if len(sync) == len(smp) else full_box(b"stss", 0, 0, struct.pack(">I", len(sync)) + b"".join(struct.pack(">I", n) for n in sync))
        stsz = full_box(b"stsz", 0, 0, struct.pack(">II", 0, len(smp)) + b"".join(struct.pack(">I", s[1]) for s in smp))
        ent = []
        for idx, ch in enumerate(t["chunks"], start=1):
            if not ent or ent[-1][1] != len(ch):
                ent.append((idx, len(ch)))
        stsc = full_box(b"stsc", 0, 0, struct.pack(">I", len(ent)) + b"".join(struct.pack(">III", a, n, 1) for a, n in ent))
        if use64:
            stco = full_box(b"co64", 0, 0, struct.pack(">I", len(offsets)) + b"".join(struct.pack(">Q", o) for o in offsets))
        else:
            stco = full_box(b"stco", 0, 0, struct.pack(">I", len(offsets)) + b"".join(struct.pack(">I", o) for o in offsets))
        sd = t["stsd"]
        return box(b"stbl", buf[sd[0]:sd[0] + sd[1]] + stts + ctts + stss + stsz + stsc + stco)

    def trak_for(t, offsets):
        minf = t["minf"]
        mch = b""
        for typ, off, size, hdr in iter_boxes(buf, minf[0] + minf[2], minf[0] + minf[1]):
            mch += stbl_for(t, offsets) if typ == b"stbl" else buf[off:off + size]
        mdhd = _patch_duration(buf, t["mdhd"][0], t["mdhd"][2], b"mdhd", t["total"], t["ts_out"])
        hd = t["hdlr"]
        new_mdia = box(b"mdia", mdhd + buf[hd[0]:hd[0] + hd[1]] + box(b"minf", mch))
        tk = t["tkhd"]
        tkhd = _patch_duration(buf, tk[0], tk[2], b"tkhd", t["movie_start"] + t["movie_dur"])
        edts = b""
        if t["movie_start"] > 0:   # an empty edit keeps a track's later start (A/V sync)
            edts = box(b"edts", full_box(b"elst", 0, 0, struct.pack(">I", 2) + struct.pack(">IiHH", t["movie_start"], -1, 1, 0)
                                          + struct.pack(">IiHH", t["movie_dur"], 0, 1, 0)))
        off, size, hdr = t["trak"]
        rest = b"".join(buf[o2:o2 + s2] for typ, o2, s2, h2 in iter_boxes(buf, off + hdr, off + size)
                        if typ not in (b"tkhd", b"mdia", b"edts"))
        return box(b"trak", tkhd + edts + rest + new_mdia)

    def build_moov(chunk_offsets):
        movie_dur = max(t["movie_start"] + t["movie_dur"] for t in tracks.values())
        body = _patch_duration(buf, mvhd[0], mvhd[2], b"mvhd", movie_dur)
        for tid in sorted(tracks):
            body += trak_for(tracks[tid], chunk_offsets[tid])
        return box(b"moov", body)

    rel = {tid: [0] * len(t["chunks"]) for tid, t in tracks.items()}
    acc = 0
    for tid, ci in order:
        rel[tid][ci] = acc
        acc += sum(s[1] for s in tracks[tid]["chunks"][ci])
    new_ftyp = box(b"ftyp", b"isom" + struct.pack(">I", 512) + b"isomiso2avc1mp41")
    probe = build_moov({tid: [0] * len(t["chunks"]) for tid, t in tracks.items()})
    mdat_hdr = (struct.pack(">I4s", 1, b"mdat") + struct.pack(">Q", 16 + payload)) if use64 else struct.pack(">I4s", 8 + payload, b"mdat")
    base = len(new_ftyp) + len(probe) + len(mdat_hdr)
    new_moov = build_moov({tid: [base + r for r in rel[tid]] for tid in tracks})
    assert len(new_moov) == len(probe)
    with open(dst, "wb") as f:
        f.write(new_ftyp); f.write(new_moov); f.write(mdat_hdr)
        for tid, ci in order:
            for s in tracks[tid]["chunks"][ci]:
                f.write(buf[s[0]:s[0] + s[1]])
    info["movie_duration_s"] = round(max(t["movie_start"] + t["movie_dur"] for t in tracks.values()) / movie_ts, 3)
    info["edit_offsets_s"] = {t["handler"]: round(t["movie_start"] / movie_ts, 4) for t in tracks.values()}
    info["cfr"] = bool(video_cfr_fps)
    return info


def describe_multi(path):
    with open(path, "rb") as f:
        buf = f.read()
    out = {"file": path, "bytes": len(buf), "top": [t.decode("latin1") for t, *_ in iter_boxes(buf)]}
    mvhd = find(buf, [b"moov", b"mvhd"])
    movie_ts = _timescale(buf, mvhd[0], mvhd[2])
    v = buf[mvhd[0] + mvhd[2]]
    d = struct.unpack_from(">Q" if v else ">I", buf, mvhd[0] + mvhd[2] + 4 + (16 if v else 8) + 4)[0]
    out["movie_duration_s"] = round(d / movie_ts, 3)
    tracks = _tracks(buf)
    fragmented = any(t == b"moof" for t, *_ in iter_boxes(buf))
    if fragmented:
        _fragments(buf, tracks)
    out["layout"] = "fragmented" if fragmented else "progressive"
    out["tracks"] = []
    for tid in sorted(tracks):
        t = tracks[tid]
        sd = t["stsd"]; e = sd[0] + sd[2] + 8
        size, typ = struct.unpack_from(">I4s", buf, e)
        tr = {"id": tid, "handler": t["handler"], "codec": typ.decode("latin1"), "timescale": t["timescale"]}
        if t["handler"] == "vide":
            w, h = struct.unpack_from(">HH", buf, e + 8 + 24); tr["coded_size"] = f"{w}x{h}"
            avcc = find(buf, [b"avcC"], e + 8 + 78, e + size)
            if avcc:
                prof, level = buf[avcc[0] + avcc[2] + 1], buf[avcc[0] + avcc[2] + 3]
                tr["h264_profile"] = {66: "Baseline", 77: "Main", 100: "High"}.get(prof, str(prof)); tr["h264_level"] = level / 10
        elif t["handler"] == "soun":
            tr["channels"] = struct.unpack_from(">H", buf, e + 8 + 16)[0]
            tr["sample_rate"] = _u32(buf, e + 8 + 24) >> 16
        if fragmented:
            durs = [s[2] for c in t["chunks"] for s in c]
            tr["start_s"] = round((t["start"] or 0) / t["timescale"], 4)
        else:
            stbl = t["stbl"]; durs = []
            stts = find(buf, [b"stts"], stbl[0] + stbl[2], stbl[0] + stbl[1])
            p = stts[0] + stts[2] + 4; n = _u32(buf, p)
            for k in range(n):
                c, dl = struct.unpack_from(">II", buf, p + 4 + 8 * k); durs += [dl] * c
            tr["start_s"] = 0.0
            elst = find(buf, [b"edts", b"elst"], t["trak"][0] + t["trak"][2], t["trak"][0] + t["trak"][1])
            if elst:
                p = elst[0] + elst[2]
                seg, mt = struct.unpack_from(">Ii", buf, p + 8)
                if mt == -1:
                    tr["start_s"] = round(seg / movie_ts, 4)
            stss = find(buf, [b"stss"], stbl[0] + stbl[2], stbl[0] + stbl[1])
            if stss:
                tr["keyframes"] = _u32(buf, stss[0] + stss[2] + 4)
        if durs:
            tot = sum(durs)
            tr["samples"] = len(durs); tr["duration_s"] = round(tot / t["timescale"], 3)
            if t["handler"] == "vide":
                tr["avg_fps"] = round(len(durs) / (tot / t["timescale"]), 3)
                tr["frame_ms_min_max"] = [round(min(durs) / t["timescale"] * 1000, 2), round(max(durs) / t["timescale"] * 1000, 2)]
                tr["frames_longer_than_1.5x_33ms"] = sum(1 for dd in durs if dd / t["timescale"] > 1.5 / 30)
        out["tracks"].append(tr)
    return out


if __name__ == "__main__":
    import json, sys
    print(json.dumps(describe_multi(sys.argv[1]), indent=1))
