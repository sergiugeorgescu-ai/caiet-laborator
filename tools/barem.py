#!/usr/bin/env python3
"""Scoate baremul din paginile publice sau îl pune la loc.

  python3 tools/barem.py scoate ../barem-lucrari.json index.html lucrarea-*.html
      Mută răspunsurile corecte, formulele, toleranțele, rezolvările și
      răspunsurile-model din lista BUILTIN a fiecărei pagini în fișierul de
      barem (îl completează dacă există). Paginile rămân doar cu enunțurile,
      iar autoevaluarea se oprește.

  python3 tools/barem.py pune ../barem-lucrari.json index.html lucrarea-*.html
      Operația inversă: reface paginile complete, pentru lucru local.

Fișierul de barem nu se pune niciodată în depozit: depozitul este public.
Profesorul îl încarcă o dată în aplicație, din Laboratoare → Importă….
"""
import json
import os
import sys

START = "const BUILTIN = "
END = "\n];\n"
KEYS = ("correct", "expr", "tolPct", "tolAbs", "solution", "explain", "model")


def split_page(src):
    a = src.index(START) + len(START)
    b = src.index(END, a) + 2
    return src[:a], json.loads(src[a:b]), src[b:]


def write_page(path, head, labs, tail):
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + json.dumps(labs, indent=1, ensure_ascii=False) + tail)


def load_barem(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"caietBarem": 1, "labs": {}}


def scoate(barem_path, pages):
    barem = load_barem(barem_path)
    for page in pages:
        with open(page, encoding="utf-8") as f:
            head, labs, tail = split_page(f.read())
        n = 0
        for lab in labs:
            if lab.get("stripped"):
                continue
            entry = barem["labs"].setdefault(lab["id"], {"questions": {}})
            entry["selfCheck"] = bool(lab.get("selfCheck"))
            for q in lab.get("questions", []):
                keys = {k: q.pop(k) for k in KEYS if k in q}
                if keys:
                    entry["questions"][q["id"]] = keys
                    n += 1
            lab["selfCheck"] = False
            lab["stripped"] = True
        write_page(page, head, labs, tail)
        print(f"{page}: {n} întrebări fără barem")
    with open(barem_path, "w", encoding="utf-8") as f:
        json.dump(barem, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"barem salvat în {barem_path}")


def pune(barem_path, pages):
    barem = load_barem(barem_path)
    for page in pages:
        with open(page, encoding="utf-8") as f:
            head, labs, tail = split_page(f.read())
        for lab in labs:
            entry = barem["labs"].get(lab["id"])
            if not entry or not lab.get("stripped"):
                continue
            for q in lab.get("questions", []):
                q.update(entry["questions"].get(q["id"], {}))
            lab["selfCheck"] = entry.get("selfCheck", False)
            del lab["stripped"]
        write_page(page, head, labs, tail)
        print(f"{page}: barem pus la loc")


if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] not in ("scoate", "pune"):
        sys.exit(__doc__)
    {"scoate": scoate, "pune": pune}[sys.argv[1]](sys.argv[2], sys.argv[3:])
