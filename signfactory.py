""" A factory for adding text to signs.
"""

from gameimage import GameImage
from sign import Sign

class SignFactory:
	""" No constructor.
	"""
	@staticmethod
	def build_entity(raw_sign_image, sign_rect, sign_data, x, y):	#not sure if I can use sign_key-- might need a different structure to figure out the proper text
		""" build_entity( Surface, Rect, SignData, int, int ) -> Sign

		Take a sign image and rect to create the sign object that will appear on the level, and use the sign data 
		to build the text on the sign that will appear when the player reads it.
		"""
		still_entity_image = GameImage.still_animation_set(raw_sign_image, sign_rect)
		sign = Sign(still_entity_image, x, y)
		sign_text_panes = sign_data.text_panes
		sign.set_text_set(sign_text_panes)
		return sign