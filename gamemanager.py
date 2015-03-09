""" A manager which controls the flow of gameplay, including switching between screens and controls.
"""


from screenmanager import *
from dungeonfactory import build_dungeon
from cutscene import *
from world import World
from player import Player
from gameaction import GameAction
from level import DUNGEON_NAME_MAP

from os import listdir
from os.path import isfile, join

class GameManager:
	"""GameManager () -> GameManager

	This is the screen used to play the game.
	(Will add more description as more stuff is implemented.)

	Attributes: None
	"""
	def __init__(self):
		pass

	def run_game(self):
		"""GM.runGame (...) -> None

		Run the game using a pygame screen.

		Attributes:
		master_screen: the pygame screen onto which everything will be displayed
		during the game.
		"""

		#factory = DungeonFactory() #might need args like filename, filepath, etc later
		start_dungeon, dungeon_name, master_screen = self.build_dungeon_and_screen() 
		world = World(start_dungeon) # TODO: implement world (contains all dungeons, along with other global data-- how to do this?)
		pygame.display.set_caption(dungeon_name)
		timer = pygame.time.Clock()

		player_animations = Player.load_player_animation_set()
		start_level = start_dungeon.start_level()
		if not start_level: raise SystemExit, "ERROR: no starting level specified."

		player = Player(player_animations, start_level)
		start_level.addPlayer(player)

		game_controls = MainGameControls(player) # TODO: consider how controls may parse buttons differently for different screens.
		control_manager = ControlManager(game_controls)
		main_screen = MainGameScreen(control_manager, player) 
		screen_manager = ScreenManager(master_screen, main_screen, player)
		start_level.initialize_screen(screen_manager, main_screen)

		# TEMP for testing cutscenes
		# TODO: figure out how to better generalize cutscenes (start by figuring out how to generalize their actions)
		player_right_method = GameManager.temp_player_right
		player_right_action = GameAction(player_right_method, 60, None, player)
		actions = [player_right_action] 		# TODO: action for player moving right
		test_cutscene = Cutscene(actions)
		player.current_level.begin_cutscene(test_cutscene)

		while 1:
			timer.tick(120) # make this value lower to make the game run slowly for testing. (use about 40-50 I think)

 			for e in pygame.event.get():
				screen_manager.process_event(e)
			screen_manager.update_current_screen()
			self.draw_screen(screen_manager)
			pygame.display.update()

	def build_dungeon_and_screen(self):
		#use this block for developers only vvvvv
		dungeon_path = "./dungeon_map_files/"
		print "Select a starting dungeon by number: "
		dungeon_path = "./dungeon_map_files/"
		dungeon_files = [ f for f in listdir(dungeon_path) if isfile(join(dungeon_path, f)) ]
		i = 0
		for f in dungeon_files:
			i += 1
			print "(", i, ") ", f
		dungeon_input = raw_input("")
		if not dungeon_input.isdigit():
			print "Invalid dungeon input. Try again.", "\n"
			return self.build_dungeon_and_screen()
		dungeon_index = int(dungeon_input) 
		if not 0 < dungeon_index <= len(dungeon_files):
			print "Invalid dungeon number. Try again.", "\n"
			return self.build_dungeon_and_screen()
		dungeon_name = dungeon_files[dungeon_index - 1]
		# ^^^^^^^^
		
		#dungeon_name = "Cave_test"
		print "Building dungeon..."
		dungeon_display_name = dungeon_name
		if dungeon_name in DUNGEON_NAME_MAP:
			dungeon_display_name = DUNGEON_NAME_MAP[dungeon_name]
		master_screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
		dungeon = build_dungeon(dungeon_path + dungeon_name, dungeon_display_name)
		print "Dungeon built."
		return dungeon, dungeon_display_name, master_screen

	@staticmethod	#TEMP FOR TESTING (therefore, no docstring)
	def temp_player_right(arg, player):
		player.button_press_map["right"] = True

	def draw_screen(self, screen_manager):
		""" gm.draw_screen( ScreenManager) -> None

		Tell the screen manager to draw whatever should be onscreen.
		"""
		screen_manager.draw_screen()