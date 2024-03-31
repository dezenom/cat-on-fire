import pygame,sys
from globals import radio

def run(screen,state_runs):
    clock = pygame.time.Clock()

    while True:
        radio.play_music()
        screen.fill("white")
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    state_runs['lvlchange'](screen,state_runs)

        pygame.display.flip()