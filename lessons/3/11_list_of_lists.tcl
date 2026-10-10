# 11_list_of_lists.tcl — Week 3 bonus: a list inside a list
# Run: make week3-11
#      tclsh lessons/3/11_list_of_lists.tcl

# Outer list holds three inner lists (rows)
set table [list \
    [list Name Score] \
    [list Amy 92] \
    [list Bob 88]]

set header [lindex $table 0]
set row1 [lindex $table 1]
set row2 [lindex $table 2]

puts "Whole table : $table"
puts "Header row  : $header"
puts "Row 1       : $row1"
puts "Name in row1: [lindex $row1 0]"
puts "Score row1  : [lindex $row1 1]"
puts "Rows total  : [llength $table]"
