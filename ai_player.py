class ChessAI:

    def __init__(self, depth=3, color='black'):
        self.depth = depth
        self.color = color
        self.opponent_color = 'white' if color == 'black' else 'black'

        self.piece_values = {
            'Pawn': 100,
            'Knight': 320,
            'Bishop': 330,
            'Rook': 500,
            'Queen': 900,
            'King': 20000
        }

    def get_best_move(self, board):
        possible_moves = self._get_all_possible_moves(board, self.color)
        return possible_moves[0] if possible_moves else None

    def _get_all_possible_moves(self, board, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color == color:
                    valid_moves = piece.get_valid_moves(board)
                    for move in valid_moves:
                        if board.is_legal_move((row, col), move, color):
                            moves.append(((row, col), move))
        return moves