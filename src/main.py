import numpy as np

from bitboard import Bitboard
from bitboard_printer import BitboardPrinter
from bitboard_storage import BitboardMasks
from bitboard_processor import BitboardProcessor
from static.squares import Squares
from static.positions import Positions
from static.pieces import Pieces
from move_validator import MoveValidator
from bitboard_helper import BitboardStorageHelper
import time

def transform_test(validator,
                   processor, 
                   board):
    side = np.bitwise_and(np.ulonglong(0b1), board.data["castling_check_color"])
    if side:
        side_pieces64_arr = board.data["w_pieces"]
        oppo_pieces64_arr = board.data["b_pieces"]
        side_pieces64 = board.data["all_w_pieces"]
        oppo_pieces64 = board.data["all_b_pieces"]
    else:
        side_pieces64_arr = board.data["b_pieces"]
        oppo_pieces64_arr = board.data["w_pieces"]
        side_pieces64 = board.data["all_b_pieces"]
        oppo_pieces64 = board.data["all_w_pieces"]
        
        
    
    valid, info = validator.is_valid(from_square_idx=Squares.input_to_sqr(squares[0])["idx"], 
                                    to_square_idx=Squares.input_to_sqr(squares[1])["idx"], 
                                    side=side,
                                    all_side_pieces64_arr=side_pieces64_arr,
                                    all_oppo_pieces64_arr=oppo_pieces64_arr,
                                    all_pieces64=board.data["all_pieces"],
                                    all_side_pieces64=side_pieces64,
                                    all_oppo_pieces64=oppo_pieces64,
                                    en_passant_squares64=np.ulonglong(0))
    
    if not valid:
        raise Exception("Invalid move!")
  
    
    if info["capture"]:
        oppo_captured_piece_type_idx = processor.get_piece_type_and_idx(not side, info["to_sqr_pos64"], oppo_pieces64_arr)[1]
        oppo_pieces64_arr[oppo_captured_piece_type_idx] = np.bitwise_xor(info["to_sqr_pos64"], oppo_pieces64_arr[oppo_captured_piece_type_idx])
        board.data["all_b_pieces"] = np.bitwise_or.reduce(oppo_pieces64_arr)
    
    board_change = np.bitwise_or(info["from_sqr_pos64"], info["to_sqr_pos64"])
    side_pieces64_arr[info["piece_type_idx"]] = np.bitwise_xor(side_pieces64_arr[info["piece_type_idx"]], board_change)
    side_pieces64 = np.bitwise_or.reduce(side_pieces64_arr)
    
    board.data["all_pieces"] = info["new_board_pos64"]

    if info["check"]:
        board.data["castling_check_color"] = np.bitwise_xor(np.ulonglong(0b01), board.data["castling_check_color"])
        board.data["castling_check_color"] = np.bitwise_or(np.ulonglong(0b10), board.data["castling_check_color"])
        return True
    
    board.data["side_to_move"] = np.bitwise_xor(np.ulonglong(0b01), board.data["castling_check_color"])
    return False

    

    



helper = BitboardStorageHelper()
test_board = Bitboard(Positions.start_pos())
masks_obj = BitboardMasks(helper_obj=helper)
processor_obj = BitboardProcessor(bb_masks_obj=masks_obj)
validator = MoveValidator(bb_masks_obj=masks_obj, bb_processor_obj=processor_obj)

is_check = False
while True:
    
    print("========WHITE ROOKS========")
    BitboardPrinter.print(test_board.data["w_pieces"][0])
    print("========WHITE KNIGHTS======")
    BitboardPrinter.print(test_board.data["w_pieces"][1])
    print("========WHITE BISHOPS=")
    BitboardPrinter.print(test_board.data["w_pieces"][2])
    print("========WHITE QUEENS=")
    BitboardPrinter.print(test_board.data["w_pieces"][3])
    print("========WHITE KINGS=")
    BitboardPrinter.print(test_board.data["w_pieces"][4])
    print("========WHITE PAWNS=")
    BitboardPrinter.print(test_board.data["w_pieces"][5])
    print("========BLACK ROOKS=")
    BitboardPrinter.print(test_board.data["b_pieces"][0])
    print("========BLACK KNIGHTS=")
    BitboardPrinter.print(test_board.data["b_pieces"][1])
    print("========BLACK BISHOPS=")
    BitboardPrinter.print(test_board.data["b_pieces"][2])
    print("========BLACK_QUEENS=")
    BitboardPrinter.print(test_board.data["b_pieces"][3])
    print("========BLACK_KING=")
    BitboardPrinter.print(test_board.data["b_pieces"][4])
    print("========BLACK PAWNS=")
    BitboardPrinter.print(test_board.data["b_pieces"][5])
    print("========WHITE PIECES=")
    BitboardPrinter.print(test_board.data["all_w_pieces"])
    print("========BLACK PIECES=")
    BitboardPrinter.print(test_board.data["all_b_pieces"])
    
    print(f"{'===== Check! =====' if is_check else ''}")
    print(f"========ALL PIECES========{'   Whites Turn' if np.bitwise_and(np.ulonglong(0b1), test_board.data['castling_check_color']) > 0 else '   Blacks Turn'}")
    BitboardPrinter.print(test_board.data, full_display=True)
    squares = input("Make a move:").lower().split()
    is_check = transform_test(validator, processor_obj, test_board)
    








