"""Interactive chess game."""

import arcade

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WIDTH_BUFFER,
    SQUARE_SIZE,
    SCREEN_TITLE,
    CHARACTER_SCALING,
    Side,
    WHITE_COLOR,
    BLACK_COLOR,
    BoardPosition,
)
from pieces import Pawn, PIECE_ORDER


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

        init_pieces(Side.WHITE, self.white_pieces)
        init_pieces(Side.BLACK, self.black_pieces)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()

        # Draw the board and pieces to start
        draw_board()
        self.white_pieces.draw()
        self.black_pieces.draw()


def init_pieces(side: Side, piece_list: arcade.SpriteList):
    """Initialize the pieces in their starting positions, depending on side."""

    # Change the order depending on the side
    order = PIECE_ORDER if side == Side.WHITE else reversed(PIECE_ORDER)
    for col, piece_cls in enumerate(order):
        # Add a major piece
        y_idx = 0 if side == Side.WHITE else 7
        piece = piece_cls(side, BoardPosition(col, y_idx), scale=CHARACTER_SCALING)
        piece_list.append(piece)

        # Add a pawn
        y_idx = 1 if side == Side.WHITE else 6
        pawn = Pawn(side, BoardPosition(col, y_idx), scale=CHARACTER_SCALING)
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
