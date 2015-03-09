from leveldata import *
from roomdata import *

class DungeonData(object):
	"""docstring for DungeonData"""
	def __init__(self, level_data_set, room_data_set):
		self.level_data_set = level_data_set
		self.rooms = room_data_set #a double array of room_data

	def formatted_data(self):	#may need a corresponding method to build a dungeonData object from this.
		formatted_level_set = self.formatted_level_set()
		formatted_rooms =  self.formatted_room_set()
		return (formatted_level_set,formatted_rooms)

	def formatted_level_set(self):
		levels = []
		for l in xrange (len(self.level_data_set)):
			next_data = self.level_data_set[l].formatted_data()
			levels.append(next_data)
		return levels

	def formatted_room_set(self):
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
		level_data_set = LevelData.deformatted_level_set(formatted_data[0])
		room_data_set = RoomData.deformatted_room_set(formatted_data[1], filepath)
		return DungeonData(level_data_set,room_data_set)
		#return dungeon_data
		#TODO: return a DungeonData object.
		#return None