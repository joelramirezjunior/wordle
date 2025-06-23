from collections import Counter
import subprocess

vocabulary_file = "vocabulary.txt"
rule_file = "rules.txt"

# Background colors using octal ANSI escape codes
BG_GREEN = "\033[42m"
BG_RED = "\033[41m"
BG_YELLOW = "\033[43m"
RESET = "\033[0m"

# Rule file placeholders
correctspot = "%GREEN%"
wrongspot = "%YELLOW%"
notpresent = "%RED%"
reset = "%RESET%"

def choose_random_word():
    return "AXIOM"

def generate_vocabulary():
    with open(vocabulary_file, "r") as f:
        return [line.strip().upper() for line in f]

class Wordle:
    def __init__(self, simulated=False, debug=False):
        self.simulated = simulated
        self.word = choose_random_word()
        self.debug = debug
        self.guesses_left = 6
        self.vocabulary = generate_vocabulary()
        self.character_set = [dict(), set(), set()]  # correct_pos, present_wrong_pos, not_present
        self.state_string = ""
        self.count = Counter()
        self.solved = False
        self._log("Intialized Game:\n", self)
    
    def __str__(self):
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
        Internal method for conditional printing 
        when in interactive mode.
        """
        if not self.simulated:
            print(*args, **kwargs)
    
    def _log(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def newround(self):
        if not self.simulated and not self.debug:
            # it would make sense not to completely clear the screen if you are trying to debug.
            subprocess.run(["clear"])
        self._print(self.state_string) 
    
    def display_rules(self):
        """
        Doesn't do anything if it is simulated. I'll blame the user for 
        writing a program that uses this and wastes time opening the file. 
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
        if not guess.isalpha():
            self._log("NOT ALPHA")
            return False

        return guess.upper() in self.vocabulary

    def advance(self, guess):
        """
        This function returns two variables. One indicated if the game has been solved. 
        The other is the string that is printed to indicate the state of the guess. 
        """
        guess = guess.upper()
        self.guesses_left -= 1
        self.build_output_string(guess)

        self.newround()
        self._log("adanced():\n", self)

    def not_done(self):
        return self.guesses_left != 0 and not self.solved
    
    def end_game(self):
        if self.solved:
            self._print("You won! Congrats!")
        else:
            self._print("You lost. Better luck next time.")
        self._log("endgame():\n", self)

    def build_output_string(self, guess):
        
        output = []
        self.count.clear()
        self.count.update(guess)

        self._log("build_output_string(): PRIOR\n", self)

        for i, char in enumerate(guess):
            if char == self.word[i]:
                self.character_set[0][char] = i
                self.character_set[1].discard(char)
                output.append(f"[{BG_GREEN} {char} {RESET}]")
                self.count[char] -= 1
            elif char in self.word and self.count[char] > 0:
                self.character_set[1].add(char)
                output.append(f"[{BG_YELLOW} {char} {RESET}]")
            else:
                self.character_set[2].add(char)
                output.append(f"[{BG_RED} {char} {RESET}]")

        output_line = " ".join(output) + "\n"
        
        self.state_string += output_line
        self.solved |= guess == self.word

        self._log("build_output_string(): POST\n")
        self._log("Here is the output string:", output_line)
        self._log("Current guess state:", self.character_set)

