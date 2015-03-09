""" A data set used to generate a dungeon.
"""

from leveldata import LevelData
from roomdata import RoomData

class DungeonData(object):
	""" DungeonData( [ LevelData ], [ [ RoomData ] ] -> DungeonData

	The dungeon is generated from a 1D list of LevelData and a 2D list of DungeonData.

	Attrbutes:

	level_data_set: A set of leveldata, some of which will associate the generated levels with rooms.

	rooms: The set of rooms that will exist on the dungeon grid. They are stored in a 2D array
	where a roomdata's index represents its coordinates in the level.
	"""
	def __init__(self, level_data_set, room_data_set):
		self.level_data_set = level_data_set
		self.rooms = room_data_set #a double array of room_data

	def formatted_data(self):	#may need a corresponding method to build a dungeonData object from this.
		""" dd.formatted_data( ) -> ( [ ( str, int, int, bool ) ], [ [ ( int, int, [ [ ( str, str, int, int ) ] ] ) ] ] )

		Returns a complicated nested tuplet of primitives representing this dungeon's data.
		This is part of the saving/loading process.
		"""
		formatted_level_set = self.formatted_level_set()
		formatted_rooms =  self.formatted_room_set()
		return (formatted_level_set, formatted_rooms)

	def formatted_level_set(self):
		""" dd.formatted_level_set( ) -> [ ( str, int, int, bool ) ]

		Returns a list of levels formatted into primitive types.
		"""
		levels = []
		for l in xrange (len(self.level_data_set)):
			next_data = self.level_data_set[l].formatted_data()
			levels.append(next_data)
		return levels

	def formatted_room_set(self):
		""" dd.formatted_room_set( ) -> [ [ ( int, int, [ [ ( str, str, int, int ) ] ] ) ] ]

		Returns a 2D list of rooms formatted into primitive types.
		"""
		if self.rooms == None: return None
		rooms = []
		for y in xrange (len(self.rooms)):
			rooms.append([])
			for x in xrange(len(self.rooms[y])):
				next_data = None
				next_room = self.rooms[y][x]
				if next_room != None:
					next_data = next_room.formatted_data()
				rooms[y].append(next_data)
		return rooms

	@staticmethod
	def deformatted_dungeon(formatted_data, filepath = "./"):
		""" deformatted_dungeon( [ ( str, int, int, bool ) ], [ [ ( int, int, [ [ ( str, str, int, int ) ] ] ) ] ] ) -> DungeonData

		Generate a dungeon from saved primitive types.
		"""
		level_data_set = LevelData.deformatted_level_set(formatted_data[0])
		room_data_set = RoomData.deformatted_room_set(formatted_data[1], filepath)
		return DungeonData(level_data_set, room_data_set)