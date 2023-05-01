import arcade
import random
from pyglet.math import Vec2
# ALL GRAPHICS AND SOUNDS WERE RETRIEVED FROM KENNLEY/ARCADE
# Declaring constants
SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 800
BORDER_WIDTH = 2048
BORDER_HEIGHT = 1536
MAP_WIDTH = 2016
MAP_HEIGHT = 1568
SCREEN_TITLE = "lab_09"
VIEWPOINT_MARGIN = 20
CAMERA_SPEED = 0.3

PLAYER_SPEED = 7.5
PLAYER_SCALE = 0.5
RIGHT_FACING = 0
LEFT_FACING = 1

AMMO_COUNT = 50
AMMO_SCALE = 0.07

UPDATES_PER_FRAME = 4


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = PLAYER_SCALE

        # Adjust the collision box. Default includes too much empty space
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        main_path = "character_maleAdventurer"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.ammo_sound = arcade.load_sound("confirmation_004.ogg")
        self.player_list = True
        self.wall_list = None
        self.border_list = None
        self.ammo_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.score = 0
        # up
        self.w_pressed = False
        # left
        self.a_pressed = False
        # down
        self.s_pressed = False
        # right
        self.d_pressed = False

        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

    def setup(self):
        space_between_pixel = 64
        self.score = 0
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.border_list = arcade.SpriteList()
        self.ammo_list = arcade.SpriteList()

        self.player_sprite = Player()

        self.player_sprite.center_x = BORDER_WIDTH/2
        self.player_sprite.center_y = BORDER_HEIGHT/2
        self.player_list.append(self.player_sprite)
        """for x in range (0+32, MAP_WIDTH-64, 64): # bottom
            border = arcade.Sprite(":resources:images/tiles/lockRed.png", SPRITE_SCALING)
            border.left = x
            border.top = x
            self.border_list.append(border)
            STAIR CODE
            """
        #  Borders
        for y in (0, BORDER_HEIGHT):  # Top and bottom borders
            for x in range(0, BORDER_WIDTH+64, SPRITE_SIZE):
                border = arcade.Sprite(":resources:images/tiles/lockRed.png", SPRITE_SCALING)
                border.left = x
                border.bottom = y
                self.wall_list.append(border)

        for x in (0, BORDER_WIDTH):  # Right and left borers
            for y in range(0, BORDER_HEIGHT, SPRITE_SIZE):
                border = arcade.Sprite(":resources:images/tiles/lockRed.png", SPRITE_SCALING)
                border.left = x
                border.bottom = y
                self.wall_list.append(border)
        #  Walls

        for x in range(160, MAP_WIDTH, space_between_pixel):
            """space_between_number = random.randrange(3)
            if space_between_number == 0:
                space_between_pixel = 64
            elif space_between_number == 1:
                space_between_pixel = 128
            else:
                space_between_pixel = 256
                I spent about 2 1/2 hours created this system and I thought it worked perfectly,
                 but I realized it changes nothing whether its there or not"""

            for y in range(160, MAP_HEIGHT, 128):
                if random.randrange(32) > 0:
                    #  Randomize which block to use
                    if random.randrange(2) == 0:
                        wall = arcade.Sprite(":resources:images/tiles/stoneCenter.png", SPRITE_SCALING)
                    else:
                        wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
        #  Make sure ammo isn't on the walls
        for i in range(AMMO_COUNT):
            ammo = arcade.Sprite("../Lab 08 - Sprites/ammo2", AMMO_SCALE)
            ammo_placed_successfully = False

            while not ammo_placed_successfully:

                ammo.center_x = random.randrange(MAP_WIDTH)
                ammo.center_y = random.randrange(MAP_HEIGHT)

                wall_hit_list = arcade.check_for_collision_with_list(ammo, self.wall_list)
                ammo_hit_list = arcade.check_for_collision_with_list(ammo, self.ammo_list)
                border_hit_list = arcade.check_for_collision_with_list(ammo, self.border_list)

                if len(wall_hit_list) == 0 and len(ammo_hit_list) == 0 and len(border_hit_list) == 0:
                    ammo_placed_successfully = True

            self.ammo_list.append(ammo)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        arcade.set_background_color(arcade.color.ROYAL_BLUE)

    def on_draw(self):
        self.clear()
        score = f"Score: {self.score}"
        self.camera_sprites.use()
        self.wall_list.draw()
        self.border_list.draw()
        self.player_list.draw()
        self.ammo_list.draw()
        self.camera_gui.use()
        arcade.draw_text(score, 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.S:
            self.s_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.S:
            self.s_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False

    def on_update(self, delta_time):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        self.ammo_list.update()
        ammo_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.ammo_list)
        for ammo in ammo_hit_list:
            self.score += 1
            arcade.play_sound(self.ammo_sound)
            ammo.remove_from_sprite_lists()
        if self.w_pressed and not self.s_pressed:
            self.player_sprite.change_y = PLAYER_SPEED
        elif self.s_pressed and not self.w_pressed:
            self.player_sprite.change_y = - PLAYER_SPEED
        elif self.a_pressed and not self.d_pressed:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif self.d_pressed and not self.a_pressed:
            self.player_sprite.change_x = PLAYER_SPEED

        self.player_list.update()
        self.player_list.update_animation()
        self.physics_engine.update()

        self.scroll_to_player()

    def scroll_to_player(self):

        position = Vec2(self.player_sprite.center_x - self.width / 2,

                        self.player_sprite.center_y - self.height / 2)

        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))

        self.camera_gui.resize(int(width), int(height))


def main():
    window = MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
