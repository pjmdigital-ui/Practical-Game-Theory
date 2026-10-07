#!/usr/bin/env python3
"""Build the course PDFs from course/modules/*.md.

Outputs:
  course/Internomics-Course-Guide.pdf      every module, with answers
  course/Internomics-Student-Workbook.pdf  worksheets, exercises, quizzes,
                                                     field assignments, no answers
Requires: pandoc, weasyprint.   Usage: python3 tools/build_course.py
"""
import html
import re
import subprocess
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
COURSE = ROOT / "course"
MODULES = sorted((COURSE / "modules").glob("module-*.md"))
WORKBOOK_SECTIONS = ("The tool", "Practice exercises", "Quiz", "Field assignment",
                     "Capstone project", "The question to carry")
BLANK = "______________________________"


def normalize(md):
    """Small fixes so pandoc reads the modules the way they read on GitHub."""
    # a list directly under a bold label needs a blank line before it
    md = re.sub(r"(?m)^(\*\*[^\n]*\*\*[^\n]*)\n(- )", r"\1\n\n\2", md)
    # "**On-screen takeaway:** > **...**" -> no stray ">"
    md = re.sub(r"(\*\*On-screen takeaway:\*\*)\s*>\s*", r"\1 ", md)
    return md


def md_to_html(md):
    return subprocess.run(["pandoc", "-f", "markdown-fancy_lists", "-t", "html5", "--wrap=none"],
                          input=md, capture_output=True, text=True, check=True).stdout


