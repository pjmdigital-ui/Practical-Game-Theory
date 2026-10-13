---
name: book-to-course
description: Turn a book manuscript (often ChatGPT-written) into a full info product. Polish it into a professional PDF and Word book with a table of contents and page numbers, build a video course from it (module guides, a course guide PDF and a student workbook), then make recording slide decks with full speaker notes in the claude.ai Slides format. Use this whenever the user wants to format or polish a book they wrote, turn a book or manuscript into a course, make course modules or a workbook from a book, or create slides to record a course, even if they only ask for one of these stages or say "do what we did for Internomics with my new product".
---

# Book → Course → Recording Slides

This is the process used to turn Paul Mascetta's *Internomics* manuscript into a 395-page book, a 13-module course (guide and workbook) and 13 recording decks with 678 slides. It runs in three stages. Each stage stands on its own, so start wherever the user is:

| Stage | Input | Output | Read |
|---|---|---|---|
| 1. Polish the book | raw manuscript (.md, .docx, pasted text) | `book/manuscript.md`, `<slug>.pdf`, `<slug>.docx` | `references/book.md` |
| 2. Build the course | clean manuscript | `course/modules/module-NN-*.md`, Course Guide PDF, Student Workbook PDF | `references/course.md`, `references/module-template.md` |
| 3. Recording slides | module files + book | one Slides deck per module, with speaker notes | `references/slides.md`, `assets/reference-deck/` |

Read the reference file for a stage before starting it. They hold the conventions the scripts expect and the author's standing feedback.

## Principles

- **Polish, don't rewrite.** The author wrote this book and wants it to look finished, not to sound like someone else. Remove only what an editor would remove without asking (duplicate titles, chat leftovers, superseded drafts). Report every removal.
- **The book is the source of truth.** Course and slides use the book's examples, wording and stories. Never invent studies, statistics, names, dates or quotes.
- **Write the way the author talks.** First person, warm and direct. Short sentences with few commas. Each slide has enough on it to teach from, with a 180–350 word talk track in the notes. This was the author's feedback on the first course, so treat it as the default.
- **Show one before making many.** Build Module 0 (or one chapter's worth) first, get the author's reaction, then fan out the rest with subagents in parallel.

## Setup

Create a `project.json` at the project root. All scripts read it:

```json
{
  "title": "Product Name",
  "subtitle": "The Subtitle",
  "author": "Author Name",
  "year": 2026,
  "slug": "Product-Name",
  "colors": {"primary": "#14213D", "accent": "#FCA311"},
  "deck": {"colors": {"dark": "#14213D", "accent": "#FCA311"},
           "heading_font": "Inter", "body_font": "Source Serif 4"}
}
```

If there's no product name or brand yet, ask. Naming may take a few rounds. Offer options with the reasoning behind each, and don't build anything with a placeholder name the user hasn't accepted.

Tools: `pandoc`, `pip install weasyprint python-docx`, and optionally LibreOffice (`soffice`) to pre-fill the Word TOC. Keep the user's original files untouched in `source/`.

## Scripts

| Script | Use |
|---|---|
| `scripts/build_book.py project.json book/manuscript.md book` | Book PDF (6x9, TOC, running heads, footnotes) and DOCX |
| `scripts/build_course.py project.json course/modules course` | Course Guide and Student Workbook PDFs |
| `scripts/check_deck.py DECK_DIR [--files]` | Validate a deck; `--files` prints the publish `files` map |
| `scripts/rebrand_deck.py DECK_DIR project.json` | Swap the reference palette and fonts for the product's |
| `scripts/make_reference_docx.py`, `scripts/update_docx_toc.py` | Used by build_book.py |

`references/example_clean_manuscript.py` is the cleaning script from the first book. It's an example to adapt, not a general tool.

## Suggested layout

```
source/                 originals, untouched
book/manuscript.md      clean canonical text
book/<slug>.pdf/.docx
book/archive/           removed drafts, kept for reference
course/README.md        course map
course/modules/         module-00-orientation.md …
course/<slug>-Course-Guide.pdf, <slug>-Student-Workbook.pdf
course/slides/mNN/      deck sources + README with deck links
tools/                  the cleaning script for this book
```

Commit as each stage lands. At the end, give the user the book, the two PDFs, a table of deck links, and one line on how to present (open a deck, press Present, and Esc exits the show).
