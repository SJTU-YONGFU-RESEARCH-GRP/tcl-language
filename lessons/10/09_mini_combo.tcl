# 09_mini_combo.tcl — Week 10: mini combo create + geometry + query
# Run: make week10-09
#      ./scripts/run_calibre_tcl.sh lessons/10/09_mini_combo.tcl
# Writes: tmp/week10_09_combo.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week10_09_combo.gds]

# CREATE
set L [layout create]
$L units microns 1000
$L create cell BRICK
$L create layer 1
$L create layer 2

# GEOMETRY
$L create polygon BRICK 1 0 0 15 10
$L create cell TOP
$L create ref TOP BRICK 0 0 0 0 1
$L create ref TOP BRICK 20 0 0 0 1
$L create text TOP 2 0 15 "COMBO"
$L gdsout $gds TOP

# QUERY
puts "=== mini combo report ==="
puts "cells  : [$L cells]"
puts "layers : [$L layers]"
puts "bbox   : [$L bbox TOP]"
puts "peek   : cells=[layout peek $gds -cells]"
puts "Wrote $gds"
exit
