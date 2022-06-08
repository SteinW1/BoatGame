import pygame
from settings import *

class Button:
    def __init__(self, x, y, w, h, msg=None, text_alignment='center'):
        
        self.display_surface = pygame.display.get_surface()
        
        # setup button rect
        self.rect = x, y, w, h
        
        # setup button graphics
        self.active_color = (255, 255, 255)
        self.inactive_color = (255, 0, 0)
        
        if msg:
            # setup button text
            self.has_text = True
            self.message = msg
            self.text_color = (0, 0, 0)
            self.text_alignment = text_alignment
            self.text_position = self.rect[0] + self.rect[2]/2, self.rect[1] + self.rect[3]/2
            
            #
            self.font_object = pygame.font.SysFont(None, UI_FONT_SIZE)
            self.textBoxSurface = self.font_object.render(self.message, True, 'black')
            self.textBoxRect = self.textBoxSurface.get_rect()

            # set the text position to match the requested text alignment
            
            if self.text_alignment.upper() == 'LEFT':
                self.textBoxRect.topleft = self.text_position[0], self.text_position[1]
            elif self.text_alignment.upper() == 'CENTER':
                self.textBoxRect.center = self.text_position[0], self.text_position[1]
            elif self.text_alignment.upper() == 'RIGHT':
                self.textBoxRect.topright = self.text_position[0], self.text_position[1]

    def detect_activity(self, mouse_pos):
        """
        Calls functions to detect if the mouse is over the button.
        
        Parameters:           
            mouse_pos:
        """
        # check if button is actively being moused over
        if self.rect[0] + self.rect[2] > mouse_pos[0] > self.rect[0] and self.rect[1] + self.rect[3] > mouse_pos[1] > self.rect[1]:
            self.active = True
        else:
            self.active = False

    def draw(self):
        """
        Draws all elements of the button
        """
        # draw the button background
        if self.active:
            pygame.draw.rect(self.display_surface, self.inactive_color, self.rect)
        else:
            pygame.draw.rect(self.display_surface, self.active_color, self.rect)
        
        # draw the button text if it exists
        if self.has_text:
            self.display_surface.blit(self.textBoxSurface, self.textBoxRect)
    
    def update(self, mouse_pos):
        self.detect_activity(mouse_pos)
        self.draw()