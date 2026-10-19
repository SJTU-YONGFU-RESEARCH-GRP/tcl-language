# drvlite.tcl — DRV-Lite Pure-Tcl Calibre DESIGNrev Simulator
#
# An educational simulator providing a pure-Tcl implementation of Siemens
# Calibre DESIGNrev's `layout` API. Allows students to learn and execute
# IC layout scripting (Weeks 21–40) without needing a commercial license.
#
# Supported commands & methods:
#   layout create ?filename? ?-dt_expand?
#   layout peek <filename> -topcell|-cells|-layers
#   $L create cell <name>
#   $L create layer <layer_num>
#   $L create polygon <cell> <layer> <x1> <y1> <x2> <y2> ...
#   $L create wire <cell> <layer> <width> <x1> <y1> ...
#   $L create text <cell> <layer> <x> <y> <text>
#   $L create ref <parent_cell> <child_cell> <x> <y> ?orient?
#   $L bbox <cell>
#   $L topcell
#   $L cells
#   $L layers ?cell?
#   $L exists cell <name>
#   $L exists layer <cell> <layer>
#   $L gdsout <filename> ?topcell?
#   $L oasisout <filename> ?topcell?
#   $L delete cell <name>

namespace eval ::drvlite {
    variable handle_counter 0
    variable layouts
    array set layouts {}

    # Initialize simulator banner once
    variable banner_shown 0
    proc show_banner {} {
        variable banner_shown
        if {!$banner_shown} {
            puts "======================================================================"
            puts { [DRV-Lite] Calibre DESIGNrev Educational Simulator (Pure-Tcl Mode)}
            puts " No commercial license required. Simulating layout object model."
            puts "======================================================================"
            set banner_shown 1
        }
    }

