import numpy as np

START_POS = {
      "W_P": 6 * 8 * '0' + 8 * '1' + 8 * '0',
      "W_R": 7 * 8 * '0' + "10000001", 
      "W_N": 7 * 8 * '0' + "01000010",
      "W_B": 7 * 8 * '0' + "00100100",
      "W_Q": 7 * 8 * '0' + "00010000",
      "W_K": 7 * 8 * '0' + "00001000",

      "B_P": 8 * '0' + 8 * '1' + 6 * 8 * '0',
      "B_R": "10000001" + 7 * 8 * '0',
      "B_N": "01000010" + 7 * 8 * '0',
      "B_B": "00100100" + 7 * 8 * '0',
      "B_Q": "00010000" + 7 * 8 * '0',
      "B_K": "00001000" + 7 * 8 * '0',
}

def convert_str_pos_into_np(pos):
    pieces_pos = np.zeros(64, dtype=int)
    for key, value in pos.items():
        if len(value) > 64:
            raise ValueError("Length of the bitboard is over 64!")
        pos[key] = np.array(list(map(lambda bit: int(bit), value)), dtype=int)
        pieces_pos = np.bitwise_or(pieces_pos, pos[key])
    pos["pos"] = pieces_pos

convert_str_pos_into_np(START_POS)



        