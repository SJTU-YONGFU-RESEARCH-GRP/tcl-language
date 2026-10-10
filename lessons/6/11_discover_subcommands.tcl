# 11_discover_subcommands.tcl — Week 6: list string ensemble map keys
# Run: make week6-11

set keys [lsort [dict keys [namespace ensemble configure string -map]]]
puts "string subcommands ([llength $keys]):"
puts [join $keys ", "]
exit
