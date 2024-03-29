import pygame
from game import GAME

def run(screen,state_runs):
    game = GAME(screen)
    clock = pygame.time.Clock()

    while True:
        screen.fill((255, 180, 80))
        clock.tick(60)
        game.run()

        pygame.display.flip()