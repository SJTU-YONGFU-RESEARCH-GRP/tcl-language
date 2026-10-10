# 10_flatten_report.tcl — Week 26 Day 5 project: before/after report
# Run: make week26-10
#      ./scripts/run_calibre_tcl.sh lessons/26/10_flatten_report.tcl
# Writes: tmp/week26_report.txt , tmp/week26_flat.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set report [file join $outDir week26_report.txt]
set gds [file join $outDir week26_flat.gds]

set L [layout create]
$L units microns 1000
$L create cell BOX
$L create layer 1
$L create polygon BOX 1_0 0 0 10 10
$L create cell TOP
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 20 0 0 0 1

set lines {}
lappend lines "Week 26 flatten report"
lappend lines "======================"
lappend lines "BEFORE"
lappend lines "  cells      = [$L cells]"
lappend lines "  children   = [$L children TOP]"
lappend lines "  n_refs     = [llength [$L iterator ref TOP range 0 end]]"
lappend lines "  n_poly_TOP = [llength [$L iterator poly TOP 1 range 0 end]]"
lappend lines "  refs       = [$L iterator ref TOP range 0 end]"

$L flatten cell TOP -withDelete

lappend lines "AFTER flatten cell TOP -withDelete"
lappend lines "  cells      = [$L cells]"
lappend lines "  children   = [$L children TOP]"
lappend lines "  n_refs     = [llength [$L iterator ref TOP range 0 end]]"
lappend lines "  n_poly_TOP = [llength [$L iterator poly TOP 1 range 0 end]]"
lappend lines "  polys      = [$L iterator poly TOP 1 range 0 end]"
lappend lines "======================"
lappend lines "Done."

set fh [open $report w]
puts $fh [join $lines \n]
close $fh

$L gdsout $gds TOP
puts "Report: $report"
puts "Flat GDS: $gds"
foreach line $lines { puts $line }
exit
