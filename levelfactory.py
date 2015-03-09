""" A factory that creates levels from LevelDatas and Rooms.
"""

from roomfactory import *
from level import Level
#The LevelFactory calls methods from RoomFactory (along with some additional methods)
	#to create the dungeon levels based on a set of input.

class LevelFactory(object):
	""" LevelFactory( ) -> LevelFactory

	The constructor for this class is pretty much not useful at all. It may become useful
	in the future if we want specific LevelFactories that have different properties.
	"""
	def __init__(self):
		# neither of these are used right now. Might make LevelFactory a static class if it needs no private data.
		self.global_x = 0
		self.global_y = 0

	#maybe this should go in roomfactory instead? Not sure
	def dungeon_rooms(self, dungeon, room_data_set, level_data_set):
		""" lf.dungeon_rooms( Dungeon, [ [ RoomData ] ], [ LevelData ] ) -> [ [ Room ] ]

		Calls the RoomFactory method to convert RoomDatas into a grid of Rooms.
		"""
		return RoomFactory.dungeon_rooms(dungeon, room_data_set, level_data_set)

	def dungeon_levels(self, dungeon, rooms, level_data_set):
		""" lf.dungeon_levels( Dungeon, [ [ Room ] ], [ LevelData ] ) -> [ Level ]

		Uses the enclosed room set  of each level, along with the upper-left corner of 
		each level, to determine where each level should be in the dungeon and what objects
		it should contain.
		"""
		levels = []
		for d in level_data_set:
			level_rooms = d.room_set(rooms)
			origin = d.corners[0]
			if origin == None: continue
			next_level = self.build_level(dungeon, d, origin, level_rooms)
			levels.append(next_level)
		return levels

		# If I end up using the system where levelIDs are stored in arrays corresponding to rooms,
		# should probably have this done for dungeon in this method.
		# NOTE: what did I mean when I wrote that?
	def build_level(self, dungeon, level_data, origin, rooms): # could also get origin from level data
		""" lf.build_level( Dungeon, [ LevelData ], ( int, int ) [ [ Room ] ] ) -> Level 

		Uses Level's constructor to build the Level.
		"""
		return Level(dungeon, level_data, origin, rooms)