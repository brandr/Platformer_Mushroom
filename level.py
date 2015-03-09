""" A set of tiles and entities that are active as long as the player is on the level.
"""

from dungeonfactory import build_dungeon
from camera import Camera
from tilefactory import TileFactory
from gameimage import GameImage
from effect import Effect

from nonplayercharacter import NonPlayerCharacter
from levelobjects import LevelObjects
from entity import Entity
from cutscenetrigger import CutsceneTrigger
from pickup import Pickup
from platform import Platform, DestructiblePlatform, PassablePlatform
from ladder import Ladder
from sign import Sign
from door import Door
from monster import Monster
from nonplayercharacter import NonPlayerCharacter
from lantern import Lantern
from chest import Chest
from exitblock import ExitBlock
from spikes import Spikes

from camera import WIN_WIDTH, WIN_HEIGHT
from roomdata import ROOM_WIDTH, ROOM_HEIGHT
from cutscenescripts import ACTOR_GROUP_MAP
from gameimage import DEFAULT_COLORKEY
from lantern import DEFAULT_MODE, MEMORY_MODE
from block import EXPLORED_GREY

import pygame
from pygame import Surface, Color
from pygame.font import Font

import math
import thread
from multiprocessing import Process

from numpy import array

BLACK = Color ("#000000")

MAX_LIGHT_RINGS = 20
RING_INNER = "ring_inner"
RING_OUTER = "ring_outer"

LANTERN_BAR_MIN_WIDTH = 128
LANTERN_BAR_MAX_WIDTH = 300

DUNGEON_NAME_MAP = {
	"Cave_test":"Caves of Mystery"
}

