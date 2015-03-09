
""" A set of data that can be used to define a level.
"""
#NOTE: this class might need to be accessed by classes outside the leveleditor.

FORMATTED_DATA_TUPLE_COUNT = 6

class LevelData(object):
	""" LevelData( str, ( int, int ), ( int, int ), bool) -> LevelData

	The data does not actually refer the level's objects, which are stored in roomdata,
	but instead stores the upper/left and upper/right corners (in rooom units) used to define the 
	level as a rectangular area of the dungeon.

	Attributes:

	name: a currently unused value that uniquely identifies the level.

	coords1: the upper-left corner of the level.

	coords2: the lower-right corner of the level.

	sunlit: whether or not the level is illuminated by sunlight.

	bg_filename: filename for loading the background image used to generate the tiles.
	"""
	def __init__(self, name, coords1, coords2, sunlit = False, bg_filename = None, travel_data = None):
		self.name = name
		self.corners = ( coords1, coords2 )
		self.sunlit = sunlit #TODO: as level data gets more complicated, maybe make this part of a more general set of tags.
		self.bg_filename = bg_filename
		self.travel_data = travel_data

	def room_set(self, rooms):
		""" ld.room_set( [ [ Room ] ] ) -> [ [ Room ] ]

		Take the room list of the whole dungeon and pull out the rooms that should be in this level.
		"""
		room_set = []
		if self.corners[0] == None: return None
		corner1 = self.corners[0]
		corner2 = self.corners[1]
		width = len(rooms[0])
		height = len(rooms)
		if not ( 0 <= corner2[0] - corner1[0] < width and 0 <= corner2[1] - corner1[1] < height):
			print corner1, corner2, width, height
			print "ERROR: attempting to load an invalid level."
			raise(SystemExit)
		for y in range(corner1[1], corner2[1] + 1):
			for x in range(corner1[0], corner2[0] + 1):
				room_set.append(rooms[y][x])
		return room_set

	def formatted_data(self): #used for saving to files
		""" ld.formatted_data( ) -> ( str, ( int, int ), ( int, int ), bool, str )

		Formats the data members of leveldata into a tuplet of primitive types.
		This is used for saving files.
		"""

		return (self.name, self.corners[0], self.corners[1], self.sunlit, self.bg_filename, self.travel_data)

	def setSunlit(self, sunlit):
		""" ld.setSunlit( ) -> bool

		A setter for the sunlit value. Not sure this is necessary.
		"""
		self.sunlit = sunlit

	@staticmethod
	def deformatted_level_set(formatted_data): #used for loading from files
		""" ld.deformatted_level_set( [ ( str, ( int, int ), ( int, int ), bool, str ) ] ) -> [ LevelData ]

		Create a useable list of LevelDatas from saved, formatted level data.
		"""
		level_set = []
		for d in formatted_data:
			level_set.append(LevelData.deformatted_level(d))
		return level_set

	@staticmethod
	def deformatted_level(formatted_data): #used for loading from files
		""" ld.deformatted_level( ( str, ( int, int ), ( int, int ), bool, str, ( str, str, str ) )  ) -> LevelData 

		Create a useable LevelData from a a saved, formatted level data.
		This is basically the reverse of formatted_data().
		"""
		if len(formatted_data) != FORMATTED_DATA_TUPLE_COUNT:
			print "ERROR: attempting to load outdated level data."
			raise(SystemExit)
		return LevelData(formatted_data[0], formatted_data[1], formatted_data[2], formatted_data[3], formatted_data[4], formatted_data[5])