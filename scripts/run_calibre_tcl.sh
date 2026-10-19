#!/usr/bin/env bash
# Run a Calibre DESIGNrev Tcl script with the project env.
# Usage:
#   ./run_calibre_tcl.sh examples/create_box.tcl
#   ./run_calibre_tcl.sh examples/hello_calibre.tcl
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$ROOT/setup_calibredrv.sh" >/dev/null

# Prefer the VNC/GUI display if present; else whatever setup chose (Xvfb/:99).
if DISPLAY=:33 xdpyinfo >/dev/null 2>&1; then
  export DISPLAY=:33
fi

# Check if calibredrv is available, or if DRV-Lite simulation mode is requested
USE_SIM=0
if [[ "${1:-}" == "--sim" ]]; then
  USE_SIM=1
  shift
fi

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 [--sim] <script.tcl> [extra args...]" >&2
  exit 2
fi

script=$1
shift
if [[ ! -f "$script" ]]; then
  # allow paths relative to repo root
  if [[ -f "$ROOT/$script" ]]; then
    script="$ROOT/$script"
  else
    echo "ERROR: script not found: $script" >&2
    exit 1
  fi
fi

if [[ "$USE_SIM" -eq 1 ]] || ! command -v calibredrv >/dev/null 2>&1 || [[ "${DRVLITE:-0}" == "1" ]]; then
  DRVLITE_TCL="$ROOT/../tools/drvlite/drvlite.tcl"
  if [[ ! -f "$DRVLITE_TCL" ]]; then
    DRVLITE_TCL="$ROOT/tools/drvlite/drvlite.tcl"
  fi
  echo "[DRV-Lite] calibredrv not found (or --sim requested). Running in pure-Tcl simulation mode via tclsh..."
  exec tclsh <(cat "$DRVLITE_TCL" "$script") "$@"
fi

echo "DISPLAY=$DISPLAY"
echo "Running: calibredrv -shell -s $script $*"
exec calibredrv -shell -s "$script" "$@"
