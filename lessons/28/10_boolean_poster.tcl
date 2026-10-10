# 10_boolean_poster.tcl — Week 28 Day 5 project: poster GDS + report
# Run: make week28-10
#      ./scripts/run_calibre_tcl.sh lessons/28/10_boolean_poster.tcl
# Writes: tmp/week28_poster.gds , tmp/week28_report.txt

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week28_poster.gds]
set report [file join $outDir week28_report.txt]

set L [layout create]
$L units microns 1000
$L create cell TOP
foreach ly {1 2 3 4 5 6 7} { $L create layer $ly }

$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 2_0 10 10 30 30

$L AND 1 2 3
$L OR  1 2 4
$L NOT 1 2 5
$L XOR 1 2 6
$L SIZE 1 7 by 0.001

$L gdsout $gds TOP

set lines {}
lappend lines "Week 28 boolean poster"
lappend lines "======================"
lappend lines "GDS: $gds"
foreach {ly name} {1 L1_input 2 L2_input 3 AND 4 OR 5 NOT 6 XOR 7 SIZE_grow} {
    set n [llength [$L iterator poly TOP $ly range 0 end]]
    lappend lines [format "  layer %-2s (%-10s) npoly=%s" $ly $name $n]
}
lappend lines "AND polys = [$L iterator poly TOP 3 range 0 end]"
lappend lines "SIZE L7   = [$L iterator poly TOP 7 range 0 end]"
lappend lines "======================"
lappend lines "Done."

set fh [open $report w]
puts $fh [join $lines \n]
close $fh

puts "Poster: $gds"
puts "Report: $report"
foreach line $lines { puts $line }
exit
