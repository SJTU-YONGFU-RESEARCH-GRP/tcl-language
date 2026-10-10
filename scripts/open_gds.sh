#!/usr/bin/env bash
# Open a GDS/OASIS in Calibre DESIGNrev on the VNC display.
# Usage:
#   ./open_gds.sh tmp/demo_box.gds
#   ./open_gds.sh /path/to/layout.oas
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
# Ensure VNC + window manager
"$ROOT/start_calibre_vnc.sh" >/dev/null

# shellcheck disable=SC1091
source "$ROOT/setup_calibredrv.sh" >/dev/null
export DISPLAY=:33

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <layout.gds|layout.oas> [calibredrv args...]" >&2
  exit 2
fi

layout=$1
shift
if [[ ! -f "$layout" ]]; then
  if [[ -f "$ROOT/$layout" ]]; then
    layout="$ROOT/$layout"
  else
    echo "ERROR: not found: $layout" >&2
    exit 1
  fi
fi

# -endDepth / -hideLayers reduce startup prompts for scripted opens
echo "Opening $layout on DISPLAY=$DISPLAY"
exec calibredrv -endDepth 32 -hideLayers "$layout" "$@"
