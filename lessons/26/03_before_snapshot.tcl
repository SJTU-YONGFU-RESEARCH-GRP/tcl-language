# 03_before_snapshot.tcl — Week 26 Day 1: inventory before flatten
# Run: make week26-03
#      ./scripts/run_calibre_tcl.sh lessons/26/03_before_snapshot.tcl

set L [layout create]
$L create cell BOX
$L create layer 1
$L create polygon BOX 1_0 0 0 10 10
$L create cell TOP
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 20 0 0 0 1

puts "BEFORE flatten"
puts "  cells      = [$L cells]"
puts "  children   = [$L children TOP]"
puts "  n_refs     = [llength [$L iterator ref TOP range 0 end]]"
puts "  n_poly_TOP = [llength [$L iterator poly TOP 1 range 0 end]]"
puts "  n_poly_BOX = [llength [$L iterator poly BOX 1 range 0 end]]"
puts "Expected: 2 refs, 0 polys on TOP, 1 poly on BOX"
exit
