# Week 5: reusable procedures and a file log that is read back.
# Run: tclsh homework/week05/toolbox.tcl

# Return a greeting for the caller to print or log.
proc greet {name} {
    return "Hello, $name!"
}

# Return the sum instead of printing inside this procedure.
proc add {a b} {
    return [expr {$a + $b}]
}

# Label example scores using the course's Pass/Fail threshold.
proc checkResult {score} {
    if {$score >= 60} {
        return "Pass"
    } else {
        return "Fail"
    }
}

# Append one result to the log and close the channel immediately.
proc appendLog {path message} {
    set fh [open $path a]
    puts $fh $message
    close $fh
}

# Locate output relative to this script, independent of the shell directory.
set scriptDir [file dirname [file normalize [info script]]]
set outputDir [file join $scriptDir output]
file mkdir $outputDir
set logPath [file join $outputDir toolbox_log.txt]

# Start a fresh log for each run; subsequent entries use append mode.
set fh [open $logPath w]
puts $fh "Week 5 toolbox results"
puts $fh "Scores below are example data, not real grades."
close $fh

appendLog $logPath [greet "GateUltra"]
set sum [add 84 6]
appendLog $logPath "add(84, 6) = $sum"

# Include the passing boundary and a failing score to show both branches.
set scores [list $sum 60 59]
foreach score $scores {
    set result [checkResult $score]
    appendLog $logPath "Example score $score: $result"
}

# Read back the file so the console shows the results actually written.
puts "Log: homework/week05/output/toolbox_log.txt"
set fh [open $logPath r]
while {[gets $fh line] >= 0} {
    puts $line
}
close $fh
