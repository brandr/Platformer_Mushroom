# -*- coding: utf-8 -*-
""" A sign that the player can read. No one else can, though.
"""

from block import Block
from gameevent import GameEvent
from dialog import Dialog, SIGN
from camera import WIN_WIDTH, WIN_HEIGHT

DIALOG_BOX_WIDTH = WIN_WIDTH - 32
DIALOG_BOX_HEIGHT = WIN_HEIGHT/6

class Sign(Block): #TODO: figure out how to set text, # of panes, whether text is scrolling, etc.
	""" Sign( AnimationSet, int, int ) -> Sign

	A sign is a passable block that the player can read by pressing x while standing near it.
	Reading a sign opens up a dialog box, preventing any entities (including the player) from moving
	until the dialog box is closed.

	Attributes:

	x_interactable: flags that the player can interact with the sign (i.e., read it) by pressing x near it.

	scrolling: flags whether the text on the sign should scroll (True) or appear instantly (False).

	text_set: A list of the text panes that will appear when the sign is read.
 	"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.x_interactable = True
		self.scrolling = True #might want to make more elaborate scrolling later
		self.text_set = None
		self.is_solid = False

	def set_text_set(self, text_set):
		""" s.set_text_set( [ [ str ] ] ) -> None

		Fill the sign's text panes with the given strings.
		Note that this method takes a 2D array becaue each element of the input is a list of lines,
		which are then parsed as string separated by the "\\n" character.
		"""
		self.text_set = []
		for i in xrange(len(text_set)):
			self.text_set.append("")
			for line in text_set[i]:
				if line != "":
					self.text_set[i] += line + "\n"

	def execute_x_action(self, level, player):
		""" s.execute_x_action( Level, Player ) -> None

		This is called when the player presses X near the sign.
		This causes the sign's dialog box to appear.
		"""
		self.execute_event(level)

	def execute_event(self, level):
		""" s.execute_event( Level ) -> None

		Executes the sign's event, making a dialog box appear onscreen.
		"""
		if self.text_set:
			dialog_set = self.build_dialog_set(self.text_set)
			event = GameEvent([dialog_set[0]])
			event.execute(level)

	def build_dialog_set(self, text_data):
		""" s.build_dialog_set( [ str ] ) -> [ Dialog ]

		Generate this sign's Dialog set from a list of strings.
		"""
		dialog_set = []
		for t in text_data:
				dialog = Dialog(SIGN, t, None, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling)
				dialog_set.append(dialog)
		for i in range(0, len(dialog_set) - 1):
			dialog_set[i].add_next_action(dialog_set[i + 1])
		return dialog_set