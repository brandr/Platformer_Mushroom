""" A pane showing a map of the the dungeon that the player is in.
"""

from pygame import Color, Surface, draw
from pygame.draw import *

WHITE = Color("#FFFFFF")
RED = Color("#FF0000")
GREEN = Color("#00FF00")
PURPLE = Color("#FF00FF")
CYAN = Color("#00FFFF")

MAP_PANE_WIDTH, MAP_PANE_HEIGHT = 400, 400
ROOM_TILE_WIDTH, ROOM_TILE_HEIGHT = MAP_PANE_WIDTH/20, MAP_PANE_HEIGHT/20

class MapPane: #inheritance?
	""" The map pane is a visual element that appears on the pause screen.
	It represents the dungeon as a grid, with unexplored rooms not shown 
	and the current room flashing.

	Attributes:

	player: The player occupying the dungeon.

	x, y: The current room coordinates of the player.

	pane_image: The Surface upon which the dungeon map is blitted.

	blink_index: A cyclic value used to create a blinking effect on the player's current room.
	"""
	def __init__(self, player, x, y):
		self.player, self.x, self.y = player, x, y
		self.pane_image = Surface((MAP_PANE_WIDTH, MAP_PANE_HEIGHT)) #TEMP
		self.blink_index = 0
		self.draw_borders()
		
	def update(self):
		""" mp.update() -> None

		Blink depending on the blink index and redraw the dungeon map.
		"""
		self.advance_blink_index()
		self.draw_map()

	def draw_borders(self):
		""" mp.draw_borders( ) -> None

		Draw the white lines that form the borders of the map pane.
		"""
		corners = [(0, 0), (MAP_PANE_WIDTH - 2, 0), (MAP_PANE_WIDTH - 2, MAP_PANE_HEIGHT - 2), (0, MAP_PANE_HEIGHT - 2)] #TEMP
		lines(self.pane_image, WHITE, True, corners, 2)

	def draw_map(self):	 
		""" mp.draw_map( ) -> None

		Grab information from the dungeon about which room have been explored and which have not.
		Use this information to draw the dungeon map. This method also handles the blink cycle.
		"""
		current_level = self.player.current_level
		dungeon = current_level.dungeon
		current_room_image = MapPane.draw_current_room_image()
		unexplored_room_image = MapPane.draw_unexplored_room_image()
		for L in dungeon.dungeon_levels:
			if not L.is_explored(): continue
			origin = L.origin
			width, height = L.room_width(), L.room_height()
			pixel_coords = ((origin[0] + 1)*ROOM_TILE_WIDTH, (origin[1] + 1)*ROOM_TILE_HEIGHT)
			explored_level_image = MapPane.draw_explored_level_image(width, height, L.outdoors)
			self.pane_image.blit(explored_level_image, pixel_coords)
			for y in xrange(height):
				for x in xrange(width):
					if not L.explored_at(x, y):
						pixel_coords = ((origin[0] + x + 1)*ROOM_TILE_WIDTH, (origin[1] + y + 1)*ROOM_TILE_HEIGHT)
						self.pane_image.blit(unexplored_room_image, pixel_coords)
		current_global_coords = current_level.global_coords(self.player.coordinates())
		current_pixel_coords = ( (current_global_coords[0] + 1)*ROOM_TILE_WIDTH, (current_global_coords[1] + 1 )*ROOM_TILE_HEIGHT)
		if self.blink_index > 20:
			self.pane_image.blit(current_room_image, current_pixel_coords)
			if self.blink_index > 40:
				self.blink_index = 0

	def advance_blink_index(self):
		""" mp.advance_blink_index( ) -> None

		Increment the blink index by 1. If it is greater than 20, then the blink is in the "on" state.
		If it is greater than 40, it is reset to 0. 
		"""
		self.blink_index += 1
					
	@staticmethod
	def draw_explored_level_image(width, height, sunlit):
		""" draw_explored_level_image( int, int, bool ) -> Surface

		Draw a green (if aboveground) or purple (if underground) rectangle of the given dimensions
		with a white outline.
		"""
		color = None
		if sunlit: color = GREEN
		else: color = PURPLE
		explored_level_image = Surface((width*ROOM_TILE_WIDTH, height*ROOM_TILE_HEIGHT))
		explored_level_image.fill(color)
		corners = [(0, 0), (width*ROOM_TILE_WIDTH - 2, 0), (width*ROOM_TILE_WIDTH - 2, height*ROOM_TILE_HEIGHT - 2), (0, height*ROOM_TILE_HEIGHT - 2)] #TEMP
		lines(explored_level_image, WHITE, True, corners, 2)
		return explored_level_image

	@staticmethod
	def draw_unexplored_room_image():
		""" draw_unexplored_room_image( ) -> Surface

		Creates a black square to represent a dark area that has not been explored yet.
		"""
		return Surface((ROOM_TILE_WIDTH, ROOM_TILE_HEIGHT))

	@staticmethod
	def draw_current_room_image():	
		""" draw_current_room_image( ) -> Surface

		Returns a cyan square that marks the room the player is currently in.
		"""
		current_room_image = Surface((ROOM_TILE_WIDTH, ROOM_TILE_HEIGHT))
		current_room_image.fill(CYAN)
		return current_room_image

