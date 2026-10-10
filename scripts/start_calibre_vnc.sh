#!/usr/bin/env bash
# Start (or reuse) a Calibre-friendly VNC desktop on hurricane.
# - TigerVNC :33 on localhost:5933 (password: calibre)
# - Motif window manager (mwm) so windows can be moved/resized
# - Optional xterm + calibredrv
#
# Usage:
#   ./start_calibre_vnc.sh              # ensure VNC+WM up
#   ./start_calibre_vnc.sh --gui        # also launch calibredrv
#   ./start_calibre_vnc.sh --term       # also launch xterm
#   ./start_calibre_vnc.sh --all        # WM + xterm + calibredrv
#   ./start_calibre_vnc.sh --restart    # kill and recreate display :33
#
# On Mac:
#   ssh -L 15933:127.0.0.1:5933 yongfu@hurricane
#   open -a TigerVNC   # connect 127.0.0.1::15933  password: calibre

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DISPLAY_NUM=33
export DISPLAY=":${DISPLAY_NUM}"
RFB_PORT=5933
PASSFILE="${HOME}/.vnc/passwd_calibre"
VNC_PASS=calibre
LOGDIR=/tmp
DO_GUI=0
DO_TERM=0
DO_RESTART=0

for arg in "$@"; do
  case "$arg" in
    --gui) DO_GUI=1 ;;
    --term) DO_TERM=1 ;;
    --all) DO_GUI=1; DO_TERM=1 ;;
    --restart) DO_RESTART=1 ;;
    -h|--help)
      sed -n '2,20p' "$0"
      exit 0
      ;;
  esac
done

have_display() {
  DISPLAY="$DISPLAY" xdpyinfo >/dev/null 2>&1
}

pids_for_cmd_on_display() {
  # args: regex matching ps cmd
  local re=$1
  local p
  for p in $(ps -u "$USER" -o pid=,cmd= | awk -v re="$re" '$0 ~ re { print $1 }'); do
    if tr '\0' '\n' <"/proc/$p/environ" 2>/dev/null | grep -qx "DISPLAY=$DISPLAY"; then
      echo "$p"
    fi
  done
}

