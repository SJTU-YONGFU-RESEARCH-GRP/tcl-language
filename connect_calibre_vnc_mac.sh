#!/bin/bash
# Run this ON YOUR MAC (Terminal.app / iTerm), not in Cursor / not on hurricane.
#
# Apple "Screen Sharing" often fails against TigerVNC with:
#   "Make sure Screen Sharing or Remote Management is enabled..."
# Use TigerVNC Viewer instead: https://github.com/TigerVNC/tigervnc/releases
#
# Usage:
#   bash connect_calibre_vnc_mac.sh [user@host]
#
HOST="${1:-yongfu@hurricane}"
LOCAL_PORT=15933
REMOTE_VNC=5933
VNC_PASSWORD=calibre

echo "1) Opening SSH tunnel: localhost:${LOCAL_PORT} -> ${HOST}:127.0.0.1:${REMOTE_VNC}"
echo "   Keep this window open."
echo ""
echo "2) On Mac, install/open TigerVNC Viewer and connect to:"
echo "     127.0.0.1::${LOCAL_PORT}"
echo "   Password: ${VNC_PASSWORD}"
echo ""
echo "   Do NOT use Apple Screen Sharing (open vnc://...) for this server."
echo ""

exec ssh -L "${LOCAL_PORT}:127.0.0.1:${REMOTE_VNC}" -N "$HOST"
