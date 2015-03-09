# this class might be obsolete. Not sure.

from pygame import *
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

class LevelEditorScreen(object):
	def __init__(self,dungeon_screen,level_renderer):
		self.dungeon_screen = dungeon_screen
		self.level_renderer = level_renderer

	def openLevelEditor(self):
		self.initComponents()
		self.level_renderer.start()

	def initComponents(self):
		close_editor_button = self.close_editor_button(32,32) 
		self.level_renderer.add_widget(close_editor_button)	  

	def closeLevelEditor(self):	#might not be using this
		pass
		#self.level_renderer.screen.

	def close_editor_button(self,x,y):
		button = Button("Close Editor")
		button.topleft = x,y
		button.connect_signal(SIG_CLICKED,self.closeLevelEditor)
		return button