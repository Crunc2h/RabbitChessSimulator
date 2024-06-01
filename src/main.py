import numpy as np

from bitboard import Bitboard
from bitboard_printer import BitboardPrinter
from bitboard_mask import BitboardMask
from static.squares import Squares
from static.positions import Positions

test_black_normal = BitboardMask.piece_position_mask(Squares.f4["idx"])
test_black_mask = BitboardMask.bishop_attack_mask(test_black_normal)
BitboardPrinter.print(test_black_mask)
