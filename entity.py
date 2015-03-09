""" An entity is more specific than a GameImage, but less specific than a Being or Block.
"""

from tile import Tile, GameImage
from gameimage import BACKGROUND_COLOR
from pygame import Color

import math

class Entity(GameImage):
    """ Entity( AnimationSet ) -> Entity

    An entity, unlike a Tile, almost always has some physical effect on other objects
    it comes into contact with. It is not necessarily locked to a tile.

    Attributes:

    color: Not sure if I use this anymore.

    unseen_color: The color this object appears as when there is no light on it.

    mapped: Flags whether or not the player has seen this entity.

    x_interactable: Flags whether or not the player can interact with this entity.

    current_level: The level this entity is currently on.

    active_subentities: Subentities are things like weapons, shields, limbs, etc.
    which act and display separately from this entity. This may be because their collisions
    have different effects, because their animations/behavior are determined by different rules
    than the main entity, or for some other reason.

    entity_effects: Special subentities that have no physical effect, but are rendered on the topmost
    visual layer.
    """
    def __init__(self, animations):
        GameImage.__init__(self, animations)
        self.color = BACKGROUND_COLOR
        self.unseen_color = Color("#FFFFFF")
        self.mapped = False
        self.x_interactable = False
        self.current_level = None
        self.active_subentities = []
        self.entity_effects = []

    def add_subentity(self, subentity):
        """ e.add_subentity( Subentity ) -> None

        Add a subentity to this entity's active subentities, meaning it will be
        updated and displayed by the level each tick until it disappears.
        """
        self.active_subentities.append(subentity)

    def remove_subentity(self, subentity):
        """ e.remove_subentity( Subentity ) -> None

        Removes the subentity from the active subentities.
        This means it will not appear on the level anymore.
        """
        if subentity in self.active_subentities:
            self.active_subentities.remove(subentity)

    def add_entity_effect(self, effect):
        """ e.add_entity_effect( EntityEffect ) -> None

        Add a visual entity effect.
        """
        self.entity_effects.append(effect)

    def remove_entity_effect(self, effect):
        """ e.remove_entity_effect( EntityEffect ) -> None

        Remove a visual entity effect.
        """
        if effect in self.entity_effects:
            self.entity_effects.remove(effect)

    def in_interact_range(self, other):
        """ e.in_interact_range( Entity ) -> None

        A general method that is overridden for x-interactable objects.
        """
        return False

    def execute_x_action(self, level, player):
        """ e.execute_x_action( Level, Player ) -> None

        A general method that is overridden for x-interactable objects.
        """
        pass

    def dist_from(self, other):
        """ e.dist_from( Entity ) -> double

        Returns the straight-line distance (in tiles) between this entity and another.
        """
        xdist = self.x_dist_from(other)
        ydist = self.y_dist_from(other)  
        xaligned = True
        yaligned = True
        if xdist >= ((self.rect.width/2) + (other.rect.width/2)):
            xaligned = False
        if ydist >= ((self.rect.height/2) + (other.rect.height/2)):
            yaligned = False
        if not xaligned:
            xdist -= ((self.rect.width/2) + (other.rect.width/2))
        if not yaligned:
            ydist -= ((self.rect.height/2) + (other.rect.height/2))
        return (math.sqrt(pow(xdist, 2) + pow(ydist, 2)))/32 + 0.0

    def pixel_dist_from(self, other):
        """ e.pixel_dist_from( Entity ) -> double

        Returns the straight-line distance (in pixels) between this entity and another.
        """
        xdist = self.x_dist_from(other)
        ydist = self.y_dist_from(other)  
        return (math.sqrt(pow(xdist, 2) + pow(ydist, 2))) + 0.0

    def x_dist_from(self, other, absolute = True):
        """ e.x_dist_from( Entity, bool ) -> int

        Returns the horizontal distance in pixels between this entity and another.
        """
        x1 = self.rect.centerx
        x2 = other.rect.centerx
        if(absolute):
            return abs(x2 - x1)
        return x2 - x1

    def y_dist_from(self, other, absolute = True):
        """ e.x_dist_from( Entity, bool ) -> int

        Returns the vertical distance in pixels between this entity and another.
        """
        y1 = self.rect.centery
        y2 = other.rect.centery
        if(absolute):
            return abs(y2 - y1)
        return y2 - y1

    def withindist(self, other, dist):	
        """ e.withindist( Entity, int ) -> bool

        checks if the entity is close enough to another (in tiles).
        """
        return self.dist_from(other) < dist

    def within_pixel_dist(self, other, dist):
        """ e.within_pixel_dist( Entity, int ) -> bool

        checks if the entity is close enough to another (in pixels).
        """
        return self.pixel_dist_from(other) < dist        

    def delete(self):
        """ e.delete( ) -> None

        Remove this entity from the the level, emptying its current tile if applicable.
        """
        self.current_tile().reset()      
        self.current_level.remove(self)    

    def current_tile(self):
        """ e.current_tile( ) -> Tile

        Returns the tile that this entity currently occupies on the level.
        """
        tiles = self.current_level.getTiles()
        coords = self.coordinates()  
        return Tile.tileat(coords, tiles)

    #CHANGED TO NEW METHOD
    #def emit_light(self, dist, tiles, light_map, otherlights = None):
    def emit_light(self, dist, tiles, light_map):
        """ e.emit_light( int, [ [ Tile ] ], [ [ double ] ], [ Entity/Lantern/? ] ) -> None

        Start spreading light outwards in a circle.
        """
        starttile = self.current_tile()
        if not (starttile == None):
            starttile.emit_light(dist, tiles, light_map)

    def calculate_brightness(self, coords):
        # this may be outdated. Delete if we don't end up using it anywhere.
        return 0

    def light_distance(self):
        """ e.light_distance( ) -> int 

        A general method giving the radius of light this entity should emit in the dark.
        """
        return 0

    #might not end up using this method. If so, delete it.
    def castShadow(self):
        tiles = self.current_level.getTiles()
        start_tile = self.current_tile()
        if not (start_tile == None):
            down_shadow_tile = start_tile.relativetile((0,1),tiles)
            right_shadow_tile = start_tile.relativetile((1,0),tiles)
            if not (down_shadow_tile == None or down_shadow_tile.block != None):
                down_shadow_tile.castShadow(tiles, 132)
            if not (right_shadow_tile == None or right_shadow_tile.block != None):
                right_shadow_tile.castShadow(tiles, 168)

