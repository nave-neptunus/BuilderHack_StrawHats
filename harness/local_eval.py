"""Score predictions against labels locally. Swap `metric` once the kit publishes the real rule.

Usage: python -m harness.local_eval preds.csv labels.csv [--track rwx] [--notes "..."]
Both CSVs need columns: id,label
"""
import argparse
import csv

from harness.log import record


def load(path):
    with open(path, newline="") as f:
        return {r["id"]: r["label"].strip().lower() for r in csv.DictReader(f)}


def accuracy(preds: dict, labels: dict) -> float:
    if not labels:
        return 0.0
    return sum(preds.get(k) == v for k, v in labels.items()) / len(labels)


metric = accuracy


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("preds")
    p.add_argument("labels")
    p.add_argument("--track", default="rwx")
    p.add_argument("--notes", default="local")
    a = p.parse_args(argv)
    labels, preds = load(a.labels), load(a.preds)
    score = metric(preds, labels)
    misses = [k for k, v in labels.items() if preds.get(k) != v]
    print(f"score={score:.4f}  n={len(labels)}  misses={len(misses)}")
    for k in misses[:20]:
        print(f"  {k}: got={preds.get(k)!r} want={labels[k]!r}")
    record(a.track, round(score, 4), f"local: {a.notes}")
    return score


if __name__ == "__main__":
    main()
