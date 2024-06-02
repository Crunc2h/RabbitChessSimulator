import numpy as np
from static.pieces import Pieces


class Positions:
    
    START_POS = { 
        "W_Pieces_arr":np.array([
                                 np.ulonglong(0b10000001),
                                 np.ulonglong(0b01000010),
                                 np.ulonglong(0b00100100),
                                 np.ulonglong(0b00010000),
                                 np.ulonglong(0b00001000),
                                 np.ulonglong(0b1111111100000000)
                                 ]),
        "B_Pieces_arr":np.array([
                                 np.ulonglong(0b1000000100000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0100001000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0010010000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0001000000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0000100000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0000000011111111000000000000000000000000000000000000000000000000),
                                 ]),
        "S": np.ulonglong(0b1)
    }

    @staticmethod
    def start_pos():
        Positions.START_POS["W_Pieces_mask"] =  np.ulonglong(0)
        Positions.START_POS["B_Pieces_mask"] =  np.ulonglong(0)
        
        for piece_type_mask in Positions.START_POS["W_Pieces_arr"]:
            Positions.START_POS["W_Pieces_mask"] = Positions.START_POS["W_Pieces_mask"] | piece_type_mask
        for piece_type_mask in Positions.START_POS["B_Pieces_arr"]:
            Positions.START_POS["B_Pieces_mask"] = Positions.START_POS["B_Pieces_mask"] | piece_type_mask
        Positions.START_POS["All_Pieces_mask"] = Positions.START_POS["W_Pieces_mask"] | Positions.START_POS["B_Pieces_mask"]
        return Positions.START_POS







        