# 11_iterator_ref_bonus.tcl — Week 25 bonus: iterator ref (placements)
# Run: make week25-11
#      ./scripts/run_calibre_tcl.sh lessons/25/11_iterator_ref_bonus.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week10_refs.gds]
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week10_graduation.gds]
}
if {![file exists $gds]} {
    puts "ERROR: need a hierarchical GDS (make week10-04 or week10-10)"
    exit 1
}

set L [layout create $gds]
set top [$L topcell]

puts "file=$gds top=$top"
puts "=== Usage hint for iterator ref ==="
if {[catch {$L iterator ref} msg]} {
    puts $msg
}

puts ""
puts "=== try: iterator ref $top range 0 end ==="
if {[catch {set refs [$L iterator ref $top range 0 end]; puts "refs=$refs count=[llength $refs]"} e]} {
    puts "ERR: $e"
}
exit
