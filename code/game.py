import sys
import pygame
from settings import *
from level import Level
from town import Town

class Game:
    def __init__(self) -> None:
        
        # game setup
        pygame.init()
        self.game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Pippen')
        
        # setup player user
        self.player = None
        
        # setup the level
        self.level = Level(self.clock)
        self.town = Town(self.clock)
        
        # list of game states
        self.game_states = [self.level, self.town]
        self.game_states = {
            'level' : self.level,
            'town' : self.town,
        }
        
    def run(self) -> None:
        """
        Main game loop.
        """
        while 1:
            # check if the user wants to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            #self.game_window.fill('black')
            
            # run the active game state
            for i in self.game_states.keys():
                if self.game_states[i].active:
                    self.game_states[i].run(self.game_states)
                
            # update the game display
            pygame.display.update()
                
            # wait until end of frame
            self.clock.tick(FPS)
         
if __name__ == '__main__':
    game = Game()
    game.run()