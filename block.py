""" An entitty that is "locked" to a tile, like a platform. A tile can only have one block.
"""

from entity import Entity
from gameimage import BACKGROUND_COLOR, DEFAULT_COLORKEY
import pygame
from pygame import Surface, Color, Rect

EXPLORED_GREY = Color("#222222")
	
class Block(Entity):
	""" Block( AnimationSet, int, int ) -> Block

	A Block is more specific than an Entity but less specific than a Platform. I can't think of any blocks that should be able to move.

	Attributes:

	is_sloped: determines whether the block is sloped, affecting how entities will collide with it.
	is_square: determines whether the block is square, affecting collisions and how light will land on it.
	is_solid: determines whether entities can pass through this block.
	"""
	def __init__(self, animations, x, y):
		Entity.__init__(self, animations)
		self.unseen_color = Color("#FFFFFF") #TODO: need "unseen image" instead
		self.rect = Rect(x, y, 32, 32)
		self.is_sloped = False
		self.is_square = True
		self.is_solid = True
		self.unseen_image = None

	def updateimage(self, lightvalue = 0): 
		""" b.updateimage( int ) -> None

		This method may be outdated with the new lighting system. Consider removing the lightvalue arg.
		"""
		if(lightvalue != 0): 
			self.image = self.default_image 
			self.image.set_alpha(lightvalue)
		else: 
			self.image = Surface((32, 32)) #TODO: consider making the unseen image a const value that 
			if(self.mapped):    			#both platforms and tiles can access (or private data if it should vary)
				self.image.fill(self.unseen_color)    #same for unseen color
				self.image.set_alpha(16)
				return
			self.image.fill(BACKGROUND_COLOR)

	def additional_block(self, x, y):
		""" b.additional_block( int, int ) -> None

		I'm not sure if this method is still used or what it was for. Try to find it somewhere else in classes like LevelFactory.
		"""
		return None

	def map(self):
		""" b.map( ) -> None

		Mark that the player has seen this block, causing it to be visible as a grey square in complete darkness.
		"""
		self.mapped = True
		#if not self.unseen_image:
		#	self.unseen_image = self.draw_memory_image()

	def draw_memory_image(self):
		""" b.draw_memory_image( ) -> None

		Set this block's image as it is viewed in memory mode.
		"""
		if self.is_sloped:
			self.unseen_image = Surface(( 32, 32 ))
			pointlist = self.sloped_point_list()
			pygame.draw.polygon( self.unseen_image, EXPLORED_GREY, pointlist )
			self.unseen_image.convert()

	def sloped_point_list(self):
		""" b.sloped_point_list( ) -> [ ( int, int ) ]

		Generates a list of relative vertices for a sloped platform.
		"""
		corners = [ ( 0, 0 ), ( 31, 0), ( 0, 31 ), ( 31, 31 ) ]
		empty_corners = []
		point_list = []
		increment_map = {0:1, 31:-1}
		for c in corners:
			if self.image.get_at(c) == DEFAULT_COLORKEY:
				empty_corners.append(c)
		if len(empty_corners) == 0: return corners
		if len(empty_corners) == 1:
			empty_corner = empty_corners[0]
			opposite_corner = ( abs(empty_corner[0] - 31), abs(empty_corner[1] - 31))	
			corner1, corner2 = empty_corner, empty_corner
			x_incr_1, y_incr_1 = 0, increment_map[corner1[1]]	#(0, 0) -> +(1,0) -> (32, 0)
			x_incr_2, y_incr_2 = increment_map[corner2[0]], 0	#(0, 0) -> +(0,1) -> (0, 32)
			next_vertex_1 = None
			for i in xrange(31):
				corner1 = (corner1[0] + x_incr_1, corner1[1] + y_incr_1)
				if not next_vertex_1 and self.image.get_at(corner1) != DEFAULT_COLORKEY:
					next_vertex_1 = corner1	# a copy is necessary because we will keep changing corner1, but we don't want it to change in the list.
			if next_vertex_1: point_list.append(next_vertex_1)
			point_list.append(corner1)
			point_list.append(opposite_corner)
			next_vertex_2 = None
			for i in xrange(31):
				corner2 = (corner2[0] + x_incr_2, corner2[1] + y_incr_2)
				if not next_vertex_2 and self.image.get_at(corner2) != DEFAULT_COLORKEY:
					next_vertex_2 = corner2	# a copy is necessary because we will keep changing corner2, but we don't want it to change in the list.
			point_list.append(corner2)
			if next_vertex_2: point_list.append(next_vertex_2)
			return point_list
		if len(empty_corners) == 2:
			corner1, corner2 = empty_corners[0], empty_corners[1]
			opposite_corner_1, opposite_corner_2 = ( abs(corner1[0] - 31), abs(corner1[1] - 31) ), ( abs(corner2[0] - 31), abs(corner2[1] - 31) )	
			x_incr = abs( ( corner1[1] - corner2[1] )/32 ) * increment_map[corner1[0]]
			y_incr = abs( ( corner1[0] - corner2[0] )/32 ) * increment_map[corner1[1]]
			next_vertex_1 = None
			for i in xrange(31):
				corner1 = ( corner1[0] + x_incr, corner1[1] + y_incr )
				if not next_vertex_1 and self.image.get_at(corner1) != DEFAULT_COLORKEY:
					next_vertex_1 = corner1
			if next_vertex_1: point_list.append(next_vertex_1)
			point_list.append(corner1)
			next_vertex_2 = None
			for i in xrange(31):			
				corner2 = (corner2[0] + x_incr, corner2[1] + y_incr)
				if not next_vertex_2 and self.image.get_at(corner2) != DEFAULT_COLORKEY:
					next_vertex_2 = corner2
			point_list.append(corner2)
			if next_vertex_2: point_list.append(next_vertex_2)	
			return point_list
		if len(empty_corners) == 3:
			for c in corners:
				if c not in empty_corners:
					start_corner = c
					point_list.append(c)
					corner1, corner2 = start_corner, start_corner
					x_incr_1, y_incr_1 = increment_map[corner1[0]], 0	#(0, 0) -> +(1,0) -> (32, 0)
					x_incr_2, y_incr_2 = 0, increment_map[corner2[1]]	#(0, 0) -> +(0,1) -> (0, 32)
					for i in xrange(31):
						corner1 = (corner1[0] + x_incr_1, corner1[1] + y_incr_1)
						if self.image.get_at(corner1) == DEFAULT_COLORKEY:				
							corner1 = (corner1[0] - x_incr_1, corner1[1] - y_incr_1)
							point_list.append(corner1)
							break
					for i in xrange(31):
						corner2 = (corner2[0] + x_incr_2, corner2[1] + y_incr_2)
						if self.image.get_at(corner2) == DEFAULT_COLORKEY:
							corner2 = (corner2[0] - x_incr_2, corner2[1] - y_incr_2)
							point_list.append(corner2)
							break
					return point_list
		return None

		"""
		if not self.is_sloped: return None
		corners = [ ( 0, 0 ), ( 32, 0), ( 0, 32 ), ( 32, 32 ) ]
		if self.image.get_at((0, 0)) == DEFAULT_COLORKEY: return corners[1:]
		if self.image.get_at((32, 0)) == DEFAULT_COLORKEY: return corners[:1] + corners[2:]
		if self.image.get_at((0, 0)) == DEFAULT_COLORKEY: return corners[:1] + corners[2:]
		"""