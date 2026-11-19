"""Score an answer file against the mock exam key.  python check.py output/answers.csv"""
import csv, sys
from pathlib import Path
def load(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return {(r["PointID"].strip().upper(), r["Month"].strip()): r for r in csv.DictReader(f)}
if len(sys.argv) != 2: sys.exit("usage: python check.py path/to/answers.csv")
key, ans = load(Path(__file__).parent / "key.csv"), load(sys.argv[1])
def same(col, a, b):
    try: return abs(float(a) - float(b)) < (0.005 if col == "mean_COD" else 1e-9)
    except (TypeError, ValueError): return False
wrong = []
for k, row in key.items():
    got = ans.get(k)
    bad = ["row missing"] if got is None else [c for c in ("n_valid", "mean_COD", "n_exceed") if not same(c, got.get(c), row[c])]
    if bad: wrong.append((k, bad))
print(f"Correct rows: {len(key) - len(wrong)} of {len(key)}")
for k, bad in wrong: print("  wrong:", k[0], k[1], "->", ", ".join(bad))
extra = [k for k in ans if k not in key]
if extra: print("  rows not in the template:", extra)
