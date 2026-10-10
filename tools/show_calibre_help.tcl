# show_calibre_help.tcl — print Calibre layout help discovered from Usage errors
# Usage: ./scripts/run_calibre_tcl.sh tools/show_calibre_help.tcl
#        make help-calibre

proc showUsage {script} {
    if {[catch {uplevel 1 $script} msg]} {
        if {[string match "Usage:*" $msg] || [string match "wrong # args:*" $msg]} {
            return $msg
        }
        return "error: $msg"
    }
    return "(ok — no usage message)"
}

puts "=== Calibre DESIGNrev — layout help ==="
puts "Tip: Calibredrv teaches syntax when arguments are missing."
puts ""

puts "--- layout (global command) ---"
puts [showUsage {layout}]
puts ""

foreach sub {create peek filemerge} {
    puts "--- layout $sub ---"
    puts [showUsage [list layout $sub]]
    puts ""
}

set L [layout create]
puts "Sample handle: $L"
puts ""

puts "--- \$L create (sub-types) ---"
puts [showUsage [list $L create]]
foreach kind {cell layer polygon wire text ref} {
    puts [showUsage [list $L create $kind]]
}
puts ""

foreach sub {gdsout exists bbox iterator delete} {
    puts "--- \$L $sub ---"
    puts [showUsage [list $L $sub]]
    puts ""
}

puts "=== Other discovery tips ==="
puts "  layout peek FILE -cells|-layers|-topcell|-precision"
puts "  Manual HTML TOC: calbr_drv_ref (see PLAN.md paths)"
puts "  Full API: Layout Commands + Layout Object in reference manual"
puts ""

exit
