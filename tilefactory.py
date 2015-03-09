""" A factory used to build tiles. Not done yet.
"""
from gameimage import GameImage
from pygame import Rect
from spritesheet import SpriteSheet

class TileFactory(object):
	""" TileFactory( Surface, ( int, int ) ) -> TileFactory

	Currently just takes an image showing one or two tiles and fills a 2D list with them. So far, it's only used to 
	store a sky tile and a cave tile.
	However, this setup might be useful for reading in an entire level of tiles, which in turn is read in from an image.
	It would be necessary in this case to make images representing the background of every level, though this might be an
	added functionality for the leveleditor.
	
	Attributes:

	tile_images: A 2D grid of tile images.	
	"""
	def __init__(self, tile_sheet_image, dimensions):
		self.tile_images = []
		default_rect = Rect(0, 0, 32, 32)
		tile_sheet = SpriteSheet(tile_sheet_image, default_rect)
		current_rect = default_rect
		for y in range(dimensions[1]): #TODO: make it possible to move rect down for y > 1
			self.tile_images.append([])
			for x in range(dimensions[0]):
				current_rect.topleft = x*32, y*32
				self.tile_images[y].append(tile_sheet_image.subsurface(current_rect))

	def image_at(self, coords):
		""" tf.image_at( ( int, int ) ) -> Surface

		Return the tile image at the given coordinates.
		"""
		return self.tile_images[coords[1]][coords[0]]
	
	def tile_at(self, coords):
		""" tf.tile_at( ( int, int ) ) -> AnimationSet

		Return an AnimationSet (though it's not animated) for the tile at the given coordinates.
		"""
		tile_image = self.image_at(coords)
		return GameImage.still_animation_set(tile_image)