import pygame,globals
from particles import particle_system
from random import randint

jump_particles = particle_system()
fire_particles = particle_system()

class player():
    def __init__(self,pos,screen):
        self.screen = screen
        self.image = pygame.Surface((12,16))
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        # movement
        self.direction = pygame.Vector2((1,0))
        self.friction = 0.6
        self.speedx = 0
        self.speedy = -13
        self.maxspeed = 5
        self.acceleration = 0.8

        # jump
        self.gravity = 0.8
        self.on_ground = False
        self.jump = False
        self.jumpcount = 2
        self.jumpmax = 2
        # animation
        self.frames = {"idle":[],"run":[],"jump":[],"fall":[]}
        self.status = "idle"
        self.is_left = False
        # checkpoints
        self.steps = 0
        self.maxsteps = 1000

    # player movement
    def keys(self):
        keys = pygame.key.get_pressed()
        if self.jump and (self.on_ground or self.jumpcount <self.jumpmax):
            self.on_ground = False
            self.jumpcount += 1
            self.direction.y = 0
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
            self.jumpcount = 0

        self.jumpmax = 2 if self.speedx >= self.maxspeed -2 and globals.cool_on else 1
        
        self.steps += self.speedx
        self.keys()
        self.applyfriction()
    def get_status(self):
        if self.direction.y <0:
            self.status = 'jump'
        elif self.direction.y>1:
            self.status = 'fall'
        else:
            if self.speedx <= 0.2:
                self.status = 'idle'
            else:
                self.status = 'run'
    # draw and update
                
    def flame(self):
        fire_particles.add_particle([self.rect.x+ self.rect.w/2,self.rect.y-10],5,(randint(1,255),40*self.speedx,50*self.speedx))

    def draw(self):
        self.screen.blit(self.image,self.rect)
        jump_particles.emit(self.screen,1,-2,3)
        fire_particles.emit(self.screen,-1,-3,3)
    def update(self):
        self.movement()
        self.flame()
        self.draw()