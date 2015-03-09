
from signdata import SignData
from cutscenetriggerdata import CutsceneTriggerData
from chestdata import ChestData
from platformdata import PlatformData, DestructiblePlatformData
from tiledata import TileData, BlockedTileData, DEFAULT_SIGN, DEFAULT_CHEST, DEFAULT_CUTSCENE_TRIGGER, DESTRUCTIBLE_PLATFORM

ROOM_WIDTH = 28
ROOM_HEIGHT = 20

class RoomData(object):
	"""docstring for RoomData"""
	def __init__(self, width, height, x, y):
		self.global_x, self.global_y = x, y
		self.tiles = RoomData.empty_tile_set(width, height)
	
	def empty(self):
		for row in self.tiles:
			for t in row:
				if t != None: return False #NOTE: because of this, if we make it possible to clear tiles, doing so should set those tiles to None.
		return True

	def tile_at(self,x,y):
		return self.tiles[y][x]

	def setAllTiles(self, tile_set):
		rows, cols = len(tile_set), len(tile_set[0])
		for y in xrange(rows):
			for x in xrange(cols):
				self.tiles[y][x] = tile_set[y][x]
	
	def set_tile(self,tile_data,col,row):
		self.tiles[row][col] = tile_data #might benefit from a special setter if tiledata becomes more complex.

	def formatted_data(self):
		return ( self.global_x, self.global_y, self.formatted_tile_set() ) #might need to format tiles

	def formatted_tile_set(self):
		tiles = []
		for y in xrange (len(self.tiles)):
			tiles.append([])
			for x in xrange(len(self.tiles[y])):
				next_data = None
				next_tile = self.tiles[y][x]
				if next_tile != None:
					next_data = next_tile.formatted_data()
				tiles[y].append(next_data)
		return tiles

	@staticmethod
	def deformatted_room_set(formatted_data, filepath = "./"):	
		rooms = []
		for y in xrange (len(formatted_data)):
			rooms.append([])
			for x in xrange(len(formatted_data[y])):
				next_data = None
				next_room = formatted_data[y][x]
				if next_room != None:
					next_data = RoomData.deformatted_room(next_room, filepath)
				rooms[y].append(next_data)
		return rooms

	@staticmethod
	def deformatted_room(formatted_data, filepath = "./"):	
		x, y = formatted_data[0], formatted_data[1]
		tile_set = RoomData.deformatted_tile_set(formatted_data[2], filepath) #have to deformat tiles before returning the room_data.
		width,height = len(tile_set[0]), len(tile_set) #might need a None exeception handler
		room_data = RoomData(width, height, x, y)
		room_data.setAllTiles(tile_set)
		return room_data

	@staticmethod
	def deformatted_tile_set(formatted_data, filepath = "./"):
		tiles = []
		for y in xrange (len(formatted_data)):
			tiles.append([])
			for x in xrange(len(formatted_data[y])):
				tiles[y].append(None)
		for y in xrange(len(formatted_data)):
			for x in xrange(len(formatted_data[y])):
				next_data = None
				next_tile = formatted_data[y][x]
				if next_tile != None:
					RoomData.addTiles(tiles, next_tile, x, y, filepath)
		return tiles

	@staticmethod
	def addTiles(tiles, formatted_data, x_pos, y_pos, filepath = "./"):
		width = formatted_data[2]
		height = formatted_data[3]
		origin_tile = RoomData.deformatted_tile(formatted_data, filepath)
		tiles[y_pos][x_pos] = origin_tile
		for x in range(x_pos + 1, x_pos + width):
			tiles[y_pos][x] = BlockedTileData(origin_tile, x_pos, y_pos)
		for y in range(y_pos + 1, y_pos + height):
			for x in range(x_pos, x_pos + width):
				tiles[y][x] = BlockedTileData(origin_tile, x_pos, y_pos)

	@staticmethod
	def deformatted_tile(formatted_data, filepath = "./"):	#this will need to change as this class's constructor does.
		entity_key = formatted_data[0]
		tile_data = None
		if entity_key in TILE_INIT_MAP:
			init_function = TILE_INIT_MAP[entity_key] 
			tile_data = init_function(formatted_data, filepath)
		else:
			tile_data = TileData(formatted_data[0], formatted_data[1], filepath)
		return tile_data

	@staticmethod
	def deformatted_sign(formatted_data, filepath):	#this will need to change as this class's constructor does.
		sign_data = SignData(formatted_data[0], formatted_data[1], filepath)
		sign_data.text_panes = formatted_data[4]
		return sign_data

	#TODO: make sure this copies Platformer/chestdata.py
	@staticmethod
	def deformatted_chest(formatted_data, filepath):	# this will need to change as this class's constructor does.
		""" deformatted_chest( ? ) -> ChestData

		Take a tuplet of primitive data loaded from a file and turn it into a usable ChestData object.
		"""
		chest_data = ChestData(formatted_data[0], formatted_data[1], filepath)
		chest_data.contents_key = formatted_data[4]
		return chest_data

	@staticmethod
	def deformatted_cutscene_trigger(formatted_data, filepath):	#this will need to change as this class's constructor does.
		trigger_data = CutsceneTriggerData(formatted_data[0], formatted_data[1], filepath)
		trigger_data.cutscene_key = formatted_data[4]
		return trigger_data

	@staticmethod
	def deformatted_destructible_platform(formatted_data, filepath):	# this will need to change as this class's constructor does.
		""" deformatted_destructible_platform( ( str, str, int, int, str ), str ) -> DestructiblePlatformData

		Take a tuplet of primitive data loaded from a file and turn it into a usable DestructiblePlatformData object.
		"""
		platform_data = DestructiblePlatformData(formatted_data[0], formatted_data[1], filepath)
		platform_data.catalyst = formatted_data[4]
		return platform_data

	@staticmethod
	def empty_tile_set(width,height):
		tiles = []
		for y in xrange(height):
			tiles.append([])
			for x in xrange(width):
				tiles[y].append(None)
		return tiles

TILE_INIT_MAP = {
	DEFAULT_SIGN:RoomData.deformatted_sign,
	DEFAULT_CHEST:RoomData.deformatted_chest,
	DEFAULT_CUTSCENE_TRIGGER:RoomData.deformatted_cutscene_trigger,
	DESTRUCTIBLE_PLATFORM:RoomData.deformatted_destructible_platform
}