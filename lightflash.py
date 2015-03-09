""" A flash of light emitted by a lantern (or occassinally some other source.)
"""

from subentity import SubEntity
from platform import DESTROY_LIGHT_FLASH
import pygame 

class LightFlash(SubEntity):
	""" LightFlash( Entity, AnimationSet, int, int ) -> LightFlash

	A LightFlash is represented as an expanding white circle that only effects
	destructible blocks it comes into contact with. 

	I might eventually make upgrades that let it damage enemies.
	"""
	def __init__(self, superentity, animation_set):
		SubEntity.__init__(self, superentity, animation_set)
		self.default_image = self.animation.images[0]

	def activate(self):
		""" lf.activate( ) -> None

		Activate the light flash, telling it to begin expanding.
		"""
		super_rect = self.superentity.rect
		self.follow_offset = (super_rect.right - super_rect.centerx - self.default_image.get_width()/2, super_rect.bottom - super_rect.centery - self.default_image.get_height()/2)
		x, y = self.superentity.rect.centerx, self.superentity.rect.centery
		self.moveRect( self.follow_offset[0], self.follow_offset[1], True )
		SubEntity.activate(self)
		self.superentity.lock_lantern()

	def deactivate(self):
		""" lf.deactivate( ) -> None

		Remove the light flash from the screen and make it stop doing things.
		"""
		self.superentity.unlock_lantern()
		SubEntity.deactivate(self)

	def update(self):
		""" lf.update( ) -> None

		Perform an update for the LightFlash, telling it to follow the player and update its animation.
		"""
		SubEntity.update(self)
		SubEntity.single_animation_update(self)
		SubEntity.follow_update(self)
		if self.superentity.get_lantern().oil_meter[0] <= 0: self.deactivate()

	def check_collisions(self):
		""" lf.check_collisions( ) -> None

		Check to see if this light hits anything it can affect.
		"""
		centerx, centery = self.rect.centerx, self.rect.centery
		
		level = self.superentity.current_level
		destructible_platforms = level.getDestructiblePlatforms()
		mask = pygame.mask.from_surface(self.image)
		radius = (mask.get_size()[0] - 32)/2 - 16
		for dp in destructible_platforms:
			if dp.within_pixel_dist(self, radius):
				dp.receive_catalyst(DESTROY_LIGHT_FLASH, level)