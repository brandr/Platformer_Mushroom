""" A single square on a level that has an image on it and may contain a block.
"""

from gameimage import GameImage
import pygame
from pygame import Rect, Color, Surface
from math import *

class Tile(GameImage):
    """ Tile( AnimationSet, int, int ) -> Tile

    A tile does not keep track of all entities that pass through it, since they do not lock to tiles.
    However, it does keep track of blocks such as platforms, ladders, and doors.

    Attributes:

    unseen_color: The color the tile will appear as in complete darkness.

    block: The object that is locked to this tile. It generally cannot move and can only be removed.

    mapped: Marks whether the Tile has been seen by the player. This is generally only relevant if there is a block in the tile.
    """
    def __init__(self, animations, x , y): 
        GameImage.__init__(self, animations) 
        self.unseen_color = Color("#000000")
        self.rect = Rect(x, y, 32, 32)
        self.block = None
        self.mapped = False

    def changeImage(self, image = None):
        """ t.changeImage( Surface ) -> None

        Change the image displayed on the tile. Note that this will not affect the block's image if there is a block.
        """
        if(image != None):
            self.default_image = image
            self.image = image

    def reset(self):
        """ t.reset( ) -> None

        Refresh the tile so that it is empty and shows its default image properly.
        """
        #brightness = self.image.get_alpha()
        self.image = self.default_image
        #self.image.set_alpha(brightness)
        self.image.convert()
        self.block = None

    def updateimage(self, lightvalue = 0):
        """ t.updateimage( int ) -> None

        Updates the tile image as a black square with this tile's block behind it, or just set this tile's image to the default image if there's no block.
        """
        if(self.block != None and self.block.is_square): 
            self.image = Surface((32, 32))
            self.image.blit(self.block.image, (0, 0))
            self.block.updateimage(lightvalue)
            return
        GameImage.updateimage(self, lightvalue)

    #CHANGED TO NEW METHOD
    #def emit_light(self, dist, tiles, light_map, otherlights = []):
    def emit_light(self, dist, tiles, light_map):
        """ emit_light( int, [ [ Tile ] ], [ [ double ] ], [ ? ]) -> None

        Light is emitted in a circle from the tile, stopping at solid walls.
        This is a very complicated algortihm so hopefully we won't have to change it.
        """
        if dist == 0: return
        coords = self.coordinates()
        light_map[coords[1]][coords[0]] = 1
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        for d in directions:
            nexttile = self.relativetile((d[0], d[1]), tiles)
            if nexttile != None:
                nexttile.spreadlight(dist - 1, tiles, light_map, 1, (d[0], d[1]) )

    #OLD METHOD DECLARATION (change back if we switch back to the old system)
    #def spreadlight(self, dist, tiles, light_map, iteration = 0, direction = None, lineflag = False, brightness = None, otherlights = []):
    def spreadlight(self, dist, tiles, light_map, iteration = 0, direction = None, lineflag = False, light_flag = 1):
        """ t.spreadlight( int, [ [ Tile ] ], [ [ double ] ], int, ( int, int ), bool, int, [ ? ] ) -> None

        After many iterations, this is the most efficient algortihm I have come up with to handle light spreading. 
        Note that emit_light is called on the center tile, which calls this on adjacent tiles.
        This method is recursive, spreading slightly dimmer light the further it goes from the center tile.
         
        The dist arg represents the remaining distance a "ray" of light can travel. From the center, it starts at the light
        radius for whatever light source is in the tile, and decrements by 1 for each unit it travels away from the center.
 
        The tiles and light_map args both represent the tiles that the light is spreading across, but light_map represents only
        the brightness values at each tile as a double between 0 and 256.

        The iteration arg represents how many times an instance of this method has recursed. A higher iteration means the 
        brightness is lower.

        The direction arg is a tuplet representing the direction the light is traveling in as ( x direction, y direction ).
        For example, (-1, 0) is left, (1, 0) is right, (0, -1) is up, and (0, 1) is down.

        The lineflag arg, if true, indicates that the light should only travel in a straight line. This is done for
        rays of light that shine perpendicular to each of the 4 rays that shine from the center, forming a circular pattern.

        The brightness arg (if it is not None, which is a value used to trigger certain cases) is a value between 0 and 256 setting
        how bright this tile should be. Brightness decreases with each iteration.

        The otherlights arg is a list of other nearby light sources that may intersect with the light being spread in this method.
        """
        #NEW METHOD
        coords = self.coordinates()
        light_map[coords[1]][coords[0]] = light_flag
        if dist <= 0:
            return               #once the light reaches its max distance, stop
        if self.block != None and self.block.is_solid:
            d1 = (-1*direction[1], direction[0])
            d2 = (direction[1], -1*direction[0])
            nexttile1 = self.relativetile(d1, tiles)
            nexttile2 = self.relativetile(d2, tiles)
            if nexttile1 != None:
                nexttile1.spreadlight(0, tiles, light_map, iteration, d1, True)
            if nexttile2 != None:
                nexttile2.spreadlight(0, tiles, light_map, iteration, d2, True)   
            light_flag = 0
            #return
        starttile = self.relativetile(direction, tiles)
        if starttile != None:
            starttile.spreadlight(dist - 1, tiles, light_map, iteration + 1, direction, lineflag)
        if lineflag: return
        
        #non-lineflag case (still going in one of the four intial directions)
        d1 = (-1*direction[1], direction[0])
        d2 = (direction[1], -1*direction[0])

        nexttile1 = self.relativetile(d1, tiles)
        nexttile2 = self.relativetile(d2, tiles)
        nextdist = sqrt(pow(iteration + dist - 1 , 2) - pow(iteration - 1, 2))

        if nexttile1:
            nexttile1.spreadlight(nextdist, tiles, light_map, iteration + 1, d1, True, light_flag)  
        if nexttile2:
            nexttile2.spreadlight(nextdist, tiles, light_map, iteration + 1, d2, True, light_flag)

        """
        #OLD  METHOD (change back if I switch back to square-based lighting)
        coords = self.coordinates()
        self.map()
        if brightness == None:
            brightness = ((0.9*dist + 1)/(max(dist + iteration, 1)))*256
        maxbrightness = brightness
        if otherlights != None:
            for o in otherlights:
                if o.withindist(self, o.light_distance()):
                    checkbrightness = o.calculate_brightness(coords, tiles)
                    maxbrightness = max(checkbrightness, brightness)
        light_map[coords[1]][coords[0]] = maxbrightness
        if dist <= 0:
            return               #once the light reaches its max distance, stop
        if self.block != None and self.block.is_solid:
            d1 = (-1*direction[1], direction[0])
            d2 = (direction[1], -1*direction[0])
            nexttile1 = self.relativetile(d1, tiles)
            nexttile2 = self.relativetile(d2, tiles)
            if nexttile1 != None:
                nexttile1.spreadlight(0, tiles, light_map, iteration, d1, True, None, otherlights)
            if nexttile2 != None:
                nexttile2.spreadlight(0, tiles, light_map, iteration, d2, True, None, otherlights)           
            return
        starttile = self.relativetile(direction, tiles)
        if starttile != None:
            starttile.spreadlight(dist - 1, tiles, light_map, iteration + 1, direction, lineflag, None, otherlights)
        if lineflag: return
        
        #non-lineflag case (still going in one of the four intial directions)
        d1 = (-1*direction[1], direction[0])
        d2 = (direction[1], -1*direction[0])

        nexttile1 = self.relativetile(d1, tiles)
        nexttile2 = self.relativetile(d2, tiles)
        nextdist = sqrt(pow(iteration + dist - 1 , 2) - pow(iteration - 1, 2))

        if nexttile1 != None:
            nexttile1.spreadlight(nextdist, tiles, light_map, iteration + 1, d1, True, None, otherlights)  
        if nexttile2 != None:
            nexttile2.spreadlight(nextdist, tiles, light_map, iteration + 1, d2, True, None, otherlights)
        """

    def relativetile(self, coords, tiles):
        """ t.relativetile( ( int, int ), [ [ Tile ] ] ) -> Tile

        From the given 2D grid of tiles, grab the tile at the given coordinates.
        """
        startcoords = self.coordinates()
        tilecoords = (startcoords[0] + coords[0], startcoords[1] + coords[1])
        if Tile.validcoords(tilecoords, tiles):
            return Tile.tileat((tilecoords[0], tilecoords[1]), tiles)
        return None

    def map(self):
        """ t.map( ) -> None

        Mark that the player has seen this tile, meaning that if it contains a block, then it will appear in darkness.
        """
        if(self.mapped): return
        self.mapped = True 
        if(self.block != None):
            self.block.map()

    def passable(self):
        """ t.passable( ) -> bool

        Returns whether Entities can pass through this tile.
        """
        return self.block == None or (not self.block.is_solid) #TODO: change this if some blocks are passable. (might already be necessary for signs and ladders)

    @staticmethod
    def validcoords(coords, tiles): 
        """ validcoords( ( int, int ), [ [ Tile ] ] ) -> bool

        Checks if a set of tile coords correspond to an actual tile on the level.
        """
        if(coords == None or coords[0] == None or coords[1] == None):
            return False
        minuscheck = coords[0] >= 0 and coords[1] >= 0
        ymax = len(tiles)
        xmax = len(tiles[0])
        pluscheck = coords[0] < xmax and coords[1] < ymax
        return minuscheck and pluscheck

    @staticmethod
    def tileat(coords, tiles):	
        """ tileat( ( int, int ), [ [ Tile ] ] ) -> Tile 

        The tile on the level at a set of coords.
        """
        if(Tile.validcoords(coords, tiles)):
            return tiles[coords[1]][coords[0]]
        return None