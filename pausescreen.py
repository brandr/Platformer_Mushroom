""" the screen that appears when the player pauses the game.
"""

from gamescreen import GameScreen
from mappane import MapPane
from dialog import WHITE, BLACK
from pygame import Surface, font 

PAUSE_PANE_WIDTH, PAUSE_PANE_HEIGHT = 400, 300
PAUSE_PANE_X, PAUSE_PANE_Y = 200, 170

class PauseScreen(GameScreen):
	""" PauseScreen( ControlManager, Player) -> PauseScreen

	Currently, the pause screen only shows the map pane. If there are multiple screens then this class
	will need to be restructured.

	Attributes:

	player: The player whose location is shown on the map pane.

	level_image: A Surface representing the level the player was on the moment it was paused.

	pause_pane: A rectangular pane showing pause options.
	"""
	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager) 
		self.player = player
		self.level_image = self.player.current_level.screen
		self.pause_pane = self.draw_pause_pane()

	def update(self):

		self.draw_bg()
		self.screen_image.blit(self.level_image, (0, 0))
		self.screen_image.blit(self.pause_pane, (PAUSE_PANE_X, PAUSE_PANE_Y))

	def draw_pause_pane(self):
		""" ps.draw_pause_pane( ) -> Surface

		Draw an image representing the pane that shows the options available while paused.
		"""
		pane = Surface((PAUSE_PANE_WIDTH, PAUSE_PANE_HEIGHT))
		pane.fill(WHITE)
		text_font = font.Font("./fonts/FreeSansBold.ttf", 28)
		text_image = text_font.render("GAME PAUSED", 1, BLACK)
		pane.blit(text_image, ( 100, 20 ))
		#...
		return pane
