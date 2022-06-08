import pygame
from settings import *

class PlayerBoxCamera:
    def __init__(self, level):
        
        # grab game display
        self.display_surface = pygame.display.get_surface()
        self.display_width = WINDOW_WIDTH
        self.display_height = WINDOW_HEIGHT
        
        # set camera rect
        self.rect = (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # initialize camera offset
        self.offset = pygame.math.Vector2()
        
        # create height and width values for center of display
        self.half_display_width = self.display_surface.get_size()[0] // 2
        self.half_display_height = self.display_surface.get_size()[1] // 2
        
        # create camera rect
        self.camera_rect = pygame.Rect(0, 0, self.display_width, self.display_height)
        
        # set camera boundaries
        self.max_x_position = level.level_width
        self.max_y_position = level.level_height
        
        # camera 'box' setup
        self.camera_borders = {'left': 300, 'right': 300, 'top': 200, 'bottom': 200} # set the size of the camera box
        box_left = self.camera_borders['left'] # create variable for left side
        box_top = self.camera_borders['top'] # create variable for top side
        box_width = self.display_surface.get_size()[0] - self.camera_borders['left'] - self.camera_borders['right']
        box_height = self.display_surface.get_size()[1] - self.camera_borders['top'] - self.camera_borders['bottom']
        
        # create the camera 'box' rect
        self.camera_box_rect = pygame.Rect(box_left, box_top, box_width, box_height)


    def box_target_camera(self) -> None:
        """
        Calculates the camera 'box' that moves the camera position when the camera's target object moves outside of it.
        """
        # check if the camera needs moved
        # camera needs moved when the player collides witht he sides of the camera 'box'
        if self.target.rect.left < self.camera_box_rect.left:
            self.camera_box_rect.left = self.target.rect.left
        if self.target.rect.right > self.camera_box_rect.right:
            self.camera_box_rect.right = self.target.rect.right
        if self.target.rect.top < self.camera_box_rect.top:
            self.camera_box_rect.top = self.target.rect.top
        if self.target.rect.bottom > self.camera_box_rect.bottom:
            self.camera_box_rect.bottom = self.target.rect.bottom
        
        # calculate new offset based on movement of the box
        self.offset.x = self.camera_box_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_box_rect.top - self.camera_borders['top']
        
        # correct the camera so that it will not move out of the map boundary
        if self.offset.x + self.display_width > self.max_x_position:
            self.offset.x = self.max_x_position - self.display_width
            
        if self.offset.y + self.display_height > self.max_y_position:
            self.offset.y = self.max_y_position - self.display_height
            
        if self.offset.x < 0:
            self.offset.x = 0
            
        if self.offset.y < 0:
            self.offset.y = 0

    def draw(self, sprite_group, target, background) -> None:
        """
        Draws all objects in a sprite group.
        
        Parameters:
            sprite_group: The group of sprites that need drawn to the screen.
            
            target: The object that the camera will follow. Needs a rect attribute or function will produce an error.
            
            background: The background that everything will be drawn over the top of.
        """
        
        # set the target that the camera will follow
        self.target = target
        
        # call method to get new camera position
        self.box_target_camera()
        
        # draw background
        ground_offset = background[1].topleft - self.offset
        self.display_surface.blit(background[0], ground_offset)
        
        # draw entities
        for sprite in sorted(sprite_group.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)