kill_display() {
  local p
  for p in $(ps -u "$USER" -o pid=,cmd= | awk -v d=":$DISPLAY_NUM" '
    $0 ~ /Xvnc / && index($0, d) { print $1 }
  '); do
    echo "Stopping Xvnc pid $p"
    kill "$p" 2>/dev/null || true
  done
  for p in $(pids_for_cmd_on_display '(^|[/ ])mwm( |$)'); do
    echo "Stopping mwm pid $p"
    kill "$p" 2>/dev/null || true
  done
  for p in $(pids_for_cmd_on_display 'icwb/pvt/calibrewb'); do
    echo "Stopping calibrewb pid $p"
    kill "$p" 2>/dev/null || true
  done
  for p in $(pids_for_cmd_on_display 'xterm'); do
    echo "Stopping xterm pid $p"
    kill "$p" 2>/dev/null || true
  done
  sleep 1
  rm -f "/tmp/.X11-unix/X${DISPLAY_NUM}"
}

ensure_password() {
  mkdir -p "$(dirname "$PASSFILE")"
  if [[ ! -f "$PASSFILE" ]]; then
    printf '%s\n%s\nn\n' "$VNC_PASS" "$VNC_PASS" | vncpasswd "$PASSFILE" >/dev/null
  fi
}

# Minimal mwm resources: title bars + keyboard move
ensure_mwmrc() {
  local rc="${HOME}/.mwmrc"
  if [[ -f "$rc" ]]; then
    return 0
  fi
  cat >"$rc" <<'EOF'
# Motif WM — enable move/resize for Calibre VNC desktop
Menu DefaultRootMenu
{
  "New Terminal"  f.exec "xterm -geometry 100x28 &"
  no-label        f.separator
  "Restart"       f.restart
  "Quit WM"       f.quit_mwm
}

Buttons DefaultButtonBindings
{
  <Btn1Down>      root | f.menu DefaultRootMenu
  <Btn3Down>      root | f.menu DefaultRootMenu
  !Shift<Key>Escape icon|window|frame|title f.post_wlist
}

Keys DefaultKeyBindings
{
  Shift<Key>Escape                  icon|window|frame|title  f.post_wlist
  Meta<Key>Tab                      root|icon|window|frame|title  f.next_key
  Meta Shift<Key>Tab                root|icon|window|frame|title  f.prev_key
  Meta<Key>F7                       window|frame|title  f.move
  Meta<Key>F8                       window|frame|title  f.resize
  Meta<Key>F9                       window|frame|title  f.minimize
  Meta<Key>F10                      window|frame|title  f.maximize
}
EOF
}

start_vnc() {
  ensure_password
  if have_display; then
    echo "VNC display $DISPLAY already up"
    return 0
  fi
  echo "Starting Xvnc $DISPLAY (rfbport $RFB_PORT)..."
  nohup Xvnc "$DISPLAY" \
    -geometry 1920x1080 -depth 24 \
    -rfbport "$RFB_PORT" \
    -SecurityTypes VncAuth \
    -PasswordFile "$PASSFILE" \
    -localhost yes \
    >"${LOGDIR}/Xvnc-${DISPLAY_NUM}.log" 2>&1 &
  sleep 1
  if ! have_display; then
    echo "ERROR: Xvnc failed; see ${LOGDIR}/Xvnc-${DISPLAY_NUM}.log" >&2
    exit 1
  fi
}

start_wm() {
  ensure_mwmrc
  if [[ -n "$(pids_for_cmd_on_display '(^|[/ ])mwm( |$)')" ]]; then
    echo "mwm already running on $DISPLAY"
    return 0
  fi
  echo "Starting mwm on $DISPLAY (title bars: drag to move, edges to resize)..."
  nohup mwm >"${LOGDIR}/mwm-${DISPLAY_NUM}.log" 2>&1 &
  sleep 0.5
}

start_term() {
  if [[ -n "$(pids_for_cmd_on_display 'xterm')" ]]; then
    echo "xterm already present on $DISPLAY"
    return 0
  fi
  # shellcheck disable=SC1091
  source "$ROOT/setup_calibredrv.sh" >/dev/null
  export DISPLAY
  echo "Starting xterm on $DISPLAY..."
  nohup xterm -geometry 100x28+20+740 -fa Monospace -fs 11 \
    -T "hurricane terminal ($DISPLAY)" \
    -e bash -lc "source '$ROOT/setup_calibredrv.sh'; export DISPLAY=$DISPLAY; cd '$ROOT'; exec bash" \
    >"${LOGDIR}/xterm-${DISPLAY_NUM}.log" 2>&1 &
}

start_gui() {
  # shellcheck disable=SC1091
  source "$ROOT/setup_calibredrv.sh" >/dev/null
  export DISPLAY
  if [[ -n "$(pids_for_cmd_on_display 'icwb/pvt/calibrewb')" ]]; then
    echo "calibredrv already running on $DISPLAY"
    return 0
  fi
  echo "Starting calibredrv on $DISPLAY..."
  nohup calibredrv >"${LOGDIR}/calibredrv-vnc.log" 2>&1 &
}

if [[ "$DO_RESTART" -eq 1 ]]; then
  kill_display
fi

start_vnc
start_wm
[[ "$DO_TERM" -eq 1 ]] && start_term
[[ "$DO_GUI" -eq 1 ]] && start_gui

# Arrange windows if present
if [[ -x "$ROOT/tools/tile_vnc_windows.py" ]]; then
  python3 "$ROOT/tools/tile_vnc_windows.py" || true
fi

echo ""
echo "VNC ready:"
echo "  DISPLAY=$DISPLAY  port=$RFB_PORT  password=$VNC_PASS"
echo "  Move: drag the window title bar"
echo "  Resize: drag window edges/corners"
echo "  Alt+Tab: cycle windows"
echo "  Alt+F7 / Alt+F8: move / resize"
echo "  Retile: python3 $ROOT/tools/tile_vnc_windows.py"
echo "  Open GDS: $ROOT/open_gds.sh tmp/demo_box.gds"
echo "Mac:"
echo "  ssh -L 15933:127.0.0.1:${RFB_PORT} yongfu@$(hostname -s)"
echo "  open -a TigerVNC   # 127.0.0.1::15933"
