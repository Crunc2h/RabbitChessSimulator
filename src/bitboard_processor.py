"""
def get_piece_position_mask(self, square_idx) -> np.ulonglong:
        return np.ulonglong(1 << square_idx)
    
    def extract_individual_position_masks(self, position_masks):
        return np.array(list(filter(lambda position_mask:np.bitwise_and(position_mask, position_masks), self.all_position_masks)))
    
    def calculate_static_piece_mask(prev_all_attacks_mask, from_sqr_piece_attack_mask, to_sqr_piece_attack_mask):
        return np.bitwise_or(np.bitwise_xor(prev_all_attacks_mask, from_sqr_piece_attack_mask), to_sqr_piece_attack_mask)
    
    def calculate_dynamic_piece_mask(self, piece_type, current_square_idx, all_pieces_mask):
        pos_mask = self.get_piece_position_mask(current_square_idx)
        attack_mask = self.get_attack_mask_of_type(current_square_idx, Pieces.QUEEN)[0]
        occupied_atk_squares = np.bitwise_and(attack_mask, np.invert(all_pieces_mask))
        if piece_type == Pieces.ROOK:
            return self.__rook_dynamic_attack_mask(pos_mask, occupied_atk_squares)
        elif piece_type == Pieces.BISHOP:
            return self.bishop_path_blocked_attack_mask(pos_mask, occupied_atk_squares)
        elif piece_type == Pieces.QUEEN:
            return self.queen_path_blocked_attack_mask(pos_mask, occupied_atk_squares)
        else:
            raise Exception("Invalid piece type for dynamic pathtracing!")
        
    """
    
    