proc measurementStats {values lower upper} {
    # 先检查上下界，再逐项验证和累计；空列表要单独处理。
    error "请实现 measurementStats"
}
proc showMeasurements {values lower upper} {
    puts [measurementStats $values $lower $upper]
}
showMeasurements {9.5 10 10.5 13} 9 12
