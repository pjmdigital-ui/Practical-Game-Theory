# Internomics

**How to See the Game Behind Every Interaction** · Paul Mascetta

> **Internomics** is the study of what happens between people. It applies the principles of game theory to communication and human interaction—not to teach you what to say, but to teach you how to understand the game you're already playing.

This repository (still named `Practical-Game-Theory`, the working title) is the source of truth for the Internomics project: the book, the course built from it, and the research behind both. The planned ecosystem is **Book → Course → AI Practice → Community**.

## Start here

| I want to… | Open |
|---|---|
| Read the finished book | [`book/Internomics.pdf`](book/Internomics.pdf) (print-ready 6×9) |
| Edit the book in Word | [`book/Internomics.docx`](book/Internomics.docx) |
| Edit the book's text (canonical) | [`book/manuscript.md`](book/manuscript.md) |
| See the course plan | [`course/README.md`](course/README.md) |
| Teach or build the course | [`course/Internomics-Course-Guide.pdf`](course/Internomics-Course-Guide.pdf) |
| Record the course videos | [`course/slides/README.md`](course/slides/README.md) (13 slide decks with speaker notes) |
| Give learners their handout | [`course/Internomics-Student-Workbook.pdf`](course/Internomics-Student-Workbook.pdf) |
| Look up research behind a chapter | [`source/Game_Theory_Dossier.md`](source/Game_Theory_Dossier.md) |

## Status

| Item | Status |
|---|---|
| Book manuscript (Introduction, 11 chapters, Conclusion) | **CURRENT**: formatted, ~51,000 words |
| Book PDF / Word editions | **CURRENT**: generated from `book/manuscript.md` |
| Course (13 modules, Orientation + 11 models + Capstone) | **CURRENT**: first complete draft |
| First Conclusion draft | **SUPERSEDED**: kept in `book/archive/` for reference only |
| Original ChatGPT exports | **ARCHIVED**: `source/` (unchanged originals) |

## Layout

```
book/
  manuscript.md                 canonical book text (edit this)
  Internomics.pdf               print-ready book (generated)
  Internomics.docx              Word edition (generated)
  archive/                      superseded drafts
course/
  README.md                     course overview, outcomes, schedule, formats
  _module-template.md           the structure every module follows
  modules/                      module-00 … module-12 (edit these)
  *.pdf                         Course Guide + Student Workbook (generated)
source/                         original uploads, untouched
tools/                          build scripts
```

## Rebuilding after edits

Requires `pandoc`, LibreOffice, and `pip install weasyprint python-docx`.

```bash
# only needed if you re-import the original ChatGPT export
python3 tools/clean_manuscript.py source/Game_Theory_original_manuscript.md source/Game_Theory_Dossier.md book

python3 tools/build_book.py     # book PDF + Word file
python3 tools/build_course.py   # course guide + student workbook
```
