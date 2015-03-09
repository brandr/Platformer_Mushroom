""" A platfrom is a block that is solid and obstructs the motion of beings.
"""

from block import Block
from gameimage import GameImage
from platformdata import DESTROY_LIGHT_FLASH, DESTROY_STEP_ON
from pygame import Surface, Color, Rect

DESTROY_FRAMES = 6
DEFAULT_COLORKEY = Color("#FF00FF")

class Platform(Block):
	""" Platform( AnimationSet, int, int ) -> Platform

	Unlike some other blocks (like ladders), platforms always obstruct movement. Some of them
	can allow passage under certain conditions.

	Attributes:

	is_solid: Flags that beings cannot pass through the platform
	"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_solid = True

	def update(self, player):	
		""" p.update( Player ) -> None

		This is a general method. If a platform should react in some way to the player's prescence, it does so here.
		"""
		pass

	def map(self):
		""" p.map( ) -> None

		Mark that the player has seen this platform.
		"""
		self.mapped = True

class DestructiblePlatform(Platform):
	""" DestructiblePlatform( AnimationSet, int, int ) -> DestructiblePlatform

	A DestructiblePlatform is identical to a platform, except that it has some criteria
	for being destroyed.
	"""
	def __init__(self, animations, x, y):
		Platform.__init__(self, animations, x, y)
		self.destroy_list = []	#consider adding more ways to destroy these blocks, such as stepping on them.
		self.destroying = False
		self.destroyed = False
		self.destroy_animation = self.build_destroy_animation()

	def update(self, player):
		""" dp.update( Player ) -> None

		The destructible platform either does nothing, or advances its destruction frames.
		"""
		if self.destroyed: 
			self.finish_destroy(player.current_level)
			return
		if not self.destroying: return
		self.updateAnimation()
		if self.animation.at_end(): self.destroyed = True

	def receive_catalyst(self, catalyst, level):
		""" dp.receive_catalyst( Str ) -> None

		The platform receives some catalyst which may or may not destroy it.
		"""
		if self.destroying or catalyst not in self.destroy_list: return
		self.begin_destroy(level)

	def begin_destroy(self, level):
		""" dp.begin_destroy( Level ) -> None

		The platform begins to be destroyed. It should stay solid for a very short period of time.
		"""
		self.destroying = True
		self.animation = self.destroy_animation
		self.animated = True

	def finish_destroy(self, level):
		""" dp.finish_destroy( Level )

		Signal that this block can now be removed from the level.
		"""
		level.remove_block(self)

	def build_destroy_animation(self):
		""" dp.build_destroy_animation( ) -> SpriteStripAnimator

		Create an animation that this block will have when it is being destroyed.
		"""
		rect = self.rect
		sprites = []
		base_image = self.default_image
		for i in xrange(DESTROY_FRAMES): #NOTE: this will not work for sloped destructible blocks.
			image = Surface( ( rect.width, rect.height ) )
			image.blit(base_image, ( 0, 0 ))
			image.set_alpha(255/max(i, 1))
			sprites.append(image)
		return GameImage.load_animation_from_images(sprites, Rect(0, 0, rect.width, rect.height), -1, True, 10)

class PassablePlatform(Block):
	""" PassablePlatform( AnimationSet, int, int ) -> PassablePlatform

	PassablePlatforms are technically not platforms, but they are stored in this file to make things less confusing.

	Attributes:

	is_solid: Flags that beings cannot pass through the platform
	"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_solid = False