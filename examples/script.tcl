set L [layout create]
set my_cell [lindex $argv 0]
$L create cell $my_cell
$L create layer [set layer1 [lindex $argv 1]]
set first_coord 2
set last_coord [expr $argc - 2]
set coords [lrange $argv $first_coord $last_coord]
puts $coords
eval $L create polygon $my_cell $layer1 $coords
$L gdsout [lindex $argv end] 
