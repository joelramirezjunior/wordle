from wordle import Wordle
import time

# Attempt to import a WordleSolver if provided by the student
try:
    from wordle_solver import WordleSolver
except ImportError:
    WordleSolver = None


class WordleSimulator:
    def __init__(self, wordle_instance=None, solver_instance=None, verbose=False):
        """
        Initializes the simulator with an optional Wordle game and solver.

        Parameters:
            wordle_instance (Wordle): An optional custom Wordle instance.
            solver_instance (WordleSolver): An optional solver object.
            verbose (bool): Whether to print each step of the simulation.
        """
        self.wordle = wordle_instance if wordle_instance else Wordle(simulated=True)
        self.solver = solver_instance if solver_instance else (WordleSolver() if WordleSolver else None)
        self.verbose = verbose
        self.result_log = []

    def simulate_game(self):
        """
        Simulates a full Wordle game using the solver. Returns a dictionary with results.

        Returns:
            dict: Contains result of the game including win status, guesses, and stats.
        """
        if not self.solver:
            raise Exception("No solver provided or found. Cannot simulate game.")

        start_time = time.time()
        guesses = []

        while self.wordle.not_done():
            guess = self.solver.make_guess(self.wordle.character_set)

            if not self.wordle.validate_guess(guess):
                self.result_log.append((guess, "Invalid"))
                break

            self.wordle.advance(guess)
            guesses.append(guess)

            if self.verbose:
                print(f"Guess: {guess}")

        end_time = time.time()

        return {
            "solved": self.wordle.solved,
            "num_guesses": len(guesses),
            "guesses": guesses,
            "answer": self.wordle.word,
            "time": round(end_time - start_time, 4)
        }
    
    def run_multiple(self, num_trials):
        """
        Runs multiple simulations to gather performance stats.

        Parameters:
            num_trials (int): Number of games to simulate.

        Returns:
            list: A list of result dictionaries from simulate_game().
        """
        results = []
        for _ in range(num_trials):
            sim = WordleSimulator(solver_instance=self.solver)
            result = sim.simulate_game()
            results.append(result)
        return results
