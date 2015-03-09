"""This is the screen used to play the game."""

#TODO: divide what is in this screen into gamescreen (abstract) and maingamescreen (specfic)

from controlmanager import *
from camera import WIN_WIDTH, WIN_HEIGHT
from pygame import Surface

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0

class GameScreen:
    """GameScreen ( ControlManager ) -> GameScreen

    This is the screen used to play the game.
    Later, it might be more useful to load the dungeon editor and the game from
    the same screen.

    Attributes:

    control_manager: An object which handles keyboard inputs.

    screen_image: The Surface to be displayed. Represents the entire screen.

    bg: A square background object to be repeatedly blitted over the screen (so that transparent objects will darken properly)
    """
    
    def __init__(self, control_manager): #not sure what other args should be yet.
        self.control_manager = control_manager
        control_manager.screen = self
        self.screen_image = Surface((WIN_WIDTH, WIN_HEIGHT))
        self.bg = Surface((32, 32))

    def update(self):
        return None #TEMP

    def master_screen(self):
        """ gs.master_screen( ) -> Surface

        Return the screen image associated with the current screen.
        """
        return self.screen_manager.master_screen

    def draw_screen(self, master_screen):
        """ gs.draw_screen( Surface ) -> None

        Update the pygame screen with the main screen.
        """
        master_screen.blit(self.screen_image, (0, 0))

    def draw_bg(self):
        """ gs.draw_bg( ) -> None

        blit the background across the screen, making it completely black.
        """
        for y in range(WIN_HEIGHT/32):  #TODO: make sure this process is correct and efficient.
                for x in range(WIN_WIDTH/32):
                    self.screen_image.blit(self.bg, (x * 32, y * 32))
