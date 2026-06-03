# Repository Guidance

This repository is only for DeepSWE/Pier benchmarks of Codex-family harnesses.

- Keep headline benchmark conditions limited to `codex-base` and `lazycodex-start-work`.
- Do not add non-Codex harnesses such as Claude Code, Gemini CLI, OpenCode, Cursor, or Mini-SWE-Agent.
- Do not include `/init-deep` in the main benchmark condition. If added later, document it as a separate warmed-context experiment.
- Use Bun commands (`bun`, `bunx`) instead of npm/npx in scripts.
- Use `uv` for Python tooling.
- Keep public docs reproducible and avoid committing raw secrets, auth files, or full benchmark job logs.

