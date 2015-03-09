""" A cutscene during which things happen and buttons only advance the dialog. This may be irrelevant since it isn't much different from any other GameEvent. Not sure.
"""

from gameevent import *

class Cutscene(GameEvent):
	""" Cutscene( [Action] ) -> Cutscene

	A cutscene is a special type of GameEvent which can have somewhat different rules, including a set beginning and end along
	with animations/actions that take set amounts of time.

	Attributes:

	level: the level that the cutscene takes place on.
	"""
	def __init__(self, start_actions = [], level = None, end_action = None): #TODO: figure out what is special about cutscenes that can be used to separate them from normal events
		GameEvent.__init__(self, start_actions)
		self.level = level #TODO: either make a way to set level, or create a system that doesn't need it.
		self.end_action = end_action

	def begin(self):
		""" c.begin( ) -> None

		Activate all start actions for this cutscene.
		"""
		for a in self.current_actions:
			a.execute(self.level) 

	def update(self, level):
		""" c.update( Level ) -> None

		Update all the current ongoing actions for this cutscene.
		"""
		for a in self.current_actions:
			a.update(self, level)

	def continue_event(self):
		""" c.continue_event( ) -> bool

		Determine whether the event should continue by checking whether any of its actions are still occurring.
		"""
		if not self.level: return True
		if self.current_actions:
			should_continue = False
			for a in reversed(self.current_actions):
				if a.continue_action(self, self.level):
					should_continue = True
			return should_continue or self.level.has_effects
		#NOTE: this is not a constant update method, but is called when the player presses X.
		# 	   it's possible that other keys should be allowed to pass into an event. Might make a key dict for some situations.
		return True

	def end(self):
		""" c.end( ) -> None

		Executes the associated end action.
		Consider giving gameevents end actions if it might be useful.
		"""
		if self.end_action: self.end_action.execute()