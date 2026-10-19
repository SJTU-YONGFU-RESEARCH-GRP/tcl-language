# Execute after the project implementation: 非法值、无穷、上下界反转
foreach bad {oops NaN Inf 1e999} {
    catch {measurementStats [list 2 $bad] 0 10} message
    puts $message
}
catch {measurementStats {1} 5 2} message
puts $message
