# 05_create_layers.tcl — Week 7: create layers on a layout
# Run: make week7-05
#      ./scripts/run_calibre_tcl.sh lessons/7/05_create_layers.tcl
#
# Layer 1     = layer 1, datatype 0 (often written 1_0 later)
# Layer 2.7   = layer 2, datatype 7

set L [layout create]
$L create cell TOP

$L create layer 1
$L create layer 2.7

puts "Layout : $L"
puts "Cell   : TOP"
puts "Layers : 1 and 2.7 created"

exit
