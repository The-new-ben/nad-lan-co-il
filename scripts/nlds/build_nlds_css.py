# -*- coding: utf-8 -*-
"""Builds the site's copy of the NadLan design system (Claude Design artifact L9Nqz7Viv7K3MYeZrBc9s8):
plugins/nadlan-config/assets/nlds/nlds.css = the tokens (compiled from tokens.json, the way the artifact's page compiles
them) + the components' bundle.css, and assets/nlds/icons/ = the design system's icon files (Icons and Professions).

What the site needs that the artifact's previews do not (all found live on 24.9.2026):
- every token is namespaced (--nlds-*): the theme already defines --space-20 as 80px, which squeezed every card;
- the components are shielded from the theme: the theme forces its article typography on every h1-h3, p, span and a
  inside the page content, several of them with !important (".page .entry-content h3" sets 19-24px, Frank Ruhl and
  28px margins). So every component rule is scoped under ":root body .nlds" and every declaration carries !important:
  inside the design system the order between rules stays exactly as in the artifact, and the theme can no longer win;
- the artifact shows each component's phone layout inside a 375px preview frame (".nlds-phone X"). Here those rules
  become the real phone layout: "@media (max-width: 600px) { X }";
- the theme forces a font on every span, a and p; inside the design system they inherit again, like in the previews;
- BrokerFeatureCard keeps its buttons as a direct child of the card (the artifact's phone markup) on every screen, so
  one markup serves both layouts: on wide screens the buttons sit under the text, next to the portrait.

  python scripts/nlds/build_nlds_css.py <design-system project folder>
"""
import json, os, re, shutil, sys

SRC = sys.argv[1]
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(REPO, "plugins", "nadlan-config", "assets", "nlds")
OUT = os.path.join(OUT_DIR, "nlds.css")
P = "nlds-"
NL = chr(10)
SCOPE = ":root body "
PHONE = "@media (max-width: 600px)"

# ---- tokens ------------------------------------------------------------------------------------------------------
t = json.load(open(os.path.join(SRC, "tokens.json"), encoding="utf-8"))
first = t["color"]["themes"][0]["id"]
color_names = {x["name"] for x in t["color"]["tokens"]}
all_names = set(color_names)


def color_value(v):
    v = v.get(first) if isinstance(v, dict) else v
    if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
        ref = v[1:-1]
        return "var(--%s%s)" % (P, ref) if ref in color_names else None
    return v


lines = []
for x in t["color"]["tokens"]:
    v = color_value(x["value"])
    if v:
        lines.append("--%s%s:%s" % (P, x["name"], v))
for fam, data in t.items():
    if fam in ("color", "type", "name", "version", "meta") or not isinstance(data, dict) or "tokens" not in data:
        continue
    for x in data["tokens"]:
        v = x["value"].get(first) if isinstance(x["value"], dict) else x["value"]
        if isinstance(v, (int, float)):
            v = "%spx" % v
        all_names.add(x["name"])
        lines.append("--%s%s:%s" % (P, x["name"].replace(".", "\\."), v))
for key, stack in t["type"]["families"].items():
    all_names.add("font-" + key)
    lines.append("--%sfont-%s:%s" % (P, key, stack))
tokens = ":root{" + ";".join(lines) + "}"


# ---- a small CSS reader: top-level statements, nested @media kept as blocks -------------------------------------
def scan(css, i, stop):
    """Index of the first char in `stop` at depth 0 (outside strings and brackets), from i."""
    depth, q, n = 0, None, len(css)
    while i < n:
        c = css[i]
        if q:
            if c == "\\":
                i += 2
                continue
            if c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif depth == 0 and c in stop:
            return i
        i += 1
    return n


