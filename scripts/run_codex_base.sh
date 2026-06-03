#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATASET="${1:-}"

if [[ -z "$DATASET" ]]; then
  echo "usage: $0 /path/to/deepswe-dataset [pier run args...]" >&2
  exit 2
fi

shift
cd "$ROOT"

ENV_FILE_ARGS=()
if [[ -f .env ]]; then
  ENV_FILE_ARGS=(--env-file .env)
fi

export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
uv run pier run \
  --config configs/codex-base.yaml \
  --path "$DATASET" \
  "${ENV_FILE_ARGS[@]}" \
  "$@"
