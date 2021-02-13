"""Classes and functions for pieces."""
from typing import List

import arcade

from constants import Side, BoardPosition


def get_horiz_vert(
    position: BoardPosition,
    ally_positions: List[BoardPosition],
    enemy_positions: List[BoardPosition],
):
    """Get possible horizontal and vertical positions given a position and the enemies and allies."""
    moves = []
    right_ok = True
    left_ok = True
    down_ok = True
    up_ok = True

    for offset in range(8):
        if offset == 0:
            continue

        # Right
        if right_ok and position.check_valid(offset, 0):
            m = position.get_offset(offset, 0)
            if m in ally_positions:
                right_ok = False
            elif m in enemy_positions:
                right_ok = False
                moves.append(m)
            else:
                moves.append(m)

        # Left
        if left_ok and position.check_valid(-offset, 0):
            m = position.get_offset(-offset, 0)
            if m in ally_positions:
                left_ok = False
            elif m in enemy_positions:
                left_ok = False
                moves.append(m)
            else:
                moves.append(m)

        # Up
        if up_ok and position.check_valid(0, offset):
            m = position.get_offset(0, offset)
            if m in ally_positions:
                up_ok = False
            elif m in enemy_positions:
                up_ok = False
                moves.append(m)
            else:
                moves.append(m)

        # Down
        if down_ok and position.check_valid(0, -offset):
            m = position.get_offset(0, -offset)
            if m in ally_positions:
                down_ok = False
            elif m in enemy_positions:
                down_ok = False
                moves.append(m)
            else:
                moves.append(m)

        return moves


def get_diag(
    position: BoardPosition,
    ally_positions: List[BoardPosition],
    enemy_positions: List[BoardPosition],
):
    """Get possible diagonal positions given a position and the enemies and allies."""
    moves = []
    ul_ok = True
    ur_ok = True
    dl_ok = True
    dr_ok = True

    for offset in range(8):
        if offset == 0:
            continue

        # Up and right
        if ur_ok and position.check_valid(offset, offset):
            m = position.get_offset(offset, offset)
            if m in ally_positions:
                ur_ok = False
            elif m in enemy_positions:
                ur_ok = False
                moves.append(m)
            else:
                moves.append(m)

        # Up and left
        if ul_ok and position.check_valid(-offset, offset):
            m = position.get_offset(-offset, offset)
            if m in ally_positions:
                ul_ok = False
            elif m in enemy_positions:
                ul_ok = False
                moves.append(m)
            else:
                moves.append(m)

        # Down and right
        if dr_ok and position.check_valid(offset, -offset):
            m = position.get_offset(offset, -offset)
            if m in ally_positions:
                dr_ok = False
            elif m in enemy_positions:
                dr_ok = False
                moves.append(m)
            else:
                moves.append(m)

        # Down
        if dl_ok and position.check_valid(-offset, -offset):
            m = position.get_offset(-offset, -offset)
            if m in ally_positions:
                dl_ok = False
            elif m in enemy_positions:
                dl_ok = False
                moves.append(m)
            else:
                moves.append(m)

        return moves


class Piece(arcade.Sprite):
    """Class representing a chess piece."""

    def __init__(
        self, side: Side, board_position: BoardPosition, filename: str, **kwargs
    ):
        center_x, center_y = board_position.get_center()
        kwargs.pop("center_x", None)
        kwargs.pop("center_y", None)
        super().__init__(filename, center_x=center_x, center_y=center_y, **kwargs)
        self.side = side
        self.board_position = board_position
        self.letter = ""

    def was_clicked(self, x_px: float, y_px: float):
        return self.board_position.square_contains(x_px, y_px)

    def __str__(self):
        return self.letter + str(self.board_position)

    def get_possible_moves(self, all_pieces, en_passant=False):
        pass


class King(Piece):
    """Class representing a king."""

    def __init__(self, side: Side, board_position: BoardPosition, **kwargs):
        filename = f"sprites/{side}_king.png"
        super().__init__(side, board_position, filename, **kwargs)
        self.letter = "K"

    def get_possible_moves(self, white_pieces, black_pieces, en_passant=False):
        """Get possible moves for a king."""
        ally_positions = [
            p.board_position
            for p in (white_pieces if self.side == Side.WHITE else black_pieces)
        ]

        moves = []
        for x_offset in range(-1, 1):
            for y_offset in range(-1, 1):
                if x_offset == 0 and y_offset == 0:
                    continue

                if self.board_position.check_valid(x_offset, y_offset):
                    position = self.board_position.get_offset(x_offset, y_offset)
                    if position not in ally_positions:
                        moves.append(self.board_position.get_offset(x_offset, y_offset))

        return moves


