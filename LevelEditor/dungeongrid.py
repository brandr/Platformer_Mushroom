import dungeongridcell
from dungeongridcell import *
#from ocempgui.events import EventManager

class DungeonGrid(Table): #table might not be the best source.
	def __init__(self, level_select_container, rows, cols): #is this the right order for rows and cols? not source
		Table.__init__(self, rows, cols)
		self.level_select_container = level_select_container
		self.spacing = 0
		self.padding = 0
		print "Initializing dungeon grid..."
		self.init_cells()
		print "Dungeon grid Intialized."
		self.rect_corner = None #a corner used to draw rectangular levels
		self.selected_cells = None 

	def init_cells(self):			#NOTE: this is causing most of the lag in the dungeon editor
		tile = DungeonGridCell.unused_empty_tile()
		for i in xrange (self._rows):
			for j in xrange (self._cols):
				cell = DungeonGridCell(i, j, tile)
				self.add_child (i, j, cell)

	def reset_cells(self):
		for i in xrange (self._rows):
			for j in xrange (self._cols):
				self.grid[(i, j)].reset(i, j)

	def reset(self):
		self.reset_cells() 
		self.rect_corner = None
		self.selected_cells = None

	def setRooms(self, room_data_set):
		rows, cols = len(room_data_set), len(room_data_set[0])
		for i in xrange (rows):
			for j in xrange (cols):
				next_room = room_data_set[i][j]
				self.grid[(i, j)].setRoom(next_room)

	def setLevelRooms(self, corners):
		#set the rooms for  the current level based on a pair of corners, rather than user input.
		if corners == None or corners[0] == None or corners[1] == None: return
		corner1 = corners[0]
		corner2 = corners[1]

		x1, y1 = corner1[0], corner1[1]
		x2, y2 = corner2[0], corner2[1]

		level_cell = self.level_cell()
		self.rect_corner = None
		self.deselect_all_cells(False)

		room_cells = []
		for y in range (0, y2 + 1):
			room_cells.append([])
			for x in range (0, x2 + 1):
				room_cells[y].append(None)
		for y in range (y1, y2 + 1):
			for x in range (x1, x2 + 1):
				next_cell = self.grid[(y, x)]
				next_cell.select(level_cell)
				room_cells[y][x] = next_cell

		self.selected_cells = room_cells
		#not sure about this method

	def cell_at(self, coords):
		width = DUNGEON_CELL_WIDTH + 10
		height = DUNGEON_CELL_HEIGHT + 10
		row = int(coords[1]/height)
		col = int(coords[0]/width)
		if (row, col) not in self.grid:
			return None
		cell = self.grid[(row, col)]
		return cell

	def level_cell(self):
		return self.level_select_container.selected_level_cell

	def room_save_data(self):
		data_set = []
		for row in xrange (self._rows):
			data_set.append([])
			for col in xrange (self._cols):
				cell = self.grid[(row,col)]
				data_set[row].append(cell.room_data) #TODO: deal with None room_datas at some point.
		return data_set

	def leftClickDungeonCell(self, cell):
		if(cell == None or cell.cell_state == DESELECTED or cell.cell_state == DESELECTED_EMPTY): return
		if(self.rect_corner != None):
			self.draw_level_rect(cell)
			self.levelSelectUpdate()
			return
		self.deselect_all_cells(True)
		self.set_rect_corner(cell)
		self.levelSelectUpdate()

	def set_rect_corner(self, cell):
		self.rect_corner = cell
		cell.select(self.level_cell())
		self.selected_cells = []
		while len(self.selected_cells) <= cell.row:
				self.selected_cells.append([])
		for y in range (0,cell.row + 1):
			while len(self.selected_cells[y]) <= cell.col:
					self.selected_cells[y].append(None)
		self.selected_cells[cell.row][cell.col] = cell
		#self.levelSelectUpdate()

	#draw a rectangle using the current rect_corner and cell arg as opposite corners
	def draw_level_rect(self, corner2):
		if(corner2 == self.rect_corner):
			self.rect_corner = None
			return
		self.selected_cells = []
		corner1 = self.rect_corner
		x1, x2 = min(corner1.col, corner2.col), max(corner1.col, corner2.col)
		y1, y2 = min(corner1.row, corner2.row), max(corner1.row, corner2.row)
		if not self.valid_level_rect(x1, y1, x2, y2):
			self.rect_corner = None
			return
		while len(self.selected_cells) <= y2:
				self.selected_cells.append([])
		for y in range (0,y2 + 1):
			while len(self.selected_cells[y]) <= x2:
					self.selected_cells[y].append(None)
		level_cell = self.level_cell()
		for y in range (y1, y2 + 1):
			for x in range(x1, x2 + 1):
				next_cell = self.grid[(y, x)]
				self.selected_cells[y][x] = next_cell
				if not next_cell.is_selected():
					next_cell.select(level_cell)
		self.rect_corner = None

	def valid_level_rect(self, x1, y1, x2, y2):
		for y in range (y1, y2 + 1):
			for x in range(x1, x2 + 1):
				next_cell = self.grid[(y, x)]
				if next_cell.level_cell != None and next_cell.level_cell != self.level_cell(): return False
		return True

	def deselect_all_cells(self, detach_level = False): 
		if self.selected_cells == None: return
		width,height = len(self.selected_cells[0]), len(self.selected_cells)
		for y in range (height):#self._rows):
			for x in range(width):
				next_cell = self.grid[(y, x)]
				if next_cell.is_selected():
					next_cell.deselect(detach_level)
		self.selected_cells = None

	def updateSelectedCells(self):
		if self.selected_cells == None: return
		self.rect_corner = None #not sure about this
		level_cell = self.level_cell
		cells = self.selected_cells
		for row in cells:
			for c in row:
				if c != None: c.select(level_cell)

	def levelSelectUpdate(self):
		level_cell = self.level_cell()
		if level_cell == None: return #might need a deselect here
		level_cell.set_rooms(self.selected_cells)
		self.level_select_container.updateSelectedLevel(False)

	def resetRooms(self): #reset currently selected rooms to match currently selected level cell.
		level_cell = self.level_cell()
		self.rect_corner = None
		self.deselect_all_cells(False)
		if(level_cell == None): return
		selected_cells = level_cell.room_cells
		self.selected_cells = selected_cells
		if(selected_cells == None):return
		x2 = len(selected_cells[0])
		y2 = len(selected_cells)
		origin = level_cell.origin()
		x1, y1 = origin[0],origin[1]
		for y in range (y1, y2):
			for x in range (x1, x2):
				next_room = selected_cells[y][x]
				if(next_room != None):
					self.grid[(y, x)].select(level_cell)

	@staticmethod
	def empty_cell(row, col):
		return DungeonGridCell(row, col)