import pygame
from board import Board
from ai_player import ChessAI

class Game:
    """Класс управления игрой с AI"""
    
    def __init__(self, screen, ai_enabled=True, ai_color='black', ai_depth=3):
        self.screen = screen
        self.board = Board()
        self.selected_piece = None
        self.selected_pos = None
        self.valid_moves = []
        self.current_turn = 'white'
        self.game_over = False
        self.winner = None
        

        self.ai_enabled = ai_enabled
        self.ai = ChessAI(depth=ai_depth, color=ai_color) if ai_enabled else None
        self.ai_thinking = False
        
        self.WHITE = (238, 238, 210)
        self.BLACK = (118, 150, 86)
        self.HIGHLIGHT = (186, 202, 68)
        self.VALID_MOVE = (246, 246, 130)
        
        self.SQUARE_SIZE = 100
        
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
    
    def handle_click(self, pos):
        """Обработка клика мыши"""
        if self.game_over or self.ai_thinking:
            return
        
        if self.ai_enabled and self.current_turn == self.ai.color:
            return
        
        col = pos[0] // self.SQUARE_SIZE
        row = pos[1] // self.SQUARE_SIZE
        
        if not self.board.is_valid_pos((row, col)):
            return
        
        clicked_piece = self.board.get_piece((row, col))
        
        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self._make_move(self.selected_pos, (row, col))
            
            elif clicked_piece and clicked_piece.color == self.current_turn:
                self.select_piece((row, col), clicked_piece)
            else:
                self.selected_piece = None
                self.selected_pos = None
                self.valid_moves = []
        
        elif clicked_piece and clicked_piece.color == self.current_turn:
            self.select_piece((row, col), clicked_piece)
    
    def _make_move(self, from_pos, to_pos):
        """Выполнить ход с проверкой мата и пата"""
        self.board.move_piece(from_pos, to_pos)
        
        piece = self.board.get_piece(to_pos)
        if piece.name == 'Pawn':
            row, col = to_pos
            if (row == 0 and self.current_turn == 'white') or \
            (row == 7 and self.current_turn == 'black'):
                from pieces import Queen
                self.board.set_piece(to_pos, Queen(self.current_turn, to_pos))
        
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        
        if self.board.is_checkmate(self.current_turn):
            self.game_over = True
            self.winner = 'Белые' if self.current_turn == 'black' else 'Черные'
        
        elif self.board.is_stalemate(self.current_turn):
            self.game_over = True
            self.winner = 'Ничья (Пат)'
        
        self.selected_piece = None
        self.selected_pos = None
        self.valid_moves = []

    
    def select_piece(self, pos, piece):
        """Выбрать фигуру и показать валидные ходы"""
        self.selected_piece = piece
        self.selected_pos = pos
        
        all_moves = piece.get_valid_moves(self.board)
        
        self.valid_moves = [
            move for move in all_moves
            if self.board.is_legal_move(pos, move, self.current_turn)
        ]
    
    def update(self):
        """Обновление состояния игры"""
        # Если ход AI
        if self.ai_enabled and self.current_turn == self.ai.color and not self.game_over and not self.ai_thinking:
            self.ai_thinking = True
            pygame.display.set_caption('Шахматы - ИИ думает...')
    
    def make_ai_move(self):
        """Сделать ход AI (вызывается после отрисовки)"""
        if self.ai_thinking:
            move = self.ai.get_best_move(self.board)
            
            if move:
                from_pos, to_pos = move
                self._make_move(from_pos, to_pos)
            
            self.ai_thinking = False
            pygame.display.set_caption('Шахматы')
    
    def draw(self):
        """Отрисовка игры"""
        self.draw_board()
        self.draw_pieces()
        
        if self.selected_pos:
            self.draw_selection()
        
        if self.valid_moves:
            self.draw_valid_moves() 
        
        if self.game_over:
            self.draw_game_over()
    
    def draw_board(self):
        """Отрисовка доски"""
        for row in range(8):
            for col in range(8):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                     self.SQUARE_SIZE, self.SQUARE_SIZE)
                )
    
    def draw_pieces(self):
        """Отрисовка фигур с правильным шрифтом"""
        piece_symbols = {
            'white': {'King': '♔', 'Queen': '♕', 'Rook': '♖', 
                    'Bishop': '♗', 'Knight': '♘', 'Pawn': '♙'},
            'black': {'King': '♚', 'Queen': '♛', 'Rook': '♜',
                    'Bishop': '♝', 'Knight': '♞', 'Pawn': '♟'}
        }
        
        try:
            font = pygame.font.SysFont('segoeuisymbol', 70)
        except:
            try:
                font = pygame.font.SysFont('dejavusans', 70)
            except:
                font = pygame.font.Font(None, 70)
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece:
                    symbol = piece_symbols[piece.color][piece.name]
                    
                    if piece.color == 'white':
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)
                    
                    text = font.render(symbol, True, color)
                    text_rect = text.get_rect(
                        center=(col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                    )

                    if piece.color == 'white':
                        outline = font.render(symbol, True, (0, 0, 0))
                        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                            outline_rect = text_rect.copy()
                            outline_rect.x += dx
                            outline_rect.y += dy
                            self.screen.blit(outline, outline_rect)
                    else:
                        outline = font.render(symbol, True, (255, 255, 255))
                        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                            outline_rect = text_rect.copy()
                            outline_rect.x += dx
                            outline_rect.y += dy
                            self.screen.blit(outline, outline_rect)
                    
                    self.screen.blit(text, text_rect)

    def draw_selection(self):
        """Подсветка выбранной фигуры"""
        row, col = self.selected_pos
        pygame.draw.rect(
            self.screen,
            self.HIGHLIGHT,
            (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
             self.SQUARE_SIZE, self.SQUARE_SIZE),
            5
        )
    
    def draw_valid_moves(self):
        """Отрисовка валидных ходов"""
        for row, col in self.valid_moves:
            pygame.draw.circle(
                self.screen,
                self.VALID_MOVE,
                (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                 row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                15
            )
    
    def draw_game_over(self):
        """Экран окончания игры"""
        overlay = pygame.Surface((800, 800))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        text = self.big_font.render(f"Победа: {self.winner}!", True, (255, 215, 0))
        text_rect = text.get_rect(center=(400, 400))
        self.screen.blit(text, text_rect)
        
        restart_text = self.font.render("Нажмите ESC для выхода", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(400, 500))
        self.screen.blit(restart_text, restart_rect)