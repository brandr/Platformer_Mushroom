""" A manager for various game screens that the player might swich between.
"""

from maingamescreen import *
from pausescreen import *
from mapscreen import MapScreen
from mapcontrols import MapControls
from inventoryscreen import InventoryScreen
from inventorycontrols import InventoryControls

class ScreenManager:
	""" ScreenManager ( Surface, GameScreen, Player ) -> ScreenManager

	A manager object used to switch screens and controls during the game.

	Attributes:
	
	master_screen: the pygame screen (technically a Surface) that screen elements are drawn onto.

	current_screen: the current screen to be displayed. Only one may display at a time.

	player: the player associated with the current game session.
	"""

	def __init__(self, master_screen, current_screen, player = None):
		self.master_screen = master_screen
		self.set_current_screen(current_screen)
		self.player = player
		if(player != None):
			player.screen_manager = self

	def set_current_screen(self, screen):
		""" sm.set_current_screen( GameScreen ) -> None

		Store the given screen to the one that should be shown.
		"""
		self.current_screen = screen
		screen.screen_manager = self

	def process_event(self, event):
		""" sm.process_event( Event ) -> None

		Process a pygame event based on the current control scheme.
		"""
		self.current_screen.control_manager.process_event(event)

	def update_current_screen(self):
		""" sm.update_current_screen( ) -> None

		Tell the current screen to update its visual elements.
		"""
		self.current_screen.update()

	def draw_screen(self):
		""" sm.draw_screen( ) -> None

		The screen manager draws its screen image onto the screen that the player would see.
		"""
		self.current_screen.draw_screen(self.master_screen)

	def switch_to_inventory_screen(self, player):
		""" sm.switch_to_inventory_screen( Player ) -> None

		Switch to the screen that shows the player's inventory.
		"""
		controls = InventoryControls(player)
		control_manager = ControlManager(controls)
		inventory_screen = InventoryScreen(control_manager, player)
		self.set_current_screen(inventory_screen)

	def switch_to_main_screen(self, player):
		""" sm.switch_to_main_screen( Player ) -> None

		Switch to the main screen and controls used to play the game.
		"""
		game_controls = MainGameControls(player) 
		control_manager = ControlManager(game_controls)
		main_screen = MainGameScreen(control_manager, player) 
		self.set_current_screen(main_screen)
		level = player.current_level
		level.initialize_screen(self, main_screen)

	def switch_to_pause_screen(self, player):
		""" sm.switch_to_pause_screen( Player ) -> None

		Switch to the pause screen.
		"""
		controls = PauseControls(player)
		control_manager = ControlManager(controls)
		pause_screen = PauseScreen(control_manager, player)
		self.set_current_screen(pause_screen)

	def switch_to_map_screen(self, player):
		""" sm.switch_to_map_screen( Player ) -> None

		Switch to the map screen, which shows the map of the dungeon.
		"""
		controls = MapControls(player)	
		control_manager = ControlManager(controls)
		map_screen = MapScreen(control_manager, player)
		self.set_current_screen(map_screen)