"""Score the answer files against the mock D key.  python check.py output/hourly.csv output/daily.csv"""
import csv, sys
from pathlib import Path
HERE = Path(__file__).parent
def load(p, k):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return {r[k].strip(): {c: (v or "").strip() for c, v in r.items()} for r in csv.DictReader(f)}
def num_same(a, b, tol=0.005):
    if a == "" or b == "": return a == b
    try: return abs(float(a) - float(b)) <= tol + 1e-9
    except ValueError: return False
if len(sys.argv) != 3: sys.exit("usage: python check.py path/to/hourly.csv path/to/daily.csv")
kh, ah = load(HERE / "key.csv", "Timestamp"), load(sys.argv[1], "Timestamp")
kd, ad = load(HERE / "key_daily.csv", "Date"), load(sys.argv[2], "Date")
wh = []
for t, r in kh.items():
    g = ah.get(t)
    if g is None: wh.append((t, "row missing")); continue
    bad = [c for c in ("closure_pct",) if not num_same(g.get(c, ""), r[c])] + (["status"] if g.get("status", "") != r["status"] else [])
    if bad: wh.append((t, ", ".join(f"{c} {g.get(c, '')!r} (key {r[c]!r})" for c in bad)))
wd = []
for d, r in kd.items():
    g = ad.get(d)
    if g is None: wd.append((d, "row missing")); continue
    bad = [c for c in ("hours_judged", "hours_flagged") if not num_same(g.get(c, ""), r[c], 1e-9)] + ([] if num_same(g.get("mean_closure", ""), r["mean_closure"]) else ["mean_closure"])
    if bad: wd.append((d, ", ".join(f"{c} {g.get(c, '')!r} (key {r[c]!r})" for c in bad)))
print(f"Hourly rows correct: {len(kh) - len(wh)} of {len(kh)}")
for t, why in wh: print("  wrong:", t, "->", why)
print(f"Daily rows correct: {len(kd) - len(wd)} of {len(kd)}")
for d, why in wd: print("  wrong:", d, "->", why)