class Queen(Piece):
    """Class representing a queen."""

    def __init__(self, side: Side, board_position: BoardPosition, **kwargs):
        filename = f"sprites/{side}_queen.png"
        super().__init__(side, board_position, filename, **kwargs)
        self.letter = "Q"

    def get_possible_moves(self, white_pieces, black_pieces, en_passant=False):
        """Get possible moves for a queen."""
        ally_positions = [
            p.board_position
            for p in (white_pieces if self.side == Side.WHITE else black_pieces)
        ]
        enemy_positions = [
            p.board_position
            for p in (black_pieces if self.side == Side.WHITE else white_pieces)
        ]

        horiz_vert_moves = get_horiz_vert(
            self.board_position, ally_positions, enemy_positions
        )
        diag_moves = get_diag(self.board_position, ally_positions, enemy_positions)
        return horiz_vert_moves + diag_moves


class Bishop(Piece):
    """Class representing a bishop."""

    def __init__(self, side: Side, board_position: BoardPosition, **kwargs):
        filename = f"sprites/{side}_bishop.png"
        super().__init__(side, board_position, filename, **kwargs)
        self.letter = "B"

    def get_possible_moves(self, white_pieces, black_pieces, en_passant=False):
        """Get possible moves for a bishop."""
        ally_positions = [
            p.board_position
            for p in (white_pieces if self.side == Side.WHITE else black_pieces)
        ]
        enemy_positions = [
            p.board_position
            for p in (black_pieces if self.side == Side.WHITE else white_pieces)
        ]

        return get_diag(self.board_position, ally_positions, enemy_positions)


class Rook(Piece):
    """Class representing a rook."""

    def __init__(self, side: Side, board_position: BoardPosition, **kwargs):
        filename = f"sprites/{side}_rook.png"
        super().__init__(side, board_position, filename, **kwargs)
        self.letter = "R"

    def get_possible_moves(self, white_pieces, black_pieces, en_passant=False):
        """Get possible moves for a rook."""
        ally_positions = [
            p.board_position
            for p in (white_pieces if self.side == Side.WHITE else black_pieces)
        ]
        enemy_positions = [
            p.board_position
            for p in (black_pieces if self.side == Side.WHITE else white_pieces)
        ]

        return get_horiz_vert(self.board_position, ally_positions, enemy_positions)


class Knight(Piece):
    """Class representing a knight."""

    def __init__(self, side: Side, board_position: BoardPosition, **kwargs):
        filename = f"sprites/{side}_knight.png"
        super().__init__(side, board_position, filename, **kwargs)
        self.letter = "N"

    def get_possible_moves(self, white_pieces, black_pieces, en_passant=False):
        """Get possible moves for a knight."""
        ally_positions = [
            p.board_position
            for p in (white_pieces if self.side == Side.WHITE else black_pieces)
        ]

        moves = []
        for position in ((2, 1), (2, -1), (-2, 1), (-2, -1)):
            if self.board_position.check_valid(*position):
                m = self.board_position.get_offset(*position)
                if m not in ally_positions:
                    moves.append(m)

            if self.board_position.check_valid(*reversed(position)):
                m = self.board_position.get_offset(*reversed(position))
                if m not in ally_positions:
                    moves.append(m)

        return moves


class Pawn(Piece):
    """Class representing a pawn."""

    def __init__(self, side: Side, board_position: BoardPosition, **kwargs):
        filename = f"sprites/{side}_pawn.png"
        super().__init__(side, board_position, filename, **kwargs)
        self.letter = ""

    def get_possible_moves(self, white_pieces, black_pieces, en_passant=False):
        """Get possible moves for a pawn."""
        ally_positions = [
            p.board_position
            for p in (white_pieces if self.side == Side.WHITE else black_pieces)
        ]

        moves = []

        multiplier = 1 if self.side == Side.WHITE else -1
        row_idx = 1 if self.side == Side.WHITE else 7
        if self.board_position.row_idx == row_idx:
            if self.board_position.check_valid(0, multiplier * 2):
                m = self.board_position.get_offset(0, multiplier * 2)
                if m not in ally_positions:
                    moves.append(m)

        if self.board_position.check_valid(0, multiplier * 1):
            m = self.board_position.get_offset(0, multiplier * 1)
            if m not in ally_positions:
                moves.append(m)

        return moves


# This is white's order of pieces, at the start of the game
PIECE_ORDER = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
