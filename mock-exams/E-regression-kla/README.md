# Mock exam E: a regression model for kLa

A timed practice task for the week 5 topic (machine learning): choose a model, train it, predict new conditions. It has planted traps and a known answer key.

## How to run it

1. Start a **new chat with Sonnet**, with the skill switched on. Set a 45-minute timer.
2. Attach every file in [`files/`](files) and send your own prompt (Role, Task, Context in tags, Format, Example, Constraints), or only the task so that the skill drafts the prompt for you to edit and send. End it with "Tell me the model we are using and the current time." and screenshot your prompt, as in the real exam.
3. Work as in the exam: run the cells in VS Code, paste back, answer the questions.
4. When Claude asks about something the files do not settle, open [`INVIGILATOR.md`](INVIGILATOR.md) and give **only** the answer to that question.
5. Do not open `KEY.md`, `key*.csv` or `verify_solution.py` until you are done.

## How to score it

```
python check.py path/to/output/scores.csv path/to/output/predictions.csv
```

It checks that all 11 models are scored, that your table picks the right model, the winner's Test RMSE and MAPE, and the six predictions (within 2 %). Then open [`KEY.md`](KEY.md) and tick off the traps.

`make_mock.py` rebuilds the files and the key (needs `numpy`, `openpyxl`, `python-docx`). `verify_solution.py` is a second solution written with scikit-learn from the raw files; it reproduces the key.
