import numpy as np
import operator
from static.pieces import Pieces

class BitboardStorageHelper:
    def conditional_bit_shift(self, 
                              curr_piece_pos64,
                              shift_len,
                              flag_func,
                              shift_func,
                              dynamic_edges=False,
                              all_edges_mask=None):
            
            original_bit = curr_piece_pos64
            mask_to_update = curr_piece_pos64
            
            while flag_func(curr_piece_pos64):
                curr_piece_pos64 = shift_func(curr_piece_pos64, shift_len)
                mask_to_update = np.bitwise_or(mask_to_update, curr_piece_pos64)
            
            if dynamic_edges and np.bitwise_and(curr_piece_pos64, all_edges_mask) == 0:
                curr_piece_pos64 = shift_func(curr_piece_pos64, shift_len)
                mask_to_update = np.bitwise_or(mask_to_update, curr_piece_pos64)
            
            return np.bitwise_xor(mask_to_update, original_bit)

    def get_bits_inbetween(self, smaller_idx, larger_idx) -> np.ulonglong:
            bits_in_between = np.ulonglong(0b1)
            diff = larger_idx - smaller_idx
            
            for i in range(diff):
                bits_in_between = np.bitwise_or(bits_in_between, np.left_shift(bits_in_between, np.uint(1)))
            
            return np.left_shift(bits_in_between, np.uint(smaller_idx))
    
    def bit_shift_func_delegator(self, bit_shift_func):
         return lambda attacks64, shift_len: bit_shift_func(attacks64, np.uint(shift_len))
    
    def attacks64_flag_func_delegator(self, op, compared_const):
        return lambda value_to_compare: op(np.bitwise_and(value_to_compare, compared_const), 0)
    
    def attacks64_dynamic_flag_func_delegator(self, op, compared_const, shift_dir_func, shift_len):
        return lambda value_to_compare: op(np.bitwise_and(shift_dir_func(value_to_compare, np.uint(shift_len)), compared_const), 0)   
    
    def get_piece_position64(self, square_idx) -> np.ulonglong:
        return np.ulonglong(1 << square_idx)