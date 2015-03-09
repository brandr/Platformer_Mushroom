""" Parses keyboard input and passes it to various components of the game for 
	processing.
"""

import pygame
from pygame.locals import *

class Controls:
	""" Controls( ) -> Controls

		An abstract class for translating key presses into actions.

		Attributes:

		control_map: a dict of key inputs to methods.

	"""

	def __init__(self): 
		self.control_map = None #TODO: add things to this class that aren't specific to the maingamecontrols.
		self.control_manager = None
		self.player = None

	def initialize_control_map(self, model_map):
		""" c.initialize_control_map( { str : method } ) -> None

		Use a dict matching string constants (representing key presses) to methods.
		"""
		self.control_map = {}
		for key in model_map:
			self.control_map[key] = model_map[key]

	def process_event(self, event): #abstract method, to be inherited from by subclasses
		""" c.process_event( Event ) -> None

		Handle a key press event based on the current set of controls.
		"""
		if event.type == QUIT: raise(SystemExit)
		if event.type == KEYDOWN:
			if event.key in(self.control_map):
				action = self.control_map[event.key]
				action(self, event.key, True)
		elif event.type == KEYUP:
			if event.key in(self.control_map):
				action = self.control_map[event.key]
				action(self, event.key, False)