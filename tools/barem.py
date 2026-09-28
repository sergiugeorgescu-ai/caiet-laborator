#!/usr/bin/env python3
"""Scoate baremul din paginile publice sau îl pune la loc.

  python3 tools/barem.py scoate [--fara-punctaj] ../barem-lucrari.json index.html lucrarea-*.html
      Mută răspunsurile corecte, formulele, toleranțele, rezolvările și
      răspunsurile-model din lista BUILTIN a fiecărei pagini în fișierul de
      barem (îl completează dacă există). Paginile rămân cu enunțurile și cu
      o cheie de punctare codificată (`k`): la lucrările cu autoevaluare,
      studentul își vede punctajul total, dar nu și care răspunsuri sunt
      corecte. Cu --fara-punctaj, cheia nu se pune deloc și autoevaluarea
      se oprește (pentru lucrări notate).

  python3 tools/barem.py pune ../barem-lucrari.json index.html lucrarea-*.html
      Operația inversă: reface paginile complete, pentru lucru local.

Fișierul de barem nu se pune niciodată în depozit: depozitul este public.
Profesorul îl încarcă o dată în aplicație, din Laboratoare → Importă….
"""
import base64
import json
import os
import sys

START = "const BUILTIN = "
END = "\n];\n"
KEYS = ("correct", "expr", "tolPct", "tolAbs", "solution", "explain", "model")
SCORING = ("correct", "expr", "tolPct", "tolAbs")


def encode_key(lab_id, keys):
    """Aceeași codificare ca scoringLab() din pagină."""
    b = bytearray(json.dumps(keys, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    for i in range(len(b)):
        b[i] ^= (ord(lab_id[i % len(lab_id)]) + i * 31) & 255
    return base64.b64encode(bytes(b)).decode("ascii")


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


def scoate(barem_path, pages, cu_punctaj=True):
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
            scoring = {}
            for q in lab.get("questions", []):
                keys = {k: q.pop(k) for k in KEYS if k in q}
                if keys:
                    entry["questions"][q["id"]] = keys
                    n += 1
                sk = {k: keys[k] for k in SCORING if k in keys}
                if sk:
                    scoring[q["id"]] = sk
            if cu_punctaj and lab.get("selfCheck") and scoring:
                lab["scoreOnly"] = True
                lab["k"] = encode_key(lab["id"], scoring)
            else:
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
            for k in ("stripped", "scoreOnly", "k"):
                lab.pop(k, None)
        write_page(page, head, labs, tail)
        print(f"{page}: barem pus la loc")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--fara-punctaj"]
    if len(args) < 3 or args[0] not in ("scoate", "pune"):
        sys.exit(__doc__)
    if args[0] == "scoate":
        scoate(args[1], args[2:], cu_punctaj="--fara-punctaj" not in sys.argv)
    else:
        pune(args[1], args[2:])
