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
BitboardPrinter.print(test_board.data["W_Attacks_mask"])



all_pieces_mask = test_board.data["All_Pieces_mask"]
w_queen = masks_obj.get_piece_position_mask(Squares.e5["idx"])
w_queen_atk = masks_obj.get_attack_mask_of_type(Squares.e5["idx"], Pieces.QUEEN)[0]
BitboardPrinter.print(w_queen)
BitboardPrinter.print(w_queen_atk)
occupied_atk_squares = np.bitwise_and(w_queen_atk, np.invert(all_pieces_mask))
BitboardPrinter.print(occupied_atk_squares)

BitboardPrinter.print(masks_obj.queen_path_blocked_attack_mask(w_queen, occupied_atk_squares))

