from game.words import random_word
from game.engine import GameState
from game.ui_cli import loop

def main():
    secret = random_word()
    state = GameState(secret=secret, attempts=6)
    loop(state)

if __name__ == "__main__":
    main()
