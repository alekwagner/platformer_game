import arcade
from consts import ENEMY_WALK_FRAMES, ENEMY_WALK_FRAMES_PER_TEXTURE, ENEMY_SCALING, RIGHT_FACING
from utils import load_enemy_texture_pair

class Enemy (arcade.Sprite):
    #Player Sprite
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.walk_cur_texture = 0
        self.attack_cur_texture = 0
        
        self.scale = ENEMY_SCALING


        #animation handling
        self.walk_virtual_textures = 0
        self.attack_virtual_textures = 0

        # --- Load Textures ---
       
        main_path = "assets/aniamations\enemy/"
       
        # Load textures for idle standing
        self.idle_texture_pair = load_enemy_texture_pair(f"{main_path}enemy_idle.png")
        
        # Load textures for walking
        self.walk_textures = []
        for i in range(ENEMY_WALK_FRAMES):
            texture = load_enemy_texture_pair(f"{main_path}enemy_walk\enemy_walk{i}.png")
            self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

        #health
        self.health = 100

        self.awake = False
        self.attacking = False
        self.attack_impact = False
        self.attack_needs_reset = False
        self.scream = False
        
    def update_animation(self, delta_time: 1/2):

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.face_direction]
            return

        #walk animation
        self.walk_virtual_textures +=1
        if self.walk_virtual_textures > ENEMY_WALK_FRAMES*ENEMY_WALK_FRAMES_PER_TEXTURE -1:
            self.walk_virtual_textures = 0
            self.walk_cur_texture = 0
        if (self.walk_virtual_textures +1)%ENEMY_WALK_FRAMES_PER_TEXTURE == 0:
            self.walk_cur_texture = self.walk_virtual_textures // ENEMY_WALK_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.walk_cur_texture][self.face_direction]
         
    def take_20_health(self):
        #this is what happens when enmey takes damage
        self.health -= 20
        if self.health <= 0:
            self.remove_from_sprite_lists()