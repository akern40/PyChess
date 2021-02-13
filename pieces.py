"""Classes and functions for pieces."""

import arcade

from constants import Color, Position


class Piece(arcade.Sprite):
    """Class representing a chess piece."""

    def __init__(self, color: Color, position: Position, filename: str, **kwargs):
        center_x, center_y = position.get_center()
        super().__init__(filename, **kwargs, center_x=center_x, center_y=center_y)
        self.color = color
        self.position = position
        self.letter = ""

    def was_clicked(self, x_px: float, y_px: float):
        return self.position.square_contains(x_px, y_px)

    def __str__(self):
        return self.letter + str(self.position)


class King(Piece):
    """Class representing a king."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.letter = "K"

    def get_possible_moves(self):
        """Get possible moves for a king."""
        moves = []
        for x_offset in range(-1, 1):
            for y_offset in range(-1, 1):

                if x_offset == 0 and y_offset == 0:
                    continue

                if self.position.check_valid(x_offset, y_offset):
                    moves.append(self.position.get_offset(x_offset, y_offset))

        return moves


class Queen(Piece):
    """Class representing a queen."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.letter = "Q"

    def get_possible_moves(self):
        """Get possible moves for a queen."""
        moves = []

        for offset in range(-7, 7):
            if offset == 0:
                continue

            # Horizontal/vertical first
            if self.position.check_valid(offset, 0):
                moves.append(self.position.get_offset(offset, 0))
            if self.position.check_valid(0, offset):
                moves.append(self.position.get_offset(0, offset))

            # Now diagonals
            if self.position.check_valid(offset, offset):
                moves.append(self.position.get_offset(offset, offset))
            if self.position.check_valid(offset, -offset):
                moves.append(self.position.get_offset(offset, -offset))
            if self.position.check_valid(-offset, offset):
                moves.append(self.position.get_offset(-offset, offset))
            if self.position.check_valid(-offset, -offset):
                moves.append(self.position.get_offset(-offset, -offset))

        return moves


class Bishop(Piece):
    """Class representing a bishop."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.letter = "B"

    def get_possible_moves(self):
        """Get possible moves for a bishop."""
        moves = []

        # Diagonals
        for offset in range(-7, 7):
            if offset == 0:
                continue
            if self.position.check_valid(offset, offset):
                moves.append(self.position.get_offset(offset, offset))
            if self.position.check_valid(offset, -offset):
                moves.append(self.position.get_offset(offset, -offset))
            if self.position.check_valid(-offset, offset):
                moves.append(self.position.get_offset(-offset, offset))
            if self.position.check_valid(-offset, -offset):
                moves.append(self.position.get_offset(-offset, -offset))

        return moves


class Rook(Piece):
    """Class representing a rook."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.letter = "R"

    def get_possible_moves(self):
        """Get possible moves for a rook."""
        moves = []

        # Diagonals
        for offset in range(-7, 7):
            if offset == 0:
                continue
            # Horizontal/vertical
            if self.position.check_valid(offset, 0):
                moves.append(self.position.get_offset(offset, 0))
            if self.position.check_valid(0, offset):
                moves.append(self.position.get_offset(0, offset))

        return moves


class Knight(Piece):
    """Class representing a knight."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.letter = "N"

    def get_possible_moves(self):
        """Get possible moves for a knight."""
        moves = []

        if self.position.check_valid(2, 1):
            moves.append(self.position.get_offset(2, 1))
        if self.position.check_valid(2, -1):
            moves.append(self.position.get_offset(2, -1))
        if self.position.check_valid(-2, 1):
            moves.append(self.position.get_offset(2, -1))
        if self.position.check_valid(-2, -1):
            moves.append(self.position.get_offset(2, -1))
        if self.position.check_valid(1, 2):
            moves.append(self.position.get_offset(2, -1))
        if self.position.check_valid(-1, 2):
            moves.append(self.position.get_offset(2, -1))
        if self.position.check_valid(1, -2):
            moves.append(self.position.get_offset(2, -1))
        if self.position.check_valid(-1, -2):
            moves.append(self.position.get_offset(2, -1))

        return moves


class Pawn(Piece):
    """Class representing a pawn."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.letter = ""

    def get_possible_moves(self):
        """Get possible moves for a pawn."""
        moves = []

        multiplier = 1 if Color.WHITE else -1
        if self.position.y_idx == multiplier * 1:
            moves.append(self.position.get_offset(0, multiplier * 1))
            moves.append(self.position.get_offset(0, multiplier * 2))
        else:
            moves.append(self.position.get_offset(0, multiplier * 1))

        return moves
