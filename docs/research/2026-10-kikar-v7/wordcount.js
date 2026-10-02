// V7 (C3): net words of an article, counted the way Maya's breakthrough asks: inside the article only (no nav, forms, schema),
// with Intl.Segmenter isWordLike for the article's locale. Usage: node wordcount.js article-he.html he
// Prints JSON: {lang, words_all, words_without_lead, lead, sections: {id: words}}.
const fs = require("fs");
const [, , file, lang] = process.argv;
const html = fs.readFileSync(file, "utf8");
const seg = new Intl.Segmenter(lang, { granularity: "word" });
const text = (h) =>
  h.replace(/<(script|style)\b[\s\S]*?<\/\1>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;|&#160;/g, " ")
    .replace(/&[a-z#0-9]+;/gi, " ");
const count = (h) => {
  let n = 0;
  for (const s of seg.segment(text(h))) if (s.isWordLike) n++;
  return n;
};
const out = { lang, words_all: count(html), sections: {} };
const lead = (html.match(/^\s*<p>[\s\S]*?<\/p>/) || [""])[0];
out.lead = count(lead);
out.words_without_lead = out.words_all - out.lead;
const re = /<section[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/section>/g;
let m;
while ((m = re.exec(html))) out.sections[m[1]] = count(m[2]);
console.log(JSON.stringify(out));
