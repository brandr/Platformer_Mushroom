from tilefactory import TileFactory
from entityfactory import EntityFactory
from platformfactory import PlatformFactory
from signfactory import SignFactory
from chestfactory import ChestFactory
from doorfactory import DoorFactory
from pickupfactory import PickupFactory
from cutscenetriggerfactory import CutsceneTriggerFactory
from levelobjects import LevelObjects
from room import Room
from block import Block
from tile import Tile
from gameimage import GameImage
from tiledata import TileData, BlockedTileData, DEFAULT_TILE_SIZE, DEFAULT_CUTSCENE_TRIGGER, PLAYER_START, DESTRUCTIBLE_PLATFORM, DEFAULT_SIGN, DEFAULT_DOOR, DEFAULT_CHEST, OIL_PICKUP
from roomdata import ROOM_WIDTH, ROOM_HEIGHT

from pygame import Rect

NON_DEFAULT_ENTITY_MAP = {
	DESTRUCTIBLE_PLATFORM:PlatformFactory,
	DEFAULT_SIGN:SignFactory,	
	DEFAULT_DOOR:DoorFactory,
	DEFAULT_CHEST:ChestFactory,
	OIL_PICKUP:PickupFactory,
	DEFAULT_CUTSCENE_TRIGGER:CutsceneTriggerFactory
}

