import numpy as np
from static.pieces import Pieces
from bitboard_printer import BitboardPrinter

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
    
    def extract_individual_position_masks(self, position_masks):
        return np.array(list(filter(lambda position_mask:np.bitwise_and(position_mask, position_masks), self.__bb_masks.get_all_piece_positions64_from_idx().values())))
    
    def update_all_attacks64_dynamic(self, pieces_arr, all_pieces_pos):
        rooks_pieces_pos64 = pieces_arr[0]
        bishops_pieces_pos64 = pieces_arr[2]
        queens_pieces_pos64 = pieces_arr[3]

        rooks_attacks64_dynamic = np.ulonglong(0)
        bishops_attacks64_dynamic = np.ulonglong(0)
        queens_attacks64_dynamic = np.ulonglong(0)

        available_squares = np.invert(all_pieces_pos)
        
        def map_piece_pos_to_dynamic_attack(piece_pos64, piece_type):
            atk =  self.__bb_masks.get_all_attacks64_static()[piece_type][piece_pos64]
            if piece_type is Pieces.ROOK:
                return self.__bb_masks.rook_attacks64_dynamic(piece_pos64, np.bitwise_and(available_squares, atk))
            elif piece_type is Pieces.BISHOP:
                return self.__bb_masks.bishop_attacks64_dynamic(piece_pos64, np.bitwise_and(available_squares, atk))
            elif piece_type is Pieces.QUEEN:
                return self.__bb_masks.queen_attacks64_dynamic(piece_pos64, np.bitwise_and(available_squares, atk))
            else:
                raise Exception("Invalid piece type for dynamic attack calculation!")
                                                                               
        if rooks_pieces_pos64.bit_count() > 0:
            
            rooks_pieces_pos64 = self.extract_individual_position_masks(rooks_pieces_pos64)

            rooks_attacks64_dynamic = np.array(list(map(lambda x: map_piece_pos_to_dynamic_attack(x, piece_type=Pieces.ROOK), rooks_pieces_pos64)))
            
            rooks_attacks64_dynamic = np.bitwise_or.reduce(rooks_attacks64_dynamic)
            
        if bishops_pieces_pos64.bit_count() > 0:
            
            bishops_pieces_pos64 = self.extract_individual_position_masks(bishops_pieces_pos64)

            bishops_attacks64_dynamic = np.array(list(map(lambda x: map_piece_pos_to_dynamic_attack(x, piece_type=Pieces.BISHOP), bishops_pieces_pos64)))
            
            bishops_attacks64_dynamic = np.bitwise_or.reduce(bishops_attacks64_dynamic)
        
        if queens_pieces_pos64.bit_count() > 0:
            queens_pieces_pos64 = self.extract_individual_position_masks(queens_pieces_pos64)
            queens_attacks64_dynamic = np.array(list(map(lambda x: map_piece_pos_to_dynamic_attack(x, piece_type=Pieces.QUEEN), queens_pieces_pos64)))
            queens_attacks64_dynamic = np.bitwise_or.reduce(queens_attacks64_dynamic)
        
        return np.bitwise_or(queens_attacks64_dynamic, np.bitwise_or(rooks_attacks64_dynamic, bishops_attacks64_dynamic)) 

    
    def update_all_attacks64_static(self, prev_all_attacks64_static, from_sqr_piece_attacks64, to_sqr_piece_attacks64):
        return np.bitwise_or(np.bitwise_xor(prev_all_attacks64_static, from_sqr_piece_attacks64), to_sqr_piece_attacks64)
    
    def update_all_pieces_pos64(self, prev_all_pieces_pos64, from_sqr_piece_pos64, to_sqr_piece_pos64):
        return self.update_all_attacks64_static(prev_all_pieces_pos64, from_sqr_piece_pos64, to_sqr_piece_pos64)
    
    def is_valid(self, from_square, to_square, board_obj):
        board_data = board_obj.data
        from_square_idx = from_square["idx"]
        to_square_idx = to_square["idx"]
        side = np.bitwise_and(board_data["side_to_move"], np.ulonglong(0b01)) > 0 
        
        from_sqr_piece_pos64 = self.__bb_masks.get_all_piece_positions64_from_idx()[from_square_idx]
        to_sqr_piece_pos64 = self.__bb_masks.get_all_piece_positions64_from_idx()[to_square_idx]

        if np.bitwise_and(from_sqr_piece_pos64, board_data["All_Pieces_mask"]) == 0:
            raise Exception("There isn't a piece at the specified source square!")
        if ((side and np.bitwise_and(from_sqr_piece_pos64, board_data["W_Pieces_mask"]) == 0)
             or (not side and np.bitwise_and(from_sqr_piece_pos64, board_data["B_Pieces_mask"]) == 0)):
            raise Exception("The piece at the source square belongs to the opponent!")
        if ((side and np.bitwise_and(to_sqr_piece_pos64, board_data["W_Pieces_mask"]) > 0)
             or (not side and np.bitwise_and(to_sqr_piece_pos64, board_data["B_Pieces_mask"]) > 0)):
            raise Exception("Another one of your pieces already occupies target square!")

        if side:
            piece_type_idx = self.get_piece_type_idx_from_pos_mask(from_sqr_piece_pos64, board_obj.data["W_Pieces_arr"])
            piece_type = self.__board_key_to_piece_type(piece_type_idx)
        else:
            piece_type_idx = self.get_piece_type_idx_from_pos_mask(from_sqr_piece_pos64, board_obj.data["B_Pieces_arr"])
            if piece_type_idx == 5: piece_type_idx *= -1
            piece_type = self.__board_key_to_piece_type(piece_type_idx)
        
        to_sqr_piece_attacks64 = None
        
        if piece_type is not Pieces.W_PAWN and piece_type is not Pieces.B_PAWN:
            from_sqr_piece_attacks64 = self.__bb_masks.get_all_attacks64_static()[piece_type][from_sqr_piece_pos64] 
        else:
            pawn_movements64, pawn_attacks64 = (self.__bb_masks.get_all_attacks64_static()[piece_type]["move"][from_sqr_piece_pos64],
                                                self.__bb_masks.get_all_attacks64_static()[piece_type]["attack"][from_sqr_piece_pos64])
            is_pawn_movement = np.bitwise_and(pawn_movements64, to_sqr_piece_pos64) > 0
            if is_pawn_movement:
                if np.bitwise_and(to_sqr_piece_pos64, board_data["All_Pieces_mask"]) > 0:
                    raise Exception("Pawn cannot move to a square already occupied by another piece!")
                from_sqr_piece_attacks64 = pawn_movements64
            else:
                if np.bitwise_and(to_sqr_piece_pos64, board_data["All_Pieces_mask"]) == 0:
                    raise Exception("There is no enemy piece at the targeted square for pawn to attack!")
                from_sqr_piece_attacks64 = pawn_attacks64
                
            to_sqr_piece_attacks64 = self.__bb_masks.get_all_attacks64_static()[piece_type]["attack"][to_sqr_piece_pos64]

        move_exists_for_piece_type = np.bitwise_and(from_sqr_piece_attacks64, to_sqr_piece_pos64) > 0
        if move_exists_for_piece_type == False:
            raise Exception("Illegal move!")
        
        adjacent_sqr_mask = self.__bb_masks.get_all_adj_squares64_of_idx()[from_square_idx]
        is_move_to_sqr_adjacent = np.bitwise_and(adjacent_sqr_mask, to_sqr_piece_pos64) > 0

        if is_move_to_sqr_adjacent == False and piece_type != Pieces.KNIGHT:
            piece_movement_path = self.__bb_masks.get_all_piece_paths64_static()[piece_type][(from_square_idx, to_square_idx)]
            if np.bitwise_and(piece_movement_path, board_data["All_Pieces_mask"]) > 0:
                raise Exception("There is a piece obstructing the path towards target square!")

        if not to_sqr_piece_attacks64: to_sqr_piece_attacks64 = self.__bb_masks.get_all_attacks64_static()[piece_type][to_sqr_piece_pos64]


        updated_all_pieces_pos64 = self.update_all_pieces_pos64(board_data["All_Pieces_mask"], from_sqr_piece_pos64, to_sqr_piece_pos64)
        
        w_pieces_arr = np.copy(board_data["W_Pieces_arr"])
        b_pieces_arr = np.copy(board_data["B_Pieces_arr"])
        
        if side:
            static_attacks = board_data["W_Attacks64_static"]
            if np.bitwise_and(to_sqr_piece_pos64, board_data["B_Pieces_mask"]) > 0:
                captured_piece_type_idx = self.get_piece_type_idx_from_pos_mask(to_sqr_piece_pos64, b_pieces_arr)
                b_pieces_arr[captured_piece_type_idx] = np.bitwise_xor(to_sqr_piece_pos64, b_pieces_arr[captured_piece_type_idx])
            
            if piece_type == Pieces.QUEEN:
                w_pieces_arr[3] = np.bitwise_xor(w_pieces_arr[3], np.bitwise_or(from_sqr_piece_pos64, to_sqr_piece_pos64))
            elif piece_type == Pieces.BISHOP:
                w_pieces_arr[2] = np.bitwise_xor(w_pieces_arr[2], np.bitwise_or(from_sqr_piece_pos64, to_sqr_piece_pos64))
            elif piece_type == Pieces.ROOK:
                w_pieces_arr[0] = np.bitwise_xor(w_pieces_arr[0], np.bitwise_or(from_sqr_piece_pos64, to_sqr_piece_pos64))
            else:
                static_attacks = self.update_all_attacks64_static(board_data["W_Attacks64_static"], from_sqr_piece_attacks64, to_sqr_piece_attacks64)
        else:
            static_attacks = board_data["B_Attacks64_static"]
            if np.bitwise_and(to_sqr_piece_pos64, board_data["W_Pieces_mask"]) > 0:
                captured_piece_type_idx = self.get_piece_type_idx_from_pos_mask(to_sqr_piece_pos64, w_pieces_arr)
                w_pieces_arr[captured_piece_type_idx] = np.bitwise_xor(to_sqr_piece_pos64, w_pieces_arr[captured_piece_type_idx])

            if piece_type == Pieces.QUEEN:
                b_pieces_arr[3] = np.bitwise_xor(b_pieces_arr[3], np.bitwise_or(from_sqr_piece_pos64, to_sqr_piece_pos64))
            elif piece_type == Pieces.BISHOP:
                b_pieces_arr[2] = np.bitwise_xor(b_pieces_arr[2], np.bitwise_or(from_sqr_piece_pos64, to_sqr_piece_pos64))
            elif piece_type == Pieces.ROOK:
                b_pieces_arr[0] = np.bitwise_xor(b_pieces_arr[0], np.bitwise_or(from_sqr_piece_pos64, to_sqr_piece_pos64))
            else:
                static_attacks = self.update_all_attacks64_static(board_data["B_Attacks64_static"], from_sqr_piece_attacks64, to_sqr_piece_attacks64)
                



        w_dynamic_attacks = self.update_all_attacks64_dynamic(w_pieces_arr, updated_all_pieces_pos64)
        b_dynamic_attacks = self.update_all_attacks64_dynamic(b_pieces_arr, updated_all_pieces_pos64)

        print("============WHITE_ALL_ATTACKS_DYNAMIC==============")
        BitboardPrinter.print(w_dynamic_attacks)
        print("============BLACK ALL ATTACKS DYNAMIC==============")
        BitboardPrinter.print(b_dynamic_attacks)

        
        if side:
            opponent_static_attacks = board_data["B_Attacks64_static"]
            opponent_all_attacks = np.bitwise_or(b_dynamic_attacks, opponent_static_attacks)
            all_attacks = np.bitwise_or(w_dynamic_attacks, static_attacks)
            
            king_pos = board_data["W_Pieces_arr"][4]
            if piece_type == Pieces.KING:
                king_pos = np.bitwise_xor(board_data["W_Pieces_arr"][4], np.bitwise_or(from_sqr_piece_pos64, to_sqr_piece_pos64))

            if np.bitwise_and(opponent_all_attacks, king_pos) > 0:
                raise Exception("Your king is still or would be under attack!")
            
            is_capture = np.bitwise_and(to_sqr_piece_pos64, board_data["B_Pieces_mask"]) > 0
            is_check = np.bitwise_and(all_attacks, board_data["B_Pieces_arr"][4])

        else:
            opponent_static_attacks = board_data["W_Attacks64_static"]
            opponent_all_attacks = np.bitwise_or(w_dynamic_attacks, opponent_static_attacks)
            all_attacks = np.bitwise_or(b_dynamic_attacks, static_attacks)
                  
            
            king_pos = board_data["B_Pieces_arr"][4]
            if piece_type == Pieces.KING:
                king_pos = np.bitwise_xor(board_data["B_Pieces_arr"][4], np.bitwise_or(from_sqr_piece_pos64, to_sqr_piece_pos64))

            if np.bitwise_and(opponent_all_attacks, king_pos) > 0:
                raise Exception("Your king is still or would be under attack!")
            
            is_capture = np.bitwise_and(to_sqr_piece_pos64, board_data["W_Pieces_mask"]) > 0
            is_check = np.bitwise_and(all_attacks, board_data["W_Pieces_arr"][4])

        
        return is_capture, is_check, updated_all_pieces_pos64, from_sqr_piece_pos64, to_sqr_piece_pos64, piece_type_idx
    

    


        
        





        