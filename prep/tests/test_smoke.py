from baselines.rwx_triage import classify
from harness.local_eval import accuracy
from harness.log import record


def test_regex_buckets():
    assert classify("step 3\nKilled process 1234 (node)\nexit code 137") == "oom"
    assert classify("npm ERR! code ERESOLVE\nunable to resolve dependency tree") == "dependency"
    assert classify("src/main.rs\nerror[E0308]: mismatched types") == "compile"
    assert classify("=== 2 failed, 40 passed in 3.1s ===") == "test"
    assert classify("curl: (6) Could not resolve host: example.com") == "network"
    assert classify("all good, nothing here") == "unknown"


def test_accuracy():
    assert accuracy({"a": "x", "b": "y"}, {"a": "x", "b": "z"}) == 0.5


def test_log(tmp_path):
    p = tmp_path / "log.csv"
    record("rwx", 0.5, "t", path=p)
    record("rwx", 0.6, "t2", path=p)
    assert p.read_text().count("\n") == 3
