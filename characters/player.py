import arcade
from consts import RIGHT_FACING, CHARACTER_SCALING, PLAYER_FRAMES, PLAYER_FRAMES_PER_TEXTURE
from utils import load_texture_pair
from threading import Timer

class PlayerCharacter(arcade.Sprite):
    #Player Sprite
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.cur_climbing_texture = 0
        self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.immune = False

        #animation handling
        self.virtual_textures = 0

        # --- Load Textures ---
        main_path = "assets/aniamations/player/"

        # Load textures for idle standing 
        self.idle_texture_pair = load_texture_pair(f"{main_path}The waste of space player_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}The waste of space player_jump.png")
     
        # Load textures for walking
        self.walk_textures = []
        for i in range(PLAYER_FRAMES):
            texture = load_texture_pair(f"{main_path}walk/The waste of space player_walk{i}.png")
            self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

        self.health = 100
        self.ammo = 10

    def update_animation(self, delta_time: 1/2):

        # Jumping animation 
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        
        # Idle animation 
        if self.change_x == 0 or self.is_on_ladder == True:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # walk animation 
        self.virtual_textures +=1
        if self.virtual_textures > PLAYER_FRAMES*PLAYER_FRAMES_PER_TEXTURE -1:
            self.virtual_textures = 0
            self.cur_texture = 0
        if (self.virtual_textures +1)%PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_textures // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

    def take_20_health(self):
        if not self.immune:
            self.health -= 20
            self.immune = True
            vunerable_timer = Timer(0.8, self.make_vunerable)
            vunerable_timer.start()
            
    def make_vunerable(self):
        self.immune = False