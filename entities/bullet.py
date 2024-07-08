from pygame import Rect, draw, K_LEFT, K_RIGHT, K_UP, K_DOWN
from pygame.sprite import Sprite
from settings import WIDTH, HEIGHT


class Bullet(Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 20
        self.rect = Rect(x, y, 10, 10)

    def move(self):
        if self.direction == K_LEFT:
            self.rect.x -= self.speed
        elif self.direction == K_RIGHT:
            self.rect.x += self.speed
        elif self.direction == K_UP:
            self.rect.y -= self.speed
        elif self.direction == K_DOWN:
            self.rect.y += self.speed

    def draw(self, screen):
        draw.rect(screen, (255, 255, 255), self.rect)

    def has_passed_the_limit(self):
        if self.direction == K_LEFT:
            return self.rect.left < 0
        elif self.direction == K_RIGHT:
            return self.rect.right > WIDTH
        elif self.direction == K_UP:
            return self.rect.top < 0
        elif self.direction == K_DOWN:
            return self.rect.bottom > HEIGHT
