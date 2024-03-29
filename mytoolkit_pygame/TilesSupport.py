import pygame,globals
from sys import path
path.append("resources")
from resources import levels as lvls

#### utils #####


def get_image(size,image_source,frame):
    image = pygame.Surface((size,size))
    image.blit(pygame.image.load(image_source),(frame*-size,0,size,size))
    image.set_colorkey((0,0,0))

    return image
def render_text(screen,text,pos,fonts,size):
    font = pygame.font.Font(fonts,size)
    text = font.render(text,False,(50,50,50))
    rect = text.get_rect(center = pos)
    screen.blit(text,rect)
class tile(pygame.sprite.Sprite):
    def __init__(self,pos,imagesource,group,tile_type,frame,x,y):
        super().__init__(group)

        # image , tile type and rect 
        # with tile type all tiles can be in one group , is that optimal, absolutely not 

        self.image = get_image(16,imagesource,frame)
        self.tile_type = tile_type
        self.rect = self.image.get_frect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        
        # position in level array
        self.level_x,self.level_y = x,y
        self.frame = frame
    def update(self,direction):

        #camera

        self.rect.x -= direction[0]
        self.rect.y -= direction[1]
class buttons ():
    def __init__(self,pos,screen,scale,imagepath,font) :
        self.screen = screen
        image = pygame.image.load(imagepath).convert_alpha()
        self.image = pygame.transform.scale(image,scale)
        self.rect = self.image.get_frect(topleft = pos)
        self.collide = False
        self.font = font
    def render_text(self,text,pos,size):
        font = pygame.font.Font(self.font,size)
        text = font.render(text,False,(50,50,50))
        rect = text.get_rect(center = pos)
        self.screen.blit(text,rect)

    def update(self,text):
        # check mouse collision

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.collide = True
        else:
            self.collide = False
    
        # drawing text if there and button
    
        self.screen.blit(self.image,self.rect)
        self.render_text(text,(self.rect.centerx,self.rect.centery),10)




#### tilemanager #####
        


class TILE_SUPPORT():
    def __init__(self,game):
        self.group = pygame.sprite.Group()
        self.game = game
        self.world_layer = lvls.all_levels[globals.Current_level]

        self.set_world()
        self.sieve_tiles()
        
    
    def set_world(self):
        size = 16
        self.array_tiles(self.world_layer,size,"All","resources/prototype.png")

    def sieve_tiles(self):
        self.PHYSICS_TILES = self.tile_sieve(0)
        self.GOUPS = self.tile_sieve(1)
        self.GODOWNS = self.tile_sieve(2)

    # used to spawn array maps
        
    def array_tiles(self,Array,size,tile_type,imagesource):
        for row_index,row in enumerate(Array):
            for col_index,col in enumerate(row):
                y = row_index * size
                x = col_index * size
                if col>-1:
                    tiles = tile((x,y),imagesource,self.group,tile_type,col,col_index,row_index)

    # collision checker / returns a list of every hit object in the group
    
    def tile_sieve(self,sprite_type):
        hit_list = []
        for sprite in self.group.sprites():
            if type(sprite_type) == str:
                if sprite.tile_type == sprite_type:
                    hit_list.append(sprite.rect)
            if type(sprite_type) == int:
                if sprite.frame == sprite_type:
                    hit_list.append(sprite.rect)

        return hit_list
    
    # special tiles  collision and reactions
    def special_collision(self):
        for rect in self.GOUPS:
            if rect.colliderect(self.game.player.rect):
                globals.Current_level+=1
                self.game.running = False
                break
        for rect in self.GODOWNS:
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
        for rect in self.PHYSICS_TILES:
            if rect.colliderect(self.game.player.rect):
                if self.game.player.direction.y > 0: 
                    self.game.player.rect.bottom = rect.top
                    self.game.player.direction.y = 0
                    self.game.player.on_ground = True
                elif self.game.player.direction.y < 0:
                    self.game.player.rect.top = rect.bottom
                    self.game.player.direction.y = 0
        if self.game.player.direction.y > 1 or self.game.player.direction.y < 0:
            self.game.player.on_ground = False

        self.game.player.rect.x += self.game.player.direction.x * self.game.player.speedx

        for rect in self.PHYSICS_TILES:
            if rect.colliderect(self.game.player.rect):
                if self.game.player.direction.x < 0: 
                    self.game.player.rect.left = rect.right
                elif self.game.player.direction.x > 0:
                    self.game.player.rect.right = rect.left
        # there is supposed to be ramp collision water collisions and whatnots but ill not have them this jam i guess

    def update(self,scroll,screen):
        self.group.update(scroll)
        self.group.draw(screen)
        self.platformer_physics()

        # special tiles
        self.special_collision()
        