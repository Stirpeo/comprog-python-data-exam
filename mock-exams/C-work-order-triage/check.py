"""Score an answer file against the mock C key.  python check.py output/answers.csv"""
import csv, sys
from pathlib import Path
def load(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return {r["id"].strip(): ((r.get("type") or "").strip(), (r.get("urgency") or "").strip()) for r in csv.DictReader(f)}
if len(sys.argv) != 2: sys.exit("usage: python check.py path/to/answers.csv")
key, ans = load(Path(__file__).parent / "key.csv"), load(sys.argv[1])
t_ok = sum(ans.get(k, ("", ""))[0] == v[0] for k, v in key.items())
u_ok = sum(ans.get(k, ("", ""))[1] == v[1] for k, v in key.items())
wrong = [(k, v, ans.get(k)) for k, v in key.items() if ans.get(k) != v]
print(f"Correct rows (type and urgency): {len(key) - len(wrong)} of {len(key)}   | type {t_ok}/{len(key)}  urgency {u_ok}/{len(key)}")
for k, v, got in wrong: print(f"  wrong: {k}  expected {v[0]}/{v[1]}  got", "row missing" if got is None else f"{got[0]}/{got[1]}")
extra = [k for k in ans if k not in key]
if extra: print("  rows not in the template:", extra)
