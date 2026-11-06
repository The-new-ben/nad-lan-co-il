"""Build php_hunks.json: exact [old, new] pairs that turn the repo's inc/near-finder.php (orig/, md5 df98425b...) into the edited
one. Each old string occurs exactly once in the original; applying them in order reproduces the edited file byte for byte."""
import difflib, hashlib, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
orig = (HERE / 'orig' / 'near-finder.php').read_text(encoding='utf-8')
new = (REPO / 'plugins' / 'nadlan-config' / 'inc' / 'near-finder.php').read_text(encoding='utf-8')
a, b = orig.splitlines(keepends=True), new.splitlines(keepends=True)
hunks = []
for grp in difflib.SequenceMatcher(None, a, b, autojunk=False).get_grouped_opcodes(1):
    i1, i2, j1, j2 = grp[0][1], grp[-1][2], grp[0][3], grp[-1][4]
    ctx = 0
    while True:  # widen until the old text is unique in the original
        lo, hi = max(0, i1 - ctx), min(len(a), i2 + ctx)
        old = ''.join(a[lo:hi])
        if orig.count(old) == 1:
            break
        ctx += 1
    nw = ''.join(a[lo:i1]) + ''.join(b[j1:j2]) + ''.join(a[i2:hi])
    hunks.append([old, nw])
out = orig
for old, nw in hunks:
    assert out.count(old) == 1, old[:80]
    out = out.replace(old, nw, 1)
assert out == new, 'hunks do not reproduce the edited file'
md5 = lambda s: hashlib.md5(s.encode('utf-8')).hexdigest()
doc = {'file': 'plugins/nadlan-config/inc/near-finder.php', 'base_md5_repo': md5(orig), 'result_md5': md5(new),
       'note': 'Apply in order; each old occurs once in the base. Owner 6.11.2026: no floating launcher; host per context; holder + dialog in wp_footer.',
       'hunks': hunks}
(HERE / 'php_hunks.json').write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(hunks), 'hunks', doc['base_md5_repo'], '->', doc['result_md5'])
