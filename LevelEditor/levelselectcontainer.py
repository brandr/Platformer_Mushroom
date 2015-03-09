import levelselectcell
from levelselectcell import *
from leveleditorwindow import *
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

MAX_LEVELS = 99

#TODO:consider separating out the levelselectwindow into its own class....
class LevelSelectContainer(Box):
	def __init__(self, editor_screen, position, dimensions):
		Box.__init__(self, dimensions[0], dimensions[1])
		self.topleft = (position[0], position[1])

		self.editor_screen = editor_screen
		self.level_count = 0
		self.selected_level_cell = None #TODO: make it possible to select a level cell (and make it visually clear which one is selected)

		level_select_label = Label("Dungeon Levels:")

		self.level_data_table = Table(MAX_LEVELS, 1)
		self.level_window_dimensions = (dimensions[0] - 36,dimensions[1] - 200,self.level_data_table)
		self.level_window = self.create_level_window(self.level_window_dimensions[0], self.level_window_dimensions[1], self.level_data_table)
		self.selected_level_label = self.selected_level_label(self.level_window.left, self.level_window.bottom + 12)

		self.add_level_button = self.add_level_button(224, 6)
		self.rename_level_button = self.rename_level_button(self.selected_level_label.left, self.selected_level_label.bottom + 8)
		self.level_name_entry = self.rename_level_entry_field(self.rename_level_button.right + 8, self.rename_level_button.top)
		self.edit_level_button = self.edit_level_button(self.rename_level_button.left, self.rename_level_button.bottom + 8)

		self.add_child(level_select_label)
		self.add_child(self.level_window)
		self.add_child(self.selected_level_label)

		self.add_child(self.add_level_button)
		self.add_child(self.rename_level_button)
		self.add_child(self.level_name_entry)
		self.add_child(self.edit_level_button)

		#TODO: resize level button (not sure this is necessary, since levels are resizable already.)
		#TODO: delete level button(NICK)
		#TODO: buttons for any levelData attributes external to rooms (though maybe these should be in the level editor)
		#TODO: whatever other useful buttons we can think of

		self.dungeon_grid_container = None #might just use the actual grid, not sure yet
		self.updateSelectedLevel()

	#buttons/entry fields

	def add_level_button(self, x, y):
		button = Button("Add a level")
		button.topleft = (x, y)
		button.connect_signal (SIG_CLICKED, self.addLevel)
		return button

	def rename_level_button(self, x, y):
		button = Button("Rename")
		button.topleft = x, y
		button.connect_signal(SIG_CLICKED, self.renameSelectedLevel)
		return button

	def rename_level_entry_field(self, x, y):
		entry = Entry(self.selected_level_string())
		entry.topleft = x, y
		return entry

	def edit_level_button(self, x, y):
		button = Button("Edit Level")
		button.topleft = x, y
		button.connect_signal(SIG_CLICKED, self.editSelectedLevel)
		return button

	#level window
	#not to be confused with level editor window
	def create_level_window(self, width, height, level_data_table):
		window = ScrolledWindow(width,height)
		window.set_child(level_data_table)
		window.connect_signal(SIG_MOUSEDOWN,self.clickLevelCell)
		window.topleft = (18, 45)
		return window

	def selected_level_label(self, x, y):
		label = Label("Selected Level:              ")
		label.topleft = x, y
		return label

	def selected_level_string(self):
		if(self.selected_level_cell == None): return "None"
		return self.selected_level_cell.get_name()

		#data about the levels (used for saving/loading the dungeon)

	def level_save_data(self):
		data_set = []
		rows = self.level_data_table._rows
		for y in xrange(rows):
			cell = self.level_data_table.grid[(y, 0)]
			if(cell != None): 
				next_data = cell.get_level_data()  # cell's type is LevelSelectCell
				data_set.append(next_data)	       # might have a check for empty or otherwise invalid levels before doing this
		return data_set

		#reset the levels

	def reset(self):
		self.clearLevelTable()
		self.level_count = 0
		self.selected_level_cell = None
		self.updateSelectedLevel(False)
	
	def clearLevelTable(self):
		rows = self.level_data_table._rows
		for y in xrange(rows):
			cell = self.level_data_table.grid[(y, 0)]
			if(cell != None): self.level_data_table.remove_child(cell)

	def addLevel(self, level_data = None):
		if level_data == None:
			level_name = "level " + str(self.level_count)
			level_data = LevelData(level_name, (0, 0), (0, 0)) # these coords shouldn't matter
			added_level_cell = LevelSelectCell(level_data)
			self.level_data_table.add_child(self.level_count, 0, added_level_cell)
			self.level_count += 1
			return
		added_level_cell = LevelSelectCell(level_data)#level_data.name, level_data.sunlit, level_data.bg_filename)	# it might later be better just to take the whole leveldata as an arg, so I'll try it for now
		self.level_data_table.add_child(self.level_count, 0, added_level_cell)
		self.level_count += 1

	def setLevels(self, level_data_set): #used when building the dungeon from a save file.
		self.clearLevelTable()
		dungeon_grid = self.dungeon_grid_container.dungeon_grid
		for L in xrange(len(level_data_set)):
			next_level = level_data_set[L]
			self.addLevel(next_level)
			self.selected_level_cell = self.level_data_table.grid[(L,0 )]
			if next_level != None and next_level.corners != None:
				dungeon_grid.setLevelRooms(next_level.corners)
				self.selected_level_cell.room_cells = dungeon_grid.selected_cells
				dungeon_grid.deselect_all_cells()
		self.selected_level_cell = None

	def renameSelectedLevel(self):
		if(self.selected_level_cell == None): return
		new_level_name = self.level_name_entry.text
		self.selected_level_cell.rename_level(new_level_name)
		self.updateSelectedLevel()

	def editSelectedLevel(self):
		title = "Level Editor" #might have title vary more and include level's name
		print "Openining level editor..."
		level_editor_window = LevelEditorWindow(self, title, self.selected_level_cell, (32, 32), (LEVEL_WIN_WIDTH, LEVEL_WIN_HEIGHT))	#TODO: fix lag
		level_editor_window.depth = 1
		self.editor_screen.dungeon_renderer.add_widget(level_editor_window)
		self.editor_screen.adjustSensitivty(False)
		print "Level editor opened."

	def clickLevelCell(self, event):
		coords = event.pos
		screen_offset = (self.left + self.level_window.left,self.top + self.level_window.top)
		relative_coords = (coords[0] - screen_offset[0], coords[1] - screen_offset[1])
		if relative_coords[0] > self.level_window.vscrollbar.left or relative_coords[1] > self.level_window.hscrollbar.top: return
		y_scroll_offset = self.level_window.vscrollbar.value
		# adjusted coords represent the coordinates of the clicked cell, in pixels, 
		# assuming that 0,0 is the upper left of the top cell (regardless of scrolling).
		adjusted_coords = (relative_coords[0],relative_coords[1] + y_scroll_offset) 
		selected_level_cell = self.cell_at(adjusted_coords) 
		self.selectLevelCell(selected_level_cell)

	def selectLevelCell(self, level_cell):
		if level_cell == None or self.selected_level_cell == level_cell:
			self.updateSelectedLevel()
			return 
		if(self.selected_level_cell != None):
			self.selected_level_cell.deselect()
		level_cell.select()
		self.selected_level_cell = level_cell
		self.updateSelectedLevel()

	def updateSelectedLevel(self, reset_rooms = True):
		self.selected_level_label.set_text("Selected Level: " + self.selected_level_string())
		self.level_name_entry.set_text(self.selected_level_string())
		
		rename_sensitive = (self.selected_level_cell != None)
		edit_level_sensitive = (self.selected_level_cell != None and self.selected_level_cell.room_cells != None)
		
		self.setSensitivity(self.rename_level_button, rename_sensitive)
		self.setSensitivity(self.level_name_entry, rename_sensitive)
		self.setSensitivity(self.edit_level_button, edit_level_sensitive)

		if self.dungeon_grid_container != None and reset_rooms:
			self.dungeon_grid_container.dungeon_grid.resetRooms()

	def setSensitivity(self, component, sensitive):
		state = Constants.STATE_INSENSITIVE
		if(sensitive): state = Constants.STATE_NORMAL
		component.set_state(state)
		component.sensitive = sensitive

	def resume(self):
		self.editor_screen.resume()
		if self.selected_level_cell != None: self.selected_level_cell.select()
		self.dungeon_grid_container.dungeon_grid.updateSelectedCells()

	def cell_at(self, coords):
		height = CELL_HEIGHT + 2
		row = int(coords[1]/height)
		col = 0	#since the level data cells have only one column, we always use the first index.
		if (row, col) not in self.level_data_table.grid: return
		cell = self.level_data_table.grid[(row, col)]
		return cell

	@staticmethod
	def empty_level_table():
		table = Table (1, 1)
		table.spacing = 5
		table.topleft = 5, 5
		return table