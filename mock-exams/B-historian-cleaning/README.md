# Mock exam B: historian data of column C-201 (task type B, cleaning plus charts)

A timed practice task for the skill, with planted traps and a known answer key. Use it to see how the exam model (Sonnet) behaves before the real exam.

## How to run it

1. Start a **new chat with Sonnet**, with the skill switched on. Set a **45-minute timer**.
2. Attach every file in [`files/`](files) and send your own prompt (Role, Task, Context in tags, Format, Example, Constraints), or only the task so that the skill drafts the prompt for you to edit and send.
3. Work as in the exam: run the cells in Jupyter, paste back, answer the questions.
4. When Claude asks about something the files do not settle, open [`INVIGILATOR.md`](INVIGILATOR.md) and give **only** the answer to that question. If Claude never asks, do not volunteer it; that is a finding.
5. Do not open `KEY.md`, `key.csv` or `verify_solution.py` until you are done.

## How to score it

```
python check.py path/to/output/answers.csv
```

It prints the score out of 20 rows and which rows are wrong. Then open [`KEY.md`](KEY.md) and tick off the traps: which did Claude catch, which did it ask about, which did it miss? Check the two charts by eye against the handout's chart sentences.

`make_mock.py` rebuilds the files and the key (needs `openpyxl` and `python-docx`). `verify_solution.py` is a second solution written from the files and the handout only; it must print `matched 20 of 20`.
