import pygame
from tic_tac_toe_game import TicTacToeGame


def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    FPS = 60
    BLACK = (0, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Крестики-нолики")

    game = TicTacToeGame(screen, WIDTH, HEIGHT, FPS, BLACK)
    game.run()


if __name__ == "__main__":
    main()
