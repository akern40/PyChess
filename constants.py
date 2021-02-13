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


# Colors
WHITE_COLOR = csscolor.GHOST_WHITE
OFFWHITE_COLOR = csscolor.CORNSILK
BLACK_COLOR = csscolor.DIM_GRAY
OFFBLACK_COLOR = csscolor.DARK_GRAY


class Side(Enum):
    WHITE = 1
    BLACK = 2

    def __str__(self):
        return self.name.lower()

    def swap(self):
        if self.value == 1:
            return Side.BLACK
        return Side.WHITE


class BoardPosition:
    """A utility class to handle board position to pixel conversions."""

    def __init__(self, col_idx: int, row_idx: int):
        """Initialize with row and column indices and calculate edges and centers."""
        self.row_idx = row_idx
        self.col_idx = col_idx

        self.left = self.col_idx * SQUARE_SIZE
        self.right = (self.col_idx + 1) * SQUARE_SIZE
        self.bot = self.row_idx * SQUARE_SIZE
        self.top = (self.row_idx + 1) * SQUARE_SIZE

        self.center_x = (self.left + self.right) / 2
        self.center_y = (self.bot + self.top) / 2

    def __str__(self):
        """Get the canonical chess representation of the position."""
        col_letter = chr(97 + self.col_idx)
        return f"{col_letter}{self.row_idx}"

    def get_center(self):
        """Get the x and y centers in pixels."""
        return self.center_x, self.center_y

    def square_contains(self, x_px: float, y_px: float):
        """Tell whether an x and y location in pixels corresponds to the square of this position."""
        in_x = self.left < x_px < self.right
        in_y = self.bot < y_px < self.top
        return in_x and in_y

    def check_valid(self, x_offset: int, y_offset: int):
        """Check whethere an x_offset and y_offset from this position is on the board."""
        x_idx = self.col_idx + x_offset
        y_idx = self.row_idx + y_offset
        return 0 <= x_idx < 8 and 0 <= y_idx < 8

    def get_offset(self, x_offset: int, y_offset: int):
        """Get a new BoardPosition instance with the given x and y offset from this instance."""
        if not self.check_valid(x_offset, y_offset):
            raise ValueError("Invalid position")
        return BoardPosition(self.col_idx + x_offset, self.row_idx + y_offset)

    def __eq__(self, other):
        if not isinstance(other, BoardPosition):
            raise NotImplementedError("Object must be a BoardPosition")
        return self.row_idx == other.row_idx and self.col_idx == other.col_idx

    def __hash__(self):
        return hash(self.row_idx, self.col_idx)
