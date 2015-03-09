""" A data object used to generate a room.
"""

from signdata import SignData
from cutscenetriggerdata import CutsceneTriggerData
from chestdata import ChestData
from platformdata import PlatformData, DestructiblePlatformData
from tiledata import TileData, BlockedTileData, DEFAULT_SIGN, DEFAULT_CHEST, DEFAULT_CUTSCENE_TRIGGER, DESTRUCTIBLE_PLATFORM

ROOM_WIDTH = 28
ROOM_HEIGHT = 20

class RoomData(object):
	""" RoomData( int, int, int, int ) -> RoomData

	A roomdata defines a room full of tiledatas as a cell in a 2D gird representing the dungeon.
	It is initialzied with an empty tiledata set.

	Attributes:

	x, y: The coordinates of the room in the dungeon.

	tiles: The grid of tiledatas in the room.
	"""
	def __init__(self, width, height, x, y):
		self.global_x, self.global_y = x, y
		self.tiles = RoomData.empty_tile_set(width, height)
	
	def empty(self):
		""" rd.empty( ) -> bool

		Return True if there is anything in the room besides empty tiles.
		"""
		for row in self.tiles:
			for t in row:
				if t != None: return False #NOTE: because of this, if we make it possible to clear tiles, doing so should set those tiles to None.
		return True

	def tile_at(self, x, y):
		""" rd.tile_at( int, int ) -> TileData

		Returns the tiledata at the given coordinates.
		"""
		return self.tiles[y][x]

	def setAllTiles(self, tile_set):
		""" rd.setAllTiles( [ [ TileData ] ] ) -> None

		Take a 2D list of tiledatas and set the tiledatas in this roomdata's list to the ones given.
		"""
		rows, cols = len(tile_set), len(tile_set[0])
		for y in xrange(rows):
			for x in xrange(cols):
				self.tiles[y][x] = tile_set[y][x]
	
	def set_tile(self, tile_data, col, row):
		""" rd.set_tile( TileData, int, int ) -> None

		Set the tile at the given coordinates to the given tiledata.
		"""
		self.tiles[row][col] = tile_data #might benefit from a special setter if tiledata becomes more complex.

	def formatted_data(self):
		""" rd.formatted_data( ) -> ( int, int, [ [ ( str, str, int, int ) ] ] ) 

		Converts this RoomData into primitive types for the purpose of saving to a file.
		"""
		return (self.global_x, self.global_y, self.formatted_tile_set()) #might need to format tiles

	def formatted_tile_set(self):
		""" rd.formatted_tile_set( ) -> [ [ ( str, str, int, int )  ] ]

		Converts the tiledatas into primitive types for the purpose of saving to a file.
		"""
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
		""" deformatted_room_set( [ [ ( int, int, [ [ ( str, str, int, int ) ] ] ) ] ], str ) -> [ [ RoomData ] ]

		Takes a list of formatted RoomDatas (loaded from a file) and converts them into usable RoomData objects.
		"""
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
		""" deformatted_room( ( int, int, [ [ ( str, str, int, int ) ] ] ) ) -> RoomData 

		Takes a formatted RoomData (loaded from a file) and converts it into a usable RoomData object.
		This is effectively a reversal of the formatted_data() method.
		"""
		x, y = formatted_data[0], formatted_data[1]
		tile_set = RoomData.deformatted_tile_set(formatted_data[2], filepath) #have to deformat tiles before returning the room_data.
		width, height = len(tile_set[0]), len(tile_set) #might need a None exeception handler
		room_data = RoomData(width, height, x, y)
		room_data.setAllTiles(tile_set)
		return room_data

	@staticmethod
	def deformatted_tile_set(formatted_data, filepath = "./"):
		""" deformatted_tile_set( [ [ ( str, str, int, int ) ] ] , str ) -> [ [ TileData ] ]

		Builds a grid of tiledatas for a roomdata using a grid of data loaded from a file. 
		"""
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
		""" addTiles( [ [ TileData ], ( str, str, int, int ), int, int, str ] ) -> None

		Use the formatted tiledata (from file) to build a usable TileData object and place it in the given "tiles"
		grid, expanding the grid if necessary. Note that this will also look at the dimensions of the TileData objects and
		mark tile slots that they will block.
		"""
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
	def deformatted_tile(formatted_data, filepath = "./"):	#this will need to change as the tiledata's constructor does.
		""" deformatted_tile( ( str, str, int, int ) ) -> TileData

		Take a tuplet of primitive data loaded from a file and turn it into a usable TileData object.
		"""
		entity_key = formatted_data[0]
		tile_data = None
		if entity_key in TILE_INIT_MAP:
			init_function = TILE_INIT_MAP[entity_key] #TODO: get a constructor from a map
			tile_data = init_function(formatted_data, filepath)
		else:
			tile_data = TileData(formatted_data[0], formatted_data[1], filepath)
		return tile_data

	@staticmethod
	def deformatted_sign(formatted_data, filepath):	# this will need to change as this class's constructor does.
		""" deformatted_sign( ( str, str, int, int, [ str ] ), str ) -> SignData

		Take a tuplet of primitive data loaded from a file and turn it into a usable SignData object.
		"""
		sign_data = SignData(formatted_data[0], formatted_data[1], filepath)
		sign_data.text_panes = formatted_data[4]
		return sign_data

	@staticmethod
	def deformatted_chest(formatted_data, filepath):	# this will need to change as this class's constructor does.
		""" deformatted_chest( ? ) -> ChestData

		Take a tuplet of primitive data loaded from a file and turn it into a usable ChestData object.
		"""
		chest_data = ChestData(formatted_data[0], formatted_data[1], filepath)
		chest_data.contents_key = formatted_data[4]
		return chest_data


	@staticmethod
	def deformatted_cutscene_trigger(formatted_data, filepath):	# this will need to change as this class's constructor does.
		""" deformatted_cutscene_trigger( ( str, str, int, int, str ), str ) -> CutsceneTriggerData

		Take a tuplet of primitive data loaded from a file and turn it into a usable CutsceneTriggerData object.
		"""
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
	def empty_tile_set(width, height):
		""" empty_tile_set( int, int ) -> [ [ None ] ]

		Builds a 2D list of the given dimensions. This list is then used to store TileDatas.
		"""
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