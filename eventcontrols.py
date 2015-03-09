""" Handles the controls used during a cutscene, while reading a sign, etc.
"""

from controls import *

class EventControls(Controls):
	""" EventControls( GameEvent, Player ) -> EventControls

	Can handle various contexts related to special ingame events, like cutscenes.

	Attributes:

	Event: the event associated with these controls. 
	"""

	def __init__(self, event, player):
		Controls.__init__(self)
		self.event, self.player = event, player
		self.initialize_control_map(EVENT_CONTROL_MAP) #TEMP. control map might vary based on the particular event.

	def prompt_continue_event(self, key, toggle):	#TODO: this should send information to the event which will do nothing if it is a cutscene but advance the event if it is dialogue.
		""" ec.prompt_continue_event( str, bool ) -> None

		End the event if appropriate. (continue_event is overridden by various classes.)
		"""
		if(toggle and not self.event.continue_event()):
			self.end_event()

	def end_event(self):
		""" ec.end_event( ) -> None 

		End this event, returning to the main game controls.
		""" 
		self.player.current_level.clear_effects()
		self.control_manager.switch_to_main_controls(self.player)

	def up_arrow_action(self, key, toggle):
		""" ec.up_arrow_action( str, bool ) -> None

		Perform some action associated with pressing the up arrow during an event, such as changing some selection.
		"""
		if(toggle):
			self.event.process_key(UP)

	def down_arrow_action(self, key, toggle):
		""" ec.down_arrow_action( str, bool ) -> None

		Perform some action associated with pressing the down arrow during an event, such as changing some selection.
		"""
		if(toggle):
			self.event.process_key(DOWN)

UP, DOWN = "up", "down"

prompt_continue_event = EventControls.prompt_continue_event
up_arrow_action = EventControls.up_arrow_action
down_arrow_action = EventControls.down_arrow_action
EVENT_CONTROL_MAP = {
	K_x:prompt_continue_event,
	K_UP:up_arrow_action,
	K_DOWN:down_arrow_action
}