# 02_iterator_usage_hint.tcl — Week 25: let Calibre print Usage
# Run: make week25-02
#      ./scripts/run_calibre_tcl.sh lessons/25/02_iterator_usage_hint.tcl

set L [layout create]
$L create cell TOP
$L create layer 1

puts "=== Asking Calibre for iterator syntax ==="
if {[catch {$L iterator poly} msg]} {
    puts $msg
}
puts ""
puts "We will use:  \$L iterator poly TOP 1 range 0 end"
exit
