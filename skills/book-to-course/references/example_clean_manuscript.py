#!/usr/bin/env python3
"""Clean the raw ChatGPT manuscript into the canonical book manuscript.

What it does (no prose is rewritten):
  * removes duplicated chapter titles (Chapters 6-11 and the Conclusion)
  * removes the superseded first Conclusion draft and the stray ChatGPT
    reply that separated it from the final draft (archived separately)
  * normalizes heading levels:  # Chapter  /  ## Section  /  ### Sub-section
  * converts inline source links (with ?utm_source=chatgpt.com) into
    numbered footnotes with clean URLs
  * removes horizontal rules that sit directly before a heading
  * inserts Part I / II / III dividers from the book architecture

  * inserts the Introduction, which was written in the research dossier
    but never copied into the manuscript

Usage: python3 tools/clean_manuscript.py source/Game_Theory_original_manuscript.md \
           source/Game_Theory_Dossier.md book
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

src, dossier, outdir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
lines = src.read_text(encoding="utf-8").splitlines()

# ---------------------------------------------------------- introduction
dl = dossier.read_text(encoding="utf-8").splitlines()
i0 = dl.index("## **Introduction**")
i1 = next(i for i in range(i0, len(dl)) if dl[i].startswith("Yes. Now that the **11-model"))
intro = ["# Introduction {.chapter}"] + dl[i0 + 1:i1]


def plain(h):
    return re.sub(r"^#+\s*", "", h).replace("**", "").strip().rstrip(".")


# ---------------------------------------------------------------- conclusion
starts = [i for i, l in enumerate(lines) if l.startswith("# **Conclusion")]
chatter = next(i for i, l in enumerate(lines) if "Picking up exactly there" in l)
assert len(starts) == 3 and starts[1] < chatter < starts[2]
archived = lines[starts[1]:chatter]
(outdir / "archive").mkdir(parents=True, exist_ok=True)
(outdir / "archive" / "conclusion-first-draft-SUPERSEDED.md").write_text(
    "<!-- SUPERSEDED: first, unfinished draft of the Conclusion. It stopped at\n"
    "     'Act' and was replaced by the complete draft now in the manuscript.\n"
    "     Kept for reference only; do not treat as current. -->\n\n"
    + "\n".join(archived) + "\n",
    encoding="utf-8",
)
# drop the teaser heading, the superseded draft and the chatter line
lines = lines[:starts[0]] + lines[starts[2]:]

# ------------------------------------------------- duplicated chapter titles
out = []
i = 0
chapter_heads = [k for k, l in enumerate(lines) if re.match(r"# \*\*(Chapter \d+|Conclusion)", l)]
dup_first = set()
for a, b in zip(chapter_heads, chapter_heads[1:]):
    if plain(lines[a]) == plain(lines[b]):
        dup_first.add(a)
for k, l in enumerate(lines):
    if k in dup_first:
        between = [x for x in lines[k + 1:chapter_heads[chapter_heads.index(k) + 1]] if x.strip()]
        if between:
            # teaser before the real chapter opener: keep it as a lead-in line
            title = re.sub(r"^Chapter \d+ — ", "", plain(l))
            out.append(f"> **{title}.**")
        continue  # back-to-back duplicate: just drop it
    out.append(l)
lines = out

# ------------------------------------------------------------- footnotes
LINK = re.compile(r"\s*\(?\[([^\]]+)\]\((https?://[^)\s]+)\)\)?")


def clean_url(u):
    p = urlsplit(u)
    q = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
         if k != "utm_source" and not k.startswith("trk")]
    return urlunsplit((p.scheme, p.netloc, p.path, urlencode(q), p.fragment))


notes = []


def to_note(m):
    notes.append((m.group(1).strip(), clean_url(m.group(2))))
    return f"[^{len(notes)}]"


lines = [LINK.sub(to_note, l) for l in lines]

# ------------------------------------------------------------- headings
parts = {
    1: ("Part I", "See the Structure Beneath the Conversation"),
    6: ("Part II", "See What Isn't Obvious"),
    9: ("Part III", "Think Beyond the Moment"),
}
out = []
for l in lines:
    m = re.match(r"^(#{1,3})\s+(.*)$", l)
    if m:
        level, text = len(m.group(1)), plain(l)
        text = text.replace("\\", "")
        cm = re.match(r"Chapter (\d+) — (.*)", text)
        if cm:
            n = int(cm.group(1))
            if n in parts:
                p, t = parts[n]
                out += [f"# {p} — {t} {{.part}}", ""]
            out.append(f"# Chapter {n} — {cm.group(2)} {{.chapter}}")
        elif text.startswith("Conclusion"):
            out.append(f"# {text} {{.chapter}}")
        else:
            out.append(("##" if level < 3 else "###") + " " + text)
        continue
    # large pull-quote "headings" inside blockquotes -> bold pull-quotes
    l = re.sub(r"^>\s*#{1,6}\s+", "> ", l)
    out.append(l)
lines = out

# horizontal rule directly before a heading is redundant
out = []
for k, l in enumerate(lines):
    if l.strip() == "---":
        nxt = next((x for x in lines[k + 1:] if x.strip()), "")
        prv = next((x for x in reversed(out) if x.strip()), "")
        if nxt.startswith("#") or prv.startswith("#") or not prv:
            continue
    out.append(l)
lines = out

# collapse runs of blank lines
text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"

DEFINITION = """::: {.definition}
**in·ter·nom·ics** *(noun)*

The study of what happens between people.

Internomics applies the principles of game theory to communication and human interaction—not to teach you what to say, but to teach you how to understand the game you're already playing.
:::

"""

front = """---
title: "Internomics"
subtitle: "How to See the Game Behind Every Interaction"
author: "Paul Mascetta"
lang: en-US
---

"""
text = front + DEFINITION + "\n".join(intro).strip() + "\n\n" + text + "\n" + "\n".join(f"[^{n}]: {lab}, <{url}>" for n, (lab, url) in enumerate(notes, 1)) + "\n"
(outdir / "manuscript.md").write_text(text, encoding="utf-8")
print(f"chapters cleaned; {len(notes)} footnotes; archived {len(archived)} lines")
