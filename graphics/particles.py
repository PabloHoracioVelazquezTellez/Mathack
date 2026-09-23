import pygame
import random

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.radius = random.uniform(3, 6)
        self.lifetime = random.randint(20, 40)
        self.max_lifetime = self.lifetime
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95  # Fricción
        self.vy *= 0.95
        self.radius = max(0.0, self.radius - 0.1)
        self.lifetime -= 1

    def is_dead(self):
        return self.lifetime <= 0 or self.radius <= 0

    def draw(self, surface):
        if self.lifetime > 0 and self.radius > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            size = max(1, int(self.radius * 2))
            
            # Superficie con soporte para transparencia Alpha
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            r, g, b = self.color
            
            pygame.draw.circle(s, (r, g, b, alpha), (size // 2, size // 2), int(self.radius))
            surface.blit(s, (int(self.x - self.radius), int(self.y - self.radius)))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit_explosion(self, screen_x, screen_y, count=30, color=(0, 220, 255)):
        """Genera una ráfaga de partículas en coordenadas de pantalla"""
        palette = [
            color,
            (255, 220, 80),   # Dorado
            (255, 255, 255)    # Blanco destello
        ]
        for _ in range(count):
            c = random.choice(palette)
            self.particles.append(Particle(screen_x, screen_y, c))

    def update_and_draw(self, surface):
        for p in self.particles[:]:
            p.update()
            if p.is_dead():
                self.particles.remove(p)
            else:
                p.draw(surface)