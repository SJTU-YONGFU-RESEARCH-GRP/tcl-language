# 10_dump_shapes.tcl — Week 11 Day 5 project: dump shape summary
# Run: make week11-10
#      ./scripts/run_calibre_tcl.sh lessons/11/10_dump_shapes.tcl
#      ./scripts/run_calibre_tcl.sh lessons/11/10_dump_shapes.tcl -- tmp/week10_graduation.gds
# Writes: tmp/week11_dump.txt

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [lindex $argv 0]
if {$gds eq ""} {
    set gds [file join $repoRoot tmp week11_shapes.gds]
}
if {![file exists $gds]} {
    puts "ERROR: missing $gds — run make week11-01"
    exit 1
}

set L [layout create $gds]
set top [$L topcell]
set report [file join $repoRoot tmp week11_dump.txt]
set fh [open $report w]

puts $fh "SHAPE DUMP"
puts $fh "file: $gds"
puts $fh "top : $top"
puts $fh "--------------------------------"

foreach lyr [$L layers] {
    puts $fh "LAYER $lyr"
    set n 0
    foreach p [$L iterator poly $top $lyr range 0 end] {
        incr n
        puts $fh "  poly $n: $p"
    }
    set n 0
    foreach w [$L iterator wire $top $lyr range 0 end] {
        incr n
        puts $fh "  wire $n: $w"
    }
    set n 0
    foreach t [$L iterator text $top $lyr range 0 end] {
        incr n
        puts $fh "  text $n: $t"
    }
}

close $fh
puts "Wrote report: $report"
puts "Preview:"
set fh [open $report r]
while {[gets $fh line] >= 0} {
    puts $line
}
close $fh
exit
