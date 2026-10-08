# Revision brief: Internomics recording decks (round 2)

Paul reviewed the decks. His feedback:
1. **Too many commas.** The writing overuses them.
2. **Not detailed enough.** He needs more content and context on each slide so he can really elaborate while recording.

Revise your deck IN PLACE (same folder, same slide ids). The look, palette, fonts and markup patterns stay exactly as defined in `decks/STYLE.md` and the Module 0 reference files.

## 1. Commas: write in short, clean sentences

Applies to on-slide text AND speaker notes.
- Prefer short declarative sentences. One idea per sentence.
- Aim for **no more than one comma per sentence**. Most sentences should have none.
- Break comma chains into separate sentences: "Maybe they're signaling, maybe they're building reciprocity, or maybe..." becomes "Maybe they're signaling. Maybe they're building reciprocity. Or maybe..."
- Do not join two clauses with ", and" / ", but" / ", so". Split them into two sentences, or drop the comma if the clause is short.
- Drop introductory commas where possible ("In this module, we..." becomes "This module..."; "Here's the thing, ..." becomes "Here's the thing.").
- Lists of three or more items in prose: turn them into separate sentences, or put them on the slide as cards or a list instead of a comma-separated line.
- On slides, a list of items belongs in cards, rows or table cells, not in one comma-separated sentence.
- Never replace commas with em dashes. Use periods.

## 2. More content on each slide

Every **teaching, statement, example, research, tool, practice and mistakes** slide should give Paul enough on screen to talk through.
- A slide that is only a headline (or a headline plus one line) gets a supporting element under it: 2–4 short supporting points (cards or rows), a "Why it matters" line, a concrete mini-example, or a question for the viewer. Use the book chapter's own reasoning and examples.
- Example slides: show the situation, what happened, and the lesson as three labeled parts (e.g. "The situation" / "What happened" / "The lesson"), not only a title.
- Keep slides readable. Respect the fit rules in STYLE.md (content area 1664 × 792 px; 72px headings ≤ 2 lines; nothing under 24px). **If a slide gets too full, split it into two slides** rather than shrinking text. Decks may grow to roughly 45–55 slides.
- Dividers, takeaway slides, the cover and the closing question keep their minimal design (comma pass only).
- New slide ids: lowercase `[a-z0-9-]`, unique (e.g. `l2-pie-2`). Add each to `order` in `deck.json` in the right place. Do not rename or remove existing ids. Keep every other key in deck.json unchanged.

## 3. Speaker notes: a real talk track

For teaching, statement, example, research, tool, practice and mistakes slides, expand the `<aside>` notes to **180–350 words**. Write them as plain-text paragraphs Paul can speak from, in his voice: first person, warm, direct and conversational. Include:
1. **The point**, stated plainly in one or two sentences.
2. **Context**: why it's true and how it works, drawn from the book chapter's own explanation.
3. **An example or story**: from the book chapter where possible, told concretely.
4. **A question for the viewer**, or the common misunderstanding to watch for.
5. **A one-line transition** to the next slide.

Dividers and takeaways: 2–4 sentences. Cover and closing: 60–120 words.
Hard limit: 3,500 characters per `<aside>`. Plain text only, no line breaks needed.

## 4. Accuracy

- Stay faithful to the module file and the book chapter. Use the book's examples and wording where you can.
- **Never invent** studies, statistics, numbers, names, dates or quotes. If the book or module doesn't give a detail, leave it out.

## 5. How to work

- Read `decks/STYLE.md`, then every file in your deck, then the module file and the book chapter.
- Edit or rewrite each slide file with the Write/Edit tools. No scripts that generate files.
- When finished, run: `python3 <scratchpad>/check_deck.py <your deck folder>` and fix anything it reports (a "gap" warning caused by the word "gap" inside notes text is a false positive).
- Also run: `grep -o ',' <your deck folder>/project/slides/*.html | wc -l` before and after, and report both counts.
- Do NOT publish, use the Artifact tool, run git, or render anything.
