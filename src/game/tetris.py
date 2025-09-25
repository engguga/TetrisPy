import pygame
import random
import time
from .config import GameConfig
from .particles import ParticleSystem

class TetrisGame:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 700
        self.block_size = 30
        self.grid_width = 10
        self.grid_height = 20
        self.left_margin = (self.screen_width - self.grid_width * self.block_size) // 2
        self.top_margin = 100
        
        self.colors = {
            'black': (10, 10, 20),
            'dark_gray': (40, 40, 50),
            'gray': (100, 100, 120),
            'white': (255, 255, 255),
            'red': (255, 50, 50),
            'green': (50, 255, 100),
            'blue_light': (100, 200, 255),
            'cyan': (0, 255, 255),
            'yellow': (255, 255, 0),
            'purple': (180, 0, 255),
            'orange': (255, 165, 0),
            'blue': (0, 0, 255),
            'green_tetris': (0, 255, 0),
            'red_tetris': (255, 0, 0)
        }
        
        self.piece_shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 1, 1], [0, 1, 0]],
            [[1, 1, 1], [1, 0, 0]],
            [[1, 1, 1], [0, 0, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]]
        ]
        
        self.piece_colors = [
            self.colors['cyan'], self.colors['yellow'], self.colors['purple'],
            self.colors['orange'], self.colors['blue'], self.colors['green_tetris'],
            self.colors['red_tetris']
        ]
        
        self.piece_names = ['I', 'O', 'T', 'L', 'J', 'S', 'Z']
        
        self.difficulties = {
            'easy': {'speed': 800, 'name': 'Easy', 'color': self.colors['green']},
            'medium': {'speed': 500, 'name': 'Medium', 'color': self.colors['yellow']},
            'hard': {'speed': 300, 'name': 'Hard', 'color': self.colors['orange']},
            'extreme': {'speed': 150, 'name': 'Extreme', 'color': self.colors['red']}
        }
        
        self.config = GameConfig()
        self.particles = ParticleSystem()
        self.reset_game()
    
    def reset_game(self):
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_time = 0
        self.start_time = time.time()
        self.game_over = False
        self.next_piece = self.create_random_piece()
        self.new_piece()
        self.current_difficulty = self.config.default_difficulty
        self.fall_speed = self.difficulties[self.current_difficulty]['speed']
    
    def create_random_piece(self):
        idx = random.randint(0, len(self.piece_shapes) - 1)
        return {
            'shape': self.piece_shapes[idx],
            'color': self.piece_colors[idx],
            'name': self.piece_names[idx],
            'x': self.grid_width // 2 - len(self.piece_shapes[idx][0]) // 2,
            'y': 0
        }
    
    def new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = self.create_random_piece()
        if self.check_collision(self.current_piece['x'], self.current_piece['y'], self.current_piece['shape']):
            self.game_over = True
    
    def check_collision(self, x, y, shape):
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    if (x + col_idx < 0 or x + col_idx >= self.grid_width or
                        y + row_idx >= self.grid_height or
                        (y + row_idx >= 0 and self.grid[y + row_idx][x + col_idx])):
                        return True
        return False
    
    def rotate_piece(self):
        shape = self.current_piece['shape']
        rotated_shape = list(zip(*shape[::-1]))
        rotated_shape = [list(row) for row in rotated_shape]
        if not self.check_collision(self.current_piece['x'], self.current_piece['y'], rotated_shape):
            self.current_piece['shape'] = rotated_shape
    
    def move_piece(self, dx, dy):
        if not self.check_collision(self.current_piece['x'] + dx, self.current_piece['y'] + dy, self.current_piece['shape']):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
            return True
        return False
    
    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell and 0 <= self.current_piece['y'] + y < self.grid_height:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        
        lines_cleared = self.clear_lines()
        self.update_score(lines_cleared)
        self.new_piece()
    
    def clear_lines(self):
        complete_lines = []
        for y in range(self.grid_height):
            if all(self.grid[y]):
                complete_lines.append(y)
        
        for line in complete_lines:
            for x in range(self.grid_width):
                pos_x = self.left_margin + x * self.block_size + self.block_size // 2
                pos_y = self.top_margin + line * self.block_size + self.block_size // 2
                self.particles.add_explosion(pos_x, pos_y, self.grid[line][x], 10)
            
            for y2 in range(line, 0, -1):
                self.grid[y2] = self.grid[y2-1][:]
            self.grid[0] = [0] * self.grid_width
        
        return len(complete_lines)
    
    def update_score(self, lines_cleared):
        if lines_cleared == 1:
            self.score += 100 * self.level
        elif lines_cleared == 2:
            self.score += 300 * self.level
        elif lines_cleared == 3:
            self.score += 500 * self.level
        elif lines_cleared == 4:
            self.score += 800 * self.level
        
        self.lines_cleared += lines_cleared
        self.level = self.lines_cleared // 10 + 1
        base_speed = self.difficulties[self.current_difficulty]['speed']
        self.fall_speed = max(50, base_speed - (self.level - 1) * 20)
    
    def update(self, dt):
        self.game_time = time.time() - self.start_time
        self.particles.update(dt)
    
    def draw(self, screen):
        screen.fill(self.colors['black'])
        self.draw_grid(screen)
        self.draw_current_piece(screen)
        self.particles.draw(screen)
    
    def draw_grid(self, screen):
        pygame.draw.rect(screen, self.colors['dark_gray'], 
                        (self.left_margin - 2, self.top_margin - 2,
                         self.grid_width * self.block_size + 4,
                         self.grid_height * self.block_size + 4))
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x],
                                   [self.left_margin + x * self.block_size,
                                    self.top_margin + y * self.block_size,
                                    self.block_size, self.block_size])
                    pygame.draw.rect(screen, self.colors['white'],
                                   [self.left_margin + x * self.block_size,
                                    self.top_margin + y * self.block_size,
                                    self.block_size, self.block_size], 1)
        
        for x in range(self.grid_width + 1):
            pygame.draw.line(screen, self.colors['gray'],
                           (self.left_margin + x * self.block_size, self.top_margin),
                           (self.left_margin + x * self.block_size, self.top_margin + self.grid_height * self.block_size))
        for y in range(self.grid_height + 1):
            pygame.draw.line(screen, self.colors['gray'],
                           (self.left_margin, self.top_margin + y * self.block_size),
                           (self.left_margin + self.grid_width * self.block_size, self.top_margin + y * self.block_size))
    
    def draw_current_piece(self, screen):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece['color'],
                                   [self.left_margin + (self.current_piece['x'] + x) * self.block_size,
                                    self.top_margin + (self.current_piece['y'] + y) * self.block_size,
                                    self.block_size, self.block_size])
                    pygame.draw.rect(screen, self.colors['white'],
                                   [self.left_margin + (self.current_piece['x'] + x) * self.block_size,
                                    self.top_margin + (self.current_piece['y'] + y) * self.block_size,
                                    self.block_size, self.block_size], 1)