def statements(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    i, n, out = 0, len(css), []
    while i < n:
        while i < n and css[i].isspace():
            i += 1
        if i >= n:
            break
        j = scan(css, i, "{;")
        prelude = css[i:j].strip()
        if j >= n or css[j] == ";":
            out.append(("stmt", prelude, None))
            i = j + 1
            continue
        k, depth = j + 1, 1
        while k < n and depth:
            k2 = scan(css, k, "{}")
            if k2 >= n:
                k = n
                break
            depth += 1 if css[k2] == "{" else -1
            k = k2 + 1
        out.append(("block", prelude, css[j + 1:k - 1]))
        i = k
    return out


def split_top(s, sep):
    parts, i = [], 0
    while True:
        j = scan(s, i, sep)
        parts.append(s[i:j].strip())
        if j >= len(s):
            break
        i = j + 1
    return [x for x in parts if x]


def important(decls):
    out = []
    for d in split_top(decls, ";"):
        if ":" not in d:
            continue
        prop, val = d.split(":", 1)
        prop, val = prop.strip(), val.strip()
        if not prop.startswith("--") and not re.search(r"!\s*important$", val):
            val += " !important"
        out.append("%s:%s" % (prop, val))
    return ";".join(out)


WRAPPER = re.compile(r"^\.nlds(?![\w-])")
DROP = re.compile(r"^(html|body)\b|^\.nlds-(preview|note|row)(?![\w-])|^\.nlds-phone(--pad)?$")
PHONE_SEL = re.compile(r"^\.nlds-phone\s+")


def scoped(sel, reduced_motion=False):
    sel = sel.replace(":where(", ":is(")  # the reset keeps its place under component rules, above the theme's
    s = SCOPE + sel if WRAPPER.match(sel) else SCOPE + ".nlds " + sel
    if reduced_motion and s.endswith("*"):
        s += ":not(#nlds-rm)"  # "no motion" must beat every component's transition, whatever its specificity
    return s


def ns_vars(css):
    def ns(m):
        name = m.group(1)
        return "var(--%s%s" % (P, name) if name.replace("\\.", ".") in all_names else m.group(0)
    return re.sub(r"var\(--([A-Za-z0-9_.\\-]+)", ns, css)


def build(css, reduced_motion=False):
    body, phone = [], []
    for kind, prelude, inner in statements(css):
        if kind == "stmt":
            continue  # @import of the fonts (Skin A loads them) or @charset
        if prelude.startswith("@"):
            if re.match(r"@(media|supports)\b", prelude):
                b, ph = build(inner, reduced_motion or "prefers-reduced-motion" in prelude)
                if b:
                    body.append(prelude + "{" + b + "}")
                phone.extend(ph)
            else:
                body.append(prelude + "{" + inner.strip() + "}")  # @keyframes and the like stay as they are
            continue
        normal, small = [], []
        for sel in split_top(prelude, ","):
            if DROP.search(sel):
                continue
            if PHONE_SEL.match(sel):
                small.append(scoped(PHONE_SEL.sub("", sel)))
            else:
                normal.append(scoped(sel, reduced_motion))
        decl = important(inner)
        if normal:
            body.append(",".join(normal) + "{" + decl + "}")
        if small:
            phone.append(",".join(small) + "{" + decl + "}")
    return NL.join(body), phone


bundle = open(os.path.join(SRC, "components", "bundle.css"), encoding="utf-8").read()
comp, phone = build(ns_vars(bundle))

# ---- the site layer (same scope and weight as the components) ---------------------------------------------------
site = [
    # the previews run at the browser's 16px; the page content here runs at the theme's 18px
    (".nlds", "font-size:16px"),
    # the theme sets a font on every span, a, p (Skin A) and forces Frank Ruhl on headings: text inherits again
    (".nlds :is(p, a, span, b, strong, em, i, small, time, label, li)", "font-family:inherit"),
    # a grid item holding a wide photo keeps its track (the portrait column is 200px; the photo is 768px wide)
    (".nlds-bfeat__portrait", "min-width:0;width:100%"),
    # BrokerFeatureCard with its buttons as a direct child: portrait over two rows, buttons under the text
    (".nlds-bfeat:has(> .nlds-bfeat__cta)", "grid-template-rows:minmax(0, 1fr) auto;row-gap:var(--nlds-space-8)"),
    (".nlds-bfeat:has(> .nlds-bfeat__cta) > .nlds-bfeat__portrait", "grid-row:span 2"),
    (".nlds-bfeat > .nlds-bfeat__cta", "grid-column:2;margin-top:0"),
]
site_phone = [
    (".nlds-bfeat:has(> .nlds-bfeat__cta)", "grid-template-rows:none;row-gap:var(--nlds-space-14)"),
    (".nlds-bfeat:has(> .nlds-bfeat__cta) > .nlds-bfeat__portrait", "grid-row:auto;align-self:start"),
    (".nlds-bfeat > .nlds-bfeat__cta", "grid-column:1 / -1;padding-top:0"),
    # the artifact's phone card has no area chips (they stay on the broker's own page)
    (".nlds-bfeat .nlds-chips", "display:none"),
]
site_css = NL.join(scoped(s) + "{" + important(d) + "}" for s, d in site)
phone_css = NL.join(phone + [scoped(s) + "{" + important(d) + "}" for s, d in site_phone])

head = "/* NadLan design system for the site: tokens + components. Source: Claude Design artifact L9Nqz7Viv7K3MYeZrBc9s8." + NL
head += "   Built by scripts/nlds/build_nlds_css.py; do not edit by hand. Scoped under .nlds, shielded from the theme. */" + NL
out = head + tokens + NL + comp + NL + "/* site layer */" + NL + site_css + NL + "/* phone: the artifact's .nlds-phone rules */" + NL + PHONE + "{" + NL + phone_css + NL + "}" + NL
os.makedirs(OUT_DIR, exist_ok=True)
open(OUT, "w", encoding="utf-8", newline=NL).write(out)

# ---- icon files, as the components use them (<img src=".../icons/profession-broker.svg">) --------------------------
icons = os.path.join(OUT_DIR, "icons")
os.makedirs(icons, exist_ok=True)
copied = 0
for group in ("Icons", "Professions"):
    folder = os.path.join(SRC, "assets", group)
    for f in sorted(os.listdir(folder)):
        if f.endswith(".svg"):
            shutil.copyfile(os.path.join(folder, f), os.path.join(icons, f))
            copied += 1

left = sorted(set(re.findall(r"var\(--(?!nlds-)([a-z0-9-]+)", out)))
print("wrote", OUT, os.path.getsize(OUT), "bytes;", len(lines), "tokens;", len(phone), "phone rules;", copied, "icons; vars not namespaced:", left)
