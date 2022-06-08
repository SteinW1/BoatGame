import pygame
from settings import *

class TileObject(pygame.sprite.Sprite):
    def __init__(self, position, group, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(group)
        self.sprite_type = sprite_type # delete this and the argument?
        self.image = surface
        self.rect = self.image.get_rect(topleft = (position[0], position[1] - TILESIZE))
        
        if sprite_type == 'object': # use 'object' for invisible collidable objects
            self.rect = self.image.get_rect(topleft = (position[0], postion[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = position)
        #self.hitbox = self.rect.inflate(0, 0) # remove .inflate(0,0)? unnecessary because not changing hitbox size?
        self.hitbox = self.rect