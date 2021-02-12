"""Interactive chess game."""

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
WIDTH_BUFFER = SCREEN_WIDTH - SCREEN_HEIGHT
SCREEN_TITLE = "Chess"


class ChessGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """Initialize the class."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.WHITE)

    def setup(self):
        """Set up the game - call to restart."""
        pass

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        draw_board()


def draw_board():
    arcade.draw_lrtb_rectangle_outline(
        0,
        SCREEN_WIDTH - WIDTH_BUFFER,
        SCREEN_HEIGHT,
        0,
        arcade.csscolor.BLACK,
        border_width=10,
    )
    SQUARE_SIZE = SCREEN_HEIGHT / 8
    color_white = False
    for row in range(8):
        for col in range(8):
            color = (
                arcade.csscolor.IVORY
                if color_white
                else arcade.csscolor.DARK_SLATE_GRAY
            )
            arcade.draw_lrtb_rectangle_filled(
                col * SQUARE_SIZE,
                (col + 1) * SQUARE_SIZE,
                (row + 1) * SQUARE_SIZE,
                row * SQUARE_SIZE,
                color,
            )
            color_white = not color_white
        color_white = not color_white


def main():
    """Main method."""
    window = ChessGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
