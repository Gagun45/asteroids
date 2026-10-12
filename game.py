from constants import GAME_DIFFICULTY


class Game:
    def __init__(self, score: int, lives: int, difficulty: GAME_DIFFICULTY) -> None:
        self.score = score
        self.lives = lives
        self.difficulty = difficulty
        self.level = 1
        self.next_level_score = 100
        
    def update_score(self, increment: int)->None:
        self.score += increment
        while self.score > self.next_level_score:
            self.next_level_score+=self.level * 100
            self.level+=1
    
    def update_lives(self, increment: int)->None:
        self.lives = min(3,self.lives+increment)