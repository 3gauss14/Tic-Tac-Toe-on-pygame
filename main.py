import pygame
import cv2
import numpy as np

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 800
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Состояния игры
START_SCREEN = 0
PLAYER_VS_PLAYER = 1
PLAYER_VS_COMPUTER = 2
current_state = START_SCREEN

# Создание игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-нолики")

# Загрузка изображений для кнопок и названия игры
game_title_img = pygame.image.load("game_title.png").convert_alpha()
game_title_img = pygame.transform.scale(game_title_img, (500, 100))

pvp_button_img = pygame.image.load("pvp_image.png").convert_alpha()
pvp_button_img = pygame.transform.scale(pvp_button_img, (200, 75))

pvc_button_img = pygame.image.load("pvc_image.png").convert_alpha()
pvc_button_img = pygame.transform.scale(pvc_button_img, (200, 75))


# Функции
def draw_start_screen():
    screen.fill(BLACK)
    if current_state == START_SCREEN:
        title_rect = game_title_img.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(game_title_img, title_rect)
        pvp_button_rect = pvp_button_img.get_rect(center=(WIDTH // 3, HEIGHT // 2))
        pvc_button_rect = pvc_button_img.get_rect(center=(2 * WIDTH // 3, HEIGHT // 2))
        screen.blit(pvp_button_img, pvp_button_rect)
        screen.blit(pvc_button_img, pvc_button_rect)
    elif current_state in (PLAYER_VS_PLAYER, PLAYER_VS_COMPUTER):
        draw_neon_grid()


def draw_neon_grid():
    cell_size = WIDTH // 3
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for i in range(1, 3):
        cv2.line(img, (cell_size * i, 0), (cell_size * i, HEIGHT), (255, 255, 255), 7)
        cv2.line(img, (0, cell_size * i), (WIDTH, cell_size * i), (255, 255, 255), 7)
    blurred = cv2.GaussianBlur(img, (25, 25), 0)
    neon = cv2.addWeighted(img, 2.5, blurred, 0.7, 0)
    neon = pygame.image.frombuffer(neon.flatten(), (WIDTH, HEIGHT), 'RGB')
    screen.blit(neon, (0, 0))


def main():
    global current_state
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and current_state == START_SCREEN:
                if pvp_button_img.get_rect(center=(WIDTH // 3, HEIGHT // 2)).collidepoint(event.pos):
                    current_state = PLAYER_VS_PLAYER
                elif pvc_button_img.get_rect(center=(2 * WIDTH // 3, HEIGHT // 2)).collidepoint(event.pos):
                    current_state = PLAYER_VS_COMPUTER
        draw_start_screen()
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
