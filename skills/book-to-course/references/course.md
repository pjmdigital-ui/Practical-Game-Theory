# Stage 2: Build the course

A course is not the book cut into pieces. Each module teaches one idea so well that the learner can use it in real life that week. The book provides the content, the examples and the voice. The course adds structure, practice and accountability.

## 1. Plan the course

- **Module 0: Orientation.** Why the course exists, what the learner will be able to do, the core vocabulary, how to use the course and the main tool or journal they'll keep.
- **One module per chapter** (usually). Merge two thin chapters or split one huge one if that teaches better. Say so in your plan.
- **A final module** built from the conclusion: integration, judgment and a capstone project.

Write `course/README.md` with the course title, positioning line, the module table (number, title, the module's question, book chapter, time), how a learner moves through each module, and what is in the guide vs the workbook.

## 2. Write each module

Use `module-template.md` in this folder as the exact structure. Every section matters to a later step:

- **Lessons** become the slide decks. Each lesson needs real teaching points, an "Example to use" from the book and an on-screen takeaway.
- **The tool** becomes the workbook worksheet. Use the book's own questions.
- **Exercises with `<details>` model answers.** The guide shows the answers; the workbook strips them.
- **Quiz** with options written as `- A) …` and an answer key in `<details>`.
- **Research spotlight** only uses studies the book actually cites. Say what each one does NOT prove.

Rules:
- Use the book's examples, wording and stories. Never invent studies, statistics, names, dates or quotes. If the book doesn't give a detail, leave it out.
- Write in the author's voice: first person, direct and warm.
- Short sentences. Few commas (see the writing rules in `slides.md`; they apply here too).

For 6+ modules, fan out: one subagent per module (or per two modules), each given the template, the chapter's line range in the manuscript, the course README and Module 0 as the finished reference. Ask each to write only its module file. Review a couple yourself before building.

## 3. Build the PDFs

```
python3 <skill>/scripts/build_course.py project.json course/modules course
```

This writes:
- `<slug>-Course-Guide.pdf`: every module with answers, for the creator or instructor.
- `<slug>-Student-Workbook.pdf`: only the tools, exercises, quiz, field assignment and question to carry, with answers removed and writing lines added.

Module files must be named `module-00-….md`, `module-01-….md` and so on, each starting with `# Module N — Title`.

Check a few pages as PNGs. The usual issue is a list right under a bold line that renders as one paragraph. The script adds the missing blank line, but check anyway.
