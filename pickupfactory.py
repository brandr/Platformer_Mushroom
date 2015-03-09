""" A factory for creating pickups.
"""

#from pickup import *
from gameimage import GameImage
from pickup import OilPickup
from tiledata import OIL_PICKUP	#TODO: import other pickup keys as necessary

PICKUP_CONSTRUCTOR_MAP = {
	OIL_PICKUP:OilPickup
}

class PickupFactory:
	""" No constructor.
	"""

	@staticmethod
	def build_entity(raw_pickup_image, pickup_rect, pickup_data, x, y):
		""" build_entity( Surface, Rect, TileData, int, int ) -> Pickup

		Use the pickup's entity key to figure out what type of pickup it is, then build it with the appropriate constructor.
		Deciding between animated and still animations is important, though I think animated makes more sense.
		"""
		still_entity_image = GameImage.still_animation_set(raw_pickup_image, pickup_rect)	#TEMP (change to animated once this simpler version works, or allow both animated and still)
		pickup_key = pickup_data.entity_key
		constructor = PICKUP_CONSTRUCTOR_MAP[pickup_key]
		pickup = constructor(still_entity_image, x, y)
		return pickup
		#TODO: make sure this is getting the right args to make an animated pickup if necessary.