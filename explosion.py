from turtle import width

from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
import pygame

class Explosion(CircleShape):
    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x,y,radius)
    
    def draw(self, screen: pygame.Surface) -> None:
        if self.radius<=0:
            self.kill()
            return
        pygame.draw.circle(screen, 'red', (self.position.x, self.position.y), self.radius, 0)
    
    def update(self, dt: float) -> None:
        if self.radius > 0:
            self.radius -=2
        
    
    