# 11_oasisout_optional.tcl — Week 22 bonus: write OASIS as well as GDS
# Run: make week22-11
#      ./scripts/run_calibre_tcl.sh lessons/22/11_oasisout_optional.tcl
# Writes: tmp/week22_11.gds and tmp/week22_11.oas

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week22_11.gds]
set oas [file join $outDir week22_11.oas]

set L [layout create]
$L create cell TOP
$L create layer 1
$L create polygon TOP 1 0 0 50 50

$L gdsout $gds TOP
puts "GDS   : $gds ([file size $gds] bytes)"

$L oasisout $oas TOP
puts "OASIS : $oas ([file size $oas] bytes)"
puts "Same drawing, two file formats."
exit