    # Dispatcher for layout object handles: $L method ...
    proc dispatch {handle cmd args} {
        variable layouts
        if {![info exists layouts($handle)]} {
            error "Unknown layout handle: $handle"
        }

        switch -exact -- $cmd {
            "create" {
                set sub [lindex $args 0]
                set subargs [lrange $args 1 end]
                switch -exact -- $sub {
                    "cell" {
                        set cell [lindex $subargs 0]
                        if {$cell eq ""} { error "create cell requires a cell name" }
                        set cells [dict get $layouts($handle) cells]
                        if {![dict exists $cells $cell]} {
                            set cell_dict [dict create layers [dict create] bbox {}]
                            dict set layouts($handle) cells $cell $cell_dict
                            if {[dict get $layouts($handle) topcell] eq ""} {
                                dict set layouts($handle) topcell $cell
                            }
                        }
                        return $cell
                    }
                    "layer" {
                        set layer [lindex $subargs 0]
                        set layer_list [dict get $layouts($handle) all_layers]
                        if {[lsearch -exact $layer_list $layer] == -1} {
                            lappend layer_list $layer
                            dict set layouts($handle) all_layers [lsort -integer $layer_list]
                        }
                        return $layer
                    }
                    "polygon" {
                        set cell [lindex $subargs 0]
                        set layer [lindex $subargs 1]
                        set coords [lrange $subargs 2 end]
                        if {[llength $coords] == 1} { set coords [lindex $coords 0] }
                        if {[llength $coords] < 6} {
                            error "Polygon requires at least 3 points (6 coordinates)"
                        }
                        ::drvlite::record_shape $handle $cell $layer "polygon" $coords
                        return ""
                    }
                    "wire" {
                        set cell [lindex $subargs 0]
                        set layer [lindex $subargs 1]
                        set width [lindex $subargs 2]
                        set coords [lrange $subargs 3 end]
                        if {[llength $coords] == 1} { set coords [lindex $coords 0] }
                        ::drvlite::record_shape $handle $cell $layer "wire" [list $width $coords]
                        return ""
                    }
                    "text" {
                        set cell [lindex $subargs 0]
                        set layer [lindex $subargs 1]
                        set x [lindex $subargs 2]
                        set y [lindex $subargs 3]
                        set text [lindex $subargs 4]
                        ::drvlite::record_shape $handle $cell $layer "text" [list $x $y $text]
                        return ""
                    }
                    "ref" {
                        set parent [lindex $subargs 0]
                        set child [lindex $subargs 1]
                        set x [lindex $subargs 2]
                        set y [lindex $subargs 3]
                        set orient [lindex $subargs 4]
                        ::drvlite::record_shape $handle $parent 0 "ref" [list $child $x $y $orient]
                        return ""
                    }
                    default {
                        error "Unknown create sub-command: create $sub"
                    }
                }
            }
            "topcell" {
                return [dict get $layouts($handle) topcell]
            }
            "cells" {
                return [dict keys [dict get $layouts($handle) cells]]
            }
            "layers" {
                set cell [lindex $args 0]
                if {$cell ne ""} {
                    set cells [dict get $layouts($handle) cells]
                    if {[dict exists $cells $cell]} {
                        set cell_dict [dict get $cells $cell]
                        return [lsort -integer [dict keys [dict get $cell_dict layers]]]
                    }
                    return {}
                }
                return [dict get $layouts($handle) all_layers]
            }
            "exists" {
                set what [lindex $args 0]
                if {$what eq "cell"} {
                    set cell [lindex $args 1]
                    return [dict exists [dict get $layouts($handle) cells] $cell]
                } elseif {$what eq "layer"} {
                    set cell [lindex $args 1]
                    set layer [lindex $args 2]
                    set cells [dict get $layouts($handle) cells]
                    if {[dict exists $cells $cell]} {
                        return [dict exists [dict get $cells $cell layers] $layer]
                    }
                    return 0
                }
                error "Unknown exists query: exists $what"
            }
            "bbox" {
                set cell [lindex $args 0]
                set cells [dict get $layouts($handle) cells]
                if {![dict exists $cells $cell]} {
                    error "Cell '$cell' does not exist in layout"
                }
                set bb [dict get $cells $cell bbox]
                if {[llength $bb] == 0} {
                    return [list 0 0 0 0]
                }
                return $bb
            }
            "delete" {
                set what [lindex $args 0]
                if {$what eq "cell"} {
                    set cell [lindex $args 1]
                    set cells [dict get $layouts($handle) cells]
                    if {[dict exists $cells $cell]} {
                        dict unset layouts($handle) cells $cell
                    }
                    return ""
                }
                error "Unknown delete sub-command: delete $what"
            }
            "gdsout" - "oasisout" {
                set out_file [lindex $args 0]
                set top [lindex $args 1]
                if {$top eq ""} { set top [dict get $layouts($handle) topcell] }
                ::drvlite::export_layout_summary $handle $out_file $top
                puts "\[DRV-Lite\] Wrote layout '$top' to $out_file (simulated GDS/OASIS format)"
                return ""
            }
            default {
                error "Unsupported method '$cmd' on layout handle $handle in DRV-Lite"
            }
        }
    }

    # Update cell bounding box with newly added coordinate points
    proc update_bbox {handle cell xs ys} {
        variable layouts
        set cells [dict get $layouts($handle) cells]
        set cell_dict [dict get $cells $cell]
        set current_bb [dict get $cell_dict bbox]

        set min_x [lindex $xs 0]
        set max_x [lindex $xs 0]
        set min_y [lindex $ys 0]
        set max_y [lindex $ys 0]

        foreach x $xs {
            if {$x < $min_x} { set min_x $x }
            if {$x > $max_x} { set max_x $x }
        }
        foreach y $ys {
            if {$y < $min_y} { set min_y $y }
            if {$y > $max_y} { set max_y $y }
        }

        if {[llength $current_bb] == 4} {
            lassign $current_bb c_min_x c_min_y c_max_x c_max_y
            if {$c_min_x < $min_x} { set min_x $c_min_x }
            if {$c_min_y < $min_y} { set min_y $c_min_y }
            if {$c_max_x > $max_x} { set max_x $c_max_x }
            if {$c_max_y > $max_y} { set max_y $c_max_y }
        }

        dict set cell_dict bbox [list $min_x $min_y $max_x $max_y]
        dict set layouts($handle) cells $cell $cell_dict
    }

