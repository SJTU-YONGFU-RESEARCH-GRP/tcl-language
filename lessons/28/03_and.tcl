# 03_and.tcl — Week 28 Day 1: $L AND in1 in2 out
# Run: make week28-03
#      ./scripts/run_calibre_tcl.sh lessons/28/03_and.tcl

set L [layout create]
$L units microns 1000
$L create cell TOP
foreach ly {1 2 3} { $L create layer $ly }
$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 2_0 10 10 30 30

$L AND 1 2 3

puts "AND 1 2 -> layer 3"
puts "  npoly = [llength [$L iterator poly TOP 3 range 0 end]]"
puts "  polys = [$L iterator poly TOP 3 range 0 end]"
puts "Expected: one square around (10,10)-(20,20)"
exit
