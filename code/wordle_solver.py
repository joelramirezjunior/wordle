# wordle_solver.py

class WordleSolver:
    """
    A class to automatically solve Wordle puzzles.
    
    You will implement logic that, given the game's state, selects the next word to guess.
    This class is meant to interact with the WordleSimulator or directly with a Wordle instance.
    """

    def __init__(self, vocabulary):
        """
        Initializes the solver with a given list of valid words.
        
        Args:
            vocabulary (list): A list of valid words to choose from.
        """
        self.vocabulary = vocabulary.copy()  # Words still in play
        self.reset()

    def reset(self):
        """
        Resets the solver's state.
        Called at the beginning of each new Wordle game.
        """
        self.possible_words = self.vocabulary.copy()
        self.known_correct = {}     # {index: letter}
        self.known_present = set()  # letters in the word but wrong position
        self.known_absent = set()   # letters not in the word

    def next_guess(self):
        """
        Returns the next guess word based on current knowledge.
        
        Returns:
            str: A valid word guess.
        """
        # TODO: Implement your guessing strategy
        return self.possible_words[0]  # Default fallback

    def update(self, guess, feedback):
        """
        Updates internal knowledge based on the feedback from the last guess.
        
        Args:
            guess (str): The word that was guessed.
            feedback (list of str): A list with the same length as guess,
                where each element is one of:
                - "correct"  (letter is correct and in the correct position)
                - "present"  (letter is in the word but wrong position)
                - "absent"   (letter is not in the word)
        """
        # TODO: Use feedback to eliminate impossible words
        pass
