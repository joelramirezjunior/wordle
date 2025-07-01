from collections import Counter
import subprocess

# Files used for vocabulary and rules display
vocabulary_file = "vocabulary.txt"
rule_file = "rules.txt"

# ANSI escape codes for background colors (used in terminal)
BG_GREEN = "\033[42m"   # Correct letter in correct spot
BG_RED = "\033[41m"     # Incorrect letter
BG_YELLOW = "\033[43m"  # Correct letter, wrong spot
RESET = "\033[0m"       # Reset formatting

# Placeholders in rules file that get replaced with colors
correctspot = "%GREEN%"
wrongspot = "%YELLOW%"
notpresent = "%RED%"
reset = "%RESET%"

def choose_random_word():
    """
    Returns the target word to guess in the game.
    This can later be randomized; currently returns a fixed word.
    """
    return "AXIOM"

def generate_vocabulary():
    """
    Loads the vocabulary of valid guess words from file.
    Converts all entries to uppercase and strips whitespace.
    """
    with open(vocabulary_file, "r") as f:
        return [line.strip().upper() for line in f]

class Wordle:
    """
    A class representing a Wordle game instance.

    Handles all logic for tracking the game state, validating guesses,
    updating color-coded feedback, and handling end-of-game conditions.
    """

    def __init__(self, simulated=False, debug=False):
        """
        Initializes the Wordle game.

        Args:
            simulated (bool): Whether this game is running in simulation mode.
            debug (bool): Whether to enable verbose logging.
        """
        self.simulated = simulated
        self.word = choose_random_word()
        self.debug = debug
        self.guesses_left = 6
        self.vocabulary = generate_vocabulary()
        
        # Stores game state about letter positions:
        # [0] = correct position (dict), [1] = wrong position (set), [2] = not present (set)
        self.character_set = [dict(), set(), set()]
        
        self.state_string = ""  # Output string shown after each guess
        self.count = Counter()  # Tracks character frequency in guesses
        self.solved = False     # Whether the correct word has been guessed

        self._log("Initialized Game:\n", self)
    
    def __str__(self):
        """
        Returns a string representation of the current game state for debugging.
        """
        return (\
            f"WordGuessGame(simulated={self.simulated},\n" \
            f"  word='{self.word}',\n"\
            f"  guesses_left={self.guesses_left},\n"\
            f"  vocabulary_size={len(self.vocabulary)},\n"\
            f"  character_set={{\n"\
            f"    correct_pos={self.character_set[0]},\n"\
            f"    present_wrong_pos={self.character_set[1]},\n"\
            f"    not_present={self.character_set[2]}\n"\
            f"  }},\n"\
            f"  state_string='{self.state_string}',\n"\
            f"  count={dict(self.count)},\n"\
            f"  solved={self.solved})")

    def _print(self, *args, **kwargs):
        """
        Helper method to print only if not in simulation mode.
        """
        if not self.simulated:
            print(*args, **kwargs)
    
    def _log(self, *args, **kwargs):
        """
        Helper method to print debug messages when debugging is enabled.
        """
        if self.debug:
            print(*args, **kwargs)

    def newround(self):
        """
        Clears the terminal and reprints the current state of guesses.
        This is skipped during simulations or debugging.
        """
        if not self.simulated and not self.debug:
            subprocess.run(["clear"])
        self._print(self.state_string) 

    def display_rules(self):
        """
        Displays the game rules using color-coded formatting.
        This is skipped during simulations. 
        """
        try:
            with open(rule_file, "r") as file:
                rules = file.read()
                rules = rules.replace(correctspot, BG_GREEN)\
                             .replace(wrongspot, BG_YELLOW)\
                             .replace(notpresent, BG_RED)\
                             .replace(reset, RESET)
                self._print(rules)
        except FileNotFoundError:
            self._log("Rules file not found.")

    def validate_guess(self, guess):
        """
        Checks if a guess is valid (alphabetic and present in the vocabulary).

        Args:
            guess (str): The guessed word.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not guess.isalpha():
            self._log("NOT ALPHA")
            return False
        return guess.upper() in self.vocabulary

    def advance(self, guess):
        """
        Processes a valid guess, updates the game state, and checks win condition.

        Args:
            guess (str): The guessed word (already validated).
        """
        guess = guess.upper()
        self.guesses_left -= 1
        self.build_output_string(guess)
        self.newround()
        self._log("advance():\n", self)

    def not_done(self):
        """
        Returns True if the game is not yet finished (still guesses left and not solved).
        """
        return self.guesses_left != 0 and not self.solved
    
    def end_game(self):
        """
        Prints final result based on whether the player won or lost.
        Also logs final game state.
        """
        if self.solved:
            self._print("You won! Congrats!")
        else:
            self._print("You lost. Better luck next time.")
        self._log("end_game():\n", self)

    def build_output_string(self, guess):
        """
        Compares the guess with the target word and builds a color-coded feedback line.

        Updates:
        - Correct positions (green)
        - Present but misplaced letters (yellow)
        - Absent letters (red)
        """
        output = []
        self.count.clear()
        self.count.update(guess)

        self._log("build_output_string(): PRIOR\n", self)

        for i, char in enumerate(guess):
            if char == self.word[i]:
                # Correct letter, correct position
                self.character_set[0][char] = i
                self.character_set[1].discard(char)
                output.append(f"[{BG_GREEN} {char} {RESET}]")
                self.count[char] -= 1
            elif char in self.word and self.count[char] > 0:
                # Correct letter, wrong position
                self.character_set[1].add(char)
                output.append(f"[{BG_YELLOW} {char} {RESET}]")
            else:
                # Letter not in the word at all
                self.character_set[2].add(char)
                output.append(f"[{BG_RED} {char} {RESET}]")

        # Build the full string from the colored letters
        output_line = " ".join(output) + "\n"
        self.state_string += output_line

        # Check if the guess is the correct word
        self.solved |= guess == self.word

        self._log("build_output_string(): POST\n")
        self._log("Here is the output string:", output_line)
        self._log("Current guess state:", self.character_set)
