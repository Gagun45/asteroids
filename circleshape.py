import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float, points: int = 0) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.points = points

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass
    
    def reached_top_border(self, include_radius:bool = False)->bool:
        padding = self.radius if include_radius else 0
        return self.position.y < -padding

    def reached_bottom_border(self, include_radius:bool = False)->bool:
            padding = self.radius if include_radius else 0
            return self.position.y > SCREEN_HEIGHT + padding
    
    def reached_left_border(self, include_radius:bool = False)->bool:
        padding = self.radius if include_radius else 0
        return self.position.x < -padding
    
    def reached_right_border(self, include_radius:bool = False)->bool:
        padding = self.radius if include_radius else 0
        return self.position.x > SCREEN_WIDTH + padding
    
    def reached_X_border(self, include_radius:bool = False, include_radius_left:bool = False, include_radius_right:bool = False)->bool:
        return self.reached_left_border(include_radius or include_radius_left) or self.reached_right_border(include_radius or include_radius_right)
    
    def reached_Y_border(self, include_radius:bool = False,include_radius_top:bool = False, include_radius_bottom:bool = False)->bool:
        return self.reached_top_border(include_radius or include_radius_top) or self.reached_bottom_border(include_radius or include_radius_bottom)
    
    def reached_any_border(self, include_radius:bool=False, include_radius_X:bool = False, include_radius_Y:bool=False)->bool:
        return self.reached_X_border(include_radius or include_radius_X) or self.reached_Y_border(include_radius or include_radius_Y) 

    def collides_with(self, other: "CircleShape")->bool:
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius