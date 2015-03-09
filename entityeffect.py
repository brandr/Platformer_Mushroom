""" A subentity that only exists as a visual effect.
"""

from subentity import SubEntity

class EntityEffect(SubEntity):
	""" EntityEffect( Entity, AnimationSet, int, int ) -> EntityEffect

	An EntityEffect is a subentity that only exists as a visual effect and is rendered
	on the top visual layer in a level.
	"""

	def __init__(self, superentity, animations, x = None, y = None):
		SubEntity.__init__(self, superentity, animations, x, y)

	def update(self):
		""" ee.update( ) -> None

		Animates the effect, removing it if it has finished its animation.
		"""
		self.animate()
		if self.animation.at_end():
			self.superentity.remove_entity_effect(self)