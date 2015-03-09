""" An abstract class for things that the player can pick up/absorb by touching.
"""

from entity import *

class Pickup(Entity):
	""" Pickup( AnimationSet, int, int ) -> Pickup

	The Pickup class is the superclass for health pickups, oil pickups, etc.
	"""
	def __init__(self, animations, x, y):
		Entity.__init__(self, animations)
		self.rect.centerx += x
		self.rect.centery += y

	def take_effect(self, player):
		""" p.take_effect( Player ) -> None

		This is a general method that is overridden by subclasses of pickup.
		It should be called when the player absorbs the pickup.
		"""
		pass

class OilPickup(Pickup):
	""" OilPickup( AnimationSet, int , int ) -> OilPickup

	A pickup that restores the player's oil meter.

	attributes:
	
	oil_value: The amount of oil restored.
	"""
	def __init__(self, animations, x, y):
		Pickup.__init__(self, animations, x, y)
		self.oil_value = 1000 #TEMP. consider allowing it to be changed in the leveleditor

	def take_effect(self, player):
		""" op.take_effect( Player ) -> None

		If the player has a lantern, that lantern is completely or partially refilled.
		"""
		if player.get_lantern():
			player.get_lantern().add_oil(self.oil_value)
