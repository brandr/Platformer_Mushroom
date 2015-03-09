""" A factory for creating both melee and ranged weapons.
"""

from pygame import image, Rect 

from gameimage import GameImage
from animationset import AnimationSet
from meleeweapon import MeleeWeapon


def weapon_animation_set(animation_data):
	""" weapon_animation_set( ( Rect, [ ( str, str, str ) ] ) ) -> AnimationSet

	Returns an animationset for a weapon based on a rect and a list of string key tuplets of the form:
	(filename, direction key, state key).
	"""
	filepath = './animations/'
	weapon_rect =  animation_data[0]
	animation_set_data = animation_data[1]
	default_anim_data = animation_set_data[0]
	default_animation = GameImage.load_animation(filepath, default_anim_data[0], weapon_rect, -1, True, 10) #last 2 args are temp
	animation_set = AnimationSet(default_animation)
	for d in animation_set_data:
		filename = d[0]
		animation = GameImage.load_animation(filepath, filename, weapon_rect, -1, True, 10) #last 2 args are temp
		animation_set.insertAnimation(animation, d[1], d[2])
	return animation_set

def build_weapon(weapon_key, superentity):
	""" build_weapon( str, Being ) -> MeleeWeapon

	Builds a weapon with the correct type, animationset, damage, etc.
	Will become more sophisticated as more weapon types are added.
	"""
	animation_data = WEAPON_ANIMATION_DATA_MAP[weapon_key]
	animation_set = weapon_animation_set(animation_data)
	return MeleeWeapon(superentity, animation_set)

LEFT = "left"
RIGHT = "right"

SWINGING = "swinging"

SWORD = "sword"
PICK = "pick"

WEAPON_ANIMATION_DATA_MAP = {
	SWORD:
		(
			Rect(0, 0, 32, 32),
			[
				("test_sword_swinging_left.bmp", LEFT, SWINGING),
				("test_sword_swinging_right.bmp", RIGHT, SWINGING)
			]	
		),
	PICK:
		(
			Rect(0, 0, 128, 128),
			[
				("pick_swinging_left.bmp", LEFT, SWINGING),
				("pick_swinging_right.bmp", RIGHT, SWINGING)
			]
		)
}