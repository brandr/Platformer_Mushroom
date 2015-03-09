""" An inventory of items held by the player.
"""

LANTERN = "lantern"
SWORD = "sword"

class Inventory:
	""" Inventory( ) -> Inventory

	By default, an inventory is generated empty, but items can be added to it.
	"""
	def __init__(self):
		self.items = {}

	def add_item(self, item, key):
		""" I.add_item( Item, str ) -> None

		Add an item to this inventory by first checking what item it is, then pmapping it to the given key.
		"""
		self.items[key] = item

	def get_item(self, key):
		""" I.get_item( str ) -> Item

		Find the item using the key.
		"""
		if not key in self.items: return None
		return self.items[ key ]

	def get_all_items(self):
		""" I.get_all_items( ) -> [ Item ]

		Returns every item in this inventory.
		"""
		return self.items.values()

	def get_all_item_keys(self):
		""" I.get_all_item_keys( ) -> [ str ]

		Returns the names of every item in this inventory.
		"""
		return self.items.keys()