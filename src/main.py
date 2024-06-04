import numpy as np

from bitboard import Bitboard
from bitboard_printer import BitboardPrinter
from bitboard_storage import BitboardMasks
from static.squares import Squares
from static.positions import Positions
from static.pieces import Pieces
from move_validator import MoveValidator
from bitboard_helper import BitboardStorageHelper
helper = BitboardStorageHelper()
test_board = Bitboard(Positions.start_pos())
masks_obj = BitboardMasks(helper_obj=helper)

sqr_e4 = helper.get_piece_position_mask(Squares.c3["idx"])
rook_blocked = masks_obj.knight_attacks64_static(sqr_e4)
BitboardPrinter.print(rook_blocked)





