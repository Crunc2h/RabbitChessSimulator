import numpy as np


class BitboardMasks:
    
    EDGE_MASK_TOP = np.ulonglong(0b11111111 << 56)
    EDGE_MASK_BOTTOM = np.ulonglong(0b11111111)
    EDGE_MASK_LEFT = np.ulonglong(0b1000000010000000100000001000000010000000100000001000000010000000)
    EDGE_MASK_RIGHT = np.ulonglong(0b0000000100000001000000010000000100000001000000010000000100000001)
    WHITE_EN_PASSANT_MASK = np.ulonglong(0b1111111100000000)
    BLACK_EN_PASSANT_MASK = np.ulonglong(0b0000000011111111 << 48)

    def __init__():
        pass
    
    def piece_position_mask(self, square_idx) -> np.ulonglong:
        return np.ulonglong(1 << square_idx)

    def pawn_movement_mask(self, piece_position_mask, color) -> np.ulonglong:
        stride = 8
        
        if color:
            if np.bitwise_and(piece_position_mask, self.WHITE_EN_PASSANT_MASK) > 0:
                return np.bitwise_or(np.left_shift(piece_position_mask, np.uint(stride)), np.left_shift(piece_position_mask, np.uint(stride * 2)))
            return np.left_shift(piece_position_mask, np.uint(stride))
        if np.bitwise_and(piece_position_mask, self.BLACK_EN_PASSANT_MASK) > 0:
            return np.bitwise_or(np.right_shift(piece_position_mask, np.uint(stride)), np.right_shift(piece_position_mask, np.uint(stride * 2)))
        return np.right_shift(piece_position_mask, np.uint(stride))
    
    def pawn_attack_mask(self, piece_position_mask, side) -> np.ulonglong:
        larger_stride = 9
        smaller_stride = 7
        
        if side:
            if np.bitwise_and(piece_position_mask, self.EDGE_MASK_TOP) > 0:
                return np.ulonglong(0)
            elif np.bitwise_and(piece_position_mask, self.EDGE_MASK_LEFT) > 0:
                return np.left_shift(piece_position_mask, np.uint(smaller_stride))
            elif np.bitwise_and(piece_position_mask, self.EDGE_MASK_RIGHT) > 0:
                return np.left_shift(piece_position_mask, np.uint(larger_stride))
            return np.bitwise_or(np.left_shift(piece_position_mask, np.uint(larger_stride)), np.left_shift(piece_position_mask, np.uint(smaller_stride)))
        
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_BOTTOM) > 0:
            return np.ulonglong(0)
        elif np.bitwise_and(piece_position_mask, self.EDGE_MASK_LEFT) > 0:
            return np.right_shift(piece_position_mask, np.uint(larger_stride))
        elif np.bitwise_and(piece_position_mask, self.EDGE_MASK_RIGHT) > 0:
            return np.right_shift(piece_position_mask, np.uint(smaller_stride))
        return np.bitwise_or(np.right_shift(piece_position_mask, np.uint(larger_stride)), np.right_shift(piece_position_mask, np.uint(smaller_stride)))
    
    def rook_attack_mask(self, piece_position_mask) -> np.ulonglong:
        file_stride = 1 
        rank_stride = 8 
        file_attack_mask = piece_position_mask
        rank_attack_mask = piece_position_mask
        
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_LEFT) == 0:
            while np.bitwise_and(file_attack_mask, self.EDGE_MASK_LEFT) == 0:
                file_attack_mask = np.bitwise_or(file_attack_mask, np.left_shift(file_attack_mask, np.uint(file_stride)))
            file_attack_mask = np.bitwise_xor(file_attack_mask, piece_position_mask)
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_RIGHT) == 0:
            while np.bitwise_and(file_attack_mask, self.EDGE_MASK_RIGHT) == 0:
                file_attack_mask = np.bitwise_or(file_attack_mask, np.right_shift(file_attack_mask, np.uint(file_stride)))
            file_attack_mask = np.bitwise_xor(file_attack_mask, piece_position_mask)
        
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_TOP) == 0:
            while np.bitwise_and(rank_attack_mask, self.EDGE_MASK_TOP) == 0:
                rank_attack_mask = np.bitwise_or(rank_attack_mask, np.left_shift(rank_attack_mask, np.uint(rank_stride)))
            rank_attack_mask = np.bitwise_xor(rank_attack_mask, piece_position_mask)
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_BOTTOM) == 0:
            while np.bitwise_and(rank_attack_mask, self.EDGE_MASK_BOTTOM) == 0:
                rank_attack_mask = np.bitwise_or(rank_attack_mask, np.right_shift(rank_attack_mask, np.uint(rank_stride)))
            rank_attack_mask = np.bitwise_xor(rank_attack_mask, piece_position_mask)
        
        return np.bitwise_or(file_attack_mask, rank_attack_mask)
    
    def bishop_attack_mask(self, piece_position_mask) -> np.ulonglong:
        larger_stride = 9
        smaller_stride = 7
        north_east_diagonal_mask = np.ulonglong(0)
        north_west_diagonal_mask = np.ulonglong(0)
        south_east_diagonal_mask = np.ulonglong(0)
        south_west_diagonal_mask = np.ulonglong(0)
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.EDGE_MASK_TOP, self.EDGE_MASK_RIGHT)) == 0:
            north_east_diagonal_mask = piece_position_mask
            while np.bitwise_and(north_east_diagonal_mask, np.bitwise_or(self.EDGE_MASK_TOP, self.EDGE_MASK_RIGHT)) == 0:
                north_east_diagonal_mask = np.bitwise_or(north_east_diagonal_mask, np.left_shift(north_east_diagonal_mask, np.uint(smaller_stride)))
            north_east_diagonal_mask = np.bitwise_xor(piece_position_mask, north_east_diagonal_mask)

        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.EDGE_MASK_TOP, self.EDGE_MASK_LEFT)) == 0:
            north_west_diagonal_mask = piece_position_mask
            while np.bitwise_and(north_west_diagonal_mask, np.bitwise_or(self.EDGE_MASK_TOP, self.EDGE_MASK_LEFT)) == 0:
                north_west_diagonal_mask = np.bitwise_or(north_west_diagonal_mask, np.left_shift(north_west_diagonal_mask, np.uint(larger_stride)))
            north_west_diagonal_mask = np.bitwise_xor(piece_position_mask, north_west_diagonal_mask)
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.EDGE_MASK_BOTTOM, self.EDGE_MASK_RIGHT)) == 0:
            south_east_diagonal_mask = piece_position_mask
            while np.bitwise_and(south_east_diagonal_mask, np.bitwise_or(self.EDGE_MASK_BOTTOM, self.EDGE_MASK_RIGHT)) == 0:
                south_east_diagonal_mask = np.bitwise_or(south_east_diagonal_mask, np.right_shift(south_east_diagonal_mask, np.uint(larger_stride)))
            south_east_diagonal_mask = np.bitwise_xor(piece_position_mask, south_east_diagonal_mask)
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.EDGE_MASK_BOTTOM, self.EDGE_MASK_LEFT)) == 0:
            south_west_diagonal_mask = piece_position_mask
            while np.bitwise_and(south_west_diagonal_mask, np.bitwise_or(self.EDGE_MASK_BOTTOM, self.EDGE_MASK_LEFT)) == 0:
                south_west_diagonal_mask = np.bitwise_or(south_west_diagonal_mask, np.right_shift(south_west_diagonal_mask, np.uint(smaller_stride)))
            south_west_diagonal_mask = np.bitwise_xor(piece_position_mask, south_west_diagonal_mask) 
        
        return np.bitwise_or(np.bitwise_or(north_east_diagonal_mask, north_west_diagonal_mask),
                             np.bitwise_or(south_east_diagonal_mask, south_west_diagonal_mask))

    def knight_attack_mask(self, piece_position_mask) -> np.ulonglong:
        stride_count = 3
        file_stride = 1
        rank_stride = 8
        west_file_attack_mask = np.ulonglong(0)
        east_file_attack_mask = np.ulonglong(0)
        north_rank_attack_mask = np.ulonglong(0)
        south_rank_attack_mask = np.ulonglong(0)
        
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_LEFT) == 0:
            west_file_attack_mask = piece_position_mask
            
            for i in range(stride_count):
                west_file_attack_mask = np.left_shift(west_file_attack_mask, np.uint(file_stride))
                
                if np.bitwise_and(west_file_attack_mask, self.EDGE_MASK_LEFT) != 0 and i < stride_count - 1:
                    west_file_attack_mask = np.ulonglong(0)
                    break     
                if i == stride_count - 1:
                    west_file_attack_mask = self.__assign_knight_file_mask(west_file_attack_mask)
        
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_RIGHT) == 0:
            east_file_attack_mask = piece_position_mask
            
            for i in range(stride_count):
                east_file_attack_mask = np.right_shift(east_file_attack_mask, np.uint(file_stride))
                
                if np.bitwise_and(east_file_attack_mask, self.EDGE_MASK_RIGHT) != 0 and i < stride_count - 1:
                    east_file_attack_mask = np.ulonglong(0)
                    break     
                if i == stride_count - 1:
                    east_file_attack_mask = self.__assign_knight_file_mask(east_file_attack_mask)    
        
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_TOP) == 0:
            north_rank_attack_mask = piece_position_mask
            
            for i in range(stride_count):
                north_rank_attack_mask = np.left_shift(north_rank_attack_mask, np.uint(rank_stride))
                
                if np.bitwise_and(north_rank_attack_mask, self.EDGE_MASK_TOP) != 0 and i < stride_count - 1:
                    north_rank_attack_mask = np.ulonglong(0)
                    break     
                if i == stride_count - 1:
                    north_rank_attack_mask = self.__assign_knight_rank_mask(north_rank_attack_mask)
        
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_BOTTOM) == 0:
            south_rank_attack_mask = piece_position_mask
            
            for i in range(stride_count):
                south_rank_attack_mask = np.right_shift(south_rank_attack_mask, np.uint(rank_stride))
                
                if np.bitwise_and(south_rank_attack_mask, self.EDGE_MASK_BOTTOM) != 0 and i < stride_count - 1:
                    south_rank_attack_mask = np.ulonglong(0)
                    break     
                if i == stride_count - 1:
                    south_rank_attack_mask = self.__assign_knight_rank_mask(south_rank_attack_mask)
                    
        return np.bitwise_or(np.bitwise_or(west_file_attack_mask, east_file_attack_mask),
                             np.bitwise_or(north_rank_attack_mask, south_rank_attack_mask))
    
    def queen_attack_mask(self, piece_position_mask) -> np.ulonglong:
        return np.bitwise_or(self.rook_attack_mask(piece_position_mask), self.bishop_attack_mask(piece_position_mask))
    
    def king_attack_mask(self, piece_position_mask) -> np.ulonglong:
        rank_stride = 8
        file_stride = 1
        larger_stride = 9
        smaller_stride = 7  
        file_attack_mask = np.ulonglong(0)
        rank_attack_mask = np.ulonglong(0)
        north_east_diagonal_mask = np.ulonglong(0)
        north_west_diagonal_mask = np.ulonglong(0)
        south_east_diagonal_mask = np.ulonglong(0)
        south_west_diagonal_mask = np.ulonglong(0)
        
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_LEFT) == 0:
                file_attack_mask = np.left_shift(piece_position_mask, np.uint(file_stride))

        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_RIGHT) == 0:
                file_attack_mask = np.bitwise_or(file_attack_mask, np.right_shift(piece_position_mask, np.uint(file_stride)))
         
        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_TOP) == 0:
            rank_attack_mask = np.left_shift(piece_position_mask, np.uint(rank_stride))

        if np.bitwise_and(piece_position_mask, self.EDGE_MASK_BOTTOM) == 0:
            rank_attack_mask = np.bitwise_or(rank_attack_mask, np.right_shift(piece_position_mask, np.uint(rank_stride)))
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.EDGE_MASK_TOP, self.EDGE_MASK_RIGHT)) == 0:
            north_east_diagonal_mask = np.left_shift(piece_position_mask, np.uint(smaller_stride))
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.EDGE_MASK_TOP, self.EDGE_MASK_LEFT)) == 0:
            north_west_diagonal_mask = np.left_shift(piece_position_mask, np.uint(larger_stride))
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.EDGE_MASK_BOTTOM, self.EDGE_MASK_RIGHT)) == 0:
            south_east_diagonal_mask = np.right_shift(piece_position_mask, np.uint(larger_stride))
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.EDGE_MASK_BOTTOM, self.EDGE_MASK_LEFT)) == 0:
            south_west_diagonal_mask = np.right_shift(piece_position_mask, np.uint(smaller_stride))

        return np.bitwise_or(np.bitwise_or(file_attack_mask, rank_attack_mask),
                             np.bitwise_or(np.bitwise_or(north_east_diagonal_mask, south_east_diagonal_mask),
                                           np.bitwise_or(north_west_diagonal_mask, south_west_diagonal_mask)))

    def __assign_knight_file_mask(self, file_attack_mask) -> np.ulonglong:
        rank_stride = 8
    
        if np.bitwise_and(file_attack_mask, np.bitwise_or(self.EDGE_MASK_TOP, self.EDGE_MASK_BOTTOM)) == 0:
            file_attack_mask = np.bitwise_or(np.left_shift(file_attack_mask, np.uint(rank_stride)),
                                             np.right_shift(file_attack_mask, np.uint(rank_stride)))
            return file_attack_mask
        elif np.bitwise_and(file_attack_mask, self.EDGE_MASK_TOP) == 0:
            file_attack_mask = np.left_shift(file_attack_mask, np.uint(rank_stride))
            
            return file_attack_mask
        file_attack_mask = np.right_shift(file_attack_mask, np.uint(rank_stride))
        
        return file_attack_mask

    def __assign_knight_rank_mask(self, rank_attack_mask) -> np.ulonglong:
        file_stride = 1
        
        if np.bitwise_and(rank_attack_mask, np.bitwise_or(self.EDGE_MASK_LEFT, self.EDGE_MASK_RIGHT)) == 0:
            rank_attack_mask = np.bitwise_or(np.left_shift(rank_attack_mask, np.uint(file_stride)),
                                             np.right_shift(rank_attack_mask, np.uint(file_stride)))
            return rank_attack_mask
        elif np.bitwise_and(rank_attack_mask, self.EDGE_MASK_LEFT) == 0:
            rank_attack_mask = np.left_shift(rank_attack_mask, np.uint(file_stride))
            
            return rank_attack_mask
        rank_attack_mask = np.right_shift(rank_attack_mask, np.uint(file_stride))
        
        return rank_attack_mask