"""Uses spritestripanimator (not made by me) to animate images.
"""

class AnimationSet(object):
	"""AnimationSet ( SpriteStripAnimator ) -> AnimationSet

	This is a set of animations which can be used by a GameImage object
	to change its sprite based on its current state. Some animations will
	loop, while others will not.

	Attributes:
	animations - a dictionary of animations, with strings as keys.
				 Keys are of the form [direction], [ID]. (where ID is some string like "jumping" or "running")
	"""
	def __init__(self, default_animation = None):
		self.animations = {}
		if(default_animation != None):
			self.insertAnimation(default_animation, 'default', 'default')

	def set_in_direction(self, direction): # could also make direction a tuplet like (0,1) and organize spriteSheets accordingly
		""" anim_set.set_in_direction( string ) -> { string : SpriteStripAnimator }

		Returns a dict of SpriteStripAnimator animation objects in the given direction.
		For instance, set_in_direction('left') will return all left-facing animations.
		"""
		if(direction == None):
			return None
		return self.animations[direction]

	def insertAnimation(self, animation, direction, ID = 'idle'): # "default" might be a better default ID. Decide once animations are more diverse.
		""" anim_set.insertAnimation( SpriteStripAnimator, string, string ) -> None

		Add an animation to this animation set at the given direction and ID.
		"""
		if (not direction in self.animations.keys()): 
			self.animations[direction] = {}
		self.animations[direction][ID] = animation

	def default_animation(self):
		""" anim_set.default_animation() -> SpriteStripAnimator

		Return the default animation in the default direction.
		"""
		if (not 'default' in self.animations.keys()
			or not 'default' in self.animations['default'].keys()): # if direciton is replaced with coords, replace default with (0,0)
			return None
		return self.animations['default']['default']