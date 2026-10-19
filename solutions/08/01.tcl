set sample [dict create id S-08 status waiting count 4]
dict set sample status done
dict set sample count [expr {[dict get $sample count] + 1}]
puts "[dict get $sample status] / [dict get $sample count]"
