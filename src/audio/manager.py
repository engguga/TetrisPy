import pygame
import os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.current_music = None
        self.music_enabled = True
        self.sfx_enabled = True
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        sound_files = {
            'move': 'move.ogg',
            'rotate': 'rotate.ogg',
            'drop': 'drop.ogg',
            'line_clear': 'line_clear.ogg',
            'tetris': 'tetris.ogg',
            'game_over': 'game_over.ogg',
            'menu_select': 'menu_select.ogg',
            'level_up': 'level_up.ogg'
        }
        
        for name, filename in sound_files.items():
            try:
                path = os.path.join('assets', 'audio', 'sfx', filename)
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
            except:
                pass
    
    def play_music(self, track_name, loops=-1):
        if not self.music_enabled:
            return
            
        try:
            path = os.path.join('assets', 'audio', 'music', f"{track_name}.ogg")
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
                self.current_music = track_name
        except:
            pass
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None
    
    def play_sound(self, sound_name):
        if not self.sfx_enabled or sound_name not in self.sounds:
            return
            
        self.sounds[sound_name].set_volume(self.sfx_volume)
        self.sounds[sound_name].play()
    
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
        elif self.current_music:
            self.play_music(self.current_music)
    
    def toggle_sfx(self):
        self.sfx_enabled = not self.sfx_enabled