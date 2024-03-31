import pygame,time
from game import GAME
from globals import radio

def run(screen,state_runs):
    game = GAME(screen)
    clock = pygame.time.Clock()
    FPS = 60

    while game.running:
        radio.play_music()

        screen.fill((200, 70, 90))
        clock.tick(FPS)
        
        game.update()
        game.render()
            
        pygame.display.flip()