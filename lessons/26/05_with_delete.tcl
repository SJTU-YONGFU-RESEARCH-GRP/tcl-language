# 05_with_delete.tcl — Week 26 Day 3: flatten cell -withDelete
# Run: make week26-05
#      ./scripts/run_calibre_tcl.sh lessons/26/05_with_delete.tcl

set L [layout create]
$L create cell BOX
$L create layer 1
$L create polygon BOX 1_0 0 0 10 10
$L create cell TOP
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 20 0 0 0 1

puts "BEFORE cells = [$L cells]"

$L flatten cell TOP -withDelete

puts "AFTER  flatten cell TOP -withDelete"
puts "  cells      = [$L cells]  (BOX removed if unused)"
puts "  n_refs     = [llength [$L iterator ref TOP range 0 end]]"
puts "  n_poly_TOP = [llength [$L iterator poly TOP 1 range 0 end]]"
puts "  polys      = [$L iterator poly TOP 1 range 0 end]"
exit
