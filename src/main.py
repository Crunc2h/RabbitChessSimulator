import numpy as np

from bitboard import Bitboard
from bitboard_printer import BitboardPrinter
from bitboard_masks import BitboardMasks
from static.squares import Squares
from static.positions import Positions
from static.pieces import Pieces
from move_validator import MoveValidator

test_board = Bitboard(Positions.start_pos())
masks_obj = BitboardMasks()
validator = MoveValidator(masks_obj)
print(validator.is_valid(Squares.a1, Squares.a3, test_board))

