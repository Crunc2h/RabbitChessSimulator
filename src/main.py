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
from board_transformer import BoardTransformer
import time
import os


def game_loop():
    helper = BitboardStorageHelper()
    test_board = Bitboard(Positions.start_pos())
    masks_obj = BitboardMasks(helper_obj=helper)
    processor_obj = BitboardProcessor(bb_masks_obj=masks_obj)
    validator = MoveValidator(bb_masks_obj=masks_obj, bb_processor_obj=processor_obj)
    transformer = BoardTransformer(bb_processor_obj=processor_obj)

    is_check = False
    while True:
        os.system('clear')
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

        side = bool(np.bitwise_and(np.ulonglong(1), test_board.data["castling_check_color"]))
        if side:
            side_pieces64_arr = test_board.data["w_pieces"]
            oppo_pieces64_arr = test_board.data["b_pieces"]
            side_pieces64 = test_board.data["all_w_pieces"]
            oppo_pieces64 = test_board.data["all_b_pieces"]
        else:
            side_pieces64_arr = test_board.data["b_pieces"]
            oppo_pieces64_arr = test_board.data["w_pieces"]
            side_pieces64 = test_board.data["all_b_pieces"]
            oppo_pieces64 = test_board.data["all_w_pieces"]

        valid_moves = validator.generate_valid_moves(side=side,
                                                     all_side_pieces64_arr=side_pieces64_arr,
                                                     all_oppo_pieces64_arr=oppo_pieces64_arr,
                                                     all_pieces64=test_board.data["all_pieces"],
                                                     all_side_pieces64=side_pieces64,
                                                     all_oppo_pieces64=oppo_pieces64)
        if is_check and len(valid_moves.keys()) == 0:
            print(f"CHECK MATE! {'White' if not side else 'Black'} Wins!")
            break
        if is_check == False and len(valid_moves.keys()) == 0:
            print("STALEMATE!")
            break
        
        for valid_move in valid_moves.keys():
            print(f"* {valid_move}")

        squares = input("Make a move:").lower().split()
        move_key = f"{squares[0].lower()} -> {squares[1].lower()}" 

        if move_key in valid_moves.keys():                                                     
            move_info = valid_moves[move_key]
            is_check = move_info["check"]
            transformer.transform_board(board=test_board,
                                        info=move_info,
                                        side_pieces64_arr=side_pieces64_arr,
                                        oppo_pieces64_arr=oppo_pieces64_arr)
        else:
            print("Invalid Move!")
            time.sleep(2)


game_loop()








