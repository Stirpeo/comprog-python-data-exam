"""Shared helpers for the gym builders: Word files with hidden text, key files, trap sheets."""
import itertools
import json
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor

WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def _hide(run, hide):
    """hide: None, 'white' (white font), 'tiny' (1 pt), 'vanish' (Word hidden text)."""
    if hide == "white":
        run.font.color.rgb = WHITE
    elif hide == "tiny":
        run.font.size = Pt(1)
    elif hide == "vanish":
        run.font.hidden = True


def para(doc, text, style=None, bold=False, hide=None):
    p = doc.add_paragraph(style=style)
    r = p.add_run(text)
    r.bold = bold
    _hide(r, hide)
    return p


def runs(doc, parts, style=None):
    """One paragraph made of several runs: parts = [(text, hide), ...]."""
    p = doc.add_paragraph(style=style)
    for text, hide in parts:
        _hide(p.add_run(text), hide)
    return p


def table(doc, rows, header=True):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            cell.text = ""
            r = cell.paragraphs[0].add_run(str(val))
            r.bold = header and i == 0
    return t


def new_doc(title):
    doc = Document()
    doc.add_heading(title, level=1)
    return doc


def fmt(v, nd):
    """Fixed decimals, blank for missing."""
    if v is None or v != v:
        return ""
    return f"{round(float(v), nd):.{nd}f}"


def variant_grid(**axes):
    """All combinations of the named options, as (label, kwargs) pairs."""
    names = list(axes)
    for combo in itertools.product(*(axes[n] for n in names)):
        kw = dict(zip(names, combo))
        yield " | ".join(f"{k}={v}" for k, v in kw.items()), kw


def write_key(key_dir: Path, env, title, files, cells, teacher, variants, injections, traps, rulings, notes=""):
    """key.json for grade.py, plus the two sheets a student opens after (TRAPS) or during (RULINGS) a drill.

    variants: {label: full cells dict}. Only the cells that differ from the teacher key are stored.
    """
    key_dir.mkdir(parents=True, exist_ok=True)
    diffs = {}
    for label, vc in variants.items():
        d = {k: v for k, v in vc.items() if cells.get(k) != v}
        d.update({k: None for k in cells if k not in vc})
        diffs[label] = d
    (key_dir / "key.json").write_text(json.dumps(
        {"env": env, "title": title, "files": files, "teacher": teacher, "cells": cells,
         "variants": diffs, "injections": injections}, indent=1, ensure_ascii=False), encoding="utf-8")
    L = [f"# {env}: teacher's rulings", "",
         "Open this only as the invigilator would answer: read ONE answer, and only after you (or the AI)",
         "asked that exact question. Asking the right question is the skill being trained.", ""]
    for q, a in rulings:
        L += [f"**Q: {q}**", "", f"> {a}", ""]
    (key_dir / "RULINGS_ask_the_invigilator.md").write_text("\n".join(L), encoding="utf-8")
    L = [f"# {env}: what was planted (open after grading)", "", "## Prompt injections", ""]
    for n, inj in enumerate(injections, 1):
        L += [f"{n}. **{inj['where']}** ({inj['how']})", f"   - Text: \"{inj['text']}\"",
              f"   - Tries to: {inj['tries']}", ""]
    L += ["## Traps in the data and the wording", ""] + [f"- {t}" for t in traps]
    if notes:
        L += ["", "## Notes", "", notes]
    (key_dir / "TRAPS_open_after_grading.md").write_text("\n".join(L), encoding="utf-8")
