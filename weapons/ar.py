import arcade
from consts import RIGHT_FACING, AR_SCALING
from utils import load_ar_texture_pair

class AR(arcade.Sprite):
    """ Player Sprite"""
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.AR_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = AR_SCALING

       

        # --- Load Textures ---

       
        main_path = "assets\weapons\AR\AR"
       

        # Load textures 
        self.idle_texture_pair = load_ar_texture_pair(f"{main_path}_idle.png")
        self.firing_texture_pair = load_ar_texture_pair(f"{main_path}_firing.png")
        
        """
        self.walk_textures = []
        for i in range(2):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture) """

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1/2):


      
        self.texture = self.idle_texture_pair[self.AR_face_direction]
        return

        """# Walking animation
        self.cur_texture += 1
        if self.cur_texture > 1:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]"""
