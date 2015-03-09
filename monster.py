""" A (possbly hostile) creature that lives in the dungeon somewhere.
"""

from being import *
from weaponfactory import build_weapon, PICK

from random import randint

class Monster(Being):
    """ Monster( AnimationSet, int, int ) -> AnimationSet

    A monster is more specific than a being in that it moves around and has AI.
    However, it is not necessarily hostile to the playerself.
    It may have some commonalities with player. these should be moved up to Being where appropriate.
    It may even make sense to make player inherit from monster. Not sure yet, though.

    Attributes:

    name: An identifier that can be used as a key to grab the monster's data.

    active: Determines whether the monster is able to move around (besides animation).

    sightdist: How far away the monster can spot you from in darkness. As far as I can tell, this isn't
    used right now, and it might be better to use a system that makes more sense, like having the monster
    become alerted to the player upon being hit by light from the player.

    max_speed: the highest speed the monster is capabale of moving in any direction. The monster may move
    slower than this value, but never faster.

    direction_val: A value set to -1 (left) or 1 (right) for the direction the player is moving in.

    direction_id: A string value to represent the direction.

    ai_counter: A temporary value used to set timers in between the monster's actions.

    hit_points: An [int, int] value represeting [current hp, max hp]. Current hp cannot exceed max hp,
    and the monster dies when its current hp reaches 0.
    """
    def __init__(self, animations, x, y): 
        Being.__init__(self, animations, x, y)
        self.name = None
        self.animated = True
        self.active = True
        self.sightdist = 6
        self.max_speed = 6
        self.contact_damage = 1 # TEMP: grab this from the MONSTER_DATA_MAP instead
        self.direction_val = -1 # -1 for left, 1 for right
        self.direction_id = 'left'
        self.changeAnimation('idle','left')

        self.can_bounce = True
        self.ai_state = AI_IDLE
        self.ai_counter = 20         # TEMP. Might want to consider this an attribute instead.
        self.hit_points = None
        self.weapon = None

    def monster_init(self, name):
        """ m.monster_init( str ) -> None

        Use the monster's name as a string key to set values like hit points.
        Might move this to a new MonsterFactory class if it clutters up this 
        class too much.
        """
        default_map = MONSTER_DATA_MAP[DEFAULT]
        if name in MONSTER_DATA_MAP:
            monster_map = MONSTER_DATA_MAP[name]
            for key in default_map:
                if key in monster_map:
                    self.init_attribute(key, monster_map[key])
                else:
                    self.init_attribute(key, default_map)
        else:
            for key in default_map:
                self.init_attribute(key, default_map[key])

    def init_attribute(self, key, value):
        """ m.init_attribute( str, ? ) -> None

        Init the appropriate attribute to the given value.
        """
        init_method = MONSTER_INIT_MAP[key]
        init_method(self, value)
    
    def init_hit_points(self, hit_points):
        """ m.init_hit_points( int ) -> None

        Set this monster's hp to the given value.
        """
        self.hit_points = [hit_points, hit_points]

    def init_weapon(self, weapon):
        """ m.init_weapon( MeleeWeapon ) -> None

        Set this monster's weapon to the given weapon.
        """
        self.weapon = weapon(self)

    def init_bounce(self, bounce):
        """ m.init_bounce( bool ) -> None

        Sets whether or not this monster can bounce.
        """
        self.can_bounce = bounce

    def init_max_speed(self, speed):
        """ m.init_max_speed( int ) -> None
        Set the monster's maximum movement speed.
        """
        self.max_speed = speed

    #TODO: make this general in the long run, so that monsters can interact with each other as well as with the player.
    #  in particular, consider having monsters "collide" with each other (they probably shouldn't bounce but I'm not sure.)
    def update(self, player):
        """ m.update( Player ) -> None

        The monster's update method depends on what kind of monster it is.
        In the future we should probably do this with a dict.
        """
        self.updateAnimation()
        #TODO: check if the monster can see the player. (using sightdist)
        #TODO: check if the monster is hostile the player.
        #TODO: figure out a better way to assosciate the monster with its udpate action (probably a dict, though name alone might not be sophisticated enoough.)
        if not self.active: return
        self.ai_update(player)
        Being.updatePosition(self)

    def set_active(self, active):
        """ m.set_active( bool ) -> None

        Activate or inactivate this monster. This might be pointless since "hurrdurr setters in python 2014"
        """
        self.active = active

    def randomize_next_action(self, actions, player):
        """ m.randomize_next_action( [ Method ], Player ) -> None

        Randomly choose a method to execute from the given set. Usually used to make AI less predictable.
        """
        if not actions: return
        action_count = len(actions) - 1
        action_index = randint(0, action_count)
        actions[action_index](self, player)

    def ai_update(self, player):
        """ m.ai_update( self, Player ) -> None

        Perform some action based on the monster's name and current AI state.
        """
        self.ai_counter -= 1
        update_method = MONSTER_AI_MAP[(self.name, self.ai_state)]
        update_method(self, player)

    def bat_update(self, player):
        """ m.bat_update( Player ) -> None 

        In-progress method handling a bat's behavior.
        """
        if self.bounce_count > 0:   #TEMP
            self.bounce()
            return
        target = player.current_tile()
        if(target != None):
            self.moveTowards(player.current_tile())

    def frog_update(self, player):
        """ m.frog_update( Player ) -> None 

        In-progress method handling a giant frog's behavior.
        """
        self.gravityUpdate()
        if self.bounce_count > 0:   #TEMP
            self.bounce()
            return
        self.faceTowards(player.current_tile())
        if self.onGround:
            self.changeAnimation('idle', self.direction_id)
            self.xvel = 0
            #TODO: make the frog try to land on the player.
                # figure out the frog's distance from the player, and calculate the necessary xvel.
                # jump with min(self.max_speed/2, target_speed)
            if self.ai_counter <= 0: #TODO: change the way this works
                self.jump(self.direction_val*self.max_speed/2, self.max_speed)
            self.wait()

    #TEMP

    def miner_update_idle(self, player):
        """ m.miner_update_idle( Player ) -> None

        The miner does nothing. Gravity is applied here.
        """
        self.gravityUpdate()
        if self.bounce_count > 0:   
            self.bounce()
        if self.onGround:
            self.changeAnimation('idle', self.direction_id)
            self.xvel = 0
        if self.ai_counter <= 0:
            self.faceTowards(player)
            next_actions = [Monster.miner_begin_charging, Monster.miner_begin_jumping] #TODO: make a more general way to select a "next action" from a set of possibilities
            self.randomize_next_action(next_actions, player)

    def miner_begin_charging(self, player):
        """ m.miner_begin_charging( Player ) -> None

        The miner begins charging towards the player.
        """        
        self.ai_state = AI_CHARGING
        self.ai_counter = 30
        if self.direction_id == 'left': self.xvel = -1*self.max_speed
        elif self.direction_id == 'right': self.xvel = self.max_speed

    def miner_update_charging(self, player):
        """ m.miner_update_charging( Player ) -> None

        The miner charges towards the player.
        """
        self.gravityUpdate()
        blocked = self.check_blocked(DIRECTION_MAP[self.direction_id])
        if blocked or self.ai_counter <= 0: # NOTE: consider dealing with blockage differently to stop the miner from glitching out all over blocks.
            self.weapon.deactivate()
            self.ai_state = AI_IDLE
            self.changeAnimation('idle', self.direction_id)
            self.ai_counter = 100
            return
        self.miner_swing()

    def miner_begin_jumping(self, player):
        """ m.miner_begin_jumping( Player ) -> None

        The miner begins jumping towards the player.
        """
        if self.onGround:
            self.faceTowards(player)
            self.ai_state = AI_JUMPING
            self.ai_counter = 50
            self.jump(self.direction_val*self.max_speed/2, self.max_speed)
            self.changeAnimation('idle', self.direction_id) #TODO: use a jumping animation rather than an idle animation
            return
        #TODO: other case?

    def miner_update_jumping(self, player):
        """ m.miner_update_jumping( Player ) -> None

        The miner jumps towards the player.
        """
        #TODO
        blocked = self.check_blocked(DIRECTION_MAP[self.direction_id])
        if blocked: self.xvel = 0
        self.gravityUpdate()
        if self.onGround:
            self.ai_state = AI_IDLE
            self.ai_counter = 100
    
    def miner_swing(self):
        self.changeAnimation('swinging', self.direction_id) # this part might not belong here if there are different animations that involve swinging the pick.
        if not self.weapon.active:
            self.weapon.activate(31, -13, self.direction_id)
        self.weapon.animation.synch_animation_frame(self.animation)

    def miner_pick(self):
        """ m.miner_pick( ) -> MeleeWeapon

        A pick used by the miner boss. May want to load this sort of data more neatly once there are a lot of weapons.
        """
        return build_weapon(PICK, self)

    def collide(self, xvel, yvel):
        """ m.collide( int, int ) -> None 

        The monster processes all the proper collisions with other objects in the level, currently only including 
        impassable objects like platforms.
        """
        level = self.current_level
        platforms = level.get_impassables() #TODO: remember that it might be possible to pass through some platforms in some directions.
        slopes = []
        default_platforms = []
        for p in platforms:
            if pygame.sprite.collide_mask(self, p) and p.is_solid:
                if p.is_sloped:
                    slopes.append(p)
                else:
                    default_platforms.append(p)
        for s in slopes:
            Being.collideWith(self, xvel, yvel, s)
        for p in default_platforms:
            Being.collideWith(self, xvel, yvel, p)
        self.collideExits()

    def collideExits(self):
        """ m.collideExits( ) -> None

        The monster exits the level if outside of its limits, apparently. I'm not really sure why things work like this for monsters.
        """
        exits = self.current_level.get_exit_blocks()
        for e in exits:
            if pygame.sprite.collide_rect(self, e):
                self.exitLevel(e)
                return

    def collide_with_damage_source(self, source):
        """ m.collide_with_monster( ? ) -> None

        A monster being hit by a weapon, projectile, etc. takes damage, goes through invincibility frames, etc.
        """
        self.bounceAgainst(source)
        source.bounceAgainst(self)

    def bounceAgainst(self, other): # this is used for a monster colliding with the player, and may be useful in other cases.
        """ m.bounceAgainst ( Being ) -> None

        Bounce against another being, starting the bounce counter so that this monster cannot
        take other actions until the counter runs out.
        """
        if self.can_bounce:
            Being.bounceAgainst(self, other)
        # TODO: separate bouncing frames from invincibility frames, and think of some structure that can hold both.

    def wait(self):
        """ m.wait( ) -> None

        Does nothing. This is done to make it wait before taking certain actions.
        """
        return # this method might be obsolete since wait counter is no longer used and the ai counter is handled elsewhere.

        #the jump method could go in Being as well.
    def jump(self, xvel = 0, yvel = 0): #TODO: figure out how a monster's jumping ability is determined.
        """ m.jump( int, int ) -> None

        Jump forward with given xvel and up with given yvel. Currently, only the frog does this.
        """
        self.xvel += xvel
        self.yvel -= yvel
        self.animation.iter()
        self.ai_count = 25 #TEMP
        self.onGround = False

    def faceTowards(self, target):
        """ m.faceTowards( Being ) -> None

        The monster faces left or right, depending on which direction the target is in.
        This will influence movement and animations.
        """
        current_tile = self.current_tile()
        if(target and current_tile):
            x_dist = target.coordinates()[0] - current_tile.coordinates()[0]
            if x_dist == 0: return
            self.direction_val = x_dist/abs(x_dist)
            #TEMP
            if self.direction_val == -1:
                self.direction_id = 'left'
            if self.direction_val == 1:
                self.direction_id = 'right'

    def gravityUpdate(self):    #NOTE: could probably make this a lot more general. (i.e., different terminal velocites for some monsters)
        """ m.gravityUpdate( ) -> None

        The monster falls faster the longer it is in the air because this method increments its yvel.
        However, it will eventually hit terminal velocity.
        """
        if not self.onGround:    # only accelerate with gravity if in the air
            self.yvel += 0.3
            if self.yvel > 100: self.yvel = 100

    def take_damage(self, damage):
        """ m.take_damage( int ) -> None

        The monster takes the given amount of damage, dying if its HP falls below zero.
        """
        if damage <= 0: return
        self.hit_points[0] -= damage
        if self.hit_points[0] <= 0: self.die()

    def die(self):
        """ m.die( ) -> None

        An unfinished method to be called when the monster dies.
        """
        self.delete()
        #TODO: death animation goes here

    def hittable_targets(self):
        """ m.hittable_targets( ) -> [ Player ]
        
        A general method used by monsters and the player. For mosters, it returns the player, wrapped in a list (since monsters would be in a list as well.)
        """
        return [self.current_level.getPlayer()]

