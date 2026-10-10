#!/usr/bin/env bash
# Setup Calibre DESIGNrev (calibredrv) on this host (RHEL 9).
# Usage: source setup_calibredrv.sh

export CALIBRE_HOME=/data1/eda/eda/mentor/aoi_cal_2019.2_26.18
export PATH="$CALIBRE_HOME/bin:$PATH"
export LD_LIBRARY_PATH="${HOME}/local/lib/calibre-stubs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export MGLS_LICENSE_FILE=/data1/eda/eda/mentor/mentor2019.dat

# Ensure GStreamer 0.10 stubs exist (OpenCV highgui dependency on RHEL 9)
STUBDIR="${HOME}/local/lib/calibre-stubs"
if [[ ! -f "$STUBDIR/libgstbase-0.10.so.0" || ! -f "$STUBDIR/libgstreamer-0.10.so.0" ]]; then
  mkdir -p "$STUBDIR"
  cat > /tmp/gst_stub.c <<'EOF'
void calibredrv_gst_stub(void) {}
EOF
  gcc -shared -fPIC -o "$STUBDIR/libgstbase-0.10.so.0" /tmp/gst_stub.c
  gcc -shared -fPIC -o "$STUBDIR/libgstreamer-0.10.so.0" /tmp/gst_stub.c
fi

# Provide a DISPLAY if none is set (Cursor/SSH sessions are often headless).
# Prefer X11 forwarding (DISPLAY=localhost:N.0 from `ssh -Y`); else fall back to Xvfb.
_calibre_display_ok() {
  local d="$1"
  DISPLAY="$d" xdpyinfo >/dev/null 2>&1
}

_calibre_is_x11_forwarded() {
  # ssh -X/-Y typically sets DISPLAY to localhost:10.0 / localhost:11.0 / ...
  [[ "${DISPLAY:-}" == localhost:* || "${DISPLAY:-}" == 127.0.0.1:* ]]
}

if [[ -n "${DISPLAY:-}" ]] && _calibre_display_ok "$DISPLAY"; then
  if _calibre_is_x11_forwarded; then
    echo "Using X11-forwarded DISPLAY=$DISPLAY"
  fi
elif [[ "${CALIBRE_FORCE_XVFB:-0}" == 1 ]] || [[ -z "${DISPLAY:-}" ]]; then
  CALIBRE_XVFB_DISPLAY="${CALIBRE_XVFB_DISPLAY:-:99}"
  if ! _calibre_display_ok "$CALIBRE_XVFB_DISPLAY"; then
    if [[ ! -e "/tmp/.X11-unix/X${CALIBRE_XVFB_DISPLAY#:}" ]]; then
      nohup Xvfb "$CALIBRE_XVFB_DISPLAY" -screen 0 1920x1080x24 -ac \
        +extension GLX +render -noreset \
        >/tmp/Xvfb-${CALIBRE_XVFB_DISPLAY#:}.log 2>&1 &
      disown $! 2>/dev/null || true
      sleep 0.5
    fi
  fi
  if _calibre_display_ok "$CALIBRE_XVFB_DISPLAY"; then
    export DISPLAY="$CALIBRE_XVFB_DISPLAY"
  else
    echo "WARNING: could not start/use Xvfb on $CALIBRE_XVFB_DISPLAY" >&2
  fi
else
  echo "WARNING: DISPLAY=$DISPLAY is set but not usable (xdpyinfo failed)" >&2
  echo "  For Mac X11 forwarding: install XQuartz, then: ssh -Y $(hostname -s)" >&2
fi

echo "calibredrv ready: $(command -v calibredrv)"
echo "  CALIBRE_HOME=$CALIBRE_HOME"
echo "  MGLS_LICENSE_FILE=$MGLS_LICENSE_FILE"
echo "  DISPLAY=${DISPLAY:-unset}"
echo "  LD_LIBRARY_PATH includes: $STUBDIR"
if _calibre_is_x11_forwarded 2>/dev/null; then
  echo "  GUI target: Mac via X11 forwarding (XQuartz)"
else
  echo "  Tip (Mac X11): open XQuartz, then from Mac Terminal:"
  echo "    ssh -Y yongfu@$(hostname -s)"
  echo "    source ~/proj/tcl-language/setup_calibredrv.sh && calibredrv"
  echo "  (Cursor's remote terminal usually has no X11 forward — use Mac Terminal.)"
fi
echo "  Headless Tcl: calibredrv -shell"
