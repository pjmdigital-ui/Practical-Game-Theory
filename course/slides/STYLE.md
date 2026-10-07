# Internomics course decks: house style

The finished reference deck is Module 0, in `decks/m00/project/`. READ ALL OF ITS SLIDE FILES FIRST and copy
their markup exactly. Every slide in every module must look like it came from the same deck.

## Palette (never introduce other colors)
- Navy (dark bg, headings on light): `#14213D`
- Cream (light bg): `#F6F4EE`
- Card white: `#FFFDF8`, card border `#E2DED3`, muted panel `#E9E5DA`, navy panel `#22325A`
- Orange accent: `#FCA311` (fills; eyebrows on navy; takeaway slide background)
- Dark orange (eyebrows on cream): `#B45309`
- Body text on cream: `#3B4252`; on navy: `#C9D3E3`
- Footer text: `#5B6577` on cream, `#8FA0BC` on navy, `#14213D` on orange

## Type
- Headings and labels: `font-family:Inter, Arial, sans-serif` (800 for h1/h2, 700 for h3/eyebrows)
- Body: `'Source Serif 4', Georgia, serif` (set on the section)
- Sizes only: 120 (cover/closing h1), 96 (lesson dividers, takeaways), 72 (slide headings), 48/44/40/36 (sub-statements, card titles), 34/32/30/28 (body), 26 (eyebrows), 24 (footer, small card text). Nothing under 24px.

## Slide kinds (copy the m00 file named)
| Kind | Copy from | Background |
|---|---|---|
| Cover | `cover.html` | navy |
| Statement (eyebrow + big claim + one support line) | `why.html`, `l1-same.html` | cream |
| Objectives list | `objectives.html` | cream |
| Lesson divider | `l1.html` | navy |
| Card grid (2-6 cards) | `l1-tactics.html`, `l2-kinds.html` | cream |
| From → To comparison | `l1-shift.html` | cream |
| Example / story cards | `l1-example.html`, `l2-example.html`, `l4-example.html` | cream |
| Takeaway | `l1-take.html` | orange |
| Definition | `l3-internomics.html` | navy |
| Table | `l3-part1.html`, `terms.html` | cream |
| Dark cards | `l4-ethics.html` | cream with navy cards |
| Process / steps | `l4-loop.html` | cream |
| Research (shows / doesn't prove) | `research.html` | cream |
| Tool / worksheet | `tool.html` | cream |
| Field assignment | `field.html` | navy |
| Closing question | `carry.html` | navy |

Every slide has the pinned footer `Internomics · Module N — <Title>` (closing slide: `Internomics · Next: Module N+1 — <Title>`; Module 12's closing slide: `Internomics · Course complete`).

## Deck plan for one module (30-40 slides)
1. `cover`: eyebrow `Internomics · Module N`, h1 = model name, sub-line = the module's question.
2. `why`: statement slide from "Why this module matters".
3. `objectives`: the learning objectives (shorten each to one line).
4. For EACH lesson in the module: divider (`Lesson N.x · M min` + title), then 2-4 teaching slides (ONE idea per slide; turn bullet lists into card grids, comparisons, tables or statements), one example slide (the lesson's "Example to use"), one takeaway slide (the lesson's on-screen takeaway).
5. `terms`: key terms table (max 7 rows; split into two slides if more).
6. `research`: research spotlight, "What it shows" / "What it doesn't prove" cards (one slide per study, max 2 slides).
7. `tool`: the module's worksheet as a card grid of its prompts (max 8; summarize if longer).
8. `practice`: Exercise A scenario, condensed, plus "Pause the video and answer:" and the questions.
9. `practice-answer`: the model answer, condensed.
10. `mistakes`: common mistakes (card grid, max 4).
11. `field`: field assignment.
12. `carry`: the question to carry.
Module 12 only: add `capstone` (steps), `capstone-rubric` (criteria table) and a final `thanks` slide after `carry` if helpful.

Slide ids: lowercase, `[a-z0-9-]`, unique, e.g. `l2-payoffs`, `l2-example`, `l2-take`.

## Fit rules (the canvas is 1920x1080; content area 1664 wide x 792 tall with the footer)
- Heading height ≈ font-size × lines × 1.1, where chars per line ≈ 1664 / (0.6 × font-size). 72px ≈ 38 chars per line: keep slide headings to 2 lines (≤ 76 characters).
- Table row ≈ 2.1 × font-size per text line. Card = lines × size × line-height + padding.
- If it doesn't fit, split into two slides; never shrink below the scale.
- `gap` takes ONE value. No `margin`, no classes, no `<style>`, no `em`/`%` font sizes, no nested lists.
- Use `&amp;` for "&" in text.

## Speaker notes (`<aside>`, last child, plain text, ≤ 3,500 characters)
Write what Paul says on camera: first person, warm, direct, conversational, like the book. 60-180 words on teaching slides, 1-2 sentences on dividers and takeaways. Expand the slide; don't just read it. Use the book chapter's own examples and wording. Never invent studies, numbers or quotes.

## deck.json
Copy `decks/m00/project/deck.json`, then change `title` to `Internomics — Module N: <Title>`, `order` to your slide ids, and `sections` (one per lesson plus intro and practice, each with a one-sentence description and its first slide id). Keep `v`, `createdOnFiles`, `lists`, `faces`, `designSystems` exactly as in m00.
