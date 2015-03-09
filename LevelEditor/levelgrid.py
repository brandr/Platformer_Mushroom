from leveltilecell import *
from roomdata import *
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.draw import Image

LEFT_MOUSE_BUTTON = 1      #NOTE: this variable is repeated in dungeongridcontainer.py. Not sure if this could become a problem.
RIGHT_MOUSE_BUTTON = 3

TILE_WIDTH, TILE_HEIGHT = 32, 32
WHITE = Color(("#FFFFFF"))
BLACK = Color(("#000000"))
RED = Color(("#FF0000"))

class LevelGrid(ImageLabel):	# maybe this should be a table instead? not sure
	def __init__(self, level_editor):
		print "Creating level grid..."
		self.level_editor = level_editor
		self.selected_tile, self.selected_row, self.selected_col = None, 0, 0
		self.room_x, self.room_y = 0, 0
		room_cols, room_rows = self.get_room_dimensions()
		self.full_image = LevelGrid.empty_grid_image(room_cols*ROOM_WIDTH, room_rows*ROOM_HEIGHT)
		self.bg_grid = self.build_bg_grid(room_cols, room_rows)	
		self.cols, self.rows = ROOM_WIDTH, ROOM_HEIGHT
		self.grid_image = Surface((ROOM_WIDTH*32, ROOM_HEIGHT*32))
		ImageLabel.__init__(self, self.grid_image)
		self.refresh_bg()
		print "Level grid created."

	def init_components(self, bg_filename):		
		self.set_bg(bg_filename)

	def build_bg_grid(self, cols, rows):
		grid = []
		for y in xrange(rows):
			grid.append([])
			for x in xrange(cols):
				grid[y].append(None)
		grid[0][0] = self.build_room_image(0, 0)
		return grid

	def build_room_image(self, x, y):
		image = Surface((ROOM_WIDTH*TILE_WIDTH, ROOM_HEIGHT*TILE_HEIGHT))
		sub_image = self.full_image.subsurface(Rect(x*ROOM_WIDTH*TILE_WIDTH, y*ROOM_HEIGHT*TILE_HEIGHT, ROOM_WIDTH*TILE_WIDTH, ROOM_HEIGHT*TILE_HEIGHT))
		image.blit(sub_image, (0, 0))
		return image

	def drawGridlines(self):
		pixel_width, pixel_height = self.get_pixel_width(), self.get_pixel_height()
		for x in range(0, self.cols): pygame.draw.line(self.grid_image, BLACK, (x*TILE_WIDTH, 0), (x*TILE_HEIGHT, pixel_height))
		for y in range (0, self.rows): pygame.draw.line(self.grid_image, BLACK, (0, y*TILE_HEIGHT), (pixel_width, y*TILE_HEIGHT))

	def get_pixel_width(self):
		return self.cols*TILE_WIDTH

	def get_pixel_height(self):
		return self.rows*TILE_HEIGHT
		
	def init_cells(self, room_cells): 
		cell = room_cells[self.room_y][self.room_x]
		self.add_room(cell)

	def set_bg(self, filename):
		if filename: self.full_image = LevelGrid.bg_grid_image(filename)
		else:
			room_cols, room_rows = self.get_room_dimensions() 
			self.full_image = LevelGrid.empty_grid_image(self.cols*room_cols, self.rows*room_rows)
		room_cols, room_rows = self.get_room_dimensions()
		self.bg_grid = self.build_bg_grid(room_cols, room_rows)
		self.refresh_bg()

	def refresh_bg(self):
		current_room_bg = self.bg_grid[self.room_y][self.room_x]
		if not current_room_bg: 
			self.bg_grid[self.room_y][self.room_x] = self.build_room_image(self.room_x, self.room_y)
			current_room_bg = self.bg_grid[self.room_y][self.room_x]
		self.grid_image.blit( current_room_bg, ( 0, 0) )
		room_cells = self.level_cell().aligned_rooms()
		self.init_cells(room_cells)
		self.drawGridlines()
		self.set_picture(self.grid_image)

	def add_room(self, room_cell):
		if room_cell.room_data == None:
			room_cell.init_room_data(ROOM_WIDTH, ROOM_HEIGHT)
			return
		room_data = room_cell.room_data
		for y in xrange (ROOM_HEIGHT):
			for x in xrange(ROOM_WIDTH):
				tile_data = room_data.tile_at(x, y)
				if tile_data == None: continue
				self.add_tile_cell(tile_data, x, y)

	def select_room(self, x, y):
		self.room_x, self.room_y = x, y
		self.refresh_bg()
		#TODO: redraw the room with correct bg subsurface etc. 

	def add_tile_cell(self, tile_data, x, y):
		if(tile_data == None or isinstance(tile_data, BlockedTileData)): return
		self.updateTileImage(tile_data.get_image(), x, y)

	def updateTileImage(self, tile_image, x, y):
		pygame.draw.line(tile_image, BLACK, (0, 0), (0, TILE_HEIGHT))
		pygame.draw.line(tile_image, BLACK, (0, 0), (TILE_WIDTH, 0))
		self.grid_image.blit(tile_image, (x*TILE_WIDTH, y*TILE_HEIGHT))
		self.set_picture(self.grid_image)

	def level_cell(self):
		return self.level_editor.level_cell

	def get_room_dimensions(self):
		level_cell = self.level_cell()
		room_cells = level_cell.room_cells
		x1, y1 = level_cell.origin()
		width, height = 0, 0
		for y in range(y1, len(room_cells)):
			height += 1
		for x in range(x1, len(room_cells[0])):
			width += 1
		return width, height

	def create_cell(self, tile_data):
		cell = LevelTileCell(tile_data)
		return cell

	def valid_coords(self, coords):
		return coords[0] >= 0 and coords[0] < self.cols and coords[1] >= 0 and coords[1] < self.rows

	def processClick(self, event, calculate_offset, bg_filename): #TODO: somewhere in here (or related methods), load additional data if necessary.
		offset = calculate_offset()
		pos = event.pos 
		adjusted_pos = ((pos[0] - offset[0] - 3, pos[1] - offset[1] + 15)) # this bit is still a little wonky, but functional for now.
		coordinate_x = int(adjusted_pos[0]/(TILE_WIDTH))
		coordinate_y = int(adjusted_pos[1]/(TILE_HEIGHT))
		coordinate_pos = (coordinate_x, coordinate_y) 
		if not self.valid_coords(coordinate_pos):return
		if event.button == LEFT_MOUSE_BUTTON:
			self.leftClick(coordinate_pos[1], coordinate_pos[0])
		elif event.button == RIGHT_MOUSE_BUTTON: self.rightClick(coordinate_pos[1], coordinate_pos[0], bg_filename)
		else: self.leftClick(coordinate_pos[1], coordinate_pos[0]) # middle mouse case
			#TODO: other click types

	def leftClick(self, row, col):
		global_row, global_col = row + self.room_y*self.rows, col + self.room_x*self.cols
		self.deselect()
		existing_tile = self.tile_at(global_row, global_col)
		if existing_tile != None: 
			if isinstance(existing_tile, BlockedTileData):
				row, col = existing_tile.origin_y%self.rows, existing_tile.origin_x%self.cols
				existing_tile = existing_tile.origin_tile
			self.select_cell(row, col)
			return
		tile = self.level_editor.entity_select_container.current_entity 
		if (tile == None): 
			return
		elif not self.room_for_tile(tile, row, col):
			return
		self.addEntity(tile, row, col)

	def select_cell(self, row, col):
		global_row, global_col = row + self.room_y*self.rows, col + self.room_x*self.cols
		tile_data = self.tile_at(global_row, global_col)
		if tile_data == None: return
		if isinstance(tile_data, BlockedTileData):
			row, col = tile_data.origin_y%self.rows, tile_data.origin_x%self.cols
			tile_data = tile_data.origin_tile
			global_row, global_col = row + self.room_y*self.rows, col + self.room_x*self.cols
		self.selected_tile, self.selected_row, self.selected_col = tile_data, row, col
		self.level_editor.select_tile(tile_data)
		self.outline_selection(row, col, tile_data) #NOTE: this part will not work for sprites over 1X1
		self.set_picture(self.grid_image)

	def deselect(self):
		#TODO: get tile, row and col from somewhere (should probably be data members of this class)
		tile, row, col = self.selected_tile, self.selected_row, self.selected_col
		if tile == None: return
		image = tile.get_image() 		# this part only needs to be done once.
		self.drawGridlines()
		self.updateTileImage(image, col, row)
		self.selected_tile, self.selected_row, self.selected_col = None, 0, 0
		self.level_editor.deselect_tile() 

	def outline_selection(self, row, col, tile_data):
		self.drawGridlines()
		entity_width, entity_height = tile_data.width, tile_data.height

		p1 = (col*TILE_WIDTH, row*TILE_HEIGHT)
		p2 = (col*TILE_WIDTH + entity_width*TILE_WIDTH - 1, row*TILE_HEIGHT)
		p3 = (col*TILE_WIDTH, row*TILE_HEIGHT + entity_height*TILE_HEIGHT - 1)
		p4 = (col*TILE_WIDTH + entity_width*TILE_WIDTH - 1, row*TILE_HEIGHT + entity_height*TILE_HEIGHT - 1)

		pygame.draw.line(self.grid_image, RED, p1, p2, 2)
		pygame.draw.line(self.grid_image, RED, p4, p2, 2)
		pygame.draw.line(self.grid_image, RED, p1, p3, 2)
		pygame.draw.line(self.grid_image, RED, p4, p3, 2)

	def addEntity(self, template, row, col):
		#TODO: test that this is right
		global_row, global_col = row + self.room_y*self.rows, col + self.room_x*self.cols
		self.deselect()
		tile = template.create_copy()
		width, height = tile.width, tile.height
		self.level_cell().add_entity(tile, global_col, global_row) 	# this will be important to setting data differently for different signs
		for x in range(global_col + 1, global_col + width):
			next_block = BlockedTileData(tile, global_col, global_row)
			self.level_cell().add_entity(next_block, x, global_row)
		for y in range(global_row + 1,  global_row + height):
			for x in range(global_row, global_col + width):
				next_block = BlockedTileData(tile, global_col, global_row)
				self.level_cell().add_entity(next_block, x, y)
		tile_image = tile.get_image() 						# this part only needs to be done once
		self.drawGridlines()
		self.updateTileImage(tile_image, col, row)

	def rightClick(self, row, col, bg_filename):
		#TODO: test
		global_row, global_col = row + self.room_y*self.rows, col + self.room_x*self.cols
		tile = self.tile_at(global_row, global_col)
		if tile == None: return
		if(isinstance(tile, BlockedTileData)):
			origin_tile = tile.origin_tile
			self.removeEntity(tile.origin_y, tile.origin_x, origin_tile.width, origin_tile.height)
			return
		self.removeEntity(row, col, tile.width, tile.height)

	def removeEntity(self, row, col, width, height):
		global_row, global_col = row + self.room_y*self.rows, col + self.room_x*self.cols
		tile = self.tile_at(global_row, global_col)
		if tile == self.selected_tile: self.deselect()
		for y in range(global_row, global_row + height):
			for x in range(global_col, global_col + width):
				self.level_cell().add_entity(None, x, y) 
				tile_image = LevelGrid.empty_tile_image()
				bg = self.bg_grid[self.room_y][self.room_x]
				if bg: tile_image.blit( bg.subsurface( Rect((x%self.cols)*32, (y%self.rows)*32, 32, 32) ), (0, 0) ) 
				self.updateTileImage(tile_image, x%self.cols, y%self.rows)

	def room_for_tile(self, tile, row, col): #make sure any tile larger that 1x1 will fit in the room.
		end_x = col + tile.width - 1
		end_y = row + tile.height - 1
		if not (end_x < self.cols and end_y < self.rows): return False
		for x in range(col + 1, end_x):
			check_tile = self.tile_at(row, x)
			if check_tile != None: return False
		for y in range(row + 1,  end_y + 1):
			for x in range(col, end_x + 1):
				check_tile = self.tile_at(y, x)
				if check_tile != None: return False
		return True

	def tile_at(self, row, col):
		return self.level_cell().tile_at(col, row)

	@staticmethod
	def empty_grid_image(cols, rows):
		image = Surface((cols*TILE_WIDTH, rows*TILE_HEIGHT))
		image.fill(WHITE)
		return image

	@staticmethod
	def bg_grid_image(filename):
		bg_image = Image.load_image("./backgrounds/" + filename)
		return bg_image

	@staticmethod
	def empty_tile_image():
		image = Surface((TILE_WIDTH, TILE_HEIGHT))
		image.fill(WHITE)
		return image