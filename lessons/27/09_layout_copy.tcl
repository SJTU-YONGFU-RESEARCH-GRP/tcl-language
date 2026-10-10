# 09_layout_copy.tcl — Week 27 bonus helper: layout copy
# Run: make week27-09
#      ./scripts/run_calibre_tcl.sh lessons/27/09_layout_copy.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week27_left.gds]
if {![file exists $gds]} {
    set L0 [layout create]
    $L0 units microns 1000
    $L0 create cell LEFT
    $L0 create layer 1
    $L0 create polygon LEFT 1_0 0 0 10 10
    file mkdir [file dirname $gds]
    $L0 gdsout $gds LEFT
}

set src [layout create $gds -dt_expand]
set dup [layout copy $src]
puts "src=$src cells=[$src cells]"
puts "dup=$dup cells=[$dup cells]"
puts "dup npoly=[llength [$dup iterator poly LEFT 1 range 0 end]]"
puts "layout copy = in-memory photocopy (handy before risky edits)."
exit
