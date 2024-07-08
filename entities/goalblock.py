from pygame import Surface, image, transform
from pygame.sprite import Sprite, collide_rect
from settings import PINK
from .player import Player


class GoalBlock(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 200
        self.height = 200
        self.image = image.load("./src/images/house.png")
        self.image = transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def can_pass_to_next_stage(self, player: Player) -> bool:
        if not player.has_objective:
            return False

        if not collide_rect(self, player):
            return False

        return True
