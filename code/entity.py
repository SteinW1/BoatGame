import pygame
from autopilot import Autopilot

class Entity(pygame.sprite.Sprite):
    def __init__(self, sprite_group):
        super().__init__(sprite_group)
        
        self.direction = pygame.math.Vector2()
        self.rect = pygame.Rect(0,0,0,0)
        self.position = self.rect.x, self.rect.y
        self.animation_frame_index = 0
        self.animation_speed = 0.1 # lower is slower

        self.hitbox_xoffset = 0
        self.hitbox_yoffset = 0
        self.hitbox_width = 0
        self.hitbox_height = 0
        self.hitbox_position = (self.rect.x + self.hitbox_xoffset, self.rect.y + self.hitbox_yoffset)
        self.hitbox = pygame.Rect(self.hitbox_position,(self.hitbox_width, self.hitbox_height))
    
    def detect_collision(self, rect_new_x, rect_new_y):
        for sprite in self.collidable_sprites:
            if sprite.hitbox.colliderect(rect_new_x):
                self.x_change = 0
            if sprite.hitbox.colliderect(rect_new_y):
                self.y_change = 0

    def update_hitbox(self, rect):
        hitbox_position = (rect.x + self.hitbox_xoffset, rect.y + self.hitbox_yoffset)
        hitbox = pygame.Rect(hitbox_position,(self.hitbox_width, self.hitbox_height))
        return hitbox

    def move(self, entity_speed):

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        if not self.autopilot_on:
            self.x_change = self.direction.x * entity_speed
            self.y_change = self.direction.y * entity_speed
    
            test_rect_new_x = pygame.Rect((self.position[0] + self.x_change, self.position[1]),(self.rect.width, self.rect.height))
            new_x_hitbox = self.update_hitbox(test_rect_new_x)
            test_rect_new_y = pygame.Rect((self.position[0], self.position[1] + self.y_change),(self.rect.width, self.rect.height))
            new_y_hitbox = self.update_hitbox(test_rect_new_y)
    
            self.detect_collision(new_x_hitbox, new_y_hitbox)        
    
            self.position = self.position[0] + self.x_change, self.position[1] + self.y_change
            self.rect.x, self.rect.y = self.position[0], self.position[1]
            self.hitbox = self.update_hitbox(self.rect)
        else:
            pass