class Level(object):
	""" Level( Dungeon, LevelData, ( int, int ), [ [ Room ] ] ) -> Level

	A level's contents are stored in its associated LevelObjects. Most of the action in the level 
	is related to the player and objects he sees/interacts with, though visual effects and cutscenes
	are also processed by the level.

	Attributes:

	screen: a pygame surface representing the entire screen used for the game. The level draws visible objects
	onto this screen.

	screen_manager: an object that handles the current gamescreen as well as its associated control scheme.

	effect_layer: a list of Effect objects to be displayed onscreen. Usually empty during gameplay, since EntityEffects 
	are preferred for visual effects that are associated with specific entities outside of cutscenes.

	has_effects: indicates whether any visual effects should be displayed. This might be redundant given that the check
	if(effect_layer) would probably achieve the same thing, but I'm not positive because I forget how effects work.

	current_event: a GameEvent (such as a cutscene or dialog) that must complete before gameplay will resume.
	These should be used sparingly.

	active: lets the level know whether entities should be moving around and taking actions.

	bg: a black square used as a background to make transparency work properly.

	dungeon: the larger dungeon containing this level.

	level_ID: a currently unused string that uniquely identifies the level.

	origin: the global coords of the upper-left corner of the level (a room is 1 unit by 1 unit).

	level_objects: a wrapper for all objects (tiles and entities) contained in the level.

	start_coords: coordinates where the player appears upon entering the level, if applicable.
	This is subject to change if I implement travel between dungeons or saving the game.

	width, height: dimensions of the level in tiles.

	level_camera: an object which displays a rectangular section of the level onscreen, staying centered on the player.

	outdoors: flags whether sunlight fills the level.

	current_light_map: a 2D list of floating point values from 0-256 representing the light level of each tile.

	explored: a 2D list of booleans representing the room-sized areas in this level that the player has been to so far.
	"""
	#a level is built from a rectangular set of rooms.
	#it copies all objects from the rooms into itself, and processes these objects as the game is running.
	#only the player's current level should be active at any given time
	def __init__(self, dungeon, level_data, origin, rooms):
		
		self.screen = None
		self.screen_manager = None
		self.effect_layer = []
		self.has_effects = False
		self.current_event = None
		self.active = True
		self.bg = Surface((32, 32))

		self.dungeon = dungeon 					# the Dungeon that the level is part of
		self.level_ID = level_data.name 		# a currently unused value which identifies the level uniquely
		self.origin = origin 					# upper-left corner of the level (in terms of global coords, so each coordinate pair corresponds to a room)
		self.level_objects = LevelObjects(self) # all objects in the level (tiles and entities)
		self.start_coords = None 				# coords where the player appears upon entering the level (set by addRooms)
		self.dungeon_travel_data = level_data.travel_data
		self.adjacent_dungeon = None #not sure if I'll use this yet
		self.addRooms(rooms)

		tiles = self.getTiles()
		self.width = len(tiles[0])
		self.height = len(tiles)
		total_level_width = self.width*32
		total_level_height = self.height*32
		self.level_camera = Camera(total_level_width, total_level_height) #might not be the best way to make the camera
		self.outdoors = level_data.sunlit
		self.concentric_circle_map = None
		if(not self.outdoors): self.concentric_circle_map = self.load_concentric_circles()
		if(self.outdoors): self.setTilesOutdoors() #TEMP
		self.init_bg(level_data.bg_filename)
		self.calibrateLighting()
		self.init_explored()
		self.tile_array = array(self.level_objects.tiles)
		self.player_dead_counter = 0


	def initialize_screen(self, screen_manager, game_screen):
		""" l.initialize_screen( ScreenManager, GameScreen ) -> None

		Associate this level with the given screen_manager and game_screen.
		"""
		self.screen_manager = screen_manager
		self.screen = game_screen.screen_image

	def init_blocks(self): #applies only to special blocks, like doors
		#TEMP. No docstring until we're sure about how this works.
		doors = self.level_objects.get_entities(Door)
		for d in doors:
			d.fill_tiles(self.getTiles())

		#toString test methods
	def to_string(self): #will only be used for testing, I  think. Therefore, no doctring.
		level_string = ""
		tiles = self.getTiles()
		for row in tiles:
			for t in row:
				if t.block != None:
					level_string += "P"
				else:
					level_string += " "
			level_string += "\n"
		return level_string

	def entities_to_string(self): # for testing. No docstring.
		dimensions = self.get_dimensions()
		entities_string_array = []
		while(len(entities_string_array) <= dimensions[1]):
			entities_string_array.append([])
		for s in entities_string_array:
			while len(s) <= dimensions[0]:
				s.append(" ")
		entities = self.getEntities()
		for e in entities:
			coords = (e.rect.left/32, e.rect.right/32)
			entities_string_array[coords[1]][coords[0]] = "E"
		entities_string = ""
		for y in range(0, dimensions[1]):
			for x in range(0, dimensions[0]):
				entities_string += entities_string_array[y][x]
			entities_string += "\n"
		return entities_string

	def respawn_player(self):
		""" l.respawn_player( ) -> None

		Add the player back to the level.
		"""
		# TODO: set the player's location first
		player = self.getPlayer()
		player.moveRect(self.start_coords[0], self.start_coords[1], True)
		player.dead = False

		# TEMP METHOD. No docstring.
	def setTilesOutdoors(self):
		default_sky_tile = GameImage.load_image_file('./images', 'test_sky_tile_1.bmp') #GameImage.loadImageFile('test_sky_tile_1.bmp') 
		dimensions =  self.get_dimensions()
		tiles = self.getTiles()
		for y in xrange(dimensions[1]):
			for x in xrange(dimensions[0]):
				tiles[y][x].changeImage(default_sky_tile)
		# TEMP METHOD

		#level building methods (called in constructor)
	def addRooms(self, rooms):
		""" l.addRooms( [ [ Room ] ] ) -> None

		Fill the level with the given rooms, placing the rooms' contents into the level.
		"""
		if rooms == None: return
		for r in rooms:
			if r == None: continue
			level_objects = r.level_objects
			self.level_objects.addLevelObjects(r.global_coords, level_objects)
			self.setStartCoords(r)
		self.init_blocks()

	def init_bg(self, filename):
		""" l.init_bg( str ) -> None

		Set all the tiles' images based on the image file loaded via the filename.
		"""
		if filename == None: return
		background_image = GameImage.load_image_file("./backgrounds", filename)
		factory = TileFactory(background_image, (self.width, self.height))
		tiles = self.getTiles()
		for y in range(len(tiles)):
			for x in range(len(tiles[y])):
				tile_image = factory.image_at( (x, y) )
				tiles[y][x].changeImage(tile_image)

	def setStartCoords(self, room):
		""" l.setStartCoords( Room ) -> None

		Set the coordinates where the player will start the game.
		"""
		if self.start_coords != None: return
		if room.start_coords[0]:
			x_offset, y_offset = room.global_coords[0] - self.origin[0], room.global_coords[1] - self.origin[1]
			self.start_coords = (room.start_coords[1] + x_offset*ROOM_WIDTH*32, room.start_coords[2] + y_offset*ROOM_HEIGHT*32)

	#outdoor-related methods
	def outdoors(self):
		#unused. Therefore, no docstring.
		if(self.global_coords[1] > 0): return False
		tiles = self.getTiles()
		width = len(tiles[0])
		blocked = 0
		for t in tiles[0]:
			if (t.block != None): #should really be transparency check
				blocked += 1
		return blocked < width/1.5

	def	calibrateLighting(self):
		""" l.calibrateLighting( ) -> None 

		Update the image of every tile in the level. I forget what happens if this isn't called,
		so it might be obsolete.
		"""
		if(self.outdoors): #TODO: separate this into its own method
			tiles = self.getTiles()
			for row in tiles:
				for t in row:
					t.changeImage()
					t.updateimage(256)
			return
		tiles = self.getTiles()
		for row in tiles:
			for t in row:
				t.updateimage(256)
		
	def calibrateExits(self):
		""" l.calibrateExits( ) -> None

		If any exits to the level don't lead anywhere, add blocks barring the player from leaving.
		"""
		tiles = self.getTiles()
		x_tiles = len(tiles[0]) - 1
		y_tiles = len(tiles) - 1
		exit_tiles = []

		for t in tiles[0]: #ceiling
			if(t.passable()):
				exit_tiles.append((t, (0, -1)))
		for t in tiles[y_tiles]: #floor
			if(t.passable()):
				exit_tiles.append((t, (0, 1)))
		for row in tiles: #walls
			if(row[0].passable()): #left wall
				exit_tiles.append((row[0], (-1, 0)))
			if(row[x_tiles].passable()): #right wall
				exit_tiles.append((row[x_tiles], (1, 0)))
		for e in exit_tiles:
			tile = e[0]
			direction = e[1]
			x = tile.coordinates()[0]
			y = tile.coordinates()[1]
			if self.next_level_exists(self.global_coords((x, y)), direction):
				continue
			exit_platform_image = GameImage.load_image_file('./data/', 'exitblock1.bmp') #TODO: make exitblocks more terrifying in case anyone finds them
			exit_platform = GameImage.still_animation_set(exit_platform_image) #TEMPORARY
			block_x = 32*(x + direction[0])
			block_y = 32*(y + direction[1])
			self.level_objects.addBlock(Platform(exit_platform, block_x, block_y))

	#NOTE: if levels take too long to load, try moving this to the dungeon init so that it only has to be done once when the dungeon is loaded.
	#NOTE: get rid of this if the other way solves the lag.
	def load_light_rings(self):
		""" l.load_light_rings( ) -> [ str: { str:Surface } ]

		Loads an array of dicts mapping string constants to light ring images.
		These images are used to light the area around the player if the level is dark.
		"""
		ring_map = []
		for i in range(1, MAX_LIGHT_RINGS):
			next_map = {}
			inner_ring = pygame.image.load("./light_rings/inner_ring_" + str(i) + ".bmp")
			outer_ring = pygame.image.load("./light_rings/outer_ring_" + str(i) + ".bmp")
			inner_ring.set_colorkey(DEFAULT_COLORKEY)
			outer_ring.set_colorkey(DEFAULT_COLORKEY)
			inner_ring.convert()
			outer_ring.convert()
			next_map[ RING_INNER ] = inner_ring
			next_map[ RING_OUTER ] = outer_ring
			ring_map.append(next_map)
		return ring_map

	def load_concentric_circles(self):
		""" TODO: docstring if this actually works and fixes the lag.
		"""
		concentric_circle_map = []
		for i in range(1, MAX_LIGHT_RINGS):
			image = pygame.image.load("./concentric_circles/concentric_circle_" + str(i) + ".png")
			image.convert_alpha()
			image.convert()
			concentric_circle_map.append(image)
		return concentric_circle_map

	def init_explored(self):
		""" l.init_explored( ) -> None 

		Set up the "explored" list tracking which rooms in the level the player has been to.
		"""
		self.explored = []
		width, height = self.room_width(), self.room_height()
		for y in xrange(height):
			self.explored.append([])
			for x in xrange(width):
				self.explored[y].append(False)

	def update_explored(self):
		""" l.update_explored( ) -> None

		Update the explored list if the player has been to a new room.
		"""
		player = self.getPlayer()
		if not player: return
		coords = player.coordinates()
		room_x, room_y = coords[0]/ROOM_WIDTH, coords[1]/ROOM_HEIGHT
		if room_y < len(self.explored) and room_x < len(self.explored[0]):
			self.explored[room_y][room_x] = True #may or may not need checks

	def is_explored(self):
		""" l.is_explored( ) -> bool 

		Checks whether any of the rooms in this level have been explored.
		"""
		width, height = self.room_width(), self.room_height()
		for row in self.explored:
			for col in row:
				if col: return True		
		return False 

	def explored_at(self, x, y):
		""" l.explored_at( int, int ) -> bool
		
		Checks whether the level has been explored at the relative room coords given.
		Example: 0, 0 is the upper-left room-sized area of the level.
		"""
		return self.explored[y][x]
		
		#directonal/movement methods

	def level_in_direction(self, global_x, global_y, direction): #
		""" l.level_in_direction( int, int, ( int, int ) ) -> Level

		Returns the level that is in the given direction from the given global coordinates in this level's associated dungeon.
		Doesn't really need anything from this level in particular, but this method works here for now.
		"""
		x_coord = global_x + direction[0]
		y_coord = global_y + direction[1]
		return self.dungeon.level_at(x_coord, y_coord)

	def direction_of(self, coords):
		""" l.direction_of( int, int ) -> ( int, int )

		Find the direction of the level a tile is in, assuming that it is outside this level's borders.
		"""
		dimensions = self.get_dimensions()
		if(coords[0] <= 1): return (-1, 0)
		if(coords[0] >= dimensions[0] - 1): return (1, 0)
		if(coords[1] <= 1): return (0, -1)
		if(coords[1] >= dimensions[1] - 1): return (0, 1)
		return (0, 0)

	def global_coords(self, position):
		""" l.global_coords( ( int, int ) ) -> ( int, int )

		Takes a level-oriented pair of coordinates and translates it into a dungeon-oriented pair of coordinates.
		Units are rooms.
		"""
		min_x = self.origin[0]
		min_y = self.origin[1]
		x_offset = position[0]/ROOM_WIDTH
		y_offset = position[1]/ROOM_HEIGHT
		return (min_x + x_offset, min_y + y_offset)

	def room_width(self): 
		""" l.room_width( ) -> int

		gives the width of thihs level in rooms.
		"""
		return self.width/ROOM_WIDTH

	def room_height(self):
		""" l.room_height( ) -> int

		gives the height of thihs level in rooms.
		"""
		return self.height/ROOM_HEIGHT

	def flipped_coords(self, global_coords, local_coords):
		""" l.flipped_coords( ( int, int ), ( int, int ) ) -> ( int, int )

		Takes a pair of global_coords (representing the player's current room's location in the dungeon)
		and a pair of local_coords (representing the player's location in this this level, in tiles)
		and returns the coordinates the player should appear on when it levaes this level and travels to
		the adjacent one.
		"""

		dimensions = self.get_dimensions()
		origin_x = self.origin[0]
		origin_y = self.origin[1]
		room_offset_x = global_coords[0] - origin_x
		room_offset_y = global_coords[1] - origin_y

		if(local_coords[0] <= 1):				# left edge of level
			return (dimensions[0] - 1, local_coords[1] + ROOM_HEIGHT*room_offset_y)		
		if(local_coords[0] >= ROOM_WIDTH - 1):	# right edge of level
			return (1, local_coords[1] + ROOM_HEIGHT*room_offset_y)
		if(local_coords[1] <= 1):				# top edge of level
			return (local_coords[0] + ROOM_WIDTH*room_offset_x, dimensions[1] - 1)
		if(local_coords[1] >= ROOM_HEIGHT - 1):	# bottom edge of level
			return (local_coords[0] + ROOM_WIDTH*room_offset_x, 1)
		#TODO: error case (no possible edge detected for exitblock)

	def next_level_exists(self, global_coords, direction):
		""" l.next_level_exists( ( int, int ), ( int, int ) ) -> bool

		Check whether a level exists in the given direction from the given room coords.
		"""
		next_level = self.level_in_direction(global_coords[0], global_coords[1], direction)
		return next_level != None

	def next_dungeon_exists(self, direction):
		""" l.next_dungeon_exists( (int, int ) ) -> bool

		Check whether another dungeon exists in the given direction.
		"""

		if not(self.dungeon_travel_data and self.adjacent_dungeon): return False
		if not(self.dungeon_travel_data[0] and self.dungeon_travel_data[1] and self.dungeon_travel_data[2]): return False
		direction_map = { "Up" : (0, -1) , "Down" : (0, 1) , "Left" : (-1, 0) , "Right" : (1, 0) }
		return self.dungeon_travel_data[2] in direction_map and direction_map[self.dungeon_travel_data[2]] == direction and self.adjacent_dungeon.contains_level(self.dungeon_travel_data[1])

	def move_player(self, coords):
		""" l.move_player( ( int, int ) ) -> None

		Takes a pair of tile coords and figures out where the player should go based on the side 
		and location the player leaves the level from.
		"""
		player = self.getPlayer()
		direction = self.direction_of(coords)
		adjusted_coords = (coords[0] - direction[0], coords[1] - direction[1])
		pixel_remainder = player.pixel_remainder()
		self.removePlayer()
		global_coords = self.global_coords(adjusted_coords)	#these represent the room coords the player is curretly at.
		if(self.next_level_exists(global_coords, direction)):
			next_level = self.level_in_direction(global_coords[0], global_coords[1], direction)
			self.dungeon.move_player(self.screen_manager, self.screen, player, next_level, global_coords, adjusted_coords, pixel_remainder)
			while not player.current_tile():
				player.rect.left += direction[0]
				player.rect.top += direction[1]
		player.current_level.update_explored()

	def move_player_dungeon(self, coords):
		""" l.move_player_dungeon( ( int, int ) ) -> None

		Takes a pair of tile coords and figures out where (in another dungeon) the player should go based on the side 
		and location the player leaves the level from.
		"""
		player = self.getPlayer()
		direction = self.direction_of(coords)
		adjusted_coords = (coords[0] - direction[0], coords[1] - direction[1])
		pixel_remainder = player.pixel_remainder()
		next_level = self.adjacent_dungeon.find_level_by_name(self.dungeon_travel_data[1])
		self.removePlayer()
		self.adjacent_dungeon.add_player(self.screen_manager, self.screen, player, next_level, adjusted_coords, pixel_remainder)

	def addPlayer(self, player, coords = None, pixel_remainder = (0, 0)):
		""" l.addPlayer( Player, ( int, int ) ) -> None

		Add the given player to the level at the given tile coordinates.
		"""
		player.current_level = self
		self.level_objects.addPlayer(player)
		if self.dungeon_travel_data: self.begin_loading_adjacent_dungeon(self.dungeon_travel_data)
		if(coords == None):	
			player.moveRect(self.start_coords[0], self.start_coords[1], True)
			self.update_explored()
			return
		player.moveTo(coords)
		player.moveRect(pixel_remainder[0], pixel_remainder[1])
		self.level_camera.update(player)
		player.update(self.getTiles(), self.empty_light_map())
		player.refresh_animation_set()

	def begin_loading_adjacent_dungeon(self, travel_data):
		""" l.begin_loading_adjacent_dungeon( ( str, str, str ) ) -> None

		Starts loading the dungeon that the player can travel to by leaving this level.
		"""
		if self.adjacent_dungeon: return
		dungeon_name, level_name, direction = travel_data[0], travel_data[1], travel_data[2]
		if not(dungeon_name and level_name and direction): return
		dungeon_directory = "./dungeon_map_files/" #TODO: store this somewhere more central in case it gets changed
		thread.start_new_thread( Level.load_adjacent_dungeon, (self, dungeon_directory, dungeon_name, ) )
		#p = Process( target = Level.load_adjacent_dungeon, args = ( self, dungeon_directory, dungeon_name,  ) )
		#IDEA: could also start a thread for the level in the correpsonding dungeon to map to this one

	def load_adjacent_dungeon(self, dungeon_directory, dungeon_name):
		""" l.load_adjacent_dungeon ( str, str ) -> None

		Sets this level's adjacent dungeon, building it if necessary.
		"""
		dungeon_display_name = dungeon_name
		if dungeon_name in DUNGEON_NAME_MAP:
			dungeon_display_name = DUNGEON_NAME_MAP[dungeon_name]
		adjacent_dungeon = build_dungeon(dungeon_directory + dungeon_name, dungeon_display_name)
		adjacent_dungeon.connect_to_level(self, self.dungeon)
		self.adjacent_dungeon = adjacent_dungeon

	# pausing/events/other thing that change screen and controls
	def pause_game(self, player):
		""" l.pause_game( Player ) -> None 

		Pauses the game and goes to the map screen.
		This is subject to change as the pause screen gets fleshed out further.
		"""
		self.set_active(False)	

	def unpause_game(self, player):
		""" l.unpause_game( Player ) -> None

		Resumes the game.
		"""
		self.set_active(True)
		self.screen_manager.switch_to_main_screen(player)

	def activate_actors(self):
		""" l.activate_actors( ) -> None

		Sets the player, all NPCs and monsters to "active", making them perform physics and AI checks at each tick.
		"""
		self.getPlayer().activate()
		for n in self.getNPCs():
			n.set_active(True)
		for m in self.getMonsters():
			m.set_active(True)

	def set_active(self, active):
		""" l.set_active( bool ) -> None

		Either activate or deactivate all actors (Player, NPCs, and monsters) on the level.
		"""
		if active:
			self.activate_actors()
		else:
			self.deactivate_actors()
		self.active = active

	def deactivate_actors(self):	
		""" l.deactivate_actors( ) -> None 

		Sets the player, all NPCs and monsters to "inactive", making them perform only animation at each tick.
		"""
		self.getPlayer().deactivate()	
		for n in self.getNPCs():
			n.set_active(False)
		for m in self.getMonsters():
			m.set_active(False)

	def get_actor(self, actor_group_type, actor_key):
		""" l.get_actor( Class, str ) -> Player/NPC/Sign

		Get an actor on this level using a unique key, along with the actor's class.
		For use during cutscenes.
		"""
		return ACTOR_GETTER_MAP[actor_group_type](self, actor_key)

	def get_NPC_actor(self, NPC_key):
		""" l.get_NPC_actor( str ) -> NonPlayerCharacter

		Gets a nonplayercharacter using its name as a unique key.
		For use during cutscenes.
		"""
		for n in self.getNPCs():
			if n.name == NPC_key: return n

	def begin_cutscene(self, cutscene, instant = False):
		""" l.begin_cutscene( Cutscene, bool ) -> None

		Start playing a cutscene during which the player can't act.
		The "instant" arg determines whether the cutscene bars appear instantaneously
		or slide in from the edges of the screen.
		"""
		self.current_event = cutscene
		self.draw_cutscene_bars(instant)
		self.deactivate_actors()
		self.screen_manager.current_screen.control_manager.switch_to_event_controls(cutscene, self.getPlayer()) #TODO: make sure the cutscene can't be cancelled with X like signs.
		cutscene.begin()

	def draw_cutscene_bars(self, instant = True, seconds = 1.5): #TODO: use second arg here, I think (if not, remove them)
		""" l.draw_cutscene_bars( bool, double ) -> None 

		Draw black bars that mark that a cutscene is occurring.
		"""
		bar_width = self.screen.get_width()
		bar_height = self.screen.get_height()/10
		top_bar = Effect(Effect.draw_black_rectangle_top, (bar_width, bar_height), (0, 0), not instant)
		bottom_bar = Effect(Effect.draw_black_rectangle_bottom, (bar_width, bar_height), (0, self.screen.get_height() - bar_height), not instant)
		self.add_effect(top_bar)
		self.add_effect(bottom_bar)

	def begin_event(self, event):
		""" l.begin_event( GameEvent ) -> None 

		Begin an event that occurs separately from normal gameplay, such a cutscene or dialog.
		"""
		self.current_event = event
		self.deactivate_actors()
		self.screen_manager.current_screen.control_manager.switch_to_event_controls(event, self.getPlayer())

	def end_current_event(self):
		""" l.end_current_event( ) -> None 

		End whatever event is currently taking place and return to normal gameplay.
		"""
		self.current_event.end()
		self.current_event = None
		self.end_effects()
		self.screen_manager.current_screen.control_manager.switch_to_main_controls(self.getPlayer())
		self.activate_actors()

	def add_effect(self, effect):
		""" l.add_effect( Effect ) -> None 

		Add a visual effect (such as cutscene bars) that is rendered on the topmost layer, even above 
		entity effects and subentities.
		"""
		self.effect_layer.append(effect)
		self.has_effects = True

	def remove_effect(self, effect):
		""" l.remove_effect( Effect ) -> None 

		Remove a visual effect from the screen.
		"""
		if effect in self.effect_layer:
			self.effect_layer.remove(effect)
			if not self.effect_layer:
				self.has_effects = False

	def end_effects(self):
		""" l.end_effects( ) -> None 

		Clear all visual effects from the screen. This must be done in reverse order,
		or else the iteration process will be interrupted by the removals.
		"""
		for e in reversed(self.effect_layer):
			e.end(self)

	def clear_effects(self):
		""" l.clear_effects( ) -> None 

		Empty the effect layer. This will probably be called at the same time as end_effects().
		"""
		self.effect_layer = []
		self.has_effects = False

	def display_dialog(self, dialog):
		""" l.display_dialog( Dialog ) -> None

		Display a dialog containing text from a sign or speaking NPC.
		"""
		self.add_effect(dialog)

