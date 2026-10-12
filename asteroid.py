import random
from explosion import Explosion
from heart import Heart
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
    
    def explode(self, screen: pygame.Surface)->None:
        chance = random.randint(0,10)
        if chance==1:
            heart = Heart(self.position.x, self.position.y, self.radius)
        explosion = Explosion(self.position.x, self.position.y, self.radius)
        self.kill()
    
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

    
    def split(self, screen: pygame.Surface)->None:
        self.explode(screen)
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
    
    def reached_top_border(self, padding:float = 0.0)->bool:
        return self.position.y < -padding and self.velocity.y < 0

    def reached_bottom_border(self, padding:float = 0.0)->bool:
            return self.position.y > SCREEN_HEIGHT + padding and self.velocity.y > 0
    
    def reached_left_border(self, padding:float = 0.0)->bool:
        return self.position.x < -padding and self.velocity.x < 0
    
    def reached_right_border(self, padding:float = 0.0)->bool:
        return self.position.x > SCREEN_WIDTH + padding and self.velocity.x > 0
    
    def reached_X_border(self, padding:float | None = None, padding_left:float | None = None, padding_right:float | None = None)->bool:
        pl: float = padding_left if padding_left is not None else padding if padding is not None else 0.0
        pr: float = padding_right if padding_right is not None else padding if padding is not None else 0.0
        return self.reached_left_border(pl) or self.reached_right_border(pr)
    
    def reached_Y_border(self, padding:float | None = None, padding_top:float | None = None, padding_bottom:float | None = None)->bool:
        pt: float = padding_top if padding_top is not None else padding if padding is not None else 0.0
        pb: float = padding_bottom if padding_bottom is not None else padding if padding is not None else 0.0
        return self.reached_top_border(pt) or self.reached_bottom_border(pb)
    
    def reached_any_border(self, padding:float | None = None, padding_x:float | None = None, padding_y:float | None = None)->bool:
        px: float = padding_x if padding_x is not None else padding if padding is not None else 0.0
        py: float= padding_y if padding_y is not None else padding if padding is not None else 0.0
        
        return self.reached_X_border(px) or self.reached_Y_border(py)
        