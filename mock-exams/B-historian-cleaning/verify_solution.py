"""Second, independent solution for mock B. Reads only files/ and uses the handout rules plus the
invigilator answers (modified z cut-off 3.5; a repeated stamp with different values keeps the first
copy; a bad value in one tag does not remove the row's other tags). Writes verify_answers.csv and
compares it with key.csv.   python verify_solution.py"""
import csv, io, sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).parent; F = HERE / "files"
MZ_CUT = 3.5                       # invigilator
FROZEN_MIN_ROWS = 6                # handout
BAD_CODE = -9999                   # handout

def read_csv_skip_comments(path):
    text = path.read_text(encoding="utf-8-sig").splitlines()
    keep = [ln for ln in text if ln.strip() and not ln.lstrip().startswith("#")]
    print(f"{path.name}: {len(text)} lines, {len(text) - len(keep)} non-data lines skipped")
    return pd.read_csv(io.StringIO("\n".join(keep)), dtype=str, keep_default_na=False)

frames = []
for i, name in enumerate(["C201_export_1.csv", "C201_export_2.csv"]):
    df = read_csv_skip_comments(F / name)
    out = pd.DataFrame({"t_utc": pd.to_datetime(df["Timestamp"].str.strip(), utc=True, format="ISO8601"),
                        "TI": df["TI201_degC"], "PI_kPa": df["PI201_kPa"], "FI": df["FI201_m3h"], "Status": df["Status"]})
    out["src"] = i; out["line"] = range(len(out)); frames.append(out)
x = pd.read_excel(F / "C201_export_3.xlsx", sheet_name="Export", dtype=object)
pi_bar = pd.to_numeric(x["PI201_bar"], errors="coerce")
out = pd.DataFrame({"t_utc": pd.to_datetime(x["Timestamp (UTC)"]).dt.tz_localize("UTC"), "TI": x["TI201_degC"],
                    "PI_kPa": (pi_bar * 100).round(1), "FI": x["FI201_m3h"], "Status": x["Status"]})
out["src"] = 2; out["line"] = range(len(out)); frames.append(out)
d = pd.concat(frames, ignore_index=True)

def num(s):
    v = pd.to_numeric(s.astype(str).str.strip().replace({"": None, "nan": None, "None": None}), errors="coerce")
    return v.where(v != BAD_CODE)
for c in ["TI", "PI_kPa", "FI"]: d[c] = num(d[c])
def state(s):
    s = str(s).strip().lower()
    if s.startswith("run"): return "Run"
    if s.startswith("shut"): return "Shutdown"
    if s.startswith("trip"): return "Trip"
    return "?" + s
d["state"] = d["Status"].map(state)
assert not d["state"].str.startswith("?").any(), d.loc[d["state"].str.startswith("?"), "Status"].unique()
d["t"] = d["t_utc"].dt.tz_convert("Asia/Bangkok").dt.tz_localize(None)

# duplicates: show which stamps disagree, then keep the first copy in file order
d = d.sort_values(["src", "line"])
grp = d.groupby("t")
nuniq = grp[["TI", "PI_kPa", "FI", "state"]].nunique(dropna=False)
print("stamps with more than one row:", int((grp.size() > 1).sum()), "| of which disagree:", list(nuniq[(nuniq > 1).any(axis=1)].index))
d = d.drop_duplicates("t", keep="first").sort_values("t").reset_index(drop=True)
print("unique stamps:", len(d), "steps:", d["t"].diff().value_counts().head(3).to_dict())

# frozen TI: runs of identical consecutive values (blank breaks a run)
run_id = (d["TI"] != d["TI"].shift()).cumsum()
run_len = d.groupby(run_id)["TI"].transform("size")
d["frozen"] = d["TI"].notna() & (run_len >= FROZEN_MIN_ROWS)
d["TI_ok"] = d["TI"].where(~d["frozen"])

d["day"] = d["t"].dt.date.astype(str)
days = ["2026-10-06", "2026-10-07", "2026-10-08"]
scope = d[d["day"].isin(days)]
runrows = scope[scope["state"] == "Run"]
ans = {}
for day in days:
    g = runrows[runrows["day"] == day]
    ans[("n_run", day)] = str(len(g))
    ans[("TI_mean", day)] = f"{g['TI_ok'].mean():.2f}"
    ans[("TI_std", day)] = f"{g['TI_ok'].std(ddof=1):.3f}"
    ans[("FI_mean", day)] = f"{g['FI'].mean():.2f}"
ans[("TI_frozen", "all")] = str(int(scope["frozen"].sum()))
p = runrows["PI_kPa"].dropna().to_numpy()
med = np.median(p); mad = np.median(np.abs(p - med))
m = 0.6745 * (p - med) / mad
ans[("PI_outliers", "all")] = str(int((np.abs(m) > MZ_CUT).sum()))
print("PI outliers at 3.0 / 3.5:", int((np.abs(m) > 3.0).sum()), int((np.abs(m) > 3.5).sum()))
edges = [76, 77, 78, 79, 80, 81, 82]
ti = runrows["TI_ok"].dropna()
assert ti.between(76, 82, inclusive="right").all()
cats = pd.cut(ti, edges, right=True)
counts = cats.value_counts().sort_index()
for iv, n in counts.items(): ans[("TI_hist", f"({int(iv.left)},{int(iv.right)}]")] = str(int(n))

with open(F / "answer_template.csv", newline="") as f: order = [(r["Question"], r["Key"]) for r in csv.DictReader(f)]
with open(HERE / "verify_answers.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Question", "Key", "Value"])
    for k in order: w.writerow([*k, ans[k]])
with open(HERE / "key.csv", newline="") as f: key = {(r["Question"], r["Key"]): r["Value"] for r in csv.DictReader(f)}
diff = [(k, key[k], ans.get(k)) for k in key if key[k] != ans.get(k)]
print(f"matched {len(key) - len(diff)} of {len(key)}")
for k, a, b in diff: print("  DIFF", k, "key", a, "second", b)
sys.exit(1 if diff else 0)
