# 01_build_hierarchy.tcl — Week 26 Day 1: BOX cell + two refs in TOP
# Run: make week26-01
#      ./scripts/run_calibre_tcl.sh lessons/26/01_build_hierarchy.tcl
# Writes: tmp/week26_hier.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week26_hier.gds]

set L [layout create]
$L units microns 1000

$L create cell BOX
$L create layer 1
$L create polygon BOX 1_0 0 0 10 10

$L create cell TOP
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 20 0 0 0 1

$L gdsout $gds TOP
puts "Hierarchy GDS: $gds"
puts "cells = [$L cells]"
puts "children TOP = [$L children TOP]"
puts "refs TOP = [$L iterator ref TOP range 0 end]"
puts "poly on TOP (before flatten) = [llength [$L iterator poly TOP 1 range 0 end]]"
puts "poly on BOX = [llength [$L iterator poly BOX 1 range 0 end]]"
exit
