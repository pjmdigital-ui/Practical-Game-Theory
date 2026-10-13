#!/usr/bin/env python3
"""Swap the reference deck's palette and fonts for a product's own brand.

Decks are always written in the reference palette (so every subagent copies the
same markup). Run this once per deck folder, after writing and before
publishing, to apply the product's colors and fonts.

Usage:  python3 rebrand_deck.py DECK_DIR project.json
project.json "deck" block (every key optional; missing keys keep the reference):
  "deck": {
    "colors": {"dark": "#14213D", "light": "#F6F4EE", "card": "#FFFDF8",
               "border": "#E2DED3", "panel": "#E9E5DA", "dark_panel": "#22325A",
               "accent": "#FCA311", "accent_text": "#B45309",
               "body": "#3B4252", "body_on_dark": "#C9D3E3",
               "muted": "#5B6577", "muted_on_dark": "#8FA0BC"},
    "heading_font": "Inter",            any Google Font family
    "body_font": "Source Serif 4"
  }
Keep contrast in mind: accent_text must be readable on light, body_on_dark on dark.
"""
import json
import re
import sys
from pathlib import Path

REF = {"dark": "#14213D", "light": "#F6F4EE", "card": "#FFFDF8", "border": "#E2DED3",
       "panel": "#E9E5DA", "dark_panel": "#22325A", "accent": "#FCA311",
       "accent_text": "#B45309", "body": "#3B4252", "body_on_dark": "#C9D3E3",
       "muted": "#5B6577", "muted_on_dark": "#8FA0BC"}

deck_dir = Path(sys.argv[1]) / "project"
cfg = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")).get("deck", {})
colors = cfg.get("colors", {})
swap = {REF[k].upper(): v for k, v in colors.items() if k in REF and v.upper() != REF[k].upper()}
hf, bf = cfg.get("heading_font"), cfg.get("body_font")

for p in (deck_dir / "slides").glob("*.html"):
    t = p.read_text(encoding="utf-8")
    t = re.sub(r"#[0-9A-Fa-f]{6}\b", lambda m: swap.get(m.group(0).upper(), m.group(0)), t)
    if hf and hf != "Inter":
        t = t.replace("font-family:Inter, Arial, sans-serif", f"font-family:'{hf}', Arial, sans-serif")
    if bf and bf != "Source Serif 4":
        t = t.replace("'Source Serif 4', Georgia, serif", f"'{bf}', Georgia, serif")
    p.write_text(t, encoding="utf-8")

deck_json = deck_dir / "deck.json"
deck = json.loads(deck_json.read_text(encoding="utf-8"))
faces = {}
for fam, wght in ((hf or "Inter", "400..800"), (bf or "Source Serif 4", "400..700")):
    key = re.sub(r"[^a-z0-9]+", "-", fam.lower()).strip("-")
    faces[key] = {"family": fam, "href": "https://fonts.googleapis.com/css2?family="
                  + fam.replace(" ", "+") + f":wght@{wght}&display=swap"}
deck["faces"] = faces
deck_json.write_text(json.dumps(deck, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"rebranded {deck_dir.parent}: {len(swap)} colors swapped; fonts {hf or 'Inter'} / {bf or 'Source Serif 4'}")
