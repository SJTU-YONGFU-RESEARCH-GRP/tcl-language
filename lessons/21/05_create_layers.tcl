# 05_create_layers.tcl — Week 21: create layers on a layout
# Run: make week21-05
#      ./scripts/run_calibre_tcl.sh lessons/21/05_create_layers.tcl
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
