""" A door that the player can open, often hiding a monster or treasure.
"""

from block import Block

PIXEL_DIST_THRESHOLD = 36

class Door(Block): #not sure how to handle a 2-part block yet
	""" Door ( AnimationSet, int, int ) -> AnimationSet

	A type of block that can be opened or closed. Might make locked doors in the future.

	Attributes:

	open: whether or not the door is open (and therefore passable)
	open_door_image: the image shown when the door is open.
	"""
	def __init__(self, animations, x, y):
		#TODO: build open and closed images out of input
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.is_solid = True
		self.x_interactable = True
		self.open = False
		self.open_door_image = None

	def in_interact_range(self, player):
		""" d.in_interact_range( Player ) -> bool

		Checks whether this door is close enough for the player to open.
		"""
		#print self.pixel_dist_from(player)
		return self.pixel_dist_from(player) < PIXEL_DIST_THRESHOLD

	def execute_x_action(self, level, player):
		""" d.execute_x_action( Level, Player ) -> None

		Opens the door in response to the player pressing X while standing near it.
		"""
		if not self.open: self.set_open()

	def set_open(self):
		""" d.set_open( ) -> None

		Change the door's attributes as a block to represent the fact that it is open.
		"""
		self.default_image = self.open_door_image
		self.image = self.open_door_image
		self.is_solid = False
		self.is_square = True

	def fill_tiles(self, tiles):
		""" d.fill_tiles( [ [ Tile ] ]) -> None

		Make the door occupy the proper set of tiles based on its dimensions.
		"""
		width, height = self.tile_dimensions()
		coords = self.coordinates()
		for y in range(coords[1], coords[1] + height):
			for x in xrange(coords[0], coords[0] + width):
				tiles[y][x].block = self #TEMP: should probably generate doorblock here

class DoorBlock(Block):
	""" Not sure I'm still using this anywhere. """
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)