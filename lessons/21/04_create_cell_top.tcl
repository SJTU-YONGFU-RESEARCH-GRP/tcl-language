# 04_create_cell_top.tcl — Week 21: empty layout + TOP cell
# Run: make week21-04
#      ./scripts/run_calibre_tcl.sh lessons/21/04_create_cell_top.tcl

set L [layout create]
puts "Layout handle: $L"

# A cell is like a sheet / container on the drawing
$L create cell TOP
puts "Created cell TOP on $L"

exit
