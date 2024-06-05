import numpy as np

from bitboard import Bitboard
from bitboard_printer import BitboardPrinter
from bitboard_storage import BitboardMasks
from static.squares import Squares
from static.positions import Positions
from static.pieces import Pieces
from move_validator import MoveValidator
from bitboard_helper import BitboardStorageHelper
import time

def transform_test(validator, board):
    validity = validator.is_valid(from_square=Squares.input_to_sqr(squares[0]), to_square=Squares.input_to_sqr(squares[1]), board_obj=test_board)
    
    if validity[0] and np.bitwise_and(np.ulonglong(0b1), board.data["side_to_move"]) > 0:
        b_pieces_arr_indx= validator.get_piece_type_idx_from_pos_mask(validity[4], board.data["B_Pieces_arr"])
        board.data["B_Pieces_arr"][b_pieces_arr_indx] = np.bitwise_xor(validity[4], board.data["B_Pieces_arr"][b_pieces_arr_indx])
        board.data["B_Pieces_mask"] = np.bitwise_or.reduce(board.data["B_Pieces_arr"])
 
    elif validity[0] and np.bitwise_and(np.ulonglong(0b1), board.data["side_to_move"]) == 0:
        w_pieces_arr_indx= validator.get_piece_type_idx_from_pos_mask(validity[4], board.data["W_Pieces_arr"])
        board.data["W_Pieces_arr"][w_pieces_arr_indx] = np.bitwise_xor(validity[4], board.data["W_Pieces_arr"][w_pieces_arr_indx])
        board.data["W_Pieces_mask"] = np.bitwise_or.reduce(board.data["W_Pieces_arr"])

    if np.bitwise_and(np.ulonglong(0b1), board.data["side_to_move"]) > 0:
        
        change = np.bitwise_or(validity[3], validity[4])
        board.data["W_Pieces_arr"][validity[5]] = np.bitwise_xor(board.data["W_Pieces_arr"][validity[5]], change)
        board.data["W_Pieces_mask"] = np.bitwise_or.reduce(board.data["W_Pieces_arr"])
    
    else:
        change = np.bitwise_or(validity[3], validity[4])
        idx = -1 * validity[5] if validity[5] < 0 else validity[5]
        board.data["B_Pieces_arr"][idx] = np.bitwise_xor(board.data["B_Pieces_arr"][idx], change)
        board.data["B_Pieces_mask"] = np.bitwise_or.reduce(board.data["B_Pieces_arr"])
    
        

    if validity[1]:
        board.data["side_to_move"] = np.bitwise_xor(np.ulonglong(0b01), board.data["side_to_move"])
        board.data["side_to_move"] = np.bitwise_or(np.ulonglong(0b10), board.data["side_to_move"])
        board.data["All_Pieces_mask"] = validity[2]
        return validity[1]
    
    board.data["side_to_move"] = np.bitwise_xor(np.ulonglong(0b01), board.data["side_to_move"])
    board.data["All_Pieces_mask"] = validity[2]
    

    



helper = BitboardStorageHelper()
test_board = Bitboard(Positions.start_pos())
masks_obj = BitboardMasks(helper_obj=helper)
validator = MoveValidator(bb_masks_obj=masks_obj)
# is_capture, is_check, updated_all_pieces_pos64,  from_sqr_piece_pos64, to_sqr_piece_pos64,
is_check = False
while True:
    try:
        print("========WHITE ROOKS========")
        BitboardPrinter.print(test_board.data["W_Pieces_arr"][0])
        print("========WHITE KNIGHTS======")
        BitboardPrinter.print(test_board.data["W_Pieces_arr"][1])
        print("========WHITE BISHOPS======")
        BitboardPrinter.print(test_board.data["W_Pieces_arr"][2])
        print("========WHITE QUEEN======")
        BitboardPrinter.print(test_board.data["W_Pieces_arr"][3])
        print("========WHITE KING======")
        BitboardPrinter.print(test_board.data["W_Pieces_arr"][4])
        print("========WHITE PAWNS======")
        BitboardPrinter.print(test_board.data["W_Pieces_arr"][5])
        print("========BLACK ROOKS======")
        BitboardPrinter.print(test_board.data["B_Pieces_arr"][0])
        print("========BLACK KNIGHTS======")
        BitboardPrinter.print(test_board.data["B_Pieces_arr"][1])
        print("========BLACK BISHOPS======")
        BitboardPrinter.print(test_board.data["B_Pieces_arr"][2])
        print("========BLACK QUEEN======")
        BitboardPrinter.print(test_board.data["B_Pieces_arr"][3])
        print("========BLACK KING======")
        BitboardPrinter.print(test_board.data["B_Pieces_arr"][4])
        print("========BLACK PAWNS======")
        BitboardPrinter.print(test_board.data["B_Pieces_arr"][5])

        print("========WHITE PIECES========")
        BitboardPrinter.print(test_board.data["W_Pieces_mask"])

        print("========BLACK PIECES========")
        BitboardPrinter.print(test_board.data["B_Pieces_mask"])


        print(f"{'===== Check! =====' if is_check else ''}")
        print(f"========ALL PIECES========{'   Whites Turn' if np.bitwise_and(np.ulonglong(0b1), test_board.data['side_to_move']) > 0 else '   Blacks Turn'}")
        BitboardPrinter.print(test_board.data, full_display=True)

        squares = input("Make a move:").lower().split()
        is_check = transform_test(validator, test_board)
    except Exception as ex:
        print(str(ex))
        time.sleep(2)







