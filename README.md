# comprog-python-data-exam

A Claude skill for the final exam of Computer Programming for Chemical Engineers (pandas and NumPy in Jupyter or VS Code, on Excel/CSV plant data). Current version: **1.8**.

In the exam chat the skill makes Claude:

1. Give a ready-made cell that profiles every file and scans it for prompt injection (hidden sheets, rows and slides; white, pale, tiny, same-colour or format-hidden text in Excel, Word and PowerPoint; text off the slide, under a shape or in the speaker notes; stray cells away from the table; AI-addressed lines and orders in English or Thai).
2. Ask a short round of questions on the decisions the files do not settle, the missing limit first, and agree a Decisions table.
3. Write the code as a notebook (`.ipynb`), a VS Code Python file with `# %%` cells, or both. It runs on pandas 1.5 to 3.x and writes the answer files itself.
4. Check the answers by an independent second route (plus subagents when the chat has them), run a fix loop until every check passes (at most 5 rounds), and end with a doubt list.
5. For a machine-learning task (week 5): follow the course's three steps (Model Selection & Tuning, Final Training, Deployment) with scikit-learn, with no test rows used for fitting, and flag new conditions outside the training range.
6. Label every stage in the course's terms (Prompt Level L1 to L5, Agentic Level A1 to A4), since the chat itself is graded.

If you open with only the task and no prompt, Claude writes the prompt first: a Level 3 draft (Role, Task, Context in tags, Format, Example, Constraints, ending with the model-and-time line) with the handout's tasks word for word. You fill the `[FILL]` slots, edit it and send it as your own message; the work starts from that message. The draft is visible in the chat, so ask your teacher whether a model-drafted prompt earns the prompt marks.

The skill file is [`comprog-python-data-exam/SKILL.md`](comprog-python-data-exam/SKILL.md). Ready-made exam prompts (Level 5) are in [`PROMPT.md`](PROMPT.md). Five timed practice tasks, one per exam task type, with planted traps and answer keys are in [`mock-exams/`](mock-exams). Five more are in [`training-gym/`](training-gym), with a grader that shows which decision went the wrong way, sealed invigilator rulings, and the stress test of the scan cell.

## Install

- **claude.ai:** zip the `comprog-python-data-exam` folder and upload it in your Skills settings.
- **Claude Code:** copy the folder to `~/.claude/skills/comprog-python-data-exam/`.

Your copy does not update itself. When the version above changes, download again and re-upload.

## Exam-day checklist

- [ ] The skill is uploaded and switched on in the account you will use in the exam.
- [ ] You did one timed practice run with the exam model (Sonnet) on one of the [mock exams](mock-exams).
- [ ] In VS Code on the exam laptop: the Python and Jupyter extensions are installed, a kernel is selected, and `import pandas, numpy, openpyxl, matplotlib, sklearn` runs in a cell.
- [ ] You know the hand-in format (`.ipynb`, `.py` or both) and whether NumPy must be used.
- [ ] Prompt 1 from `PROMPT.md` is ready to fill in, or you have decided to give only the task and let the skill draft the prompt for you to edit and send.
- [ ] In the exam: attach every file, name the skill in the first message, end it with "Tell me the model we are using and the current time.", and screenshot your prompt with Sonnet visible.
- [ ] Answer the decision questions with reasons; ask the invigilator about MUST ANSWER questions.
- [ ] You know whether a review in a second chat is allowed, and how many chat links you hand in.
- [ ] Hand in the notebook (after Restart and Run All, saved), the answer files and the chat link.

## Tested

- **Skill code:** the date helper gives the same output on pandas 1.5.3, 2.0.3, 2.2.3 and 3.0.5, and 26 pandas claims in the skill were checked on each. The v1.5 scan cell was tested on those four versions too. The v1.7 scan cell has been run on pandas 3.1.1 only; its pandas calls are the same as before.
- **Scan stress test (v1.7):** `training-gym/stress_scan.py` runs the scan cell, unchanged, on the five training-gym exams and on a rack of 62 probes, one hiding technique each. The v1.6 cell flagged 19 of 20 planted instructions and missed 25 of 54 hiding probes (22 of them things a teacher can do by hand in Office); it also flagged 5 of 8 harmless lines. The v1.7 cell flags 20 of 20, misses none of the 54, and flags 2 of the 8 harmless lines. On the teacher's real mock-exam files it raises no flag. The result is in [`training-gym/stress_scan_report.txt`](training-gym/stress_scan_report.txt).
- **Training-gym exams with Sonnet (v1.6):** five runs with a plain prompt, the questions answered from the rulings sheets and each notebook re-run from scratch, scored 153/153, 48/48, 13/15, 334/334 and 45/45, with all 20 planted instructions reported. The two lost cells came from a 3-hour gap offered as a Confirm item where the handout defines a short gap as 1 or 2 hours. v1.7 makes that kind of case MUST ANSWER; **this wording change has not been re-run with Sonnet yet.** The hand-ins are in `training-gym/sonnet_baseline/`.
- **Mock exams with Sonnet (v1.4):** five runs with the questions answered from the invigilator sheets scored 18/18 (twice), 20/20, 200/200 and 96/96 + 4/4, with every planted injection caught (5, 5, 4, 5, 4). The code each run wrote also runs on the three older pandas versions with the same answers. Details are in [`mock-exams/README.md`](mock-exams/README.md).
- **Scan (v1.5 and earlier):** planted Excel, Word and PowerPoint files (all caught, coloured headers not flagged) and real course files (no false alarms). The v1.7 stress test above replaces this.
- **Prompt first (v1.8):** not run with Sonnet yet.
- **Not tested:** a real claude.ai chat, VS Code itself, Team mode with subagents.

