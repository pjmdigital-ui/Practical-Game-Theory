#!/usr/bin/env python3
"""Build the printable extras: the worksheet pack and the three bonuses.

Outputs (in course/extras/):
  Internomics-Worksheet-Pack.pdf     the 13 module tools, one per section, ready to print
  Internomics-Bonus-1-Cheat-Sheet.pdf
  Internomics-Bonus-2-Situation-Diagnosis-Matrix.pdf
  Internomics-Bonus-3-Prep-System.pdf
  ...and an editable .docx next to each bonus.
Requires: pandoc, weasyprint.   Usage: python3 tools/build_extras.py
"""
import html
import re
import subprocess
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
COURSE = ROOT / "course"
OUT = COURSE / "extras"
OUT.mkdir(exist_ok=True)
BLANK = "______________________________"
TITLE, SUBTITLE, AUTHOR = "Internomics", "How to See the Game Behind Every Interaction", "Paul Mascetta"

BONUSES = [
    ("bonus-1-conversation-teardowns.md", "Internomics-Bonus-1-Conversation-Teardowns", "Bonus 1",
     "Conversation Teardowns"),
    ("bonus-2-ai-practice-partner.md", "Internomics-Bonus-2-AI-Practice-Partner-Pack", "Bonus 2",
     "The AI Practice Partner Pack"),
    ("bonus-3-field-playbooks.md", "Internomics-Bonus-3-Field-Playbooks", "Bonus 3", "The Field Playbooks"),
]

