# NOTE: not sure this is actually used by leveleditor clalsses.
#NOTE: this class might need to be accessed by classes outside the leveleditor.

# TODO: implemeent dungeon travel data

class LevelData(object):
	"""docstring for LevelData"""
	def __init__(self, name, coords1, coords2, sunlit = False, bg_filename = None, travel_data = None):
		self.name = name
		self.corners = (coords1, coords2)
		self.sunlit = sunlit #TODO: as level data gets more complicated, make this part of a more general set of tags.
		self.bg_filename = bg_filename
		self.travel_data = travel_data

	def room_set(self, rooms):
		room_set = []
		corner1 = self.corners[0]
		corner2 = self.corners[1]
		for y in range(corner1[1], corner2[1] + 1):
			for x in range(corner1[0], corner2[0] + 1):
				room_set.append(rooms[y][x])
		return room_set

	def formatted_data(self): #used for saving to files
		return (self.name, self.corners[0], self.corners[1], self.sunlit, self.bg_filename, self.travel_data)	#TODO: add travel data

	def setSunlit(self,sunlit):
		self.sunlit = sunlit

	@staticmethod
	def deformatted_level_set(formatted_data): #used for loading from files
		level_set = []
		for d in formatted_data:
			level_set.append(LevelData.deformatted_level(d))
		return level_set

	@staticmethod
	def deformatted_level(formatted_data): #used for loading from files
		return LevelData(formatted_data[0], formatted_data[1], formatted_data[2], formatted_data[3], formatted_data[4], formatted_data[5])	#TODO: add travel data