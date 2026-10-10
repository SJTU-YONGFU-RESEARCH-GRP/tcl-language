#!/bin/bash
# Install TigerVNC Viewer on macOS (CLIENT).
# Run this ON YOUR MAC, not on hurricane.
#
# Hurricane already runs the VNC server (Xvnc). The viewer belongs on the Mac
# that displays the GUI.
#
# Usage (on Mac):
#   scp yongfu@hurricane:~/proj/tcl-language/install_tigervnc_viewer_mac.sh .
#   bash install_tigervnc_viewer_mac.sh

set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "ERROR: this script is for macOS only."
  echo "You are on: $(uname -s) $(hostname 2>/dev/null || true)"
  echo "Run it in Terminal.app on your Mac, not on hurricane."
  exit 1
fi

echo "==> Installing TigerVNC Viewer on this Mac..."

if command -v brew >/dev/null 2>&1; then
  echo "==> Using Homebrew"
  brew install --cask tigervnc-viewer
else
  echo "==> Homebrew not found. Installing Homebrew first is recommended:"
  echo "    /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
  echo ""
  echo "Or download TigerVNC Viewer manually:"
  echo "    https://github.com/TigerVNC/tigervnc/releases"
  echo "    (pick the macOS .dmg for your CPU: arm64 for Apple Silicon, x86_64 for Intel)"
  exit 1
fi

echo ""
echo "==> Done."
echo "Open: TigerVNC Viewer (Spotlight: TigerVNC)"
echo ""
echo "Then on Mac:"
echo "  1) ssh -L 15933:127.0.0.1:5933 yongfu@hurricane   # keep open"
echo "  2) TigerVNC Viewer -> connect to 127.0.0.1::15933"
echo "  3) Password: calibre"
echo ""
echo "Do NOT use Apple Screen Sharing for this."
