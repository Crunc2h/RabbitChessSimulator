class BitboardPrinter:
    
    @staticmethod
    def position_to_str(board, full_display=False):

        if full_display:
            w_r = format(board["W_Pieces_arr"][0], "#b")[2::].zfill(64)[::-1]
            w_n = format(board["W_Pieces_arr"][1], "#b")[2::].zfill(64)[::-1]
            w_b = format(board["W_Pieces_arr"][2], "#b")[2::].zfill(64)[::-1]
            w_q = format(board["W_Pieces_arr"][3], "#b")[2::].zfill(64)[::-1]
            w_k = format(board["W_Pieces_arr"][4], "#b")[2::].zfill(64)[::-1]
            w_p = format(board["W_Pieces_arr"][5], "#b")[2::].zfill(64)[::-1]
            b_r = format(board["B_Pieces_arr"][0], "#b")[2::].zfill(64)[::-1]
            b_n = format(board["B_Pieces_arr"][1], "#b")[2::].zfill(64)[::-1]
            b_b = format(board["B_Pieces_arr"][2], "#b")[2::].zfill(64)[::-1]
            b_q = format(board["B_Pieces_arr"][3], "#b")[2::].zfill(64)[::-1]
            b_k = format(board["B_Pieces_arr"][4], "#b")[2::].zfill(64)[::-1]
            b_p = format(board["B_Pieces_arr"][5], "#b")[2::].zfill(64)[::-1]

            binary_as_str = BitboardPrinter.overwrite_str("0" * 64, w_r, "r")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, w_n, "n")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, w_b, "b")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, w_q, "q")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, w_k, "k")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, w_p, "p")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, b_r, "R")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, b_n, "N")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, b_b, "B")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, b_q, "Q")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, b_k, "K")
            binary_as_str = BitboardPrinter.overwrite_str(binary_as_str, b_p, "P")
        else:
            binary_as_str = format(board, "#b")[2::].zfill(64)[::-1]
        
        
        res = "\n\n"
        
        for i in range(len(binary_as_str), 0, -1):
            if i % 8 == 0 and i != 0:
                res += f"{int(i / 8)}   "
            res += f"{binary_as_str[i - 1]} "
            
            if (i - 1) % 8 == 0:
                res += "\n"
            if i == 1:
                res += "\n    a b c d e f g h\n\n"
        
        return res
    
    @staticmethod
    def print(board, full_display=False):
        print(BitboardPrinter.position_to_str(board, full_display))

    @staticmethod
    def overwrite_str(str1, str2, overwrite_char):
        res= ""
        for i in range(len(str1)):
            if str1[i] == "0" and str2[i] != "0":
                res += overwrite_char
            else:
                res += str1[i]
        return res