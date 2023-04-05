import arcade
import random
import math

PLAYER_SCALE = .8
AMMO_SCALE = .07
ZOMBIE_SCALE = .5
AMMO_COUNT = 50
ZOMBIE_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

MOVEMENT_SPEED = 5


class Ammo(arcade.Sprite):

    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):

        self.center_y -= 1

        if self.top < 0:
            self.reset_pos()


class Zombie(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)
        self.circle_angle = 0
        self.circle_radius = 0
        self.circle_speed = 0.008
        self.circle_center_x = 0
        self.circle_center_y = 0

    def update(self):
        self.center_x = self.circle_radius * math.sin(self.circle_angle) \
                        + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) + \
                        self.circle_center_y

        self.circle_angle += self.circle_speed

    """def freeze(self):
        self.center_x = self.center_x
        self.center_y = self.center_y
        self.change_x = self.change_x
        self.change_y = self.change_y"""


class Player(arcade.Sprite):
    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:

            self.left = 0

        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0

        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "Zombie-Ammo starter")

        self.ammo_list = None
        self.player_list = None
        self.zombie_list = None

        self.player_sprite = None
        self.score = 0

        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.ammo_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()

        self.score = 0

        self.player_sprite = Player("character_malePerson_idle.png", PLAYER_SCALE )
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)

        for i in range(AMMO_COUNT):

            ammo = Ammo("ammo2", AMMO_SCALE)

            ammo.center_x = random.randrange(SCREEN_WIDTH)
            ammo.center_y = random.randrange(SCREEN_HEIGHT)

            self.ammo_list.append(ammo)

        for i in range(ZOMBIE_COUNT):

            zombie = Zombie("character_zombie_idle.png", ZOMBIE_SCALE)

            zombie.circle_center_x = random.randrange(SCREEN_WIDTH)
            zombie.circle_center_y = random.randrange(SCREEN_HEIGHT)

            zombie.circle_radius = random.randrange(10, 200)

            zombie.circle_angle = random.random() * 2 * math.pi

            self.zombie_list.append(zombie)

    def on_draw(self):
        arcade.start_render()

        self.ammo_list.draw()
        self.zombie_list.draw()


        self.player_list.draw()

        score = f"Score: {self.score}"
        arcade.draw_text(score, 10, 20, arcade.color.WHITE, 14)


    def update(self, delta_time):
        self.player_list.update()
        self.zombie_list.update()
        self.ammo_list.update()

        ammo_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.ammo_list)
        zombie_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.zombie_list)

        for ammo in ammo_hit_list:
            ammo.reset_pos()
            self.score += 1

        for zombie in zombie_hit_list:
            zombie.remove_from_sprite_lists()
            self.score -= 1

        """if len(zombie_hit_list) == 0:
            self.zombie.freeze()
            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text("GAME OVER", 400, 400, arcade.color.RED, 25)"""




    def on_key_press(self, key, modifiers):

        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED

        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED

        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0

        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
