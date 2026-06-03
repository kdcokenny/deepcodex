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
| Date | TBD |
| Dataset path/version | TBD |
| Pier version | TBD |
| LazyCodex package | `lazycodex-ai@latest` |
| Codex model | TBD |
| Reasoning effort | TBD |
| Environment | Docker |
| Attempts per task | 1 |
| Concurrent trials | 1 |

## Summary

| Condition | Tasks | Passes | Pass rate | Mean cost | Mean wall time | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `codex-base` | TBD | TBD | TBD | TBD | TBD | TBD |
| `lazycodex-start-work` | TBD | TBD | TBD | TBD | TBD | TBD |

## Method

`codex-base` uses Pier's built-in Codex runner.

`lazycodex-start-work` uses the local `LazyCodexStartWork` Pier agent, which installs LazyCodex into the sandbox Codex home and prefixes the task instruction with `$start-work`.

## Reproduction Commands

```bash
scripts/run_codex_base.sh /path/to/deepswe-dataset
scripts/run_lazycodex_start_work.sh /path/to/deepswe-dataset
```

## Notes

- Add any failed setup tasks, verifier anomalies, or excluded trials here.
- Do not merge `$ulw-loop` or `/init-deep` variants into this headline table.

