from levelgrid import *

class LevelGridWindow(ScrolledWindow):
	def __init__(self, level_editor, x, y, width, height, bg_filename):
		ScrolledWindow.__init__(self, width, height)
		self.topleft = x, y
		
		self.level_grid = LevelGrid(level_editor)	
		print "Adding level grid to window..."
		self.set_child(self.level_grid)		# lots of lag still happening in here for some reason
		print "Level grid added to window."
		self.level_grid.init_components(bg_filename)
		self.master_editor = level_editor
		self.connect_signal(SIG_MOUSEDOWN, self.processClick)

	def setLevelData(self, level_cell):#TODO: build from dungeon grid cells, not level data.
		self.level_grid.setLevelData(level_cell)

	def set_bg(self, filename):
		self.level_grid.set_bg(filename)

	def processClick(self, event):
		check_pos = (event.pos[0] - self.left - 38,event.pos[1] - self.top - 54)
		if check_pos[0] >= self.hscrollbar.top or check_pos[1] >= self.vscrollbar.left: return
		bg_filename = self.master_editor.current_bg
		self.level_grid.processClick(event, self.calculate_offset, bg_filename)

	def calculate_offset(self):
		window_pos = (self.left, self.top)
		x_scroll_offset = self.hscrollbar.value
		y_scroll_offset = self.vscrollbar.value
		container = self.master_editor
		container_offset = (container.left, container.top)
		master_window = container.master_window
		master_window_offset = (master_window.left, master_window.top)
		caption_bar_height = master_window._captionrect.height
		x_total_offset = master_window_offset[0] + container_offset[0] + window_pos[0] - x_scroll_offset
		y_total_offest = master_window_offset[1] + container_offset[1] + window_pos[1] - y_scroll_offset + caption_bar_height
		return (x_total_offset,y_total_offest)