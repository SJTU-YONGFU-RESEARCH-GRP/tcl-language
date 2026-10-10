# 02_filemerge_usage.tcl — Week 27: catch Usage for layout filemerge
# Run: make week27-02
#      ./scripts/run_calibre_tcl.sh lessons/27/02_filemerge_usage.tcl

puts "=== layout filemerge (no args) ==="
if {[catch {layout filemerge} msg]} {
    puts $msg
}
puts ""
puts "Kid-sized pattern:"
puts "  layout filemerge -in a.gds -in b.gds -out out.gds"
exit
