import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_state, log_event
from player import Player
from asteroids import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys
import random

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clck = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    asteriod_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill('black')
        updatable.update(dt)
        for ast in asteroids:
            col = player.collides_with(ast)
            if col:
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for shot in shots:
                hit = ast.collides_with(shot)
                if hit:
                    log_event("asteroid_shot")
                    ast.kill()
                    shot.kill()
                    if ast.radius <= ASTEROID_MIN_RADIUS:
                        return
                    else:
                        log_event("asteroid_split")
                        deg = random.uniform(20, 50)
                        new_ast_1 = Asteroid(ast.position.x, ast.position.y, ast.radius - ASTEROID_MIN_RADIUS)
                        new_ast_2 = Asteroid(ast.position.x, ast.position.y, ast.radius - ASTEROID_MIN_RADIUS)
                        new_ast_1.velocity = ast.velocity.rotate(deg) * 1.2
                        new_ast_2.velocity = ast.velocity.rotate(-deg) * 1.2






        for draw1 in drawable:
            draw1.draw(screen)
        pygame.display.flip()
        dt = clck.tick(60)/1000
        



if __name__ == "__main__":
    main()
