import pygame,sys
from globals import radio
from mytoolkit_pygame.TilesSupport import Buttons

def run(screen,state_runs):
    clock = pygame.time.Clock()
    buttons = Buttons([(320,100),(320,190)],screen,3,"resources/tileset.png")
    while True:
        radio.play_music() 
        clock.tick(60)

        screen.blit(pygame.image.load("resources/bground.png"),(0,0))
        buttons.render()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        

        action = buttons.update(click)
        if action== "play":
            state_runs['lvlchange'](screen,state_runs)
        if action== "exit":
            pygame.quit()
            sys.exit()

        action = 69

        pygame.display.flip()