# DeepSWE Codex Harness Results

## Scope

This report compares Codex-family harnesses on DeepSWE through Pier.

Included conditions:

- `codex-base`
- `lazycodex-start-work`

Excluded from headline results:

- Non-Codex harnesses.
- `/init-deep` warmed-context runs.
- `$ulw-loop` ceiling runs.

## Environment

| Field | Value |
| --- | --- |
| Date | 2026-06-03 |
| Dataset path/version | `datasets/deep-swe/tasks` at `datacurve-ai/deep-swe@578129c` |
| Pier version | `datacurve-pier 0.2.0` |
| LazyCodex package | `lazycodex-ai@latest` |
| Codex model | `gpt-5.5` |
| Reasoning effort | `high` |
| Environment | Docker |
| Attempts per task | 1 |
| Concurrent trials | `1` for the first paired smoke task; `2` per condition for the remaining 9 tasks |

## Summary

| Condition | Tasks | Passes | Pass rate | Total cost | Mean cost/task | Wall time | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `codex-base` | 10 | 7 | 70% | `$32.792263` | `$3.279226` | 1h 31m 48s total runner time | First task run at concurrency 1; remaining 9 at concurrency 2 |
| `lazycodex-start-work` | 10 | 7 | 70% | `$50.942104` | `$5.094210` | 2h 34m 17s total runner time | Includes LazyCodex install time inside each sandbox |

## Job Breakdown

| Condition | Job | Tasks | Passes | Pass rate | Cost | Wall time | Failed tasks |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `codex-base` | `jobs/codex-base` | 1 | 1 | 100% | `$3.565835` | 16m 27s | None |
| `codex-base` | `jobs/codex-base-remaining9` | 9 | 6 | 66.7% | `$29.226428` | 1h 15m 21s | `arktype-json-schema-refs-dependencies`, `katex-multicolumn-array-spans`, `scc-bounded-memory-spilling` |
| `lazycodex-start-work` | `jobs/lazycodex-start-work` | 1 | 1 | 100% | `$5.991173` | 21m 51s | None |
| `lazycodex-start-work` | `jobs/lazycodex-start-work-remaining9` | 9 | 6 | 66.7% | `$44.950931` | 2h 12m 32s | `anko-typed-variable-bindings`, `arktype-json-schema-refs-dependencies`, `katex-multicolumn-array-spans` |

## Per-Task Results

| Task | `codex-base` | `lazycodex-start-work` |
| --- | --- | --- |
| `meriyah-explicit-resource-declarations` | Pass | Pass |
| `query-persist-restored-query-state` | Pass | Pass |
| `helm-unified-manifest-stream` | Pass | Pass |
| `anko-typed-variable-bindings` | Pass | Fail |
| `igel-persist-feature-schema` | Pass | Pass |
| `fastapi-deprecation-response-headers` | Pass | Pass |
| `scc-bounded-memory-spilling` | Fail | Pass |
| `katex-multicolumn-array-spans` | Fail | Fail |
| `arktype-json-schema-refs-dependencies` | Fail | Fail |
| `vulture-persistent-analysis-cache` | Pass | Pass |

## Token And Cost Totals

| Condition | Input tokens | Output tokens | Cost |
| --- | ---: | ---: | ---: |
| `codex-base` | 42,167,483 | 214,000 | `$32.792263` |
| `lazycodex-start-work` | 72,403,412 | 229,638 | `$50.942104` |

## Method

`codex-base` uses Pier's built-in Codex runner.

`lazycodex-start-work` uses the local `LazyCodexStartWork` Pier agent, which installs LazyCodex into the sandbox Codex home and prefixes the task instruction with `$start-work`.

The 10-task set is the deterministic DeepSWE sample selected with seed 0. The first task was run as a paired smoke at concurrency 1. The remaining 9 were run as separate jobs with `--n-concurrent 2` per condition to keep total parallelism at 4, without restarting already completed work.

## Reproduction Commands

```bash
scripts/run_smoke_10.sh /path/to/deepswe-dataset
scripts/run_codex_base.sh /path/to/deepswe-dataset
scripts/run_lazycodex_start_work.sh /path/to/deepswe-dataset
```

## Notes

- This is a 10-task partial benchmark, not the full 100-task benchmark.
- Both conditions completed with zero Pier trial errors. Failures above are verifier reward `0.0`, not infrastructure exceptions.
- An initial LazyCodex setup attempt failed before agent execution because Pier egress blocked `registry.npmjs.org`; that failed setup is preserved under `jobs/lazycodex-start-work.registry403-20260603152431` and excluded from the headline table.
- Do not merge `$ulw-loop` or `/init-deep` variants into this headline table.
