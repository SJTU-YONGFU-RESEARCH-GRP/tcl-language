# 06_iterator_text.tcl — Week 25 Day 2: iterate text
# Run: make week25-06
#      ./scripts/run_calibre_tcl.sh lessons/25/06_iterator_text.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week25_shapes.gds]
if {![file exists $gds]} {
    puts "Run make week25-01 first"
    exit 1
}

set L [layout create $gds]
set texts [$L iterator text TOP 1 range 0 end]

puts "=== iterator text TOP layer 1 ==="
puts "count = [llength $texts]"
foreach t $texts {
    puts "text entry: $t"
}
exit
