# 08_exists_layer_and_file.tcl — Week 9: exists layer + $L file
# Run: make week9-08
#      ./scripts/run_calibre_tcl.sh lessons/9/08_exists_layer_and_file.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week8_my_shapes.gds]
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week8_01_box.gds]
}
if {![file exists $gds]} {
    puts "ERROR: run make week8-10 first"
    exit 1
}

set L [layout create $gds -dt_expand]

puts "source file : [$L file]"
puts "layers list : [$L layers]"

foreach lyr {1 2 99} {
    if {[$L exists layer $lyr]} {
        puts "layer $lyr : YES"
    } else {
        puts "layer $lyr : no"
    }
}
exit
