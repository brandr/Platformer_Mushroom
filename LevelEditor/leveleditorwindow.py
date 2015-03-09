from leveleditorcontainer import *

LEVEL_WIN_WIDTH = 1120	#not sure these are needed (YES THEY ARE)
LEVEL_WIN_HEIGHT = 720

class LevelEditorWindow(Window): 
	def __init__(self, level_select_container, title, level_cell, position, dimensions):
		Window.__init__(self, title)
		self.level_select_container = level_select_container #need this to access click sensitivity
		self.topleft = (position[0], position[1])
		print "Building level editor container..."
		level_editor_container = LevelEditorContainer(self, level_cell, dimensions)
		print "Level editor container built."
		self.set_child(level_editor_container)