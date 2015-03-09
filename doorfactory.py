""" A special factory for making doors.
"""

#from door import *
from door import Door
from gameimage import GameImage

from pygame import Rect

class DoorFactory:
	""" No constructor.
	"""
	@staticmethod
	def build_entity(raw_door_image, door_rect, door_data, x, y):	
		""" build_entity( Surface, Rect, ?, int, int) -> Door

		Create a door based on the given data. door_data is not used here, but still appears as an arg
		because other factories may take an argument there.

		The raw_door_image contains both the open and closed version of the door, which are then attached
		to the door.
		"""
		door_width, door_height = raw_door_image.get_width()/2, raw_door_image.get_height()
		door_rect = Rect(door_rect.left, door_rect.top, door_rect.width/2, door_rect.height)
		closed_door_image = raw_door_image.subsurface(Rect(0, 0, door_width, door_height))
		open_door_image = raw_door_image.subsurface(Rect(door_width, 0, door_width, door_height))
		door_anim_set = GameImage.still_animation_set(closed_door_image, door_rect)
		door = Door(door_anim_set, x, y)
		door.open_door_image = open_door_image
		return door