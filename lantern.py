""" An item the player can acquire to light the area around him.
"""

from entity import *
import math

FLICKER_CONSTANT = 120

class Lantern(Entity):	#lantern which can help the player see
    """ Lantern( AnimationSet, int, int ) -> Lantern

    A lantern exists either on the ground or in the player's inventory. I may change this in the future,
    and make it so lanterns can't just sit on the ground.

    Attributes:

    flicker_index: a cyclic value which controls the lantern's flickering effect.

    oil_meter: The first value is the current oil amount and the second is the maximum amount.
    The ratio of current to max determines the lantern's brightness.

    light_multiplier: A value applied to the current oil ratio. Effectively represents the maximum light radius.
    """
    def __init__(self, animations, x, y):
        Entity.__init__(self, animations)
        self.rect.centerx += x
        self.rect.centery += y
        self.animated = True
        self.available_modes = ALL_LANTERN_MODES
        self.mode = DEFAULT_MODE
        self.flicker_index = 0
        self.flicker_lock = False
        self.oil_meter = [9999, 9999]
        self.light_multiplier = 5           # Note that light multiplier is technically meant to determine light radius, but sometimes there is an off-by-one or off-by-two error of some sort.

    def update(self, player):
        """ l.update( Player ) -> None

        Calls the flicker update, which may temporarily change the light radius.
        This method should only be called when the lantern is sitting on the ground.
        Other methods are called separately if the player is holding the lantern.

        NOTE: this method may end up being unused.
        """
        self.flicker_update()
        self.updateAnimation()

    def active_update(self, player_active):
        """ l.active_update( bool ) -> None

        If the lantern is held by the player and is currently being used, update it proprely.
        player_active will be false if the player is in an event. It will keep the lantern's oil from draining
        and also turn off non-default lantern modes.
        """
        if not player_active: self.mode = DEFAULT_MODE
        update_method = UPDATE_MODE_MAP[self.mode]
        update_method(self, player_active)
        cost = OIL_COST_MAP[self.mode]
        self.oil_update(cost)

    def default_update(self, player_active):
        """ l.default_update( bool ) -> None

        Basic update for when the lantern is in its default mode.
        """
        self.flicker_update()
        #if player_active: self.oil_update(1)

    def memory_update(self, player_active):
        """ l.memory_update( ) -> None

        Update for when the lantern is in memory mode.
        Note that an empty lantern might want to switch modes. Not sure.
        """
        pass
        #if player_active: self.oil_update(1)

    def oil_update(self, oil_decrement):
        """ l.oil_update( ) -> None

        Causes 1 unit of oil to drain from the lantern.
        Also adjusts the flicker, making the lantern's radius swell and shrink slightly.
        """
        if self.flicker_lock: return
        if self.oil_meter[0] > 0:
            self.oil_meter[0] -= oil_decrement

    def flicker_update(self):
        """ l.flicker_update( ) -> None

        Updates the lantern's flicker index, possibly changing its light radius temporarily.
        """
        if self.flicker_lock: return
        self.flicker_index += 1
        if self.flicker_index >= FLICKER_CONSTANT: self.flicker_index = 0

    def lock(self):
        """ l.lock( ) -> None

        Locks the lantern, preventing it from flickering.
        """
        if self.flicker_index < FLICKER_CONSTANT/2: self.flicker_index = 0
        else: self.flicker_index = FLICKER_CONSTANT/2
        self.flicker_lock = True
    
    def unlock(self):
        """ unlock( ) -> None

        Unocks the lantern, resuming its flickering.
        """
        if self.flicker_index < FLICKER_CONSTANT/2: self.flicker_index = 0
        else: self.flicker_index = FLICKER_CONSTANT/2
        self.flicker_lock = False

    def change_mode(self, direction):
        """ l.change_mode( direction ) -> None

        Change the lantern mode to create different visual effects.
        """
        if len(self.available_modes) < 2: return
        mode_index = -1
        if self.mode in ALL_LANTERN_MODES:
            mode_index = ALL_LANTERN_MODES.index(self.mode)
        #TODO: error case???
        mode_index = (mode_index + direction)%(len(ALL_LANTERN_MODES))
        while ALL_LANTERN_MODES[mode_index] not in self.available_modes:
            mode_index = (mode_index + direction)%(len(ALL_LANTERN_MODES))
        self.mode = ALL_LANTERN_MODES[mode_index]

    def activate_ability(self, player, center_x, center_y):
        """ l.activate_ability( Player ) -> None

        Depending on the current mode, activate some special ability.
        """
        if self.oil_meter[0] <= 0: return
        oil_cost = ABILITY_COST_MAP[self.mode]
        if oil_cost >= self.oil_meter[0]: return # check if there is enough oil for the given ability
        if self.mode == DEFAULT_MODE and self.light_distance() == 0: return 
        ability = ABILITY_MAP[self.mode]
        ability(self, player, center_x, center_y)
        self.oil_meter[0] -= oil_cost

    def default_ability(self, player, center_x, center_y):
        """ l.default_ability( Player, int, int ) -> None

        Executes the default lantern ability, which is destroying breakable blocks.
        """
        radius = self.light_distance()
        player.destroy_blocks_in_radius( radius, center_x, center_y )

    def memory_ability(self, level, center_x, center_y):
        """ l.memory_ability( Level, int, int ) -> None

        Executest the lantern ability associated with memory mode. Not sure what that is yet.
        """
        pass #TODO. not sure what it should be though.

    def light_distance(self): #may have different lantern with different light functions for different gameplay
        """ l.light_distance( ) -> int

        Returns the current light radius of the lantern.
        """
        oil_ratio = float(self.oil_meter[0])/(self.oil_meter[1])
        if oil_ratio <= 0:
            return 0
        distance = int(oil_ratio*self.light_multiplier)
        if self.flicker_index < FLICKER_CONSTANT/2:
            prev_ratio = float(self.oil_meter[0] + 1)/(self.oil_meter[1])
            prev_distance = int(prev_ratio*self.light_multiplier)
            if prev_distance != distance:
                self.flicker_index = FLICKER_CONSTANT/2
            else:      
                distance -= 1 
        return distance + 1

    def darkness_multiplier(self):
        """ l.darkness_multiplier( ) -> float

        Returns the current multiplier for darkness between light layers.
        A higher value means a dimmer lantern, though it will still cover the same radius.
        """
        radius = self.light_distance()
        if radius == 0: return 255
        base_alpha = self.base_alpha()
        multiplier = math.pow( ( float( 250.0/base_alpha ) ), float( 1.0/radius ) )
        return multiplier 

    def base_alpha(self):
        """ l.base_alpha( ) -> float

        Returns a value used to calculate light levels in other methods.
        A higher base alpha represents more darkness.
        """
        oil_ratio = float(self.oil_meter[0])/(self.oil_meter[1])
        return 60.0 - float( oil_ratio*20.0 )

    def update_light(self, tiles, light_map):
        """ l.update_light( [ [ Tile ] ] ) -> [ [ double ] ] ) -> None

        If the lantern is sitting on the ground, this method is called to make it emit light.
        """
        light_distance = self.light_distance()
        self.emit_light(light_distance, tiles, light_map)

    def add_oil(self, oil_value):
        """ l.add_oil( int ) -> None

        Refills the oil meter by the given amount without going above the maximum oil amount.
        """
        self.oil_meter[0] = min(self.oil_meter[0] + oil_value, self.oil_meter[1])

    def is_empty(self):
        """ l.is_empty( ) -> bool

        Returns True if the lantern is out of oil and False if it isn't.
        """
        return self.oil_meter[0] <= 0 

DEFAULT_MODE = "default_mode"
MEMORY_MODE = "memory_mode"
ALL_LANTERN_MODES = [DEFAULT_MODE, MEMORY_MODE]

UPDATE_MODE_MAP = {
    DEFAULT_MODE:Lantern.default_update,
    MEMORY_MODE:Lantern.memory_update
}

ABILITY_MAP = {
    DEFAULT_MODE:Lantern.default_ability,
    MEMORY_MODE:Lantern.memory_ability
}

# oil costs per frame when different lantern modes are on
OIL_COST_MAP = {
    DEFAULT_MODE:2,
    MEMORY_MODE:1
}

# costs to use lantern abilities, measured in oil units
ABILITY_COST_MAP = {
    DEFAULT_MODE:300,
    MEMORY_MODE:250
}
