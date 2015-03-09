
import levelselectcontainer
from levelselectcontainer import *
import dungeongridcontainer
from dungeongridcontainer import *
from filemanagercontainer import *
from leveleditorscreen import *

DUNGEON_WIN_WIDTH = 1200	  #TEMP (maybe?)
DUNGEON_WIN_HEIGHT = 800 #TEMP

class DungeonEditorScreen:
	def __init__(self, dungeon_renderer):
		self.dungeon_renderer = dungeon_renderer

	def openDungeonEditor(self):
		print "Opening dungeon editor screen..."
		self.initComponents()
		self.dungeon_renderer.start()

	def initComponents(self): #could maybe be static
		print "Intializing dungeon editor components..."
		self.level_select_container = self.level_select_container(32, 32, 312, 400)
		self.dungeon_grid_container = self.dungeon_grid_container(self.level_select_container, self.level_select_container.right + 36, self.level_select_container.top, 350, 400)
		self.file_manager_container = self.file_manager_container(self.level_select_container, self.dungeon_grid_container, self.level_select_container.left, self.level_select_container.bottom + 16, 700, 256)
		print "Dungeon editor components Intialized.", '\n'
		self.dungeon_renderer.add_widget(self.level_select_container)
		self.dungeon_renderer.add_widget(self.dungeon_grid_container)
		self.dungeon_renderer.add_widget(self.file_manager_container)

	def resetEditor(self):
		self.level_select_container.reset()
		self.dungeon_grid_container.reset()

	def resume(self):
		self.adjustSensitivty(True)
		self.file_manager_container.updateFileSelection()

	def adjustSensitivty(self, sensitive):
		self.setSensitivity(self.level_select_container, sensitive)
		self.setSensitivity(self.dungeon_grid_container, sensitive)
		self.setSensitivity(self.file_manager_container, sensitive)

	def setSensitivity(self, component, sensitive):
		state = Constants.STATE_INSENSITIVE
		if(sensitive): state = Constants.STATE_NORMAL
		component.set_state(state)
		component.sensitive = sensitive

	def level_select_container(self, x, y, width, height):
		position = (x, y)
		dimensions = (width, height)
		return LevelSelectContainer(self, position, dimensions)

	def dungeon_grid_container(self, level_select_container, x, y, width, height):
		position = (x, y)
		dimensions = (width, height)
		return DungeonGridContainer(level_select_container, position, dimensions)

	def file_manager_container(self, level_select_container, dungeon_grid_container, x, y, width, height):
		position = (x, y)
		dimensions = (width, height)
		return FileManagerContainer(level_select_container, dungeon_grid_container, position, dimensions)