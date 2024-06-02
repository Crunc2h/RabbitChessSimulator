import numpy as np

from bitboard import Bitboard
from bitboard_printer import BitboardPrinter
from bitboard_mask import BitboardMasks
from static.squares import Squares
from static.positions import Positions
from static.pieces import Pieces

masks = BitboardMasks()

atk1 = masks.get_path_mask_of_type(12, 33, Pieces.BISHOP) 
BitboardPrinter.print(atk1)


