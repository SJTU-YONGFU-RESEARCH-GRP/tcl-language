proc teachingSlack {period delay} {
    return [expr {double($period) - $delay}]
}
puts [format "教学 slack：%.2f ns" [teachingSlack 10 9.5]]
