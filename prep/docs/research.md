# Buildathon prep notes

Written Nov 19, the day before kickoff. The four track problems are still "to be announced" on [the event page](https://www.joinbuilders.org/buildathon). The kit drops at kickoff, so everything about the tracks below is a guess based on what each sponsor does.

## Confirmed from the page

- Kickoff: Nov 20, 6 PM, Evans Lab 1008. The challenge kit is released there.
- Close: Nov 22, 12 PM, Hitchcock Hall 131. Leaderboards freeze then.
- Build from anywhere in between. There's a live team chat.
- Four tracks: RWX, Builders, Machina, Databricks. $5,000 per track, winner takes all.
- No judges and no pitch. Each track has a published scoring rule, code runs on unseen test cases, and the leaderboard is public and updates live.
- The page's only scoring example: "Find the cause of a failed build: accuracy on the same 100 test cases, higher wins." The mock leaderboard is titled "Find what broke the build." Both point at RWX.
- Not on the page: team size, eligibility, LLM/tool rules, entering or switching tracks, submission rate limits. Contact: hi@joinbuilders.org.

## Tracks

### RWX (CI/CD platform)

The most likely task is classifying or locating the cause of a failed build from its logs, scored by accuracy. The pattern that works in industry: deterministic rules first, an LLM only for leftovers, and a cache so repeat failures cost nothing ([Block](https://engineering.block.xyz/blog/actionable-ci), [Cloudkeeper](https://www.cloudkeeper.com/insights/blog/failed-builds-root-causes-ai-assisted-jenkins-triage)). Keep logs short before sending them to a model, since failures sit near the end ([GeekyAnts](https://geekyants.com/blog/ai-code-healer-for-fixing-broken-cicd-builds-fast)). LLMs will invent causes with confidence, so check that any line they cite actually appears in the log ([Red Hat](https://developers.redhat.com/articles/2026/09/29/how-we-cut-ci-failure-triage-from-hours-to-minutes-using-ai)). Datadog keeps an explicit `unknown` category ([Datadog](https://docs.datadoghq.com/ja/continuous_integration/guides/use_ci_jobs_failure_analysis/)).

### Databricks

Probably "build X on the platform." If the kit needs Free Edition, know the limits: serverless only, no GPUs, one 2X-Small SQL warehouse, 5 concurrent job tasks, Python/SQL only (no R or Scala). Go over the daily quota and compute shuts off for the rest of the day ([docs](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations)). That last one can lose you hours, so don't burn compute on retries.

### Machina

Still unidentified. A search turned up no "Machina" tied to Ohio State events. If it's Machina Labs (robotic sheet-metal forming), expect geometry, toolpath, or sensor data. Ask at kickoff.

### Builders

The host. No hints.

## Practice data for RWX

- [LogChunks](https://zenodo.org/records/3632351): 797 Travis CI logs, each with a hand-labeled chunk that says why the build failed. The best match for "find the cause."
- [JetBrains lca-ci-builds-repair](https://huggingface.co/datasets/JetBrains-Research/lca-ci-builds-repair): failed GitHub Actions logs paired with fixing commits.
- [GHALogs](https://www.eurecom.edu/en/node/4899917): 116k GitHub Actions runs with full logs, unlabeled.

## Questions to email hi@joinbuilders.org

1. Max team size?
2. Can one team enter more than one track, or switch tracks after submitting?
3. Are hosted LLM APIs (Groq, Gemini) allowed in submissions? Does code run on our machine or theirs?
4. Submission rate limit per track?
5. Which company is the Machina track?

## Kickoff-night plan

1. Read all four problems. Watch which boards fill up in the first hour.
2. Fill in `SUBMIT_URL` and the label set (`CATEGORIES` in `baselines/rwx_triage.py`).
3. Hold out about 20% of the sample data. Every change gets `python -m harness.local_eval`, and only local gains get submitted.
4. Make the first submission within an hour, even if it's bad. That proves the pipeline works.
