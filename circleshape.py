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

    def collides_with(self, other: "CircleShape")->bool:
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius