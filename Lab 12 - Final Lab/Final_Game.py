import random
import arcade
from pyglet.math import Vec2
import CONSTANTS
import PLAYER
import ZOMBIES
"""
Controls: 
<-a
d ->
space = jump
mouse/trackpad_click = shoot
e = pickup items (bullets, apples, power_ups)
esc = pause (any above key will un_pause)

Zombies take 3 hits to die
Player starts at 1 life with 5 max
Power-ups will stack

Objective:
Survive as many rounds as possible against a horrific zombie hoard by collecting ammo, health, and power_ups with the 
points you get from killing them in this epic gamed call "One Bullet Extra"
"""


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

        # Screen related
        self.pause = False
        self.game_over = False
        self.start_game = False
        self.game_over_text = None
        self.round_number_text = None
        self.reload_text = None
        self.background_music = arcade.load_sound("background_music.mp3")
        """background music. Chosic: https://www.chosic.com/download-audio/25499/"""
        self.background_music_player = self.background_music.play(loop=True)
        #  Player related
        self.player_list = True
        self.player_sprite = None
        self.player_hit_list = None
        self.spawn = None
        self.player_hit_sound = arcade.load_sound("player_damage.mp3")
        """When the player gets hit. freesound: https://freesound.org/people/Raclure/sounds/458867/"""

        #  Zombie related
        self.zombie_list = None
        self.zombie_bullet_hit_sound = arcade.load_sound("zombie_bullet.mp3")
        """When bullet hits zombie. fesliyanstudios:https://www.fesliyanstudios.com
        /sound-effects-search.php?q=zombie+aggressive+attack"""

        #  Bullet/ammo related
        self.direction = True
        self.bullet_list = None  # A list of the visible projectiles
        self.ammo_hit_list = None
        self.ammo_full = True
        self.gun_shot = arcade.load_sound("gun_shot.mp3")
        """When the gun is fired. mixkit: https://mixkit.co/free-sound-effects/gun/"""
        self.ammo_pickup_sound = arcade.load_sound("gun_reload.mp3")
        """When picking up ammo. fesliyanstudios: https://www.fesliyanstudios.com/
        sound-effects-search.php?q=Pushing+magazine+into+gun+"""
        self.ammo_list = None  # A list of the floating ammo images that are used for reloading
        self.ammo = None
        self.mag_amount = None
        self.ammo_amount = None

        #  Wall/map related
        self.round_change_sound = arcade.load_sound("round_change.mp3")
        """A zombie breath when the round changes. fesliyanstudios: https://www.fesliyanstudios.com/
        sound-effects-search.php?q=Zombie+breath"""
        self.wall_hit_list = None
        self.wall_list = None
        self.background = None
        self.title_map = None
        self.view_bottom = 0
        self.view_left = 0
        self.grid_size = None
        self.game_over = False
        self.pause = False
        self.round_delay = None
        self.total_time = None
        self.game_over = False
        self.pause = False
        self.physics_engine = None
        self.score = 0
        self.round_count = None
        self.start = 1035
        self.end = 12498

        #  Food related
        self.food_list = None
        self.food_sprite = None
        self.food_sound = None
        self.food_pickup_sound = arcade.load_sound("confirmation_004.ogg")
        """When the apples are picked up. kenney:https://kenney.nl/assets/interface-sounds"""

        #  Power-up related
        self.power_up_hit_list = None
        self.power_up_list = None
        self.power_up_sound = None
        self.power_up_number = None
        self.power_up_on = None

        # Keyboard related
        # Space/jump
        self.space_bar_pressed = False
        # left
        self.a_pressed = False
        # down
        self.s_pressed = False
        # right
        self.d_pressed = False
        # Pickup ammo
        self.e_pressed = False
        #  Shoot
        self.left_click_pressed = False
        #  Pause
        self.esc_pressed = False

        #  Camera related
        self.camera_sprites = arcade.Camera(CONSTANTS.DEFAULT_SCREEN_WIDTH, CONSTANTS.DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(CONSTANTS.DEFAULT_SCREEN_WIDTH, CONSTANTS.DEFAULT_SCREEN_HEIGHT)

    def setup(self):

        self.spawn = [6118, 3038]
        self.round_delay = 0.0
        self.score = 0
        self.mag_amount = 4
        self.round_count = 1
        self.power_up_on = False

        self.player_list = arcade.SpriteList()
        self.player_sprite = PLAYER.Player()
        self.player_sprite.center_x = self.spawn[0]
        self.player_sprite.center_y = self.spawn[1]
        self.player_list.append(self.player_sprite)

        self.background = arcade.load_texture("abandonded.png")
        """Background image. From Google images"""
        self.grid_size = CONSTANTS.SPRITE_SIZE
        self.wall_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=128)
        map_name = "Map_final_game.tmj"
        """Name of the map in Tile used for the blocks"""
        self.title_map = arcade.load_tilemap(map_name, CONSTANTS.TILE_SCALING)
        self.wall_list = self.title_map.sprite_lists["Walls_and_blocks"]

        self.power_up_sound = arcade.load_sound("power_up_sound.mp3")
        """When picking up a power up, fesliyanstudios: https://www.fesliyanstudios.com
        /sound-effects-search.php?q=Video+Game+Unlock"""
        self.power_up_number = random.randrange(0, 3)
        self.power_up_list = arcade.SpriteList()
        power_up = arcade.Sprite("fast.png", .05)
        self.power_up_list.append(power_up)

        self.zombie_list = arcade.SpriteList()
        for i in range(int(self.round_count * 1.7)):
            zombie = ZOMBIES.Zombie("character_zombie_idle.png", CONSTANTS.SPRITE_SCALING)
            """Main zombie image. Kenney: https://kenney.nl/assets/platformer-characters
            Any and all character and zombies images are from the pack of kenney platformers
            The character images are customized after kenney to add the gun texture"""
            self.zombie_list.append(zombie)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=CONSTANTS.GRAVITY)

        self.ammo_full = True
        self.bullet_list = arcade.SpriteList()
        self.ammo_list = arcade.SpriteList()

        self.food_list = arcade.SpriteList()
        for i in range(CONSTANTS.FOOD_AMOUNT):
            food = arcade.Sprite("Apple.png", .04)
            """Apple icon. From Google images"""
            food.center_x = random.randrange(1070, 4500)
            food.center_y = 2143
            if len(arcade.check_for_collision_with_list(food, self.food_list)) > 0:
                food.center_x += 64
            self.food_list.append(food)

    def on_update(self, delta_time):
        if not self.game_over and not self.pause:
            self.player_sprite.change_x = 0
            if self.a_pressed and not self.d_pressed:
                self.player_sprite.change_x = -CONSTANTS.PLAYER_SPEED
            elif self.d_pressed and not self.a_pressed:
                self.player_sprite.change_x = CONSTANTS.PLAYER_SPEED

            self.player_list.update()
            self.player_list.update_animation()
            self.ammo_list.update()
            self.bullet_list.update()
            self.food_list.update()
            self.physics_engine.update()

            self.zombie_list.update()
            self.zombie_list.update_animation()

            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.zombie_list)
                hit_list2 = arcade.check_for_collision_with_list(bullet, self.wall_list)
                if len(hit_list) > 0:
                    arcade.play_sound(self.zombie_bullet_hit_sound)
                    for zombie in hit_list:
                        zombie.hit_count -= 1
                        if zombie.hit_count <= 0:
                            ammo = arcade.Sprite("ammo_icon.png", CONSTANTS.AMMO_SCALE)
                            """Used for the ammo the player collects. From Google images"""
                            ammo.center_x = zombie.center_x
                            ammo.center_y = 2143
                            self.ammo_list.append(ammo)
                            zombie.remove_from_sprite_lists()
                            if self.round_count > 5:
                                number = random.randrange(1, 8)
                                if number == 4:
                                    self.power_up_list[0].center_x = zombie.center_x
                                    self.power_up_list[0].center_y = 2143

                        self.score += 10
                    bullet.remove_from_sprite_lists()

                elif len(hit_list2) > 0:
                    bullet.remove_from_sprite_lists()

                elif bullet.right > self.player_sprite.center_x + CONSTANTS.DEFAULT_SCREEN_WIDTH // 2 or \
                        bullet.left < self.player_sprite.center_x - CONSTANTS.DEFAULT_SCREEN_WIDTH // 2:
                    bullet.remove_from_sprite_lists()

            for ammo in self.ammo_list:
                ammo_player_hit_list = arcade.check_for_collision_with_list(ammo, self.player_list)
                if len(ammo_player_hit_list) != 0 and self.e_pressed:
                    ammo.remove_from_sprite_lists()
                    arcade.play_sound(self.ammo_pickup_sound)
                    self.mag_amount += 4
                    self.ammo_full = True

            for food in self.food_list:
                food_hit_list = arcade.check_for_collision_with_list(food, self.player_list)
                if len(food_hit_list) > 0 and self.e_pressed:
                    arcade.play_sound(self.food_pickup_sound)
                    for player in self.player_list:
                        player.hit_count_player += 1
                        if player.hit_count_player > 5:
                            player.hit_count_player = 5
                        food.remove_from_sprite_lists()
                    
            if len(self.zombie_list) == 0:
                self.round_delay += delta_time
                self.total_time = self.round_delay
                if round(self.round_delay, 1) == 8.0:
                    arcade.play_sound(self.round_change_sound)
                    self.round_delay = 0
                    self.round_count += 1
                    self.on_round_change(self.score, self.round_count, CONSTANTS.FOOD_AMOUNT,
                                         CONSTANTS.POWER_UP)

            for zombie in self.zombie_list:
                if len(arcade.check_for_collision_with_list(zombie, self.wall_list)) != 0:
                    zombie.change_x *= -1

            for i in range(len(self.zombie_list)):
                zombie_x = self.zombie_list[i].center_x
                player_x = self.player_sprite.center_x
                player_speed = self.player_sprite.change_x
                zombie_speed = self.zombie_list[i].change_x

                if player_x > zombie_x and player_speed > 0:
                    if zombie_speed < 0:
                        self.zombie_list[i].change_x = (abs(self.zombie_list[i].change_x))
                    else:
                        self.zombie_list[i].change_x = (abs(self.zombie_list[i].change_x))
                elif player_x > zombie_x and player_speed < 0:
                    if zombie_speed < 0:
                        self.zombie_list[i].change_x = (abs(self.zombie_list[i].change_x))
                    else:
                        self.zombie_list[i].change_x = (abs(self.zombie_list[i].change_x))
                elif player_x < zombie_x and player_speed < 0:
                    if zombie_speed > 0:
                        self.zombie_list[i].change_x = ((abs(self.zombie_list[i].change_x)) * -1)
                    else:
                        self.zombie_list[i].change_x = ((abs(self.zombie_list[i].change_x)) * -1)
                elif player_x < zombie_x and player_speed > 0:
                    if zombie_speed > 0:
                        self.zombie_list[i].change_x = ((abs(self.zombie_list[i].change_x)) * -1)
                    else:
                        self.zombie_list[i].change_x = ((abs(self.zombie_list[i].change_x)) * -1)

            for zombie in self.zombie_list:

                zombie_player_hit_list = arcade.check_for_collision_with_list(zombie, self.player_list)
                if len(zombie_player_hit_list) > 0:
                    arcade.play_sound(self.player_hit_sound)
                    self.player_sprite.position = self.spawn
                    CONSTANTS.PLAYER_SPEED = 4
                    CONSTANTS.JUMP_SPEED = 10.5
                    zombie.remove_from_sprite_lists()
                    for player in self.player_list:
                        player.hit_count_player -= 1
                        if player.hit_count_player == 0:
                            self.game_over = True
                            player.hit_count_player = 0

            for power_up in self.power_up_list:
                self.power_up_hit_list = arcade.check_for_collision_with_list(power_up, self.player_list)
                if len(self.power_up_hit_list) != 0 and self.e_pressed:
                    self.power_up_on = True
                    if self.score >= 300:
                        self.score -= 300
                        arcade.play_sound(self.power_up_sound)
                        power_up.remove_from_sprite_lists()
                        CONSTANTS.PLAYER_SPEED *= 2
                        CONSTANTS.JUMP_SPEED *= 1.5

            self.scroll_to_player()

    def on_draw(self):
        eighth_h = CONSTANTS.DEFAULT_SCREEN_HEIGHT / 8
        font = "Kenney Future"
        """Font used for text on the screen. It came installed"""
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, CONSTANTS.DEFAULT_SCREEN_WIDTH,
                                            CONSTANTS.DEFAULT_SCREEN_HEIGHT, self.background)
        self.game_over_text = arcade.Text(
            f"YOU DIED "
            f"\n ROUNDS PASSED:{self.round_count - 1} "
            f"\nSCORE:{self.score} "
            f"\nZOMBIES LEFT: {len(self.zombie_list)}",
            (CONSTANTS.DEFAULT_SCREEN_WIDTH / 4),
            (CONSTANTS.DEFAULT_SCREEN_HEIGHT / 2) + 100,
            arcade.color.RED,
            24,
            multiline=True,
            width=1000,
            font_name=font,
            align="center"
        )

        self.round_number_text = arcade.Text(
            f"Score: {self.score}\n"
            f"\nRound: {self.round_count}\n"
            f"\nBullet: {self.mag_amount}\n"
            f"\nPotent life apples: {self.player_sprite.hit_count_player}\n"
            f"\nZombies left: {len(self.zombie_list)}\n",
            10,
            eighth_h * 7.5,
            CONSTANTS.AMMO_COUNT_COLOR,
            18,
            multiline=True,
            font_name=font,
            align="left",
            width=1000
        )

        self.reload_text = arcade.Text(
            f"YOU NEED TO RELOAD",
            (CONSTANTS.DEFAULT_SCREEN_WIDTH / 3) +100,
            CONSTANTS.DEFAULT_SCREEN_HEIGHT / 2,
            arcade.color.RED,
            24,
            font_name=font,
            width=1000

        )

        self.camera_sprites.use()
        self.wall_list.draw()
        self.food_list.draw()
        self.ammo_list.draw()
        self.bullet_list.draw()
        self.zombie_list.draw()
        self.power_up_list.draw()
        self.player_list.draw()
        self.camera_gui.use()

        position = f"Scroll value: ({self.player_sprite.position[0]:5.1f}, " \
               f"{self.player_sprite.position[1]:5.1f})"

        arcade.draw_rectangle_filled(self.width // 2, 20, self.width, 40, arcade.color.ALMOND)

        arcade.draw_text(position, 10, 10, arcade.color.BLACK_BEAN, 20)
        if self.round_delay < 8.00 and len(self.zombie_list) == 0:
            arcade.draw_text("ROUND CHANGE", (CONSTANTS.DEFAULT_SCREEN_WIDTH // 2) - 140,
                             eighth_h * 5, arcade.color.RED, 24)
        if len(self.power_up_hit_list) != 0 and self.score < 300:
            arcade.draw_text("Score is less than 300. Can't unlock power-up",
                             (CONSTANTS.DEFAULT_SCREEN_WIDTH / 2) - 350,
                             CONSTANTS.DEFAULT_SCREEN_HEIGHT / 2,
                             arcade.color.RED, 24)
        if self.game_over:
            self.clear()
            self.background = arcade.load_texture("black.png")
            """Black screen when the game is over. From Google images"""
            self.game_over_text.draw()
        else:
            self.round_number_text.draw()

        if self.mag_amount < 1 and not self.game_over:
            self.ammo_full = False
            self.reload_text.draw()

    def on_round_change(self, score, round_count, food_amount, power_up_amount):
        self.score = score
        self.round_count = round_count

        food_amount = food_amount
        power_up_amount = power_up_amount

        for i in range(int(self.round_count ** 1.2)):
            zombie = ZOMBIES.Zombie("character_zombie_idle.png", CONSTANTS.SPRITE_SCALING)
            zombie.change_x *= 1.1
            if zombie.center_x - self.player_sprite.center_x > 0:
                zombie.center_x += 100
            else:
                zombie.center_x -= 100
            self.zombie_list.append(zombie)

        for i in range(int(food_amount * 1.2)):
            food = arcade.Sprite("Apple.png", .04)
            food.center_x = random.randrange(1070, 4500)
            food.center_y = 2143
            if len(arcade.check_for_collision_with_list(food, self.food_list)) > 0:
                food.center_x += 64
            self.food_list.append(food)

        for i in range(int(power_up_amount * self.round_count)):
            power_up = arcade.Sprite("fast.png", .05)
            self.power_up_list.append(power_up)

        if len(self.power_up_hit_list) != 0 and self.score < 300:
            arcade.draw_text("Score is less than 300. Can't unlock power-up",
                             (CONSTANTS.DEFAULT_SCREEN_WIDTH / 2) - 350,
                             CONSTANTS.DEFAULT_SCREEN_HEIGHT / 2,
                             arcade.color.RED, 24)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.a_pressed = True
            self.direction = False
            self.pause = False
        elif key == arcade.key.D:
            self.d_pressed = True
            self.direction = True
            self.pause = False
        elif key == arcade.key.SPACE:
            self.pause = False
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = CONSTANTS.JUMP_SPEED
        elif key == arcade.key.E:
            self.pause = False
            self.e_pressed = True
        elif key == arcade.key.ESCAPE:
            self.pause = False
            self.esc_pressed = True
            self.pause = True
        elif key == arcade.key.ESCAPE:
            self.pause = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False
        elif key == arcade.key.SPACE:
            self.space_bar_pressed = False
        elif key == arcade.key.E:
            self.e_pressed = False

    def scroll_to_player(self):
        camera_position = Vec2(self.player_sprite.center_x - self.width / 2,
                               self.player_sprite.center_y - self.height / 3)
        self.camera_sprites.move_to(camera_position, CONSTANTS.CAMERA_SPEED)

    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))
        CONSTANTS.DEFAULT_SCREEN_WIDTH = width
        CONSTANTS.DEFAULT_SCREEN_HEIGHT = height

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if not self.game_over and not self.pause:
            if self.ammo_full:
                arcade.play_sound(self.gun_shot)
                bullet = arcade.Sprite("Bullet.png", .04)
                """Fired bullet icon. From Googles images"""
                bullet.angle = 90
                self.mag_amount -= 1
                person_x = self.player_sprite.center_x - 8
                person_y = self.player_sprite.center_y - 12
                if self.direction:
                    bullet.center_x = person_x
                    bullet.center_y = person_y
                    bullet.change_x = CONSTANTS.BULLET_SPEED
                    bullet.angle = 270
                else:
                    bullet.center_x = person_x
                    bullet.center_y = person_y
                    bullet.change_x = -CONSTANTS.BULLET_SPEED
                self.bullet_list.append(bullet)


def main():

    window = MyGame(CONSTANTS.DEFAULT_SCREEN_WIDTH, CONSTANTS.DEFAULT_SCREEN_HEIGHT, CONSTANTS.SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
