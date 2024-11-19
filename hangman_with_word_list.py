import random
import os

# Visual representation of the hangman
HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\\  |
      |
     ===''', '''
  +---+
  O   |
 /|\\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\\  |
 / \\  |
     ===''']

def load_words_from_file(file_path='word_list.txt'):
    """
    Load words from a given file and return a list of uppercase words.
    Only includes words that are purely alphabetical and in lowercase.
    """
    try:
        with open(file_path, 'r') as file:
            words = file.read().splitlines()
        # Filter words: remove proper nouns and non-alphabetic words
        words = [word.upper() for word in words if word.isalpha() and word.islower()]
        return words
    except FileNotFoundError:
        print(f"Word list file not found at '{file_path}'. Please ensure the file exists.")
        return []


def get_random_word(word_list):
    """Select and return a random word from the word list."""
    return random.choice(word_list).upper()


def display_current_state(word, guessed_letters):
    """
    Display the current state of the word with guessed letters revealed
    and remaining letters as underscores.
    """
    display = ' '.join([letter if letter in guessed_letters else '_' for letter in word])
    print("\nWord: " + display)


def get_user_guess(guessed_letters):
    """
    Prompt the user to enter a guess and validate the input.
    Returns a valid uppercase single letter.
    """
    while True:
        guess = input("Enter a letter: ").upper()
        if len(guess) != 1:
            print("Please enter a single letter.")
        elif not guess.isalpha():
            print("Please enter a valid alphabet letter.")
        elif guess in guessed_letters:
            print("You have already guessed that letter. Try another one.")
        else:
            return guess


def play_hangman(word_list):
    """
    Core function to play a single game of Hangman.
    """
    word = get_random_word(word_list)
    guessed_letters = set()
    incorrect_guesses = 0
    max_incorrect = len(HANGMAN_PICS) - 1

    print("\nWelcome to Hangman!")
    print(HANGMAN_PICS[incorrect_guesses])
    display_current_state(word, guessed_letters)

    while incorrect_guesses < max_incorrect:
        guess = get_user_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in word:
            print(f"Good job! '{guess}' is in the word.")
        else:
            incorrect_guesses += 1
            print(f"Sorry, '{guess}' is not in the word.")

        print(HANGMAN_PICS[incorrect_guesses])
        display_current_state(word, guessed_letters)

        # Check if all letters have been guessed
        if all(letter in guessed_letters for letter in word):
            print("\nCongratulations! You've guessed the word correctly and won the game!")
            break
    else:
        print("\nYou've been hanged! The word was:", word)

def main():
    """
    Main function to manage game sessions and replay options.
    """
    default_path = 'word_list.txt'
    use_default = input(f"Do you want to use the default word list ('{default_path}')? (Y/N): ").upper()
    if use_default == 'Y':
        word_list = load_words_from_file(default_path)
    else:
        custom_path = input("Enter the path to your word list file: ")
        word_list = load_words_from_file(custom_path)

    if not word_list:
        print("No words available to play. Exiting the game.")
        return

    while True:
        play_hangman(word_list)
        replay = input("\nDo you want to play again? (Y/N): ").upper()
        if replay != 'Y':
            print("Thank you for playing Hangman! Goodbye!")
            break

if __name__ == "__main__":
    main()
