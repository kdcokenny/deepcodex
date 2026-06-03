# DeepCodex

DeepCodex is a small benchmark harness for running DeepSWE/Pier trials on Codex-family harnesses.

The initial comparison is deliberately narrow:

- `codex-base`: Pier's stock Codex runner.
- `lazycodex-start-work`: the same Pier Codex runner with LazyCodex installed in the sandbox Codex home and the task prompt routed through `$start-work`.

Out of scope for this repository: Claude Code, Gemini CLI, OpenCode, Cursor, Mini-SWE-Agent, `/init-deep`, and headline `$ulw-loop` results. `$ulw-loop` can be added later as a separate ceiling experiment, but it should not be mixed into the primary comparison.

## Prerequisites

- Docker, for Pier's local sandbox environment.
- `uv`, for running Pier and this local package.
- Bun, for running the LazyCodex installer with `bunx`.
- An OpenAI API key in the environment or a `.env` file.
- A local DeepSWE/Harbor-format dataset directory.

Install the local package in an isolated environment:

```bash
uv sync
```

Copy the environment template and fill it in:

```bash
cp .env.example .env
```

## Run

Run a small smoke first:

```bash
scripts/run_smoke_10.sh /path/to/deepswe-dataset
```

The smoke runs 10 deterministic tasks per condition. Override the count or seed with `DEEPCODEX_SMOKE_TASKS` and `DEEPCODEX_SMOKE_SEED`.

Run the full configured comparison:

```bash
scripts/run_codex_base.sh /path/to/deepswe-dataset
scripts/run_lazycodex_start_work.sh /path/to/deepswe-dataset
```

Both scripts write Pier jobs under `jobs/`. Use `pier view` or Pier's generated summaries to inspect trajectories.

## Conditions

### `codex-base`

Uses Pier's built-in `codex` agent with the configured model and reasoning effort. The task prompt is passed through unchanged.

### `lazycodex-start-work`

Uses `deepcodex_bench.agents:LazyCodexStartWork`, a thin subclass of Pier's Codex agent. It:

1. Lets Pier create the sandbox `CODEX_HOME`.
2. Runs `bunx --yes lazycodex-ai@latest install --no-tui --codex-autonomous --skip-auth` against that same `CODEX_HOME`.
3. Prefixes each task instruction with `$start-work`.
4. Falls back to Pier's normal `codex exec` path for the actual run and trajectory capture.

This keeps the A/B comparison focused on Codex vs. Codex with LazyCodex's intended plan-execution workflow installed.

## Results

Use [results/deepswe-codex-results.md](results/deepswe-codex-results.md) for public reporting. Keep raw Pier outputs in `jobs/` locally; publish only sanitized summaries or selected artifacts.

## Configuration

The Pier configs live in [configs/](configs/):

- [configs/codex-base.yaml](configs/codex-base.yaml)
- [configs/lazycodex-start-work.yaml](configs/lazycodex-start-work.yaml)

Edit the `model_name` and `reasoning_effort` fields in the config files when changing benchmark model settings. Pier resolves environment templates in `agent.env`, but the model and agent kwargs should stay explicit in committed configs for reproducibility.
