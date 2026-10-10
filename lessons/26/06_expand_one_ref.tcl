# 06_expand_one_ref.tcl — Week 26 Day 4: expand only one instance
# Run: make week26-06
#      ./scripts/run_calibre_tcl.sh lessons/26/06_expand_one_ref.tcl
#
# Must create ref first; expand ref needs matching x y mirror angle mag.

set L [layout create]
$L create cell BOX
$L create layer 1
$L create polygon BOX 1_0 0 0 10 10
$L create cell TOP
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 20 0 0 0 1

puts "BEFORE refs = [$L iterator ref TOP range 0 end]"

# Expand only the instance at (0,0)
$L expand ref TOP BOX 0 0 0 0 1

puts "AFTER  expand ref at (0,0)"
puts "  refs  = [$L iterator ref TOP range 0 end]"
puts "  polys = [$L iterator poly TOP 1 range 0 end]"
puts "Expected: 1 ref left at (20,0), 1 polygon from the expanded instance"
exit
