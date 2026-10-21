import io, re
p = r"C:\Users\777\nad-lan\nad-lan-co-il\docs\sales\kochav-ph\world\home.html"; s = io.open(p, encoding="utf-8").read()
R = [
("@media (max-width:760px){.btn{", "body.emb #top{padding-top:calc(env(safe-area-inset-top,0px) + 66px)}\n#furn{display:flex;border:1.5px solid var(--ink);background:var(--glass)}\n#furn button{font:600 13px inherit;font-family:inherit;border:0;background:none;padding:6px 12px;min-height:40px;cursor:pointer;color:var(--ink)}\n#furn button.on{background:var(--ink);color:#fff}\n@media (max-width:760px){.btn{"),
('<div id="acts"><button class="btn" id="vBtn" type="button"></button>', '<div id="acts"><div id="furn" hidden><button type="button" data-f="0" class="on"></button><button type="button" data-f="1"></button></div><button class="btn" id="vBtn" type="button"></button>'),
("  v: 'The view (real photo)',", "  f0: 'Furnished', f1: 'Empty (illustration)', v: 'The view (real photo)',"),
("  v: 'הנוף (צילום אמיתי)',", "  f0: 'עם ריהוט', f1: 'ללא ריהוט (הדמיה)', v: 'הנוף (צילום אמיתי)',"),
("$('vImg').alt = T.vcap;", "$('vImg').alt = T.vcap; $('furn').children[0].textContent = T.f0; $('furn').children[1].textContent = T.f1;\nconst EMPTY = new Set(['living', 'dining', 'terrace', 'entrance']); let empty = false;\nfor (const b of $('furn').children) b.onclick = () => { empty = b.dataset.f === '1'; for (const x of $('furn').children) x.classList.toggle('on', x === b); room.keep = true; room(cur).then(() => { room.keep = false; }); };"),
("  cur = id; for (const b of $('rooms').children) b.classList.toggle('on', b.dataset.id === id);\n  fadeT = 1; const t = await load(id);",
 "  cur = id; for (const b of $('rooms').children) b.classList.toggle('on', b.dataset.id === id);\n  $('furn').hidden = !EMPTY.has(id); const key = (empty && EMPTY.has(id)) ? id + '-empty' : id;\n  fadeT = 1; const t = await load(key);"),
("  const i = ROOMS.indexOf(id); if (ROOMS[i + 1]) load(ROOMS[i + 1]);", "  const i = ROOMS.indexOf(id); if (ROOMS[i + 1]) load(ROOMS[i + 1]); if (EMPTY.has(id)) load(empty ? id : id + '-empty');"),
("yaw = 0; pitch = -0.04;", "if (!room.keep) { yaw = 0; pitch = -0.04; }"),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]; s = s.replace(a, b, 1)
s, n = re.subn(r"(const EN = [^\n]*\n)", lambda m: m.group(1) + "if (window.self !== window.top) document.body.classList.add('emb');\n", s, count=1)
assert n == 1
io.open(p, "w", encoding="utf-8", newline="\n").write(s); print("patched")
