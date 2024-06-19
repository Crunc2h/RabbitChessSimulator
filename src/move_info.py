class MoveInfo:
    def __init__(self,
                 is_white,
                 is_capture,
                 is_check,
                 from_sqr_pos64,
                 to_sqr_pos64,
                 updated_board,
                 piece_type_idx):
        self.is_white = is_white
        self.is_capture = is_capture
        self.is_check = is_check
        self.from_sqr_pos64 = from_sqr_pos64
        self.to_sqr_pos64 = to_sqr_pos64
        self.updated_board = updated_board
        self.piece_type_idx = piece_type_idx
