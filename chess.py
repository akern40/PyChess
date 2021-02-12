"""Interactive chess game."""

import arcade

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WIDTH_BUFFER,
    SQUARE_SIZE,
    SCREEN_TITLE,
    CHARACTER_SCALING,
    PIECE_ORDER,
    Color,
    WHITE_COLOR,
    BLACK_COLOR,
)


class ChessGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """Initialize the class."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Setup the piece lists
        self.white_pieces = None
        self.black_pieces = None

        # Set the background color
        arcade.set_background_color(arcade.csscolor.WHITE)

    def setup(self):
        """Set up the game - call to restart."""

        # Set up empty sprite lists
        self.white_pieces = arcade.SpriteList()
        self.black_pieces = arcade.SpriteList()

        init_pieces(Color.WHITE, self.white_pieces)
        init_pieces(Color.BLACK, self.black_pieces)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()

        # Draw the board and pieces to start
        draw_board()
        self.white_pieces.draw()
        self.black_pieces.draw()


def init_pieces(color: Color, piece_list: arcade.SpriteList):
    """Initialize the pieces in their starting positions, depending on color."""

    # Change the order depending on the color
    order = PIECE_ORDER if color == Color.WHITE else reversed(PIECE_ORDER)
    for col, piece in enumerate(order):
        # Add a major piece
        location = f"sprites/{color}_{piece}.png".lower()
        piece = arcade.Sprite(location, scale=CHARACTER_SCALING)
        piece.center_x = (col + 0.5) * SQUARE_SIZE  # Set the x by column

        # The y-location depends on the color
        y_loc = 0.5 * SQUARE_SIZE
        if color == Color.BLACK:
            y_loc = SCREEN_HEIGHT - y_loc
        piece.center_y = y_loc
        piece_list.append(piece)

        # Add a pawn
        location = f"sprites/{color}_pawn.png".lower()
        pawn = arcade.Sprite(f"sprites/{color}_pawn.png", scale=CHARACTER_SCALING)
        pawn.center_x = piece.center_x  # Same x as major piece

        # Again, y-location depends on color
        y_offset = SQUARE_SIZE if color == Color.WHITE else -SQUARE_SIZE
        pawn.center_y = piece.center_y + y_offset
        piece_list.append(pawn)


def draw_board():
    """Draw the underlying board."""
    arcade.draw_lrtb_rectangle_outline(
        0,
        SCREEN_WIDTH - WIDTH_BUFFER,
        SCREEN_HEIGHT,
        0,
        arcade.csscolor.BLACK,
        border_width=10,
    )
    color_white = False
    for row in range(8):
        for col in range(8):
            # Get color based on boolean
            color = WHITE_COLOR if color_white else BLACK_COLOR
            # Draw a filled rectangle
            arcade.draw_lrtb_rectangle_filled(
                col * SQUARE_SIZE,
                (col + 1) * SQUARE_SIZE,
                (row + 1) * SQUARE_SIZE,
                row * SQUARE_SIZE,
                color,
            )
            # Switch color based on column
            color_white = not color_white
        # Switch starting color based on row
        color_white = not color_white


def main():
    """Main method."""
    window = ChessGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
