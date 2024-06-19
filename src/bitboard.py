import numpy as np


class Bitboard:   
    def __init__(self, data):
        self.w_pieces = data["w_pieces"]
        self.b_pieces = data["b_pieces"]
        self.castling_rights = data["castling_rights"]
        self.en_passant_squares = data["en_passant_squares"]
        self.is_check = data["check"]
        self.is_white = data["is_white"]
        self.all_pieces_mask = data["all_pieces_mask"]
        self.w_pieces_mask = data["w_pieces_mask"]
        self.b_pieces_mask = data["b_pieces_mask"]
    

        
        
             
    

    
    


    

    

