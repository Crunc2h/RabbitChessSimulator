import numpy as np



class Board:   
    
    def __init__(self, position):
        self.pos = self.str_to_np_pos(position)
    

    def __repr__(self):
        pass

            
            
    def str_to_np_pos(self, pos):
        converted_pos = []
        pieces_pos = np.zeros(64, dtype=np.ulonglong)
        for key, value in pos.items():
            if len(value) > 64:
                raise ValueError("Length of the bitboard is over 64!")
            converted_val = np.ulonglong(value)
            converted_pos.append(converted_val)
            pieces_pos = np.bitwise_or(pieces_pos, converted_val)
        converted_pos.append(pieces_pos)
        return np.array(converted_pos)
    

    

