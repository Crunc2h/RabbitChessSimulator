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
    
    
    
    def __init__(self, helper_obj):
        self.helper = helper_obj
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
        
        """
        self.all_position_masks = np.array([np.ulonglong(1 << i) for i in range(64)])
        self.__all_attack_masks = self.__construct_all_attack_masks()
        self.__all_path_masks = self.__construct_all_path_masks()
        """
    
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

    def rook_attacks64_dynamic(self, curr_piece_pos64, unblocked_attack_paths64):
        file_attacks_left = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                       shift_len=self.__FILE_STRIDE,
                                                       flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                   compared_const=unblocked_attack_paths64,
                                                                                                                   shift_dir_func=np.left_shift,
                                                                                                                   shift_len=self.__FILE_STRIDE),
                                                       shift_func=self.helper.bit_shift_func_delegator(np.left_shift))
        
        file_attacks_right = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                        shift_len=self.__FILE_STRIDE,
                                                        flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                    compared_const=unblocked_attack_paths64,
                                                                                                                    shift_dir_func=np.right_shift,
                                                                                                                    shift_len=self.__FILE_STRIDE),
                                                        shift_func=self.helper.bit_shift_func_delegator(np.right_shift))
        
        rank_attacks_top = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                      shift_len=self.__RANK_STRIDE_EQ,
                                                      flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                  compared_const=unblocked_attack_paths64,
                                                                                                                  shift_dir_func=np.left_shift,
                                                                                                                  shift_len=self.__RANK_STRIDE_EQ),
                                                      shift_func=self.helper.bit_shift_func_delegator(np.left_shift))
        
        rank_attacks_bottom = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                         shift_len=self.__RANK_STRIDE_EQ,
                                                         flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                     compared_const=unblocked_attack_paths64,
                                                                                                                     shift_dir_func=np.right_shift,
                                                                                                                     shift_len=self.__RANK_STRIDE_EQ),
                                                         shift_func=self.helper.bit_shift_func_delegator(np.right_shift))

        return np.bitwise_or(np.bitwise_or(file_attacks_left, file_attacks_right),
                             np.bitwise_or(rank_attacks_top, rank_attacks_bottom))
    
    def bishop_attacks64_dynamic(self, 
                                 curr_piece_pos64, 
                                 unblocked_attack_paths64) -> np.ulonglong:

        north_east_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                       shift_len=self.__RANK_STRIDE_SHORT,
                                                       flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                   compared_const=unblocked_attack_paths64,
                                                                                                                   shift_dir_func=np.left_shift,
                                                                                                                   shift_len=self.__RANK_STRIDE_SHORT),
                                                       shift_func=self.helper.bit_shift_func_delegator(np.left_shift))
        
        north_west_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                       shift_len=self.__RANK_STRIDE_LONG,
                                                       flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                   compared_const=unblocked_attack_paths64,
                                                                                                                   shift_dir_func=np.left_shift,
                                                                                                                   shift_len=self.__RANK_STRIDE_LONG),
                                                       shift_func=self.helper.bit_shift_func_delegator(np.left_shift))
        

        south_east_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                       shift_len=self.__RANK_STRIDE_LONG,
                                                       flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                   compared_const=unblocked_attack_paths64,
                                                                                                                   shift_dir_func=np.right_shift,
                                                                                                                   shift_len=self.__RANK_STRIDE_LONG),
                                                       shift_func=self.helper.bit_shift_func_delegator(np.right_shift))
        

        south_west_diagonal_attacks = self.helper.conditional_bit_shift(curr_piece_pos64=curr_piece_pos64,
                                                       shift_len=self.__RANK_STRIDE_SHORT,
                                                       flag_func=self.helper.attacks64_dynamic_flag_func_delegator(op=operator.gt,
                                                                                                                   compared_const=unblocked_attack_paths64,
                                                                                                                   shift_dir_func=np.right_shift,
                                                                                                                   shift_len=self.__RANK_STRIDE_SHORT),
                                                       shift_func=self.helper.bit_shift_func_delegator(np.right_shift))
        
        return np.bitwise_or(np.bitwise_or(north_east_diagonal_attacks, north_west_diagonal_attacks),
                             np.bitwise_or(south_east_diagonal_attacks, south_west_diagonal_attacks))

    
    def queen_path_blocked_attack_mask(self, piece_position_mask, unblocked_attack_mask):
        unblocked_rook = np.bitwise_and(self.get_attack_mask_of_type(None, Pieces.ROOK, pos_mask=piece_position_mask)[0],
                                        unblocked_attack_mask)
        unblocked_bishop = np.bitwise_and(self.get_attack_mask_of_type(None, Pieces.BISHOP, pos_mask=piece_position_mask)[0],
                                          unblocked_attack_mask)
        return np.bitwise_or(self.bishop_attacks64_dynamic(piece_position_mask, unblocked_bishop), 
                             self.__rook_attacks64_dynamic(piece_position_mask, unblocked_rook))

    def pawn_movements64_static(self, curr_piece_pos64, color) -> np.ulonglong:
        if color:
            if np.bitwise_and(curr_piece_pos64, self.__W_EN_PASSANT_MASK) > 0:
                
                return np.bitwise_or(np.left_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ)), 
                                     np.left_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ * 2)))   
            
            return np.left_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ))
        
        if np.bitwise_and(curr_piece_pos64, self.__B_EN_PASSANT_MASK) > 0:
            
            return np.bitwise_or(np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ)), 
                                 np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ * 2)))
        
        return np.right_shift(curr_piece_pos64, np.uint(self.__RANK_STRIDE_EQ))
    
    def pawn_attacks64_static(self, current_piece_pos64, color) -> np.ulonglong:
        if color:
            if np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_TOP) > 0:
                return np.ulonglong(0)
            elif np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_LEFT) > 0:
                return np.left_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))
            elif np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_RIGHT) > 0:
                return np.left_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))
            
            return np.bitwise_or(np.left_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT)), 
                                 np.left_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT)))
        
        if np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_BOTTOM) > 0:
            return np.ulonglong(0)
        elif np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_LEFT) > 0:
            return np.right_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))
        elif np.bitwise_and(current_piece_pos64, self.__EDGE_MASK_RIGHT) > 0:
            return np.right_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT))
        
        return np.bitwise_or(np.right_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT)), 
                             np.right_shift(current_piece_pos64, np.uint(self.__RANK_STRIDE_SHORT)))
    
    def rook_attacks64_static(self, curr_piece_pos64) -> np.ulonglong:  
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
    
    def bishop_attacks64_static(self, curr_piece_pos64) -> np.ulonglong:
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
    
    def knight_attacks64_static(self, curr_piece_pos64) -> np.ulonglong:
        west_file_attack_mask = np.ulonglong(0)
        east_file_attack_mask = np.ulonglong(0)
        north_rank_attack_mask = np.ulonglong(0)
        south_rank_attack_mask = np.ulonglong(0)
        
        west_file_attack_mask = self.knight_strider(curr_piece_pos64=curr_piece_pos64,
                                                    edge_mask64=self.__EDGE_MASK_LEFT,
                                                    shift_func=np.left_shift,
                                                    shift_len=self.__FILE_STRIDE,
                                                    file_or_rank=False)
        
        
        east_file_attack_mask = self.knight_strider(curr_piece_pos64=curr_piece_pos64,
                                                    edge_mask64=self.__EDGE_MASK_RIGHT,
                                                    shift_func=np.right_shift,
                                                    shift_len=self.__FILE_STRIDE,
                                                    file_or_rank=False)
        north_rank_attack_mask = self.knight_strider(curr_piece_pos64=curr_piece_pos64,
                                                    edge_mask64=self.__EDGE_MASK_TOP,
                                                    shift_func=np.left_shift,
                                                    shift_len=self.__RANK_STRIDE_EQ,
                                                    file_or_rank=True)
        south_rank_attack_mask = self.knight_strider(curr_piece_pos64=curr_piece_pos64,
                                                    edge_mask64=self.__EDGE_MASK_BOTTOM,
                                                    shift_func=np.right_shift,
                                                    shift_len=self.__RANK_STRIDE_EQ,
                                                    file_or_rank=True)
             
        return np.bitwise_or(np.bitwise_or(west_file_attack_mask, east_file_attack_mask),
                             np.bitwise_or(north_rank_attack_mask, south_rank_attack_mask))
    
    def knight_strider(self,
                       curr_piece_pos64,
                       edge_mask64,
                       shift_func,
                       shift_len,
                       file_or_rank,
                       knight_stride_range=3):
        
        if np.bitwise_and(curr_piece_pos64, edge_mask64) == 0:
            attacks64 = curr_piece_pos64
            
            for i in range(knight_stride_range):
                attacks64 = shift_func(attacks64, np.uint(shift_len))
                
                if np.bitwise_and(attacks64, edge_mask64) > 0 and i < knight_stride_range - 1:
                    attacks64 = np.ulonglong(0)
                    break     
                
                if i == knight_stride_range - 1:
                    from bitboard_printer import BitboardPrinter
                    print("=======before assigning")
                    BitboardPrinter.print(attacks64)
                    
                    
                    if file_or_rank:
                        
                        assigned_attacks64 = self.__assign_knight_attack64_static(attacks64,
                                                                              edge_mask64_pos=self.__EDGE_MASK_TOP,
                                                                              edge_mask64_neg=self.__EDGE_MASK_BOTTOM,
                                                                              shift_len=self.__RANK_STRIDE_EQ)
                        print("=========after assigning file squaress")
                        BitboardPrinter.print(assigned_attacks64)
                    else:
                        assigned_attacks64 = self.__assign_knight_attack64_static(attacks64,
                                                                                              edge_mask64_pos=self.__EDGE_MASK_RIGHT,
                                                                                              edge_mask64_neg=self.__EDGE_MASK_LEFT,
                                                                                              shift_len=self.__RANK_STRIDE_EQ)
                        print("========after assigning rank squares")
                        BitboardPrinter.print(assigned_attacks64)
                    final_attacks64 = np.bitwise_or(assigned_attacks64, attacks64)
        return final_attacks64
    
    
    def __assign_knight_attack64_static(self, 
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






    def queen_attacks64_static(self, piece_position_mask) -> np.ulonglong:
        return np.bitwise_or(self.__rook_attacks64_static(piece_position_mask), 
                             self.__bishop_attack_mask(piece_position_mask))
    
    def king_attacks64_static(self, curr_piece_pos64) -> np.ulonglong:
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

    