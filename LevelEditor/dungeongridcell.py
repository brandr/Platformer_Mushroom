from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from pygame import *

from roomdata import *

DUNGEON_CELL_WIDTH = 18
DUNGEON_CELL_HEIGHT = 18

SELECTED = "selected"
SELECTED_EMPTY = "selected_empty"
DESELECTED = "deselected"
DESELECTED_EMPTY = "deselected_empty"
UNUSED = "unused"
UNUSED_EMPTY = "unused_empty"

class DungeonGridCell(ImageButton):
	#a cell that reprensents a room.
	def __init__(self, row, col, start_tile):
		ImageButton.__init__(self, "")
		self.minsize = DUNGEON_CELL_WIDTH, DUNGEON_CELL_HEIGHT
		self.set_picture(start_tile)
		self.level_cell = None
		self.cell_state = UNUSED_EMPTY
		self.row, self.col = row, col
		self.room_data = None

	def init_room_data(self, width, height):
		self.room_data = RoomData(width, height, self.col, self.row)

	def reset(self, row, col):
		if(self.cell_state == UNUSED_EMPTY):return
		self.set_picture(DungeonGridCell.unused_empty_tile())
		self.level_cell = None
		self.cell_state = UNUSED_EMPTY
		self.row, self.col = row, col #not sure this is necessary
		self.room_data = None

	def setRoom(self, room_data):
		if room_data == None: return #not sure if we want this yet
		self.level_cell = None
		self.cell_state = UNUSED_EMPTY
		self.set_picture(DungeonGridCell.unused_empty_tile())
		self.room_data = room_data
		self.cell_state = UNUSED
		self.set_picture(DungeonGridCell.unused_tile())

	def empty(self):
		return self.room_data == None or self.room_data.empty()

	def is_selected(self):
		return self.cell_state == SELECTED or self.cell_state == SELECTED_EMPTY

	def select(self, level_cell):
		self.level_cell = level_cell
		if(self.empty()):
			self.set_picture(DungeonGridCell.selected_empty_tile())
			self.cell_state = SELECTED_EMPTY
			return
		self.set_picture(DungeonGridCell.selected_tile())
		self.cell_state = SELECTED

	def deselect(self, detach_level): 
		if(detach_level):
			self.level_cell = None
		if self.level_cell != None:
			if self.empty():
				self.set_picture(DungeonGridCell.deselected_empty_tile())	#NOTE: could also make the image correspond to the level
				self.cell_state = DESELECTED_EMPTY
				return
			self.set_picture(DungeonGridCell.deselected_tile())	#NOTE: could also make the image correspond to the level
			self.cell_state = DESELECTED 
			return
		if self.empty():
			self.set_picture(DungeonGridCell.unused_empty_tile())
			self.cell_state = UNUSED_EMPTY
			return
		self.set_picture(DungeonGridCell.unused_tile())
		self.cell_state = UNUSED

	def add_entity(self, tile_data, col, row):
		self.room_data.set_tile(tile_data, col, row)

	def tile_at(self, x, y):
		return self.room_data.tile_at(x, y)

	#NOTE: could put these tiles (or just the color codes) in a dict as constants
	@staticmethod
	def selected_tile():
		tile = Surface((DUNGEON_CELL_WIDTH, DUNGEON_CELL_HEIGHT))
		tile.fill(Color("#FF0000"))
		return tile

	@staticmethod
	def selected_empty_tile():
		tile = Surface((DUNGEON_CELL_WIDTH, DUNGEON_CELL_HEIGHT))
		tile.fill(Color("#880000"))
		return tile

	@staticmethod
	def deselected_tile():
		tile = Surface((DUNGEON_CELL_WIDTH, DUNGEON_CELL_HEIGHT))
		tile.fill(Color("#FF0066"))
		return tile

	@staticmethod
	def deselected_empty_tile():
		tile = Surface((DUNGEON_CELL_WIDTH, DUNGEON_CELL_HEIGHT))
		tile.fill(Color("#FF99FF"))
		return tile

	@staticmethod
	def unused_tile():
		tile = Surface((DUNGEON_CELL_WIDTH, DUNGEON_CELL_HEIGHT))
		tile.fill(Color("#444444"))
		return tile

	@staticmethod
	def unused_empty_tile():
		tile = Surface((DUNGEON_CELL_WIDTH, DUNGEON_CELL_HEIGHT))
		tile.fill(Color("#FFFFFF"))
		return tile