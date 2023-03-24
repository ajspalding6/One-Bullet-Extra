import arcade
import random
import math

# All the constants
PLAYER_SCALE = .8
AMMO_SCALE = .07
ZOMBIE_SCALE = .5
AMMO_COUNT = 25
ZOMBIE_COUNT = 40
ZOMBIE_CHECK = ZOMBIE_COUNT - 5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
MOVEMENT_SPEED = 5

# Declares the Ammo class and holds the logic


class Ammo(arcade.Sprite):
    def __init__(self, file, scale):
        super().__init__(file, scale)

# Resets the position of the ammo
    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

# Updates the positions of the ammo. Moves it 1 pixel down a time
    def update(self):
        self.center_y -= 1
# If the ammo reaches the top it resets its position to off the screen
        if self.top < 0:
            self.reset_pos()

# Declares the zombie class and holds the logic


class Zombie(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.circle_angle = 0
        self.circle_radius = 0
        self.circle_speed = 0.008
        self.circle_center_x = 0
        self.circle_center_y = 0

# Moves the zombies in circles
    def update(self):
        self.center_x = self.circle_radius * math.sin(self.circle_angle) + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) + self.circle_center_y
        self.circle_angle += self.circle_speed


# Declares the player class and holds the logic

class Player(arcade.Sprite):
    # Moves the player based on the key pressed
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


# Declares the game itself and holds the game logic
class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Zombie-Ammo starter")
        self.ammo_sound = arcade.load_sound("confirmation_004.ogg")
        self.zombie_sound = arcade.load_sound("error_004.ogg")
        self.ammo_list = None
        self.player_list = None
        self.zombie_list = None
        self.player_sprite = None
        self.score = 0
        self.ammo_check = 0
        self.zombie_score = 0
        self.game_over = False
        self.win = False
        arcade.set_background_color(arcade.color.SKY_BLUE)
# Loads all the textures and creates the game logic

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.ammo_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        self.score = 0
        self.ammo_check = 0
        self.zombie_score = 0
        self.player_sprite = Player("character_malePerson_idle.png", PLAYER_SCALE)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)
# Repeats creating the ammo and zombies till they are all created
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

# Draws everything and holds the logic for winning and losing the game
    def on_draw(self):
        arcade.start_render()
        self.ammo_list.draw()
        self.zombie_list.draw()
        self.player_list.draw()
        score = f"Score: {self.score}"
        ammo_score = f"Ammo Count: ({self.ammo_check}/25)"
        zombie_score = f"Zombie Count: ({self.zombie_score}/5)"
        arcade.draw_text(score, 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(ammo_score, 10, 40, arcade.color.GREEN, 14)
        arcade.draw_text(zombie_score, 10, 60, arcade.color.RED, 14)
        if self.game_over:
            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text("GAME OVER", 280, 400, arcade.color.RED, 25)
        if self.win:
            arcade.set_background_color(arcade.color.GOLD)
            arcade.draw_text("YOU WON", 280, 400, arcade.color.ROYAL_BLUE, 40)

    def update(self, delta_time):
        if not self.game_over and not self.win:
            self.player_list.update()
            self.zombie_list.update()
            self.ammo_list.update()
            ammo_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.ammo_list)
            zombie_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.zombie_list)
            for ammo in ammo_hit_list:
                ammo.reset_pos()
                self.score += 1
                self.ammo_check += 1
                arcade.play_sound(self.ammo_sound)
            for zombie in zombie_hit_list:
                zombie.remove_from_sprite_lists()
                self.score -= 1
                self.zombie_score += 1
                arcade.play_sound(self.zombie_sound)
        if len(self.ammo_list) <= self.ammo_check:
            self.win = True
        if len(self.zombie_list) <= ZOMBIE_CHECK:
            self.game_over = True

# Holds the logic for moving the keys
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


# Calls each class and renders it
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
