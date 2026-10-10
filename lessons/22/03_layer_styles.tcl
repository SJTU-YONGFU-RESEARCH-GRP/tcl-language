# 03_layer_styles.tcl — Week 22 Day 2: layer number styles that work here
# Run: make week22-03
#      ./scripts/run_calibre_tcl.sh lessons/22/03_layer_styles.tcl
#
# On this Calibre: create layer wants 1 or 1.0 (NOT 1_0).
# create polygon accepts 1, 1.0, or 1_0 after the layer exists.

set L [layout create]
$L create cell TOP

$L create layer 1
$L create layer 2.0
puts "Created layers with styles: 1  and  2.0"

$L create polygon TOP 1 0 0 20 20
puts "polygon with layer style 1 OK"

$L create polygon TOP 1_0 30 0 50 0 50 20 30 20
puts "polygon with layer style 1_0 OK"

$L create polygon TOP 2.0 60 0 80 20
puts "polygon with layer style 2.0 OK"

puts "Pick ONE style and stick to it in a script."
exit
