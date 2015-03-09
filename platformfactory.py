""" A factory for creating platforms.
"""

from platform import Platform, DestructiblePlatform
from platformdata import PlatformData, DestructiblePlatformData
from gameimage import GameImage
#seems like I'm not really using this now, but keep it around because I might flesh it out more later.

class PlatformFactory(object):

	@staticmethod
	def build_entity(raw_platform_image, platform_rect, platform_data, x, y):	#not sure if I can use sign_key-- might need a different structure to figure out the proper text
		""" build_entity( Surface, Rect, PlatformData, int, int ) -> Sign

		Take a sign image and rect to create the sign object that will appear on the level, and use the sign data 
		to build the text on the sign that will appear when the player reads it.
		"""
		still_entity_image = GameImage.still_animation_set(raw_platform_image, platform_rect)
		if isinstance( platform_data, DestructiblePlatformData ):
			platform = DestructiblePlatform(still_entity_image, x, y)
			platform.destroy_list = [platform_data.catalyst]
			return platform
		platform = Platform(still_entity_image, x, y) #if platforms can become more complex, deal with those complexities here.
		return platform