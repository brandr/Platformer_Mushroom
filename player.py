""" The only being directly controlled by the person playing the game.
"""
import os

from being import *
from lantern import *
from exitblock import *
from platform import Platform, DestructiblePlatform
from platformdata import DESTROY_STEP_ON
from animationset import AnimationSet
from lightflash import LightFlash
from entityeffect import EntityEffect

from weaponfactory import build_weapon, SWORD
from inventory import Inventory, LANTERN
from level import DISPLAY_MEMORY
from maingamecontrols import LEFT, RIGHT, DOWN, UP, SPACE, CONTROL, X
from lantern import DEFAULT_MODE, MEMORY_MODE

MAX_LIGHT_FLASH_RADIUS = 10 #might move this somewhere else
LIGHT_FLASH_ALPHA = 100

STARTING_BUTTON_PRESS_MAP = {
    LEFT:False, RIGHT:False, DOWN:False, UP:False,
    SPACE:False, CONTROL:False, X:False
}

LANTERN_MODE_MAP = {
    DEFAULT_MODE:"default",
    MEMORY_MODE:"memory"
}

HUD_LANTERN_MODE_NONE = "hud_lantern_mode_none"
HUD_LANTERN_MODE_DEFAULT = "hud_lantern_mode_default"
HUD_LANTERN_MODE_MEMORY = "hud_lantern_mode_memory"
HUD_LANTERN_MODE_SUNLIT = "hud_lantern_mode_sunlit"
HUD_HP_BAR_START_EMPTY = "hud_hp_bar_start_empty"
HUD_HP_BAR_MIDDLE_EMPTY = "hud_hp_bar_middle_empty"
HUD_HP_BAR_END_EMPTY = "hud_hp_bar_end_empty"
HUD_HP_BAR_START_FILLED = "hud_hp_bar_start_filled"
HUD_HP_BAR_MIDDLE_FILLED = "hud_hp_bar_middle_filled"
HUD_HP_BAR_END_FILLED = "hud_hp_bar_end_filled"

HUD_COMPONENT_LIST = [
    HUD_LANTERN_MODE_NONE,
    HUD_LANTERN_MODE_DEFAULT,
    HUD_LANTERN_MODE_MEMORY,
    HUD_LANTERN_MODE_SUNLIT,
    HUD_HP_BAR_START_EMPTY,
    HUD_HP_BAR_MIDDLE_EMPTY,
    HUD_HP_BAR_END_EMPTY,
    HUD_HP_BAR_START_FILLED,
    HUD_HP_BAR_MIDDLE_FILLED,
    HUD_HP_BAR_END_FILLED
]

