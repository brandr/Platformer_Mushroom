""" the screen that appears when the player opens its inventory.
"""

from gameimage import GameImage, DEFAULT_COLORKEY
from gamescreen import GameScreen
from dialog import WHITE, BLACK
from inventory import LANTERN, SWORD
import pygame
from pygame import font, Surface, Color

RED = Color("#FF0000")

INVENTORY_PANE_WIDTH, INVENTORY_PANE_HEIGHT = 640, 480
INVENTORY_PANE_X, INVENTORY_PANE_Y = 80, 80
ITEM_GRID_WIDTH, ITEM_GRID_HEIGHT = INVENTORY_PANE_WIDTH - 256, INVENTORY_PANE_HEIGHT - 96
ITEM_GRID_X, ITEM_GRID_Y = 32, 48
INFO_PANE_WIDTH, INFO_PANE_HEIGHT = INVENTORY_PANE_WIDTH - ITEM_GRID_WIDTH - 96, ITEM_GRID_HEIGHT
INFO_PANE_X, INFO_PANE_Y = ITEM_GRID_X + ITEM_GRID_WIDTH + 32, ITEM_GRID_Y

ITEM_CELL_SIZE = 32
ITEM_ROWS, ITEM_COLS = ITEM_GRID_HEIGHT/ITEM_CELL_SIZE, ITEM_GRID_WIDTH/ITEM_CELL_SIZE

class InventoryScreen(GameScreen):
	""" InventoryScreen( ControlManager, Player) -> InventoryScreen

	Shows the inventory screen. Allows some changes to be made, such as the current lantern mode.

	Attributes:

	player: The player whose inventory is being shown.
	"""
	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager) 
		self.player = player
		self.init_item_cells()
		self.inventory_pane = self.build_inventory_pane()
		self.cell_x, self.cell_y = 0, 0
		self.draw_cell_selection()
		self.update()

	def init_item_cells(self):
		""" is.init_item_cells( ) -> [ [ ItemCell ] ]

		Creates a 2D grid of item cells.
		"""
		item_names = self.player.inventory.get_all_item_keys()
		item_count = len(item_names)
		index = 0
		cells = []
		for y in xrange(ITEM_COLS):
			cells.append([])
			for x in xrange(ITEM_ROWS):
				cell = None
				if index < item_count: cell = ItemCell(item_names[index])
				cells[y].append(cell)
				index += 1
		self.item_cells = cells
		
	def update(self):
		""" is.update( ) -> None

		Update the components of the inventory screen.
		"""
		self.draw_bg()
		self.screen_image.blit(self.inventory_pane, (INVENTORY_PANE_X, INVENTORY_PANE_Y))
		self.draw_cell_selection()
		self.draw_info_pane()

	def build_inventory_pane(self):
		""" is.build_inventory_pane( ) -> Surface

		Generates an image representing the player's inventory.
		"""
		pane = Surface( (INVENTORY_PANE_WIDTH, INVENTORY_PANE_HEIGHT) )
		pane.fill(WHITE)
		text_font = font.Font("./fonts/FreeSansBold.ttf", 20)
		text_image = text_font.render("Inventory", 1, BLACK)
		pane.blit(text_image, ( 20, 20 ))
		self.draw_player_items(pane)
		return pane

	def draw_player_items(self, pane):
		""" is.draw_player_items( Surface ) -> None

		Draw the player's owned items onto the inventory pane.
		"""
		item_grid = self.build_item_grid()
		pane.blit(item_grid,( ITEM_GRID_X, ITEM_GRID_Y) )

	def draw_cell_selection(self):
		""" is.draw_cell_selection( ) -> None

		Selects the proper item cell based on the current cell_x and cell_y.
		"""
		self.draw_player_items(self.inventory_pane)
		screen_x, screen_y = ITEM_GRID_X + self.cell_x*ITEM_CELL_SIZE, ITEM_GRID_Y + self.cell_y*ITEM_CELL_SIZE
		points = ((screen_x, screen_y), (screen_x + ITEM_CELL_SIZE - 1, screen_y), (screen_x + ITEM_CELL_SIZE - 1, screen_y + ITEM_CELL_SIZE - 1), (screen_x, screen_y + ITEM_CELL_SIZE - 1))
		pygame.draw.lines(self.inventory_pane, RED, True, points )

	def draw_info_pane(self):
		""" is.draw_info_pane( ) -> None

		If an item is selected, show more info about it in this pane.
		"""
		info_pane = Surface(( INFO_PANE_WIDTH, INFO_PANE_HEIGHT ))
		# TODO: show info about the selected object if there is one
		self.inventory_pane.blit(info_pane, (INFO_PANE_X, INFO_PANE_Y))

	#TODO: consider basing this more directly on the actual 2D cell list once it is implemented.
	def build_item_grid(self):
		""" is.build_item_grid( ) -> Surface

		Generates a grid for showing the player's items.
		"""
		grid = Surface((ITEM_GRID_WIDTH, ITEM_GRID_HEIGHT))
		for y in xrange(ITEM_ROWS):
			for x in xrange(ITEM_COLS):
				cell = self.item_cells[y][x]
				if cell:
					item_image = GameImage.load_image_file("./inventory_images/", cell.item_name + ".bmp")
					item_image.set_colorkey(DEFAULT_COLORKEY)
					item_image.convert()
					grid.blit(item_image, ( x*ITEM_CELL_SIZE, y*ITEM_CELL_SIZE))
		return grid

	def move_cursor(self, direction):
		""" is.move_cursor( ( int, int ) ) -> Surface

		Moves the cursor to select a different item in order to perform some action on it.
		"""
		start_x, start_y = self.cell_x, self.cell_y
		if start_x + direction[0] < 0 or start_x + direction[0] >= ITEM_COLS or start_y + direction[1] < 0 or start_y + direction[1] >= ITEM_ROWS: return
		self.cell_x, self.cell_y = start_x + direction[0], start_y + direction[1]
		self.draw_cell_selection()

class ItemCell():
	""" ItemCell( Str ) -> ItemCell

	A container for items on the inventory screen, used to interface with them in some way.
	"""
	def __init__(self, item_name):
		self.item_name = item_name #TODO: other stuff