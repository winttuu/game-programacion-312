from pygame import Surface, image, transform
from pygame.sprite import Sprite
from settings import GREEN


class Obstacle(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 100
        self.height = 120
        self.image = image.load("./src/images/tree.png")
        self.image = transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
