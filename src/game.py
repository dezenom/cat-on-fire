import pygame,sys
sys.path.append("mytoolkit_pygame")

from mytoolkit_pygame.TilesSupport import TILE_SUPPORT
from settings import *
from player import player

class GAME():
    def __init__(self,display):
        # screen
        self.screen = display
        self.screen_w,self.screen_h = WIDTH,HEIGHT

        # basic scroll camera 
        self.scroll = (0,0)
        self.camera_entities = []

        # level/world
        self.TileManager = TILE_SUPPORT()

        self.player = player((30,30),self.screen)
        self.camera_entities.append(self.player.rect)


#camera  
        
    def getscroll(self):
        scroll = [0,0]
        scroll[0] += self.player.rect.x - scroll[0] - self.screen_w/2
        scroll[1] += self.player.rect.y - scroll[1] - self.screen_h/2
        return scroll
    def camera(self):
        self.scroll = self.getscroll()
        self.scroll[0] = self.scroll[0]//10
        self.scroll[1] = self.scroll[1]//10
        for rect in self.camera_entities:
            rect.x -= self.scroll[0]
            rect.y -= self.scroll[1]


# events
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.jump = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True

# sprites
    
    def spritecontrol(self):
        self.camera()
        self.TileManager.update(self.player,self.scroll,self.screen)
        self.player.update()
        

    def run(self):
        self.event_handler()
        self.spritecontrol()