proc parsePaths {text} {
    # 返回 dict: paths、rejected。
    error "请实现教学报告解析"
}
proc selectPaths {paths {threshold 0}} {
    error "请实现筛选和严重程度排序"
}
proc showPathReport {text} {puts [parsePaths $text]}
set channel [open paths.txt r]
set text [read $channel]; close $channel
showPathReport $text
