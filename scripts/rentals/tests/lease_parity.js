// Renders the same sample lease with assets/rentals/rm-lease.js (Node, no DOM)
const fs = require("fs"), path = require("path"), A = path.join(__dirname, "../../../plugins/nadlan-config/assets/rentals/");
global.window = global; global.addEventListener = () => {}; global.document = { getElementById: () => null, addEventListener: () => {}, documentElement: { classList: { add() {}, remove() {} } } };
eval(fs.readFileSync(A + "rm-core.js", "utf8")); eval(fs.readFileSync(A + "rm-lease.js", "utf8"));
const N = window.NLRM, lang = process.argv[3];
N.LEASE = JSON.parse(fs.readFileSync(A + "i18n/lease.json", "utf8"));
const ui = JSON.parse(fs.readFileSync(A + "i18n/" + lang + ".json", "utf8")).ui;
const lease = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const methods = {}; ["transfer", "standing", "cheque", "bit", "paybox", "cash", "card", "other"].forEach(k => methods[k] = (ui["m_" + k] || k).toLowerCase());
const en = lang === "en";
const doc = N.leaseDoc({ lease, unit: { id: 11, property_id: 1, label: en ? "Apt 7" : "דירה 7", floor: 3, rooms: 3, meta: { furnished: true, parking: false, storage: true } },
  property: { address: en ? "78 Arlozorov St" : "ארלוזורוב 78", city: en ? "Tel Aviv-Yafo" : "תל אביב-יפו" }, tenants: [{ name: en ? "The Levi family" : "משפחת לוי", idno: "" }],
  landlord: en ? "Dan Cohen" : "דני כהן", landlord_id: "", date: lease.created_at.slice(0, 10), methods }, lang);
process.stdout.write(JSON.stringify(doc));
