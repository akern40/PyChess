"""Constants for the chess game."""
from enum import Enum

from arcade import csscolor


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
WIDTH_BUFFER = SCREEN_WIDTH - SCREEN_HEIGHT  # We're adding a buffer for later
SQUARE_SIZE = SCREEN_HEIGHT / 8

SCREEN_TITLE = "Chess"

# The pieces are natively 240px, we need to scale them down
CHARACTER_SCALING = SQUARE_SIZE / 240

# This is white's order of pieces, at the start of the game
PIECE_ORDER = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

# Colors
WHITE_COLOR = csscolor.GHOST_WHITE
BLACK_COLOR = csscolor.DIM_GRAY


class Color(Enum):
    WHITE = 1
    BLACK = 2

    def __str__(self):
        return self.name.lower()


class Position:
    def __init__(self, row_idx: int, col_idx: int):
        self.row_idx = row_idx
        self.col_idx = col_idx

        self.left = self.col_idx * SQUARE_SIZE
        self.right = (self.col_idx + 1) * SQUARE_SIZE
        self.bot = self.row_idx * SQUARE_SIZE
        self.top = (self.row_idx + 1) * SQUARE_SIZE

        self.center_x = (self.left + self.right) / 2
        self.center_y = (self.bot + self.top) / 2

    def __str__(self):
        col_letter = chr(97 + self.col_idx)
        return f"{col_letter}{self.row_idx}"

    def get_center(self):
        return self.center_x, self.center_y

    def square_contains(self, x_px: float, y_px: float):
        in_x = self.left < x_px < self.right
        in_y = self.bot < y_px < self.top
        return in_x and in_y
