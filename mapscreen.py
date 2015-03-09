""" the screen that appears when the player opens the map.
"""

from gamescreen import GameScreen
from mappane import MapPane
from dialog import WHITE
from pygame import font 

class MapScreen(GameScreen):
	""" MapScreen( ControlManager, Player) -> MapScreen

	Shows the map pane. Not sure if it should show any more than that yet.

	Attributes:

	player: The player whose location is shown on the map pane.

	map_pane: The set of panes shown onscreen while the game is paused.
	"""
	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager) 
		self.player = player
		self.map_pane = MapPane(player, 200, 120) #TODO: other panes

	def update(self):
		self.draw_bg()
		self.map_pane_update()

	def map_pane_update(self):
		self.map_pane.update()
		self.display_pane(self.map_pane)
		text_font = font.Font("./fonts/FreeSansBold.ttf", 20)
		dungeon_name = self.player.current_level.dungeon.dungeon_name
		text_image = text_font.render(dungeon_name, 1, WHITE)	# TODO: this might be a good place to put the name of the current dungeons
		self.screen_image.blit(text_image, (self.map_pane.x, self.map_pane.y - 40))

	def display_pane(self, pane):
		self.screen_image.blit(pane.pane_image, (pane.x, pane.y))