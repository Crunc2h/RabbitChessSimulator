import numpy as np

from bitboard import Bitboard
from bitboard_printer import BitboardPrinter
from bitboard_mask import BitboardMasks
from static.squares import Squares
from static.positions import Positions
from static.pieces import Pieces

masks = BitboardMasks()
print(masks.move_exists(Squares.b1, Squares.a3, Pieces.KNIGHT))
