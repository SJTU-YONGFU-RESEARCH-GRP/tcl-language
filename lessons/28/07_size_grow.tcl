# 07_size_grow.tcl — Week 28 Day 3: $L SIZE in out by amt (grow)
# Run: make week28-07
#      ./scripts/run_calibre_tcl.sh lessons/28/07_size_grow.tcl
#
# With `$L units microns 1000`, `by 0.001` grows about 1 user-micron.

set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1
$L create layer 3
$L create polygon TOP 1_0 10 10 20 20

puts "BEFORE L1 = [$L iterator poly TOP 1 range 0 end]"
$L SIZE 1 3 by 0.001
puts "AFTER  SIZE 1 3 by 0.001"
puts "  L3 = [$L iterator poly TOP 3 range 0 end]"
puts "Expected: roughly (9,9)-(21,21)"
exit
