""" An ingame dialog, as from a sign or a character.
"""

import os
from pygame import font, Color, Surface
from effect import *
from camera import WIN_WIDTH, WIN_HEIGHT

BLACK = Color("#000000") #TEMP
WHITE = Color("#FFFFFF")

SIGN = "sign"
SCROLL_CONSTANT = 2.5
DIALOG_BOX_WIDTH = WIN_WIDTH - 32
DIALOG_BOX_HEIGHT = WIN_HEIGHT/6

class Dialog(Effect):
	""" Dialog( str, str, str, (int, int), bool, Color ) -> Dialog

	A type of ingame effect that appears as a box at the top of the screen, containing text.

	Attributes:

	next_actions: The next set of actions to be executed (simultaneously). Each action contains a reference to the action that comes after it, if there is one.

	index: A measure of how far this dialog has progressed (and therefore how many letters of text should be shown).

	draw_pane: The pane containing the text.

	text: The text to be displayed in this dialog.

	portrait_filename: None if there is no portrait. Otherwise, holds the filename of the portrait image that should be used for the character that is curretly speaking.

	dimensions: width and height of this dialog.

	scrolling: if true, then the text gradually scrolls.

	font_color: the color of the text in this dialog.

	offset: The offset of the dialog box on the screen.
	"""
	def __init__(self, source_type, text = "", portrait_filename = None, dimensions = (0, 0), scrolling = False, font_color = BLACK): #TODO: consider an arg just for the font.
		Effect.__init__(self, Dialog.draw_image)
		self.next_actions = []
		self.index = 0
		self.draw_pane = None
		if source_type in PANE_MAP:
			self.draw_pane = PANE_MAP[source_type]
		self.text = text
		self.portrait_filename = portrait_filename
		self.dimensions = dimensions
		self.scrolling = scrolling
		self.font_color = font_color
		self.offset = (12, 12) #TEMP

	def process_key(self, key):
		""" d.process_key( str ) -> None

		An abstract method that does nothing for dialogs. I think keyboard input is still handled somewhere else, though.
		"""
		pass

		#NOTE: is the source arg really necessary?

	def draw_text_image(self):
		""" d.draw_text_image( ) -> Surface

		Returns a text image representing this dialog.
		"""
		current_text = self.text[0:int(self.index/SCROLL_CONSTANT)] 
		text_lines = [s.strip() for s in current_text.splitlines()]
		text_font = font.Font("./fonts/FreeSansBold.ttf", 20)	#TEMP
		text_image = Surface((self.dimensions[0] - 64, self.dimensions[1])) #TEMPORARY dimensions
		text_image.fill(WHITE)
		for i in range(len(text_lines)): 
			next_line = text_lines[i]
			text_image.blit(text_font.render(text_lines[i], 1, self.font_color), (16, 32*i))
		text_image.convert()
		return text_image

	def draw_image(self, level):
		""" d.draw_image( Level ) -> Surface, (int, int)

		Returns the image of the dialog, along with its offset.
		"""
		pane_image = self.draw_pane(self)
		text_image = self.draw_text_image()
		sign_image = pane_image
		portrait_image = self.load_portrait_image()
		if portrait_image:
			sign_image.blit(portrait_image, (0, 0))
			sign_image.blit(text_image, (72, 0)) #TEMP
			return sign_image, (0, 0)
		sign_image.blit(text_image, (0, 0))
		return sign_image, (0, 0)

	def load_portrait_image(self):
		""" d.load_portrait_image( ) -> Surface

		Returns the image for this dialog's associated portrait, if there is one.
		"""
		if self.portrait_filename:
			return Dialog.load_image_file("./portraits/", self.portrait_filename)
		return None

	def sign_pane_image(self):
		""" d.sign_pane_image( ) -> Surface

		Returns the default image for a sign's dialog pane.
		"""
		pane = Surface(self.dimensions) #TEMP. make it cuter.
		pane.fill(WHITE)
		return pane

	# even though dialog inherits from effect, it shares some methods with GameAction.

	def add_next_action(self, action):
		""" d.add_next_action( GameAction ) -> None

		Adds an action that is about to occur.
		"""
		self.next_actions.append(action)

	def continue_action(self, event, level):
		""" d.continue_action( GameEvent, Level ) -> bool

		This method is called when the player presses X and determines whether the dialog
		box should advance to the next dialog. It also advances the text if it is not done scrolling.
		"""
		if(self.index/SCROLL_CONSTANT <= len(self.text)):
			self.index = int(SCROLL_CONSTANT * len(self.text))
			return True
		event.remove_action(self)
		if self.next_actions:
			level.remove_effect(self)
			for a in self.next_actions:
				event.add_action(a)
				a.execute(level)
			return True
		return False

	def execute(self, level):
		""" d.execute( Level ) -> None

		A method shared by GameAction. In the dialog's case, it causes the dialog to display onscreen.
		"""
		level.display_dialog(self)

	def update(self, event, level):
		""" d.update( GameEvent, Level ) -> None

		Updates the dialog's index, effectively making the text scroll.
		"""
		self.index += 1

	@staticmethod
	def load_image_file(path, name, colorkey = None):
		""" load_image_file( str, str, str ) -> Surface

		If a valid filepath is given, loads an image from it.
		This is used to load portraits.
		"""
		fullname = os.path.join(path, name)
		try:
			image = pygame.image.load(fullname)
		except pygame.error, message:
			print 'Cannot load image:', name
			raise SystemExit, message
		image = image.convert()
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0, 0))
			image.set_colorkey(colorkey, RLEACCEL)
		return image

PANE_MAP = {
	SIGN:Dialog.sign_pane_image
}