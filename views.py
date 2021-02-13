"""Views for the chess game."""

import arcade
from enum import Enum

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WIDTH_BUFFER,
    CHARACTER_SCALING,
    Side,
    WHITE_COLOR,
    OFFWHITE_COLOR,
    BLACK_COLOR,
    OFFBLACK_COLOR,
    BoardPosition,
)
from pieces import Pawn, PIECE_ORDER, King


class PlayerState(Enum):
    SELECT_PIECE = 1
    MOVE_PIECE = 2


class ChessGame(arcade.View):
    """Main application class."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()

        # Setup the piece lists
        self.white_pieces = None
        self.black_pieces = None

        # Setup the game states
        self.current_player = None
        self.player_state = None
        self.selected_square = None
        self.selected_piece = None
        self.possible_moves = None

        # Sounds!
        self.move_sound = arcade.load_sound(":resources:sounds/rockHit2.wav")
        self.take_sound = arcade.load_sound(":resources:sounds/jump2.wav")

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

    def on_mouse_press(self, x: float, y: float, button: int, _modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        position = BoardPosition.get_from_pixels(x, y)
        if position.check_valid(0, 0):
            self.selected_square = position

    def update(self, _delta_time):
        if self.selected_square is None:  # Only update if we've selected a square
            return

        if self.player_state == PlayerState.SELECT_PIECE:
            # Find if a piece was selected
            piece_list = (
                self.white_pieces
                if self.current_player == Side.WHITE
                else self.black_pieces
            )
            for piece in piece_list:
                if piece.board_position == self.selected_square:
                    self.selected_piece = piece
                    break

            # Get that piece's possible moves, and change the game state
            if self.selected_piece is not None:
                self.possible_moves = self.selected_piece.get_possible_moves(
                    self.white_pieces, self.black_pieces
                )
                self.player_state = PlayerState.MOVE_PIECE
        else:
            # Get the move corresponding to the selected square
            move = next(
                (m for m in self.possible_moves if m == self.selected_square), None
            )
            if move is not None:
                # Find captured pieces
                enemy_pieces = (
                    self.black_pieces
                    if self.current_player == Side.WHITE
                    else self.white_pieces
                )
                captured_piece = next(
                    (p for p in enemy_pieces if p.board_position == move), None
                )
                if captured_piece is not None:
                    enemy_pieces.remove(captured_piece)
                    arcade.play_sound(self.take_sound)

                    if isinstance(captured_piece, King):
                        end_view = EndView(self.current_player)
                        self.window.show_view(end_view)
                else:
                    arcade.play_sound(self.move_sound)
                self.selected_piece.set_board_position(move)

                # Swap player
                self.current_player = self.current_player.swap()

            # Reset relevant items
            self.selected_piece = None
            self.possible_moves = []
            self.player_state = PlayerState.SELECT_PIECE

        # Reset selected square
        self.selected_square = None

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


class WelcomeView(arcade.View):
    def on_show(self):
        """Run once when we switch to this view."""
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        """Draw this view."""
        arcade.start_render()
        arcade.draw_text(
            "Welcome to PyChess!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "Click to Play",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 75,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = ChessGame()
        game_view.setup()
        self.window.show_view(game_view)


class EndView(arcade.View):
    def __init__(self, winner: Side, **kwargs):
        """Create the view."""
        super().__init__(**kwargs)
        self.winner = winner

    def on_show(self):
        """Run once when we switch to this view."""
        color = (
            arcade.csscolor.WHITE
            if self.winner == Side.WHITE
            else arcade.csscolor.BLACK
        )
        arcade.set_background_color(color)

    def on_draw(self):
        """Draw this view."""
        arcade.start_render()
        color = (
            arcade.csscolor.BLACK
            if self.winner == Side.WHITE
            else arcade.csscolor.WHITE
        )
        arcade.draw_text(
            f"{self.winner} wins!".capitalize(),
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            color,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "Click to Restart",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 75,
            color,
            font_size=20,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        view = WelcomeView()
        self.window.show_view(view)
