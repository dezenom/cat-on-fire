import pygame,sys
sys.path.append('src')
from src.settings import *
import src.states.menu as menu
import src.states.gameplay as game
import src.states.levelchanger as lvlchange

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.SCALED)

state_runs = {"menu":menu.run,"lvlchange":lvlchange.run ,"game":game.run}

state_runs['menu'](screen,state_runs)
