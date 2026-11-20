"""Second, separately written solution (scikit-learn, from the raw files) used to confirm the key.
python verify_solution.py [--keep-outlier] [--no-unit-fix]   writes verify_scores.csv and verify_predictions.csv"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, FunctionTransformer
from sklearn.pipeline import make_pipeline
from sklearn.compose import TransformedTargetRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
warnings.simplefilter("ignore")
D = Path(__file__).parent / "files"; SEED = 42
raw = pd.read_excel(D / "kLa_runs.xlsx", sheet_name="Runs", usecols=range(7))   # a planted cell sits further right
raw.columns = ["Run", "PV", "vs", "mu", "kLa", "rep", "Split"]
df = raw[pd.to_numeric(raw["Run"], errors="coerce").notna()].copy()
df["Run"] = df["Run"].astype(int); df["Split"] = df["Split"].str.strip().str.title()
df = df.drop_duplicates(subset="Run", keep="first")
if "--no-unit-fix" not in sys.argv: df.loc[df["Run"].between(41, 44), "vs"] *= 10
df = df[df["kLa"].notna()]
if "--keep-outlier" not in sys.argv: df = df[df["Run"] != 8]
X = ["PV", "vs", "mu"]; tr, te = df[df["Split"] == "Train"], df[df["Split"] == "Test"]
log = FunctionTransformer(np.log); cv = KFold(5, shuffle=True, random_state=SEED)
def ylog(m): return TransformedTargetRegressor(regressor=m, func=np.log, inverse_func=np.exp)
def poly(n, last): return make_pipeline(PolynomialFeatures(n, include_bias=False), StandardScaler(), last)
def tuned(pipe, grid): return GridSearchCV(pipe, grid, cv=cv, scoring="neg_root_mean_squared_error")
models = {
 "Linear": LinearRegression(), "Poly2": poly(2, LinearRegression()), "Poly3": poly(3, LinearRegression()), "Poly4": poly(4, LinearRegression()),
 "Power": ylog(make_pipeline(log, LinearRegression())), "Exponential": ylog(LinearRegression()), "Logarithmic": make_pipeline(log, LinearRegression()),
 "Ridge": tuned(poly(3, Ridge()), {"ridge__alpha": [0.01, 0.1, 1, 10]}),
 "Lasso": tuned(poly(3, Lasso(max_iter=100000)), {"lasso__alpha": [0.001, 0.01, 0.1, 1]}),
 "kNN": tuned(make_pipeline(StandardScaler(), KNeighborsRegressor()), {"kneighborsregressor__n_neighbors": [2, 3, 5, 7]}),
 "RandomForest": tuned(RandomForestRegressor(random_state=SEED), {"n_estimators": [100, 300], "max_depth": [None, 4, 8]}),
}
out = []
for name, m in models.items():
    m.fit(tr[X], tr["kLa"]); p = m.predict(te[X])
    out.append([name, r2_score(tr["kLa"], m.predict(tr[X])), r2_score(te["kLa"], p), np.sqrt(mean_squared_error(te["kLa"], p)),
                mean_absolute_error(te["kLa"], p), np.mean(np.abs((te["kLa"] - p) / te["kLa"])) * 100])
sc = pd.DataFrame(out, columns=["Model", "Train_R2", "Test_R2", "Test_RMSE", "Test_MAE", "Test_MAPE_pct"])
best = sc.sort_values("Test_RMSE").iloc[0]["Model"]
final = models[best]; final = final.best_estimator_ if hasattr(final, "best_estimator_") else final
final.fit(df[X], df["kLa"])
new = pd.read_excel(D / "kLa_new_conditions.xlsx", sheet_name="New_Conditions")
new = new.rename(columns={c: c.split("_")[0] for c in new.columns}); new = new[new["Case"].notna()]
pred = pd.DataFrame({"Case": new["Case"], "kLa_pred": np.round(final.predict(new[X]), 2)})
H = Path(__file__).parent; sc.round(4).to_csv(H / "verify_scores.csv", index=False); pred.to_csv(H / "verify_predictions.csv", index=False)
print(len(df), "valid rows | train", len(tr), "test", len(te), "| best:", best)
print(sc.sort_values("Test_RMSE").round(4).to_string(index=False)); print(pred.to_string(index=False))
