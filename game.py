"""todo
add a gameover and death when u stay near enemy to long
make code for enemy animations and for the enemy waking up
make a tile that spawns a enemy on it 
"""







import random
import arcade
import math
import os
from arcade.experimental.lights import Light, LightLayer
from pathlib import Path, WindowsPath








"screen var"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "game"

START = 0
END = 2000
STEP = 50

"scaling var"
CHARACTER_SCALING = 1.2
TILE_SCALING = 0.5
SPRITE_SCALING_BULLET = 1
AR_SCALING = 1.4
ENEMY_SCALING

"pixel var"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

"player mechanics"
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
BULLET_SPEED = 20

"enemy mechanics"
ENEMY_ACCELERATION_RATE = 0.2
ENEMY_FRICTION = 0.05
ENEMY_MAX_SPEED = 6


# scrapped var ENEMY_MAX_WONDER_SPEED = 1



# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

PLAYER_START_X = 80
PLAYER_START_Y = 260

AMBIENT_COLOR = (10,10, 10)
PLAYER_LIGHT_RADIUS = 150
PLAYER_LIGHT_MODE = 'soft'
PLAYER_LIGHT_COLOR = (300, 300, 300)

PLAYER_FRAMES = 32
PLAYER_FRAMES_PER_TEXTURE = 3






# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class PlayerCharacter(arcade.Sprite):
    """ Player Sprite"""
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

        #animation handling
        self.virtual_textures = 0

        # --- Load Textures ---

       
        main_path = "assets/aniamations/"
       

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}The waste of space player_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}The waste of space player_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}The waste of space player_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(PLAYER_FRAMES):
            texture = load_texture_pair(f"{main_path}walk/The waste of space player_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}The waste of space player_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}The waste of space player_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

        self.health = 100

    def update_animation(self, delta_time: 1/2):

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_climbing_texture += 1
            if self.cur_climbing_texture > 7:
                self.cur_climbing_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_climbing_texture // 4]
            return


        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        #walk animation
        self.virtual_textures +=1
        if self.virtual_textures > PLAYER_FRAMES*PLAYER_FRAMES_PER_TEXTURE -1:
            self.virtual_textures = 0
            self.cur_texture = 0
        if (self.virtual_textures +1)%PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_textures // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

    def take_20_health(self):
        
        self.health -= 20
        if self.health <= 0:
            self.center_x = PLAYER_START_X
            self.center_y = PLAYER_START_Y
       



AR_RIGHT_FACING = 0
AR_LEFT_FACING = 1

def load_ar_texture_pair(ar_filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(ar_filename),
        arcade.load_texture(ar_filename, flipped_vertically=True)
    ]


class AR(arcade.Sprite):
    """ Player Sprite"""
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.AR_face_direction = AR_RIGHT_FACING

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

class Bullet(arcade.Sprite):

    def __init__(self, light_layer):
        super().__init__()
        self.light_layer = light_layer
        self.texture = arcade.load_texture(f"assets\Floor_board_wall.png")
        self.scale = SPRITE_SCALING_BULLET/4
        self.light = Light( -1000, -1000, 300,(100,100,300),'soft')
        self.light_layer.add(self.light)

        

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.light.position = self.position


    def kill(self):
        
        self.remove_from_sprite_lists()
        self.light_layer.remove(self.light)
        
        
        
        
""" Constants used to track if the player is facing left or right """
ENEMY_RIGHT_FACING = 0
ENEMY_LEFT_FACING = 1

def load_enemy_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class Enemy (arcade.Sprite):
    """ Player Sprite"""
    def __init__(self):

        # Set up parent class
        super().__init__()

        "animations"

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        
        self.scale = ENEMY_SCALING


        #animation handling
        self.virtual_textures = 0

        # --- Load Textures ---

       
        main_path = "assets/aniamations\The waste of space player_idle.png"
       

        # Load textures for idle standing
        self.idle_texture_pair = load_enemy_texture_pair(f"{main_path}")
        

        # Load textures for walking
        self.walk_textures = []
        for i in range(PLAYER_FRAMES):
            texture = load_enemy_texture_pair(f"{main_path}")
            self.walk_textures.append(texture)


        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

        "health"
        self.health = 100

        self.awake = False
        self.on_attack = True


    def update_animation(self, delta_time: 1/2):

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        """#walk animation
        self.virtual_textures +=1
        if self.virtual_textures > PLAYER_FRAMES*PLAYER_FRAMES_PER_TEXTURE -1:
            self.virtual_textures = 0
            self.cur_texture = 0
        if (self.virtual_textures +1)%PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_textures // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]"""

         

    def take_20_health(self):
        "this is what happens when enmey takes damage"
        self.health -= 20
        if self.health <= 0:
            self.remove_from_sprite_lists()


        

#Main class of game
class MyGame(arcade.Window):
   
    def __init__(self): 

        # "call the parent class" window set up
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Background image will be stored in this variable
        
      
        # Set the path to start with this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
      
       # lists to organize different spirts into groups
        self.wall_list = None
        self.foreground_list = None
        self.background_list = None
        self.dont_touch_list = None
        self.player_list = None
        self.enemy_list = None  
        self.bullet_list = None
        self.ar_list = None
        self.light_emittor_list = None
        self.enemy_spawn_list = None

        self.bullet_sprite= None

        #var for gun
        self.ar_sprite = None

       #variable for player spirt
        self.player_sprite = None

        self.enemy_sprite = None

        self.skybox_sprite = None

       # physics engine being used
        self.physics_engine = None 

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # where is the right edge of the map?
        self.end_of_map = 0

        # level
        self.level = 1
       
        # Load sounds
        self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/phaseJump1.wav")
     
     # --- Light related ---
        # List of all the lights
        self.light_layer = None
        # Individual light we move with player, and turn on/off
        self.player_light = None

        self.bullet_light = None



    def setup(self, level):
     # set up the game here. call this function to restart the game
     
       

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # asign my sprite lists to their arcade lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.foreground_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ar_list = arcade.SpriteList()

        
        
        

        # set up player and player start position
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        self.ar_sprite = AR()
        self.ar_sprite.center_x = PLAYER_START_X
        self.ar_sprite.center_y = PLAYER_START_Y
        self.ar_list.append(self.ar_sprite)



        # --- Load in map from tiled editor ---

        # name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'platforms'
        moving_platforms_layer_name = 'moving platforms'

        # name of the layer that has items for foreground
        foreground_layer_name = 'foreground'
        # name of the layer that has items for background
        background_layer_name = 'background'
        # name of the layer that has items that we dont touch
        dont_touch_layer_name = 'dont_touch_layer'

        # name of light bulbs and stuffs and things
        lights_layer_name = 'lights'

        # enemy spawn list
        enemy_spawn_layer_name = 'enemy'

        # name of map
        map_name = f"maps/tiledmap{level}.tmx"

        # read in tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        #calculate the right edge of the my_map in pixels
        self.end_of_map_weight = my_map.map_size.width * GRID_PIXEL_SIZE
        self.end_of_map_height = my_map.map_size.height * GRID_PIXEL_SIZE
        

        # platforms
        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      platforms_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)

        # -- Moving Platforms
        moving_platforms_list = arcade.tilemap.process_layer(my_map, moving_platforms_layer_name, TILE_SCALING)
        for sprite in moving_platforms_list:
            self.wall_list.append(sprite)  
       
        # lights
        self.light_emittor_list = arcade.tilemap.process_layer(my_map,
                                                          lights_layer_name,
                                                          scaling=TILE_SCALING)

        # enemy
        self.enemy_spawn_list = arcade.tilemap.process_layer(my_map,
                                                          enemy_spawn_layer_name,
                                                          scaling=TILE_SCALING)  

        # background
        self.background_list = arcade.tilemap.process_layer(my_map,
                                                            background_layer_name,
                                                            TILE_SCALING)

        # foreground
        self.foreground_list = arcade.tilemap.process_layer(my_map,
                                                            foreground_layer_name, 
                                                            TILE_SCALING)

        
        # -- Don't Touch Layer
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            dont_touch_layer_name,
                                                            TILE_SCALING,
                                                            use_spatial_hash=True)
        
        # ladders
        self.ladder_list = arcade.tilemap.process_layer(my_map,
                                                        "ladders",
                                                        scaling=TILE_SCALING,
                                                        use_spatial_hash=True)
        
        
       
        # other stuff
        # set background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)
        
          # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY,
                                                             ladders=self.ladder_list)
      
        # Create a light layer, used to render things to, then post-process and
        # add lights. This must match the screen size.
        self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)

        # We can also set the background color that will be lit by lights,
        # but in this instance we just want a black background
        #self.light_layer.set_background_color(arcade.color.BLACK)

         # Create a light to follow the player around.
        # We'll position it later, when the player moves.
        # We'll only add it to the light layer when the player turns the light
        # on. We start with the light off.
        radius = PLAYER_LIGHT_RADIUS
        mode = PLAYER_LIGHT_MODE
        color = PLAYER_LIGHT_COLOR
        self.player_light = Light(0, 0, radius, color, mode)
        self.light_layer.add(self.player_light)


        for light_emitter in self.light_emittor_list:
                light = Light(light_emitter.center_x, light_emitter.center_y, 150, (500,0,0), mode='soft')
                self.light_layer.add(light)

        for enemy_spawn in self.enemy_spawn_list:        
                enemy= Enemy()
                enemy.center_x = enemy_spawn.center_x
                enemy.center_y = enemy_spawn.center_y
                self.enemy_list.append(enemy)


        self.skybox_sprite = arcade.load_texture("assets\sky box.png")




    def on_draw(self):
        # Clear the screen to the background color
        arcade.start_render()
        
        # Draw our Scene/ all the sprites
        # --- Light related ---
        # Everything that should be affected by lights gets rendered inside this
        # 'with' statement. Nothing is rendered to the screen yet, just the light
        # layer.
        with self.light_layer:
            arcade.draw_texture_rectangle(self.end_of_map_weight // 2, self.end_of_map_height // 2, self.end_of_map_weight*1.5, self.end_of_map_height*1.5, self.skybox_sprite)
            self.background_list.draw()
            self.wall_list.draw()
            self.ladder_list.draw()
            self.dont_touch_list.draw()
            self.bullet_list.draw()
            self.player_list.draw()
            self.enemy_list.draw()
            self.ar_list.draw()
            self.light_emittor_list.draw()
            self.enemy_spawn_list.draw()
            self.foreground_list.draw()
        
        # Draw the light layer to the screen.
        # This fills the entire screen with the lit version
        # of what we drew into the light layer above.
        self.light_layer.draw(ambient_color=AMBIENT_COLOR)

        # Now draw anything that should NOT be affected by lighting.
        arcade.draw_text("dont die",
                         10 + self.view_left, 10 + self.view_bottom,
                         arcade.color.WHITE, 20)

        


    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(None)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        """elif key == arcade.key.SPACE:
            # --- Light related ---
            # We can add/remove lights from the light layer. If they aren't
            # in the light layer, the light is off.
            if self.player_light in self.light_layer:
                self.light_layer.remove(self.player_light)
            else:
                self.light_layer.add(self.player_light)"""

        self.process_keychange()


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange() 


    
    def on_mouse_press(self, x, y ,botton, modifiers):
        """ Called whenever the mouse button is clicked. """
        

        # Create a bullet
        bullet = Bullet(self.light_layer)
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y
        

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = self.view_left + x #mouse x
        dest_y = self.view_bottom + y #mouse y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle_in_radians = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        bullet.angle = math.degrees(angle_in_radians)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle_in_radians) * BULLET_SPEED
        bullet.change_y = math.sin(angle_in_radians) * BULLET_SPEED
        self.bullet_list.append(bullet)
        

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called whenever the mouse button is clicked. """

        ar_x = self.ar_sprite.center_x
        ar_y = self.ar_sprite.center_y
        

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        mouse_x = self.view_left + x #mouse x
        mouse_y = self.view_bottom + y #mouse y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        ar_x_diff = mouse_x - ar_x
        ar_y_diff = mouse_y - ar_y
        angle_in_radians = math.atan2(ar_y_diff, ar_x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        self.ar_sprite.angle = math.degrees(angle_in_radians)
       

        if angle_in_radians > math.pi / 2 or angle_in_radians < -math.pi/2:
            self.player_sprite.character_face_direction = LEFT_FACING
            self.ar_sprite.AR_face_direction = AR_LEFT_FACING
        else:
            self.player_sprite.character_face_direction = RIGHT_FACING
            self.ar_sprite.AR_face_direction = AR_RIGHT_FACING
        

    

    def on_update(self, delta_time):  
        
        """ move player with physics engine"""         
        self.physics_engine.update()

        """ Update animations """
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        self.background_list.update_animation(delta_time)
        self.player_list.update_animation(delta_time)
        self.enemy_list.update_animation(delta_time)
    
        "ar"
        self.ar_list.update_animation(delta_time)
        self.ar_sprite.position = self.player_sprite.position

        "shooting" 
        # Call update on all sprites
        self.bullet_list.update()

        for bullet in self.bullet_list:
            # Check this bullet to see if it hit a wall
            hits_wall = arcade.check_for_collision_with_list(bullet, self.wall_list) 

                # If it did, get rid of the bullet
            if len(hits_wall) > 0:
                bullet.kill()
                    
                'if the bullet flies off-screen, remove it'
            if bullet.center_x > self.end_of_map_weight or bullet.center_x < -100 or bullet.center_y > self.end_of_map_height or bullet.center_y < -100:
                bullet.kill()
                # think about changing this to make the bullet delet when it leaves the view port


        'enemy'
        self.enemy_list.update()

        for enemy in self.enemy_list:

            

            if len(arcade.check_for_collision_with_list(enemy, self.bullet_list)) > 0:
               enemy.take_20_health()
               bullet.kill()


            # If the enemy hit a wall, reverse
            
            if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                enemy.change_x *= -1

            if enemy.health <100 or arcade.has_line_of_sight(self.player_sprite.position,
                                                enemy.position,
                                                self.wall_list) and self.player_sprite.center_x -100 < enemy.center_x and self.player_sprite.center_x +100 > enemy.center_x: 
                enemy.awake = True

            if enemy.awake == True and arcade.has_line_of_sight(self.player_sprite.position,
                                                enemy.position,
                                                self.wall_list):
                "enemy friction"
                if enemy.change_x > ENEMY_FRICTION:
                    enemy.change_x -= ENEMY_FRICTION
                elif enemy.change_x < -ENEMY_FRICTION:
                    enemy.change_x += ENEMY_FRICTION
                else:
                    enemy.change_x = 0
                "enemy "
                if self.player_sprite.center_x < enemy.center_x:
                   enemy.change_x -= ENEMY_ACCELERATION_RATE
                elif self.player_sprite.center_x > enemy.center_x:
                    enemy.change_x += ENEMY_ACCELERATION_RATE

                if enemy.change_x > ENEMY_MAX_SPEED:
                    enemy.change_x = ENEMY_MAX_SPEED
                elif enemy.change_x < -ENEMY_MAX_SPEED:
                    enemy.change_x = -ENEMY_MAX_SPEED
            
                """elif enemy.change_x > ENEMY_MAX_WONDER_SPEED:
                    enemy.change_x = ENEMY_MAX_WONDER_SPEED
                elif enemy.change_x < -ENEMY_MAX_WONDER_SPEED:
                    enemy.change_x = -ENEMY_MAX_WONDER_SPEED"""
        
                if arcade.has_line_of_sight(self.player_sprite.position,
                                                enemy.position,
                                                self.wall_list) and self.player_sprite.center_x -200 < enemy.center_x and self.player_sprite.center_x +200 > enemy.center_x: 
                        enemy.attacking = True
                        if enemy.on_attack == True:
                            self.player_sprite.take_20_health()

            
                

           

            
        

           
       


       
        "moving platforms"

        # Update walls, used with moving platforms
        self.wall_list.update()

        # See if the wall hit a boundary and needs to reverse direction.
        for wall in self.wall_list:

            if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
                wall.change_x *= -1
            if wall.boundary_left and wall.left < wall.boundary_left and wall.change_x < 0:
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
                wall.change_y *= -1

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

        # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(None)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(None)

        "manage level"
        # See if the user got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map_weight and self.level <3:
            # Advance to the next level
            self.level += 1

            # Load the next level
            self.setup(self.level)

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

            " player light related "
        # We can easily move the light by setting the position,
        # or by center_x, center_y.
        self.player_light.position = self.player_sprite.position
    
       


    # --- Manage Scrolling ---

        # Track if we need to change the viewport
        changed_viewport = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
          


        


  
    

        

def main():
    """ Main method """
    window = MyGame()
    window.setup(window.level)
    arcade.run()


if __name__ == "__main__":
    main()