# comprog-python-data-exam

A Claude skill for the final exam of Computer Programming for Chemical Engineers (pandas and Jupyter on Excel/CSV plant data). Current version: **1.2**.

In the exam chat the skill makes Claude:

1. Give a ready-made cell that profiles every file and scans it for prompt injection (hidden sheets, rows and slides; white, tiny, same-colour or format-hidden text in Excel, Word and PowerPoint; AI-addressed lines in English or Thai).
2. Ask a short round of questions on the decisions the files do not settle, the missing limit first, and agree a Decisions table.
3. Write one notebook that runs on pandas 1.5 to 3.x and writes the answer files itself.
4. Check the answers by an independent second route (plus subagents when the chat has them), run a fix loop until every check passes (at most 5 rounds), and end with a doubt list.
5. Label every stage in the course's terms (Prompt Level L1 to L5, Agentic Level A1 to A4), since the chat itself is graded.

The skill file is [`comprog-python-data-exam/SKILL.md`](comprog-python-data-exam/SKILL.md). Ready-made exam prompts (Level 5) are in [`PROMPT.md`](PROMPT.md). A timed practice task with planted traps and an answer key is in [`mock-exam/`](mock-exam).

## Install

- **claude.ai:** zip the `comprog-python-data-exam` folder and upload it in your Skills settings.
- **Claude Code:** copy the folder to `~/.claude/skills/comprog-python-data-exam/`.

Your copy does not update itself. When the version above changes, download again and re-upload.

## Exam-day checklist

- [ ] The skill is uploaded and switched on in the account you will use in the exam.
- [ ] You did one timed practice run with the exam model (Sonnet) on the [mock exam](mock-exam).
- [ ] `import openpyxl` works in Jupyter on the exam laptop.
- [ ] Prompt 1 from `PROMPT.md` is ready to fill in.
- [ ] In the exam: attach every file, name the skill in the first message, answer the decision questions with reasons.
- [ ] Hand in the notebook (after Restart and Run All, saved), the answer files and the chat link.

## Tested

Run against the course's EV-101 and incident-classification quizzes, the wastewater exercise, versions of them with planted injections, and a new trap task, on pandas 1.5.3, 2.0.3, 2.2.3 and 3.1.1. The v1.1 scan was tested on planted Excel, Word and PowerPoint files (all caught, coloured headers not flagged) and on real course files (no false alarms), on pandas 3.0.5.

## Changelog

- **1.2** (2026-11-19): scan also catches Excel text hidden by a `;;;` number format or by a font the same colour as the fill; mock exam with 14 traps, answer key and checker.
- **1.1** (2026-11-19): scan catches white or tiny text in Excel cells, scans PowerPoint slides, notes and hidden slides, and flags Thai AI-addressed words; fix loop with stop condition, 5-round cap and status lines; stage labels and level summary for the graded chat; `PROMPT.md` with Level 5 prompts.
- **1.0** (2026-11-16): first release.

## License

[MIT](LICENSE). Use, change and share it freely; keep the copyright notice.