def details_to_div(md, keep):
    """<details><summary>X</summary> ... </details>  ->  answer box, or removed."""
    pat = re.compile(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", re.S)
    if keep:
        return pat.sub(lambda m: f"\n::: {{.answer}}\n**{m.group(1).strip()}**\n\n{m.group(2).strip()}\n:::\n", md)
    return pat.sub("", md)


def sections(md):
    """Split a module into (preamble, [(h2 title, text), ...])."""
    parts = re.split(r"(?m)^## ", md)
    out = []
    for p in parts[1:]:
        title = p.split("\n", 1)[0].strip()
        out.append((title, "## " + p))
    return parts[0], out


def module_md(path, workbook):
    md = normalize(path.read_text(encoding="utf-8"))
    md = details_to_div(md, keep=not workbook)
    if workbook:
        pre, secs = sections(md)
        # keep the title, the module question and the selected sections
        title = re.search(r"(?m)^# .*$", pre).group(0)
        q = re.search(r"(?m)^> \*\*The question:\*\*.*$", pre)
        body = [title, "", q.group(0) if q else ""]
        body += [t for name, t in secs if name.startswith(WORKBOOK_SECTIONS)]
        md = "\n\n".join(body)
        # the quiz in the workbook gets an answer line instead of a key
        md = md.replace(BLANK, "<span class=\"blank\"></span><span class=\"blank\"></span>")
        md += "\n\n## My notes\n\n" + "<span class=\"blank\"></span>" * 8 + "\n"
    else:
        md = md.replace(BLANK, "<span class=\"blank\"></span>")
    md = re.sub(r"(?m)^# (.*)$", lambda m: f"# {m.group(1)} {{.module}}", md, count=1)
    return md


CSS = """
@page { size: letter; margin: 0.8in 0.85in 0.9in;
  @top-right { content: string(mod); font: 7.5pt 'Inter', sans-serif; letter-spacing: 1.2pt; color: #888; text-transform: uppercase; }
  @top-left { content: "INTERNOMICS · __KIND__"; font: 7.5pt 'Inter', sans-serif; letter-spacing: 1.2pt; color: #888; }
  @bottom-center { content: counter(page); font: 9pt 'Inter', sans-serif; color: #666; } }
@page cover { margin: 0; @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }
@page front { @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }
html { font: 10.5pt/1.5 'Bitstream Charter', Georgia, serif; color: #1b1b1b; }
body { margin: 0; }
p { margin: 0 0 0.6em; }
a { color: inherit; text-decoration: none; }
.cover { page: cover; height: 11in; background: #14213d; color: #fff; padding: 2.6in 0.9in 0; box-sizing: border-box; break-after: page; }
.cover .k { font: 700 10pt 'Inter', sans-serif; letter-spacing: 3pt; text-transform: uppercase; color: #fca311; }
.cover .t { font: 800 40pt/1.05 'Inter Display', 'Inter', sans-serif; margin: 0.25in 0 0.2in; }
.cover .s { font: italic 15pt 'Bitstream Charter', Georgia, serif; color: #e5e5e5; }
.cover .a { position: absolute; bottom: 0.9in; font: 600 11pt 'Inter', sans-serif; letter-spacing: 2pt; text-transform: uppercase; }
.toc { page: front; break-after: page; }
.toc h2 { font: 700 18pt 'Inter', sans-serif; margin: 0 0 0.3in; }
.toc ul { list-style: none; padding: 0; margin: 0; }
.toc li { font-size: 11pt; line-height: 2.1; border-bottom: 0.5pt solid #e3e3e3; }
.toc li a::after { content: leader(' ') target-counter(attr(href), page); }
h1.module { break-before: page; string-set: mod attr(data-short); font: 800 24pt/1.15 'Inter Display', 'Inter', sans-serif;
  margin: 0 0 0.25in; padding-bottom: 0.15in; border-bottom: 2pt solid #14213d; }
h2 { font: 700 14pt/1.3 'Inter', sans-serif; color: #14213d; margin: 1.5em 0 0.5em; break-after: avoid; }
h3 { font: 700 11pt/1.3 'Inter', sans-serif; margin: 1.2em 0 0.4em; break-after: avoid; }
h1.module + blockquote { background: #f3f4f7; border-left: 4pt solid #fca311; margin: 0 0 1em; padding: 0.6em 0.9em; font-size: 12pt; }
blockquote { margin: 0.4em 0 0.6em 1.2em; padding-left: 0.8em; border-left: 2pt solid #ccc; }
blockquote p { margin: 0; }
table { border-collapse: collapse; width: 100%; margin: 0.6em 0 1em; font-size: 9.5pt; break-inside: auto; }
th, td { border-bottom: 0.5pt solid #bbb; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { font-family: 'Inter', sans-serif; border-bottom: 1.2pt solid #14213d; }
tr { break-inside: avoid; }
ul, ol { margin: 0.2em 0 0.7em; padding-left: 1.4em; }
li { margin-bottom: 0.25em; }
.answer { background: #f6f7f2; border: 0.75pt solid #d5d9c7; border-radius: 4pt; padding: 0.6em 0.9em; margin: 0.6em 0 1em; font-size: 9.8pt; }
.blank { display: block; height: 1.7em; border-bottom: 0.6pt solid #9a9a9a; }
code { font-size: 9pt; }
ol > li > ul { list-style: none; padding-left: 0.4em; }
ol > li > ul > li { margin: 0.1em 0; }
"""


def build(kind, workbook, out):
    mods = [module_md(p, workbook) for p in MODULES]
    body = md_to_html("\n\n".join(mods))
    body = re.sub(r'<h1 class="module" id="([^"]+)">((Module \d+).*?)</h1>',
                  r'<h1 class="module" id="\1" data-short="\3">\2</h1>', body)
    toc = "".join(
        f'<li><a href="#{i}">{t}</a></li>'
        for i, t in re.findall(r'<h1 class="module" id="([^"]+)"[^>]*>(.*?)</h1>', body))
    sub = ("Instructor & Course-Builder Guide" if not workbook else "Student Workbook")
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Internomics — {sub}</title>
<style>{CSS.replace('__KIND__', html.escape(kind))}</style></head><body>
<div class="cover"><div class="k">The Course</div><div class="t">Internomics</div>
<div class="s">How to See the Game Behind Every Interaction</div><div class="s" style="margin-top:0.5in">{sub}</div>
<div class="a">Paul Mascetta</div></div>
<div class="toc"><h2>Contents</h2><ul>{toc}</ul></div>
{body}</body></html>"""
    HTML(string=doc, base_url=str(COURSE)).write_pdf(out)
    print("wrote", out)


build("COURSE GUIDE", False, COURSE / "Internomics-Course-Guide.pdf")
build("WORKBOOK", True, COURSE / "Internomics-Student-Workbook.pdf")
