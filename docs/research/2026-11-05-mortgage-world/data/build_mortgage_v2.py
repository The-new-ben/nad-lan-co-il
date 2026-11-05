# -*- coding: utf-8 -*-
"""Mortgage world v2 (research prototype, 5.11.2026): every number the /mortgage-calculator/ page could show, from official,
dated, public sources, in one JSON. Nothing here touches the live site or plugins/.

What it does
  1. Runs the LIVE builder tools/instruments/build_boi_mortgage_data.py unchanged, with its output redirected to a temporary file,
     so every key of the live boi-mortgage.json (rates, market, policy, term, cpi, forecast, rules, baskets, fees, tracks,
     sources, log) is kept exactly as that builder makes it. The live builder needs xlrd for mashfix.xls / pribmash.xls; when
     xlrd is not installed this file gives it a small zero-dependency BIFF8 reader instead (same calls: open_workbook,
     sheet_by_index, sheet_by_name, nrows, row_values).
  2. Adds new datasets under new keys, each with source URL, series ids, retrieved_at and as_of:
       flows     Bank of Israel SDMX BIR_MRTG_99: new housing loans month by month (count, volume, average loan, rates, terms,
                 PTI, LTV bands, PTI bands, track volumes, investment / reduced price / buying group / refinance / any purpose).
       by_bank   Bank of Israel Banking Supervision TamInt010.xls ("השוואת ריביות - הלוואות למטרת מגורים"): average rate per
                 track, the track mix and the forecast overall rate (IRR) per bank and for the whole system, monthly.
       stock     Bank of Israel SDMX BMB_99: the outstanding housing-loan book (by track, by balance size, 90+ days arrears,
                 loans in grace, bullet/balloon, foreign residents).
       expect    Bank of Israel SDMX ZCM: inflation expectations (capital market, forecasters) and the zero-coupon government
                 curve (nominal, real).
       homes     CBS dwelling price index 40010 (api.cbs.gov.il) and the Tax Authority median closed-deal prices by city and
                 rooms that the site already holds in data/value-series.json (read only, never rewritten here).
       prepay    The early-repayment fee inputs (the average rates by term, full history with buckets, from mashfix.xls and
                 pribmash.xls) and the Banking Order 2002 formula in structured form.
       insurance What official comparison exists for mortgage life and structure insurance (no published price table).
       headlines 12 to 20 quotable numbers, each with its formula and the JSON paths and values it was computed from.
       fresh     What is newer than the live file (built 2026-10-25).
  3. Writes boi-mortgage-v2.json next to this file (or --out).

Zero dependency: Python 3 standard library only (xlsx is read with zipfile + xml.etree, xls with the BIFF8 reader below).
python build_mortgage_v2.py [--out FILE] [--cache DIR]
"""
import argparse
import csv
import datetime
import importlib.util
import io
import json
import os
import re
import shutil
import struct
import sys
import tempfile
import time
import types
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
V1 = os.path.join(REPO, "tools", "instruments", "build_boi_mortgage_data.py")
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")  # read only
LIVE_JSON = os.path.join(DATA, "boi-mortgage.json")
VALUE_SERIES = os.path.join(DATA, "value-series.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-instruments"}
SDMX = "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS"
U_TAMINT = "https://www.boi.org.il/boi_files/Pikuah/TamInt010.xls"
U_TAMINT_PAGE = "https://www.boi.org.il/information/bank-paymnts/financial-education/campaigns/boi-equator/mortgage/"
U_TAMINT_EN = "https://www.boi.org.il/en/information-and-service-to-the-public/interest-rates-and-early-repayment-fees/interest-rate-comparisons-housing-loans/"
U_MASHFIX = "https://www.boi.org.il/boi_files/Pikuah/mashfix.xls"
U_PRIBMASH = "https://www.boi.org.il/boi_files/Pikuah/pribmash.xls"
U_CBS_HPI = "https://api.cbs.gov.il/index/data/price?id=40010&format=json&download=false&lang=he&startPeriod=01-2023&PageSize=100"
TODAY = datetime.date.today()
NOW = time.strftime("%Y-%m-%dT%H:%M:%S")
LOG, FAILS = [], []
CACHE = None


def log(msg):
    LOG.append(msg)
    print(msg)


def fail(what, err):
    FAILS.append({"what": what, "error": str(err)[:300]})
    log(f"FAILED {what}: {err}")


def get(url, binary=False, tries=3, name=None):
    last = None
    for i in range(tries):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()
            if CACHE and name:
                open(os.path.join(CACHE, name), "wb").write(raw)
            return raw if binary else raw.decode("utf-8-sig")
        except Exception as e:  # network, bot wall, timeout
            last = e
            time.sleep(2 + 3 * i)
    raise last


def months_back(n):
    y, m = TODAY.year, TODAY.month - n
    while m <= 0:
        y, m = y - 1, m + 12
    return f"{y}-{m:02d}"


def nom(eff):
    """effective annual % -> nominal annual % for monthly payments (same conversion as the live builder, unrounded)"""
    return 1200 * ((1 + eff / 100) ** (1 / 12) - 1)


def pmt(principal, annual_nominal_pct, months):
    r = annual_nominal_pct / 1200
    return principal / months if r == 0 else principal * r / (1 - (1 + r) ** -months)


def pv(payment, annual_nominal_pct, months):
    r = annual_nominal_pct / 1200
    return payment * months if r == 0 else payment * (1 - (1 + r) ** -months) / r


def r2(x, n=2):
    return None if x is None else round(x, n)


