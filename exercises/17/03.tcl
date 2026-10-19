proc attentionPaths {records} {
    # 构造排序行，只选择严格负值
}
set paths [list     [dict create path a slack -0.2]     [dict create path b slack 0.0]     [dict create path c slack -1.1]]
foreach row [attentionPaths $paths] {
    lassign $row slack path
    puts [format "%s：%.2f ns" $path $slack]
}
