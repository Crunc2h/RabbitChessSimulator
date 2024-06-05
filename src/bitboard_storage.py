import numpy as np
import operator
from static.pieces import Pieces


class BitboardMasks:
    
    def get_all_piece_positions64_from_idx(self):
        return self.__all_piece_positions64_from_idx
    
    def get_all_piece_positions64_to_idx(self):
        return self.__all_piece_positions64_to_idx
    
    def get_all_adj_squares64_of_idx(self):
        return self.__all_adj_squares64_of_idx
    
    def get_all_attacks64_static(self):
        return self.__all_attacks64_static
    
    def get_all_piece_paths64_static(self):
        return self.__all_piece_paths64_static
    
    def rook_attacks64_dynamic(self, curr_piece_pos64, unblocked_attack_paths64) -> np.ulonglong:
        file_attacks_left = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                              shift_len=self.__FILE_STRIDE,
                                                              flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                          compared_const=unblocked_attack_paths64,
                                                                                                                          shift_dir_func=np.left_shift,
                                                                                                                          shift_len=self.__FILE_STRIDE),
                                                              shift_func=self.helper.bit_shift_func_delegator(np.left_shift),
                                                              dynamic_edges=True,
                                                                all_edges_mask=self.__EDGE_MASK_OMNI)
        
        file_attacks_right = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                               shift_len=self.__FILE_STRIDE,
                                                               flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                           compared_const=unblocked_attack_paths64,
                                                                                                                           shift_dir_func=np.right_shift,
                                                                                                                           shift_len=self.__FILE_STRIDE),
                                                               shift_func=self.helper.bit_shift_func_delegator(np.right_shift),
                                                               dynamic_edges=True,
                                                                all_edges_mask=self.__EDGE_MASK_OMNI)
        
        rank_attacks_top = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                             shift_len=self.__RANK_STRIDE_EQ,
                                                             flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                         compared_const=unblocked_attack_paths64,
                                                                                                                         shift_dir_func=np.left_shift,
                                                                                                                         shift_len=self.__RANK_STRIDE_EQ),
                                                             shift_func=self.helper.bit_shift_func_delegator(np.left_shift),
                                                             dynamic_edges=True,
                                                             all_edges_mask=self.__EDGE_MASK_OMNI)
        
        rank_attacks_bottom = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                                shift_len=self.__RANK_STRIDE_EQ,
                                                                flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                            compared_const=unblocked_attack_paths64,
                                                                                                                            shift_dir_func=np.right_shift,
                                                                                                                            shift_len=self.__RANK_STRIDE_EQ),
                                                                shift_func=self.helper.bit_shift_func_delegator(np.right_shift),
                                                                dynamic_edges=True,
                                                                all_edges_mask=self.__EDGE_MASK_OMNI)

        return np.bitwise_or(np.bitwise_or(file_attacks_left, file_attacks_right),
                             np.bitwise_or(rank_attacks_top, rank_attacks_bottom))
    
    def bishop_attacks64_dynamic(self, curr_piece_pos64, unblocked_attack_paths64) -> np.ulonglong:
        north_east_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_SHORT,
                                                                        flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                                    compared_const=unblocked_attack_paths64,
                                                                                                                                    shift_dir_func=np.left_shift,
                                                                                                                                    shift_len=self.__RANK_STRIDE_SHORT),
                                                                        shift_func=self.helper.bit_shift_func_delegator(np.left_shift),
                                                                        dynamic_edges=True,
                                                                        all_edges_mask=self.__EDGE_MASK_OMNI)
        
        north_west_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_LONG,
                                                                        flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                                    compared_const=unblocked_attack_paths64,
                                                                                                                                    shift_dir_func=np.left_shift,
                                                                                                                                    shift_len=self.__RANK_STRIDE_LONG),
                                                                        shift_func=self.helper.bit_shift_func_delegator(np.left_shift),
                                                                        dynamic_edges=True,
                                                                        all_edges_mask=self.__EDGE_MASK_OMNI)
        

        south_east_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_LONG,
                                                                        flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                                    compared_const=unblocked_attack_paths64,
                                                                                                                                    shift_dir_func=np.right_shift,
                                                                                                                                    shift_len=self.__RANK_STRIDE_LONG),
                                                                        shift_func=self.helper.bit_shift_func_delegator(np.right_shift),
                                                                        dynamic_edges=True,
                                                                        all_edges_mask=self.__EDGE_MASK_OMNI)
        

        south_west_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_SHORT,
                                                                        flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                                    compared_const=unblocked_attack_paths64,
                                                                                                                                    shift_dir_func=np.right_shift,
                                                                                                                                    shift_len=self.__RANK_STRIDE_SHORT),
                                                                        shift_func=self.helper.bit_shift_func_delegator(np.right_shift),
                                                                        dynamic_edges=True,
                                                                        all_edges_mask=self.__EDGE_MASK_OMNI)
        
        return np.bitwise_or(np.bitwise_or(north_east_diagonal_attacks, north_west_diagonal_attacks),
                             np.bitwise_or(south_east_diagonal_attacks, south_west_diagonal_attacks))

    def queen_attacks64_dynamic(self, curr_piece_pos64, unblocked_attack_paths64):
        unblocked_rook_paths64 = np.bitwise_and(self.__rook_attacks64_static(curr_piece_pos64), unblocked_attack_paths64)
        unblocked_bishop_paths64 = np.bitwise_and(self.__bishop_attacks64_static(curr_piece_pos64), unblocked_attack_paths64)
        
        return np.bitwise_or(self.bishop_attacks64_dynamic(curr_piece_pos64, unblocked_bishop_paths64), 
                             self.rook_attacks64_dynamic(curr_piece_pos64, unblocked_rook_paths64))
    
    def __init__(self, helper_obj):
        self.helper = helper_obj
        
        self.__EDGE_MASK_TOP = np.ulonglong(0b11111111 << 56)
        self.__EDGE_MASK_BOTTOM = np.ulonglong(0b11111111)
        self.__EDGE_MASK_LEFT = np.ulonglong(0b1000000010000000100000001000000010000000100000001000000010000000)
        self.__EDGE_MASK_RIGHT = np.ulonglong(0b0000000100000001000000010000000100000001000000010000000100000001)
        self.__EDGE_MASK_OMNI = np.bitwise_or.reduce([self.__EDGE_MASK_TOP, self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_LEFT, self.__EDGE_MASK_RIGHT])
        self.__W_EN_PASSANT_MASK = np.ulonglong(0b1111111100000000)
        self.__B_EN_PASSANT_MASK = np.ulonglong(0b0000000011111111 << 48)
        
        self.__RANK_STRIDE_LONG = 9
        self.__RANK_STRIDE_EQ = 8
        self.__RANK_STRIDE_SHORT = 7
        self.__FILE_STRIDE = 1
        
        self.__all_piece_positions64_from_idx = {}
        self.__all_piece_positions64_to_idx = {}
        self.__all_adj_squares64_of_idx = {}
        for i in range(64):
            self.__all_piece_positions64_from_idx[i] = self.helper.get_piece_position64(i)
            self.__all_piece_positions64_to_idx[self.__all_piece_positions64_from_idx[i]] = i
            self.__all_adj_squares64_of_idx[i] = self.__king_attacks64_static(self.__all_piece_positions64_from_idx[i])
        
        self.__all_attacks64_static = self.__construct_all_attacks64()
        self.__all_piece_paths64_static = self.__construct_all_paths64()
        
    def __construct_all_attacks64(self) -> dict:
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
                curr_piece_pos64 = self.helper.get_piece_position64(i)
                if key != Pieces.W_PAWN and key != Pieces.B_PAWN:
                    all_attack_masks[key][curr_piece_pos64] = self.__piece_type_to_piece_attacks64(key, curr_piece_pos64)
                else:
                    pawn_attacks64, pawn_movements64 = self.__piece_type_to_piece_attacks64(key, curr_piece_pos64)
                   
                    all_attack_masks[key]["move"][curr_piece_pos64] = pawn_movements64
                    all_attack_masks[key]["attack"][curr_piece_pos64] = pawn_attacks64 
     
        return all_attack_masks
    
    def __construct_all_paths64(self) -> dict:
        all_path_masks = {
            Pieces.W_PAWN:{},
            Pieces.B_PAWN:{},
            Pieces.ROOK:{},
            Pieces.BISHOP:{},
        }
        
        for key in all_path_masks.keys():
            for i in range(64):
                curr_piece_pos64 = self.__all_piece_positions64_from_idx[i]
                if key == Pieces.W_PAWN or key == Pieces.B_PAWN:
                    curr_sqr_piece_attacks64 = self.__piece_type_to_piece_attacks64(key, curr_piece_pos64)[1]
                else:
                    curr_sqr_piece_attacks64 = self.__piece_type_to_piece_attacks64(key, curr_piece_pos64)
                
                for f in range(64):

                    target_sqr_piece_pos64 = self.__all_piece_positions64_from_idx[f]
                    
                    if np.bitwise_and(curr_sqr_piece_attacks64, target_sqr_piece_pos64) == 0:
                        continue
                    
                    target_sqr_piece_attacks64 = self.__piece_type_to_piece_attacks64(key, target_sqr_piece_pos64)
                    all_path_masks[key][(i, f)] = self.__piece_path64_static(i, f, curr_sqr_piece_attacks64, target_sqr_piece_attacks64, key)
        
        all_path_masks[Pieces.QUEEN] = {}
        all_path_masks[Pieces.QUEEN].update(all_path_masks[Pieces.BISHOP])
        all_path_masks[Pieces.QUEEN].update(all_path_masks[Pieces.ROOK])
        
        return all_path_masks   

    def __piece_type_to_piece_attacks64(self, piece_type, curr_piece_pos64):
        if piece_type == Pieces.W_PAWN:
            return self.__pawn_attacks64_static(curr_piece_pos64, True), self.__pawn_movements64_static(curr_piece_pos64, True)
        elif piece_type == Pieces.B_PAWN:
            return self.__pawn_attacks64_static(curr_piece_pos64, False), self.__pawn_movements64_static(curr_piece_pos64, False)
        elif piece_type == Pieces.ROOK:
            return self.__rook_attacks64_static(curr_piece_pos64)
        elif piece_type == Pieces.KNIGHT:
            return self.__knight_attacks64_static(curr_piece_pos64)
        elif piece_type == Pieces.BISHOP:
            return self.__bishop_attacks64_static(curr_piece_pos64)
        elif piece_type == Pieces.QUEEN:
            return self.__queen_attacks64_static(curr_piece_pos64)
        elif piece_type == Pieces.KING:
            return self.__king_attacks64_static(curr_piece_pos64)
        raise ValueError("Invalid piece type passed to the mask getter!") 
    
    def __piece_path64_static(self,
                              curr_piece_pos_idx,
                              target_piece_pos_idx, 
                              curr_piece_attacks64, 
                              target_piece_attacks64, 
                              piece_type) -> np.ulonglong:
        
        if curr_piece_pos_idx > target_piece_pos_idx: larger_idx, smaller_idx = curr_piece_pos_idx, target_piece_pos_idx
        else: larger_idx, smaller_idx = target_piece_pos_idx, curr_piece_pos_idx
        interval_bits_mask = self.helper.get_bits_inbetween(smaller_idx, larger_idx)
        
        if piece_type == Pieces.W_PAWN or piece_type == Pieces.B_PAWN:
            return np.bitwise_and(interval_bits_mask, curr_piece_attacks64)
        return np.bitwise_and(interval_bits_mask, np.bitwise_and(curr_piece_attacks64, target_piece_attacks64))

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
                return np.left_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))
            
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
        file_attacks_left = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                              shift_len=self.__FILE_STRIDE,
                                                              flag_func=self.helper.attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                 compared_const=self.__EDGE_MASK_LEFT),
                                                              shift_func=self.helper.bit_shift_func_delegator(np.left_shift))
        
        file_attacks_right = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                               shift_len=self.__FILE_STRIDE,
                                                               flag_func=self.helper.attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                  compared_const=self.__EDGE_MASK_RIGHT),
                                                               shift_func=self.helper.bit_shift_func_delegator(np.right_shift))
         
        rank_attacks_up = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                            shift_len=self.__RANK_STRIDE_EQ,
                                                            flag_func=self.helper.attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                 compared_const=self.__EDGE_MASK_TOP),
                                                            shift_func=self.helper.bit_shift_func_delegator(np.left_shift))
        
        rank_attacks_down = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                              shift_len=self.__RANK_STRIDE_EQ,
                                                              flag_func=self.helper.attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                   compared_const=self.__EDGE_MASK_BOTTOM),
                                                              shift_func=self.helper.bit_shift_func_delegator(np.right_shift))
        
        return np.bitwise_or(np.bitwise_or(file_attacks_left, file_attacks_right),
                             np.bitwise_or(rank_attacks_up, rank_attacks_down))      
    
    def __bishop_attacks64_static(self, curr_piece_pos64) -> np.ulonglong:
        north_east_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_SHORT,
                                                                        flag_func=self.helper.attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                           compared_const=np.bitwise_or(self.__EDGE_MASK_TOP,
                                                                                                                                                        self.__EDGE_MASK_RIGHT)),
                                                                        shift_func=self.helper.bit_shift_func_delegator(np.left_shift))
        
        north_west_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_LONG,
                                                                        flag_func=self.helper.attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                           compared_const=np.bitwise_or(self.__EDGE_MASK_TOP,
                                                                                                                                                        self.__EDGE_MASK_LEFT)),
                                                                        shift_func=self.helper.bit_shift_func_delegator(np.left_shift))
        
        south_east_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_LONG,
                                                                        flag_func=self.helper.attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                           compared_const=np.bitwise_or(self.__EDGE_MASK_BOTTOM,
                                                                                                                                                        self.__EDGE_MASK_RIGHT)),
                                                                        shift_func=self.helper.bit_shift_func_delegator(np.right_shift))
        
        south_west_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                                        shift_len=self.__RANK_STRIDE_SHORT,
                                                                        flag_func=self.helper.attacks64_flag_func_delegator(op=operator.eq,
                                                                                                                           compared_const=np.bitwise_or(self.__EDGE_MASK_BOTTOM,
                                                                                                                                                        self.__EDGE_MASK_LEFT)),
                                                                        shift_func=self.helper.bit_shift_func_delegator(np.right_shift))
        
        return np.bitwise_or(np.bitwise_or(north_east_diagonal_attacks, north_west_diagonal_attacks),
                             np.bitwise_or(south_east_diagonal_attacks, south_west_diagonal_attacks))
    
    def __knight_attacks64_static(self, curr_piece_pos64) -> np.ulonglong: 
        west_file_attack_mask = self.__stride_for_knight_attacks64_static(curr_piece_pos64=curr_piece_pos64,
                                                    edge_mask64=self.__EDGE_MASK_LEFT,
                                                    shift_func=np.left_shift,
                                                    shift_len=self.__FILE_STRIDE,
                                                    file_or_rank=True)

        east_file_attack_mask = self.__stride_for_knight_attacks64_static(curr_piece_pos64=curr_piece_pos64,
                                                    edge_mask64=self.__EDGE_MASK_RIGHT,
                                                    shift_func=np.right_shift,
                                                    shift_len=self.__FILE_STRIDE,
                                                    file_or_rank=True)
        
        north_rank_attack_mask = self.__stride_for_knight_attacks64_static(curr_piece_pos64=curr_piece_pos64,
                                                    edge_mask64=self.__EDGE_MASK_TOP,
                                                    shift_func=np.left_shift,
                                                    shift_len=self.__RANK_STRIDE_EQ,
                                                    file_or_rank=False)

        south_rank_attack_mask = self.__stride_for_knight_attacks64_static(curr_piece_pos64=curr_piece_pos64,
                                                    edge_mask64=self.__EDGE_MASK_BOTTOM,
                                                    shift_func=np.right_shift,
                                                    shift_len=self.__RANK_STRIDE_EQ,
                                                    file_or_rank=False)

        west_file_attack_mask = np.ulonglong(0) if west_file_attack_mask == None else west_file_attack_mask
        east_file_attack_mask = np.ulonglong(0) if east_file_attack_mask == None else east_file_attack_mask
        north_rank_attack_mask = np.ulonglong(0) if north_rank_attack_mask == None else north_rank_attack_mask
        south_rank_attack_mask = np.ulonglong(0) if south_rank_attack_mask == None else south_rank_attack_mask
             
        return np.bitwise_or(np.bitwise_or(west_file_attack_mask, east_file_attack_mask),
                             np.bitwise_or(north_rank_attack_mask, south_rank_attack_mask))
    
    def __stride_for_knight_attacks64_static(self,
                       curr_piece_pos64,
                       edge_mask64,
                       shift_func,
                       shift_len,
                       file_or_rank,
                       knight_stride_range=2):
        if np.bitwise_and(curr_piece_pos64, edge_mask64) == 0:
            attacks64 = curr_piece_pos64
        
            for i in range(knight_stride_range):
                attacks64 = shift_func(attacks64, np.uint(shift_len))
        
                if np.bitwise_and(attacks64, edge_mask64) > 0 and i < knight_stride_range - 1:
                    attacks64 = np.ulonglong(0)
                    break     
                if i == knight_stride_range - 1:              
                    if file_or_rank:
                        
                        assigned_attacks64 = self.__assign_adjacent_knight_attacks64_static(attacks64,
                                                                              edge_mask64_pos=self.__EDGE_MASK_TOP,
                                                                              edge_mask64_neg=self.__EDGE_MASK_BOTTOM,
                                                                              shift_len=self.__RANK_STRIDE_EQ)
                    else:
                        assigned_attacks64 = self.__assign_adjacent_knight_attacks64_static(attacks64,
                                                                                  edge_mask64_pos=self.__EDGE_MASK_LEFT,
                                                                                  edge_mask64_neg=self.__EDGE_MASK_RIGHT,
                                                                                              shift_len=self.__FILE_STRIDE)
                    return assigned_attacks64
    
    def __assign_adjacent_knight_attacks64_static(self, 
                                                  attacks64,
                                                  shift_len,
                                                  edge_mask64_pos,
                                                  edge_mask64_neg) -> np.ulonglong: 
        
        if np.bitwise_and(attacks64, np.bitwise_or(edge_mask64_pos, edge_mask64_neg)) == 0:
            attacks64 = np.bitwise_or(np.left_shift(attacks64, np.uint(shift_len)),
                                          np.right_shift(attacks64, np.uint(shift_len)))
            return attacks64
        elif np.bitwise_and(attacks64, edge_mask64_pos) == 0:
            attacks64 = np.left_shift(attacks64, np.uint(shift_len))
            return attacks64
        attacks64 = np.right_shift(attacks64, np.uint(shift_len))
        return attacks64
    
    def __queen_attacks64_static(self, curr_piece_pos64) -> np.ulonglong:
        return np.bitwise_or(self.__rook_attacks64_static(curr_piece_pos64), 
                             self.__bishop_attacks64_static(curr_piece_pos64))
    
    def __king_attacks64_static(self, curr_piece_pos64) -> np.ulonglong:
        file_attack_left, file_attack_right = np.ulonglong(0), np.ulonglong(0)
        rank_attack_top, rank_attack_bottom = np.ulonglong(0), np.ulonglong(0)
        north_east_diagonal_attack, north_west_diagonal_attack = np.ulonglong(0), np.ulonglong(0)
        south_east_diagonal_attack, south_west_diagonal_attack = np.ulonglong(0), np.ulonglong(0) 
        
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
            north_west_diagonal_attack = np.left_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT)) 
        if np.bitwise_and(curr_piece_pos64, np.bitwise_or(self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_LEFT)) == 0:
            south_west_diagonal_attack = np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))
        if np.bitwise_and(curr_piece_pos64, np.bitwise_or(self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_RIGHT)) == 0:
            south_east_diagonal_attack = np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))

        return np.bitwise_or(np.bitwise_or(np.bitwise_or(file_attack_left, file_attack_right),
                                           np.bitwise_or(rank_attack_top, rank_attack_bottom)),
                             np.bitwise_or(np.bitwise_or(north_east_diagonal_attack, south_east_diagonal_attack),
                                           np.bitwise_or(north_west_diagonal_attack, south_west_diagonal_attack)))

    