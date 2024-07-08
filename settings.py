import pygame

pygame.font.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (227, 61, 148)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 100, 200)

WIDTH = 1280
HEIGHT = 800
FPS = 30

SIZE_SCREEN = (WIDTH, HEIGHT)

HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
 
ORIGIN = (0, 0)
INITIAL_HEARTS = 3

INVULNERABLE_TIME = 1000
GRID_SIZE = 10

background_image_menu = pygame.image.load("./src/images/background-menu.png")
background_image_menu = pygame.transform.scale(background_image_menu, SIZE_SCREEN)

score_filepath = "./config/scores.json"
player_config_filepath = "./config/player.json"

font = pygame.font.Font(None, 36)
