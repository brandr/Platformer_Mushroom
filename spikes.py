""" spikes that kill the player.
"""

from block import Block
import pygame 

class Spikes(Block):
	""" Spikes( AnimationSet, int, int ) -> Spikes

	TODO: docstring
	"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False

	def update(self, player):
		""" s.update( Player ) -> None

		If the player touches the spikes, he dies horribly.
		"""
		if pygame.sprite.collide_mask(self, player):
			player.die()

	#TODO