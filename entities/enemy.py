from pygame import Surface
from pygame.sprite import Sprite, collide_rect
from .bullet import Bullet
from settings import RED


class Enemy(Sprite):
    def __init__(self, origin, destination, speed, damage):
        super().__init__()
        self.image = Surface((50, 50))
        self.image.fill(RED)
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
        current_x = self.rect.x
        current_y = self.rect.y

        if current_x < self.destination[0]:
            current_x += self.speed

        if current_y < self.destination[1]:
            current_y += self.speed

        self.rect.x = current_x
        self.rect.y = current_y

        if current_x >= self.destination[0] and current_y >= self.destination[1]:
            self.is_moving_to_destination = False

    def _go_to_origin(self):
        current_x = self.rect.x
        current_y = self.rect.y

        if current_x > self.origin[0]:
            current_x -= self.speed

        if current_y > self.origin[1]:
            current_y -= self.speed

        self.rect.x = current_x
        self.rect.y = current_y

        if current_x <= self.origin[0] and current_y <= self.origin[1]:
            self.is_moving_to_destination = True

    def has_received_damage(self, bullet: Bullet) -> bool:
        return collide_rect(self, bullet)

    def die(self):
        self.kill()
