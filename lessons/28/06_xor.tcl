# 06_xor.tcl — Week 28 Day 4 bonus: $L XOR (symmetric difference)
# Run: make week28-06
#      ./scripts/run_calibre_tcl.sh lessons/28/06_xor.tcl

set L [layout create]
$L units microns 1000
$L create cell TOP
foreach ly {1 2 6} { $L create layer $ly }
$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 2_0 10 10 30 30

$L XOR 1 2 6

puts "XOR 1 2 -> layer 6"
puts "  npoly = [llength [$L iterator poly TOP 6 range 0 end]]"
puts "  polys = [$L iterator poly TOP 6 range 0 end]"
puts "Expected: two pieces — only the non-overlapping parts"
exit
