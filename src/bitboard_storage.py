import numpy as np
import operator
from static.pieces import Pieces


class BitboardMasks:
    
    def get_attack_mask_of_type(self, square_idx, piece_type, pos_mask=None) -> np.ulonglong:
        if piece_type not in self.__all_attack_masks.keys():
            raise KeyError("Invalid piece type for attack mask retreival!")
        
        piece_pos_mask = self.get_piece_position_mask(square_idx) if pos_mask is None else pos_mask
        
        if piece_type == Pieces.W_PAWN or piece_type == Pieces.B_PAWN:
            try:
                try:
                    return self.__all_attack_masks[piece_type]["attack"][piece_pos_mask], True
                except KeyError:
                    return self.__all_attack_masks[piece_type]["move"][piece_pos_mask], None
            except KeyError:
                return None, None
        try:
            return self.__all_attack_masks[piece_type][piece_pos_mask], None
        except KeyError:
            return None, None  
        
    def get_path_mask_of_type(self, source_square_idx, target_square_idx, piece_type) -> np.ulonglong:
        if piece_type not in self.__all_path_masks.keys():
            raise KeyError("Invalid piece type for path mask retreival!")
        try:
            return self.__all_path_masks[piece_type][(source_square_idx, target_square_idx)]
        except KeyError:
            return None
    
    
    
    def __init__(self):
        self.__EDGE_MASK_TOP = np.ulonglong(0b11111111 << 56)
        self.__EDGE_MASK_BOTTOM = np.ulonglong(0b11111111)
        self.__EDGE_MASK_LEFT = np.ulonglong(0b1000000010000000100000001000000010000000100000001000000010000000)
        self.__EDGE_MASK_RIGHT = np.ulonglong(0b0000000100000001000000010000000100000001000000010000000100000001)
        self.__W_EN_PASSANT_MASK = np.ulonglong(0b1111111100000000)
        self.__B_EN_PASSANT_MASK = np.ulonglong(0b0000000011111111 << 48)
        self.__RANK_STRIDE_LONG = 9
        self.__RANK_STRIDE_EQ = 8
        self.__RANK_STRIDE_SHORT = 7
        self.__FILE_STRIDE = 1
        self.all_position_masks = np.array([np.ulonglong(1 << i) for i in range(64)])
        self.__all_attack_masks = self.__construct_all_attack_masks()
        self.__all_path_masks = self.__construct_all_path_masks()
    
    def __construct_all_attack_masks(self) -> dict:
        all_attack_masks = {
            Pieces.W_PAWN:{
                "move":{},
                "attack":{}
            },
            Pieces.B_PAWN:{
                "move":{},
                "attack":{}
            },
            Pieces.ROOK:{},
            Pieces.KNIGHT:{},
            Pieces.BISHOP:{},
            Pieces.QUEEN:{},
            Pieces.KING:{}
        }
        
        for key in all_attack_masks.keys():
            for i in range(64):
                piece_position_mask = self.get_piece_position_mask(i)
                if key != Pieces.W_PAWN and key != Pieces.B_PAWN:
                    all_attack_masks[key][piece_position_mask] = self.__attack_mask_type_switch(key, piece_position_mask)
                else:
                    pawn_movement_mask, pawn_attack_mask = self.__attack_mask_type_switch(key, piece_position_mask)
                    all_attack_masks[key]["move"][piece_position_mask] = pawn_movement_mask
                    all_attack_masks[key]["attack"][piece_position_mask] = pawn_attack_mask 
     
        return all_attack_masks
    
    def __construct_all_path_masks(self) -> dict:
        all_path_masks = {
            Pieces.W_PAWN:{},
            Pieces.B_PAWN:{},
            Pieces.ROOK:{},
            Pieces.BISHOP:{},
        }
        for key in all_path_masks.keys():
            for i in range(64):
                source_pos_attack_mask = self.get_attack_mask_of_type(i, key)[0]
                for f in range(64):
                    target_pos_mask = self.get_piece_position_mask(f)
                    if np.bitwise_and(source_pos_attack_mask, target_pos_mask) == 0:
                        continue
                    target_pos_attack_mask = self.get_attack_mask_of_type(f, key)[0]
                    all_path_masks[key][(i, f)] = self.__piece_path_mask(i, f, source_pos_attack_mask, target_pos_attack_mask, key)
        
        all_path_masks[Pieces.QUEEN] = {}
        all_path_masks[Pieces.QUEEN].update(all_path_masks[Pieces.BISHOP])
        all_path_masks[Pieces.QUEEN].update(all_path_masks[Pieces.ROOK])
        
        return all_path_masks    
    
    def __piece_path_mask(self,
                          source_pos_idx,
                          target_pos_idx, 
                          source_pos_attack_mask, 
                          target_pos_attack_mask, 
                          piece_type) -> np.ulonglong:
        
        if source_pos_idx > target_pos_idx: larger_idx, smaller_idx = source_pos_idx, target_pos_idx
        else: larger_idx, smaller_idx = target_pos_idx, source_pos_idx
        interval_bits_mask = self.__get_bits_inbetween(smaller_idx, larger_idx)
        
        if piece_type == Pieces.W_PAWN or piece_type == Pieces.B_PAWN:
            return np.bitwise_and(interval_bits_mask, source_pos_attack_mask)
        return np.bitwise_and(interval_bits_mask, np.bitwise_and(source_pos_attack_mask, target_pos_attack_mask))

    def __rook_attacks64_dynamic(self, curr_piece_pos64, blocked_attack_paths64):
        flag_func = (lambda blocked_attack_paths64, shift_dir_func: 
                     lambda attacks64, shift_len, blocked_attack_paths64, shift_dir_func: 
                     np.bitwise_and(shift_dir_func(attacks64, np.uint(shift_len)), blocked_attack_paths64) == 0)
    
        file_attacks_left = self.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                                           shift_len=self.__FILE_STRIDE,
                                                           flag_func=flag_func(blocked_attack_paths64=blocked_attack_paths64,
                                                                               shift_dir_func=np.left_shift),
                                                           shift_func=self.helper.__bit_shift_func_delegator(np.left_shift))
        
        file_attacks_right = self.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                                            shift_len=self.__FILE_STRIDE,
                                                            flag_func=lambda mask, shift_len: {np.bitwise_and(np.left_shift(mask, np.uint(shift_len)), 
                                                                                                             blocked_attack_paths64) == 0},
                                                            shift_func=self.helper__bit_shift_func_delegator(np.right_shift))
        
        
        rank_attacks_top = self.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                               shift_len=self.__RANK_STRIDE_EQ,
                               flag_func=lambda mask, shift_len: {np.bitwise_and(np.left_shift(mask, np.uint(shift_len)), 
                                                                                 blocked_attack_paths64) == 0},
                               shift_func=self.helper__bit_shift_func_delegator(np.left_shift))
        
        rank_attacks_bottom = self.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                  shift_len=self.__RANK_STRIDE_EQ,
                                  flag_func=lambda mask, shift_len: {np.bitwise_and(np.left_shift(mask, np.uint(shift_len)), 
                                                                                 blocked_attack_paths64) == 0},
                                  shift_func=self.helper__bit_shift_func_delegator(np.left_shift))

        return np.bitwise_or(np.bitwise_or(file_attacks_left, file_attacks_right),
                             np.bitwise_or(rank_attacks_top, rank_attacks_bottom))
    
    def queen_path_blocked_attack_mask(self, piece_position_mask, unblocked_attack_mask):
        unblocked_rook = np.bitwise_and(self.get_attack_mask_of_type(None, Pieces.ROOK, pos_mask=piece_position_mask)[0],
                                        unblocked_attack_mask)
        unblocked_bishop = np.bitwise_and(self.get_attack_mask_of_type(None, Pieces.BISHOP, pos_mask=piece_position_mask)[0],
                                          unblocked_attack_mask)
        return np.bitwise_or(self.bishop_path_blocked_attack_mask(piece_position_mask, unblocked_bishop), 
                             self.__rook_attacks64_dynamic(piece_position_mask, unblocked_rook))
    
    def bishop_path_blocked_attack_mask(self, piece_position_mask, unblocked_attack_mask) -> np.ulonglong:
        larger_stride = 9
        smaller_stride = 7
        org_piece_position_mask = piece_position_mask
        north_east_diagonal_mask = piece_position_mask
        north_west_diagonal_mask = piece_position_mask
        south_east_diagonal_mask = piece_position_mask
        south_west_diagonal_mask = piece_position_mask
        
        while np.bitwise_and(np.left_shift(piece_position_mask, np.uint(smaller_stride)), unblocked_attack_mask) > 0:
            piece_position_mask = np.left_shift(piece_position_mask, np.uint(smaller_stride))
            north_east_diagonal_mask = np.bitwise_or(north_east_diagonal_mask, piece_position_mask)
        
        piece_position_mask = org_piece_position_mask
        while np.bitwise_and(np.left_shift(piece_position_mask, np.uint(larger_stride)), unblocked_attack_mask) > 0:
            piece_position_mask = np.left_shift(piece_position_mask, np.uint(larger_stride))
            north_west_diagonal_mask = np.bitwise_or(north_west_diagonal_mask, piece_position_mask)
        
        piece_position_mask = org_piece_position_mask
        while np.bitwise_and(np.right_shift(piece_position_mask, np.uint(smaller_stride)), unblocked_attack_mask) > 0:
            piece_position_mask = np.right_shift(piece_position_mask, np.uint(smaller_stride))
            south_west_diagonal_mask = np.bitwise_or(south_west_diagonal_mask, piece_position_mask)
        
        piece_position_mask = org_piece_position_mask
        while np.bitwise_and(np.right_shift(piece_position_mask, np.uint(larger_stride)), unblocked_attack_mask) > 0:
            piece_position_mask = np.right_shift(piece_position_mask, np.uint(larger_stride))
            south_east_diagonal_mask = np.bitwise_or(south_east_diagonal_mask, piece_position_mask)
        
        return np.bitwise_xor(np.bitwise_or(np.bitwise_or(north_east_diagonal_mask,
                                                          north_west_diagonal_mask), 
                                            np.bitwise_or(south_east_diagonal_mask,
                                                          south_west_diagonal_mask)),
                              org_piece_position_mask)

    def __pawn_movements64_static(self, curr_piece_pos64, color) -> np.ulonglong:
        if color:
            if np.bitwise_and(curr_piece_pos64, self.__W_EN_PASSANT_MASK) > 0:
                
                return np.bitwise_or(np.left_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ)), 
                                     np.left_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ * 2)))   
            
            return np.left_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ))
        
        if np.bitwise_and(curr_piece_pos64, self.__B_EN_PASSANT_MASK) > 0:
            
            return np.bitwise_or(np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ)), 
                                 np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ * 2)))
        
        return np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ))
    
    def __pawn_attacks64_static(self, current_piece_pos64, color) -> np.ulonglong:
        if color:
            if np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_TOP) > 0:
                return np.ulonglong(0)
            elif np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_LEFT) > 0:
                return np.left_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))
            elif np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_RIGHT) > 0:
                return np.left_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_LONG))
            
            return np.bitwise_or(np.left_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_LONG)), 
                                 np.left_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT)))
        
        if np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_BOTTOM) > 0:
            return np.ulonglong(0)
        elif np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_LEFT) > 0:
            return np.right_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_LONG))
        elif np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_RIGHT) > 0:
            return np.right_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))
        
        return np.bitwise_or(np.right_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_LONG)), 
                             np.right_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT)))
    
    def __rook_attacks64_static(self, curr_piece_pos64) -> np.ulonglong:  
        file_attacks_left = self.helper.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                                           shift_len=self.__FILE_STRIDE,
                                                           flag_func=self.helper.__attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                 compared_const=self.__EDGE_MASK_LEFT),
                                                           shift_func=self.helper.__bit_shift_func_delegator(np.left_shift))
        
        file_attacks_right = self.helper.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                                            shift_len=self.__FILE_STRIDE,
                                                            flag_func=self.helper.__attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                  compared_const=self.__EDGE_MASK_RIGHT),
                                                            shift_func=self.helper.__bit_shift_func_delegator(np.right_shift))
         
        rank_attacks_up = self.helper.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                                           shift_len=self.__RANK_STRIDE_EQ,
                                                           flag_func=self.helper.__attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                 compared_const=self.__EDGE_MASK_TOP),
                                                           shift_func=self.helper.__bit_shift_func_delegator(np.left_shift))
        
        rank_attacks_down = self.helper.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                                             shift_len=self.__RANK_STRIDE_EQ,
                                                             flag_func=self.helper.__attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                   compared_const=self.__EDGE_MASK_BOTTOM),
                                                             shift_func=self.helper.__bit_shift_func_delegator(np.right_shift))
        
        return np.bitwise_or(np.bitwise_or(file_attacks_left, file_attacks_right),
                             np.bitwise_or(rank_attacks_up, rank_attacks_down))      
    
    def __bishop_attacks64_static(self, curr_piece_pos64) -> np.ulonglong:
        north_east_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_SHORT,
                                                                        flag_func=self.helper.__attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                           compared_const=np.bitwise_or(self.__EDGE_MASK_TOP,
                                                                                                                                                        self.__EDGE_MASK_RIGHT)),
                                                                        shift_func=self.helper.__bit_shift_func_delegator(np.left_shift))
        
        north_west_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_LONG,
                                                                        flag_func=self.helper.__attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                           compared_const=np.bitwise_or(self.__EDGE_MASK_TOP,
                                                                                                                                                        self.__EDGE_MASK_LEFT)),
                                                                        shift_func=self.helper.__bit_shift_func_delegator(np.left_shift))
        
        south_east_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_LONG,
                                                                        flag_func=self.helper.__attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                           compared_const=np.bitwise_or(self.__EDGE_MASK_BOTTOM,
                                                                                                                                                        self.__EDGE_MASK_RIGHT)),
                                                                        shift_func=self.helper.__bit_shift_func_delegator(np.right_shift))
        
        south_west_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos_mask=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_LONG,
                                                                        flag_func=self.helper.__attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                           compared_const=np.bitwise_or(self.__EDGE_MASK_BOTTOM,
                                                                                                                                                        self.__EDGE_MASK_RIGHT)),
                                                                        shift_func=self.helper.__bit_shift_func_delegator(np.right_shift))
        
        return np.bitwise_or(np.bitwise_or(north_east_diagonal_attacks, north_west_diagonal_attacks),
                             np.bitwise_or(south_east_diagonal_attacks, south_west_diagonal_attacks))
    
    def __knight_attack_mask(self, piece_position_mask) -> np.ulonglong:
        stride_count = 3
        file_stride = 1
        rank_stride = 8
        west_file_attack_mask = np.ulonglong(0)
        east_file_attack_mask = np.ulonglong(0)
        north_rank_attack_mask = np.ulonglong(0)
        south_rank_attack_mask = np.ulonglong(0)
        
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_LEFT) == 0:
            west_file_attack_mask = piece_position_mask
            
            for i in range(stride_count):
                west_file_attack_mask = np.left_shift(west_file_attack_mask, np.uint(file_stride))
                
                if np.bitwise_and(west_file_attack_mask, self.__EDGE_MASK_LEFT) != 0 and i < stride_count - 1:
                    west_file_attack_mask = np.ulonglong(0)
                    break     
                if i == stride_count - 1:
                    west_file_attack_mask = self.__assign_knight_file_mask(west_file_attack_mask)
        
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_RIGHT) == 0:
            east_file_attack_mask = piece_position_mask
            
            for i in range(stride_count):
                east_file_attack_mask = np.right_shift(east_file_attack_mask, np.uint(file_stride))
                
                if np.bitwise_and(east_file_attack_mask, self.__EDGE_MASK_RIGHT) != 0 and i < stride_count - 1:
                    east_file_attack_mask = np.ulonglong(0)
                    break     
                if i == stride_count - 1:
                    east_file_attack_mask = self.__assign_knight_file_mask(east_file_attack_mask)    
        
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_TOP) == 0:
            north_rank_attack_mask = piece_position_mask
            
            for i in range(stride_count):
                north_rank_attack_mask = np.left_shift(north_rank_attack_mask, np.uint(rank_stride))
                
                if np.bitwise_and(north_rank_attack_mask, self.__EDGE_MASK_TOP) != 0 and i < stride_count - 1:
                    north_rank_attack_mask = np.ulonglong(0)
                    break     
                if i == stride_count - 1:
                    north_rank_attack_mask = self.__assign_knight_rank_mask(north_rank_attack_mask)
        
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_BOTTOM) == 0:
            south_rank_attack_mask = piece_position_mask
            
            for i in range(stride_count):
                south_rank_attack_mask = np.right_shift(south_rank_attack_mask, np.uint(rank_stride))
                
                if np.bitwise_and(south_rank_attack_mask, self.__EDGE_MASK_BOTTOM) != 0 and i < stride_count - 1:
                    south_rank_attack_mask = np.ulonglong(0)
                    break     
                if i == stride_count - 1:
                    south_rank_attack_mask = self.__assign_knight_rank_mask(south_rank_attack_mask)
                    
        return np.bitwise_or(np.bitwise_or(west_file_attack_mask, east_file_attack_mask),
                             np.bitwise_or(north_rank_attack_mask, south_rank_attack_mask))
    
    def __queen_attacks64_static(self, piece_position_mask) -> np.ulonglong:
        return np.bitwise_or(self.__rook_attacks64_static(piece_position_mask), 
                             self.__bishop_attack_mask(piece_position_mask))
    
    def __king_attacks64_static(self, curr_piece_pos64) -> np.ulonglong:
        if np.bitwise_and(curr_piece_pos64, self.__EDGE_MASK_LEFT) == 0:
            file_attack_left = np.left_shift(curr_piece_pos64, np.uint(self.__FILE_STRIDE))
        if np.bitwise_and(curr_piece_pos64, self.__EDGE_MASK_RIGHT) == 0:
            file_attack_right = np.right_shift(curr_piece_pos64, np.uint(self.__FILE_STRIDE))      
        if np.bitwise_and(curr_piece_pos64, self.__EDGE_MASK_TOP) == 0:
            rank_attack_top = np.left_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ))
        if np.bitwise_and(curr_piece_pos64, self.__EDGE_MASK_BOTTOM) == 0:
            rank_attack_bottom = np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ))
        
        if np.bitwise_and(curr_piece_pos64, np.bitwise_or(self.__EDGE_MASK_TOP, self.__EDGE_MASK_RIGHT)) == 0:
            north_east_diagonal_attack = np.left_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))
        if np.bitwise_and(curr_piece_pos64, np.bitwise_or(self.__EDGE_MASK_TOP, self.__EDGE_MASK_LEFT)) == 0:
            north_west_diagonal_attack = np.left_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_LONG)) 
        if np.bitwise_and(curr_piece_pos64, np.bitwise_or(self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_LEFT)) == 0:
            south_west_diagonal_attack = np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))
        if np.bitwise_and(curr_piece_pos64, np.bitwise_or(self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_RIGHT)) == 0:
            south_east_diagonal_attack = np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_LONG))

        return np.bitwise_or(np.bitwise_or(np.bitwise_or(file_attack_left, file_attack_right),
                                           np.bitwise_or(rank_attack_top, rank_attack_bottom)),
                             np.bitwise_or(np.bitwise_or(north_east_diagonal_attack, south_east_diagonal_attack),
                                           np.bitwise_or(north_west_diagonal_attack, south_west_diagonal_attack)))

    