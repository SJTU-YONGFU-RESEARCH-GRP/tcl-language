# Week 6: clean a string, summarize it, and write a text report.
# Run: tclsh homework/week06/string_toolkit.tcl

# Challenge: remove edge whitespace, lowercase, then map spaces to underscores.
proc slugify {s} {
    set trimmed [string trim $s]
    set lower [string tolower $trimmed]
    return [string map {" " "_"} $lower]
}

# Example text; each step demonstrates one string operation.
set raw "   VLSI / EDA Tcl FLOW   "
set trimmed [string trim $raw]
set lower [string tolower $trimmed]
set clean [string map {/ and} $lower]
set length [string length $clean]
set firstChar [string index $clean 0]
set hasEda [string match {*eda*} $clean]
set slug [slugify "   $clean   "]

# Construct a portable output path relative to this script.
set scriptDir [file dirname [file normalize [info script]]]
set outputDir [file join $scriptDir output]
file mkdir $outputDir
set reportPath [file join $outputDir string_toolkit_report.txt]

set lines [list \
    "Week 6 string toolkit" \
    "========================================" \
    "Raw: <$raw>" \
    "Trimmed: <$trimmed>" \
    "Lowercase: $lower" \
    "Mapped: $clean" \
    "Length of mapped text: $length" \
    "First character: $firstChar" \
    "Matches *eda*: $hasEda" \
    "Slug: $slug" \
    "========================================"]

# Write the report, then read back exactly what was saved.
set fh [open $reportPath w]
foreach line $lines {
    puts $fh $line
}
close $fh

puts "Report: homework/week06/output/string_toolkit_report.txt"
set fh [open $reportPath r]
while {[gets $fh line] >= 0} {
    puts $line
}
close $fh
