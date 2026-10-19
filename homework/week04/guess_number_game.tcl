# Week 4: a batch game using foreach, if/elseif/else, and break.
# Run: tclsh homework/week04/guess_number_game.tcl

# Fixed input makes the demonstration reproducible without keyboard input.
set secret 13
set guesses [list 3 19 8 16 11 13 17]
set attempts 0
set found 0

puts "============================================================"
puts "Guess the number (1-20)"
puts "Guesses: $guesses"
puts "------------------------------------------------------------"

# Count only guesses that are actually attempted.
foreach guess $guesses {
    incr attempts
    if {$guess < $secret} {
        puts "Attempt $attempts: $guess -> too low"
    } elseif {$guess > $secret} {
        puts "Attempt $attempts: $guess -> too high"
    } else {
        puts "Attempt $attempts: $guess -> correct"
        set found 1
        break
    }
}

# Report failure if the entire list was exhausted without a match.
if {!$found} {
    puts "Game over: no correct guess."
}
puts "Attempts used: $attempts"
puts "============================================================"
