"""Interactive chess game."""

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
WIDTH_BUFFER = SCREEN_WIDTH - SCREEN_HEIGHT  # We're adding a buffer for later
SQUARE_SIZE = SCREEN_HEIGHT / 8

SCREEN_TITLE = "Chess"

# The pieces are natively 240px, we need to scale them down
CHARACTER_SCALING = SQUARE_SIZE / 240

# This is white's order of pieces, at the start of the game
PIECE_ORDER = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]


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

        init_pieces("white", self.white_pieces)
        init_pieces("black", self.black_pieces)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()

        # Draw the board and pieces to start
        draw_board()
        self.white_pieces.draw()
        self.black_pieces.draw()


def init_pieces(color, piece_list):
    if color not in ["white", "black"]:
        raise ValueError(f"Color must be 'white' or 'black', got '{color}")

    order = PIECE_ORDER if color == "white" else reversed(PIECE_ORDER)
    for col, piece in enumerate(order):
        # Add a major piece
        location = f"sprites/{color}_{piece}.png"
        piece = arcade.Sprite(location, scale=CHARACTER_SCALING)

        piece.center_x = (col + 0.5) * SQUARE_SIZE  # Set the x by column
        y_loc = 0.5 * SQUARE_SIZE
        if color == "black":
            y_loc = SCREEN_HEIGHT - y_loc
        piece.center_y = y_loc
        piece_list.append(piece)

        # Add a pawn
        pawn = arcade.Sprite(f"sprites/{color}_pawn.png", scale=CHARACTER_SCALING)
        pawn.center_x = piece.center_x  # Same x as major piece
        y_offset = SQUARE_SIZE if color == "white" else -SQUARE_SIZE
        pawn.center_y = piece.center_y + y_offset
        piece_list.append(pawn)


def draw_board():
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
