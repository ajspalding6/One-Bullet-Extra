import arcade
from pyglet.math import Vec2
import CONSTANTS


def load_texture_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]

class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        # Default to facing right
        self.facing_direction = CONSTANTS.RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = CONSTANTS.PLAYER_SCALE

        main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"

        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = CONSTANTS.RIGHT_FACING

        self.cur_texture = 0

        self.scale = CONSTANTS.PLAYER_SCALE

        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        main_path = "character_maleAdventurer"

        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.character_face_direction == CONSTANTS.RIGHT_FACING:
            self.character_face_direction = CONSTANTS.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == CONSTANTS.LEFT_FACING:
            self.character_face_direction = CONSTANTS.RIGHT_FACING
        elif self.change_y < 0 and self.character_face_direction == CONSTANTS.UP_FACING:
            self.character_face_direction = CONSTANTS.UP_FACING
        elif self.change_y > 0 and self.character_face_direction == CONSTANTS.DOWN_FACING:
            self.character_face_direction = CONSTANTS.DOWN_FACING

        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        self.cur_texture += 1
        if self.cur_texture > 7 * CONSTANTS.UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // CONSTANTS.UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

        self.player_list = True

        self.wall_list = None

        self.zombie_list = None

        self.ammo_list = None

        self.player_sprite = None
        self.physics_engine = None
        self.score = 0

        self.ammo_amount = 0
        self.round_count = 0
        self.pause = False

        self.game_over = False
        self.background = None

        # Space/jump
        self.space_bar_pressed = False
        # left
        self.a_pressed = False
        # down
        self.s_pressed = False
        # right
        self.d_pressed = False

        self.title_map = None

        self.camera_sprites = arcade.Camera(CONSTANTS.DEFAULT_SCREEN_WIDTH, CONSTANTS.DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(CONSTANTS.DEFAULT_SCREEN_WIDTH, CONSTANTS.DEFAULT_SCREEN_HEIGHT)

    def setup(self):
        self.score = 0

        self.player_list = arcade.SpriteList()

        self.wall_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()

        self.player_sprite = Player()
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 2000

        self.player_list.append(self.player_sprite)

        self.background = arcade.load_texture("background.jpg")

        map_name = "Map_final_game.tmj"
        self.title_map = arcade.load_tilemap(map_name, CONSTANTS.TILE_SCALING)
        self.wall_list = self.title_map.sprite_lists["Walls_and_blocks"]

        zombie = arcade.Sprite("character_zombie_idle.png", CONSTANTS.SPRITE_SCALING)

        zombie.bottom = CONSTANTS.SPRITE_SIZE * 2
        zombie.top = CONSTANTS.SPRITE_SIZE * 21

        zombie.boundary_top = CONSTANTS.SPRITE_SIZE * 8
        zombie.boundary_bottom = CONSTANTS.SPRITE_SIZE * 3

        zombie.change_x = 2
        self.zombie_list.append(zombie)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=CONSTANTS.GRAVITY)

    def on_draw(self):

        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, CONSTANTS.DEFAULT_SCREEN_WIDTH,
                                            CONSTANTS.DEFAULT_SCREEN_HEIGHT, self.background)
        score = f"Score: {self.score}"
        self.camera_sprites.use()
        self.wall_list.draw()
        self.zombie_list.draw()
        self.player_list.draw()
        self.camera_gui.use()

        arcade.draw_text(score, 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.S:
            self.s_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True
        elif key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = CONSTANTS.JUMP_SPEED
        
    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.S:
            self.s_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False
        elif key == arcade.key.SPACE:
            self.space_bar_pressed = False

    def on_update(self, delta_time):
        self.player_sprite.change_x = 0

        self.zombie_list.update()

        if self.a_pressed and not self.d_pressed:
            self.player_sprite.change_x = -CONSTANTS.PLAYER_SPEED
        elif self.d_pressed and not self.a_pressed:
            self.player_sprite.change_x = CONSTANTS.PLAYER_SPEED

        self.player_list.update()
        self.player_list.update_animation()
        self.physics_engine.update()

        if len(arcade.check_for_collision_with_list(self.player_sprite, self.zombie_list)) > 0:
            self.game_over = True

        self.scroll_to_player()

    def scroll_to_player(self):

        position = Vec2(self.player_sprite.center_x - self.width / 3,

                        self.player_sprite.center_y - self.height / 3)

        self.camera_sprites.move_to(position, CONSTANTS.CAMERA_SPEED)

    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))

        self.camera_gui.resize(int(width), int(height))


def main():
    window = MyGame(CONSTANTS.DEFAULT_SCREEN_WIDTH, CONSTANTS.DEFAULT_SCREEN_HEIGHT, CONSTANTS.SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
