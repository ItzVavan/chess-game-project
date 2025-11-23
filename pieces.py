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
