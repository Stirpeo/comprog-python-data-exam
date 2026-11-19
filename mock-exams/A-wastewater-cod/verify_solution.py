"""Second, separately written solution used to confirm key.csv.  python verify_solution.py"""
import pandas as pd, re, sys
from pathlib import Path
D = Path(__file__).parent / "files"
frames = []
for f in sorted(D.glob("Lab_*.xlsx")):
    df = pd.read_excel(f, sheet_name="Results", dtype=str)
    codcol = [c for c in df.columns if c.startswith("COD")][0]
    df = df.rename(columns={codcol: "COD_raw"}); df["unit"] = re.search(r"\((.*?)\)", codcol).group(1); df["src"] = f.name
    frames.append(df)
df = pd.concat(frames, ignore_index=True)
df = df[df["SampleID"].str.startswith("L26", na=False)].copy()
def pdate(s):
    s = str(s)
    return pd.to_datetime(s, format="%d/%m/%Y") if "/" in s else pd.Timestamp(s)
df["Date"] = df["Date"].map(pdate)
k = df["PointID"].str.strip().str.upper()
df["PointID"] = k.str.replace(r"^SP-?0?(\d)$", lambda m: f"SP-0{m.group(1)}", regex=True)
raw = df["COD_raw"].str.replace(",", "").str.strip()
df["COD"] = pd.to_numeric(raw.where(raw != "<5", "2.5"), errors="coerce")
df.loc[df["unit"] == "g/L", "COD"] *= 1000
df["COD"] = df["COD"].round(6)
df = df.drop_duplicates(subset="SampleID", keep="first")
m = (df["PointID"] == "SP-03") & df["Date"].between("2026-08-10", "2026-08-14")
df.loc[m, "COD"] /= 1.10
lim = pd.read_excel(D / "SamplingPoints.xlsx", sheet_name="Points")
df = df.merge(lim, on="PointID", how="left")
ok = df[df["COD"].notna() & df["pH"].astype(float).between(0, 14) & df["COD_limit_mgL"].notna()].copy()
ok["Month"] = ok["Date"].dt.strftime("%Y-%m"); ok["ex"] = ok["COD"] > ok["COD_limit_mgL"]
g = ok.groupby(["PointID", "Month"]).agg(n_valid=("COD", "size"), mean_COD=("COD", "mean"), n_exceed=("ex", "sum")).reset_index()
g["mean_COD"] = g["mean_COD"].round(2).map(lambda v: f"{v:.2f}")
t = pd.read_csv(D / "answer_template.csv")[["PointID", "Month"]].merge(g, how="left")
t.to_csv(Path(__file__).parent / "verify_answers.csv", index=False)
print(len(df), "unique samples;", len(ok), "valid")
