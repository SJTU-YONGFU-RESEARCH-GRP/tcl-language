# 07_import_layout.tcl — Week 27 Day 4: $L import layout $src $del $mode
# Run: make week27-07
#      ./scripts/run_calibre_tcl.sh lessons/27/07_import_layout.tcl
#
# Working form on this machine:
#   $L import layout $src 0 append   ;# del=0 keep source alive
#   $L import layout $src 1 append   ;# del=1 destroy source handle

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set right [file join $repoRoot tmp week27_right.gds]
if {![file exists $right]} {
    set L0 [layout create]
    $L0 units microns 1000
    $L0 create cell RIGHT
    $L0 create layer 1
    $L0 create polygon RIGHT 1_0 0 0 8 8
    file mkdir [file join $repoRoot tmp]
    $L0 gdsout $right RIGHT
}

set src [layout create $right -dt_expand]
set L [layout create]
$L create cell TOP
$L create layer 1
$L create polygon TOP 1_0 0 0 2 2

puts "BEFORE import: L cells=[$L cells]  src cells=[$src cells]"
$L import layout $src 0 append
puts "AFTER  import layout \$src 0 append"
puts "  L cells   = [$L cells]"
puts "  src alive = [expr {[catch {$src cells}] == 0}]"
foreach c [$L cells] {
    catch {puts "  $c npoly=[llength [$L iterator poly $c 1 range 0 end]]"}
}
exit
