import pygame
import sys

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((game.screen_width, game.screen_height))
        pygame.display.set_caption("TestrisPy")
        
        self.font_large = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 32)
        self.font_small = pygame.font.SysFont('Arial', 24)
        
        self.selected_option = 0
        self.menu_options = [
            "Start Game",
            "Difficulty: Medium",
            "Exit"
        ]
        
        self.difficulty_index = 1
        self.difficulties = list(self.game.difficulties.keys())
        self.update_difficulty_text()
    
    def update_difficulty_text(self):
        diff_name = self.game.difficulties[self.difficulties[self.difficulty_index]]['name']
        self.menu_options[1] = f"Difficulty: {diff_name}"
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()
                elif event.key == pygame.K_LEFT and self.selected_option == 1:
                    self.difficulty_index = (self.difficulty_index - 1) % len(self.difficulties)
                    self.update_difficulty_text()
                elif event.key == pygame.K_RIGHT and self.selected_option == 1:
                    self.difficulty_index = (self.difficulty_index + 1) % len(self.difficulties)
                    self.update_difficulty_text()
    
    def select_option(self):
        if self.selected_option == 0:
            self.start_game()
        elif self.selected_option == 2:
            pygame.quit()
            sys.exit()
    
    def start_game(self):
        self.game.current_difficulty = self.difficulties[self.difficulty_index]
        self.game.reset_game()
        game_loop = GameLoop(self.game, self.screen)
        game_loop.run()
    
    def draw(self):
        self.screen.fill(self.game.colors['black'])
        
        title = self.font_large.render("TESTRIS PY", True, self.game.colors['blue_light'])
        title_rect = title.get_rect(center=(self.game.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        high_score = self.font_small.render(f"High Score: {self.game.config.high_score}", True, self.game.colors['white'])
        high_score_rect = high_score.get_rect(center=(self.game.screen_width // 2, 160))
        self.screen.blit(high_score, high_score_rect)
        
        for i, option in enumerate(self.menu_options):
            color = self.game.colors['green'] if i == self.selected_option else self.game.colors['white']
            text = self.font_medium.render(option, True, color)
            rect = text.get_rect(center=(self.game.screen_width // 2, 250 + i * 60))
            self.screen.blit(text, rect)
            
            if i == self.selected_option:
                pygame.draw.rect(self.screen, color, (rect.left - 10, rect.top - 5, rect.width + 20, rect.height + 10), 2)
        
        controls = self.font_small.render("Controls: ↑↓ Navigate  ←→ Change Difficulty  ENTER Select", True, self.game.colors['gray'])
        controls_rect = controls.get_rect(center=(self.game.screen_width // 2, 500))
        self.screen.blit(controls, controls_rect)
        
        pygame.display.flip()
    
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
        diff_name = self.game.difficulties[self.game.current_difficulty]['name']
        diff_color = self.game.difficulties[self.game.current_difficulty]['color']
        
        score_text = self.font_medium.render(f"Score: {self.game.score}", True, self.game.colors['white'])
        level_text = self.font_medium.render(f"Level: {self.game.level}", True, self.game.colors['white'])
        lines_text = self.font_medium.render(f"Lines: {self.game.lines_cleared}", True, self.game.colors['white'])
        diff_text = self.font_medium.render(f"Difficulty: {diff_name}", True, diff_color)
        high_score_text = self.font_small.render(f"High Score: {self.game.config.high_score}", True, self.game.colors['gray'])
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(level_text, (20, 50))
        self.screen.blit(lines_text, (20, 80))
        self.screen.blit(diff_text, (20, 110))
        self.screen.blit(high_score_text, (20, 140))
        
        next_piece_text = self.font_medium.render("Next Piece:", True, self.game.colors['white'])
        self.screen.blit(next_piece_text, (500, 120))
        
        self.draw_next_piece()
        
        controls = self.font_small.render("Controls: ←→ Move  ↑ Rotate  ↓ Fast Drop  SPACE Hard Drop  ESC Menu", True, self.game.colors['gray'])
        self.screen.blit(controls, (self.game.screen_width // 2 - controls.get_width() // 2, 650))
    
    def draw_next_piece(self):
        pygame.draw.rect(self.screen, self.game.colors['dark_gray'], (500, 150, 200, 150))
        
        offset_x = 580 - len(self.game.next_piece['shape'][0]) * self.game.block_size // 2
        offset_y = 200 - len(self.game.next_piece['shape']) * self.game.block_size // 2
        
        for y, row in enumerate(self.game.next_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.game.next_piece['color'],
                                   [offset_x + x * self.game.block_size,
                                    offset_y + y * self.game.block_size,
                                    self.game.block_size, self.game.block_size])
                    pygame.draw.rect(self.screen, self.game.colors['white'],
                                   [offset_x + x * self.game.block_size,
                                    offset_y + y * self.game.block_size,
                                    self.game.block_size, self.game.block_size], 1)
    
    def draw_game_over(self):
        overlay = pygame.Surface((self.game.screen_width, self.game.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over = self.font_large.render("GAME OVER", True, self.game.colors['red'])
        score = self.font_medium.render(f"Final Score: {self.game.score}", True, self.game.colors['white'])
        high_score = self.font_medium.render(f"High Score: {self.game.config.high_score}", True, self.game.colors['green'])
        continue_text = self.font_small.render("Press ENTER to continue", True, self.game.colors['gray'])
        
        self.screen.blit(game_over, (self.game.screen_width // 2 - game_over.get_width() // 2, 250))
        self.screen.blit(score, (self.game.screen_width // 2 - score.get_width() // 2, 320))
        self.screen.blit(high_score, (self.game.screen_width // 2 - high_score.get_width() // 2, 360))
        self.screen.blit(continue_text, (self.game.screen_width // 2 - continue_text.get_width() // 2, 420))
    
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