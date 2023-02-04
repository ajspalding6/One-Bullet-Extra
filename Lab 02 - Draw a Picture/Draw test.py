import arcade
"""
Yes I'm aware this drawing is terrible haha
"""

# Set height and width of the window
WIDTH = 1200
HEIGHT = 1200

# Opens window
arcade.open_window(WIDTH, HEIGHT, "STANLEY THE DINO")

# Sets background color
arcade.set_background_color(arcade.csscolor.SKY_BLUE)

# Begins rendering
arcade.start_render()

# Begin drawing

# Grass
arcade.draw_lrtb_rectangle_filled(0, 1200, 400, 0, arcade.csscolor.DARK_GREEN)

# Sun
arcade.draw_circle_filled(1050, 1050, 50, arcade.csscolor.YELLOW)
arcade.draw_circle_outline(1050, 1050, 52, arcade.csscolor.ORANGE, 8)
arcade.draw_circle_outline(1050, 1050, 56, arcade.csscolor.RED, 4)

# Head
arcade.draw_ellipse_filled(125, 1100, 100, 60, arcade.csscolor.LIGHT_GREEN, 160)
arcade.draw_ellipse_outline(125, 1100, 100, 60, arcade.csscolor.BLACK, 1, 160)

# Eye
arcade.draw_circle_filled(130, 1110, 6, arcade.csscolor.BLACK)

# Mouth
arcade.draw_arc_outline(110, 1090, 20, 20, arcade.csscolor.BLACK, 180, 300, 5)

# Neck
arcade.draw_ellipse_filled(285, 1050, 300, 80, arcade.csscolor.LIGHT_GREEN, 200)
arcade.draw_ellipse_outline(285, 1050, 300, 80, arcade.csscolor.BLACK, 1, 200)

# Body
arcade.draw_lrtb_rectangle_filled(575, 800, 900, 780, arcade.csscolor.GREEN)
arcade.draw_lrtb_rectangle_outline(575, 800, 900, 780, arcade.csscolor.BLACK, 1)

arcade.draw_circle_filled(500, 900, 150, arcade.csscolor.LIGHT_GREEN)
arcade.draw_circle_filled(650, 1000, 150, arcade.csscolor.LIGHT_GREEN)
arcade.draw_circle_filled(800, 900, 150, arcade.csscolor.LIGHT_GREEN)

# Front upper leg
ROTATION1=310
X_START1=365
Y_START1=670
LENGTH1=350
WIDTH1=110

arcade.draw_ellipse_filled(X_START1, Y_START1, LENGTH1, WIDTH1, arcade.csscolor.GREEN, ROTATION1)
arcade.draw_ellipse_outline(X_START1, Y_START1, LENGTH1, WIDTH1, arcade.csscolor.BLACK, 1, ROTATION1)

# Front lower leg
R3=280
X3=240
Y3=415
L3=275
W3=55
arcade.draw_ellipse_filled(X3, Y3, L3, W3, arcade.csscolor.LIGHT_GREEN, R3)
arcade.draw_ellipse_outline(X3, Y3, L3, W3, arcade.csscolor.BLACK, 1, R3)

# Front foot
L1=190
R1=230
T1=290
B1=260
arcade.draw_lrtb_rectangle_filled(L1, R1, T1, B1, arcade.csscolor.GREEN)
arcade.draw_lrtb_rectangle_outline(L1, R1, T1, B1, arcade.csscolor.BLACK, 1)

# Back upper Leg
ROTATION2=225
X_START2=980
Y_START2=675
LENGTH2=400
WIDTH2=110
arcade.draw_ellipse_filled(X_START2, Y_START2, LENGTH2, WIDTH2, arcade.csscolor.GREEN, ROTATION2)
arcade.draw_ellipse_outline(X_START2, Y_START2, LENGTH2, WIDTH2, arcade.csscolor.BLACK, 1, ROTATION2)

# Back lower leg
R4=280
X4=1085
Y4=405
L4=275
W4=55
arcade.draw_ellipse_filled(X4, Y4, L4, W4, arcade.csscolor.LIGHT_GREEN, R4)
arcade.draw_ellipse_outline(X4, Y4, L4, W4, arcade.csscolor.BLACK, 1, R4)

# Back foot
L2=1020
R2=1060
T2=290
B2=260
arcade.draw_lrtb_rectangle_filled(L2, R2, T2, B2, arcade.csscolor.GREEN)
arcade.draw_lrtb_rectangle_outline(L2, R2, T2, B2, arcade.csscolor.BLACK, 1)

arcade.finish_render()

arcade.run()
