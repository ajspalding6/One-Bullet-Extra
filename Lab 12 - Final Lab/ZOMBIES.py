import random
import arcade
import CONSTANTS


def load_texture_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]


class Zombie(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)

        self.speed = CONSTANTS.ZOMBIE_SPEED
        self.hit_count = 3
        self.center_x = random.randrange(1418, 2143)
        self.center_y = 2143
        self.change_x = random.randrange(1, 10)
        self.change_y = 0
        self.facing_direction = CONSTANTS.RIGHT_FACING
        self.cur_texture = 0
        self.scale = CONSTANTS.PLAYER_SCALE
        main_path = f"character_zombie"
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.facing_direction == CONSTANTS.RIGHT_FACING:
            self.facing_direction = CONSTANTS.LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == CONSTANTS.LEFT_FACING:
            self.facing_direction = CONSTANTS.RIGHT_FACING
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]






