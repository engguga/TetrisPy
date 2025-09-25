import random
import pygame

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-5, -1)
        self.lifetime = random.uniform(0.5, 1.5)
        self.age = 0
    
    def update(self, dt):
        self.age += dt
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.2
        return self.age < self.lifetime
    
    def draw(self, surface):
        alpha = 255 * (1 - self.age / self.lifetime)
        color = (*self.color, int(alpha))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, x, y, color, count=20):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)