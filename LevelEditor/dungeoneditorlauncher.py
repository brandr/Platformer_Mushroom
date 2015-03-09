import dungeoneditorscreen
from dungeoneditorscreen import *
"""
	#LEVEL EDITOR GRID STUFF

#TODO: Since adding differently rotated platforms is currently annoying, consider ways of rotating selected entities, 
	#  or choosing from a 9x9 grid of possible orientations
	#  this may mean it will be easier to store a tiledata's associated image (or even animation), rather than the filepath.

#IDEA: in the level editor, consider axis labels for the level grid to number rooms/tiles by their coords.

#TODO: make it possible to "paint" entities in the level editor by holding and dragging the mouse.
	#this has proven difficult to do, so consider other shortcuts for drawing many tiles. (like drawing lines)

#TODO: figure out how image transparency will work for leveleditor images.
	# remember that the GameImage method which loads these images has to deal with transparency
		#I forget how it does it, though.

#consider making it possible  to add background tiles of varying sizes (possibly on multiple layers) in the leveleditor.
	#could make this a separate screen and allow the user to toggle back and forth between tiles/entities.
	#If we use layers, make a layer selection area (probably a ScrolledList) containing the layers, along with buttons to
		#toggle their visibilty and a way to select which layer we are on.
			#also move layers up/down, delete/add layers, etc
		#when building a level, we would either: 
			#A) use a TileFactory (maybe with some new methods) to divide up a level's corresponding tile image
				# (saved as one image), or
			#B) store the corresponding 32x32 tile image from the Level Grid's tile view in the same tiledata which stores
				#the entity, and set the Tile's image to this image.
					#Might end up with an EntityData class. Each tileData would have an entitydata to represent
						#its starting entity (*not* the data member called "block", unless the entity is a platform), set to None by default.
		#NOTE: this is low priority since it will have little effect on game mechanics (the player does not interact with the tiles themselves)

	#DUNGEON GRID CONTAINER STUFF

#IDEA: visually indicate which level the player will start in. (may also affect level select container)

#IDEA: give the dungeon grid container a color key explaining what the six different colors mean.

#IDEA: make the deselected color of a dungeon grid tile correspond to its associated level's color.
    #A level's color would be set by the user.

	#LEVEL SELECT CONTAINER STUFF

#TODO: delete level button
	#Nick pls

#IDEA: make it clear somehow which levels are empty (no rooms) in the LevelSelectContainer (not the dungeon grid).
    #could grey out the names of these levels
    #could also find a way to represent levels which contain rooms, but whose rooms have no tile data.

#IDEA: a button to move a level (or set of levels, which would be much more complicated) 
    #while also moving the rooms inside the level.
        #i.e., the level itself would not change at all, but simply be in a different part of the dungeon.

#IDEA: a quick way of deleting everything in each room of a level without deleting or resizing the level itself.

	#MISC STUFF

#NOTE: might end up moving the folder that currently holds sprite data into the LevelEditor folder

#consider a set of "level tags", as well as different "layers" that can be toggled 
	#(i.e.,background layer, platforms layer, and (at dungeon zoom level)
         #a layer which shows which levels contain which rooms)
"""
def load_dungeon_editor():
	pygame.init()
	print "Loading dungeon editor..."
	dungeon_renderer = Renderer()
	dungeon_renderer.create_screen(DUNGEON_WIN_WIDTH, DUNGEON_WIN_HEIGHT)
	dungeon_renderer.title = "Dungeon Editor"
	dungeon_renderer.color = (250, 250, 250)
	dungeon_editor_screen = DungeonEditorScreen(dungeon_renderer)
	dungeon_editor_screen.openDungeonEditor() #add more args if necessary

if __name__ == "__main__":
	load_dungeon_editor()