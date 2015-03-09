""" The controls used when the game is paused.
"""

from controls import *

class MapControls(Controls):
	""" MapControls( Player ) -> MapControls

	The map controls are currently limited to pressing enter or M to resume the game.

	Attributes:

	player: The Player to be shown on the map screen while the game is paused.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.initialize_control_map(PAUSE_CONTROL_MAP)
		self.player = player

	def unpause(self, key, toggle):
		""" mc.unpause( str, bool ) -> None

		When the player presses enter, resume the game.
		"""
		if toggle:
			self.player.unpause_game()

	def move_cursor(self, key, toggle):
		""" mc.move_cursor( str, bool ) -> None

		Move the pause cursor from its current position.
		"""
		if toggle: pass #TODO

unpause = MapControls.unpause
move_cursor = MapControls.move_cursor

PAUSE_CONTROL_MAP = {
	K_RETURN:unpause,
	K_m:unpause,
	K_LEFT:move_cursor,
	K_RIGHT:move_cursor
}