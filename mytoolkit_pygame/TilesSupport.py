import pygame,globals
from sys import path
path.append("resources")
from resources.levels import levels
from settings import WIDTH,HEIGHT
#### utils #####


def get_image(image_source,framex,size=[16,16],layery=0):
    fullimage = pygame.image.load(image_source)
    image = pygame.Surface((size[0],size[1]))
    lengthx = fullimage.get_width()/size[0] -1
    if framex > lengthx :
        layery += int(framex//lengthx)
        framex = int(framex%lengthx)-layery

    image.blit(fullimage,(framex*-size[0],layery*-size[1],size[0],size[1]))
    image.set_colorkey((0,0,0))

    return image
def render_text(screen,text,pos,fonts,size):
    font = pygame.font.Font(fonts,size)
    text = font.render(text,False,(50,50,50))
    rect = text.get_rect(center = pos)
    screen.blit(text,rect)
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,imagesource,group,tile_type,framex,x= None,y = None,size= [16,16],scale = 1):
        super().__init__(group)

        # image , tile type and rect 
        # with tile type all tiles can be in one group , is that optimal, absolutely not 

        self.image = pygame.transform.scale_by(get_image(imagesource,framex,size = size),scale)
        self.tile_type = tile_type
        self.rect = self.image.get_frect(topleft=pos)
        
        # position in level array
        self.level_x,self.level_y = x,y
        self.frame = framex

    def draw(self,screen):
        screen.blit(self.image,self.rect)   
    def update(self,direction):

        #camera

        self.rect.x -= direction[0]
        self.rect.y -= direction[1]
class Buttons ():
    def __init__(self,pos,screen,scale,imagesource) :
        self.screen = screen
        self.playimage, self.exitimage = pygame.transform.scale_by(get_image(imagesource,5,size=[40,30]),scale),pygame.transform.scale_by(get_image(imagesource,6,size=[40,30]),scale)
        self.playrect, self.exitrect = self.playimage.get_frect(center = pos[0]),self.playimage.get_frect(center = pos[1])
        self.collide = False

    def render(self):
        
        self.screen.blit(self.playimage,self.playrect)
        self.screen.blit(self.exitimage,self.exitrect)


    def update(self,click):
        # check mouse collision

        if self.playrect.collidepoint(pygame.mouse.get_pos()):
            if click:
                return "play"
            else: return ""
        if self.exitrect.collidepoint(pygame.mouse.get_pos()):
            if click:
                return "exit"
            else :return ""
        return ""



#### tilemanager #####
        


class TILE_SUPPORT():
    def __init__(self,game) :
        self.group = pygame.sprite.Group()
        self.game = game
        self.world_layer = levels(globals.Current_level)

        self.set_world()
        self.sieve_tiles()
        for rect in self.sieved_tiles["playerpos"]:
            self.game.player.rect.x = rect.x
            self.game.player.rect.y = rect.y
            self.game.player.checkpoint =  self.game.player.rect 

        
    
    def set_world(self):
        size = 16
        for key in self.world_layer.keys():
            self.array_tiles(self.world_layer[key][0],key,self.world_layer[key][1])

    def sieve_tiles(self):
        self.sieved_tiles = {}
        for key in self.world_layer.keys():
            self.sieved_tiles[key] = self.tile_sieve(key)


    # used to spawn array maps
        
    def array_tiles(self,Array,tile_type,imagesource,size = [16,16]):
        for row_index,row in enumerate(Array):
            for col_index,col in enumerate(row):
                y = row_index * size[0]
                x = col_index * size[1]
                if col>-1:
                    tiles = Tile((x,y),imagesource,self.group,tile_type,col,col_index,row_index,size = size)

    # collision checker / returns a list of every hit object in the group
    
    def tile_sieve(self,sprite_type):
        hit_list = []
        for sprite in self.group.sprites():
            if sprite.tile_type == sprite_type:
                hit_list.append(sprite.rect)
        return hit_list
    
    # special tiles  collision and reactions
    def special_collision(self):
        for rect in self.sieved_tiles["GOUPS"]:
            if rect.colliderect(self.game.player.rect):
                globals.Current_level+=1
                self.game.running = False
                break
        for rect in self.sieved_tiles["GODOWNS"]:
            if rect.colliderect(self.game.player.rect):
                globals.Current_level+=-1
                self.game.running = False
                break
        
        # burnables
        for sprite in self.group.sprites():
            if sprite.frame == 3:
                if sprite.rect.colliderect(self.game.player.rect):
                    globals.cool_on = True

    def platformer_physics(self):
        self.game.player.applygravity()
        for rect in self.sieved_tiles["physics"]:
            if rect.colliderect(self.game.player.rect):
                if self.game.player.direction.y > 0: 
                    self.game.player.rect.bottom = rect.top
                    self.game.player.direction.y = 0
                    
                    self.game.player.on_ground = True
                elif self.game.player.direction.y < 0:
                    self.game.player.rect.top = rect.bottom
                    self.game.player.direction.y = 0
        if self.game.player.direction.y > self.game.player.gravity or self.game.player.direction.y < 0:
            self.game.player.on_ground = False

        self.game.player.rect.x += self.game.player.direction.x * self.game.player.speedx

        for rect in self.sieved_tiles["physics"]:
            if rect.colliderect(self.game.player.rect):
                if self.game.player.direction.x < 0: 
                    self.game.player.rect.left = rect.right
                elif self.game.player.direction.x > 0:
                    self.game.player.rect.right = rect.left
        # there is supposed to be ramp collision water collisions and whatnots but ill not have them this jam i guess


    def render(self,screen):
        for sprite in self.group.sprites():
            if (sprite.rect.x>-16 and sprite.rect.x<WIDTH+16) and (sprite.rect.y>-16 and sprite.rect.y<HEIGHT+16) :
                sprite.draw(screen)


    def update(self,scroll):

        for rect in self.sieved_tiles["playerpos"]:
            if self.game.player.rect.y - rect.y > HEIGHT*2:
                self.game.running = False

        self.group.update(scroll)
        self.platformer_physics()
        self.special_collision()
        