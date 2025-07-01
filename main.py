import sys
from wordle import Wordle

def play_game():
    """
    This function runs the game in interactive mode.

    It creates a Wordle object and enters a loop where the user provides guesses.
    The game gives feedback after each guess until the player either wins or 
    runs out of attempts.
    """

    # Initialize the Wordle game in debug mode to get internal prints/logs
    wordle = Wordle(debug=True)

    # Display the rules of Wordle to the player
    wordle.display_rules()

    # Main game loop: keep asking for input while the game is not over
    while wordle.not_done():
        # Prompt the user for their guess
        x = input("Enter your guess: ").strip()

        # If the guess is invalid (e.g. wrong length, not in dictionary),
        # skip processing and go to a new round
        if not wordle.validate_guess(x):
            wordle.newround()
            continue

        # If valid, advance the game logic with the given guess
        wordle.advance(x)

    # Once the game loop ends, print the end-game message or results
    wordle.end_game()


def simulate_game():
    """
    This function will eventually be responsible for running automated simulations.
    
    In simulation mode, an agent will be making guesses instead of a human.
    You'll plug in your Solver here once you build it.
    """
    pass  # TODO: Implement this after writing the Solver


def main():
    """
    Entry point for the program.

    Determines which mode to run the game in based on command-line flags:
    - If run in interactive mode (e.g., python3 -i), it plays in terminal.
    - Otherwise, it assumes simulation mode.
    """

    # If no command-line arguments are provided, print help text
    if len(sys.argv) == 1:
        print("Usage: python3 main.py -d [debug] -i [interactive]")

    # Print the flags to see how Python was invoked (for debugging purposes)
    print(sys.flags)

    # Check if Python is running in interactive mode (e.g., with the -i flag)
    if sys.flags.interactive:
        play_game()
    else:
        simulate_game()


# Python runs this block only if the file is executed directly,
# not if it's imported as a module
if __name__ == "__main__":
    main()