CSS = """
@page { size: letter; margin: 0.75in 0.8in 0.85in;
  @top-left { content: "INTERNOMICS · __KIND__"; font: 7.5pt 'Inter', sans-serif; letter-spacing: 1.2pt; color: #888; }
  @top-right { content: string(sec); font: 7.5pt 'Inter', sans-serif; letter-spacing: 1.2pt; color: #888; text-transform: uppercase; }
  @bottom-center { content: counter(page); font: 9pt 'Inter', sans-serif; color: #666; } }
@page cover { margin: 0; @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }
@page front { @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }
html { font: 10.5pt/1.5 'Bitstream Charter', Georgia, serif; color: #1b1b1b; }
body { margin: 0; }
p { margin: 0 0 0.6em; }
a { color: inherit; text-decoration: none; }
.cover { page: cover; height: 11in; background: #14213d; color: #fff; padding: 2.6in 0.9in 0; box-sizing: border-box; break-after: page; position: relative; }
.cover .k { font: 700 10pt 'Inter', sans-serif; letter-spacing: 3pt; text-transform: uppercase; color: #fca311; }
.cover .t { font: 800 38pt/1.08 'Inter Display', 'Inter', sans-serif; margin: 0.25in 0 0.25in; }
.cover .rule { width: 1.1in; border-top: 4pt solid #fca311; margin: 0 0 0.25in; }
.cover .s { font: italic 15pt/1.4 'Bitstream Charter', Georgia, serif; color: #e5e5e5; }
.cover .a { position: absolute; bottom: 0.9in; left: 0.9in; font: 600 11pt 'Inter', sans-serif; letter-spacing: 2pt; text-transform: uppercase; }
.toc { page: front; break-after: page; }
.toc h2 { font: 700 18pt 'Inter', sans-serif; margin: 0 0 0.3in; color: #14213d; }
.toc ul { list-style: none; padding: 0; margin: 0; }
.toc li { font-size: 11pt; line-height: 2.1; border-bottom: 0.5pt solid #e3e3e3; }
.toc li a::after { content: leader(' ') target-counter(attr(href), page); }
h1 { font: 800 22pt/1.15 'Inter Display', 'Inter', sans-serif; color: #14213d; margin: 0 0 0.2in; padding-bottom: 0.12in; border-bottom: 2pt solid #14213d; string-set: sec content(); }
h1.tool { break-before: page; string-set: sec attr(data-title); }
h1 .num { display: block; font: 700 8.5pt 'Inter', sans-serif; letter-spacing: 2.5pt; text-transform: uppercase; color: #b45309; margin-bottom: 6pt; }
h2 { font: 700 14pt/1.3 'Inter', sans-serif; color: #14213d; margin: 1.3em 0 0.5em; break-after: avoid; }
.bonus h2 { string-set: sec content(); }
h3 { font: 700 11pt/1.3 'Inter', sans-serif; margin: 1.1em 0 0.4em; break-after: avoid; }
.lead { font-size: 12pt; color: #333; background: #f3f4f7; border-left: 4pt solid #fca311; padding: 0.55em 0.9em; margin: 0 0 1em; }
blockquote { margin: 0.4em 0 0.8em; padding: 0.5em 0.9em; background: #f3f4f7; border-left: 4pt solid #fca311; font-size: 11pt; }
blockquote p { margin: 0; }
table { border-collapse: collapse; width: 100%; margin: 0.5em 0 1em; font-size: 9.3pt; }
th, td { border-bottom: 0.5pt solid #bbb; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { font-family: 'Inter', sans-serif; border-bottom: 1.2pt solid #14213d; background: #f3f4f7; }
tr { break-inside: avoid; }
thead th:empty { display: none; }
h3 + table { break-before: avoid; }
table.kv { break-inside: avoid; table-layout: fixed; }
table.kv td:first-child { width: 27%; font-family: 'Inter', sans-serif; font-size: 8.8pt; }
table.kv thead { display: none; }
table.who { table-layout: fixed; }
table.who th:first-child, table.who td:first-child { width: 11%; font-family: 'Inter', sans-serif; font-size: 8.8pt; }
table.who td:nth-child(2) { width: 42%; }
ul, ol { margin: 0.2em 0 0.7em; padding-left: 1.4em; }
li { margin-bottom: 0.25em; }
ul.task-list, ul:has(> li > input) { list-style: none; padding-left: 0.3em; }
.cb { display: inline-block; width: 8pt; height: 8pt; border: 0.8pt solid #555; margin-right: 6pt; vertical-align: -0.5pt; }
ul.task-list li { margin-bottom: 0.35em; }
.box { background: #fff8e8; border: 1pt solid #f2c86b; border-radius: 4pt; padding: 0.6em 0.9em; margin: 0.6em 0 1em; break-inside: avoid; }
.box > :last-child { margin-bottom: 0; }
.pagebreak { break-after: page; height: 0; }
.blank { display: block; height: 1.75em; border-bottom: 0.6pt solid #9a9a9a; }
.blank + .blank { margin-top: 0; }
pre { white-space: pre-wrap; background: #f3f4f7; border: 0.75pt solid #d6d9e0; border-left: 3pt solid #14213d;
  border-radius: 3pt; break-inside: avoid; padding: 0.6em 0.8em; font: 8.6pt/1.45 'DejaVu Sans Mono', monospace; margin: 0.4em 0 0.8em; }
pre code { font: inherit; }
h4 { font: 700 10.5pt/1.3 'Inter', sans-serif; color: #b45309; margin: 1em 0 0.3em; break-after: avoid; }
"""


def pandoc_html(md):
    return subprocess.run(["pandoc", "-f", "markdown-fancy_lists", "-t", "html5", "--wrap=none"],
                          input=md, capture_output=True, text=True, check=True).stdout


def normalize(md):
    md = re.sub(r"(?m)^(\*\*[^\n]*\*\*[^\n]*)\n(- )", r"\1\n\n\2", md)
    return md


def kv_tables(h):
    """Two-column label/value tables: narrow label column, kept on one page."""
    def fix(m):
        t = m.group(0)
        row = re.search(r"<tr[^>]*>(.*?)</tr>", t, re.S)
        if row and len(re.findall(r"<t[hd][ >]", row.group(1))) == 2:
            t = re.sub(r"<colgroup>.*?</colgroup>", "", t, flags=re.S)
            return t.replace("<table", '<table class="kv"', 1)
        return t
    return re.sub(r"<table.*?</table>", fix, h, flags=re.S)


