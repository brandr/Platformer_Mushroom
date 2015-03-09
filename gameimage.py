""" The most abstract type of object that can appear in the game.
"""


from animationset import AnimationSet
from spritestripanimator import SpriteStripAnimator
from camera import WIN_WIDTH, WIN_HEIGHT

import pygame
from pygame import Surface, Color, Rect
import os
import copy

BACKGROUND_COLOR = Color("#000000")
DEFAULT_COLORKEY = Color("#FF00FF")

class GameImage(pygame.sprite.Sprite):
    """ GameImage( AnimationSet ) -> GameImage

    A GameImage inherits from pygame sprite. You can look at its documentation to see what methods can be called on a GameImage.

    Attributes:

    unseen_image: This is how the GameImage appears in complete darkness.

    mapped: Flags whether the player has seen this thing.

    animated: Flags whether the GameImage's appearance changes each frame.

    animation_set: An object containing possible animations for this object.

    animation: This GameImage's current animation.

    direction_id and animation_id are keys used to determine the GameImage's current animation.

    default_image: The default image that this GameImage reverts to if it isn't animated or doesn't know what to do.

    image: The current image that this GameImage appears as on the level.

    rect: A pygame Rect representing the space this GameImage occupies.

    mask: A pygame Mask used to detect collisions in some cases. (For simple collisions, rect is used.)
    """
    def __init__(self, animations):
        pygame.sprite.Sprite.__init__(self)

        self.unseen_image = Surface((32, 32))
        self.mapped = False
        self.animated = False #Temporary. this should probably be determined some other way (eg as a property of the animationSet itself)

        self.animation_set = animations
        self.animation = self.animation_set.default_animation()
        
        self.direction_id = 'default'
        self.animation_id = ('default', 'default')

        self.default_image = copy.copy(self.animation.images[0]) #this might be an inefficient/awkward place to use copy in the long run.
        self.image = self.default_image
        self.image.convert()
        self.rect = self.image.get_bounding_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def coordinates(self):
        """ gi.coordinates -> ( int, int )

        Returns the tile coordinates of this GameImage's upper-left corner.
        """
        return (self.rect.left/32, self.rect.top/32)

    def rect_coords(self):
        """ gi.rect_coords -> ( int, int )

        Returns the pixel coordinates of this GameImage's upper-left corner.
        """
        return (self.rect.left, self.rect.top)

    def center_rect_coords(self):
        """ gi.center_rect_coords -> ( int, int )

        Returns the pixel coordinates of this GameImage's rect center.
        """
        return (self.rect.left + self.rect.width/2, self.rect.top + self.rect.height/2)

    def tile_dimensions(self):
        """ gi.tile_dimensions -> int, int 

        Returns the width and height of this GameImage in tiles.
        """
        return self.image.get_width()/32, self.image.get_height()/32

    def pixel_remainder(self):
        """ gi.pixel_remainder( ) -> ( int, int )

        Find out how may additonal pixels the gameimage is from the closest tile corner (to the up/left).
        """
        pixel_coords = self.rect_coords()
        x_remainder = pixel_coords[0] % 32
        y_remainder = pixel_coords[1] % 32
        return (x_remainder, y_remainder)

    def moveTo(self, coords):
        """ gi.moveTo( int, int ) -> None

        Move this GameImage to the given tile coordinates.
        """
        self.moveRect(coords[0]*32, coords[1]*32, True)

    def moveRect(self, x_offset, y_offset, absolute = False):
        """ gi.moveRect( int, int, bool ) -> None

        Move this GameImage by the given tile coordinates.
        If absolute is true, move it *to* those coordinates.
        """
        if(absolute):
            self.rect.left = x_offset
            self.rect.top = y_offset
            return
        self.rect.left += x_offset
        self.rect.top += y_offset

    def change_animation_set(self, animations):
        """ gi.change_animation_set( AnimationSet ) -> None

        A rarely-used method to change the entire animation set for this game image.
        Note that this assumes the new set will use the same keys as the current one.
        """
        self.animation_set = animations
        self.animation = self.animation_set.animations[self.direction_id][self.animation_id[0]]

    def changeAnimation(self, ID, direction):
        """ gi.changeAnimation( str, str ) -> None

        Change the current animation using the given string keys.
        """
        if(self.animation_id[0] == (ID)):
            if(direction == None or self.animation_id[1] == direction):
               return
        if(direction != None):
            self.changeDirection(direction)
        self.animation = self.direction_set[ID]
        self.animation.iter()
        self.animation_id = (ID, direction)

    def changeDirection(self, direction):
        """ gi.changeDirection( str ) -> None

        Change the current animation to face in the given direction.
        """
        self.direction_set = self.animation_set.set_in_direction(direction) 

    def updateimage(self, lightvalue = 0):  #this darkening system may be useless now that the lighting system is different.
        """ gi.updateimage( int ) -> None

        Revert the current image to this object's default image.
        """
        if(self.default_image != None):
            self.image = self.default_image

    def updateAnimation(self, lightvalue = 0):
        """ gi.updateAnimation( int ) -> None

        Update the current image by advancing the animation to the next frame.
        """
        if(self.animated):
            self.animate()
            return
        self.updateimage(lightvalue)

    def animate(self):
        """ gi.animate( ) -> None

        Advance the current animation to its next frame, looping it if necessary.
        """
        self.image = self.animation.next()

    def fully_darken(self):
        """ gi.fully_darken( ) -> None

        Set this object to whatever it should look like in complete darkness.
        """
        self.image = self.unseen_image

    def clear_image(self):
        """ gi.clear_image( ) -> None
        Make this gameimage completely invisible.
        """
        nothing_image = Surface((32, 32))
        nothing_image.fill(DEFAULT_COLORKEY)
        self.image = nothing_image

    @staticmethod
    def still_animation_set(still_image, rect = Rect(0, 0, 32, 32), colorkey = DEFAULT_COLORKEY):
        """ still_animation_set( Surface, Rect, str ) -> AnimationSet

        Return an "animation set" containing only one image.
        """
        still_animation = SpriteStripAnimator(still_image, rect, 1, colorkey, False, 1)
        return AnimationSet(still_animation)

    @staticmethod
    def load_animation_set(tile_data, tile_size, colorkey = DEFAULT_COLORKEY):
        """ load_animation_set( TileData, int, int ) -> AnimationSet

        Build an animation set from a TileData object.
        """
        image_pixel_width = tile_size*tile_data.width
        image_pixel_height = tile_size*tile_data.height
        image_rect = Rect(0, 0, image_pixel_width, image_pixel_height)

        key = tile_data.entity_key

        animation_keys = tile_data.animation_keys()
        if animation_keys == None: return None

        #animation_filepath = tile_data.animation_filepath('./LevelEditor/')
        animation_filepath = "./animations"
        default_key = animation_keys[0][0]
        
        default_animation_filename = key + "_" + default_key + ".bmp"
        default_animation = GameImage.load_animation("./animations", default_animation_filename, image_rect, colorkey)
        animation_set = AnimationSet(default_animation)
        
        for n in xrange(1, len(animation_keys)):
            anim_file_key = animation_keys[n][0]
            anim_key = animation_keys[n][1]
            anim_direction = animation_keys[n][2] 
            anim_frames = 10
            if len(animation_keys[n]) > 3:
                anim_frames = animation_keys[n][3]
            animation_filename = key + "_" + anim_file_key + ".bmp"
            next_animation = GameImage.load_animation(animation_filepath, animation_filename, image_rect, colorkey, True, anim_frames)
            #TODO: get the colorkey more generally (this may come up if we use animated blocks or square enemies).
            animation_set.insertAnimation(next_animation, anim_direction, anim_key)

        return animation_set

    @staticmethod
    def load_animation(filepath, filename, rect, colorkey = None, loop = True, frames = 10): #change frames to 50 if necessary for testing
        """ load_animation( str, str, Rect, str, bool, int ) -> SpriteStripAnimator
        
        Load an animation given two parts of a filepath and some other data.
        """
        animation_strip = GameImage.load_image_file(filepath, filename)  
        count = animation_strip.get_width()/rect.width                          # assume that the animation strip is wide only, not long
        return SpriteStripAnimator(animation_strip, rect, count, colorkey, loop, frames)

    @staticmethod
    def load_animation_from_images(images, rect, colorkey = None, loop = True, frames = 10): #change frames to 50 if necessary for testing
        """ load_animation_from_images( [ Surface ], Rect, str, bool, int ) -> SpriteStripAnimator
        
        Load an animation given a set of images and some other data.
        """
        count = len(images)
        animation_strip = Surface( ( rect.width*count, rect.height ) )
        for i in xrange(count):
            animation_strip.blit(images[i], ( rect.width*i, 0 ) )
        animation = SpriteStripAnimator(animation_strip, rect, count, colorkey, loop, frames)
        return animation
    
    @staticmethod
    def load_image_file(path, name, colorkey = None):
        """ load_image_file( str, str, str ) -> Surface

        Load an image from a filepath.
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