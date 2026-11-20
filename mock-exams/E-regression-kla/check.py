"""Score mock exam E.  python check.py output/scores.csv output/predictions.csv"""
import csv, sys
from pathlib import Path
if len(sys.argv) != 3: sys.exit("usage: python check.py path/to/scores.csv path/to/predictions.csv")
H = Path(__file__).parent
def rows(p):
    with open(p, newline="", encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def num(v):
    try: return float(v)
    except (TypeError, ValueError): return None
key = {r["Case"]: float(r["kLa_pred"]) for r in rows(H / "key.csv")}; km = rows(H / "key_model.csv")[0]
sc = rows(sys.argv[1]); pr = {r["Case"].strip().upper(): num(r.get("kLa_pred")) for r in rows(sys.argv[2])}
NEED = ["Linear", "Poly2", "Poly3", "Poly4", "Power", "Exponential", "Logarithmic", "Ridge", "Lasso", "kNN", "RandomForest"]
norm = lambda s: "".join(ch for ch in s.lower() if ch.isalnum())
have = {norm(r["Model"]): r for r in sc}
missing = [m for m in NEED if norm(m) not in have or num(have[norm(m)].get("Test_RMSE")) is None]
print("Scores table: all 11 models scored" if not missing else f"Scores table: missing or blank -> {missing}")
ranked = sorted((r for r in sc if num(r.get("Test_RMSE")) is not None), key=lambda r: num(r["Test_RMSE"]))
best = ranked[0]["Model"] if ranked else "none"
print(f"Best model by lowest Test RMSE in your table: {best}  ->", "correct" if norm(best) == "power" else "WRONG")
p = have.get("power"); rm = num(p.get("Test_RMSE")) if p else None; k = float(km["test_RMSE"])
print("Power Test RMSE:", rm, "->", "correct" if rm is not None and abs(rm - k) <= 0.05 * k else "WRONG (data cleaning or split differs)")
mp = num(p.get("Test_MAPE_pct")) if p else None
print("Power Test MAPE in %:", mp, "->", "correct" if mp is not None and 1.0 <= mp <= 3.0 else "WRONG (fraction instead of %, or data differs)")
good = 0
for case, v in key.items():
    got = pr.get(case); ok = got is not None and abs(got - v) <= 0.02 * v
    good += ok
    if not ok: print(f"  wrong prediction: case {case} -> {got}")
print(f"Predictions correct (within 2 %): {good} of {len(key)}")
