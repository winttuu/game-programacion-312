import pygame
import json
import sys
import settings
from entities import Player, Stage, Menu
from tools import render_text
from exceptions import PlayerHasDiedError, PlayerHasReceivedDamageError, NotMoreStages


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.stage = Stage(Player())
        self.game_is_running = True
        self.score = self._load_score()
        self.menu = Menu(self.screen)
        self.create_map()

    def _load_score(self):
        try:
            with open(settings.score_filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"max_score": 0, "coin": 0, "kill": 0, "nex_stage": 0}

    def initialize_stage(self):
            print(f"{self.stage.current_stage=}")
            self.stage.create()
            self.player = self.stage.player
            self.all_sprites = self.stage.all_sprites
            self.enemies = self.stage.enemies
            self.coins = self.stage.coins
            self.potions = self.stage.potions
            self.objective = self.stage.objective
            self.goal_block = self.stage.goal
            self.obstacles = self.stage.obstables
            self.background = self.stage.background
            self.all_sprites.add(self.player)

    def create_map(self):
        try:
            self.initialize_stage()
        except NotMoreStages as e:
            self.menu.draw(is_the_end=True, score=self.player.points)
            # if self.menu.play:
            self.stage.reset_stage()
            print(f"{self.stage.current_stage=}")
            self.create_map()

    def run(self):
        clock = pygame.time.Clock()


        pygame.mixer.music.load('./src/sounds/game-music.mp3')
        pygame.mixer.music.play(-1)

        self.menu.draw(score=self._load_score())

        while self.game_is_running:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False

            self.all_sprites.update(keys)
            self.check_enemies()
            self.check_coins()
            self.check_potions()
            self.check_objective()
            self.check_goal()
            self.check_damage()
            self.check_player_status()

            self.screen.blit(self.background, settings.ORIGIN)

            self.all_sprites.draw(self.screen)
            self.render_bala()
            self.draw_ui()

            pygame.display.flip()
            clock.tick(settings.FPS)

    def check_player_status(self):
        self.player.check_time_invulnerable(settings.INVULNERABLE_TIME)

    def check_enemies(self):
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                try:
                    self.player.receive_damage(enemy)
                except PlayerHasReceivedDamageError:
                    self.player.activate_invulnerable()
                except PlayerHasDiedError:
                    self.check_score()
                    self.menu.draw(is_the_end=True, is_lost=True, score=self.player.points)
                    if self.menu.play:
                        self.stage.reset_stage()
                        self.create_map()

    def check_coins(self):
        coin_collisions = pygame.sprite.spritecollide(self.player, self.coins, True)

        if coin_collisions:
            sound = pygame.mixer.Sound('src/sounds/coin.mp3')
            sound.play()
            self.player.collect_coins(len(coin_collisions))

    def check_potions(self):
        potion_collisions = pygame.sprite.spritecollide(self.player, self.potions, True)

        if potion_collisions:
            self.player.collect_potion()

    def check_objective(self):
        if pygame.sprite.spritecollide(self.player, self.objective, True):
            self.player.finish_level()
            sound = pygame.mixer.Sound('src/sounds/key.mp3')
            sound.play()

    def check_goal(self):
        goal = self.goal_block.sprite

        if goal.can_pass_to_next_stage(self.player):
            self.player.collect_coins(self.score["next_stage"])
            self.stage.move_to_next_stage()
            self.create_map()

    def check_damage(self):
        if not self.player.current_bullet:
            return

        for enemy in self.enemies:
            if enemy.has_received_damage(self.player.current_bullet):
                self.player.current_bullet.kill()
                self.player.current_bullet = None

                sound = pygame.mixer.Sound('src/sounds/die_enemy.mp3')
                sound.play()

                enemy.die()
                self.player.collect_coins(self.score["kill"])

                break

    def render_bala(self):
        if self.player.current_bullet:
            self.player.current_bullet.draw(self.screen)

    def draw_ui(self):
        font = pygame.font.Font(None, 36)
        self.draw_ammunition()
        score_text = font.render(f"Puntos: {self.player.points}", True, settings.WHITE)
        hearts_text = font.render(f"Corazones: {'X' * self.player.hearts}", True, settings.RED)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(hearts_text, (10, 50))

    def draw_ammunition(self):
        x_offset = 10  # Desplazamiento inicial en el eje x
        y_position = 700  # Posición fija en el eje y
        spacing = 60  # Espaciado entre imagenes

        # Cargar la imagen de la munición
        bullet_image = pygame.image.load('./src/images/pergamino.png')
        # Escala la imagen si es necesario
        bullet_image = pygame.transform.scale(bullet_image, (80, 80))

        for index, item in enumerate(self.player.ammunition):
            # Dibujar la imagen en la pantalla
            self.screen.blit(bullet_image, (x_offset + index * spacing, y_position))

    def check_score(self):
        if self.score["max_score"] < self.player.points:
            self.score["max_score"] = self.player.points

            with open(settings.score_filepath, 'w') as file:
                json.dump(self.score, file, indent=2)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Juego Base")
    tile_size = settings.WIDTH // settings.GRID_SIZE
    game = Game(screen)
    game.run()
    pygame.quit()
