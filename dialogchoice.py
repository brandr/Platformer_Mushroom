""" A specific type of dialog to be used when the player is given a dialog choice.
"""

from dialog import *
from gameaction import *

UP, DOWN = "up", "down"

class DialogChoice(Dialog):
	""" DialogChoice( Sign/NonPlayerCharacter, str, [ (str, str, str) ], str, str, (int, int ), bool, Color) -> DialogChoice
	
	A special type of dialog that contains a set of choices which will lead to different dialos or actions, depending on which one the player chooses.

	Attributes:

	choice_data_list: A list of data tuplets. Each tuplet corresponds to a specific dialog choice.

	source: Where the dialog originates from (a sign or NPC).

	choosing: Determines whether it is possible to select something yet.

	select_index: Determines which choice is selected right now.

	"""

	def __init__(self, source, source_type, choice_data_list, text = "", portrait_filename = None, dimensions = (0, 0), scrolling = False, font_color = BLACK):
		self.choice_data_list = choice_data_list
		self.source = source
		for d in self.choice_data_list:
			choice_text = d[0]
			text += "\n" + choice_text
		self.choosing = False
		self.select_index = 0
		Dialog.__init__(self, source_type, text, portrait_filename, dimensions, scrolling, font_color)

	def get_source(self):
		""" dc.get_source( ) -> Sign/NonPlayerCharacter

		Return the original source of this dialog choice.
		"""
		return self.source.get_source()

	def get_name(self):
		""" dc.get_name( ) -> str

		Returns the name of the source of this dialog.
		"""
		return self.source.get_name()

	def build_dialog_choice_set(self, dialog_set, action_data):
		""" dc.build_dialog_choice_set( [ Dialog ], (???) ) -> [ Dialog ]

		I don't remember how this works, but I'll update this docstring if I need to change the dialog system.
		"""
		start_choice_text_data = action_data[1]
		start_choice_list = action_data[2]
		portrait_filename = self.build_portrait_filename(start_choice_text_data[1])
		start_dialog_choice = DialogChoice(self, SIGN, start_choice_list, start_choice_text_data[0], portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling)
		#TODO: fix the SIGN part (probably by getting some key associated with NPCs)
		dialog_set[-1].add_next_action(start_dialog_choice)
		return dialog_set

	def add_dialog_set(self, start_dialog_set, add_dialog_data):
		""" dc.add_dialog_set( [ Dialog ], ? ) -> [ Dialog ]

		I don't remember how this works, but I'll update this docstring if I need to change the dialog system.
		"""
		next_dialog_data = add_dialog_data[1]
		next_dialog_set = self.build_dialog_branch(next_dialog_data)
		next_action_data = add_dialog_data[2]
		if(next_action_data):
			next_dialog_set = self.get_source().init_dialog_set(next_dialog_set, next_action_data)
		start_dialog_set[-1].add_next_action(next_dialog_set[0])
		return start_dialog_set

	def build_action_set(self, dialog_set, action_data):
		""" dc.build_action_set( [ Dialog ], ? ) -> [ Dialog ]

		I don't remember how this works, but I'll update this docstring if I need to change the dialog system.
		"""
		action_data_set = action_data[1]
		action_set = []
		for a in action_data_set:
			action = GameAction(a[0], a[1], self.get_source(), a[2])
			action_set.append(action)
		for i in range(0, len(action_data_set) - 1):
			action_set[i].add_next_action(action_set[i + 1])
		dialog_set[-1].add_next_action(action_set[0])
		next_action_data = action_data[2]  #this part is untested and may cause bugs.
		if next_action_data:
			action_key = next_action_data[0]
			build_method = BUILD_METHOD_MAP[action_key]
			dialog_set = build_method(self, action_set, next_action_data)
		return dialog_set

	def setup_next_dialog(self, dialog_set, action_data):
		""" dc.setup_next_dialog( [ Dialog ], ? ) -> [ Dialog ]

		I don't remember how this works, but I'll update this docstring if I need to change the dialog system.
		"""
		source = self.get_source()
		dialog_key = action_data[1]
		action = GameAction(source.__class__.change_current_dialog, 0, source, dialog_key)
		dialog_set[-1].add_next_action(action)
		return dialog_set

	def current_choice(self):
		""" dc.current_choice( ) -> ?

		Returns the currently selected dialog option. Figure out what type it is if I need to change the dialog system.
		"""
		return self.choice_data_list[self.select_index]

	def process_key(self, key):
		""" dc.process_key( str ) -> None

		If it is possible to select an option, process a key press that changes the currently selected option.
		"""
		if(self.index/SCROLL_CONSTANT >= len(self.text)):
			if(key == UP):
				self.select_index = max(0, self.select_index - 1)
			elif(key == DOWN):
				self.select_index = min(len(self.choice_data_list) - 1, self.select_index + 1)
	
	def draw_text_image(self):
		""" dc.draw_text_image( ) -> Surface

		Draw an image of this dialog's text on a pane.
		"""
		text_image = Dialog.draw_text_image(self)
		if(self.index/SCROLL_CONSTANT >= len(self.text)):
			arrow = Surface((12, 12)) #TEMP
			text_image.blit(arrow, (4, 8 + 32 * (1 + self.select_index))) #TEMP VALUES
			#TODO: draw arrow pointing to currently selected option (currently just a black square)
		return text_image

	def update(self, event, level):
		""" dc.update( GameEvent, Level ) -> None

		Updates the same as a normal dialog, advancing the text if necessary.
		"""
		Dialog.update(self, event, level)
		if(self.index/SCROLL_CONSTANT >= len(self.text)):
			self.choosing = True
		
	def continue_action(self, event, level):
		""" dc.continue_action( GameEvent, Level ) -> bool

		When the player presses X, either advances the text (if it isn't done scrolling)
		or selects the current option and executes its associated action.
		"""
		if(self.index/SCROLL_CONSTANT <= len(self.text)):
			self.index = int(SCROLL_CONSTANT * len(self.text))
			return True
		event.remove_action(self)
		level.remove_effect(self)
		choice = self.current_choice()
		dialog_branch = self.build_dialog_branch(choice[1])
		next_action_data = choice[2] 
		if(next_action_data):
			action_key = next_action_data[0]
			build_method = BUILD_METHOD_MAP[action_key]
			dialog_branch = build_method(self, dialog_branch, next_action_data)
		event.add_action(dialog_branch[0])
		dialog_branch[0].execute(level)
		return True

	def build_dialog_branch(self, dialog_data):
		""" dc.build_dialog_branch( [ ? ] ) -> [ Dialog ] 

		Not sure what this does. Update this docstring if necessary.
		"""
		dialog_set = []
		for d in dialog_data:
				portrait_filename = self.build_portrait_filename(d[1])
				dialog = Dialog(SIGN, d[0], portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling) #SIGN arg is temporary
				dialog_set.append(dialog)
		for i in range(0, len(dialog_set) - 1):
			dialog_set[i].add_next_action(dialog_set[i + 1])
		return dialog_set

	def build_portrait_filename(self, key):
		""" dc.build_portrait_filename( str ) -> str

		Returns the portrait filename for the given "expression" key. (usually refers to different facial expressions for NPCs)
		"""
		name = self.source.get_name()
		if name == None:
			return None
		return "portrait_" + name + "_" + key + ".bmp"

#constants are the same as for NPCs. (might not want this redundancy if things get much more complicated)

ACTION_SET = "action_set"	
ADD_DIALOG_SET = "add_dialog_set"
DIALOG_CHOICE = "dialog_choice"
SETUP_NEXT_DIALOG = "setup_next_dialog"
BUILD_METHOD_MAP = {
	ACTION_SET:DialogChoice.build_action_set,
	ADD_DIALOG_SET:DialogChoice.add_dialog_set,
	DIALOG_CHOICE:DialogChoice.build_dialog_choice_set, 
	SETUP_NEXT_DIALOG:DialogChoice.setup_next_dialog
	}