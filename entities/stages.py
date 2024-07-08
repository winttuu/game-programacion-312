import json
from pygame.sprite import Group, GroupSingle
from pygame import image, transform
from settings import WIDTH, HEIGHT, SIZE_SCREEN, INITIAL_HEARTS
from .player import Player
from .enemy import Enemy
from .coin import Coin
from .potion import Potion
from .objective import Objective
from .goalblock import GoalBlock
from .obstacle import Obstacle
from exceptions import NotMoreStages

with open('./config/stages.json', 'r') as file:
    STAGE = json.load(file)

class Stage:
    def __init__(self, player: Player, stage=1):
        self.player = player
        self.current_stage = stage
        self.is_changed_stage = False
        self.not_more_stages = False

    def create(self):
        self.all_sprites = Group()

        self.enemies = Group()
        self.coins = Group()
        self.potions = Group()
        self.obstables = Group()
        self.goal = GroupSingle()
        self.objective = GroupSingle()
        self.background = None

        actual_stage = self.map_settings()

        if self.not_more_stages:
            raise NotMoreStages("No hay más niveles.")

        for enemy in self._make_enemies():
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        for coin in self._make_coins():
            self.coins.add(coin)
            self.all_sprites.add(coin)

        for potion in self._make_potions():
            self.potions.add(potion)
            self.all_sprites.add(potion)

        for obstacle in self._make_obstacles():
            self.obstables.add(obstacle)
            self.all_sprites.add(obstacle)

        o = self._make_objective()
        self.objective.add(o)
        self.all_sprites.add(o)

        self.player.rect.x = actual_stage["player"]["x"]
        self.player.rect.y = actual_stage["player"]["y"]
        self.player.obstacles = self.obstables
        self.player.has_objective = False
        self.all_sprites.add(self.player)

        g = self._make_goal()
        self.goal.add(g)
        self.all_sprites.add(g)

        self._make_background()
        self.is_changed_stage = False

    def map_settings(self):
        if len(STAGE) < (self.current_stage):
            self.not_more_stages = True
            return

        return STAGE[self.current_stage - 1]
    
    def _make_enemies(self):
        actual_stage = self.map_settings()
        enemies = []
        for option in actual_stage["enemies"]:
            origin = option["origin"]
            destination = option["destination"]
            speed = option["speed"]
            damage = option["damage"]
            enemy = Enemy(origin, destination, speed, damage)
            enemies.append(enemy)

        return enemies

    def _make_coins(self):
        actual_stage = self.map_settings()
        coins = []
        for option in actual_stage["coins"]:
            x = option["x"]
            y = option["y"]
            coin = Coin(x, y)
            coins.append(coin)

        return coins

    def _make_potions(self):
        actual_stage = self.map_settings()
        potions = []
        for option in actual_stage["potions"]:
            x = option["x"]
            y = option["y"]
            potion = Potion(x, y)
            potions.append(potion)

        return potions

    def _make_obstacles(self):
        actual_stage = self.map_settings()
        obstacles = []
        for option in actual_stage["obstacles"]:
            x = option["x"]
            y = option["y"]
            obstacle = Obstacle(x, y)
            obstacles.append(obstacle)

        return obstacles

    def _make_objective(self):
        actual_stage = self.map_settings()
        option = actual_stage["objective"]
        x = option["x"]
        y = option["y"]
        return Objective(x, y)

    def _make_goal(self):
        actual_stage = self.map_settings()
        option = actual_stage["goal"]
        x = option["x"]
        y = option["y"]
        return GoalBlock(x, y)

    def _make_background(self):
        actual_stage = self.map_settings()
        self.background = image.load(actual_stage["background"])
        self.background = transform.scale(self.background, SIZE_SCREEN)

    def move_to_next_stage(self):
        if self.is_changed_stage:
            return

        self.current_stage += 1
        self.is_changed_stage = True

    def reset_stage(self):
        self.player.ammunition = self.player.create_ammunition(5)
        self.player.points = 0
        self.player.hearts = INITIAL_HEARTS
        self.current_stage = 1

        print(f"{self.current_stage=}")
        print(f"{self.player.ammunition=}")
        print(f"{self.player.points=}")
        print(f"{self.player.hearts=}")