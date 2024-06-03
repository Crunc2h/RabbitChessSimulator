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



all_pieces_mask = test_board.data["All_Pieces_mask"]


testers = test_board.data["W_Pieces_arr"][5]
for t in masks_obj.extract_individual_position_masks(testers):
    BitboardPrinter.print(t)

