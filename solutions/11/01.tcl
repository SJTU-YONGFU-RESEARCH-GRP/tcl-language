proc cleanNote {inputPath outputPath} {
    set input [open $inputPath r]
    set cleaned [string trim [read $input]]
    close $input
    set output [open $outputPath w]
    puts $output $cleaned
    close $output
    return $cleaned
}
puts [cleanNote note.txt clean.txt]
