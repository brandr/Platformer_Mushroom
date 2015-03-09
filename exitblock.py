from block import *

class ExitBlock(Block): #block which exits the level and takes the player elsewhere
	""" ExitBlock( AnimationSet, int, int ) -> ExitBlock

	A special block that spawns outside the bounds of a level if there is no corresponding adjacent level.
	This effectively stops the player from leaving the world and crashing the game.
	"""
	def __init__(self, animations,x, y):
		Block.__init__(self, animations, x, y)

	def update(self, player): 
		pass