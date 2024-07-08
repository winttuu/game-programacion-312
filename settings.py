import pygame

pygame.font.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (227, 61, 148)

WIDTH = 1280
HEIGHT = 800
FPS = 30

SIZE_SCREEN = (WIDTH, HEIGHT)

ORIGIN = (0, 0)

INVULNERABLE_TIME = 1000
GRID_SIZE = 10

background_image_menu = pygame.image.load("./src/images/background-menu.png")
background_image_menu = pygame.transform.scale(background_image_menu, SIZE_SCREEN)

score_filepath = "./config/scores.json"
player_config_filepath = "./config/player.json"

font = pygame.font.Font(None, 36)