# ============================================================ a zero-dependency BIFF8 (.xls) reader, only what the builders use
def _cfb_stream(data, want="workbook"):
    if data[:8] != b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1":
        raise ValueError("not an OLE2 file")
    ssz = 1 << struct.unpack_from("<H", data, 30)[0]
    mssz = 1 << struct.unpack_from("<H", data, 32)[0]
    dir_start, = struct.unpack_from("<I", data, 48)
    cutoff, = struct.unpack_from("<I", data, 56)
    minifat_start, = struct.unpack_from("<I", data, 60)
    difat_start, n_difat = struct.unpack_from("<II", data, 68)
    difat = [x for x in struct.unpack_from("<109I", data, 76)]
    sec = lambda s: data[(s + 1) * ssz:(s + 2) * ssz]
    s = difat_start
    while n_difat and s < 0xFFFFFFFA:
        ent = struct.unpack("<%dI" % (ssz // 4), sec(s))
        difat += ent[:-1]
        s, n_difat = ent[-1], n_difat - 1
    fat = []
    for s in difat:
        if s < 0xFFFFFFFA:
            fat += struct.unpack("<%dI" % (ssz // 4), sec(s))

    def chain(s):
        out, seen = [], set()
        while s < 0xFFFFFFFA and s not in seen:
            seen.add(s)
            out.append(s)
            s = fat[s]
        return out

    dirdata = b"".join(sec(s) for s in chain(dir_start))
    entries = []
    for i in range(0, len(dirdata), 128):
        e = dirdata[i:i + 128]
        nl, = struct.unpack_from("<H", e, 64)
        name = e[:max(0, nl - 2)].decode("utf-16le", "ignore")
        entries.append((name, e[66], struct.unpack_from("<I", e, 116)[0], struct.unpack_from("<I", e, 120)[0]))
    root = entries[0]
    for name, typ, start, size in entries:
        if typ == 2 and name.lower() in (want, "book"):
            if size >= cutoff:
                return b"".join(sec(s) for s in chain(start))[:size]
            ministream = b"".join(sec(s) for s in chain(root[2]))
            minifat = []
            for s in chain(minifat_start):
                minifat += struct.unpack("<%dI" % (ssz // 4), sec(s))
            out, s = [], start
            while s < 0xFFFFFFFA:
                out.append(ministream[s * mssz:(s + 1) * mssz])
                s = minifat[s]
            return b"".join(out)[:size]
    raise ValueError("no Workbook stream")


def _rk(v):
    if v & 2:
        x = struct.unpack("<i", struct.pack("<I", v & 0xFFFFFFFC))[0] >> 2
        x = float(x)
    else:
        x = struct.unpack("<d", struct.pack("<Q", (v & 0xFFFFFFFC) << 32))[0]
    return x / 100 if v & 1 else x


class _Seg:
    """reads across an SST record and its CONTINUE records (char arrays split at a CONTINUE restart with a flags byte)"""

    def __init__(self, segs):
        self.s, self.i, self.p = segs, 0, 0

    def _next(self):
        while self.i < len(self.s) and self.p >= len(self.s[self.i]):
            self.i, self.p = self.i + 1, 0

    def read(self, n):
        out = b""
        while n > 0:
            self._next()
            seg = self.s[self.i]
            take = min(n, len(seg) - self.p)
            out += seg[self.p:self.p + take]
            self.p += take
            n -= take
        return out

    def chars(self, cch, high):
        out = []
        while cch > 0:
            if self.p >= len(self.s[self.i]):
                self.i, self.p = self.i + 1, 0
                high = self.s[self.i][0] & 1
                self.p = 1
            seg, bpc = self.s[self.i], (2 if high else 1)
            take = min(cch, (len(seg) - self.p) // bpc)
            raw = seg[self.p:self.p + take * bpc]
            out.append(raw.decode("utf-16le" if high else "latin-1"))
            self.p += take * bpc
            cch -= take
        return "".join(out)


class MiniSheet:
    def __init__(self, name, cells):
        self.name = name
        self.cells = cells
        self.nrows = 1 + max((r for r, c in cells), default=-1)
        self.ncols = 1 + max((c for r, c in cells), default=-1)

    def row_values(self, i):
        return [self.cells.get((i, c), "") for c in range(self.ncols)]


class MiniBook:
    def __init__(self, path):
        wb = _cfb_stream(open(path, "rb").read())
        recs, p = [], 0
        while p + 4 <= len(wb):
            rt, ln = struct.unpack_from("<HH", wb, p)
            recs.append((p, rt, wb[p + 4:p + 4 + ln]))
            p += 4 + ln
        sheets, sst, i = [], [], 0
        while i < len(recs):  # globals
            p, rt, d = recs[i]
            if rt == 0x0085:
                pos, cch, fl = struct.unpack_from("<I", d, 0)[0], d[6], d[7]
                nm = d[8:8 + cch * 2].decode("utf-16le") if fl & 1 else d[8:8 + cch].decode("latin-1")
                sheets.append((nm, pos, d[5]))
            elif rt == 0x00FC:
                segs = [d[8:]]
                n, = struct.unpack_from("<I", d, 4)
                while i + 1 < len(recs) and recs[i + 1][1] == 0x003C:
                    i += 1
                    segs.append(recs[i][2])
                rd = _Seg(segs)
                for _ in range(n):
                    cch, = struct.unpack("<H", rd.read(2))
                    fl = rd.read(1)[0]
                    rt_n = struct.unpack("<H", rd.read(2))[0] if fl & 8 else 0
                    ext = struct.unpack("<I", rd.read(4))[0] if fl & 4 else 0
                    sst.append(rd.chars(cch, fl & 1))
                    rd.read(rt_n * 4 + ext)
            elif rt == 0x000A:
                break
            i += 1
        bypos = {p: k for k, (p, _, _) in enumerate(recs)}
        self._sheets = []
        for nm, pos, typ in sheets:
            if typ != 0 or pos not in bypos:
                continue
            cells, k, pend = {}, bypos[pos] + 1, None
            while k < len(recs):
                _, rt, d = recs[k]
                if rt == 0x000A:
                    break
                if rt == 0x0203:
                    r, c, _x, v = struct.unpack_from("<HHHd", d, 0)
                    cells[(r, c)] = v
                elif rt == 0x027E:
                    r, c, _x, v = struct.unpack_from("<HHHI", d, 0)
                    cells[(r, c)] = _rk(v)
                elif rt == 0x00BD:
                    r, c0 = struct.unpack_from("<HH", d, 0)
                    for j in range((len(d) - 6) // 6):
                        cells[(r, c0 + j)] = _rk(struct.unpack_from("<I", d, 4 + 6 * j + 2)[0])
                elif rt == 0x00FD:
                    r, c, _x, ix = struct.unpack_from("<HHHI", d, 0)
                    cells[(r, c)] = sst[ix] if ix < len(sst) else ""
                elif rt == 0x0204:
                    r, c, _x, cch = struct.unpack_from("<HHHH", d, 0)
                    fl = d[8]
                    cells[(r, c)] = d[9:9 + cch * 2].decode("utf-16le") if fl & 1 else d[9:9 + cch].decode("latin-1")
                elif rt == 0x0006:
                    r, c = struct.unpack_from("<HH", d, 0)
                    res = d[6:14]
                    if res[6:8] == b"\xff\xff":
                        pend = (r, c) if res[0] == 0 else None
                    else:
                        cells[(r, c)] = struct.unpack("<d", res)[0]
                elif rt == 0x0207 and pend:
                    cch, fl = struct.unpack_from("<H", d, 0)[0], d[2]
                    cells[pend] = d[3:3 + cch * 2].decode("utf-16le") if fl & 1 else d[3:3 + cch].decode("latin-1")
                    pend = None
                k += 1
            self._sheets.append(MiniSheet(nm, cells))

    def sheet_by_index(self, i):
        return self._sheets[i]

    def sheet_by_name(self, n):
        for s in self._sheets:
            if s.name == n:
                return s
        raise KeyError(n)

    def sheet_names(self):
        return [s.name for s in self._sheets]


def xls_open(path):
    try:
        import xlrd  # noqa
        return xlrd.open_workbook(path)
    except ImportError:
        return MiniBook(path)


# ============================================================ a zero-dependency xlsx reader (TamInt010.xls is OOXML inside)
def xlsx_read(data):
    z = zipfile.ZipFile(io.BytesIO(data))
    M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(M + "si"):
            ss.append("".join(t.text or "" for t in si.iter(M + "t")))
    out = {}
    for sh in ET.fromstring(z.read("xl/workbook.xml")).find(M + "sheets"):
        tgt = rels[sh.get(R + "id")]
        path = tgt.lstrip("/") if tgt.startswith("/") else "xl/" + tgt
        grid = {}
        for c in ET.fromstring(z.read(path)).iter(M + "c"):
            m = re.match(r"([A-Z]+)(\d+)", c.get("r"))
            col = 0
            for ch in m.group(1):
                col = col * 26 + ord(ch) - 64
            t, v = c.get("t"), c.find(M + "v")
            if t == "s":
                val = ss[int(v.text)]
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter(M + "t"))
            elif t in ("str", "e"):
                val = v.text if v is not None else None
            else:
                val = float(v.text) if v is not None and v.text is not None else None
            if val is not None:
                grid[(int(m.group(2)) - 1, col - 1)] = val
        out[sh.get("name")] = grid
    return out


# ============================================================ SDMX
def sdmx(flow, start, key="", name=None):
    url = f"{SDMX}/{flow}/1.0/{key}?c%5BTIME_PERIOD%5D=ge:{start}&format=csv"
    rows = list(csv.DictReader(io.StringIO(get(url, name=name))))
    ser = {}
    for r in rows:
        if r.get("OBS_VALUE") in (None, ""):
            continue
        try:
            ser.setdefault(r["SERIES_CODE"], {})[r["TIME_PERIOD"]] = float(r["OBS_VALUE"])
        except ValueError:
            pass
    return ser, url


# ============================================================ 1. the live builder, output redirected
def run_v1():
    spec = importlib.util.spec_from_file_location("boim_v1", V1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        import xlrd  # noqa
        log("xlrd is installed: the live builder reads the xls files with it")
    except ImportError:
        sys.modules["xlrd"] = types.SimpleNamespace(open_workbook=MiniBook)
        log("xlrd is not installed: the live builder reads mashfix.xls / pribmash.xls with the zero-dependency BIFF8 reader")
    tmp = tempfile.mkdtemp(prefix="boim-v1-")
    mod.OUT = os.path.join(tmp, "boi-mortgage.json")
    mod.main()
    base = json.load(open(mod.OUT, encoding="utf-8"))
    log("live builder ran unchanged (output redirected); its log: " + " || ".join(base.get("log", [])))
    return base


# ============================================================ 2a. flows (BIR_MRTG_99)
BIR_SER = {
    "loans": "63", "volume_k": "897", "volume_sa_k": "897_SA", "rate_fixed_nl": "467", "rate_fixed_cpi": "1492",
    "rate_var_cpi_bench": "1489", "rate_var_cpi_margin": "1488", "rate_cpi_all": "1485", "pti_avg": "155", "term_nl": "461",
    "term_cpi_fixed": "1491", "term_cpi_var": "1487", "invest_loans": "62", "invest_volume_k": "776", "reduced_loans": "13",
    "reduced_volume_k": "14", "reduced_pti": "1", "group_var_k": "64", "group_fixed_k": "65", "refi_loans": "31",
    "refi_volume_k": "32", "from_other_bank_loans": "52", "from_other_bank_volume_k": "896", "anypurpose_loans": "61",
    "anypurpose_volume_k": "154", "anypurpose_pti": "153", "bullet_balloon_k": "779", "no_collateral_calc_k": "833",
    "trk_var_nl_k": "70", "trk_fixed_nl_k": "71", "trk_fixed_cpi_k": "69", "trk_var_cpi_k": "68", "trk_fx_var_k": "66", "trk_fx_fixed_k": "67",
}
LTV_BANDS = [("887", 0, 30), ("878", 30, 45), ("869", 45, 60), ("860", 60, 75), ("851", 75, 90), ("842", 90, None)]
PTI_BANDS = [("161", 0, 10), ("160", 10, 20), ("815", 20, 30), ("806", 30, 40), ("159", 40, 50), ("158", 50, 60), ("157", 60, 80), ("156", 80, None)]


def build_flows():
    start = months_back(36)
    ser, url = sdmx("BIR_MRTG_99", start, name="BIR_MRTG_99.csv")
    s = {code.split("MRTG_")[1]: v for code, v in ser.items() if code.startswith("BNK_99034_")}
    if "63" not in s or "897" not in s:
        raise RuntimeError("BIR_MRTG_99: count or volume missing")
    last = max(s["63"])  # newest month with the loan count (the full monthly release)
    months = [m for m in sorted(s["63"]) if m <= last][-25:]
    col = lambda code: [r2(s.get(code, {}).get(m), 4) for m in months]
    out = {"months": months, "unit_volume": "ILS thousands", "series": {}}
    for k, code in BIR_SER.items():
        out["series"][k] = {"id": "BNK_99034_L%s_BIR_MRTG_%s" % ("M" if code.startswith("897_SA") else "R", code), "v": col(code)}
    out["series"]["volume_sa_k"]["id"] = "BNK_99034_LM_BIR_MRTG_897_SA"
    out["series"]["avg_loan"] = {"formula": "1000 * volume_k / loans", "v": [round(1000 * a / b) if a and b else None for a, b in zip(col("897"), col("63"))]}
    vb = [s.get("897", {}).get(m) for m in months]
    out["ltv"] = {"bands": [[a, b] for _, a, b in LTV_BANDS], "series": ["BNK_99034_LR_BIR_MRTG_" + c for c, _, _ in LTV_BANDS],
                  "volume_k": [[r2(s.get(c, {}).get(m), 1) for c, _, _ in LTV_BANDS] for m in months]}
    out["ltv"]["share"] = [[r2(100 * x / sum(row), 2) if sum(row) else None for x in row] for row in out["ltv"]["volume_k"]]
    out["pti"] = {"bands": [[a, b] for _, a, b in PTI_BANDS], "series": ["BNK_99034_LR_BIR_MRTG_" + c for c, _, _ in PTI_BANDS],
                  "volume_k": [[r2(s.get(c, {}).get(m), 1) for c, _, _ in PTI_BANDS] for m in months]}
    out["pti"]["share"] = [[r2(100 * x / sum(row), 2) if sum(row) else None for x in row] for row in out["pti"]["volume_k"]]
    tk = [("var_nl", "70"), ("fixed_nl", "71"), ("fixed_cpi", "69"), ("var_cpi", "68"), ("fx", ("66", "67"))]
    rows = []
    for m in months:
        vals = []
        for _, c in tk:
            vals.append(sum(s.get(x, {}).get(m) or 0 for x in c) if isinstance(c, tuple) else (s.get(c, {}).get(m) or 0))
        rows.append([r2(100 * v / sum(vals), 2) if sum(vals) else None for v in vals])
    out["track_share"] = {"keys": [k for k, _ in tk], "note": "share of the volume excluding buying groups (series _70 _71 _69 _68 _66+_67); "
                          "variable not linked includes prime and every other not-linked variable rate", "v": rows}
    nxt = sorted(m for m in s["897"] if m > last)
    out["first_release"] = [{"month": m, "volume_k": r2(s["897"][m], 2), "volume_sa_k": r2(s.get("897_SA", {}).get(m), 2)} for m in nxt]
    out["gaps"] = ["no split by borrower type (first home / replacement / upgrader) in this dataflow; only investment dwelling, "
                   "reduced price, buying group, refinance and any-purpose loans are separate",
                   "no distribution of new loans by size or by term; only averages (volume / count, average term per track)",
                   "LTV bands are 0-30, 30-45, 45-60, 60-75, 75-90, 90+; a 70% threshold cannot be read from them"]
    out["src"] = {"label": "Bank of Israel, Banking Supervision, interest rates and business volume, housing loans (SDMX dataflow BIR_MRTG_99), total banking system",
                  "url": url, "series": "BNK_99034_LR_BIR_MRTG_<n> (see series ids)", "retrieved_at": NOW, "as_of": last,
                  "cadence": "monthly, about 4 to 6 weeks after the month; the volume (_897) has an earlier first release"}
    log(f"flows: {months[0]}..{last}, first release {[x['month'] for x in out['first_release']]}")
    return out


# ============================================================ 2b. by bank (TamInt010)
BANKS = {"פועלים": ("hapoalim", "Bank Hapoalim"), "לאומי": ("leumi", "Bank Leumi"), "דיסקונט": ("discount", "Israel Discount Bank"),
         "מזרחי": ("mizrahi", "Mizrahi-Tefahot"), "בינלאומי": ("fibi", "First International (Habeinleumi)"),
         "מרכנתיל": ("mercantile", "Mercantile"), "ירושלים": ("jerusalem", "Bank of Jerusalem"), "סך מערכת": ("system", "Total banking system")}


def track_key(lbl):
    lbl = str(lbl)
    if "IRR" in lbl:
        return "irr"
    if "פריים" in lbl and "שאינה" in lbl:
        return "var_nl_other"
    if "פריים" in lbl:
        return "prime"
    if "קבועה" in lbl and "לא צמודה" in lbl:
        return "fixed_nl"
    if "קבועה" in lbl and "מדד" in lbl:
        return "fixed_cpi"
    if "משתנה" in lbl and "מדד" in lbl:
        return "var_cpi"
    return None


def parse_tamint(grid):
    hdr_r = next(r for (r, c), v in grid.items() if v in BANKS)
    trk_r = hdr_r + 2
    starts = sorted((c, BANKS[v][0]) for (r, c), v in grid.items() if r == hdr_r and v in BANKS)
    colmap = {}
    for (r, c), v in grid.items():
        if r == trk_r and track_key(v):
            bank = [b for s0, b in starts if s0 <= c][-1]
            colmap[c] = (bank, track_key(v))
    data = {}
    for (r, c), v in grid.items():
        if c == 1 and isinstance(v, str) and re.match(r"^\d{4}-\d{2}$", v):
            data[v] = {cc: grid.get((r, cc)) for cc in colmap}
    stamp = next((v for (r, c), v in sorted(grid.items()) if r == 0 and isinstance(v, float) and v > 20000), None)
    if stamp:
        stamp = (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(stamp))).isoformat()
    return colmap, data, stamp


def build_by_bank():
    raw = get(U_TAMINT, binary=True, name="TamInt010.xlsx")
    sheets = xlsx_read(raw)
    names = list(sheets)
    c1, d1, stamp = parse_tamint(sheets[names[0]])
    c2, d2, _ = parse_tamint(sheets[names[1]])
    months = sorted(set(d1) | set(d2))
    banks = [k for k, _ in BANKS.values()]
    names_en = dict(BANKS.values())
    tracks = ["fixed_nl", "prime", "var_nl_other", "var_cpi", "fixed_cpi"]
    rate = {b: {t: [] for t in tracks + ["irr"]} for b in banks}
    mix = {b: {t: [] for t in tracks} for b in banks}
    for m in months:
        for c, (b, t) in c1.items():
            v = d1.get(m, {}).get(c)
            rate[b][t].append(r2(v, 4) if isinstance(v, float) else None)
        for c, (b, t) in c2.items():
            v = d2.get(m, {}).get(c)
            mix[b][t].append(r2(v, 3) if isinstance(v, float) else None)
    last = months[-1]
    li = len(months) - 1
    table = []
    for b in banks:
        row = {"bank": b, "name": names_en[b], "irr": rate[b]["irr"][li]}
        for t in tracks:
            row[t] = {"rate": rate[b][t][li], "share": mix[b][t][li]}
        table.append(row)
    big5 = ["hapoalim", "leumi", "discount", "mizrahi", "fibi"]
    rk = sorted((r for r in table if r["bank"] in big5 and r["irr"] is not None), key=lambda r: r["irr"])
    out = {"months": months, "banks": [{"k": k, "he": he, "en": en} for he, (k, en) in BANKS.items()],
           "tracks": {"fixed_nl": "קבועה לא צמודה", "prime": "משתנה לא צמודה - פריים", "var_nl_other": "משתנה לא צמודה שאינה פריים",
                      "var_cpi": "משתנה צמודה למדד", "fixed_cpi": "קבועה צמודה למדד", "irr": "ריבית כוללת חזויה (IRR)"},
           "rate": rate, "mix": mix, "latest": {"month": last, "table": table, "big5_rank_by_irr": [r["bank"] for r in rk]},
           "notes": ["rates are annual adjusted (effective) rates, not nominal (file note 2)",
                     "IRR = the forecast rate over the whole loan, from the BoI CPI and interest forecasts for the reporting month, by the "
                     "formula of Directive 451; it is a portfolio average, not a quote (file notes and BoI page)",
                     "excludes bullet, balloon and foreign-currency loans; the mix is the share of the month's credit per track",
                     "banks are ordered by their share of the housing-credit market (BoI page)",
                     "the Power BI dashboard on the English BoI page stops at 10-2025; this Excel file is the current one",
                     "cross-check: Power BI 10-2025 Hapoalim IRR 5.20 and Leumi fixed not linked 4.78 equal this file's 5.2009 and 4.7754"]}
    out["src"] = {"label": "Bank of Israel, Banking Supervision, השוואת ריביות - הלוואות למטרת מגורים (TamInt010.xls, sheets L01 rates and IRR, L02 track mix)",
                  "url": U_TAMINT, "page": U_TAMINT_PAGE, "page_en": U_TAMINT_EN, "series": "TamInt010.xls L01 / L02",
                  "retrieved_at": NOW, "as_of": last, "file_date": stamp, "cadence": "monthly, around the 20th, for the previous month"}
    log(f"by_bank: {months[0]}..{last}, file date {stamp}, big-5 by IRR {[(r['bank'], r['irr']) for r in rk]}")
    return out


# ============================================================ 2c. stock (BMB_99)
BMB = {"total_k": "7", "count": "8", "fixed_nl_k": "1", "var_nl_k": "2", "fixed_cpi_k": "3", "var_cpi_k": "4", "fx_fixed_k": "5",
       "fx_var_k": "6", "anypurpose_k": "9", "anypurpose_count": "10", "buying_group_k": "17", "foreign_res_k": "25",
       "arrears90_k": "74", "grace_k": "93", "bullet_balloon_k": "98"}
SIZE = [("38", "39", 0, 300), ("44", "45", 300, 600), ("50", "51", 600, 1200), ("56", "57", 1200, 2000), ("62", "63", 2000, 4000), ("68", None, 4000, None)]


def build_stock():
    ser, url = sdmx("BMB_99", months_back(36), name="BMB_99.csv")
    s = {code.rsplit("_", 1)[1]: v for code, v in ser.items() if code.startswith("BNK_99034_LR_MRTG_OL_")}
    last = max(s["7"])
    months = [m for m in sorted(s["7"]) if m <= last][-25:]
    out = {"months": months, "unit": "ILS thousands (count = number of loans)", "series": {}}
    for k, c in BMB.items():
        out["series"][k] = {"id": "BNK_99034_LR_MRTG_OL_" + c, "v": [r2(s.get(c, {}).get(m), 1) for m in months]}
    # by current balance size; the arrears code of the top bucket is _69 if it exists (the 74 series is the total arrears)
    size_rows, arr_rows = [], []
    arr_codes = ["39", "45", "51", "57", "63"] + (["69"] if "69" in s else [])
    for m in months:
        size_rows.append([r2(s.get(a, {}).get(m), 1) for a, _, _, _ in SIZE])
        arr_rows.append([r2(s.get(c, {}).get(m), 1) for c in arr_codes])
    out["by_size"] = {"bands_k_ils": [[a, b] for _, _, a, b in SIZE], "series": ["BNK_99034_LR_MRTG_OL_" + a for a, _, _, _ in SIZE],
                      "balance_k": size_rows,
                      "arrears90_series": ["BNK_99034_LR_MRTG_OL_" + c for c in arr_codes], "arrears90_k": arr_rows,
                      "note": "bands are the CURRENT outstanding balance of each loan (SDMX dimension CURR_BAL_SETT), not the original amount"}
    out["src"] = {"label": "Bank of Israel, Banking Supervision, balances of housing loans (SDMX dataflow BMB_99), total banking system",
                  "url": url, "series": "BNK_99034_LR_MRTG_OL_<n>", "retrieved_at": NOW, "as_of": last, "cadence": "monthly"}
    log(f"stock: {last}: total {s['7'][last]:.0f}k ILS, {s['8'][last]:.0f} loans")
    return out


# ============================================================ 2d. expectations (ZCM)
ZCM = {"exp_1y_capital_market": "EXP_EXP_01Y_BI_MA", "exp_1y_forecasters": "EXP_HAZ_MAD_AVG_01Y_MA", "exp_1y_bank_rates": "EXP_EXP_IRB_1Y_MA",
       "exp_1y_forwards": "EXP_EXP_ISSWIT1_01Y_MA", "exp_5y_capital_market": "EXP_EXB_ZD_5Y_MA", "exp_10y_capital_market": "EXP_EXB_ZD_10Y_MA",
       "gov_nominal_1y": "ZC_TSB_ZND_01Y_MA", "gov_nominal_5y": "ZC_TSB_ZND_05Y_MA", "gov_nominal_10y": "ZC_TSB_ZND_10Y_MA", "gov_nominal_15y": "ZC_TSB_ZND_15Y_MA",
       "gov_real_1y": "ZC_TSB_ZRD_01Y_MA", "gov_real_5y": "ZC_TSB_ZRD_05Y_MA", "gov_real_10y": "ZC_TSB_ZRD_10Y_MA", "gov_real_15y": "ZC_TSB_ZRD_15Y_MA"}


def build_expect():
    ser, url = sdmx("ZCM", months_back(26), name="ZCM.csv")
    out = {"series": {}, "unit": "percent, monthly average"}
    for k, code in ZCM.items():
        v = ser.get(code, {})
        ks = sorted(v)[-25:]
        out["series"][k] = {"id": code, "last": ks[-1] if ks else None, "value": r2(v[ks[-1]], 4) if ks else None,
                            "hist": [[m, r2(v[m], 4)] for m in ks]}
    out["target"] = {"low": 1, "high": 3, "series": ["INF_MIN_TRGT_D", "INF_MAX_TRGT_D"]}
    asof = max(x["last"] for x in out["series"].values() if x["last"])
    out["src"] = {"label": "Bank of Israel, inflation expectations and the zero-coupon yield curve (SDMX dataflow ZCM)", "url": url,
                  "series": ", ".join(ZCM.values()), "retrieved_at": NOW, "as_of": asof, "cadence": "monthly averages (curve one month behind)"}
    log(f"expect: 1y capital market {out['series']['exp_1y_capital_market']['value']} ({out['series']['exp_1y_capital_market']['last']}), "
        f"gov nominal 10y {out['series']['gov_nominal_10y']['value']} ({out['series']['gov_nominal_10y']['last']})")
    return out


# ============================================================ 2e. homes (CBS 40010 + Tax Authority medians already in the repo)
def build_homes():
    out = {}
    d = json.loads(get(U_CBS_HPI, name="cbs-40010.json"))
    rows = sorted(d["month"][0]["date"], key=lambda r: (r["year"], r["month"]))
    out["hpi"] = {"id": 40010, "name": d["month"][0].get("name"), "base": rows[-1]["currBase"]["baseDesc"],
                  "hist": [[f"{r['year']}-{r['month']:02d}", r["currBase"]["value"], r.get("percent"), r.get("percentYear")] for r in rows][-25:],
                  "cols": ["period", "index", "change vs previous %", "change over 12 months %"],
                  "note": "CBS publishes the dwelling price index for two-month periods; the newest values are provisional",
                  "src": {"label": "CBS, dwelling price index (series 40010)", "url": U_CBS_HPI, "series": "40010",
                          "retrieved_at": NOW, "as_of": f"{rows[-1]['year']}-{rows[-1]['month']:02d}", "cadence": "monthly, about the 15th"}}
    vs = json.load(open(VALUE_SERIES, encoding="utf-8"))
    q = vs["q"]

    def last_val(arr):
        for i in range(len(arr) - 1, -1, -1):
            if arr[i] is not None:
                return arr[i], q[i]
        return None, None

    cities = {}
    for name, c in vs["city"].items():
        row = {}
        for k in ("r3", "r4", "r5"):
            v, qq = last_val(c.get(k) or [])
            if v:
                row[k] = {"median": v, "quarter": qq}
        if row:
            cities[name] = row
    il = {k: dict(zip(("median", "quarter"), last_val(vs["il"].get(k) or []))) for k in ("r3", "r4", "r5") if vs["il"].get(k)}
    out["medians"] = {"il": il, "city": cities, "quarters": q,
                      "src": {"label": vs.get("source"), "url": vs.get("url"), "series": "nadlan.gov.il public summary files, file " + str(vs.get("file")),
                              "retrieved_at": vs.get("read"), "as_of": q[-1], "cadence": "quarterly (the Tax Authority file of 20.8.2026 is still the newest on 5.11.2026)",
                              "via": "plugins/nadlan-config/assets/instruments/data/value-series.json (read only)"}}
    log(f"homes: CBS 40010 {out['hpi']['src']['as_of']}; Tax Authority medians {len(cities)} cities, Israel 4 rooms {il.get('r4')}")
    return out


# ============================================================ 2f. prepay (history with buckets + the formula)
def build_prepay():
    out = {}
    tmp = tempfile.mkdtemp(prefix="boim-prepay-")
    for key, url, sheet, ncol in (("nl", U_MASHFIX, 0, 7), ("cpi", U_PRIBMASH, "RESULT", 6)):
        p = os.path.join(tmp, key + ".xls")
        open(p, "wb").write(get(url, binary=True, name=os.path.basename(url)))
        b = xls_open(p)
        sh = b.sheet_by_index(0) if sheet == 0 else b.sheet_by_name(sheet)
        n_in, n_m = ncol + 1, ncol + 2
        rows = []
        for i in range(sh.nrows):
            c = sh.row_values(i)
            if len(c) > n_m and isinstance(c[0], float):
                d_in, d_m = xldate(c[n_in]), xldate(c[n_m])
                if d_in:
                    rows.append([d_in, d_m] + [r2(c[j], 3) for j in range(0, ncol + 1)])
        rows.sort()
        out[key] = {"cols": ["in_force_from", "data_month", "avg"] + (["gt25", "20_25", "15_20", "10_15", "5_10", "1_5", "le1"] if key == "nl"
                    else ["gt25", "20_25", "15_20", "10_15", "5_10", "le5"]), "rows": rows[-60:],
                    "unit": "effective annual %", "n_total_rows": len(rows),
                    "src": {"label": "Bank of Israel, average mortgage rate by term to maturity, " + ("not linked (mashfix.xls)" if key == "nl" else "CPI-linked (pribmash.xls)"),
                            "url": url, "series": os.path.basename(url), "retrieved_at": NOW, "as_of": rows[-1][1] if rows else None,
                            "cadence": "monthly, published about the 18th, in force from the next day"}}
        log(f"prepay {key}: {len(rows)} rows, last in force {rows[-1][0] if rows else None}")
    out["formula"] = {
        "law": "צו הבנקאות (פירעון מוקדם של הלוואה לדיור), התשס״ב-2002, as amended 2014, sections 3 to 8 and the second schedule",
        "operational_fee_max_ils": 60,
        "short_notice_fee": "0.1% of the repaid amount if notice is under 10 days (not on a refinance by the same bank, not on death)",
        "capitalization_3_3": "if the average rate on the repayment day < the loan's current rate: fee <= PV(A) - PV, where PV(A) = the future payments "
                              "(up to the rate-change day, plus the principal on that day) discounted at the average rate on the repayment day, "
                              "and PV = the repaid principal with linkage and accrued interest",
        "capitalization_3_4": "if the average rate at origination < the loan's rate at origination: fee <= PV(A) - PV(C), where PV(C) = the same payments "
                              "discounted at the average rate at origination",
        "charged": "the lower of 3(3) and 3(4) when both exist (s.3(5))",
        "average_rate": "the average rate published by the Supervisor for the remaining term bucket (s.7(a)); for a variable loan, the term to "
                        "the next rate-change day (s.4)",
        "no_capitalization_fee": "loans whose rate changes at least yearly or at unknown dates (prime) (s.4(2)); repayment on a rate-change day (s.4(3)); directed (state) loans (s.2)",
        "reductions": {"regular": [{"after_years": 3, "cut": 0.20}, {"after_years": 5, "cut": 0.30}],
                       "complementary": [{"after_years": 1, "cut": 0.10}, {"after_years": 2, "cut": 0.20}, {"after_years": 3, "cut": 0.30}, {"after_years": 4, "cut": 0.40}]},
        "cpi_fee": "CPI-linked loan repaid between the 1st and the 15th of a month: repaid amount x half of the average monthly CPI change over the last 12 indices (s.5)",
        "fx_fee": "foreign-currency loan with notice under 2 business days: the exchange-rate difference (s.6)",
        "notice": "notice may be given up to 45 days ahead (s.10(b))",
        "src": {"label": "Banking Order 2002 text (Nevo copy order-116.pdf, read 25.10.2026 for the U1 research)", "url": "https://www.boi.org.il/",
                "retrieved_at": "2026-10-25", "as_of": "2014-08-27 (last amendment)", "cadence": "law"}}
    return out


def xldate(v):
    if isinstance(v, (int, float)) and v > 20000:
        return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(v))).isoformat()
    s = str(v).strip()
    for fmt in ("%d/%m/%Y", "%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    return None


# ============================================================ 2g. insurance (what exists, no invented prices)
def insurance_block():
    return {"official_price_table": None,
            "official_calculators": [
                {"name": "רשות שוק ההון, ביטוח וחיסכון: השוואת תעריפי ביטוח חיים למשכנתה", "url": "https://life.cma.gov.il/",
                 "what": "per-borrower quote comparison by insurer (age, sum, term, smoking); no published average or table"},
                {"name": "רשות שוק ההון, ביטוח וחיסכון: מחשבון ביטוח דירה (מבנה, כולל מבנה למשכנתה)", "url": "https://dira.cma.gov.il/",
                 "what": "per-property quote comparison by insurer; no published average or table"}],
            "status": "unverified: the two calculators were identified from search results on 5.11.2026; both hosts answer a script with "
                      "HTTP 202 and an empty body (bot protection), so their pages were not read or run. No official, dated price level for "
                      "mortgage life or structure insurance was found, so none is shown",
            "retrieved_at": NOW}


# ============================================================ 3. headline numbers (computed only from values stored in this JSON)
def headlines(J):
    H = []
    bb, fl, st, ex, hm, pp = J["by_bank"], J["flows"], J["stock"], J["expect"], J["homes"], J["prepay"]
    months = bb["months"]
    li = len(months) - 1
    m_last = months[li]
    y_ago = f"{int(m_last[:4]) - 1}{m_last[4:]}"
    yi = months.index(y_ago) if y_ago in months else None
    trk = ["fixed_nl", "prime", "var_nl_other", "var_cpi", "fixed_cpi"]

    def mix_payment(i, principal, years):
        tot, parts = 0.0, {}
        for t in trk:
            sh, rt = bb["mix"]["system"][t][i], bb["rate"]["system"][t][i]
            p = pmt(principal * sh / 100, nom(rt), years * 12)
            parts[t] = round(p, 2)
            tot += p
        return tot, parts

    def add(hid, text, value, unit, formula, inputs, as_of):
        H.append({"id": hid, "text": text, "value": value, "unit": unit, "formula": formula, "inputs": inputs, "as_of": as_of})

    inp_mix = lambda i: {f"by_bank.mix.system.{t}[{i}]": bb["mix"]["system"][t][i] for t in trk} | {f"by_bank.rate.system.{t}[{i}]": bb["rate"]["system"][t][i] for t in trk}
    F_PAY = ("sum over the 5 tracks of PMT(1,000,000 x share/100, nominal(rate), 300); nominal(e) = 1200 x ((1 + e/100)^(1/12) - 1); "
             "PMT(P, n%, N) = P x r / (1 - (1+r)^-N), r = n/1200; CPI-linked tracks at their real rate (first payment, CPI unchanged)")
    p_now, _ = mix_payment(li, 1_000_000, 25)
    if yi is not None:
        p_then, _ = mix_payment(yi, 1_000_000, 25)
        add("pay_1m_25y", f"The first monthly payment on a 1,000,000 ILS, 25-year mortgage at the {m_last} system-average track mix and rates was "
            f"{p_now:,.0f} ILS, {p_then - p_now:,.0f} ILS {'less' if p_now < p_then else 'more'} than at the {y_ago} mix ({p_then:,.0f} ILS).",
            round(p_now), "ILS/month", F_PAY + f"; same for index {yi} ({y_ago})", inp_mix(li) | inp_mix(yi), m_last)
    p30, _ = mix_payment(li, 1_000_000, 30)
    add("pay_1m_30y", f"Over 30 years instead of 25 the same 1,000,000 ILS costs {p30:,.0f} ILS a month ({p_now - p30:,.0f} ILS less), "
        f"but about {(p30 * 360 - p_now * 300):,.0f} ILS more in total payments at unchanged rates.", round(p30), "ILS/month",
        F_PAY.replace("300", "360") + "; total difference = 360 x PMT30 - 300 x PMT25", inp_mix(li), m_last)
    irr = bb["rate"]["system"]["irr"]
    if yi is not None:
        add("irr_system", f"The forecast all-in rate (IRR) on new mortgages across the banking system was {irr[li]:.2f}% in {m_last}, "
            f"against {irr[yi]:.2f}% a year earlier.", r2(irr[li], 2), "%", "read directly", {f"by_bank.rate.system.irr[{li}]": irr[li], f"by_bank.rate.system.irr[{yi}]": irr[yi]}, m_last)
    big5 = bb["latest"]["big5_rank_by_irr"]
    lo, hi = big5[0], big5[-1]
    nm = {b["k"]: b["en"] for b in bb["banks"]}
    i_lo, i_hi = bb["rate"][lo]["irr"][li], bb["rate"][hi]["irr"][li]
    pl, ph = pmt(1_000_000, nom(i_lo), 300), pmt(1_000_000, nom(i_hi), 300)
    add("irr_gap_big5", f"Among the five largest banks, {nm[lo]} had the lowest forecast all-in rate in {m_last} ({i_lo:.2f}%) and {nm[hi]} the highest "
        f"({i_hi:.2f}%): {100 * (i_hi - i_lo):.0f} basis points, about {ph - pl:,.0f} ILS a month on 1,000,000 ILS over 25 years if each IRR "
        f"were a flat rate (illustration only; IRR is a portfolio average that depends on each bank's mix and borrowers).",
        r2(i_hi - i_lo, 3), "percentage points", "IRR(high) - IRR(low); payment gap = PMT(1e6, nominal(IRR_high), 300) - PMT(1e6, nominal(IRR_low), 300)",
        {f"by_bank.rate.{lo}.irr[{li}]": i_lo, f"by_bank.rate.{hi}.irr[{li}]": i_hi}, m_last)
    pr = bb["mix"]["system"]["prime"]
    if yi is not None:
        add("prime_share", f"Prime made up {pr[li]:.1f}% of new mortgage credit in {m_last}, up from {pr[yi]:.1f}% a year earlier "
            f"(banks' track reports; 'variable not linked, not prime' is a separate track).", r2(pr[li], 1), "%", "read directly",
            {f"by_bank.mix.system.prime[{li}]": pr[li], f"by_bank.mix.system.prime[{yi}]": pr[yi]}, m_last)
    prime_rate = J["policy"]["prime"]
    pt = bb["rate"]["system"]["prime"][li]
    add("prime_margin", f"The average prime-track rate on new mortgages was {pt:.2f}% (effective) in {m_last}, with prime at {prime_rate:.2f}%: "
        f"in nominal monthly terms about prime {nom(pt) - prime_rate:+.2f}.", r2(nom(pt) - prime_rate, 2), "percentage points",
        "nominal(prime-track rate) - prime; prime = BoI rate + 1.5", {f"by_bank.rate.system.prime[{li}]": pt, "policy.prime": prime_rate}, m_last)
    # flows
    fm = fl["months"]
    fi = len(fm) - 1
    fy = fm.index(f"{int(fm[fi][:4]) - 1}{fm[fi][4:]}") if f"{int(fm[fi][:4]) - 1}{fm[fi][4:]}" in fm else None
    S = fl["series"]
    al = S["avg_loan"]["v"]
    if fy is not None:
        add("avg_loan", f"Banks granted {S['loans']['v'][fi]:,.0f} new mortgages worth {S['volume_k']['v'][fi] / 1e6:.2f} billion ILS in {fm[fi]} "
            f"({S['loans']['v'][fy]:,.0f} a year earlier); the average loan was {al[fi]:,} ILS, {100 * (al[fi] / al[fy] - 1):+.1f}% on a year earlier ({al[fy]:,} ILS).",
            al[fi], "ILS", "1000 x volume_k / loans; billions = volume_k / 1e6", {f"flows.series.volume_k.v[{fi}]": S["volume_k"]["v"][fi], f"flows.series.loans.v[{fi}]": S["loans"]["v"][fi],
                                                      f"flows.series.volume_k.v[{fy}]": S["volume_k"]["v"][fy], f"flows.series.loans.v[{fy}]": S["loans"]["v"][fy]}, fm[fi])
    v12 = S["volume_k"]["v"][-12:]
    v12p = S["volume_k"]["v"][-24:-12]
    if len(v12p) == 12 and all(v12) and all(v12p):
        add("volume_12m", f"New mortgages in the 12 months to {fm[fi]} totalled {sum(v12) / 1e6:.1f} billion ILS, {100 * (sum(v12) / sum(v12p) - 1):+.1f}% on the previous 12 months.",
            r2(sum(v12) / 1e6, 1), "billion ILS", "sum(flows.series.volume_k.v[-12:]) / 1e6 vs the 12 before", {"flows.series.volume_k.v[-24:]": S["volume_k"]["v"][-24:]}, fm[fi])
    lt = fl["ltv"]["share"][fi]
    add("ltv_above_60", f"{lt[3] + lt[4] + lt[5]:.1f}% of new mortgage money in {fm[fi]} went to loans above 60% of the home's value, almost all of it "
        f"in the 60-75% band; only {lt[4] + lt[5]:.2f}% was above 75%.", r2(lt[3] + lt[4] + lt[5], 1), "% of volume",
        "share(60-75) + share(75-90) + share(90+); share = band volume / sum of the 6 bands", {f"flows.ltv.share[{fi}]": lt}, fm[fi])
    pt_ = fl["pti"]["share"][fi]
    add("pti_above_30", f"{sum(pt_[3:]):.1f}% of new mortgage money in {fm[fi]} went to loans whose monthly payment is more than 30% of the "
        f"borrowers' income (average payment-to-income {S['pti_avg']['v'][fi]:.1f}%; above 40%, {sum(pt_[4:]):.1f}%).", r2(sum(pt_[3:]), 1), "% of volume",
        "sum of PTI band shares above 30%; average = series _155", {f"flows.pti.share[{fi}]": pt_, f"flows.series.pti_avg.v[{fi}]": S["pti_avg"]["v"][fi]}, fm[fi])
    inv = S["invest_volume_k"]["v"]
    vol = S["volume_k"]["v"]
    if fy is not None:
        add("invest_share", f"Investment-home loans were {100 * inv[fi] / vol[fi]:.1f}% of new mortgage volume in {fm[fi]} "
            f"({S['invest_loans']['v'][fi]:,.0f} loans), against {100 * inv[fy] / vol[fy]:.1f}% a year earlier.", r2(100 * inv[fi] / vol[fi], 1), "% of volume",
            "invest_volume_k / volume_k", {f"flows.series.invest_volume_k.v[{fi}]": inv[fi], f"flows.series.volume_k.v[{fi}]": vol[fi],
                                           f"flows.series.invest_volume_k.v[{fy}]": inv[fy], f"flows.series.volume_k.v[{fy}]": vol[fy]}, fm[fi])
    rf = S["refi_volume_k"]["v"]
    if fy is not None:
        add("refi", f"Recycled (refinanced) housing loans reached {rf[fi] / 1e6:.2f} billion ILS in {fm[fi]} ({S['refi_loans']['v'][fi]:,.0f} loans), "
            f"{100 * (rf[fi] / rf[fy] - 1):+.0f}% on a year earlier; separately, {S['from_other_bank_volume_k']['v'][fi] / 1e6:.2f} billion ILS of new loans "
            f"were issued to repay a mortgage at another bank.", r2(rf[fi] / 1e6, 2), "billion ILS", "refi_volume_k / 1e6; change vs the same month a year earlier",
            {f"flows.series.refi_volume_k.v[{fi}]": rf[fi], f"flows.series.refi_volume_k.v[{fy}]": rf[fy], f"flows.series.from_other_bank_volume_k.v[{fi}]": S["from_other_bank_volume_k"]["v"][fi]}, fm[fi])
    # stock
    sm = st["months"]
    si = len(sm) - 1
    T = st["series"]
    tot, cnt, arr, gr = T["total_k"]["v"][si], T["count"]["v"][si], T["arrears90_k"]["v"][si], T["grace_k"]["v"][si]
    add("stock", f"Israelis owed the banks {tot / 1e6:.1f} billion ILS in {cnt:,.0f} housing loans at the end of {sm[si]} "
        f"(about {1000 * tot / cnt:,.0f} ILS per loan); {100 * arr / tot:.2f}% of it was 90 days or more past due and {100 * gr / tot:.1f}% was in a grace period.",
        r2(tot / 1e6, 1), "billion ILS", "total_k / 1e6; per loan = 1000 x total_k / count; arrears share = arrears90_k / total_k; grace share = grace_k / total_k",
        {f"stock.series.total_k.v[{si}]": tot, f"stock.series.count.v[{si}]": cnt, f"stock.series.arrears90_k.v[{si}]": arr, f"stock.series.grace_k.v[{si}]": gr}, sm[si])
    bs = st["by_size"]["balance_k"][si]
    add("stock_big", f"Loans with more than 2 million ILS still outstanding were {100 * (bs[4] + bs[5]) / sum(bs):.1f}% of the housing-loan book in {sm[si]}.",
        r2(100 * (bs[4] + bs[5]) / sum(bs), 1), "% of balance", "(balance 2-4M + balance 4M+) / sum of the 6 size bands", {f"stock.by_size.balance_k[{si}]": bs}, sm[si])
    # spreads over government yields
    E = ex["series"]
    rfix, mm = J["rates"]["fixed_nl"]["rate"], J["market"]["month"]
    g10 = dict(E["gov_nominal_10y"]["hist"]).get(mm)
    if g10 is not None:
        add("spread_fixed", f"The average fixed not-linked mortgage rate ({rfix:.2f}%, {mm}) was {rfix - g10:.2f} points above the 10-year "
            f"government zero-coupon yield in the same month ({g10:.2f}%).", r2(rfix - g10, 2), "percentage points",
            "rates.fixed_nl.rate - expect.series.gov_nominal_10y.hist[<market month>]", {"rates.fixed_nl.rate": rfix, f"expect.series.gov_nominal_10y.hist[{mm}]": g10}, mm)
    e1, f1 = E["exp_1y_capital_market"]["value"], J["forecast"].get("inflation_4q")
    add("inflation_exp", f"The capital market expects {e1:.2f}% inflation over the next year ({E['exp_1y_capital_market']['last']}); professional forecasters "
        f"{E['exp_1y_forecasters']['value']:.2f}%; the Bank of Israel Research forecast {f1}% (October 2026). CPI-linked balances grow with it.",
        r2(e1, 2), "%", "read directly", {"expect.series.exp_1y_capital_market.value": e1, "expect.series.exp_1y_forecasters.value": E["exp_1y_forecasters"]["value"],
                                          "forecast.inflation_4q": f1}, E["exp_1y_capital_market"]["last"])
    # homes x mortgage
    il4 = hm["medians"]["il"].get("r4") or {}
    pti_avg = S["pti_avg"]["v"][fi]
    if il4.get("median"):
        loan = 0.75 * il4["median"]
        p = mix_payment(li, loan, 25)[0]
        add("pay_median_4room", f"A 75% mortgage on the national median 4-room home sold in {il4['quarter']} ({il4['median']:,} ILS) costs about {p:,.0f} ILS a "
            f"month over 25 years at {m_last} average rates; at the market's average payment-to-income ratio ({pti_avg:.1f}%, {fm[fi]}) that takes about "
            f"{p / (pti_avg / 100):,.0f} ILS of household income a month.", round(p), "ILS/month",
            "loan = 0.75 x median; payment = system-mix payment as in pay_1m_25y scaled to the loan; income = payment / (pti_avg / 100)",
            {"homes.medians.il.r4.median": il4["median"], f"flows.series.pti_avg.v[{fi}]": pti_avg} | inp_mix(li), m_last)
    tlv = hm["medians"]["city"].get("תל אביב יפו") or {}
    if tlv.get("r4"):
        loan = 0.75 * tlv["r4"]["median"]
        p = mix_payment(li, loan, 25)[0]
        add("pay_tlv_4room", f"In Tel Aviv-Yafo the median 4-room home ({tlv['r4']['median']:,} ILS, {tlv['r4']['quarter']}) means a 75% mortgage of "
            f"{loan:,.0f} ILS and about {p:,.0f} ILS a month over 25 years.", round(p), "ILS/month", "as pay_median_4room with the Tel Aviv-Yafo median",
            {"homes.medians.city.תל אביב יפו.r4.median": tlv["r4"]["median"], "homes.payments.payment_per_1m": J["homes"]["payments"]["payment_per_1m"]}, m_last)
    fx = {b: bb["rate"][b]["fixed_nl"][li] for b in ["hapoalim", "leumi", "discount", "mizrahi", "fibi"]}
    flo, fhi = min(fx, key=fx.get), max(fx, key=fx.get)
    add("fixed_nl_by_bank", f"In {m_last} the average fixed not-linked rate on new mortgages ran from {fx[flo]:.2f}% at {nm[flo]} to {fx[fhi]:.2f}% at "
        f"{nm[fhi]} among the five largest banks (effective annual rates, bank reports to the Supervisor).", r2(fx[fhi] - fx[flo], 3), "percentage points",
        "max - min of by_bank.rate.<bank>.fixed_nl[last] over the five largest banks", {f"by_bank.rate.{b}.fixed_nl[{li}]": v for b, v in fx.items()}, m_last)
    # early repayment example from the bucket history
    nl = pp["nl"]
    cols = nl["cols"]
    org_m = months_back(24)
    org_rows = [r for r in nl["rows"] if r[0] <= org_m + "-28"]
    now_row = nl["rows"][-1]
    rate_org = None
    rr = fl["series"]["rate_fixed_nl"]["v"]
    if org_m in fl["months"]:
        rate_org = rr[fl["months"].index(org_m)]
    if org_rows and rate_org:
        org_row = org_rows[-1]
        N0, done = 300, 24
        pay = pmt(1_000_000, rate_org, N0)
        n_left = N0 - done
        bal = pv(pay, rate_org, n_left)
        yrs_left = n_left / 12
        bucket = "20_25" if 20 < yrs_left <= 25 else ("15_20" if 15 < yrs_left <= 20 else "gt25")
        avg_now = nom(now_row[cols.index(bucket)])
        avg_org = nom(org_row[cols.index(bucket)])
        fee33 = max(0.0, pv(pay, avg_now, n_left) - bal) if avg_now < rate_org else 0.0
        fee34 = max(0.0, pv(pay, avg_now, n_left) - pv(pay, avg_org, n_left)) if avg_org < rate_org else None
        fee = min(fee33, fee34) if fee34 is not None else fee33
        add("prepay_fee", f"A borrower who took 1,000,000 ILS fixed not-linked over 25 years in {org_m} at that month's average rate ({rate_org:.2f}%) and repays "
            f"in full now would owe about {fee:,.0f} ILS in capitalization fee on a balance of {bal:,.0f} ILS (no reduction before 3 years; "
            f"average rate for {yrs_left:.0f} years left: {now_row[cols.index(bucket)]:.2f}% effective, in force from {now_row[0]}).",
            round(fee), "ILS", "Banking Order s.3(3): PV(payments, avg_now) - balance; s.3(4): PV(payments, avg_now) - PV(payments, avg_at_origination); charged = lower; "
            "payments = PMT(1e6, rate_org, 300), 276 left; avg rates converted with nominal()", {
                f"flows.series.rate_fixed_nl.v[{fl['months'].index(org_m)}]": rate_org, "prepay.nl.rows[-1]": now_row, "prepay.nl.row_at_origination": org_row,
                "bucket": bucket}, now_row[0])
    return H


def city_payments(J):
    """'what a mortgage on the median home in city X costs this month': 75% LTV (the single-home cap), 25 years, the newest system-wide
    track mix and track rates of TamInt010; first payment, CPI-linked tracks at their real rate. Only published medians are used."""
    bb, hm = J["by_bank"], J["homes"]["medians"]
    li = len(bb["months"]) - 1
    trk = ["fixed_nl", "prime", "var_nl_other", "var_cpi", "fixed_cpi"]
    per_1m = sum(pmt(1_000_000 * bb["mix"]["system"][t][li] / 100, nom(bb["rate"]["system"][t][li]), 300) for t in trk)
    rows = {}
    for name, c in [("ישראל", hm["il"])] + sorted(hm["city"].items()):
        rows[name] = {k: {"median": v["median"], "quarter": v["quarter"], "loan": round(0.75 * v["median"]),
                          "payment": round(per_1m * 0.75 * v["median"] / 1_000_000)} for k, v in c.items() if v.get("median")}
    return {"ltv": 0.75, "years": 25, "mix_month": bb["months"][li], "payment_per_1m": round(per_1m, 2), "rows": rows,
            "formula": "payment = payment_per_1m x loan / 1,000,000; payment_per_1m = sum over tracks of PMT(1e6 x share/100, nominal(rate), 300) "
                       "with by_bank.mix.system and by_bank.rate.system of mix_month; loan = 0.75 x median (Tax Authority median closed-deal price, "
                       "3/4/5 rooms, newest published quarter of the last 22)"}


# ============================================================ fresh vs the live file
def freshness(new, old):
    def g(d, path):
        for k in path.split("."):
            d = d.get(k) if isinstance(d, dict) else None
        return d
    fields = ["market.month", "market.loans", "market.volume_k", "market.next_volume.month", "market.next_volume.volume_k", "rates.fixed_nl.rate",
              "rates.fixed_cpi.rate", "rates.var_cpi.rate", "policy.rate", "policy.prime", "policy.from", "policy.asof", "term.nl.inforce", "term.nl.month",
              "term.nl.avg_eff", "term.cpi.inforce", "term.cpi.avg_eff", "cpi.latest", "cpi.y12", "cpi.avg_m12", "forecast.published", "forecast.next_decision"]
    rows = [{"field": f, "live_2026_10_25": g(old, f), "now": g(new, f), "changed": g(old, f) != g(new, f)} for f in fields]
    return {"live_built": old.get("built"), "compared": rows, "changed": [r["field"] for r in rows if r["changed"]]}


def main():
    global CACHE
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "boi-mortgage-v2.json"))
    ap.add_argument("--cache", default=None, help="keep the raw downloads in this folder")
    a = ap.parse_args()
    if a.cache:
        CACHE = a.cache
        os.makedirs(CACHE, exist_ok=True)
    work = tempfile.mkdtemp(prefix="boim-v2-")
    tempfile.tempdir = work  # the live builder's own temp files (xls, json) land here and are removed at the end
    try:
        build(a)
    finally:
        tempfile.tempdir = None
        shutil.rmtree(work, ignore_errors=True)


def build(a):
    out = run_v1()
    old = json.load(open(LIVE_JSON, encoding="utf-8"))
    for key, fn in (("flows", build_flows), ("by_bank", build_by_bank), ("stock", build_stock), ("expect", build_expect),
                    ("homes", build_homes), ("prepay", build_prepay)):
        try:
            out[key] = fn()
        except Exception as e:
            fail(key, e)
            out[key] = None
    out["insurance"] = insurance_block()
    out["policy"]["next_decision_checked"] = {"date": "2026-11-23", "how": "boi.org.il home page header read in a browser on 5.11.2026 "
                                              "('מועד ההחלטה הבא: 23/11/2026', 'ריבית בנק ישראל 3.25%', 'אינפלציה 1.6%')"}
    try:
        out["homes"]["payments"] = city_payments(out)
    except Exception as e:
        fail("homes.payments", e)
    try:
        out["headlines"] = headlines(out)
    except Exception as e:
        fail("headlines", e)
        out["headlines"] = []
    out["fresh"] = freshness(out, old)
    new_src = [out[k]["src"] for k in ("flows", "by_bank", "stock", "expect") if out.get(k)]
    if out.get("homes"):
        new_src += [out["homes"]["hpi"]["src"], out["homes"]["medians"]["src"]]
    if out.get("prepay"):
        new_src += [out["prepay"]["nl"]["src"], out["prepay"]["cpi"]["src"], out["prepay"]["formula"]["src"]]
    out["sources_v2"] = new_src
    out["v2"] = {"built": NOW, "builder": "docs/research/2026-11-05-mortgage-world/data/build_mortgage_v2.py", "prototype": True,
                 "kept_keys": ["rates", "market", "policy", "term", "cpi", "forecast", "rules", "baskets", "fees", "tracks", "sources", "log"],
                 "new_keys": ["flows", "by_bank", "stock", "expect", "homes", "prepay", "insurance", "headlines", "fresh", "sources_v2", "fails", "log_v2"]}
    out["fails"] = FAILS
    out["log_v2"] = LOG
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("wrote", a.out, os.path.getsize(a.out), "bytes;", len(out["headlines"]), "headlines;", len(FAILS), "failures")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
