"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.
"""
import arcade

# Set how many rows and columns we will have
ROW_COUNT = 10
COLUMN_COUNT = 10

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN


class MyGame(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.grid = []
        self.cell_count = 0
        self.ir = 0
        self.ic = 0
        self.row_counter = []
        self.column_counter = []

        for row in range(ROW_COUNT):
            self.grid.append([])
            self.row_counter.append([])
            self.column_counter.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)
                self.row_counter[row].append(0)
                self.column_counter[row].append(0)

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the grid
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Figure out what color to draw the box
                if self.grid[row][column] == 1:
                    color = arcade.color.GREEN
                else:
                    color = arcade.color.WHITE

                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                # Draw the box
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def on_mouse_press(self, x, y, button, modifiers):
        self.ir = 0
        column = x // (WIDTH + MARGIN)
        row = y // (HEIGHT + MARGIN)
        on_grid = False
        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")
        if row < ROW_COUNT and column < COLUMN_COUNT:
            on_grid = True
            if self.grid[row][column] == 0:
                self.grid[row][column] = 1
                self.cell_count += 1

            else:
                self.grid[row][column] = 0
                self.cell_count -= 1
        print(f"\nTotal of {self.cell_count} cells are selected.")

        while on_grid:
            for row in range(ROW_COUNT):
                ir = 0
                continuous_count = 0
                for column in range(COLUMN_COUNT):
                    if self.grid[row][column] == 1:
                        ir += 1
                        self.row_counter[row][column] = ir
                        continuous_count += 1

                    else:
                        self.row_counter[row][column] = ir
                        if continuous_count > 2:
                            print(f"There are {continuous_count} continuous blocks selected in row {row}")

                        continuous_count = 0

                print(f"Row {row} has {self.row_counter[row][column]} cells selected")
                if continuous_count > 2:
                    print(f"There are {continuous_count} continuous blocks selected in row {row}")
                    continuous_count = 0

            for column in range(ROW_COUNT):
                ic = 0
                for row in range(COLUMN_COUNT):
                    if self.grid[row][column] == 1:
                        ic += 1
                        self.column_counter[row][column] = ic

                    else:
                        self.column_counter[row][column] = ic
                print(f"Column {column} has {self.column_counter[row][column]} cells selected")

            on_grid = False



def main():

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()