#!/usr/bin/env python3
"""Build the print-ready PDF and the editable Word file from book/manuscript.md.

Requires: pandoc, weasyprint (pip install weasyprint)
Usage:    python3 tools/build_book.py
Outputs:  book/Practical-Game-Theory.pdf
          book/Practical-Game-Theory.docx
"""
import html
import re
import subprocess
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
MD = BOOK / "manuscript.md"
TITLE = "Practical Game Theory"
SUBTITLE = "See the Game Behind the Conversation"
AUTHOR = "Paul Mascetta"
YEAR = "2026"


def pandoc(*args, stdin=None):
    return subprocess.run(["pandoc", *args], input=stdin, capture_output=True,
                          text=True, check=True).stdout


# ------------------------------------------------------------------ HTML body
body = pandoc(str(MD), "-f", "markdown", "-t", "html5", "--wrap=none")

# Move each footnote's text to its reference point so WeasyPrint can float it
# to the bottom of the page (float: footnote).
notes = {}
fn_section = re.search(r'<(?:section|aside)[^>]*id="footnotes".*?</(?:section|aside)>', body, re.S)
if fn_section:
    for m in re.finditer(r'<li id="(fn\d+)">(.*?)</li>', fn_section.group(0), re.S):
        txt = re.sub(r'<a href="#fnref\d+"[^>]*>.*?</a>', "", m.group(2), flags=re.S)
        txt = re.sub(r"</?p>", "", txt).strip()
        notes[m.group(1)] = txt
    body = body.replace(fn_section.group(0), "")
body = re.sub(
    r'<a href="#(fn\d+)" class="footnote-ref" id="fnref\d+"[^>]*><sup>\d+</sup></a>',
    lambda m: f'<span class="fn">{notes[m.group(1)]}</span>', body)

# Table of contents: parts, chapters and conclusion with live page numbers.
toc = []
for m in re.finditer(r'<h1 class="(part|chapter)" id="([^"]+)">(.*?)</h1>', body):
    kind, ident, label = m.groups()
    toc.append(f'<li class="toc-{kind}"><a href="#{ident}">{label}</a></li>')

# Split "Chapter 3 — Think in Responses" into a label and a title line.
def chapter_head(m):
    kind, ident, label = m.groups()
    if " — " in label:
        num, title = label.split(" — ", 1)
    else:
        num, title = "", label
    return (f'<h1 id="{ident}" class="{kind}" data-title="{html.escape(title, quote=True)}">'
            f'<span class="num">{num}</span><span class="ttl">{title}</span></h1>')


body = re.sub(r'<h1 class="(part|chapter)" id="([^"]+)">(.*?)</h1>', chapter_head, body)

