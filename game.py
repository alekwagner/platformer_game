import arcade
import math
import os
from arcade.color import WHITE
from arcade.experimental.lights import Light, LightLayer
import time
from pyglet.libs.win32.constants import IS_TEXT_UNICODE_ASCII16
from consts import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, MUSIC_VOLUME, PLAYER_START_X, PLAYER_START_Y, GRID_PIXEL_SIZE, TILE_SCALING, PLAYER_LIGHT_RADIUS, PLAYER_LIGHT_MODE, PLAYER_LIGHT_COLOR, GRAVITY, AMBIENT_COLOR, PLAYER_MOVEMENT_SPEED, PLAYER_JUMP_SPEED, BULLET_SPEED, LEFT_FACING, RIGHT_FACING, ENEMY_FRICTION, ENEMY_ACCELERATION_RATE, ENEMY_MAX_SPEED, ENEMY_TURN_RATE, ENEMY_LEFT_FACING, ENEMY_RIGHT_FACING, LEFT_VIEWPORT_MARGIN, RIGHT_VIEWPORT_MARGIN, TOP_VIEWPORT_MARGIN, BOTTOM_VIEWPORT_MARGIN

from characters.player import PlayerCharacter
from characters.enemy import Enemy
from weapons.ar import AR
from weapons.bullet import Bullet
from threading import Timer

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
        self.ammo_list = None
        self.crate_list = None

        self.bullet_sprite= None

        #var for gun
        self.ar_sprite = None

       #variable for player spirt
        self.player_sprite = None

        self.enemy_sprite = None

        self.skybox_sprite = None

        self.info_sprite = None

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
        self.gun_sound = arcade.sound.load_sound("sound\gun shot.mp3")
        self.hit_sound = arcade.sound.load_sound("sound\screaming.mp3")
        self.breathing_sound = arcade.sound.load_sound("sound\player_breathing.mp3")
     
     # --- Light related ---
        # List of all the lights
        self.light_layer = None
        # Individual light we move with player, and turn on/off
        self.player_light = None

        self.bullet_light = None

        #from python arcade
        # Variables used to manage our music. See setup() for giving them
        # values.
        self.music_list = []
        self.current_song_index = 0
        self.current_player = None
        self.music = None

        self.draw_info = True

    def advance_song(self):
        #Advance our pointer to the next song. This does NOT start the song. 
        self.current_song_index += 1
        if self.current_song_index >= len(self.music_list):
            self.current_song_index = 0
        
    def play_song(self):
        #Play the song. 
         # Stop what is currently playing.
        if self.music:
            self.music.stop(self.current_player)
 
         # Play the next song
        self.music = arcade.Sound(self.music_list[self.current_song_index], streaming=True)
        self.current_player = self.music.play(MUSIC_VOLUME)
        time.sleep(0.0)

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
        self.ammo_list = arcade.SpriteList()
        self.crate_list = arcade.SpriteList()

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

        ammo_layer_name = 'ammo'

        crate_layer_name = 'crate'

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

        #ammo
        self.ammo_list = arcade.tilemap.process_layer(my_map, ammo_layer_name, scaling=TILE_SCALING )

        #crate
        self.crate_list = arcade.tilemap.process_layer(my_map, crate_layer_name, scaling=TILE_SCALING, use_spatial_hash=True)

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
        
        # Create a light layer, used to render things to, then post-process and
        # add lights. This must match the screen size.
        self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)
        
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

        self.engines_list = []
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY,
                                                             ladders=self.ladder_list)
        self.engines_list.append(self.physics_engine)

        for enemy in self.enemy_list:
            enemy_engine = arcade.PhysicsEnginePlatformer(enemy, self.wall_list, GRAVITY)
            self.engines_list.append(enemy_engine)

        for crate in self.crate_list:
            crate_engine = arcade.PhysicsEnginePlatformer(crate, self.wall_list, GRAVITY)
            self.engines_list.append(crate_engine)

        self.skybox_sprite = arcade.load_texture("assets\sky box.png")

        self.info_sprite = arcade.load_texture("assets\info.png")

        #from arcade
        #music list
        # List of music
        self.music_list = ["sound/final background noise.mp3", "sound\music track.mp3", "sound\monster sounds.mp3"]
        # Array index of what to play
        self.current_song_index = 0
        # Play the song
        self.play_song()

        arcade.play_sound(self.breathing_sound,0.25,0,True)
        
    def on_draw(self):
        # Clear the screen to the background color
        arcade.start_render()
        
        position = self.music.get_stream_position(self.current_player)
        length = self.music.get_length()
        size = 20
        margin = size * .5
 
        # Print time elapsed and total
        y = SCREEN_HEIGHT - (size + margin)
        text = f"{int(position) // 60}:{int(position) % 60:02} of {int(length) // 60}:{int(length) % 60:02}"
        arcade.draw_text(text, 0, y, arcade.csscolor.BLACK, size)
 
        # Print current song
        y -= size + margin
        text = f"Currently playing: {self.music_list[self.current_song_index]}"
        arcade.draw_text(text, 0, y, arcade.csscolor.BLACK, size)

        # Draw our Scene/ all the sprites
        # --- Light related ---
        # Everything that should be affected by lights gets rendered inside this
        # 'with' statement. Nothing is rendered to the screen yet, just the light
        # layer.
        with self.light_layer:
            arcade.draw_texture_rectangle(self.get_viewport()[0], self.get_viewport()[2], self.end_of_map_weight*1.5, self.end_of_map_height*1.5, self.skybox_sprite)
            self.background_list.draw()
            self.wall_list.draw()
            self.ladder_list.draw()
            self.dont_touch_list.draw()
            self.bullet_list.draw()
            self.player_list.draw()
            self.enemy_list.draw()
            self.ar_list.draw()
            self.ammo_list.draw()
            self.crate_list.draw()
            self.light_emittor_list.draw()
            self.enemy_spawn_list.draw()
            self.foreground_list.draw()
        
        # Draw the light layer to the screen.
        # This fills the entire screen with the lit version
        # of what we drew into the light layer above.
        self.light_layer.draw(ambient_color=AMBIENT_COLOR)

        # Now draw anything that should NOT be affected by lighting.
        arcade.draw_text( str(self.player_sprite.ammo)  ,
                          110 + self.view_left, 50 + self.view_bottom,
                         arcade.color.WHITE, 20)
        arcade.draw_text(str("ammo:"),
                          30 + self.view_left, 50 + self.view_bottom,
                         arcade.color.WHITE, 20)
        if self.player_sprite.center_x >= self.end_of_map_weight and self.level == 3:
                        arcade.draw_text(str("THE END"), 300, 300, WHITE, 12)   
                                      
        vp_x = self.get_viewport()[0]
        vp_y = self.get_viewport()[2]
        arcade.draw_lrtb_rectangle_filled(vp_x, vp_x + (SCREEN_WIDTH/100) * self.player_sprite.health, vp_y + 30, vp_y, arcade.color.RED)

        if self.draw_info:
            arcade.draw_texture_rectangle(400, 400, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, self.info_sprite)
      
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

        if key == arcade.key.L:
            self.setup(self.level)

        if self.draw_info:
            self.draw_info = False

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        #Called when the user releases a key. 

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
        #Called whenever the mouse button is clicked. 

        if self.player_sprite.ammo > 0:
            # Create a bullet
            bullet = Bullet(self.light_layer)
            arcade.play_sound(self.gun_sound)
            self.player_sprite.ammo -= 1

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

        self.ar_sprite.angle = math.degrees(angle_in_radians)
       
        if angle_in_radians > math.pi / 2 or angle_in_radians < -math.pi/2:
            self.player_sprite.character_face_direction = LEFT_FACING
            self.ar_sprite.AR_face_direction = LEFT_FACING
        else:
            self.player_sprite.character_face_direction = RIGHT_FACING
            self.ar_sprite.AR_face_direction = RIGHT_FACING
        
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
            self.ar_sprite.AR_face_direction = LEFT_FACING
        else:
            self.player_sprite.character_face_direction = RIGHT_FACING
            self.ar_sprite.AR_face_direction = RIGHT_FACING

    def on_update(self, delta_time):  

        position = self.music.get_stream_position(self.current_player)
 
         # The position pointer is reset to 0 right after we finish the song.
         # This makes it very difficult to figure out if we just started playing
         # or if we are doing playing.
        if position == 0.0:
            self.advance_song()
            self.play_song()
        
        # move player with physics engine        
        # self.physics_engine.update()
        for engines in self.engines_list:
            engines.update()

        #Update animations 
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
    
        #ar
        self.ar_list.update_animation(delta_time)
        self.ar_sprite.position = self.player_sprite.position

        #shooting
        # Call update on all sprites
        self.bullet_list.update()

        for bullet in self.bullet_list:
            # Check this bullet to see if it hit a wall
            hits_wall = arcade.check_for_collision_with_list(bullet, self.wall_list) 

                # If it did, get rid of the bullet
            if len(hits_wall) > 0:
                bullet.kill()
                    
                #if the bullet flies off-screen, remove it
            if bullet.center_x > self.end_of_map_weight or bullet.center_x < -100 or bullet.center_y > self.end_of_map_height or bullet.center_y < -100:
                bullet.kill()
                # think about changing this to make the bullet delet when it leaves the view port
        #ammo
        self.ammo_list.update()

        for ammo in self.ammo_list:
            if len(arcade.check_for_collision_with_list( self.player_sprite, self.ammo_list)) > 0:
                self.player_sprite.ammo += 20
                ammo.remove_from_sprite_lists()

        # crate
        self.crate_list.update()

        for crate in self.crate_list:
            if len(arcade.check_for_collision_with_list( self.player_sprite, self.crate_list)) > 0:
                crate.change_x = self.player_sprite.change_x
            else:
                crate.change_x = 0
                     
        #enemy
        self.enemy_list.update()

        for enemy in self.enemy_list:                         

            #death
            if len(arcade.check_for_collision_with_list(enemy, self.bullet_list)) > 0:
               enemy.take_20_health()
               bullet.kill()
               
            #If the enemy hit a wall, reverse
            if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                enemy.change_x *= -1
            
            #seeing and chasing
            if  arcade.has_line_of_sight(self.player_sprite.position,
                                                enemy.position,
                                                self.wall_list):

                if enemy.scream == True:
                    arcade.play_sound(self.hit_sound,0.01)
                    enemy.scream = False

                #enemy friction
                if enemy.change_x > ENEMY_FRICTION:
                    enemy.change_x -= ENEMY_FRICTION
                elif enemy.change_x < -ENEMY_FRICTION:
                    enemy.change_x += ENEMY_FRICTION
                else:
                    enemy.change_x = 0
                #enemy chase player movement
                if self.player_sprite.center_x +1 < enemy.center_x:
                   enemy.change_x -= ENEMY_ACCELERATION_RATE
                   
                elif self.player_sprite.center_x - 1 > enemy.center_x:
                    enemy.change_x += ENEMY_ACCELERATION_RATE

                else:
                    enemy.change_x = 0

                #enemy max speed
                if enemy.change_x > ENEMY_MAX_SPEED:
                    enemy.change_x = ENEMY_MAX_SPEED
                elif enemy.change_x < -ENEMY_MAX_SPEED:
                    enemy.change_x = -ENEMY_MAX_SPEED

            if arcade.has_line_of_sight(self.player_sprite.position,
                                                                enemy.position,
                                                                self.wall_list) and self.player_sprite.center_x -100 < enemy.center_x and self.player_sprite.center_x +100 > enemy.center_x and self.player_sprite.center_y -200 < enemy.center_y and self.player_sprite.center_y +200 > enemy.center_y: 
                self.player_in_striking_range = True
            else: 
                self.player_in_striking_range = False

            if self.player_in_striking_range == True:             
                attack_timer = Timer(0.8, self.check_striking_distance)
                attack_timer.start()
                                    
            #enemy turning and face direction
            if enemy.change_x < -ENEMY_TURN_RATE:
                enemy.face_direction = ENEMY_LEFT_FACING

            if enemy.change_x > ENEMY_TURN_RATE:
                enemy.face_direction = ENEMY_RIGHT_FACING

            if enemy.center_y == -100:
                enemy.kill()

        """
        moving platforms"
        """
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
            self.setup()

        # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(None)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):
            self.player_sprite.take_20_health()
            if self.player_sprite.health <= 0:
                self.setup(self.level)
        
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(None)

        # ---manage level---
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

            #--- player light related ---
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
                                    
    def check_striking_distance (self):  
        if self.player_in_striking_range == True:
            self.player_sprite.take_20_health()
            if self.player_sprite.health <= 0:
                self.setup(self.level)
            arcade.play_sound(self.hit_sound, 0.005)

def main():
    # Main method    
    window = MyGame()
    window.setup(window.level)
    arcade.run()

if __name__ == "__main__":
    main()