# 02_flatten_usage_hint.tcl — Week 26: catch Usage for flatten / expand
# Run: make week26-02
#      ./scripts/run_calibre_tcl.sh lessons/26/02_flatten_usage_hint.tcl

set L [layout create]

puts "=== flatten (incomplete call) ==="
if {[catch {$L flatten} msg]} {
    puts $msg
}

puts ""
puts "=== expand (incomplete call) ==="
if {[catch {$L expand} msg]} {
    puts $msg
}

puts ""
puts "Tip: flatten cell <name>  |  expand ref <incell> <refcell> x y mirror angle mag"
exit
