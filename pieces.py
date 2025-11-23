class Piece:

    
    def __init__(self, color, pos):
        assert color in ['white', 'black'], "Цвет должен быть white или black"
        assert len(pos) == 2, "Позиция должна быть кортежем (row, col)"
        
        self.color = color
        self.pos = pos
        self._has_moved = False
        self.name = self.__class__.__name__
        print(f"✅ Создана фигура {self.name} {self.color} на {pos}, has_moved={self._has_moved}")
    
    @property
    def has_moved(self):
        return self._has_moved
    
    @has_moved.setter
    def has_moved(self, value):
        if value != self._has_moved:
            import traceback
            print(f"\n⚠️ ИЗМЕНЕНИЕ has_moved для {self.name} {self.color} на {self.pos}")
            print(f"   Было: {self._has_moved} → Стало: {value}")
            print("   Вызвано из:")
            traceback.print_stack(limit=5)
        self._has_moved = value
    
    def get_valid_moves(self, board):
        raise NotImplementedError("Каждая фигура должна реализовать этот метод")



class Pawn(Piece):
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.pos
        direction = -1 if self.color == 'white' else 1

        starting_row = 6 if self.color == 'white' else 1

        new_row = row + direction
        if board.is_valid_pos((new_row, col)) and board.get_piece((new_row, col)) is None:
            moves.append((new_row, col))

            if row == starting_row:
                new_row2 = row + 2 * direction
                if board.get_piece((new_row2, col)) is None:
                    moves.append((new_row2, col))

        for dc in [-1, 1]:
            new_pos = (row + direction, col + dc)
            if board.is_valid_pos(new_pos):
                target = board.get_piece(new_pos)
                if target and target.color != self.color:
                    moves.append(new_pos)
        
        return moves



class Rook(Piece):
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.pos
        

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_pos = (row + dr * i, col + dc * i)
                if not board.is_valid_pos(new_pos):
                    break
                
                target = board.get_piece(new_pos)
                if target is None:
                    moves.append(new_pos)
                elif target.color != self.color:
                    moves.append(new_pos)
                    break
                else:
                    break
        
        return moves


class Knight(Piece):
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.pos
        

        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_pos = (row + dr, col + dc)
            if board.is_valid_pos(new_pos):
                target = board.get_piece(new_pos)
                if target is None or target.color != self.color:
                    moves.append(new_pos)
        
        return moves


class Bishop(Piece):
    
    def get_valid_moves(self, board):

        moves = []
        row, col = self.pos
        

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_pos = (row + dr * i, col + dc * i)
                if not board.is_valid_pos(new_pos):
                    break
                
                target = board.get_piece(new_pos)
                if target is None:
                    moves.append(new_pos)
                elif target.color != self.color:
                    moves.append(new_pos)
                    break
                else:
                    break
        
        return moves
class Queen(Piece):

    
    def get_valid_moves(self, board):

        moves = []
        row, col = self.pos
        

        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_pos = (row + dr * i, col + dc * i)
                if not board.is_valid_pos(new_pos):
                    break
                
                target = board.get_piece(new_pos)
                if target is None:
                    moves.append(new_pos)
                elif target.color != self.color:
                    moves.append(new_pos)
                    break
                else:
                    break
        
        return moves


