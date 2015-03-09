""" A factory for creating cutscene triggers.
"""

from cutscenetrigger import CutsceneTrigger
from gameimage import GameImage

class CutsceneTriggerFactory:
	""" No constructor.
	"""
	@staticmethod
	def build_entity(raw_trigger_image, trigger_rect, trigger_data, x, y):	#not sure if I can use sign_key-- might need a different structure to figure out the proper text
		""" build_entity( Surface, Rect, SignData, int, int ) -> CutsceneTrigger

		Build a cutscene trigger, setting its string key to the given data's associated key.
		"""
		still_entity_image = GameImage.still_animation_set(raw_trigger_image, trigger_rect)
		trigger = CutsceneTrigger(still_entity_image, x, y)
		trigger.cutscene_key = trigger_data.cutscene_key
		return trigger