# Mock exam C: triage of maintenance work orders (task type C, classifying text by written rules)

A timed practice task for the skill, with planted traps and a known answer key. Use it to see how the exam model (Sonnet) behaves before the real exam. It is built like the course's incident-classification quiz, in a new domain.

## How to run it

1. Start a **new chat with Sonnet**, with the skill switched on. Set a **45-minute timer**.
2. Attach every file in [`files/`](files) and send your own prompt (Role, Task, Context in tags, Format, Example, Constraints), or only the task so that the skill drafts the prompt for you to edit and send.
3. Work as in the exam: run the cells in Jupyter, paste back, answer the questions.
4. When Claude asks about something the files do not settle, open [`INVIGILATOR.md`](INVIGILATOR.md) and give **only** the answer to that question. If Claude never asks, do not volunteer it; that is a finding.
5. Do not open `KEY.md`, `key.csv`, `key_patterns.csv` or `verify_solution.py` until you are done.

## How to score it

```
python check.py path/to/output/answers.csv
```

It prints the score out of 200 rows (both columns right), the type and urgency scores separately, and which rows are wrong. Then open [`KEY.md`](KEY.md) and tick off the traps. `key_patterns.csv` shows the sentence pattern behind every work order, which helps to see *why* a row went wrong.

`make_mock.py` rebuilds the files and the key (needs `openpyxl` and `python-docx`). `verify_solution.py` is a second solution: a rule function written from the handout that reads only the text; it must print `worked examples: 4 of 4 pass` and `matched 200 of 200`.
