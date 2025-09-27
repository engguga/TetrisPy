import pygame
import os

class CityTheme:
    def __init__(self, name, music_track, background_image, colors, description):
        self.name = name
        self.music_track = music_track
        self.background_image = background_image
        self.colors = colors
        self.description = description
        self.background_surface = None
        self.load_background()
    
    def load_background(self):
        try:
            path = os.path.join('assets', 'backgrounds', f"{self.background_image}.png")
            if os.path.exists(path):
                original_bg = pygame.image.load(path).convert()
                self.background_surface = pygame.transform.scale(original_bg, (800, 700))
        except:
            pass

class ThemeManager:
    def __init__(self, audio_manager):
        self.audio_manager = audio_manager
        self.themes = {}
        self.current_theme = None
        self.load_themes()
    
    def load_themes(self):
        self.themes = {
            'default': CityTheme(
                "Classic",
                "main_theme",
                "default",
                {
                    'background': (10, 10, 20),
                    'grid': (40, 40, 50),
                    'text': (255, 255, 255)
                },
                "Classic Tetris experience"
            ),
            'tokyo': CityTheme(
                "Tokyo Night",
                "tokyo",
                "tokyo",
                {
                    'background': (25, 25, 40),
                    'grid': (60, 40, 80),
                    'text': (255, 100, 150)
                },
                "Neon-lit Tokyo streets"
            ),
            'new_york': CityTheme(
                "New York",
                "new_york",
                "new_york",
                {
                    'background': (30, 30, 50),
                    'grid': (80, 60, 40),
                    'text': (255, 200, 100)
                },
                "Big Apple skyline"
            ),
            'paris': CityTheme(
                "Paris",
                "paris",
                "paris",
                {
                    'background': (40, 30, 50),
                    'grid': (70, 50, 80),
                    'text': (200, 220, 255)
                },
                "City of Lights"
            ),
            'rio': CityTheme(
                "Rio de Janeiro",
                "rio",
                "rio",
                {
                    'background': (20, 40, 60),
                    'grid': (40, 80, 60),
                    'text': (255, 220, 100)
                },
                "Sunny Brazilian beaches"
            )
        }
        
        self.current_theme = self.themes['default']
    
    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = self.themes[theme_name]
            self.audio_manager.play_music(self.current_theme.music_track)
            return True
        return False
    
    def get_theme_colors(self):
        return self.current_theme.colors