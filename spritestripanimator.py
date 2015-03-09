""" NOTE: this class was not written by Robert.
"""

from spritesheet import *
 
class SpriteStripAnimator(object):
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, sprites, rect, count, colorkey = None, loop = True, frames = 10):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        ss = SpriteSheet(sprites)
        self.images = ss.load_strip(rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    def iter(self):
        self.i = 0
        self.f = self.frames
        return self

    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image

    def at_end(self):
        return self.i >= len(self.images)

    def synch_animation_frame(self, other):
        self.i = other.i
        self.f = other.f

    def set_all_alphas(self, alpha):
        for i in self.images:
            i.set_alpha(alpha)

    def __add__(self, ss):
        self.images.extend(ss.images)
        return self