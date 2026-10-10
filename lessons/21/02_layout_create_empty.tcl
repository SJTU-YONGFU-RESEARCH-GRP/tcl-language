# 02_layout_create_empty.tcl — Week 21 Day 3: layout create returns a handle
# Run: make week21-02
#      ./scripts/run_calibre_tcl.sh lessons/21/02_layout_create_empty.tcl

# layout create = make a new empty layout (blank drawing paper)
set L [layout create]

# L is a handle (句柄) — a name for this layout object in Tcl
puts "Created empty layout."
puts "Handle L = $L"

exit
