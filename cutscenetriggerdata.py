# TODO: cutscene trigger data instead of sign data

from tiledata import *
import cutscenescripts

class CutsceneTriggerData(TileData):
	""" TODO: docstring"""
	def __init__(self, key, filepath, filepath_start = "./"):
		TileData.__init__(self, key, filepath, filepath_start)
		self.cutscene_key = None

	def create_copy(self):
		copy_trigger = CutsceneTriggerData(self.entity_key, self.image_filepath)
		copy_trigger.cutscene_key = self.cutscene_key
		return copy_trigger

	def formatted_data(self):
		return (self.entity_key, self.image_filepath, self.width, self.height, self.cutscene_key) 