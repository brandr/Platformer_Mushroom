""" An invisible trigger that will cause a cutscene to play if the player comes into contact with it and hasn't seen the cutscene yet.
"""

from block import *
#from cutscenescripts import MASTER_CUTSCENE_MAP, ACTOR_GROUP_MAP, BEGIN_DIALOG_TREE
from cutscenescripts import *
from cutscene import Cutscene
from gameaction import GameAction
from nonplayercharacter import NonPlayerCharacter

class CutsceneTrigger(Block):
	""" CutsceneTrigger( AnimationSet, int, int ) -> CutsceneTrigger

	TODO

	Attributes:

	cutscene_key: A string key uniquely associating this trigger with some cutscene.
	"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.x_interactable = False
		self.is_solid = False
		self.cutscene_key = None

	def update(self, player):
		""" ct.update( Player ) -> None

		Check if the player has collided with this trigger (and not activated the cutscene yet).
		If the cutscene has already been activated, delete this trigger.
		"""
		if player.has_viewed_cutscene(self.cutscene_key):
			self.delete()
			return
		if pygame.sprite.collide_rect(self, player) and self.cutscene_key:
			self.begin_cutscene(player)

	def begin_cutscene(self, player):
		""" ct.begin_cutscene( Player ) -> None

		Build the cutscene associated with this trigger and make the player watch it.
		"""
		# TODO: make this handle cutscenes that contain more complex/multiple actions, too.
		level = player.current_level
		cutscene_script = MASTER_CUTSCENE_MAP[self.cutscene_key]
		cutscene_action_data_list = cutscene_script[0]
		start_action_list = self.build_cutscene_action_list(cutscene_action_data_list, level)
		cutscene_end_action_data = cutscene_script[1]
		cutscene_end_action = self.build_action(cutscene_end_action_data, level)
		cutscene = Cutscene(start_action_list, level, cutscene_end_action)
		level.begin_cutscene(cutscene)

		# mark that the player has already seen the cutscene.
		player.viewed_cutscene_keys.append(self.cutscene_key)

	def build_cutscene_action_list(self, action_data_list, level):
		""" ct.build_cutscene_action_list( [ ? ], Level ) -> [ GameAction ]

		Parse a set of primitive action_data into a list of start GameActions (to be executed simultaneously).
		"""
		start_action_list = []
		for d in action_data_list:
			action = self.build_action(d, level)
			start_action_list.append(action)
		return start_action_list

	def build_action(self, action_data, level):
		""" ct.build_action( ?, Level ) -> GameAction

		Figure out what type of action an action is based on its key (found in cutscenescripts.py),
		and then return it.
		"""
		action_key = action_data[1]
		actor_key = action_data[0]
		actor_group_type = ACTOR_GROUP_MAP[actor_key]
		actor = level.get_actor(actor_group_type, actor_key)
		return MASTER_ACTION_MAP[action_key](self, actor, action_data)

	def begin_dialog_tree_action(self, actor, action_data): #what args are needed?
		""" ct.begin_dialog_tree( Player/NPC/Sign, ? ) -> Dialog

		Return a Dialog that will serve as a GameAction for a cutscene.
		"""
		dialog_tree = action_data[2]
		actor.init_dialogs(dialog_tree)
		return actor.first_dialog

	#TEMP
	def test_begin_miner_fight(self, miner, action_data):
		return GameAction(NonPlayerCharacter.test_begin_fight, 0, miner, None) # (method, duration, actor, arg)

# conisder putting this map in cutscenescripts.py to keep all maps in one place.
MASTER_ACTION_MAP = {
	BEGIN_DIALOG_TREE:CutsceneTrigger.begin_dialog_tree_action,
	TEST_BEGIN_MINER_FIGHT_1:CutsceneTrigger.test_begin_miner_fight
}