from wordle import Wordle

class WordleSimulator:
    def __init__(self, wordle_instance=None, guesses=None):
        
        """
        wordle_instance: Optional custom Wordle instance to inject (default: new Wordle)
        guesses: Optional list of guesses to simulate (default: preset)
        """
        self.wordle = wordle_instance if wordle_instance and wordle_instance.simulated \
                                      else Wordle(simulated=True)
        self.result_log = []

    def input_guess(self, guess):
        
        if not self.wordle.validate_guess(guess):
            self.result_log.append((guess, "Invalid guess"))
            return False
            # throw INVALIDGUESS

        self.wordle.advance(guess)
    
    def was_solved(self):
        return self.wordle.solved
    
    def wordle_state(self):
        return self.wordle.character_set

