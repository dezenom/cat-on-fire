import pygame
from sys import path
path.append("resources")
from resources import levels as lvls


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


class TILE_SUPPORT():
    def __init__(self):
        self.group = pygame.sprite.Group()
        
        self.world_layer = lvls.current_level

        self.set_world()
        self.sieve_tiles()
        
    
    def set_world(self):
        size = 16
        self.array_tiles(self.world_layer[0],size,"physics","resources/prototype.png")
        self.array_tiles(self.world_layer[1],size,"goups","resources/prototype.png")

    def sieve_tiles(self):
        self.PHYSICS_TILES = self.tile_sieve("physics")
        self.GOUPS = self.tile_sieve("goups")

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
            if sprite.tile_type == sprite_type:
                hit_list.append(sprite.rect)
        return hit_list
    
    # special tiles  collision and reactions
    def special_collision(self,player):
        for rect in self.GOUPS:
            if rect.colliderect(player.rect):
                print("GOOOOO UP")
    def platformer_physics(self,player):
        player.applygravity()
        for rect in self.PHYSICS_TILES:
            if rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = rect.bottom
                    player.direction.y = 0
        if player.direction.y > 1 or player.direction.y < 0:
            player.on_ground = False

        player.rect.x += player.direction.x * player.speedx

        for rect in self.PHYSICS_TILES:
            if rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = rect.right
                elif player.direction.x > 0:
                    player.rect.right = rect.left
        # there is supposed to be ramp collision water collisions and whatnots but ill not have them this jam i guess

        return player.rect

    def update(self,playerIN,scroll,screen):
        self.group.update(scroll)
        self.group.draw(screen)
        playerIN.rect = self.platformer_physics(playerIN)

        # special tiles
        self.special_collision(playerIN)
        