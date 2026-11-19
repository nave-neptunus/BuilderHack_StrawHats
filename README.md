# StrawHats: Builders Buildathon (Nov 20 to 22, 2026)

Prep notes and track guesses are in `docs/research.md`.

```bash
pip install -r requirements.txt
```

```bash
pytest
```

```bash
python -m baselines.rwx_triage data/logs out.csv --llm
```

```bash
python -m harness.local_eval out.csv data/labels.csv --notes "regex v1"
```

```bash
python -m harness.submit out.csv --track rwx --notes "regex v1"
```

Every local eval and submission adds a row to `harness/log.csv`. LLM calls are cached in `.cache/llm`. In the cloud environment, the proxy injects the Groq key, so `GROQ_API_KEY` can stay unset.
