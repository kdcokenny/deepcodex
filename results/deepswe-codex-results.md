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
| Concurrent trials | 1 |

## Summary

| Condition | Tasks | Passes | Pass rate | Mean cost | Mean wall time | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `codex-base` | 1 | 1 | 100% | `$3.565835` | 16m 27s | 1-task smoke on `meriyah-explicit-resource-declar__tgBHPxZ` |
| `lazycodex-start-work` | 1 | 1 | 100% | `$5.991173` | 21m 51s | 1-task smoke on `meriyah-explicit-resource-declar__9cesecj`; includes LazyCodex install time |

## Method

`codex-base` uses Pier's built-in Codex runner.

`lazycodex-start-work` uses the local `LazyCodexStartWork` Pier agent, which installs LazyCodex into the sandbox Codex home and prefixes the task instruction with `$start-work`.

## Reproduction Commands

```bash
scripts/run_smoke_10.sh /path/to/deepswe-dataset
scripts/run_codex_base.sh /path/to/deepswe-dataset
scripts/run_lazycodex_start_work.sh /path/to/deepswe-dataset
```

## Notes

- This is a 1-task paired smoke, not the full 10-task or 100-task benchmark.
- `codex-base` verifier reward: `1.0`; full verifier baseline and new tests passed.
- `lazycodex-start-work` verifier reward: `1.0`; full verifier baseline and new tests passed.
- An initial LazyCodex setup attempt failed before agent execution because Pier egress blocked `registry.npmjs.org`; that failed setup is preserved under `jobs/lazycodex-start-work.registry403-20260603152431` and excluded from the headline table.
- Do not merge `$ulw-loop` or `/init-deep` variants into this headline table.
