# my_graduation.tcl — customize this (from lessons/10/10_graduation_project.tcl)
# Run: ./scripts/run_calibre_tcl.sh examples/my_graduation.tcl
# Writes: tmp/week10_graduation.gds

set repoRoot [file normalize [file join [file dirname [info script]] ..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week10_graduation.gds]

puts "================================"
puts "   WEEK 10 GRADUATION PROJECT"
puts "   Brick array layout"
puts "================================"

set L [layout create]
$L units microns 1000
$L create cell BRICK
$L create layer 1.0
$L create layer 2.0

$L create polygon BRICK 1.0 0 0 12 8

$L create cell TOP
$L create ref TOP BRICK 0 0 0 0 1 3 2 16 12
$L create text TOP 2.0 0 30 "GRAD"

$L gdsout $gds TOP
puts "Wrote $gds ([file size $gds] bytes)"

puts "--------------------------------"
puts "peek cells  : [layout peek $gds -cells]"
puts "peek layers : [layout peek $gds -layers]"
puts "peek top    : [layout peek $gds -topcell]"
puts "\$L cells    : [$L cells]"
puts "\$L layers   : [$L layers]"
puts "children    : [$L children TOP]"
if {[$L exists cell TOP]} {
    puts "bbox TOP    : [$L bbox TOP]"
}
puts "================================"
puts "Used APIs: create, polygon, create ref, text, gdsout, peek, cells, bbox"
exit
