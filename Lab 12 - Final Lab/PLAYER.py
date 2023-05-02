import CONSTANTS
import ENTITY
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


class Player(ENTITY.Entity):
    def __init__(self):
        super().__init__()
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.hit_count_player = 1

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.facing_direction == CONSTANTS.RIGHT_FACING:
            self.facing_direction = CONSTANTS.LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == CONSTANTS.LEFT_FACING:
            self.facing_direction = CONSTANTS.RIGHT_FACING
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.facing_direction]
            return
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]