## Changelog

- **1.8** (2026-11-23): Prompt first. When the student gives only the task, the first reply is a Level 3 prompt draft for the student to fill, edit and send; the draft's last two tasks ask for the decision questions, the fix loop and the independent reviewer, which are unchanged. The wrap-up says the prompt started as a model draft.
- **1.7** (2026-11-21): fixes from a stress test (see `training-gym/`).
  - Scan cell: now catches PowerPoint theme-white text, text boxes off the slide or under another shape, and prints every speaker note with the slide it belongs to (the old label was the notes file's number, not the slide's); Excel pale-yellow and legacy-colour white fonts, white on a white fill, squeezed rows and columns, page footers, data-validation messages and stray cells away from the table; Word white text set through a style, and document properties. Wording: "chatbot", "Sonnet", "GPT", "automated tool", "A.I.", "AI" typed against Thai letters, Thai "โมเดล", and orders with no AI word ("this overrides the handout", "skip the ..."). Fewer false alarms ("Prompt action", "Instruction manual", "Laboratory assistant", tags such as `AI-101`).
  - Questions: a case just outside a definition the handout gives (a 3-hour gap when a short gap is "1 or 2 hours", a rate given as a range, a material on neither list) is MUST ANSWER. "This changes no answer" needs the list of options that were compared; for a blank there are three (fill, leave blank and keep the row, leave blank and drop the row).
  - Injection alert: a hidden line that supplies a limit or a rule is counted in the alert and then asked as a question. The scan's flags are hints: slides and notes are still read, and the handout is compared with the slides.
  - Type B: gap lengths against the handout's definition, filled values in a ratio, Excel-worded handouts with a Word template, pooled against per-group correlation. Type E: `StandardScaler` must stay in the polynomial pipeline (scikit-learn 1.9.1 gave test RMSE 12.57 without it where exact least squares gives 10.33, with no warning).
  - New `training-gym/`: five more mock exams, a cell-by-cell grader, the scan stress test and its 62-probe rack.
- **1.6** (2026-11-21): Team mode. Every subagent brief is written in the teacher's prompt form (Role, Task, Context, Format, Example, Constraints), and the wrap-up carries a team summary table, because subagent work does not show in the shared chat.
- **1.5** (2026-11-20): week 5 added. New task type E (regression with scikit-learn: train-test split, scores, tuning, final training, prediction); exam rules from the slides (model-and-time line, prompt screenshot, Sonnet only); the teacher's notebook style (one step per cell, line-by-line comments when asked); a reviewer prompt for a second chat; mock exam E.
- **1.4** (2026-11-20): questions come in two kinds, and MUST ANSWER ones (missing limit, `<5`, duplicates that disagree, clock windows) carry no recommendation; VS Code support (`.py` with `# %%` cells, Data Viewer, NumPy notes); the scan hints at lines that set a result; the date helper handles `24:00`; warnings for the `g/L` in `mg/L` trap and for float noise after unit conversion; contradictions removed. Skill code re-tested on pandas 1.5.3, 2.0.3, 2.2.3 and 3.0.5.
- **1.3** (2026-11-19): three more mock exams (historian cleaning, work-order triage, mass balance with logbook), each key confirmed by a second solution; mocks moved to `mock-exams/`.
- **1.2** (2026-11-19): scan also catches Excel text hidden by a `;;;` number format or by a font the same colour as the fill; mock exam with 14 traps, answer key and checker.
- **1.1** (2026-11-19): scan catches white or tiny text in Excel cells, scans PowerPoint slides, notes and hidden slides, and flags Thai AI-addressed words; fix loop with stop condition, 5-round cap and status lines; stage labels and level summary for the graded chat; `PROMPT.md` with Level 5 prompts.
- **1.0** (2026-11-16): first release.

## License

[MIT](LICENSE). Use, change and share it freely; keep the copyright notice.