class Player(Being):
    """ Player( AnimationSet, Level ) -> Player

    The player's inheritance from Being handles most, but not all of the physics that apply to it.
    A lot of mechanics like inventory and health have not been implemented for the player yet.

    Attributes:

    active: This flags whether the player is affected by gravity and keyboard input.

    can_jump: This flags whether pressing space will make the player jump.

    left, right, down, up, space, control, x: these represent keyboard inputs that make the player move.

    movement_state: a string key used to map the player's current conditions to the proper physics that should affect him.

    lantern: Currently represents the player's lantern, if he has one. This may be wrapped in inventory later on.
    """
    def __init__(self, player_animations, start_level):
        Being.__init__(self, player_animations)
        self.changeAnimation('idle','right')
        self.direction_id = 'right'
        self.animated = True
        self.default_image = self.animation.images[0]
        self.current_level = start_level
        self.can_leave_level = True
        self.active = True
        self.can_jump = True
        self.button_press_map = STARTING_BUTTON_PRESS_MAP
        self.movement_state = DEFAULT_MOVEMENT_STATE
        self.inventory = Inventory()
        self.hud_map = self.load_hud_map()
        self.light_flash_animations = self.load_light_flash_animations()
        self.light_flash = None
        #self.light_flash_circles = self.load_light_flash_circles()
        #TODO: come up with a more general system for swords/weapons
        self.viewed_cutscene_keys = []
        #TEMP
        sword = build_weapon(SWORD, self)
        self.acquire_item(sword, SWORD)
        #self.sword = build_weapon(SWORD, self)
        self.hit_points = [10, 10]
        self.dead = False 
        self.death_count = 0
        #TEMP

    def temp_z_method(self):    
        #TEMP (no docstring)
        #TODO: find some way to pass this directional check into the sword itself.
        self.get_sword().activate(32, 0, self.direction_id) 
        #TODO: make a sword-swinging animation for the player, and set it so that the player cannot face the other way if moving left while swinging right (i.e., he just walks backwards)
        #TEMP

    @staticmethod
    def load_player_animation_set():
        """ load_player_animation_set( ) -> AnimationSet

        Load all animations that the player can use and put them into an AnimationSet object.
        """
        player_rect = Rect(0, 0, 64, 64)
        filepath = './animations/'
        
        # could probably use the same system used for loading monster animations, and simply store
        # player animation keys in tiledata with the other keys.
        
        # NOTE: change/add player sprites here.
        
        player_idle_left = GameImage.load_animation(filepath, 'player_1_idle_left.bmp', player_rect, -1)
        player_idle_right = GameImage.load_animation(filepath, 'player_1_idle_right.bmp', player_rect, -1)

        player_walking_left = GameImage.load_animation(filepath, 'player_1_walking_left.bmp', player_rect, -1, True, 6)
        player_walking_right = GameImage.load_animation(filepath, 'player_1_walking_right.bmp', player_rect, -1, True, 6)

        player_running_left = GameImage.load_animation(filepath, 'player_1_walking_left.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_running_left.bmp', player_rect, -1, True, 5)
        player_running_right = GameImage.load_animation(filepath, 'player_1_walking_right.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_running_right.bmp', player_rect, -1, True, 5)

        player_jumping_left = GameImage.load_animation(filepath, 'player_1_idle_left.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_jumping_left.bmp', player_rect, -1, True, 12)
        player_jumping_right = GameImage.load_animation(filepath, 'player_1_idle_right.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_jumping_right.bmp', player_rect, -1, True, 12)

        animation_set = AnimationSet(player_idle_right)
        animation_set.insertAnimation(player_idle_left,'left', 'idle')
        animation_set.insertAnimation(player_idle_right,'right', 'idle')

        animation_set.insertAnimation(player_walking_left,'left', 'walking')
        animation_set.insertAnimation(player_walking_right,'right','walking') 

        animation_set.insertAnimation(player_running_left,'left', 'running')
        animation_set.insertAnimation(player_running_right,'right', 'running')

        animation_set.insertAnimation(player_jumping_left,'left', 'jumping')
        animation_set.insertAnimation(player_jumping_right,'right', 'jumping')

        #TODO: jumping, falling, and (maybe) terminal velocity
        #TODO: attacking, other sprite animations

        return animation_set

    @staticmethod
    def load_player_silhouette_animation_set():
        """ load_player_silhouette_animation_set( ) -> AnimationSet

        Load all animations that will show the player as a grey silhouette.
        """
        player_rect = Rect(0, 0, 32, 64)
        filepath = './animations/'

        player_idle_left = GameImage.load_animation(filepath, 'player_1_idle_left_silhouette.bmp', player_rect, -1)
        player_idle_right = GameImage.load_animation(filepath, 'player_1_idle_right_silhouette.bmp', player_rect, -1)

        player_walking_left = GameImage.load_animation(filepath, 'player_1_walking_left_silhouette.bmp', player_rect, -1, True, 6)
        player_walking_right = GameImage.load_animation(filepath, 'player_1_walking_right_silhouette.bmp', player_rect, -1, True, 6)

        player_running_left = GameImage.load_animation(filepath, 'player_1_walking_left_silhouette.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_running_left.bmp', player_rect, -1, True, 5)
        player_running_right = GameImage.load_animation(filepath, 'player_1_walking_right_silhouette.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_running_right.bmp', player_rect, -1, True, 5)

        player_jumping_left = GameImage.load_animation(filepath, 'player_1_idle_left_silhouette.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_jumping_left.bmp', player_rect, -1, True, 12)
        player_jumping_right = GameImage.load_animation(filepath, 'player_1_idle_right_silhouette.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_jumping_right.bmp', player_rect, -1, True, 12)

        animation_set = AnimationSet(player_idle_right)
        animation_set.insertAnimation(player_idle_left,'left', 'idle')
        animation_set.insertAnimation(player_idle_right,'right', 'idle')

        animation_set.insertAnimation(player_walking_left,'left', 'walking')
        animation_set.insertAnimation(player_walking_right,'right','walking') 

        animation_set.insertAnimation(player_running_left,'left', 'running')
        animation_set.insertAnimation(player_running_right,'right', 'running')

        animation_set.insertAnimation(player_jumping_left,'left', 'jumping')
        animation_set.insertAnimation(player_jumping_right,'right', 'jumping')

        #TODO: jumping, falling, and (maybe) terminal velocity
        #TODO: attacking, other sprite animations

        return animation_set

    def deactivate(self):
        """ p.deactivate( ) -> None

        Make the player unable to move, as for a cutscene.
        """
        self.refresh_animation_set()
        self.active = False
        for button in self.button_press_map:
            self.button_press_map[button] = False

    def activate(self):
        """ p.activate( ) -> None

        Makes the player active, such as after a cutscene is over.
        """
        self.active = True

    def update(self, tiles, light_map):
        """ p.update( [ [ Tile ] ], [ [ double ] ]) -> None

        Exit the level if the player is outside its boundaries.
        Otherwise, figure out the current movement state and apply physics accordingly.
        All entities that "care" about the player (monsters, NPCs, etc.) then act.
        Afterwards, update the player's view (indirectly updating the screen).
        """
        if self.dead: return
        if(self.exitLevelCheck()): return
        update_method = MOVEMENT_STATE_MAP[self.movement_state]
        update_method(self)
        self.invincibility_update()
        self.lantern_update()
        Being.updatePosition(self)
        player_interactables = self.current_level.player_interactables()
        for e in player_interactables: e.update(self)
        self.updateView(tiles, light_map)

    def default_move_update(self):  #consider separating midair update into its own method if this gets too complex.
        """ p.default_move_update( ) -> None

        Check which buttons are currently being pressed and move the player accordingly.
        This is a little complicated, so I can go more in-depth if necessary.
        """
        up, down, left, right, space, running, x = self.button_press_map[UP], self.button_press_map[DOWN], self.button_press_map[LEFT], self.button_press_map[RIGHT], self.button_press_map[SPACE], self.button_press_map[CONTROL], self.button_press_map[X]
        self.xvel = 0
        if x:
            if self.x_action_check(): return
        if up:
            if self.collide_ladder():
                self.movement_state = LADDER_MOVEMENT_STATE
        if down:
            pass
        if left and not right:
            self.xvel = -3
            self.direction_id = 'left'

        if right and not left:
            self.xvel = 3
            self.direction_id = 'right'

        if space and self.onGround:
                self.yvel -= 13.0
                self.changeAnimation('jumping', self.direction_id)
                self.animation.iter()
                self.onGround = False
                self.can_jump = True
        if not self.onGround:    # only accelerate with gravity if in the air
            self.yvel += 0.40
            #TODO: falling animation starts once self.yvel >=0 (or maybe slightly lower/higher)
            # max falling speed
            if self.yvel > 90: self.yvel = 90
            if not space or self.yvel > 0:
                self.yvel = max(self.yvel, 0)
                self.can_jump = False
            #TODO: consider a separate falling animation at terminal velocity.
        #else:
        #    self.running = running
        if(running):#self.running):
            self.xvel *= 1.6
            if(self.onGround):
                self.changeAnimation('running', self.direction_id)
        else:
            if(self.onGround):
                if(left != right):
                    self.changeAnimation('walking', self.direction_id)
                else:
                    self.xvel = 0
                    self.changeAnimation('idle', self.direction_id)
            else: 
                if(left == right):
                    self.xvel = 0

    def bounce_move_update(self):
        """ p.bounce_move_update( ) -> None

        Calls the player's bounce method. This is generally done if the player has just been knocked back by an enemy.
        """
        self.bounce()

    def ladder_move_update(self):
        """ p.ladder_move_update( ) -> None

        This update is called if the player is grabbing onto a ladder. Note that this doesn't happen if the player is in collision with the ladder,
        only if he actually "grabs" it by pressing up.
        """
        #TODO: ladder climbing animations go here
        up, down, left, right, space, running, x = self.button_press_map[UP], self.button_press_map[DOWN], self.button_press_map[LEFT], self.button_press_map[RIGHT], self.button_press_map[SPACE], self.button_press_map[CONTROL], self.button_press_map[X]
        self.xvel, self.yvel = 0, 0
        if not self.collide_ladder():
            self.movement_state = DEFAULT_MOVEMENT_STATE
            return
        #TODO: make behavior at the top and bottom of a ladder less awkward.
        if up and not down:         
            self.yvel = -2      

        elif down and not up: 
            self.yvel = 2

        if left and not right:
            self.xvel = -2
            self.direction_id = 'left'

        if right and not left:
            self.xvel = 2
            self.direction_id = 'right'

    def invincibility_update(self):
        """ p.invincibility_update( ) -> None

        Advances the player's invincibility frames.
        """
        if self.invincibility_frames > 0: self.invincibility_frames -= 1

    def lantern_update(self):
        """ p.lantern_update( ) -> None

        Update the player's lantern (draining oil) if the player is underground and holding a lantern.
        """
        lantern = self.get_lantern()
        if lantern and not self.current_level.outdoors:
            lantern.active_update(self.active)

    def refresh_animation_set(self):
        """ p.refresh_animation_set( ) -> None

        Set the player's animation set based on current lantern mode.
        """
        animations = None
        if self.current_level.display_mode(self) == DISPLAY_MEMORY:
            animations = Player.load_player_silhouette_animation_set()
        else:
            animations = Player.load_player_animation_set()
        self.change_animation_set(animations)

    def activate_lantern_ability(self):
        """ p.activate_lantern_ability( ) -> None

        Activate some action using the player's lantern,
        based on its current mode.
        """
        if self.light_flash and self.light_flash.active: return #might want to replace this with a more general check to see if the lantern is "busy"
        lantern = self.get_lantern()
        if not lantern: return
        level = self.current_level
        if level.outdoors: return
        lantern.activate_ability(self, self.rect.centerx, self.rect.centery)

    def toggle_lantern_mode(self, direction):
        """ p.toggle_lantern_mode( int ) -> None

        Change the mode of the player's lantern to create different effects.
        """
        lantern = self.get_lantern()
        if not lantern: return
        lantern.change_mode(direction)
        self.refresh_animation_set()

    def lock_lantern(self):
        """ p.lock_lantern( ) -> None

        Locks the lantern, preventing it from flickering.
        """
        self.get_lantern().lock()

    def unlock_lantern(self):
        """ p.unlock_lantern( ) -> None

        Unlocks the lantern, resuming its flickering.
        """
        self.get_lantern().unlock()

    def destroy_blocks_in_radius( self, radius, center_x, center_y ):
        """ p.destroy_blocks_in_radius( int, int, int ) -> None

        After the lantern ability that causes this event is confirmed, the player 
        emits a flash of light that destroys all valid blocks in the given radius.
        """
        flash_animation = self.light_flash_animations[ min( radius, MAX_LIGHT_FLASH_RADIUS ) ]
        self.light_flash = LightFlash( self, flash_animation )
        self.light_flash.activate()

    def x_action_check(self):
        """ p.x_action_check( ) -> None

        If the player presses x, the first thing he is found to be in range of is activated.
        This includes doors, signs, and NPCs.
        """
        x_interactables = self.current_level.x_interactable_objects()
        for x in x_interactables:
            if x.in_interact_range(self) or pygame.sprite.collide_rect(self, x):
                self.x_interact(x)
                return

    def x_interact(self, interactable):
        """ p.x_interact( ? ) -> None

        This is an extension of x_action_check.
        """
        interactable.execute_x_action(self.current_level, self)
     
     #this gets laggy when there is too much light. try to fix it. (might have to fix other methods instead)
    def updateView(self, all_tiles, light_map): #note: this is only to be used in "cave" settings. for areas that are outdoors, use something else.
        """ p.updateView( [ [ Tile ] ], [ [ double ] ]) -> None

        Use the given light map of the level to figure out how bright each tile should be (assuming the player is underground).
        This updates the player's view and makes visible light sources emit light.
        """
        GameImage.updateAnimation(self, 256)  
        self.explore_adjacent_tiles(all_tiles)       
        #if(self.current_level.outdoors):
        #    return
        #self.emit_light(self.sight_dist(), all_tiles, light_map)

    def explore_adjacent_tiles(self, tiles):
        """ p.explore_adjacent_tiles( [ [ Tile ] ] ) -> None

        Mark tiles adjacent to the player as explored so that they will appear in memory mode.
        """
        center_x, center_y = (self.rect.left + 1)/32, (self.rect.top + 1)/32
        width, height = len(tiles[0]), len(tiles) 
        x1, y1 = center_x - 2, center_y - 2
        x2, y2 = center_x + 2, center_y + 3
        for y in xrange( y1, y2 ):
            if( 0 <= y < height ):
                for x in xrange( x1, x2 ):
                    if( 0 <= x < width ):
                        tiles[y][x].map()
    def sight_dist(self):
        """ p.sight_dist( ) -> int 

        Returns the radius of light that the player's lantern should emit.
        """
        lantern = self.get_lantern()
        if lantern and not lantern.is_empty():
            return lantern.light_distance()
        return 0 

    def in_vision_range(self, other):	
        """ p.in_vision_range( ? ) -> bool 

        Checks if the player can see the given object in the dark.
        """
        if(self.withindist(other, self.sight_dist() + other.light_distance())):
            return True
        else:
            return False 

    def load_hud_map(self):
        """ p.load_hud_map( ) -> { str:Surface }
        
        Load all of the image components that can be used in the player hud.
        """
        hud_map = {}
        for hud_component_name in HUD_COMPONENT_LIST:
            image = pygame.image.load("./hud/" + hud_component_name + ".bmp")
            hud_map[hud_component_name] = image
        return hud_map

    def current_lantern_mode_image(self):
        """ p.current_lantern_mode_image( ) -> Surface

        Figure out which image should be used for the player's current lantern mode.
        """
        if self.current_level.outdoors:
            return self.hud_map[HUD_LANTERN_MODE_SUNLIT]
        lantern = self.get_lantern()
        if not lantern or not lantern.oil_meter[0]:
            return self.hud_map[HUD_LANTERN_MODE_NONE]
        mode_name = LANTERN_MODE_MAP[lantern.mode]
        return self.hud_map["hud_lantern_mode_" + mode_name]

    def load_hp_bar_images(self):
        """ p.load_hp_bar_images( ) -> Surface, Surface, Surface, Surface, Surface, Surface

        Load all of the images associated with the player's HP bar.
        """ 
        return self.hud_map[HUD_HP_BAR_START_EMPTY], self.hud_map[HUD_HP_BAR_MIDDLE_EMPTY], self.hud_map[HUD_HP_BAR_END_EMPTY], self.hud_map[HUD_HP_BAR_START_FILLED], self.hud_map[HUD_HP_BAR_MIDDLE_FILLED], self.hud_map[HUD_HP_BAR_END_FILLED]

    def load_light_flash_animations(self):
        """ p.load_light_flash_animations( ) -> [ AnimationSet ]

        Loads the animations used to represent expanding bursts of light when the lantern is used
        to reveal hidden areas.
        """
        animations = []
        filepath = "./light_flash_circles"
        for i in range(1, MAX_LIGHT_FLASH_RADIUS):
            filename = "circle_strip_" + str(i) + ".png"
            rect = Rect( 0, 0, i*64, i*64 )
            anim = GameImage.load_animation(filepath, filename, rect)
            anim.set_all_alphas(LIGHT_FLASH_ALPHA)
            animation_set = AnimationSet(anim)
            animations.append(animation_set)
        return animations

            #this could probably be moved up in inheritance
    def get_point(self, start, end, slope, x):
        # this seems to be unused, but I don't want to get rid of it unless I'm sure.
        p = start
        if(start[0] > end[0]): 
            p = end
        y = p[1] + slope*(x - p[0])
        return (x, y)

    #TODO: collidewith could be an abstract method in the object we collide with
    #TODO: could speed this method up by only checking collidable objects near the player.

    def take_damage(self, damage):
        """ p.take_damage( int ) -> None
        
        The player receives the given amount of damage.
        Since the game would be a pain to test if the player could die, this is not yet implemented.
        """
        if damage <= 0: return
        self.hit_points[0] = max( self.hit_points[0] - damage, 0 )

    def die(self):
        """ p.die( ) -> None

        The player dies horribly.
        """
        if self.dead: return
        self.death_count += 1
        print self.death_count
        self.dead = True
        self.add_death_explosion()
        self.current_level.player_dead_counter = 150

    def add_death_explosion(self):
        animation_set = self.load_death_explosion_animation()
        explosion = EntityEffect(self, animation_set, self.rect.left - 32, self.rect.top - 32)
        self.add_entity_effect(explosion)

    def load_death_explosion_animation(self):
        explosion_rect = Rect(0, 0, 64, 64)
        filepath = './animations/'
        explosion_animation = GameImage.load_animation(filepath, 'player_death_explosion.bmp', explosion_rect, -1, False, 16)
        animation_set = AnimationSet(explosion_animation)
        return animation_set

    def collide(self, xvel, yvel):
        """ p.collide( int, int ) -> None

        The player collides with any adjacent objects that he is in contact with.
        This includes stopping against platforms, being hit by monsters, absorb pickups, etc.
        """
        level = self.current_level
        platforms = level.get_impassables() #TODO: remember that it might be possible to pass through some platforms in some directions. 
        destructible_platforms = []
        slopes = []
        default_platforms = []
        for p in platforms:
            if self.pixel_dist_from(p) > self.rect.height: continue # this check should help reduce lag.
            if pygame.sprite.collide_mask(self, p) and p.is_solid:
                if isinstance(p, DestructiblePlatform):
                    destructible_platforms.append(p)
                if p.is_sloped:
                    slopes.append(p)
                else:
                    default_platforms.append(p)
        for s in slopes:
            Being.collideWith(self, xvel, yvel, s)
        for p in default_platforms:
            Being.collideWith(self, xvel, yvel, p)
        for dp in destructible_platforms:         
            if Being.standing_on_object(self, xvel, yvel, dp):
                dp.receive_catalyst(DESTROY_STEP_ON, level)
        #self.collideExits()
        self.collidePickups()
        self.collideLanterns() #might not need this with the new lantern system (if lantern is obtained  from a chest or something)
        if(self.bounce_count <= 0):
            self.collideMonsters(xvel, yvel)

    def collide_ladder(self): #
        """ p.collide_ladder( ) -> bool

        Note that this is a boolean, not an action. (might be a more general and efficient way to implement the check for what object(s) the player is currently colliding with.)
        This is called if the player presses up, and checks to see whether the player grabs onto a ladder.
        """
        ladders = self.current_level.getLadders()
        for l in ladders:
            if pygame.sprite.collide_rect(self, l):
                return True
        return False

    def collideExits(self):
        """ p.collideExits( ) -> None

        Check if the player should leave the level.
        The way this method is written sort of confuses me, because the exit blocks are supposed to stop the player from leaving the level.
        """
        exits = self.current_level.get_exit_blocks()
        for e in exits:
            if pygame.sprite.collide_rect(self, e):
                self.exitLevel(e)
                return

    def collidePickups(self):
        """ p.collidePickups( ) -> None

        The player absorbs any pickups he is in contact with.
        """
        level = self.current_level
        pickups = level.getPickups()
        for p in pickups:
            if pygame.sprite.collide_rect(self, p):
                self.pick_up(p)
                return

    def collideLanterns(self):
        """ p.collideLanterns( ) -> None

        The player picks up any lanterns he is touching.
        This may change if the player instead gets lanterns from a chest, has to press a button to pick them up, etc.
        """
        level = self.current_level
        lanterns = level.getLanterns()
        for l in lanterns:
            if pygame.sprite.collide_rect(self, l):
                self.pick_up_lantern(l) #TEMP
                return

    def pick_up(self, pickup):
        """ p.pick_up( Pickup ) -> None

        The player absorbs a pickup, removing it from the level.
        """
        pickup.delete()
        pickup.take_effect( self )

    def collideMonsters(self, xvel, yvel):
        """ p.collideMonsters( int, int ) -> None

        If the player is touching any monsters, he gets hurt and bounces off of them.
        """
        if self.invincibility_frames > 0: return
        x_direction_sign = 1
        y_direction_sign = 1
        level = self.current_level
        monsters = level.getMonsters()
        for m in monsters:
            if pygame.sprite.collide_rect(self, m):
                self.mask = pygame.mask.from_surface(self.image)
                m.mask = pygame.mask.from_surface(m.image)
                if pygame.sprite.collide_mask(self, m):
                    self.collide_with_damage_source(m)
                    self.take_damage(m.contact_damage) #TODO: grab this from monster
                    break #makes sure the player can only collide with one monster per cycle

    def collide_with_damage_source(self, source):
        """ p.collide_with_damage_source( Monster/Weapon ) -> None

        A player being hit by a monster, weapon, projectile, etc. takes damage, goes through invincibility frames, etc.
        """
        self.bounceAgainst(source)
        self.invincibility_frames = 100
        source.bounceAgainst(self)
        
    def bounce(self):
        """ p.bounce( ) -> None

        The player performs one frame of being bounced away from an enemy.
        """
        if(self.bounce_count <= 0): 
            self.movement_state = DEFAULT_MOVEMENT_STATE
            return
        self.bounce_count -= 1

    def bounceAgainst(self, other): 
        """ b.bounceAgainst ( Being ) -> None

        Bounce against another being, starting the bounce counter so that the player cannot
        take other actions until the counter runs out.
        Similar to Being's bounceAgainst, except it alters the current state.
        """
        if self.invincibility_frames > 0: return
        x_direction_sign = 1
        y_direction_sign = 1
        if(self.rect.left < other.rect.left):
            x_direction_sign = -1
        if(self.rect.top < other.rect.top):
            y_direction_sign = -1
        new_xvel = 4 * x_direction_sign
        new_yvel = y_direction_sign
        self.xvel = new_xvel
        self.yvel = new_yvel 
        self.movement_state = BOUNCING_MOVEMENT_STATE
        self.bounce_count = 15

    def light_distance(self):
        """ p.light_distance( ) -> int

        Returns the radius of light emitted by the player in darkness.
        """
    	return self.sight_dist()

    def exitLevelCheck(self):
        """ p.exitLevelCheck() -> bool

        Checks whether the player is outside the level and send him to the adjacent level in that direction if necessary.
        """
        if(self.current_tile() == None):
            self.die()
            return False
            """
            coords = self.coordinates()
            x, y = coords[0], coords[1]
            x_dir, y_dir = 0, 0
            level_dimensions = self.current_level.get_dimensions()
            if x <= 0: x_dir = -1
            elif x >= level_dimensions[0]: x_dir = 1
            if y <= 0: y_dir = -1
            elif y >= level_dimensions[1]: y_dir = 1
            direction = (x_dir, y_dir)
            x -= x_dir
            y -= y_dir
            if self.current_level.next_level_exists(self.current_level.global_coords( (x, y) ), direction) :
                self.exit_level(coords)
                return True
            if self.current_level.next_dungeon_exists(direction):
                self.exit_dungeon(coords)
                return True
            else:
                if self.rect.left < 0: 
                    self.rect.left = 0
                    self.xvel = 0
                if self.rect.right >= 32*level_dimensions[0]: 
                    self.rect.right = 32*level_dimensions[0]
                    self.xvel = 0
                if self.rect.top < 0: 
                    self.rect.top = 0
                    self.yvel = 0
                if self.rect.bottom >= 32*level_dimensions[1]: 
                    self.rect.bottom = 32*level_dimensions[1]
                    self.onGround = True
                    self.yvel = 0
        return False
        """
    def exit_level(self, coords):
        """ p.exit_level( ( int, int ) ) -> None 

        Move the player to the proper adjacent level.
        This is called if the player is outside the current level.
        """
        self.current_level.move_player(coords)

    def exit_dungeon(self, coords):
        """ p.exit_dungeon( (int, int ) ) -> None

        Move the player to an adjacent level.
        This happens at very specific level borders.
        """
        self.current_level.move_player_dungeon(coords)

    # ITEM-RELATED METHODS
    def get_lantern(self):
        """ p.get_latern( ) -> Lantern

        Return the player's current lantern, or None if he has no lantern.
        """
        return self.inventory.get_item(LANTERN)

    def get_sword(self):
        """ p.get_sword( ) -> Sword

        Return the player's current sword, or None if he has no sword.
        """
        return self.inventory.get_item(SWORD)

    def acquire_item(self, item, key):
        """ p.acquire_item( Item, str ) -> None

        The player acquires the given item.
        """
        self.inventory.add_item( item, key )

    def open_inventory(self):
        """ p.open_inventory( ) -> None

        Open the inventory screen to view the player's items and make changes (such as setting lantern mode).
        """
        self.current_level.pause_game(self)
        self.current_level.screen_manager.switch_to_inventory_screen(self)

    def open_map(self):
        """ p.open_map( ) -> None

        The player opens up the map screen.
        """
        self.current_level.pause_game(self)
        self.current_level.screen_manager.switch_to_map_screen(self)

    def pause_game(self):
        """ p.pause_game( ) -> None

        Pause the game and open the pause screen (which is currently the map screen).
        """
        self.current_level.pause_game(self)
        self.current_level.screen_manager.switch_to_pause_screen(self)

    def unpause_game(self):
        """ p.unpause_game( ) -> None

        Resume normal gameplay.
        """
        self.current_level.unpause_game(self)

    def has_viewed_cutscene(self, cutscene_key):
        """ p.has_viewed_cutscene( str ) -> bool

        Check whether the player has seen a cutscene based on its associated string key.
        """
        return cutscene_key in self.viewed_cutscene_keys

    def hittable_targets(self):
        """ p.hittable_targets( ) -> [ Monster ]

        Returns everything that can be hit by the player's weapons. Currently only includes monsters.
        """
        return self.current_level.getMonsters()

DEFAULT_MOVEMENT_STATE = "default_movement_state"
BOUNCING_MOVEMENT_STATE = "bouncing_movement_state"
LADDER_MOVEMENT_STATE = "ladder_movement_state"

MOVEMENT_STATE_MAP = {
    DEFAULT_MOVEMENT_STATE:Player.default_move_update,
    BOUNCING_MOVEMENT_STATE:Player.bounce_move_update,
    LADDER_MOVEMENT_STATE:Player.ladder_move_update
}