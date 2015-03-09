from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

import json
from json import *
from os import path

from dungeondata import *

DEFAULT_FILE_COUNT = 10

# use Json to read/write files containing DungeonData objects.
# "Another variant of the dumps() function, called dump(), simply serializes the object to a file. So if f is a file object opened for writing, we can do this:
# json.dump(x, f)
# To decode the object again, if f is a file object which has been opened for reading:
# x = json.load(f)"

class FileManagerContainer(Box):
	"""docstring for FileManagerContainer"""
	def __init__(self, level_select_container, dungeon_grid_container, position, dimensions):
		#init basic attributes
		Box.__init__(self, dimensions[0], dimensions[1])
		self.topleft = (position[0], position[1])
		
		#init data specific to this container
		self.level_select_container, self.dungeon_grid_container = level_select_container, dungeon_grid_container

		#create components
		self.new_dungeon_button = self.new_dungeon_button(8, 8)
		self.save_dungeon_button = self.save_dungeon_button(self.new_dungeon_button.right + 16, self.new_dungeon_button.top)
		self.load_dungeon_button = self.load_dungeon_button(self.save_dungeon_button.right + 16, self.save_dungeon_button.top)
		self.current_file_label = self.current_file_label(dimensions[0] - 320, 8)
		self.filename_entry = self.filename_entry(self.current_file_label.right + 8, self.current_file_label.top - 4)
		self.file_select_window = self.file_select_window(self.current_file_label.left, self.current_file_label.bottom + 8)
		
		#TODO: delete dungeon data button? Other buttons?

		#add components to contaier
		self.add_child(self.new_dungeon_button)
		self.add_child(self.save_dungeon_button)
		self.add_child(self.load_dungeon_button)
		self.add_child(self.file_select_window)
		self.add_child(self.filename_entry)
		self.add_child(self.current_file_label)
		
		self.updateFileSelection()

	#methods for making GUI components

	def new_dungeon_button(self, x, y):
		button = Button("New Dungeon")
		button.topleft = x, y
		button.connect_signal(SIG_CLICKED, self.level_select_container.editor_screen.resetEditor) 
		return button

	def save_dungeon_button(self, x, y):
		button = Button("Save Dungeon")
		button.topleft = x, y
		button.connect_signal(SIG_CLICKED, self.saveDungeon)
		return button

	def load_dungeon_button(self, x, y):
		button = Button("Load Dungeon")
		button.topleft = x, y
		button.connect_signal(SIG_CLICKED, self.loadDungeon)
		return button

	def file_select_window(self, x, y): 
		file_list = FileList (280, 72, "./dungeon_map_files")
		file_list.topleft = x, y
		file_list.connect_signal(SIG_SELECTCHANGED, self.change_selection, file_list)
		return file_list

	def current_file_label(self, x, y):
		label = Label ("Selected save: ")
		label.topleft = x, y
		return label

	def filename_entry(self, x, y):
		entry = Entry("                  ") # all these spaces are only to set the size
		entry.set_text("")
		entry.topleft = x, y
		return entry

	#methods that affect components

	def setSensitivity(self, component, sensitive):
		state = Constants.STATE_INSENSITIVE
		if(sensitive): state = Constants.STATE_NORMAL
		component.set_state(state)
		component.sensitive = sensitive

	#save-related methods

	def saveDungeon(self):
		current_filename = self.current_filename()
		if current_filename == None: return
		print "Saving dungeon..."
		filename = "./dungeon_map_files/" + current_filename
		dungeon_file = open(filename, 'wb') #'wb' means "write binary"
		dungeon_data = self.dungeon_save_data()
		save_data = dungeon_data.formatted_data()
		json.dump(save_data, dungeon_file)
		self.file_select_window.set_directory('./dungeon_map_files')
		#TODO: update the save pane here.
		dev_filepath = "/home/robert/Documents/python_stuff/Platformer_Mushroom_Hero/dungeon_map_files"
		if(path.exists(dev_filepath)):
			dev_filename = dev_filepath + "/" + current_filename
			print "Saving dungeon for the developers..."
			dev_dungeon_file = open(dev_filename,'wb') #'wb' means "write binary"
			json.dump(save_data, dev_dungeon_file)
		else:
			print "ERROR: failed to save for developers."

		print "Dungeon saved. \n"

	def dungeon_save_data(self): #return a DungeonData object used for reading/writing files
		#TODO: (make sure to deal with ununsed rooms/levels properly when building the DungeonData)
		level_data_set = self.level_select_container.level_save_data() 
		room_data_set = self.dungeon_grid_container.room_save_data() 
		dungeon_data = DungeonData(level_data_set, room_data_set)
		return dungeon_data

	#load method

	def loadDungeon(self):
		current_filename = self.current_filename()
		if current_filename == None: return
		filename = "./dungeon_map_files/" + current_filename
		deformatted_dungeon = FileManagerContainer.dungeonDataFromFile(filename)
		self.buildDungeon(deformatted_dungeon)

	@staticmethod
	def dungeonDataFromFile(filename, filepath = "./"):
		dungeon_file = open(filename, 'rb') #'rb' means "read binary"
		dungeon_data = json.load(dungeon_file) #this part reads the data from file
		deformatted_dungeon = DungeonData.deformatted_dungeon(dungeon_data, filepath)
		return deformatted_dungeon

	def buildDungeon(self, dungeon_data): #uncomment the prints in this method to test load times.
		if dungeon_data == None: return
		print "Building dungeon..."
		level_data_set = dungeon_data.level_data_set
		room_data_set = dungeon_data.rooms
		print "Resetting the editor..."
		self.level_select_container.editor_screen.resetEditor()
		self.dungeon_grid_container.setRooms(room_data_set) 
		print "Loading levels..."
		self.level_select_container.setLevels(level_data_set) 
		print "Dungeon built. \n"

	#methods for file slot selection

	def current_filename(self):
		return self.filename_entry._text

	def change_selection(self, window):
		selected_file = self.file_select_window.get_selected()
		filename = selected_file[0]._text
		self.filename_entry.set_text(filename)	# error checking?
		self.updateFileSelection()

	def updateFileSelection(self):
		current_filename = self.current_filename()
		valid_filename = current_filename != None and len(current_filename) > 0	and current_filename != ".." #TODO: consider checking for spaces and stuff too
		self.setSensitivity(self.save_dungeon_button, valid_filename)
		self.setSensitivity(self.load_dungeon_button, valid_filename)
