from constants import GAME_DIFFICULTY
from game import Game
from rectshape import RectShape
from player import Player
import pygame

class Info(RectShape):
    def __init__(self, left, top, width, height, game: Game):
        super().__init__(left, top, width, height)
        self.game = game
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, 'white', self.rect, width=1)
        font = pygame.font.Font(None, 28)
        text_lines:list[tuple[str, str]] = []
        
        score_text = f'Score: {self.game.score}'
        level_text = f'Level: {self.game.level}'
        next_level_score_next = f'Next: {self.game.next_level_score}'
        score_color = 'green'

        
        lives_text = f'Lives: {self.game.lives}'
        lives_color = 'blue'
        
        
        text_lines.append((score_text, score_color))
        text_lines.append((level_text, score_color))
        text_lines.append((next_level_score_next, score_color))
        text_lines.append((lives_text, lives_color))
        
        for index, line in enumerate(text_lines):
            text, color = line
            to_render = font.render(text, False, color)
            screen.blit(to_render, (self.rect.left +10, self.rect.top + 25 + index * 15))