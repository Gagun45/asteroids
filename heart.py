import random
from explosion import Explosion
from logger import log_event
from circleshape import CircleShape
import pygame
from constants import ASTEROID_KINDS, GAME_DIFFICULTY, LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_HEIGHT,SCREEN_WIDTH

class Heart(CircleShape):
    def __init__(self, x:float, y:float, radius: float) -> None:
        super().__init__(x,y,radius)
        self.velocity = pygame.Vector2(0, 1)
        
    def draw(self, screen: pygame.Surface):
        points = [
            (0.50, 0.20),  # Top notch
            (0.35, 0.00),
            (0.15, 0.00),
            (0.00, 0.20),
            (0.00, 0.40),
            (0.15, 0.60),
            (0.50, 1.00),  # Bottom tip
            (0.85, 0.60),
            (1.00, 0.40),
            (1.00, 0.20),
            (0.85, 0.00),
            (0.65, 0.00),
        ]

        x = self.position.x - self.radius
        y = self.position.y - self.radius
        color=(230, 50, 80)
        size = self.radius
        vertices = [
            (round(x + px * size), round(y + py * size))
            for px, py in points
        ]

        pygame.draw.polygon(screen, color, vertices)
    def update(self, dt: float):
        self.position+= self.velocity * dt * 25
        if self.reached_bottom_border(self.radius):
            self.kill()