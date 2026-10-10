# 11_oasisout_optional.tcl — Week 8 bonus: write OASIS as well as GDS
# Run: make week8-11
#      ./scripts/run_calibre_tcl.sh lessons/8/11_oasisout_optional.tcl
# Writes: tmp/week8_11.gds and tmp/week8_11.oas

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week8_11.gds]
set oas [file join $outDir week8_11.oas]

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