class RoomFactory(object):

	@staticmethod
	def dungeon_rooms(dungeon, room_data_set, level_data_set):
		""" dungeon_rooms( Dungeon, [ [ RoomData ] ], [ LevelData ] ) -> [ [ Room ] ]

		Generate a double list of rooms from a double list of roomdatas along with some leveldatas..
		"""
		# TODO: probably sort out level backgrounds starting here
		rooms = []
		x1, y1 = RoomFactory.origin(level_data_set)
		x2, y2 = RoomFactory.lower_right(level_data_set)
		for y in range(0, y2 + 1):	
			rooms.append([])
			for x in range(0, x2 + 1):
				rooms[y].append(None)
		for y in range(y1, y2 + 1):	
			for x in range(x1, x2 + 1):
				next_data = room_data_set[y][x]
				next_room = RoomFactory.build_room(dungeon, next_data, x, y)
				rooms[y][x] = next_room
				#rooms[y].append(next_room)
		print "Rooms set up."
		return rooms

	@staticmethod
	def origin(level_data_set):
		""" origin( [ LevelData ] ) -> int, int

		Go through the set of all levels in the dungeon and finds the coordinates of the upper-left room.
		"""
		origin = level_data_set[0].corners[0]
		for data in level_data_set:
			corner = data.corners[0]
			origin = ( min(origin[0], corner[0]), min(origin[1], corner[1]) )
		return origin
		"""
		for y in xrange(len(room_data_set)):
			for x in xrange(len(room_data_set[y])):
				next_data = room_data_set[y][x]
				if(room_data_set[y][x] != None): return x, y
		return None
		"""

	@staticmethod
	def lower_right(level_data_set):
		""" lower_right( [ LevelData ] ) -> int, int 

		Go through the set of all levels in the dungeon and finds the coordinates of the lower-right room.
		"""
		lower_right = level_data_set[0].corners[1]
		for data in level_data_set:
			corner = data.corners[1]
			lower_right = ( max(lower_right[0], corner[0]), max(lower_right[1], corner[1]) )
		return lower_right

	@staticmethod
	def build_room(dungeon, room_data, global_x, global_y): #might be able to get global x and global y through roomdata's coords instead
		""" build_room( Dungeon, RoomData, int, int ) -> Room

		Creates a room using a roomdata and a pair of global coordinates giving the room's location in the dungeon
		(with rooms as units). A None RoomData can be passed to generate an empty room. However, it doesn't really make
		sense to allow the player to travel through a room created this way (since there will technically be no tiles),
		so in practice these should be blocked off.

		Note that currently, tiles are created with temporary images which will be overridden when the actual level is created.
		This isn't really an issue though it might make sense to change it later if it improves efficiency.

		The 2D for loop iterates through the tiledata set, generating an entity if it finds a non-empty tiledata. This is where
		the entities' images/animations are first created, and also where we check whether an entity can be created with the default 
		factory (called the EntityFactory) or a non-default factory (such as SignFactory).
		"""
		if(room_data == None): return RoomFactory.empty_room(dungeon, global_x, global_y) 
		tiles = []
		entities = [] #TODO: figure out why the example platformer used Group

		start_coords = (False, 0, 0)
		x = y = 0

		# TODO: remove test tiles to make this part more efficient if necessary, since the test tiles will be overwritten anyway.

		tile_images = GameImage.load_image_file('./data/', 'test_tiles_1.bmp') 
		tile_factory = TileFactory(tile_images, (2, 1))
		default_cave_tile = tile_factory.tile_at((0, 0))
		default_tile = default_cave_tile

		end_x = ROOM_WIDTH
		end_y = ROOM_HEIGHT

		for row in xrange(end_y):
			tiles.append([])
			for col in xrange(end_x):
				next_tile_data = room_data.tile_at(col, row)
				t = Tile(default_tile, x, y)
				if next_tile_data != None and not isinstance(next_tile_data, BlockedTileData):
					if next_tile_data.entity_key == PLAYER_START:
						start_coords = (True, x, y)
					else:

						#TODO: remember that this part may need some checks if the object created is larger than 32*32.
						raw_entity_image = next_tile_data.get_image("./LevelEditor/")
						entity_width, entity_height = next_tile_data.width, next_tile_data.height
						entity_rect = Rect(0, 0, entity_width*DEFAULT_TILE_SIZE, entity_height*DEFAULT_TILE_SIZE)

						key = next_tile_data.entity_key
						if key in NON_DEFAULT_ENTITY_MAP:
							factory = NON_DEFAULT_ENTITY_MAP[key]
							entity = factory.build_entity(raw_entity_image, entity_rect, next_tile_data, x, y)
							entities.append(entity)
							if isinstance(entity, Block): 
								t.block = entity
						
						elif next_tile_data.is_animated():
							entity_animation_set = GameImage.load_animation_set(next_tile_data, DEFAULT_TILE_SIZE)	#TODO: allow this to incorporate frames
							e = EntityFactory.build_entity(entity_animation_set, key, x, y)
							entities.append(e)
		
						else:
							still_entity_image = GameImage.still_animation_set(raw_entity_image, entity_rect)
							e = EntityFactory.build_entity(still_entity_image, key, x, y)
							entities.append(e)
							if isinstance(e, Block): 
								t.block = e
		
				tiles[y/DEFAULT_TILE_SIZE].append(t)
				x += DEFAULT_TILE_SIZE 
			y += DEFAULT_TILE_SIZE
			x = 0
			
		room_objects = LevelObjects(None, tiles, entities)
		created_room = Room(room_objects, dungeon, (global_x, global_y), start_coords)
		#print "MADE ROOM AT: " + str((global_x, global_y))
		return created_room

	@staticmethod
	def empty_room(dungeon, global_x, global_y):
		""" empty_room( Dungeon, int, int ) -> Room

		Generates an empty room. Note that this means there are not even walls around the edges of the room.
		Also, I'm pretty sure that a room with no objects contained in a level (such as the center room in a 3x3 level)
		does not technically count as an empty room. These only exist because the set of rooms "contained" in the dungeon 
		must always be rectangular, even if the set of explorable rooms is not.
		"""
		tiles = []
		entities = []

		start_coords = (False, 0, 0)
		x = y = 0

		tile_images = GameImage.load_image_file('./images/', 'test_tiles_1.bmp') 
		tile_factory = TileFactory(tile_images, (2, 1))
		default_cave_tile = tile_factory.tile_at((0, 0))
		default_sky_tile = tile_factory.tile_at((1, 0))
		default_tile = default_cave_tile

		end_x = ROOM_WIDTH
		end_y = ROOM_HEIGHT

		for row in xrange(end_y):
			tiles.append([])
			for col in xrange(end_x):
				t = Tile(default_tile, x, y)
				tiles[y/DEFAULT_TILE_SIZE].append(t)
				x += DEFAULT_TILE_SIZE 
			y += DEFAULT_TILE_SIZE
			x = 0

		room_objects = LevelObjects(None, tiles, entities)
		created_room = Room(room_objects, dungeon,(global_x, global_y), start_coords)
		return created_room