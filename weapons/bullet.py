import arcade 
from consts import SPRITE_SCALING_BULLET
from arcade.experimental.lights import Light

class Bullet(arcade.Sprite):

    def __init__(self, light_layer):
        super().__init__()
        self.light_layer = light_layer
        self.texture = arcade.load_texture(f"assets/plasma bullet.png")
        self.scale = SPRITE_SCALING_BULLET
        self.light = Light( -1000, -1000, 300,(100,100,300),'soft')
        self.light_layer.add(self.light)

        

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.light.position = self.position


    def kill(self):
        
        self.remove_from_sprite_lists()
        self.light_layer.remove(self.light)      
        
