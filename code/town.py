import pygame
from ui import Button
from settings import *
from support import *
from debug import debug

class Town:
    def __init__(self, clock):
        self.game_clock = clock
        self.active = False
        
        # get display surface
        self.display_surface = pygame.display.get_surface()
        
        # setup town UI
        self.ui = TownUI(self)
        
    def input(self, states):
        keys = pygame.key.get_pressed()
        mouse_click_status = pygame.mouse.get_pressed()
        
        if keys[pygame.K_q]:
            # switch states
            self.active = False
            states['level'].active = True

    def run(self, states): # called once per game loop
        
        #self.input(states)
        
        mouse_position = pygame.mouse.get_pos()
        mouse_click_status = pygame.mouse.get_pressed()
        
        # draw to the screen
        self.draw()
        
        #update the UI
        self.ui.update(states)
        
        # debug
        fps = self.game_clock.get_fps()
        debug(f'FPS:{round(fps)}')
        
    def draw(self):
        pygame.draw.rect(self.display_surface, (255,0,0), pygame.Rect(100, 100, 100, 100))
        
    def switch_state(self, new_state):        
        self.active = False
        new_state.active = True

class TownUI:
    def __init__(self, parent_state):
        
        # general
        self.parent_state = parent_state
        self.display_surface = pygame.display.get_surface()
        self.display_size = self.display_surface.get_size()
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.graphics_path = f'../graphics/town/'
        
        # setup graphics
        self.background = pygame.image.load(self.graphics_path + 'town_bg.png').convert_alpha()
        
        self.set_sail_button = Button(600, 425, 100,50, 'Set Sail')
        
    def update(self, states):
        # draw background
        self.display_surface.blit(self.background, (0, 0))
        
        # get mouse position
        mouse_position = pygame.mouse.get_pos()
        
        # get mouse click status
        mouse_click = pygame.mouse.get_pressed()
        
        # set sail button
        self.set_sail_button.update(mouse_position)
        if self.set_sail_button.active and mouse_click[0]:
            self.parent_state.switch_state(states['level'])