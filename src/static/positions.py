import numpy as np

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
        "castling_rights": np.ulonglong(0b1111),
        "is_white": np.ulonglong(0),
        "check": np.ulonglong(0),
        "en_passant_squares": np.ulonglong(0),
        "w_pieces_mask":np.ulonglong(0),
        "b_pieces_mask":np.ulonglong(0),
        "all_pieces_mask":np.ulonglong(0)
    }

    @staticmethod
    def start_pos():
        all_w_pieces = np.bitwise_or.reduce(Positions.START_POS["w_pieces"])
        all_b_pieces = np.bitwise_or.reduce(Positions.START_POS["b_pieces"])
        all_pieces = np.bitwise_or(all_w_pieces, all_b_pieces)

        Positions.START_POS["w_pieces_mask"] = all_w_pieces
        Positions.START_POS["b_pieces_mask"] = all_b_pieces
        Positions.START_POS["all_pieces_mask"] = all_pieces

        return Positions.START_POS







        