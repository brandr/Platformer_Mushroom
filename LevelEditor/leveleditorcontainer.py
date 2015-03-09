from levelgridwindow import *
from entityselectcontainer import *
from entitydatapane import *
from dungeontravelpane import DungeonTravelPane

from ocempgui.draw import Image
import os.path

ROOM_CELL_WIDTH = 18
ROOM_CELL_HEIGHT = 18

class LevelEditorContainer(Box):
	def __init__(self, window, level_cell, dimensions):
		Box.__init__(self, dimensions[0], dimensions[1])
		self.master_window = window
		self.level_cell = level_cell
		self.current_bg = self.level_cell.bg_filename
		
		level_name_label = Label(level_cell.get_name())
		print "Building level grid window..."
		self.level_grid_window = self.level_grid_window(self.current_bg)
		print "Level grid windows built."
		self.entity_select_container = self.entity_select_container(self.left + 8, level_name_label.bottom + 8, 360, 240)
		self.travel_pane = self.dungeon_travel_pane(self.entity_select_container.right + 16, level_name_label.bottom + 8, (self.level_grid_window.left - 16 - self.entity_select_container.right), 200)
		self.room_select_grid_window = self.room_select_grid_window(self.travel_pane.left, self.travel_pane.bottom + 4, self.travel_pane.width - 16, 120)
		self.room_select_grid = self.build_room_select_grid()
		self.room_select_grid_window.set_child(self.room_select_grid)
		self.additional_entity_data_pane = self.additional_entity_data_pane(self.level_grid_window.left, self.level_grid_window.bottom + 8, self.level_grid_window.width, 160)
		self.background_select_label = self.background_select_label(self.entity_select_container.left, self.entity_select_container.bottom + 64)
		self.background_select_list = self.build_background_select_list(self.background_select_label.left, self.background_select_label.bottom + 16, self.level_grid_window.left - 16, 120)
		self.invalid_bg_label = Label("")
		self.invalid_bg_label.topleft = self.background_select_list.left, self.background_select_list.bottom + 8
		close_editor_button = self.close_editor_button(self.left + 8, self.bottom - 32) # also consider lower right corner
		self.sunlit = False
		self.sunlit_button = CheckButton("Sunlit")
		self.sunlit_button.connect_signal(SIG_TOGGLED, self.toggleSunlit)
		self.sunlit_button.topleft = (close_editor_button.right + 16, close_editor_button.top)
		self.setSunlit(level_cell.sunlit)
		self.select_room(self.room_select_grid.grid[(0, 0)], 0 , 0)

		self.add_child(level_name_label) # should be self if it can be altered, I think.
		self.add_child(self.level_grid_window)
		self.add_child(self.entity_select_container)
		self.add_child(self.travel_pane)
		self.add_child(self.room_select_grid_window)
		self.add_child(self.additional_entity_data_pane)
		self.add_child(self.background_select_label)
		self.add_child(self.background_select_list)
		self.add_child(self.invalid_bg_label)
		self.add_child(close_editor_button)
		self.add_child(self.sunlit_button)

		#TODO: add something that will allow linkage to another dungeon

	def entity_select_container(self, x, y, width, height):
		container = EntitySelectContainer(width, height) # may need "self" arg
		container.topleft = x, y
		return container

	def dungeon_travel_pane(self, x, y, width, height):
		travel_pane = DungeonTravelPane(width, height)
		travel_pane.topleft = x, y
		travel_pane.initialize_travel_data(self.level_cell.travel_data)
		return travel_pane

	def room_select_grid_window(self, x, y, width, height):
		window = ScrolledWindow(width, height)
		window.topleft = x, y
		window.connect_signal(SIG_MOUSEDOWN, self.click_room_cell)
				
		# TODO: fill the table with imagebuttons that will connect to the levelgrid, changing its bg image to a different subsurface of the full background
		# and displaying entities with a different offset.
		#window.set_child(room_select_grid)
		return window

	def build_room_select_grid(self):
		room_width, room_height = self.level_grid_window.level_grid.get_room_dimensions()
		room_select_grid = Table(room_height, room_width)
		for i in xrange (room_height):
			for j in xrange (room_width):
				cell = self.room_select_cell(i, j)
				room_select_grid.add_child (i, j, cell)
		
		return room_select_grid

	def room_select_cell(self, row, col):
		cell = ImageButton("")
		blank_image = Surface((ROOM_CELL_WIDTH, ROOM_CELL_HEIGHT))
		blank_image.fill(WHITE)
		cell.set_picture(blank_image)
		return cell

	def background_select_label(self, x, y):
		bg_name = "None"
		if self.current_bg: bg_name = self.current_bg
		label = Label("Current background: " + bg_name)
		label.topleft = x, y
		return label

	def build_background_select_list(self, x, y, width, height):
		background_list = FileList(width, height, "./backgrounds")
		background_list.topleft = x, y
		background_list.connect_signal(SIG_SELECTCHANGED, self.select_bg, background_list)
		return background_list
	
	def click_room_cell(self, event):
		if(event.button != LEFT_MOUSE_BUTTON): return
		coords = event.pos
		screen_offset = (self.room_select_grid_window.left + self.left + self.master_window.left, self.room_select_grid_window.top + self.top + self.master_window.top)
		relative_coords = (coords[0] - screen_offset[0], coords[1] - screen_offset[1])
		if relative_coords[0] > self.room_select_grid_window.vscrollbar.left or relative_coords[1] > self.room_select_grid_window.hscrollbar.top: return
		x_scroll_offset = self.room_select_grid_window.hscrollbar.value
		y_scroll_offset = self.room_select_grid_window.vscrollbar.value
		adjusted_coords = (relative_coords[0] + x_scroll_offset, relative_coords[1] + y_scroll_offset) 
		row = int(adjusted_coords[1]/30)
		col = int(adjusted_coords[0]/30)
		if (row, col) not in self.room_select_grid.grid: return None
		cell = self.room_select_grid.grid[(row, col)]
		self.select_room(cell, col, row) #.leftClickDungeonCell(selected_dungeon_cell)

	def select_room(self, room_cell, x, y):
		self.deselect_room_cell()
		cell_image = Surface((ROOM_CELL_WIDTH, ROOM_CELL_HEIGHT))
		cell_image.fill(RED)
		room_cell.set_picture(cell_image)
		self.level_grid_window.level_grid.select_room(x, y)
		#TODO: select the room, altering:
		# 1. the level grid's background image
		# 2. the entities blitted onto the level grid
		# 3. where entities added to the level should be placed.

	def deselect_room_cell(self):
		x, y = self.level_grid_window.level_grid.room_x, self.level_grid_window.level_grid.room_y
		cell_image = Surface((ROOM_CELL_WIDTH, ROOM_CELL_HEIGHT))
		cell_image.fill(WHITE)
		self.room_select_grid.grid[y, x].set_picture(cell_image)

	def select_bg(self, file_list):
		if self.background_select_list.get_selected() == None:
			bg_filename = None
		else: 
			bg_filename = self.background_select_list.get_selected()[0]._text
		if not bg_filename or not os.path.isfile("./backgrounds/" + bg_filename): return
		bg_image = Image.load_image("./backgrounds/" + bg_filename)
		level_dimensions = self.level_grid_window.level_grid.get_room_dimensions()
		bg_dimensions = bg_image.get_width()/32/ROOM_WIDTH, bg_image.get_height()/32/ROOM_HEIGHT
		if level_dimensions == bg_dimensions:
			self.cancel_invalid_bg()
			self.set_bg(bg_filename)
		else: self.display_invalid_bg()

	def set_bg(self, filename):
		self.current_bg = filename
		self.level_cell.bg_filename = filename
		self.background_select_label.set_text("Current background: " + filename)
		self.level_grid_window.set_bg(filename)

	def display_invalid_bg(self):
		self.invalid_bg_label.set_text("Invalid background size.")

	def cancel_invalid_bg(self):
		self.invalid_bg_label.set_text("")

	def close_editor_button(self, x, y):
		button = Button("Close and Save")
		button.topleft = x,y
		button.connect_signal(SIG_CLICKED, self.closeEditor)
		return button

	def additional_entity_data_pane(self, x, y, width, height):
		data_pane = EntityDataPane(width, height)
		data_pane.topleft = x, y
		return data_pane

	def select_tile(self, tile):
		self.additional_entity_data_pane.select_tile(tile)

	def deselect_tile(self):
		self.additional_entity_data_pane.deselect_tile()

	def closeEditor(self):	
		self.additional_entity_data_pane.save_data()
		self.level_cell.bg_filename = self.current_bg
		self.master_window.level_select_container.resume()
		self.level_cell.updateSunlit(self.sunlit)
		travel_data = self.travel_pane.build_travel_data()
		self.level_cell.update_travel_data(travel_data)
		self.master_window.destroy()

	def level_grid_window(self, bg_filename):
		window = LevelGridWindow(self, self.right - 480, self.top + 8, 420, 420, bg_filename) 
		return window

	def setSunlit(self, sunlit):
		if(sunlit): self.sunlit_button.activate()

	def toggleSunlit(self):
		self.sunlit = not(self.sunlit)