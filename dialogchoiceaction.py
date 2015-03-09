""" A specific type of gameaction to be used when the player is given a dialog choice.
NOTE: this may be outdated. Not sure if it's used anywhere.
"""

from gameaction import *

class DialogChoiceAction(GameAction):

	def __init__(self, choice_data):
		#IDEA: could make this inherit from dialog instead of gameaction
		self.choice_data = choice_data
		#yn_choices = [("Yes", yes_text_set, None), ("No", no_text_set, None)] #None means the conversation ends after the set in question.

		#GameAction.__init__(self, self.)
		#self, method, duration = 0, actor = None, arg = None

	def execute_event(self, level):
		pass #TODO