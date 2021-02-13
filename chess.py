"""Interactive chess game."""

from enum import Enum

import arcade

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WIDTH_BUFFER,
    SCREEN_TITLE,
    CHARACTER_SCALING,
    Side,
    WHITE_COLOR,
    OFFWHITE_COLOR,
    BLACK_COLOR,
    OFFBLACK_COLOR,
    BoardPosition,
)
from pieces import Pawn, PIECE_ORDER


class PlayerState(Enum):
    SELECT_PIECE = 1
    MOVE_PIECE = 2


class ChessGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """Initialize the class."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Setup the piece lists
        self.white_pieces = None
        self.black_pieces = None

        # Setup the game states
        self.current_player = None
        self.player_state = None
        self.selected_piece = None
        self.possible_moves = None

        # Set the background color
        arcade.set_background_color(arcade.csscolor.WHITE)

    def setup(self):
        """Set up the game - call to restart."""

        # Set up empty sprite lists
        self.white_pieces = arcade.SpriteList()
        self.black_pieces = arcade.SpriteList()

        # Setup the game states
        self.current_player = Side.WHITE
        self.player_state = PlayerState.SELECT_PIECE
        self.selected_piece = None
        self.possible_moves = []

        init_pieces(Side.WHITE, self.white_pieces)
        init_pieces(Side.BLACK, self.black_pieces)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()

        # Draw the board and pieces to start
        self.draw_board()
        self.white_pieces.draw()
        self.black_pieces.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if self.player_state == PlayerState.SELECT_PIECE:
            piece_list = (
                self.white_pieces
                if self.current_player == Side.WHITE
                else self.black_pieces
            )
            for piece in piece_list:
                if piece.was_clicked(x, y):
                    self.selected_piece = piece
                    break

            if self.selected_piece is not None:
                self.possible_moves = self.selected_piece.get_possible_moves(
                    self.white_pieces, self.black_pieces
                )
                print([str(m) for m in self.possible_moves])

    def draw_board(self):
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
                position = BoardPosition(col, row)

                # Get color based on boolean
                if self.selected_piece is not None and (
                    self.selected_piece.board_position == position
                    or position in self.possible_moves
                ):
                    color = OFFWHITE_COLOR if color_white else OFFBLACK_COLOR
                else:
                    color = WHITE_COLOR if color_white else BLACK_COLOR

                # Draw a filled rectangle
                arcade.draw_lrtb_rectangle_filled(
                    position.left,
                    position.right,
                    position.top,
                    position.bot,
                    color,
                )
                # Switch color based on column
                color_white = not color_white
            # Switch starting color based on row
            color_white = not color_white


def init_pieces(side: Side, piece_list: arcade.SpriteList):
    """Initialize the pieces in their starting positions, depending on side."""

    # Change the order depending on the side
    order = PIECE_ORDER if side == Side.WHITE else reversed(PIECE_ORDER)
    for col, piece_cls in enumerate(order):
        # Add a major piece
        row_idx = 0 if side == Side.WHITE else 7
        piece = piece_cls(side, BoardPosition(col, row_idx), scale=CHARACTER_SCALING)
        piece_list.append(piece)

        # Add a pawn
        row_idx = 1 if side == Side.WHITE else 6
        pawn = Pawn(side, BoardPosition(col, row_idx), scale=CHARACTER_SCALING)
        piece_list.append(pawn)


def main():
    """Main method."""
    window = ChessGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
