# Builds the artifact copy (site/): the page without its own document skeleton (the artifact host adds one), plus the data and
# the textures it loads. The raw generations and the generator stay out.
import io, os, re, shutil
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, "site")
os.makedirs(os.path.join(S, "tex"), exist_ok=True)
s = io.open(os.path.join(H, "index.html"), encoding="utf-8").read()
s = re.sub(r"<!doctype html>\s*<html[^>]*>\s*<head>\s*", "", s, count=1, flags=re.I)
s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">', '<meta name="claude:viewport-fit-sides" content="cover">\n<meta name="robots" content="noindex">', 1)
s = re.sub(r"</head>\s*<body>", "", s, count=1); s = re.sub(r"</body>\s*</html>\s*$", "", s)
s = s.replace('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n', "", 1)
io.open(os.path.join(S, "index.html"), "w", encoding="utf-8", newline="\n").write(s)
for f in ("city.json", "places.json", "quarter.json", "building.json", "view-11.jpg"): shutil.copy(os.path.join(H, f), os.path.join(S, f))
for f in os.listdir(os.path.join(H, "tex")):
    if f.endswith((".jpg", ".png")) and "_raw" not in f: shutil.copy(os.path.join(H, "tex", f), os.path.join(S, "tex", f))
print(sorted(os.listdir(S)), sorted(os.listdir(os.path.join(S, "tex"))))
