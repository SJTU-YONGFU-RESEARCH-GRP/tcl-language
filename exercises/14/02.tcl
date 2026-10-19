proc reportArgs {argsList} {
    # 校验列表长度，再建立字典
}
set request [reportArgs $argv]
puts [dict get $request title]
puts [dict get $request input]
