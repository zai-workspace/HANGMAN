import random

# Optional: Visual representation of the hangman
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

WORD_LIST = [
    'python', 'hangman', 'challenge', 'programming',
    'developer', 'openai', 'artificial', 'intelligence',
    'computer', 'science'
]

def get_random_word(word_list):
    return random.choice(word_list).upper()

def display_current_state(word, guessed_letters):
    display = ' '.join([letter if letter in guessed_letters else '_' for letter in word])
    print("\nWord: " + display)

def get_user_guess(guessed_letters):
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

def play_hangman():
    word = get_random_word(WORD_LIST)
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
    while True:
        play_hangman()
        replay = input("\nDo you want to play again? (Y/N): ").upper()
        if replay != 'Y':
            print("Thank you for playing Hangman! Goodbye!")
            break

if __name__ == "__main__":
    main()
