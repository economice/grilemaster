#!/usr/bin/env python3
"""Regenereaza quiz_master.html din JSON-urile de admitere master. Ruleaza: python3 build_quiz_master.py"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
NAMES = {
    "ro": "tematica_master_romana.json",
    "en": "tematica_master_engleza.json",
}

data = {}
for lang, fname in NAMES.items():
    with open(os.path.join(BASE, fname), encoding="utf-8") as fh:
        d = json.load(fh)
    bad = [q.get("numar") for q in d
           if sorted(q.get("raspunsuri", {}).keys()) != ["A", "B", "C", "D"]
           or not q.get("raspuns_corect") or not q.get("intrebare")]
    if bad:
        raise SystemExit(f"{fname}: intrebari incomplete la nr {bad}")
    data[lang] = d
    print(f"{fname}: {len(d)} intrebari ok")

with open(os.path.join(BASE, "quiz_master_template.html"), encoding="utf-8") as fh:
    tpl = fh.read()
html = tpl.replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False))
if html == tpl:
    raise SystemExit("marker /*__DATA__*/ lipseste din quiz_master_template.html")
with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as fh:
    fh.write(html)
print(f"index.html regenerat ({len(html)} bytes)")
