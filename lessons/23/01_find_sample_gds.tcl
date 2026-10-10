# 01_find_sample_gds.tcl — Week 23 Day 1: pick a GDS to inspect
# Run: make week23-01
#      ./scripts/run_calibre_tcl.sh lessons/23/01_find_sample_gds.tcl
# Prefer Week 8 output; fall back to other tmp GDS files.

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set candidates [list \
    [file join $repoRoot tmp week8_my_shapes.gds] \
    [file join $repoRoot tmp week8_01_box.gds] \
    [file join $repoRoot tmp demo_box.gds] \
    [file join $repoRoot tmp week7_script1.gds]]

set gds ""
foreach c $candidates {
    if {[file exists $c]} {
        set gds $c
        break
    }
}

if {$gds eq ""} {
    puts "ERROR: no sample GDS found. Run: make week8-10"
    exit 1
}

puts "Using sample GDS:"
puts "  $gds"
puts "size=[file size $gds] bytes"
puts "Tip: pass another file later as argv (see 10_report_gds.tcl)"
exit
