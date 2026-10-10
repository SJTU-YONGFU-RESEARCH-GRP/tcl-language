# 03_create_ref_once.tcl — Week 10: place BOX once inside TOP
# Run: make week10-03
#      ./scripts/run_calibre_tcl.sh lessons/10/03_create_ref_once.tcl
# Writes: tmp/week10_03_one_ref.gds
#
# create ref: incell refcell x y mirror angle mag

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week10_03_one_ref.gds]

set L [layout create]
$L units microns 1000

$L create cell BOX
$L create layer 1.0
$L create polygon BOX 1.0 0 0 20 20

$L create cell TOP
# Place BOX into TOP at (0,0); mirror=0; angle=0; mag=1
$L create ref TOP BOX 0 0 0 0 1

puts "TOP contains one BOX via create ref"
puts "cells=[$L cells] children of TOP=[$L children TOP]"
$L gdsout $gds TOP
puts "Wrote $gds ([file size $gds] bytes)"
exit
