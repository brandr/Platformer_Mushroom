# -*- coding: utf-8 -*-
""" A special kind of tiledata specific to signs"""

from tiledata import *

class SignData(TileData):
	""" SignData( str, str, str ) -> SignData

	A special type of tiledata used to generate signs.

	Attrbitues:

	text_panes: A list of strings where each element represents a line of text.
	There can be 4 lines at most.

	"""
	def __init__(self, key, filepath, filepath_start = "./"):
		TileData.__init__(self, key, filepath, filepath_start)
		self.text_panes = [
			["", "", "", ""]
		]

	def create_copy(self):
		""" sd.create_copy( ) -> SignData

		Create a signdata that is identical to this one. This is essentially a deep copy.
		I forget what I used this for, but I'm pretty sure it's important.
		"""
		copy_sign = SignData(self.entity_key, self.image_filepath)
		copy_sign.text_panes = []
		for i in range(len(self.text_panes)):
			copy_sign.text_panes.append([])
			for line in self.text_panes[i]:
				copy_sign.text_panes[i].append(line)
		return copy_sign

	def set_sign_text(self, text_panes):
		""" sd.set_sign_text( [ str ]) -> None

		>using setters in python
		mfw:

		ಠ_ಠ 

		"""
		self.text_panes = text_panes

	def formatted_data(self):
		""" sd.formatted_data( ) -> ( str, str, int, int, [ str ] )

		Format this signdata into primitive types so that it can be saved to a file.
		"""
		return (self.entity_key, self.image_filepath, self.width, self.height, self.text_panes) 