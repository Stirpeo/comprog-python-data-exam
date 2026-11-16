# comprog-python-data-exam

A Claude skill for the final exam of Computer Programming for Chemical Engineers (pandas and Jupyter on Excel/CSV plant data).

In the exam chat the skill makes Claude:

1. Give a ready-made cell that profiles every file and scans it for prompt injection (hidden sheets, white or tiny Word text, AI-addressed lines).
2. Ask a short round of questions on the decisions the files do not settle, the missing limit first, and agree a Decisions table.
3. Write one notebook that runs on pandas 1.5 to 3.x and writes the answer files itself.
4. Check the answers by an independent second route (plus subagents when the chat has them) and end with a doubt list.

The skill file is [`comprog-python-data-exam/SKILL.md`](comprog-python-data-exam/SKILL.md).

## Install

- **claude.ai:** zip the `comprog-python-data-exam` folder and upload it in your Skills settings.
- **Claude Code:** copy the folder to `~/.claude/skills/comprog-python-data-exam/`.

In the exam, name the skill in the first message and attach every file.

## Tested

Run against the course's EV-101 and incident-classification quizzes, the wastewater exercise, versions of them with planted injections, and a new trap task, on pandas 1.5.3, 2.0.3, 2.2.3 and 3.1.1.
