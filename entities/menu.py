from pygame import Rect
import sys
from tools import render_text
from settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = background_image_menu

    def draw(self, is_the_end:bool=False, is_lost:bool=False, score:any=0): 
        self.screen.blit(self.background_image, ORIGIN)
        
        play_button_rect = self._create_rect(550, 500, 200, 50)
        quit_button_rect = self._create_rect(550, 400, 200, 50)
        scores_button_rect = self._create_rect(550, 300, 200, 50)
        message_rect = self._create_rect(550, 150, 300, 50)

        pygame.display.flip()
        display = True

        while display:
            mouse_pos = pygame.mouse.get_pos()

            play_hover = play_button_rect.collidepoint(mouse_pos)
            quit_hover = quit_button_rect.collidepoint(mouse_pos)
            score_hover = scores_button_rect.collidepoint(mouse_pos)
            
            self.draw_button(quit_button_rect, "Cerrar", quit_hover)

            if not is_the_end:
                self.draw_button(scores_button_rect, "Scores", score_hover)
                self.draw_button(play_button_rect, "Jugar", play_hover)
            else:
                if is_lost:
                    self.draw_message(rect=message_rect, text="GAME OVER")
                    self.draw_button(play_button_rect, "Jugar", play_hover)
                    self.draw_button(scores_button_rect, f"Score: {score}")
                else:
                    self.draw_message(rect=message_rect, text="Ganaste!!")
                    self.draw_button(scores_button_rect, f"Score: {score}")

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  
                        if play_button_rect.collidepoint(event.pos):
                            display = False
                        elif quit_button_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                        elif scores_button_rect.collidepoint(event.pos) and not is_the_end:
                            self.draw_score(score=score)
                            return

    def draw_button(self, rect, text, hover=False):
        color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
        pygame.draw.rect(self.screen, color, rect)
        render_text(text, self.screen, rect.centerx, rect.centery, WHITE)

    def draw_message(self, rect, text):
        pygame.draw.rect(surface=self.screen, color=YELLOW, rect=rect)
        render_text(text, self.screen, rect.centerx, rect.centery, BLACK)

    def draw_score(self, score):
        self.screen.blit(self.background_image, ORIGIN)
        pygame.display.flip()
        display_score = True

        while display_score:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        display_score = False
                        self.draw()  

        
            score_rect = self._create_rect(500, 209, 350, 50)
            coins_rect = self._create_rect(500, 300, 350, 50)
            kills_rect = self._create_rect(500, 400, 350, 50)
            level_rect = self._create_rect(500, 500, 300, 50)

            exit_rect = self._create_rect(500, 700, 500, 50)

            self.draw_button(score_rect, f"Score maximo obtenido: {score['max_score']}")
            self.draw_button(coins_rect, f"Coins maximas obtenidas: {score['coin']}")
            self.draw_button(kills_rect, f"Kills maximas obtenido: {score['kill']}")
            self.draw_button(level_rect, f"Nivel llegado: {score['next_stage']}")


            self.draw_button(exit_rect, "Presiona escape para volver al menu!")
            pygame.display.update()


    def _create_rect(self, left, top, width, height) -> Rect:
        return Rect(left, top, width, height)
