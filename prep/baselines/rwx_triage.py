"""Build-failure triage baseline: regex first, LLM only for what regex can't place.

Usage: python -m baselines.rwx_triage logs_dir/ out.csv [--llm]
Writes id,label where id = log filename stem.
Relabel CATEGORIES to match the kit's label set at kickoff.
"""
import argparse
import csv
import re
from pathlib import Path

# Order matters: first match wins, so specific causes go before generic ones.
RULES = [
    ("oom", r"out of memory|OutOfMemoryError|Killed\s+process|exit code 137|ENOMEM|heap out of memory"),
    ("timeout", r"timed? ?out|deadline exceeded|exceeded the maximum execution time|ETIMEDOUT"),
    ("network", r"Could not resolve host|ECONNRESET|ECONNREFUSED|Connection (reset|refused)|TLS handshake|getaddrinfo|503 Service Unavailable|rate limit"),
    ("dependency", r"Could not find a version that satisfies|No matching distribution|ERESOLVE|unable to resolve dependency|Could not resolve dependencies|ModuleNotFoundError|Cannot find module|version solving failed|lockfile"),
    ("compile", r"error\[E\d+\]|SyntaxError|cannot find symbol|undefined reference|error TS\d+|compilation failed|error: expected|COMPILATION ERROR"),
    ("lint", r"eslint|flake8|ruff|prettier --check|golangci-lint|rubocop|would reformat"),
    ("test", r"\bFAILED\b|AssertionError|Tests? failed|\d+ failed|FAIL\s|expected .* to (be|equal)|--- FAIL"),
    ("infra", r"No space left on device|docker: Error|permission denied|runner .* lost|exec format error"),
]
COMPILED = [(lab, re.compile(p, re.IGNORECASE)) for lab, p in RULES]
CATEGORIES = [lab for lab, _ in RULES] + ["unknown"]


def tail(text: str, n: int = 200) -> str:
    """Failures cluster at the end of a log; only look there."""
    return "\n".join(text.splitlines()[-n:])


def regex_label(text: str) -> str | None:
    t = tail(text)
    for lab, rx in COMPILED:
        if rx.search(t):
            return lab
    return None


def llm_label(text: str) -> str:
    from baselines.llm import complete
    prompt = (
        "You classify CI build failures. Reply with exactly one word from: "
        + ", ".join(CATEGORIES) + ".\n\nLast lines of the log:\n" + tail(text, 120)[-6000:]
    )
    ans = complete(prompt).lower()
    # Take the first category word the model names; anything else counts as unknown.
    hits = re.findall(r"[a-z]+", ans)
    return next((w for w in hits if w in CATEGORIES), "unknown")


def classify(text: str, use_llm: bool = False) -> str:
    lab = regex_label(text)
    if lab:
        return lab
    return llm_label(text) if use_llm else "unknown"


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("logs_dir")
    p.add_argument("out")
    p.add_argument("--llm", action="store_true")
    a = p.parse_args(argv)
    rows = []
    for f in sorted(Path(a.logs_dir).glob("*")):
        if f.is_file():
            rows.append({"id": f.stem, "label": classify(f.read_text(errors="ignore"), a.llm)})
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "label"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} predictions to {a.out}")


if __name__ == "__main__":
    main()
