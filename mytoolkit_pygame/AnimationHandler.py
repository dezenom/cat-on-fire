from os import walk
import pygame

def frames(path,scale):
    surface_list=[]
    for i,ii,filename in walk(path):
        for file in filename:
            file = path + '/' + file
            image= pygame.transform.scale_by(pygame.image.load(file).convert_alpha(),scale)
            surface_list.append(image)
    return surface_list 

class ANIMATION_HANDLER():
    def __init__(self,framedict,animation_speed, animation_path) :
        self.animation_path = animation_path
        
        # all animations
        self.framedict = framedict
        self.getframes(1)

        # animation control
        self.animation_speed = animation_speed
        self.current_index = 0

    def getframes(self,scale):  

        for key in self.framedict.keys():
            fullpath = self.animation_path + key
            self.framedict[key] = frames(fullpath,scale)

    def animation(self,status,left):
        animation = self.framedict[status]
        image = animation[self.current_index//5]
        self.current_index+=1
        if self.current_index >= len(animation)*5:
            self.current_index = 0
        if left:
            image = pygame.transform.flip(animation[self.current_index//5],True,False)
        else:
            image = animation[self.current_index//5]

        return image
    
