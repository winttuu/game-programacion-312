from pygame import Surface, image, transform
from pygame.sprite import Sprite
from settings import WHITE


class Objective(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 50
        self.image = image.load("./src/images/key.png")
        self.image = transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
