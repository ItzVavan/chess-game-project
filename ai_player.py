import math


class ChessAI:

    def __init__(self, depth=3, color='black'):
        assert depth > 0
        assert color in ['white', 'black']

        self.depth = depth
        self.color = color
        self.opponent_color = 'white' if color == 'black' else 'black'
        self.nodes_evaluated = 0

        self.transposition_table = {}

        self.piece_values = {
            'Pawn': 100,
            'Knight': 320,
            'Bishop': 330,
            'Rook': 500,
            'Queen': 900,
            'King': 20000
        }

        self.pawn_table = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.knight_table = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20, 0, 0, 0, 0, -20, -40],
            [-30, 0, 10, 15, 15, 10, 0, -30],
            [-30, 5, 15, 20, 20, 15, 5, -30],
            [-30, 0, 15, 20, 20, 15, 0, -30],
            [-30, 5, 10, 15, 15, 10, 5, -30],
            [-40, -20, 0, 5, 5, 0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ]

        self.king_table = [
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [20, 20, 0, 0, 0, 0, 20, 20],
            [20, 30, 10, 0, 0, 10, 30, 20]
        ]

    def get_best_move(self, board):
        self.nodes_evaluated = 0
        self.transposition_table.clear()

        best_move = None
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf

        possible_moves = self._get_all_possible_moves(board, self.color)

        if not possible_moves:
            return None

        possible_moves = self._order_moves_smart(board, possible_moves)

        for from_pos, to_pos in possible_moves:
            piece = board.get_piece(from_pos)
            captured = board.get_piece(to_pos)
            old_pos = piece.pos
            old_has_moved = piece.has_moved

            old_rook_state = None
            if piece.name == 'King' and abs(to_pos[1] - from_pos[1]) == 2:
                row = from_pos[0]
                if to_pos[1] > from_pos[1]:
                    rook = board.get_piece((row, 7))
                    old_rook_state = (rook.pos, rook.has_moved) if rook else None
                else:
                    rook = board.get_piece((row, 0))
                    old_rook_state = (rook.pos, rook.has_moved) if rook else None

            board.move_piece(from_pos, to_pos)

            is_capture = captured is not None
            search_depth = self.depth if not is_capture else self.depth + 1

            value = self._minimax_optimized(board, search_depth - 1, alpha, beta, False)

            board.set_piece(from_pos, piece)
            board.set_piece(to_pos, captured)
            piece.pos = old_pos
            piece.has_moved = old_has_moved

            if old_rook_state:
                row = from_pos[0]
                if to_pos[1] > from_pos[1]:  # Короткая
                    rook = board.get_piece((row, 5))
                    if rook:
                        board.set_piece((row, 7), rook)
                        board.set_piece((row, 5), None)
                        rook.pos, rook.has_moved = old_rook_state
                else:
                    rook = board.get_piece((row, 3))
                    if rook:
                        board.set_piece((row, 0), rook)
                        board.set_piece((row, 3), None)
                        rook.pos, rook.has_moved = old_rook_state

            if value > best_value:
                best_value = value
                best_move = (from_pos, to_pos)

            alpha = max(alpha, value)

            if beta <= alpha:
                break

        print(f"AI: {self.nodes_evaluated} позиций, оценка: {best_value}")
        return best_move

    def _minimax_optimized(self, board, depth, alpha, beta, is_maximizing):
        self.nodes_evaluated += 1

        board_hash = self._get_board_hash(board)
        if board_hash in self.transposition_table:
            cached_depth, cached_value = self.transposition_table[board_hash]
            if cached_depth >= depth:
                return cached_value

        if depth == 0:
            eval_score = self._evaluate_board_fast(board)
            self.transposition_table[board_hash] = (depth, eval_score)
            return eval_score

        color = self.color if is_maximizing else self.opponent_color

        if board.is_checkmate(color):
            return -20000 if is_maximizing else 20000

        possible_moves = self._get_all_possible_moves(board, color)

        if not possible_moves:
            return 0

        possible_moves = self._order_moves_smart(board, possible_moves)

        if is_maximizing:
            max_eval = -math.inf
            for from_pos, to_pos in possible_moves:
                piece = board.get_piece(from_pos)
                captured = board.get_piece(to_pos)
                old_pos = piece.pos
                board.move_piece(from_pos, to_pos)

                eval = self._minimax_optimized(board, depth - 1, alpha, beta, False)

                board.set_piece(from_pos, piece)
                board.set_piece(to_pos, captured)
                piece.pos = old_pos

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break

            self.transposition_table[board_hash] = (depth, max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for from_pos, to_pos in possible_moves:
                piece = board.get_piece(from_pos)
                captured = board.get_piece(to_pos)
                old_pos = piece.pos
                board.move_piece(from_pos, to_pos)

                eval = self._minimax_optimized(board, depth - 1, alpha, beta, True)

                board.set_piece(from_pos, piece)
                board.set_piece(to_pos, captured)
                piece.pos = old_pos

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break

            self.transposition_table[board_hash] = (depth, min_eval)
            return min_eval

    def _evaluate_board_fast(self, board):
        score = 0

        # Только материал и простые позиционные бонусы
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece:
                    piece_value = self._get_piece_value_fast(piece, row, col)

                    if piece.color == self.color:
                        score += piece_value
                    else:
                        score -= piece_value

        return score

    def _get_piece_value_fast(self, piece, row, col):
        base_value = self.piece_values[piece.name]
        positional_bonus = 0

        if piece.name == 'Pawn':
            positional_bonus = self.pawn_table[row if piece.color == 'white' else 7 - row][col]
        elif piece.name == 'Knight':
            positional_bonus = self.knight_table[row][col]
        elif piece.name == 'King':
            positional_bonus = self.king_table[row if piece.color == 'white' else 7 - row][col]

        return base_value + positional_bonus

    def _get_board_hash(self, board):
        board_str = ""
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece:
                    board_str += f"{piece.name[0]}{piece.color[0]}"
                else:
                    board_str += "."
        return hash(board_str)

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

    def _order_moves_smart(self, board, moves):

        def move_priority(move):
            from_pos, to_pos = move
            score = 0

            piece = board.get_piece(from_pos)
            target = board.get_piece(to_pos)

            if piece.name == 'King' and abs(to_pos[1] - from_pos[1]) == 2:
                score += 5000

            if target:
                score += 10000 + self.piece_values[target.name] - self.piece_values[piece.name] // 10

            row, col = to_pos
            if 3 <= row <= 4 and 3 <= col <= 4:
                score += 50
            elif 2 <= row <= 5 and 2 <= col <= 5:
                score += 20

            if piece.name in ['Knight', 'Bishop'] and not piece.has_moved:
                score += 30

            return score

        return sorted(moves, key=move_priority, reverse=True)
