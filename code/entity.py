import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, sprite_group):
        super().__init__(sprite_group)
        
        # setup default values
        self.direction = pygame.math.Vector2()
        self.rect = pygame.Rect(0,0,0,0)
        self.frame_index = 0
        self.animation_speed = 0.1 # lower is slower

        # default hitbox setup
        self.hitbox_xoffset = 0
        self.hitbox_yoffset = 0
        self.hitbox_width = 0
        self.hitbox_height = 0
        self.hitbox_position = (self.rect.x + self.hitbox_xoffset, self.rect.y + self.hitbox_yoffset)
        self.hitbox = pygame.Rect(self.hitbox_position,(self.hitbox_width, self.hitbox_height))
        
    def collision(self, direction):
        
        # test for horizontal collisions, reset the hitbox if there is a collision
        if direction == 'horizontal':
            for sprite in self.collidable_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    
                    if self.direction.x > 0:                    # if moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:                  # if moving left
                        self.hitbox.left = sprite.hitbox.right
                    
                    return True
                    
        # test for vertical collisions, reset the hitbox if there is a collision
        if direction == 'vertical':
            for sprite in self.collidable_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    
                    if self.direction.y > 0:                    # if moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:                  # if moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    
                    return True
                    
    def move(self, speed):
        
        # check if the player is moving and normalize their movement vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # reset entity hitbox before testing for collisions
        self.hitbox.x, self.hitbox.y = self.rect.x + self.hitbox_xoffset, self.rect.y + self.hitbox_yoffset
        
        # calculation change in position
        x, y = self.position
        x_change = self.direction.x * speed
        y_change = self.direction.y * speed
        
        # check for horizontal collisions
        self.hitbox_test_position = self.hitbox.x + x_change, self.hitbox.y
        self.hitbox.topleft = self.hitbox_test_position
        if self.collision('horizontal'): # if horizontal collision
            x_change = 0
        
        # check for vertical collisions
        self.hitbox_test_position = self.hitbox.x, self.hitbox.y + y_change
        self.hitbox.topleft = self.hitbox_test_position
        if self.collision('vertical'):                                          # test for a vertical collision using the updated hitbox
            y_change = 0                                                        # if vertical collision do not change entity y position
        
        # update entity position
        self.position = x + x_change, y + y_change
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]