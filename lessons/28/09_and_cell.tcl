# 09_and_cell.tcl — Week 28 Day 4: AND with -cell
# Run: make week28-09
#      ./scripts/run_calibre_tcl.sh lessons/28/09_and_cell.tcl

set L [layout create]
$L units microns 1000
$L create cell TOP
$L create cell OTHER
foreach ly {1 2 3} { $L create layer $ly }

$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 2_0 10 10 30 30
$L create polygon OTHER 1_0 0 0 5 5
$L create polygon OTHER 2_0 0 0 5 5

$L AND 1 2 3 -cell TOP

puts "AND -cell TOP"
puts "  TOP   L3 npoly=[llength [$L iterator poly TOP 3 range 0 end]]"
puts "  OTHER L3 npoly=[llength [$L iterator poly OTHER 3 range 0 end]]"
puts "Expected: result only on TOP; OTHER untouched on L3"
exit
