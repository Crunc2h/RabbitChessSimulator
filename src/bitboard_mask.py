import numpy as np
from static.pieces import Pieces


class BitboardMasks:
    
    def move_exists(self, from_square, to_square, piece_type) -> bool:
        from_piece_pos_mask = self.__get_piece_position_mask(from_square["idx"])
        to_piece_pos_mask = self.__get_piece_position_mask(to_square["idx"])

        if piece_type == Pieces.W_PAWN or piece_type == Pieces.B_PAWN:
            try:
                try:
                    matching_mask = self.__all_piece_masks[piece_type]["attack"][from_piece_pos_mask]
                except KeyError:
                    matching_mask = self.__all_piece_masks[piece_type]["move"][from_piece_pos_mask]
            except KeyError:
                raise ValueError("Invalid move!")
            return np.bitwise_and(matching_mask, to_piece_pos_mask) > 0
        try:
            matching_mask = self.__all_piece_masks[piece_type][from_piece_pos_mask]
        except KeyError:
            raise ValueError("Invalid move!")
        
        return np.bitwise_and(matching_mask, to_piece_pos_mask) > 0

    def __init__(self):
        self.__EDGE_MASK_TOP = np.ulonglong(0b11111111 << 56)
        self.__EDGE_MASK_BOTTOM = np.ulonglong(0b11111111)
        self.__EDGE_MASK_LEFT = np.ulonglong(0b1000000010000000100000001000000010000000100000001000000010000000)
        self.__EDGE_MASK_RIGHT = np.ulonglong(0b0000000100000001000000010000000100000001000000010000000100000001)
        self.__W_EN_PASSANT_MASK = np.ulonglong(0b1111111100000000)
        self.__B_EN_PASSANT_MASK = np.ulonglong(0b0000000011111111 << 48)
        self.__all_piece_masks = self.__construct_all_piece_masks()
    
    def __construct_all_piece_masks(self):
        all_piece_masks = {
            Pieces.W_PAWN:{
                "move":{},
                "attack": {}
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
        
        for key in all_piece_masks.keys():
            for i in range(64):
                piece_position_mask = self.__get_piece_position_mask(i)
                if key != Pieces.W_PAWN and key != Pieces.B_PAWN:
                    all_piece_masks[key][piece_position_mask] = self.__get_masks_of_type(key, piece_position_mask)
                else:
                    pawn_movement_mask, pawn_attack_mask = self.__get_masks_of_type(key, piece_position_mask)
                    all_piece_masks[key]["move"][piece_position_mask] = pawn_movement_mask
                    all_piece_masks[key]["attack"][piece_position_mask] = pawn_attack_mask
        
        return all_piece_masks

    def __get_masks_of_type(self, piece_type, piece_position_mask):
        if piece_type == Pieces.W_PAWN:
            return self.__pawn_attack_mask(piece_position_mask, True), self.__pawn_movement_mask(piece_position_mask, True)
        elif piece_type == Pieces.B_PAWN:
            return self.__pawn_attack_mask(piece_position_mask, False), self.__pawn_movement_mask(piece_position_mask, False)
        elif piece_type == Pieces.ROOK:
            return self.__rook_attack_mask(piece_position_mask)
        elif piece_type == Pieces.KNIGHT:
            return self.__knight_attack_mask(piece_position_mask)
        elif piece_type == Pieces.BISHOP:
            return self.__bishop_attack_mask(piece_position_mask)
        elif piece_type == Pieces.QUEEN:
            return self.__queen_attack_mask(piece_position_mask)
        elif piece_type == Pieces.KING:
            return self.__king_attack_mask(piece_position_mask)
        else:
            raise ValueError("Invalid piece type passed to mask getter!")

    def __get_piece_position_mask(self, square_idx) -> np.ulonglong:
        return np.ulonglong(1 << square_idx)

    def __pawn_movement_mask(self, piece_position_mask, color) -> np.ulonglong:
        stride = 8
        
        if color:
            if np.bitwise_and(piece_position_mask, self.__W_EN_PASSANT_MASK) > 0:
                return np.bitwise_or(np.left_shift(piece_position_mask, np.uint(stride)), np.left_shift(piece_position_mask, np.uint(stride * 2)))
            return np.left_shift(piece_position_mask, np.uint(stride))
        if np.bitwise_and(piece_position_mask, self.__B_EN_PASSANT_MASK) > 0:
            return np.bitwise_or(np.right_shift(piece_position_mask, np.uint(stride)), np.right_shift(piece_position_mask, np.uint(stride * 2)))
        return np.right_shift(piece_position_mask, np.uint(stride))
    
    def __pawn_attack_mask(self, piece_position_mask, side) -> np.ulonglong:
        larger_stride = 9
        smaller_stride = 7
        
        if side:
            if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_TOP) > 0:
                return np.ulonglong(0)
            elif np.bitwise_and(piece_position_mask, self.__EDGE_MASK_LEFT) > 0:
                return np.left_shift(piece_position_mask, np.uint(smaller_stride))
            elif np.bitwise_and(piece_position_mask, self.__EDGE_MASK_RIGHT) > 0:
                return np.left_shift(piece_position_mask, np.uint(larger_stride))
            return np.bitwise_or(np.left_shift(piece_position_mask, np.uint(larger_stride)), np.left_shift(piece_position_mask, np.uint(smaller_stride)))
        
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_BOTTOM) > 0:
            return np.ulonglong(0)
        elif np.bitwise_and(piece_position_mask, self.__EDGE_MASK_LEFT) > 0:
            return np.right_shift(piece_position_mask, np.uint(larger_stride))
        elif np.bitwise_and(piece_position_mask, self.__EDGE_MASK_RIGHT) > 0:
            return np.right_shift(piece_position_mask, np.uint(smaller_stride))
        return np.bitwise_or(np.right_shift(piece_position_mask, np.uint(larger_stride)), np.right_shift(piece_position_mask, np.uint(smaller_stride)))
    
    def __rook_attack_mask(self, piece_position_mask) -> np.ulonglong:
        file_stride = 1 
        rank_stride = 8 
        file_attack_mask = piece_position_mask
        rank_attack_mask = piece_position_mask
        
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_LEFT) == 0:
            while np.bitwise_and(file_attack_mask, self.__EDGE_MASK_LEFT) == 0:
                file_attack_mask = np.bitwise_or(file_attack_mask, np.left_shift(file_attack_mask, np.uint(file_stride)))
            file_attack_mask = np.bitwise_xor(file_attack_mask, piece_position_mask)
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_RIGHT) == 0:
            while np.bitwise_and(file_attack_mask, self.__EDGE_MASK_RIGHT) == 0:
                file_attack_mask = np.bitwise_or(file_attack_mask, np.right_shift(file_attack_mask, np.uint(file_stride)))
            file_attack_mask = np.bitwise_xor(file_attack_mask, piece_position_mask)
        
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_TOP) == 0:
            while np.bitwise_and(rank_attack_mask, self.__EDGE_MASK_TOP) == 0:
                rank_attack_mask = np.bitwise_or(rank_attack_mask, np.left_shift(rank_attack_mask, np.uint(rank_stride)))
            rank_attack_mask = np.bitwise_xor(rank_attack_mask, piece_position_mask)
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_BOTTOM) == 0:
            while np.bitwise_and(rank_attack_mask, self.__EDGE_MASK_BOTTOM) == 0:
                rank_attack_mask = np.bitwise_or(rank_attack_mask, np.right_shift(rank_attack_mask, np.uint(rank_stride)))
            rank_attack_mask = np.bitwise_xor(rank_attack_mask, piece_position_mask)
        
        return np.bitwise_or(file_attack_mask, rank_attack_mask)
    
    def __bishop_attack_mask(self, piece_position_mask) -> np.ulonglong:
        larger_stride = 9
        smaller_stride = 7
        north_east_diagonal_mask = np.ulonglong(0)
        north_west_diagonal_mask = np.ulonglong(0)
        south_east_diagonal_mask = np.ulonglong(0)
        south_west_diagonal_mask = np.ulonglong(0)
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.__EDGE_MASK_TOP, self.__EDGE_MASK_RIGHT)) == 0:
            north_east_diagonal_mask = piece_position_mask
            while np.bitwise_and(north_east_diagonal_mask, np.bitwise_or(self.__EDGE_MASK_TOP, self.__EDGE_MASK_RIGHT)) == 0:
                north_east_diagonal_mask = np.bitwise_or(north_east_diagonal_mask, np.left_shift(north_east_diagonal_mask, np.uint(smaller_stride)))
            north_east_diagonal_mask = np.bitwise_xor(piece_position_mask, north_east_diagonal_mask)

        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.__EDGE_MASK_TOP, self.__EDGE_MASK_LEFT)) == 0:
            north_west_diagonal_mask = piece_position_mask
            while np.bitwise_and(north_west_diagonal_mask, np.bitwise_or(self.__EDGE_MASK_TOP, self.__EDGE_MASK_LEFT)) == 0:
                north_west_diagonal_mask = np.bitwise_or(north_west_diagonal_mask, np.left_shift(north_west_diagonal_mask, np.uint(larger_stride)))
            north_west_diagonal_mask = np.bitwise_xor(piece_position_mask, north_west_diagonal_mask)
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_RIGHT)) == 0:
            south_east_diagonal_mask = piece_position_mask
            while np.bitwise_and(south_east_diagonal_mask, np.bitwise_or(self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_RIGHT)) == 0:
                south_east_diagonal_mask = np.bitwise_or(south_east_diagonal_mask, np.right_shift(south_east_diagonal_mask, np.uint(larger_stride)))
            south_east_diagonal_mask = np.bitwise_xor(piece_position_mask, south_east_diagonal_mask)
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_LEFT)) == 0:
            south_west_diagonal_mask = piece_position_mask
            while np.bitwise_and(south_west_diagonal_mask, np.bitwise_or(self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_LEFT)) == 0:
                south_west_diagonal_mask = np.bitwise_or(south_west_diagonal_mask, np.right_shift(south_west_diagonal_mask, np.uint(smaller_stride)))
            south_west_diagonal_mask = np.bitwise_xor(piece_position_mask, south_west_diagonal_mask) 
        
        return np.bitwise_or(np.bitwise_or(north_east_diagonal_mask, north_west_diagonal_mask),
                             np.bitwise_or(south_east_diagonal_mask, south_west_diagonal_mask))

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
    
    def __assign_knight_file_mask(self, file_attack_mask) -> np.ulonglong:
        rank_stride = 8
    
        if np.bitwise_and(file_attack_mask, np.bitwise_or(self.__EDGE_MASK_TOP, self.__EDGE_MASK_BOTTOM)) == 0:
            file_attack_mask = np.bitwise_or(np.left_shift(file_attack_mask, np.uint(rank_stride)),
                                             np.right_shift(file_attack_mask, np.uint(rank_stride)))
            return file_attack_mask
        elif np.bitwise_and(file_attack_mask, self.__EDGE_MASK_TOP) == 0:
            file_attack_mask = np.left_shift(file_attack_mask, np.uint(rank_stride))
            
            return file_attack_mask
        file_attack_mask = np.right_shift(file_attack_mask, np.uint(rank_stride))
        
        return file_attack_mask

    def __assign_knight_rank_mask(self, rank_attack_mask) -> np.ulonglong:
        file_stride = 1
        
        if np.bitwise_and(rank_attack_mask, np.bitwise_or(self.__EDGE_MASK_LEFT, self.__EDGE_MASK_RIGHT)) == 0:
            rank_attack_mask = np.bitwise_or(np.left_shift(rank_attack_mask, np.uint(file_stride)),
                                             np.right_shift(rank_attack_mask, np.uint(file_stride)))
            return rank_attack_mask
        elif np.bitwise_and(rank_attack_mask, self.__EDGE_MASK_LEFT) == 0:
            rank_attack_mask = np.left_shift(rank_attack_mask, np.uint(file_stride))
            
            return rank_attack_mask
        rank_attack_mask = np.right_shift(rank_attack_mask, np.uint(file_stride))
        
        return rank_attack_mask
    
    def __queen_attack_mask(self, piece_position_mask) -> np.ulonglong:
        return np.bitwise_or(self.__rook_attack_mask(piece_position_mask), self.__bishop_attack_mask(piece_position_mask))
    
    def __king_attack_mask(self, piece_position_mask) -> np.ulonglong:
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
        
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_LEFT) == 0:
                file_attack_mask = np.left_shift(piece_position_mask, np.uint(file_stride))

        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_RIGHT) == 0:
                file_attack_mask = np.bitwise_or(file_attack_mask, np.right_shift(piece_position_mask, np.uint(file_stride)))
         
        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_TOP) == 0:
            rank_attack_mask = np.left_shift(piece_position_mask, np.uint(rank_stride))

        if np.bitwise_and(piece_position_mask, self.__EDGE_MASK_BOTTOM) == 0:
            rank_attack_mask = np.bitwise_or(rank_attack_mask, np.right_shift(piece_position_mask, np.uint(rank_stride)))
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.__EDGE_MASK_TOP, self.__EDGE_MASK_RIGHT)) == 0:
            north_east_diagonal_mask = np.left_shift(piece_position_mask, np.uint(smaller_stride))
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.__EDGE_MASK_TOP, self.__EDGE_MASK_LEFT)) == 0:
            north_west_diagonal_mask = np.left_shift(piece_position_mask, np.uint(larger_stride))
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_RIGHT)) == 0:
            south_east_diagonal_mask = np.right_shift(piece_position_mask, np.uint(larger_stride))
        
        if np.bitwise_and(piece_position_mask, np.bitwise_or(self.__EDGE_MASK_BOTTOM, self.__EDGE_MASK_LEFT)) == 0:
            south_west_diagonal_mask = np.right_shift(piece_position_mask, np.uint(smaller_stride))

        return np.bitwise_or(np.bitwise_or(file_attack_mask, rank_attack_mask),
                             np.bitwise_or(np.bitwise_or(north_east_diagonal_mask, south_east_diagonal_mask),
                                           np.bitwise_or(north_west_diagonal_mask, south_west_diagonal_mask)))

    