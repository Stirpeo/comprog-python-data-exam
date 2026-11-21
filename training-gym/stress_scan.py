"""Stress test of the skill's own profile-and-scan cell: run it, unchanged, on every gym folder.

    python stress_scan.py [path to SKILL.md]      (default: the skill beside this folder, else the installed one)

It answers two questions: does the cell run on this laptop without an error, and which planted
instructions does it flag with a `!!` line. Results go to stress_scan_report.txt.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GYM = Path(__file__).resolve().parent


def skill_cell(path):
    if path is None:
        # in the repository the skill sits beside this folder; on a laptop it is in the Claude skills folder
        hits = [GYM.parent / "comprog-python-data-exam" / "SKILL.md"]
        hits = [h for h in hits if h.exists()] or sorted(Path.home().glob(".claude/skills/**/comprog-python-data-exam/SKILL.md"), key=lambda p: p.stat().st_mtime)
        if not hits:
            sys.exit("SKILL.md not found: pass its path as the first argument")
        path = hits[-1]
    text = Path(path).read_text(encoding="utf-8")
    cell = re.search(r"## The profile and scan cell.*?```python\n(.*?)```", text, flags=re.S).group(1)
    version = re.search(r"Version ([\d.]+)", text)
    return cell, (version.group(1) if version else "?"), path


def run_cell(cell, folder: Path):
    """Run the cell in a throw-away copy of the folder, so the exam folder stays as the student gets it."""
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "exam"
        shutil.copytree(folder, work)
        (Path(tmp) / "cell.py").write_text(cell, encoding="utf-8")
        p = subprocess.run([sys.executable, "-X", "utf8", str(Path(tmp) / "cell.py")], cwd=work, capture_output=True, text=True, encoding="utf-8")
        return p.stdout, p.stderr, p.returncode


def sections(out):
    """Output lines grouped under the file they belong to."""
    sec, cur = {}, None
    for ln in out.splitlines():
        m = re.match(r"FILE (.+?) \|", ln)
        if m:
            cur = m.group(1)
        sec.setdefault(cur, []).append(ln)
    return sec


if __name__ == "__main__":
    cell, version, path = skill_cell(sys.argv[1] if len(sys.argv) > 1 else None)
    R = [f"Scan cell from skill v{version}", ""]
    total = caught = 0
    for env in sorted(p for p in (GYM / "envs").iterdir() if (GYM / "keys" / p.name / "key.json").exists()):
        out, err, code = run_cell(cell, env / "exam")
        flags = [ln for ln in out.splitlines() if "!!" in ln]
        R.append(f"== {env.name}: exit code {code}, {len(flags)} flag lines" + (f"\n   STDERR: {err.strip()[-300:]}" if code else ""))
        R += [f"   could not scan: {ln.strip()}" for ln in out.splitlines() if "could not be scanned" in ln]
        key = json.loads((GYM / "keys" / env.name / "key.json").read_text(encoding="utf-8"))
        hit = set()
        for inj in key["injections"]:
            total += 1
            if any(inj["needle"] in ln for ln in flags):
                verdict = "FLAGGED"; caught += 1
            elif inj["needle"] in out:
                verdict = "printed in the profile, NOT flagged"
            else:
                verdict = "NOT in the scan output at all"
            hit |= {ln for ln in flags if inj["needle"] in ln}
            R.append(f"   {verdict:38s} | {inj['how']} | {inj['where']}")
        R.append(f"   other flag lines (false alarms or structure notes): {len(set(flags) - hit)}")
        R += [f"      {ln.strip()[:150]}" for ln in sorted(set(flags) - hit)[:8]]
        R.append("")
    R.insert(1, f"Planted injections in the five environments flagged by the cell: {caught} of {total}")

    rack = GYM / "envs" / "scanner_rack" / "exam"
    if rack.exists():
        out, err, code = run_cell(cell, rack)
        sec = sections(out)
        man = json.loads((GYM / "keys" / "scanner_rack" / "manifest.json").read_text(encoding="utf-8"))
        R.append(f"== scanner_rack: exit code {code}. One probe per hiding technique; the planted line has no AI word in it.")
        miss = []
        for p in man["probes"]:
            lines = sec.get(p["file"], [])
            if p["kind"] == "format":
                flagged = any("!!" in ln for ln in lines)
            else:
                flagged = any("!!" in ln and f":: {p['id']} |" in ln for ln in lines)
            if p["kind"] == "harmless line":
                verdict = "false alarm" if flagged else "quiet (right)"
            else:
                verdict = "flagged" if flagged else "MISSED"
                if not flagged:
                    miss.append(p)
            R.append(f"   {p['id']} {verdict:14s} | {p['kind']:17s} | {'by hand ' if p['by_hand'] else 'needs code'} | {p['how']}")
        R += ["", f"   Missed {len(miss)} of {sum(1 for p in man['probes'] if p['kind'] != 'harmless line')} hiding probes. "
                  f"Missed ones a teacher can make by hand in Office: {', '.join(p['id'] for p in miss if p['by_hand'])}"]
    text = "\n".join(R)
    (GYM / "stress_scan_report.txt").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)
