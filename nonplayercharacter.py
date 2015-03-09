""" A non-hostile character that the player can walk past and not bounce off of.
"""

from being import Being
from gameevent import GameEvent
from dialog import Dialog
from dialogchoice import DialogChoice
from monster import Monster

from dialog import SIGN, DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT

class NonPlayerCharacter(Being):
	""" NonPlayerCharacter( AnimationSet, int, int ) -> NonPlayerCharacter

	The player can talk to most NPCs. Since they are non-hostile by definition,
	they generally sholudn't do much else unless they give the player an item or
	are associated with some kind of quest.

	Attributes:

	x_interactable: Flags that the player can interact (talk) with the NPC by pressing X.

	scrolling: Flags that text in the NPC's dialog box scrolls instead of appearing all at once.

	name: A currently unused string represeting the NPC's name. Will probably be a key to access dialog trees at some point.

	active: Causes the NPC to perform actions like pacing around or turning to face the player.

	direction_id: String to determine the NPC's animation.
	"""
	def __init__(self, animations, x, y):
		Being.__init__(self, animations, x, y)
		self.animated = True
		self.x_interactable = True
		self.scrolling = True #might want to make more elaborate scrolling later
		self.name = None
		self.active = True
		self.direction_id = 'left'
		self.changeAnimation('idle','left')

		self.right = False #TEMP

	def get_name(self):
		""" npc.get_name( ) -> str

		A probably useless getter. (Durrr getters in python isshy geddit)
		"""
		return self.name

	def get_source(self): 
		""" npc.get_source( ) -> NonPlayerCharacter

		A general method used to make dialog trees work properly whether the source of the dialog is an NPC or a sign.
		"""
		return self

	def update(self, player):
		""" npc.update( Player ) -> None 

		Updates the NPC's animation and make it face towards the player.
		"""
		if not (self.onGround): self.snap_to_ground()
		self.changeAnimation('idle', self.direction_id)
		if self.active:
			self.NPC_update(player)

		#TEMP	
		if(self.right):
			self.xvel = 4
			self.direction_id = 'right'	
		else:
			self.xvel = 0
		#TEMP	

		Being.update(self, player)
		Being.updatePosition(self)

	def NPC_update(self, player):	
		""" npc.NPC_update( Player ) -> None 

		Makes the NPC face towards the player.
		NOTE: might want some NPCs to walk around instead of doing this. Not sure.
		"""
		self.face_towards(player)

	def face_towards(self, target):
		""" npc.face_towards( Being ) -> None

		Figure out if the player is to the left or to the right of this NPC, and face in that direction.
		"""
		if(target != None):
			x_dist = target.coordinates()[0] - self.current_tile().coordinates()[0]
			if x_dist == 0: return
			self.direction_val = x_dist/abs(x_dist)
			if self.direction_val == -1:
				self.direction_id = 'left'
			if self.direction_val == 1:
				self.direction_id = 'right'

	def set_active(self, active):
		""" npc.set_active( bool ) -> None

		HERP DERP LOOK AT ME I USE SETTERS IN PYTHON XD XD 
		(for real though, if something else should happen when the NPC becomes active then we'll have a use for this)
		"""
		self.active = active

	def temp_stop_method(self, arg = None):
		# no docstring because temp
		self.left, self.right, self.up, self.down = False, False, False, False	

	def temp_npc_right_method(self, arg = None): #TEMP for testing
		# no docstring because temp
		self.right = True

	def init_dialogs(self, dialog_tree):
		""" npc.init_dialogs( ? ) -> None

		TODO: fill this out if we need to change the dialog system.
		"""
		start_dialog_set = self.build_dialog_set(dialog_tree[0])
		start_action_data = dialog_tree[1]
		if(start_action_data):
			start_dialog_set = self.init_dialog_set(start_dialog_set, start_action_data)	
		self.first_dialog = start_dialog_set[0]

	def init_dialog_set(self, dialog_set, action_data):
		""" npc.init_dialog_set( ?, ? ) -> None

		TODO: fill this out if we need to change the dialog system.
		"""
		action_key = action_data[0]
		build_method = BUILD_METHOD_MAP[action_key]
		return build_method(self, dialog_set, action_data)

	def build_dialog_choice_set(self, dialog_set, action_data):
		""" npc.build_dialog_choice_set( ?, ? ) -> None

		TODO: fill this out if we need to change the dialog system.
		"""
		start_choice_text_data = action_data[1]
		start_choice_list = action_data[2]
		portrait_filename = self.build_portrait_filename(start_choice_text_data[1])
		start_dialog_choice = DialogChoice(self, SIGN, start_choice_list, start_choice_text_data[0], portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling)
		#TODO: fix the SIGN part (probably by getting some key associated with NPCs)
		dialog_set[-1].add_next_action(start_dialog_choice)
		return dialog_set

	def add_dialog_set(self, start_dialog_set, add_dialog_data):
		""" npc.add_dialog_set( ?, ? ) -> None

		TODO: fill this out if we need to change the dialog system.
		"""
		next_dialog_data = add_dialog_data[1]
		next_dialog_set = self.build_dialog_set(next_dialog_data)
		next_action_data = add_dialog_data[2]
		if(next_action_data):
			next_dialog_set = self.init_dialog_set(next_dialog_set, next_action_data)
		start_dialog_set[-1].add_next_action(next_dialog_set[0])
		return start_dialog_set

	def build_action_set(self, dialog_set, action_data):
		""" npc.init_dialogs( ?, ? ) -> None

		TODO: fill this out if we need to change the dialog system.
		"""
		action_data_set = action_data[1]
		action_set = []
		for a in action_data_set:
			action = GameAction(a[0], a[1], self, a[2])
			action_set.append(action)
		for i in range(0, len(action_data_set) - 1):
			action_set[i].add_next_action(action_set[i + 1])
		dialog_set[-1].add_next_action(action_set[0])
		next_action_data = action_data[2]  #this part is untested and may cause bugs.
		if next_action_data:
			dialog_set = self.init_dialog_set(action_set, next_action_data)
		return dialog_set

	def setup_next_dialog(self, dialog_set, action_data):	#no need to check for next action because this is done at the very end only.
		""" npc.setup_next_dialog( ?, ? ) -> None

		TODO: fill this out if we need to change the dialog system.
		"""
		dialog_key = action_data[1]
		action = GameAction(NonPlayerCharacter.change_current_dialog, 0, self, dialog_key)
		dialog_set[-1].add_next_action(action)
		return dialog_set

	def change_current_dialog(self, dialog_key):
		""" npc.change_current_dialog( str ) -> None

		Change the dialog that will appear if the player talks to the NPC, using a dict.
		"""
		self.dialog_tree = self.dialog_tree_map[dialog_key] #might want error checking here

	def build_dialog_set(self, dialog_data):
		""" npc.build_dialog_set( ? ) -> None

		TODO: fill this out if we need to change the dialog system.
		"""
		dialog_set = []
		for d in dialog_data:
				portrait_filename = self.build_portrait_filename(d[1])
				dialog = Dialog(SIGN, d[0], portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling) #TODO: change the SIGN arg
				dialog_set.append(dialog)
		for i in range(0, len(dialog_set) - 1):
			dialog_set[i].add_next_action(dialog_set[i + 1])
		return dialog_set
		
	def execute_x_action(self, level, player):
		""" npc.execute_x_action( Level, Player ) -> None

		Execute this NPC's dialog event when the player presses X nearby.
		"""
		self.execute_event(level)

	def execute_event(self, level):
		""" npc.execute_event( Level ) -> None

		Set up this NPC's dialogs and open the dialog box onscreen.
		"""
		self.init_dialogs(self.dialog_tree)
		event = GameEvent([self.first_dialog])
		event.execute(level)

	def build_portrait_filename(self, key):
		""" npc.build_portrait_filename( str ) -> str

		Use the NPC's name concatenated with a string key (represeting a facial expression) to make the filename for the current portrait.
		"""
		if self.name == None:
			return None
		return "portrait_" + self.name + "_" + key + ".bmp"

		#TEMP
		#IDEA: change this method to "become hostile" or something in order to turn any NPC into its corresponding (mapped) monster.
	def test_begin_fight(self, arg = None):
		#TODO
		monster_self = Monster(self.animation_set, self.rect.left, self.rect.top)
		monster_self.name = self.name
		monster_self.monster_init(self.name)
		self.current_level.level_objects.addEntity(monster_self)
		self.delete()
		#TEMP

NEUTRAL = "neutral"

KENSTAR = "kenstar"

MINER = "miner"

#NPCS_WITH_PORTRAITS = ["Kenstar"] #TODO: if this NPC's name is in this list, they have a portrait. Otherwise, they don't.
								  # might not need this: could just use a default (None) arg for all NPCs that don't have portraits.

ACTION_SET = "action_set"	
ADD_DIALOG_SET = "add_dialog_set"
DIALOG_CHOICE = "dialog_choice"
SETUP_NEXT_DIALOG = "setup_next_dialog"
BUILD_METHOD_MAP = {
	ACTION_SET:NonPlayerCharacter.build_action_set,
	ADD_DIALOG_SET:NonPlayerCharacter.add_dialog_set,
	DIALOG_CHOICE:NonPlayerCharacter.build_dialog_choice_set, 
	SETUP_NEXT_DIALOG:NonPlayerCharacter.setup_next_dialog
}