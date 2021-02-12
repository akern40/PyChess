"""Constants for the chess game."""
from enum import Enum

from arcade import csscolor


class Color(Enum):
    WHITE = 1
    BLACK = 2

    def __str__(self):
        return self.name.lower()


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
