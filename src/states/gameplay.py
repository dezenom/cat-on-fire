import pygame,time
from game import GAME
from globals import radio,start_time
from time import time
from mytoolkit_pygame.TilesSupport import render_text


def run(screen,state_runs):
    game = GAME(screen)
    clock = pygame.time.Clock()
    FPS = 60

    game_start = time()

    while game.running:
        radio.play_music()

        screen.fill((200, 120, 90))
        clock.tick(FPS)
        
        game.update()
        game.render()
        render_text(screen,str(int(time()-start_time)),(40,40),"resources/Daydream.ttf",20)
        pygame.display.flip()