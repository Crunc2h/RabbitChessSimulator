import numpy as np
from static.pieces import Pieces
from bitboard_storage import BitboardMasks
from bitboard_helper import BitboardStorageHelper
from bitboard_printer import BitboardPrinter

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
        "W_Attacks64_static": np.ulonglong(0),
        "B_Pieces_arr":np.array([
                                 np.ulonglong(0b1000000100000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0100001000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0010010000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0001000000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0000100000000000000000000000000000000000000000000000000000000000),
                                 np.ulonglong(0b0000000011111111000000000000000000000000000000000000000000000000),
                                 ]),
        "B_Attacks64_static": np.ulonglong(0), 
        "side_to_move": np.ulonglong(0b01)
    }

    @staticmethod
    def start_pos():

        init_w_pawn_idxs = [8, 9, 10, 11, 12, 13, 14, 15]
        init_w_n_idxs = [1, 6]
        init_w_k_idx = [3]
        init_b_pawn_idxs = [55, 54, 53, 52, 51, 50, 49, 48]
        init_b_n_idxs = [62, 57]

        init_b_k_idx = [59]
        
        Positions.START_POS["W_Attacks64_static"] = np.ulonglong(0)
        Positions.START_POS["B_Attacks64_static"] = np.ulonglong(0)
        masks = BitboardMasks(BitboardStorageHelper())
        
        masks_atks = masks.get_all_attacks64_static()
        masks_poss = masks.get_all_piece_positions64_from_idx()
        
        for idx in init_w_pawn_idxs:
            Positions.START_POS["W_Attacks64_static"] = masks_atks[Pieces.W_PAWN]["attack"][masks_poss[idx]]

        for idx in init_w_n_idxs:
            Positions.START_POS["W_Attacks64_static"] = np.bitwise_or(Positions.START_POS["W_Attacks64_static"], masks_atks[Pieces.KNIGHT][masks_poss[idx]])
        for idx in init_w_k_idx:
            Positions.START_POS["W_Attacks64_static"] = np.bitwise_or(Positions.START_POS["W_Attacks64_static"], masks_atks[Pieces.KING][masks_poss[idx]])

        
        for idx in init_b_pawn_idxs:
            Positions.START_POS["B_Attacks64_static"] = masks_atks[Pieces.B_PAWN]["attack"][masks_poss[idx]]
        for idx in init_b_n_idxs:
            Positions.START_POS["B_Attacks64_static"] = np.bitwise_or(Positions.START_POS["B_Attacks64_static"], masks_atks[Pieces.KNIGHT][masks_poss[idx]])
        for idx in init_b_k_idx:
            Positions.START_POS["B_Attacks64_static"] = np.bitwise_or(Positions.START_POS["B_Attacks64_static"], masks_atks[Pieces.KING][masks_poss[idx]])



        
        Positions.START_POS["W_Pieces_mask"] =  np.ulonglong(0)
        Positions.START_POS["B_Pieces_mask"] =  np.ulonglong(0)
        
        for piece_type_mask in Positions.START_POS["W_Pieces_arr"]:
            Positions.START_POS["W_Pieces_mask"] = Positions.START_POS["W_Pieces_mask"] | piece_type_mask
        for piece_type_mask in Positions.START_POS["B_Pieces_arr"]:
            Positions.START_POS["B_Pieces_mask"] = Positions.START_POS["B_Pieces_mask"] | piece_type_mask
        Positions.START_POS["All_Pieces_mask"] = Positions.START_POS["W_Pieces_mask"] | Positions.START_POS["B_Pieces_mask"]

    
        
        return Positions.START_POS







        