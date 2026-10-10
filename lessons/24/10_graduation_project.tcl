# 10_graduation_project.tcl — Week 24 Day 5: graduation (brick array + report)
# Run: make week24-10
#      ./scripts/run_calibre_tcl.sh lessons/24/10_graduation_project.tcl
# Writes: tmp/week24_graduation.gds
#
# Combines: layout create, create cell/layer, polygon, create ref (array),
#           text, gdsout, peek, cells, bbox, exists

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week24_graduation.gds]

puts "================================"
puts "   WEEK 10 GRADUATION PROJECT"
puts "   Brick array layout"
puts "================================"

# --- CREATE ---
set L [layout create]
$L units microns 1000
$L create cell BRICK
$L create layer 1.0
$L create layer 2.0

# --- GEOMETRY (leaf) ---
$L create polygon BRICK 1.0 0 0 12 8

# --- HIERARCHY (array of bricks) ---
$L create cell TOP
$L create ref TOP BRICK 0 0 0 0 1 3 2 16 12
$L create text TOP 2.0 0 30 "GRAD"

# --- EXPORT ---
$L gdsout $gds TOP
puts "Wrote $gds ([file size $gds] bytes)"

# --- QUERY ---
puts "--------------------------------"
puts "peek cells  : [layout peek $gds -cells]"
puts "peek layers : [layout peek $gds -layers]"
puts "peek top    : [layout peek $gds -topcell]"
puts "\$L cells    : [$L cells]"
puts "\$L layers   : [$L layers]"
puts "children    : [$L children TOP]"
if {[$L exists cell TOP]} {
    puts "bbox TOP    : [$L bbox TOP]"
}
puts "================================"
puts "Used APIs: create, polygon, create ref, text, gdsout, peek, cells, bbox"
exit
