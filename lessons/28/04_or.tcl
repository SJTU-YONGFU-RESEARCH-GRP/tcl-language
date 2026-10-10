# 04_or.tcl — Week 28 Day 2: $L OR in1 in2 out
# Run: make week28-04
#      ./scripts/run_calibre_tcl.sh lessons/28/04_or.tcl

set L [layout create]
$L units microns 1000
$L create cell TOP
foreach ly {1 2 4} { $L create layer $ly }
$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 2_0 10 10 30 30

$L OR 1 2 4

puts "OR 1 2 -> layer 4"
puts "  npoly = [llength [$L iterator poly TOP 4 range 0 end]]"
puts "  polys = [$L iterator poly TOP 4 range 0 end]"
puts "Expected: one merged outline covering both boxes"
exit