    # Record shape and update layer tracking
    proc record_shape {handle cell layer type data} {
        variable layouts
        set cells [dict get $layouts($handle) cells]
        if {![dict exists $cells $cell]} {
            set cell_dict [dict create layers [dict create] bbox {}]
            dict set layouts($handle) cells $cell $cell_dict
        }

        # Track layer in cell
        set cell_dict [dict get $layouts($handle) cells $cell]
        set layers_in_cell [dict get $cell_dict layers]
        if {![dict exists $layers_in_cell $layer]} {
            dict set layers_in_cell $layer [list]
        }
        dict lappend layers_in_cell $layer [list $type $data]
        dict set cell_dict layers $layers_in_cell
        dict set layouts($handle) cells $cell $cell_dict

        # Track globally in layout
        set all_layers [dict get $layouts($handle) all_layers]
        if {[lsearch -exact $all_layers $layer] == -1} {
            lappend all_layers $layer
            dict set layouts($handle) all_layers [lsort -integer $all_layers]
        }

        # Update bounding box for polygon/wire
        if {$type eq "polygon"} {
            set xs {}
            set ys {}
            for {set i 0} {$i < [llength $data]} {incr i 2} {
                lappend xs [lindex $data $i]
                lappend ys [lindex $data [expr {$i + 1}]]
            }
            ::drvlite::update_bbox $handle $cell $xs $ys
        } elseif {$type eq "wire"} {
            set coords [lindex $data 1]
            set xs {}
            set ys {}
            for {set i 0} {$i < [llength $coords]} {incr i 2} {
                lappend xs [lindex $coords $i]
                lappend ys [lindex $coords [expr {$i + 1}]]
            }
            ::drvlite::update_bbox $handle $cell $xs $ys
        } elseif {$type eq "text"} {
            set x [lindex $data 0]
            set y [lindex $data 1]
            ::drvlite::update_bbox $handle $cell [list $x] [list $y]
        }
    }

    # Export human-readable ASCII layout summary as standalone file
    proc export_layout_summary {handle filename topcell} {
        variable layouts
        set fh [open $filename w]
        puts $fh "# DRV-Lite GDS/OASIS Simulated Output"
        puts $fh "# Format: GDS-II ASCII Structure"
        puts $fh "# TopCell: $topcell"
        set cells [dict get $layouts($handle) cells]
        foreach cell [dict keys $cells] {
            set cdict [dict get $cells $cell]
            puts $fh "BGNLIB; CELL: $cell; BBOX: [dict get $cdict bbox]"
            set ldict [dict get $cdict layers]
            foreach l [dict keys $ldict] {
                puts $fh "  LAYER $l: [llength [dict get $ldict $l]] shapes"
            }
            puts $fh "ENDCELL"
        }
        close $fh
    }
}

# Top-level 'layout' command (identical to Calibre DESIGNrev CLI)
proc layout {cmd args} {
    ::drvlite::show_banner
    switch -exact -- $cmd {
        "create" {
            variable ::drvlite::handle_counter
            variable ::drvlite::layouts

            set handle "layout$handle_counter"
            incr handle_counter

            # Initialize layout structure
            set ::drvlite::layouts($handle) [dict create \
                topcell "" \
                cells [dict create] \
                all_layers [list] \
                filesource [lindex $args 0] \
            ]

            # Register handle as a callable Tcl command
            interp alias {} $handle {} ::drvlite::dispatch $handle

            # If an input file was provided, load topcell metadata if existing
            set infile [lindex $args 0]
            if {$infile ne "" && [file exists $infile]} {
                # Attempt to extract topcell from file name or comments
                set guessed_top [file rootname [file tail $infile]]
                dict set ::drvlite::layouts($handle) topcell $guessed_top
                set cell_dict [dict create layers [dict create 1 [list [list "polygon" {0 0 1000 0 1000 1000 0 1000}]]] bbox {0 0 1000 1000}]
                dict set ::drvlite::layouts($handle) cells $guessed_top $cell_dict
                dict set ::drvlite::layouts($handle) all_layers {1}
            }

            return $handle
        }
        "peek" {
            set filename [lindex $args 0]
            set option [lindex $args 1]
            if {$filename eq ""} { error "layout peek requires a filename" }
            set basename [file rootname [file tail $filename]]
            switch -exact -- $option {
                "-topcell" { return $basename }
                "-cells" { return [list $basename] }
                "-layers" { return [list 1 2 3] }
                default {
                    return $basename
                }
            }
        }
        "copy" {
            puts "\[DRV-Lite\] layout copy simulated."
            return ""
        }
        default {
            error "Unknown layout command: layout $cmd"
        }
    }
}
