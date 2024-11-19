import random
import os

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


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.total_games = 0
        self.wins = 0
        self.hints_used = 0

    def add_score(self, points):
        self.score += points
        
    def record_game(self, won):
        self.total_games += 1
        if won:
            self.wins += 1
            
    def use_hint(self):
        self.hints_used += 1
        self.score = max(0, self.score - 5)

class HangmanGame:
    def __init__(self, word_list_path='word_list.txt'):
        self.word_list = self.load_words_from_file(word_list_path)
        self.max_incorrect = len(HANGMAN_PICS) - 1
        self.players = {}
        self.points_per_correct = 10
        self.reset_game()

    def load_words_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                words = file.read().splitlines()
            return [word.upper() for word in words if word.isalpha() and word.islower()]
        except FileNotFoundError:
            print(f"Word list file not found at '{file_path}'.")
            return []

    def reset_game(self):
        self.word = random.choice(self.word_list) if self.word_list else ""
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.hint_given = False

    def get_hint(self):
        unguessed_letters = [letter for letter in self.word if letter not in self.guessed_letters]
        if unguessed_letters:
            hint_letter = random.choice(unguessed_letters)
            positions = [i for i, letter in enumerate(self.word) if letter == hint_letter]
            return f"The letter '{hint_letter}' appears at position(s): {[pos + 1 for pos in positions]}"
        return "No more hints available."

    def offer_hint(self, current_player):
        if self.incorrect_guesses >= self.max_incorrect - 1 or self.incorrect_guesses >= 2:
            if not self.hint_given and input("Would you like a hint? (Y/N): ").upper() == 'Y':
                hint = self.get_hint()
                print(f"\nHint: {hint}")
                self.hint_given = True
                current_player.use_hint()
                print(f"5 points deducted for using a hint. Current score: {current_player.score}")
                return True
        return False

    def display_highscores(self):
        print("\n=== HIGHSCORES ===")
        sorted_players = sorted(self.players.values(), 
                              key=lambda x: (x.score, x.wins/max(1, x.total_games)), 
                              reverse=True)
        for i, player in enumerate(sorted_players, 1):
            win_rate = (player.wins / max(1, player.total_games)) * 100
            print(f"{i}. {player.name}: {player.score} points (Games: {player.total_games}, "
                  f"Wins: {player.wins}, Win Rate: {win_rate:.1f}%, Hints: {player.hints_used})")

    def display_game_state(self):
        print("\n" + HANGMAN_PICS[self.incorrect_guesses])
        display = ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])
        print("\nWord:", display)
        print(f"Incorrect guesses remaining: {self.max_incorrect - self.incorrect_guesses}")


    def get_valid_guess(self, current_player):
        while True:
            guess = input(f"{current_player.name}, enter a letter: ").upper()
            if len(guess) != 1:
                print("Please enter a single letter.")
            elif not guess.isalpha():
                print("Please enter a valid alphabet letter.")
            elif guess in self.guessed_letters:
                print("This letter has already been guessed. Try another one.")
            else:
                return guess


    def play_round(self, current_player):
        if not self.word_list:
            print("No words available to play.")
            return False

        print(f"\n{current_player.name}'s turn!")
        self.display_game_state()

        while self.incorrect_guesses < self.max_incorrect:
            self.display_highscores()
            self.offer_hint(current_player)
            
            guess = self.get_valid_guess(current_player)
            self.guessed_letters.add(guess)

            if guess in self.word:
                points = self.points_per_correct * self.word.count(guess)
                current_player.add_score(points)
                print(f"Correct! +{points} points!")
            else:
                self.incorrect_guesses += 1
                print("Incorrect guess!")

            self.display_game_state()

            if all(letter in self.guessed_letters for letter in self.word):
                print(f"\nCongratulations {current_player.name}! You've won!")
                current_player.record_game(True)
                return True

        print(f"\nGame Over! The word was: {self.word}")
        current_player.record_game(False)
        return False


def main():
    default_path = 'word_list.txt'
    use_default = input(f"Use default word list ('{default_path}')? (Y/N): ").upper() == 'Y'
    file_path = default_path if use_default else input("Enter word list file path: ")
    
    game = HangmanGame(file_path)
    
    while True:
        player_name = input("\nEnter player name (or 'quit' to exit): ").strip()
        if player_name.lower() == 'quit':
            break
            
        if player_name not in game.players:
            game.players[player_name] = Player(player_name)
        
        game.play_round(game.players[player_name])
        game.reset_game()
        
        game.display_highscores()
    
    print("\nFinal Scores:")
    game.display_highscores()
    print("Thanks for playing!")

if __name__ == "__main__":
    main()