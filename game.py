from constants import GAME_DIFFICULTY


class Game:
    def __init__(self, score: int, lives: int, difficulty: GAME_DIFFICULTY) -> None:
        self.score = score
        self.lives = lives
        self.difficulty = difficulty
        
    def update_score(self, increment: int)->None:
        self.score += increment
    
    def update_lives(self, increment: int)->None:
        self.lives+=increment