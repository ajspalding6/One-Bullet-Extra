""" Lab 7 - User Control """

import arcade

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
MOVEMENT_SPEED = 3


def draw_backboard(left, right, top, bottom, left1, right1, top1, bottom1,
                   startx, starty, endx, endy, width, startx1, starty1, endx1, endy1, width1):

    arcade.draw_lrtb_rectangle_filled(left, right, top, bottom, arcade.csscolor.WHITE)
    arcade.draw_lrtb_rectangle_outline(left, right, top, bottom, arcade.csscolor.BLACK, 1)

    # Draw the post
    arcade.draw_lrtb_rectangle_filled(left1, right1, top1, bottom1, arcade.csscolor.ROYAL_BLUE)

    # Draw the connecting poles
    arcade.draw_line(startx, starty, endx, endy, arcade.csscolor.BLACK, width)
    arcade.draw_line(startx1, starty1, endx1, endy1, arcade.csscolor.BLACK, width1)

# Rim


def draw_rim(x, y, length, height, angle):
    arcade.draw_point(x, y, arcade.csscolor.RED, 5)
    # Draws a point through passing x and y and making sure it is centered
    arcade.draw_ellipse_outline(x, y, length, height, arcade.csscolor.ORANGE, 6, angle)
    arcade.draw_ellipse_outline(x, y, length, height, arcade.csscolor.BLACK, 1, angle)

# Back of the iron
    arcade.draw_triangle_filled(115, 525, 115, 550, 135, 550, arcade.csscolor.ORANGE)
    arcade.draw_triangle_outline(115, 525, 115, 550, 135, 550, arcade.csscolor.BLACK, 1)

# Net


def draw_net(x1, x2, y1, y2):
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
        x_end = x_end-4
        x_start = x_start+2
        y_end = y_end + 20
        y_start = y_start + 20
    arcade.draw_line(145, 445, 220, 445, arcade.csscolor.WHITE, 2)


"""def ball_rotation():
    bball = arcade.load_texture("bball")
    arcade.draw_scaled_texture_rectangle(400, 400, bball, .03)"""


class Ball:
    def __init__(self, position_x, position_y, change_x, change_y, texture):

        # Take the parameters of the init function above,
        # and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.texture = arcade.load_texture("bball")

    def draw(self):
        """ Draw the balls with the instance variables we have. """


        arcade.draw_scaled_texture_rectangle(self.position_x,
                                             self.position_y,
                                             self.texture,
                                             self.scale)

    def update(self):
        # Move the ball
        self.position_y += self.change_y
        self.position_x += self.change_x


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self, width, height, title):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")

        self.set_mouse_visible(False)

        # Create our ball
        ball = arcade.load_texture("bball")
        self.ball = Ball(50, 50, ball, .3)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.csscolor.LIGHT_GRAY)
        draw_backboard(100, 115, 700, 500, 20, 50, 650, 0, 50, 625, 100, 625, 6, 50, 575, 100, 575, 6)
        draw_rim(180, 547, 100, 20, 180)
        draw_net(146, 220, 465, 445)
        self.ball.draw()

    def update(self, delta_time):
        self.ball.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.ball.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.ball.change_x = MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.ball.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.ball.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.ball.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.ball.change_y = 0


def main():
    window = MyGame(800, 800, "Hi")

    arcade.run()


main()
