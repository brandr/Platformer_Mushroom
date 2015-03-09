""" Handles the controls used when the player is in the main game.
"""

from controls import *

LEFT, RIGHT, DOWN, UP, SPACE, CONTROL, X = "left", "right", "down", "up", "space", "control", "x"

class MainGameControls(Controls):
	""" MainGameControls( Player ) -> MainGameControls

	Can handle various contexts, but they should all be associated with
	the main game.

	Attributes:

	player: the player associated with these controls. 

	direction_map: the buttons used in the main game (as strings) mapped to the actions they cause.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.player = player
		self.initialize_control_map(MAIN_GAME_CONTROL_MAP)

	def move_up(self, key, toggle):
		""" mgc.move_up( str, bool ) -> None

		Up key action.
		"""
		self.player.button_press_map[UP] = toggle

	def move_down(self, key, toggle):
		""" mgc.move_down( str, bool ) -> None

		Down key action.
		"""
		self.player.button_press_map[DOWN] = toggle

	def move_left(self, key, toggle):
		""" mgc.move_left( str, bool ) -> None

		Left key action.
		"""
		self.player.button_press_map[LEFT] = toggle

	def move_right(self, key, toggle):
		""" mgc.move_right( str, bool ) -> None

		Right key action.
		"""
		self.player.button_press_map[RIGHT] = toggle

	def move_space(self, key, toggle):
		""" mgc.move_space( str, bool ) -> None

		Space key action.
		"""
		self.player.button_press_map[SPACE] = toggle

	def move_control(self, key, toggle):
		""" mgc.move_control( str, bool ) -> None

		Control key action.
		"""
		self.player.button_press_map[CONTROL] = toggle

	def press_c(self, key, toggle):
		""" mgc.press_c( str, bool ) -> None

		c key action.
		"""
		if toggle:
			self.player.activate_lantern_ability()

	def press_i(self, key, toggle):
		""" mgc.press_i( str, bool ) -> None

		i key action.
		"""
		if toggle:
			self.player.open_inventory()

	def press_m(self, key, toggle):
		""" mgc.press_m( str, bool ) -> None

		m key action.
		"""
		if toggle:
			self.player.open_map()

	def press_q(self, key, toggle):
		""" mgc.press_q( str, bool ) -> None

		q key action.
		"""
		if toggle:
			self.player.toggle_lantern_mode(-1)

	def press_w(self, key, toggle):
		""" mgc.press_w( str, bool ) -> None

		w key action.
		"""
		if toggle:
			self.player.toggle_lantern_mode(1)

	def press_x(self, key, toggle):
		""" mgc.press_x( str, bool ) -> None

		x key action.
		"""
		self.player.button_press_map[X] = toggle
		
	def press_z(self, key, toggle):
		""" mgc.press_z( str, bool ) -> None

		z key action.
		"""
		if toggle:
			self.player.temp_z_method()	#consider making this work like every other button, or making the x key work like this.

	def press_return(self, key, toggle):
		""" mgc.press_return( str, bool ) -> None

		Tell the player to pause the game.
		"""
		if(toggle):
			self.player.pause_game()

move_up = MainGameControls.move_up
move_down = MainGameControls.move_down
move_left = MainGameControls.move_left
move_right = MainGameControls.move_right

move_space = MainGameControls.move_space
move_control = MainGameControls.move_control

press_c = MainGameControls.press_c
press_i = MainGameControls.press_i
press_m = MainGameControls.press_m
press_q = MainGameControls.press_q
press_w = MainGameControls.press_w
press_x = MainGameControls.press_x
press_z = MainGameControls.press_z

press_return = MainGameControls.press_return

MAIN_GAME_CONTROL_MAP = { 
	K_UP:move_up, K_DOWN:move_down, K_LEFT: move_left, K_RIGHT:move_right,
	K_SPACE:move_space, K_LSHIFT:move_control,
	K_c:press_c,
	K_i:press_i,
	K_m:press_m,
	K_q:press_q,
	K_w:press_w,
	K_x:press_x,
	K_z:press_z,
	K_RETURN:press_return
}