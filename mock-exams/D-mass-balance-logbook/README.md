# Mock exam D: hourly mass balance of SRU-1 (task type D, hourly logs judged with a logbook)

A timed practice task for the skill, with planted traps and a known answer key. Use it to see how the exam model (Sonnet) behaves before the real exam.

## How to run it

1. Start a **new chat with Sonnet**, with the skill switched on. Set a **45-minute timer**.
2. Attach every file in [`files/`](files) and send your own prompt (Role, Task, Context in tags, Format, Example, Constraints), or only the task so that the skill drafts the prompt for you to edit and send.
3. Work as in the exam: run the cells in Jupyter, paste back, answer the questions.
4. When Claude asks about something the files do not settle, open [`INVIGILATOR.md`](INVIGILATOR.md) and give **only** the answer to that question. If Claude never asks, do not volunteer it; that is a finding.
5. Do not open `KEY.md`, `key.csv`, `key_daily.csv` or `verify_solution.py` until you are done.

## How to score it

```
python check.py path/to/output/hourly.csv path/to/output/daily.csv
```

It prints the score out of 96 hourly rows and 4 daily rows, and which rows are wrong. The note (`output/note.txt`) and the chart are checked by eye against the list in [`KEY.md`](KEY.md). Then tick off the traps.

`make_mock.py` rebuilds the files and the keys (needs `openpyxl` and `python-docx`). `verify_solution.py` is a second solution written from the files, the handout and the logbook only; it must print `hourly matched 96 of 96 | daily matched 4 of 4`.
