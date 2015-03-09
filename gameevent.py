""" A scripted game event, like a sign displaying text or a cutscene.
"""

#from dialog import *
#from gameaction import *

# IDEA: make  a gameevent instant only

class GameEvent:
	""" GameEvent( [ GameAction ] ) -> GameEvent

	Attributes:

	current_actions: A list of actions that this gameevent is currently executing.
	"""
	def __init__(self, start_actions = []): 
		self.current_actions = start_actions
		self.level = None

	def process_key(self, key):
		""" ge.process_key( str ) -> None

		Passes the given key to each of the current actions to handle it appropriately.
		"""
		for a in self.current_actions:
			a.process_key(key)

	def execute(self, level):
		""" ge.execute( Level ) -> None

		Each of the currently stored actions execute on the level.
		"""
		self.level = level
		level.begin_event(self)
		for a in self.current_actions:
			a.execute(level)

	def continue_event(self):
		""" ge.continue_event( ) -> bool

		Determine whether the event should continue by checking whether any of its actions are still occurring.
		"""
		if self.current_actions:
			should_continue = False
			for a in reversed(self.current_actions):
				if a.continue_action(self, self.level):
					should_continue = True
			return should_continue
		#NOTE: this is not a constant update method, but is called when the player presses X.
		# 	   it's possible that other keys should be allowed to pass into an event. Might make a key dict for some situations.
		return False 

	def end(self):
		""" ge.end( ) -> None

		Does nothing, but overridden by cutscene.
		"""
		return

	def add_action(self, action):
		""" ge.add_action( GameAction ) -> None

		Add an action to the set of current actions.
		"""
		self.current_actions.append(action)

	def remove_action(self, event):
		""" ge.remove_action( GameAction ) -> None

		Remove an action from the set of current actions.
		"""
		self.current_actions.remove(event)

	def update(self, level):
		""" ge.update( Level ) -> None

		Each current gameaction updates appropriately.
		"""
		for a in self.current_actions:
			a.update(self, level)
		#pass
			# TODO (or maybe have subclasses inherit). Should probably update all current actions, which will
			# add new actions to this event if necessary. Finished actions are removed.
			# should iterate in reverse so that removing actions does not mess up the updating process.

	def is_complete(self):
		""" ge.is_complete( ) -> bool

		Check whether the event is finished. This may be outdated.
		"""
		return not self.current_actions #TEMP