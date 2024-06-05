import numpy as np
from static.pieces import Pieces


class MoveValidator:
    
    def __init__(self, bb_masks_obj):
        self.key_map = {
            5:Pieces.W_PAWN,
           -5:Pieces.B_PAWN,
            0:Pieces.ROOK,
            1:Pieces.KNIGHT,
            2:Pieces.BISHOP,
            3:Pieces.QUEEN,
            4:Pieces.KING,
        }
        self.__bb_masks = bb_masks_obj
    
    def __board_key_to_piece_type(self, key_int):
        return self.key_map[key_int]
    
    def get_piece_type_idx_from_pos_mask(self, pos_mask, pieces_arr):
        return np.argmax(np.apply_along_axis(func1d=lambda piece_type_mask: np.bitwise_and(piece_type_mask, pos_mask) > 0,
                                             axis=0, 
                                             arr=pieces_arr))
    
    def is_valid(self, from_square, to_square, board_obj):
        board_data = board_obj.data
        from_square_idx = from_square["idx"]
        to_square_idx = to_square["idx"]
        side = board_data["S"]
        
        from_sqr_piece_pos64 = self.__bb_masks.get_piece_positions64_from_idx()[from_square_idx]
        to_sqr_piece_pos64 = self.__bb_masks.get_piece_positions64_from_idx()[to_square_idx]

        if np.bitwise_and(from_sqr_piece_pos64, board_data["All_Pieces_mask"]) == 0:
            raise Exception("There isn't a piece at the specified source square!")
        if ((side and np.bitwise_and(from_sqr_piece_pos64, board_data["W_Pieces_mask"]) == 0)
             or (not side and np.bitwise_and(from_sqr_piece_pos64, board_data["B_Pieces_mask"]) == 0)):
            raise Exception("The piece at the source square belongs to the opponent!")
        if ((side and np.bitwise_and(to_sqr_piece_pos64, board_data["W_Pieces_mask"]) > 0)
             or (not side and np.bitwise_and(to_sqr_piece_pos64, board_data["B_Pieces_mask"]) > 0)):
            raise Exception("Another one of your pieces already occupies target square!")
        
        if side:
            piece_type = self.__board_key_to_piece_type(self.get_piece_type_idx_from_pos_mask(from_sqr_piece_pos64, board_obj.data["W_Pieces_arr"]))
        else:
            piece_type_idx = self.get_piece_type_idx_from_pos_mask(from_sqr_piece_pos64, board_obj.data["B_Pieces_arr"])
            if piece_type_idx == 5: piece_type_idx *= -1
            piece_type = self.__board_key_to_piece_type(piece_type_idx)
        

        if piece_type != Pieces.W_PAWN and piece_type != Pieces.B_PAWN:
            from_sqr_piece_attacks64 = self.__bb_masks.get_all_piece_attacks64()[piece_type][from_sqr_piece_pos64] 
        else:
            pawn_movements64, pawn_attacks64 = (self.__bb_masks.get_all_piece_attacks64()[piece_type]["move"][from_sqr_piece_pos64],
                                                self.__bb_masks.get_all_piece_attacks64()[piece_type]["attack"][from_sqr_piece_pos64])
            is_pawn_movement = np.bitwise_and(pawn_movements64, to_sqr_piece_pos64) > 0
            if is_pawn_movement:
                from_sqr_piece_attacks64 = pawn_movements64
                if np.bitwise_and(to_sqr_piece_pos64, board_data["All_Pieces_mask"]) > 0:
                    raise Exception("Pawn cannot move to a square already occupied by another piece!")
            else:
                from_sqr_piece_attacks64 = pawn_attacks64
        
        move_exists_for_piece_type = np.bitwise_and(from_sqr_piece_attacks64, to_sqr_piece_pos64) > 0
        if not move_exists_for_piece_type:
            raise Exception("Illegal move!")
        
        adjacent_sqr_mask = self.__bb_masks.get_all_adj_squares64_of_idx()[from_square_idx]
        is_move_to_sqr_adjacent = np.bitwise_and(adjacent_sqr_mask, to_sqr_piece_pos64) > 0
        
        if not is_move_to_sqr_adjacent and piece_type != Pieces.KNIGHT:
            piece_movement_path = self.__bb_masks.get_all_piece_paths64_static()[piece_type][(from_square_idx, to_square_idx)]
            if np.bitwise_and(piece_movement_path, board_data["All_Pieces_mask"]) > 0:
                raise Exception("There is a piece obstructing the path towards target square!")
        
        
        if side:
            is_capture = np.bitwise_and(to_sqr_piece_pos64, board_data["B_Pieces_mask"]) > 0
            to_square_piece_attack_mask = self.__bb_masks.get_attack_mask_of_type(to_square_idx, piece_type)
            is_check = np.bitwise_and(to_square_piece_attack_mask, board_data["B_Pieces_arr"][4])
        else:
            is_capture = np.bitwise_and(to_sqr_piece_pos64, board_data["W_Pieces_mask"]) > 0
            to_square_piece_attack_mask = self.__bb_masks.get_attack_mask_of_type(to_square_idx, piece_type)
            is_check = np.bitwise_and(to_square_piece_attack_mask, board_data["W_Pieces_arr"][4])

        
        





        