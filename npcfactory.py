""" A special factory for setting up NPCs.
"""

from nonplayercharacter import *
#NOTE: in the future, this may require saving/loading data
#about NPCs that appear in more than one area.

class NPCFactory:
	""" No constructor.
	"""
	@staticmethod
	def init_NPC(npc, name):
		""" init_NPC( NonPlayerCharacter, str ) -> None

		Temporary method which initializes the NPC's dialog tree and name.
		I'm not sure how I want dialog trees to be stored and assigned to NPCs.
		They shouldn't have to be too complex, so it might be possible to just hardcode them.
		"""
		npc.name = name

		#TEMP FOR TESTING
		temp_dialog_tree_map = MASTER_NPC_DIALOG_MAP[name] 
		# TODO: need to make dialog more extensible later on
		# IDEA: map each NPC by name to a dict of possible dialogs, whose key (or value?) can in turn be changed somehow.
		#TEMP FOR TESTING

		npc.dialog_tree = temp_dialog_tree_map[START] # later on, it might be useful to change START to some value that can change as the game progresses.
		npc.dialog_tree_map = temp_dialog_tree_map

START = "start"
TEST_KENSTAR_TIRED = "test_kenstar_tired"

# for now, test dialog trees go here.

#MINER
TEST_MINER_DIALOG_TREE = (	# TODO: figure out how to store this at a cutscene and parse it properly
	[
		("I am a boss character!", NEUTRAL),
		("I am going to fight you now!", NEUTRAL)
	],
	None #TODO: add some trigger to begin boss battle
)

#KENSTAR
TEST_KENSTAR_START_DIALOG_TREE = (
	[
		("Whaaaaaaaaaaat is this place??", NEUTRAL),
		("It looks like some kind of... demo.", NEUTRAL)
	],
	(
		DIALOG_CHOICE,
		("Do you know the way out of here?", NEUTRAL),
		[ 
			("Yes", 
				[
					("Whoa, really?", NEUTRAL)
				],
				(
					DIALOG_CHOICE,
					("Is it to the right?", NEUTRAL),
					[
						("Yes",
							[
								("Well, then, I'd better get going!", NEUTRAL),
								("...and by that, I mean walk slightly to the right.", NEUTRAL)		
							],
							(
								ACTION_SET,
								[ 
									(	#TODO: make the action work
										NonPlayerCharacter.temp_npc_right_method, 30, None 
									),
									(
										NonPlayerCharacter.temp_stop_method, 0, None 
									)
								],
								(
									ADD_DIALOG_SET,
									[
										("That's enough walking for one day.", NEUTRAL)
									], 
									(
										SETUP_NEXT_DIALOG,
										TEST_KENSTAR_TIRED
									)
								), None
							)
						),
						("No",
							[
								("I don't belive you! I came from that direction!", NEUTRAL)
							], None
						)
					]
				)
			),
			("No", 
				[
					("Well, let me know if you find it.", NEUTRAL)
				], None
			)
		]
	)
)

TEST_KENSTAR_TIRED_DIALOG_TREE = (
	[
		("Boy, I sure am tired.", NEUTRAL)
	], None
)

TEST_KENSTAR_DIALOG_TREE_MAP = {
	START:TEST_KENSTAR_START_DIALOG_TREE,
	TEST_KENSTAR_TIRED:TEST_KENSTAR_TIRED_DIALOG_TREE
}

TEST_MINER_DIALOG_TREE_MAP = {
	START:TEST_MINER_DIALOG_TREE
}

MASTER_NPC_DIALOG_MAP = {
	KENSTAR:TEST_KENSTAR_DIALOG_TREE_MAP,
	MINER:TEST_MINER_DIALOG_TREE_MAP
}