DIRECTION_MAP = {'left': -1, 'right': 1}

# monster build keys

DEFAULT = "default"
BAT = "bat"
GIANT_FROG = "giant_frog"
MINER = "miner"

HIT_POINTS = "hit_points"
WEAPON = "weapon"
BOUNCE = "bounce"
MAX_SPEED = "max_speed"

MONSTER_DATA_MAP = { 
    DEFAULT:
        {
        HIT_POINTS:1,
        WEAPON:None,
        BOUNCE:True,
        MAX_SPEED:6
        },
    GIANT_FROG:
        {
        HIT_POINTS:3
        },
    MINER:
        {
        HIT_POINTS:20,
        WEAPON:Monster.miner_pick,
        BOUNCE:False,
        MAX_SPEED:8
        }
}

MONSTER_INIT_MAP = {
    HIT_POINTS:Monster.init_hit_points,
    WEAPON:Monster.init_weapon,
    BOUNCE:Monster.init_bounce,
    MAX_SPEED:Monster.init_max_speed
}

# monster AI keys

AI_IDLE = "idle"
AI_CHARGING = "charging"
AI_JUMPING = "jumping"

MONSTER_AI_MAP = {
    (BAT, AI_IDLE):Monster.bat_update,

    (GIANT_FROG, AI_IDLE):Monster.frog_update, #TEMP: frog should also have jump method

    (MINER, AI_IDLE):Monster.miner_update_idle,
    (MINER, AI_CHARGING):Monster.miner_update_charging,
    (MINER, AI_JUMPING):Monster.miner_update_jumping
}