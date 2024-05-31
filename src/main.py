import numpy as np
from static.positions import START_POS
from board import Board



test = Board(START_POS)

print(np.bitwise_xor(test.pos, np.zeros(64, dtype=np.ulonglong)))