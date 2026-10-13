import pygame

from circleshape import CircleShape
from constants import  PLAYER_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_SHOOT_SPEED, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED
from game import Game
from shot import Shot

class Player(CircleShape):
    def __init__(self, x: float, y:float, game: Game):
        super().__init__(x,y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.game = game
        
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.polygon(screen, 'white', self.triangle(), LINE_WIDTH)
    
    def rotate(self, dt: float):
        self.rotation +=dt*PLAYER_TURN_SPEED
    
    def update(self, dt: float) -> None:
        self.cooldown-=dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt*3 if keys[pygame.K_LSHIFT] else dt)
        if keys[pygame.K_s]:
            self.move(-dt*3 if keys[pygame.K_LSHIFT] else -dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def wrap(self, left: bool = False, right: bool = False, top: bool = False, bottom: bool = False)->None:
        x = SCREEN_WIDTH if left else 0 if right else self.position.x
        y = SCREEN_HEIGHT if top else 0 if bottom else self.position.y
        self.position = pygame.Vector2(x,y)
    
    def move(self, dt: float):
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        if self.reached_any_border(self.radius):
            left=self.reached_left_border(self.radius)
            right = self.reached_right_border(self.radius)
            top = self.reached_top_border(self.radius)
            bottom = self.reached_bottom_border(self.radius)
            self.wrap(left, right, top, bottom)
    
    def shoot(self):
        if self.cooldown > 0:
            return
        self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        r = range(0,1)
        angle = 0
        if self.game.level > 1:
            angle = 5
        if self.game.level > 2:
            r = range(-1,2)
        if self.game.level > 3:
            angle = 10
            r = range(-2,3)
        for i in r:
            shot = Shot(self.position.x, self.position.y)
            unit_vector = pygame.Vector2(0,1)
            rotated_unit_vector = unit_vector.rotate(self.rotation + i*angle) * PLAYER_SHOOT_SPEED
            shot.velocity = rotated_unit_vector

    
    def respawn(self, x: int | None = None, y: int | None = None):
        pos_x = SCREEN_WIDTH/2 if x is None else x
        pos_y = SCREEN_HEIGHT/2 if y is None else y
        self.position = pygame.Vector2(pos_x,pos_y)
        self.radius = PLAYER_RADIUS
        self.rotation = 0
        self.cooldown = 0