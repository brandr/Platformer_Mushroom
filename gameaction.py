""" An action in the game which has another action after it. Spefically meant for cutscenes.
"""

class GameAction:
	""" GameAction( method, int, Entity, ? ) -> GameAction

	A gameaction is represented by an actor, a single-method action, and a set of next actions.
	These are used to make the actor execute the action.

	Attributes:

	next_actions: A list of linked actions to be executed simultaneously when this action is done.

	method: A method to be executed-- this is effectively the "action" that a GameAction is a wrapper for.

	duration: How many frames the action lasts for.

	actor: the Entity that executes this action.

	arg: Some abstracted arg taken by the wrapped method. If multiple args are required, consider passing
	a tuplet of args as this single arg.
	"""
	def __init__(self, method, duration = 0, actor = None, arg = None):
		self.next_actions = []
		self.method = method
		self.duration = duration
		self.actor = actor
		self.arg = arg

	def process_key(self, key):
		""" ga.process_key( str ) -> None

		An abstract method that is handled differently by different objects.
		"""
		pass

	def add_next_action(self, action):
		""" ga.add_next_action( GameAction ) -> None

		Add a next action to be executed when this action completes.
		"""
		self.next_actions.append(action)

	def continue_action(self, level = None, Event = None):
		""" ga.continue_action( Level, GameEvent ) -> bool

		Returns True if this action is not finished yet.
		"""
		return self.duration > 0 #TODO: may need a better way to determine this

	def execute(self, level = None):
		"""  ga.execute( Level ) -> None

		Execute this GameAction.
		"""
		self.method(self.actor, self.arg)

	def update(self, event, level = None):
		""" ga.update( GameEvent, Level ) -> None

		Advance this action, decrementing its remaining duration.
		"""
		if self.duration <= 0:
			for a in self.next_actions:
				event.add_action(a)
				a.execute(level)
			event.remove_action(self)
			return
		self.duration -= 1