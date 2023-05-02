import arcade
import os
import CONSTANTS


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(CONSTANTS.DEFAULT_SCREEN_WIDTH, CONSTANTS.DEFAULT_SCREEN_HEIGHT, CONSTANTS.SCREEN_TITLE)
        self.title_map = None
        self.scene = None

        self.player_sprite = None

        self.physics_engine = None

        self.camera = None

        self.gui_camera = None

        self.score = 0

        self.wall_list = None
        self.player_list = None
        self.zombie_list = None

    def setup(self):

        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        map_name = "Map_final_game.tmj"

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        self.title_map = arcade.load_tilemap(map_name, CONSTANTS.TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.score = 0

        self.player_sprite = arcade.Sprite("character_maleAdventurer_idle.png", CONSTANTS.PLAYER_SCALE)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 64
        self.scene.add_sprite("Player", self.player_sprite)

        if self.title_map.background_color:
            arcade.set_background_color(self.title_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, CONSTANTS.GRAVITY,
                                                             walls=self.scene["Platforms"])

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()

        score_text = f"Score: (self.score)"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)



    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.S:
            self.s_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True
        elif key == arcade.key.ESCAPE:
            self.esc_pressed = True
        elif key == arcade.key.E:
            self.e_pressed = True
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
        elif key == arcade.key.ESCAPE:
            self.esc_pressed = False
        elif key == arcade.key.E:
            self.e_pressed = False
        elif key == arcade.key.SPACE:
            self.space_bar_pressed = False

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        self.physics_engine.update()

        self.center_camera_to_player()


def main():
    window = MyGame(CONSTANTS.DEFAULT_SCREEN_WIDTH, CONSTANTS.DEFAULT_SCREEN_HEIGHT, CONSTANTS.SCREEN_TITLE)
    window.setup
    arcade.run()


if __name__ == "__main__":
    main()

