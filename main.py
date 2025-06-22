import subprocess
from wordle import Wordle



def refresh_console():
    subprocess.run(["clear"])

def main():

    wordle = Wordle()
    wordle.start()

    while(wordle.guesses_left != 0 and not wordle.solved):

        x = input(wordle.state_string)

        if(not wordle.validate_guess(x)):
            print("INVALID")
            refresh_console()
            continue

        wordle.advance(x)
        refresh_console()
    
    print(wordle.state_string)
    wordle.end_game()

if __name__ == "__main__":
    main()
