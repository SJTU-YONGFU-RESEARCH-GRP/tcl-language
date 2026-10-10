# 02_units_microns.tcl — Week 22: set database units (ruler scale)
# Run: make week22-02
#      ./scripts/run_calibre_tcl.sh lessons/22/02_units_microns.tcl

set L [layout create]
# 1000 database units = 1 micron (common setting for new layouts)
$L units microns 1000
$L create cell TOP
$L create layer 1
$L create polygon TOP 1 0 0 10 10

puts "Layout $L: units microns 1000 set"
puts "Drew a small 10x10 box on TOP / layer 1"
exit
