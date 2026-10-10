# 02_boolean_usage.tcl — Week 28: catch Usage for AND / OR / NOT / SIZE
# Run: make week28-02
#      ./scripts/run_calibre_tcl.sh lessons/28/02_boolean_usage.tcl

set L [layout create]

foreach op {AND OR NOT XOR SIZE} {
    puts "=== $op ==="
    if {[catch {$L $op} msg]} {
        puts $msg
    }
    puts ""
}

puts "Kid patterns:"
puts "  \$L AND 1 2 3"
puts "  \$L OR  1 2 4"
puts "  \$L NOT 1 2 5"
puts "  \$L SIZE 1 3 by 0.001"
exit
