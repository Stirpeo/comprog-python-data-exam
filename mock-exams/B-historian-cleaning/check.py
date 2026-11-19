"""Score an answer file against the mock B key.  python check.py output/answers.csv"""
import csv, sys
from pathlib import Path
TOL = {"TI_mean": 0.005, "FI_mean": 0.005, "TI_std": 0.0005}       # counts must be exact
def load(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return {(r["Question"].strip(), r["Key"].strip()): r.get("Value", "") for r in csv.DictReader(f)}
if len(sys.argv) != 2: sys.exit("usage: python check.py path/to/answers.csv")
key, ans = load(Path(__file__).parent / "key.csv"), load(sys.argv[1])
def same(q, a, b):
    try: return abs(float(a) - float(b)) <= TOL.get(q, 1e-9) + 1e-12
    except (TypeError, ValueError): return False
wrong = [(k, "row missing" if k not in ans else f"got {ans[k]!r}") for k in key if k not in ans or not same(k[0], ans[k], key[k])]
print(f"Correct rows: {len(key) - len(wrong)} of {len(key)}")
for k, why in wrong: print("  wrong:", k[0], k[1], "->", why)
extra = [k for k in ans if k not in key]
if extra: print("  rows not in the template:", extra)
