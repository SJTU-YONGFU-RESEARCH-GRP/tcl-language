# 07_script1_skeleton.tcl — Week 7: official Script 1 skeleton (from PLAN)
# Run: make week7-07
#      ./scripts/run_calibre_tcl.sh lessons/7/07_script1_skeleton.tcl
# Writes: tmp/week7_script1.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week7_script1.gds]

set L [layout create]
$L create cell TOP
$L create layer 1
$L create layer 2.7
$L create polygon TOP 1_0 0 0 100 100

puts "Layout handle: $L"
puts "Writing $gds"
$L gdsout $gds TOP
puts "done size=[file size $gds] bytes"

exit
