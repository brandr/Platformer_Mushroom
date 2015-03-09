""" A set of all objects (tiles and entities) in a level.
"""

from roomdata import *
from chest import Chest #TEMP

from numpy import array

class LevelObjects(object):
	""" LevelObjects( Level, [ [ Tile ] ], [ Entity ] ) -> LevelObjects

	The LevelObjects exists to manage the contents of a level and access
	entites of a specific type.

	Attributes:

	level: the level these objects will be placed in.

	tiles: a double list of the tiles that will be in the level.

	entities: all entities (player, monsters, blocks, etc.) in the level.

	player: the player currently on the level. There can only be one.
	"""
	def __init__(self, level, tiles = None, entities = None):
		self.level = level
		self.tiles = tiles
		#self.tiles = array(tiles)
		self.entities = entities
		self.player = None

	def get_entities(self, entity_type):
		""" lo.get_entities( Class ) -> [ Entity ]

		Filter out all entities in the level of the given class.		
		"""
		return [e for e in self.entities if isinstance(e, entity_type)]

	def get_tiles(self):
		""" lo.get_tiles( ) -> [ [ Tile ] ]

		Returns the grid of all tiles on this level. This might not be necessary.
		"""
		return self.tiles

	def addPlayer(self, player):
		""" lo.addPlayer( Player ) -> None

		Adds the player to the level and also the entity list.
		"""
		self.player = player
		self.entities.append(player)

	def remove(self, entity):
		""" lo.remove( Entity ) -> None

		Remove the entity from the level unless it's not in the level.
		"""
		if entity in self.entities:
			self.entities.remove(entity)

	def removePlayer(self):
		""" lo.removePlayer( ) -> None

		Remove the player from the level.
		"""
		self.entities.remove(self.player)
		self.player = None

	def addBlock(self, block, tile = None):
		""" lo.addBlock( Block, Tile ) -> None 

		Add a block to the level. (Note that in this and other methods, the location is stored by the
		object itself.)
		"""
		if tile != None:
			tile.block = block
		self.addEntity(block)

	def addLevelObjects(self, room_coords, level_objects):
		""" lo.addLevelObjects( ( int, int ), LevelObjects ) -> None

		Calculate the offset of the given level objects (with rooms as the units)
		and add all of the level objects to this set of LevelObjects with that offset.
		This is generally done if there is a saved set of level objects to be placed into
		a level when it's generated.
		"""
		if self.tiles == None:
			self.tiles = []
		if self.entities == None:
			self.entities = []
		level = self.level
		x_offset = room_coords[0] - level.origin[0]	#this didn't work. need to test new version before deleting, though.
		y_offset = room_coords[1] - level.origin[1]
		for e in level_objects.entities:
			self.entities.append(e)
			entity_x_offset = ROOM_WIDTH*x_offset
			entity_y_offset = ROOM_HEIGHT*y_offset
			if(entity_x_offset != 0 or entity_y_offset != 0):
				e.moveRect(entity_x_offset*32, entity_y_offset*32)
			e.current_level = level
		for row in level_objects.tiles:
			for t in row:
				self.addTile(t, x_offset, y_offset)

	def addEntity(self, entity):
		""" lo.addEntity( Entity ) -> None

		Add an entity to the entity list.
		"""
		self.entities.append(entity)
		entity.current_level = self.level

	def addTile(self, tile, x_offset, y_offset):
		""" lo.addTile( Tile, int, int ) -> None

		Add a tile to the level objects, increasing the size of the 2D
		list to accomodate it if necessary.
		"""
		level = self.level
		new_x = tile.coordinates()[0] + ROOM_WIDTH*x_offset
		new_y = tile.coordinates()[1] + ROOM_HEIGHT*y_offset
		while len(self.tiles) <= new_y:
			self.tiles.append([])
		while len(self.tiles[new_y]) <= new_x:
			self.tiles[new_y].append(None)
		self.tiles[new_y][new_x] = tile
		tile.current_level = level
		tile.moveRect(new_x*32, new_y*32, True)