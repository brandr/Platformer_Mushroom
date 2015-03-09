"""This is currently the only class with a main method, so you can run the game from it.
currently the data for building the dungeon is read in from here, though that is likely to change as
the data gets more complicated."""

from gamemanager import *

def runGame():
    """
    runGame () -> None

    Run the game with the dungeon saved in file 'dungeon0'. 
    Later, we might run the game with arguments to choose
    a particular dungeon.

    """
    pygame.init()
    manager = GameManager()
    manager.run_game()

if __name__ == "__main__":
    runGame()