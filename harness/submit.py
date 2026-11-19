"""Submit predictions to the official grader. Endpoint and format get filled in from the kit at kickoff.

Usage: SUBMIT_URL=... TEAM_TOKEN=... python -m harness.submit preds.csv --track rwx --notes "regex v2"
"""
import argparse
import os

import requests
from dotenv import load_dotenv

from harness.log import record


def main(argv=None):
    load_dotenv()
    p = argparse.ArgumentParser()
    p.add_argument("file")
    p.add_argument("--track", default="rwx")
    p.add_argument("--notes", default="")
    a = p.parse_args(argv)
    url = os.environ.get("SUBMIT_URL")
    if not url:
        raise SystemExit("SUBMIT_URL not set. Fill it in from the challenge kit.")
    headers = {"Authorization": f"Bearer {os.environ.get('TEAM_TOKEN', '')}"}
    with open(a.file, "rb") as f:
        r = requests.post(url, headers=headers, files={"file": f}, timeout=120)
    print(r.status_code, r.text[:2000])
    score = None
    if r.headers.get("content-type", "").startswith("application/json"):
        score = r.json().get("score")
    record(a.track, score, f"submit {r.status_code}: {a.notes}")


if __name__ == "__main__":
    main()
