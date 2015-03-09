""" The controls used when the game is paused.
"""

from controls import *

class PauseControls(Controls):
	""" PauseControls( Player ) -> PauseControls

	The pause controls are currently limited to pressing enter to resume the game, but if menus are
	added to the pause screen then this will change.

	Attributes:

	player: The Player to be shown on the map screen while the game is paused.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.initialize_control_map(PAUSE_CONTROL_MAP)
		self.player = player

	def unpause(self, key, toggle):
		""" pc.unpause( str, bool ) -> None

		When the player presses enter, resume the game.
		"""
		if toggle:
			self.player.unpause_game()

	def move_cursor(self, key, toggle):
		""" pc.move_cursor( str, bool ) -> None

		Move the pause cursor from its current position.
		"""
		if toggle: pass #TODO

unpause = PauseControls.unpause
move_cursor = PauseControls.move_cursor

PAUSE_CONTROL_MAP = {
	K_RETURN:unpause,
	K_LEFT:move_cursor,
	K_RIGHT:move_cursor
}