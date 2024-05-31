import numpy as np



class Board:   
    
    def __init__(self, position):
        self.pos = self.bin_to_htable(position)
    

    def __repr__(self):
        binary_as_str = format(self.pos["pos"], '#64b')[2::]
        res = "\n\n"
        for i in range(len(binary_as_str), 0, -1):
            if i % 8 == 0 and i != 0:
                res += f"{int(i / 8)}   "
            res += f"{binary_as_str[i - 1]} "
            
            if (i - 1) % 8 == 0:
                res += "\n"
            if i == 1:
                res += "\n    a b c d e g h f\n\n"
        
        return res
            
            
    def bin_to_htable(self, pos):
        converted_pos = {}
        pieces_pos = np.ulonglong(0)
        for key, value in pos.items():
            converted_pos[key] = value
            pieces_pos = np.bitwise_or(pieces_pos, value)
        
        converted_pos["pos"] = pieces_pos
        return converted_pos
    
    
    def mask_piece_pos(self, sqr_idx):
        mask = np.zeros(64).astype(np.bool_)
        mask[sqr_idx] = np.bool_(1)
        return mask

    

    

