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
from player import Player


class PlayerState(Enum):
    SELECT_PIECE = 1
    MOVE_PIECE = 2


class ChessGame(arcade.View):
    """Main application class."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()

        # Setup the game states
        self.white_player = None
        self.black_player = None
        self.white_turn = None

        # Sounds!
        self.move_sound = arcade.load_sound(":resources:sounds/rockHit2.wav")
        self.take_sound = arcade.load_sound(":resources:sounds/jump2.wav")

        # Set the background color
        arcade.set_background_color(arcade.csscolor.WHITE)

    def setup(self):
        """Set up the game - call to restart."""

        self.white_player = Player(Side.WHITE, self)
        self.black_player = Player(Side.BLACK, self)
        self.white_turn = True

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()

        # Draw the board and pieces to start
        self.draw_board()
        self.white_player.pieces.draw()
        self.black_player.pieces.draw()

    def on_mouse_press(self, x: float, y: float, button: int, _modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        current_player = self.white_player if self.white_turn else self.black_player
        opponent = self.black_player if self.white_turn else self.white_player

        position = BoardPosition.get_from_pixels(x, y)
        if position.check_valid(0, 0):
            change_turn = current_player.update(position, opponent)
            if change_turn:
                self.white_turn = not self.white_turn

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

        current_player = self.white_player if self.white_turn else self.black_player

        color_white = False
        for row in range(8):
            for col in range(8):
                position = BoardPosition(col, row)

                # Get color based on boolean
                if current_player.selected_piece is not None and (
                    current_player.selected_piece.board_position == position
                    or position
                    in current_player.selected_piece.get_possible_moves(
                        self.white_player.pieces, self.black_player.pieces
                    )
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

    def end_game(self, winner: Player):
        end_view = EndView(winner)
        self.window.show_view(end_view)


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
    def __init__(self, winner: Player, **kwargs):
        """Create the view."""
        super().__init__(**kwargs)
        self.winner = winner

    def on_show(self):
        """Run once when we switch to this view."""
        color = (
            arcade.csscolor.WHITE
            if self.winner.side == Side.WHITE
            else arcade.csscolor.BLACK
        )
        arcade.set_background_color(color)

    def on_draw(self):
        """Draw this view."""
        arcade.start_render()
        color = (
            arcade.csscolor.BLACK
            if self.winner.side == Side.WHITE
            else arcade.csscolor.WHITE
        )
        arcade.draw_text(
            f"{self.winner.side} wins!".capitalize(),
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
