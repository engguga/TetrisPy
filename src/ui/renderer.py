import pygame

class UIRenderer:
    def __init__(self, game):
        self.game = game
        self.font_large = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 24)
        self.font_small = pygame.font.SysFont('Arial', 18)
    
    def draw_text(self, surface, text, size, x, y, color):
        if size == "large":
            font = self.font_large
        elif size == "small":
            font = self.font_small
        else:
            font = self.font_medium
            
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)
    
    def draw_centered_text(self, surface, text, size, y, color):
        if size == "large":
            font = self.font_large
        elif size == "small":
            font = self.font_small
        else:
            font = self.font_medium
            
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.game.screen_width // 2, y))
        surface.blit(text_surface, text_rect)