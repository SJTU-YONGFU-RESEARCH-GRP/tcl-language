proc reportArgs {argsList} {
    if {[llength $argsList] != 2} { error "需要标题和输入文件两个参数" }
    lassign $argsList title inputPath
    return [dict create title $title input $inputPath]
}
set request [reportArgs $argv]
puts [dict get $request title]
puts [dict get $request input]
