import pygame
from constants import GAME_DIFFICULTY, SCREEN_HEIGHT, SCREEN_WIDTH
from game import Game
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from info import Info
import sys

def main():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)
    Info.containers = (drawable,)
    game = Game(0,3, GAME_DIFFICULTY.HARD)

    info = Info(2, 2, 200, 100, game)
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    AsteroidField(game)

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f'Screen width: {SCREEN_WIDTH}')
    print(f'Screen height: {SCREEN_HEIGHT}')

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return

        screen.fill('black')
        
        for d in drawable:
            info.draw(screen)
            d.draw(screen)
            
        pygame.display.flip()
        dt = clock.tick(60)/1000
        updatable.update(dt)

        for a in asteroids:
            if not isinstance(a, Asteroid):
                continue   
            if a.collides_with(player):
                log_event('player_hit')
                a.kill()
                player.respawn()
                game.update_lives(-1)
                if game.lives<=0:
                    print('Game over!')
                    sys.exit(1)
                need_to_break = False
                for ast in asteroids:
                    ast.kill()
                    need_to_break = True
                for shot in shots:
                    shot.kill()
                if need_to_break:
                    break
            for s in shots:
                if not isinstance(s, Shot):
                    continue
                if a.collides_with(s):
                    log_event('asteroid_shot')
                    game.update_score(a.points)
                    a.split()
                    s.kill()


if __name__ == "__main__":
    main()
