import random
from logger import log_event
from circleshape import CircleShape
import pygame
from constants import ASTEROID_KINDS, GAME_DIFFICULTY, LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_HEIGHT,SCREEN_WIDTH

class Asteroid(CircleShape):
    def __init__(self, x:float, y:float, radius: float, kind: int, game_difficulty: GAME_DIFFICULTY) -> None:
        super().__init__(x,y,radius)
        self.kind = kind
        self.points = (ASTEROID_KINDS - kind + 1 ) * 5
        self.game_difficulty: GAME_DIFFICULTY = game_difficulty
        
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, 'white', self.position, self.radius, LINE_WIDTH)
    
    def bounce(self, x:bool = False, y:bool= False):
        self.velocity.x *= -1 if x else 1
        self.velocity.y *= -1 if y else 1

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        match self.game_difficulty:
            case GAME_DIFFICULTY.EASY:
                if self.reached_any_border():
                    self.kill()
            case GAME_DIFFICULTY.HARD:
                if self.reached_X_border(-self.radius):
                    self.bounce(x=True)
                if self.reached_Y_border(-self.radius):
                    self.bounce(y=True)

    
    def split(self)->None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event('asteroid_split')
        rand_angle = random.uniform(20, 50)
        first_vector = self.velocity.rotate(rand_angle)
        second_vector = self.velocity.rotate(-rand_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        first_ast = Asteroid(self.position.x, self.position.y, new_radius, self.kind-1, self.game_difficulty)
        second_ast = Asteroid(self.position.x, self.position.y, new_radius, self.kind-1, self.game_difficulty)
        first_ast.velocity = first_vector * 1.2
        second_ast.velocity = second_vector * 1.2
        