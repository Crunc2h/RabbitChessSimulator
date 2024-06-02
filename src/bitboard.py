import numpy as np


class Bitboard:   
    
    def __init__(self, position):
        self.data = self.bin_to_htable(position)
             
    def bin_to_htable(self, board_data):
        converted_data = {}
        for key, value in board_data.items():
            converted_data[key] = value
    
        return converted_data
    
    


    

    

