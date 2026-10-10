# 09_layout_dt_expand.tcl — Week 21: layout create with -dt_expand option
# Run: make week21-09
#      ./scripts/run_calibre_tcl.sh lessons/21/09_layout_dt_expand.tcl
#
# -dt_expand keeps layer/datatype separate (do not merge different datatypes).

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week21_script1.gds]

if {![file exists $gds]} {
    puts "Need $gds — run make week21-07 first."
    exit 1
}

set Lplain [layout create $gds]
set Lexpand [layout create $gds -dt_expand]

puts "Opened without -dt_expand : $Lplain"
puts "Opened with    -dt_expand : $Lexpand"
puts "Both are handles. -dt_expand is for layer/datatype detail."

exit
