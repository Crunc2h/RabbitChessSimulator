import numpy as np

class BoardTransformer:
    
    def __init__(self, bb_processor_obj) -> None:
        self.__bb_processor = bb_processor_obj
    
    def transform_board(self,
                        info,
                        board):
        

        if info.is_capture:              
            if board.is_white:
                captured_piece_type_idx = self.__bb_processor.get_piece_type_and_idx(not info.is_white, info.to_sqr_pos64, board.b_pieces)[1]
                board.b_pieces[captured_piece_type_idx] = np.bitwise_xor(info.to_sqr_pos64, board.b_pieces[captured_piece_type_idx])
                board.b_pieces_mask = np.bitwise_or.reduce(board.b_pieces)
            else:
                captured_piece_type_idx = self.__bb_processor.get_piece_type_and_idx(not info.is_white, info.to_sqr_pos64, board.w_pieces)[1]
                board.w_pieces[captured_piece_type_idx] = np.bitwise_xor(info.to_sqr_pos64, board.w_pieces[captured_piece_type_idx])
                board.w_pieces_mask = np.bitwise_or.reduce(board.w_pieces)
        
        board_change = np.bitwise_or(info.from_sqr_pos64, info.to_sqr_pos64)
        if board.is_white:
            board.w_pieces[info.piece_type_idx] = np.bitwise_xor(board.w_pieces[info.piece_type_idx], board_change)
            board.w_pieces_mask = np.bitwise_or.reduce(board.w_pieces)
        else:
            board.b_pieces[info.piece_type_idx] = np.bitwise_xor(board.b_pieces[info.piece_type_idx], board_change)
            board.b_pieces_mask = np.bitwise_or.reduce(board.b_pieces)
           
        board.all_pieces_mask = info.updated_board

        if info.is_check:
            board.is_check = np.ulonglong(0)
            board.is_white = np.bitwise_xor(board.is_white, np.ulonglong(0b1))
            return
        board.is_white = np.bitwise_xor(board.is_white, np.ulonglong(0b1))
