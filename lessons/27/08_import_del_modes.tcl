# 08_import_del_modes.tcl — Week 27 Day 4: del flag + conflict modes
# Run: make week27-08
#      ./scripts/run_calibre_tcl.sh lessons/27/08_import_del_modes.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week27_right.gds]
if {![file exists $gds]} {
    set L0 [layout create]
    $L0 units microns 1000
    $L0 create cell RIGHT
    $L0 create layer 1
    $L0 create polygon RIGHT 1_0 0 0 8 8
    file mkdir [file dirname $gds]
    $L0 gdsout $gds RIGHT
}

# del=1 removes the source handle after import
set src [layout create $gds -dt_expand]
set L [layout create]
$L import layout $src 1 append
puts "del=1 append -> L cells=[$L cells]  src alive=[expr {[catch {$src cells}] == 0}]"

# Conflict modes when both have cell B
proc conflict_demo {mode} {
    set src [layout create]
    $src units microns 1000
    $src create cell B
    $src create layer 1
    $src create polygon B 1_0 0 0 8 8

    set L [layout create]
    $L create cell B
    $L create layer 1
    $L create polygon B 1_0 90 90 100 100

    $L import layout $src 0 $mode
    puts "mode=$mode -> cells=[$L cells] npoly_B=[llength [$L iterator poly B 1 range 0 end]]"
}

puts ""
puts "Same cell name B already in destination:"
conflict_demo append
conflict_demo overwrite
conflict_demo rename
exit
