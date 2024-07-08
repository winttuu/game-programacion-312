import json
import pygame
import settings
from pygame import image, transform, K_DOWN, K_RIGHT, K_UP, K_LEFT, K_SPACE
from pygame.sprite import Sprite, collide_rect
from .enemy import Enemy
from .bullet import Bullet
from exceptions import PlayerHasDiedError, PlayerHasReceivedDamageError

def create_bullet(x, y, direction):
    return Bullet(x, y, direction)

class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.images = {
            K_DOWN: [],
            K_RIGHT: [],
            K_UP: [],
            K_LEFT: []
        }
        self.speed = 10
        self.hearts = 3
        self.points = 0
        self.has_objective = False
        self.is_invulnerable = False
        self.collision_time = None
        self.current_bullet = None  # Atributo para la bala
        self.obstacles = []
        self.direction = K_DOWN
        self._load_images()
        self.current_sprite = 0
        self.image = self.images[self.direction][0]
        self.rect = self.image.get_rect()
        self.rect.center = (settings.WIDTH // 2, settings.HEIGHT // 2)
        self.animation_speed = 10
        self.is_moving = False
        self.ammunition = self._create_ammunition()

    def _load_images(self):
        with open(settings.player_config_filepath, "r") as file:
            sources = json.load(file)["assets"]

        groups = [K_DOWN, K_RIGHT, K_UP, K_LEFT]

        for index, folder in enumerate(sources):
            for i in range(0, 8):
                img = image.load('{}/{}'.format(folder, f'sprite{i}.png'))
                self.images[groups[index]].append(img)

    def _create_ammunition(self):
        return [
            create_bullet,
            create_bullet,
            create_bullet,
            create_bullet,
            create_bullet,
        ]

    def update(self, keys):
        self._animate()

        if any([keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN]]):
            self.is_moving = True
            self._move(keys)
        else:
            self.is_moving = False

        if keys[K_SPACE]:
            self._shoot()

        self._check_active_bullet()

    def _animate(self):
        if self.is_moving and self.current_sprite < 4:
            self.current_sprice = 4

        self.current_sprite += 1

        if self.is_moving:
            if self.current_sprite > 7:
                self.current_sprite = 4
        else:
            if self.current_sprite > 3:
                self.current_sprite = 0

        self.image = self.images[self.direction][self.current_sprite]

    def _move(self, keys):
        current_position = self.rect.copy()
        new_x = self.rect.x
        new_y = self.rect.y

        if keys[K_LEFT]:
            self.direction = K_LEFT
            new_x -= self.speed

        if keys[K_RIGHT]:
            self.direction = K_RIGHT
            new_x += self.speed

        if keys[K_UP]:
            self.direction = K_UP
            new_y -= self.speed

        if keys[K_DOWN]:
            self.direction = K_DOWN
            new_y += self.speed

        if self._has_collision_with_obstacles(new_x, new_y):
            self.rect = current_position
            return

        self.rect.x = new_x
        self.rect.y = new_y

    def _has_collision_with_obstacles(self, x, y):
        if x <= 0 or x + self.image.get_width() >= settings.WIDTH:
            return True

        if y <= 0 or y + self.image.get_height() >= settings.HEIGHT:
            return True

        self.rect.x = x
        self.rect.y = y

        for obstacle in self.obstacles:
            if collide_rect(self, obstacle):
                return True

        return False

    def _shoot(self):
        if not self.current_bullet and len(self.ammunition) > 0:
            sound = pygame.mixer.Sound('src/sounds/shoot.mp3')
            sound.play()
            x = self.rect.centerx
            y = self.rect.centery
            create_ammunition = self.ammunition.pop(0)
            self.current_bullet = create_ammunition(x, y, self.direction)
            print(f'Balas restantes: {len(self.ammunition)}')

    def _check_active_bullet(self):
        if not self.current_bullet:
            return

        self.current_bullet.move()

        if self.current_bullet.has_passed_the_limit():
            self.current_bullet = None

    def receive_damage(self, enemy: Enemy):
        if self.hearts > 0 and not self.is_invulnerable:
            self.hearts -= enemy.damage
            raise PlayerHasReceivedDamageError()

        if self.hearts < 1:
            raise PlayerHasDiedError()

    def activate_invulnerable(self):
        self.is_invulnerable = True

    def collect_coins(self, score):
        self.points += score

    def collect_potion(self):
        self.hearts += 1

    def finish_level(self):
        self.has_objective = True

    def check_time_invulnerable(self, time_to_check):
        if self.collision_time is None:
            self.collision_time = pygame.time.get_ticks()

        elapsed_time = pygame.time.get_ticks() - self.collision_time

        if elapsed_time > time_to_check:
            self.is_invulnerable = False
            self.collision_time = None
