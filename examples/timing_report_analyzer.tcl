#!/usr/bin/env tclsh
# timing_report_analyzer.tcl — Industrial Static Timing Analysis (STA) Report Parser
#
# A capstone EDA automation lab script that reads an STA timing report, parses
# critical path timing information (Startpoint, Endpoint, Path Group, Slack),
# and computes key VLSI sign-off metrics:
#   - Worst Negative Slack (WNS)
#   - Total Negative Slack (TNS)
#   - Violating Paths Count & Summary Table
#
# Usage:
#   tclsh examples/timing_report_analyzer.tcl ?report_file?

namespace eval ::sta_analyzer {
    # Parse a timing report file and return a list of path dictionaries
    proc parse_report {filepath} {
        if {![file exists $filepath]} {
            error "Report file not found: $filepath"
        }

        set fh [open $filepath r]
        fconfigure $fh -encoding utf-8

        set paths [list]
        set current_path [dict create]
        set in_path 0

        try {
            while {[gets $fh line] >= 0} {
                set trimmed [string trim $line]

                # Match Startpoint
                if {[regexp {^\s*Startpoint:\s*(\S+)} $line -> sp]} {
                    if {[dict size $current_path] > 0 && [dict exists $current_path slack]} {
                        lappend paths $current_path
                    }
                    set current_path [dict create startpoint $sp]
                    continue
                }

                # Match Endpoint
                if {[regexp {^\s*Endpoint:\s*(\S+)} $line -> ep]} {
                    dict set current_path endpoint $ep
                    continue
                }

                # Match Path Group
                if {[regexp {^\s*Path Group:\s*(\S+)} $line -> pg]} {
                    dict set current_path path_group $pg
                    continue
                }

                # Match Slack line: e.g. slack (VIOLATED) -0.11 or slack (MET) 1.15
                if {[regexp {^\s*slack\s*\((VIOLATED|MET)\)\s*([+-]?[0-9]*\.?[0-9]+)} $line -> status slack_val]} {
                    dict set current_path status $status
                    dict set current_path slack [expr {$slack_val + 0.0}]
                    lappend paths $current_path
                    set current_path [dict create]
                    continue
                }
            }
        } finally {
            close $fh
        }

        return $paths
    }

    # Compute WNS, TNS, and violation summary from parsed paths
    proc summarize {paths} {
        set total [llength $paths]
        set violations 0
        set wns 0.0
        set tns 0.0

        foreach p $paths {
            set s [dict get $p slack]
            if {$s < 0.0} {
                incr violations
                set tns [expr {$tns + $s}]
                if {$s < $wns} {
                    set wns $s
                }
            }
        }

        return [dict create \
            total_paths $total \
            violations $violations \
            wns [format "%.3f" $wns] \
            tns [format "%.3f" $tns] \
        ]
    }

    # Print a formatted summary report to stdout
    proc print_report {paths summary} {
        puts "======================================================================"
        puts "        VLSI Static Timing Analysis (STA) Slack Summary Report        "
        puts "======================================================================"
        puts [format "%-35s %-35s %-10s %s" "Startpoint" "Endpoint" "Slack(ns)" "Status"]
        puts [string repeat "-" 90]

        foreach p $paths {
            set sp [dict get $p startpoint]
            set ep [dict get $p endpoint]
            set sl [dict get $p slack]
            set st [dict get $p status]

            # Truncate long pin names for tidy terminal output
            if {[string length $sp] > 33} { set sp "[string range $sp 0 30]..." }
            if {[string length $ep] > 33} { set ep "[string range $ep 0 30]..." }

            set tag [expr {$st eq "VIOLATED" ? "\[VIOLATION\]" : "\[MET\]"}]
            puts [format "%-35s %-35s %10.3f  %s" $sp $ep $sl $tag]
        }

        puts [string repeat "=" 90]
        puts "SIGN-OFF METRICS:"
        puts "  Total Paths Analyzed   : [dict get $summary total_paths]"
        puts "  Violating Paths        : [dict get $summary violations]"
        puts "  Worst Negative Slack   : [dict get $summary wns] ns"
        puts "  Total Negative Slack   : [dict get $summary tns] ns"
        if {[dict get $summary violations] > 0} {
            puts "  Timing Sign-Off Status : FAIL (Timing Closure Required)"
        } else {
            puts "  Timing Sign-Off Status : PASS (Timing Met)"
        }
        puts "======================================================================"
    }
}

# Main execution entry
set report_file [file join [file dirname [info script]] "data" "sample_timing.rpt"]
if {[llength $argv] > 0} {
    set report_file [lindex $argv 0]
}

puts "Reading timing report: $report_file\n"
set parsed_paths [::sta_analyzer::parse_report $report_file]
set summary_dict [::sta_analyzer::summarize $parsed_paths]
::sta_analyzer::print_report $parsed_paths $summary_dict
