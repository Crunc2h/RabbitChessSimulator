import numpy as np
from static.pieces import Pieces


class BitboardProcessor:
    def __init__(self, bb_masks_obj):
        self.key_map = {
            True:{
                  5:Pieces.W_PAWN,
                  0:Pieces.ROOK,
                  1:Pieces.KNIGHT,
                  2:Pieces.BISHOP,
                  3:Pieces.QUEEN,
                  4:Pieces.KING,
            },
            False:{
                5:Pieces.B_PAWN,
                0:Pieces.ROOK,
                1:Pieces.KNIGHT,
                2:Pieces.BISHOP,
                3:Pieces.QUEEN,
                4:Pieces.KING,
            }
        }
        self.__bb_masks = bb_masks_obj
        self.__all_static_attacks64 = self.__bb_masks.get_all_attacks64_static()
    
    def get_piece_type_and_idx(self, side, from_sqr_piece_pos64, all_side_pieces64):
        piece_type_idx = self.get_piece_type_idx_from_pos64(from_sqr_piece_pos64, all_side_pieces64)
        return self.key_map[bool(side)][piece_type_idx], piece_type_idx
    
    def get_side(board_auxiliary_info_int64):
        return bool(np.bitwise_and(board_auxiliary_info_int64, np.ulonglong(0b1)))
    
    def get_piece_type_idx_from_pos64(self, curr_piece_pos64, pieces_arr):
        return np.argmax(np.apply_along_axis(func1d=lambda piece_type_mask: np.bitwise_and(piece_type_mask, curr_piece_pos64) > 0,
                                             axis=0, 
                                             arr=pieces_arr))
    
    def update_all_attacks64_dynamic(self, 
                                     pieces_arr, 
                                     all_pieces_pos):
        rooks_pieces_pos64 = pieces_arr[0]
        bishops_pieces_pos64 = pieces_arr[2]
        queens_pieces_pos64 = pieces_arr[3]
        
        empty_squares64 = np.invert(all_pieces_pos)
        
        rooks_attacks64_dynamic = self.__update_piece_type_dynamic_attacks64(piece_type=Pieces.ROOK,
                                                                             pieces_pos64=rooks_pieces_pos64,
                                                                             empty_squares64=empty_squares64)
        bishops_attacks64_dynamic = self.__update_piece_type_dynamic_attacks64(piece_type=Pieces.BISHOP,
                                                                             pieces_pos64=bishops_pieces_pos64,
                                                                             empty_squares64=empty_squares64)
        queens_attacks64_dynamic = self.__update_piece_type_dynamic_attacks64(piece_type=Pieces.QUEEN,
                                                                             pieces_pos64=queens_pieces_pos64,
                                                                             empty_squares64=empty_squares64)
        
        return np.bitwise_or(queens_attacks64_dynamic, np.bitwise_or(rooks_attacks64_dynamic, bishops_attacks64_dynamic)) 
    
    def update_all_attacks64_static(self,
                                    pieces_arr,
                                    side):
        king_piece_pos64 = pieces_arr[4]
        pawns_pieces_pos64 = pieces_arr[5]
        knights_pieces_pos64 = pieces_arr[1]

        pawns_attacks64_static = self.__update_piece_type_static_attacks64(piece_type= Pieces.W_PAWN if side else Pieces.B_PAWN,
                                                                           pieces_pos64=pawns_pieces_pos64,
                                                                           side=side)
        knights_attacks64_static = self.__update_piece_type_static_attacks64(piece_type= Pieces.KNIGHT,
                                                                           pieces_pos64=knights_pieces_pos64,
                                                                           side=side)
        king_attacks64_static = self.__update_piece_type_static_attacks64(piece_type= Pieces.KING,
                                                                          pieces_pos64=king_piece_pos64,
                                                                          side=side)
        
        return np.bitwise_or(king_attacks64_static, np.bitwise_or(pawns_attacks64_static, knights_attacks64_static)) 
    
    def __map_piece_pos_to_dynamic_attack(self, 
                                          piece_pos64, 
                                          piece_type,
                                          empty_squares64):
            static_attacks64 =  self.__all_static_attacks64[piece_type][piece_pos64]
            unblocked_attack_paths64 = np.bitwise_and(empty_squares64, static_attacks64)
            if piece_type == Pieces.ROOK:
                return self.__bb_masks.rook_attacks64_dynamic(piece_pos64, np.bitwise_and(unblocked_attack_paths64, static_attacks64))
            elif piece_type == Pieces.BISHOP:
                return self.__bb_masks.bishop_attacks64_dynamic(piece_pos64, np.bitwise_and(unblocked_attack_paths64, static_attacks64))
            elif piece_type == Pieces.QUEEN:
                return self.__bb_masks.queen_attacks64_dynamic(piece_pos64, np.bitwise_and(unblocked_attack_paths64, static_attacks64))
            else:
                raise Exception("Invalid piece type for dynamic attack calculation!")
    
    def __map_piece_pos_to_static_attack(self,
                                         piece_pos64,
                                         piece_type,
                                         side):
        if piece_type == Pieces.W_PAWN or piece_type == Pieces.B_PAWN:
            if side:
                return self.__all_static_attacks64[Pieces.W_PAWN]["attack"][piece_pos64]
            return self.__all_static_attacks64[Pieces.B_PAWN]["attack"][piece_pos64]
        elif piece_type == Pieces.KNIGHT:
            return self.__all_static_attacks64[Pieces.KNIGHT][piece_pos64]
        elif piece_type == Pieces.KING:
            return self.__all_static_attacks64[Pieces.KING][piece_pos64]
        else:
            raise Exception("Invalid piece type for static attack calculation!")
    
    def __update_piece_type_dynamic_attacks64(self, piece_type, pieces_pos64, empty_squares64):
        piece_attacks64_dynamic = np.ulonglong(0)
        
        if pieces_pos64.bit_count() > 0:
            pieces_pos64 = self.extract_individual_position_masks(pieces_pos64)
            piece_attacks64_dynamic = np.array(list(map(lambda piece_pos64: self.__map_piece_pos_to_dynamic_attack(piece_pos64=piece_pos64, 
                                                                                                                    piece_type=piece_type,
                                                                                                                    empty_squares64=empty_squares64), pieces_pos64)))
            piece_attacks64_dynamic = np.bitwise_or.reduce(piece_attacks64_dynamic)
        
        return piece_attacks64_dynamic
    
    def __update_piece_type_static_attacks64(self, piece_type, pieces_pos64, side):
        piece_attacks64_static = np.ulonglong(0)
        
        if pieces_pos64.bit_count() > 0:
            pieces_pos64 = self.extract_individual_position_masks(pieces_pos64)
            piece_attacks64_static = np.array(list(map(lambda piece_pos64: self.__map_piece_pos_to_static_attack(piece_pos64=piece_pos64, 
                                                                                                                 piece_type=piece_type,
                                                                                                                 side=side), pieces_pos64)))
            piece_attacks64_static = np.bitwise_or.reduce(piece_attacks64_static)
        
        return piece_attacks64_static

    def extract_individual_position_masks(self, position_masks):
        return np.array(list(filter(lambda position_mask:np.bitwise_and(position_mask, position_masks), self.__bb_masks.get_all_piece_positions64_from_idx().values())))
    
    def update_pos64(self, prev_pos64, from_sqr_piece_pos64, to_sqr_piece_pos64):
        return np.bitwise_or(np.bitwise_xor(prev_pos64, from_sqr_piece_pos64), to_sqr_piece_pos64)
    