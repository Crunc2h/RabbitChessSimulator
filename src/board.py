import numpy as np



class Board:   
    
    def __init__(self, position):
        self.pos = self.str_to_np_pos(position)
    

    def __repr__(self):
        pass

            
            
    def str_to_np_pos(self, pos):
        converted_pos = []
        pieces_pos = np.zeros(64, dtype=np.bool_)
        for value in pos.values():
            if len(value) != 64:
                raise ValueError("Length of the bitboard is not 64!")
            
            value_as_bit_arr = np.array(list(map(lambda bit: int(bit), value)), dtype=np.bool_)
            converted_pos.append(value_as_bit_arr)
            
            pieces_pos = np.bitwise_or(pieces_pos, value_as_bit_arr)
        
        converted_pos.append(pieces_pos)
        
        return np.array(converted_pos)
    

    

