# 08_size_shrink.tcl — Week 28 Day 3: negative SIZE (shrink)
# Run: make week28-08
#      ./scripts/run_calibre_tcl.sh lessons/28/08_size_shrink.tcl

set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1
$L create layer 3
$L create polygon TOP 1_0 10 10 20 20

puts "BEFORE L1 = [$L iterator poly TOP 1 range 0 end]"
$L SIZE 1 3 by -0.001
puts "AFTER  SIZE 1 3 by -0.001"
puts "  L3 = [$L iterator poly TOP 3 range 0 end]"
puts "Expected: roughly (11,11)-(19,19)"
exit
