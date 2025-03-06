secret_word = "pass"
guess = "  "
guess_number = 0
guess_limit = 3
out_of_guesses = False

while guess != secret_word and not (out_of_guessing):
    if guess_number < guess_limit:
        guess = input(" Enter your guess: ")
        guess_number += 1
    else:
        out_of_guesses = True
        
if out_of_guesses:
    print("Lost!")
else:
    print("Word founded!")

