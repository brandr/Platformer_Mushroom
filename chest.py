""" A treasure chest that the player can open.
"""

from block import Block
from chestcontents import *
from gameevent import GameEvent
from dialog import Dialog, SIGN, DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT
from itemfactory import build_item

class Chest(Block):
	""" Chest( AnimationSet, int, int ) -> Chest

	A chest is a block containing an item (or nothing). The player can open the chest
	by interacting with it, unless it is locked or otherwise impossible to open.
	Since not all chests contain the same thing, the chest is a nonstandard object.
	"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.x_interactable = True
		self.scrolling = True
		self.is_solid = False
		self.open = False
		self.open_chest_image = None
		self.contents_data = None
		self.text_set = None

	# methods for building the chest


	def generate_contents(self, key):
		""" c.generate_contents( str ) -> None

		Fill the chests with the proper contents based on the string key.
		"""
		if not key in MASTER_CHEST_CONTENTS_MAP: return
		item_data = MASTER_CHEST_CONTENTS_MAP[key]
		constructor = item_data[ITEM_CLASS]
		item_key = item_data[ITEM_KEY]
		display_name = item_data[DISPLAY_NAME]
		dialog_data = item_data[RECEIVE_DIALOG_DATA]
		#TODO: set self.contents to item
		self.contents_data = { ITEM_CLASS:constructor, ITEM_KEY:item_key, DISPLAY_NAME:display_name }
		self.set_text_set(dialog_data)

	def set_text_set(self, text_set):
		""" c.set_text_set( [ [ str ] ] ) -> None

		Fill the chest's text panes with the given strings.
		Note that this method takes a 2D array becaue each element of the input is a list of lines,
		which are then parsed as string separated by the "\\n" character.
		"""
		self.text_set = []
		for i in xrange(len(text_set)):
			self.text_set.append("")
			for line in text_set[i]:
				if line != "":
					self.text_set[i] += line + "\n"

	# methods for activating the chest

	def execute_x_action(self, level, player):
		"""c.execute_x_action( Level, Player ) -> None

		This is called when the player presses X near the chest.
		This causes the chest to open, giving the player its contents.
		"""
		if not self.open: 
			self.execute_event( level )
			self.set_open( player )


	def set_open(self, player):
		""" c.set_open( Player ) -> None

		The chest opens, giving its contents to the player.
		"""
		#TODO: open and give the player the item contained.
		self.open = True
		self.default_image = self.open_chest_image #TODO: set open chest image
		self.image = self.open_chest_image
		if not self.contents_data: return # case for empty chest
		item = self.build_item()
		key = self.contents_data[ ITEM_KEY ]
		player.acquire_item( item, key )

	def build_item(self):
		""" c.build_item( ) -> ?

		Use this chest's item data to build its contained item.
		"""
		if not self.contents_data: return None
		constructor = self.contents_data[ ITEM_CLASS ]
		key = self.contents_data[ ITEM_KEY ]
		return build_item( constructor, key, 0, 0 )

	def execute_event(self, level):
		""" c.execute_event( Level ) -> None

		Executes the chest's event, making a dialog box appear onscreen.
		"""
		if self.text_set:
			dialog_set = self.build_dialog_set(self.text_set)
			event = GameEvent([dialog_set[0]])
			event.execute(level)

	def build_dialog_set(self, text_data):
		""" c.build_dialog_set( [ str ] ) -> [ Dialog ]

		Generate this sign's Dialog set from a list of strings.
		"""
		dialog_set = []
		portrait_filename = self.acquire_image_filename()
		for t in text_data:
				dialog = Dialog(SIGN, t, portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling)
				dialog_set.append(dialog)
		for i in range(0, len(dialog_set) - 1):
			dialog_set[i].add_next_action(dialog_set[i + 1])
		return dialog_set

	def acquire_image_filename(self):
		""" c.acquire_image_filename( ) -> str

		Determine this chest's image filename-- used to create an image representing the object in the chest.
		"""
		item_key = self.contents_data[ITEM_KEY]
		if not item_key: return None
		return "portrait_" + item_key + ".bmp"