# 01_build_overlap.tcl — Week 28 Day 1: two overlapping boxes on L1/L2
# Run: make week28-01
#      ./scripts/run_calibre_tcl.sh lessons/28/01_build_overlap.tcl
# Writes: tmp/week28_overlap.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week28_overlap.gds]

set L [layout create]
$L units microns 1000
$L create cell TOP
foreach ly {1 2 3 4 5 6} { $L create layer $ly }

# L1: (0,0)-(20,20)   L2: (10,10)-(30,30)  → overlap (10,10)-(20,20)
$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 2_0 10 10 30 30

$L gdsout $gds TOP
puts "Wrote $gds"
puts "L1 npoly=[llength [$L iterator poly TOP 1 range 0 end]]"
puts "L2 npoly=[llength [$L iterator poly TOP 2 range 0 end]]"
puts "Overlap region should be about (10,10)-(20,20)"
exit
