# 06_create_text.tcl — Week 8 Day 3: create text label
# Run: make week8-06
#      ./scripts/run_calibre_tcl.sh lessons/8/06_create_text.tcl
# Writes: tmp/week8_06_text.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week8_06_text.gds]

set L [layout create]
$L create cell TOP
$L create layer 1

$L create polygon TOP 1 0 0 100 100
# create text: cell layer x y string
$L create text TOP 1 10 110 HELLO

puts "Box + text HELLO at (10,110)"
$L gdsout $gds TOP
puts "Wrote $gds ([file size $gds] bytes)"
exit
