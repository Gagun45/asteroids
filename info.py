from rectshape import RectShape
from player import Player
import pygame

class Info(RectShape):
    def __init__(self, left, top, width, height, score: int, lives: int):
        super().__init__(left, top, width, height)
        self.score = score
        self.lives = lives
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, 'white', self, width=1)
        font = pygame.font.Font(None, 28)
        text_lines:list[tuple[str, str]] = []
        
        score_text = f'Score: {self.score}'
        score_color = 'green'
        
        lives_text = f'Lives: {self.lives}'
        lives_color = 'blue'
        
        
        text_lines.append((score_text, score_color))
        text_lines.append((lives_text, lives_color))
        
        for index, line in enumerate(text_lines):
            text, color = line
            to_render = font.render(text, None, color)
            screen.blit(to_render, (self.rect.left +10, self.rect.top + 25 + index * 15))
    
    def update_score(self, increment: int)->None:
        self.score += increment
    
    def update_lives(self, increment: int)->None:
        self.lives+=increment