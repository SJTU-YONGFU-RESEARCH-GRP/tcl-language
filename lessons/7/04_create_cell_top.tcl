# 04_create_cell_top.tcl — Week 7: empty layout + TOP cell
# Run: make week7-04
#      ./scripts/run_calibre_tcl.sh lessons/7/04_create_cell_top.tcl

set L [layout create]
puts "Layout handle: $L"

# A cell is like a sheet / container on the drawing
$L create cell TOP
puts "Created cell TOP on $L"

exit
