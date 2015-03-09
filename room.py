""" A rectangular container for tiles and entites that will be added into a level.
"""

from roomdata import ROOM_WIDTH, ROOM_HEIGHT

class Room(object):
	""" Room( LevelObjects, Dungeon, ( int, int ), ( int, int ) ) -> Room

	Rooms do not actually end up doing anything during gameplay, but are instead used as templates to build levels when they are loaded.
	This is because all entities and tiles in the player's current level (which may be built from one or more Rooms) are active at the same time, 
	and there is no reason to keep track of which Room they came from after they are created. In cases where the Room as a concept becomes necessary
	during gameplay (for example, when the player looks at the map screen to see which rooms he has explored), the dimensions of a room (which are the
	same for any room) are used to figure out which parts of a level have been explored.

	Attributes:

	level objects: Used to store all entities and tiles in the room.

	global_coords: The x and y coordinates (with rooms as units) of the room in the dungenon.

	start_coords: The coordinates where the player will start, if applicable. This is subject to change once the beginning of the game is set up and 
	things like saving/loading the game are implemented.

	dungeon: The dungeon containing the room.
	"""
	def __init__(self, level_objects, dungeon, global_coords, start_coords):
		tiles = level_objects.get_tiles()
		self.level_objects = level_objects
		self.global_coords = global_coords
		self.start_coords = start_coords
		self.dungeon = dungeon

	def calibratePositions(self, level_origin):
		""" r.calibratePositions( ( int, int ) ) -> None

		Adjust the postions where tiles and entities will be placed in the level based on this room's position in the level.
		For example, this will do nothing if the room is in the upper-left corner of the level, or if the level only has one room.
		"""
		x_offset = 32*(self.global_coords[0] - level_origin[0])
		y_offset = 32*(self.global_coords[1] - level_origin[1])
		self.level_objects.calibratePositions(x_offset, y_offset)

	def setLevel(self, level): #if it's useful, actually store the level as a data member.
		""" r.setLevel( Level ) -> None

		Associate all tiles and entities in this room with the given level. 
		"""
		self.level_objects.setLevel(level)

	def entities_to_string(self): #for testing.
		# no docstring because only for testing
		dimensions = (ROOM_WIDTH, ROOM_HEIGHT)
		entities_string_array = []
		while(len(entities_string_array) <= dimensions[1]):
			entities_string_array.append([])
		for s in entities_string_array:
			while len(s) <= dimensions[0]:
				s.append(" ")
		entities = self.level_objects.get_entities(Entity)
		for e in entities:
			coords = (e.rect.centerx/32, e.rect.centery/32)
			entities_string_array[coords[1]][coords[0]] = "E"
		entities_string = ""
		for y in range(0, dimensions[1]):
			for x in range(0, dimensions[0]):
				entities_string += entities_string_array[y][x]
			entities_string += "\n"
		return entities_string
