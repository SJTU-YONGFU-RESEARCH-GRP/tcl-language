set runCount 0
proc recordRun {} {
    global runCount
    return [incr runCount]
}
puts [recordRun]
puts [recordRun]
