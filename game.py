
import arcade
 

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "bob"

class MyGame(arcade.Window):
   
    def __init__(self): 
     super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
     self.player_list = None
     self.player_sprite = None
     arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
     
     
     
    def setup(self):
        self.player_list = arcade.SpriteList()
        
        self.player_sprite = arcade.Sprite("waste of space helmet 1.png")
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)




    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()


def main():
   window = MyGame()
   window.setup()
   arcade.run()
 

if __name__ == "__main__":
 main()