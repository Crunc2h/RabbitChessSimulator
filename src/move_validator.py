import numpy as np
from static.pieces import Pieces
from bitboard_printer import BitboardPrinter

class MoveValidator:
    
    def __init__(self, 
                 bb_masks_obj,
                 bb_processor_obj):  
        self.__bb_masks = bb_masks_obj
        self.__bb_processor = bb_processor_obj
    
    def is_valid(self,
                 side, 
                 from_square_idx, 
                 to_square_idx, 
                 all_side_pieces64_arr,
                 all_oppo_pieces64_arr,
                 all_pieces64,
                 all_side_pieces64,
                 all_oppo_pieces64,
                 en_passant_squares64):
        all_piece_positions64_from_idx = self.__bb_masks.get_all_piece_positions64_from_idx()
        
        from_sqr_piece_pos64 = all_piece_positions64_from_idx[from_square_idx]
        to_sqr_piece_pos64 = all_piece_positions64_from_idx[to_square_idx]

        if np.bitwise_and(from_sqr_piece_pos64, all_pieces64) == 0:
            return False, None
        if np.bitwise_and(from_sqr_piece_pos64, all_side_pieces64) == 0:
            return False, None
        if np.bitwise_and(to_sqr_piece_pos64, all_side_pieces64) > 0:
            return False, None
        
        piece_type, piece_type_idx = self.__bb_processor.get_piece_type_and_idx(side, 
                                                                                from_sqr_piece_pos64, 
                                                                                all_side_pieces64)
        all_attacks64 = self.__bb_masks.get_all_attacks64_static()
        to_sqr_piece_attacks64 = None
        
        if piece_type != Pieces.W_PAWN and piece_type != Pieces.B_PAWN:
            from_sqr_piece_attacks64 = all_attacks64[piece_type][from_sqr_piece_pos64] 
        else:
            pawn_movements64, pawn_attacks64 = (all_attacks64[piece_type]["move"][from_sqr_piece_pos64],
                                                all_attacks64[piece_type]["attack"][from_sqr_piece_pos64])
            
            is_pawn_movement = np.bitwise_and(pawn_movements64, to_sqr_piece_pos64) > 0
            if is_pawn_movement:
                if np.bitwise_and(to_sqr_piece_pos64, all_pieces64) > 0:
                    return False, None
                from_sqr_piece_attacks64 = pawn_movements64
            else:
                if np.bitwise_and(to_sqr_piece_pos64, all_pieces64) == 0 and np.bitwise_and(to_sqr_piece_pos64, en_passant_squares64):
                    return False, None
                from_sqr_piece_attacks64 = pawn_attacks64
                
            to_sqr_piece_attacks64 = all_attacks64[piece_type]["attack"][to_sqr_piece_pos64]

        move_exists_for_piece_type = np.bitwise_and(from_sqr_piece_attacks64, to_sqr_piece_pos64) > 0
        if move_exists_for_piece_type == False:
            return False, None
        
        adjacent_sqr_mask = self.__bb_masks.get_all_adj_squares64_of_idx()[from_square_idx]
        is_move_to_sqr_adjacent = np.bitwise_and(adjacent_sqr_mask, to_sqr_piece_pos64) > 0

        if is_move_to_sqr_adjacent == False and piece_type != Pieces.KNIGHT:
            piece_movement_path = self.__bb_masks.get_all_piece_paths64_static()[piece_type][(from_square_idx, to_square_idx)]
            
            if np.bitwise_and(piece_movement_path, all_pieces64) > 0:
                return False, None

        if not to_sqr_piece_attacks64: to_sqr_piece_attacks64 = all_attacks64[piece_type][to_sqr_piece_pos64]

        updated_all_pieces_pos64 = self.update_pos64(all_pieces64, from_sqr_piece_pos64, to_sqr_piece_pos64)
        cp_side_pieces64_arr = np.copy(all_side_pieces64_arr)
        cp_oppo_pieces64_arr = np.copy(all_oppo_pieces64_arr)
        
        if np.bitwise_and(to_sqr_piece_pos64, all_oppo_pieces64) > 0:
            captured_piece_type_idx = self.__bb_processor.get_piece_type_idx_from_pos64(to_sqr_piece_pos64, cp_oppo_pieces64_arr)
            cp_oppo_pieces64_arr[captured_piece_type_idx] = np.bitwise_xor(to_sqr_piece_pos64, cp_oppo_pieces64_arr[captured_piece_type_idx])
        
        cp_side_pieces64_arr[piece_type_idx] = np.bitwise_xor(cp_side_pieces64_arr[piece_type_idx], np.bitwise_or(from_sqr_piece_pos64, to_sqr_piece_pos64))
                
        side_static_attacks = self.__bb_processor.update_all_attacks64_static(cp_side_pieces64_arr, side)
        oppo_static_attacks = self.__bb_processor.update_all_attacks64_static(cp_oppo_pieces64_arr, not side)

        side_dynamic_attacks = self.update_all_attacks64_dynamic(cp_side_pieces64_arr, updated_all_pieces_pos64)
        oppo_dynamic_attacks = self.update_all_attacks64_dynamic(cp_oppo_pieces64_arr, updated_all_pieces_pos64)

        print("============WHITE_ALL_ATTACKS_DYNAMIC==============")
        BitboardPrinter.print(side_dynamic_attacks)
        print("============BLACK ALL ATTACKS DYNAMIC==============")
        BitboardPrinter.print(oppo_dynamic_attacks)

        oppo_all_attacks = np.bitwise_or(oppo_dynamic_attacks, oppo_static_attacks)
        side_all_attacks = np.bitwise_or(side_dynamic_attacks, side_static_attacks)
        
        side_king_pos64 = cp_side_pieces64_arr[4]
        enemy_king_pos64 = cp_oppo_pieces64_arr[4]
        
        if np.bitwise_and(oppo_all_attacks, side_king_pos64) > 0:
            return False, None
        
        is_capture = np.bitwise_and(to_sqr_piece_pos64, all_oppo_pieces64) > 0
        is_check = np.bitwise_and(side_all_attacks, enemy_king_pos64) > 0
        
        return True, {
            "capture":is_capture,
            "check":is_check,
            "new_board_pos64":updated_all_pieces_pos64,
            "from_sqr_pos64":from_sqr_piece_pos64,
            "to_sqr_pos64":to_sqr_piece_pos64,
            "piece_type_idx":piece_type_idx
        }
    

    


        
        





        