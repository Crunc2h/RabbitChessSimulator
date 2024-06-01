import numpy as np


class BitboardMask:
    
    EDGE_MASK_TOP = np.ulonglong(0b11111111 << 56)
    EDGE_MASK_BOTTOM = np.ulonglong(0b11111111)
    EDGE_MASK_LEFT = np.ulonglong(0b1000000010000000100000001000000010000000100000001000000010000000)
    EDGE_MASK_RIGHT = np.ulonglong(0b0000000100000001000000010000000100000001000000010000000100000001)
    WHITE_EN_PASSANT_MASK = np.ulonglong(0b1111111100000000)
    BLACK_EN_PASSANT_MASK = np.ulonglong(0b0000000011111111 << 48)
    
    @staticmethod
    def piece_position_mask(square_idx) -> np.ulonglong:
        return np.ulonglong(1 << square_idx)
    
    @staticmethod
    def pawn_movement_mask(piece_position_mask, side) -> np.ulonglong:
        stride = 8
        if side:
            if np.bitwise_and(piece_position_mask, BitboardMask.WHITE_EN_PASSANT_MASK) > 0:
                return np.bitwise_or(np.left_shift(piece_position_mask, np.uint(stride)), np.left_shift(piece_position_mask, np.uint(stride * 2)))
            return np.left_shift(piece_position_mask, np.uint(stride))
        if np.bitwise_and(piece_position_mask, BitboardMask.BLACK_EN_PASSANT_MASK) > 0:
            return np.bitwise_or(np.right_shift(piece_position_mask, np.uint(stride)), np.right_shift(piece_position_mask, np.uint(stride * 2)))
        return np.right_shift(piece_position_mask, np.uint(stride))
    
    @staticmethod
    def pawn_attack_mask(piece_position_mask, side) -> np.ulonglong:
        larger_stride = 9
        smaller_stride = 7
        
        if side:
            if np.bitwise_and(piece_position_mask, BitboardMask.EDGE_MASK_TOP) > 0:
                return np.ulonglong(0)
            elif np.bitwise_and(piece_position_mask, BitboardMask.EDGE_MASK_LEFT) > 0:
                return np.left_shift(piece_position_mask, np.uint(smaller_stride))
            elif np.bitwise_and(piece_position_mask, BitboardMask.EDGE_MASK_RIGHT) > 0:
                return np.left_shift(piece_position_mask, np.uint(larger_stride))
            return np.bitwise_or(np.left_shift(piece_position_mask, np.uint(larger_stride)), np.left_shift(piece_position_mask, np.uint(smaller_stride)))
        if np.bitwise_and(piece_position_mask, BitboardMask.EDGE_MASK_BOTTOM) > 0:
            return np.ulonglong(0)
        elif np.bitwise_and(piece_position_mask, BitboardMask.EDGE_MASK_LEFT) > 0:
            return np.right_shift(piece_position_mask, np.uint(larger_stride))
        elif np.bitwise_and(piece_position_mask, BitboardMask.EDGE_MASK_RIGHT) > 0:
            return np.right_shift(piece_position_mask, np.uint(smaller_stride))
        return np.bitwise_or(np.right_shift(piece_position_mask, np.uint(larger_stride)), np.right_shift(piece_position_mask, np.uint(smaller_stride)))
    
    @staticmethod
    def rook_attack_mask(piece_position_mask) -> np.ulonglong:
        
        file_attack_mask = piece_position_mask
        file_stride = 1  
        if np.bitwise_and(piece_position_mask, BitboardMask.EDGE_MASK_LEFT) == 0:
            while np.bitwise_and(file_attack_mask, BitboardMask.EDGE_MASK_LEFT) == 0:
                file_attack_mask = np.bitwise_or(file_attack_mask, np.left_shift(file_attack_mask, np.uint(file_stride)))
            file_attack_mask = np.bitwise_xor(file_attack_mask, piece_position_mask)
        if np.bitwise_and(piece_position_mask, BitboardMask.EDGE_MASK_RIGHT) == 0:
            while np.bitwise_and(file_attack_mask, BitboardMask.EDGE_MASK_RIGHT) == 0:
                file_attack_mask = np.bitwise_or(file_attack_mask, np.right_shift(file_attack_mask, np.uint(file_stride)))
            file_attack_mask = np.bitwise_xor(file_attack_mask, piece_position_mask)
        
        rank_attack_mask = piece_position_mask
        rank_stride = 8
        if np.bitwise_and(piece_position_mask, BitboardMask.EDGE_MASK_TOP) == 0:
            while np.bitwise_and(rank_attack_mask, BitboardMask.EDGE_MASK_TOP) == 0:
                rank_attack_mask = np.bitwise_or(rank_attack_mask, np.left_shift(rank_attack_mask, np.uint(rank_stride)))
            rank_attack_mask = np.bitwise_xor(rank_attack_mask, piece_position_mask)
        if np.bitwise_and(piece_position_mask, BitboardMask.EDGE_MASK_BOTTOM) == 0:
            while np.bitwise_and(rank_attack_mask, BitboardMask.EDGE_MASK_BOTTOM) == 0:
                rank_attack_mask = np.bitwise_or(rank_attack_mask, np.right_shift(rank_attack_mask, np.uint(rank_stride)))
            rank_attack_mask = np.bitwise_xor(rank_attack_mask, piece_position_mask)
        
        return np.bitwise_or(file_attack_mask, rank_attack_mask)
    
    @staticmethod
    def bishop_attack_mask(piece_position_mask) -> np.ulonglong:
        larger_stride = 9
        smaller_stride = 7
    




    