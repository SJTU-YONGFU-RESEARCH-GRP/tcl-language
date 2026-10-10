# 06_two_layer_house.tcl — Week 24: house on two layers + door text
# Run: make week24-06
#      ./scripts/run_calibre_tcl.sh lessons/24/06_two_layer_house.tcl
# Writes: tmp/week24_06_house.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week24_06_house.gds]

set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1.0
$L create layer 2.0

# Body on layer 1
$L create polygon TOP 1.0 0 0 100 60
# Roof-ish triangle-ish on layer 2 (simple box above)
$L create polygon TOP 2.0 0 60 100 60 50 90
$L create text TOP 1.0 35 20 "HOME"

$L gdsout $gds TOP
puts "House: body L1 + roof L2 + text"
puts "Wrote $gds ([file size $gds] bytes)"
exit