class King(Piece):

    
    def get_valid_moves(self, board):

        moves = []
        row, col = self.pos
        

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if board.is_valid_pos(new_pos):
                target = board.get_piece(new_pos)
                if target is None or target.color != self.color:
                    moves.append(new_pos)
        

        print(f"\n=== ПРОВЕРКА РОКИРОВКИ для {self.color} короля ===")
        print(f"Король на позиции: {self.pos}")
        print(f"has_moved: {self.has_moved}")
        print(f"Король под шахом: {board.is_check(self.color)}")
        
        if not self.has_moved and not board.is_check(self.color):
            print(" Король не двигался и не под шахом")
            

            print("\n--- Проверка КОРОТКОЙ рокировки ---")
            can_castle_short = self._can_castle_kingside(board)
            print(f"Короткая рокировка: {' ВОЗМОЖНА' if can_castle_short else ' НЕВОЗМОЖНА'}")
            if can_castle_short:
                moves.append((row, col + 2))
            

            print("\n--- Проверка ДЛИННОЙ рокировки ---")
            can_castle_long = self._can_castle_queenside(board)
            print(f"Длинная рокировка: {' ВОЗМОЖНА' if can_castle_long else ' НЕВОЗМОЖНА'}")
            if can_castle_long:
                moves.append((row, col - 2))
        else:
            print(" Рокировка невозможна (король двигался или под шахом)")
        
        print(f"Всего ходов короля: {len(moves)}")
        print("="*50)
        
        return moves
    
    def _can_castle_kingside(self, board):

        row, col = self.pos
        

        rook_pos = (row, 7)
        rook = board.get_piece(rook_pos)
        
        print(f"  Ладья на {rook_pos}: {rook}")
        if not rook:
            print(f"   Ладьи нет на {rook_pos}")
            return False
        print(f"  Ладья: {rook.name}, has_moved: {rook.has_moved}")
        
        if rook.name != 'Rook':
            print(f"   Это не ладья: {rook.name}")
            return False
        
        if rook.has_moved:
            print(f"   Ладья уже двигалась")
            return False
        

        print(f"  Проверка клеток между {col+1} и 7:")
        for c in range(col + 1, 7):
            piece = board.get_piece((row, c))
            print(f"    Клетка ({row}, {c}): {piece if piece else 'пусто'}")
            if piece is not None:
                print(f"   Клетка ({row}, {c}) занята")
                return False
        

        print(f"  Проверка атакованных клеток:")
        for c in range(col, col + 3):
            attacked = self._is_square_attacked_safe(board, (row, c))
            print(f"    Клетка ({row}, {c}): {' АТАКОВАНА' if attacked else ' безопасна'}")
            if attacked:
                return False
        
        return True
    
    def _can_castle_queenside(self, board):
        """Проверка возможности длинной рокировки"""
        row, col = self.pos
        

        rook_pos = (row, 0)
        rook = board.get_piece(rook_pos)
        
        print(f"  Ладья на {rook_pos}: {rook}")
        if not rook:
            print(f"   Ладьи нет на {rook_pos}")
            return False
        print(f"  Ладья: {rook.name}, has_moved: {rook.has_moved}")
        
        if rook.name != 'Rook':
            print(f"   Это не ладья: {rook.name}")
            return False
        
        if rook.has_moved:
            print(f"   Ладья уже двигалась")
            return False
        

        print(f"  Проверка клеток между 1 и {col}:")
        for c in range(1, col):
            piece = board.get_piece((row, c))
            print(f"    Клетка ({row}, {c}): {piece if piece else 'пусто'}")
            if piece is not None:
                print(f"   Клетка ({row}, {c}) занята")
                return False
        

        print(f"  Проверка атакованных клеток:")
        for c in range(col - 2, col + 1):
            attacked = self._is_square_attacked_safe(board, (row, c))
            print(f"    Клетка ({row}, {c}): {' АТАКОВАНА' if attacked else ' безопасна'}")
            if attacked:
                return False
        
        return True
    
    def _is_square_attacked_safe(self, board, square):
        """Проверка атаки БЕЗ рекурсии"""
        opponent_color = 'black' if self.color == 'white' else 'white'
        sq_row, sq_col = square
        

        pawn_dir = 1 if opponent_color == 'white' else -1
        for dc in [-1, 1]:
            pr, pc = sq_row - pawn_dir, sq_col + dc
            if board.is_valid_pos((pr, pc)):
                piece = board.get_piece((pr, pc))
                if piece and piece.name == 'Pawn' and piece.color == opponent_color:
                    return True
        

        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            nr, nc = sq_row + dr, sq_col + dc
            if board.is_valid_pos((nr, nc)):
                piece = board.get_piece((nr, nc))
                if piece and piece.name == 'Knight' and piece.color == opponent_color:
                    return True
        

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = sq_row + dr, sq_col + dc
                if board.is_valid_pos((nr, nc)):
                    piece = board.get_piece((nr, nc))
                    if piece and piece.name == 'King' and piece.color == opponent_color:
                        return True
        

        diagonal_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in diagonal_dirs:
            for dist in range(1, 8):
                nr, nc = sq_row + dr * dist, sq_col + dc * dist
                if not board.is_valid_pos((nr, nc)):
                    break
                piece = board.get_piece((nr, nc))
                if piece:
                    if piece.color == opponent_color and piece.name in ['Bishop', 'Queen']:
                        return True
                    break
        

        straight_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in straight_dirs:
            for dist in range(1, 8):
                nr, nc = sq_row + dr * dist, sq_col + dc * dist
                if not board.is_valid_pos((nr, nc)):
                    break
                piece = board.get_piece((nr, nc))
                if piece:
                    if piece.color == opponent_color and piece.name in ['Rook', 'Queen']:
                        return True
                    break
        
        return False
