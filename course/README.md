# Internomics — The Course

**How to See the Game Behind Every Interaction**
A 13-week course built from the book *Internomics* by Paul Mascetta.

> **Internomics** is the study of what happens between people. It applies the principles of game theory to communication and human interaction—not to teach you what to say, but to teach you how to understand the game you're already playing.

## The promise

Most communication training teaches you what to say. This course teaches you to see what is happening *before* you speak: who the real players are, what each one values, how they'll respond, what they know and believe, what makes a message credible, and when the problem isn't the conversation at all but the structure of the game.

Graduates don't leave with scripts. They leave with **strategic judgment**: the habit of asking the right question at the right moment, and the discipline to test their read of a situation against what actually happens.

## Who it's for

- Professionals who negotiate, lead, sell or manage: anyone whose results depend on other people's decisions.
- Readers of the book who want structured practice, not just ideas.
- Anyone stuck in recurring conflicts at work or at home who suspects better wording isn't the answer.

No math is required.

## Course outcomes

By the end of the course, learners will be able to:

1. Map any important interaction as a game: players, payoffs, options, constraints, information, timing, alternatives and dependencies.
2. Explain other people's behavior through what they value, not just what they say.
3. Anticipate responses and reason backward from where an interaction is likely to end.
4. Recognize and manage what their own patterns teach others to predict.
5. Diagnose stable bad patterns (equilibria) and identify what would have to change to move them.
6. Separate facts, beliefs and assumptions, and evaluate the credibility of messages, including their own.
7. Make commitments, promises and boundaries that are actually believable.
8. Factor the future ("the shadow of the future") into today's choices.
9. Tell genuine conflict apart from coordination failure, and fix the latter.
10. Redesign incentives, information and rules when better moves inside the current game won't work.
11. Do all of this within an explicit ethical standard: **truth, autonomy, dignity, informed choice.**

## Structure

| Week | Module | Book reading | Tool learners build |
|---|---|---|---|
| 0 | [Orientation: The Game Behind the Conversation](modules/module-00-orientation.md) | Introduction | The Interaction Journal |
| **Part I** | **See the Structure Beneath the Conversation** | | |
| 1 | [See the Game](modules/module-01-see-the-game.md) | Chapter 1 | The Game Map |
| 2 | [See the Payoffs](modules/module-02-see-the-payoffs.md) | Chapter 2 | The Payoff Map |
| 3 | [Think in Responses](modules/module-03-think-in-responses.md) | Chapter 3 | The Response Map |
| 4 | [Manage Predictability](modules/module-04-manage-predictability.md) | Chapter 4 | The Predictability Audit |
| 5 | [See the Equilibrium](modules/module-05-see-the-equilibrium.md) | Chapter 5 | The Equilibrium Audit |
| **Part II** | **See What Isn't Obvious** | | |
| 6 | [Map Information & Beliefs](modules/module-06-map-information-and-beliefs.md) | Chapter 6 | The Information Map |
| 7 | [Separate Words From Credibility](modules/module-07-separate-words-from-credibility.md) | Chapter 7 | The Credibility Test |
| 8 | [Commitment Changes the Game](modules/module-08-commitment-changes-the-game.md) | Chapter 8 | The Commitment Test |
| **Part III** | **Think Beyond the Moment** | | |
| 9 | [The Shadow of the Future](modules/module-09-the-shadow-of-the-future.md) | Chapter 9 | The Repeated-Game Audit |
| 10 | [Diagnose the Coordination Problem](modules/module-10-diagnose-the-coordination-problem.md) | Chapter 10 | The Coordination Diagnostic |
| 11 | [Change the Game](modules/module-11-change-the-game.md) | Chapter 11 | The Game-Change Audit |
| 12 | [Strategic Judgment + Capstone](modules/module-12-strategic-judgment.md) | Conclusion | The Strategic Judgment Worksheet + capstone project |

## What every module contains

Each module follows the same structure ([template](_module-template.md)), so learners always know where they are:

1. **The question:** the single question the mental model teaches you to ask.
2. **Why this module matters:** the problem it solves and the mental shift.
3. **Learning objectives.**
4. **Lessons:** 3–5 short video lessons, written as recording outlines (teaching points, the example to use, an on-screen takeaway).
5. **Key terms:** plain-language glossary.
6. **Research spotlight:** the evidence behind the model, including what the research does *not* prove.
7. **The tool:** a fill-in worksheet drawn from the chapter.
8. **Practice exercises:** (A) analyze a scenario, with a model answer; (B) apply it to your own life; (C) a partner or role-play drill.
9. **Common mistakes.**
10. **Quiz:** 8 questions with an answer key.
11. **Field assignment:** one real-world practice task for the week, with debrief questions.
12. **The question to carry.**

## Delivery formats

The same curriculum supports three formats:

| Format | How it runs |
|---|---|
| **Self-paced online** | One module per week. Videos recorded from the lesson outlines; workbook as a downloadable PDF; quizzes in the course platform. |
| **Cohort / live** | Weekly 90-minute session: 20 min field-assignment debrief → 30 min teaching → 30 min partner drill (Exercise C) → 10 min next-week setup. |
| **Workshop** | One-day intensive: Module 0 + Part I (morning), selected modules from Parts II–III (afternoon), capstone assigned as follow-up. |

## How the course fits the ecosystem

**Book → Course → AI Practice → Community.** The book builds the intellectual framework. The course turns it into a skill through structured practice. Exercise C in every module is written so it can also run with an AI practice partner (the planned AI training platform), and the field-assignment debriefs are designed to become community discussion prompts.

## Files

| File | Purpose |
|---|---|
| `modules/` | The 13 modules (source of truth for course content) |
| `_module-template.md` | The structure every module follows |
| `Internomics-Course-Guide.pdf` | The full course in one document: all lessons, answer keys, rubrics. For the instructor or course builder. |
| `Internomics-Student-Workbook.pdf` | Learner handout: worksheets, exercises, quizzes and field assignments, without answers |

Rebuild the PDFs after editing any module:

```bash
python3 tools/build_course.py
```