CSS = """
@page {
  size: 6in 9in;
  margin: 0.85in 0.7in 0.85in 0.8in;
  @bottom-center { content: counter(page); font: 9pt 'Inter', sans-serif; color: #555; }
}
@page :left  { margin-left: 0.7in; margin-right: 0.8in;
  @top-left  { content: "PRACTICAL GAME THEORY"; font: 7.5pt 'Inter', sans-serif; letter-spacing: 1.5pt; color: #777; } }
@page :right {
  @top-right { content: string(chap); font: 7.5pt 'Inter', sans-serif; letter-spacing: 1.5pt; color: #777; text-transform: uppercase; } }
@page front { @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }
@page front-num { @top-left { content: none; } @top-right { content: none; }
  @bottom-center { content: none; } }
@page opener { @top-left { content: none; } @top-right { content: none; } }
@page part { @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }
@page :blank { @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }

html { font-family: 'Bitstream Charter', 'Charter', Georgia, serif; font-size: 10.5pt; line-height: 1.5; color: #1b1b1b; hyphens: auto; }
body { margin: 0; }
p { margin: 0 0 0.6em; text-align: justify; orphans: 2; widows: 2; }
strong { font-weight: bold; }
a { color: inherit; text-decoration: none; }

.front { page: front; break-after: right; }
.front-num { page: front-num; }
.title-page { text-align: center; padding-top: 1.6in; }
.title-page .t { font: 800 30pt/1.1 'Inter Display', 'Inter', sans-serif; letter-spacing: -0.5pt; }
.title-page .rule { width: 1in; border-top: 2pt solid #1b1b1b; margin: 0.3in auto; }
.title-page .s { font-style: italic; font-size: 14pt; color: #444; }
.title-page .a { margin-top: 2.4in; font: 600 12pt 'Inter', sans-serif; letter-spacing: 2pt; text-transform: uppercase; }
.copyright { padding-top: 4.4in; font-size: 8pt; line-height: 1.55; color: #333; }
.copyright p { text-align: left; margin-bottom: 0.7em; }

.toc h2 { font: 700 16pt 'Inter', sans-serif; margin: 0.4in 0 0.3in; text-align: left; }
.toc ul { list-style: none; padding: 0; margin: 0; }
.toc li a::after { content: leader('.') target-counter(attr(href), page); }
.toc li { margin: 0; }
.toc-part { font: 700 8pt 'Inter', sans-serif; letter-spacing: 1.5pt; text-transform: uppercase; color: #666; margin-top: 1.1em !important; margin-bottom: 0.35em !important; }
.toc-part a::after { content: none !important; }
.toc-chapter { font-size: 10.5pt; line-height: 1.9; }

h1.part { page: part; break-before: right; break-after: page; text-align: center; padding-top: 2.4in; }
h1.part .num { display: block; font: 700 9pt 'Inter', sans-serif; letter-spacing: 3pt; text-transform: uppercase; color: #777; margin-bottom: 0.25in; }
h1.part .ttl { display: block; font: 800 20pt/1.2 'Inter Display', 'Inter', sans-serif; }
h1.chapter { page: opener; break-before: right; string-set: chap attr(data-title); padding-top: 1.3in; margin: 0 0 0.45in; }
h1.chapter .num { display: block; font: 700 9pt 'Inter', sans-serif; letter-spacing: 3pt; text-transform: uppercase; color: #777; margin-bottom: 0.18in; }
h1.chapter .ttl { display: block; font: 800 22pt/1.15 'Inter Display', 'Inter', sans-serif; letter-spacing: -0.3pt; padding-bottom: 0.2in; border-bottom: 1.5pt solid #1b1b1b; }
h2 { font: 700 12.5pt/1.3 'Inter', sans-serif; margin: 1.6em 0 0.6em; break-after: avoid; text-align: left; }
h3 { font: 700 10.5pt/1.3 'Inter', sans-serif; margin: 1.2em 0 0.4em; break-after: avoid; text-transform: none; color: #333; }
blockquote { margin: 0.3em 0 0.3em 1.6em; padding: 0; break-inside: avoid; }
blockquote + blockquote { margin-top: -0.25em; }
blockquote p { text-align: left; margin-bottom: 0.3em; }
ul, ol { margin: 0.2em 0 0.7em 0; padding-left: 1.4em; }
li { margin-bottom: 0.2em; }
hr { border: 0; text-align: center; margin: 1.2em 0; height: 1em; }
hr::after { content: "\\2022\\2003\\2022\\2003\\2022"; font-size: 8pt; color: #888; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; margin: 0.6em 0 1em; }
th, td { border-bottom: 0.5pt solid #aaa; padding: 3pt 4pt; text-align: left; vertical-align: top; }
th { font-family: 'Inter', sans-serif; font-weight: 700; border-bottom: 1pt solid #1b1b1b; }

.fn { float: footnote; font-size: 7pt; line-height: 1.35; text-align: left; hyphens: none; word-break: break-all; }
.fn::footnote-call { content: counter(footnote); font-size: 6.5pt; vertical-align: super; line-height: 0; }
.fn::footnote-marker { content: counter(footnote) ". "; }
@page { @footnote { border-top: 0.5pt solid #999; padding-top: 4pt; margin-top: 8pt; } }
"""

toc_html = "\n".join(toc)
doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{TITLE}</title><style>{CSS}</style></head><body>
<div class="front"><div class="title-page">
  <div class="t">{TITLE}</div><div class="rule"></div>
  <div class="s">{SUBTITLE}</div>
  <div class="a">{AUTHOR}</div></div></div>
<div class="front" style="break-after: page"><div class="copyright">
  <p><strong>{TITLE}</strong><br>{SUBTITLE}</p>
  <p>Copyright &copy; {YEAR} {AUTHOR}. All rights reserved.</p>
  <p>No part of this book may be reproduced, stored in a retrieval system, or transmitted in any form or by any
  means&mdash;electronic, mechanical, photocopying, recording, or otherwise&mdash;without the prior written
  permission of the author, except for brief quotations in reviews and articles.</p>
  <p>This book is intended for educational purposes. The examples are illustrations, not guarantees of outcome,
  and nothing in it constitutes legal, financial, or psychological advice.</p>
  <p>First edition</p></div></div>
<div class="front-num toc"><h2>Contents</h2><ul>{toc_html}</ul></div>
<main>{body}</main>
</body></html>"""

(BOOK / "build").mkdir(exist_ok=True)
(BOOK / "build" / "book.html").write_text(doc, encoding="utf-8")
pdf = BOOK / "Practical-Game-Theory.pdf"
HTML(string=doc, base_url=str(BOOK)).write_pdf(pdf)
print("wrote", pdf)

# ------------------------------------------------------------------ DOCX
ref = ROOT / "tools" / "reference.docx"
args = [str(MD), "-o", str(BOOK / "Practical-Game-Theory.docx"), "--toc", "--toc-depth=1",
        "-M", "toc-title=Contents"]
if ref.exists():
    args += ["--reference-doc", str(ref)]
pandoc(*args)
print("wrote", BOOK / "Practical-Game-Theory.docx")

# Fill in the Word table of contents so it shows page numbers on first open.
subprocess.run(["python3", str(ROOT / "tools" / "update_docx_toc.py"),
                str(BOOK / "Practical-Game-Theory.docx")], check=True)
