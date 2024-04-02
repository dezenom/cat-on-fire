import pygame
from particles import particle_system
from random import randint
from mytoolkit_pygame.AnimationHandler import ANIMATION_HANDLER
from globals import radio

jump_particles = particle_system()
fire_particles = particle_system()

player_animations = ANIMATION_HANDLER(1,"resources/Animations/spritesheet.png",[24,20]) 

class player():
    def __init__(self,pos,screen):
        self.screen = screen
        self.image = pygame.Surface((24,20))
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        # movement
        self.direction = pygame.Vector2((1,0))
        self.friction = 0.6
        self.speedx = 0
        self.speedy = -8
        self.maxspeed = 5
        self.acceleration = 0.8

        # jump
        self.gravity = 0.4
        self.on_ground = False
        self.jump = False
        self.jumpcount = 2
        self.jumpmax = 2
        # animation
        self.get_status()
        self.is_left = False

    # player movement
    def keys(self):
        keys = pygame.key.get_pressed()
        if self.jump and (self.on_ground or self.jumpcount <self.jumpmax):
            self.on_ground = False
            self.jumpcount += 1
            self.direction.y = 0
            radio.play_effect("jump")
            self.jumping()
        self.jump = False
        if keys[pygame.K_a] and self.speedx < self.maxspeed:
            self.direction.x = -1
            self.is_left = True
            self.speedx += self.acceleration
        elif keys[pygame.K_d] and self.speedx < self.maxspeed:
            self.direction.x = 1
            self.is_left = False
            self.speedx += self.acceleration
    def applyfriction(self):
        self.speedx -= self.friction
        if self.speedx <= 0.1:
            self.speedx = 0
    def applygravity(self):
        self.direction.y += self.gravity if self.direction.y < 30 else 0 
        self.rect.y += self.direction.y 

    def jumping(self):
        if self.jumpcount == 2:
            for i in range(5):
                jump_particles.add_particle([self.rect.x + self.rect.w/2,self.rect.y + self.rect.h],8,(50*i,150,200))
        self.direction.y = self.speedy
        self.rect.y += self.direction.y
    def movement(self):
        if self.on_ground:
            if self.jumpcount>0:
                radio.play_effect("hit")
            self.jumpcount = 0

        
        self.keys()
        self.applyfriction()
    def get_status(self):
        if self.direction.y <0:
            self.status = 2
        elif self.direction.y>0.8:
            self.status = 3
        else:
            if self.speedx <= 0.2:
                self.status = 0
            else:
                self.status = 1
    # draw and update
                
    def render_controls(self):
        self.get_status()


    def render(self):
        jump_particles.emit(self.screen,3,-2,3)
        self.screen.blit(self.image,self.rect)
    def update(self):
        self.image = player_animations.animation(self.status,self.is_left)
        self.movement()
        self.render_controls()