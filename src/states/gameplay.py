import pygame,time
from game import GAME

def run(screen,state_runs):
    game = GAME(screen)
    clock = pygame.time.Clock()
    FPS = 60

    interval = 1000000000/FPS
    last_time = time.time_ns()
    delta = 0

    while game.running:
        screen.fill((255, 180, 80))
        clock.tick(FPS)
        
        current_time = time.time_ns()

        delta += (current_time-last_time)/interval


        if delta>=1:
            game.update()
            game.render()

        pygame.display.flip()