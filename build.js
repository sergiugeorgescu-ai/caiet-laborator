#!/usr/bin/env node
/* Generează paginile publicate din sursa unică din src/.
 *
 *   src/app.html                    aplicația (cu {{TITLE}}, {{IMG}}, {{LABS}})
 *   src/labs/<id>/lab.json          datele unei lucrări
 *   src/labs/<id>/img/<cheie>.webp  figurile lucrării (cheia = numele din ![..](cheie))
 *
 * Rulare:  node build.js          scrie index.html și lucrarea-N.html
 *          node build.js --check  doar verifică dacă paginile sunt la zi
 */
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const SRC = path.join(ROOT, "src");
const LABS = ["lucrarea-1", "lucrarea-2", "lucrarea-3", "lucrarea-4"];

const PAGES = [
  { file: "index.html", title: "Caiet de Laborator", labs: LABS },
  ...LABS.map((id, i) => ({ file: id + ".html", title: "Lucrarea " + (i + 1) + " · Caiet de Laborator", labs: [id] }))
];

const natural = (a, b) => a.localeCompare(b, "en", { numeric: true });

function loadLab(id) {
  const dir = path.join(SRC, "labs", id);
  const lab = JSON.parse(fs.readFileSync(path.join(dir, "lab.json"), "utf8"));
  if (lab.id !== id) throw new Error(dir + "/lab.json are id-ul " + JSON.stringify(lab.id));
  const imgDir = path.join(dir, "img");
  const img = {};
  if (fs.existsSync(imgDir)) {
    for (const f of fs.readdirSync(imgDir).filter(f => f.endsWith(".webp")).sort(natural)) {
      img[f.slice(0, -5)] = "data:image/webp;base64," + fs.readFileSync(path.join(imgDir, f)).toString("base64");
    }
  }
  return { lab, img };
}

function fill(template, key, value) {
  const token = "{{" + key + "}}";
  const parts = template.split(token);
  if (parts.length !== 2) throw new Error("src/app.html trebuie să conțină " + token + " exact o dată");
  return parts[0] + value + parts[1];
}

function render(template, page, labs) {
  const img = Object.assign({}, ...page.labs.map(id => labs[id].img));
  let out = fill(template, "TITLE", page.title);
  out = fill(out, "IMG", JSON.stringify(img));
  out = fill(out, "LABS", JSON.stringify(page.labs.map(id => labs[id].lab), null, 1));
  return out;
}

const check = process.argv.includes("--check");
const template = fs.readFileSync(path.join(SRC, "app.html"), "utf8");
const labs = {};
for (const id of LABS) labs[id] = loadLab(id);

let stale = 0;
for (const page of PAGES) {
  const out = render(template, page, labs);
  const file = path.join(ROOT, page.file);
  const cur = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : null;
  if (cur === out) { console.log("la zi   " + page.file); continue; }
  if (check) { stale++; console.log("DIFERĂ  " + page.file); continue; }
  fs.writeFileSync(file, out);
  console.log("scris   " + page.file);
}
if (stale) {
  console.error("\n" + stale + " pagini nu corespund sursei. Rulați: node build.js");
  process.exit(1);
}
