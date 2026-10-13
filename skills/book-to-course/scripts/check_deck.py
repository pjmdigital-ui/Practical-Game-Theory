#!/usr/bin/env python3
"""Check one Slides deck folder before publishing.

Usage:  python3 check_deck.py DECK_DIR [--files]
DECK_DIR holds project/deck.json and project/slides/<id>.html.

Reports: order/file mismatches, bad section starts, one <section> per file with
the right id, fonts under 24px, banned markup (margin, <style>, class=, em
sizes, CSS variables), multi-value gap, missing or oversized speaker notes,
plus writing stats: notes word counts and sentences with 2+ commas.
--files also prints the `files` map to pass to the Artifact publish call.
"""
import json
import re
import sys
from pathlib import Path

d = Path(sys.argv[1]) / "project"
deck = json.loads((d / "deck.json").read_text(encoding="utf-8"))
order = deck["order"]
files = {p.stem for p in (d / "slides").glob("*.html")}
probs, thin, commas = [], [], 0

if len(order) != len(set(order)):
    probs.append("duplicate ids in order")
if set(order) != files:
    probs.append(f"order/files mismatch: missing={sorted(set(order) - files)} extra={sorted(files - set(order))}")
for k, s in deck.get("sections", {}).items():
    if s.get("start") not in order:
        probs.append(f"section {k}: start {s.get('start')!r} not in order")

for sid in order:
    p = d / "slides" / f"{sid}.html"
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", sid):
        probs.append(f"{sid}: id must be lowercase a-z 0-9 -")
    if t.count("<section") != 1 or not re.search(rf'<section id="{re.escape(sid)}"', t):
        probs.append(f"{sid}: needs exactly one <section id=\"{sid}\">")
    markup = re.sub(r"<aside>.*?</aside>", "", t, flags=re.S)
    for m in re.findall(r"font-size:\s*(\d+)px", markup):
        if int(m) < 24:
            probs.append(f"{sid}: font-size {m}px (min 24)")
    for bad in ("margin", "<style", "class=", "em;", "var(", "%;font-size"):
        if bad in markup:
            probs.append(f"{sid}: contains {bad!r}")
    for g in re.findall(r"gap:\s*([^;\"]+)", markup):
        if len(g.split()) > 1:
            probs.append(f"{sid}: gap {g.strip()!r} takes one value")
    a = re.search(r"<aside>(.*?)</aside>\s*</section>", t, re.S)
    if not a:
        probs.append(f"{sid}: speaker notes <aside> missing or not the last child")
        continue
    notes = a.group(1)
    if len(notes) > 3500:
        probs.append(f"{sid}: notes {len(notes)} chars (max 3500)")
    words = len(notes.split())
    if words < 60 and not re.search(r"(^l\d+$|take$|^cover$|^carry$)", sid):
        thin.append(f"{sid} ({words} words)")
    text = re.sub(r"<[^>]+>", " ", markup) + " " + notes
    commas += sum(1 for s in re.split(r"[.!?]", text) if s.count(",") >= 2)

print(f"{len(order)} slides;", "structure OK" if not probs else "PROBLEMS:\n  " + "\n  ".join(probs))
if thin:
    print("Thin speaker notes (teaching slides want 180-350 words):", ", ".join(thin))
print(f"Sentences with 2+ commas: {commas} (aim for close to 0)")
if "--files" in sys.argv:
    print(json.dumps({f"project/slides/{s}.html": f"project/slides/{s}.html" for s in order}))
