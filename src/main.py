import numpy as np

from bitboard import Bitboard
from bitboard_printer import BitboardPrinter
from bitboard_mask import self
from static.squares import Squares
from static.positions import Positions

test_black_normal = self.piece_position_mask(Squares.e5["idx"])
test_black_mask = self.king_attack_mask(test_black_normal)
BitboardPrinter.print(test_black_mask)
