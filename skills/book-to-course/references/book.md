# Stage 1: Polish the book

The goal is a professional book, not a new book. The author wrote it (often with ChatGPT) and wants it to look and read like a finished product. Keep their words. Every removal should be something a copy editor would remove without asking: duplicates, chat leftovers, drafts that were replaced. When in doubt, keep it and mention it in your summary.

## 1. Survey before you touch anything

Read the whole source once and make a list. ChatGPT-assembled manuscripts usually have these problems:

| Problem | What it looks like | Fix |
|---|---|---|
| Duplicated chapter titles | `# Chapter 6 — X` twice in a row, or a teaser title, a paragraph, then the real title | Drop the back-to-back duplicate. A teaser with text under it becomes a bold lead-in line (`> **X.**`). |
| Chat leftovers | "Yes. Now that the 11-model…", "Picking up exactly there…", "Would you like me to…", "Here's the revised…" | Delete the line. |
| Superseded drafts | Two versions of a chapter or conclusion; the first stops mid-way | Keep the complete, later one. Move the old one to `archive/…-SUPERSEDED.md` with a comment saying why. |
| Missing pieces | The introduction or a chapter lives in a separate notes/dossier file and was never pasted in | Insert it from that file. Tell the user. |
| Inline source links | `([site](https://…?utm_source=chatgpt.com))` | Turn each into a numbered footnote. Strip `utm_source` and tracking params. |
| Messy heading levels | `#`, `##`, `####` used randomly; bold inside headings | Normalize (below). |
| Stray rules | `---` right before or after a heading | Remove. |
| Headings inside quotes | `> ## A big line` | Make it a plain bold pull-quote. |

Don't fix style, tighten prose, or merge repeated ideas across chapters. Those are rewrites. Offer them separately if they're bad.

## 2. Write a cleaning script for this book

Write a small Python script for this specific manuscript rather than hand-editing a 10,000-line file. It makes the cleanup repeatable and reviewable. `example_clean_manuscript.py` in this folder is the one used for the first book. Borrow its pieces (duplicate-title detection, footnote conversion, heading normalization, archiving) and adapt the parts that are specific to the book. Keep the original source files untouched in `source/`.

## 3. Manuscript conventions (what build_book.py expects)

```markdown
---
title: "Book Title"
subtitle: "The Subtitle"
author: "Author Name"
lang: en-US
---

::: {.definition}
**term** *(noun)*

Optional definition or epigraph page. Delete this block if the book has none.
:::

# Introduction {.chapter}

# Part I — Part Title {.part}

# Chapter 1 — Chapter Title {.chapter}

## Section heading

### Sub-section heading

Body text with a footnote.[^1]

# Conclusion — Title {.chapter}

[^1]: Source label, <https://clean.url/path>
```

- `{.part}` gets its own page. `{.chapter}` starts on a right-hand page. Both go into the table of contents.
- "Chapter N — Title" (em dash with spaces) is split into a small label and a big title on the chapter opener. The title also becomes the running head.
- Parts are optional. Add them only if the author's outline groups chapters.

## 4. Build

Create `project.json` next to the manuscript:

```json
{"title": "Book Title", "subtitle": "The Subtitle", "author": "Author Name",
 "year": 2026, "slug": "Book-Title",
 "colors": {"primary": "#14213D", "accent": "#FCA311"}}
```

Then run `python3 <skill>/scripts/build_book.py project.json book/manuscript.md book`. It writes:

- `<slug>.pdf`: 6x9 trim, title and copyright pages, a TOC with page numbers, part pages, chapter openers on right-hand pages, running heads, page numbers and real footnotes at the bottom of the page.
- `<slug>.docx`: an editable Word version with a filled-in TOC (LibreOffice fills it if present; otherwise Word offers to update it on open).

Install anything missing with `pip install weasyprint python-docx` and the system `pandoc`.

## 5. Check the output

Render a few pages to PNG (`pdftoppm -f N -l N -r 60 -png`) and look at them: the title page, the TOC, a part page, a chapter opener, a page with footnotes, and the last page. Common fixes:

- Subtitle hyphenating on the title page: the `.title-page` rule already has `hyphens:none`. Keep it.
- A heading that didn't become a chapter: it's missing `{.chapter}` or the em dash.
- Footnote text showing at the end instead of the page bottom: a link wasn't converted to a `[^n]` note.

## 6. Report

Tell the user what you removed and why (counts plus examples), what you inserted, the page count, and anything you weren't sure about.
