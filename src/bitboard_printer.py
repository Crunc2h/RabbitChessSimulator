class BitboardPrinter:
    
    @staticmethod
    def position_to_str(board):
        
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
    def print(board):
        print(BitboardPrinter.position_to_str(board))