# 10_toolbox.tcl — Week 5 Day 5 project: toolbox (procs + file log)
# Run: make week5-10
#      tclsh lessons/5/10_toolbox.tcl
# Writes: tmp/week5_toolbox_log.txt

proc greet {name} {
    return "Hi $name!"
}

proc add {a b} {
    return [expr {$a + $b}]
}

proc printList {title items} {
    puts "=== $title ==="
    foreach item $items {
        puts "  - $item"
    }
}

proc appendLog {path message} {
    set fh [open $path a]
    puts $fh $message
    close $fh
}

file mkdir tmp
set logPath tmp/week5_toolbox_log.txt

set fh [open $logPath w]
puts $fh "Toolbox session started"
close $fh

set msg1 [greet "Amy"]
puts $msg1
appendLog $logPath $msg1

set sum [add 40 50]
puts "40 + 50 = $sum"
appendLog $logPath "add result: $sum"

set tools [list hammer ruler glue]
printList "My toolbox" $tools
appendLog $logPath "printed toolbox list"

puts ""
puts "Log written to $logPath"
puts "=== Log contents ==="
set fh [open $logPath r]
while {[gets $fh line] >= 0} {
    puts $line
}
close $fh
