import numpy as np
from static.pieces import Pieces
from bitboard_storage import BitboardMasks

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
        """
        init_w_pawn_idxs = [8, 9, 10, 11, 12, 13, 14, 15]
        init_w_r_idxs = [0, 7]
        init_w_n_idxs = [1, 6]
        init_w_b_idxs = [2, 5]
        init_w_q_idx = [4]
        init_w_k_idx = [3]
        init_b_pawn_idxs = [55, 54, 53, 52, 51, 50, 49, 48]
        init_b_r_idxs = [63, 56]
        init_b_n_idxs = [62, 57]
        init_b_b_idxs = [61, 58]
        init_b_q_idx = [60]
        init_b_k_idx = [59]
        Positions.START_POS["W_Attacks_mask"] = np.ulonglong(0)
        Positions.START_POS["B_Attacks_mask"] = np.ulonglong(0)
        masks_test = BitboardMasks()
        
        for idx in init_w_pawn_idxs:
            Positions.START_POS["W_Attacks_mask"] = np.bitwise_or(Positions.START_POS["W_Attacks_mask"]
                                                                  ,masks_test.get_attack_mask_of_type(idx, Pieces.W_PAWN)[0])
        for idx in init_w_n_idxs:
            Positions.START_POS["W_Attacks_mask"] = np.bitwise_or(Positions.START_POS["W_Attacks_mask"], masks_test.get_attack_mask_of_type(idx, Pieces.KNIGHT)[0])
        for idx in init_w_k_idx:
            Positions.START_POS["W_Attacks_mask"] = np.bitwise_or(Positions.START_POS["W_Attacks_mask"], masks_test.get_attack_mask_of_type(idx, Pieces.KING)[0])

        
        
        for idx in init_b_pawn_idxs:
            Positions.START_POS["B_Attacks_mask"] = np.bitwise_or(Positions.START_POS["B_Attacks_mask"], masks_test.get_attack_mask_of_type(idx, Pieces.W_PAWN)[0])
        for idx in init_b_n_idxs:
            Positions.START_POS["B_Attacks_mask"] = np.bitwise_or(Positions.START_POS["B_Attacks_mask"], masks_test.get_attack_mask_of_type(idx, Pieces.KNIGHT)[0])
        for idx in init_b_k_idx:
            Positions.START_POS["B_Attacks_mask"] = np.bitwise_or(Positions.START_POS["B_Attacks_mask"], masks_test.get_attack_mask_of_type(idx, Pieces.KING)[0])



        
        Positions.START_POS["W_Pieces_mask"] =  np.ulonglong(0)
        Positions.START_POS["B_Pieces_mask"] =  np.ulonglong(0)
        
        for piece_type_mask in Positions.START_POS["W_Pieces_arr"]:
            Positions.START_POS["W_Pieces_mask"] = Positions.START_POS["W_Pieces_mask"] | piece_type_mask
        for piece_type_mask in Positions.START_POS["B_Pieces_arr"]:
            Positions.START_POS["B_Pieces_mask"] = Positions.START_POS["B_Pieces_mask"] | piece_type_mask
        Positions.START_POS["All_Pieces_mask"] = Positions.START_POS["W_Pieces_mask"] | Positions.START_POS["B_Pieces_mask"]

        """
        
        return Positions.START_POS







        