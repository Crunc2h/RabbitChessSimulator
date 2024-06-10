import numpy as np
from static.pieces import Pieces
from bitboard_storage import BitboardMasks
from bitboard_helper import BitboardStorageHelper
from bitboard_printer import BitboardPrinter

class Positions:
    
    START_POS = { 
        "w_pieces":np.array([
                                 np.ulonglong(0b10000001),
                                 np.ulonglong(0b01000010),
                                 np.ulonglong(0b00100100),
                                 np.ulonglong(0b00010000),
                                 np.ulonglong(0b00001000),
                                 np.ulonglong(0b1111111100000000)
                                 ]),
        "b_pieces":np.array([
                                 np.ulonglong(0b1000000100000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0100001000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0010010000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0001000000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0000100000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0000000011111111000000000000000000000000000000000000000000000000),
                                 ]),
        "castling_check_color": np.ulonglong(0b01),
        "all_w_pieces":np.ulonglong(0),
        "all_b_pieces":np.ulonglong(0),
        "all_pieces":np.ulonglong(0)
    }

    @staticmethod
    def start_pos():
        
        
        all_w_pieces = np.bitwise_or.reduce(Positions.START_POS["w_pieces"])
        all_b_pieces = np.bitwise_or.reduce(Positions.START_POS["b_pieces"])
        all_pieces = np.bitwise_or(all_w_pieces, all_b_pieces)

        Positions.START_POS["all_w_pieces"] = all_w_pieces
        Positions.START_POS["all_b_pieces"] = all_b_pieces
        Positions.START_POS["all_pieces"] = all_pieces
        
        return Positions.START_POS







        