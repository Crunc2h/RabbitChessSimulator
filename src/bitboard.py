import numpy as np


class Bitboard:   
    
    def __init__(self, position):
        self.data = self.bin_to_htable(position)
             
    def bin_to_htable(self, pos):
        converted_data = {}
        pieces_pos = np.ulonglong(0)
        for key, value in pos.items():
            converted_data[key] = value
            pieces_pos = np.bitwise_or(pieces_pos, value)
        
        converted_data["pos"] = pieces_pos
        return converted_data
    
    


    

    

