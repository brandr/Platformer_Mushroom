""" A visual effect that appears in the game, like a dialog box or black cutscene bars.
"""

#from pygame import Surface, Rect
from tile import *

class Effect:
	""" Effect( method, ( int, int ), ( int, int ), bool ) -> Effect

	The effect belongs to the level it appears on and updates until it receives some
	signal telling it to disappear.

	Attributes:

	draw_function: The method used to draw the effect onscreen.

	end_function: The method called when the effect is ending.

	draw_dimensions: The width and height of the effect.

	offset: The x, y coordinates of the upper-left of the Effect on screen.

	animated: Whether or not the effect will change over time.

	animated_end: If true, the effect has some animation as it is ending.
	Otherwise, it will end instantly when it gets the signal.

	ending: Becomes true when the animation starts ending.

	index: Tracks how far the effect's animation has advanced.
	"""

	def __init__(self, draw_function, draw_dimensions = (0, 0), offset = (0, 0), animated = False): #TODO: provide method or information needed to create the Surface we want, since we don't want to save a Surface every time we make an Effect.
		self.draw_function = draw_function
		self.end_function = None
		self.draw_dimensions = draw_dimensions
		self.offset = offset
		self.animated = animated
		self.animated_end = animated
		self.ending = False
		self.index = 0
		self.init_end_function()

	def init_end_function(self):
		""" e.init_end_function( ) -> None

		Sets this effect's end function based on its draw function, if there is a corresponding one.
		"""
		if self.draw_function in END_FUNCTION_MAP:
			self.end_function = END_FUNCTION_MAP[self.draw_function]
			return
		self.end_function = Effect.instant_close

	def instant_close(self, level, clear_all = False):
		""" e.instant_close( Level, Bool ) -> Surface

		Removes this effect from the level instantly, along with all other effects if clear_all is True.
		"""
		level.remove_effect(self)
		level.clear_effects()
		return Surface((0, 0)), (0, 0)

	def draw_black_rectangle_top(self, dimensions, time = None): #currently used specifically for cutscenes
		""" e.draw_black_rectangle_top( ( int, int ), int ) -> Surface

		Draw the top black rectangle effect that appears during cutscenes.
		"""
		if time != None:
			if time*4 >= dimensions[1]:
				self.animated = False
				return Surface(dimensions), (0, 0)
			width, height = dimensions[0], time*4
			return Surface((width, height)), (0, 0)
		return Surface(dimensions), (0, 0)

	def draw_black_rectangle_bottom(self, dimensions, time = None):
		""" e.draw_black_rectangle_bottom( ( int, int ), int ) -> Surface

		Draw the bottom black rectangle effect that appears during cutscenes.
		"""
		if time != None:
			if time*4 >= dimensions[1]:
				self.animated = False
				return Surface(dimensions), (0, 0)
			width, height = dimensions[0], time*4
			offset_y = dimensions[1] - time*4
			return Surface((width, height)), (0, offset_y)
		return Surface(dimensions), (0, 0)

	def remove_black_rectangle_top(self, level): #currently used specifically for cutscenes
		if self.animated_end:
			time = self.index
			dimensions = self.draw_dimensions
			width, height = dimensions[0], time*4
			return Surface((width, height)), (0, 0)
		return self.instant_close(level)

	def remove_black_rectangle_bottom(self, level):
		if self.animated_end:
			time = self.index
			dimensions = self.draw_dimensions
			width, height = dimensions[0], time*4
			offset_y = max(0, dimensions[1] - time*4)
			return Surface((width, height)), (0, offset_y)
		return self.instant_close(level, True)

	def draw_image(self, level = None):
		if self.ending:
			self.index -= 1
			if self.index <= 0:
				return self.instant_close(level)
			return self.end_function(self, level) 
		if self.animated:
			self.index += 1
			return self.draw_function(self, self.draw_dimensions, self.index)
		return self.draw_function(self, self.draw_dimensions)

	def end(self, level):
		self.ending = True

END_FUNCTION_MAP = {
	Effect.draw_black_rectangle_top:Effect.remove_black_rectangle_top, 
	Effect.draw_black_rectangle_bottom:Effect.remove_black_rectangle_bottom
}