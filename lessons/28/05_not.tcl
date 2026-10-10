# 05_not.tcl — Week 28 Day 2: $L NOT in1 in2 out  (L1 minus L2)
# Run: make week28-05
#      ./scripts/run_calibre_tcl.sh lessons/28/05_not.tcl

set L [layout create]
$L units microns 1000
$L create cell TOP
foreach ly {1 2 5} { $L create layer $ly }
$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 2_0 10 10 30 30

$L NOT 1 2 5

puts "NOT 1 2 -> layer 5  (keep L1, cut away L2)"
puts "  npoly = [llength [$L iterator poly TOP 5 range 0 end]]"
puts "  polys = [$L iterator poly TOP 5 range 0 end]"
puts "Expected: L-shaped leftover of the first box"
exit
