from pygame import Surface, image, transform
from pygame.sprite import Sprite, collide_rect
from .bullet import Bullet
from settings import RED


class Enemy(Sprite):
    def __init__(self, origin, destination, speed, damage):
        super().__init__()
        self.width = 50
        self.height = 50
        self.image = image.load("./src/images/enemy.png")
        self.image = transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.origin = origin
        self.destination = destination
        self.rect.x = origin[0]
        self.rect.y = origin[1]
        self.speed = speed
        self.damage = damage
        self.is_moving_to_destination = True

    def update(self, *args):
        if self.is_moving_to_destination:
            self._go_to_destination()
        else:
            self._go_to_origin()

    def _go_to_destination(self):
        if self.rect.x < self.destination[0]:
            self.rect.x += self.speed

        if self.rect.y < self.destination[1]:
            self.rect.y += self.speed

        if self.rect.x >= self.destination[0] and self.rect.y >= self.destination[1]:
            self.is_moving_to_destination = False

    def _go_to_origin(self):
        if self.rect.x > self.origin[0]:
            self.rect.x -= self.speed

        if self.rect.y > self.origin[1]:
            self.rect.y -= self.speed

        if self.rect.x <= self.origin[0] and self.rect.y <= self.origin[1]:
            self.is_moving_to_destination = True

    def has_received_damage(self, bullet: Bullet) -> bool:
        return collide_rect(self, bullet)

    def die(self):
        self.kill()
