""" Organizes various control contexts based on the situation.
"""

from maingamecontrols import * 
from eventcontrols import *
from pausecontrols import *

class ControlManager:
	""" ControlManager( Controls ) -> ControlManager

	Can hold one Controls object at a time. Uses this to decide what the current input should do.

	Attributes:

	Controls: current control scheme for keyboard input.

	"""

	def __init__(self, controls):
		self.current_controls = controls
		self.current_controls.control_manager = self
		self.screen = None

	def process_event(self, event):
		""" cm.process_event( EVent ) -> None

		Process a keybord/mouse event properly given the current control scheme.
		"""
		self.current_controls.process_event(event)

	def switch_screen(self, screen):
		""" cm.switch_screen( GameScreen ) -> None

		Switch to the given screen.
		"""
		self.screen.switch_screen(screen)

	def switch_controls(self, controls):
		""" cm.switch_controls ( Controls ) -> None

		Change the current control scheme.
		"""
		controls.control_manager = self
		self.current_controls = controls 

	def switch_to_main_controls(self, player):
		""" switch_to_main_controls( Player ) -> None

		Change the controls to the main game controls and make them apply to the given player.
		"""
		player.deactivate()
		main_controls = MainGameControls(player)
		self.switch_controls(main_controls)

	def switch_to_event_controls(self, event, player): #TODO: make it so pressing x doesn't cancel cutscenes
		""" switch_to_event_controls( GameEvent, Player ) -> None

		Change to controls for some event. Example: choosing a dialog option.
		"""
		event_controls = EventControls(event, player)
		self.switch_controls(event_controls)