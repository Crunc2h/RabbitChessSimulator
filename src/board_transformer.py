import numpy as np
from bitboard_printer import BitboardPrinter
import copy

class BoardTransformer:
    
    MATCH_BOARDS = []
    
    
    def __init__(self, bb_processor_obj) -> None:
        self.__bb_processor = bb_processor_obj
    
    def transform_board(self,
                        side_pieces64_arr,
                        oppo_pieces64_arr,
                        info,
                        board):
        side = np.bitwise_and(np.ulonglong(0b1), board.data["castling_check_color"])
        BoardTransformer.MATCH_BOARDS.append(copy.deepcopy(board))

        if info["capture"]:
            oppo_captured_piece_type_idx = self.__bb_processor.get_piece_type_and_idx(not side, info["to_sqr_pos64"], oppo_pieces64_arr)[1]
            if oppo_captured_piece_type_idx == 4:
                raise Exception("YOU CANNOT EAT THE FUCKING KING")
            oppo_pieces64_arr[oppo_captured_piece_type_idx] = np.bitwise_xor(info["to_sqr_pos64"], oppo_pieces64_arr[oppo_captured_piece_type_idx])
            board.data[f"all_{'b' if side else 'w'}_pieces"] = np.bitwise_or.reduce(oppo_pieces64_arr)

        board_change = np.bitwise_or(info["from_sqr_pos64"], info["to_sqr_pos64"])
        side_pieces64_arr[info["piece_type_idx"]] = np.bitwise_xor(side_pieces64_arr[info["piece_type_idx"]], board_change)
        board.data[f"all_{'w' if side else 'b'}_pieces"] = np.bitwise_or.reduce(side_pieces64_arr)
        board.data["all_pieces"] = info["new_board_pos64"] 

        if info["check"]:
            board.data["castling_check_color"] = np.bitwise_xor(np.ulonglong(0b01), board.data["castling_check_color"])
            board.data["castling_check_color"] = np.bitwise_or(np.ulonglong(0b10), board.data["castling_check_color"])
            return
        board.data["castling_check_color"] = np.bitwise_xor(np.ulonglong(0b01), board.data["castling_check_color"])
