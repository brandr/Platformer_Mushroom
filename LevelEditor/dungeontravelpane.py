""" A visual pane in the level editor used to set if and how it is possible to travel to another dungeon via this level.
"""

from filemanagercontainer import FileManagerContainer

from ocempgui.widgets import Box, CheckButton, FileList, Label, RadioButton, ScrolledList
from ocempgui.widgets.Constants import SIG_SELECTCHANGED, SIG_TOGGLED
from ocempgui.widgets.components import ListItem, ListItemCollection, TextListItem

class DungeonTravelPane(Box):
	""" DungeonTravelPane( int, int ) -> DungeonTravelPane

	A pane in the Level Editor which contains sub-components that allow the user to set whether it is possible to travel to another dungeon
	from this level, which level in that dungeon it is linked to,
	"""
	def __init__(self, width, height):
		Box.__init__(self, width, height)
		self.dungeon_travel_label = Label("Dungeon travel settings:")
		self.travel_toggle_button = self.travel_toggle_button(self.dungeon_travel_label.left, self.dungeon_travel_label.bottom + 8)
		self.dungeon_list_label = Label("Travel to dungeon:")
		self.dungeon_list_label.topleft = self.travel_toggle_button.left, self.travel_toggle_button.bottom + 8
		self.dungeon_select_list = self.dungeon_select_list(self.travel_toggle_button.left, self.dungeon_list_label.bottom + 8, self.width - 140, 80)
		self.level_select_label = Label("Travel to level:")
		self.level_select_label.topleft = self.dungeon_select_list.right + 8, self.dungeon_list_label.top
		self.level_select_list = self.level_select_list(self.level_select_label.left, self.level_select_label.bottom + 8, self.dungeon_select_list.width, self.dungeon_select_list.height)
		self.up_button, self.down_button, self.left_button, self.right_button = self.direction_buttons(self.dungeon_select_list.left, self.dungeon_select_list.bottom + 8)
		self.set_children([self.dungeon_travel_label, self.travel_toggle_button, self.dungeon_list_label, self.dungeon_select_list, self.level_select_label, self.level_select_list, 
			self.up_button, self.down_button, self.left_button, self.right_button])
		
		# TODO: initialize the dungeon travel settings to whatever they should be based on level data (which might be taken as an arg)
		# TODO: some kind of key to determine what dungeon should be linked, and some kind of key for the linked location 
			# (either select it from a loaded list, or just put in a letter or something as the key)
			# the linked dungeon should probably be loaded, at least

	def initialize_travel_data(self, travel_data):
		""" DTP.initialize_travel_data( ( str, str, str ) ) -> None

		Set up the dungeon travel pane based on the existing travel data for this level.
		This includes toggling travel and selecting the correct dungeon, level, and direction.
		"""
		if not travel_data: return
		self.travel_toggle_button.activate()	# if the travel data is not None, then travel must be toggled on.
		dungeon_name, level_name, direction = travel_data[0], travel_data[1], travel_data[2]
		if dungeon_name:
			for d in self.dungeon_select_list.items:
				if d._text == dungeon_name: 	
					self.dungeon_select_list.select(d)
					self.dungeon_select_list.set_cursor(d, True)
					continue
			if level_name:
				for l in self.level_select_list.items:
					if l._text == level_name:
						self.level_select_list.select(l)
						self.level_select_list.set_cursor(l, True)
			if direction: #direction is techinically allowed with no level, though this alone will not allow travel in practice. This is done since there will be no receiving level for the first level set.
				buttons = [self.up_button, self.down_button, self.left_button, self.right_button]
				for b in buttons:
					if b.get_text() == direction: b.activate()

	def build_travel_data(self):
		""" DTP.build_travel_data( ) -> ( str, str, str )

		Returns a tuple of data necessary to determine if and how the player can travel from this level.
		"""
		#TODO: consider giving warnings if the linked dungeon is not this one.
		if not self.travel_toggle_button.active: return None
		dungeon_list, level_list = self.dungeon_select_list, self.level_select_list
		dungeon_list_item, level_list_item = dungeon_list.get_selected(), level_list.get_selected()
		dungeon_name, level_name = None, None
		if dungeon_list_item: 
			dungeon_name = dungeon_list_item[0]._text
			if level_list_item: 
				level_name = level_list_item[0]._text
		direction = self.travel_direction()
		return (dungeon_name, level_name, direction)
		
	def travel_toggle_button(self, x, y):
		""" DTP.travel_toggle_button( int, int ) -> CheckButton

		Create a checkbox that sets whether or not it is possible to travel to another dungeon via this level.
		"""
		travel_toggle_button = CheckButton("Enable dungeon travel from this level")
		travel_toggle_button.topleft = x, y
		travel_toggle_button.connect_signal(SIG_TOGGLED, self.toggle_travel, travel_toggle_button)		
		return travel_toggle_button

	def toggle_travel(self, button):
		""" DTP.toggle_travel( CheckButton) -> None

		Toggle travel between dungeons on or off.
		"""
		active = button.active
		if active:
			self.select_dungeon(self.dungeon_select_list)
		#TODO: add a case for off if it proves useful

	def dungeon_select_list(self, x, y, width, height):
		""" DTP.dungeon_select_list( int, int, int, int, int ) -> FileList

		Uses the given dimensions to make a FileList of dungeons to connect to.
		"""
		dungeon_list = FileList(width, height, './dungeon_map_files')
		dungeon_list.topleft = x, y
		dungeon_list.connect_signal(SIG_SELECTCHANGED, self.select_dungeon, dungeon_list)
		#TODO: conisder removing the current dungeon from this select list (may need arg in this method or in constructor for dungeontravelpane)
		return dungeon_list

	def select_dungeon(self, dungeon_list):
		""" DTP.select_dungeon( FileList ) -> None

		Change the currently selected dungeon to travel to.
		"""
		if not (self.travel_toggle_button.active and dungeon_list.get_selected()) : return
		dungeon_list_item = dungeon_list.get_selected()[0]
		directory, filename = dungeon_list._directory, dungeon_list_item._text
		if filename == "..": return
		filepath = "./" + directory + "/" + filename
		deformatted_dungeon = FileManagerContainer.dungeonDataFromFile(filepath)
		self.level_select_list.items = ListItemCollection()
		for ld in deformatted_dungeon.level_data_set:			# TODO: consider only allowing levels that have travel toggled "on."
			if ld.travel_data:
				self.level_select_list.items.append(TextListItem(ld.name))

		#TODO: if this gets laggy, don't load any more data than necessary, to save time

	def level_select_list(self, x, y, width, height):
		""" DTP.level_select_list( int, int, int, int, int ) -> ScrolledList

		Create a ScrolledList used to select the specific level that the player can travel to via this level.
		"""
		level_list = ScrolledList(width, height, ListItemCollection()) #TODO: empty collection?
		level_list.topleft = x, y
		#TODO: may want another arg that can be used to populate the list if necessary.
		return level_list

	def direction_buttons(self, x, y):
		""" DTP.direction_buttons( int, int ) -> RadioButton, RadioButton, RadioButton, RadioButton

		Create a set of directional buttons, only one of which can be toggled at a time.
		These are used to determine which direction the player leaves the level from to reach a different dungeon.
		"""
		up_button = RadioButton("Up")
		up_button.topleft = x, y
		down_button = RadioButton("Down", up_button)
		down_button.topleft = up_button.right + 16, y
		left_button = RadioButton("Left", up_button)
		left_button.topleft = down_button.right + 16, y
		right_button = RadioButton("Right", up_button)
		right_button.topleft = left_button.right + 16, y
		return up_button, down_button, left_button, right_button 

	def travel_direction(self):
		""" DTP.travel_direction( ) -> str

		Returns the current direction that this level can be exited from to reach another dungeon.
		"""
		buttons = [self.up_button, self.down_button, self.left_button, self.right_button]
		for b in buttons:
			if b.active: return	b.get_text()
		return None