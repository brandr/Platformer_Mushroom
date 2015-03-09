""" A ladder that the player (and maybe monsters) can climb up or down.
"""

from block import Block

class Ladder(Block):
	""" Ladder( AnimationSet, int, int ) -> Ladder

	Set the ladder's properties upon creation. The player class handles interaction with it.	
	"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.is_solid = False

	#TODO: map ladders properly in darkness