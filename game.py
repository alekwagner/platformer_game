
import arcade
 

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "bob"

PLAYER_MOVEMENT_SPEED = 5

class MyGame(arcade.Window):
   
    def __init__(self): 
     super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
     self.player_list = None
     self.wall_list = None
     self.player_sprite = None
     self.physics_engine = None
     arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
     
     
     
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_sprite = arcade.Sprite("waste of space helmet 1.png")
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        for x in range(0, 1250, 64):
             wall = arcade.Sprite("New Piskel-1.png.png")
             wall.center_x = x
             wall.center_y = 32
             self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.player_list.draw()


    def on_key_press(self, key, modifiers):
            
    
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
            
    
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0




    def on_update(self, delta_time):           
        self.physics_engine.update()

def main():
   window = MyGame()
   window.setup()
   arcade.run()
 

if __name__ == "__main__":
 main()