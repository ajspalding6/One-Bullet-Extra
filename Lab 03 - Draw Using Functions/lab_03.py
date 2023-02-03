import arcade
import random

WIDTH = 800
HEIGHT = 800

# Backboard


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

# Rotation and red dots

def on_draw(delta_time):
    arcade.start_render()
    # Draws the red dots signaling where I want the basketball to go
    i = 1
    x = 800
    y = 700

    while i < 75:
        i = i + 1
        x = x - 8
        y = y - 2
        arcade.draw_point(x, y, arcade.csscolor.RED, 3)

    if i == 75:
        while i < 150:
            i = i + 1
            x = x - 2
            y = y - 8
            arcade.draw_point(x, y, arcade.csscolor.RED, 3)

    # Rotates/moves the basketball
    on_draw.x += on_draw.x_increment
    on_draw.y += on_draw.y_increment
    if on_draw.x > WIDTH or on_draw.x < 0:
        # on_draw.x = on_draw.x-2
        # on_draw.y = on_draw.y-8
        on_draw.x_increment = -on_draw.x_increment
        on_draw.rotation_increment = random.randint(-10, 10)
        # arcade.draw_scaled_texture_rectangle(on_draw.x, on_draw.y, on_draw.ball_texture, .03, on_draw.rotation)
    if on_draw.y > HEIGHT or on_draw.y < 0:
        # on_draw.x = on_draw.x - 2
        # on_draw.y = on_draw.y - 8
        on_draw.y_increment = -on_draw.y_increment
        on_draw.rotation_increment = random.randint(-10, 10)
    on_draw.rotation += on_draw.rotation_increment
    # arcade.draw_scaled_texture_rectangle(on_draw.x, on_draw.y, on_draw.ball_texture, .03, on_draw.rotation)
    if on_draw.rotation == 360:
        on_draw.rotation = 0

    arcade.draw_scaled_texture_rectangle(on_draw.x, on_draw.y, on_draw.ball_texture, .03, on_draw.rotation)
    # Calls each function and passes the parameters set before
    draw_backboard(100, 115, 700, 500, 20, 50, 650, 0, 50, 625, 100, 625, 6, 50, 575, 100, 575, 6)
    draw_rim(180, 547, 100, 20, 180)
    draw_net(146, 220, 465, 445)

# Declares all the variables for the function
on_draw.ball_texture = arcade.load_texture("bball")
on_draw.x = random.randint(0, 800)
on_draw.y = random.randint(0, 800)
on_draw.x_increment = random.randint(-5, 5)
on_draw.y_increment = random.randint(-8, 8)
on_draw.rotation_increment = random.randint(5, 10)
on_draw.rotation = 0

# Declares the image/texture for the basketball
bball = arcade.load_texture("bball")


def main():
    arcade.open_window(WIDTH, HEIGHT, "Basketball Animation:")

    arcade.set_background_color(arcade.csscolor.LIGHT_GRAY)
    # Draws everything since each function is nested in the on_draw function and calls it 1 time 100th of a second
    arcade.schedule(on_draw, 1 / 100)
    arcade.run()


main()
