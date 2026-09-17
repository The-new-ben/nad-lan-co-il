#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply {json-path: new value} patches to the editorial and dossier sources.

Path syntax: dek.en | story.en[0] | features.en[0][1] | faq[2].a.en | seo.en.title
Every patch prints old -> new so the change is auditable; a path that does not exist is an error.
"""
import json, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/package/source"
TOK = re.compile(r"([^.\[\]]+)|\[(\d+)\]")

def parse(path):
    out = []
    for m in TOK.finditer(path):
        out.append(m.group(1) if m.group(1) is not None else int(m.group(2)))
    return out

def key_for(obj, k):
    # *_override blocks are objects keyed by digit strings; lists take integers
    if isinstance(obj, dict) and isinstance(k, int) and k not in obj:
        return str(k)
    if isinstance(obj, dict) and isinstance(k, str) and k not in obj and k.isdigit() and int(k) in obj:
        return int(k)
    return k

def dig(obj, keys):
    for k in keys:
        obj = obj[key_for(obj, k)]
    return obj

def apply_file(target, patches, dry=False):
    p = f"{BASE}/{target}"
    d = json.load(open(p, encoding="utf-8"))
    n = 0
    for path, new in patches.items():
        keys = parse(path)
        try:
            parent = dig(d, keys[:-1]); last = key_for(parent, keys[-1]); old = parent[last]
        except Exception as e:
            raise SystemExit(f"!! {target} {path}: {e}")
        if old == new:
            continue
        print(f"   {path}\n     -  {json.dumps(old, ensure_ascii=False)[:300]}\n     +  {json.dumps(new, ensure_ascii=False)[:300]}")
        parent[last] = new
        n += 1
    if not dry and n:
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"== {target}: {n} field(s) {'(dry)' if dry else 'written'}")
    return n

if __name__ == "__main__":
    dry = "--dry" in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    total = 0
    for f in files:
        spec = json.load(open(f, encoding="utf-8"))
        for target, patches in spec.items():
            total += apply_file(target, patches, dry)
    print("total", total)
