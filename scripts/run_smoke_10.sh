#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATASET="${1:-}"
SEED="${DEEPCODEX_SMOKE_SEED:-0}"
TASKS="${DEEPCODEX_SMOKE_TASKS:-10}"

if [[ -z "$DATASET" ]]; then
  echo "usage: $0 /path/to/deepswe-dataset [pier run args...]" >&2
  echo "env: DEEPCODEX_SMOKE_TASKS=10 DEEPCODEX_SMOKE_SEED=0" >&2
  exit 2
fi

shift
cd "$ROOT"

scripts/run_codex_base.sh "$DATASET" --n-tasks "$TASKS" --sample-seed "$SEED" "$@"
scripts/run_lazycodex_start_work.sh "$DATASET" --n-tasks "$TASKS" --sample-seed "$SEED" "$@"