#TODO: could put up,down,left,right and running into a single object which describes the player's current state
	def update(self, up, down, left, right, space, running):	
		""" l.update( bool, bool, bool, bool, bool, bool ) -> None 

		The update method does nothing if the level is inactive.
		Otherwise, it starts by updating the current event (if applicable).
		
		Then, it separates out the onscreen tiles from the 2D list (basically a grid) of all its tiles.
		(The onscreen list is used to save time when rendering visible tiles and objects.)

		A 2D list (the light_map) is generated and used to set the light level at each tile to a float value 
		between 0 and 256. This is currently the most efficient method I have found to handle lighting.

		If the player is still on the level at this iteration of the update, the player performs a physical
		update in which things like gravity and collisions are applied.

		At this point, objects in the level are blitted onto the screen in the following order:

		-tiles
		-stationary objects
		-moving non-player objects
		-subentites of non-player objects (not yet implemented)
		-entity effects of non-player objects (not yet implemented)
		-the player 
		-subentites of the player
		-entity effects of the player

		After this, lighting is applied by blitting black squares of varying transparency over the tiles. 
		Finally, visual effects like cutscene bars or dialog boxes are displayed.
		"""
		if(not self.active): return
		if(self.current_event):
			self.current_event.update(self)
			if(self.current_event.is_complete()):
				self.end_current_event()
		dimensions = self.get_dimensions()
		player = self.getPlayer()
		if player.dead:
			self.player_dead_counter -= 1
			if self.player_dead_counter <= 0: self.respawn_player()
		all_tiles = self.level_objects.tiles 
		start_x = max(0, -1*self.level_camera.state.left/32 - 2)			#TODO: get rid of these 32s and replace with some constant.
		end_x = min( self.width, start_x + WIN_WIDTH/32 + 4)
		start_y = max(0, -1*self.level_camera.state.top/32 - 2)
		end_y = min( self.height, start_y + WIN_HEIGHT/32 + 4 )	
		tiles = self.tile_array[start_y:end_y, start_x:end_x]
		light_map = self.empty_light_map()
		if(player != None):
			self.update_explored()
			self.level_camera.update( player )						# try calling this at the end of this method if there are weird visual effects.
			player.update(all_tiles, light_map)
			player_subs = player.active_subentities
			if player_subs:
				for s in player_subs: s.update()
			destructible_platforms = self.getDestructiblePlatforms()
			for dp in destructible_platforms:
				dp.update(player)
			display_mode = self.display_mode( player )
			display_method = DISPLAY_MODE_MAP[display_mode]
			display_method( self, tiles, player )
			pygame.display.update()

	def display_outdoors(self, tiles, player):
		""" l.display_outdoors( [ [ Tile ] ], Player ) -> None

		Display method for sunlit levels.
		"""
		self.draw_level_contents(tiles, player)
		if (player.invincibility_frames % 2) == 0 and not player.dead: self.screen.blit(player.image, self.level_camera.apply(player))
		self.display_passable_blocks()
		if not self.current_event:
			self.update_player_hud(player) 
		if(self.has_effects): 
			self.update_effects()

	def display_dark(self, tiles, player):
		""" l.display_dark( [ [ Tile ] ], Player ) -> None

		Display method for dark levels when the player has a lit lantern.
		"""
		self.draw_level_contents( tiles, player, True )
		light_map = self.empty_light_map( )
		if (player.invincibility_frames % 2) == 0: self.screen.blit(player.image, self.level_camera.apply(player))
		self.display_passable_blocks()
		if light_map: self.update_light(light_map)	
		if not self.current_event:
			self.update_player_hud(player) 
		if(self.has_effects): 
			self.update_effects()
		
	def display_full_dark(self, tiles, player):
		""" l.display_full_dark( [ [ Tile ] ], Player ) -> None

		Display method for complete darkness. This is similar to display_outdoors,
		except that nothing is drawn but the player.
		"""
		if (player.invincibility_frames % 2) == 0: self.screen.blit(player.image, self.level_camera.apply(player))
		if not self.current_event:
			self.update_player_hud(player) 
		if(self.has_effects): 
			self.update_effects()

	def display_memory(self, tiles, player):
		""" l.display_memory( [ [ Tile ] ], Player ) -> None

		Display method for when the player is using the lantern's memory mode.
		"""
		explored = Surface((32, 32))
		explored.fill(EXPLORED_GREY)
		explored.convert()
		dimensions = self.get_dimensions()
		origin_x, origin_y = self.level_camera.origin()
		for y in xrange(dimensions[1]):
			for x in xrange(dimensions[0]):
				grey_flag = False
				x1 = x*32 + origin_x
				y1 = y*32 + origin_y
				x_check = x1 >= -32 and x1 < WIN_WIDTH + 32 
				y_check = y1 >= -32 and y1 < WIN_HEIGHT + 32 
				if x_check and y_check:
					check_tile = self.getTiles()[y][x]
					if check_tile.mapped and not check_tile.passable():
						if check_tile.block and check_tile.block.is_sloped:
							self.screen.blit(check_tile.block.unseen_image, (x1, y1))
						else:
							self.screen.blit(explored, (x1, y1))
		self.screen.blit(player.image, self.level_camera.apply(player)) #TODO: make this a grey silhouette of the player
		if not self.current_event:
			self.update_player_hud(player) 

	def draw_level_contents(self, tiles, player, dark = False):
		""" l.draw_level_contents( [ [  Tile ] ], Player ) -> None

		Draw the level's tiles, platforms, chests, doors, etc. along with moving entities like monsters and the player.
		"""
		# if it's dark, don't blit tiles that are too far from the player. otherswise, blit every tile onscreen.
		if dark:
			lantern = player.get_lantern()
			if lantern:
				radius = lantern.light_distance()
				width = len(tiles[0])
				height = len(tiles)
				player_x, player_y = player.rect.center
				start_x, start_y = min( width, max( 0, player_x/32 - radius ) ), min( height, max ( 0, player_y/32 - radius ) )
				end_x, end_y = min( width, max( 0, player_x/32 + radius + 1 ) ), min( height, max ( 0, player_y/32 + radius + 1 ) )
				for y in range(  start_y , end_y ):
					for x in range ( start_x, end_x ):
						t = tiles[y][x]
						self.screen.blit(t.image, self.level_camera.apply(t))
		else:
			for row in tiles:
				for t in row:
					self.screen.blit(t.image, self.level_camera.apply(t))

		# stationary update
		# no need to blit all platforms, since this is already handled by tiles.
		for dp in self.getDestructiblePlatforms():
			self.screen.blit(dp.image, self.level_camera.apply(dp))
		for p in self.getPlatforms():
			if p.is_sloped:
				self.screen.blit(p.image, self.level_camera.apply(p))
		for l in self.getLadders():
			self.screen.blit(l.image, self.level_camera.apply(l))
		for s in self.getSigns():
			self.screen.blit(s.image, self.level_camera.apply(s))
		for c in self.getChests():
			self.screen.blit(c.image, self.level_camera.apply(c))
		for d in self.getDoors():
			self.screen.blit(d.image, self.level_camera.apply(d))
		for s in self.getSpikes():
			self.screen.blit(s.image, self.level_camera.apply(s))

		# non-stationary update
		for l in self.getLanterns():
			self.screen.blit(l.image, self.level_camera.apply(l))
		for n in self.getNPCs():
			self.screen.blit(n.image, self.level_camera.apply(n))
		for m in self.getMonsters():
			self.screen.blit(m.image, self.level_camera.apply(m))

		# TODO: blit subentites and then entity effects of non-player objects starting here
		for m in self.getMonsters():
			monster_subs = m.active_subentities
			if monster_subs:
				for s in monster_subs:
					s.update()
					if s.active:
						self.screen.blit(s.image, self.level_camera.apply(s))
			monster_effects = player.entity_effects
			if monster_effects:
				for e in monster_effects:
					e.update()
					self.screen.blit(e.image, self.level_camera.apply(e))	
			# ...and ending here

		player_subs = player.active_subentities
		if player_subs:
			for s in player_subs:
				if s.active:
					self.screen.blit(s.image, self.level_camera.apply(s))	
		player_effects = player.entity_effects
		if player_effects:
			for e in player_effects:
				e.update()
				self.screen.blit(e.image, self.level_camera.apply(e))		

	def update_light(self, light_map):
		""" l.update_light( [ [ double ] ] ) -> None 

		Draw concentric circles around the player to light his immediate surroundings.
		"""
		player = self.getPlayer()
		if not player: return
		concentric_circle_map = self.concentric_circle_map
		if not concentric_circle_map: return
		origin_x, origin_y = self.level_camera.origin()
		player_coords = player.center_rect_coords()		
		center_x, center_y = player_coords[0], player_coords[1]
		lantern = player.get_lantern()
		circle_count = max(1, lantern.light_distance() )
		circle_image = concentric_circle_map[circle_count]
		outer_rect = circle_image.get_rect()
		rect_left = center_x + origin_x - outer_rect.width/2
		rect_right = center_x + origin_x + outer_rect.width/2
		rect_top = center_y + origin_y - outer_rect.height/2
		rect_bottom = center_y + origin_y + outer_rect.height/2
		fill_area_data = [ ( 0, 0, WIN_WIDTH, rect_top ), ( 0, rect_bottom, WIN_WIDTH, max( 0, WIN_HEIGHT - rect_bottom ) ),
		( 0, rect_top, rect_left, outer_rect.height ), ( rect_right, rect_top, max( 0, WIN_WIDTH - rect_right ), outer_rect.height ) ]
		for data in fill_area_data:
			x, y, width, height = data[0], data[1], data[2], data[3]
			if( width <= 0 or height <= 0 ): continue
			fill_rect = Surface( ( width, height ) )
			self.screen.blit( fill_rect, ( x, y ) )
		self.screen.blit( circle_image, ( center_x + origin_x - circle_image.get_width()/2, center_y + origin_y - circle_image.get_height()/2) )	# this line is causing the lag

	def display_passable_blocks(self):
		""" l.display_passable_blocks( ) -> None

		Display all blocks the player can pass through.
		"""
		for p in self.getPassablePlatforms():
			self.screen.blit(p.image, self.level_camera.apply(p))	

	def display_mode(self, player):
		""" l.display_mode( Player ) -> str

		Figure out how the level should display the objects it contains.
		"""
		if self.outdoors:
			return DISPLAY_OUTDOORS
		lantern = player.get_lantern()
		if ( not lantern or not lantern.light_distance() ):
			return DISPLAY_FULL_DARK
		return LANTERN_MODE_MAP[lantern.mode]

	def empty_light_map(self):
		""" l.empty_light_map( ) -> [ [ double ] ]

		Creates an empty light map with the same dimensions as the tile list.
		"""
		if self.outdoors: return None
		light_map = []
		dimensions = self.get_dimensions()
		for y in xrange(dimensions[1]):
			light_map.append([])
			for x in xrange(dimensions[0]):
				light_map[y].append(0)
		return light_map

	def update_effects(self):
		""" l.update_effects( ) -> None 

		Display visual effects like cutscene bars and dialog boxes.
		These are usually on the topmost layer.
		"""
		for e in self.effect_layer:
			next_effect, offset = e.draw_image(self)
			self.screen.blit(next_effect, (e.offset[0] + offset[0], e.offset[1] + offset[1]))

	def update_player_hud(self, player):
		""" l.update_player_hud( ) -> None

		Blit visual effects like the player's current health and lantern oil onto the screen.
		"""
		self.update_lantern_mode_display( player )
		self.update_heatlh_display( player )
		self.update_oil_display( player )
		self.update_death_counter( player )
		#TODO: other components of HUD

	def update_lantern_mode_display(self, player):
		""" l.update_lantern_mode_display( Player ) -> None

		Show the current lantern mode the player is using.
		"""
		lantern_mode_image = player.current_lantern_mode_image()
		self.screen.blit( lantern_mode_image, ( 8, 8 ) )

	def update_heatlh_display(self, player):
		""" l.update_heatlh_display( Player ) -> None

		Show the player's current health on the screen.
		"""
		hp = player.hit_points
		current_hp, max_hp = hp[0], hp[1]
		hp_bar_start_empty, hp_bar_middle_empty, hp_bar_end_empty, hp_bar_start_filled, hp_bar_middle_filled, hp_bar_end_filled = player.load_hp_bar_images()
		if current_hp == 0:
			self.screen.blit( hp_bar_start_empty, ( 72, 8 ) )
		else:
			self.screen.blit( hp_bar_start_filled, ( 72, 8 ) )
		for i in xrange( 1, min( current_hp, max_hp - 1) ):
			self.screen.blit( hp_bar_middle_filled, ( 72 + 32*i, 8 ) )
		for i in xrange( current_hp, max_hp - 1 ):
			self.screen.blit( hp_bar_middle_empty, ( 72 + 32*i, 8 ) )
		if current_hp == max_hp:
			self.screen.blit( hp_bar_end_filled, ( 72 + 32*( max_hp - 1), 8 ) )
		else:
			self.screen.blit( hp_bar_end_empty, ( 72 + 32*( max_hp - 1), 8 ) )

	def update_oil_display(self, player):
		""" l.update_oil_display( Player ) -> None

		Show the player's current lantern information on the screen.
		"""
		lantern = player.get_lantern( )
		if lantern:
			current_oil, max_oil = lantern.oil_meter[0], lantern.oil_meter[1]
			bar_width = max_oil/40	# can probably determine this other way
			bar_image = Surface( ( bar_width + 4, 32 ) )
			inner_bar_image = Surface( ( bar_width, 28 ) )
			inner_bar_image.fill( Color( "#222222" ) )
			bar_ratio = ( ( float ) ( current_oil ) / ( float ) ( max_oil ) )
			filled_width = bar_ratio*bar_width
			filled_bar_image = Surface( ( filled_width, 28 ) )
			filled_bar_image.fill( Color( "#FFFF00" ) )
			inner_bar_image.blit( filled_bar_image, ( 0, 0 ) )
			bar_image.blit( inner_bar_image, ( 2, 2 ) )
			self.screen.blit( bar_image, ( 72, 40 ) )

	def update_death_counter(self, player):
		""" TODO
		"""
		text_font = Font("./fonts/FreeSansBold.ttf", 20)
		death_count_text = "You have died " + str(player.death_count) + " times. :^)"
		text_image = text_font.render(death_count_text, 1, BLACK)
		self.screen.blit(text_image, ( 520, 16 ))

	def level_end_coords(self):
		""" l.level_end_coords( ) -> ( int, int )

		Returns the coordinates of the lower-right of the level, with rooms as the units.
		"""
		tiles = self.getTiles()
		width  = len(tiles[0]) - 1
		height = len(tiles) - 1
		len(tiles) - 1
		return (self.origin[0] + (width/ROOM_WIDTH), self.origin[1] + (height/ROOM_HEIGHT))

	def get_dimensions(self):
		""" l.get_dimensions( ) -> ( int, int )

		Returns the width and height of the level in tile units.
		"""
		tiles = self.getTiles()
		width  = len(tiles[0])
		height = len(tiles)
		return (width, height)

	def player_interactables(self):
		""" l.player_interactables( ) -> [ Entity ]

		Returns the set of all entities the player can interact with, not including blocks.
		"""
		interactables = []
		for m in self.getMonsters(): interactables.append(m)
		for n in self.getNPCs(): interactables.append(n)
		for t in self.getTriggers(): interactables.append(t)
		for s in self.getSpikes(): interactables.append(s)
		return interactables
		#TODO: other objects that should update based on the player

	def x_interactable_objects(self):
		""" l.x_interactable_objects( ) -> [ Entity ]

		Returns all objects the player can interact with by pressing X.
		"""
		x_interactables = []
		for e in self.getEntities():
			if e.x_interactable:
				x_interactables.append(e)
		return x_interactables

	def get_impassables(self):
		""" l.get_impassables( ) -> [ Block ]

		Returns all solid objects that block the player's movement.
		"""
		impassables = self.getPlatforms()
		doors = self.level_objects.get_entities(Door)
		for d in doors:
			if not d.open:
				impassables.append(d)
		return impassables

	def remove(self, entity):
		""" l.remove( Entity ) -> None 

		Remove an entity from the level.
		"""
		self.level_objects.remove(entity)
		if(self.outdoors): self.calibrateLighting()

	def remove_block(self, block):
		""" l.remove( Block ) -> None

		Remove a block from the level.
		"""
		tile = block.current_tile()
		self.remove(block)
		tile.reset()

	def getTilesOnScreen(self):
		""" l.getTilesOnScreen( ) -> [ [ Tile ] ]

		Returns all of the tiles that appear on the screen.
		"""
		all_tiles = self.getTiles()
		return self.level_camera.on_screen_tiles(all_tiles)

	def removePlayer(self):
		""" l.removePlayer( ) -> None

		The player is removed from the level.
		This is called when the player leaves the level off the edge of the screen.
		"""
		self.level_objects.removePlayer()

	def getPlayer(self):
		""" l.getPlayer( ) -> Player 

		Returns the player.
		"""
		return self.level_objects.player

	def getTiles(self):
		""" l.getTiles( ) -> [ [ Tile ] ]

		Returns a 2D list of the level's tiles.
		"""
		return self.level_objects.tiles

	def tile_at(self, x, y):
		""" l.tile_at( int, int ) -> Tile

		Returns the tile at the given coordinates.
		"""
		tiles = self.getTiles()
		if 0 <= y and y < len(tiles):
			if 0 <= x and x < len(tiles[y]):
				return tiles[y][x]

	def getEntities(self):
		""" l.getEntities( ) -> [ Entity ]

		Returns all entities in the level.
		"""
		return self.level_objects.get_entities(Entity)

	def getTriggers(self):
		""" l.getTriggers( ) -> [?]

		Returns all triggers in the level.
		Currently, only cutscene triggers exist and there is no superclass.
		This is because these may end up being the only trigger types that exist.
		"""
		return self.level_objects.get_entities(CutsceneTrigger)

	def getPickups(self):
		""" l.getPickups( ) -> [ Pickup ]

		Returns all pickups in the level.
		"""
		return self.level_objects.get_entities(Pickup)
		
	def getPlatforms(self):
		""" l.getPlatforms( ) -> [ Platform ]

		Returns all platforms in the level.
		"""
		return self.level_objects.get_entities(Platform)

	def getDestructiblePlatforms(self):
		""" l.getDestructiblePlatforms( ) -> [ DestructiblePlatform ]

		Returns all destructible platforms in the level.
		"""
		return self.level_objects.get_entities(DestructiblePlatform)

	def getPassablePlatforms(self):
		""" l.getPassablePlatforms( ) -> [ getPassablePlatforms ]

		Returns all passable platforms in the level.
		"""
		return self.level_objects.get_entities(PassablePlatform)

	def getLadders(self):
		""" l.getLadders( ) -> [ Ladder ]

		Returns all ladders in the level.
		"""
		return self.level_objects.get_entities(Ladder)

	def getSigns(self):
		""" l.getSigns( ) -> [ Sign ]

		Returns all signs in the level.
		"""
		return self.level_objects.get_entities(Sign)

	def getDoors(self):
		""" l.getDoors( ) -> [ Door ]

		Returns all doors in the level.
		"""
		return self.level_objects.get_entities(Door)
		
	def getMonsters(self):
		""" l.getMonsters( ) -> [ Monster ]

		Returns all monsters in the level.
		"""
		return self.level_objects.get_entities(Monster)

	def getNPCs(self):
		""" l.getNPCs( ) -> [ NonPlayerCharacter ]

		Returns all NonPlayerCharacters in the level.
		"""
		return self.level_objects.get_entities(NonPlayerCharacter)

	def getLanterns(self):
		""" l.getLanterns( ) -> [ Lantern ]

		Returns all lanterns in the level.
		"""
		return self.level_objects.get_entities(Lantern)

	def getChests(self):
		""" l.getChests( ) -> [ Chest ]

		Returns all chests in the level.
		"""
		return self.level_objects.get_entities(Chest)

	def get_exit_blocks(self):
		""" l.get_exit_blocks( ) -> [ ExitBlock ]

		Returns all exitblocks in the level.
		"""
		return self.level_objects.get_entities(ExitBlock)

	def getSpikes(self):
		""" l.getSpikes( ) -> [ getSpikes ]

		Returns all spikes in the level.
		"""
		return self.level_objects.get_entities(Spikes)
	
		
ACTOR_GETTER_MAP = {
	NonPlayerCharacter:Level.get_NPC_actor
}

DISPLAY_OUTDOORS = "display_outdoors"
DISPLAY_DARK = "display_dark"
DISPLAY_FULL_DARK = "display_full_dark"
DISPLAY_MEMORY = "display_memory"

DISPLAY_MODE_MAP = {
	DISPLAY_OUTDOORS:Level.display_outdoors,
	DISPLAY_DARK:Level.display_dark,
	DISPLAY_FULL_DARK:Level.display_full_dark,
	DISPLAY_MEMORY:Level.display_memory
}

LANTERN_MODE_MAP = {
	DEFAULT_MODE:DISPLAY_DARK,
	MEMORY_MODE:DISPLAY_MEMORY
}