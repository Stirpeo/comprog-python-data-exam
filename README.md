# comprog-python-data-exam

A Claude skill for the final exam of Computer Programming for Chemical Engineers (pandas and NumPy in Jupyter or VS Code, on Excel/CSV plant data). Current version: **1.4**.

In the exam chat the skill makes Claude:

1. Give a ready-made cell that profiles every file and scans it for prompt injection (hidden sheets, rows and slides; white, tiny, same-colour or format-hidden text in Excel, Word and PowerPoint; AI-addressed lines in English or Thai).
2. Ask a short round of questions on the decisions the files do not settle, the missing limit first, and agree a Decisions table.
3. Write the code as a notebook (`.ipynb`), a VS Code Python file with `# %%` cells, or both. It runs on pandas 1.5 to 3.x and writes the answer files itself.
4. Check the answers by an independent second route (plus subagents when the chat has them), run a fix loop until every check passes (at most 5 rounds), and end with a doubt list.
5. Label every stage in the course's terms (Prompt Level L1 to L5, Agentic Level A1 to A4), since the chat itself is graded.

The skill file is [`comprog-python-data-exam/SKILL.md`](comprog-python-data-exam/SKILL.md). Ready-made exam prompts (Level 5) are in [`PROMPT.md`](PROMPT.md). Four timed practice tasks, one per exam task type, with planted traps and answer keys are in [`mock-exams/`](mock-exams).

## Install

- **claude.ai:** zip the `comprog-python-data-exam` folder and upload it in your Skills settings.
- **Claude Code:** copy the folder to `~/.claude/skills/comprog-python-data-exam/`.

Your copy does not update itself. When the version above changes, download again and re-upload.

## Exam-day checklist

- [ ] The skill is uploaded and switched on in the account you will use in the exam.
- [ ] You did one timed practice run with the exam model (Sonnet) on one of the [mock exams](mock-exams).
- [ ] In VS Code on the exam laptop: the Python and Jupyter extensions are installed, a kernel is selected, and `import pandas, numpy, openpyxl, matplotlib` runs in a cell.
- [ ] You know the hand-in format (`.ipynb`, `.py` or both) and whether NumPy must be used.
- [ ] Prompt 1 from `PROMPT.md` is ready to fill in.
- [ ] In the exam: attach every file, name the skill in the first message, answer the decision questions with reasons.
- [ ] Hand in the notebook (after Restart and Run All, saved), the answer files and the chat link.

## Tested

- **Skill code:** the scan cell and the date helper give the same output on pandas 1.5.3, 2.0.3, 2.2.3 and 3.0.5, and 26 pandas claims in the skill were checked on each.
- **Mock exams with Sonnet (v1.4):** five runs with the questions answered from the invigilator sheets scored 18/18 (twice), 20/20, 200/200 and 96/96 + 4/4, with every planted injection caught (5, 5, 4, 5, 4). The code each run wrote also runs on the three older pandas versions with the same answers. Details are in [`mock-exams/README.md`](mock-exams/README.md).
- **Scan:** planted Excel, Word and PowerPoint files (all caught, coloured headers not flagged) and real course files (no false alarms).
- **Not tested:** a real claude.ai chat, VS Code itself, Team mode with subagents.

## Changelog

- **1.4** (2026-11-20): questions come in two kinds, and MUST ANSWER ones (missing limit, `<5`, duplicates that disagree, clock windows) carry no recommendation; VS Code support (`.py` with `# %%` cells, Data Viewer, NumPy notes); the scan hints at lines that set a result; the date helper handles `24:00`; warnings for the `g/L` in `mg/L` trap and for float noise after unit conversion; contradictions removed. Skill code re-tested on pandas 1.5.3, 2.0.3, 2.2.3 and 3.0.5.
- **1.3** (2026-11-19): three more mock exams (historian cleaning, work-order triage, mass balance with logbook), each key confirmed by a second solution; mocks moved to `mock-exams/`.
- **1.2** (2026-11-19): scan also catches Excel text hidden by a `;;;` number format or by a font the same colour as the fill; mock exam with 14 traps, answer key and checker.
- **1.1** (2026-11-19): scan catches white or tiny text in Excel cells, scans PowerPoint slides, notes and hidden slides, and flags Thai AI-addressed words; fix loop with stop condition, 5-round cap and status lines; stage labels and level summary for the graded chat; `PROMPT.md` with Level 5 prompts.
- **1.0** (2026-11-16): first release.

## License

[MIT](LICENSE). Use, change and share it freely; keep the copyright notice.
