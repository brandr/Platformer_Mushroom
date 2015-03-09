""" A factory that creates different kinds of entities, initializing them as appropriate.
"""

#from pickupfactory import *

from ladder import Ladder
from lantern import Lantern
from chest import Chest
from platform import Platform, DestructiblePlatform, PassablePlatform
from monster import Monster
from sign import Sign
from cutscenetrigger import CutsceneTrigger
from block import Block
from door import Door
from spikes import Spikes
from nonplayercharacter import NonPlayerCharacter
from npcfactory import NPCFactory
from tiledata import * 

ENTITY_CONSTRUCTOR_MAP = { #TODO: try to figure out why signs aren't in here
	DEFAULT_PLATFORM:Platform,
	SLOPING_PLATFORM:Platform,
	DESTRUCTIBLE_PLATFORM:DestructiblePlatform,
	PASSABLE_PLATFORM:PassablePlatform,

	DEFAULT_LADDER:Ladder,

	DEFAULT_DOOR:Door,

	DEFAULT_LANTERN:Lantern,
	
	DEFAULT_SPIKES:Spikes,

	BAT:Monster,
	GIANT_FROG:Monster,

	MINER:NonPlayerCharacter,

	DEFAULT_CUTSCENE_TRIGGER:CutsceneTrigger,	#this might not be necessary, but I'm not sure.
	#TEMP
	KENSTAR:NonPlayerCharacter
}

class EntityFactory(object):
	""" No constructor.
	"""
	@staticmethod
	def build_entity(animation_set, entity_key, x, y):
		""" build_entity( AnimationSet, str, int, int ) -> Entity 

		Creates an entity based on a string key connecting it to its constructor
		in the entity constructor map.
		"""
		if entity_key not in ENTITY_CONSTRUCTOR_MAP: return None
		constructor = ENTITY_CONSTRUCTOR_MAP[entity_key]
		entity = constructor(animation_set, x, y)
		if entity_key in ENTITY_BUILD_MAP:		# not sure to what extent the entity build map is used anymore.
			build_function = ENTITY_BUILD_MAP[entity_key]
			build_function(entity, entity_key)
		return entity 					

	#add other monster init stuff as necessary.

	@staticmethod
	def initMonster(monster, name):
		""" initMonster( Monster, str ) -> None

		Initializes the monster using the proper init function, using its name as a key.
		"""
		monster.name = name
		monster.monster_init(name)

	@staticmethod
	def initNPC(npc, name):
		""" initNPC( NonPlayerCharacter, str ) -> None

		Uses an NPCFactory to init the NPC.
		""" 
		NPCFactory.init_NPC(npc, name)

	@staticmethod
	def initSign(sign, sign_key):	
		""" initSign( Sign, str ) -> None

		Uses a SignFactory to init the sign.
		"""
		SignFactory.init_sign(sign, sign_key)

	@staticmethod
	def initSlopingPlatform(platform, arg):
		""" initSlopingPlatform( Platform, None ) -> None 

		Change a platform's flags to indicate that it is sloped and not square.		
		"""
		platform.is_sloped = True
		platform.is_square = False
		platform.is_solid = True 
		platform.draw_memory_image()

ENTITY_BUILD_MAP = {
	SLOPING_PLATFORM:EntityFactory.initSlopingPlatform,
	BAT:EntityFactory.initMonster,
	GIANT_FROG:EntityFactory.initMonster,
	KENSTAR:EntityFactory.initNPC,
	MINER:EntityFactory.initNPC,
	DEFAULT_SIGN:EntityFactory.initSign
}