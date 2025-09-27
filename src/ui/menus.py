import pygame
import sys

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((game.screen_width, game.screen_height))
        pygame.display.set_caption("TetrisPy")
        
        self.font_large = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 32)
        self.font_small = pygame.font.SysFont('Arial', 24)
        
        self.selected_option = 0
        self.menu_options = [
            "Start Game",
            f"Theme: {self.game.themes.current_theme.name}",
            f"Difficulty: {self.game.difficulties[self.game.config.default_difficulty]['name']}",
            "Audio Settings",
            "Exit"
        ]
        
        self.difficulty_index = list(self.game.difficulties.keys()).index(self.game.config.default_difficulty)
        self.theme_index = list(self.game.themes.themes.keys()).index(self.game.config.current_theme)
        self.in_audio_settings = False
        self.audio_options = ["Music Volume", "SFX Volume", "Toggle Music", "Toggle SFX", "Back"]
        self.audio_selected = 0
        
    def update_menu_text(self):
        self.menu_options[1] = f"Theme: {self.game.themes.current_theme.name}"
        self.menu_options[2] = f"Difficulty: {self.game.difficulties[self.game.config.default_difficulty]['name']}"
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.in_audio_settings:
                    self.handle_audio_events(event)
                else:
                    self.handle_main_events(event)
    
    def handle_main_events(self, event):
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            self.game.audio.play_sound('menu_select')
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            self.game.audio.play_sound('menu_select')
        elif event.key == pygame.K_RETURN:
            self.select_option()
        elif event.key == pygame.K_LEFT:
            self.handle_left_key()
        elif event.key == pygame.K_RIGHT:
            self.handle_right_key()
    
    def handle_audio_events(self, event):
        if event.key == pygame.K_UP:
            self.audio_selected = (self.audio_selected - 1) % len(self.audio_options)
            self.game.audio.play_sound('menu_select')
        elif event.key == pygame.K_DOWN:
            self.audio_selected = (self.audio_selected + 1) % len(self.audio_options)
            self.game.audio.play_sound('menu_select')
        elif event.key == pygame.K_LEFT:
            self.handle_audio_left()
        elif event.key == pygame.K_RIGHT:
            self.handle_audio_right()
        elif event.key == pygame.K_RETURN:
            if self.audio_selected == 4:  # Back
                self.in_audio_settings = False
            elif self.audio_selected == 2:  # Toggle Music
                self.game.audio.toggle_music()
                self.game.config.music_enabled = self.game.audio.music_enabled
                self.game.config.save_config()
            elif self.audio_selected == 3:  # Toggle SFX
                self.game.audio.toggle_sfx()
                self.game.config.sfx_enabled = self.game.audio.sfx_enabled
                self.game.config.save_config()
        elif event.key == pygame.K_ESCAPE:
            self.in_audio_settings = False
    
    def handle_left_key(self):
        if self.selected_option == 1:  # Theme
            themes = list(self.game.themes.themes.keys())
            self.theme_index = (self.theme_index - 1) % len(themes)
            new_theme = themes[self.theme_index]
            self.game.themes.set_theme(new_theme)
            self.game.config.current_theme = new_theme
            self.game.config.save_config()
            self.update_menu_text()
        elif self.selected_option == 2:  # Difficulty
            difficulties = list(self.game.difficulties.keys())
            self.difficulty_index = (self.difficulty_index - 1) % len(difficulties)
            self.game.config.default_difficulty = difficulties[self.difficulty_index]
            self.game.config.save_config()
            self.update_menu_text()
    
    def handle_right_key(self):
        if self.selected_option == 1:  # Theme
            themes = list(self.game.themes.themes.keys())
            self.theme_index = (self.theme_index + 1) % len(themes)
            new_theme = themes[self.theme_index]
            self.game.themes.set_theme(new_theme)
            self.game.config.current_theme = new_theme
            self.game.config.save_config()
            self.update_menu_text()
        elif self.selected_option == 2:  # Difficulty
            difficulties = list(self.game.difficulties.keys())
            self.difficulty_index = (self.difficulty_index + 1) % len(difficulties)
            self.game.config.default_difficulty = difficulties[self.difficulty_index]
            self.game.config.save_config()
            self.update_menu_text()
    
    def handle_audio_left(self):
        if self.audio_selected == 0:  # Music Volume
            new_volume = max(0.0, self.game.config.music_volume - 0.1)
            self.game.config.music_volume = new_volume
            self.game.audio.set_music_volume(new_volume)
            self.game.config.save_config()
        elif self.audio_selected == 1:  # SFX Volume
            new_volume = max(0.0, self.game.config.sfx_volume - 0.1)
            self.game.config.sfx_volume = new_volume
            self.game.audio.set_sfx_volume(new_volume)
            self.game.config.save_config()
    
    def handle_audio_right(self):
        if self.audio_selected == 0:  # Music Volume
            new_volume = min(1.0, self.game.config.music_volume + 0.1)
            self.game.config.music_volume = new_volume
            self.game.audio.set_music_volume(new_volume)
            self.game.config.save_config()
        elif self.audio_selected == 1:  # SFX Volume
            new_volume = min(1.0, self.game.config.sfx_volume + 0.1)
            self.game.config.sfx_volume = new_volume
            self.game.audio.set_sfx_volume(new_volume)
            self.game.config.save_config()
    
    def select_option(self):
        if self.selected_option == 0:
            self.start_game()
        elif self.selected_option == 3:
            self.in_audio_settings = True
            self.audio_selected = 0
        elif self.selected_option == 4:
            pygame.quit()
            sys.exit()
    
    def start_game(self):
        self.game.current_difficulty = self.game.config.default_difficulty
        self.game.reset_game()
        game_loop = GameLoop(self.game, self.screen)
        game_loop.run()
    
    def draw(self):
        theme_colors = self.game.themes.get_theme_colors()
        
        if self.game.themes.current_theme.background_surface:
            self.screen.blit(self.game.themes.current_theme.background_surface, (0, 0))
        else:
            self.screen.fill(theme_colors['background'])
        
        title = self.font_large.render("TETRIS PY", True, theme_colors['text'])
        title_rect = title.get_rect(center=(self.game.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        high_score = self.font_small.render(f"High Score: {self.game.config.high_score}", True, theme_colors['text'])
        high_score_rect = high_score.get_rect(center=(self.game.screen_width // 2, 160))
        self.screen.blit(high_score, high_score_rect)
        
        if self.in_audio_settings:
            self.draw_audio_menu()
        else:
            self.draw_main_menu()
        
        pygame.display.flip()
    
    def draw_main_menu(self):
        theme_colors = self.game.themes.get_theme_colors()
        
        for i, option in enumerate(self.menu_options):
            color = (50, 255, 100) if i == self.selected_option else theme_colors['text']
            text = self.font_medium.render(option, True, color)
            rect = text.get_rect(center=(self.game.screen_width // 2, 250 + i * 60))
            self.screen.blit(text, rect)
            
            if i == self.selected_option:
                pygame.draw.rect(self.screen, color, (rect.left - 10, rect.top - 5, rect.width + 20, rect.height + 10), 2)
        
        controls = self.font_small.render("Controls: ↑↓ Navigate  ←→ Change  ENTER Select", True, theme_colors['text'])
        controls_rect = controls.get_rect(center=(self.game.screen_width // 2, 550))
        self.screen.blit(controls, controls_rect)
    
    def draw_audio_menu(self):
        theme_colors = self.game.themes.get_theme_colors()
        
        title = self.font_medium.render("Audio Settings", True, theme_colors['text'])
        title_rect = title.get_rect(center=(self.game.screen_width // 2, 150))
        self.screen.blit(title, title_rect)
        
        audio_display = [
            f"Music Volume: {int(self.game.config.music_volume * 100)}%",
            f"SFX Volume: {int(self.game.config.sfx_volume * 100)}%",
            f"Music: {'ON' if self.game.config.music_enabled else 'OFF'}",
            f"SFX: {'ON' if self.game.config.sfx_enabled else 'OFF'}",
            "Back"
        ]
        
        for i, option in enumerate(audio_display):
            color = (50, 255, 100) if i == self.audio_selected else theme_colors['text']
            text = self.font_medium.render(option, True, color)
            rect = text.get_rect(center=(self.game.screen_width // 2, 220 + i * 50))
            self.screen.blit(text, rect)
            
            if i == self.audio_selected:
                pygame.draw.rect(self.screen, color, (rect.left - 10, rect.top - 5, rect.width + 20, rect.height + 10), 2)
        
        controls = self.font_small.render("↑↓ Navigate  ←→ Adjust  ENTER Select  ESC Back", True, theme_colors['text'])
        controls_rect = controls.get_rect(center=(self.game.screen_width // 2, 500))
        self.screen.blit(controls, controls_rect)
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.handle_events()
            self.draw()
            clock.tick(60)

class GameLoop:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.last_fall_time = pygame.time.get_ticks()
        self.font_medium = pygame.font.SysFont('Arial', 24)
        self.font_small = pygame.font.SysFont('Arial', 18)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.game.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.game.move_piece(0, 1)
                elif event.key == pygame.K_UP:
                    self.game.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    while self.game.move_piece(0, 1):
                        pass
                    self.game.lock_piece()
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time > self.game.fall_speed:
            if not self.game.move_piece(0, 1):
                self.game.lock_piece()
            self.last_fall_time = current_time
        
        self.game.update(self.clock.get_time() / 1000.0)
        
        if self.game.game_over:
            self.game.config.update_high_score(self.game.score)
            return False
        
        return True
    
    def draw_ui(self):
        theme_colors = self.game.themes.get_theme_colors()
        diff_name = self.game.difficulties[self.game.current_difficulty]['name']
        diff_color = self.game.difficulties[self.game.current_difficulty]['color']
        
        score_text = self.font_medium.render(f"Score: {self.game.score}", True, theme_colors['text'])
        level_text = self.font_medium.render(f"Level: {self.game.level}", True, theme_colors['text'])
        lines_text = self.font_medium.render(f"Lines: {self.game.lines_cleared}", True, theme_colors['text'])
        diff_text = self.font_medium.render(f"Difficulty: {diff_name}", True, diff_color)
        high_score_text = self.font_small.render(f"High Score: {self.game.config.high_score}", True, theme_colors['text'])
        theme_text = self.font_small.render(f"Theme: {self.game.themes.current_theme.name}", True, theme_colors['text'])
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(level_text, (20, 50))
        self.screen.blit(lines_text, (20, 80))
        self.screen.blit(diff_text, (20, 110))
        self.screen.blit(high_score_text, (20, 140))
        self.screen.blit(theme_text, (20, 170))
        
        next_piece_text = self.font_medium.render("Next Piece:", True, theme_colors['text'])
        self.screen.blit(next_piece_text, (500, 120))
        
        self.draw_next_piece()
        
        controls = self.font_small.render("Controls: ←→ Move  ↑ Rotate  ↓ Fast Drop  SPACE Hard Drop  ESC Menu", True, theme_colors['text'])
        self.screen.blit(controls, (self.game.screen_width // 2 - controls.get_width() // 2, 650))
    
    def draw_next_piece(self):
        theme_colors = self.game.themes.get_theme_colors()
        pygame.draw.rect(self.screen, theme_colors['grid'], (500, 150, 200, 150))
        
        offset_x = 580 - len(self.game.next_piece['shape'][0]) * self.game.block_size // 2
        offset_y = 200 - len(self.game.next_piece['shape']) * self.game.block_size // 2
        
        for y, row in enumerate(self.game.next_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.game.next_piece['color'],
                                   [offset_x + x * self.game.block_size,
                                    offset_y + y * self.game.block_size,
                                    self.game.block_size, self.game.block_size])
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                   [offset_x + x * self.game.block_size,
                                    offset_y + y * self.game.block_size,
                                    self.game.block_size, self.game.block_size], 1)
    
    def draw_game_over(self):
        overlay = pygame.Surface((self.game.screen_width, self.game.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.SysFont('Arial', 48, bold=True)
        font_medium = pygame.font.SysFont('Arial', 32)
        font_small = pygame.font.SysFont('Arial', 24)
        
        game_over = font_large.render("GAME OVER", True, (255, 50, 50))
        score = font_medium.render(f"Final Score: {self.game.score}", True, (255, 255, 255))
        
        if self.game.score == self.game.config.high_score:
            high_score = font_medium.render("NEW HIGH SCORE!", True, (50, 255, 100))
        else:
            high_score = font_medium.render(f"High Score: {self.game.config.high_score}", True, (255, 255, 255))
        
        continue_text = font_small.render("Press ENTER to continue", True, (200, 200, 200))
        
        self.screen.blit(game_over, (self.game.screen_width // 2 - game_over.get_width() // 2, 250))
        self.screen.blit(score, (self.game.screen_width // 2 - score.get_width() // 2, 320))
        self.screen.blit(high_score, (self.game.screen_width // 2 - high_score.get_width() // 2, 370))
        self.screen.blit(continue_text, (self.game.screen_width // 2 - continue_text.get_width() // 2, 430))
    
    def run(self):
        running = True
        game_over = False
        
        while running:
            if not game_over:
                if not self.handle_events():
                    break
                
                if not self.update():
                    game_over = True
                
                self.game.draw(self.screen)
                self.draw_ui()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        return
                
                self.game.draw(self.screen)
                self.draw_ui()
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)