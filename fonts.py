import pygame

# font manager
class FontManager:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.fonts = {}


    def add_font(self, name, font_file, size):
        try:
            font = pygame.font.Font(font_file, size)
            self.fonts[name] = font
        except pygame.error:
            print(f"Failed to load font: {font_file}")

    def render_text(self, text, font_name, color, x=None, y=None):
        if font_name not in self.fonts:
            print(f"Font '{font_name}' not found. Using default font.")
            font = pygame.font.Font(None, 36)
        else:
            font = self.fonts[font_name]

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if x is None:
            x = (self.screen.get_width() - text_rect.width) // 2
        if y is None:
            y = text_rect.height

        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
