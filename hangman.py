from random_word import RandomWords
import zufallsworte as zufall

PUNISH_WORD = 2                         # The number of guesses lost on wrong full word guess
PUNISH_CHAR = 1                         # THe number of guesses lost on wrong letter
GUESS_COUNT = 10                        # The number of guesses the player has in total
PLACEHOLDER = '_'                       # The Placeholder showing not guessed characters
LANGUAGES = ["german", "english"]       # The Languages available TODO currently unused
ENGLISH_SELECTOR = 'e'                  # Showing that english is selected as language
GERMAN_SELECTOR = 'g'                   # Showing that german is selected as language
GENERATOR = RandomWords()               # generator for english words


# TODO bei 2 eigenen wörtern (ein begriff) kann mann nicht vollständig eingeben

def print_array(array):
    for char in array:
        print(char, end=" ")
    print()


def ask_for_language():
    choice = input(f"What language should the hidden word be from? (GERMAN [{GERMAN_SELECTOR.upper()}] / english [{ENGLISH_SELECTOR}])")
    if not choice or choice.lower() == "german" or choice.lower() == GERMAN_SELECTOR:
        return 'g'
    elif choice.lower() == ENGLISH_SELECTOR or choice.lower() == "english":
        return 'e'
    else:
        return None
    

def enter_own_word():
    word = input(f"Enter a word (blank for random word): ")
    print(f"\033[A\rEnter a word (blank for random word): {' ' * len(word)}")   # Remove input from console
    return word

def main_game():
    # one iteration = one round
    while True:
        print("Starting a new round of Hangman...")
        custom_word = ''
        custom_word = enter_own_word()
        if not custom_word:
            language = ask_for_language()
            if language == ENGLISH_SELECTOR:
                hidden_word = GENERATOR.get_random_word()
            elif language == GERMAN_SELECTOR:
                hidden_word = zufall.zufallswoerter(1)[0]
            else:
                print("Invalid language selected. Terminating ...")
                break
        else:
            hidden_word = custom_word

        # print(hidden_word)
        hidden_word_list = list(hidden_word.lower())
        guess_list = [PLACEHOLDER for elem in range(len(hidden_word))]
        # filter spaces out of guess list
        for i in range(len(guess_list)):
            if hidden_word_list[i] == ' ':
                guess_list[i] = ' '
        already_guessed_list = []

        print_array(guess_list)

        lives = GUESS_COUNT
        # one iteration = one guess
        while True:
            guess = input("Enter a guess: ").lower()

            # Check if word guess is correct
            if guess == hidden_word.lower():
                print("Correct! The Word was " + hidden_word + ".")
                break
            elif len(guess) > 1:
                lives -= PUNISH_WORD
                print("Unfortunatly thats not the hidden word. -" + str(PUNISH_WORD) + " guesses. Remaining guesses: " + str(lives))
                print_array(guess_list)


            # check if char guess is correct
            if guess != '' and guess not in already_guessed_list and guess.lower() in hidden_word_list:
                print("Correct!")
                for i in range(len(hidden_word_list)):
                    if hidden_word_list[i] == guess:
                        guess_list[i] = hidden_word[i]
                print_array(guess_list)
            elif len(guess) == 1:
                lives -= PUNISH_CHAR
                if guess in already_guessed_list:
                    print("You already guessed that letter! -" + str(PUNISH_CHAR) + " guesses. Remaining guesses: " + str(lives))
                else:
                    print("The word doesn't contain that letter. -" + str(PUNISH_CHAR) + " guesses. Remaining guesses: " + str(lives))
                print_array(guess_list)

            already_guessed_list.append(guess)

            if PLACEHOLDER not in guess_list:
                print("You guessed the Word! It was '" + hidden_word + "'.")
                break

            if lives <= 0:
                print("You couldn't guess the Word in time! It was '" + hidden_word + "'.")
                break


        want_play_again = input("Do you want to play again? (Y/n) ")
        if want_play_again and want_play_again.lower() != "y":
            print("Ending the game...")
            break


if __name__ == "__main__":
    main_game()