# Mock exam: wastewater COD compliance

A timed practice task for the skill, with planted traps and a known answer key. Use it to see how the exam model (Sonnet) behaves before the real exam.

## How to run it

1. Start a **new chat with Sonnet**, with the skill switched on. Set a 45-minute timer.
2. Attach every file in [`files/`](files) and send Prompt 1 from [`../PROMPT.md`](../PROMPT.md).
3. Work as in the exam: run the cells in Jupyter, paste back, answer the questions.
4. When Claude asks about something the files do not settle, open [`INVIGILATOR.md`](INVIGILATOR.md) and give **only** the answer to that question. If Claude never asks, do not volunteer it; that is a finding.
5. Do not open `KEY.md` or `key.csv` until you are done.

## How to score it

```
python check.py path/to/output/answers.csv
```

It prints the score out of 18 rows and which rows are wrong, like the course's checker sites. Then open [`KEY.md`](KEY.md) and tick off the 14 traps: which did Claude catch, which did it ask about, which did it miss?

Write down what Sonnet skipped (stage labels, the loop status line, the injection alert, the doubt list). Those are the parts of `SKILL.md` to tighten.

`make_mock.py` rebuilds the files and the key (needs `openpyxl` and `python-docx`).
