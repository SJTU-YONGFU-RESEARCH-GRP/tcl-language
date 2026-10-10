# 04_flatten_cell.tcl — Week 26 Day 2: $L flatten cell TOP
# Run: make week26-04
#      ./scripts/run_calibre_tcl.sh lessons/26/04_flatten_cell.tcl

set L [layout create]
$L create cell BOX
$L create layer 1
$L create polygon BOX 1_0 0 0 10 10
$L create cell TOP
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 20 0 0 0 1

puts "BEFORE: refs=[llength [$L iterator ref TOP range 0 end]] poly_TOP=[llength [$L iterator poly TOP 1 range 0 end]]"

$L flatten cell TOP

puts "AFTER  flatten cell TOP"
puts "  children   = [$L children TOP]"
puts "  n_refs     = [llength [$L iterator ref TOP range 0 end]]"
puts "  n_poly_TOP = [llength [$L iterator poly TOP 1 range 0 end]]"
puts "  polys      = [$L iterator poly TOP 1 range 0 end]"
puts "  cells      = [$L cells]  (BOX still exists without -withDelete)"
exit
