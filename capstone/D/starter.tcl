proc diagnoseLog {text {radius 1}} {
    # 返回 dict: counts incidents invalid。
    error "请实现日志解析与上下文收集"
}
proc showDiagnosis {text {radius 1}} {puts [diagnoseLog $text $radius]}
set log "09:00:00 INFO start\n09:00:01 INFO read input\n09:00:02 WARN slow read\n09:00:03 INFO retry\n09:00:04 ERROR missing result\n09:00:05 INFO stop"
showDiagnosis $log
