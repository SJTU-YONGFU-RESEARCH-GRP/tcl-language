# 10_my_shapes.tcl — Week 8 Day 5 project: my shapes (polygon + text)
# Run: make week8-10
#      ./scripts/run_calibre_tcl.sh lessons/8/10_my_shapes.tcl
# Writes: tmp/week8_my_shapes.gds
# Challenge: change name initials and box size; optional wire.

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week8_my_shapes.gds]

set student "Amy"
set initials "A"

puts "================================"
puts "   MY SHAPES — $student"
puts "================================"

set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1
$L create layer 2

# Required: polygon (house body)
$L create polygon TOP 1_0 \
  0 0 \
  120 0 \
  120 80 \
  0 80

# Required: text label
$L create text TOP 1 10 90 $initials

# Bonus: wire as a path/road
$L create wire TOP 2_0 6 \
  0 40 \
  120 40

puts "Shapes: polygon + text + wire"
puts "Writing $gds"
$L gdsout $gds TOP
puts "done size=[file size $gds] bytes"
puts "================================"
exit
