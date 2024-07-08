from pygame import Surface, image, transform
from pygame.sprite import Sprite
from settings import YELLOW


class Coin(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 45
        self.height = 45
        self.image = image.load("./src/images/CoinGold.png")
        self.image = transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
