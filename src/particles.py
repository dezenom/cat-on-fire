import pygame
from random import randint

class particle_system():
    def __init__(self) :
        self.particles = []
    def add_particle(self,pos,radius,colour):
        radius = radius
        direction = [randint(-2,2),randint(-2,0)]
        particle = [pos,radius,direction,colour]
        self.particles.append (particle)
    def emit(self,screen,directiony,directionx1,directionx2):
        if self.particles:
            self.delete()
            for particle in self.particles:
                particle[0][0] += particle[2][0]* randint(directionx1,directionx2)
                particle[0][1] += particle[2][1]*directiony
                particle[2][1] += 0.3
                particle[1] -= 0.2
                pygame.draw.circle(screen, particle[3],particle[0],particle[1])
    def delete(self):
        particle = [particle for particle in self.particles if particle[1]<70]
        self.particles = particle