"""A player class for PyChess."""
from __future__ import annotations

import arcade

from constants import Side, BoardPosition, CHARACTER_SCALING
from pieces import PIECE_ORDER, Pawn, King


class Player:
    def __init__(self, side: Side, game):
        self.side = side
        self.game = game

        self.pieces = arcade.SpriteList()

        self.selected_piece = None
        self.possible_moves = []

        self.init_pieces()

    def init_pieces(self):
        order = PIECE_ORDER if self.side == Side.WHITE else reversed(PIECE_ORDER)
        for col, piece_cls in enumerate(order):
            row_idx = 0 if self.side == Side.WHITE else 7
            piece = piece_cls(
                self.side, BoardPosition(col, row_idx), scale=CHARACTER_SCALING
            )
            self.pieces.append(piece)

            # Add a pawn
            row_idx = 1 if self.side == Side.WHITE else 6
            pawn = Pawn(self.side, BoardPosition(col, row_idx), scale=CHARACTER_SCALING)
            self.pieces.append(pawn)

    def update(self, selected_square: BoardPosition, opponent: Player):
        finished_move = False
        if self.selected_piece is None:
            # Find if a piece was selected
            for piece in self.pieces:
                if piece.board_position == selected_square:
                    self.selected_piece = piece
                    break

            # Get that piece's possible moves, and changee the state
            if self.selected_piece is not None:
                white_pieces = (
                    self.pieces if self.side == Side.WHITE else opponent.pieces
                )
                black_pieces = (
                    self.pieces if self.side == Side.BLACK else opponent.pieces
                )
                self.possible_moves = self.selected_piece.get_possible_moves(
                    white_pieces, black_pieces
                )
        else:
            # Check if the selected square is a valid move
            if selected_square in self.possible_moves:
                finished_move = True

                # Find captured pieces, if any
                captured_piece = next(
                    (p for p in opponent.pieces if p.board_position == selected_square),
                    None,
                )
                if captured_piece is not None:
                    opponent.captured_piece(captured_piece)

                    if isinstance(captured_piece, King):
                        self.game.end_game(self)
                else:
                    arcade.play_sound(self.game.move_sound)
                self.selected_piece.set_board_position(selected_square)

            # Reset variables
            self.selected_piece = None
            self.possible_moves = []

        return finished_move

    def captured_piece(self, piece):
        self.pieces.remove(piece)
        arcade.play_sound(self.game.take_sound)
