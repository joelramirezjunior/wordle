import sys
from wordle import Wordle


def play_game():

    wordle = Wordle(debug=True)
    wordle.display_rules()

    while(wordle.not_done()):
        
        x = input()
        
        if(not wordle.validate_guess(x)):
            wordle.newround()
            continue

        wordle.advance(x)

    wordle.end_game()


def simulate_game():   
    pass

def main():
    if len(sys.argv) == 1:
        print("Usage: python3 main.py -d [debug] -i [interractive]")
    print(sys.flags)
    if sys.flags.interactive:
        play_game()
    else:
        simulate_game()    
if __name__ == "__main__":
    main()
