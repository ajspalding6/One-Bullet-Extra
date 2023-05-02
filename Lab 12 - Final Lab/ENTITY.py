import CONSTANTS
import arcade


def load_texture_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]


class Entity(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.facing_direction = CONSTANTS.RIGHT_FACING
        self.cur_texture = 0
        self.scale = CONSTANTS.PLAYER_SCALE
        main_path = f"character_maleAdventurer"
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)
        self.texture = self.idle_texture_pair[0]
        self.set_hit_box(self.texture.hit_box_points)