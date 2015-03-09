""" Data specifically used to generate platforms. Special platforms might be icy, possible to pass through, moving, etc.
"""

from tiledata import TileData

DESTROY_LIGHT_FLASH = "destroy_light_flash"
DESTROY_STEP_ON = "destroy_step_on"

class PlatformData(TileData):
	""" PlatformData( str, str, str ) -> PlatformData

	Currently the same as TileData, but subject to change.
	"""
	def __init__(self, key, filepath, filepath_start = "./"):
		TileData.__init__(self, key, filepath, filepath_start)

	def create_copy(self):
		""" pd.create_copy( ) -> PlatformData

		Create a copy of the PlatformData.
		"""
		copy_platform = PlatformData(self.entity_key, self.image_filepath)
		#TODO: set whatever platform data belongs here if necessary.
		return copy_platform

	def formatted_data(self):
		""" pd.formatted_data( ) -> ( str, str, int, int  )

		Format this platformdata into primitive types so that it can be saved to a file.
		"""
		return (self.entity_key, self.image_filepath, self.width, self.height) 

class DestructiblePlatformData(PlatformData):
	""" DestructiblePlatformData( str, str, str ) -> DestructiblePlatformData

	A special data type used to generate platforms that can be destroyed in some way.
	"""
	def __init__(self, key, filepath, filepath_start = "./"):
		PlatformData.__init__(self, key, filepath, filepath_start)
		self.catalyst = None

	def create_copy(self):
		""" dpd.create_copy( ) -> DestructiblePlatformData

		Create a copy of the DestructiblePlatformData.
		"""
		copy_platform = DestructiblePlatformData(self.entity_key, self.image_filepath)
		copy_platform.catalyst = self.catalyst
		return copy_platform

	def formatted_data(self):
		""" dpd.formatted_data( ) -> ( str, str, int, int, str  )

		Format this platformdata into primitive types so that it can be saved to a file.
		"""
		return (self.entity_key, self.image_filepath, self.width, self.height, self.catalyst) 