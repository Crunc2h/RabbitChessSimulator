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
        from_sqr_piece_pos_mask = self.__bb_masks.get_piece_position_mask(from_square_idx)
        to_sqr_piece_pos_mask = self.__bb_masks.get_piece_position_mask(to_square_idx)

        if np.bitwise_and(from_sqr_piece_pos_mask, board_data["All_Pieces_mask"]) == 0:
            raise Exception("There isn't a piece at the specified source square!")
        if ((side and np.bitwise_and(from_sqr_piece_pos_mask, board_data["W_Pieces_mask"]) == 0)
             or (not side and np.bitwise_and(from_sqr_piece_pos_mask, board_data["B_Pieces_mask"]) == 0)):
            raise Exception("That piece at the source square belongs to the opponent!")
        if ((side and np.bitwise_and(to_sqr_piece_pos_mask, board_data["W_Pieces_mask"]) > 0)
             or (not side and np.bitwise_and(to_sqr_piece_pos_mask, board_data["B_Pieces_mask"]) > 0)):
            raise Exception("Another one of your pieces already occupies target square!")
        
        if side:
            piece_type = self.__board_key_to_piece_type(self.get_piece_type_idx_from_pos_mask(from_sqr_piece_pos_mask, board_obj.data["W_Pieces_arr"]))
        else:
            piece_type_idx = self.get_piece_type_idx_from_pos_mask(from_sqr_piece_pos_mask, board_obj.data["B_Pieces_arr"])
            if piece_type_idx == 5: piece_type_idx *= -1
            piece_type = self.__board_key_to_piece_type(piece_type_idx)
        
        from_sqr_piece_attack_mask, pawn_movement = self.__bb_masks.get_attack_mask_of_type(from_square_idx, piece_type)
        
        move_exists_for_piece_type = np.bitwise_and(from_sqr_piece_attack_mask, to_sqr_piece_pos_mask) > 0
        if not move_exists_for_piece_type:
            raise Exception("Illegal move!")
        
        if pawn_movement != None:
            if ((side and np.bitwise_and(to_sqr_piece_pos_mask, board_data["B_Pieces_mask"]) > 0) 
            or (not side and np.bitwise_and(to_sqr_piece_pos_mask, board_data["W_Pieces_mask"]) > 0)):
                raise Exception("Pawn cannot move to a square already occupied by an enemy piece!")
        
        adjacent_sqr_mask = self.__bb_masks.get_attack_mask_of_type(from_square_idx, Pieces.KING)
        is_move_to_sqr_adjacent = np.bitwise_and(adjacent_sqr_mask, to_sqr_piece_pos_mask) > 0
        if not is_move_to_sqr_adjacent and piece_type != Pieces.KNIGHT:
            piece_movement_path = self.__bb_masks.get_path_mask_of_type(from_square_idx, to_square_idx, piece_type)
            if np.bitwise_and(piece_movement_path, board_data["All_Pieces_mask"]) > 0:
                raise Exception("There is a piece obstructing the path towards target square!")
        
        
        if side:
            is_capture = np.bitwise_and(to_sqr_piece_pos_mask, board_data["B_Pieces_mask"]) > 0
            to_square_piece_attack_mask = self.__bb_masks.get_attack_mask_of_type(to_square_idx, piece_type)
            is_check = np.bitwise_and(to_square_piece_attack_mask, board_data["B_Pieces_arr"][4])
        else:
            is_capture = np.bitwise_and(to_sqr_piece_pos_mask, board_data["W_Pieces_mask"]) > 0
            to_square_piece_attack_mask = self.__bb_masks.get_attack_mask_of_type(to_square_idx, piece_type)
            is_check = np.bitwise_and(to_square_piece_attack_mask, board_data["W_Pieces_arr"][4])

        
        





        