def blanks(h):
    h = kv_tables(h)
    # WeasyPrint ignores <ol start>; carry the number through the list-item counter
    h = re.sub(r'<ol start="(\d+)"', lambda m: f'<ol style="counter-reset: list-item {int(m.group(1)) - 1}"', h)
    # dialogue tables: narrow "Who" column
    h = re.sub(r'<table>(\s*<colgroup>.*?</colgroup>)?(\s*<thead>\s*<tr[^>]*>\s*<th[^>]*>Who</th>)',
               lambda m: '<table class="who">' + m.group(2), h, flags=re.S)
    # a paragraph that is only an answer line becomes a ruled writing line
    h = re.sub(rf"<p>{BLANK}</p>", '<span class="blank"></span>', h)
    h = re.sub(r'<input type="checkbox"[^>]*/?>', '<span class="cb"></span>', h)
    h = re.sub(r'<label>(.*?)</label>', r'\1', h, flags=re.S)
    return h.replace(BLANK, '<span class="blank" style="display:inline-block;width:2.6in;height:1.1em"></span>')


def page(kind, cover_kicker, cover_title, body, toc=None):
    toc_html = ""
    if toc:
        items = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc)
        toc_html = f'<div class="toc"><h2>Contents</h2><ul>{items}</ul></div>'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{TITLE} — {html.escape(cover_title)}</title><style>{CSS.replace('__KIND__', kind)}</style></head><body>
<div class="cover"><div class="k">{html.escape(cover_kicker)}</div><div class="t">{html.escape(cover_title)}</div>
<div class="rule"></div><div class="s">{TITLE}: {SUBTITLE}</div><div class="a">{AUTHOR}</div></div>
{toc_html}{body}</body></html>"""


# ------------------------------------------------------------ worksheet pack
def worksheet_pack():
    parts, toc = [], []
    for path in sorted((COURSE / "modules").glob("module-*.md")):
        md = normalize(path.read_text(encoding="utf-8"))
        head = re.search(r"(?m)^# Module (\d+) — (.*)$", md)
        num, mod_title = head.group(1), head.group(2).strip()
        tool = re.search(r"(?ms)^## The tool: (.*?)$\n(.*?)(?=^## )", md)
        if not tool:
            continue
        name, text = tool.group(1).strip(), tool.group(2)
        q = re.search(r"(?m)^> \*\*The question:\*\*\s*(.*)$", md)
        ident = f"tool-{int(num):02d}"
        toc.append((ident, f"Module {num} · {name}"))
        text = re.sub(r"(?m)^### ", "## ", text)
        parts.append(
            f'<h1 class="tool" id="{ident}" data-title="{html.escape(name, quote=True)}"><span class="num">Module {num} · {html.escape(mod_title)}</span>'
            f'{html.escape(name)}</h1>'
            + (f'<p class="lead"><strong>The question:</strong> {html.escape(q.group(1).strip())}</p>' if q else "")
            + blanks(pandoc_html(text)))
    doc = page("WORKSHEETS", "The Worksheet Pack", "The 13 Internomics Tools", "\n".join(parts), toc)
    out = OUT / "Internomics-Worksheet-Pack.pdf"
    HTML(string=doc, base_url=str(COURSE)).write_pdf(out)
    print("wrote", out)


# ------------------------------------------------------------ bonuses
def bonus(src, stem, kicker, title):
    p = COURSE / "bonuses" / src
    if not p.exists():
        print("skip (missing)", p)
        return
    md = normalize(p.read_text(encoding="utf-8"))
    body = '<div class="bonus">' + blanks(pandoc_html(md)) + '</div>'
    doc = page(kicker.upper(), f"{kicker} · {TITLE}", title, body)
    out = OUT / f"{stem}.pdf"
    HTML(string=doc, base_url=str(COURSE)).write_pdf(out)
    print("wrote", out)
    docx_md = re.sub(r"(?ms)^::: \{\.pagebreak\}\n:::\n?", "", md)
    subprocess.run(["pandoc", "-f", "markdown", "-o", str(OUT / f"{stem}.docx")]
                   + (["--reference-doc", str(ROOT / "tools/reference-letter.docx")]
                      if (ROOT / "tools/reference-letter.docx").exists() else []),
                   input=docx_md, text=True, check=True)
    print("wrote", OUT / f"{stem}.docx")


if __name__ == "__main__":
    worksheet_pack()
    for b in BONUSES:
        bonus(*b)
