""" Data relates to chest contents are stored in this file.
"""

from lantern import Lantern

# item constants
ITEM_CLASS = "item_class"
ITEM_KEY = "item_key"
DISPLAY_NAME = "display_name"
RECEIVE_DIALOG_DATA = "receieve_dialog_data"
#TODO: other constants

LANTERN_MAP = {
	ITEM_CLASS:Lantern, 
	ITEM_KEY:"lantern",
	DISPLAY_NAME: "Lantern",
	RECEIVE_DIALOG_DATA:
	[
		[
			"You got a lantern!",
			"It will light up when you travel through dark places.",
			"Using it will drain your lantern oil."
		]
	]
}

MASTER_CHEST_CONTENTS_MAP = {
	"lantern":LANTERN_MAP
}