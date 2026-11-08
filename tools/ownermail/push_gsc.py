# -*- coding: utf-8 -*-
"""Push the daily Google Search Console totals of nad-lan.co.il to the site, for the owner's morning mail (HAD-687, OwnerMail v1).

The site cannot read Search Console by itself (the OAuth token stays on this computer), so once a day this script asks the existing
zero-dependency client tools/gsc/gsc_api.py for clicks and impressions per day (last 14 days, final data only) and POSTs them to
/wp-json/nadlan/v1/om-metrics (admin only, the WordPress application password the release runners use, decrypted here and never
printed). The morning mail shows Google rows only when a push arrived in the last 3 days: a computer that was off means no Google
row, never a guess.

Run:  python tools/ownermail/push_gsc.py            (prints the days pushed)
      python tools/ownermail/push_gsc.py --dry      (reads Search Console, sends nothing)
"""
import base64, csv, ctypes, ctypes.wintypes, json, os, subprocess, sys, tempfile, time, urllib.request
from datetime import date, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
URL = "https://nad-lan.co.il/wp-json/nadlan/v1/om-metrics"


class DB(ctypes.Structure):
    _fields_ = [("cb", ctypes.wintypes.DWORD), ("pb", ctypes.POINTER(ctypes.c_char))]


def dpapi(b64):
    raw = base64.b64decode(b64)
    bi = DB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
        raise RuntimeError("DPAPI")
    try:
        return ctypes.string_at(bo.pb, bo.cb).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pb)


def main():
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=14)
    out = os.path.join(tempfile.gettempdir(), "nadlan-om-gsc.csv")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "gsc", "gsc_api.py"), "query", "--site", "sc-domain:nad-lan.co.il",
                        "--start", start.isoformat(), "--end", end.isoformat(), "--dimensions", "date", "--out", out],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if r.returncode != 0:
        raise SystemExit("gsc_api.py failed: " + (r.stderr or r.stdout)[-400:])
    days = {}
    with open(out, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            days[row["date"]] = {"clicks": int(float(row["clicks"])), "impressions": int(float(row["impressions"]))}
    os.remove(out)
    if not days:
        raise SystemExit("Search Console returned no days")
    last = max(days)
    print("days", len(days), "| last", last, days[last])
    if "--dry" in sys.argv[1:]:
        return
    with open(SECRETS_PATH, encoding="utf-8-sig") as f:
        sec = json.load(f)
    auth = "Basic " + base64.b64encode((sec["username"] + ":" + dpapi(sec["password_dpapi"])).encode()).decode()
    req = urllib.request.Request(URL, data=json.dumps({"gsc": days}).encode(), method="POST",
                                 headers={"Authorization": auth, "Content-Type": "application/json", "User-Agent": "NadLan-OwnerMail-GSC/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        print("pushed:", resp.status, resp.read().decode("utf-8", "replace")[:200], time.strftime("%Y-%m-%d %H:%M"))


if __name__ == "__main__":
    main()
