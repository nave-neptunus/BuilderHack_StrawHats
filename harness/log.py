"""Append one row per submission so we can tell which change moved the score."""
import csv
import datetime as dt
import subprocess
from pathlib import Path

LOG = Path(__file__).with_name("log.csv")
FIELDS = ["time", "git_sha", "track", "score", "notes"]


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "nogit"


def record(track: str, score, notes: str = "", path: Path = LOG) -> dict:
    new = not path.exists()
    row = {"time": dt.datetime.now().isoformat(timespec="seconds"), "git_sha": git_sha(),
           "track": track, "score": score, "notes": notes}
    with path.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    return row
