proc attentionPaths {records} {
    set selected {}
    foreach record $records {
        set slack [dict get $record slack]
        if {$slack < 0} {
            lappend selected [list $slack [dict get $record path]]
        }
    }
    return [lsort -real -index 0 $selected]
}
set paths [list     [dict create path a slack -0.2]     [dict create path b slack 0.0]     [dict create path c slack -1.1]]
foreach row [attentionPaths $paths] {
    lassign $row slack path
    puts [format "%s：%.2f ns" $path $slack]
}
