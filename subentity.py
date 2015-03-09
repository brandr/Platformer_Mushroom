
"""An entity linked to (and usually dependent upon) another entity.
"""

from gameimage import GameImage
from being import Being

LEFT = 'left'
RIGHT = 'right'

class SubEntity(Being): #NOTE: should lanterns be a subentity?
	""" SubEntity( Entity, AnimationSet, int, int ) -> SubEntity

	A subentity generally follows its superentiy as it moves, unless the subentity is a projectile or something.
	It is usually something temporary, like a weapon as it is being swung.	

	Attrbitues:

	active_count: Currently used to keep track of how long the subentity has left onscreen (in frames).

	follow_offset: Used to determine how far the subentity should appear from its superentity, assuming that it 
	follows the superentity as it moves.
	"""
	def __init__(self, superentity, animations, x = None, y = None):
		self.superentity = superentity
		Being.__init__(self, animations, x, y)
		self.animated = True
		self.active = False
		self.active_count = 0
		self.follow_offset = (0, 0)

	def activate(self):
		""" se.activate( ) -> None

		Make the subentity appear onscreen and start doing whatever it does.
		(That means this is an abstract class, not that I'm too lazy to describe it.)
		"""
		if self.active: return
		self.active = True
		self.superentity.add_subentity(self)
		self.active_count = 20

	def deactivate(self):
		""" se.deactivate( ) -> None

		Remove the subentity from the screen and make it stop doing things.
		"""
		self.active = False
		self.superentity.remove_subentity(self)

	def update(self):
		""" se.update( ) -> None

		This method is incomplete. Currently it really just advanced the subentity's animation.
		"""
		GameImage.updateAnimation(self, 256)
		self.check_collisions()
	
	# TODO: consider checking collisions in a general way if subentities have enough commonality.
	# for instance, many (but not all) subentities may copy Being's collide method for platforms.

	def check_collisions(self):
		""" se.check_collisions( ) -> None

		A general method that I might add more to later.
		"""
		pass

	def single_animation_update(self):
		""" se.single_animation_update( ) -> None

		If this subentity only gets one animation, then it is removed from the level after its animation is done.
		"""
		if self.active and self.animation.at_end():
			self.deactivate()

	def timed_update(self):
		""" se.timed_update( ) -> None

		Update the subentity assuming that its duration is based on a timer rather than completing its animation.
		"""
		if self.active:
			self.active_count -= 1
			if self.active_count <= 0:
				self.deactivate()

	def follow_update(self):
		""" se.follow_update( ) -> None

		If the subentity is supposted to follow its superentity, it adjusts its position in this method.
		"""
		if self.active:
			coords = self.superentity.rect_coords()
			self.moveRect(self.follow_offset[0] + coords[0], self.follow_offset[1] + coords[1], True)