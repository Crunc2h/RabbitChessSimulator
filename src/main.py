import time
import os
import copy
from bitboard import Bitboard
from bitboard_printer import BitboardPrinter
from bitboard_storage import BitboardMasks
from bitboard_processor import BitboardProcessor
from static.positions import Positions
from move_validator import MoveValidator
from bitboard_helper import BitboardStorageHelper
from board_transformer import BoardTransformer

def tst(test_board):
    print("========WHITE ROOKS========")
    BitboardPrinter.print(test_board.w_pieces[0])
    print("========WHITE KNIGHTS======")
    BitboardPrinter.print(test_board.w_pieces[1])
    print("========W_BISHOP===")
    BitboardPrinter.print(test_board.w_pieces[2])
    print("=======W_QUEEN")
    BitboardPrinter.print(test_board.w_pieces[3])
    print("======W_KING")
    BitboardPrinter.print(test_board.w_pieces[4])
    print("======W_PAWN==")
    BitboardPrinter.print(test_board.w_pieces[5])
    print("========BLACK ROOKS=")
    BitboardPrinter.print(test_board.b_pieces[0])
    print("=======B_KNIGHT==")
    BitboardPrinter.print(test_board.b_pieces[1])
    print("=======B_BISHOP=====")
    BitboardPrinter.print(test_board.b_pieces[2])
    print("======B_QUEEN==========")
    BitboardPrinter.print(test_board.b_pieces[3])
    print("====B_KING========")
    BitboardPrinter.print(test_board.b_pieces[4])
    print("=====B_PAWNS=======")
    BitboardPrinter.print(test_board.b_pieces[5])
    print("========WHITE PIECES=")
    BitboardPrinter.print(test_board.w_pieces_mask)
    print("========BLACK PIECES=")
    BitboardPrinter.print(test_board.b_pieces_mask)
    
    
    print(f"{'===== Check! =====' if test_board.is_check.bit_count() > 0 else ''}")
    print(f"========BOARD========{'   Whites Turn' if test_board.is_white.bit_count() > 0 else '   Blacks Turn'}")
    BitboardPrinter.print(test_board.all_pieces_mask, full_display=False)

def game_loop(board):
    helper = BitboardStorageHelper()
    masks_obj = BitboardMasks(helper_obj=helper)
    processor_obj = BitboardProcessor(bb_masks_obj=masks_obj)
    validator = MoveValidator(bb_masks_obj=masks_obj, bb_processor_obj=processor_obj)
    transformer = BoardTransformer(bb_processor_obj=processor_obj)
    move_count = 0
    
    is_check = False
    while True:
        os.system('clear')
        print(move_count)
        side = board.is_white.bit_count() > 0
        print(side)
        print(f"{'===== Check! =====' if is_check else ''}")
        print(f"========BOARD========{'   Whites Turn' if side else '   Blacks Turn'}")
        
        if side:
            side_pieces = board.w_pieces
            oppo_pieces = board.b_pieces
            side_pieces_mask = board.w_pieces_mask
            oppo_pieces_mask = board.b_pieces_mask
        else:
            side_pieces = board.w_pieces
            oppo_pieces = board.b_pieces
            side_pieces_mask = board.w_pieces_mask
            oppo_pieces_mask = board.b_pieces_mask
        
        valid_moves = validator.generate_valid_moves(side=side,
                                                     side_pieces=side_pieces,
                                                     oppo_pieces=oppo_pieces,
                                                     side_pieces_mask=side_pieces_mask,
                                                     oppo_pieces_mask=oppo_pieces_mask,
                                                     all_pieces_mask=board.all_pieces_mask,
                                                     en_passant_squares=board.en_passant_squares)
        tst(board)
        if is_check and len(valid_moves.keys()) == 0:
            print(f"CHECK MATE! {'White' if not side else 'Black'} Wins!")
            time.sleep(5)
            break
        
        if ((is_check == False and len(valid_moves.keys()) == 0) or
            (is_check == False and board.all_pieces_mask.bit_count() == 2) or
            (is_check == False and board.all_pieces_mask.bit_count() == 3 and side_pieces[0].bit_count() == 0 and side_pieces[3].bit_count() == 0 and oppo_pieces[0].bit_count() == 0 and oppo_pieces[3].bit_count() == 0) or
            (is_check == False and board.all_pieces_mask.bit_count() == 4 and side_pieces[1].bit_count() == 1 and oppo_pieces[1].bit_count() == 1) or
            (is_check == False and board.all_pieces_mask.bit_count() == 4 and side_pieces[5].bit_count() == 1 and oppo_pieces[5].bit_count() == 1)):
            print("STALEMATE!")
            time.sleep(5)
            break
        
        [print(valid_move) for valid_move in valid_moves.keys()]
        squares = input("Ur move:").split()
        move_info = valid_moves[f"{squares[0]} -> {squares[1]}"]
        is_check = move_info.is_check
        transformer.transform_board(board=test_board,
                                    info=move_info)
        move_count += 1


test_board = Bitboard(copy.deepcopy(Positions.start_pos()))
game_loop(test_board)




