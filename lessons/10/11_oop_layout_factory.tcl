# 11_oop_layout_factory.tcl — Week 10 bonus: TclOO wraps $L methods
# Run: make week10-11
#      ./scripts/run_calibre_tcl.sh lessons/10/11_oop_layout_factory.tcl
# Writes: tmp/week10_11_factory.gds

oo::class create LayoutFactory {
    variable L outPath

    constructor {path} {
        set outPath $path
        set L [layout create]
        $L units microns 1000
    }

    method addRect {cell layer x1 y1 x2 y2} {
        variable L
        if {![$L exists cell $cell]} {
            $L create cell $cell
        }
        catch {$L create layer $layer}
        $L create polygon $cell $layer $x1 $y1 $x2 $y2
    }

    method place {parent child x y} {
        variable L
        if {![$L exists cell $parent]} {
            $L create cell $parent
        }
        $L create ref $parent $child $x $y 0 0 1
    }

    method label {cell layer x y text} {
        variable L
        $L create text $cell $layer $x $y $text
    }

    method save {top} {
        variable L
        variable outPath
        $L gdsout $outPath $top
        puts "saved $outPath"
    }

    method report {top} {
        variable L
        puts "cells=[$L cells] bbox=[$L bbox $top]"
    }
}

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week10_11_factory.gds]

set f [LayoutFactory new $gds]
$f addRect BOX 1 0 0 15 15
$f place TOP BOX 0 0
$f place TOP BOX 25 0
$f label TOP 1 0 20 "OOP"
$f save TOP
$f report TOP
exit
