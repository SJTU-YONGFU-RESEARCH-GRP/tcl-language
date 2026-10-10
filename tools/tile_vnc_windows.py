#!/usr/bin/env python3
"""Tile Calibre + xterm on DISPLAY=:33 via ICCCM (works with mwm)."""
import os
import sys
import ctypes
from ctypes import POINTER, Structure, byref, c_char_p, c_int, c_uint, c_ulong, c_void_p

os.environ.setdefault("DISPLAY", ":33")

CWX = 1 << 0
CWY = 1 << 1
CWWidth = 1 << 2
CWHeight = 1 << 3


class XWindowChanges(Structure):
    _fields_ = [
        ("x", c_int),
        ("y", c_int),
        ("width", c_int),
        ("height", c_int),
        ("border_width", c_int),
        ("sibling", c_ulong),
        ("stack_mode", c_int),
    ]


X = ctypes.CDLL("libX11.so.6")
X.XOpenDisplay.restype = c_void_p
X.XOpenDisplay.argtypes = [c_char_p]
X.XDefaultRootWindow.restype = c_ulong
X.XDefaultRootWindow.argtypes = [c_void_p]
X.XQueryTree.argtypes = [
    c_void_p,
    c_ulong,
    POINTER(c_ulong),
    POINTER(c_ulong),
    POINTER(POINTER(c_ulong)),
    POINTER(c_uint),
]
X.XFetchName.argtypes = [c_void_p, c_ulong, POINTER(c_char_p)]
X.XReconfigureWMWindow.argtypes = [c_void_p, c_ulong, c_int, c_uint, POINTER(XWindowChanges)]
X.XDestroyWindow.argtypes = [c_void_p, c_ulong]
X.XFlush.argtypes = [c_void_p]
X.XSync.argtypes = [c_void_p, c_int]
X.XFree.argtypes = [c_void_p]


def main() -> int:
    dpy = X.XOpenDisplay(None)
    if not dpy:
        print("ERROR: cannot open DISPLAY", os.environ.get("DISPLAY"), file=sys.stderr)
        return 1
    root = X.XDefaultRootWindow(dpy)
    screen = 0

    def children(w):
        r = c_ulong()
        p = c_ulong()
        ch = POINTER(c_ulong)()
        n = c_uint()
        X.XQueryTree(dpy, w, byref(r), byref(p), byref(ch), byref(n))
        out = [ch[i] for i in range(n.value)]
        if ch:
            X.XFree(ch)
        return out

    def name(w):
        n = c_char_p()
        if X.XFetchName(dpy, w, byref(n)) and n.value:
            return n.value.decode(errors="ignore")
        return ""

    def find(substr):
        hits = []

        def walk(parent):
            for w in children(parent):
                if substr in name(w):
                    hits.append(w)
                walk(w)

        walk(root)
        return hits

    layout = [
        ("DESIGNrev", 20, 40, 1100, 900),
        ("hurricane terminal", 1140, 500, 740, 540),
    ]
    for substr, x, y, w, h in layout:
        hits = find(substr)
        if not hits:
            print(f"skip (not found): {substr}")
            continue
        client = hits[0]
        chg = XWindowChanges(x=x, y=y, width=w, height=h, border_width=0, sibling=0, stack_mode=0)
        rc = X.XReconfigureWMWindow(dpy, client, screen, CWX | CWY | CWWidth | CWHeight, byref(chg))
        print(f"tile {substr}: {hex(client)} -> {w}x{h}+{x}+{y} rc={rc}")

    for w in find("Choose Viewing Detail"):
        print(f"destroy dialog {hex(w)}")
        X.XDestroyWindow(dpy, w)

    X.XSync(dpy, False)
    X.XFlush(dpy)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
