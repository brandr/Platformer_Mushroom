""" A special factory that builds dungeons.
"""

import sys
import json

def build_dungeon(filename, dungeon_name):
	""" build_dungeon( str ) -> Dungeon

	Creates a DungeonData object from a file stored in the given file.
	The DungeonData is then used to generate a dungeon.
	"""
	dungeon_data = dungeonDataFromFile(filename)
	level_data_set = dungeon_data.level_data_set
	room_data_set = dungeon_data.rooms
	print "Setting up main level group..."
	return Dungeon(level_data_set, room_data_set, dungeon_name) #could also give the factory itself more of the work than this


def dungeonDataFromFile(filename, filepath = "./"):
	""" dungeonDataFromFile( str, str ) -> DungeonData

	Uses json format to load a dungeon from the given directory.
	"""
	dungeon_file = open(filename, 'rb') 	# 'rb' means "read binary"
	dungeon_data = json.load(dungeon_file) 	# this part reads the data from file
	deformatted_dungeon = DungeonData.deformatted_dungeon(dungeon_data, filepath)
	return deformatted_dungeon

from dungeondata import DungeonData
from dungeon import Dungeon