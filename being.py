"""Represents something more specific than an entity or gameImage, but less specific than
a block or monster. A being is an entity that does not occupy a specific tile 
(like a block/platform does). Beings can be stationary, though they almost always move.
"""

from gameimage import GameImage
from entity import Entity
from door import Door
from platform import Platform
import pygame

ON_TOP_CONSTANT = 4

class Being(Entity):
    """ Being ( animations ) -> Being

    A Being is initialized the same as its supeclass, Entity, but it is still an abstract class
    that can be used for monsters, the player, moving traps, or anything else that affects 
    gameplay but isn't bound to a specific tile.

    The xvel and yvel attributes represent the being's current x and y velocities (where a positive
    xvel makes the Being move right and a positive yvel moves it down).

    The onGround attribute says whether the being is on the ground, and is useful for jumping methods.

    Running says whether the being is currently running. Currently this is only applicable to the player,
    so it might need to be renamed to be more general or moved to the player class.

    Sightdist represents the Being's vision radius in tiles. For the player, it determines the radius of 
    lit tiles around the player, and for monsters, it should determine how far away they can see the player
    from.

    max_speed determines the fastest speed the Being can travel in any direction.

    bounce_count represents the remaining time that the Being is "bouncing" for. Generally, no Being can
    change direction while it's bouncing.
    """

    def __init__(self, animations, x = None, y = None):
        Entity.__init__(self, animations)
        self.direction_id = None
        if x and y:
            self.rect.centerx += x
            self.rect.centery += y
        self.xvel = 0
        self.yvel = 0
        self.can_leave_level = False
        self.onGround = False
        self.running = False
        self.sightdist = 5
        self.max_speed = 10   # doesn't apply to player yet, but could
        self.bounce_count = 0 # might want a more general counter system, like a dict of counters
        self.invincibility_frames = 0
        self.hit_points = None
        #TODO: if methods/data from monster/player are universal, move them to this class.

    def update(self, player):
        """ b.update( Player ) -> None

        Calls the updateAnimation method below.
        """
        self.updateAnimation()

    def updateAnimation(self, light_value = None): #
        """ b.updateAnimation ( int ) -> None

        Updates the animation and image of the Being based on the light that is on it. Differs from usual 
        updateImage in that we must find this being's current tile because it can change a lot.
        Currently, Beings cannot be shaded based on light value, but we could probably have them be darkened
        completely for a value of 0 if this works well for the gameplay.
        """
        if self.current_tile() == None: return
        GameImage.updateAnimation(self, 256) 

    def updatePosition(self):
        """ b.updatePosition () -> None
        Updates the Being's pixel coordinate position on the screen based on its current velocities.
        """
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel)
        if not self.can_leave_level:
            self.stay_in_level_update()

    def stay_in_level_update(self):
        """ b.stay_in_level_update( ) -> None

        If any part of this being is outside the level, nudge it back in.
        """
        dimensions = self.current_level.get_dimensions()
        pixel_width, pixel_height = dimensions[0]*32, dimensions[1]*32
        while self.rect.left < 0: self.rect.left += 1
        while self.rect.right > pixel_width: self.rect.right -= 1
        while self.rect.top < 0: self.rect.top += 1
        while self.rect.bottom > pixel_height: self.rect.bottom -= 1

    #TODO: consider having bounce take effect here, like in player.
    def collide(self, xvel, yvel, collide_objects = None):
        """ b.collide (double, double, [ Platform ] ) -> None

        Collide with all solid platforms using the collideWith method also found in Being.
        Collisions with non-platform objects are handled by other methods.
        """

        level = self.current_level
        platforms = level.get_impassables()
        slopes = []
        default_platforms = []
        for p in platforms:
            if pygame.sprite.collide_mask(self, p) and p.is_solid:
                if p.is_sloped:
                    slopes.append(p)
                else:
                    default_platforms.append(p)
        for s in slopes:
            self.collideWith(xvel, yvel, s)
        for p in default_platforms:
            self.collideWith(xvel, yvel, p)

    def collideWith(self, xvel, yvel, collide_object):
        """ b.collideWith (double, double, Platform) -> None

        If the Being is "up against" a platform (based on pygame's built-in collide method), 
        it will become flush with that platform no matter what its velocity is, and be unable 
        to move in the direction of that platform. (i.e., through the platform.)
        """
        if pygame.sprite.collide_rect(self, collide_object):  #may need collide_mask in some cases, not sure.
            self.mask = pygame.mask.from_surface(self.image)
            if isinstance(collide_object, Platform) and collide_object.is_sloped:   # not sure whether the slope version will work for non-sloping objects
                self.collide_with_slope(xvel, yvel, collide_object)
                return
            if isinstance(collide_object, Door):
                self.collide_with_door(xvel, yvel, collide_object)
                return
            if isinstance(collide_object, Being):
                if not pygame.spirte.collide_mask(self, collide_object):
                    return
            # TODO: better collision handling.
            if xvel > 0:
                self.rect.right = collide_object.rect.left
            if xvel < 0:
                self.rect.left = collide_object.rect.right
            if yvel > 0:
                self.rect.bottom = collide_object.rect.top
                self.onGround = True
                self.yvel = 0
            if yvel < 0:
                self.rect.top = collide_object.rect.bottom

    def standing_on_object(self, xvel, yvel, collide_object):
        """ b.standing_on_object (double, double, Platform) -> None

        Returns True if the Being is standing on top of the given object.
        """
        if not self.onGround: return
        if abs(self.rect.bottom - collide_object.rect.top) < ON_TOP_CONSTANT:  #may need collide_mask in some cases, not sure.
            self.mask = pygame.mask.from_surface(self.image)
            #if pygame.sprite.collide_mask(self, collide_object):
            if self.rect.centery > collide_object.rect.centery: return False
            return True #TEMP

    def collide_with_slope(self, xvel, yvel, slope): #NOTE: this only works for slopes on the ground, not on the ceiling.
        """ b.collide_with_slope( double, double, Block ) -> None

        A special method that uses a more expensive collision check for slopes.
        """
        if yvel == 0:
            while pygame.sprite.collide_mask(self, slope):
                self.rect.bottom -= 1
        else:
            while pygame.sprite.collide_mask(self, slope):
                if xvel > 0:
                    self.rect.right -= 1
                if xvel < 0:
                    self.rect.left += 1
                if yvel > 0:
                    self.rect.bottom -= 1
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top += 1

    def collide_with_door(self, xvel, yvel, door):
        """ b.collide_with_door( double, double, Door ) -> None

        A special method used to collide with doors. It ensures that the being's
        sprite can be flush with the edge of the door.
        """
        if xvel >= 0:
            while pygame.sprite.collide_mask(self, door):
                self.rect.right -= 1
        else:
            while pygame.sprite.collide_mask(self, door):
                self.rect.left += 1

    def check_blocked(self, direction_val):
        """ b.check_blocked( int ) -> bool

        Check whether this being is immediately blocked in the given direction.
        """
        y1 = self.rect.top/32
        y2 = self.rect.bottom/32
        if direction_val == -1:
            x = self.rect.left/32 - 1
        else:
            x = self.rect.right/32 + 1
        level = self.current_level
        for y in range(y1, y2):
            tile = level.tile_at(x, y)
            if not tile or not tile.passable():
                return True
        return False

    def flip_direction(self):
        """ b.flip_direction( ) -> None

        Reverses this being's direction.
        """
        if self.direction_id == 'left': self.direction_id = 'right'
        elif self.direction_id == 'right': self.direction_id = 'left'

    def moveTowards(self, destination):
        """ b.moveTowards ( GameImage ) -> None

        Move towards some destination, assuming the Being is not currently bouncing.
        I'm not sure I like this structure. Beings should probably just collide first,
        check bounce second, and perform whatever other actions they can only after the
        bounce check, and these should all be in single method. I'm too lazy to set that
        up right now, though.
        """
        if self.bounce_count > 0:
            self.bounce()
            return 
        distance = self.dist_from(destination)
        if(distance == 0): return
        dist_ratio = self.max_speed/distance
        self.xvel = dist_ratio*self.x_dist_from(destination, False)/32
        self.yvel = dist_ratio*self.y_dist_from(destination, False)/32

    def snap_to_ground(self): # might want to move this to GameImage, not sure
        """ b.snap_to_ground( ) -> None

        Keep moving the being down until it is touching the ground.
        This is different from the normal effects of gravity in that it happens instantaneously.
        """
        level = self.current_level
        platforms = level.get_impassables() # TODO: remember that it might be possible to pass through some platforms in some directions.
        while 1:
            for p in platforms:
                Being.collideWith(self, 0, 1, p)
                if self.onGround: return
                self.rect.top += 1

    def bounceAgainst(self, other): # this is used for a monster colliding with the player, and may be useful in other cases.
        """ b.bounceAgainst ( Being ) -> None

        Bounce against another being, starting the bounce counter so that this being cannot
        take other actions until the counter runs out.
        """
        if(self.bounce_count > 0): return
        x_direction_sign = 1
        y_direction_sign = 1
        if(self.rect.left < other.rect.left):
            x_direction_sign = -1
        if(self.rect.top < other.rect.top):
            y_direction_sign = -1
        new_xvel = 2 * x_direction_sign
        new_yvel = 2 * y_direction_sign
        self.xvel = new_xvel
        self.yvel = new_yvel 
        self.collide(self.xvel, self.yvel)
        self.bounce_count = 40

    def bounce(self):
        """ b.bounce () -> None

        Go through one iteration of "bouncing" (i.e., being knocked away from the source of the bounce)
        and reducing the bounce counter by 1.
        """
        if(self.bounce_count <= 0): 
            return
        self.bounce_count -= 1