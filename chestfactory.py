""" A factory for adding an item to a chest.
"""

from chest import Chest
from gameimage import GameImage, DEFAULT_COLORKEY

import pygame
from pygame import Rect

class ChestFactory:
	""" No constructor.
	"""
	@staticmethod
	def build_entity(raw_chest_image, chest_rect, chest_data, x, y):	
		""" build_entity( Surface, Rect, ChestData, int, int ) -> Chest

		Take a chest image and rect to create the chest object that will appear on the level, and use the chest data 
		to set the item that is in the chest.
		"""
		chest_width, chest_height = raw_chest_image.get_width()/2, raw_chest_image.get_height()
		chest_rect = Rect(chest_rect.left, chest_rect.top, chest_rect.width/2, chest_rect.height)
		closed_chest_image = raw_chest_image.subsurface(Rect(0, 0, chest_width, chest_height))
		open_chest_image = raw_chest_image.subsurface(Rect(chest_width, 0, chest_width, chest_height))
		open_chest_image.set_colorkey(DEFAULT_COLORKEY, pygame.RLEACCEL)
		chest_anim_set = GameImage.still_animation_set(closed_chest_image, chest_rect)
		chest = Chest(chest_anim_set, x, y)
		chest.open_chest_image = open_chest_image
		#use chest_data.contents_key
		chest.generate_contents(chest_data.contents_key)
		#TODO: actually add the chests item.
		return chest