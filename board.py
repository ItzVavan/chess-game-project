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
    
