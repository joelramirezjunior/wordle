from collections import Counter, defaultdict

vocabulary_file = "vocabulary.txt"

# Background colors using octal ANSI escape codes
BG_GREEN = "\033[42m"
BG_RED = "\033[41m"
BG_YELLOW = "\033[43m"

# Reset formatting
RESET = "\033[0m"

correctspot = "%GREEN%"
wrongspot = "%YELLOW%"
notpresent = "%RED%"
reset = "%RESET%"

rule_file = "rules.txt"


def choose_random_word():
    return "AXIOM"

def generate_vocabulary():
    with open(vocabulary_file, "r") as f:
        all_words = f.readlines()
        all_words = map(lambda val: val[:-1], all_words) #remove the newline
        all_words = map(lambda val: val.upper(), all_words) #convert to uppercase
        return list(all_words)

class Wordle:

    def __init__(self):
        self.word = choose_random_word()
        self.guesses_left = 6
        self.vocabulary = generate_vocabulary()
        self.character_set = [dict(), set(), set()]
        # [0] -> maps characters found in the correct place to their index
        # [1] -> set of characters that are in the word but placement is unknown
        # [2] -> set of characters that are not present
        self.state_string = ""
        self.count = Counter()
        self.solved = False

    def start(self):
        with open(rule_file, "r") as file:
            lines = file.readlines()
            lines = "".join(lines)

            lines = lines.replace(correctspot, BG_GREEN)
            lines = lines.replace(wrongspot, BG_YELLOW)
            lines = lines.replace(notpresent, BG_RED)
            lines = lines.replace(reset, RESET)
            print(lines)

    def validate_guess(self, guess):
        if not guess.isalpha():
            print("NOT ALPHA")
            return False
        return guess.upper() in self.vocabulary


    def advance(self, guess):
        self.guesses_left -= 1
        guess = guess.upper()
        solved, state_string = self.build_output_string(guess)
        if(solved): self.solved = True
        self.state_string += state_string
        return solved, self.state_string

    def end_game(self):
        if self.solved:
            print("You won! Congrats!")
        else:
            print("You lost. Better luck next time.")

    def build_output_string(self, guess):
        string = ""
        guess = guess.upper()
        self.count.clear()
        self.count.update(guess)

        for i, char in enumerate(guess):
            if char  == self.word[i]:
                if char not in self.character_set[0]:
                    self.character_set[0][char] = i

                if char in self.character_set[1]:
                    self.character_set[1].remove(char)

                string += f"[ {BG_GREEN}{char}{RESET} ]"
                self.count[char] -= 1

            elif char  in self.word and self.count[char] != 0:
                self.character_set[1].add(char)
                string += f"[ {BG_YELLOW}{char}{RESET} ]"

            else:
                self.character_set[2].add(char)
                string += f"[ {BG_RED}{char}{RESET} ]"

        string += "\n"

        print(f"Here is the output string: {string}")
        print("Here is the state of your guesses", self.character_set)
        return guess == self.word, string



