import pygame
import cv2
import numpy as np
import random


class TicTacToe:
    def __init__(self):
        pygame.init()

        # Константы
        self.WIDTH, self.HEIGHT = 800, 800
        self.FPS = 60
        self.BLACK = (0, 0, 0)

        # Состояния игры
        self.START_SCREEN = 0
        self.PLAYER_VS_PLAYER = 1
        self.PLAYER_VS_COMPUTER = 2
        self.current_state = self.START_SCREEN

        # Создание игрового окна
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Крестики-нолики")

        # Загрузка изображений для кнопок и названия игры
        self.game_title_img = pygame.image.load("game_title.png").convert_alpha()
        self.game_title_img = pygame.transform.scale(self.game_title_img, (500, 100))

        self.pvp_button_img = pygame.image.load("pvp_image.png").convert_alpha()
        self.pvp_button_img = pygame.transform.scale(self.pvp_button_img, (200, 75))

        self.pvc_button_img = pygame.image.load("pvc_image.png").convert_alpha()
        self.pvc_button_img = pygame.transform.scale(self.pvc_button_img, (200, 75))

        # Загрузка изображений для крестиков и ноликов
        self.X_img = pygame.image.load("X.png").convert_alpha()
        self.X_img = pygame.transform.scale(self.X_img, (250, 250))

        self.O_img = pygame.image.load("O.png").convert_alpha()
        self.O_img = pygame.transform.scale(self.O_img, (250, 250))

        self.player_turn = True

    def draw_start_screen(self):
        self.screen.fill(self.BLACK)
        # Отображение начального экрана с кнопками и названием
        if self.current_state == self.START_SCREEN:
            title_rect = self.game_title_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4))
            self.screen.blit(self.game_title_img, title_rect)

            # Отображение кнопок горизонтально
            pvp_button_rect = self.pvp_button_img.get_rect(center=(self.WIDTH // 3, self.HEIGHT // 2))
            pvc_button_rect = self.pvc_button_img.get_rect(center=(2 * self.WIDTH // 3, self.HEIGHT // 2))

            self.screen.blit(self.pvp_button_img, pvp_button_rect)
            self.screen.blit(self.pvc_button_img, pvc_button_rect)
        elif self.current_state in (self.PLAYER_VS_PLAYER, self.PLAYER_VS_COMPUTER):
            self.draw_neon_grid()

    def draw_neon_grid(self):
        cell_size = self.WIDTH // 3

        # Создание изображения с размытыми белыми линиями
        img = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)
        for i in range(1, 3):
            cv2.line(img, (cell_size * i, 0), (cell_size * i, self.HEIGHT), (255, 255, 255), 7)
            cv2.line(img, (0, cell_size * i), (self.WIDTH, cell_size * i), (255, 255, 255), 7)

        # Применение эффекта неона с помощью размытия и масштабирования
        blurred = cv2.GaussianBlur(img, (25, 25), 0)
        neon = cv2.addWeighted(img, 2.5, blurred, 0.7, 0)  # Изменение коэффициентов здесь для увеличения яркости

        # Преобразование изображения в формат Pygame Surface и отображение на экране
        neon = pygame.image.frombuffer(neon.flatten(), (self.WIDTH, self.HEIGHT), 'RGB')
        self.screen.blit(neon, (0, 0))

    def draw_symbol(self, symbol, row, col):
        cell_size = self.WIDTH // 3
        if symbol == 'X':
            # Отображение крестика по центру клетки
            self.screen.blit(self.X_img, (col * cell_size + (cell_size - self.X_img.get_width()) // 2,
                                          row * cell_size + (cell_size - self.X_img.get_height()) // 2))
        elif symbol == 'O':
            # Отображение нолика по центру клетки
            self.screen.blit(self.O_img, (col * cell_size + (cell_size - self.O_img.get_width()) // 2,
                                          row * cell_size + (cell_size - self.O_img.get_height()) // 2))

    def computer_move(self, board):
        best_score = -float('inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if board[row][col] == '-':
                    board[row][col] = 'O'
                    score = self.minimax(board, 0, False)
                    board[row][col] = '-'

                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move

    def minimax(self, board, depth, is_maximizing):
        result = self.check_winner(board)
        if result == 'X':
            return -1
        elif result == 'O':
            return 1
        elif result == 'Draw':
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == '-':
                        board[row][col] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = '-'
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == '-':
                        board[row][col] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = '-'
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, board):
        # Проверка строк
        for row in board:
            if row.count(row[0]) == len(row) and row[0] != '-':
                return row[0]

        # Проверка столбцов
        for col in range(len(board)):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '-':
                return board[0][col]

        # Проверка диагоналей
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '-':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '-':
            return board[0][2]

        # Проверка ничьи
        if '-' not in board[0] and '-' not in board[1] and '-' not in board[2]:
            return 'Draw'

        return None

    def get_empty_cells(self, board):
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if board[row][col] == '-':
                    empty_cells.append((row, col))
        return empty_cells

    def main(self):
        running = True
        winner_img = None
        board = [['-' for _ in range(3)] for _ in range(3)]
        while running:
            self.screen.fill(self.BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.current_state == self.START_SCREEN:
                    if self.pvp_button_img.get_rect(center=(self.WIDTH // 3, self.HEIGHT // 2)).collidepoint(event.pos):
                        self.current_state = self.PLAYER_VS_PLAYER
                    elif self.pvc_button_img.get_rect(center=(2 * self.WIDTH // 3, self.HEIGHT // 2)).collidepoint(
                            event.pos):
                        self.current_state = self.PLAYER_VS_COMPUTER

                elif event.type == pygame.MOUSEBUTTONDOWN and self.current_state in (
                        self.PLAYER_VS_PLAYER, self.PLAYER_VS_COMPUTER):
                    row = event.pos[1] // (self.HEIGHT // 3)
                    col = event.pos[0] // (self.WIDTH // 3)
                    if board[row][col] == '-' and self.current_state == self.PLAYER_VS_PLAYER:
                        if self.player_turn:
                            board[row][col] = 'X'
                            self.player_turn = False
                        else:
                            board[row][col] = 'O'
                            self.player_turn = True
                    elif self.current_state == self.PLAYER_VS_COMPUTER and self.player_turn and board[row][col] == '-':
                        board[row][col] = 'X'
                        self.player_turn = False
                        if self.check_winner(board) is None:
                            computer_row, computer_col = self.computer_move(board)
                            board[computer_row][computer_col] = 'O'
                            self.player_turn = True
            self.draw_start_screen()
            if self.current_state in (self.PLAYER_VS_PLAYER, self.PLAYER_VS_COMPUTER):
                for row in range(3):
                    for col in range(3):
                        if board[row][col] != '-':
                            self.draw_symbol(board[row][col], row, col)

                winner = self.check_winner(board)
                if winner is not None:
                    if winner == 'X':
                        winner_img = pygame.image.load("player_1_win.png").convert_alpha()
                    elif winner == 'O':
                        if self.current_state == self.PLAYER_VS_PLAYER:
                            winner_img = pygame.image.load("player_2_win.png").convert_alpha()
                        else:
                            winner_img = pygame.image.load("pvc_player_win.png").convert_alpha()
                    elif winner == 'Draw':
                        winner_img = pygame.image.load("tie.png").convert_alpha()

                    self.current_state = self.START_SCREEN

            if winner_img is not None:
                self.screen.fill(self.BLACK)
                self.screen.blit(winner_img,
                                 (self.WIDTH // 2 - winner_img.get_width() // 2,
                                  self.HEIGHT // 2 - winner_img.get_height() // 2))
                pygame.display.flip()
                pygame.time.delay(2000)  # Показываем изображение на 2 секунды
                winner_img = None

            self.draw_start_screen()
            if self.current_state in (self.PLAYER_VS_PLAYER, self.PLAYER_VS_COMPUTER):
                for row in range(3):
                    for col in range(3):
                        if board[row][col] != '-':
                            self.draw_symbol(board[row][col], row, col)

                winner = self.check_winner(board)
                if winner is not None:
                    print(f"Winner is {winner}")
                    self.current_state = self.START_SCREEN

            pygame.display.flip()
            pygame.time.Clock().tick(self.FPS)
        pygame.quit()


if __name__ == "__main__":
    game = TicTacToe()
    game.main()
