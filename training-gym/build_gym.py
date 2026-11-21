"""Rebuild every training environment and its hidden key. Deterministic: the same files every time.

    python build_gym.py            # all environments
    python build_gym.py E1 E5      # only these
"""
import importlib
import shutil
import sys
from pathlib import Path

GYM = Path(__file__).resolve().parent
sys.path.insert(0, str(GYM / "src"))
MODULES = ["e1_closure", "e2_batches", "e3_boiler", "e4_triage", "e5_regression", "rack"]

if __name__ == "__main__":
    want = [a.upper() for a in sys.argv[1:]]
    for name in MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name != name:
                raise
            continue
        if want and not any(mod.ENV.upper().startswith(w) for w in want):
            continue
        exam = GYM / "envs" / mod.ENV / "exam"
        key = GYM / "keys" / mod.ENV
        for d in (exam, key):
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True)
        info = mod.build(exam, key)
        print(f"built {mod.ENV}: {len(list(exam.iterdir()))} exam files | {info}")
