from settings import font, WHITE

def render_text(text, surface, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))
