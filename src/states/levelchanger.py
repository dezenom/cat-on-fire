from globals import change_level
from mytoolkit_pygame.TilesSupport import render_text
from pygame import display

def run(screen,state_runs):
    while change_level:
        
        screen.fill((2, 180, 80))
        render_text(screen,"LOADING......",(400,200),"resources/Daydream.ttf",20)
        display.flip()
        state_runs["game"](screen,state_runs)