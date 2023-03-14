import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
MOVEMENT_SPEED = 5


class Ball:
    def __init__(self, ball_position_x, ball_position_y, ball_change_x, ball_change_y, ball_texture, ball_scale):

        # Take the parameters of the init function above,
        # and create instance variables out of them.
        self.ball_position_x = ball_position_x
        self.ball_position_y = ball_position_y
        self.ball_change_x = ball_change_x
        self.ball_change_y = ball_change_y
        self.ball_texture = ball_texture
        self.ball_scale = ball_scale
        self.ball_sound = arcade.load_sound("ball.sideborder.wav")

    def draw(self):
        arcade.draw_scaled_texture_rectangle(self.ball_position_x,
                                             self.ball_position_y,
                                             self.ball_texture,
                                             self.ball_scale)

    def update(self):
        # Move the ball and plays sound when it hits the side of the screen
        if self.ball_position_x >= 757:
            self.ball_position_x = 756
            self.ball_change_x = 0
            arcade.play_sound(self.ball_sound)
        if self.ball_position_x <= 43:
            self.ball_position_x = 44
            self.ball_change_x = 0
            arcade.play_sound(self.ball_sound)
        if self.ball_position_y >= 757:
            self.ball_position_y = 756
            self.ball_change_y = 0
            arcade.play_sound(self.ball_sound)
        if self.ball_position_y <= 43:
            self.ball_position_y = 44
            self.ball_change_y = 0
            arcade.play_sound(self.ball_sound)
        self.ball_position_y += self.ball_change_y
        self.ball_position_x += self.ball_change_x


class Player:
    def __init__(self, player_position_x, player_position_y, player_change_x, player_change_y,
                 player_texture, player_scale):

        # Take the parameters of the init function above,
        # and create instance variables out of them.
        self.player_position_x = player_position_x
        self.player_position_y = player_position_y
        self.player_change_x = player_change_x
        self.player_change_y = player_change_y
        self.player_texture = player_texture
        self.player_scale = player_scale

    def draw2(self):
        """ Draw the player with the instance variables we have. """

        arcade.draw_scaled_texture_rectangle(self.player_position_x,
                                             self.player_position_y,
                                             self.player_texture,
                                             self.player_scale)

    def update2(self):
        # Move the player
        self.player_position_y += self.player_change_y
        self.player_position_x += self.player_change_x


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def draw_backboard(self, left_backboard, right_backboard, top_backboard, bottom_backboard, left_post, right_post,
                       top_post, bottom_post, start_x, start_y, end_x, end_y, width, start_x2, start_y2, end_x2, end_y2,
                       width2):

        # Draw the backboard and the outline
        arcade.draw_lrtb_rectangle_filled(left_backboard, right_backboard, top_backboard, bottom_backboard,
                                          arcade.csscolor.WHITE)
        arcade.draw_lrtb_rectangle_outline(left_backboard, right_backboard, top_backboard, bottom_backboard,
                                           arcade.csscolor.BLACK, 1)

        # Draw the post
        arcade.draw_lrtb_rectangle_filled(left_post, right_post, top_post, bottom_post, arcade.csscolor.ROYAL_BLUE)

        # Draw the connecting poles
        arcade.draw_line(start_x, start_y, end_x, end_y, arcade.csscolor.BLACK, width)
        arcade.draw_line(start_x2, start_y2, end_x2, end_y2, arcade.csscolor.BLACK, width2)

    # Rim

    def draw_rim(self, x, y, length, height, angle):
        arcade.draw_point(x, y, arcade.csscolor.RED, 5)
        # Draws a point through passing x and y and making sure it is centered
        arcade.draw_ellipse_outline(x, y, length, height, arcade.csscolor.ORANGE, 6, angle)
        arcade.draw_ellipse_outline(x, y, length, height, arcade.csscolor.BLACK, 1, angle)

        # Back of the iron
        arcade.draw_triangle_filled(115, 525, 115, 550, 135, 550, arcade.csscolor.ORANGE)
        arcade.draw_triangle_outline(115, 525, 115, 550, 135, 550, arcade.csscolor.BLACK, 1)

    # Net

    def draw_net(self, x1, x2, y1, y2):
        # Draws the first two lines since they can't be looped
        arcade.draw_line(130, 545, 145, 445, arcade.csscolor.WHITE, 2)
        arcade.draw_line(145, 540, 150, 445, arcade.csscolor.WHITE, 2)
        # Loops the vertical lines
        x = 145
        while x <= 205:
            arcade.draw_line(x, 535, x, 445, arcade.csscolor.WHITE, 2)
            if x == 205:
                break
            x = x + 15

        # Draws the last two lines since they can't be looped
        arcade.draw_line(217, 540, 212, 445, arcade.csscolor.WHITE, 2)
        arcade.draw_line(230, 545, 220, 445, arcade.csscolor.WHITE, 2)

        # Loops the diagonal/tilted lines
        x_end = x1
        x_start = x2
        y_end = y1
        y_start = y2
        while x_end != 130:
            arcade.draw_line(x_start, y_start, x_end, y_end, arcade.csscolor.WHITE, 2)
            if x_end == 130:
                break
            x_end = x_end - 4
            x_start = x_start + 2
            y_end = y_end + 20
            y_start = y_start + 20
        arcade.draw_line(145, 445, 220, 445, arcade.csscolor.WHITE, 2)

    def __init__(self, width, height, title):
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")

        # Lets me see the mouse
        self.set_mouse_visible(True)

        # Create the ball
        self.ball = Ball(650, 350, 0, 0, arcade.load_texture("bball"), .03)

        # Create the player
        self.player = Player(350, 350, 0, 0, arcade.load_texture("kobe"), .14)

    # Updates and moves the ball around
    def update(self, delta_time):
        self.ball.update()

    # Updates and moves the player around
    def update2(self):
        self.player.update2()

    # Beginning of user control
        # Determines what key is pressed and what to do when it's pressed
    def on_key_press(self, key, modifiers):

        if key == arcade.key.A:
            self.ball.ball_change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.ball.ball_change_x = MOVEMENT_SPEED
        elif key == arcade.key.W:
            self.ball.ball_change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.ball.ball_change_y = -MOVEMENT_SPEED

    # Determines what to do after the key is released
    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.ball.ball_change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.ball.ball_change_y = 0

    # Tracks the mouse
        # Determines what to do if a button is pressed
    def on_mouse_press(self, x, y, button, modifiers):
        right_click_sound = arcade.load_sound("Metal Click.wav")
        left_click_sound = arcade.load_sound("Toom Click.wav")
        if button == arcade.MOUSE_BUTTON_LEFT:
            print("Left mouse button pressed at", x, y)
            arcade.play_sound(right_click_sound)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            print("Right mouse button pressed at", x, y)
            arcade.play_sound(left_click_sound)
            # play sound

    # Determines what to do if a button is released
    def on_mouse_motion(self, x, y, dx, dy):
        self.player.player_position_x = x
        self.player.player_position_y = y

    # Draws/calls everything
    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.csscolor.LIGHT_GRAY)

        self.ball.draw()
        self.player.draw2()
        self.draw_backboard(100, 115, 700, 500, 20, 50, 650, 0, 50, 625, 100, 625, 6, 50, 575, 100, 575, 6)
        self.draw_rim(180, 547, 100, 20, 180)
        self.draw_net(146, 220, 465, 445)


# Opens window and runs


def main():
    MyGame(800, 800, "User Control")

    arcade.run()


main()
