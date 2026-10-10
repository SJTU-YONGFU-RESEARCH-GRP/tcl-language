# 09_coords_after_flatten.tcl — Week 26: transformed polygon coordinates
# Run: make week26-09
#      ./scripts/run_calibre_tcl.sh lessons/26/09_coords_after_flatten.tcl

set L [layout create]
$L create cell BOX
$L create layer 1
# BOX local square: (0,0)-(10,10)
$L create polygon BOX 1_0 0 0 10 10
$L create cell TOP
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 20 0 0 0 1

$L flatten cell TOP

puts "Polygons on TOP after flatten (placement shifts coords):"
set i 0
foreach p [$L iterator poly TOP 1 range 0 end] {
    incr i
    puts "  #$i  $p"
}
puts "Expect roughly: (0..10,0..10) and (20..30,0..10)"
exit
