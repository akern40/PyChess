"""Interactive chess game."""

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
WIDTH_BUFFER = SCREEN_WIDTH - SCREEN_HEIGHT
SQUARE_SIZE = SCREEN_HEIGHT / 8

SCREEN_TITLE = "Chess"

CHARACTER_SCALING = SQUARE_SIZE / 240

PIECE_ORDER = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]


class ChessGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """Initialize the class."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.white_pieces = None
        self.black_pieces = None

        arcade.set_background_color(arcade.csscolor.WHITE)

    def setup(self):
        """Set up the game - call to restart."""
        self.white_pieces = arcade.SpriteList()
        self.black_pieces = arcade.SpriteList()
        for col, piece in enumerate(PIECE_ORDER):
            location = f"sprites/white_{piece}.png"
            piece = arcade.Sprite(location, scale=CHARACTER_SCALING)
            piece.center_x = (col + 0.5) * SQUARE_SIZE
            piece.center_y = 0.5 * SQUARE_SIZE
            self.white_pieces.append(piece)

            pawn = arcade.Sprite("sprites/white_pawn.png", scale=CHARACTER_SCALING)
            pawn.center_x = piece.center_x
            pawn.center_y = piece.center_y + SQUARE_SIZE
            self.white_pieces.append(pawn)

        for col, piece in enumerate(reversed(PIECE_ORDER)):
            location = f"sprites/black_{piece}.png"
            piece = arcade.Sprite(location, scale=CHARACTER_SCALING)
            piece.center_x = (col + 0.5) * SQUARE_SIZE
            piece.center_y = SCREEN_HEIGHT - 0.5 * SQUARE_SIZE
            self.black_pieces.append(piece)

            pawn = arcade.Sprite("sprites/black_pawn.png", scale=CHARACTER_SCALING)
            pawn.center_x = piece.center_x
            pawn.center_y = piece.center_y - SQUARE_SIZE
            self.black_pieces.append(pawn)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        draw_board()
        self.white_pieces.draw()
        self.black_pieces.draw()


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
