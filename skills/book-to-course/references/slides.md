# Stage 3: Recording slide decks

One deck per module, built in the claude.ai **Slides** Artifact type. Every slide has speaker notes written as a talk track in the author's voice, so they can record while reading or riffing from presenter view.

The finished reference deck is in `assets/reference-deck/` (46 slides, Module 0 of the first course). It shows every slide kind and the level of detail the author approved. Copy its markup patterns exactly. The content is from another product. Use it only for layout, density and tone.

## Contents
1. Writing rules (the author's standing feedback)
2. Slide format and fit rules
3. Slide kinds
4. Deck plan for one module
5. Speaker notes
6. Workflow: build, check, rebrand, publish
7. Gotchas

## 1. Writing rules

These come from the author's review of the first course. Apply them from the first draft. Don't wait for a revision round.

**Short sentences. Few commas.**
- One idea per sentence. Most sentences have no comma. Never more than one.
- Split comma chains. "Maybe they're signaling, maybe they're building trust, or maybe…" becomes "Maybe they're signaling. Maybe they're building trust. Or maybe…"
- Don't join clauses with ", and" / ", but" / ", so". Make two sentences.
- Drop introductory commas. "In this module, we…" becomes "This module…".
- Lists of three or more go on the slide as cards or rows. In notes, make them separate sentences.
- Don't swap commas for em dashes. Use periods.

**Enough on each slide to teach from.**
- A slide that is only a headline gets a supporting element: 2–4 cards or rows, a "Why it matters" line, a mini-example or a question for the viewer.
- Example slides show three labeled parts: **The situation / What happened / The lesson**.
- If a slide gets crowded, split it into two. Never shrink text below the scale.
- Decks land around 45–55 slides per module.

**Accuracy.** Use the book's examples and wording. Never invent studies, numbers, names, dates or quotes.

## 2. Slide format and fit rules

Each deck is a folder:

```
mNN/project/deck.json
mNN/project/slides/<id>.html     one <section id="<id>"> per file, notes in a final <aside>
```

- Canvas 1920x1080. Section padding `128px 128px 160px`. Content area 1664 x 792.
- Footer pinned: `position:absolute;left:128px;bottom:64px;width:1664px`, 24px uppercase, `Brand · Module N — Title`. Closing slide: `Brand · Next: Module N+1 — Title`. Last module: `Brand · Course complete`.
- Inline styles only. No `<style>`, no classes, no `margin`, no `em` or `%` font sizes, no CSS variables, no nested lists. `gap` takes one value. Write `&amp;` for "&".
- Type scale (px): 120 cover/closing h1 · 96 lesson dividers and takeaways · 72 slide headings · 48/44/40/36 sub-statements and card titles · 34/32/30/28 body · 26 eyebrows · 24 footer and small card text. Nothing under 24.
- Heading fit: about 1664 / (0.6 x size) characters per line. 72px is about 38 characters per line. Keep 72px headings to 2 lines (76 characters).
- Cards: lines x size x line-height + padding. Table row: about 2.1 x size per line of text.

**Palette roles.** Always write in the reference palette below. `rebrand_deck.py` swaps in the product's colors afterwards. That keeps every subagent copying identical markup.

| Role | Reference hex | Used for |
|---|---|---|
| dark | `#14213D` | dark backgrounds, headings on light |
| light | `#F6F4EE` | light backgrounds |
| card / border | `#FFFDF8` / `#E2DED3` | cards on light |
| panel / dark_panel | `#E9E5DA` / `#22325A` | muted panels |
| accent | `#FCA311` | fills, eyebrows on dark, takeaway background |
| accent_text | `#B45309` | eyebrows on light |
| body / body_on_dark | `#3B4252` / `#C9D3E3` | body text |
| muted / muted_on_dark | `#5B6577` / `#8FA0BC` | footer text (`#14213D` on accent) |

Fonts: headings `Inter, Arial, sans-serif` (800 for h1/h2, 700 for h3/eyebrows). Body `'Source Serif 4', Georgia, serif` set on the section.

## 3. Slide kinds (copy the reference file named)

| Kind | Reference file | Background |
|---|---|---|
| Cover | `cover.html` | dark |
| Statement: eyebrow, big claim, support | `why.html`, `l1-same.html` | light |
| Objectives | `objectives.html` | light |
| Lesson divider | `l1.html` | dark |
| Card grid (2–6 cards) | `l1-tactics.html`, `l2-kinds.html`, `l2-lens.html` | light |
| From → To | `l1-shift.html` | light |
| Questions | `l1-questions.html` | light |
| Example (situation / what happened / lesson) | `l1-example.html` … `l1-example-4.html`, `l2-example.html`, `l4-example.html` | light |
| Takeaway | `l1-take.html` | accent |
| Definition | `l3-internomics.html` | dark |
| Table | `l3-part1.html`, `terms.html` | light |
| Dark cards | `l4-ethics.html` | light with dark cards |
| Four-part grid | `l3-judgment.html` | light |
| Process / loop | `l4-loop.html` | light |
| Research: shows / doesn't prove | `research.html` | light |
| Tool / worksheet | `tool.html` | light |
| Practice scenario and answer | `practice.html`, `practice-2.html`, `practice-answer.html`, `practice-b.html` | light |
| Common mistakes | `mistakes.html` | light |
| Field assignment | `field.html` | dark |
| Closing question | `carry.html` | dark |

## 4. Deck plan for one module

1. `cover`: eyebrow `Brand · Module N`, h1 = module title, sub-line = the module's question. Footer = author name.
2. `why`: statement slide from "Why this module matters".
3. `objectives`: one line per objective.
4. For each lesson: divider (`Lesson N.x · M min` + title), then 3–6 teaching slides (one idea each; turn bullet lists into cards, comparisons, tables or statements), example slides (situation / what happened / lesson; split long stories across 2–4 slides), a takeaway slide.
5. `terms`: key terms table, max 7 rows (split if more).
6. `research`: one slide per study, max 2.
7. `tool`: the worksheet prompts as a card grid (max 8).
8. `practice`, `practice-2`: the scenario and "Pause the video and answer:" questions. `practice-answer`: the model answer. `practice-b`: the personal exercise.
9. `mistakes`: card grid, max 4 (split if more).
10. `field`: field assignment.
11. `carry`: the question to carry.

Last module only: add `capstone`, `capstone-rubric` and a `thanks` slide if helpful.

Ids: lowercase `[a-z0-9-]`, unique, e.g. `l2-payoffs`, `l2-example-2`, `l2-take`.

`deck.json`: copy the reference one. Change `title` to `Brand — Module N: Title`, `order` to your ids and `sections` (intro, one per lesson, practice; each a one-sentence `description` and its `start` id). Keep `v`, `createdOnFiles`, `lists`, `designSystems` as they are. `faces` is set by `rebrand_deck.py`.

## 5. Speaker notes

Plain text in the `<aside>`, the last child of the section. Hard limit 3,500 characters.

- **Teaching, statement, example, research, tool, practice and mistakes slides: 180–350 words.** Cover in order:
  1. The point, plainly, in one or two sentences.
  2. Context: why it's true and how it works, from the book.
  3. An example or story from the book, told concretely.
  4. A question for the viewer, or the common misunderstanding.
  5. A one-line transition to the next slide.
- Dividers and takeaways: 2–4 sentences. Cover and closing: 60–120 words.
- First person, warm, direct, conversational. It's what the author says on camera. Expand the slide; don't read it.
- Same comma rules as the slides.

## 6. Workflow

1. **Get the brand.** Ask for the product name, author name and colors/fonts if there's no brand yet. Otherwise suggest a palette that fits the topic. Put it in `project.json` under `"deck"` (see `rebrand_deck.py` for keys).
2. **Build Module 0 yourself first** in the scratchpad (`decks/m00/project/`). Show the author. Fix anything they flag before fanning out. Their feedback on one deck is cheap. On thirteen it's expensive.
3. **Fan out.** One subagent per module (in parallel). Give each:
   - this file's path, the reference deck path and the finished Module 0 path,
   - the module file and the book chapter's line range,
   - its output folder, and the instruction to write each slide with Write/Edit (no generator scripts), run `check_deck.py` and fix what it reports, and NOT publish or use the Artifact tool.
4. **Check every deck** with `python3 <skill>/scripts/check_deck.py decks/mNN`. Structure must be OK. Thin notes and comma counts should be near zero.
5. **Rebrand** each deck: `python3 <skill>/scripts/rebrand_deck.py decks/mNN project.json`. Re-run the check.
6. **Publish.** Do the quickstart once (`Artifact action:"quickstart" intent:"slides"`) to get the Slides `type_url`. Then for each deck:
   - Create: `Artifact publish` with `type_url`, `title: "Brand — Module N: Title"`, `auto_open: "after_first_write"`. Note the returned `url`.
   - Fill: `Artifact publish` with that `url`, `root: decks/mNN`, `file_path: decks/mNN/project/deck.json`, and `files` from `check_deck.py decks/mNN --files`.
   - To update later, publish the same way to the same `url`.
7. **Save the sources** in the repo (e.g. `course/slides/mNN/`) with a README table linking every deck, and commit.

## 7. Gotchas

- **"I can't see the play button."** In present mode the editor toolbar (and the Present button) is hidden. Press Esc to leave the show. Present starts from the selected slide, so select the cover first.
- A deck may move to a newer release of the Slides viewer the first time it's opened. The toolbar can look slightly different. That's expected.
- A session can watch only about 10 artifacts for changes. With 13+ decks, some won't be watched. Mention it, and re-read a deck before editing it later.
- `gap:16px 64px` breaks the editor. Use one value.
- Never put a real comma-separated list in one sentence on a slide. It reads badly on camera. Use cards.
