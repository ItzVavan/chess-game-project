from pieces import Rook, Knight, Bishop, Queen, King, Pawn

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_king_pos = None
        self.black_king_pos = None
        self.setup_pieces()
    
    def setup_pieces(self):
        # Черные
        self.board[0][0] = Rook('black', (0, 0))
        self.board[0][1] = Knight('black', (0, 1))
        self.board[0][2] = Bishop('black', (0, 2))
        self.board[0][3] = Queen('black', (0, 3))
        self.board[0][4] = King('black', (0, 4))
        self.board[0][5] = Bishop('black', (0, 5))
        self.board[0][6] = Knight('black', (0, 6))
        self.board[0][7] = Rook('black', (0, 7))
        for col in range(8):
            self.board[1][col] = Pawn('black', (1, col))
        
        # Белые
        self.board[7][0] = Rook('white', (7, 0))
        self.board[7][1] = Knight('white', (7, 1))
        self.board[7][2] = Bishop('white', (7, 2))
        self.board[7][3] = Queen('white', (7, 3))
        self.board[7][4] = King('white', (7, 4))
        self.board[7][5] = Bishop('white', (7, 5))
        self.board[7][6] = Knight('white', (7, 6))
        self.board[7][7] = Rook('white', (7, 7))
        for col in range(8):
            self.board[6][col] = Pawn('white', (6, col))
        
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
    
    def get_piece(self, pos):
        row, col = pos
        return self.board[row][col]
    
    def set_piece(self, pos, piece):
        row, col = pos
        self.board[row][col] = piece
        if piece and piece.name == 'King':
            if piece.color == 'white':
                self.white_king_pos = pos
            else:
                self.black_king_pos = pos
    
    def is_valid_pos(self, pos):
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8
    def move_piece(self, from_pos, to_pos):
        piece = self.get_piece(from_pos)
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        

        if piece.name == 'King' and abs(to_col - from_col) == 2:
            self.set_piece(to_pos, piece)
            self.set_piece(from_pos, None)
            piece.pos = to_pos
            piece.has_moved = True
            
            if to_col > from_col:
                rook = self.get_piece((from_row, 7))
                self.set_piece((from_row, 5), rook)
                self.set_piece((from_row, 7), None)
                rook.pos = (from_row, 5)
                rook.has_moved = True
            else:
                rook = self.get_piece((from_row, 0))
                self.set_piece((from_row, 3), rook)
                self.set_piece((from_row, 0), None)
                rook.pos = (from_row, 3)
                rook.has_moved = True
        else:
            self.set_piece(to_pos, piece)
            self.set_piece(from_pos, None)
            piece.pos = to_pos
            piece.has_moved = True
    def is_check(self, color):
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        if not king_pos:
            return False
        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    if piece.name == 'King':
                        if abs(row - king_pos[0]) <= 1 and abs(col - king_pos[1]) <= 1:
                            return True
                    else:
                        if king_pos in piece.get_valid_moves(self):
                            return True
        return False
    
    def is_checkmate(self, color):
        if not self.is_check(color):
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for move in piece.get_valid_moves(self):
                        if self.is_legal_move((row, col), move, color):
                            return False
        return True
    
    def is_stalemate(self, color):
        if self.is_check(color):
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for move in piece.get_valid_moves(self):
                        if self.is_legal_move((row, col), move, color):
                            return False
        return True
    def is_legal_move(self, from_pos, to_pos, color):
        piece = self.get_piece(from_pos)
        captured = self.get_piece(to_pos)
        old_pos = piece.pos
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        

        is_castling = piece.name == 'King' and abs(to_col - from_col) == 2
        
        if is_castling:

            direction = 1 if to_col > from_col else -1
            

            if self.is_check(color):
                return False
            

            for step in range(1, 3):
                intermediate_col = from_col + step * direction
                self.set_piece((from_row, intermediate_col), piece)
                self.set_piece(from_pos if step == 1 else (from_row, from_col + (step-1)*direction), None)
                piece.pos = (from_row, intermediate_col)
                
                if self.is_check(color):
                    # Откатываем
                    self.set_piece(from_pos, piece)
                    for c in range(min(from_col, to_col), max(from_col, to_col) + 1):
                        if c != from_col:
                            self.set_piece((from_row, c), None)
                    piece.pos = old_pos
                    return False
            

            self.set_piece(from_pos, piece)
            self.set_piece(to_pos, None)
            piece.pos = old_pos
            return True
        

        self.set_piece(to_pos, piece)
        self.set_piece(from_pos, None)
        piece.pos = to_pos
        
        in_check = self.is_check(color)
        
        self.set_piece(from_pos, piece)
        self.set_piece(to_pos, captured)
        piece.pos = old_pos
        
        return not in_check

