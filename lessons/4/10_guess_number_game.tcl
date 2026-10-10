# 10_guess_number_game.tcl — Week 4 Day 5 project: guess-the-number (batch demo)
# Run: make week4-10
#      tclsh lessons/4/10_guess_number_game.tcl
#
# This version uses a list of guesses (no keyboard input) so it runs in batch.
# Change secret or guesses and run again.

set secret 7
set guesses [list 3 9 5 7]

puts "================================"
puts "   GUESS THE NUMBER (1-10)"
puts "================================"
puts "Secret number is hidden."
puts "Trying guesses: $guesses"
puts "--------------------------------"

set found 0
foreach guess $guesses {
    if {$guess == $secret} {
        puts "Guess $guess -> CORRECT! You found $secret."
        set found 1
        break
    } elseif {$guess < $secret} {
        puts "Guess $guess -> too low"
    } else {
        puts "Guess $guess -> too high"
    }
}

if {!$found} {
    puts "No correct guess in the list."
}

puts "================================"
