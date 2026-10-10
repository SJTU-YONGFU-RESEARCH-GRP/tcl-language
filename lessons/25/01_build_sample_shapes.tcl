# 01_build_sample_shapes.tcl — Week 25 Day 1: GDS with known poly/wire/text
# Run: make week25-01
#      ./scripts/run_calibre_tcl.sh lessons/25/01_build_sample_shapes.tcl
# Writes: tmp/week25_shapes.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week25_shapes.gds]

set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1
$L create layer 2

$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 1_0 30 0 50 20
$L create wire TOP 2_0 4 0 40 80 40
$L create text TOP 1 5 30 HI

$L gdsout $gds TOP
puts "Sample shapes written: $gds"
puts "Expected: 2 polygons on L1, 1 wire on L2, 1 text on L1"
exit
